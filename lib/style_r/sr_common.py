"""Style R (realistic 3D) shared helpers: meshes, PBR materials, render setup, camera keys.

Used by cabin.py, sr_sky.py, sr_jet.py, sr_hand.py. Works both from the repo (lib/style_r/) and
from a flat Kaggle dataset folder (all files side by side).
Coordinates everywhere: metres, X = aircraft nose direction, +Y = left side, Z up.
"""
import math, os, sys
import bpy, bmesh
from mathutils import Vector, Matrix

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, os.path.dirname(_HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import camera as camlib  # lib/camera.py (pure numpy): same eased camera maths as Style T

_M = {}


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _M.clear()


def srgb(h, a=1.0):
    if not isinstance(h, str):
        return (*h[:3], a)
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return (*c, a)


# ------------------------------------------------------------------ objects / meshes

def link(o, parent=None):
    bpy.context.scene.collection.objects.link(o)
    if parent is not None:
        o.parent = parent
    return o


def empty(name, loc=(0, 0, 0), rot=(0, 0, 0), parent=None, matrix=None):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = 0.05
    link(e, parent)
    if matrix is not None:
        e.matrix_local = matrix
    else:
        e.location = loc
        e.rotation_euler = rot
    return e


def auto_sharp(o, deg=40.0):
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    lim = math.radians(deg)
    for e in bm.edges:
        if len(e.link_faces) == 2:
            e.smooth = e.calc_face_angle(0.0) < lim
    bm.to_mesh(me); bm.free()


def mesh_obj(name, verts, faces, mat=None, smooth=True, sharp=40.0, parent=None, fix_normals=False):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], faces)
    if fix_normals:
        bm = bmesh.new(); bm.from_mesh(me)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(me); bm.free()
    me.update()
    o = bpy.data.objects.new(name, me)
    link(o, parent)
    if mat is not None:
        me.materials.append(mat)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
        if sharp:
            auto_sharp(o, sharp)
    return o


def loft(name, rings, mat=None, close_u=True, close_v=False, cap_start=False, cap_end=False,
         smooth=True, sharp=40.0, parent=None, fix_normals=False):
    """rings: list of rings, each a list of nu points. Quads between consecutive rings."""
    nu = len(rings[0]); nv = len(rings)
    verts = [p for r in rings for p in r]
    faces = []
    for j in range(nv if close_v else nv - 1):
        j2 = (j + 1) % nv
        for i in range(nu if close_u else nu - 1):
            i2 = (i + 1) % nu
            faces.append((j * nu + i, j * nu + i2, j2 * nu + i2, j2 * nu + i))
    if cap_start:
        faces.append(tuple(range(nu - 1, -1, -1)))
    if cap_end:
        faces.append(tuple((nv - 1) * nu + i for i in range(nu)))
    return mesh_obj(name, verts, faces, mat, smooth, sharp, parent, fix_normals)


def rbox(name, size, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, bevel=0.008, seg=3, subsurf=0, parent=None):
    """Box with rounded edges (bevel + weighted normals); subsurf>0 gives a soft upholstered shape."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= size[0]; v.co.y *= size[1]; v.co.z *= size[2]
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    link(o, parent)
    o.location = loc; o.rotation_euler = rot
    if mat is not None:
        me.materials.append(mat)
    for p in me.polygons:
        p.use_smooth = True
    if bevel > 0:
        b = o.modifiers.new("bev", "BEVEL")
        b.width = min(bevel, 0.49 * min(size)); b.segments = seg; b.limit_method = "ANGLE"
    if subsurf:
        s = o.modifiers.new("sub", "SUBSURF"); s.levels = subsurf; s.render_levels = subsurf
    else:
        w = o.modifiers.new("wn", "WEIGHTED_NORMAL"); w.keep_sharp = False
    return o


def cyl(name, r, h, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, verts=32, bevel=0.0, r2=None, parent=None):
    """Cylinder/cone along local Z, centred."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=verts, radius1=r,
                          radius2=r if r2 is None else r2, depth=h)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    link(o, parent)
    o.location = loc; o.rotation_euler = rot
    if mat is not None:
        me.materials.append(mat)
    for p in me.polygons:
        p.use_smooth = True
    if bevel > 0:
        b = o.modifiers.new("bev", "BEVEL"); b.width = bevel; b.segments = 2; b.limit_method = "ANGLE"
        w = o.modifiers.new("wn", "WEIGHTED_NORMAL"); w.keep_sharp = False
    else:
        auto_sharp(o, 40)
    return o


