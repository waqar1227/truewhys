"""A-018 Style R scenes (Blender). Renders every shot of shots.json as PNG frames.
/opt/c3d/bin/python -I scene.py <shots.json> <out_dir> [--w 540 --h 960 --samples 12 --step 3 --shots a,b --gpu --part 0/2 --mblur --measure]
Kaggle: blender -b --python scene.py -- <same args>. Needs MPFB 2.0.18 installed (docs/audit/style_r/install_mpfb.py).
Every shot: studio backdrop in our colours (navy -> warm sand), one hero prop (the wavy brick wall), the gardener moves (IK hands, head look,
expression keys, blinks). Original staging (TrueWhys); only the topic is shared with the Short that inspired it.
"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, os.path.join(HERE, "..", "..", "lib", "style_r"), os.path.join(HERE, "..", "..", "lib")):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
import bpy
from mathutils import Vector
import sr_common as C, sr_props as P, sr_human as Hm, sr_walls as Wl
from sr_shot import key_obj, cam_move, W_, puffs_rise, life

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]

GARD = dict(macro={"gender": 1, "age": 0.62, "muscle": 0.5, "weight": 0.55, "proportions": 0.55, "height": 0.5}, skin="#E2AE8A",
            hair="#8A8178", shirt="#3F6E8C", trousers="#5A4A36", shoes="#3A2A20", iris="#4A6A5C", sleeve="long")
AMP, WAVE, HT = 0.32, 2.4, 1.40
BG = ("#14213D", "#E7C9A0")


def set_stage(top=BG[0], bottom=BG[1], mid=None, y0=8.5):
    P.world(top, 0.3); P.studio(top=top, bottom=bottom, mid=mid, y0=y0)


def side_wall(x0=0.45, y0=0.0, L=9.0):
    """Wavy wall running away from the camera (along +Y) at x = x0. Returns (root, point(y_local) -> world centre line point)."""
    w = Wl.wavy_wall("wall", (x0, y0 + L / 2 - 1.0, 0), L=L, height=HT, amp=AMP, wave=WAVE, rot_z=math.radians(90))
    def pt(t):                                   # t = distance along the wall from its near end
        xl = -L / 2 + t
        return Vector((x0 - AMP * math.sin(2 * math.pi * xl / WAVE), y0 - 1.0 + t, 0))
    return w, pt


def gardener(loc, rot_z=0.0, name="man"):
    h = Hm.build(dict(GARD, loc=loc, rot_z=rot_z), name); ct = Hm.controls(h)
    return h, ct


def wall_top(p):
    return Vector((p.x, p.y, HT + 0.09))


# ------------------------------------------------------------------ shots
def hook_wall(sh, cam, n):
    """Frame 1: gardener in front, left hand on the crest of the wavy wall that snakes away behind him; suspicious face."""
    set_stage()
    w, pt = side_wall(0.42, 0.0)
    h, ct = gardener((0.12, 0.05, 0), rot_z=-12)
    hp = Vector((pt(1.05).x - 0.02, pt(1.05).y, HT + 0.06))
    ct["handL"].location = hp; Hm.grip(h, "L", 0.25, 0.2)
    ct["handR"].location = (-0.22, -0.02, 0.98)
    key_obj(ct["look"], 0, loc=(-0.5, -1.6, 1.55)); key_obj(ct["look"], int(n * 0.55), loc=(0.9, 0.6, 1.35)); key_obj(ct["look"], n, loc=(0.8, 0.9, 1.3))   # eyes us, then glances at the wall
    Hm.face(h["keys"], 0, squint=0.55, browL_up=0.8, sneer=0.2); Hm.face(h["keys"], int(n * 0.6), squint=0.6, browL_up=0.9, frown=0.2)
    life(h, n, 1, blinks=False)
    P.lights((0.2, 0.4, 1.2), key=900, rim=900)
    ec = h["eye_c"]
    cam_move(cam, n, ((-0.72, -1.02, 1.42), (0.35, 0.9, 1.02), 26), ((-0.68, -0.96, 1.43), (0.35, 0.9, 1.04), 27), focus=(0, 0.05, 1.5), fstop=5.6)


def aerial_snake(sh, cam, n):
    set_stage(y0=8.0)
    Wl.wavy_wall("wall", (0, 1.0, 0), L=12.0, height=HT, amp=AMP, wave=WAVE)
    h, ct = gardener((-1.2, 0.35, 0), rot_z=0)
    Hm.face(h["keys"], 0, brows_up=0.3)
    P.lights((0, 1.0, 1.0), key=1400, rim=900, scale=1.6)
    cam_move(cam, n, ((-2.6, -2.2, 6.2), (0.2, 1.0, 0.4), 30), ((-1.8, -2.0, 5.6), (0.8, 1.0, 0.4), 30), fstop=11)


def push_test(sh, cam, n):
    """Gardener shoves the one-brick wall with both hands: it does not move. Camera sees the thin crest."""
    set_stage()
    w, pt = side_wall(0.50, 0.0)
    h, ct = gardener((0.0, 0.10, 0), rot_z=78)
    fp = W_(sh, "fall", 2.2)
    a = pt(1.10); b = pt(1.35)
    for f, lean, push in ((0, 0.0, 0.0), (int(n * 0.25), 0.0, 0.0), (int(n * 0.40), 0.05, 1.0), (fp, 0.06, 1.0), (n, 0.02, 0.4)):
        key_obj(ct["handL"], f, loc=(a.x - 0.10 + 0.03 * push, a.y, 1.18))
        key_obj(ct["handR"], f, loc=(b.x - 0.10 + 0.03 * push, b.y, 1.12))
        key_obj(h["rig"], f, loc=(lean, 0.10, 0))
    key_obj(ct["look"], 0, loc=(1.0, 0.4, 1.3)); key_obj(ct["look"], fp, loc=(-0.4, -1.4, 1.5))
    Hm.face(h["keys"], 0, frown=0.3, brows_down=0.4); Hm.face(h["keys"], int(n * 0.45), squint=0.7, frown=0.6, brows_down=0.7)
    Hm.face(h["keys"], fp + 6, browL_up=0.8, smile=0.2, squint=0.1, frown=0.0, brows_down=0.0)
    P.lights((0.4, 0.4, 1.2), key=900, rim=900)
    cam_move(cam, n, ((-0.75, -1.25, 1.75), (0.45, 0.6, 1.25), 30), ((-0.65, -1.05, 1.80), (0.48, 0.6, 1.30), 34), focus=(0.45, 0.6, 1.4), fstop=5.6)


def thin_topple(sh, cam, n):
    """A straight wall only one brick thick wobbles in the wind and falls flat."""
    set_stage(bottom="#D9C3A5")
    wl = Wl.straight_wall("thin", (0, 0.4, 0), L=2.6, height=HT, thick=1)
    fo = W_(sh, "over", 1.3)
    key_obj(wl, 0, rot=(0, 0, 0)); key_obj(wl, max(1, fo - 22), rot=(math.radians(-2.5), 0, 0)); key_obj(wl, max(2, fo - 14), rot=(math.radians(3), 0, 0))
    key_obj(wl, fo, rot=(math.radians(88), 0, 0)); key_obj(wl, fo + 3, rot=(math.radians(84), 0, 0)); key_obj(wl, fo + 6, rot=(math.radians(89), 0, 0))
    gp = P.gas_puffs((-1.6, -0.2, 0.8), n=40, spread=0.25, size=0.04, color="#F4F1EA")
    for i, p in enumerate(gp):                    # wind gusts streaming from the left
        ph = (i * 0.137) % 1.0
        for f in range(0, n + 1, 2):
            u = (f / 30.0 * 0.9 + ph) % 1.0
            key_obj(p, f, loc=(-2.0 + 4.0 * u, -0.1 + 0.5 * math.sin(i), 0.4 + 1.2 * ((i * 0.37) % 1.0)), scale=0.6 * math.sin(math.pi * u))
    dust = P.gas_puffs((0, -0.9, 0.05), n=30, spread=0.5, size=0.05, color="#D9C3A5")
    puffs_rise(dust, n, Vector((0, -0.8, 0.03)), 0.5, t0=fo, speed=1.0, spread=0.6)
    P.lights((0, 0.0, 0.8), key=1000, rim=900, scale=1.2)
    cam_move(cam, n, ((2.3, -3.0, 1.2), (0.0, 0.0, 0.7), 32), ((2.0, -2.7, 1.1), (0.0, -0.2, 0.6), 32), fstop=8)


def thick_pillars(sh, cam, n):
    """To stand, a straight wall needs two bricks of thickness plus pillars: it rises, then the pillars pop in."""
    set_stage(bottom="#D9C3A5")
    wl = Wl.straight_wall("thick", (0, 0.4, 0), L=3.0, height=HT, thick=2, piers=3)
    fp = W_(sh, "pillars", 2.4); ft = W_(sh, "two", 1.0)
    kids = [o for o in wl.children if "pier" in o.name]
    body = [o for o in wl.children if "pier" not in o.name]
    for o in body:
        key_obj(o, 0, scale=(1, 1, 0.02)); key_obj(o, max(2, ft), scale=(1, 1, 1.0))
    for i, o in enumerate(kids):
        f0 = fp - 4 + i * 4
        key_obj(o, 0, scale=(0, 0, 0)); key_obj(o, max(1, f0), scale=(0, 0, 0)); key_obj(o, f0 + 6, scale=(1.15, 1.15, 1.05)); key_obj(o, f0 + 9, scale=(1, 1, 1))
    P.lights((0, 0.3, 0.8), key=1000, rim=900, scale=1.2)
    cam_move(cam, n, ((-2.2, -2.6, 1.6), (0.0, 0.3, 0.7), 32), None, orbit=18, fstop=8)


def brace_top(sh, cam, n):
    """Top view of the wavy wall: glowing arrows show each curve leaning on the next."""
    set_stage(bottom="#E7C9A0", y0=6.0)
    Wl.wavy_wall("wall", (0, 0.3, 0), L=6.0, height=HT, amp=AMP, wave=WAVE)
    fb = W_(sh, "braces", 1.2)
    xs = [-WAVE * 0.75, -WAVE * 0.25, WAVE * 0.25, WAVE * 0.75]
    for i, x in enumerate(xs):
        y = 0.3 + AMP * math.sin(2 * math.pi * x / WAVE)
        sd = 1 if math.sin(2 * math.pi * x / WAVE) > 0 else -1          # arrow on the convex side, pointing into the bend
        a = Wl.arrow3d(f"ar{i}", (x, y + sd * 0.55, HT + 0.15), (x, y + sd * 0.12, HT + 0.15), r=0.03)
        f0 = fb - 6 + i * 5
        key_obj(a, 0, scale=0.0); key_obj(a, max(1, f0), scale=0.0); key_obj(a, f0 + 6, scale=1.2); key_obj(a, f0 + 9, scale=1.0)
    P.lights((0, 0.3, 1.0), key=1100, rim=900, scale=1.4)
    cam_move(cam, n, ((0.0, -1.2, 4.6), (0.0, 0.35, 0.8), 30), ((0.25, -1.0, 4.3), (0.15, 0.35, 0.8), 30), fstop=11)


def paper_demo(sh, cam, n):
    """On a table: a flat sheet stood on its edge falls over; the same sheet folded into a zigzag stands."""
    set_stage(bottom="#E7C9A0")
    P.counter((0, 0.0, 0), w=1.2, d=0.6, top="#F1E8DA", top2="#E6D8C4")
    top = 0.92
    flat = Wl.paper_sheet("flat", (-0.18, -0.02, top), zigzag=False, rot_z=0)
    zz = Wl.paper_sheet("zig", (0.18, -0.02, top), zigzag=True, folds=6, angle=40, rot_z=math.radians(-30))
    fp = W_(sh, "paper", 0.6)
    key_obj(flat, 0, rot=(0, 0, 0)); key_obj(flat, fp + 2, rot=(math.radians(-4), 0, 0)); key_obj(flat, fp + 14, rot=(math.radians(-90), 0, 0))
    key_obj(zz, 0, scale=(0.4, 1, 1)); key_obj(zz, fp + 10, scale=(0.4, 1, 1)); key_obj(zz, fp + 22, scale=(1, 1, 1))
    P.lights((0, -0.05, top + 0.2), key=650, rim=700, scale=0.7)
    cam_move(cam, n, ((0.05, -0.95, top + 0.62), (0.03, 0.0, top + 0.08), 45), ((0.10, -0.88, top + 0.58), (0.05, 0.0, top + 0.08), 48),
             focus=(0.1, -0.02, top + 0.1), fstop=4)


def sun_pockets(sh, cam, n):
    """The sun swings over; the hollows of the curves glow warm and the fruit trees in them ripen. The gardener picks one."""
    set_stage(top="#1F3A68", bottom="#F2D2A0", y0=4.0)
    Wl.wavy_wall("wall", (0, 0.5, 0), L=7.0, height=HT, amp=AMP, wave=WAVE)
    pockets = [x for x in (-WAVE * 0.75, WAVE * 0.25, WAVE * 1.25)]
    for i, x in enumerate(pockets):
        y = 0.5 + AMP - 0.16
        Wl.fruit_tree(f"tree{i}", (x, y, 0), s=1.0, seed=3 + i)
        g = C.area(f"warm{i}", (x, y - 0.45, 0.9), (math.radians(80), 0, 0), 0.9, "#FF9A3C", 0.0)
        g.data.energy = 0.0; g.data.keyframe_insert("energy", frame=0)
        g.data.energy = 0.0; g.data.keyframe_insert("energy", frame=10 + i * 8)
        g.data.energy = 260.0; g.data.keyframe_insert("energy", frame=34 + i * 8)
    sun = Wl.sun_disc((-3.0, -2.5, 3.2), r=0.35, strength=10.0)
    key_obj(sun, 0, loc=(-3.2, -2.0, 2.4)); key_obj(sun, n, loc=(-1.0, -2.4, 3.6))
    h, ct = gardener((WAVE * 0.25 - 0.62, 0.25, 0), rot_z=20)
    ff = W_(sh, "fruit", 3.0)
    fruit = Vector((WAVE * 0.25 - 0.32, 0.5 + AMP - 0.24, 0.95))
    key_obj(ct["handR"], 0, loc=(-0.25 + WAVE * 0.25 - 0.62, 0.25, 0.95)); key_obj(ct["handR"], max(1, ff - 8), loc=fruit + Vector((-0.04, -0.03, 0)))
    key_obj(ct["handR"], ff + 10, loc=fruit + Vector((-0.20, -0.25, 0.25)))
    key_obj(ct["look"], 0, loc=(fruit.x, fruit.y, fruit.z + 0.2)); key_obj(ct["look"], ff + 10, loc=(fruit.x - 0.5, -1.5, 1.6))
    Hm.face(h["keys"], 0, brows_up=0.3, smile=0.2); Hm.face(h["keys"], ff + 10, smile=0.7, brows_up=0.5)
    life(h, n, 2)
    P.lights((0, 0.4, 1.0), key=700, rim=900, scale=1.3)
    cam_move(cam, n, ((-0.6, -2.3, 1.35), (0.3, 0.5, 1.0), 32), ((-0.45, -2.0, 1.30), (0.3, 0.5, 1.0), 34), focus=(0.0, 0.3, 1.2), fstop=5.6)


def brick_pile(name, loc, n_layers, per_layer=6, seed=4):
    mats = Wl.brick_mats(); rnd = random.Random(seed); out = []
    for k in range(n_layers):
        for i in range(per_layer):
            ox = (i % 3) * (Wl.BL + 0.01) - Wl.BL; oy = (i // 3) * (Wl.BW + 0.01)
            rot = math.radians(90) if k % 2 else 0
            b = C.rbox(f"{name}_{k}_{i}", (Wl.BL, Wl.BW, Wl.BH), (0, 0, 0), mat=mats[rnd.randrange(len(mats))], bevel=0.004)
            b.location = Vector(loc) + Vector((ox if not rot else oy - 0.1, oy if not rot else ox, Wl.BH / 2 + k * (Wl.BH + 0.002)))
            b.rotation_euler = (0, 0, rot + rnd.uniform(-0.03, 0.03)); out.append(b)
    root = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(root); root.location = (0, 0, 0)
    for b in out: b.parent = root
    return root


def brick_count(sh, cam, n):
    """Side by side: wavy one-brick wall (left) and straight two-brick wall with pillars (right); brick piles show the totals."""
    set_stage(bottom="#E7C9A0", y0=5.0)
    Wl.wavy_wall("wavy", (-1.25, 0.8, 0), L=2.4, height=HT, amp=AMP, wave=WAVE)
    Wl.straight_wall("thick", (1.25, 0.8, 0), L=2.4, height=HT, thick=2, piers=2)
    small = brick_pile("pileA", (-1.25, -0.4, 0), 4); big = brick_pile("pileB", (1.25, -0.4, 0), 11)
    ff = W_(sh, "fewer", 2.0)
    for pile, f0 in ((small, ff - 10), (big, ff - 16)):
        key_obj(pile, 0, scale=(0, 0, 0)); key_obj(pile, max(1, f0), scale=(0, 0, 0)); key_obj(pile, f0 + 8, scale=(1, 1, 1.0))
    P.lights((0, 0.4, 0.8), key=1100, rim=900, scale=1.5)
    cam_move(cam, n, ((0.0, -4.4, 2.6), (0.0, 0.4, 0.6), 30), ((0.0, -4.0, 2.4), (0.0, 0.4, 0.6), 31), fstop=11)


def loop_q(sh, cam, n):
    """Ends on hook_wall's opening frame so the Short loops; the gardener raises an eyebrow: 'Agree?'."""
    set_stage()
    w, pt = side_wall(0.42, 0.0)
    h, ct = gardener((0.12, 0.05, 0), rot_z=-12)
    ct["handL"].location = Vector((pt(1.05).x - 0.02, pt(1.05).y, HT + 0.06)); Hm.grip(h, "L", 0.25, 0.2)
    key_obj(ct["handR"], 0, loc=(-0.22, -0.02, 0.98)); key_obj(ct["handR"], int(n * 0.5), loc=(-0.20, -0.12, 1.12))
    key_obj(ct["look"], 0, loc=(-0.3, -1.6, 1.5))
    Hm.face(h["keys"], 0, smile=0.3, browL_up=0.4); Hm.face(h["keys"], int(n * 0.5), browL_up=0.9, smile=0.45, squint=0.2)
    life(h, n, 6)
    P.lights((0.2, 0.4, 1.2), key=900, rim=900)
    cam_move(cam, n, ((-0.64, -0.92, 1.44), (0.35, 0.9, 1.06), 28), ((-0.72, -1.02, 1.42), (0.35, 0.9, 1.02), 26), focus=(0, 0.05, 1.5), fstop=5.6)


SHOTS = {f.__name__: f for f in (hook_wall, aerial_snake, push_test, thin_topple, thick_pillars, brace_top, paper_demo, sun_pockets, brick_count, loop_q)}


if __name__ == "__main__":
    from sr_shot import run
    run(SHOTS, argv)
