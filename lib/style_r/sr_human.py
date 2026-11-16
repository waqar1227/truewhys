"""Style R people: MPFB 2 base human (CC0 output) with stylised proportions + our own code-built eyes, hair, clothes, brows.
Works without the MakeHuman asset pack (its server is often down): clothes are painted face regions of the body pushed out
a few mm (toy-like, flat clean colours), hair is MPFB's own hair helper shell puffed out, eyes are our spheres on the eye bones.
Faces move with MPFB expression-unit shape keys (blink, squint, brows, smile, mouth open) and the default rig's bones.

build(spec) -> dict(body, rig, eyes=[L, R], keys={name: shape key}, top=height)
spec keys: macro{gender, age, muscle, weight, proportions, height}, targets{path: w}, skin, hair, hair_style ('short'|'bun'|'bald'),
           shirt, trousers, shoes, sleeve ('short'|'long'), iris, brow, loc [x,y,z], rot_z (deg).
Needs MPFB 2.0.18 installed in bpy (docs/audit/style_r/README.md step 1).
"""
import math, os
import bpy, bmesh, addon_utils
from mathutils import Vector, Matrix
from sr_common import srgb, pbr, _new

EXPR = ["eye-left-closure", "eye-right-closure", "eye-left-slit", "eye-right-slit", "eye-left-opened-up", "eye-right-opened-up",
        "eyebrows-left-up", "eyebrows-right-up", "eyebrows-left-down", "eyebrows-right-down", "eyebrows-left-inner-up", "eyebrows-right-inner-up",
        "mouth-corner-puller", "mouth-open", "mouth-depression", "mouth-pursing", "mouth-compression", "nose-left-elevation", "nose-right-elevation"]

TORSO = ("spine", "breast", "clavicle", "shoulder01", "neck01")
UPPERARM = ("upperarm01", "upperarm02")
LOWERARM = ("lowerarm01", "lowerarm02")
LEGS = ("pelvis", "upperleg", "lowerleg")
FEET = ("foot", "toe")


def _svc():
    addon_utils.enable("bl_ext.user_default.mpfb", default_set=True)
    from bl_ext.user_default.mpfb.services.humanservice import HumanService
    from bl_ext.user_default.mpfb.services.targetservice import TargetService
    from bl_ext.user_default.mpfb.services.locationservice import LocationService
    return HumanService, TargetService, LocationService


def skin_mat(hexcol):
    return pbr(f"skin_{hexcol}", hexcol, 0.5, sss=0.18, sss_radius=(1.0, 0.4, 0.25), sss_scale=0.01, bump="noise", bscale=900, bstr=0.04,
               color2=None, cvar=0.03, cscale=30)


def cloth_mat(hexcol, name):
    return pbr(f"{name}_{hexcol}", hexcol, 0.75, sheen=0.4, bump="weave", bscale=900, bstr=0.08, cvar=0.04, cscale=12)


def hair_mat(hexcol):
    return pbr(f"hair_{hexcol}", hexcol, 0.5, coat=0.0, bump="noise", bscale=420, bstr=0.5, cvar=0.18, cscale=60, stretch=(1, 1, 0.2), sheen=0.15)