def tube(name, pts, radius, mat=None, closed=False, n=10, parent=None, cap=True):
    """Round tube following a polyline (parallel-transport frames)."""
    P = [Vector(p) for p in pts]
    m = len(P)
    rings = []
    prev_n = None
    for i in range(m):
        if closed:
            t = (P[(i + 1) % m] - P[i - 1]).normalized()
        else:
            t = (P[min(i + 1, m - 1)] - P[max(i - 1, 0)]).normalized()
        if prev_n is None:
            a = Vector((0, 0, 1)) if abs(t.z) < 0.9 else Vector((1, 0, 0))
            nrm = (a - t * a.dot(t)).normalized()
        else:
            nrm = (prev_n - t * prev_n.dot(t)).normalized()
        prev_n = nrm
        b = t.cross(nrm)
        rings.append([tuple(P[i] + radius * (math.cos(2 * math.pi * k / n) * nrm + math.sin(2 * math.pi * k / n) * b))
                      for k in range(n)])
    return loft(name, rings, mat, close_u=True, close_v=closed, cap_start=cap and not closed,
                cap_end=cap and not closed, sharp=60, parent=parent)


def join(objs, name):
    """Apply modifiers and join into one object (keeps materials)."""
    dg = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    mats = []
    for o in objs:
        if o.type not in ("MESH", "CURVE", "FONT"):
            continue
        ev = o.evaluated_get(dg)
        me = bpy.data.meshes.new_from_object(ev)
        me.transform(o.matrix_world)
        if o.matrix_world.determinant() < 0:
            me.flip_normals()
        remap = []
        for m in (me.materials if len(me.materials) else [None]):
            if m not in mats:
                mats.append(m)
            remap.append(mats.index(m))
        for p in me.polygons:
            p.material_index = remap[min(p.material_index, len(remap) - 1)]
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
    out = bpy.data.meshes.new(name)
    bm.to_mesh(out); bm.free()
    for m in mats:
        out.materials.append(m)
    for o in list(objs):
        bpy.data.objects.remove(o, do_unlink=True)
    ob = bpy.data.objects.new(name, out)
    link(ob)
    return ob


# ------------------------------------------------------------------ materials

