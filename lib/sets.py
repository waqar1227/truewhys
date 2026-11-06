"""TrueWhys 3D toon sets, built procedurally with bpy (Blender 5).

build(set_id, variant) clears the scene and builds one set. Sets are reusable library assets:
  square   (variants: day, dusk, alpine)   medieval town square with town hall, houses, scaffold
  court    (variants: town, church)       stone courtroom / church court
  land     (variants: barley, vineyard, night)  countryside
  study    (variant: day)                  Wy's study (channel home set)
Coordinates: metres, Z up, characters stand on z=0. Camera marks live in shots (plan).
"""
import math, random
import bpy
from mathutils import Vector

R = random.Random(7)

# ----------------------------------------------------------------- helpers

def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def hexrgb(h, a=1.0):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return (*c, a)


_MATS = {}


def mat(name, color, rough=0.7, noise=0.12, emit=None, emit_strength=0.0, metal=0.0, scale=3.0, bricks=None):
    key = (name, color, rough, noise, emit, emit_strength, str(bricks))
    if key in _MATS:
        return _MATS[key]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    base = hexrgb(color)
    if noise > 0 or bricks:
        tc = nt.nodes.new("ShaderNodeTexCoord")
        ramp_in = None
        if bricks:
            br = nt.nodes.new("ShaderNodeTexBrick")
            br.inputs["Scale"].default_value = bricks.get("scale", 4.0) * bricks.get("k", 0.4)
            br.inputs["Mortar Size"].default_value = bricks.get("mortar", 0.02)
            br.inputs["Color1"].default_value = base
            br.inputs["Color2"].default_value = hexrgb(bricks.get("c2", color))
            br.inputs["Mortar"].default_value = hexrgb(bricks.get("mortar_c", "#6B5B4B"))
            br.offset = 0.5
            if "w" in bricks:
                br.inputs["Brick Width"].default_value = bricks["w"]
                br.inputs["Row Height"].default_value = bricks.get("h", 0.25)
            # world-space projection: walls use (x+y, z), floors/roofs use (x, y)
            geo = nt.nodes.new("ShaderNodeNewGeometry")
            sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Position"], sp.inputs["Vector"])
            add = nt.nodes.new("ShaderNodeMath"); add.operation = "ADD"
            nt.links.new(sp.outputs["X"], add.inputs[0]); nt.links.new(sp.outputs["Y"], add.inputs[1])
            cv = nt.nodes.new("ShaderNodeCombineXYZ"); nt.links.new(add.outputs[0], cv.inputs["X"]); nt.links.new(sp.outputs["Z"], cv.inputs["Y"])
            ch = nt.nodes.new("ShaderNodeCombineXYZ"); nt.links.new(sp.outputs["X"], ch.inputs["X"]); nt.links.new(sp.outputs["Y"], ch.inputs["Y"])
            sn = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Normal"], sn.inputs["Vector"])
            ab = nt.nodes.new("ShaderNodeMath"); ab.operation = "ABSOLUTE"; nt.links.new(sn.outputs["Z"], ab.inputs[0])
            gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.5
            nt.links.new(ab.outputs[0], gt.inputs[0])
            mv = nt.nodes.new("ShaderNodeMix"); mv.data_type = "VECTOR"
            nt.links.new(gt.outputs[0], mv.inputs["Factor"])
            nt.links.new(cv.outputs["Vector"], mv.inputs[4]); nt.links.new(ch.outputs["Vector"], mv.inputs[5])
            nt.links.new(mv.outputs[1], br.inputs["Vector"])
            ramp_in = br.outputs["Color"]
        nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = scale
        nz.inputs["Detail"].default_value = 3.0
        nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.blend_type = "MULTIPLY"
        mix.inputs["Factor"].default_value = noise
        if ramp_in is not None:
            nt.links.new(ramp_in, mix.inputs["A"])
        else:
            mix.inputs["A"].default_value = base
        mr = nt.nodes.new("ShaderNodeMapRange")
        mr.inputs["To Min"].default_value = 0.75
        mr.inputs["To Max"].default_value = 1.15
        nt.links.new(nz.outputs["Fac"], mr.inputs["Value"])
        cr = nt.nodes.new("ShaderNodeCombineColor")
        for s in ("Red", "Green", "Blue"):
            nt.links.new(mr.outputs["Result"], cr.inputs[s])
        nt.links.new(cr.outputs["Color"], mix.inputs["B"])
        nt.links.new(mix.outputs["Result"], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = base
    if emit:
        bsdf.inputs["Emission Color"].default_value = hexrgb(emit)
        bsdf.inputs["Emission Strength"].default_value = emit_strength
    _MATS[key] = m
    return m


def obj_from(o, m, bevel=0.0, seg=3, smooth=True):
    if m is not None:
        o.data.materials.clear()
        o.data.materials.append(m)
    if bevel > 0:
        b = o.modifiers.new("bev", "BEVEL")
        b.width = bevel
        b.segments = seg
        b.limit_method = "ANGLE"
    if smooth and hasattr(o.data, "polygons"):
        for p in o.data.polygons:
            p.use_smooth = True
    return o


def box(loc, size, m, bevel=0.04, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.active_object
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    return obj_from(o, m, bevel)


def cyl(loc, r, h, m, verts=24, bevel=0.02, rot=(0, 0, 0), r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=h, location=loc, rotation=rot)
    o = bpy.context.active_object
    return obj_from(o, m, bevel)


def sphere(loc, r, m, scale=(1, 1, 1), sub=3):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=r, location=loc)
    o = bpy.context.active_object
    o.scale = scale
    return obj_from(o, m, 0)


def prism_roof(loc, w, d, h, m, overhang=0.35, rot_z=0):
    """Gabled roof, ridge along X (width w), depth d."""
    import bmesh
    me = bpy.data.meshes.new("roof")
    bm = bmesh.new()
    W, D = w / 2 + overhang, d / 2 + overhang
    v = [bm.verts.new(p) for p in [(-W, -D, 0), (W, -D, 0), (W, D, 0), (-W, D, 0), (-W, 0, h), (W, 0, h)]]
    for f in [(0, 1, 5, 4), (2, 3, 4, 5), (0, 4, 3), (1, 2, 5), (0, 3, 2, 1)]:
        bm.faces.new([v[i] for i in f])
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("roof", me)
    bpy.context.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (0, 0, rot_z)
    sol = o.modifiers.new("sol", "SOLIDIFY")
    sol.thickness = 0.18
    return obj_from(o, m, 0.03, smooth=False)


def plane(loc, size, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.scale = (size[0], size[1], 1)
    bpy.ops.object.transform_apply(scale=True)
    return obj_from(o, m, 0, smooth=False)


def world(top="#8FD3F4", horizon="#FFE9C7", strength=1.0):
    w = bpy.data.worlds.new("w")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sep.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = hexrgb(horizon)
    ramp.color_ramp.elements[1].position = 0.35
    ramp.color_ramp.elements[1].color = hexrgb(top)
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength


def sun(rot_deg, color="#FFE2B8", energy=4.0, angle=4.0):
    d = bpy.data.lights.new("sun", "SUN")
    d.energy = energy
    d.color = hexrgb(color)[:3]
    d.angle = math.radians(angle)
    o = bpy.data.objects.new("sun", d)
    bpy.context.collection.objects.link(o)
    o.rotation_euler = [math.radians(a) for a in rot_deg]
    return o


def area(loc, rot_deg, size, color, energy):
    d = bpy.data.lights.new("area", "AREA")
    d.size = size
    d.energy = energy
    d.color = hexrgb(color)[:3]
    o = bpy.data.objects.new("area", d)
    bpy.context.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = [math.radians(a) for a in rot_deg]
    return o


def point(loc, color, energy, radius=0.2):
    d = bpy.data.lights.new("pt", "POINT")
    d.energy = energy
    d.color = hexrgb(color)[:3]
    d.shadow_soft_size = radius
    o = bpy.data.objects.new("pt", d)
    bpy.context.collection.objects.link(o)
    o.location = loc
    return o


def tree(loc, s=1.0, leaf="#5E9E4A"):
    x, y, z = loc
    cyl((x, y, z + 1.0 * s), 0.18 * s, 2.0 * s, mat("trunk", "#6B4A32", noise=0.2))
    lm = mat("leaf" + leaf, leaf, rough=0.8, noise=0.25, scale=1.5)
    for dx, dy, dz, r in [(0, 0, 2.6, 1.2), (0.6, 0.2, 2.2, 0.85), (-0.6, -0.1, 2.3, 0.9), (0.1, 0.5, 3.2, 0.8), (-0.2, -0.5, 3.0, 0.75)]:
        sphere((x + dx * s, y + dy * s, z + dz * s), r * s, lm, sub=2)


def lantern(loc):
    cyl(loc, 0.12, 0.3, mat("lant", "#2A1C1E"), verts=6)
    sphere((loc[0], loc[1], loc[2]), 0.09, mat("lantglow", "#FFD27A", emit="#FFB84D", emit_strength=8))
    point(loc, "#FFB060", 25, 0.1)


def barrel(loc, s=1.0):
    cyl((loc[0], loc[1], loc[2] + 0.45 * s), 0.34 * s, 0.9 * s, mat("barrel", "#9C6B3F", noise=0.25), r2=None)
    for z in (0.15, 0.75):
        cyl((loc[0], loc[1], loc[2] + z * s), 0.355 * s, 0.06 * s, mat("hoop", "#3E3A3A", rough=0.4, metal=0.6))


def crate(loc, s=0.7, rz=0.0):
    box((loc[0], loc[1], loc[2] + s / 2), (s, s, s), mat("crate", "#B5824E", noise=0.3, scale=6), 0.03, (0, 0, rz))



def bunting(p0, p1, sag=0.8, n=18, colors=("#FF6B5B", "#FFC93C", "#5ED3B5", "#FFF4E0", "#0F6B78")):
    """String of triangular flags between two points."""
    import bmesh
    x0, y0, z0 = p0; x1, y1, z1 = p1
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, z0 + (z1 - z0) * t - sag * 4 * t * (1 - t)))
    for i in range(n):
        a, b = pts[i], pts[i + 1]
        cyl(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2), 0.012, 0.01, mat("rope", "#3A2A22"), verts=4, bevel=0)
        me = bpy.data.meshes.new("flag"); bm = bmesh.new()
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2 - 0.45)
        vs = [bm.verts.new(v) for v in (a, b, m)]
        bm.faces.new(vs); bm.to_mesh(me); bm.free()
        o = bpy.data.objects.new("flag", me); bpy.context.collection.objects.link(o)
        c = colors[i % len(colors)]
        o.data.materials.append(mat("flag" + c, c, rough=0.8, noise=0.05))
        sol = o.modifiers.new("s", "SOLIDIFY"); sol.thickness = 0.02
    # rope as thin boxes between points
    for i in range(n):
        a, b = Vector(pts[i]), Vector(pts[i + 1])
        mid = (a + b) / 2; d = b - a
        bpy.ops.mesh.primitive_cylinder_add(vertices=4, radius=0.015, depth=d.length, location=mid)
        o = bpy.context.active_object
        o.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
        o.data.materials.append(mat("rope", "#3A2A22"))


