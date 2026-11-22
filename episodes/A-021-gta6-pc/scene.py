"""A-021 Style R scenes (Blender): "Why can't you play GTA 6 on PC yet?". Renders every shot of shots.json as frames.
/opt/c3d/bin/python -I scene.py <shots.json> <out_dir> [--w 540 --h 960 --samples 12 --step 3 --shots a,b --gpu --part 0/2 --mblur --measure]
Our own cast and props on a studio backdrop in our colours: a PC player at his desk, a console player at his TV, plain game boxes on pedestals.
No game art, logos or characters (text labels are added in 2D by make.py).
"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, os.path.join(HERE, "..", "..", "lib", "style_r"), os.path.join(HERE, "..", "..", "lib")):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
import bpy
from mathutils import Vector
import sr_common as C, sr_props as P, sr_human as Hm
from sr_shot import key_obj, cam_move, W_, life

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]

PCG = dict(macro={"gender": 1, "age": 0.40, "muscle": 0.5, "weight": 0.5, "proportions": 0.6, "height": 0.55}, skin="#E2AE8A",
           hair="#2A170C", shirt="#2E2E3A", trousers="#3A4A66", shoes="#F4F1EA", iris="#4A3A2C", sleeve="long")      # PC player, dark hoodie
CON = dict(macro={"gender": 1, "age": 0.36, "muscle": 0.55, "weight": 0.55, "proportions": 0.6, "height": 0.5}, skin="#B9805A",
           hair="#1A1410", shirt="#FF6B5B", trousers="#2B3440", shoes="#2A2420", iris="#3A2416")                         # console player, coral tee
BOSS = dict(macro={"gender": 1, "age": 0.62, "muscle": 0.45, "weight": 0.6, "proportions": 0.55, "height": 0.5}, skin="#EBC09E",
            hair="#8A8178", shirt="#2F3A4F", trousers="#2F3A4F", shoes="#1A1A1A", iris="#3E5A7A", sleeve="long")         # generic exec in a dark suit
BG = ("#2E5E86", "#F0D2A8")
DESK_H = 0.95


def set_stage(top=BG[0], bottom=BG[1], mid="#E7A07A", y0=8.5, flip=False):
    """flip=True turns the seamless backdrop round (wall on -Y) for cameras that look towards -Y."""
    P.world(top, 0.6); cyc = P.studio(top=top, bottom=bottom, mid=mid, y0=y0, glow=0.55, height=18.0, width=40.0, depth=12.0)
    if flip:
        cyc.rotation_euler = (0, 0, math.pi)
    return cyc


def screen_mat(col, strength):
    return C.pbr("scr_" + col, "#101018", 0.2, emit=col, estr=strength)


def monitor(loc, w=0.62, h=0.36, col="#3A4A7A", strength=2.0, rot_z=0.0):
    root = bpy.data.objects.new("monitor", None); bpy.context.scene.collection.objects.link(root)
    frame = C.rbox("mon_frame", (w + 0.03, 0.03, h + 0.03), (0, 0, 0.20 + h / 2), mat=C.pbr("monblack", "#16161E", 0.35), bevel=0.006)
    scr = C.rbox("mon_screen", (w, 0.006, h), (0, -0.017, 0.20 + h / 2), mat=screen_mat(col, strength), bevel=0.002)
    stand = C.rbox("mon_stand", (0.05, 0.05, 0.20), (0, 0.02, 0.10), mat=C.pbr("monblack", "#16161E", 0.35))
    base = C.rbox("mon_base", (0.24, 0.16, 0.012), (0, 0.02, 0.006), mat=C.pbr("monblack", "#16161E", 0.35))
    for o in (frame, scr, stand, base): o.parent = root
    root.location = loc; root.rotation_euler = (0, 0, rot_z)
    return root, scr


def pc_desk(loc=(0, 0, 0), screen_col="#3A4A7A", strength=2.0):
    x, y, z = loc
    top = C.rbox("desk_top", (1.3, 0.62, 0.04), (x, y, DESK_H), mat=C.pbr("desk", "#2A2A38", 0.5), bevel=0.008)
    for sx in (-0.6, 0.6):
        C.rbox("desk_leg", (0.05, 0.55, DESK_H), (x + sx, y, DESK_H / 2), mat=C.pbr("desk", "#2A2A38", 0.5))
    mon, scr = monitor((x, y + 0.12, DESK_H + 0.02), col=screen_col, strength=strength)
    C.rbox("keyboard", (0.44, 0.14, 0.02), (x, y - 0.12, DESK_H + 0.03), mat=C.pbr("kb", "#1E1E28", 0.45), bevel=0.004)
    C.rbox("tower", (0.2, 0.45, 0.45), (x + 0.48, y + 0.05, DESK_H + 0.245), mat=C.pbr("tower", "#1E1E28", 0.35, emit="#7FD1FF", estr=0.15), bevel=0.01)
    C.area("screenglow", (x, y - 0.05, DESK_H + 0.4), (math.radians(90), 0, 0), 0.5, "#9FB8FF", 60.0)
    return scr


def tv_stand(loc=(0, 0, 0), col="#FFB15B", strength=3.0):
    x, y, z = loc
    C.rbox("tv_cab", (1.4, 0.45, 0.5), (x, y, 0.25), mat=C.pbr("cab", "#5B3B2E", 0.6), bevel=0.01)
    root = bpy.data.objects.new("tv", None); bpy.context.scene.collection.objects.link(root)
    fr = C.rbox("tv_frame", (1.25, 0.05, 0.72), (0, 0, 0.5 + 0.42), mat=C.pbr("tvblack", "#121218", 0.3), bevel=0.01)
    sc = C.rbox("tv_screen", (1.18, 0.01, 0.65), (0, -0.026, 0.5 + 0.42), mat=screen_mat(col, strength), bevel=0.003)
    for o in (fr, sc): o.parent = root
    root.location = (x, y, 0)
    C.area("tvglow", (x, y - 0.6, 1.0), (math.radians(90), 0, 0), 1.0, col, 140.0)
    return sc


def controller(name="pad"):
    m = C.pbr("padmat", "#1E1E28", 0.4)
    body = C.rbox(name, (0.15, 0.06, 0.035), (0, 0, 0), mat=m, bevel=0.012)
    for sx in (-0.06, 0.06):
        g = C.rbox(name + "_grip", (0.04, 0.05, 0.03), (sx, -0.03, -0.005), mat=m, bevel=0.012); g.parent = body
    return body


def person(spec, loc, rot_z, name):
    h = Hm.build(dict(spec, loc=loc, rot_z=rot_z), name); ct = Hm.controls(h)
    return h, ct


def game_box(name, loc, col="#3E7CB1"):
    root = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(root)
    b = C.rbox(name + "_case", (0.19, 0.03, 0.24), (0, 0, 0.12), mat=C.pbr("case_" + col, col, 0.35, coat=0.4), bevel=0.006); b.parent = root
    s = C.rbox(name + "_spine", (0.006, 0.031, 0.24), (-0.095, 0, 0.12), mat=C.pbr("spine", "#F4F1EA", 0.4)); s.parent = root
    root.location = loc
    return root


def pedestal(name, loc, h=0.9, col="#F4F1EA"):
    C.cyl(name, 0.26, h, (loc[0], loc[1], h / 2), mat=C.pbr("ped_" + col, col, 0.35), verts=48, bevel=0.01)
    return Vector((loc[0], loc[1], h))


# ------------------------------------------------------------------ shots
def at_desk(n, screen_col="#3A4A7A", strength=1.4, look0=None):
    """PC player stands at his desk facing the monitor (+Y); camera sits beyond the desk so we see his face lit by the screen.
    He faces +Y, so his right hand is on +X (mouse)."""
    set_stage(flip=True)
    scr = pc_desk((0.35, 0.0, 0), screen_col=screen_col, strength=strength)
    h, ct = person(PCG, (-0.55, -0.45, 0), 180, "man")
    ct["handR"].location = (-0.33, -0.22, DESK_H + 0.07); ct["handL"].location = (-0.78, -0.40, 0.98)
    Hm.grip(h, "R", 0.4, 0.3)
    P.lights((-0.2, -0.2, 1.2), key=700, rim=900)
    return h, ct


MON = (0.35, 0.10, 1.25)
CAMP = (0.62, 1.20, 1.50); CAMT = (-0.50, -0.45, 1.30)


def hook_pc(sh, cam, n):
    """Frame 1: PC player at his desk, big in frame, lit by a dull empty screen; frustrated face, hand on the mouse."""
    h, ct = at_desk(n)
    key_obj(ct["look"], 0, loc=(CAMP[0], CAMP[1], 1.55)); key_obj(ct["look"], int(n * 0.6), loc=MON)
    Hm.face(h["keys"], 0, frown=0.5, brows_inner=0.6, squint=0.3); Hm.face(h["keys"], int(n * 0.6), frown=0.6, brows_down=0.5)
    life(h, n, 1, blinks=False)
    cam_move(cam, n, (CAMP, CAMT, 42), ((0.58, 1.10, 1.50), CAMT, 44), focus=(-0.55, -0.45, 1.5), fstop=4.5)


def console_win(sh, cam, n):
    set_stage(bottom="#F2D2A0", flip=True)
    tv_stand((0.0, 0.6, 0), col="#FFB15B", strength=3.5)
    h, ct = person(CON, (0.0, -0.55, 0), 180, "man")                   # faces the TV (+Y): right hand on +X
    pad = controller(); Hm.hold(h, pad, "R", offset=(0, 0, 0))
    key_obj(ct["handR"], 0, loc=(0.08, -0.35, 1.05)); key_obj(ct["handL"], 0, loc=(-0.08, -0.35, 1.05))
    fu = W_(sh, "playstation", 2.0)
    key_obj(ct["handR"], fu, loc=(0.08, -0.35, 1.05)); key_obj(ct["handR"], fu + 8, loc=(0.25, -0.5, 1.75))
    key_obj(ct["handL"], fu, loc=(-0.08, -0.35, 1.05)); key_obj(ct["handL"], fu + 8, loc=(-0.25, -0.5, 1.75))
    key_obj(ct["look"], 0, loc=(0, 0.6, 1.0)); key_obj(ct["look"], fu + 8, loc=(0, 0.6, 1.4))
    Hm.face(h["keys"], 0, smile=0.4, brows_up=0.3); Hm.face(h["keys"], fu + 8, smile=0.9, wide=0.3, brows_up=0.6)
    P.lights((0, 0.0, 1.0), key=700, rim=1000)
    cam_move(cam, n, ((1.35, 0.95, 1.35), (0.0, -0.55, 1.30), 30), ((1.25, 0.85, 1.36), (0.0, -0.55, 1.32), 32), fstop=5.6)


def pc_nothing(sh, cam, n):
    """Close on the PC player's face in the blue light of an empty screen."""
    h, ct = at_desk(n, screen_col="#2A3050", strength=1.0)
    key_obj(ct["look"], 0, loc=MON)
    fn = W_(sh, "nothing", 1.0)
    Hm.face(h["keys"], 0, brows_up=0.4, wide=0.3); Hm.face(h["keys"], fn + 4, frown=0.7, brows_inner=0.8, squint=0.2)
    ec = Vector((-0.55, -0.38, 1.60))                 # face (he faces +Y; rest-pose eye data is not rotated)
    cam_move(cam, n, ((-0.12, 0.42, 1.64), (ec.x, ec.y, ec.z - 0.07), 48), ((-0.14, 0.36, 1.64), (ec.x, ec.y, ec.z - 0.07), 52),
             focus=ec, fstop=3.5)


