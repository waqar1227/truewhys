"""A-024 Style R scenes (Blender): "Why is there a metal net in your microwave door?". Renders every shot of shots.json as frames.
/opt/c3d/bin/python -I scene.py <shots.json> <out_dir> [--w 540 --h 960 --samples 12 --step 3 --shots a,b --gpu --part 0/2 --mblur --measure]
Our own generic over-the-range microwave (no brand), a perforated-metal door screen (real holes via a procedural cut-out material:
3 mm holes on a 4.5 mm staggered pitch), glowing microwave waves (12 cm wavelength) and light rays, our MPFB cast, a simple kitchen.
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

COOK = dict(macro={"gender": 1, "age": 0.45, "muscle": 0.5, "weight": 0.55, "proportions": 0.55, "height": 0.5}, skin="#9A6646",
            hair="#151010", shirt="#C98A2E", trousers="#2E3B52", shoes="#2A1A10", iris="#2E1E12", sleeve="long",
            shirt_push=0.026, shirt_iters=45, tuck=0.035)                                  # home cook, mustard long-sleeve top (loose)
PITCH, HOLE_R = 0.0045, 0.0015                    # door screen: 3 mm holes, 4.5 mm staggered pitch (patent rule: far below 1/10 of 12 cm)
WAVE_L = 0.122                                    # 2.45 GHz microwave wavelength (m)
MICRO, LIGHT, MESH = "#57C8FF", "#FFE08A", "#1A1C20"
DOOR_Y = -0.36                                    # door front plane (person at origin faces -Y, towards the microwave)
WIN_W, WIN_H = 0.32, 0.19


# ------------------------------------------------------------------ materials
def screen_mat(name="screen", col=MESH, pitch=PITCH, r=HOLE_R):
    """Perforated metal sheet: object-space XZ hole pattern (staggered rows); holes are fully transparent."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    tc = N("ShaderNodeTexCoord"); sp = N("ShaderNodeSeparateXYZ"); L(tc.outputs["Object"], sp.inputs[0])

    def math_(op, a, b=None, val=None):
        n = N("ShaderNodeMath"); n.operation = op
        L(a, n.inputs[0]) if not isinstance(a, (int, float)) else n.inputs[0].__setattr__("default_value", a)
        if b is not None:
            L(b, n.inputs[1]) if not isinstance(b, (int, float)) else n.inputs[1].__setattr__("default_value", b)
        return n.outputs[0]
    zr = math_("DIVIDE", sp.outputs["Z"], pitch * 0.866)                 # row index (hex rows 0.866 * pitch apart)
    row = math_("FLOOR", zr)
    odd = math_("MULTIPLY", math_("FLOORED_MODULO", row, 2.0), 0.5)
    xu = math_("ADD", math_("DIVIDE", sp.outputs["X"], pitch), odd)
    fx = math_("SUBTRACT", math_("FRACT", xu), 0.5)
    fz = math_("SUBTRACT", math_("FRACT", zr), 0.5)
    d = math_("SQRT", math_("ADD", math_("MULTIPLY", fx, fx), math_("MULTIPLY", math_("MULTIPLY", fz, fz), 0.75)))
    hole = math_("LESS_THAN", d, r / pitch)
    b = N("ShaderNodeBsdfPrincipled"); b.inputs["Base Color"].default_value = C.srgb(col)
    b.inputs["Metallic"].default_value = 0.85; b.inputs["Roughness"].default_value = 0.42
    tr = N("ShaderNodeBsdfTransparent")
    mx = N("ShaderNodeMixShader"); L(hole, mx.inputs["Fac"]); L(b.outputs[0], mx.inputs[1]); L(tr.outputs[0], mx.inputs[2])
    o = N("ShaderNodeOutputMaterial"); L(mx.outputs[0], o.inputs["Surface"])
    m.blend_method = "HASHED" if hasattr(m, "blend_method") else None
    return m