def flower_box(loc, w=0.9):
    x, y, z = loc
    box((x, y, z), (w, 0.3, 0.22), mat("fbox", "#8A5A3B", noise=0.2), 0.02)
    for k in range(5):
        c = ["#FF6B5B", "#FFC93C", "#F28CC0", "#FFFFFF", "#FF6B5B"][k]
        sphere((x - w / 2 + 0.1 + k * (w - 0.2) / 4, y, z + 0.17), 0.09, mat("fl" + c, c, rough=0.7), sub=2)
        sphere((x - w / 2 + 0.2 + k * (w - 0.3) / 4, y + 0.02, z + 0.12), 0.08, mat("leaf5E9E4A", "#5E9E4A", rough=0.8, noise=0.25, scale=1.5), sub=1)


def hay_cart(loc, rz=0.0):
    x, y, z = loc
    root = bpy.data.objects.new("cart", None); bpy.context.collection.objects.link(root)
    parts = [box((0, 0, 0.75), (2.2, 1.2, 0.12), mat("cartwood", "#9C6B3F", noise=0.3), 0.02)]
    for sx in (-1, 1):
        parts.append(box((0, sx * 0.6, 1.0), (2.2, 0.08, 0.45), mat("cartwood", "#9C6B3F", noise=0.3), 0.02))
        for wx in (-0.6, 0.6):
            parts.append(cyl((wx, sx * 0.72, 0.42), 0.42, 0.1, mat("wheel", "#6B4A32", noise=0.2), rot=(math.radians(90), 0, 0), verts=16))
    parts.append(sphere((0, 0, 1.25), 0.8, mat("hay", "#E8C46A", rough=0.95, noise=0.4, scale=5), scale=(1.3, 0.75, 0.55), sub=2))
    parts.append(box((1.7, 0, 0.75), (1.4, 0.08, 0.08), mat("cartwood", "#9C6B3F", noise=0.3), 0.01))
    for o in parts:
        o.parent = root
    root.location = (x, y, z); root.rotation_euler = (0, 0, rz)