def shrug_pc(sh, cam, n):
    set_stage()
    pc_desk((0.6, 0.2, 0), screen_col="#2A3050", strength=1.0)
    h, ct = person(PCG, (0.0, -0.3, 0), 0, "man")
    key_obj(ct["handR"], 0, loc=(-0.22, -0.38, 0.92)); key_obj(ct["handR"], 10, loc=(-0.36, -0.50, 1.08))
    key_obj(ct["handL"], 0, loc=(0.22, -0.38, 0.92)); key_obj(ct["handL"], 10, loc=(0.36, -0.50, 1.08))
    key_obj(ct["look"], 0, loc=(0, -1.6, 1.6))
    Hm.face(h["keys"], 0, browL_up=0.6, smile=0.15); Hm.face(h["keys"], 10, brows_up=0.7, smile=0.3)
    P.lights((0, -0.3, 1.2), key=900, rim=900)
    cam_move(cam, n, ((0.15, -2.0, 1.35), (0.05, -0.3, 1.15), 32), ((0.12, -1.85, 1.36), (0.05, -0.3, 1.16), 34), fstop=5.6)


def _pedestals(cam, n, sh, w1, w2, colA="#3E7CB1", colB="#5ED3B5"):
    set_stage(bottom="#F0D2A8")
    ta = pedestal("pedA", (-0.35, 0.3, 0), 0.6); tb = pedestal("pedB", (0.55, 0.3, 0), 0.6, col="#FFE3B8")
    a = game_box("boxA", ta + Vector((0, 0, 0)), colA); b = game_box("boxB", tb + Vector((0, 0, 0)), colB)
    fa, fb = W_(sh, w1, 0.5), W_(sh, w2, 2.0)
    key_obj(a, 0, scale=0.0); key_obj(a, max(1, fa - 4), scale=0.0); key_obj(a, fa + 4, scale=2.6); key_obj(a, fa + 8, scale=2.3, rot=(0, 0, 0))
    key_obj(a, n, rot=(0, 0, math.radians(25)))
    key_obj(b, 0, scale=0.0); key_obj(b, max(1, fb - 4), scale=0.0); key_obj(b, fb + 4, scale=2.6); key_obj(b, fb + 8, scale=2.3, rot=(0, 0, 0))
    key_obj(b, n, rot=(0, 0, math.radians(-25)))
    h, ct = person(PCG, (-1.05, -0.15, 0), 25, "man")
    ct["handR"].location = (-1.25, -0.35, 0.92)
    key_obj(ct["handL"], 0, loc=(-0.85, -0.35, 0.92)); key_obj(ct["handL"], max(2, fb), loc=(-0.60, -0.25, 1.25))
    key_obj(ct["look"], 0, loc=(-0.35, 0.3, 1.0)); key_obj(ct["look"], max(2, fb), loc=(0.55, 0.3, 1.0))
    Hm.face(h["keys"], 0, brows_up=0.3); Hm.face(h["keys"], max(2, fb), frown=0.4, brows_inner=0.5)
    P.lights((0, 0.0, 1.0), key=1000, rim=900, scale=1.2)
    cam_move(cam, n, ((-0.25, -2.15, 1.15), (-0.2, 0.1, 0.95), 30), ((-0.25, -2.0, 1.16), (-0.2, 0.1, 0.96), 31), fstop=8)