def plane_xz(name, w, h, loc, mat):
    o = C.mesh_obj(name, [(-w / 2, 0, -h / 2), (w / 2, 0, -h / 2), (w / 2, 0, h / 2), (-w / 2, 0, h / 2)], [(0, 1, 2, 3)], mat=mat, smooth=False)
    o.location = loc
    return o


# ------------------------------------------------------------------ set
def microwave(wz, on=1.0, screen=True, x0=0.0, glass_refl=0.03):
    """Over-the-range microwave; window centre at (x0, DOOR_Y, wz). Returns dict of parts."""
    M = dict(body=C.pbr("mw_body", "#D8DCE0", 0.35, metal=0.6), dark=C.pbr("mw_dark", "#202328", 0.4, metal=0.3),
             cav=C.pbr("mw_cav", "#E9E4D8", 0.6), panel=C.pbr("mw_panel", "#15171B", 0.25, coat=0.6),
             disp=C.emission("mw_disp", "#7CFFB0", 6.0), lamp=C.emission("mw_lamp", "#FFE2A8", 6.0 * on))
    W_, D_, H_ = 0.56, 0.40, 0.31
    cx, cz = x0 + 0.05, wz + 0.005
    yb = DOOR_Y - 0.03                                                        # body front
    parts = {}
    for nm, size, loc in (("top", (W_, D_, 0.02), (cx, yb - D_ / 2, cz + H_ / 2 - 0.01)),
                          ("bot", (W_, D_, 0.02), (cx, yb - D_ / 2, cz - H_ / 2 + 0.01)),
                          ("left", (0.02, D_, H_), (cx - W_ / 2 + 0.01, yb - D_ / 2, cz)),
                          ("right", (0.02, D_, H_), (cx + W_ / 2 - 0.01, yb - D_ / 2, cz)),
                          ("back", (W_, 0.02, H_), (cx, yb - D_ + 0.01, cz))):
        parts[nm] = C.rbox("mw_" + nm, size, loc, mat=M["body"], bevel=0.004)
    # cavity lining (light cream walls) + warm lamp in the roof
    C.rbox("cav_floor", (W_ - 0.16, D_ - 0.05, 0.005), (x0, yb - D_ / 2, cz - H_ / 2 + 0.025), mat=M["cav"], bevel=0.0)
    C.rbox("cav_back", (W_ - 0.16, 0.005, H_ - 0.05), (x0, yb - D_ + 0.03, cz), mat=M["cav"], bevel=0.0)
    for s in (-1, 1):
        C.rbox("cav_side", (0.005, D_ - 0.05, H_ - 0.05), (x0 + s * (W_ - 0.16) / 2, yb - D_ / 2, cz), mat=M["cav"], bevel=0.0)
    C.rbox("cav_roof", (W_ - 0.16, D_ - 0.05, 0.005), (x0, yb - D_ / 2, cz + H_ / 2 - 0.025), mat=M["cav"], bevel=0.0)
    lamp_o = C.rbox("cav_lamp", (0.06, 0.04, 0.004), (x0 - 0.08, yb - D_ / 2 + 0.06, cz + H_ / 2 - 0.03), mat=M["lamp"], bevel=0.0)
    lamp_o.visible_glossy = False                                               # QA 23 Nov: no lamp streak in the door glass
    if on > 0:
        cl = C.area("cavlight", (x0 - 0.05, yb - D_ / 2, cz + H_ / 2 - 0.04), (0, 0, 0), 0.12, "#FFD9A0", 9.0 * on)
        cl.visible_glossy = False
    # door: dark frame around the window, glass pane, perforated screen behind it, control panel on the right
    fw = 0.035
    for nm, size, loc in (("dtop", (WIN_W + 2 * fw, 0.025, fw), (x0, DOOR_Y - 0.0125, wz + WIN_H / 2 + fw / 2)),
                          ("dbot", (WIN_W + 2 * fw, 0.025, fw + 0.02), (x0, DOOR_Y - 0.0125, wz - WIN_H / 2 - fw / 2 - 0.01)),
                          ("dl", (fw, 0.025, WIN_H), (x0 - WIN_W / 2 - fw / 2, DOOR_Y - 0.0125, wz)),
                          ("dr", (fw, 0.025, WIN_H), (x0 + WIN_W / 2 + fw / 2, DOOR_Y - 0.0125, wz))):
        C.rbox(nm, size, loc, mat=M["dark"], bevel=0.004)
    C.rbox("handle", (0.022, 0.03, WIN_H + 0.04), (x0 + WIN_W / 2 + fw + 0.004, DOOR_Y + 0.012, wz), mat=M["body"], bevel=0.008)
    glass = plane_xz("doorglass", WIN_W, WIN_H, (x0, DOOR_Y, wz), C.glass("doorglass" if glass_refl else "doorglass_clear", refl=glass_refl))
    scr = plane_xz("screen", WIN_W, WIN_H, (x0, DOOR_Y - 0.008, wz), screen_mat()) if screen else None
    px = x0 + WIN_W / 2 + fw + 0.07
    C.rbox("panel", (0.11, 0.02, H_ - 0.02), (px, DOOR_Y - 0.01, cz), mat=M["panel"], bevel=0.004)
    C.rbox("display", (0.07, 0.004, 0.022), (px, DOOR_Y + 0.001, cz + 0.1), mat=M["disp"], bevel=0.0)
    for i in range(4):
        for j in range(3):
            C.rbox("btn", (0.022, 0.006, 0.014), (px - 0.027 + j * 0.027, DOOR_Y + 0.001, cz + 0.05 - i * 0.03), mat=M["dark"], bevel=0.002)
    # turntable + bowl of soup
    fz = cz - H_ / 2 + 0.03
    tt = C.cyl("turntable", 0.13, 0.006, (x0, yb - D_ / 2 + 0.02, fz + 0.012), mat=C.glass("tt", refl=0.1), verts=48)
    bowl = C.cyl("bowl", 0.055, 0.05, (x0 + 0.05, yb - D_ / 2 + 0.02, fz + 0.04), mat=C.pbr("bowl", "#FF6B5B", 0.25, coat=0.7), verts=40, r2=0.04)
    soup = C.cyl("soup", 0.05, 0.004, (x0 + 0.05, yb - D_ / 2 + 0.02, fz + 0.063), mat=C.pbr("soup", "#E88A2A", 0.2, coat=0.8), verts=40)
    piv = C.empty("tt_pivot", (x0, yb - D_ / 2 + 0.02, fz))
    for o in (bowl, soup):
        o.parent = piv; o.location = Vector(o.location) - Vector(piv.location)
    return dict(M=M, glass=glass, screen=scr, pivot=piv, bowl=bowl, fz=fz, cz=cz, yb=yb, depth=D_)