def sign(loc, color, rz=0.0):
    x, y, z = loc
    box((x, y, z + 0.45), (0.9, 0.06, 0.06), mat("iron", "#2A1C1E", rough=0.5, metal=0.5), 0, (0, 0, rz))
    box((x + 0.25 * math.cos(rz), y + 0.25 * math.sin(rz), z), (0.6, 0.05, 0.5), mat("sign" + color, color, noise=0.1), 0.02, (0, 0, rz))


def torch_sconce(loc, rz=0.0):
    x, y, z = loc
    box((x, y, z), (0.12, 0.25, 0.08), mat("iron", "#2A1C1E", rough=0.5, metal=0.5), 0.01, (0, 0, rz))
    cyl((x, y, z + 0.2), 0.05, 0.4, mat("tstick", "#6B4A32"), verts=8)
    sphere((x, y, z + 0.48), 0.1, mat("fire", "#FFB238", emit="#FF8A2A", emit_strength=25), sub=2)
    point((x, y, z + 0.55), "#FF9A40", 60, 0.1)

# ----------------------------------------------------------------- houses

WALLS = ["#F3E2BC", "#F6D7B0", "#EBD9C2", "#F2C9A0", "#E8E0CF", "#F0D3A4", "#DCE7D8"]
ROOFS = ["#B5523B", "#8F3D2E", "#5E6B7A", "#9C5A3C", "#7A4A3A", "#B86B3E"]
TIMBER = "#5B3A29"


def house(loc, w, d, h, rot_z=0.0, wall=None, roof=None, floors=2, timber=True, door=True):
    """Half-timbered house, front facing -Y before rotation."""
    import bpy as _b
    x0, y0, z0 = loc
    wall = wall or R.choice(WALLS)
    roof = roof or R.choice(ROOFS)
    objs = []
    objs.append(box((0, 0, h / 2), (w, d, h), mat("wall" + wall, wall, noise=0.15, scale=2), 0.03))
    objs.append(box((0, 0, 0.3), (w + 0.06, d + 0.06, 0.6), mat("plinth", "#9A8C7C", noise=0.25, bricks={"scale": 3, "c2": "#8C7E6E", "mortar_c": "#6E6256"}), 0.03))
    rh = min(w, d) * 0.55
    objs.append(prism_roof((0, 0, h), w, d, rh, mat("roof" + roof, roof, rough=0.6, noise=0.2, bricks={"scale": 6, "c2": roof, "mortar_c": "#3A2A22", "w": 0.5, "h": 0.25})))
    tm = mat("timber", TIMBER, noise=0.2)
    if timber:
        fy = -d / 2 - 0.03
        for zz in [h * (i / floors) for i in range(1, floors)] + [h - 0.08]:
            objs.append(box((0, fy, zz), (w, 0.08, 0.16), tm, 0.01))
        for xx in (-w / 2 + 0.08, w / 2 - 0.08):
            objs.append(box((xx, fy, h / 2), (0.16, 0.08, h), tm, 0.01))
        # diagonal braces upper floor
        fh = h / floors
        for sgn in (-1, 1):
            o = box((sgn * w * 0.3, fy, h - fh / 2), (0.12, 0.07, fh * 1.1), tm, 0.01, (0, sgn * 0.6, 0))
            objs.append(o)
    wm = mat("winglass", "#2D4A6B", rough=0.15, emit="#FFC870", emit_strength=0.0)
    fm = mat("winframe", "#FFF4E0", noise=0.05)
    sh = mat("shutter" + roof, R.choice(["#2E6F6B", "#3E8E5E", "#B3262E", "#2E5A8C"]), noise=0.1)
    fh = h / floors
    nwin = max(1, int(w / 1.6))
    for f in range(floors):
        for i in range(nwin):
            xx = -w / 2 + (i + 0.5) * w / nwin
            zz = f * fh + fh * 0.55
            if f == 0 and door and i == nwin // 2:
                objs.append(box((xx, -d / 2 - 0.02, 1.0), (0.95, 0.12, 2.0), mat("door", "#6B3F25", noise=0.25), 0.04))
                objs.append(box((xx, -d / 2 - 0.04, 2.05), (1.1, 0.14, 0.14), tm, 0.02))
                continue
            objs.append(box((xx, -d / 2 - 0.02, zz), (0.72, 0.1, 0.9), fm, 0.02))
            objs.append(box((xx, -d / 2 - 0.05, zz), (0.56, 0.1, 0.74), wm, 0.0))
            for sgn in (-1, 1):
                objs.append(box((xx + sgn * 0.55, -d / 2 - 0.03, zz), (0.3, 0.08, 0.92), sh, 0.02))
    # chimney
    objs.append(box((w * 0.25, d * 0.15, h + rh * 0.8), (0.5, 0.5, 1.2), mat("chim", "#A08672", bricks={"scale": 8, "c2": "#8E7462", "mortar_c": "#5E4E42"}), 0.02))
    # parent & place
    root = bpy.data.objects.new("house", None)
    bpy.context.collection.objects.link(root)
    for o in objs:
        o.parent = root
    root.location = (x0, y0, z0)
    root.rotation_euler = (0, 0, rot_z)
    return root

# ----------------------------------------------------------------- sets

def cobbles(size=60, color="#B9A88E", c2="#A6957C"):
    m = mat("cobble", color, rough=0.85, noise=0.18, bricks={"scale": 3, "c2": c2, "mortar_c": "#7E705E", "w": 0.4, "h": 0.25, "mortar": 0.04})
    plane((0, 0, 0), (size, size), m)