def pedestals_a(sh, cam, n):
    _pedestals(cam, n, sh, "2013", "2015")


def pedestals_b(sh, cam, n):
    _pedestals(cam, n, sh, "2018", "later", colA="#8E2430", colB="#C9A23A")


def boss(sh, cam, n):
    """A generic company boss (not a real likeness) at a lectern, points: console first."""
    set_stage(top="#3A6E9A")
    C.rbox("lectern", (0.55, 0.4, 1.05), (0, -0.15, 0.525), mat=C.pbr("lect", "#2F3A4F", 0.4), bevel=0.02)
    tv_stand((-0.95, 0.7, 0), col="#FFB15B", strength=3.0)
    h, ct = person(BOSS, (0, 0.15, 0), 0, "man")
    ct["handL"].location = (0.18, -0.20, 1.08)
    fc = W_(sh, "console", 1.0)
    key_obj(ct["handR"], 0, loc=(-0.18, -0.20, 1.08)); key_obj(ct["handR"], max(1, fc - 2), loc=(-0.18, -0.20, 1.08)); key_obj(ct["handR"], fc + 8, loc=(-0.58, -0.10, 1.42))
    key_obj(ct["look"], 0, loc=(0, -1.8, 1.6)); key_obj(ct["look"], fc + 8, loc=(-0.95, 0.5, 1.1)); key_obj(ct["look"], n, loc=(-0.2, -1.8, 1.6))
    Hm.face(h["keys"], 0, smile=0.2, brows_up=0.2); Hm.face(h["keys"], fc + 8, smile=0.35)
    life(h, n, 3)
    P.lights((0, 0.0, 1.3), key=900, rim=900)
    cam_move(cam, n, ((0.40, -1.75, 1.5), (-0.1, 0.1, 1.35), 44), ((0.36, -1.62, 1.5), (-0.1, 0.1, 1.37), 47), fstop=5.6)


