"""Cruise-altitude sky for Style R: physical sky, sun, a cloud deck far below and near cloud puffs.

build_sky() -> dict(deck, sun, world, bg).  animate_deck() slides the whole cloud layer backwards at
aircraft speed (object motion, so Cycles motion blur streaks it). All procedural, no external files.
"""
import math, random
import bpy
from mathutils import Vector, noise
import sr_common as C


def _cloud_mat(name, soft_edge=False):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    N = nt.nodes.new; L = nt.links.new
    tc = N("ShaderNodeTexCoord")
    nz = N("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 0.02 if not soft_edge else 0.08
    nz.inputs["Detail"].default_value = 6.0; nz.inputs["Roughness"].default_value = 0.6
    L(tc.outputs["Object"], nz.inputs["Vector"])
    bp = N("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.55; bp.inputs["Distance"].default_value = 18.0 if not soft_edge else 5.0
    L(nz.outputs["Fac"], bp.inputs["Height"])
    df = N("ShaderNodeBsdfDiffuse"); df.inputs["Color"].default_value = (0.93, 0.94, 0.96, 1)
    L(bp.outputs["Normal"], df.inputs["Normal"])
    tl = N("ShaderNodeBsdfTranslucent"); tl.inputs["Color"].default_value = (0.95, 0.95, 0.97, 1)
    m1 = N("ShaderNodeMixShader"); m1.inputs["Fac"].default_value = 0.3
    L(df.outputs[0], m1.inputs[1]); L(tl.outputs[0], m1.inputs[2])
    em = N("ShaderNodeEmission"); em.inputs["Color"].default_value = (0.62, 0.74, 0.95, 1); em.inputs["Strength"].default_value = 0.16
    ad = N("ShaderNodeAddShader"); L(m1.outputs[0], ad.inputs[0]); L(em.outputs[0], ad.inputs[1])
    # distance haze towards the horizon colour
    cd = N("ShaderNodeCameraData")
    dv = N("ShaderNodeMath"); dv.operation = "DIVIDE"; dv.inputs[1].default_value = -30000.0
    L(cd.outputs["View Distance"], dv.inputs[0])
    ex = N("ShaderNodeMath"); ex.operation = "EXPONENT"; L(dv.outputs[0], ex.inputs[0])
    lp = N("ShaderNodeLightPath")
    cam_only = N("ShaderNodeMath"); cam_only.operation = "MULTIPLY"
    inv = N("ShaderNodeMath"); inv.operation = "SUBTRACT"; inv.inputs[0].default_value = 1.0; L(ex.outputs[0], inv.inputs[1])
    L(inv.outputs[0], cam_only.inputs[0]); L(lp.outputs["Is Camera Ray"], cam_only.inputs[1])
    hz = N("ShaderNodeEmission"); hz.name = "Haze"; hz.inputs["Color"].default_value = (0.66, 0.80, 1.0, 1); hz.inputs["Strength"].default_value = 1.0
    m2 = N("ShaderNodeMixShader"); L(cam_only.outputs[0], m2.inputs["Fac"]); L(ad.outputs[0], m2.inputs[1]); L(hz.outputs[0], m2.inputs[2])
    out = N("ShaderNodeOutputMaterial")
    if soft_edge:
        lw = N("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.5
        mr = N("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = 0.35; mr.inputs["From Max"].default_value = 0.95
        mr.inputs["To Min"].default_value = 0.0; mr.inputs["To Max"].default_value = 1.0
        L(lw.outputs["Facing"], mr.inputs["Value"])
        n3 = N("ShaderNodeTexNoise"); n3.inputs["Scale"].default_value = 0.05; n3.inputs["Detail"].default_value = 5.0
        L(tc.outputs["Object"], n3.inputs["Vector"])
        mm = N("ShaderNodeMath"); mm.operation = "MULTIPLY_ADD"; mm.inputs[1].default_value = 0.9; mm.inputs[2].default_value = -0.3; mm.use_clamp = True
        L(n3.outputs["Fac"], mm.inputs[0])
        mxx = N("ShaderNodeMath"); mxx.operation = "MAXIMUM"; mxx.use_clamp = True
        L(mr.outputs["Result"], mxx.inputs[0]); L(mm.outputs[0], mxx.inputs[1])
        tr = N("ShaderNodeBsdfTransparent")
        m3 = N("ShaderNodeMixShader"); L(mr.outputs["Result"], m3.inputs["Fac"]); L(m2.outputs[0], m3.inputs[1]); L(tr.outputs[0], m3.inputs[2])
        L(m3.outputs[0], out.inputs["Surface"])
    else:
        L(m2.outputs[0], out.inputs["Surface"])
    return m


def _h(x, y, cell, seed):
    """Cloud-top height field: big coverage patches + billowy (abs-noise) lumps."""
    def n(s, o):
        return noise.noise(Vector((x / s + o, y / s - o * 0.7, seed)))

    def w(s):
        return min(1.0, max(0.0, (s / max(cell, 1e-3) - 2.0) / 3.0))
    big = n(2600.0, 3.1) + 0.35 * n(900.0, 7.7)
    m = min(1.0, max(0.0, (big + 0.42) / 0.5)); m = m * m * (3 - 2 * m)
    b = 150.0 * abs(n(520.0, 11.0)) * w(520) + 70.0 * abs(n(190.0, 23.0)) * w(190) + 26.0 * abs(n(64.0, 31.0)) * w(64) + 9.0 * abs(n(22.0, 5.0)) * w(22)
    return m * (40.0 + b) - (1 - m) * 60.0


def build_deck(deck_z=-320.0, seed=3.0, r0=14.0, g=1.021, rmax=170000.0):
    nth = int(round(2 * math.pi / (g - 1)))
    radii = []
    r = r0
    while r < rmax:
        radii.append(r); r *= g
    verts = [(0.0, 0.0, _h(0, 0, r0, seed))]
    for r in radii:
        cell = r * (g - 1)
        for k in range(nth):
            a = 2 * math.pi * k / nth
            x, y = r * math.cos(a), r * math.sin(a)
            fade = min(1.0, max(0.0, (120000.0 - r) / 60000.0))
            verts.append((x, y, _h(x, y, cell, seed) * fade))
    faces = [(0, 1 + k, 1 + (k + 1) % nth) for k in range(nth)]
    for j in range(len(radii) - 1):
        a0 = 1 + j * nth; a1 = a0 + nth
        for k in range(nth):
            k2 = (k + 1) % nth
            faces.append((a0 + k, a1 + k, a1 + k2, a0 + k2))
    deck = C.mesh_obj("cloud_deck", verts, faces, _cloud_mat("cloud"), smooth=True, sharp=None)
    deck.location = (0, 0, deck_z)
    return deck


def build_puff(name, size, seed, mat, parent):
    me = bpy.data.meshes.new(name)
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=4, radius=1.0)
    for v in bm.verts:
        p = v.co.copy()
        d = 1.0 + 0.55 * abs(noise.noise(p * 1.3 + Vector((seed, 0, 0)))) + 0.22 * abs(noise.noise(p * 3.7 + Vector((0, seed, 0)))) \
            + 0.08 * abs(noise.noise(p * 9.0 + Vector((0, 0, seed))))
        fl = 0.55 if p.z < 0 else 1.0  # flatter base
        v.co = Vector((p.x * d * size[0], p.y * d * size[1], p.z * d * size[2] * fl))
    bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me)
    C.link(o, parent)
    return o


def build_sky(sun_elev=27.0, sun_az=70.0, sun_strength=5.0, sky_strength=0.3, deck_z=-320.0, puffs=(), seed=3.0, altitude=10700.0):
    """sun_az: where the sun stands, degrees from +X towards +Y. puffs: list of (x, y, z, sx, sy, sz) in deck space."""
    sc = bpy.context.scene
    w = bpy.data.worlds.new("sky"); sc.world = w; w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    try:
        sky = nt.nodes.new("ShaderNodeTexSky")
        for t in ("MULTIPLE_SCATTERING", "NISHITA", "SINGLE_SCATTERING"):
            try:
                sky.sky_type = t; break
            except Exception:
                continue
        sky.sun_disc = False
        sky.sun_elevation = math.radians(sun_elev)
        sky.sun_rotation = math.radians(90.0 - sun_az)
        sky.altitude = altitude
        nt.links.new(sky.outputs[0], bg.inputs["Color"])
    except Exception:
        bg.inputs["Color"].default_value = (0.25, 0.45, 0.9, 1)
    bg.inputs["Strength"].default_value = sky_strength
    el, az = math.radians(sun_elev), math.radians(sun_az)
    to_sun = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)))
    sd = bpy.data.lights.new("sun", "SUN"); sd.energy = sun_strength; sd.angle = math.radians(1.2)
    sd.color = (1.0, 0.955, 0.89)
    sun = bpy.data.objects.new("sun", sd); C.link(sun)
    sun.rotation_euler = (-to_sun).to_track_quat("-Z", "Y").to_euler()
    deck = build_deck(deck_z, seed)
    hz = deck.data.materials[0].node_tree.nodes["Haze"]
    hz.inputs["Strength"].default_value = sky_strength * 4.6
    pm = _cloud_mat("puff", soft_edge=True)
    pm.node_tree.nodes["Haze"].inputs["Strength"].default_value = sky_strength * 4.6
    for i, p in enumerate(puffs):
        o = build_puff(f"puff{i}", p[3:6], seed + i * 1.37, pm, deck)
        o.location = (p[0], p[1], p[2] - deck_z)
        o.rotation_euler = (0, 0, i * 1.1)
    return {"deck": deck, "sun": sun, "world": w, "bg": bg}


def animate_deck(deck, nfr, fps=30, speed=235.0, x0=0.0):
    """Cloud layer slides towards -X (aircraft flies +X). Linear keys."""
    C.clear_anim(deck)
    z = deck.location.z; y = deck.location.y
    deck.location = (x0, y, z); deck.keyframe_insert("location", frame=0)
    deck.location = (x0 - speed * (nfr + 1) / fps, y, z); deck.keyframe_insert("location", frame=nfr + 1)
    C.set_interp(deck, "LINEAR")
    deck.location = (x0, y, z)