def set_square(variant="day"):
    alpine = variant == "alpine"
    cobbles(80)
    # ring of houses around a plaza ~24 x 20, open towards -Y (camera side)
    for i, x in enumerate([-13, -8.6, -4.2]):
        house((x, 13, 0), 4.2, 5, R.uniform(6, 7.5))
    # town hall at the back centre with clock tower
    th = "#E8D9B8"
    box((2.5, 13.5, 4.5), (9, 6, 9), mat("hall", th, noise=0.12, bricks={"scale": 3, "c2": "#DCCBA6", "mortar_c": "#B8A684", "w": 0.6, "h": 0.3}), 0.04)
    prism_roof((2.5, 13.5, 9), 9, 6, 3.2, mat("hallroof", "#3E5A7A", bricks={"scale": 6, "c2": "#36506E", "mortar_c": "#22303E", "w": 0.5, "h": 0.25}))
    for i in range(4):
        xx = -0.6 + i * 2.1
        box((xx, 10.45, 2.0), (1.3, 0.2, 3.2), mat("arch", "#5E4632", noise=0.2), 0.08)
        box((xx, 10.42, 6.2), (1.0, 0.15, 1.6), mat("winglass", "#2D4A6B", rough=0.15), 0.02)
        box((xx, 10.4, 6.2), (1.2, 0.1, 1.8), mat("winframe", "#FFF4E0", noise=0.05), 0.02)
    box((2.5, 13.5, 14), (2.6, 2.6, 7), mat("tower", th, noise=0.12, bricks={"scale": 3, "c2": "#DCCBA6", "mortar_c": "#B8A684", "w": 0.6, "h": 0.3}), 0.04)
    cyl((2.5, 13.5, 19.2), 2.0, 3.4, mat("spire", "#3E5A7A", rough=0.5), verts=4, r2=0.02, rot=(0, 0, math.radians(45)))
    cyl((2.5, 12.15, 15.2), 0.8, 0.12, mat("clock", "#FFF4E0"), rot=(math.radians(90), 0, 0))
    box((2.5, 12.06, 15.35), (0.06, 0.04, 0.6), mat("hand", "#2A1C1E"), 0)
    box((2.75, 12.06, 15.2), (0.5, 0.04, 0.06), mat("hand", "#2A1C1E"), 0)
    for x in [8.8, 13.2]:
        house((x, 13, 0), 4.2, 5, R.uniform(6, 7.5))
    for y, rot in [(7, -math.pi / 2), (2, -math.pi / 2), (-3, -math.pi / 2)]:
        house((-15, y, 0), 4.6, 5, R.uniform(6, 8), rot_z=rot + math.pi)
        house((16, y, 0), 4.6, 5, R.uniform(6, 8), rot_z=rot)
    # church spire far behind
    box((-9, 26, 5), (5, 9, 10), mat("church", "#D8CBB0", bricks={"scale": 3, "c2": "#CBBC9E", "mortar_c": "#A6977C", "w": 0.6, "h": 0.3}), 0.05)
    box((-9, 21, 10), (3, 3, 20), mat("church", "#D8CBB0", bricks={"scale": 3, "c2": "#CBBC9E", "mortar_c": "#A6977C", "w": 0.6, "h": 0.3}), 0.05)
    cyl((-9, 21, 23.5), 2.2, 7, mat("spire2", "#5E6B7A"), verts=4, r2=0.02, rot=(0, 0, math.radians(45)))
    # market stalls with striped awnings
    for x, c in [(-9.5, "#FF6B5B"), (9.5, "#0F6B78")]:
        for dx in (-0.9, 0.9):
            box((x + dx, 6.5, 1.1), (0.12, 0.12, 2.2), mat("post", "#8A5A3B"), 0.02)
        box((x, 6.5, 0.9), (2.2, 1.0, 0.12), mat("table", "#B5824E", noise=0.2), 0.02)
        for k in range(6):
            col = c if k % 2 == 0 else "#FFF4E0"
            box((x - 1.0 + k * 0.4 + 0.2, 6.2, 2.25), (0.4, 1.6, 0.06), mat("aw" + col, col, noise=0.05), 0.0, (math.radians(-12), 0, 0))
        for k in range(4):
            sphere((x - 0.6 + k * 0.4, 6.5, 1.05), 0.14, mat("fruit%d" % k, ["#E8513A", "#FFC93C", "#7CB342", "#F28C28"][k]))
    # well
    cyl((-6, 1.5, 0.45), 1.0, 0.9, mat("well", "#A89A88", bricks={"scale": 6, "c2": "#968876", "mortar_c": "#6E6256"}), verts=24)
    cyl((-6, 1.5, 0.92), 0.82, 0.05, mat("water", "#2E6F8C", rough=0.05))
    for dx in (-0.8, 0.8):
        box((-6 + dx, 1.5, 1.6), (0.12, 0.12, 1.5), mat("post", "#8A5A3B"), 0.02)
    prism_roof((-6, 1.5, 2.3), 1.8, 1.2, 0.6, mat("roofB5523B", "#B5523B"), overhang=0.15)
    # scaffold / platform centre (z top = 1.2)
    box((2, 5, 0.6), (4.4, 3.4, 1.2), mat("plank", "#A0703F", noise=0.3, bricks={"scale": 5, "c2": "#8E6236", "mortar_c": "#5E3E22", "w": 1.0, "h": 0.12}), 0.03)
    for k in range(4):
        box((2, 2.95 - k * 0.32, 0.15 + k * 0.3), (1.4, 0.34, 0.3 + k * 0.0), mat("plank2", "#8E6236", noise=0.3), 0.02)
    barrel((7.5, 9, 0)); barrel((8.2, 9.4, 0)); crate((-11, 9, 0), 0.8, 0.3); crate((-10.2, 9.2, 0), 0.6, 0.6)
    for x in (-3.5, 7.5):
        box((x, 9.7, 1.6), (0.14, 0.14, 3.2), mat("lpost", "#2A1C1E"), 0.02)
        lantern((x, 9.7, 3.3))
    for x, y in [(-12, -9), (12, -9), (-17, 16), (18, 16)]:
        tree((x, y, 0), 1.2)
    if alpine:
        mm = mat("mount", "#7D8FA8", rough=0.9, noise=0.2, scale=0.5)
        sn = mat("snow", "#F4F7FB", rough=0.6)
        for x, y, r, h in [(-40, 90, 30, 40), (5, 110, 40, 55), (45, 95, 32, 42), (80, 120, 40, 50)]:
            cyl((x, y, h / 2), r, h, mm, verts=7, r2=0.5, bevel=0)
            cyl((x, y, h * 0.83), r * 0.18, h * 0.34, sn, verts=7, r2=0.3, bevel=0)
    # dressing: bunting across the square, flower boxes, shop signs, hay cart, sacks
    bunting((-12.5, 10.4, 5.2), (13.5, 10.4, 5.0), 0.9)
    bunting((-12.8, 9.5, 4.6), (-12.8, -3.5, 4.4), 0.7)
    bunting((14.0, 9.5, 4.6), (14.0, -3.5, 4.4), 0.7)
    for x in (-13, -8.6, 8.8, 13.2):
        flower_box((x - 1.0, 10.35, 3.65))
    sign((-11.2, 10.2, 2.8), "#FFC93C"); sign((10.6, 10.2, 2.9), "#5ED3B5")
    hay_cart((-9.5, 2.5, 0), 0.4)
    for k in range(3):
        sphere((9.3 + k * 0.5, 7.2, 0.3), 0.32, mat("sack", "#D8B27A", rough=0.95, noise=0.3, scale=6), scale=(1, 1, 1.25), sub=2)
    if variant == "dusk":
        world("#3E5A9C", "#FFB38A", 0.7)
        sun((70, 0, -40), "#FFB27A", 3.0, 3)
    else:
        world("#7EC8F0", "#FFF1D6", 1.0)
        sun((52, 0, -35), "#FFE6C4", 4.2, 3)