def eye_mat(iris="#4C6B3A"):
    """Ball material in object space: iris/pupil around local -Y (the eye looks along its object's -Y)."""
    m, nt, b = _new(f"eye_{iris}")
    N = nt.nodes.new; L = nt.links.new
    tc = N("ShaderNodeTexCoord"); nrm = N("ShaderNodeVectorMath"); nrm.operation = "NORMALIZE"; L(tc.outputs["Object"], nrm.inputs[0])
    sp = N("ShaderNodeSeparateXYZ"); L(nrm.outputs[0], sp.inputs[0])
    # angle from -Y: d = 1 + y  (0 at the pupil centre, 1 at the side, 2 at the back)
    d = N("ShaderNodeMath"); d.operation = "ADD"; d.inputs[1].default_value = 1.0; L(sp.outputs["Y"], d.inputs[0])
    ramp = N("ShaderNodeValToRGB"); e = ramp.color_ramp.elements
    e[0].position = 0.0; e[0].color = (0.004, 0.004, 0.004, 1); e[1].position = 0.035; e[1].color = (0.004, 0.004, 0.004, 1)
    for pos, col in ((0.045, "#22301A"), (0.09, iris), (0.125, "#2B3A20"), (0.14, "#141A10"), (0.16, "#F7F2EC"), (0.9, "#F7EEE8"), (1.3, "#EBC9C2")):
        el = ramp.color_ramp.elements.new(min(pos / 1.3, 1.0)); el.color = srgb(col)
    mr = N("ShaderNodeMath"); mr.operation = "DIVIDE"; mr.inputs[1].default_value = 1.3; L(d.outputs[0], mr.inputs[0])
    L(mr.outputs[0], ramp.inputs["Fac"]); L(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.08; b.inputs["Coat Weight"].default_value = 1.0; b.inputs["Coat Roughness"].default_value = 0.0
    b.inputs["Subsurface Weight"].default_value = 0.15; b.inputs["Subsurface Scale"].default_value = 0.003
    return m


def _vg_members(obj, names):
    idx = {obj.vertex_groups[n].index for n in names if n in obj.vertex_groups}
    out = set()
    for v in obj.data.vertices:
        for g in v.groups:
            if g.group in idx and g.weight > 0.3:
                out.add(v.index); break
    return out


def _dominant_bone(obj, rig_bones):
    gi = {g.index: g.name for g in obj.vertex_groups if g.name in rig_bones}
    dom = {}
    for v in obj.data.vertices:
        best, bw = None, 0.0
        for g in v.groups:
            if g.group in gi and g.weight > bw:
                best, bw = gi[g.group], g.weight
        dom[v.index] = best or ""
    return dom


def build(spec, name="person"):
    HS, TS, LS = _svc()
    macro = TS.get_default_macro_info_dict()
    macro.update({k: v for k, v in spec.get("macro", {}).items() if k != "race"})
    macro["race"] = spec.get("macro", {}).get("race", {"asian": 0.0, "caucasian": 1.0, "african": 0.0})
    body = HS.create_human(macro_detail_dict=macro)
    body.name = name
    tdir = LS.get_mpfb_data("targets")
    for t, w in spec.get("targets", {}).items():
        TS.load_target(body, os.path.join(tdir, t + ".target.gz"), weight=w, name=t.replace("/", "_"))
    # stylised default: bigger head and eyes (audit §6.2: head ~15 % bigger, larger eyes)
    for t, w in (("head/head-scale-vert-incr", 0.5), ("head/head-scale-horiz-incr", 0.45), ("head/head-scale-depth-incr", 0.4),
                 ("eyes/l-eye-scale-incr", 0.55), ("eyes/r-eye-scale-incr", 0.55)):
        if t not in spec.get("targets", {}):
            TS.load_target(body, os.path.join(tdir, t + ".target.gz"), weight=w, name=t.replace("/", "_"))
    keys = {}
    for u in EXPR:
        p = os.path.join(tdir, "expression/units/caucasian", u + ".target.gz")
        if os.path.exists(p):
            TS.load_target(body, p, weight=0.0, name="x_" + u)
    HS.add_builtin_rig(body, "default")
    rig = body.parent
    for m in list(body.modifiers):
        if m.type != "ARMATURE":
            body.modifiers.remove(m)
    sk = body.data.shape_keys
    if sk:
        for kb in sk.key_blocks:
            if kb.name.startswith("x_"):
                keys[kb.name[2:]] = kb
                kb.slider_min = -0.5
    # ---- rest-pose geometry with all non-expression keys applied (for measuring)
    def rest_co():
        if not sk:
            return [v.co.copy() for v in body.data.vertices]
        base = sk.key_blocks[0]
        co = [v.co.copy() for v in base.data]
        for kb in sk.key_blocks[1:]:
            if kb.name.startswith("x_") or kb.value == 0:
                continue
            for i, (a, b) in enumerate(zip(kb.data, base.data)):
                co[i] += (a.co - b.co) * kb.value
        return co
    co = rest_co()
    mw = body.matrix_world
    eyeL = _vg_members(body, ["helper-l-eye"]); eyeR = _vg_members(body, ["helper-r-eye"])
    hair = _vg_members(body, ["helper-hair"])
    allhelp = _vg_members(body, ["HelperGeometry", "JointCubes"])
    def centre(ix):
        pts = [mw @ co[i] for i in ix]
        c = sum(pts, Vector()) / len(pts)
        r = sum((p - c).length for p in pts) / len(pts)
        return c, r
    cL, rL = centre(eyeL); cR, rR = centre(eyeR)
    top = max((mw @ co[i]).z for i in range(len(co)) if i not in allhelp)
    rig_bones = {b.name for b in rig.data.bones}
    dom = _dominant_bone(body, rig_bones)
    style = spec.get("hair_style", "short")
    kill = allhelp            # all helpers go (MPFB's hair helper is long strips); hair = a scalp cap painted + pushed out
    # ---- materials: 0 skin, 1 shirt, 2 trousers, 3 shoes
    mats = [skin_mat(spec.get("skin", "#E8B48E")), cloth_mat(spec.get("shirt", "#FF6B5B"), "shirt"), cloth_mat(spec.get("trousers", "#2E3A55"), "trousers"),
            pbr(f"shoes_{spec.get('shoes', '#2A2420')}", spec.get("shoes", "#2A2420"), 0.45, coat=0.3)]
    hm = hair_mat(spec.get("hair", "#3B2A1E"))
    body.data.materials.clear()
    for m in mats:
        body.data.materials.append(m)
    sleeve_long = spec.get("sleeve", "short") == "long"
    B = rig.data.bones
    J = lambda n: (rig.matrix_world @ B[n].head_local) if n in B else None
    neck_z = J("neck01").z; waist_z = J("spine05").z + 0.02 if "spine05" in B else J("pelvis.L").z + 0.09
    ank_z = J("foot.L").z
    def arm_t(q, side):
        """position along the arm: 0 shoulder, 1 elbow, 2 wrist."""
        sh, el, wr = J(f"upperarm01.{side}"), J(f"lowerarm01.{side}"), J(f"wrist.{side}")
        u = (el - sh); t1 = (q - sh).dot(u) / u.length_squared
        if t1 <= 1.0:
            return t1
        v = (wr - el); return 1.0 + (q - el).dot(v) / v.length_squared
    ARM = ("upperarm", "lowerarm", "wrist", "finger", "metacarpal")
    sleeve_end = 1.85 if sleeve_long else spec.get("sleeve_t", 0.55)
    ecz = (cL.z + cR.z) / 2
    def face_region(c, b):
        if b.startswith(("head", "jaw", "special", "oris", "levator", "orbicularis", "oculi", "temporalis", "risorius", "eye", "tongue")):
            return 0
        if b.startswith(ARM):
            side = "L" if c.x > 0 else "R"
            return 1 if arm_t(c, side) < sleeve_end else 0
        if c.z < ank_z + 0.035 and b.startswith(("foot", "toe", "lowerleg")):
            return 3
        if b.startswith(("lowerleg", "upperleg", "pelvis")) or c.z < waist_z:
            return 2 if c.z > ank_z + 0.035 else 3
        # torso: smooth crew neckline (dips 2 cm at the front)
        nl = neck_z - 0.018 - 0.022 * max(0.0, 1 - (c.x / 0.075) ** 2) * (1.0 if c.y < J("neck01").y else 0.25)
        return 1 if c.z < nl else 0
    for p in body.data.polygons:
        vs = list(p.vertices)
        c = sum((mw @ co[v] for v in vs), Vector()) / len(vs)
        bs = [dom.get(v, "") for v in vs]
        p.material_index = face_region(c, max(set(bs), key=bs.count))
    # cranium (verts above the eyes, head bone) for the hair cap and brows
    ec = (cL + cR) / 2
    head_pts = [mw @ co[i] for i in range(len(co)) if i not in allhelp and dom.get(i, "").startswith("head")]
    cran = [q for q in head_pts if q.z > ec.z]
    # ---- delete all helpers (MPFB's hair helper is long strips; eyes/brows/hair are ours)
    bm = bmesh.new(); bm.from_mesh(body.data); bm.verts.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[bm.verts[i] for i in allhelp], context="VERTS")
    bm.to_mesh(body.data); bm.free()
    for p in body.data.polygons:
        p.use_smooth = True
    body.modifiers.new("smooth", "SUBSURF").levels = 0
    body.modifiers["smooth"].render_levels = 1
    clothes = [_cloth_layer(body, rig, k, push, iters=it) for k, push, it in ((1, spec.get("shirt_push", 0.009), 30), (2, 0.006, 12), (3, 0.008, 12))]
    hair = None
    if style != "bald":
        body.data.materials.append(hm)            # index 4 = hair on the scalp (also under the hair layer)
        hl = spec.get("hairline", 3.6)
        sk = body.data.shape_keys
        co2 = rest_co()                                   # shaped rest positions (after the helper delete)
        for p in body.data.polygons:
            if p.material_index != 0:
                continue
            c = mw @ (sum((co2[v] for v in p.vertices), Vector()) / len(p.vertices))
            f = max(0.0, min(1.0, (ec.y + rL * 6.0 - c.y) / (rL * 7.0)))        # 1 at the forehead, 0 at the back
            zt = ec.z + rL * (hl * f - 3.2 * (1 - f)) + rL * 0.12 * math.sin((c.x - ec.x) / rL * 1.1) * f
            if abs(c.x - ec.x) > rL * 4.4 and c.y > ec.y + rL * 1.0:       # above the ears: lift the line
                zt = max(zt, ec.z + rL * 0.9)
            if c.z > zt and c.z > ec.z - rL * 6.5 and c.y > ec.y - rL * 2.0 - 99 * (c.z > ec.z + rL * 2.0):
                p.material_index = 4
        hair = _cloth_layer(body, rig, 4, spec.get("hair_puff", rL * 1.3), edge=0.4, iters=6)
        tx = bpy.data.textures.new(f"{name}_hairtex", "CLOUDS"); tx.noise_scale = 0.035; tx.noise_depth = 2
        dt = hair.modifiers.new("tousle", "DISPLACE"); dt.texture = tx; dt.strength = rL * 0.45; dt.vertex_group = "tw_push"; dt.texture_coords = "LOCAL"
        hair.modifiers.move(len(hair.modifiers) - 1, len(hair.modifiers) - 2)
    # hems: a fitted band on every opening of every clothes layer (collar, cuffs, shirt hem, trouser cuffs)
    hems = []
    for o in clothes:
        if o is not None:
            hems += _hems_for(o, rig, rig_bones, o.data.materials[o.data.polygons[0].material_index] if o.data.polygons else None)
    brows = _brows(body, rig, keys, head_pts, cL, cR, rL, spec.get("brow", spec.get("hair", "#3B2A1E")), name)
    # ---- eyes: our spheres on the eye bones
    eyes = []
    em = eye_mat(spec.get("iris", "#4C6B3A"))
    for c, r, side in ((cL, rL, "L"), (cR, rR, "R")):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 1.08, location=c, segments=48, ring_count=24)
        e = bpy.context.object; e.name = f"{name}_eye{side}"; e.data.materials.append(em)
        for p in e.data.polygons:
            p.use_smooth = True
        bone = rig.data.bones.get(f"eye.{side}")
        if bone:
            mwe = e.matrix_world.copy()
            e.parent = rig; e.parent_type = "BONE"; e.parent_bone = bone.name
            e.matrix_world = mwe
        eyes.append(e)
    if style == "bun":
        _bun(rig, cL, cR, rL, top, hm, name)
    # place in the scene
    if spec.get("loc"):
        rig.location = spec["loc"]
    if spec.get("rot_z"):
        rig.rotation_euler = (0, 0, math.radians(spec["rot_z"]))
    for b in rig.pose.bones:
        b.rotation_mode = "XYZ"
    return dict(body=body, rig=rig, eyes=eyes, keys=keys, top=top, eye_c=(cL + cR) / 2, eye_r=rL, clothes=clothes, hair=hair, brows=brows, hems=hems)