def spin(piv, n, turns=0.35):
    key_obj(piv, 0, rot=(0, 0, 0)); key_obj(piv, n, rot=(0, 0, turns * 2 * math.pi))
    C.set_interp(piv, "LINEAR")


def kitchen(wz):
    P.world("#2A3A4A", 0.5)
    wall = C.rbox("wall", (4.0, 0.05, 3.0), (0, DOOR_Y - 0.46, 1.5), mat=C.pbr("wall", "#2F5E7A", 0.8, cvar=0.03), bevel=0.0)
    C.rbox("backsplash", (2.4, 0.02, 0.5), (0, DOOR_Y - 0.43, wz - 0.42), mat=C.pbr("tiles", "#F4F1EA", 0.3, bump="cells", bscale=40, bstr=0.25), bevel=0.0)
    (b, t), top = P.counter(loc=(0, DOOR_Y - 0.43 - 0.65, 0), w=2.4, d=0.65, h=0.92, body="#22313F")
    for s in (-1, 1):                                                         # upper cabinets either side + above
        C.rbox("cab", (0.62, 0.34, 0.75), (s * 0.62, DOOR_Y - 0.25, wz + 0.2), mat=C.pbr("cab", "#F2E8D8", 0.45), bevel=0.01)
    C.rbox("cab_top", (0.64, 0.34, 0.3), (0.05, DOOR_Y - 0.25, wz + 0.35), mat=C.pbr("cab", "#F2E8D8", 0.45), bevel=0.01)
    C.rbox("floor", (6, 6, 0.02), (0, 0, -0.01), mat=C.pbr("floor", "#B98A5E", 0.6, cvar=0.08), bevel=0.0)