def set_court(variant="town"):
    church = variant == "church"
    W, D, H = 16, 22, 10
    floor_m = mat("floorwood", "#A0703F", rough=0.6, noise=0.25, bricks={"scale": 2, "c2": "#8E6236", "mortar_c": "#5E3E22", "w": 1.5, "h": 0.18, "mortar": 0.01, "k": 1})
    plane((0, 0, 0), (W, D), floor_m)
    wall_c = "#CBBBA0" if not church else "#D8D0C0"
    wm = mat("stone" + variant, wall_c, rough=0.9, noise=0.15, bricks={"scale": 1.5, "c2": "#B8A88C" if not church else "#C9C0AE", "mortar_c": "#8E7E66", "w": 0.7, "h": 0.32, "mortar": 0.012, "k": 1})
    # back wall and right wall solid; left wall with window openings
    box((0, D / 2, H / 2), (W, 0.6, H), wm, 0.02)
    box((W / 2, 0, H / 2), (0.6, D, H), wm, 0.02)
    xL = -W / 2
    wins = [-6, 0, 6]
    ys = sorted([-D / 2] + [y - 1.0 for y in wins] + [y + 1.0 for y in wins] + [D / 2])
    for a, b in zip(ys[0::2], ys[1::2]):
        box((xL, (a + b) / 2, H / 2), (0.6, b - a, H), wm, 0.02)
    for y in wins:
        box((xL, y, 1.4), (0.6, 2.0, 2.8), wm, 0.02)
        box((xL, y, 8.6), (0.6, 2.0, 2.8), wm, 0.02)
        glass = mat("glass" + variant, "#BFE3F0" if not church else "#E8B04B", rough=0.1,
                    emit="#FFF2D0" if not church else "#FFB84D", emit_strength=1.5 if not church else 3.0)
        box((xL - 0.1, y, 5.0), (0.05, 2.0, 4.4), glass, 0)
        if church:
            for k, c in enumerate(["#B3262E", "#2E5A8C", "#3E8E5E", "#FFC93C"]):
                box((xL - 0.05, y - 0.75 + k * 0.5, 5.0 + (k % 2) * 0.8), (0.05, 0.45, 0.7), mat("sg" + c, c, emit=c, emit_strength=4), 0)
        cyl((xL - 0.1, y, 7.2), 1.0, 0.05, glass, rot=(0, math.radians(90), 0), verts=24)
    # ceiling beams
    plane((0, 0, H), (W, D), mat("ceil", "#8A6A4E", noise=0.2), rot=(math.pi, 0, 0))
    for y in range(-10, 11, 3):
        box((0, y, H - 0.3), (W, 0.4, 0.6), mat("beam", "#5B3A29", noise=0.2), 0.03)
    # judge's bench (back), raised
    dais = mat("dais", "#6B3F25", noise=0.25, bricks={"scale": 3, "c2": "#5E3720", "mortar_c": "#3E2412", "w": 1.2, "h": 0.2, "k": 1})
    box((0, 8.5, 0.5), (8, 3, 1.0), dais, 0.03)
    box((0, 7.6, 1.6), (6.4, 0.9, 1.3), mat("bench", "#7A4A2B", noise=0.25), 0.05)
    cloth = "#B3262E" if not church else "#6E3A8C"
    box((0, 7.1, 1.5), (5.0, 0.06, 1.1), mat("cloth" + cloth, cloth, rough=0.9, noise=0.1), 0.01)
    box((0, 7.08, 1.35), (0.9, 0.06, 0.9), mat("emblem", "#FFC93C", rough=0.4, metal=0.3), 0.02)
    box((0, 9.4, 2.6), (1.6, 0.4, 3.2), mat("throne" + cloth, cloth, noise=0.1), 0.1)
    box((0, 9.6, 4.3), (1.9, 0.3, 0.4), mat("gold", "#FFC93C", rough=0.35, metal=0.6), 0.05)
    # banners on back wall
    for x in (-5, 5):
        bc = "#0F6B78" if not church else "#6E3A8C"
        box((x, D / 2 - 0.35, 6.2), (1.6, 0.06, 3.6), mat("ban" + bc, bc, rough=0.9), 0.01)
        cyl((x, D / 2 - 0.4, 6.8), 0.4, 0.05, mat("gold", "#FFC93C", rough=0.35, metal=0.6), rot=(math.radians(90), 0, 0))
    if church:
        box((0, D / 2 - 0.35, 7.0), (0.3, 0.1, 2.6), mat("gold", "#FFC93C", rough=0.35, metal=0.6), 0.03)
        box((0, D / 2 - 0.35, 7.5), (1.4, 0.1, 0.3), mat("gold", "#FFC93C", rough=0.35, metal=0.6), 0.03)
        for x in (-2.5, 2.5):
            cyl((x, 7.5, 2.6), 0.08, 0.8, mat("candle", "#FFF4E0"))
            sphere((x, 7.5, 3.1), 0.07, mat("flame", "#FFD27A", emit="#FFB84D", emit_strength=20))
            point((x, 7.3, 3.2), "#FFB060", 40, 0.05)
    # dock (left front) and spectator benches (right)
    rail = mat("rail", "#8A5A3B", noise=0.25)
    dx, dy = -3.6, 1.0
    box((dx, dy, 0.15), (2.6, 2.2, 0.3), dais, 0.02)
    for (x, y, sx, sy) in [(dx, dy - 1.1, 2.6, 0.12), (dx - 1.3, dy, 0.12, 2.2), (dx + 1.3, dy, 0.12, 2.2)]:
        box((x, y, 1.15), (sx, sy, 0.12), rail, 0.02)
        n = int(max(sx, sy) / 0.35)
        for k in range(n + 1):
            px = x - sx / 2 + k * sx / n if sx > sy else x
            py = y - sy / 2 + k * sy / n if sy > sx else y
            cyl((px, py, 0.7), 0.04, 0.9, rail, verts=8)
    for row in range(3):
        y = 1.5 - row * 2.2
        box((4.0, y, 0.45), (4.5, 0.5, 0.1), mat("pew", "#7A4A2B", noise=0.25), 0.03)
        box((4.0, y + 0.25, 0.8), (4.5, 0.08, 0.7), mat("pew", "#7A4A2B", noise=0.25), 0.02)
        for x in (2.0, 6.0):
            box((x, y, 0.22), (0.1, 0.5, 0.44), mat("pew", "#7A4A2B", noise=0.25), 0.02)
    # table with scroll & inkwell in front of bench
    box((2.4, 4.2, 0.8), (2.2, 1.0, 0.1), mat("table", "#B5824E", noise=0.2), 0.02)
    for x in (1.5, 3.3):
        box((x, 4.2, 0.4), (0.1, 0.8, 0.8), mat("table", "#B5824E", noise=0.2), 0.02)
    box((2.2, 4.2, 0.87), (0.6, 0.4, 0.03), mat("parch", "#F3E2BC"), 0.005)
    cyl((2.9, 4.1, 0.92), 0.08, 0.14, mat("ink", "#2A1C1E", rough=0.2))
    # chandelier
    cyl((0, 2, 7.8), 1.2, 0.08, mat("iron", "#2A1C1E", rough=0.5, metal=0.5), verts=32)
    for k in range(8):
        a = k * math.pi / 4
        p = (1.2 * math.cos(a), 2 + 1.2 * math.sin(a), 7.95)
        sphere(p, 0.06, mat("flame", "#FFD27A", emit="#FFB84D", emit_strength=20))
    point((0, 2, 7.5), "#FFB060", 400, 1.0)
    # dressing: red carpet runner, wall torches, books, coat of arms shields
    box((0, 1.0, 0.012), (2.2, 12.0, 0.02), mat("carpet" + variant, "#9C2430" if not church else "#5A2E73", rough=0.95, noise=0.1), 0.0)
    box((0, 1.0, 0.016), (1.8, 12.0, 0.02), mat("carpet2" + variant, "#B3262E" if not church else "#6E3A8C", rough=0.95, noise=0.1), 0.0)
    for y in (-7, -1, 5):
        torch_sconce((W / 2 - 0.4, y, 3.4))
    for k in range(4):
        box((2.0 + k * 0.12, 4.0, 0.95), (0.1, 0.35, 0.28), mat("book" + str(k), ["#B3262E", "#0F6B78", "#FFC93C", "#5B3A29"][k], rough=0.6), 0.01)
    for x in (-3.0, 3.0):
        cyl((x, D / 2 - 0.4, 3.6), 0.5, 0.08, mat("shield" + variant, "#FFC93C" if not church else "#FFF4E0", rough=0.4, metal=0.3), rot=(math.radians(90), 0, 0), verts=6)
    # light
    world("#9FD0E8", "#FFF1D6", 0.35)
    s = sun((60, 0, -80), "#FFE6C4", 6.0 if not church else 4.5, 2)
    area((0, -6, 8.5), (60, 0, 0), 8, "#FFE7C8", 800)
    area((5, 4, 7), (0, -40, 0), 4, "#FFD9A8", 300)