def _cloth_layer(body, rig, k, push, edge=0.0, iters=12):
    """Separate clothes object for material k: a copy of those body faces, smoothed (no body detail shows) and pushed out,
    tapering to 0 at the openings so it meets the skin cleanly."""
    if not any(p.material_index == k for p in body.data.polygons):
        return None
    me = body.data.copy(); o = bpy.data.objects.new(f"{body.name}_cloth{k}", me)
    bpy.context.scene.collection.objects.link(o); o.matrix_world = body.matrix_world
    o.parent = body.parent; o.matrix_parent_inverse = body.matrix_parent_inverse.copy()
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index != k], context="FACES")
    bm.to_mesh(me); bm.free()
    if me.shape_keys:
        # apply the mix: keep only the mixed shape as the base
        sk = me.shape_keys.key_blocks
        mix = [v.co.copy() for v in sk[0].data]
        for kb in sk[1:]:
            if kb.value:
                for i, (a, b) in enumerate(zip(kb.data, sk[0].data)):
                    mix[i] += (a.co - b.co) * kb.value
        o.shape_key_clear()
        for v, c in zip(me.vertices, mix):
            v.co = c
    # distance-from-opening weights (0 at the boundary, 1 after 3 rings)
    bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
    dist = {v.index: (0 if v.is_boundary else None) for v in bm.verts}
    front = [v for v in bm.verts if v.is_boundary]
    for ring in range(1, 4):
        nxt = []
        for v in front:
            for e in v.link_edges:
                w = e.other_vert(v)
                if dist[w.index] is None:
                    dist[w.index] = ring; nxt.append(w)
        front = nxt
    bm.free()
    g = o.vertex_groups.new(name="tw_push")
    for i, dd in dist.items():
        g.add([i], 1.0 if dd is None else edge + (1 - edge) * dd / 3.0, "REPLACE")
    for m in list(o.modifiers):
        o.modifiers.remove(m)
    am = o.modifiers.new("rig", "ARMATURE"); am.object = rig
    sm = o.modifiers.new("smooth", "SMOOTH"); sm.factor = 0.9; sm.iterations = iters; sm.vertex_group = "tw_push"
    dp = o.modifiers.new("push", "DISPLACE"); dp.strength = push; dp.mid_level = 0.0; dp.vertex_group = "tw_push"
    sb = o.modifiers.new("soft", "SUBSURF"); sb.levels = 0; sb.render_levels = 1
    for p in me.polygons:
        p.use_smooth = True
    return o