def cook(n, look=None):
    h = Hm.build(dict(COOK, loc=(0, 0.04, 0), rot_z=0), "man"); ct = Hm.controls(h)
    E = h["eye_c"].z
    ct["handR"].location = (-0.2, -0.05, E - 0.6); ct["handL"].location = (0.2, -0.05, E - 0.6)
    return h, ct, E


def wave_pts(L=WAVE_L, n_waves=3.0, amp=0.022, steps=160, axis="x"):
    pts = []
    for i in range(steps + 1):
        s = i / steps * n_waves * L
        y = amp * math.sin(2 * math.pi * s / L)
        pts.append((s, 0.0, y) if axis == "x" else (0.0, s, y))
    return pts


def wave(name, L=WAVE_L, n_waves=3.0, amp=0.022, r=0.0035, col=MICRO, strength=8.0, axis="x"):
    o = C.tube(name, wave_pts(L, n_waves, amp, axis=axis), r, mat=C.emission(name + "_m", col, strength), n=10)
    return o


def ring(name, R, r=0.003, col=MICRO, strength=6.0):
    pts = [(R * math.cos(a), 0.0, R * math.sin(a)) for a in [i * 2 * math.pi / 64 for i in range(64)]]
    return C.tube(name, pts, r, mat=C.emission(name + "_m", col, strength), closed=True, n=8)


# ------------------------------------------------------------------ shots
def _pov_set(n):
    h, ct, E = cook(n)
    wz = E - 0.07
    kitchen(wz)
    mw = microwave(wz, glass_refl=0.0)                                         # POV through the door: no glass reflection
    spin(mw["pivot"], n)
    P.lights((0, -0.1, E), key=700, rim=500, fill=250)
    C.area("facefill", (0.0, DOOR_Y + 0.02, E - 0.02), (math.radians(90), 0, 0), 0.25, "#FFD9A0", 7.0)
    C.area("facekey", (-0.5, -0.45, E + 0.3), (math.radians(70), 0, math.radians(-50)), 0.4, "#FFF1DC", 40.0)
    return h, ct, E, wz, mw


def _pov_cam(cam, n, E, wz, mw, a=0.0, b=1.0):
    y = DOOR_Y - 0.2
    A = ((0.0, y, wz + 0.02), (0.0, 0.1, E - 0.0), 46)
    B = ((0.0, y + 0.02, wz + 0.02), (0.0, 0.1, E - 0.0), 50)
    cam_move(cam, n, A if a == 0 else B, B if a == 0 else A, focus=(0.0, -0.08, E), fstop=7.0)


def hook_pov(sh, cam, n):
    """Frame 1: from INSIDE the running microwave, through the dotted metal screen: the cook's face pressed close, eyes wide, bowl turning."""
    h, ct, E, wz, mw = _pov_set(n)
    key_obj(ct["look"], 0, loc=(0.03, -0.5, wz - 0.06)); key_obj(ct["look"], n, loc=(-0.02, -0.5, wz - 0.03))
    Hm.face(h["keys"], 0, wide=1.0, brows_up=0.8, open=0.35); Hm.face(h["keys"], n, wide=0.5, squint=0.3, browL_up=0.9, purse=0.3, brows_up=0.0, open=0.0)
    life(h, n, 3, blinks=False)
    _pov_cam(cam, n, E, wz, mw)


def loop_pov(sh, cam, n):
    """Last shot: same POV; he leans back in, ends on hook_pov's first frame (loop)."""
    h, ct, E, wz, mw = _pov_set(n)
    key_obj(ct["look"], 0, loc=(0.0, -0.5, wz - 0.02)); key_obj(ct["look"], n, loc=(0.03, -0.5, wz - 0.06))
    Hm.face(h["keys"], 0, smile=0.5, browL_up=0.3); Hm.face(h["keys"], n, wide=1.0, brows_up=0.8, open=0.35, smile=0.0, browL_up=0.0)
    _pov_cam(cam, n, E, wz, mw, a=1)


