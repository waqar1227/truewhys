"""Style R (close-to-human 3D, audit §6.2) studio + hero props, built in code (no downloads).
Studio cyc in our colours (deep navy -> coral / cream, NOT cyan), soft key/rim lights, and props for
A-016 (onion, knife, board, cells, tear gas, eye macro) and A-017 (ice tray, cloudy cube, freezing
cross-section, lake ice, drink). Every function returns the object(s) so shot code can animate them.
Units: metres, Z up, camera usually looks along +Y.
"""
import math, random
import bpy, bmesh
from mathutils import Vector
from sr_common import srgb, link, mesh_obj, rbox, cyl, tube, pbr, emission, glass, ghost, area, _new

NAVY, NAVY2, CORAL, CREAM, YEL = "#14213D", "#1F3A68", "#FF6B5B", "#FFF1DC", "#FFC93C"


# ------------------------------------------------------------------ studio

def backdrop_mat(top=NAVY, bottom=CORAL, mid=None, glow=0.35):
    """Vertical gradient (world Z) for the cyc: bottom colour on the floor, top colour high on the wall."""
    m, nt, b = _new(f"cyc_{top}_{bottom}")
    N = nt.nodes.new; L = nt.links.new
    tc = N("ShaderNodeTexCoord"); sep = N("ShaderNodeSeparateXYZ"); L(tc.outputs["Generated"], sep.inputs[0])
    ramp = N("ShaderNodeValToRGB"); el = ramp.color_ramp.elements
    el[0].position = 0.12; el[0].color = srgb(bottom); el[1].position = 0.95; el[1].color = srgb(top)
    if mid:
        e = el.new(0.45); e.color = srgb(mid)
    L(sep.outputs["Z"], ramp.inputs["Fac"])
    L(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.9
    L(ramp.outputs["Color"], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = glow
    return m


def studio(top=NAVY, bottom=CORAL, mid=None, width=14.0, depth=6.0, height=7.0, curve=2.2, glow=0.35, y0=2.0):
    """Seamless curved backdrop: floor from y=-depth to y0, then a quarter-circle up into a wall."""
    prof = [(-depth, 0.0)] + [(y0 + curve * math.sin(math.radians(a)), curve - curve * math.cos(math.radians(a))) for a in range(0, 91, 5)] \
        + [(y0 + curve, height)]
    verts, faces = [], []
    xs = (-width / 2, width / 2)
    for x in xs:
        for (y, z) in prof:
            verts.append((x, y, z))
    n = len(prof)
    for i in range(n - 1):
        faces.append((i, i + 1, n + i + 1, n + i))
    o = mesh_obj("cyc", verts, faces, backdrop_mat(top, bottom, mid, glow), smooth=True, sharp=None)
    return o


def lights(target=(0, 0, 1.0), key=900, rim=700, fill=220, warm=True, scale=1.0):
    """Warm key (front-left), cool fill (front-right), two coral/cream rims from behind."""
    def aim(o, t):
        d = Vector(t) - o.location
        o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    s = scale
    out = []
    for name, loc, size, col, en in (("key", (-2.6 * s, -3.0 * s, 3.2 * s), 3.0 * s, "#FFE9D2" if warm else "#FFFFFF", key),
                                     ("fill", (3.0 * s, -2.8 * s, 1.6 * s), 4.0 * s, "#DCE6FF", fill),
                                     ("rimL", (-2.0 * s, 2.4 * s, 2.8 * s), 1.6 * s, "#FFB59E", rim),
                                     ("rimR", (2.0 * s, 2.2 * s, 2.6 * s), 1.6 * s, "#FFF1DC", rim * 0.7)):
        o = area(name, Vector(target) + Vector(loc), (0, 0, 0), size, col, en * s * s)
        aim(o, target); out.append(o)
    return out


def world(color=NAVY, strength=0.25):
    w = bpy.data.worlds.new("w"); bpy.context.scene.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = srgb(color); bg.inputs[1].default_value = strength
    return w


def counter(loc=(0, 0, 0), w=1.6, d=0.7, h=0.92, top="#F4EEE4", body=NAVY2, top2="#E8DDCC"):
    """Simple kitchen counter block; loc = front-centre of the floor footprint. Returns (obj, top_z)."""
    x, y, z = loc
    b = rbox("counter_body", (w, d, h - 0.04), (x, y + d / 2, z + (h - 0.04) / 2), mat=pbr("counter_body", body, 0.55, cvar=0.04), bevel=0.01)
    t = rbox("counter_top", (w + 0.04, d + 0.04, 0.04), (x, y + d / 2, z + h - 0.02), mat=pbr("counter_top", top, 0.3, cvar=0.06, color2=top2, cscale=9), bevel=0.006)
    return (b, t), z + h


# ------------------------------------------------------------------ onion

def _onion_r(t):
    """Onion profile radius at t in [0, 1] (0 = root, 1 = tip), unit max radius."""
    s = math.sin(math.pi * min(1.0, t * 1.08)) ** 0.75 if t < 0.92 else 0.0
    if t > 0.7:
        s *= 1 - 0.55 * ((t - 0.7) / 0.3) ** 1.3
    return max(s, 0.0)


def onion_mats():
    skin = pbr("onion_skin", "#6E3608", 0.5, bump="noise", bscale=260, bstr=0.35, color2="#A8611A", cscale=14, sheen=0.6, rvar=0.15,
               stretch=(1, 1, 0.18))
    # cut face: concentric rings (spherical wave on object coords), creamy, translucent
    m, nt, b = _new("onion_flesh")
    N = nt.nodes.new; L = nt.links.new
    tc = N("ShaderNodeTexCoord"); mp = N("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1.0, 1.0, 0.62); mp.inputs["Location"].default_value = (0, 0, -0.022)
    L(tc.outputs["Object"], mp.inputs["Vector"])
    wv = N("ShaderNodeTexWave"); wv.wave_type = "RINGS"; wv.rings_direction = "SPHERICAL"; wv.inputs["Scale"].default_value = 95.0
    wv.inputs["Distortion"].default_value = 0.3; wv.wave_profile = "SAW"
    L(mp.outputs["Vector"], wv.inputs["Vector"])
    ramp = N("ShaderNodeValToRGB"); e = ramp.color_ramp.elements
    e[0].position = 0.0; e[0].color = srgb("#FFFBEA"); e[1].position = 0.86; e[1].color = srgb("#F4EBC6")
    e2 = ramp.color_ramp.elements.new(0.93); e2.color = srgb("#D9CF9A")
    L(wv.outputs["Fac"], ramp.inputs["Fac"]); L(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.25; b.inputs["Coat Weight"].default_value = 0.6
    b.inputs["Subsurface Weight"].default_value = 0.5; b.inputs["Subsurface Radius"].default_value = (1.0, 0.9, 0.6); b.inputs["Subsurface Scale"].default_value = 0.01
    bp = N("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.25; bp.inputs["Distance"].default_value = 0.002
    L(wv.outputs["Fac"], bp.inputs["Height"]); L(bp.outputs["Normal"], b.inputs["Normal"])
    return skin, m


def onion(loc=(0, 0, 0), R=0.045, H=0.085, cut=True, gap=0.0, name="onion"):
    """Brown onion standing on its root. cut=True -> two halves split along the YZ plane (cut faces toward +/-X),
    separated by `gap` metres. Returns list of halves (or [whole])."""
    skin, flesh = onion_mats()
    nz, na = 28, 48
    out = []
    halves = ((-1, "L"), (1, "R")) if cut else ((0, "W"),)
    for side, tag in halves:
        verts, faces = [], []
        a0, a1 = (math.pi / 2, 3 * math.pi / 2) if side < 0 else ((-math.pi / 2, math.pi / 2) if side > 0 else (0, 2 * math.pi))
        na_ = na // 2 if side else na
        for i in range(nz + 1):
            t = i / nz; r = R * _onion_r(t); z = H * t
            for j in range(na_ + 1):
                a = a0 + (a1 - a0) * j / na_
                verts.append((r * math.cos(a), r * math.sin(a), z))
        row = na_ + 1
        for i in range(nz):
            for j in range(na_ if side else na_):
                faces.append((i * row + j, i * row + j + 1, (i + 1) * row + j + 1, (i + 1) * row + j))
        nskin = len(faces)
        if side:  # flat cut face in the YZ plane, fan from the axis
            base = len(verts)
            for i in range(nz + 1):
                t = i / nz
                verts.append((0.0, 0.0, H * t))
            for i in range(nz):
                f0, f1 = i * row, (i + 1) * row
                l0, l1 = i * row + na_, (i + 1) * row + na_
                faces.append((base + i, base + i + 1, f1, f0) if side > 0 else (base + i, f0, f1, base + i + 1))
                faces.append((base + i, l0, l1, base + i + 1) if side > 0 else (base + i, base + i + 1, l1, l0))
        o = mesh_obj(f"{name}_{tag}", verts, faces, skin, smooth=True, sharp=50, fix_normals=True)
        o.data.materials.append(flesh)
        for k, p in enumerate(o.data.polygons):
            if k >= nskin:
                p.material_index = 1
                p.use_smooth = False
        o.location = (loc[0] + side * gap / 2, loc[1], loc[2])
        out.append(o)
    # little root tuft + dry tip
    tip = tube(f"{name}_tip", [(loc[0], loc[1], loc[2] + H * 0.9), (loc[0] + 0.003, loc[1], loc[2] + H * 1.12)], 0.004,
               mat=pbr("onion_tip", "#9A6A35", 0.7))
    out.append(tip)
    return out


def knife(loc=(0, 0, 0), rot=(0, 0, 0), L_=0.22, name="knife"):
    """Chef's knife: steel blade along +X from the bolster, dark handle along -X. Pivot at the bolster."""
    steel = pbr("steel", "#D9DEE4", 0.18, metal=1.0, bump="noise", bscale=900, bstr=0.05)
    hd = pbr("handle", "#232638", 0.35, coat=0.4)
    bl = []
    n = 24
    verts = []
    for i in range(n + 1):
        t = i / n; x = L_ * t
        hgt = 0.045 * (1 - t ** 2.2) + 0.004
        verts += [(x, -0.0012, 0.0), (x, 0.0012, 0.0), (x, -0.0002, -hgt), (x, 0.0002, -hgt)]
    faces = []
    for i in range(n):
        a = i * 4; b = a + 4
        faces += [(a, b, b + 2, a + 2), (a + 1, a + 3, b + 3, b + 1), (a, a + 1, b + 1, b), (a + 2, b + 2, b + 3, a + 3)]
    blade = mesh_obj(f"{name}_blade", verts, faces, steel, smooth=True, sharp=30, fix_normals=True)
    handle = rbox(f"{name}_handle", (0.12, 0.022, 0.026), (-0.062, 0, -0.012), mat=hd, bevel=0.009, seg=4)
    piv = bpy.data.objects.new(name, None); link(piv)
    for o in (blade, handle):
        o.parent = piv
    piv.location = loc; piv.rotation_euler = rot
    return piv


def board(loc=(0, 0, 0), size=(0.42, 0.28, 0.024)):
    return rbox("board", size, (loc[0], loc[1], loc[2] + size[2] / 2), mat=pbr("board", "#C89A62", 0.5, bump="noise", bscale=40, bstr=0.15,
                color2="#B07F49", cscale=6, stretch=(1, 6, 1)), bevel=0.008)


# ------------------------------------------------------------------ cells (cross-section macro)

def cells(loc=(0, 0, 0), nx=5, nz=4, s=0.5, seed=3):
    """Macro 'inside the onion': a wall of translucent cream cells (rounded boxes), each holding an orange
    blob (the sulphur chemical, in the cell fluid) and a separate green sac (the enzyme, in the vacuole).
    Returns dict(cells=[...], chem=[...], enz=[...], walls=[...]) for animation."""
    rnd = random.Random(seed)
    wall = pbr("cellwall", "#FFF3D6", 0.35, sss=0.6, sss_radius=(1, 0.9, 0.5), sss_scale=0.2, coat=0.5)
    chem = pbr("chem", "#FF8A3D", 0.3, emit="#FF8A3D", estr=0.6, sss=0.3)
    enz = pbr("enz", "#59D18C", 0.3, emit="#59D18C", estr=0.6, sss=0.3)
    sac = glass("vacuole", tint=(0.8, 1.0, 0.85), refl=0.12)
    out = dict(cells=[], chem=[], enz=[], sacs=[])
    for i in range(nx):
        for k in range(nz):
            x = loc[0] + (i - (nx - 1) / 2) * s * 1.02 + (s * 0.5 if k % 2 else 0)
            z = loc[2] + k * s * 0.62
            c = rbox(f"cell_{i}_{k}", (s * 0.96, s * 0.5, s * 0.58), (x, loc[1], z), mat=wall, bevel=s * 0.12, seg=4)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=s * 0.13, location=(x - s * 0.2, loc[1] - s * 0.28, z - s * 0.05), segments=20, ring_count=12)
            ch = bpy.context.object; ch.name = f"chem_{i}_{k}"; ch.data.materials.append(chem)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=s * 0.15, location=(x + s * 0.18, loc[1] - s * 0.28, z + s * 0.04), segments=20, ring_count=12)
            en = bpy.context.object; en.name = f"enz_{i}_{k}"; en.data.materials.append(enz)
            for o in (ch, en):
                for p in o.data.polygons:
                    p.use_smooth = True
                o.scale = (1.0, 0.7, 0.8 + rnd.random() * 0.3)
            out["cells"].append(c); out["chem"].append(ch); out["enz"].append(en)
    return out


def wisp(name, color, alpha=0.35, glow=1.2):
    """Soft gas blob: denser and glowing in the middle, fading to nothing at the edge (no bubble rim)."""
    from sr_common import _M
    key = ("W", name, str(color), alpha, glow)
    if key in _M:
        return _M[key]
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    lw = N("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.5
    pw = N("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 3.0; L(lw.outputs["Facing"], pw.inputs[0])
    inv = N("ShaderNodeMath"); inv.operation = "SUBTRACT"; inv.inputs[0].default_value = 1.0; L(pw.outputs[0], inv.inputs[1])
    mul = N("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = alpha; L(inv.outputs[0], mul.inputs[0])
    tr = N("ShaderNodeBsdfTransparent")
    em = N("ShaderNodeEmission"); em.inputs["Color"].default_value = srgb(color); em.inputs["Strength"].default_value = glow
    mx = N("ShaderNodeMixShader"); L(mul.outputs[0], mx.inputs["Fac"]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2])
    o = N("ShaderNodeOutputMaterial"); L(mx.outputs[0], o.inputs["Surface"])
    _M[key] = m
    return m


def gas_puffs(origin=(0, 0, 0), n=60, spread=0.06, seed=7, color="#C8F5D2", size=0.012):
    """Soft glowing gas wisps for the tear gas (big, see-through blobs); shot code moves them (returns list of objects)."""
    rnd = random.Random(seed)
    m = wisp("gas", color, alpha=0.13, glow=1.6)
    out = []
    for i in range(n):
        bpy.ops.mesh.primitive_ico_sphere_add(radius=size * (1.0 + 1.2 * rnd.random()), subdivisions=3,
                                              location=(origin[0] + rnd.gauss(0, spread), origin[1] + rnd.gauss(0, spread * 0.6), origin[2]))
        o = bpy.context.object; o.name = f"gas_{i}"; o.data.materials.append(m)
        for p in o.data.polygons:
            p.use_smooth = True
        o["seed"] = rnd.random()
        out.append(o)
    return out


# ------------------------------------------------------------------ eye macro (stylised, not a real person's eye)

def eye_macro(loc=(0, 0, 0), R=0.5, iris="#5B8A3C", name="eye"):
    """Big stylised eyeball facing -Y with lids, cornea dome, X-ray nerve lines (hidden until shown) and a tear gland.
    Returns dict of parts."""
    x, y, z = loc
    m, nt, b = _new(f"{name}_ballmat")
    N = nt.nodes.new; L = nt.links.new
    tc = N("ShaderNodeTexCoord"); sp = N("ShaderNodeSeparateXYZ"); L(tc.outputs["Object"], sp.inputs[0])
    cb = N("ShaderNodeCombineXYZ"); L(sp.outputs["X"], cb.inputs["X"]); L(sp.outputs["Z"], cb.inputs["Z"])
    ln = N("ShaderNodeVectorMath"); ln.operation = "LENGTH"; L(cb.outputs[0], ln.inputs[0])
    dv = N("ShaderNodeMath"); dv.operation = "DIVIDE"; dv.inputs[1].default_value = R; L(ln.outputs["Value"], dv.inputs[0])
    front = N("ShaderNodeMath"); front.operation = "LESS_THAN"; front.inputs[1].default_value = 0.0; L(sp.outputs["Y"], front.inputs[0])
    mxd = N("ShaderNodeMath"); mxd.operation = "MULTIPLY_ADD"; L(front.outputs[0], mxd.inputs[0]); mxd.inputs[1].default_value = -1.0; mxd.inputs[2].default_value = 1.0
    d2 = N("ShaderNodeMath"); d2.operation = "ADD"; L(dv.outputs[0], d2.inputs[0]); L(mxd.outputs[0], d2.inputs[1])   # back half -> d >= 1 (white)
    wv = N("ShaderNodeTexWave"); wv.wave_type = "RINGS"; wv.rings_direction = "SPHERICAL"; wv.inputs["Scale"].default_value = 2.0
    wv.inputs["Distortion"].default_value = 8.0; wv.inputs["Detail"].default_value = 4.0; L(tc.outputs["Object"], wv.inputs["Vector"])
    ramp = N("ShaderNodeValToRGB"); e = ramp.color_ramp.elements
    e[0].position = 0.0; e[0].color = (0.005, 0.005, 0.005, 1); e[1].position = 0.17; e[1].color = (0.005, 0.005, 0.005, 1)
    for pos, col in ((0.19, "#2E4A1E"), (0.33, iris), (0.40, "#3A5A28"), (0.425, "#1A2212"), (0.455, "#FBF6F0"), (0.85, "#FBF2EC"), (0.99, "#F2C9C0")):
        el = ramp.color_ramp.elements.new(pos); el.color = srgb(col)
    L(d2.outputs[0], ramp.inputs["Fac"]); L(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.3; b.inputs["Subsurface Weight"].default_value = 0.25; b.inputs["Subsurface Scale"].default_value = 0.02
    bp = N("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.15; L(wv.outputs["Fac"], bp.inputs["Height"]); L(bp.outputs["Normal"], b.inputs["Normal"])
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R, location=loc, segments=64, ring_count=32)
    ball = bpy.context.object; ball.name = f"{name}_ball"; ball.data.materials.append(m)
    for p in ball.data.polygons:
        p.use_smooth = True
    ir = ball
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R * 1.015, location=loc, segments=64, ring_count=32)
    cor = bpy.context.object; cor.name = f"{name}_cornea"; cor.data.materials.append(glass("cornea", refl=0.25, rough=0.0))
    for p in cor.data.polygons:
        p.use_smooth = True
    # face plate: curved skin shell in front of the eye with an almond-shaped opening (lids = its edges)
    skin = pbr("lidskin", "#E3A27E", 0.5, sss=0.35, sss_scale=0.05, bump="noise", bscale=40, bstr=0.08)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R * 2.6, location=(x, y + R * 1.55, z), segments=64, ring_count=32)
    plate = bpy.context.object; plate.name = f"{name}_face"; plate.data.materials.append(skin)
    bm = bmesh.new(); bm.from_mesh(plate.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > -R * 1.2], context="VERTS"); bm.to_mesh(plate.data); bm.free()
    for p in plate.data.polygons:
        p.use_smooth = True
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(x, y - R, z), segments=48, ring_count=24)
    hole = bpy.context.object; hole.scale = (R * 1.05, R * 2.0, R * 0.62); hole.hide_render = True; hole.hide_viewport = True
    bo = plate.modifiers.new("almond", "BOOLEAN"); bo.object = hole; bo.operation = "DIFFERENCE"
    sol = plate.modifiers.new("thick", "SOLIDIFY"); sol.thickness = R * 0.12
    sub = plate.modifiers.new("soft", "SUBSURF"); sub.levels = 1; sub.render_levels = 2
    lids = [plate, hole]
    # nerves: glowing thin tubes across the cornea surface (show by animating the ghost glow)
    nerve = emission("nerve", "#FFE36E", 0.0)
    nerves = []
    rnd = random.Random(5)
    for i in range(9):
        a = rnd.uniform(0, 2 * math.pi); pts = []
        for k in range(6):
            r = R * (0.15 + 0.13 * k); aa = a + 0.25 * math.sin(k * 1.3 + i)
            px, pz = r * math.cos(aa), r * math.sin(aa)
            py = -math.sqrt(max(R * R * 1.06 - px * px - pz * pz, 0.0))
            pts.append((x + px, y + py - R * 0.03, z + pz))
        nerves.append(tube(f"{name}_nerve{i}", pts, R * 0.008, mat=nerve, n=6))
    gl = pbr("gland", "#F6A9A0", 0.4, sss=0.5, sss_scale=0.05)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R * 0.22, location=(x - R * 0.85, y - R * 0.2, z + R * 0.7), segments=24, ring_count=16)
    gland = bpy.context.object; gland.name = f"{name}_gland"; gland.data.materials.append(gl); gland.scale = (1.4, 0.8, 0.7)
    return dict(ball=ball, iris=ir, cornea=cor, lids=lids, nerves=nerves, nerve_mat=nerve, gland=gland)


def tear(loc, r=0.03, name="tear"):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=24, ring_count=16)
    o = bpy.context.object; o.name = name; o.data.materials.append(pbr("tearwater", "#DDF2FF", 0.02, coat=1.0))
    m = o.active_material; m.node_tree.nodes["Principled BSDF"].inputs["Transmission Weight"].default_value = 1.0
    o.scale = (1, 0.8, 1.35)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def medal(loc=(0, 0, 0), r=0.06):
    """Our own gold prize medal with an onion relief (no real award logo)."""
    gold = pbr("gold", "#E8B33A", 0.22, metal=1.0, bump="noise", bscale=500, bstr=0.05)
    d = cyl("medal", r, r * 0.12, loc, (math.radians(90), 0, 0), mat=gold, verts=64, bevel=r * 0.03)
    rel = onion((loc[0], loc[1] - r * 0.08, loc[2] - r * 0.45), R=r * 0.38, H=r * 0.8, cut=False, name="medal_onion")
    for o in rel:
        o.data.materials.clear(); o.data.materials.append(gold); o.scale = (1, 0.25, 1)
    rib = rbox("ribbon", (r * 0.7, r * 0.05, r * 1.6), (loc[0], loc[1] + r * 0.05, loc[2] + r * 1.6), mat=pbr("ribbon", CORAL, 0.6, sheen=0.5), bevel=0.002)
    return [d, rib] + rel