def _hems_for(o, rig, rig_bones, mat, pad=0.005, band=0.011):
    """Find the boundary loops of a clothes layer and put a band on each (fitted ellipse, parented to the loop's main bone)."""
    import numpy as np
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
    bverts = {v.index for v in bm.verts if v.is_boundary}
    adj = {i: set() for i in bverts}
    for e in bm.edges:
        if e.is_boundary:
            a, b = e.verts[0].index, e.verts[1].index; adj[a].add(b); adj[b].add(a)
    bm.free()
    seen, loops = set(), []
    for i in bverts:
        if i in seen:
            continue
        comp, stack = [], [i]; seen.add(i)
        while stack:
            j = stack.pop(); comp.append(j)
            for k in adj[j]:
                if k not in seen:
                    seen.add(k); stack.append(k)
        if len(comp) >= 10:
            loops.append(comp)
    gi = {g.index: g.name for g in o.vertex_groups if g.name in rig_bones}
    out = []
    for n_, comp in enumerate(loops):
        P = np.array([tuple(o.matrix_world @ me.vertices[i].co) for i in comp])
        c = P.mean(0); U, S, Vt = np.linalg.svd(P - c); nrm = Vector(Vt[2]); a = Vector(Vt[0]); b = Vector(Vt[1])
        ra = float(np.abs((P - c) @ Vt[0]).max()) + pad; rb = float(np.abs((P - c) @ Vt[1]).max()) + pad
        votes = {}
        for i in comp:
            for g in me.vertices[i].groups:
                if g.group in gi:
                    votes[gi[g.group]] = votes.get(gi[g.group], 0) + g.weight
        bone = max(votes, key=votes.get) if votes else None
        out.append(_band(Vector(c), nrm, a, b, ra, rb, pad, band, mat, rig, bone, f"{o.name}_hem{n_}"))
    return out