def macro_mesh(sh, cam, n):
    """'It's not decoration': outside, an extreme close-up gliding across the perforated screen, the lit bowl turning behind."""
    E = 1.6; wz = E - 0.07
    kitchen(wz); mw = microwave(wz); spin(mw["pivot"], n, 0.25)
    P.lights((0, DOOR_Y, wz), key=500, rim=300, fill=150)
    cam_move(cam, n, ((-0.06, DOOR_Y + 0.07, wz + 0.02), (-0.05, DOOR_Y - 0.2, wz - 0.02), 60),
             ((0.06, DOOR_Y + 0.07, wz + 0.01), (0.05, DOOR_Y - 0.2, wz - 0.03), 62), focus=(0, DOOR_Y - 0.008, wz), fstop=8.0)


def leak(sh, cam, n):
    """'Without it...': same microwave with the screen gone (plain glass); glowing wave rings pour out through the glass at us."""
    E = 1.6; wz = E - 0.07
    kitchen(wz); mw = microwave(wz, screen=False); spin(mw["pivot"], n, 0.3)
    P.lights((0, DOOR_Y, wz), key=500, rim=300, fill=150)
    f0 = W_(sh, "pour", 0.8)
    for i in range(7):
        rg = ring(f"ring{i}", 0.08, r=0.004, strength=9.0)
        a = max(0, f0 - 18) + i * 9
        key_obj(rg, 0, loc=(0.0, DOOR_Y - 0.12, wz), scale=0.0); key_obj(rg, a, loc=(0.0, DOOR_Y - 0.12, wz), scale=0.3)
        key_obj(rg, a + 40, loc=(0.0, DOOR_Y + 0.75, wz + 0.02), scale=3.2)
    cam_move(cam, n, ((0.1, DOOR_Y + 0.62, wz + 0.03), (0.03, DOOR_Y, wz - 0.01), 30),
             ((0.08, DOOR_Y + 0.55, wz + 0.03), (0.03, DOOR_Y, wz - 0.01), 32), focus=(0.03, DOOR_Y + 0.1, wz), fstop=5.6)


def wave_ruler(sh, cam, n):
    """'Microwaves are waves... about twelve centimetres': a glowing wave travels in front of the dark studio; a ruler marks one 12 cm wave."""
    P.world("#0E1A2A", 0.3)
    P.studio(top="#0E2A44", bottom="#1B3A5C", mid="#14304E", y0=0.5, glow=0.3, height=4.0, width=8.0, depth=3.0)
    Z0 = 1.0
    wv = wave("mwave", n_waves=6.0, amp=0.03, r=0.0045)
    key_obj(wv, 0, loc=(-0.4, 0, Z0)); key_obj(wv, n, loc=(-0.4 + WAVE_L * 1.5, 0, Z0)); C.set_interp(wv, "LINEAR")
    ruler_y = Z0 - 0.06
    C.rbox("ruler", (WAVE_L + 0.02, 0.006, 0.03), (0, 0.005, ruler_y), mat=C.pbr("ruler", "#FFC93C", 0.4), bevel=0.002)
    for i in range(13):
        hgt = 0.014 if i % 5 == 0 else 0.008
        C.rbox("tick", (0.0012, 0.008, hgt), (-WAVE_L / 2 + i * WAVE_L / 12, 0.0, ruler_y + 0.015 - hgt / 2), mat=C.pbr("ink", "#1A1A1A", 0.6), bevel=0.0)
    for s in (-1, 1):                                                           # end markers at one wavelength (crest to crest)
        C.rbox("mark", (0.002, 0.004, 0.09), (s * WAVE_L / 2, -0.004, Z0 - 0.005), mat=C.emission("markm", "#FFF4E0", 4.0), bevel=0.0)
    P.lights((0, 0, Z0), key=300, rim=200, fill=80)
    cam_move(cam, n, ((0.0, -0.3, Z0 + 0.0), (0.0, 0.0, Z0 + 0.01), 40), ((0.0, -0.26, Z0 + 0.0), (0.0, 0.0, Z0 + 0.01), 42),
             focus=(0, 0, Z0), fstop=6.3)