def terrain(size, color, c2=None, rows=None, amp=1.2):
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=160, y_subdivisions=160, size=size)
    o = bpy.context.active_object
    for v in o.data.vertices:
        x, y = v.co.x, v.co.y
        d = max(0.0, (math.hypot(x, y) - 12) / 60)
        v.co.z = amp * d * (math.sin(x * 0.08) * 1.5 + math.cos(y * 0.06 + 1) * 2.0 + math.sin((x + y) * 0.13) * 0.8) + d * d * 6
    m = patchwork(color, c2) if rows else mat("terr" + color, color, rough=0.95, noise=0.2, scale=0.3)
    return obj_from(o, m, 0)


def patchwork(c1, c2):
    """Farmland: voronoi fields in golds and greens, with wave rows."""
    m = bpy.data.materials.new("fields"); m.use_nodes = True; nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]; bsdf.inputs["Roughness"].default_value = 0.95
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 0.035
    nt.links.new(geo.outputs["Position"], vo.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); cr = ramp.color_ramp; cr.interpolation = "CONSTANT"
    cols = [c1, "#9CC45A", c2, "#7FB04E", "#EBD27C", "#B7C95E"]
    cr.elements[0].color = hexrgb(cols[0]); cr.elements[1].position = 1 / 6; cr.elements[1].color = hexrgb(cols[1])
    for i, c in enumerate(cols[2:], 2):
        e = cr.elements.new(i / 6); e.color = hexrgb(c)
    nt.links.new(vo.outputs["Color"], ramp.inputs["Fac"])
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = 0.6; wv.inputs["Distortion"].default_value = 0.5
    nt.links.new(geo.outputs["Position"], wv.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["To Min"].default_value = 0.85; mr.inputs["To Max"].default_value = 1.05
    nt.links.new(wv.outputs["Fac"], mr.inputs["Value"])
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"; mix.inputs["Factor"].default_value = 1.0
    nt.links.new(ramp.outputs["Color"], mix.inputs["A"])
    cc = nt.nodes.new("ShaderNodeCombineColor")
    for k in ("Red", "Green", "Blue"):
        nt.links.new(mr.outputs["Result"], cc.inputs[k])
    nt.links.new(cc.outputs["Color"], mix.inputs["B"])
    nt.links.new(mix.outputs["Result"], bsdf.inputs["Base Color"])
    return m


def set_land(variant="barley"):
    night = variant == "night"
    vine = variant == "vineyard"
    if vine:
        terrain(400, "#8DBE5A", amp=2.0)
        # vine rows on the slope in front
        vm = mat("vine", "#3E7E3A", rough=0.9, noise=0.3, scale=2)
        pm = mat("vpost", "#6B4A32")
        for r in range(9):
            y = 4 + r * 1.8
            for k in range(14):
                x = -13 + k * 2.0
                sphere((x, y, 0.75), 0.55, vm, scale=(1.4, 0.6, 0.8), sub=2)
                if k % 2 == 0:
                    cyl((x, y, 0.6), 0.04, 1.2, pm, verts=6)
                    for g in range(3):
                        sphere((x + 0.3 - g * 0.3, y - 0.35, 0.5), 0.07, mat("grape", "#5B2E6E", rough=0.3))
        mm = mat("mount", "#7D8FA8", rough=0.9, noise=0.2, scale=0.5)
        sn = mat("snow", "#F4F7FB", rough=0.6)
        for x, y, r, h in [(-80, 160, 50, 70), (0, 190, 70, 95), (70, 170, 55, 75), (130, 200, 60, 80), (-140, 190, 60, 70)]:
            cyl((x, y, h / 2), r, h, mm, verts=7, r2=0.5, bevel=0)
            cyl((x, y, h * 0.83), r * 0.18, h * 0.34, sn, verts=7, r2=0.3, bevel=0)
    else:
        terrain(400, "#E8C46A" if not night else "#5E6B4A", "#D9B04E" if not night else "#4E5A3E", rows=30, amp=1.0)
    # dirt path towards village
    path = mat("path", "#C9A77A", rough=0.95, noise=0.2)
    box((0, 0, 0.02), (2.6, 120, 0.06), path, 0.0)
    # village cluster on the hill
    vx, vy = (8, 46) if not night else (0, 40)
    for i in range(7):
        a = i * 0.9
        house((vx + math.cos(a) * 7, vy + math.sin(a) * 4, 0), 4, 4, R.uniform(4.5, 6), rot_z=R.uniform(-0.4, 0.4), floors=2)
    box((vx - 2, vy + 6, 6), (3, 3, 12), mat("church", "#D8CBB0", bricks={"scale": 3, "c2": "#CBBC9E", "mortar_c": "#A6977C", "w": 0.6, "h": 0.3}), 0.05)
    cyl((vx - 2, vy + 6, 14.5), 2.1, 5, mat("spire2", "#5E6B7A"), verts=4, r2=0.02, rot=(0, 0, math.radians(45)))
    if vine:
        sm = mat("stonewall", "#A89A88", rough=0.9, bricks={"scale": 3, "c2": "#968876", "mortar_c": "#6E6256", "w": 0.6, "h": 0.3})
        box((-3.2, 8, 0.45), (0.5, 16, 0.9), sm, 0.05)
        hay_cart((-4.8, 3.0, 0), 1.2)
        box((5.5, 2.0, 0.6), (0.5, 0.5, 1.2), mat("shrine", "#D8CBB0"), 0.04)
        prism_roof((5.5, 2.0, 1.2), 0.6, 0.6, 0.35, mat("roofB5523B", "#B5523B"), overhang=0.1)
        for k in range(4):
            box((-1.6 + k * 0.45, 1.0, 0.25), (0.4, 0.4, 0.5), mat("basket", "#B5824E", noise=0.4, scale=8), 0.05)
            sphere((-1.6 + k * 0.45, 1.0, 0.55), 0.17, mat("grape", "#5B2E6E", rough=0.3), scale=(1, 1, 0.6))
    if night:
        # Basel-like city wall with towers (generic), torches, glow
        wallm = mat("cwall", "#5A5048", rough=0.9, bricks={"scale": 2, "c2": "#4E463E", "mortar_c": "#2E2824", "w": 0.8, "h": 0.4})
        box((0, 60, 5), (70, 2, 10), wallm, 0.05)
        for x in range(-30, 31, 15):
            cyl((x, 60, 8), 2.6, 16, wallm, verts=12)
            cyl((x, 60, 18), 3.0, 4, mat("troof", "#3A2E2A"), verts=12, r2=0.1)
        for x, y in [(-4, 6), (4, 7), (-2.5, 11), (3, 12)]:
            box((x, y, 1.0), (0.12, 0.12, 2.0), mat("tpost", "#3A2618"), 0.02)
            sphere((x, y, 2.15), 0.18, mat("fire", "#FFB238", emit="#FF8A2A", emit_strength=25))
            point((x, y, 2.3), "#FF9A40", 300, 0.3)
        point((0, 9, 1.5), "#FF7A2A", 1200, 1.5)  # off-screen bonfire glow
        world("#14244E", "#3E4E86", 1.2)
        sun((60, 0, 140), "#9FB8FF", 1.4, 1)
        sphere((-40, 160, 70), 6, mat("moon", "#FFF6DA", emit="#FFF6DA", emit_strength=6))
    else:
        for i in range(26):
            x = R.uniform(-60, 60)
            y = R.uniform(15, 90)
            if abs(x) < 4:
                continue
            tree((x, y, 0), R.uniform(1.0, 1.8), R.choice(["#5E9E4A", "#4E8E42", "#6FAE52"]))
        # fence along path
        fm = mat("fence", "#8A5A3B", noise=0.2)
        for k in range(16):
            y = -4 + k * 1.6
            cyl((-2.2, y, 0.5), 0.05, 1.0, fm, verts=8)
            if k:
                box((-2.2, y - 0.8, 0.8), (0.06, 1.6, 0.08), fm, 0.01)
        world("#6FC0EE", "#FFF4DE", 1.0)
        sun((55, 0, -30), "#FFE6C4", 4.5, 3)
        if not vine:
            for x, y in [(4, 4), (5.5, 5.5), (-6, 8)]:
                cyl((x, y, 0.6), 0.5, 1.2, mat("sheaf", "#E8C46A", noise=0.3), verts=12, r2=0.2)


def set_study(variant="day"):
    W, D, H = 10, 9, 5
    plane((0, 0, 0), (W, D), mat("sfloor", "#B07A48", rough=0.6, noise=0.25, bricks={"scale": 2, "c2": "#9E6A3C", "mortar_c": "#6E4422", "w": 1.4, "h": 0.2, "mortar": 0.01, "k": 1}))
    wallm = mat("swall", "#2F8C8C", rough=0.9, noise=0.08)
    box((0, D / 2, H / 2), (W, 0.3, H), wallm, 0.02)
    box((-W / 2, 0, H / 2), (0.3, D, H), wallm, 0.02)
    box((W / 2, 0, H / 2), (0.3, D, H), wallm, 0.02)
    box((0, D / 2 - 0.2, 0.5), (W, 0.1, 1.0), mat("wainscot", "#0B3F4C", noise=0.1), 0.02)
    # big round window (left of back wall)
    cyl((-2.6, D / 2 - 0.1, 2.9), 1.3, 0.3, mat("wframe", "#FFF4E0"), rot=(math.radians(90), 0, 0), verts=48)
    cyl((-2.6, D / 2 - 0.2, 2.9), 1.15, 0.32, mat("sky", "#9ED8F0", emit="#CFEFFF", emit_strength=2.5), rot=(math.radians(90), 0, 0), verts=48)
    box((-2.6, D / 2 - 0.4, 2.9), (2.3, 0.06, 0.08), mat("wframe", "#FFF4E0"), 0.01)
    box((-2.6, D / 2 - 0.4, 2.9), (0.08, 0.06, 2.3), mat("wframe", "#FFF4E0"), 0.01)
    # bookshelf (right of back wall)
    sh = mat("shelf", "#6B3F25", noise=0.2)
    box((2.8, D / 2 - 0.2, 2.0), (3.4, 0.1, 4.0), sh, 0.02)
    for x in (1.15, 4.45):
        box((x, D / 2 - 0.5, 2.0), (0.12, 0.7, 4.0), sh, 0.02)
    box((2.8, D / 2 - 0.5, 4.0), (3.5, 0.75, 0.12), sh, 0.02)
    bc = ["#FF6B5B", "#FFC93C", "#5ED3B5", "#0F6B78", "#FFF4E0", "#B3262E", "#2E5A8C", "#8A5A3B"]
    for row in range(4):
        z = 0.35 + row * 0.95
        box((2.8, D / 2 - 0.5, z - 0.05), (3.2, 0.65, 0.06), sh, 0.01)
        x = 1.25
        while x < 4.3:
            w = R.uniform(0.1, 0.2)
            h = R.uniform(0.55, 0.8)
            box((x + w / 2, D / 2 - 0.6, z + h / 2), (w * 0.95, 0.45, h), mat("book" + str(R.randrange(8)), R.choice(bc), rough=0.6), 0.01, (0, R.choice([0, 0, 0, 0.12]), 0))
            x += w
    # desk with globe, lamp, papers
    dm = mat("desk", "#8A5A3B", noise=0.2)
    box((0.6, 1.6, 1.0), (3.2, 1.3, 0.12), dm, 0.04)
    for x in (-0.8, 2.0):
        box((x, 1.6, 0.48), (0.4, 1.1, 0.96), dm, 0.03)
    cyl((1.7, 1.7, 1.2), 0.12, 0.2, mat("gold", "#FFC93C", rough=0.35, metal=0.6))
    sphere((1.7, 1.7, 1.6), 0.3, mat("globe", "#2E8CB8", rough=0.4, noise=0.4, scale=4))
    cyl((-0.4, 1.8, 1.3), 0.05, 0.6, mat("iron", "#2A1C1E", rough=0.5, metal=0.5))
    cyl((-0.4, 1.8, 1.65), 0.25, 0.3, mat("shade", "#FFC93C", emit="#FFC93C", emit_strength=2), r2=0.12)
    point((-0.4, 1.7, 1.5), "#FFC870", 60, 0.2)
    for k in range(3):
        box((0.5 + k * 0.25, 1.4, 1.07), (0.5, 0.36, 0.01), mat("parch", "#F3E2BC"), 0.0, (0, 0, R.uniform(-0.3, 0.3)))
    # map board on left wall
    box((-W / 2 + 0.2, 0.5, 2.6), (0.08, 2.6, 1.7), mat("frame", "#5B3A29"), 0.03)
    box((-W / 2 + 0.25, 0.5, 2.6), (0.06, 2.4, 1.5), mat("parch", "#F3E2BC"), 0.0)
    # rug
    cyl((0.4, 0.0, 0.01), 2.2, 0.02, mat("rug", "#FF6B5B", rough=0.95, noise=0.15), verts=48)
    cyl((0.4, 0.0, 0.015), 1.7, 0.02, mat("rug2", "#FFC93C", rough=0.95, noise=0.15), verts=48)
    # plant
    cyl((-3.8, 3.4, 0.35), 0.35, 0.7, mat("pot", "#C76A2B"), r2=0.28)
    for k in range(5):
        sphere((-3.8 + R.uniform(-.3, .3), 3.4 + R.uniform(-.3, .3), 1.0 + R.uniform(0, .5)), 0.35, mat("leaf5E9E4A", "#5E9E4A", rough=0.8, noise=0.25, scale=1.5), sub=2)
    # dressing: framed pictures, stack of books, candle, hanging lamp, logo badge
    for x, c in ((0.6, "#FFC93C"), (-0.6, "#FF6B5B")):
        box((x, D / 2 - 0.17, 3.5), (0.8, 0.06, 0.6), mat("frame", "#5B3A29"), 0.02)
        box((x, D / 2 - 0.2, 3.5), (0.66, 0.05, 0.46), mat("pic" + c, c, rough=0.6, noise=0.3, scale=4), 0.0)
    for k in range(5):
        box((-3.0, -1.5, 0.08 + k * 0.13), (0.6 - k * 0.04, 0.42, 0.12), mat("book" + str(k), ["#FF6B5B", "#0F6B78", "#FFC93C", "#5ED3B5", "#FFF4E0"][k], rough=0.6), 0.01, (0, 0, k * 0.2))
    cyl((1.05, 1.35, 1.15), 0.05, 0.2, mat("candle", "#FFF4E0"))
    sphere((1.05, 1.35, 1.3), 0.035, mat("flame", "#FFD27A", emit="#FFB84D", emit_strength=20))
    cyl((0.4, 0.4, 4.3), 0.02, 1.4, mat("iron", "#2A1C1E", rough=0.5, metal=0.5), verts=6)
    cyl((0.4, 0.4, 3.55), 0.45, 0.35, mat("shade2", "#FF6B5B", emit="#FFB070", emit_strength=0.6), r2=0.18)
    point((0.4, 0.4, 3.3), "#FFC880", 120, 0.3)
    cyl((3.2, D / 2 - 0.17, 3.0), 0.35, 0.05, mat("gold", "#FFC93C", rough=0.35, metal=0.6), rot=(math.radians(90), 0, 0), verts=32)
    # ceiling
    plane((0, 0, H), (W, D), mat("sceil", "#F3E2BC"), rot=(math.pi, 0, 0))
    world("#9ED8F0", "#FFF1D6", 0.4)
    area((-2.6, 2.0, 3.0), (90, 0, 180), 2.4, "#DDF2FF", 250)
    area((2, -4, 4.5), (50, 0, 20), 6, "#FFE7C8", 700)
    area((0, 0, 4.9), (0, 0, 0), 5, "#FFF1D6", 250)


BUILDERS = {"square": set_square, "court": set_court, "land": set_land, "study": set_study}


def build(set_id, variant):
    clear()
    global R
    R = random.Random(hash((set_id, variant)) % 1000)
    _MATS.clear()
    BUILDERS[set_id](variant)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    bpy.context.collection.objects.link(cam)
    cam.data.sensor_fit = "HORIZONTAL"
    cam.data.sensor_width = 36.0
    bpy.context.scene.camera = cam
    return cam


def setup_render(W, H, samples, gpu=False):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 6
    sc.cycles.diffuse_bounces = 3
    sc.cycles.glossy_bounces = 2
    sc.cycles.transmission_bounces = 2
    sc.cycles.caustics_reflective = False
    sc.cycles.caustics_refractive = False
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.adaptive_threshold = 0.02
    sc.render.resolution_x = W
    sc.render.resolution_y = H
    sc.render.resolution_percentage = 100
    sc.render.use_persistent_data = True
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Punchy"
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = "PNG"
    if gpu:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        for dev in ("OPTIX", "CUDA"):
            try:
                prefs.compute_device_type = dev
                prefs.get_devices()
                if any(d.type == dev for d in prefs.devices):
                    break
            except Exception:
                pass
        for d in prefs.devices:
            d.use = d.type != "CPU"
        sc.cycles.device = "GPU"
        sc.cycles.denoiser = "OPENIMAGEDENOISE"  # OptiX denoiser weights are missing on Kaggle
        try:
            sc.cycles.denoising_use_gpu = True
        except Exception:
            pass
    else:
        sc.cycles.denoiser = "OPENIMAGEDENOISE"