# ------------------------------------------------------------------ ice

def ice_mat(name="ice", cloud=0.0):
    """Ice that lets light through (transparent + fresnel gloss + a little refraction, so shadow rays reach the inside)
    and, with cloud > 0, a white scattering core that is densest at the centre (trapped air)."""
    key = ("ICE", name, cloud)
    from sr_common import _M
    if key in _M:
        return _M[key]
    m = bpy.data.materials.new(f"{name}_{cloud}"); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N("ShaderNodeOutputMaterial")
    tr = N("ShaderNodeBsdfTransparent"); tr.inputs["Color"].default_value = (0.93, 0.98, 1.0, 1)
    rf = N("ShaderNodeBsdfRefraction"); rf.inputs["IOR"].default_value = 1.31; rf.inputs["Roughness"].default_value = 0.02
    gl = N("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.03
    nz = N("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 160
    bp = N("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.05; L(nz.outputs["Fac"], bp.inputs["Height"])
    for n_ in (rf, gl):
        L(bp.outputs["Normal"], n_.inputs["Normal"])
    m1 = N("ShaderNodeMixShader"); m1.inputs["Fac"].default_value = 0.25; L(tr.outputs[0], m1.inputs[1]); L(rf.outputs[0], m1.inputs[2])
    fr = N("ShaderNodeLayerWeight"); fr.inputs["Blend"].default_value = 0.2
    mr = N("ShaderNodeMapRange"); mr.inputs["To Min"].default_value = 0.04; mr.inputs["To Max"].default_value = 0.7; L(fr.outputs["Fresnel"], mr.inputs["Value"])
    m2 = N("ShaderNodeMixShader"); L(mr.outputs["Result"], m2.inputs["Fac"]); L(m1.outputs[0], m2.inputs[1]); L(gl.outputs[0], m2.inputs[2])
    L(m2.outputs[0], out.inputs["Surface"])
    if cloud > 0:
        tc = N("ShaderNodeTexCoord"); grad = N("ShaderNodeTexGradient"); grad.gradient_type = "SPHERICAL"
        mp = N("ShaderNodeMapping"); mp.inputs["Location"].default_value = (-0.5, -0.5, -0.5)
        L(tc.outputs["Generated"], mp.inputs["Vector"])
        sc2 = N("ShaderNodeVectorMath"); sc2.operation = "SCALE"; sc2.inputs["Scale"].default_value = 2.3; L(mp.outputs["Vector"], sc2.inputs[0])
        L(sc2.outputs[0], grad.inputs["Vector"])
        pw = N("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 2.5; L(grad.outputs["Fac"], pw.inputs[0])
        mul = N("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = cloud * 400.0; L(pw.outputs[0], mul.inputs[0])
        vs = N("ShaderNodeVolumePrincipled"); vs.inputs["Color"].default_value = (1, 1, 1, 1)
        L(mul.outputs[0], vs.inputs["Density"]); L(vs.outputs[0], out.inputs["Volume"])
    _M[key] = m
    return m


def ice_cube(loc=(0, 0, 0), s=0.03, cloud=0.0, bubbles=0, seed=1, name="cube"):
    o = rbox(name, (s, s, s * 0.9), loc, mat=ice_mat("ice", cloud), bevel=s * 0.18, seg=4)
    bs = []
    if bubbles:
        rnd = random.Random(seed)
        bm = pbr("bubble", "#FFFFFF", 0.1, emit="#FFFFFF", estr=0.4)
        for i in range(bubbles):
            r = s * 0.22 * rnd.random() ** 0.6
            th, ph = rnd.uniform(0, 2 * math.pi), math.acos(rnd.uniform(-1, 1))
            p = (loc[0] + r * math.sin(ph) * math.cos(th), loc[1] + r * math.sin(ph) * math.sin(th), loc[2] + r * math.cos(ph) * 0.8)
            bpy.ops.mesh.primitive_ico_sphere_add(radius=s * rnd.uniform(0.006, 0.02), subdivisions=1, location=p)
            b = bpy.context.object; b.name = f"{name}_bub{i}"; b.data.materials.append(bm); b.parent = o; b.matrix_parent_inverse = o.matrix_world.inverted()
            bs.append(b)
    return o, bs


def ice_tray(loc=(0, 0, 0), nx=4, ny=2, cell=0.034, water=0.0, cubes=True, cloud=0.9, name="tray"):
    """Plastic tray (coral) with nx*ny cells. water: 0 = empty, 0..1 fill (liquid look) or cubes=True for frozen cubes."""
    pl = pbr("tray", CORAL, 0.35, coat=0.3)
    W, D = nx * cell + 0.012, ny * cell + 0.012
    base = rbox(name, (W, D, cell * 0.85), (loc[0], loc[1], loc[2] + cell * 0.425), mat=pl, bevel=0.004)
    items = []
    for i in range(nx):
        for j in range(ny):
            cx = loc[0] + (i - (nx - 1) / 2) * cell; cy = loc[1] + (j - (ny - 1) / 2) * cell
            hole = rbox(f"{name}_hole{i}{j}", (cell * 0.86, cell * 0.86, cell * 0.8), (cx, cy, loc[2] + cell * 0.5), bevel=0.004)
            bo = base.modifiers.new(f"h{i}{j}", "BOOLEAN"); bo.object = hole; bo.operation = "DIFFERENCE"; hole.hide_render = True; hole.hide_viewport = True
            if cubes:
                c, _ = ice_cube((cx, cy, loc[2] + cell * 0.45), cell * 0.84, cloud=cloud, name=f"{name}_cube{i}{j}")
                items.append(c)
            elif water > 0:
                w = rbox(f"{name}_water{i}{j}", (cell * 0.84, cell * 0.84, cell * 0.7 * water), (cx, cy, loc[2] + cell * 0.12 + cell * 0.35 * water),
                         mat=pbr("water", "#CFEFFF", 0.02, coat=1.0), bevel=0.003)
                w.active_material.node_tree.nodes["Principled BSDF"].inputs["Transmission Weight"].default_value = 1.0
                items.append(w)
    return base, items


def freeze_section(loc=(0, 0, 0), s=1.0, name="xsec"):
    """Cut-open ice cube seen face-on (camera looks +Y): pale ice square, a dark-blue liquid core square in front of it
    that the shot shrinks (freezing from the outside in), layer lines left behind, and white air dots kept inside the core.
    Returns dict(ice, core, air=[...], frame). Shot code: core.scale -> k, air positions *= k (crowding to the centre)."""
    ice = rbox(f"{name}_ice", (s, s * 0.06, s * 0.92), loc, mat=pbr("xice", "#D9F1FF", 0.15, emit="#BFE6FF", estr=0.35, coat=0.8,
               bump="noise", bscale=12, bstr=0.08), bevel=s * 0.05)
    core = rbox(f"{name}_core", (s * 0.9, s * 0.02, s * 0.82), (loc[0], loc[1] - s * 0.035, loc[2]),
                mat=pbr("xliquid", "#1E5FA8", 0.1, emit="#1A4F8F", estr=0.6, coat=1.0), bevel=s * 0.04)
    rnd = random.Random(11)
    am = pbr("air", "#FFFFFF", 0.2, emit="#FFFFFF", estr=1.5)
    air = []
    for i in range(70):
        p = (rnd.uniform(-0.42, 0.42) * s, -s * 0.05, rnd.uniform(-0.38, 0.38) * s)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=s * rnd.uniform(0.008, 0.017), subdivisions=2, location=(loc[0] + p[0], loc[1] + p[1], loc[2] + p[2]))
        b = bpy.context.object; b.name = f"{name}_air{i}"; b.data.materials.append(am); b["home"] = p
        for f in b.data.polygons:
            f.use_smooth = True
        air.append(b)
    frame = rbox(f"{name}_frame", (s * 1.08, s * 0.04, s * 1.0), (loc[0], loc[1] + s * 0.05, loc[2]), mat=pbr("xframe", NAVY2, 0.5), bevel=s * 0.05)
    return dict(ice=ice, core=core, air=air, frame=frame, loc=loc, s=s)


def lake(loc=(0, 0, 0), w=3.0, d=2.0, ice_t=0.12):
    """Cut-away block of a frozen lake: clear ice slab on top of dark water, air bubbles escaping above."""
    water = rbox("lakewater", (w, d, 0.8), (loc[0], loc[1], loc[2] - 0.4 - ice_t), mat=pbr("lakewater", "#103A5C", 0.1, coat=0.8, emit="#0E2F4D", estr=0.2), bevel=0.02)
    ice = rbox("lakeice", (w, d, ice_t), (loc[0], loc[1], loc[2] - ice_t / 2), mat=ice_mat("lakeice", 0.0), bevel=0.01)
    snow = rbox("lakebank", (w * 0.2, d, 0.3), (loc[0] - w * 0.6, loc[1], loc[2] - 0.15), mat=pbr("snow", "#F6F8FB", 0.6, bump="noise", bscale=30, bstr=0.2), bevel=0.05)
    return water, ice, snow


def drink(loc=(0, 0, 0), r=0.04, h=0.11, cubes=3, cloud=0.9):
    """Tumbler with an amber soft drink and cubes (cloudy or clear)."""
    g = cyl("tumbler", r, h, (loc[0], loc[1], loc[2] + h / 2), mat=glass("tumbler", refl=0.1), verts=48, r2=r * 0.9)
    liq_m = pbr("cola", "#B5651D", 0.05, coat=1.0)
    liq_m.node_tree.nodes["Principled BSDF"].inputs["Transmission Weight"].default_value = 0.85
    liq = cyl("liquid", r * 0.93, h * 0.7, (loc[0], loc[1], loc[2] + h * 0.36), mat=liq_m, verts=48, r2=r * 0.85)
    cs = []
    for i in range(cubes):
        c, _ = ice_cube((loc[0] + 0.012 * math.cos(i * 2.1), loc[1] + 0.012 * math.sin(i * 2.1), loc[2] + h * 0.62 + i * 0.012), r * 0.75, cloud=cloud, name=f"dcube{i}")
        c.rotation_euler = (0.2 * i, 0.3, 0.5 * i)
        cs.append(c)
    return g, liq, cs
