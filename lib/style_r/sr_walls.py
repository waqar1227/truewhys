"""Style R props for brick walls (A-018, 20 Nov 2026). Original, code-built (TrueWhys), CC0-style use.
wavy_wall(...)   one-brick crinkle-crankle wall along a sine path (running bond, per-brick colour variation, mortar core)
straight_wall()  straight wall, 1 or 2 bricks thick, optional piers (pillars); origin on the base front edge (so it can topple)
paper_sheet()    flat sheet standing on its edge; zigzag=True folds it into a self-supporting zigzag
fruit_tree(), sun_disc(), arrow3d()
UK brick: 215 x 102.5 x 65 mm, 10 mm mortar.
"""
import math, random
import bpy, bmesh
from mathutils import Vector, Matrix
import sr_common as C

BL, BW, BH, MJ = 0.215, 0.1025, 0.065, 0.010
_BRICK_COLS = ["#A8432F", "#B5523A", "#9A3B2A", "#C0623F", "#8E3726", "#B9573E"]


def brick_mats():
    return [C.pbr(f"brick{i}", c, 0.85, bump="noise", bscale=180.0, bstr=0.35, cvar=0.12, cscale=9.0) for i, c in enumerate(_BRICK_COLS)]


def mortar_mat():
    return C.pbr("mortar", "#CFC6B4", 0.95, bump="noise", bscale=400.0, bstr=0.2)


def _add_box(bm, centre, tangent, size, mat_idx):
    t = Vector((tangent.x, tangent.y, 0)).normalized(); n = Vector((-t.y, t.x, 0)); z = Vector((0, 0, 1))
    hx, hy, hz = size[0] / 2, size[1] / 2, size[2] / 2
    vs = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                vs.append(bm.verts.new(centre + t * (sx * hx) + n * (sy * hy) + z * (sz * hz)))
    idx = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    for q in idx:
        f = bm.faces.new([vs[i] for i in q]); f.material_index = mat_idx


def _path(L, amp, wave, n=600):
    pts = []
    for i in range(n + 1):
        x = -L / 2 + L * i / n
        pts.append(Vector((x, amp * math.sin(2 * math.pi * x / wave) if amp else 0.0, 0.0)))
    s = [0.0]
    for i in range(1, len(pts)):
        s.append(s[-1] + (pts[i] - pts[i - 1]).length)
    return pts, s


def _at(pts, s, d):
    lo, hi = 0, len(s) - 1
    while hi - lo > 1:
        m = (lo + hi) // 2
        if s[m] < d: lo = m
        else: hi = m
    k = (d - s[lo]) / max(1e-9, s[hi] - s[lo])
    p = pts[lo].lerp(pts[hi], k)
    t = (pts[hi] - pts[lo]).normalized()
    return p, t