def report_2027(sh, cam, n):
    h, ct = at_desk(n, screen_col="#5ED3B5", strength=1.6)
    C.rbox("calendar", (0.5, 0.02, 0.6), (-1.15, 0.45, 1.45), mat=C.pbr("cal", "#FFF4E0", 0.6), bevel=0.01)
    C.rbox("calband", (0.5, 0.025, 0.14), (-1.15, 0.44, 1.68), mat=C.pbr("calband", "#FF6B5B", 0.5), bevel=0.005)
    fo = W_(sh, "official", 3.0)
    key_obj(ct["look"], 0, loc=(-1.15, 0.45, 1.45)); key_obj(ct["look"], max(2, fo), loc=(CAMP[0], CAMP[1], 1.55))
    key_obj(ct["handL"], 0, loc=(-0.78, -0.40, 0.98)); key_obj(ct["handL"], 10, loc=(-1.0, 0.05, 1.40)); key_obj(ct["handL"], max(12, fo), loc=(-0.78, -0.40, 0.98))
    Hm.face(h["keys"], 0, brows_up=0.5, smile=0.3); Hm.face(h["keys"], max(2, fo), frown=0.4, brows_inner=0.5, smile=0.0)
    cam_move(cam, n, ((0.30, 1.25, 1.55), (-0.80, -0.20, 1.40), 30), ((0.26, 1.15, 1.55), (-0.80, -0.20, 1.41), 32), fstop=5.6)


def loop_q(sh, cam, n):
    """Ends on hook_pc's opening frame so the Short loops; he turns to us: 'Are you still waiting?'."""
    h, ct = at_desk(n)
    key_obj(ct["look"], 0, loc=MON); key_obj(ct["look"], int(n * 0.4), loc=(CAMP[0], CAMP[1], 1.55))
    Hm.face(h["keys"], 0, frown=0.3, brows_inner=0.4); Hm.face(h["keys"], int(n * 0.5), browL_up=0.9, smile=0.25, squint=0.2)
    life(h, n, 6)
    cam_move(cam, n, ((0.56, 1.05, 1.50), CAMT, 45), (CAMP, CAMT, 42), focus=(-0.55, -0.45, 1.5), fstop=4.5)


SHOTS = {f.__name__: f for f in (hook_pc, console_win, pc_nothing, shrug_pc, pedestals_a, pedestals_b, boss, report_2027, loop_q)}


if __name__ == "__main__":
    from sr_shot import run
    run(SHOTS, argv)
