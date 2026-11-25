"""A-033 "Why Do Plane Toilets Still Have Ashtrays?" — standalone Short, Style R, 25 Nov 2026. Slot Fri 1 Jan 2027 18:00 UTC.
python episodes/A-033-plane-ashtray/make.py plan            -> shots.json (timing for the Blender scenes in scene.py)
python episodes/A-033-plane-ashtray/make.py sheet|anim|render|qa [renders_dir]
3D frames come from scene.py (animatic here at low res; finals on Kaggle GPU). This file adds the title (frame 1), a few 2D labels,
corner badge, voice, music and SFX via lib/flat2d.Video. No captions (owner 22 Nov).
"""
import sys, json, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *

RDIR = Path(sys.argv[2]) if len(sys.argv) > 2 else EP / "renders"
import srplate
plate = lambda name: srplate.plate(RDIR, name)


def start_of(name):
    return lambda c: min(sh["start"] for sh in c.V.shots if sh["name"] == name)


def zplate(name, z=(1.16, 1.22), focus=(540, 900)):
    return srplate.plate(RDIR, name, zoom=(z[0], z[1], focus), t0=start_of(name))


def tag(name, items, base=None):
    """Plate + popping labels: items = [(word, text, x, y, size, colour)]."""
    base = base or plate(name)
    def fn(g, c):
        base(g, c)
        with g.screen():
            for wd, txt, x, y, size, col in items:
                try:
                    t0 = c.w(wd) - 0.1
                except KeyError:
                    t0 = 0.15
                k = pop(c.t, t0, 0.32)
                if k > 0:
                    g.text(txt, x, y, size, col, sw=size * 0.2, depth=size * 0.08, sc=k, rot=-0.03)
    return fn


V = Video(EP, title=("WHY AN", "ASHTRAY?"), keys=set(), music="curious")
RED, YEL = "#FF6B5B", PAL["yellow"]

def Z(line, part, name, sfx=(), focus=(540, 900), fn=None, z=(1.16, 1.22)):
    V.shot(line, fn or zplate(name, z=z, focus=focus), part, sfx=list(sfx), name=name + "#z", tr="cut")


def S(line, part, name, sfx=(), fn=None, music=None, tr="punch"):
    V.shot(line, fn or plate(name), part, sfx=list(sfx), name=name, music=music, tr=tr)


S("H1", (0, 1), "hook_door", [(0.0, "chime", 0.45), (0.0, "sting", 0.25), (0.6, "clunk", 0.3)], tr="cut")
S("L01", (0, "yet"), "cabin_sign", [(0.15, "chime", 0.35), (0.6, "chime", 0.25), (0.05, "room_tone", 0.2)],
  fn=tag("cabin_sign", [("2000", "BANNED SINCE 2000", W / 2, 1500, 100, "#FFFFFF")]))
S("L01", ("yet", 1), "ashtray_macro", [("ashtray", "click", 0.45)], fn=tag("ashtray_macro", [("demand", "STILL REQUIRED", W / 2, 430, 110, YEL)]))
S("L02", (0, 1), "cig_fall", [(0.0, "whoosh_soft", 0.35), ("ends", "thud", 0.3)], music="adventure")
S("L03", (0, "nearest"), "bin_flap", [("hides", "creak", 0.4), ("hides", "clunk", 0.35)])
S("L03", ("nearest", 1), "bin_xray", [("bin", "thud", 0.3), ("paper", "hiss", 0.3)], fn=tag("bin_xray", [("paper", "PAPER TOWELS", W / 2, 430, 110, RED)]))
S("L04", (0, 1), "stub_out", [("out", "clunk", 0.5)], music="curious")
S("L05", (0, "and"), "ext_shot", [("extinguisher", "hiss", 0.5)])
S("L05", ("and", 1), "detector", [("detector", "beep3", 0.25)])
S("L06", (0, "it's"), "loop_ots", [(0.1, "hmm", 0.2)])
S("L06", ("it's", 1), "loop_door", [("fire", "chime", 0.3)])
V.build()


def write_plan():
    """One Blender shot per rendered name; zoom cuts (name '<shot>#z') extend the duration of the shot they belong to."""
    def wkeys(L, base, out_d):
        for i, w in enumerate(L["words"]):
            k = "".join(ch for ch in w["w"].lower() if ch.isalnum())
            n = sum(1 for ww in L["words"][:i] if "".join(ch for ch in ww["w"].lower() if ch.isalnum()) == k)
            out_d.setdefault(f"{k}#{n}" if n else k, round(V.voice0[L["id"]] + w["s"] - base, 3))
    out = []
    for sh in V.shots:
        L = V.T[sh["line"]]
        if "#" in sh["name"]:
            prev = out[-1]; prev["dur"] = round(sh["start"] + sh["dur"] - prev["start"], 4); prev["frames"] = int(round(prev["dur"] * FPS))
            wkeys(L, prev["start"], prev["words"]); continue
        words = {}; wkeys(L, sh["start"], words)
        out.append(dict(id=sh["id"], name=sh["name"], line=sh["line"], start=sh["start"], dur=sh["dur"], frames=int(round(sh["dur"] * FPS)), words=words))
    (EP / "shots.json").write_text(json.dumps(dict(fps=FPS, w=W, h=H, duration=V.duration, shots=out), indent=1))
    print(f"{len(out)} shots, {V.duration:.2f} s, {sum(s['frames'] for s in out)} frames")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "plan"
    if cmd == "plan":
        write_plan()
    elif cmd == "sheet":
        V.sheet(str(EP / "animatic/sheet.jpg"), per_shot=1, cols=6, scale=0.16)
    elif cmd == "qa":
        V.qa_numbers()
    elif cmd == "anim":
        V.load_env(); V.mix()
        V.render(str(EP / "animatic/animatic.mp4"), crf=26, preset="veryfast")
    elif cmd == "render":
        V.load_env(); V.mix()
        (EP / "final").mkdir(exist_ok=True)
        V.render(str(EP / "final/A-033.mp4"))