def wavy_wall(name="wall", loc=(0, 0, 0), L=6.0, height=1.5, amp=0.32, wave=2.4, thick=1, coping=True, seed=1, rot_z=0.0):
    """Crinkle-crankle (amp > 0) or straight (amp = 0) wall, `thick` bricks thick, centred on loc, along local X. Returns the object."""
    rnd = random.Random(seed)
    mats = brick_mats()
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    pts, s = _path(L, amp, wave)
    total = s[-1]
    rows = int(height / (BH + MJ))
    depth = BW * thick + MJ * (thick - 1)
    for r in range(rows):
        z = r * (BH + MJ) + BH / 2
        off = (BL + MJ) / 2 if r % 2 else 0.0
        d = off - (BL + MJ) / 2
        while d < total:
            a, b = max(0.0, d), min(total, d + BL)
            if b - a > 0.03:
                p, t = _at(pts, s, (a + b) / 2)
                for k in range(thick):
                    nrm = Vector((-t.y, t.x, 0))
                    c = p + nrm * ((k - (thick - 1) / 2) * (BW + MJ)) + Vector((0, 0, z))
                    _add_box(bm, c, t, ((b - a) * 0.985, BW * (0.97 + 0.03 * rnd.random()), BH), rnd.randrange(len(mats)))
            d += BL + MJ
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    for m in mats: o.data.materials.append(m)
    # mortar core (fills the joints)
    core = C.loft(name + "_mortar", [[(p.x + n_.x * w, p.y + n_.y * w, zz) for (w, zz) in ((-depth * 0.42, 0.0), (depth * 0.42, 0.0),
                                                                                         (depth * 0.42, rows * (BH + MJ) - MJ), (-depth * 0.42, rows * (BH + MJ) - MJ))]
                                      for p, n_ in _ribbon(pts)], mortar_mat(), close_u=True, cap_start=True, cap_end=True, smooth=False) \
        if hasattr(C, "loft") else None
    parts = [o] + ([core] if core else [])
    if coping:                                                   # brick-on-edge coping course on top
        cm = bpy.data.meshes.new(name + "_cap"); bm = bmesh.new()
        z = rows * (BH + MJ) + BL * 0.0 + BW / 2
        d = 0.0
        while d < total:
            p, t = _at(pts, s, min(total, d + BH / 2))
            _add_box(bm, p + Vector((0, 0, rows * (BH + MJ) + BW / 2)), t, (BH, depth + 0.02, BW), rnd.randrange(len(mats)))
            d += BH + MJ
        bm.to_mesh(cm); bm.free()
        co = bpy.data.objects.new(name + "_cap", cm); bpy.context.scene.collection.objects.link(co)
        for m in mats: co.data.materials.append(m)
        parts.append(co)
    root = bpy.data.objects.new(name + "_root", None); bpy.context.scene.collection.objects.link(root)
    for p in parts:
        p.parent = root
    root.location = loc; root.rotation_euler = (0, 0, rot_z)
    root["top_z"] = rows * (BH + MJ) + (BW if coping else 0)
    return root


def _ribbon(pts, step=6):
    out = []
    for i in range(0, len(pts), step):
        a = pts[max(0, i - 1)]; b = pts[min(len(pts) - 1, i + 1)]
        t = (b - a).normalized(); out.append((pts[i], Vector((-t.y, t.x, 0))))
    if (len(pts) - 1) % step:
        a, b = pts[-2], pts[-1]; t = (b - a).normalized(); out.append((pts[-1], Vector((-t.y, t.x, 0))))
    return out


def wall_point(L, amp, wave, x, loc=(0, 0, 0)):
    """World point on the wall centre line at local x (for hands, arrows, trees)."""
    return Vector(loc) + Vector((x, amp * math.sin(2 * math.pi * x / wave), 0))


def straight_wall(name="swall", loc=(0, 0, 0), L=3.0, height=1.5, thick=1, piers=0, seed=2):
    """Straight wall whose origin is the base FRONT edge centre (rotate about X to topple it backwards/forwards)."""
    w = wavy_wall(name, (0, 0, 0), L=L, height=height, amp=0.0, thick=thick, seed=seed)
    depth = BW * thick + MJ * (thick - 1)
    pivot = bpy.data.objects.new(name + "_pivot", None); bpy.context.scene.collection.objects.link(pivot)
    w.parent = pivot; w.location = (0, depth / 2, 0)
    if piers:
        mats = brick_mats()
        for i in range(piers):
            x = -L / 2 + L * (i + 0.5) / piers
            p = C.rbox(f"{name}_pier{i}", (BL * 1.6, BL * 1.6, height + 0.06), (x, depth / 2 - BL * 0.5 - depth / 2, (height + 0.06) / 2),
                       mat=mats[i % len(mats)], bevel=0.006)
            p.parent = pivot
    pivot.location = loc
    return pivot