def _band(c, n, a, b, ra, rb, pad, band, mat, rig, bone, name):
    bm = bmesh.new(); N = 48
    def row(h, rr):
        return [bm.verts.new(c + n * h + a * ((ra - rr) * math.cos(2 * math.pi * i / N)) + b * ((rb - rr) * math.sin(2 * math.pi * i / N))) for i in range(N)]
    loop = [row(-band / 2, 0), row(band / 2, 0), row(band / 2, pad * 0.9), row(-band / 2, pad * 0.9)]
    for j in range(4):
        r0, r1 = loop[j], loop[(j + 1) % 4]
        for i in range(N):
            bm.faces.new((r0[i], r0[(i + 1) % N], r1[(i + 1) % N], r1[i]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    if mat:
        o.data.materials.append(mat)
    for p in me.polygons:
        p.use_smooth = True
    sb = o.modifiers.new("soft", "SUBSURF"); sb.levels = 1; sb.render_levels = 2
    if bone and bone in rig.data.bones:
        mwo = o.matrix_world.copy(); o.parent = rig; o.parent_type = "BONE"; o.parent_bone = bone; o.matrix_world = mwo
    return o


def _ring(pts, P, n, mat, rig, bone, pad, name, side=None, band=0.01):
    """Elliptical band hugging the body section through P (plane normal n); parented to `bone`."""
    sel = [q for q in pts if abs((q - P).dot(n)) < 0.006 and (q - P).length < 0.22 and (side is None or (q.x > 0) == (side == "L"))]
    if len(sel) < 8:
        return None
    c = sum(sel, Vector()) / len(sel)
    a = n.orthogonal().normalized(); b = n.cross(a).normalized()
    ra = max(abs((q - c).dot(a)) for q in sel) + pad; rb = max(abs((q - c).dot(b)) for q in sel) + pad
    bm = bmesh.new(); N = 48
    rings = []
    for k, h in enumerate((-band / 2, band / 2)):
        row = []
        for i in range(N):
            t = 2 * math.pi * i / N
            row.append(bm.verts.new(c + n * h + a * (ra * math.cos(t)) + b * (rb * math.sin(t))))
        rings.append(row)
    inner = [[bm.verts.new(c + n * h + a * ((ra - pad * 0.8) * math.cos(2 * math.pi * i / N)) + b * ((rb - pad * 0.8) * math.sin(2 * math.pi * i / N)))
              for i in range(N)] for h in (band / 2, -band / 2)]
    loop = [rings[0], rings[1], inner[0], inner[1]]
    for j in range(4):
        r0, r1 = loop[j], loop[(j + 1) % 4]
        for i in range(N):
            bm.faces.new((r0[i], r0[(i + 1) % N], r1[(i + 1) % N], r1[i]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(mat)
    for p in me.polygons:
        p.use_smooth = True
    bv = o.modifiers.new("soft", "SUBSURF"); bv.levels = 1; bv.render_levels = 2
    if bone in rig.data.bones:
        mwo = o.matrix_world.copy(); o.parent = rig; o.parent_type = "BONE"; o.parent_bone = bone; o.matrix_world = mwo
    return o


def _hair_cap(rig, cran, ec, r, top, mat, name, hairline=0.30):
    """Clean, toy-like short-hair cap: an ellipsoid fitted to the cranium, cut along a smooth hairline."""
    cx = sum(q.x for q in cran) / len(cran); cy = sum(q.y for q in cran) / len(cran)
    rx = max(abs(q.x - cx) for q in cran) * 1.07; ry = max(abs(q.y - cy) for q in cran) * 1.07
    cz = ec.z; rz = (top - ec.z) * 1.06
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0), segments=64, ring_count=32)
    o = bpy.context.object; o.name = f"{name}_hair"
    bm = bmesh.new(); bm.from_mesh(o.data)
    kill = []
    for v in bm.verts:
        x, y, z = v.co
        f = (1 - y) / 2                       # 1 at the face (-Y), 0 at the back
        fx = abs(x)
        zt = hairline * f ** 1.5 - 0.55 * (1 - f) ** 1.2 + 0.05 * math.sin(x * 9.0) * f
        if fx > 0.85 and f > 0.35:            # keep a little sideburn above the ears
            zt = min(zt, 0.05)
        if z < zt:
            kill.append(v)
    bmesh.ops.delete(bm, geom=kill, context="VERTS"); bm.to_mesh(o.data); bm.free()
    o.scale = (rx, ry, rz); o.location = (cx, cy + ry * 0.04, cz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    s = o.modifiers.new("thick", "SOLIDIFY"); s.thickness = -r * 0.25; s.offset = 1.0
    o.modifiers.new("soft", "SUBSURF").levels = 1
    mwo = o.matrix_world.copy()
    o.parent = rig; o.parent_type = "BONE"; o.parent_bone = "head"; o.matrix_world = mwo
    return o


def _brows(body, rig, keys, head_pts, cL, cR, r, col, name):
    """Two soft brow arcs on the face surface, parented to the head bone and driven by the eyebrow shape keys."""
    from sr_common import tube
    m = pbr(f"brow_{col}", col, 0.6, bump="noise", bscale=500, bstr=0.3)
    out = []
    for ce, side, sgn in ((cL, "left", 1), (cR, "right", -1)):
        pts = []
        for k in range(7):
            t = k / 6.0
            x = ce.x + sgn * (t - 0.42) * r * 2.9
            z = ce.z + r * 1.75 + r * 0.45 * math.sin(math.pi * min(1, t * 1.15)) - r * 0.25 * t
            near = [q for q in head_pts if abs(q.x - x) < r * 0.35 and abs(q.z - z) < r * 0.35]
            y = (min(q.y for q in near) if near else ce.y - r) - r * 0.05
            pts.append((x, y, z))
        b = tube(f"{name}_brow_{side}", pts, r * 0.30, mat=m, n=8)
        mwo = b.matrix_world.copy()
        b.parent = rig; b.parent_type = "BONE"; b.parent_bone = "head"; b.matrix_world = mwo
        # drivers: brow up/down follows the shape keys (bone space Y ~ up)
        up, dn = keys.get(f"eyebrows-{side}-up"), keys.get(f"eyebrows-{side}-down")
        if up is not None and dn is not None:
            fc = b.driver_add("delta_location", 1); d = fc.driver; d.type = "SCRIPTED"
            for nm, kb in (("u", up), ("d", dn)):
                v = d.variables.new(); v.name = nm; v.type = "SINGLE_PROP"
                v.targets[0].id_type = "KEY"; v.targets[0].id = body.data.shape_keys; v.targets[0].data_path = f'key_blocks["{kb.name}"].value'
            d.expression = f"{r * 0.6:.5f}*u - {r * 0.45:.5f}*d"
        out.append(b)
    return out


def _bun(rig, cL, cR, r, top, mat, name):
    """Neat bun at the back of the head (parented to the head bone)."""
    ec = (cL + cR) / 2
    loc = Vector((ec.x, ec.y + r * 7.2, top - r * 2.2))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 2.3, location=loc, segments=32, ring_count=16)
    o = bpy.context.object; o.name = f"{name}_bun"; o.data.materials.append(mat); o.scale = (1.0, 0.85, 0.9)
    for p in o.data.polygons:
        p.use_smooth = True
    mwo = o.matrix_world.copy()
    o.parent = rig; o.parent_type = "BONE"; o.parent_bone = "head"; o.matrix_world = mwo
    return o


# ------------------------------------------------------------------ posing helpers

def pose(rig, bone, rot_deg, frame=None):
    pb = rig.pose.bones.get(bone)
    if pb is None:
        return
    pb.rotation_mode = "XYZ"; pb.rotation_euler = [math.radians(a) for a in rot_deg]
    if frame is not None:
        pb.keyframe_insert("rotation_euler", frame=frame)


def expr(keys, name, value, frame=None):
    kb = keys.get(name)
    if kb is None:
        return
    kb.value = value
    if frame is not None:
        kb.keyframe_insert("value", frame=frame)


def relax_arms(rig, frame=None, out=38):
    for side, s in (("L", 1), ("R", -1)):
        pose(rig, f"upperarm01.{side}", (0, 0, -out * s), frame)


# ------------------------------------------------------------------ controls (animate empties, not bones)

def controls(h):
    """IK hand targets + pole targets and a head look-at target. Returns dict(handL, handR, look) empties (world space).
    Move/key the empties to animate: hands reach, head turns (influence 0.7 so the neck shares it)."""
    rig = h["rig"]; B = rig.data.bones
    out = {}
    for side in ("L", "R"):
        wr = rig.matrix_world @ B[f"wrist.{side}"].head_local
        el = rig.matrix_world @ B[f"lowerarm01.{side}"].head_local
        t = bpy.data.objects.new(f"{h['body'].name}_hand{side}", None); bpy.context.scene.collection.objects.link(t)
        t.location = wr; t.empty_display_size = 0.04
        p = bpy.data.objects.new(f"{h['body'].name}_pole{side}", None); bpy.context.scene.collection.objects.link(p)
        p.location = el + Vector((0.18 if side == "L" else -0.18, 0.30, -0.35))
        c = rig.pose.bones[f"lowerarm02.{side}"].constraints.new("IK")
        c.target = t; c.pole_target = p; c.chain_count = 4; c.pole_angle = math.radians(-90 if side == "L" else -90)
        c.use_stretch = False
        out[f"hand{side}"] = t; out[f"pole{side}"] = p
    hd = rig.matrix_world @ B["head"].head_local
    lk = bpy.data.objects.new(f"{h['body'].name}_look", None); bpy.context.scene.collection.objects.link(lk)
    lk.location = hd + Vector((0, -1.0, 0.08))
    for bn, inf in (("neck02", 0.35), ("head", 0.7)):
        if bn in rig.pose.bones:
            m3 = B[bn].matrix_local.to_3x3()
            fwd = Vector((0, -1, 0))                       # the face looks along world -Y in rest
            axes = {"TRACK_X": m3.col[0], "TRACK_NEGATIVE_X": -m3.col[0], "TRACK_Z": m3.col[2], "TRACK_NEGATIVE_Z": -m3.col[2]}
            ax = max(axes, key=lambda k: axes[k].dot(fwd))
            c = rig.pose.bones[bn].constraints.new("DAMPED_TRACK"); c.target = lk; c.track_axis = ax; c.influence = inf
    out["look"] = lk
    return out


def key_loc(o, frame, loc):
    o.location = loc; o.keyframe_insert("location", frame=frame)


def blink(keys, f0, dur=5):
    """Quick natural blink starting at frame f0."""
    for side in ("left", "right"):
        expr(keys, f"eye-{side}-closure", 0.0, f0)
        expr(keys, f"eye-{side}-closure", 1.0, f0 + dur // 2)
        expr(keys, f"eye-{side}-closure", 0.0, f0 + dur)


def face(keys, frame, **w):
    """Key a set of expression units at once, e.g. face(keys, 12, squint=0.6, brows_up=0.3, smile=0.2).
    Aliases: squint, wide, brows_up, brows_down, brows_inner, smile, open, frown, purse, sneer."""
    alias = {"squint": ["eye-left-slit", "eye-right-slit"], "wide": ["eye-left-opened-up", "eye-right-opened-up"],
             "brows_up": ["eyebrows-left-up", "eyebrows-right-up"], "brows_down": ["eyebrows-left-down", "eyebrows-right-down"],
             "brows_inner": ["eyebrows-left-inner-up", "eyebrows-right-inner-up"], "smile": ["mouth-corner-puller"], "open": ["mouth-open"],
             "frown": ["mouth-depression"], "purse": ["mouth-pursing"], "sneer": ["nose-left-elevation", "nose-right-elevation"],
             "close": ["eye-left-closure", "eye-right-closure"], "browL_up": ["eyebrows-left-up"]}
    for k, v in w.items():
        for u in alias.get(k, [k]):
            expr(keys, u, v, frame)


def grip(h, side="R", amt=0.8, thumb=0.5, frame=None, axis=0, sign=1):
    """Curl the fingers into a holding grip (amt 0 = open, 1 = fist). Thumb curls less."""
    rig = h["rig"]
    for f in range(1, 6):
        for j in range(1, 4):
            pb = rig.pose.bones.get(f"finger{f}-{j}.{side}")
            if pb is None:
                continue
            a = (thumb if f == 1 else amt) * (35 if j == 1 else 55) * sign
            r = [0.0, 0.0, 0.0]; r[axis] = math.radians(a)
            pb.rotation_mode = "XYZ"; pb.rotation_euler = r
            if frame is not None:
                pb.keyframe_insert("rotation_euler", frame=frame)


def hold(h, obj, side="R", offset=(0, 0, 0)):
    """Put obj in the hand: at the point between thumb tip and index knuckle, parented to the wrist bone (follows IK)."""
    rig = h["rig"]; bpy.context.view_layer.update()
    pb = rig.pose.bones
    a = rig.matrix_world @ pb[f"finger1-3.{side}"].tail if f"finger1-3.{side}" in pb else rig.matrix_world @ pb[f"wrist.{side}"].tail
    b = rig.matrix_world @ pb[f"finger2-1.{side}"].head if f"finger2-1.{side}" in pb else a
    c = (a + b) / 2 + Vector(offset)
    obj.parent = None; obj.location = c
    bpy.context.view_layer.update()
    mw = obj.matrix_world.copy(); obj.parent = rig; obj.parent_type = "BONE"; obj.parent_bone = f"wrist.{side}"; obj.matrix_world = mw
    return c