def _new(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    return m, nt, nt.nodes["Principled BSDF"]


def pbr(name, color, rough=0.5, metal=0.0, bump=None, bscale=300.0, bstr=0.3, cvar=0.0, cscale=4.0,
        coat=0.0, sheen=0.0, emit=None, estr=0.0, sss=0.0, sss_radius=(1.0, 0.35, 0.2), sss_scale=0.01,
        rvar=0.0, color2=None, stretch=None):
    """Principled material. bump: None | 'noise' | 'weave' | 'cells' | 'grille'."""
    key = (name, str(color), rough, metal, bump, bscale, bstr, cvar, coat, sheen, str(emit), estr, sss, rvar, str(color2))
    if key in _M:
        return _M[key]
    m, nt, b = _new(name)
    N = nt.nodes.new; L = nt.links.new
    base = srgb(color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = 0.08
    b.inputs["Sheen Weight"].default_value = sheen
    b.inputs["Sheen Roughness"].default_value = 0.5
    tc = N("ShaderNodeTexCoord")
    vec = tc.outputs["Object"]
    if stretch:
        mp = N("ShaderNodeMapping"); mp.inputs["Scale"].default_value = stretch
        L(vec, mp.inputs["Vector"]); vec = mp.outputs["Vector"]
    if cvar > 0 or color2 is not None:
        nz = N("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = cscale; nz.inputs["Detail"].default_value = 5.0
        L(vec, nz.inputs["Vector"])
        if color2 is not None:
            mx = N("ShaderNodeMix"); mx.data_type = "RGBA"
            mr = N("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = 0.35; mr.inputs["From Max"].default_value = 0.65
            L(nz.outputs["Fac"], mr.inputs["Value"]); L(mr.outputs["Result"], mx.inputs["Factor"])
            mx.inputs["A"].default_value = base; mx.inputs["B"].default_value = srgb(color2)
            L(mx.outputs["Result"], b.inputs["Base Color"])
        else:
            mr = N("ShaderNodeMapRange"); mr.inputs["To Min"].default_value = 1 - cvar; mr.inputs["To Max"].default_value = 1 + cvar * 0.4
            L(nz.outputs["Fac"], mr.inputs["Value"])
            mx = N("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "MULTIPLY"; mx.inputs["Factor"].default_value = 1.0
            mx.inputs["A"].default_value = base
            cc = N("ShaderNodeCombineColor")
            for s in ("Red", "Green", "Blue"):
                L(mr.outputs["Result"], cc.inputs[s])
            L(cc.outputs["Color"], mx.inputs["B"]); L(mx.outputs["Result"], b.inputs["Base Color"])
        if rvar > 0:
            mr2 = N("ShaderNodeMapRange"); mr2.inputs["To Min"].default_value = max(0.02, rough - rvar); mr2.inputs["To Max"].default_value = min(1, rough + rvar)
            L(nz.outputs["Fac"], mr2.inputs["Value"]); L(mr2.outputs["Result"], b.inputs["Roughness"])
    else:
        b.inputs["Base Color"].default_value = base
    h = None
    if bump == "noise":
        n2 = N("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = bscale; n2.inputs["Detail"].default_value = 4.0
        L(vec, n2.inputs["Vector"]); h = n2.outputs["Fac"]
    elif bump == "weave":
        w1 = N("ShaderNodeTexWave"); w1.wave_type = "BANDS"; w1.bands_direction = "X"; w1.inputs["Scale"].default_value = bscale
        w2 = N("ShaderNodeTexWave"); w2.wave_type = "BANDS"; w2.bands_direction = "Y"; w2.inputs["Scale"].default_value = bscale
        w3 = N("ShaderNodeTexWave"); w3.wave_type = "BANDS"; w3.bands_direction = "Z"; w3.inputs["Scale"].default_value = bscale
        for w in (w1, w2, w3):
            w.inputs["Distortion"].default_value = 0.6; L(vec, w.inputs["Vector"])
        mx1 = N("ShaderNodeMath"); mx1.operation = "MULTIPLY"; L(w1.outputs["Fac"], mx1.inputs[0]); L(w2.outputs["Fac"], mx1.inputs[1])
        mx2 = N("ShaderNodeMath"); mx2.operation = "ADD"; L(mx1.outputs[0], mx2.inputs[0]); L(w3.outputs["Fac"], mx2.inputs[1])
        h = mx2.outputs[0]
    elif bump == "cells":
        v = N("ShaderNodeTexVoronoi"); v.inputs["Scale"].default_value = bscale
        L(vec, v.inputs["Vector"]); h = v.outputs["Distance"]
    elif bump == "grille":
        w1 = N("ShaderNodeTexWave"); w1.wave_type = "BANDS"; w1.bands_direction = "X"; w1.inputs["Scale"].default_value = bscale
        L(vec, w1.inputs["Vector"]); h = w1.outputs["Fac"]
    if h is not None:
        bp = N("ShaderNodeBump"); bp.inputs["Strength"].default_value = bstr
        bp.inputs["Distance"].default_value = 0.6 / max(bscale, 1e-3)
        L(h, bp.inputs["Height"]); L(bp.outputs["Normal"], b.inputs["Normal"])
    if emit is not None:
        b.inputs["Emission Color"].default_value = srgb(emit)
        b.inputs["Emission Strength"].default_value = estr
    if sss > 0:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = sss_radius
        b.inputs["Subsurface Scale"].default_value = sss_scale
    _M[key] = m
    return m


def emission(name, color, strength):
    key = ("E", name, str(color), strength)
    if key in _M:
        return _M[key]
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission"); e.name = "Emission"
    e.inputs["Color"].default_value = srgb(color); e.inputs["Strength"].default_value = strength
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(e.outputs[0], o.inputs["Surface"])
    _M[key] = m
    return m


def glass(name="glass", tint=(0.92, 0.97, 1.0), refl=0.06, rough=0.02):
    """Thin window glass: lets light and camera rays straight through (no caustic noise) + a faint reflection."""
    key = ("G", name, refl)
    if key in _M:
        return _M[key]
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    N = nt.nodes.new; L = nt.links.new
    tr = N("ShaderNodeBsdfTransparent"); tr.inputs["Color"].default_value = (*tint, 1)
    gl = N("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = rough
    lw = N("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.25
    mr = N("ShaderNodeMapRange"); mr.inputs["To Min"].default_value = refl * 0.5; mr.inputs["To Max"].default_value = min(1.0, refl * 6)
    L(lw.outputs["Fresnel"], mr.inputs["Value"])
    mx = N("ShaderNodeMixShader"); L(mr.outputs["Result"], mx.inputs["Fac"]); L(tr.outputs[0], mx.inputs[1]); L(gl.outputs[0], mx.inputs[2])
    o = N("ShaderNodeOutputMaterial"); L(mx.outputs[0], o.inputs["Surface"])
    _M[key] = m
    return m


def ghost(name, color, glow=1.5, core=0.05, power=2.0):
    """X-ray skin: see-through, glowing at grazing angles."""
    key = ("X", name, str(color), glow, core)
    if key in _M:
        return _M[key]
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    N = nt.nodes.new; L = nt.links.new
    lw = N("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.35
    pw = N("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = power
    L(lw.outputs["Facing"], pw.inputs[0])
    tr = N("ShaderNodeBsdfTransparent")
    em = N("ShaderNodeEmission"); em.inputs["Color"].default_value = srgb(color); em.inputs["Strength"].default_value = glow
    mr = N("ShaderNodeMapRange"); mr.inputs["To Min"].default_value = core; mr.inputs["To Max"].default_value = 0.85
    L(pw.outputs[0], mr.inputs["Value"])
    mx = N("ShaderNodeMixShader"); L(mr.outputs["Result"], mx.inputs["Fac"]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2])
    o = N("ShaderNodeOutputMaterial"); L(mx.outputs[0], o.inputs["Surface"])
    _M[key] = m
    return m


# ------------------------------------------------------------------ lights

def area(name, loc, rot, size, color, energy, parent=None, size_y=None):
    d = bpy.data.lights.new(name, "AREA")
    d.energy = energy; d.color = srgb(color)[:3]
    d.shape = "RECTANGLE"; d.size = size; d.size_y = size_y or size
    o = bpy.data.objects.new(name, d); link(o, parent)
    o.location = loc; o.rotation_euler = rot
    return o


# ------------------------------------------------------------------ render / camera

def setup_render(W, H, samples, gpu=False, mblur=True, thr=0.02, exposure=0.0, look="AgX - Medium High Contrast"):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    c = sc.cycles
    c.samples = samples
    c.use_adaptive_sampling = True; c.adaptive_threshold = thr
    c.use_denoising = True; c.denoiser = "OPENIMAGEDENOISE"
    try:
        c.denoising_input_passes = "RGB_ALBEDO_NORMAL"
    except Exception:
        pass
    c.max_bounces = 8; c.diffuse_bounces = 4; c.glossy_bounces = 4; c.transmission_bounces = 6
    c.transparent_max_bounces = 16; c.volume_bounces = 0
    c.caustics_reflective = False; c.caustics_refractive = False
    c.sample_clamp_indirect = 8.0
    c.blur_glossy = 1.0
    sc.render.resolution_x = W; sc.render.resolution_y = H; sc.render.resolution_percentage = 100
    sc.render.use_persistent_data = True
    sc.render.use_motion_blur = bool(mblur)
    sc.render.motion_blur_shutter = 0.5
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.view_settings.view_transform = "AgX"
    try:
        sc.view_settings.look = look
    except Exception:
        pass
    sc.view_settings.exposure = exposure
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
        c.device = "GPU"
        try:
            c.denoising_use_gpu = True
        except Exception:
            pass


def make_camera():
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    link(cam)
    cam.data.sensor_fit = "HORIZONTAL"; cam.data.sensor_width = 36.0
    cam.data.clip_start = 0.03; cam.data.clip_end = 400000.0
    cam.rotation_mode = "QUATERNION"
    bpy.context.scene.camera = cam
    return cam


def clear_anim(o):
    if o.animation_data:
        o.animation_data_clear()
    if getattr(o, "data", None) is not None and getattr(o.data, "animation_data", None):
        o.data.animation_data_clear()


def key_camera(cam, c, nfr):
    """Bake the eased move of lib/camera.py into per-frame keys (so motion blur sees it).
    Extra keys in c: focus [x,y,z] (default tgt), fstop, shake (metres), dof false to switch off."""
    clear_anim(cam)
    prev = None
    use_dof = c.get("dof", True) is not False
    cam.data.dof.use_dof = use_dof
    cam.data.dof.aperture_fstop = c.get("fstop", 2.8)
    for f in range(nfr + 1):
        t = f / max(1, nfr - 1)
        pos, tgt, lens = camlib.cam_at(c, min(t, 1.0))
        if c.get("shake"):
            a = c["shake"]
            pos = [pos[0] + a * math.sin(f * 0.9), pos[1] + a * 0.6 * math.sin(f * 1.7 + 1), pos[2] + a * math.cos(f * 1.3)]
        d = Vector(tgt) - Vector(pos)
        q = d.to_track_quat("-Z", "Y")
        if prev is not None and q.dot(prev) < 0:
            q.negate()
        prev = q.copy()
        cam.location = pos; cam.rotation_quaternion = q; cam.data.lens = lens
        cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_quaternion", frame=f)
        cam.data.keyframe_insert("lens", frame=f)
        if use_dof:
            fo = c.get("focus") or tgt
            cam.data.dof.focus_distance = max(0.05, (Vector(fo) - Vector(pos)).length)
            cam.data.dof.keyframe_insert("focus_distance", frame=f)


def set_interp(o, kind="LINEAR"):
    """Set interpolation of all keys of an object (works with Blender 4.4+ slotted actions too)."""
    ad = o.animation_data
    if not ad or not ad.action:
        return
    act = ad.action
    fcs = []
    try:
        fcs = list(act.fcurves)
    except Exception:
        pass
    if not fcs:
        try:
            for lay in act.layers:
                for st in lay.strips:
                    for cb in st.channelbags:
                        fcs += list(cb.fcurves)
        except Exception:
            pass
    for fc in fcs:
        for k in fc.keyframe_points:
            k.interpolation = kind