def paper_sheet(name="paper", loc=(0, 0, 0), w=0.21, h=0.297, zigzag=False, folds=6, angle=38.0, rot_z=0.0):
    """Sheet of paper standing on its long edge; zigzag folds it (accordion) so it stands by itself."""
    mat = C.pbr("paper", "#FBF8F1", 0.7, sss=0.05)
    verts, faces = [], []
    n = folds if zigzag else 1
    seg = w / n
    a = math.radians(angle) if zigzag else 0.0
    x = -w * math.cos(a) / 2; y = 0.0
    xs = [(x, y)]
    for i in range(n):
        dy = (seg * math.sin(a)) * (1 if i % 2 == 0 else -1)
        x += seg * math.cos(a); y += dy
        xs.append((x, y))
    for (px, py) in xs:
        verts += [(px, py, 0.0), (px, py, h)]
    for i in range(n):
        faces.append((2 * i, 2 * i + 2, 2 * i + 3, 2 * i + 1))
    o = C.mesh_obj(name, verts, faces, mat, smooth=False, sharp=None)
    sol = o.modifiers.new("thick", "SOLIDIFY"); sol.thickness = 0.0012
    root = bpy.data.objects.new(name + "_root", None); bpy.context.scene.collection.objects.link(root)
    o.parent = root; root.location = loc; root.rotation_euler = (0, 0, rot_z)
    return root


def fruit_tree(name="tree", loc=(0, 0, 0), s=1.0, seed=3, fruit="#E2392F"):
    rnd = random.Random(seed)
    bark = C.pbr("bark", "#5B3A22", 0.9, bump="noise", bscale=60.0, bstr=0.5)
    leaf = C.pbr("leaves", "#4E8F3A", 0.8, bump="noise", bscale=30.0, bstr=0.6, cvar=0.15)
    fm = C.pbr("fruit_" + fruit, fruit, 0.35, coat=0.6)
    parts = [C.cyl(name + "_trunk", 0.035 * s, 0.9 * s, (0, 0, 0.45 * s), mat=bark, verts=12)]
    for i in range(3):                                            # espalier arms along the wall
        for sd in (-1, 1):
            z = (0.55 + 0.25 * i) * s
            parts.append(C.cyl(f"{name}_arm{i}{sd}", 0.018 * s, 0.55 * s, (sd * 0.27 * s, 0, z), rot=(0, math.radians(90), 0), mat=bark, verts=8))
    for i in range(9):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=(0.12 + 0.05 * rnd.random()) * s,
                                              location=(rnd.uniform(-0.45, 0.45) * s, rnd.uniform(-0.04, 0.04) * s, rnd.uniform(0.55, 1.15) * s))
        lb = bpy.context.object; lb.name = f"{name}_leaf{i}"; lb.data.materials.append(leaf); lb.scale = (1.0, 0.45, 0.8); parts.append(lb)
    for i in range(10):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.028 * s, location=(rnd.uniform(-0.42, 0.42) * s, -0.07 * s, rnd.uniform(0.55, 1.12) * s), segments=16, ring_count=10)
        f = bpy.context.object; f.name = f"{name}_fruit{i}"; f.data.materials.append(fm)
        for p in f.data.polygons: p.use_smooth = True
        parts.append(f)
    root = bpy.data.objects.new(name + "_root", None); bpy.context.scene.collection.objects.link(root)
    for p in parts: p.parent = root
    root.location = loc
    return root


def sun_disc(loc=(0, 3, 4), r=0.45, strength=12.0):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=32, ring_count=16)
    o = bpy.context.object; o.name = "sun"; o.data.materials.append(C.emission("sun_glow", "#FFD27A", strength))
    return o


def arrow3d(name, start, end, r=0.025, col="#FFC93C"):
    """Glowing arrow from start to end (cylinder shaft + cone head)."""
    m = C.pbr("arrow_" + col, col, 0.4, emit=col, estr=0.8)
    a, b = Vector(start), Vector(end); d = b - a; L = d.length
    head = min(0.12, L * 0.35)
    shaft = C.cyl(name + "_shaft", r, L - head, (0, 0, (L - head) / 2), mat=m, verts=16)
    bpy.ops.mesh.primitive_cone_add(radius1=r * 2.6, radius2=0.0, depth=head, location=(0, 0, L - head / 2), vertices=24)
    cone = bpy.context.object; cone.name = name + "_head"; cone.data.materials.append(m)
    root = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(root)
    shaft.parent = root; cone.parent = root
    root.location = a; root.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    return root