def hole_macro(sh, cam, n):
    """'Just a few millimetres wide': extreme macro of the screen holes with a steel ruler's millimetre marks along the bottom."""
    P.world("#1A2633", 0.4)
    wz = 1.0
    plane_xz("bigscreen", 0.12, 0.08, (0, 0, wz), screen_mat("bigscreen"))
    C.area("behind", (0, 0.12, wz), (math.radians(-90), 0, 0), 0.3, "#FFD9A0", 60.0)
    plane_xz("glowcard", 0.4, 0.3, (0, 0.06, wz), C.emission("glowcard", "#FFD9A0", 2.5))
    C.rbox("steelrule", (0.08, 0.002, 0.012), (0, -0.003, wz - 0.022), mat=C.pbr("steelrule", "#E3E6EA", 0.45, metal=0.5), bevel=0.0005)
    for i in range(41):
        hgt = 0.006 if i % 10 == 0 else (0.0045 if i % 5 == 0 else 0.003)
        C.rbox("mm", (0.00025, 0.0012, hgt), (-0.02 + i * 0.001, -0.0042, wz - 0.016 - hgt / 2), mat=C.pbr("mmink", "#111111", 0.6), bevel=0.0)
    P.lights((0, 0, wz), key=700, rim=200, fill=250, scale=0.3)
    cam_move(cam, n, ((-0.004, -0.075, wz + 0.002), (-0.004, 0.0, wz - 0.004), 60), ((0.004, -0.068, wz + 0.002), (0.004, 0.0, wz - 0.004), 62),
             focus=(0, 0, wz - 0.004), fstop=11.0)


def bounce(sh, cam, n):
    """'Far too small... so the waves bounce back inside': a big 12 cm wave runs into the dotted screen and reflects straight back."""
    P.world("#0E1A2A", 0.3)
    P.studio(top="#0E2A44", bottom="#1B3A5C", mid="#14304E", y0=0.6, glow=0.3, height=4.0, width=8.0, depth=3.0)
    Z0 = 1.0
    scr = plane_xz("wall_screen", 0.5, 0.36, (0, 0.0, Z0), screen_mat("wall_screen", col="#3A3F48"))
    scr.rotation_euler = (0, 0, math.radians(90))                               # screen plane faces +X/-X; waves travel along X into it
    gc = plane_xz("glowcard", 0.8, 0.6, (0.12, 0.0, Z0), C.emission("glowcard2", "#FFC27A", 2.2)); gc.rotation_euler = (0, 0, math.radians(90))
    fb = W_(sh, "bounce", 2.0)
    wv = wave("bwave", n_waves=2.5, amp=0.035, r=0.006)
    Lw = 2.5 * WAVE_L
    key_obj(wv, 0, loc=(-0.48, 0, Z0), rot=(0, 0, 0)); key_obj(wv, fb, loc=(-Lw, 0, Z0), rot=(0, 0, 0))
    key_obj(wv, fb + 1, loc=(0.0, 0, Z0), rot=(0, 0, math.pi)); key_obj(wv, n, loc=(-0.45, 0, Z0), rot=(0, 0, math.pi))
    C.set_interp(wv, "LINEAR")
    fl = C.cyl("flash", 0.09, 0.002, (-0.004, 0, Z0), rot=(0, math.radians(90), 0), mat=C.emission("flashm", "#BFF0FF", 10.0), verts=32)
    key_obj(fl, 0, scale=0.0); key_obj(fl, fb - 1, scale=0.0); key_obj(fl, fb + 2, scale=1.0); key_obj(fl, fb + 10, scale=0.0)
    P.lights((-0.2, 0, Z0), key=300, rim=200, fill=80)
    cam_move(cam, n, ((-0.14, -0.32, Z0 + 0.05), (-0.08, 0.0, Z0), 22), ((-0.13, -0.3, Z0 + 0.05), (-0.08, 0.0, Z0), 23), focus=(-0.08, 0, Z0), fstop=6.3)


