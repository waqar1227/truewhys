"""A-035 Style R scenes (Blender): "Fold paper 42 times and it would reach the Moon". Renders every shot of shots.json as frames.
/opt/c3d/bin/python -I scene.py <shots.json> <out_dir> [--w 540 --h 960 --samples 12 --step 3 --shots a,b --gpu --part 0/2 --mblur]
Our own sets (look.md): a home study at night (forest-green wall, oak desk, tangerine desk lamp) with our new MPFB lead Gus pressing a fat
folded paper block; a paper stack growing beside a mug; a cream paper column rising past generic glass towers at plum dusk; the column from the
Earth's rim to the Moon in black space; a macro cross-section of the nested fold curves; a long plain corridor with a paper strip running out of
sight (the 2002 record, no person shown). No brands, logos or real people. Facts in sources.md.
"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, os.path.join(HERE, "..", "..", "lib", "style_r"), os.path.join(HERE, "..", "..", "lib")):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
import bpy
from mathutils import Vector
import sr_common as C, sr_props as P, sr_human as Hm
from sr_shot import key_obj, cam_move, W_, life, ease

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]

FOREST, PAPER, TANG, PLUM, LIME = "#2E5E4E", "#EFE6D2", "#F08A24", "#4A2E4F", "#B5D33D"
GUS = dict(macro={"gender": 1.0, "age": 0.80, "muscle": 0.75, "weight": 0.42, "proportions": 0.5, "height": 0.55}, skin="#C68B65",
           hair="#A9A8A2", hair_style="short", shirt="#B8623A", trousers="#3A3340", shoes="#5A4030", iris="#4A3A2C", sleeve="long",
           shirt_push=0.03, shirt_iters=40, tuck=0.05)          # Gus: ~60, short grey hair, rust-tangerine knit top, plum-grey trousers
DESK_Z = 0.76                                                   # desk top height
GX, GY = 0.0, -0.05                                             # Gus stands behind the desk facing +Y (the camera side)
BLOCK = Vector((0.0, 0.21, DESK_Z))                             # folded block on the desk, in front of him


def mats():
    return dict(
        paper=C.pbr("paper", PAPER, 0.85, bump="noise", bscale=400, bstr=0.18, cvar=0.03, sss=0.05),
        oak=C.pbr("oak", "#8A5A35", 0.45, bump="noise", bscale=60, bstr=0.15, cvar=0.18, cscale=3.0, color2="#6E4426", stretch=(1, 12, 1)),
        wall=C.pbr("wall", FOREST, 0.85, bump="noise", bscale=300, bstr=0.08, cvar=0.05),
        dark=C.pbr("dark", "#1A1A1C", 0.5),
        brass=C.pbr("brass", "#B08A4A", 0.3, metal=0.9),
        mug=C.pbr("mug", PLUM, 0.25, coat=0.6),
        floor=C.pbr("floorwood", "#4A3426", 0.6, bump="noise", bscale=80, bstr=0.1, cvar=0.12, stretch=(1, 10, 1)),
    )


def key_emit(mat, f, s):
    n = mat.node_tree.nodes.get("Emission")
    n.inputs["Strength"].default_value = s; n.inputs["Strength"].keyframe_insert("default_value", frame=f)


def spot(name, loc, target, col, energy, size_deg=70, blend=0.6, r=0.05):
    d = bpy.data.lights.new(name, "SPOT"); d.energy = energy; d.color = C.srgb(col)[:3]; d.spot_size = math.radians(size_deg)
    d.spot_blend = blend; d.shadow_soft_size = r
    o = bpy.data.objects.new(name, d); bpy.context.scene.collection.objects.link(o); o.location = loc
    dv = Vector(target) - Vector(loc); o.rotation_euler = dv.to_track_quat("-Z", "Y").to_euler()
    return o


def sky(top, horizon, strength=1.0):
    """World: vertical gradient by view direction (horizon colour low, top colour high)."""
    w = bpy.data.worlds.new("sky"); bpy.context.scene.world = w; w.use_nodes = True
    nt = w.node_tree; N = nt.nodes.new; L = nt.links.new
    bg = nt.nodes["Background"]; tc = N("ShaderNodeTexCoord"); sep = N("ShaderNodeSeparateXYZ")
    L(tc.outputs["Generated"], sep.inputs[0])
    mr = N("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = -0.05; mr.inputs["From Max"].default_value = 1.0
    L(sep.outputs["Z"], mr.inputs["Value"])
    ramp = N("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = C.srgb(horizon); ramp.color_ramp.elements[1].color = C.srgb(top)
    L(mr.outputs["Result"], ramp.inputs["Fac"]); L(ramp.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = strength
    return w


# ------------------------------------------------------------------ the folded paper
def fold_block(name, L=0.11, Wd=0.08, t=0.0009, pairs=24, loc=(0, 0, 0), rot_z=0.0, seed=1, arc_mat=None):
    """A folded paper block as its real cross-section: `pairs` nested U-shaped sheets (each fold wraps the ones inside it).
    The fold edge (arcs) faces local -X; flat ends are slightly ragged. Returns (root empty, flats obj, arcs obj).
    Bottom of the block sits at local z = 0."""
    M = mats(); rnd = random.Random(seed)
    root = C.empty(name, loc, (0, 0, rot_z))
    H = pairs * t
    def ribbon(nm, prof, mat):
        verts, faces = [], []
        ny = 6
        for j in range(ny + 1):
            y = -Wd / 2 + Wd * j / ny
            for (x, z) in prof:
                wob = 0.0004 * math.sin(7 * y / Wd + x * 40)
                verts.append((x, y, z + wob))
        m = len(prof)
        for j in range(ny):
            for i in range(m - 1):
                a = j * m + i; faces.append((a, a + 1, a + 1 + m, a + m))
        return verts, faces
    fv, ff, av, af = [], [], [], []
    for k in range(pairs):
        r = (k + 0.5) * t
        ext_top = L + rnd.uniform(-0.002, 0.002); ext_bot = L + rnd.uniform(-0.002, 0.002)
        top = [(ext_top * (1 - i / 6), H + r) for i in range(7)]              # every U is centred on the block's mid-height H
        arc = [(min(0.0, r * math.cos(math.radians(a))), H + r * math.sin(math.radians(a))) for a in range(90, 271, 12)]
        bot = [(ext_bot * i / 6, H - r) for i in range(7)]
        for prof, vs, fs in ((top, fv, ff), (arc, av, af), (bot, fv, ff)):
            v, f = ribbon("", prof, None)
            o = len(vs); vs.extend(v); fs.extend(tuple(i + o for i in q) for q in f)
    flats = C.mesh_obj(name + "_flats", fv, ff, mat=M["paper"], parent=root)
    arcs = C.mesh_obj(name + "_arcs", av, af, mat=arc_mat or M["paper"], parent=root)
    for o in (flats, arcs):
        s = o.modifiers.new("solid", "SOLIDIFY"); s.thickness = t * 0.8; s.offset = 0.0
    return root, flats, arcs


def layers_mat(name="stackedge", bands=260.0, emit=0.0):
    """Paper-edge look: fine alternating cream bands along the stack height (object Z, so the count stays fixed while it grows)."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.8
    tc = N("ShaderNodeTexCoord"); wv = N("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Z"
    wv.inputs["Scale"].default_value = bands; wv.inputs["Distortion"].default_value = 1.5; wv.inputs["Detail"].default_value = 2.0
    L(tc.outputs["Object"], wv.inputs["Vector"])
    rp = N("ShaderNodeValToRGB"); rp.color_ramp.elements[0].color = C.srgb("#A89A80"); rp.color_ramp.elements[1].color = C.srgb(PAPER)
    rp.color_ramp.elements[0].position = 0.45; rp.color_ramp.elements[1].position = 0.55
    L(wv.outputs["Fac"], rp.inputs["Fac"]); L(rp.outputs["Color"], b.inputs["Base Color"])
    if emit:
        L(rp.outputs["Color"], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = emit
    return m


def stack(name, Wd=0.21, D=0.15, loc=(0, 0, 0), mat=None):
    """A sheet stack (box with page-edge bands). Height is animated with scale z (1 unit = 1 m tall at scale 1)."""
    M = mats()
    m = mat or layers_mat("stackedge", 22.0)
    root = C.empty(name, loc)
    C.rbox(name + "_box", (Wd, D, 1.0), (0, 0, 0.5), mat=m, bevel=0.0005, parent=root)
    return root


# ------------------------------------------------------------------ the study
def study(M, lamp=True):
    P.world("#141C2A", 0.15)
    C.rbox("floor", (6, 6, 0.02), (0, 0, -0.01), mat=M["floor"], bevel=0.0)
    C.rbox("backwall", (6, 0.05, 3.0), (0, -1.0, 1.5), mat=M["wall"], bevel=0.0)
    # desk
    C.rbox("desk_top", (1.30, 0.62, 0.04), (0, 0.42, DESK_Z - 0.02), mat=M["oak"], bevel=0.006)
    for sx in (-1, 1):
        for sy in (0.16, 0.68):
            C.rbox("desk_leg", (0.05, 0.05, DESK_Z - 0.04), (sx * 0.60, sy, (DESK_Z - 0.04) / 2), mat=M["oak"], bevel=0.004)
    # shelf with books on the wall behind him
    C.rbox("shelf", (1.1, 0.22, 0.03), (0.55, -0.88, 1.72), mat=M["oak"], bevel=0.004)
    rnd = random.Random(4); x = 0.08
    while x < 1.0:
        w = rnd.uniform(0.025, 0.05); h = rnd.uniform(0.18, 0.27)
        col = rnd.choice(["#7A3B2E", "#2F4858", PLUM, "#8C7A4A", "#3E5C3A", "#9C6B3E"])
        C.rbox("book", (w, 0.17, h), (x + w / 2, -0.87, 1.735 + h / 2), rot=(0, rnd.uniform(-0.04, 0.04), 0),
               mat=C.pbr("book" + col, col, 0.7, cvar=0.08), bevel=0.003)
        x += w + 0.004
    C.rbox("frame", (0.42, 0.02, 0.32), (-0.55, -0.97, 1.55), mat=M["dark"], bevel=0.006)
    C.rbox("frame_art", (0.36, 0.01, 0.26), (-0.55, -0.955, 1.55), mat=C.pbr("art", "#C8A76A", 0.8, cvar=0.4, cscale=2.0, color2="#7FA0A8"), bevel=0.0)
    # props: mug, pencil, loose sheets
    C.cyl("mug", 0.042, 0.10, (0.36, 0.50, DESK_Z + 0.05), mat=M["mug"], verts=32, bevel=0.004)
    C.tube("mug_handle", [(0.40, 0.50, DESK_Z + 0.08), (0.43, 0.50, DESK_Z + 0.065), (0.43, 0.50, DESK_Z + 0.035), (0.40, 0.50, DESK_Z + 0.025)],
           0.007, mat=M["mug"])
    C.cyl("pencil", 0.0035, 0.17, (-0.30, 0.44, DESK_Z + 0.004), rot=(0, math.radians(90), math.radians(20)),
          mat=C.pbr("pencil", "#E0A030", 0.5), verts=6)
    for k in range(3):
        C.rbox("sheet", (0.21, 0.297, 0.0003), (-0.36 + k * 0.01, 0.20 + k * 0.012, DESK_Z + 0.0003 * (k + 1)),
               rot=(0, 0, math.radians(-14 + 7 * k)), mat=M["paper"], bevel=0.0)
    if lamp:
        desk_lamp(M, (-0.42, 0.62, DESK_Z), BLOCK + Vector((0, 0, 0.02)))
    C.area("moonrim", (0.9, -0.7, 2.0), (math.radians(-55), 0, math.radians(-140)), 1.0, "#9FB8FF", 60)
    C.area("roomfill", (0.0, 2.6, 1.6), (math.radians(85), 0, math.radians(180)), 2.0, "#E8D8C0", 45)


def desk_lamp(M, base, target):
    bx, by, bz = base
    C.cyl("lamp_base", 0.07, 0.02, (bx, by, bz + 0.01), mat=M["dark"], verts=32, bevel=0.004)
    elbow = (bx + 0.02, by - 0.06, bz + 0.40)
    head = (bx + 0.16, by - 0.10, bz + 0.46)
    C.tube("lamp_arm1", [(bx, by, bz + 0.02), elbow], 0.008, mat=M["brass"])
    C.tube("lamp_arm2", [elbow, head], 0.008, mat=M["brass"])
    d = (Vector(target) - Vector(head)).normalized()
    sh = C.cyl("lamp_shade", 0.06, 0.12, head, mat=C.pbr("shade", TANG, 0.4, coat=0.4), verts=32, r2=0.025)
    sh.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    bulb_pos = Vector(head) + d * 0.04
    C.cyl("lamp_bulb", 0.03, 0.01, tuple(bulb_pos), mat=C.emission("bulb_e", "#FFD9A0", 25.0), verts=24).rotation_euler = sh.rotation_euler
    spot("lamp_spot", tuple(bulb_pos), target, "#FFB36A", 260, size_deg=85, blend=0.7, r=0.03)


def gus():
    h = Hm.build(dict(GUS, loc=(GX, GY, 0), rot_z=180), "gus"); ct = Hm.controls(h)
    E = h["eye_c"].z
    return h, ct, E


def press_pose(h, ct, f, depth=0.0, lean=14):
    """Both palms flat on top of the block; `depth` pushes the hands down (m). Spine leans over the desk."""
    for b, a in (("spine05", lean * 0.4), ("spine04", lean * 0.35), ("spine03", lean * 0.25)):
        Hm.pose(h["rig"], b, (a, 0, 0), f)
    top = BLOCK.z + 0.06 - depth
    key_obj(ct["handL"], f, loc=(BLOCK.x - 0.065, BLOCK.y - 0.02, top + 0.015))     # he faces +Y: his left hand is world -X
    key_obj(ct["handR"], f, loc=(BLOCK.x + 0.065, BLOCK.y - 0.02, top + 0.015))


def hook_cam(cam, n, rev=False):
    """Low at desk height in front: the block big in the lower frame, Gus's straining face above it."""
    A = ((0.10, 1.05, 1.02), (0.0, 0.10, 1.30), 31)
    B = ((0.07, 0.99, 1.01), (0.0, 0.10, 1.31), 32)
    P0, P1 = (B, A) if rev else (A, B)
    cam_move(cam, n, P0, P1, focus=(0, GY + 0.05, 1.40), fstop=4.0)


def press_set(n):
    M = mats(); study(M)
    blk, fl, ar = fold_block("blk", L=0.15, Wd=0.12, t=0.001, pairs=30, loc=tuple(BLOCK), rot_z=math.radians(180), seed=2)
    h, ct, E = gus()
    C.area("facekey", (-0.5, 0.9, E + 0.35), (math.radians(55), 0, math.radians(-150)), 0.5, "#FFE2C0", 14.0)
    return M, blk, h, ct, E


def squash(blk, f, s):
    key_obj(blk, f, scale=(1.0 + (1 - s) * 0.25, 1.0 + (1 - s) * 0.25, s))


def hook_press(sh, cam, n):
    """Frame 1: Gus already leaning his whole weight on the fat folded block, jaw set; it squashes a little and springs back
    (paper crumple at 0.0 s); on 'Moon' he looks up at us, eyebrows high (amazed)."""
    M, blk, h, ct, E = press_set(n)
    for f, d, s in ((0, 0.010, 0.86), (8, 0.014, 0.80), (16, 0.004, 0.96), (24, 0.0, 1.0), (40, 0.012, 0.84), (52, 0.0, 1.0)):
        press_pose(h, ct, f, depth=d, lean=30); squash(blk, f, s)
    press_pose(h, ct, n, depth=0.0, lean=22); squash(blk, n, 1.0)
    key_obj(ct["look"], 0, loc=(0.02, 1.2, 0.95)); key_obj(ct["look"], 30, loc=(0.02, 1.2, 0.95))      # straining face toward us (frame 1 emotion)
    key_obj(ct["look"], 44, loc=(0, BLOCK.y, BLOCK.z)); key_obj(ct["look"], 60, loc=(0, BLOCK.y, BLOCK.z))
    fm = W_(sh, "moon", 4.6)
    key_obj(ct["look"], fm - 6, loc=(0, BLOCK.y, BLOCK.z + 0.05)); key_obj(ct["look"], fm + 4, loc=(0.03, 1.4, 1.20)); key_obj(ct["look"], n, loc=(0.03, 1.4, 1.20))
    Hm.face(h["keys"], 0, squint=0.7, brows_down=0.6, purse=0.5, sneer=0.3); Hm.face(h["keys"], 50, squint=0.8, brows_down=0.7, purse=0.6, sneer=0.4)
    Hm.face(h["keys"], fm - 6, squint=0.3, brows_down=0.2, purse=0.2, sneer=0.0)
    Hm.face(h["keys"], fm + 6, squint=0.0, brows_down=0.0, purse=0.0, wide=0.9, brows_up=0.9, open=0.3)
    Hm.face(h["keys"], n, wide=0.8, brows_up=0.8, open=0.25)
    hook_cam(cam, n)


def loop_press(sh, cam, n):
    """Last shot, same framing: Gus looks at us with a dry little smile ('it's not you'), then leans back onto the block and pushes
    again, ending on hook_press's first pose (loop)."""
    M, blk, h, ct, E = press_set(n)
    press_pose(h, ct, 0, depth=0.0, lean=10); squash(blk, 0, 1.0)
    press_pose(h, ct, n - 22, depth=0.0, lean=10); squash(blk, n - 22, 1.0)
    press_pose(h, ct, n, depth=0.010, lean=30); squash(blk, n, 0.86)
    key_obj(ct["look"], 0, loc=(0.03, 1.4, 1.22)); key_obj(ct["look"], n - 24, loc=(0.03, 1.4, 1.22)); key_obj(ct["look"], n - 8, loc=(0.02, 1.2, 0.95))
    key_obj(ct["look"], n, loc=(0.02, 1.2, 0.95))
    Hm.face(h["keys"], 0, smile=0.15, browL_up=0.4); Hm.face(h["keys"], 30, smile=0.5, squint=0.25, browL_up=0.5)
    Hm.face(h["keys"], n - 22, smile=0.4, squint=0.2, browL_up=0.3)
    Hm.face(h["keys"], n, smile=0.0, browL_up=0.0, squint=0.7, brows_down=0.6, purse=0.5, sneer=0.3)
    life(h, n - 24, 5)
    hook_cam(cam, n, rev=True)


def desk_ask(sh, cam, n):
    """'So why can't you?': close on Gus, he straightens up, holds the block up at eye level and turns it, puzzled."""
    M, blk, h, ct, E = press_set(n)
    for b in ("spine05", "spine04", "spine03"):
        Hm.pose(h["rig"], b, (0, 0, 0))
    hold_c = Vector((0.08, GY + 0.34, E - 0.30))
    key_obj(blk, 0, loc=tuple(hold_c - Vector((0, 0, 0.02))), rot=(0, 0, math.radians(180))); key_obj(blk, n, loc=tuple(hold_c), rot=(0, math.radians(-14), math.radians(200)))
    ct["handL"].location = (GX - 0.24, GY + 0.06, E - 0.78)                       # left arm relaxed at his side
    key_obj(ct["handR"], 0, loc=tuple(hold_c + Vector((0.05, -0.02, -0.03)))); key_obj(ct["handR"], n, loc=tuple(hold_c + Vector((0.05, -0.02, -0.01))))
    Hm.grip(h, "R", 0.5, 0.45)
    key_obj(ct["look"], 0, loc=tuple(hold_c)); key_obj(ct["look"], n, loc=tuple(hold_c + Vector((0, 0, 0.02))))
    Hm.face(h["keys"], 0, brows_inner=0.6, browL_up=0.4, purse=0.3); Hm.face(h["keys"], n, brows_inner=0.8, browL_up=0.6, purse=0.45, squint=0.2)
    life(h, n, 7)
    cam_move(cam, n, ((0.10, 0.75, E - 0.05), (0.0, GY, E - 0.12), 48), ((0.08, 0.68, E - 0.06), (0.0, GY, E - 0.12), 52),
             focus=(0, GY + 0.1, E - 0.05), fstop=2.8)


def stuck_macro(sh, cam, n):
    """'you'll get stuck at about seven': macro on the block under his palms; it barely moves, springs back each push."""
    M, blk, h, ct, E = press_set(n)
    for f, d, s in ((0, 0.0, 1.0), (14, 0.012, 0.85), (24, 0.0, 1.0), (44, 0.014, 0.83), (56, 0.0, 1.0), (76, 0.012, 0.86), (n, 0.0, 1.0)):
        press_pose(h, ct, f, depth=d, lean=30); squash(blk, f, s)
    cam_move(cam, n, ((0.16, BLOCK.y + 0.30, BLOCK.z + 0.10), tuple(BLOCK + Vector((0, 0, 0.02))), 55),
             ((0.11, BLOCK.y + 0.27, BLOCK.z + 0.08), tuple(BLOCK + Vector((0, 0, 0.02))), 60), focus=tuple(BLOCK + Vector((0, 0.02, 0.025))), fstop=4.0)


def stack_desk(sh, cam, n):
    """'Every fold doubles it. Ten folds: ten centimetres.': on the desk by the plum mug, a paper stack doubles in jumps
    (2, 4, 8 … 1,024 layers) until it is as tall as the mug (10.2 cm)."""
    M = mats(); study(M)
    st = stack("stk", Wd=0.12, D=0.085, loc=(0.20, 0.46, DESK_Z))
    f0, f1 = W_(sh, "doubles", 0.8), W_(sh, "ten#1", 2.8)
    hts = [0.0001 * 2 ** k for k in range(11)]
    for k, ht in enumerate(hts):
        f = int(f0 + (f1 - f0) * (k / 10) ** 0.8)
        key_obj(st, f, scale=(1, 1, max(ht, 0.0001)))
        key_obj(st, f + 3, scale=(1, 1, max(ht, 0.0001) * 1.0))
    key_obj(st, n, scale=(1, 1, hts[-1]))
    C.set_interp(st, "CONSTANT")
    cam_move(cam, n, ((0.17, 0.74, DESK_Z + 0.04), (0.24, 0.47, DESK_Z + 0.045), 50), ((0.16, 0.70, DESK_Z + 0.06), (0.24, 0.47, DESK_Z + 0.05), 50),
             focus=(0.22, 0.46, DESK_Z + 0.05), fstop=5.6)


def towers(rnd, n=26, spread=900, tall=None):
    glass = C.pbr("glass_t", "#2B2F45", 0.12, metal=0.7)
    win = C.pbr("win_t", "#3A3550", 0.3, emit="#FFC47A", estr=0.0, bump="grille", bscale=0.05, bstr=0.2)
    lit = C.pbr("lit_t", "#2A2A3A", 0.25, emit="#FFC47A", estr=2.2)
    for i in range(n):
        x = rnd.uniform(-spread, spread); y = rnd.uniform(200, 1400)
        if abs(x) < 70 and y < 400:
            continue
        w = rnd.uniform(25, 60); h = rnd.uniform(60, 360)
        C.rbox("tw", (w, w * rnd.uniform(0.8, 1.2), h), (x, y, h / 2), mat=glass if rnd.random() < 0.6 else win, bevel=0.0)
        for k in range(int(h // 40)):
            if rnd.random() < 0.5:
                C.rbox("band", (w * 1.002, w * 0.3, 1.5), (x, y - w * 0.36, 20 + k * 40 + rnd.uniform(-5, 5)), mat=lit, bevel=0.0)
    if tall:                                                    # one generic needle-like supertall (~828 m), no real design copied
        x, y = tall
        for k, (w, h0, h1) in enumerate(((70, 0, 300), (52, 300, 520), (36, 520, 680), (22, 680, 780), (6, 780, 828))):
            C.rbox("st", (w, w, h1 - h0), (x, y, (h0 + h1) / 2), mat=glass, bevel=0.0)
            C.rbox("stl", (w * 1.01, w * 0.2, 2.0), (x, y - w * 0.41, h1 - 6), mat=lit, bevel=0.0)


def stack_city(sh, cam, n):
    """'Twenty-three folds: taller than the tallest building on Earth.': plum dusk city; a cream paper column climbs past
    every tower, past a generic 828 m supertall, to ~839 m; the camera tilts up with it."""
    sky("#3A2546", "#F2A65A", 1.0)
    sun = bpy.data.lights.new("sun", "SUN"); sun.energy = 2.5; sun.color = C.srgb("#FFB070")[:3]; sun.angle = math.radians(2)
    so = bpy.data.objects.new("sun", sun); bpy.context.scene.collection.objects.link(so); so.rotation_euler = (math.radians(84), 0, math.radians(-50))
    C.rbox("ground", (8000, 8000, 1), (0, 0, -0.5), mat=C.pbr("ground", "#2A2430", 0.9), bevel=0.0)
    rnd = random.Random(7); towers(rnd, n=90, spread=1200, tall=(300, 1000))
    st = stack("col", Wd=70, D=50, loc=(0, 420, 0), mat=layers_mat("colpaper", 30.0, emit=0.35))
    f1 = W_(sh, "taller", 1.8)
    for f in range(0, n + 1, 2):
        u = ease(min(1.0, f / max(1, f1 + 14)))
        key_obj(st, f, scale=(1, 1, 120 + (839 - 120) * u))
    cam = cam
    cam_move(cam, n, ((-140, -620, 25), (0, 420, 180), 24), ((-140, -620, 60), (0, 420, 720), 22), focus=(0, 420, 400), fstop=16)
    cam.data.clip_end = 20000


def stack_moon(sh, cam, n):
    """'Forty-two? Past the Moon.': black space, the Earth's blue rim below; a thin cream paper line shoots up from it and
    passes the grey Moon (440,000 km vs 384,400 km)."""
    P.world("#000000", 0.0)
    sun = bpy.data.lights.new("sun", "SUN"); sun.energy = 4.0; sun.color = C.srgb("#FFF4E0")[:3]; sun.angle = math.radians(0.6)
    so = bpy.data.objects.new("sun", sun); bpy.context.scene.collection.objects.link(so); so.rotation_euler = (math.radians(70), 0, math.radians(60))
    earth = C.pbr("earth", "#1E4F8C", 0.6, cvar=0.0, color2="#3E6B3A", cscale=3.0)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=60, segments=96, ring_count=48, location=(0, 0, -60)); e = bpy.context.object
    e.data.materials.append(earth); bpy.ops.object.shade_smooth()
    halo = C.ghost("halo", "#7FB8FF", glow=2.5, core=0.0, power=4.0)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=61.5, segments=96, ring_count=48, location=(0, 0, -60)); hb = bpy.context.object
    hb.data.materials.append(halo); bpy.ops.object.shade_smooth()
    moon = C.pbr("moon", "#9A9A96", 0.95, bump="cells", bscale=3.0, bstr=0.6, cvar=0.25, cscale=2.0, color2="#6E6E6A")
    MZ = 384.4
    bpy.ops.mesh.primitive_uv_sphere_add(radius=34, segments=64, ring_count=32, location=(46, 0, MZ)); mo = bpy.context.object
    mo.data.materials.append(moon); bpy.ops.object.shade_smooth()
    rnd = random.Random(5); star = C.emission("star", "#FFFFFF", 6.0)
    for i in range(500):
        th = rnd.uniform(0, 2 * math.pi); ph = rnd.uniform(-0.2, 1.2); R = 3000
        C.cyl("s", rnd.uniform(1.0, 2.6), 0.1, (R * math.cos(th) * math.cos(ph), R * math.sin(th) * math.cos(ph) + 1500, R * math.sin(ph)), mat=star, verts=6)
    st = stack("line", Wd=3.0, D=3.0, loc=(0, 0, -0.5), mat=layers_mat("linepaper", 30.0, emit=1.2))
    fm = W_(sh, "past", 1.6)
    for f in range(0, n + 1, 2):
        u = ease(min(1.0, f / max(1, fm + 10)))
        key_obj(st, f, scale=(1, 1, 5 + (440.0 - 5) * u))
    cam_move(cam, n, ((22, -75, 6), (4, 0, 22), 20), ((70, -160, 290), (24, 0, 395), 26), focus=(15, 0, 300), fstop=32)
    cam.data.clip_end = 20000


def fold_curve(sh, cam, n):
    """'Each fold halves the sheet, and every bend swallows more paper': macro side-slice of a big folded block on a dark desk;
    the nested arcs at the fold edge light up tangerine from the inside out (outer bends need the most paper)."""
    M = mats(); P.world("#101418", 0.1)
    C.rbox("desk_dark", (1.0, 1.0, 0.04), (0, 0, -0.02), mat=M["oak"], bevel=0.0)
    C.rbox("bg", (2, 0.05, 1.2), (0, 0.5, 0.3), mat=M["wall"], bevel=0.0)
    glow = C.pbr("arcglow", PAPER, 0.8, emit=TANG, estr=0.0)
    root, fl, ar = fold_block("big", L=0.10, Wd=0.07, t=0.0016, pairs=22, loc=(0, 0, 0), seed=5, arc_mat=glow)
    b = glow.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    fb = W_(sh, "bend", 2.6)
    b.default_value = 0.0; b.keyframe_insert("default_value", frame=0); b.keyframe_insert("default_value", frame=max(1, fb - 6))
    b.default_value = 2.5; b.keyframe_insert("default_value", frame=fb + 12); b.keyframe_insert("default_value", frame=n)
    C.area("mkey", (-0.25, -0.35, 0.30), (math.radians(55), 0, math.radians(-35)), 0.3, "#FFE2C0", 18)
    C.area("mrim", (0.25, 0.3, 0.25), (math.radians(-60), 0, math.radians(140)), 0.3, "#9FB8FF", 10)
    H = 2 * 22 * 0.0016
    cam_move(cam, n, ((-0.06, -0.20, H / 2 + 0.02), (0.0, 0.0, H / 2), 70), ((-0.03, -0.16, H / 2 + 0.012), (-0.012, 0.0, H / 2), 85),
             focus=(-0.015, -0.035, H / 2), fstop=5.6)


def long_strip(sh, cam, n):
    """'In 2002, a student managed twelve folds… with paper over a kilometre long': a long, plain, empty corridor at night;
    a thin paper strip runs down the middle of the floor and out of sight; low camera glides along it."""
    M = mats(); P.world("#0E1218", 0.1)
    Lc = 160.0
    floor = C.pbr("hallfloor", "#5E5862", 0.6, bump="noise", bscale=40, bstr=0.05, cvar=0.08, cscale=0.5)
    C.rbox("hfloor", (3.2, Lc, 0.02), (0, Lc / 2 - 2, -0.01), mat=floor, bevel=0.0)
    for s in (-1, 1):
        C.rbox("hwall", (0.05, Lc, 3.0), (s * 1.6, Lc / 2 - 2, 1.5), mat=C.pbr("hwall", "#D8D2C4", 0.8, cvar=0.03), bevel=0.0)
        C.rbox("hrail", (0.06, Lc, 0.10), (s * 1.56, Lc / 2 - 2, 0.05), mat=C.pbr("hrail", PLUM, 0.5), bevel=0.0)
    C.rbox("hceil", (3.2, Lc, 0.05), (0, Lc / 2 - 2, 3.0), mat=C.pbr("hceil", "#CFC9BB", 0.9), bevel=0.0)
    lamp = C.emission("hlamp", "#FFF1DC", 6.0)
    for k in range(int(Lc // 4)):
        C.rbox("hl", (0.3, 1.2, 0.02), (0, k * 4.0, 2.97), mat=lamp, bevel=0.0)
    C.rbox("hend", (3.2, 0.05, 3.0), (0, Lc - 2, 1.5), mat=C.pbr("hend", "#3B2747", 0.9), bevel=0.0)
    strip = C.pbr("strip", PAPER, 0.85, bump="noise", bscale=200, bstr=0.2, emit=PAPER, estr=0.35)
    pts = []
    for k in range(400):
        y = -0.6 + k * (Lc - 3) / 399
        pts.append((0.06 * math.sin(y * 0.21), y, 0.002))
    verts, faces = [], []
    for i, (x, y, z) in enumerate(pts):
        verts += [(x - 0.11, y, z), (x + 0.11, y, z)]
        if i:
            a = 2 * i; faces.append((a - 2, a - 1, a + 1, a))
    C.mesh_obj("strip", verts, faces, mat=strip)
    C.cyl("roll", 0.06, 0.24, (0, -0.72, 0.06), rot=(0, math.radians(90), 0), mat=strip, verts=32)
    for s in (-1, 1):
        C.area("hfill", (s * 1.2, 2.0, 2.4), (math.radians(40), 0, math.radians(90 * s)), 1.0, "#FFF1DC", 30)
    cam_move(cam, n, ((0.25, -1.6, 0.35), (0.0, 30, 0.0), 30), ((0.18, 1.8, 0.28), (0.0, 34, 0.0), 30), focus=(0, 6, 0), fstop=2.8)


SHOTS = {f.__name__: f for f in (hook_press, stuck_macro, stack_desk, stack_city, stack_moon, desk_ask, fold_curve, long_strip, loop_press)}


if __name__ == "__main__":
    from sr_shot import run
    run(SHOTS, argv)
