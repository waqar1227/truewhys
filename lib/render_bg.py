"""Render background plates for shots (Blender, Cycles).

python lib/render_bg.py <shots.json> <out_dir> --w 1920 --h 1080 --samples 96 [--gpu] [--step 1]
    [--shots S001,S002] [--chapters 0,1] [--stills]
For every shot: builds its set (cached between shots on the same set), animates the camera exactly
as lib/camera.py describes, renders frames and encodes <out_dir>/<shot>.mp4 (30 fps, near-lossless).
Static shots render one frame. --stills renders only the first frame of each shot (contact sheets).
"""
import sys, os, json, math, argparse, subprocess, shutil, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import sets, camera
try:
    import sets2  # more sets (B-002+), registers into sets.BUILDERS
except ImportError:
    pass

ap = argparse.ArgumentParser()
ap.add_argument("shots"); ap.add_argument("out")
ap.add_argument("--w", type=int, default=1920); ap.add_argument("--h", type=int, default=1080)
ap.add_argument("--samples", type=int, default=96); ap.add_argument("--gpu", action="store_true")
ap.add_argument("--step", type=int, default=1); ap.add_argument("--interp", action="store_true", help="with --step 2: interpolate in-betweens"); ap.add_argument("--shots_only", default="")
ap.add_argument("--chapters", default=""); ap.add_argument("--thr", type=float, default=0.02); ap.add_argument("--stills", action="store_true")
ap.add_argument("--deadline", type=float, default=0, help="stop starting new shots after N seconds")
ap.add_argument("--part", default="0/1", help="i/n: render every n-th shot starting at i (multi-GPU)")
a = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])

plan = json.load(open(a.shots))
FPS = plan.get("fps", 30)
os.makedirs(a.out, exist_ok=True)
want = set(a.shots_only.split(",")) if a.shots_only else None
chs = set(int(c) for c in a.chapters.split(",")) if a.chapters else None
pi, pn = (int(x) for x in a.part.split("/"))

todo = [s for s in plan["shots"] if s.get("set") and (not want or s["id"] in want) and (chs is None or s.get("chapter") in chs)]
todo = todo[pi::pn]
cur = None
T_START = time.time()
log = open(os.path.join(a.out, f"render_log_{pi}.txt"), "a")
for s in todo:
    if a.deadline and time.time() - T_START > a.deadline:
        print("deadline reached, stopping", flush=True); break
    out_mp4 = os.path.join(a.out, s["id"] + (".png" if a.stills else ".mp4"))
    if os.path.exists(out_mp4):
        continue
    key = (s["set"], s.get("variant", "day"))
    if key != cur:
        cam_obj = sets.build(*key)
        sets.setup_render(a.w, a.h, a.samples, a.gpu)
        bpy.context.scene.cycles.adaptive_threshold = a.thr
        cur = key
    cam_obj = bpy.context.scene.camera
    cam = s["cam"]
    nfr = max(1, int(round(s["dur"] * FPS)))
    static = cam.get("to") is None and not cam.get("orbit") and not cam.get("shake")
    step = a.step
    if a.interp and not static:  # interpolation only where it is invisible: slow, smooth moves, no orbit/shake
        c0, c1 = camera.cam_at(cam, 0), camera.cam_at(cam, 1)
        mv = math.dist(c0[0], c1[0]) + math.dist(c0[1], c1[1]) * 0.5 + abs(c0[2] - c1[2]) * 0.05
        if cam.get("orbit") or cam.get("shake") or mv / max(s["dur"], 0.1) > 0.6:
            step = 1
    frames = [0] if (static or a.stills) else list(range(0, nfr, step))
    tmp = os.path.join(a.out, "_tmp_" + s["id"])
    os.makedirs(tmp, exist_ok=True)
    t0 = time.time()
    dof = cam.get("dof")
    for fi in frames:
        t = fi / max(1, nfr - 1)
        pos, tgt, lens = camera.cam_at(cam, t)
        if cam.get("shake"):
            amp = cam["shake"]
            pos = [pos[0] + amp * math.sin(fi * 0.9), pos[1], pos[2] + amp * math.cos(fi * 1.3)]
        cam_obj.location = pos
        d = Vector(tgt) - Vector(pos)
        cam_obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        cam_obj.data.lens = lens
        if dof:
            cam_obj.data.dof.use_dof = True
            cam_obj.data.dof.focus_distance = d.length if dof.get("focus") is None else dof["focus"]
            cam_obj.data.dof.aperture_fstop = dof.get("fstop", 2.8)
        else:
            cam_obj.data.dof.use_dof = False
        bpy.context.scene.render.filepath = os.path.join(tmp, f"f{fi:05d}.png")
        bpy.ops.render.render(write_still=True)
    if a.stills:
        shutil.move(os.path.join(tmp, "f00000.png"), out_mp4)
    elif step > 1 and a.interp and len(frames) > 2:
        # in-between frames by motion-compensated interpolation (static set + smooth camera: clean result)
        lst = sorted(os.listdir(tmp))
        seq = os.path.join(tmp, "seq"); os.makedirs(seq, exist_ok=True)
        for k, n in enumerate(lst):
            os.link(os.path.join(tmp, n), os.path.join(seq, f"{k:05d}.png"))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", f"{FPS}/{step}", "-i", os.path.join(seq, "%05d.png"),
                        "-vf", f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,tpad=stop_mode=clone:stop_duration=1",
                        "-frames:v", str(nfr), "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", out_mp4], check=True)
    else:
        # fill skipped frames by holding (only used for low-res animatics with --step>1)
        lst = sorted(os.listdir(tmp))
        have = {int(n[1:6]): n for n in lst}
        seq = os.path.join(tmp, "seq"); os.makedirs(seq, exist_ok=True)
        last = have[0]
        for fi in range(nfr):
            last = have.get(fi, last)
            os.link(os.path.join(tmp, last), os.path.join(seq, f"{fi:05d}.png"))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(seq, "%05d.png"),
                        "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", out_mp4], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    msg = f"{s['id']} set={key} frames={len(frames)} sec={time.time()-t0:.1f}"
    print(msg, flush=True); log.write(msg + "\n"); log.flush()