def light_through(sh, cam, n):
    """'Light waves are hundreds of thousands of times smaller. They slip through': tiny bright rays stream out through the holes,
    while the big blue microwave wave stays trapped behind the screen."""
    E = 1.6; wz = E - 0.07
    kitchen(wz); mw = microwave(wz); spin(mw["pivot"], n, 0.3)
    P.lights((0, DOOR_Y, wz), key=350, rim=250, fill=120)
    fs = W_(sh, "slip", 2.5)
    rnd = random.Random(4); lm = C.emission("ray_m", LIGHT, 30.0)
    for i in range(70):
        x = rnd.uniform(-0.13, 0.13); z = wz + rnd.uniform(-0.07, 0.07)
        ray = C.cyl(f"ray{i}", 0.0012, 0.08, (x, DOOR_Y - 0.15, z), rot=(math.radians(90), 0, 0), mat=lm, verts=6)
        a = rnd.randint(0, max(1, n - 30)) if i < 35 else rnd.randint(max(0, fs - 10), max(1, n - 20))
        key_obj(ray, 0, loc=(x, DOOR_Y - 0.15, z), scale=0.0); key_obj(ray, max(0, a - 1), loc=(x, DOOR_Y - 0.15, z), scale=0.0)
        key_obj(ray, a, loc=(x, DOOR_Y - 0.12, z), scale=1.0); key_obj(ray, a + 22, loc=(x, DOOR_Y + 0.35, z), scale=1.0)
        key_obj(ray, a + 23, scale=0.0)
    wv = wave("trapped", n_waves=1.6, amp=0.02, r=0.004)                       # big wave sloshing inside (stays in)
    for f, xo in ((0, -0.1), (n // 3, -0.02), (2 * n // 3, -0.1), (n, -0.02)):
        key_obj(wv, f, loc=(xo, DOOR_Y - 0.1, wz - 0.02))
    cam_move(cam, n, ((0.2, DOOR_Y + 0.42, wz + 0.04), (0.0, DOOR_Y, wz), 40), ((0.15, DOOR_Y + 0.36, wz + 0.03), (0.0, DOOR_Y, wz), 44),
             focus=(0.0, DOOR_Y + 0.02, wz), fstop=5.6)


def watch(sh, cam, n):
    """'That's why you can watch your food': outside, beside the door: the cook watching his soup turn, a small smile."""
    h, ct, E = cook(n)
    wz = E - 0.07
    kitchen(wz); mw = microwave(wz); spin(mw["pivot"], n, 0.2)
    key_obj(ct["look"], 0, loc=(0.03, -0.55, wz - 0.06)); key_obj(ct["look"], n, loc=(0.0, -0.55, wz - 0.05))
    Hm.face(h["keys"], 0, squint=0.2, browL_up=0.3); Hm.face(h["keys"], n, smile=0.6, squint=0.3)
    life(h, n, 5)
    P.lights((0, -0.1, E), key=800, rim=600, fill=260)
    C.area("facefill", (0.0, DOOR_Y + 0.02, E - 0.02), (math.radians(90), 0, 0), 0.25, "#FFD9A0", 10.0)
    cam_move(cam, n, ((-0.36, 0.36, E + 0.1), (0.06, DOOR_Y, wz - 0.02), 30), ((-0.35, 0.33, E + 0.1), (0.06, DOOR_Y, wz - 0.02), 32),
             focus=(0.03, DOOR_Y, wz), fstop=4.5)


SHOTS = {f.__name__: f for f in (hook_pov, macro_mesh, leak, wave_ruler, hole_macro, bounce, light_through, watch, loop_pov)}


if __name__ == "__main__":
    from sr_shot import run
    run(SHOTS, argv)
