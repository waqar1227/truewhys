"""Toon sets for standalone Shorts batch 1 (A-001..A-007). Registered into sets.BUILDERS on import.
More sets of this batch (cutaway_head, comet) live in lib/sets4.py and reuse the helpers below.
All sets: metres, Z up, camera looks towards +y, vertical 9:16 marks (sensor fit horizontal 36 mm).
Sky objects stay within ~95 m of the camera (camera clip_end is 100 m).

marsh  (tide | flood | dusk)   A-001 quicksand. Tidal beach at golden hour.
    Sand is flat z=0 for y<3, then slopes gently to the sea. Sea level: tide = shoreline y~8.5,
    flood = shoreline y~4.5 (the tide has raced in behind Wy), dusk = tide with a later, pinker sky.
    Quicksand patch (dark, glossy, ripple rings, bubbles): centre (0,2,0), radius ~1.7 (puppet cut at z=0.02).
    Warning sign (1.9,0.4) · beached boat (-3.9,5.6) · rope posts x=-2.6..2.9 at y~-0.3
    cliffs + lighthouse: left, lighthouse at (-17,46) top z~17 · huts on stilts (6.8,7.5) (9.6,10.5)
    pier x=4.6, y 9..24, deck z=1.1 · dunes x>8 · sun low over the sea at right (az ~ +25 deg)
    Camera marks:
      hero     pos (0.5,-3.6,1.75) tgt (0,2.6,0.75) lens 24   Wy waist-deep at (0,2), sea + lighthouse behind
      wide     pos (2.2,-7.5,3.6)  tgt (-0.3,5,0.6)  lens 22   establishing, whole beach
      low      pos (-2.6,-1.2,0.7) tgt (0.6,4.5,0.9) lens 26   low angle, tide line behind Wy
      top      pos (0,0.6,5.2)     tgt (0,2.05,0)    lens 26   looking down on the patch (float to the edge)

arctic (night)   A-002 polar bear liver. 1590s Dutch sailors' ice camp under the aurora.
    Campfire (0.6,1.2) with cooking pot on a tripod · tent (-3.1,3.4) opening faces the fire
    sledge with crates and barrel (3.3,3.0) · stacked crates/barrels (-1.2,4.6) · oars rack (1.9,5.0)
    ship frozen in the ice: hull centre (4.5,17), bow towards -x, main mast top z~13 · pressure ridge y 8..11
    aurora ribbons y~75..88, z 16..52 · moon (-20,85,40)
    Camera marks:
      hero     pos (1.2,-4.2,1.5)  tgt (0.9,3.5,2.3)  lens 22   fire low centre, ship + aurora above
      fire     pos (-0.9,-2.2,1.25) tgt (0.7,1.6,1.0) lens 28   close on the fire and the sailor (0.6..1.6,1.2)
      wide     pos (-3.5,-8,3.2)   tgt (1.5,6,2.6)    lens 22   camp + ship, establishing
      ship     pos (-2,3,1.8)      tgt (4.2,17,5.5)   lens 30   the trapped ship

castle (night | day | cutaway)   A-006 garderobes. Attackers' bank is z=0 for y<-1.5; moat y -1.5..3 (water z=-0.7).
    Curtain wall front face y=3.2, wall-walk z=10, merlons to 11.2, flanking round towers x=+-10.
    Garderobe turret corbelled out at x=0: y 1.7..3.2, z 6.5..8.7 (seat z~7.0), lit slit window.
    Chute: light stone shaft x -0.6..0.6, y 2.35..3.2, z 0.0..6.5, dark arched outlet at its foot (z -0.6..0.6);
    raft with ladder under the outlet (0.0,1.4). "cutaway" opens the turret and the shaft (seat, hole,
    hollow shaft with bars, hanging clothes) in neutral daylight for the zoom-in beat.
    Camera marks:
      hero     pos (1.4,-9.5,1.7)  tgt (0,3,5.2)     lens 22   looking up the chute to the turret, moon right
      chute    pos (-2.6,-4.5,1.2) tgt (0,2.6,3.4)   lens 28   soldiers climbing (x 0, y 2.2, z 0..6)
      turret   pos (2.2,-3.5,6.2)  tgt (0,2.4,7.4)   lens 35   close on the garderobe (use with cutaway too)
      wide     pos (-5,-16,3.5)    tgt (0,4,6)       lens 24   whole castle, siege camp in front

lab    (day)   A-004 tickling. Bright cartoon neuroscience lab, room x -6..6, back wall y=5.5.
    Bench y 1.2..2.2, top z=0.95. Robot arm base (1.2,1.7), feather tip at about (2.05,1.55,1.55).
    Brain model under glass (-0.9,1.8,1.35) · big brain screen on the back wall (0,5.4,2.7)
    posters (-3.6 and 3.9, 5.4) · shelves left wall · window right wall · plants (-5.2,4.6) (5.2,0.8)
    Camera marks:
      hero     pos (0.4,-3.6,1.55) tgt (0.6,2,1.45)   lens 24   bench, robot arm right of centre, screen above
      robot    pos (0.2,-0.9,1.5)  tgt (1.6,1.7,1.45) lens 30   close on the robot arm and feather
      screen   pos (0,-1.5,2.0)    tgt (0,5.4,2.7)    lens 32   the brain screen (cerebellum highlighted)
      wide     pos (-3.2,-5.2,2.3) tgt (0.8,2.5,1.4)  lens 22   whole lab with depth
"""
import math, random
import bpy
import sets
from sets import (mat, box, cyl, sphere, plane, prism_roof, world, sun, area, point, tree, barrel, crate, torch_sconce, hexrgb)
from sets2 import flames

# ---------------------------------------------------------------- geometry helpers

def _link(o):
    bpy.context.collection.objects.link(o)
    return o


def mesh(name, verts, faces, m=None, smooth=False):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    o = _link(bpy.data.objects.new(name, me))
    if m is not None:
        me.materials.append(m)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    return o


def chaikin(pts, n=2, closed=True):
    """Corner-cutting smoothing of a 2D/3D point list."""
    for _ in range(n):
        out, L = [], len(pts)
        for i in range(L if closed else L - 1):
            p, q = pts[i], pts[(i + 1) % L]
            out.append(tuple(0.75 * a + 0.25 * b for a, b in zip(p, q)))
            out.append(tuple(0.25 * a + 0.75 * b for a, b in zip(p, q)))
        if not closed:
            out = [tuple(pts[0])] + out + [tuple(pts[-1])]
        pts = out
    return pts


def poly(pts, y, thick, m, bevel=0.0, axis="xz", smooth_n=0):
    """Extruded flat shape. axis "xz": outline in the XZ plane at depth y, extruded to y+thick (a relief layer).
    axis "xy": outline on the ground at height y, extruded up by thick."""
    if smooth_n:
        pts = chaikin(pts, smooth_n)
    n = len(pts)
    P = (lambda a, b, d: (a, d, b)) if axis == "xz" else (lambda a, b, d: (a, b, d))
    verts = [P(a, b, y) for a, b in pts]
    faces = [tuple(range(n))]
    if thick:
        verts += [P(a, b, y + thick) for a, b in pts]
        faces.append(tuple(range(2 * n - 1, n - 1, -1)))
        faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    o = mesh("poly", verts, faces, m)
    if bevel and thick:
        b = o.modifiers.new("bev", "BEVEL"); b.width = bevel; b.segments = 2; b.limit_method = "ANGLE"; b.angle_limit = math.radians(50)
    return o


def terrain(fn, x0, x1, y0, y1, nx, ny, m):
    verts = []
    for j in range(ny + 1):
        y = y0 + (y1 - y0) * j / ny
        for i in range(nx + 1):
            x = x0 + (x1 - x0) * i / nx
            verts.append((x, y, fn(x, y)))
    faces = [(j * (nx + 1) + i, j * (nx + 1) + i + 1, (j + 1) * (nx + 1) + i + 1, (j + 1) * (nx + 1) + i) for j in range(ny) for i in range(nx)]
    return mesh("terrain", verts, faces, m, smooth=True)


def tube(pts, r, m, closed=False, res=2, smooth=True, radii=None):
    """Round tube along a 3D path (curve object: light and smooth). radii = per-point radius factors."""
    cu = bpy.data.curves.new("tube", "CURVE")
    cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = res; cu.use_fill_caps = True; cu.resolution_u = 6
    nurbs = smooth and len(pts) > 2
    sp = cu.splines.new("NURBS" if nurbs else "POLY")
    sp.points.add(len(pts) - 1)
    for i, (p, q) in enumerate(zip(sp.points, pts)):
        p.co = (q[0], q[1], q[2], 1.0)
        if radii:
            p.radius = radii[i]
    if nurbs:
        sp.order_u = min(4, len(pts)); sp.use_endpoint_u = not closed
    sp.use_cyclic_u = closed
    o = _link(bpy.data.objects.new("tube", cu))
    cu.materials.append(m)
    return o


def loft(rings, m, caps=True, smooth=True):
    """Skin a list of closed rings (same point count)."""
    n = len(rings[0]); verts = [p for r in rings for p in r]; faces = []
    for k in range(len(rings) - 1):
        for i in range(n):
            a, b = k * n + i, k * n + (i + 1) % n
            faces.append((a, b, b + n, a + n))
    if caps:
        faces.append(tuple(range(n - 1, -1, -1)))
        faces.append(tuple(range((len(rings) - 1) * n, len(rings) * n)))
    return mesh("loft", verts, faces, m, smooth=smooth)


class Group:
    """with Group(loc, rot_deg, scale): build things around the origin; they are then placed together."""

    def __init__(self, loc=(0, 0, 0), rot=(0, 0, 0), scale=1.0):
        self.loc, self.rot, self.scale = loc, rot, scale

    def __enter__(self):
        self.before = set(bpy.data.objects)
        return self

    def __exit__(self, *a):
        root = _link(bpy.data.objects.new("grp", None))
        for o in bpy.data.objects:
            if o not in self.before and o.parent is None and o is not root:
                o.parent = root
        root.location = self.loc
        root.rotation_euler = [math.radians(v) for v in self.rot]
        root.scale = (self.scale,) * 3 if not isinstance(self.scale, (tuple, list)) else self.scale
        self.root = root


def ring(loc, r, w, m, flat=0.25):
    bpy.ops.mesh.primitive_torus_add(location=loc, major_radius=r, minor_radius=w, major_segments=48, minor_segments=6)
    o = bpy.context.active_object
    o.scale = (1, 1, flat)
    o.data.materials.append(m)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def disc(loc, r, m, scale=(1, 1, 1), rot=(0, 0, 0), depth=0.02):
    bpy.ops.mesh.primitive_cylinder_add(location=loc, radius=r, depth=depth, vertices=40, rotation=rot)
    o = bpy.context.active_object
    o.scale = scale
    o.data.materials.append(m)
    return o


def rock(loc, s, m, rz=0.0, squash=0.6):
    o = sphere(loc, s, m, scale=(1.3, 1.0, squash), sub=2)
    o.rotation_euler = (0.1 * math.sin(rz * 7), 0.1 * math.cos(rz * 5), rz)
    for p in o.data.polygons:
        p.use_smooth = False
    return o


def rope(p0, p1, sag, m, r=0.025, n=8):
    pts = [(p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t, p0[2] + (p1[2] - p0[2]) * t - sag * 4 * t * (1 - t)) for t in [i / n for i in range(n + 1)]]
    return tube(pts, r, m)


# ---------------------------------------------------------------- material helpers

def nmat(key, fn):
    """Cached custom node material: fn(nt, bsdf, N, L) builds the tree."""
    k = ("n", key)
    if k in sets._MATS:
        return sets._MATS[k]
    m = bpy.data.materials.new(key)
    m.use_nodes = True
    nt = m.node_tree
    fn(nt, nt.nodes["Principled BSDF"], nt.nodes.new, nt.links.new)
    sets._MATS[k] = m
    return m


def _math(nt, op, a, b=None, clamp=False):
    n = nt.nodes.new("ShaderNodeMath"); n.operation = op; n.use_clamp = clamp
    for i, v in enumerate((a, b)):
        if v is None:
            continue
        if isinstance(v, (int, float)):
            n.inputs[i].default_value = v
        else:
            nt.links.new(v, n.inputs[i])
    return n.outputs[0]


def _mixc(nt, fac, a, b):
    n = nt.nodes.new("ShaderNodeMix"); n.data_type = "RGBA"
    for sock, v in ((n.inputs[0], fac), (n.inputs[6], a), (n.inputs[7], b)):
        if isinstance(v, (int, float)):
            sock.default_value = v
        elif isinstance(v, str):
            sock.default_value = hexrgb(v)
        else:
            nt.links.new(v, sock)
    return n.outputs[2]


def _ramp(nt, fac, stops):
    n = nt.nodes.new("ShaderNodeValToRGB"); cr = n.color_ramp
    while len(cr.elements) < len(stops):
        cr.elements.new(0.5)
    for e, (p, c) in zip(cr.elements, stops):
        e.position = p; e.color = hexrgb(c) if isinstance(c, str) else (c, c, c, 1)
    nt.links.new(fac, n.inputs[0])
    return n.outputs[0]


def _pos(nt):
    geo = nt.nodes.new("ShaderNodeNewGeometry"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Position"], sp.inputs[0])
    return geo.outputs["Position"], sp.outputs


def _noise(nt, vec, scale, detail=2.0, rough=0.5):
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = detail
    n.inputs["Roughness"].default_value = rough
    if vec is not None:
        nt.links.new(vec, n.inputs["Vector"])
    return n.outputs[0]


def _bump(nt, bsdf, height, strength=0.3, dist=0.05):
    b = nt.nodes.new("ShaderNodeBump"); b.inputs["Strength"].default_value = strength; b.inputs["Distance"].default_value = dist
    nt.links.new(height, b.inputs["Height"]); nt.links.new(b.outputs[0], bsdf.inputs["Normal"])


def sky3(stops, strength=1.0):
    """World gradient by elevation. stops = [(pos, colour)...], pos 0 = horizon (and below), 1 = zenith."""
    w = bpy.data.worlds.new("w"); bpy.context.scene.world = w; w.use_nodes = True
    nt = w.node_tree; bg = nt.nodes["Background"]
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    nt.links.new(_ramp(nt, sp.outputs["Z"], stops), bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength


def glow_mat(key, color, strength, power=2.0, color2=None):
    """Soft radial glow card (transparent edge). Use on a plane/disc: falloff from the object's centre."""
    def f(nt, bsdf, N, L):
        tc = N("ShaderNodeTexCoord"); vm = N("ShaderNodeVectorMath"); vm.operation = "LENGTH"
        mp = N("ShaderNodeMapping"); mp.inputs["Location"].default_value = (-0.5, -0.5, -0.5)
        L(tc.outputs["Generated"], mp.inputs[0]); L(mp.outputs[0], vm.inputs[0])
        d = _math(nt, "MULTIPLY", vm.outputs["Value"], 2.0)
        a = _math(nt, "POWER", _math(nt, "SUBTRACT", 1.0, d, clamp=True), power)
        em = N("ShaderNodeEmission"); em.inputs[1].default_value = strength
        if color2:
            L(_mixc(nt, a, color2, color), em.inputs[0])
        else:
            em.inputs[0].default_value = hexrgb(color)
        tr = N("ShaderNodeBsdfTransparent"); mx = N("ShaderNodeMixShader")
        L(a, mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2])
        L(mx.outputs[0], nt.nodes["Material Output"].inputs[0])
    return nmat(key, f)


def glow(loc, r, color, strength, power=2.0, color2=None, facing="y"):
    """Glow card. facing "y": stands up facing the camera side (-y); "z": lies flat on the ground."""
    m = glow_mat(f"glow{color}{strength}{power}{color2}", color, strength, power, color2)
    rot = (math.radians(90), 0, 0) if facing == "y" else (0, 0, 0)
    bpy.ops.mesh.primitive_plane_add(size=2 * r, location=loc, rotation=rot)
    o = bpy.context.active_object; o.data.materials.append(m)
    o.visible_shadow = False
    return o


def water_mat(key, color, alpha=0.55, rough=0.06, wave=0.0, wave_scale=1.2, emit=0.0):
    """Toon water: glossy tinted surface, partly see-through, optional noise ripples."""
    def f(nt, bsdf, N, L):
        bsdf.inputs["Base Color"].default_value = hexrgb(color); bsdf.inputs["Roughness"].default_value = rough
        if emit:
            bsdf.inputs["Emission Color"].default_value = hexrgb(color); bsdf.inputs["Emission Strength"].default_value = emit
        if wave:
            pos, _ = _pos(nt)
            mp = N("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (0.35, 1.0, 1.0); L(pos, mp.inputs[0])
            _bump(nt, bsdf, _noise(nt, mp.outputs[0], wave_scale, 2.0), wave, 0.1)
        if alpha < 1:
            tr = N("ShaderNodeBsdfTransparent"); mx = N("ShaderNodeMixShader"); mx.inputs[0].default_value = alpha
            L(tr.outputs[0], mx.inputs[1]); L(bsdf.outputs[0], mx.inputs[2])
            L(mx.outputs[0], nt.nodes["Material Output"].inputs[0])
    return nmat(key, f)


def stars(R, n, y, x_range, z_range, strength=8):
    sm = mat("star", "#FFFFFF", emit="#FFFFFF", emit_strength=strength, noise=0)
    sb = mat("starb", "#CFE0FF", emit="#BFD4FF", emit_strength=strength, noise=0)
    for k in range(n):
        o = sphere((R.uniform(*x_range), y + R.uniform(-3, 3), R.uniform(*z_range)), R.choice((0.09, 0.11, 0.14, 0.2)), sm if k % 3 else sb, sub=1)
        o.visible_shadow = False


def moon(loc, r, strength=5.0, halo=5.0):
    sphere(loc, r, mat("moon", "#FFF6E2", emit="#FFF2D8", emit_strength=strength, noise=0))
    for dx, dz, s in ((-0.35, 0.3, 0.22), (0.3, -0.2, 0.3), (0.05, 0.45, 0.14)):
        disc((loc[0] + dx * r, loc[1] - r * 0.93, loc[2] + dz * r), s * r, mat("mooncr", "#E4D8BE", emit="#E0D2B4", emit_strength=strength * 0.75, noise=0), rot=(math.radians(90), 0, 0))
    glow((loc[0], loc[1] + r, loc[2]), r * halo, "#BFD0FF", 1.2, 2.6)


def cloud(loc, s, m, n=4, flat=0.45):
    for k in range(n):
        o = sphere((loc[0] + (k - (n - 1) / 2) * s * 0.75, loc[1] + (k % 2) * 0.6, loc[2] + (0.25 if k % 2 else 0) * s), s * (0.7 + 0.25 * ((k * 7) % 3) / 2), m, scale=(1.5, 0.5, flat), sub=2)
        o.visible_shadow = False


def grass_tuft(x, y, z, R, m, h=0.6, n=5):
    for k in range(n):
        a = R.uniform(0, math.tau); t = R.uniform(0.15, 0.5)
        hh = h * R.uniform(0.7, 1.2)
        cyl((x + math.cos(a) * 0.06 + math.sin(t) * math.cos(a) * hh / 2, y + math.sin(a) * 0.06 + math.sin(t) * math.sin(a) * hh / 2, z + hh / 2 * math.cos(t)),
            0.035, hh, m, verts=4, bevel=0, r2=0.004, rot=(0, t, a))


def bird(loc, s, m):
    """Far gull silhouette: a shallow M."""
    x, y, z = loc
    tube([(x - s, y, z), (x - s * 0.45, y, z + s * 0.32), (x, y, z), (x + s * 0.45, y, z + s * 0.32), (x + s, y, z)], s * 0.05, m, smooth=False)


def gull(loc, rz=0.0):
    """Little toon gull standing on something."""
    w = mat("gullw", "#FFFFFF", rough=0.8, noise=0); g = mat("gullg", "#9AA6B4", rough=0.8, noise=0); o_ = mat("gullo", "#FFB238", rough=0.6, noise=0)
    with Group(loc, (0, 0, math.degrees(rz))):
        sphere((0, 0, 0.16), 0.11, w, scale=(1.5, 1, 0.95), sub=2)
        sphere((0.02, 0, 0.19), 0.1, g, scale=(1.45, 1.06, 0.6), sub=2)
        sphere((0.14, 0, 0.3), 0.065, w, sub=2)
        cyl((0.23, 0, 0.29), 0.022, 0.09, o_, verts=6, r2=0.004, rot=(0, math.radians(90), 0), bevel=0)
        sphere((0.17, -0.05, 0.32), 0.012, mat("eyek", "#1E1A18", noise=0), sub=1)
        for s in (-0.03, 0.03):
            cyl((0, s, 0.04), 0.008, 0.1, o_, verts=4, bevel=0)


# ---------------------------------------------------------------- marsh (A-001 quicksand)

def _sand_mat(dusk):
    def f(nt, bsdf, N, L):
        pos, s = _pos(nt)
        n1 = _noise(nt, pos, 0.45, 3.0)
        n2 = _noise(nt, pos, 6.0, 2.0)
        # wetness: lower ground and ground nearer the sea is wetter, broken up by noise
        w = _math(nt, "ADD", _math(nt, "MULTIPLY", s["Z"], -22.0), _math(nt, "MULTIPLY", _math(nt, "SUBTRACT", s["Y"], 0.5), 0.09))
        w = _math(nt, "ADD", w, _math(nt, "MULTIPLY", _math(nt, "SUBTRACT", n1, 0.5), 1.5))
        mr = N("ShaderNodeMapRange"); mr.interpolation_type = "SMOOTHSTEP"
        mr.inputs["From Min"].default_value = -0.15; mr.inputs["From Max"].default_value = 0.85
        L(w, mr.inputs["Value"]); wet = mr.outputs["Result"]
        dry_c = _mixc(nt, n2, "#F0D49C" if not dusk else "#E8C290", "#E2C084" if not dusk else "#D8AE7C")
        wet_c = _mixc(nt, n1, "#B98F5E" if not dusk else "#A87E5E", "#9C7648" if not dusk else "#8E6850")
        L(_mixc(nt, wet, dry_c, wet_c), bsdf.inputs["Base Color"])
        r = N("ShaderNodeMapRange"); r.inputs["To Min"].default_value = 0.95; r.inputs["To Max"].default_value = 0.16
        L(wet, r.inputs["Value"]); L(r.outputs["Result"], bsdf.inputs["Roughness"])
        # ripple marks left by the tide, parallel to the shore
        wv = N("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Y"
        wv.inputs["Scale"].default_value = 3.2; wv.inputs["Distortion"].default_value = 2.2; wv.inputs["Detail"].default_value = 1.0
        L(pos, wv.inputs["Vector"])
        _bump(nt, bsdf, _math(nt, "ADD", _math(nt, "MULTIPLY", wv.outputs["Fac"], 0.6), n2), 0.28, 0.05)
    return nmat("sand" + str(dusk), f)


def _quicksand_mat():
    def f(nt, bsdf, N, L):
        tc = N("ShaderNodeTexCoord")
        wv = N("ShaderNodeTexWave"); wv.wave_type = "RINGS"; wv.rings_direction = "Z"
        wv.inputs["Scale"].default_value = 2.4; wv.inputs["Distortion"].default_value = 0.6; wv.inputs["Detail"].default_value = 1.0
        L(tc.outputs["Object"], wv.inputs["Vector"])
        nz = _noise(nt, tc.outputs["Object"], 3.0, 3.0)
        c = _mixc(nt, wv.outputs["Fac"], "#6E4E30", "#8E6A44")
        L(_mixc(nt, _math(nt, "MULTIPLY", nz, 0.5), c, "#5A3E28"), bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 0.07
        _bump(nt, bsdf, wv.outputs["Fac"], 0.5, 0.06)
    return nmat("quicksand", f)


def _cliffs(R, pts, grassm, h0=4.0):
    """Chunky layered sandstone cliff along a polyline, grass on top."""
    lo = mat("cliff_lo", "#B8794E", rough=0.9, noise=0.3, scale=1.2)
    mid = mat("cliff_mid", "#D99A62", rough=0.9, noise=0.3, scale=1.2)
    hi = mat("cliff_hi", "#EEC08A", rough=0.9, noise=0.25, scale=1.2)
    for i in range(len(pts) - 1):
        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
        n = max(1, int(math.dist(pts[i], pts[i + 1]) / 3.2))
        for k in range(n):
            t = (k + 0.5) / n
            x, y = xa + (xb - xa) * t, ya + (yb - ya) * t
            h = h0 * R.uniform(0.75, 1.25); w = R.uniform(3.6, 5.2); rz = math.atan2(yb - ya, xb - xa) + R.uniform(-0.25, 0.25)
            box((x, y, h * 0.18 - 0.3), (w * 1.12, 5.2, h * 0.36 + 0.6), lo, 0.35, (0, 0, rz))
            box((x, y, h * 0.55), (w, 4.6, h * 0.4), mid, 0.3, (0, 0, rz + R.uniform(-0.1, 0.1)))
            box((x, y, h * 0.86), (w * 0.94, 4.3, h * 0.26), hi, 0.25, (0, 0, rz + R.uniform(-0.1, 0.1)))
            box((x, y, h + 0.08), (w * 1.0, 4.6, 0.36), grassm, 0.17, (0, 0, rz))
            for _ in range(3):
                grass_tuft(x + R.uniform(-w / 2, w / 2) * 0.8, y + R.uniform(-1.8, 1.8), h + 0.22, R, grassm, 0.55, 4)
            if R.random() < 0.6:  # fallen blocks at the foot
                rock((x + R.uniform(-2, 2), y + math.copysign(3.0, -1) * math.cos(rz) + R.uniform(-0.4, 0.4), 0.15), R.uniform(0.35, 0.7), mid, R.random() * 3)


def _lighthouse(loc, s=1.0, lit=True):
    with Group(loc, (0, 0, 0), s):
        white = mat("lhw", "#FFF6E6", rough=0.7, noise=0.06); red = mat("lhr", "#E8513A", rough=0.6, noise=0.06)
        H, r0, r1, nb = 9.0, 1.5, 1.0, 5
        for k in range(nb):
            ra, rb = r0 + (r1 - r0) * k / nb, r0 + (r1 - r0) * (k + 1) / nb
            cyl((0, 0, H * (k + 0.5) / nb), ra, H / nb, red if k % 2 else white, verts=20, bevel=0, r2=rb)
        cyl((0, 0, H + 0.12), 1.45, 0.24, mat("lhk", "#33414E", rough=0.5, noise=0), verts=20)
        for k in range(10):
            a = k / 10 * math.tau
            cyl((1.38 * math.cos(a), 1.38 * math.sin(a), H + 0.6), 0.03, 0.7, mat("lhk", "#33414E", rough=0.5, noise=0), verts=4, bevel=0)
        ring((0, 0, H + 0.95), 1.38, 0.035, mat("lhk", "#33414E", rough=0.5, noise=0), 1.0)
        cyl((0, 0, H + 0.95), 0.8, 1.4, mat("lhglass", "#FFF2B8", rough=0.2, emit="#FFE28A", emit_strength=9 if lit else 2.5, noise=0), verts=12)
        cyl((0, 0, H + 2.05), 1.0, 0.9, red, verts=16, r2=0.08)
        sphere((0, 0, H + 2.6), 0.14, mat("lhk", "#33414E", rough=0.5, noise=0), sub=1)
        box((0, -1.42, 0.95), (0.7, 0.2, 1.7), mat("lhdoor", "#33414E", noise=0.1), 0.04)
        for z in (3.6, 6.2):
            box((0, -r0 + 0.12 + z * 0.055, z), (0.42, 0.2, 0.62), mat("lhwin", "#2D4A6B", rough=0.2, noise=0), 0.03)
        # keeper's cottage
        box((2.9, 0.3, 1.1), (3.0, 2.6, 2.2), white, 0.05)
        prism_roof((2.9, 0.3, 2.2), 3.0, 2.6, 1.2, red, overhang=0.25)
        box((2.9, -1.02, 0.8), (0.6, 0.1, 1.5), mat("lhdoor", "#33414E", noise=0.1), 0.03)
        if lit:
            glow((0, -1.6, H + 0.95), 4.5, "#FFE9A8", 3.0, 2.2)


def _hut(loc, rz, wallc, roofc, R):
    """Fishing hut on stilts with ladder, net and buoys."""
    wood = mat("stilt", "#7A5C42", rough=0.9, noise=0.35, scale=4)
    wall = mat("hut" + wallc, wallc, rough=0.8, noise=0.18, bricks={"scale": 1, "c2": wallc, "mortar_c": "#4A3A2E", "w": 0.26, "h": 4.0, "mortar": 0.012, "k": 1})
    with Group(loc, (0, 0, rz)):
        for sx in (-1.15, 1.15):
            for sy in (-0.95, 0.95):
                cyl((sx, sy, 0.7), 0.09, 2.6, wood, verts=8, rot=(0.04 * sy, 0.04 * sx, 0))
        for sy in (-0.95, 0.95):
            box((0, sy, 0.75), (2.6, 0.06, 0.1), wood, 0.01, (0, math.radians(32), 0))
        box((0, 0, 1.75), (3.1, 2.6, 0.14), wood, 0.03)
        box((0.15, 0.15, 2.85), (2.4, 2.0, 2.1), wall, 0.04)
        prism_roof((0.15, 0.15, 3.9), 2.4, 2.0, 0.95, mat("hutroof" + roofc, roofc, rough=0.7, noise=0.2), overhang=0.3)
        box((-0.3, -0.87, 2.72), (0.7, 0.08, 1.7), mat("hutdoor", "#5B4332", noise=0.25), 0.03)
        box((0.75, -0.87, 3.05), (0.6, 0.08, 0.6), mat("winframe", "#FFF4E0", noise=0.05), 0.02)
        box((0.75, -0.9, 3.05), (0.46, 0.08, 0.46), mat("hutglass", "#FFD88A", rough=0.2, emit="#FFC060", emit_strength=3.5, noise=0), 0)
        for k in range(5):  # ladder
            box((-1.05, -1.5 + 0.0, 0.25 + k * 0.36), (0.5, 0.05, 0.05), wood, 0)
        for sx in (-1.3, -0.8):
            box((sx, -1.5, 0.9), (0.06, 0.06, 1.9), wood, 0.01)
        for sx in (-1.4, 1.4):  # porch rail posts
            box((sx, -1.2, 2.2), (0.07, 0.07, 0.8), wood, 0.01)
        box((0.4, -1.2, 2.58), (2.0, 0.06, 0.07), wood, 0.01)
        # buoys hanging on the wall, net draped over the rail
        for k, c in enumerate(("#FF6B5B", "#FFF4E0", "#FFC93C")):
            sphere((1.42, -0.5 + k * 0.42, 2.5 - 0.1 * (k % 2)), 0.16, mat("buoy" + c, c, rough=0.5, noise=0.05), scale=(0.8, 1, 1.15), sub=2)
        box((0.9, -1.23, 2.3), (0.9, 0.03, 0.55), mat("net", "#3E7E8E", rough=0.95, noise=0.5, scale=14), 0, (0.12, 0, 0))
        cyl((0.9, 0.5, 4.75), 0.11, 0.7, mat("hutpipe", "#33414E", rough=0.5, noise=0), verts=8)


def _boat(loc, rot, hullc="#2E8CB8", trim="#FFF4E0"):
    """Small clinker fishing boat lying on the sand."""
    L, B, D = 4.4, 0.85, 0.8
    hull = mat("boat" + hullc, hullc, rough=0.6, noise=0.18, scale=5)
    tr = mat("boattrim" + trim, trim, rough=0.6, noise=0.1)
    wood = mat("boatwood", "#9C6B3F", rough=0.8, noise=0.3, scale=5)
    with Group(loc, rot):
        rings, inner = [], []
        ns = 12
        for i in range(ns + 1):
            t = i / ns
            x = -L / 2 + L * t
            b = B * (math.sin(math.pi * min(1, 0.12 + t * 0.95)) ** 0.55) * (0.55 + 0.45 * min(1, (1 - t) * 3.2))
            sheer = D + 0.35 * (2 * t - 1) ** 2 + 0.25 * max(0, t - 0.7)
            keel = 0.25 * max(0, t - 0.75) * 4 * 0.6
            rings.append([(x, -b, sheer), (x, -b * 0.95, sheer * 0.55), (x, -b * 0.55, keel + 0.12), (x, 0, keel), (x, b * 0.55, keel + 0.12), (x, b * 0.95, sheer * 0.55), (x, b, sheer)])
            inner.append([(x, -b * 0.86, sheer), (x, -b * 0.6, 0.38), (x, 0, 0.3), (x, b * 0.6, 0.38), (x, b * 0.86, sheer)])
        loft(rings, hull, caps=True)
        loft(inner, wood, caps=False)
        for sgn in (-1, 1):  # gunwale + painted strake
            tube([(p[0][0], sgn * abs(p[0][1]), p[0][2] + 0.02) for p in rings], 0.055, tr)
            tube([(p[1][0], sgn * abs(p[1][1]) * 1.02, p[1][2] + 0.1) for p in rings], 0.03, tr)
        for x in (-1.1, 0.2, 1.2):  # thwarts
            box((x, 0, 0.72), (0.28, 1.5, 0.05), wood, 0.01)
        cyl((0.55, 0, 1.6), 0.05, 2.4, wood, verts=8)  # stub mast
        tube([(0.55, 0, 2.75), (0.2, 0.05, 2.2), (-1.9, 0.1, 1.1)], 0.015, mat("ropem", "#C9B48E", rough=0.9, noise=0))
        cyl((-0.3, 0.55, 0.92), 0.03, 2.6, wood, verts=6, rot=(0, math.radians(88), 0.12))  # oar across
        box((-1.65, 0.7, 0.95), (0.5, 0.16, 0.03), wood, 0.01, (0, 0, 0.12))


def _pier(x0, y0, y1, R, sea_z):
    wood = mat("pierwood", "#8A6A4E", rough=0.9, noise=0.35, scale=4)
    dark = mat("pierdark", "#5E4634", rough=0.9, noise=0.35, scale=4)
    z = 1.1
    n = int((y1 - y0) / 0.42)
    for k in range(n):
        y = y0 + k * 0.42
        if k in (7, 19):
            continue  # missing planks: weathered
        box((x0 + R.uniform(-0.04, 0.04), y, z + R.uniform(-0.012, 0.012)), (1.9 + R.uniform(-0.1, 0.1), 0.36, 0.07), wood, 0.012, (0, 0, R.uniform(-0.03, 0.03)))
    for sx in (-0.85, 0.85):
        box((x0 + sx, (y0 + y1) / 2, z - 0.12), (0.12, y1 - y0, 0.16), dark, 0.02)
    k = 0
    y = y0 + 0.3
    while y < y1:
        for sx in (-0.95, 0.95):
            top = z + (0.75 if (k % 2 == 0) else 0.12)
            cyl((x0 + sx, y, (top - 1.2) / 2 + 0.0), 0.11, top + 1.2, dark, verts=8, rot=(R.uniform(-0.04, 0.04), R.uniform(-0.04, 0.04), 0))
        box((x0, y, z - 0.45), (2.3, 0.07, 0.09), dark, 0.01, (0, math.radians(22), 0))
        y += 3.0; k += 1
    ropem = mat("ropem", "#C9B48E", rough=0.9, noise=0)
    yy = y0 + 0.3
    while yy + 6 < y1:
        for sx in (-0.95, 0.95):
            rope((x0 + sx, yy, z + 0.68), (x0 + sx, yy + 6, z + 0.68), 0.22, ropem, 0.022)
        yy += 6
    # lamp post at the pier head + a crate and a coil
    cyl((x0 - 0.8, y1 - 0.6, z + 1.3), 0.05, 2.6, dark, verts=8)
    box((x0 - 0.8, y1 - 0.6, z + 2.7), (0.26, 0.26, 0.34), mat("pierlamp", "#FFE08A", emit="#FFC860", emit_strength=10, noise=0), 0.03)
    glow((x0 - 0.8, y1 - 0.8, z + 2.7), 1.1, "#FFD080", 2.0, 2.2)
    crate((x0 + 0.5, y0 + 2.2, z + 0.03), 0.5, 0.3)
    ring((x0 - 0.45, y0 + 4.0, z + 0.1), 0.2, 0.06, ropem, 1.0)


def set_marsh(variant="tide"):
    R = random.Random(11)
    dusk = variant == "dusk"
    flood = variant == "flood"
    sea_z = -0.016 if flood else -0.066
    SLOPE = 0.012

    def wav(x):
        return 0.008 * math.sin(x * 0.45 + 0.6) + 0.005 * math.sin(x * 1.15 + 2.0)

    DUNES = ((9.5, 2.5, 3.2, 4.0, 2.4), (13.5, 8, 4, 5, 3.3), (17, 0, 5, 6, 4.2), (11.5, -5, 4, 4, 2.6), (21, 15, 6, 7, 3.4), (26, 4, 7, 9, 5.0),
             (-11, -4, 4, 4, 2.0), (-16, 1, 5, 5, 2.4), (15, 19, 4, 5, 1.6), (-22, 12, 6, 8, 2.0))
    CHAN = ((-3.4, 11), (-2.6, 8.2), (-3.2, 6.2), (-4.8, 4.2), (-5.4, 2.2), (-7.2, 0.2), (-8.5, -3))
    POOLS = ((3.3, 5.4, 1.15, 0.7), (-1.2, 6.9, 0.8, 0.55), (4.6, 1.2, 0.7, 0.5), (1.6, 8.2, 1.3, 0.6), (-2.2, -2.2, 0.9, 0.55), (2.4, -3.6, 0.7, 0.5))

    def seg_d(px, py, a, b):
        ax, ay = a; bx, by = b
        dx, dy = bx - ax, by - ay
        t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
        return math.hypot(px - ax - dx * t, py - ay - dy * t)

    def h(x, y):
        z = -max(0.0, y - 3.0) * SLOPE + (wav(x) * min(1.0, max(0.0, (y - 3.0) / 2.0)))
        if y > 30:
            z -= (y - 30) * 0.03
        d = 0.0
        for cx, cy, rx, ry, hh in DUNES:
            d += hh * math.exp(-(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2))
        z += max(0.0, d - 0.03)
        dc = min(seg_d(x, y, CHAN[i], CHAN[i + 1]) for i in range(len(CHAN) - 1))
        z -= 0.14 * math.exp(-(dc / 0.42) ** 2)
        for cx, cy, rx, ry in POOLS:
            z -= 0.13 * math.exp(-(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2) * 1.6)
        return z

    sand = _sand_mat(dusk)
    terrain(h, -34, 34, -16, 44, 230, 200, sand)
    plane((0, 0, -0.4), (190, 190), mat("deep", "#9C7648", rough=0.9, noise=0.1))
    # sea: one glossy sheet under the sand; it shows wherever the sand dips below sea level (pools, channel, shore)
    seac = "#3FA7B8" if not dusk else "#4E8FA8"
    plane((0, 35, sea_z), (190, 130), water_mat("sea" + variant, seac, alpha=1.0, rough=0.09, wave=0.35, wave_scale=1.6))
    # foam: shoreline edge + breaking lines further out
    foam = mat("foam", "#FFFDF4", rough=0.6, emit="#FFF4E0", emit_strength=0.5, noise=0)

    def shore(x):
        return 3.0 + (wav(x) - sea_z) / SLOPE

    def foam_line(off, width, amp, ph, gaps, x0=-34, x1=34):
        n = 170; seg = []
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            y = shore(x) + off + amp * math.sin(x * 0.33 + ph) + amp * 0.5 * math.sin(x * 0.9 + ph * 2)
            wv = width * (0.55 + 0.45 * math.sin(x * 0.8 + ph * 3) ** 2)
            cut = gaps and math.sin(x * 0.27 + ph * 5) > 0.55
            if cut or (abs(x - 4.6) < 1.0 and off > 0.5 and y < 24):
                if len(seg) > 2:
                    _strip(seg)
                seg = []
                continue
            seg.append((x, y, wv))
        if len(seg) > 2:
            _strip(seg)

    def _strip(seg):
        verts = [(x, y - w / 2, sea_z + 0.006) for x, y, w in seg] + [(x, y + w / 2, sea_z + 0.006) for x, y, w in seg]
        n = len(seg)
        o = mesh("foam", verts, [(i, i + 1, n + i + 1, n + i) for i in range(n - 1)], foam)
        o.visible_shadow = False

    foam_line(0.16, 0.26, 0.0, 0.0, False)
    foam_line(0.7, 0.12, 0.12, 1.0, True)
    for off, wd, amp, ph in ((2.4, 0.3, 0.35, 0.4), (4.6, 0.22, 0.5, 1.7), (7.8, 0.36, 0.6, 2.9), (12.5, 0.3, 0.8, 4.0), (18.5, 0.4, 1.0, 5.2), (27, 0.5, 1.2, 0.9), (38, 0.6, 1.4, 2.2)):
        foam_line(off, wd, amp, ph, True, -60, 60)

    # --- the quicksand patch at (0,2): darker, glossy, ripple rings, bubbles, crumbly rim
    outline = []
    for i in range(40):
        a = i / 40 * math.tau
        r = 1.0 + 0.07 * math.sin(a * 3 + 0.5) + 0.05 * math.sin(a * 7 + 1.2) + 0.03 * math.sin(a * 11)
        outline.append((1.95 * r * math.cos(a), 2.0 + 1.5 * r * math.sin(a)))
    rim = mat("qsrim", "#C29A66", rough=0.75, noise=0.3, scale=5)
    poly([(x * 1.07, 2.0 + (y - 2.0) * 1.08) for x, y in outline], 0.0, 0.016, rim, axis="xy")
    o = poly(outline, 0.004, 0.016, _quicksand_mat(), axis="xy")
    ripple = mat("ripple", "#A88052", rough=0.1, noise=0)
    for r in (0.42, 0.74, 1.08, 1.42):
        q = ring((0, 2, 0.022), r, 0.026, ripple)
        q.scale = (1.0, 0.82, 0.3)
    bub = mat("qsbubble", "#9A7850", rough=0.05, noise=0)
    for bx, by, br in ((0.75, 1.55, 0.07), (-0.9, 2.3, 0.05), (0.35, 2.85, 0.06), (-0.5, 1.2, 0.045), (1.25, 2.4, 0.04), (-1.3, 1.75, 0.035)):
        sphere((bx, by, 0.02), br, bub, scale=(1, 1, 0.55), sub=2)
    for i in range(26):  # crumbling lumps round the rim
        a = i / 26 * math.tau + R.uniform(-0.08, 0.08)
        rr = 1.07 + R.uniform(0.0, 0.07)
        rock((2.0 * rr * math.cos(a), 2.0 + 1.55 * rr * math.sin(a), 0.01), R.uniform(0.05, 0.12), rim, R.random() * 3, 0.5)

    # --- warning sign + rope posts on the safe side
    wood = mat("drift", "#A08A6C", rough=0.9, noise=0.4, scale=5)
    dark = mat("pierdark", "#5E4634", rough=0.9, noise=0.35, scale=4)
    with Group((1.95, 0.35, 0), (0, -5, -14)):
        cyl((0, 0, 0.75), 0.05, 1.5, dark, verts=8)
        cyl((0, -0.04, 1.42), 0.46, 0.05, mat("signy", "#FFC93C", rough=0.5, noise=0.05), verts=3, rot=(math.radians(90), 0, math.radians(0)), bevel=0.02)
        cyl((0, -0.075, 1.42), 0.33, 0.02, mat("signw", "#FFF4E0", rough=0.5, noise=0), verts=3, rot=(math.radians(90), 0, 0), bevel=0)
        box((0, -0.095, 1.46), (0.055, 0.02, 0.22), mat("signk", "#1E1A18", noise=0), 0.005)
        sphere((0, -0.095, 1.29), 0.035, mat("signk", "#1E1A18", noise=0), sub=1)
    ropem = mat("ropem", "#C9B48E", rough=0.9, noise=0)
    posts = [(-2.9, -0.2), (-1.6, -0.55), (-0.2, -0.7), (1.1, -0.55), (2.9, -0.1), (3.6, 1.4)]
    for i, (px, py) in enumerate(posts):
        cyl((px, py, 0.4), 0.055, 0.9, dark, verts=8, rot=(R.uniform(-0.08, 0.08), R.uniform(-0.08, 0.08), 0))
        if i and i != 3:
            a = posts[i - 1]
            rope((a[0], a[1], 0.78), (px, py, 0.78), 0.14, ropem, 0.02)

    # --- beached boat, driftwood, rocks with seaweed, shells, starfish, lobster pot
    _boat((-3.9, 5.6, 0.02), (16, 4, -28))
    cyl((-2.35, 4.1, 0.25), 0.07, 0.6, dark, verts=8, rot=(0.1, 0.1, 0))
    rope((-2.35, 4.1, 0.5), (-2.85, 4.75, 0.75), 0.1, ropem, 0.02)
    for (x, y, l, rz) in ((-3.3, 0.9, 2.3, 22), (3.3, 3.5, 1.5, -40), (6.2, 0.2, 1.9, 70), (-6.2, 6.6, 1.6, 10)):
        cyl((x, y, 0.09), 0.1, l, wood, rot=(0, math.radians(90), math.radians(rz)), verts=8, r2=0.06)
        cyl((x + 0.2, y + 0.1, 0.2), 0.035, 0.5, wood, rot=(0.9, 0.3, math.radians(rz)), verts=6, r2=0.015)
    rk = mat("rock", "#7E766C", rough=0.85, noise=0.35, scale=3)
    weed = mat("weed", "#5E8A4A", rough=0.6, noise=0.2)
    for (x, y, s) in ((-4.9, 2.6, 0.45), (-5.5, 2.9, 0.28), (5.3, 3.4, 0.5), (5.9, 3.0, 0.3), (-1.6, 8.6, 0.4), (2.4, 9.6, 0.5), (3.0, 9.9, 0.3), (-7.5, 8.5, 0.6), (0.9, -2.4, 0.22), (7.4, 5.3, 0.4)):
        rock((x, y, 0.06), s, rk, R.random() * 3)
        if s > 0.38:
            sphere((x + 0.05, y - 0.05, 0.06 + s * 0.45), s * 0.55, weed, scale=(1.2, 0.9, 0.35), sub=2)
    star = mat("starfish", "#FF6B5B", rough=0.6, noise=0.1)
    for (x, y, rz) in ((2.9, 0.9, 0.3), (-1.9, 3.9, 1.2), (0.9, 5.4, 2.0)):
        for k in range(5):
            a = rz + k / 5 * math.tau
            cyl((x + 0.08 * math.cos(a), y + 0.08 * math.sin(a), 0.03), 0.04, 0.17, star, verts=6, r2=0.008, rot=(0, math.radians(90), a), bevel=0)
    shell = mat("shell", "#FFF4E0", rough=0.4, noise=0.05)
    for _ in range(16):
        x, y = R.uniform(-6, 6), R.uniform(-3, 7)
        if abs(x) < 2.4 and 0.2 < y < 3.8:
            continue
        sphere((x, y, 0.015), R.uniform(0.035, 0.06), shell, scale=(1.2, 1, 0.5), sub=1)
    with Group((4.3, -0.9, 0), (0, 0, 25)):  # lobster pot + buoy
        box((0, 0, 0.22), (0.8, 0.5, 0.42), mat("pot", "#8A6A4E", rough=0.9, noise=0.5, scale=16), 0.12)
        sphere((0.6, 0.2, 0.17), 0.17, mat("buoy#FF6B5B", "#FF6B5B", rough=0.5, noise=0.05), scale=(0.85, 0.85, 1.2), sub=2)
        ring((0.6, 0.2, 0.2), 0.15, 0.03, mat("buoy#FFF4E0", "#FFF4E0", rough=0.5, noise=0.05), 1.0)

    # --- dunes with marram grass (right), cliffs + lighthouse headland (left), huts, pier
    grass = mat("dunegrass", "#8FAE5A" if not dusk else "#7E9A5A", rough=0.8, noise=0.2)
    grass2 = mat("dunegrass2", "#B5BE6A" if not dusk else "#9CA868", rough=0.8, noise=0.2)
    placed = 0
    while placed < 120:
        x, y = R.uniform(6, 30), R.uniform(-9, 24)
        z = h(x, y)
        if z < 0.5:
            continue
        grass_tuft(x, y, z - 0.03, R, grass if placed % 3 else grass2, R.uniform(0.5, 0.95), 5)
        placed += 1
    placed = 0
    while placed < 26:
        x, y = R.uniform(-20, -8), R.uniform(-8, 5)
        z = h(x, y)
        if z < 0.45:
            continue
        grass_tuft(x, y, z - 0.03, R, grass, R.uniform(0.5, 0.9), 5); placed += 1
    cliffg = mat("cliffgrass", "#7FA650" if not dusk else "#6E9050", rough=0.9, noise=0.25, scale=1.5)
    _cliffs(R, [(-9.5, 3.5), (-10.5, 9), (-12.5, 15), (-13.5, 22), (-16, 29), (-17, 37)], cliffg, 4.2)
    _cliffs(R, [(-14, 40), (-18, 44), (-24, 46)], cliffg, 5.5)
    _cliffs(R, [(-17, 2), (-18, 12), (-20, 24), (-23, 36)], cliffg, 5.8)
    _lighthouse((-17.5, 45.5, 5.6), 1.15, lit=True)
    # far headland + islands in haze (right, behind the dunes)
    haze = mat("haze", "#E8A888" if not dusk else "#B88AA0", rough=1.0, noise=0.0, emit="#E8A080" if not dusk else "#A87A98", emit_strength=0.35)
    for (x, y, s, f) in ((30, 84, 16, 0.22), (48, 80, 20, 0.3), (-44, 82, 22, 0.25), (8, 90, 9, 0.12)):
        o = sphere((x, y, -0.5), s, haze, scale=(1.8, 0.4, f), sub=3); o.visible_shadow = False
    _hut((6.9, 7.4, 0.1), -18, "#3E9E9A", "#B5523B", R)
    _hut((9.9, 10.6, 0.3), -32, "#F2C9A0", "#5E6B7A", R)
    box((8.3, 5.4, 0.9), (0.06, 0.06, 1.8), dark, 0.01); box((9.9, 6.0, 0.95), (0.06, 0.06, 1.9), dark, 0.01)   # net drying rack
    box((9.1, 5.7, 1.25), (1.75, 0.03, 1.0), mat("net", "#3E7E8E", rough=0.95, noise=0.5, scale=14), 0, (0, 0, math.radians(20)))
    _pier(4.6, 8.6, 24.5, R, sea_z)
    gull((4.6 - 0.95, 8.9, 1.85), 2.2); gull((4.6 + 0.95, 14.9, 1.85), -1.0); gull((-2.35, 4.1, 0.55), 0.5); gull((3.6, 1.4, 0.83), 2.6)
    # a second boat moored off the pier, sail up
    with Group((9.5, 26, sea_z - 0.1), (0, 0, 200)):
        _boat((0, 0, 0), (0, 0, 0), "#E8513A", "#FFF4E0")
        mesh("sail", [(0.6, 0, 1.0), (0.6, 0, 4.4), (-1.9, 0, 1.1)], [(0, 1, 2)], mat("sail", "#FFF1D6", rough=0.9, noise=0.08))
        cyl((0.55, 0, 2.7), 0.045, 3.6, mat("boatwood", "#9C6B3F", rough=0.8, noise=0.3, scale=5), verts=8)

    # --- sky: low golden sun over the sea (right of centre), warm layered clouds, far gulls
    if dusk:
        sky3([(0.0, "#FFB98A"), (0.06, "#FF9E86"), (0.2, "#C583A8"), (0.5, "#5B5E9E"), (1.0, "#2E3A72")], 1.0)
        sun((82, 0, 155), "#FF9A6A", 3.2, 4)
        area((0, -8, 7), (58, 0, 0), 12, "#A8A0E8", 420)
        sunc, cl1, cl2 = "#FFC890", "#FF9E8A", "#C87E9E"
    else:
        sky3([(0.0, "#FFE2A8"), (0.05, "#FFD29A"), (0.18, "#F4C2A4"), (0.42, "#8EC6E4"), (1.0, "#4E96D0")], 1.05)
        sun((74, 0, 155), "#FFC98A", 4.6, 4)
        area((-3, -8, 7), (58, 0, -15), 12, "#CFE0FF", 380)
        sunc, cl1, cl2 = "#FFF2C0", "#FFD9A8", "#FFB8A0"
    sx, sy, sz = 36, 82, (5.5 if dusk else 10.5)
    o = sphere((sx, sy, sz), 3.0, mat("sundisc", sunc, emit=sunc, emit_strength=14, noise=0)); o.visible_shadow = False
    glow((sx, sy - 3.5, sz), 26, "#FFD890" if not dusk else "#FF9E70", 2.4, 2.4, color2="#FFB070" if not dusk else "#E86A80")
    c1 = mat("cloud1", cl1, rough=1.0, emit=cl1, emit_strength=0.75, noise=0)
    c2 = mat("cloud2", cl2, rough=1.0, emit=cl2, emit_strength=0.65, noise=0)
    for (x, z, s, m) in ((-30, 16, 5, c1), (-8, 22, 6, c1), (14, 15, 4, c2), (40, 24, 6.5, c1), (-48, 26, 6, c2), (0, 34, 5, c2), (26, 36, 5.5, c1), (-24, 40, 6, c1), (52, 12, 4, c2), (-58, 13, 5, c1)):
        cloud((x, 88 + (z % 5), z), s, m, 4 if s < 6 else 5)
    bk = mat("birdk", "#4A3E4A", rough=1, noise=0)
    for (x, y, z, s) in ((-6, 40, 9, 0.6), (-4.2, 42, 9.8, 0.5), (-7.6, 44, 10.4, 0.45), (10, 50, 14, 0.7), (12, 52, 13.2, 0.55), (-20, 48, 19, 0.6)):
        bird((x, y, z), s, bk)


# ---------------------------------------------------------------- arctic (A-002 polar bear liver)

def aurora_mat(key, c_low, c_mid, c_top, strength=3.0):
    def f(nt, bsdf, N, L):
        tc = N("ShaderNodeTexCoord"); sp = N("ShaderNodeSeparateXYZ"); L(tc.outputs["Generated"], sp.inputs[0])
        u, v = sp.outputs["X"], sp.outputs["Z"]
        col = _ramp(nt, v, [(0.0, c_low), (0.28, c_mid), (0.8, c_top), (1.0, c_top)])
        # vertical rays: noise stretched along the height
        mp = N("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (46.0, 1.0, 0.5); L(tc.outputs["Generated"], mp.inputs[0])
        rays = _math(nt, "ADD", _math(nt, "MULTIPLY", _noise(nt, mp.outputs[0], 1.0, 2.0, 0.6), 1.1), 0.12)
        mp2 = N("ShaderNodeMapping"); mp2.inputs["Scale"].default_value = (5.0, 1.0, 0.2); L(tc.outputs["Generated"], mp2.inputs[0])
        slow = _math(nt, "ADD", _math(nt, "MULTIPLY", _noise(nt, mp2.outputs[0], 1.0, 1.0), 1.3), -0.1, clamp=True)
        fall = _math(nt, "POWER", _math(nt, "SUBTRACT", 1.0, v, clamp=True), 1.7)
        foot = _math(nt, "MULTIPLY", v, 14.0, clamp=True)                       # soft lower edge
        ends = _math(nt, "POWER", _math(nt, "SINE", _math(nt, "MULTIPLY", u, math.pi)), 0.6)
        a = _math(nt, "MULTIPLY", _math(nt, "MULTIPLY", fall, foot), _math(nt, "MULTIPLY", ends, _math(nt, "MULTIPLY", rays, slow)), clamp=True)
        em = N("ShaderNodeEmission"); em.inputs[1].default_value = strength; L(col, em.inputs[0])
        tr = N("ShaderNodeBsdfTransparent"); mx = N("ShaderNodeMixShader")
        L(a, mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2])
        L(mx.outputs[0], nt.nodes["Material Output"].inputs[0])
    return nmat(key, f)


def aurora(path, z0, height, m, lean=6.0, n=120):
    """Curtain ribbon: path(t) -> (x, y) for t 0..1, hanging from z0+height down to z0 (wavy lower edge)."""
    lo, hi = [], []
    for i in range(n + 1):
        t = i / n
        x, y = path(t)
        zb = z0 + 1.6 * math.sin(t * 9.0) + 0.8 * math.sin(t * 23.0)
        lo.append((x, y, zb)); hi.append((x, y + lean, zb + height))
    o = mesh("aurora", lo + hi, [(i, i + 1, n + 2 + i, n + 1 + i) for i in range(n)], m)
    o.visible_shadow = False
    return o


def _ship(loc, rot, lit=True):
    """Generic 1590s three-masted Dutch ship (fluyt-like), sails furled, snow on rails and yards. Bow towards +x."""
    L, B = 15.0, 2.1
    hullm = mat("hull", "#6B4630", rough=0.8, noise=0.3, bricks={"scale": 1, "c2": "#5E3C28", "mortar_c": "#3A261A", "w": 3.0, "h": 0.2, "mortar": 0.012, "k": 1})
    ochre = mat("hullochre", "#D9A04E", rough=0.7, noise=0.15)
    dark = mat("hulldark", "#3E2A1E", rough=0.8, noise=0.2)
    spar = mat("spar", "#8A6444", rough=0.8, noise=0.2)
    snow = mat("shipsnow", "#F2F8FF", rough=0.8, noise=0.05)
    sail = mat("sailf", "#E4D6B4", rough=0.9, noise=0.15)
    rig = mat("rig", "#2E2420", rough=0.9, noise=0)
    with Group(loc, rot):
        ns = 16; rings = []; sheer = []
        for i in range(ns + 1):
            t = i / ns
            x = -L / 2 + L * t
            b = B * (0.72 + 0.28 * math.sin(math.pi * min(1.0, t * 1.5)) ** 0.8) * (1.0 if t < 0.72 else max(0.06, math.cos((t - 0.72) / 0.28 * math.pi / 2) ** 0.8))
            hs = 3.0 + 2.3 * max(0.0, (0.3 - t) / 0.3) ** 1.3 + 0.9 * max(0.0, (t - 0.78) / 0.22) ** 1.2
            keel = 1.4 * max(0.0, (t - 0.8) / 0.2) ** 2
            rings.append([(x, -b * 0.78, hs), (x, -b * 1.0, hs * 0.55 + keel * 0.4), (x, -b * 0.8, 0.5 + keel), (x, 0, keel), (x, b * 0.8, 0.5 + keel), (x, b * 1.0, hs * 0.55 + keel * 0.4), (x, b * 0.78, hs)])
            sheer.append((x, b * 0.78, hs))
        loft(rings, hullm, caps=True)
        for sgn in (-1, 1):
            tube([(x, sgn * y, z + 0.05) for x, y, z in sheer], 0.11, snow)                         # snow on the rail
            tube([(r[5][0], sgn * r[5][1] * 1.03, r[5][2] + 0.75) for r in rings], 0.09, ochre)       # painted wale
            tube([(r[5][0], sgn * r[5][1] * 1.04, r[5][2] + 0.1) for r in rings], 0.07, dark)
        # deck (snowy) and stern castle face with lit windows
        loft([[(r[0][0], r[0][1] * 0.96, r[0][2] - 0.25), (r[0][0], -r[0][1] * 0.96, r[0][2] - 0.25), (r[0][0], -r[0][1] * 0.96, r[0][2] - 0.3), (r[0][0], r[0][1] * 0.96, r[0][2] - 0.3)] for r in rings], snow, caps=False, smooth=False)
        box((-L / 2 - 0.03, 0, 3.9), (0.12, 2.5, 2.6), mat("stern", "#7A5236", rough=0.8, noise=0.25), 0.04)
        win = mat("shipwin", "#FFD88A", rough=0.3, emit="#FFB850", emit_strength=7 if lit else 0.5, noise=0)
        for wy in (-0.75, 0, 0.75):
            box((-L / 2 - 0.1, wy, 4.3), (0.06, 0.5, 0.62), win, 0.02)
        for wx in (-6.3, -5.2):
            for sgn in (-1, 1):
                box((wx, sgn * 1.62, 4.2), (0.5, 0.1, 0.5), win, 0.02)
        box((-L / 2 - 0.1, 0, 3.4), (0.07, 2.3, 0.14), ochre, 0.02); box((-L / 2 - 0.1, 0, 5.05), (0.07, 2.3, 0.14), ochre, 0.02)
        cyl((-L / 2 - 0.3, 0, 5.75), 0.16, 0.42, win, verts=8); cyl((-L / 2 - 0.3, 0, 6.03), 0.2, 0.16, dark, verts=8, r2=0.03)   # stern lantern
        if lit:
            point((-L / 2 - 1.0, 0, 5.0), "#FFB060", 500, 0.3)
            glow((-L / 2 - 0.3, -0.4, 5.75), 1.3, "#FFC070", 2.0, 2.2)
        # masts: (x, height above deck base, yard widths)
        tops = []
        for mx, mh, yards in ((4.0, 10.0, (4.6, 3.2)), (0.2, 12.2, (5.6, 3.8, 2.4)), (-4.4, 8.4, (0,))):
            zb = 2.6
            cyl((mx, 0, zb + mh / 2), 0.17, mh, spar, verts=10, r2=0.09)
            tops.append((mx, zb + mh))
            for k, yw in enumerate(yards):
                if not yw:
                    continue
                zz = zb + mh * (0.5 + 0.26 * k)
                cyl((mx + 0.2, 0, zz), 0.08, yw, spar, verts=8, rot=(math.radians(90), 0, 0))
                cyl((mx + 0.2, 0, zz - 0.2), 0.2, yw * 0.86, sail, verts=10, rot=(math.radians(90), 0, 0))     # furled sail
                box((mx + 0.2, 0, zz + 0.1), (0.22, yw * 0.9, 0.09), snow, 0.04)                              # snow on the yard
                for sgn in (-1, 1):
                    tube([(mx + 0.2, sgn * yw / 2, zz), (mx, 0, zz + mh * 0.2)], 0.02, rig, smooth=False)
            cyl((mx, 0, zb + mh * 0.62), 0.55, 0.14, spar, verts=12)                                           # top platform
            cyl((mx, 0, zb + mh * 0.62 + 0.11), 0.5, 0.08, snow, verts=12)
            for sgn in (-1, 1):                                                                                # shrouds
                for dx in (-0.7, 0.0, 0.7):
                    tube([(mx, 0, zb + mh * 0.62), (mx + dx, sgn * 1.75, 3.1)], 0.022, rig, smooth=False)
        # mizzen lateen yard, bowsprit, stays, pennant
        cyl((-4.6, 0, 8.2), 0.07, 5.2, spar, verts=8, rot=(0, math.radians(38), 0))
        cyl((-4.75, 0, 8.05), 0.16, 4.4, sail, verts=8, rot=(0, math.radians(38), 0))
        cyl((8.6, 0, 5.2), 0.13, 4.6, spar, verts=8, rot=(0, math.radians(62), 0))
        tube([(10.6, 0, 6.3), (tops[0][0], 0, tops[0][1] - 0.4)], 0.025, rig, smooth=False)
        tube([(tops[0][0], 0, tops[0][1] - 0.3), (tops[1][0], 0, tops[1][1] - 1.5)], 0.025, rig, smooth=False)
        tube([(tops[1][0], 0, tops[1][1] - 0.4), (tops[2][0], 0, tops[2][1] - 0.3)], 0.025, rig, smooth=False)
        tube([(tops[0][0] + 0.2, 0, 2.6 + 10 * 0.5), (7.2, 0, 4.1)], 0.025, rig, smooth=False)
        tube([(tops[2][0], 0, tops[2][1] - 0.3), (-7.4, 0, 5.4)], 0.025, rig, smooth=False)
        for k, c in enumerate(("#F28C28", "#FFF4E0", "#2E5A8C")):  # plain three-band pennant on the main top
            box((tops[1][0] - 0.75, 0, tops[1][1] - 0.2 - k * 0.2), (1.5, 0.03, 0.2), mat("pen" + c, c, rough=0.8, noise=0.05, emit=c, emit_strength=0.25), 0)


def _tent(loc, rz, lit=True):
    canvas = mat("canvas", "#D8C49A", rough=0.95, noise=0.3, scale=3)
    canvas2 = mat("canvas2", "#BFA87C", rough=0.95, noise=0.3, scale=3)
    pole = mat("tentpole", "#6B4A32", rough=0.8, noise=0.2)
    snow = mat("snowcap", "#F4F9FF", rough=0.8, noise=0.05)
    W, Ln, H = 1.7, 3.6, 2.3
    with Group(loc, (0, 0, rz)):
        v = [(-W, -Ln / 2, 0), (W, -Ln / 2, 0), (W, Ln / 2, 0), (-W, Ln / 2, 0), (0, -Ln / 2, H), (0, Ln / 2, H)]
        o = mesh("tent", v, [(0, 4, 5, 3), (1, 2, 5, 4), (3, 5, 2)], canvas)
        sol = o.modifiers.new("s", "SOLIDIFY"); sol.thickness = 0.05
        # front: two flaps pulled aside, warm dark inside
        mesh("flapL", [(-W, -Ln / 2 - 0.02, 0), (-0.55, -Ln / 2 - 0.02, 0), (-0.05, -Ln / 2 - 0.02, H - 0.05)], [(0, 1, 2)], canvas2)
        mesh("flapR", [(W, -Ln / 2 - 0.02, 0), (0.55, -Ln / 2 - 0.02, 0), (0.05, -Ln / 2 - 0.02, H - 0.05)], [(0, 1, 2)], canvas2)
        mesh("inside", [(-W * 0.95, -Ln / 2 + 0.25, 0.02), (W * 0.95, -Ln / 2 + 0.25, 0.02), (0, -Ln / 2 + 0.25, H * 0.95)], [(0, 1, 2)],
             mat("tentin", "#5A3420", rough=0.9, emit="#FF9A4A", emit_strength=0.9 if lit else 0.0, noise=0.2))
        for k in range(1, 4):  # seams
            for sgn in (-1, 1):
                yy = -Ln / 2 + k * Ln / 4
                tube([(sgn * W * 1.01, yy, 0.02), (sgn * 0.01, yy, H + 0.02)], 0.018, canvas2, smooth=False)
        for sy in (-Ln / 2 - 0.05, Ln / 2 + 0.05):  # crossed poles
            for sgn in (-1, 1):
                cyl((sgn * 0.06, sy, H / 2 + 0.25), 0.05, H * 1.35, pole, verts=6, rot=(0, sgn * math.atan2(W, H) * 0.12, 0))
        cyl((0, 0, H + 0.05), 0.045, Ln + 0.5, pole, verts=6, rot=(math.radians(90), 0, 0))
        ropem = mat("ropem", "#C9B48E", rough=0.9, noise=0)
        for sgn in (-1, 1):
            for sy in (-Ln / 2, 0, Ln / 2):
                tube([(sgn * W * 0.55, sy, H * 0.45), (sgn * (W + 1.0), sy, 0.02)], 0.014, ropem, smooth=False)
                cyl((sgn * (W + 1.0), sy, 0.1), 0.03, 0.25, pole, verts=5, rot=(0, -sgn * 0.4, 0))
            box((sgn * (W + 0.05), 0, 0.12), (0.55, Ln * 1.02, 0.3), snow, 0.13)          # snow banked on the skirts
            box((sgn * 0.55, 0.3, H * 0.68), (0.5, Ln * 0.6, 0.07), snow, 0.03, (0, -sgn * math.atan2(H, W), 0))   # snow patches on the roof
        if lit:
            point((0, -Ln / 2 + 0.6, 0.8), "#FF9A4A", 30, 0.2)


def _sledge(loc, rz):
    wood = mat("sledge", "#8A6444", rough=0.8, noise=0.3, scale=5)
    ropem = mat("ropem", "#C9B48E", rough=0.9, noise=0)
    with Group(loc, (0, 0, rz)):
        for sy in (-0.45, 0.45):
            tube([(-1.5, sy, 0.06), (0.9, sy, 0.06), (1.35, sy, 0.16), (1.6, sy, 0.48)], 0.05, wood)
            for sx in (-1.1, -0.2, 0.7):
                box((sx, sy, 0.24), (0.07, 0.07, 0.34), wood, 0.01)
        box((-0.2, 0, 0.42), (2.5, 1.05, 0.06), wood, 0.015)
        for sx in (-1.1, -0.2, 0.7):
            box((sx, 0, 0.37), (0.08, 1.0, 0.06), wood, 0.01)
        crate((-0.85, 0.1, 0.45), 0.6, 0.12); crate((-0.15, -0.12, 0.45), 0.5, -0.2); crate((-0.75, 0.05, 1.05), 0.42, 0.5)
        barrel((0.6, 0.05, 0.46), 0.62)
        box((-0.5, 0, 1.0), (1.3, 1.1, 0.03), mat("tarp", "#5E7A6E", rough=0.9, noise=0.25), 0.01, (0, 0.05, 0.1)).location.z = 0.98
        tube([(1.6, -0.45, 0.48), (2.6, -0.2, 0.05), (3.1, 0.3, 0.03)], 0.02, ropem)
        tube([(1.6, 0.45, 0.48), (2.5, 0.6, 0.05), (3.0, 0.5, 0.03)], 0.02, ropem)
        box((-0.2, 0.0, 0.5), (0.3, 1.12, 0.02), ropem, 0)


def _ice_slab(R, x, y, s, m, m2):
    box((x, y, s * 0.28), (s * R.uniform(1.0, 2.0), s * R.uniform(0.35, 0.7), s * R.uniform(0.9, 1.8)), m if R.random() < 0.7 else m2, 0.06,
        (R.uniform(-0.75, 0.75), R.uniform(-0.5, 0.5), R.uniform(0, 3.1)))


def set_arctic(variant="night"):
    R = random.Random(23)
    CAMP = (0.3, 2.4)

    def h(x, y):
        d = math.hypot(x - CAMP[0], (y - CAMP[1]) * 0.9)
        k = min(1.0, max(0.0, (d - 5.5) / 5.0))
        z = k * (0.22 * math.sin(x * 0.31 + 1.0) * math.cos(y * 0.23) + 0.12 * math.sin(x * 0.9 + y * 0.6) + 0.1)
        for cx, cy, rx, ry, hh in ((-9, 6, 4, 3, 1.3), (11, 5, 4, 3, 1.5), (-13, -2, 5, 4, 1.2), (9, -4, 4, 4, 0.9), (-16, 16, 6, 5, 1.8), (18, 16, 6, 5, 1.6), (-6, -7, 4, 3, 0.7)):
            z += hh * math.exp(-(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2))
        return z

    def snow_f(nt, bsdf, N, L):
        pos, s = _pos(nt)
        n1 = _noise(nt, pos, 0.5, 3.0)
        L(_mixc(nt, n1, "#DCEBFA", "#F6FAFF"), bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 0.55
        _bump(nt, bsdf, _noise(nt, pos, 3.5, 3.0), 0.25, 0.06)
    snow = nmat("snowground", snow_f)
    terrain(h, -60, 60, -20, 90, 170, 160, snow)
    snowm = mat("snowcap", "#F4F9FF", rough=0.8, noise=0.05)
    ice = mat("ice", "#A8E0F2", rough=0.12, noise=0.15, scale=3, emit="#5EC8E8", emit_strength=0.12)
    ice2 = mat("ice2", "#7FC4E4", rough=0.12, noise=0.15, scale=3, emit="#3EA8D8", emit_strength=0.12)

    # trampled camp floor + path to the ship (slightly darker packed snow), footprints
    pk = mat("packed", "#C8DCF0", rough=0.7, noise=0.25, scale=6)
    o = poly([(CAMP[0] + 3.6 * math.cos(a) * (1 + 0.12 * math.sin(3 * a)), CAMP[1] - 0.6 + 2.6 * math.sin(a) * (1 + 0.1 * math.cos(5 * a))) for a in [i / 30 * math.tau for i in range(30)]], 0.004, 0, pk, axis="xy")
    for i in range(22):
        t = i / 21
        fx, fy = 1.4 + 2.6 * t + 0.5 * math.sin(t * 5), 4.0 + 8.5 * t
        disc((fx + (0.14 if i % 2 else -0.14), fy, h(fx, fy) + 0.012), 0.11, pk, (0.7, 1.25, 1))

    # pressure ridges: jagged tilted slabs of ice in bands, plus blocks around the ship
    for i in range(46):
        t = i / 45
        x = -26 + 52 * t + R.uniform(-0.6, 0.6)
        y = 9.2 + 1.6 * math.sin(t * 7.0) + R.uniform(-0.9, 0.9)
        if 0.5 < x < 4.6:
            continue  # gap: the path to the ship
        _ice_slab(R, x, y, R.uniform(0.6, 1.5), ice, ice2)
    for i in range(34):
        t = i / 33
        _ice_slab(R, -30 + 60 * t + R.uniform(-1, 1), 27 + 3.0 * math.sin(t * 5.0 + 1) + R.uniform(-1.5, 1.5), R.uniform(1.2, 2.6), ice, ice2)
    for (x, y, s) in ((-6.2, 3.2, 0.7), (-6.9, 4.3, 1.0), (6.6, 1.2, 0.8), (7.3, 2.4, 0.5), (-5.2, -1.6, 0.55), (5.6, -2.4, 0.6), (6.4, 6.0, 0.9), (-4.6, 7.0, 0.8)):
        _ice_slab(R, x, y, s, ice, ice2)

    # the ship, held fast and heeled over, ice piled against the hull
    SH = (4.5, 17.0)
    _ship((SH[0], SH[1], -1.0), (7, -2.5, 168))
    for i in range(30):
        a = i / 30 * math.tau
        _ice_slab(R, SH[0] + 8.6 * math.cos(a) + R.uniform(-0.5, 0.5), SH[1] + 3.1 * math.sin(a) + R.uniform(-0.4, 0.4), R.uniform(0.7, 1.5), ice, ice2)
    for i in range(10):
        sphere((SH[0] - 7 + i * 1.6, SH[1] - 2.3, 0.1), R.uniform(0.6, 1.0), snowm, scale=(1.5, 0.8, 0.45), sub=2)

    # camp: tent, sledge, stores, oars rack, fire with tripod and pot, log seats
    _tent((-3.1, 3.4, 0), -52)
    _sledge((3.3, 3.0, 0), -158)
    for (x, y, s, rz) in ((-1.5, 4.9, 0.7, 0.2), (-0.75, 5.1, 0.6, -0.3), (-1.3, 4.95, 0.5, 0.6)):
        crate((x, y, 0.0 if s > 0.55 else 0.7), s, rz)
    barrel((-0.1, 5.3, 0), 0.8); barrel((0.5, 5.0, 0), 0.7)
    sphere((-1.1, 5.0, 1.24), 0.3, snowm, scale=(1.5, 1.2, 0.3), sub=2)
    wood = mat("sledge", "#8A6444", rough=0.8, noise=0.3, scale=5)
    with Group((2.0, 5.3, 0), (0, 0, -15)):       # oars and a boat hook leaning on a rack
        for sx in (-0.7, 0.7):
            cyl((sx, 0, 0.75), 0.05, 1.5, wood, verts=6, rot=(0, sx * 0.25, 0))
        cyl((0, 0, 1.4), 0.04, 1.9, wood, verts=6, rot=(0, math.radians(90), 0))
        for k in range(3):
            cyl((-0.45 + k * 0.42, -0.42, 1.2), 0.035, 2.6, wood, verts=6, rot=(math.radians(-20), 0, 0))
            box((-0.45 + k * 0.42, -0.85, 2.38), (0.16, 0.04, 0.55), wood, 0.02, (math.radians(-20), 0, 0))
    st = mat("stone", "#6A6660", rough=0.8, noise=0.3)
    FX, FY = 0.6, 1.2
    for k in range(10):
        a = k / 10 * math.tau
        rock((FX + 0.5 * math.cos(a), FY + 0.5 * math.sin(a), 0.07), 0.13, st, a, 0.75)
    log = mat("log", "#5B3A29", noise=0.3)
    for k in range(5):
        a = k / 5 * math.pi
        cyl((FX + 0.02 * math.cos(a), FY + 0.02 * math.sin(a), 0.14), 0.06, 0.8, log, verts=8, rot=(0, math.radians(72), a))
    flames(FX, FY, 0.1, 0.9, 5, None)
    flames(FX, FY - 0.14, 0.08, 0.6, 3, None)
    iron = mat("iron", "#2A1C1E", rough=0.5, metal=0.5)
    for k in range(3):
        a = k / 3 * math.tau + 0.5
        tube([(FX + 0.75 * math.cos(a), FY + 0.75 * math.sin(a), 0.0), (FX, FY, 1.75)], 0.028, iron, smooth=False)
    tube([(FX, FY, 1.72), (FX, FY, 1.15)], 0.012, iron, smooth=False)
    cyl((FX, FY, 0.98), 0.24, 0.3, iron, verts=14, r2=0.2)
    ring((FX, FY, 1.13), 0.2, 0.025, iron, 1.0)
    glow((FX, FY - 0.3, 0.7), 2.0, "#FF9A40", 1.6, 2.6)
    glow((FX, FY, 0.02), 3.6, "#FF8A3C", 0.5, 2.0, facing="z")
    point((FX, FY - 0.25, 0.75), "#FF8A3C", 900, 0.25)
    point((FX + 0.2, FY + 0.5, 1.3), "#FFA050", 500, 0.3)
    for (x, y, rz) in ((-0.9, 0.4, 0.5), (2.0, 0.6, -0.5)):   # log seats
        cyl((x, y, 0.2), 0.2, 1.3, log, verts=10, rot=(0, math.radians(90), rz))
        box((x, y, 0.4), (1.1, 0.26, 0.05), snowm, 0.02, (0, 0, rz))
    # harpoon + axe stuck in a stump, lantern on a crate
    cyl((1.4, 5.5, 0.9), 0.025, 1.8, wood, verts=5, rot=(0.25, 0, 0))
    box((-1.5, 4.55, 1.33), (0.16, 0.16, 0.24), mat("lglass", "#FFD27A", emit="#FFB84D", emit_strength=8, noise=0), 0.02)
    point((-1.5, 4.3, 1.35), "#FFB060", 60, 0.1)

    # far: icebergs and snowy peaks ringing the horizon
    berg = mat("berg", "#B8D8F0", rough=0.5, noise=0.2, scale=0.5, emit="#6E9AD0", emit_strength=0.18)
    berg2 = mat("berg2", "#8EB4DC", rough=0.5, noise=0.2, scale=0.5, emit="#5E88C0", emit_strength=0.15)
    for i in range(30):
        x = -75 + i * 5.2 + R.uniform(-1.5, 1.5)
        y = R.uniform(52, 72); s = R.uniform(4, 10)
        o = cyl((x, y, s * 0.42), s * R.uniform(0.7, 1.1), s, berg if i % 2 else berg2, verts=R.choice((4, 5, 6)), r2=s * R.uniform(0.02, 0.25), rot=(R.uniform(-0.12, 0.12), R.uniform(-0.12, 0.12), R.uniform(0, 3)), bevel=0.15)
        for p in o.data.polygons:
            p.use_smooth = False

    # sky: aurora curtains, stars, moon
    am1 = aurora_mat("aur1", "#7CFFB0", "#34E89A", "#2E9AD8", 4.2)
    am2 = aurora_mat("aur2", "#8CFFD0", "#3EDCC0", "#8A6CF0", 3.6)
    am3 = aurora_mat("aur3", "#B8FFB0", "#5CE8A0", "#C06CE0", 3.0)
    aurora(lambda t: (-70 + 120 * t, 78 + 7 * math.sin(t * 5.2) + 3 * math.sin(t * 13)), 17, 30, am1, 8)
    aurora(lambda t: (-30 + 105 * t, 84 + 6 * math.sin(t * 6.5 + 2) + 2.5 * math.sin(t * 15)), 27, 26, am2, 6)
    aurora(lambda t: (-78 + 80 * t, 88 + 5 * math.sin(t * 7 + 4)), 33, 22, am3, 5)
    stars(R, 190, 91, (-95, 95), (6, 78), 9)
    moon((-21, 86, 41), 3.0, 6.0, 4.5)
    sky3([(0.0, "#2E5A86"), (0.07, "#1E3E6E"), (0.3, "#10244E"), (1.0, "#070F2A")], 0.75)
    sun((48, 0, -155), "#A8C4FF", 2.3, 5)          # moonlight from the upper left
    area((0, -9, 8), (52, 0, 0), 14, "#6E96E0", 500)
    area((4, 30, 12), (-68, 0, 0), 20, "#4EE8B0", 2600)   # aurora light rims the ship and ridges from behind


# ---------------------------------------------------------------- castle (A-006 garderobes)

def _stone(name, c1, c2, mortar, w=0.7, hh=0.36):
    return mat(name, c1, rough=0.9, noise=0.22, scale=1.6, bricks={"scale": 1.0, "c2": c2, "mortar_c": mortar, "w": w, "h": hh, "mortar": 0.018, "k": 1})


def _merlons_line(x0, x1, y, z, m, depth=0.5, step=1.5, mw=0.85, mh=1.2):
    n = int((x1 - x0) / step)
    for k in range(n + 1):
        box((x0 + k * step, y, z + mh / 2), (mw, depth, mh), m, 0.04)


def _round_tower(x, y, r, z0, z1, m, m2, roofm=None, lit=False, slits=((0, 0.45), (0, 0.75))):
    cyl((x, y, (z0 + z1) / 2), r, z1 - z0, m, verts=28, bevel=0)
    cyl((x, y, z0 + 1.0), r * 1.12, 2.4, m, verts=28, bevel=0, r2=r)                 # battered base
    cyl((x, y, z1 - 0.2), r, 0.5, m2, verts=28, bevel=0, r2=r + 0.35)                # corbel flare
    cyl((x, y, z1 + 0.35), r + 0.35, 0.7, m, verts=28, bevel=0.03)
    n = 12
    for k in range(n):
        a = (k + 0.5) / n * math.tau
        box((x + (r + 0.12) * math.cos(a), y + (r + 0.12) * math.sin(a), z1 + 1.2), (0.46, 0.85, 1.0), m, 0.04, (0, 0, a))
    if roofm:
        cyl((x, y, z1 + 0.7 + (r * 1.3)), r - 0.15, r * 2.6, roofm, verts=20, bevel=0, r2=0.03)
        cyl((x, y, z1 + 0.7 + r * 2.6 + 0.6), 0.03, 1.4, mat("iron", "#2A1C1E", rough=0.5, metal=0.5), verts=5, bevel=0)
    sm = mat("slitlit", "#FFC870", emit="#FFB050", emit_strength=6, noise=0) if lit else mat("slitdark", "#1E1A1C", noise=0)
    for (da, f) in slits:
        a = -math.pi / 2 + da
        box((x + r * math.cos(a), y + r * math.sin(a), z0 + (z1 - z0) * f), (0.16, 0.16, 1.0), sm, 0.02, (0, 0, a))


def _banner(loc, c1, c2, h=2.6, w=0.9):
    x, y, z = loc
    cyl((x, y, z + h / 2 + 0.2), 0.035, h + 0.6, mat("spar", "#8A6444", rough=0.8, noise=0.2), verts=6)
    mesh("ban", [(x, y, z + h + 0.4), (x + w, y, z + h + 0.4), (x + w, y, z + h - 0.75), (x + w / 2, y, z + h - 0.5), (x, y, z + h - 0.75)], [(0, 1, 2, 3, 4)], mat("ban" + c1, c1, rough=0.8, noise=0.05, emit=c1, emit_strength=0.12))
    box((x + w / 2, y - 0.01, z + h + 0.1), (w, 0.01, 0.16), mat("ban" + c2, c2, rough=0.8, noise=0.05, emit=c2, emit_strength=0.12), 0)


def _siege_tent(loc, rz, c1, c2):
    with Group(loc, (0, 0, rz)):
        n = 10
        for k in range(n):
            a0, a1 = k / n * math.tau, (k + 1) / n * math.tau
            m = mat("st" + (c1 if k % 2 else c2), c1 if k % 2 else c2, rough=0.9, noise=0.12)
            v = [(1.5 * math.cos(a0), 1.5 * math.sin(a0), 0), (1.5 * math.cos(a1), 1.5 * math.sin(a1), 0), (1.5 * math.cos(a1), 1.5 * math.sin(a1), 1.5), (1.5 * math.cos(a0), 1.5 * math.sin(a0), 1.5), (0, 0, 3.0)]
            mesh("tentp", v, [(0, 1, 2, 3), (3, 2, 4)], m)
        cyl((0, 0, 3.2), 0.03, 0.6, mat("spar", "#8A6444", rough=0.8, noise=0.2), verts=5)
        sphere((0, 0, 3.5), 0.08, mat("gold", "#FFC93C", rough=0.35, metal=0.6), sub=1)


def set_castle(variant="night"):
    night = variant == "night"
    cut = variant == "cutaway"
    R = random.Random(37)
    WY = 3.2          # y of the wall's outer face
    WZ = 10.0         # wall-walk height
    MZ = -0.7         # moat water level
    if night:
        stone = _stone("cwall", "#8E97B0", "#7E88A4", "#565E7A")
        stone2 = _stone("cwall2", "#A0A8BE", "#8E97B0", "#606884")
        chute = _stone("cchute", "#D8CDB4", "#C6BBA2", "#8A8270", 0.5, 0.3)
        grassc, grass2c, waterc, roofc = "#3E6A52", "#345A48", "#2A5E7E", "#4A5A86"
    else:
        stone = _stone("cwall", "#B9AD98", "#A89C88", "#7E7464")
        stone2 = _stone("cwall2", "#C8BCA6", "#B9AD98", "#857B6A")
        chute = _stone("cchute", "#E6D9BC", "#D6C9AC", "#9A8E78", 0.5, 0.3)
        grassc, grass2c, waterc, roofc = "#7FAE52", "#6E9E4A", "#4E9AA8", "#5E6B8A"
    slate = mat("slate", roofc, rough=0.6, noise=0.2, bricks={"scale": 1, "c2": roofc, "mortar_c": "#2E3448", "w": 0.5, "h": 0.3, "mortar": 0.015, "k": 1})
    grass = mat("cgrass", grassc, rough=0.95, noise=0.3, scale=1.2)
    grass2 = mat("cgrass2", grass2c, rough=0.95, noise=0.3, scale=1.2)
    iron = mat("iron", "#2A1C1E", rough=0.5, metal=0.5)
    wood = mat("siegewood", "#8A6444" if not night else "#7A6458", rough=0.85, noise=0.3, scale=5)

    # ground: attackers' bank (z=0) with a sloping moat edge; castle side rises as a rocky mound
    def h(x, y):
        if y < -1.4:
            z = 0.0 + 0.25 * math.exp(-((y + 9) / 4) ** 2) * math.sin(x * 0.4)
            return z - max(0.0, (y + 2.6)) * 1.0
        if y < 3.4:
            return -1.6
        return -0.4
    terrain(h, -45, 45, -30, 6, 120, 90, grass)
    plane((0, 0.9, MZ), (90, 5.6), water_mat("moat" + variant, waterc, alpha=1.0, rough=0.05, wave=0.2, wave_scale=2.5))
    plane((0, 40, -0.45), (120, 70), grass2)
    for i in range(40):   # reeds and stones along the near moat edge
        x = R.uniform(-22, 22)
        if abs(x) < 1.6:
            continue
        if i % 3:
            grass_tuft(x, -1.9 + R.uniform(-0.2, 0.2), -0.25, R, grass2, 0.9, 5)
        else:
            rock((x, -1.75, -0.45), R.uniform(0.2, 0.45), stone2, R.random() * 3)
    for i in range(45):
        grass_tuft(R.uniform(-20, 20), R.uniform(-14, -2.8), 0.0, R, grass2, 0.4, 4)

    # curtain wall with battered plinth, string course, battlements, arrow slits
    box((0, WY + 1.25, (WZ - 1.6) / 2), (26, 2.5, WZ + 1.6), stone, 0.04)
    box((0, WY - 0.15, -0.2), (26, 0.9, 2.8), stone2, 0.12, (math.radians(-8), 0, 0))        # sloping plinth
    box((0, WY - 0.06, WZ - 0.25), (26, 0.3, 0.3), stone2, 0.06)
    box((0, WY + 0.1, WZ + 0.3), (26, 0.5, 0.6), stone, 0.04)
    _merlons_line(-12.0, 12.0, WY + 0.1, WZ + 0.6, stone, 0.5, 1.5, 0.85, 1.1)
    slit = mat("slitdark", "#1E1A1C", noise=0)
    for x in (-6.5, -3.4, 3.4, 6.5):
        box((x, WY - 0.02, 4.6), (0.14, 0.1, 1.2), slit, 0.02); box((x, WY - 0.02, 4.6), (0.5, 0.1, 0.14), slit, 0.02)
    # flanking towers, gatehouse far left, keep and inner towers behind
    _round_tower(-10.5, WY + 1.0, 2.7, -1.6, 12.5, stone, stone2, slate, night, ((0.0, 0.5), (0.0, 0.78), (0.5, 0.64)))
    _round_tower(10.5, WY + 1.0, 2.7, -1.6, 12.5, stone, stone2, slate, night, ((0.0, 0.5), (0.0, 0.78), (-0.5, 0.64)))
    box((2.5, 13, 9), (9, 7, 21), stone, 0.05)                                   # keep
    box((2.5, 9.45, 19.8), (9.4, 0.4, 0.5), stone2, 0.05)
    _merlons_line(-1.7, 6.7, 9.6, 19.5, stone, 0.5, 1.4, 0.8, 1.1)
    winm = mat("keepwin", "#FFC870", emit="#FFB050", emit_strength=5 if night else 0.0, noise=0) if night else slit
    for (x, z) in ((0.2, 13.0), (2.5, 13.0), (4.8, 13.0), (1.3, 16.4), (3.7, 16.4)):
        box((x, 9.46, z), (0.55, 0.12, 1.2), winm, 0.04)
        cyl((x, 9.46, z + 0.6), 0.275, 0.12, winm, verts=12, rot=(math.radians(90), 0, 0), bevel=0)
    _round_tower(-2.6, 10.2, 1.9, 0, 21.5, stone, stone2, slate, night, ((0.0, 0.7), (0.0, 0.86)))
    _round_tower(7.6, 10.2, 1.9, 0, 20.0, stone, stone2, slate, night, ((0.0, 0.72), (0.0, 0.88)))
    _round_tower(-7.0, 12.5, 2.0, 0, 15.5, stone, stone2, slate, False, ((0.0, 0.85),))
    for (x, y, z, c1, c2) in ((-10.5, WY + 1.0, 20.3, "#C0392B", "#FFC93C"), (10.5, WY + 1.0, 20.3, "#C0392B", "#FFC93C"), (2.5, 13, 20.6, "#C0392B", "#FFC93C")):
        _banner((x, y, z), c1, c2, 2.4, 1.3)

    # --- garderobe turret, corbelled out of the wall at x=0, and its chute down to the moat
    GZ0, GZ1, GY = 6.5, 8.7, 1.7
    cutc = mat("cutface", "#E8C99A", rough=0.9, noise=0.08)
    dark_in = mat("shaftin", "#3A3640" if night else "#4A4038", rough=0.95, noise=0.2)
    for k, x in enumerate((-0.72, 0.0, 0.72)):                                               # three stepped corbels
        for j in range(3):
            box((x, WY - 0.25 - j * 0.24, GZ0 - 0.2 - j * 0.3), (0.34, 0.5 + j * 0.0, 0.32), stone2, 0.05)
    box((0, (GY + WY) / 2, GZ0 + 0.06), (2.1, WY - GY + 0.1, 0.22), stone2, 0.04)             # floor slab
    if not cut:
        box((0, (GY + WY) / 2, (GZ0 + GZ1) / 2 + 0.1), (1.9, WY - GY, GZ1 - GZ0), chute, 0.05)
        sl = mat("slitlit", "#FFC870", emit="#FFB050", emit_strength=7, noise=0) if night else slit
        box((0, GY - 0.02, 7.75), (0.2, 0.1, 0.75), sl, 0.03)
        box((-0.96, GY + 0.7, 7.75), (0.1, 0.18, 0.6), sl, 0.03); box((0.96, GY + 0.7, 7.75), (0.1, 0.18, 0.6), sl, 0.03)
        if night:
            glow((0, GY - 0.12, 7.75), 0.9, "#FFB860", 1.6, 2.4)
    else:  # opened turret: side walls, back wall, stone seat with hole, window slit, hanging clothes, candle niche
        for sx in (-0.85, 0.85):
            box((sx, (GY + WY) / 2, (GZ0 + GZ1) / 2 + 0.1), (0.2, WY - GY, GZ1 - GZ0), chute, 0.03)
            box((sx, GY - 0.01, (GZ0 + GZ1) / 2 + 0.1), (0.2, 0.03, GZ1 - GZ0), cutc, 0)
        box((0, WY - 0.02, (GZ0 + GZ1) / 2 + 0.1), (1.5, 0.08, GZ1 - GZ0), mat("gback", "#C9BCA0", rough=0.9, noise=0.2, bricks={"scale": 1, "c2": "#BBAE92", "mortar_c": "#8A8270", "w": 0.5, "h": 0.3, "mortar": 0.015, "k": 1}), 0)
        box((0, GY + 0.55, GZ0 + 0.45), (1.5, 0.75, 0.55), stone2, 0.04)                       # seat bench
        box((0, GY + 0.55, GZ0 + 0.75), (1.52, 0.8, 0.07), mat("seatwood", "#9C6B3F", rough=0.7, noise=0.3, scale=5), 0.02)
        cyl((0, GY + 0.5, GZ0 + 0.79), 0.2, 0.03, mat("holedark", "#1A1614", noise=0), verts=20, bevel=0)
        box((0, GY - 0.01, GZ0 + 0.45), (1.5, 0.03, 0.55), cutc, 0)
        box((0, WY - 0.07, 7.95), (0.16, 0.05, 0.6), mat("skyslit", "#BFE3F4", emit="#BFE3F4", emit_strength=1.5, noise=0), 0.02)
        tube([(-0.7, WY - 0.12, 8.3), (0.7, WY - 0.12, 8.3)], 0.02, wood, smooth=False)        # clothes rail (the "moths" beat)
        for (x, c) in ((-0.5, "#B3262E"), (0.45, "#2E5A8C")):
            mesh("robe", [(x - 0.16, WY - 0.14, 8.28), (x + 0.16, WY - 0.14, 8.28), (x + 0.27, WY - 0.14, 7.5), (x - 0.27, WY - 0.14, 7.5)], [(0, 1, 2, 3)], mat("robe" + c, c, rough=0.9, noise=0.12))
        cyl((0.55, GY + 0.9, GZ0 + 0.9), 0.035, 0.2, mat("candle", "#FFF4E0", noise=0), verts=8)
        sphere((0.55, GY + 0.9, GZ0 + 1.04), 0.035, mat("flame", "#FFD27A", emit="#FFB84D", emit_strength=20, noise=0), sub=1)
        point((0.3, GY + 0.5, 8.0), "#FFD8A0", 30, 0.2)
    prism_roof((0, (GY + WY) / 2 - 0.05, GZ1 + 0.1), 1.9, WY - GY + 0.1, 0.95, slate, overhang=0.22)
    # chute shaft: lighter ashlar, clearly proud of the wall, quoins on the edges, dark outlet arch at the foot
    CY = 2.35
    CZ0 = 0.0
    if not cut:
        box((0, (CY + WY) / 2, (CZ0 + GZ0) / 2), (1.2, WY - CY, GZ0 - CZ0), chute, 0.05)
    else:
        for sx in (-0.5, 0.5):
            box((sx, (CY + WY) / 2, (CZ0 + GZ0) / 2), (0.2, WY - CY, GZ0 - CZ0), chute, 0.03)
            box((sx, CY - 0.01, (CZ0 + GZ0) / 2), (0.2, 0.03, GZ0 - CZ0), cutc, 0)
        box((0, WY - 0.04, (CZ0 + GZ0) / 2), (0.8, 0.06, GZ0 - CZ0), dark_in, 0)
        for z in (2.2, 2.45):                                                                   # later castles: iron bars across the shaft
            tube([(-0.4, CY + 0.4, z), (0.4, CY + 0.4, z)], 0.035, iron, smooth=False)
        for k in range(7):                                                                      # arrows: the way down
            zz = 5.6 - k * 0.75
            cyl((0, CY + 0.45, zz), 0.1, 0.22, mat("arrowy", "#FFC93C", emit="#FFC93C", emit_strength=1.0, noise=0), verts=3, rot=(math.radians(90), math.radians(180), 0), bevel=0)
    for k in range(9):                                                                          # quoins
        z = CZ0 + 0.45 + k * 0.7
        for sx in (-0.6, 0.6):
            box((sx, CY + 0.02, z), (0.22 if k % 2 else 0.34, 0.12, 0.3), stone2, 0.03)
    for sx in (-0.45, 0.45):                                                                    # outlet: two piers + arch + dark mouth
        box((sx, (CY + WY) / 2, -0.55), (0.32, WY - CY, 1.3), chute, 0.04)
    box((0, CY + 0.3, -0.35), (0.62, 0.4, 1.3), mat("outlet", "#141218", noise=0), 0)
    cyl((0, CY + 0.02, 0.3), 0.33, 0.5, mat("outlet", "#141218", noise=0), verts=16, rot=(math.radians(90), 0, 0), bevel=0)
    ring((0, CY - 0.02, 0.3), 0.38, 0.07, stone2, 1.0).rotation_euler = (math.radians(90), 0, 0)
    # raft with a ladder up into the outlet: the way in
    with Group((0.15, 1.35, MZ), (0, 0, 8)):
        for k in range(6):
            cyl((-0.75 + k * 0.3, 0, 0.06), 0.14, 2.0, wood, verts=8, rot=(math.radians(90), 0, 0))
        for sy in (-0.7, 0.7):
            box((0, sy, 0.2), (1.9, 0.12, 0.08), wood, 0.02)
        cyl((0.75, -0.6, 0.9), 0.03, 2.4, wood, verts=6, rot=(0.25, 0.3, 0))                    # pole
    with Group((0.0, 1.75, MZ + 0.2), (-24, 0, 0)):
        for sx in (-0.26, 0.26):
            box((sx, 0, 1.0), (0.07, 0.07, 2.3), wood, 0.01)
        for k in range(6):
            box((0, 0, 0.15 + k * 0.38), (0.52, 0.05, 0.05), wood, 0.005)
    # torches along the wall, wall-walk braziers
    for x in (-6.0, -2.6, 2.6, 6.0):
        torch_sconce((x, WY - 0.15, 6.0))
        if night:
            glow((x, WY - 0.3, 6.5), 1.1, "#FF9A40", 1.6, 2.4)
    # --- attackers' side: mantlets, stakes, siege ladders, tents, campfire, trebuchet silhouette, trees
    for (x, y, rz) in ((-4.2, -3.6, 12), (4.4, -3.9, -10), (-8.5, -4.6, 20)):
        with Group((x, y, 0), (0, 0, rz)):
            box((0, 0, 0.95), (1.9, 0.1, 1.9), wood, 0.03, (math.radians(-14), 0, 0))
            for sx in (-0.6, 0, 0.6):
                box((sx, -0.06, 0.95), (0.08, 0.06, 1.9), mat("siegedark", "#5A4636", rough=0.9, noise=0.2), 0.01, (math.radians(-14), 0, 0))
            cyl((0, 0.65, 0.6), 0.04, 1.6, wood, verts=6, rot=(math.radians(48), 0, 0))
    for k in range(9):
        x = -12 + k * 0.9
        cyl((x, -2.9, 0.5), 0.07, 1.4, wood, verts=6, r2=0.01, rot=(math.radians(-38), 0, 0))
    for k in range(7):
        x = 6.5 + k * 0.9
        cyl((x, -2.9, 0.5), 0.07, 1.4, wood, verts=6, r2=0.01, rot=(math.radians(-38), 0, 0))
    with Group((6.8, -6.2, 0.12), (0, 0, -30)):     # a siege ladder lying ready
        for sy in (-0.3, 0.3):
            box((0, sy, 0), (5.5, 0.08, 0.08), wood, 0.01)
        for k in range(13):
            box((-2.5 + k * 0.42, 0, 0), (0.05, 0.6, 0.05), wood, 0.005)
    _siege_tent((-9.5, -11, 0), 10, "#C0392B", "#FFF4E0")
    _siege_tent((9.0, -12.5, 0), 40, "#2E5A8C", "#FFF4E0")
    _siege_tent((-15, -16, 0), 0, "#FFC93C", "#FFF4E0")
    _siege_tent((15.5, -8, 0), 0, "#C0392B", "#FFF4E0")
    _banner((-7.6, -10.2, 0), "#2E5A8C", "#FFC93C", 3.2, 1.1)
    _banner((11, -11.5, 0), "#2E5A8C", "#FFC93C", 3.2, 1.1)
    if not cut:
        for (fx, fy) in ((-6.5, -8.2), (12.2, -10.0)):
            for k in range(8):
                a = k / 8 * math.tau
                rock((fx + 0.4 * math.cos(a), fy + 0.4 * math.sin(a), 0.06), 0.11, stone2, a, 0.75)
            flames(fx, fy, 0.05, 0.7, 5, None)
            if night:
                point((fx, fy - 0.2, 0.7), "#FF8A3C", 500, 0.25)
                glow((fx, fy - 0.3, 0.6), 1.6, "#FF9A40", 1.2, 2.6)
    leaf = "#2E6A56" if night else "#4E8A3E"
    for p in ((-17, -5, 1.5), (18.5, -3.5, 1.4), (-21, -13, 1.7), (21, -15, 1.6), (-14.5, 1.0 - 4.5, 1.1), (-26, -2, 1.8), (26, -6, 1.8)):
        tree((p[0], p[1], 0), p[2], leaf)
    # distant hills
    hill = mat("chill", "#2E4A6A" if night else "#8EB878", rough=1, noise=0.1)
    for (x, s) in ((-38, 20), (-12, 16), (20, 22), (46, 18)):
        sphere((x, 70, -2), s, hill, scale=(1.8, 0.5, 0.45), sub=3)

    if night:
        sky3([(0.0, "#3A5E9A"), (0.08, "#27467E"), (0.35, "#152A5C"), (1.0, "#0A1436")], 0.85)
        sun((52, 0, -140), "#A8C0FF", 3.0, 5)                    # moonlight from the upper right, raking the wall
        area((0, -14, 9), (62, 0, 0), 18, "#6E8EE0", 1500)       # soft blue fill
        moon((17, 80, 44), 3.4, 6.0, 4.5)
        stars(R, 170, 88, (-90, 90), (12, 80), 9)
        cm = mat("ncloud", "#4E6AA8", rough=1, emit="#4460A0", emit_strength=0.5, noise=0)
        for (x, z, s) in ((-30, 30, 6), (34, 26, 5), (-6, 52, 6), (48, 50, 5)):
            cloud((x, 84, z), s, cm, 4)
        point((0, GY - 0.6, 7.6), "#FFB060", 120, 0.2)
        point((0, 1.3, 1.2), "#9FB8FF", 60, 0.5)                 # lift the outlet and the ladder
    else:
        sky3([(0.0, "#FFE9C7"), (0.1, "#CFE8F4"), (0.4, "#8FD3F4"), (1.0, "#5EA8E0")], 1.0)
        sun((50, 0, -140), "#FFE2B8", 4.2, 3)
        area((0, -14, 9), (62, 0, 0), 18, "#FFF1D6", 500)
        cm = mat("dcloud", "#FFFFFF", rough=1, emit="#FFFFFF", emit_strength=0.8, noise=0)
        for (x, z, s) in ((-30, 30, 6), (34, 26, 5), (-6, 52, 6), (48, 50, 5)):
            cloud((x, 84, z), s, cm, 4)


# ---------------------------------------------------------------- brain graphic (lab posters, screens, cutaway_head)

BRAIN_OUT = [(1.0, 0.02), (0.97, 0.36), (0.78, 0.62), (0.45, 0.78), (0.05, 0.84), (-0.38, 0.78), (-0.74, 0.58), (-0.96, 0.28), (-1.0, -0.04),
             (-0.86, -0.26), (-0.56, -0.3), (-0.3, -0.26), (-0.05, -0.3), (0.3, -0.34), (0.62, -0.3), (0.86, -0.2)]
TEMPORAL = [(0.58, -0.1), (0.3, 0.0), (-0.1, -0.02), (-0.4, -0.12), (-0.5, -0.32), (-0.3, -0.5), (0.1, -0.56), (0.45, -0.5), (0.66, -0.34)]
CEREB = [(-0.42, -0.3), (-0.62, -0.26), (-0.86, -0.34), (-0.95, -0.52), (-0.84, -0.7), (-0.6, -0.76), (-0.4, -0.66), (-0.34, -0.48)]


def _scallop(pts, amp, k=5):
    pts = chaikin(pts, 3)
    cx = sum(p[0] for p in pts) / len(pts); cz = sum(p[1] for p in pts) / len(pts)
    out = []
    for i, (x, z) in enumerate(pts):
        f = 1.0 + amp * abs(math.sin(i / len(pts) * math.pi * k))
        out.append((cx + (x - cx) * f, cz + (z - cz) * f))
    return out


def brain(cx, cy, cz, s, depth=None, pink="#F7A8B8", fold="#E27E98", cereb="#C98AD8", stem="#F2C9A0", hi_cereb=False, emit=0.0, gyri=True):
    """Cartoon brain in side view, front towards +x, as layered relief facing the camera (-y).
    cx,cz = centre, s = half length, cy = y of the front faces. Returns nothing; ~1.9 s long, 1.6 s tall."""
    d = depth or 0.22 * s
    P = lambda pts: [(cx + x * s, cz + z * s) for x, z in pts]
    pm = mat("brainpink" + pink + str(emit), pink, rough=0.55, noise=0.06, emit=pink if emit else None, emit_strength=emit)
    fm = mat("brainfold" + fold + str(emit), fold, rough=0.55, noise=0, emit=fold if emit else None, emit_strength=emit)
    cm = mat("braincereb" + cereb + str(hi_cereb) + str(emit), cereb if not hi_cereb else "#FFC93C", rough=0.5, noise=0.05,
             emit=("#FFC93C" if hi_cereb else (cereb if emit else None)), emit_strength=(2.2 if hi_cereb else emit))
    sm = mat("brainstem" + stem + str(emit), stem, rough=0.6, noise=0.05, emit=stem if emit else None, emit_strength=emit)
    # brain stem first (furthest back), then cerebellum, cerebrum, temporal lobe on top
    tube([(cx - 0.2 * s, cy + d * 0.5, cz - 0.2 * s), (cx - 0.3 * s, cy + d * 0.5, cz - 0.6 * s), (cx - 0.36 * s, cy + d * 0.5, cz - 1.15 * s)], 0.13 * s, sm, radii=[1.0, 0.9, 0.6])
    poly(P(_scallop(CEREB, 0.05, 7)), cy + d * 0.2, d * 0.8, cm, bevel=0.03 * s)
    for k in range(4):       # cerebellum stripes
        z = cz + (-0.4 - k * 0.09) * s
        tube([(cx - 0.9 * s + 0.04 * k * s, cy + d * 0.18, z), (cx - 0.65 * s, cy + d * 0.16, z - 0.02 * s), (cx - 0.4 * s, cy + d * 0.18, z + 0.01 * s)], 0.012 * s,
             mat("cerebline" + str(hi_cereb), "#9A5CB0" if not hi_cereb else "#E08A1E", rough=0.6, noise=0))
    poly(P(_scallop(BRAIN_OUT, 0.035, 9)), cy, d, pm, bevel=0.05 * s)
    poly(P(_scallop(TEMPORAL, 0.03, 5)), cy - d * 0.22, d * 0.6, pm, bevel=0.04 * s)
    if gyri:
        yy = cy - 0.012 * s
        folds = [
            [(-0.82, 0.2), (-0.6, 0.42), (-0.35, 0.3), (-0.2, 0.55), (0.02, 0.4), (0.12, 0.68)],
            [(0.3, 0.7), (0.34, 0.45), (0.52, 0.5), (0.6, 0.3), (0.8, 0.34)],
            [(-0.85, -0.05), (-0.6, 0.08), (-0.42, -0.06), (-0.25, 0.12), (-0.05, 0.1)],
            [(0.1, 0.2), (0.3, 0.14), (0.45, 0.22), (0.62, 0.05), (0.85, 0.08)],
            [(-0.55, 0.62), (-0.42, 0.52), (-0.5, 0.4)],
            [(0.62, -0.08), (0.72, 0.1), (0.9, -0.02)],
            [(-0.02, 0.76), (-0.06, 0.6), (-0.2, 0.7)],
        ]
        for f in folds:
            tube([(cx + x * s, yy, cz + z * s) for x, z in f], 0.022 * s, fm)
        yt = cy - d * 0.22 - 0.012 * s
        for f in ([(-0.38, -0.3), (-0.15, -0.22), (0.1, -0.34), (0.35, -0.24), (0.52, -0.3)], [(-0.2, -0.44), (0.05, -0.46), (0.3, -0.4)]):
            tube([(cx + x * s, yt, cz + z * s) for x, z in f], 0.02 * s, fm)


# ---------------------------------------------------------------- lab (A-004 tickling)

def _plant(loc, s=1.0, potc="#FF6B5B"):
    x, y, z = loc
    cyl((x, y, z + 0.22 * s), 0.2 * s, 0.44 * s, mat("pot" + potc, potc, rough=0.5, noise=0.05), verts=16, r2=0.27 * s)
    cyl((x, y, z + 0.43 * s), 0.25 * s, 0.03 * s, mat("soil", "#5B3A29", noise=0.2), verts=16, bevel=0)
    lm = mat("plantleaf", "#4EAE6A", rough=0.5, noise=0.12); lm2 = mat("plantleaf2", "#3E9458", rough=0.5, noise=0.12)
    for k in range(9):
        a = k / 9 * math.tau + 0.3; t = 0.35 + 0.35 * ((k * 5) % 3) / 2
        L_ = (0.75 + 0.3 * ((k * 3) % 4) / 3) * s
        o = sphere((x + math.cos(a) * math.sin(t) * L_ * 0.5, y + math.sin(a) * math.sin(t) * L_ * 0.5, z + 0.45 * s + math.cos(t) * L_ * 0.5), L_ * 0.5, lm if k % 2 else lm2, scale=(0.24, 0.06, 1.0), sub=2)
        o.rotation_euler = (0, t, a)


def _robot_arm(base, feather=True):
    """Chunky friendly desktop robot arm; reaches towards +x and forward (-y). Base on the bench top."""
    bx, by, bz = base
    white = mat("robowhite", "#F6F8FA", rough=0.3, noise=0.03)
    coral = mat("robocoral", "#FF6B5B", rough=0.35, noise=0.03)
    dark = mat("robodark", "#33414E", rough=0.4, noise=0.03)
    teal = mat("roboteal", "#0F6B78", rough=0.4, noise=0.03)
    cyl((bx, by, bz + 0.05), 0.3, 0.1, dark, verts=28, bevel=0.02)
    cyl((bx, by, bz + 0.2), 0.22, 0.24, white, verts=28, bevel=0.04)
    ring((bx, by, bz + 0.2), 0.225, 0.02, coral, 1.0)
    sphere((bx + 0.2, by - 0.1, bz + 0.2), 0.03, mat("roboled", "#5EF2A8", emit="#5EF2A8", emit_strength=6, noise=0), sub=1)
    J1 = (bx, by, bz + 0.42)
    J2 = (bx + 0.12, by - 0.02, bz + 1.02)
    J3 = (bx + 0.66, by - 0.1, bz + 0.98)
    J4 = (bx + 0.82, by - 0.14, bz + 0.72)

    def link(a, b, r, m):
        from mathutils import Vector
        d = Vector(b) - Vector(a)
        o = cyl(tuple((Vector(a) + Vector(b)) / 2), r, d.length, m, verts=20, bevel=0.03)
        o.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    link(J1, J2, 0.1, white); link(J2, J3, 0.085, white); link(J3, J4, 0.065, white)
    for j, r in ((J1, 0.15), (J2, 0.14), (J3, 0.115)):
        sphere(j, r, coral, sub=3)
        cyl((j[0], j[1] - r * 0.9, j[2]), r * 0.5, 0.05, dark, verts=16, rot=(math.radians(90), 0, 0), bevel=0)
    sphere(J4, 0.085, teal, sub=3)
    # gripper holding a feather
    for sgn in (-1, 1):
        box((J4[0] + 0.03 + sgn * 0.05, J4[1] - 0.01, J4[2] - 0.13), (0.03, 0.06, 0.2), dark, 0.01, (0, sgn * 0.2, 0))
    if feather:
        fm = mat("feather", "#FFC93C", rough=0.6, noise=0.05, emit="#FFC93C", emit_strength=0.25)
        fm2 = mat("feather2", "#FFE28A", rough=0.6, noise=0.05, emit="#FFE28A", emit_strength=0.25)
        tip = (J4[0] + 0.42, J4[1] - 0.06, J4[2] - 0.42)
        tube([(J4[0] + 0.03, J4[1] - 0.01, J4[2] - 0.2), tip], 0.012, mat("quill", "#FFF4E0", noise=0), smooth=False)
        o = sphere((J4[0] + 0.27, J4[1] - 0.04, J4[2] - 0.34), 0.24, fm, scale=(1.0, 0.1, 0.36), sub=3); o.rotation_euler = (0, math.radians(45), 0)
        o = sphere((J4[0] + 0.29, J4[1] - 0.06, J4[2] - 0.35), 0.17, fm2, scale=(1.0, 0.1, 0.3), sub=3); o.rotation_euler = (0, math.radians(45), 0)
    # cable from the base to a control box
    tube([(bx - 0.25, by + 0.1, bz + 0.05), (bx - 0.5, by + 0.25, bz + 0.03), (bx - 0.75, by + 0.2, bz + 0.03), (bx - 0.95, by + 0.25, bz + 0.1)], 0.02, dark)
    box((bx - 1.1, by + 0.25, bz + 0.12), (0.4, 0.3, 0.24), teal, 0.03)
    for k, c in enumerate(("#5EF2A8", "#FFC93C", "#FF6B5B")):
        sphere((bx - 1.22 + k * 0.12, by + 0.09, bz + 0.16), 0.03, mat("led" + c, c, emit=c, emit_strength=5, noise=0), sub=1)
    cyl((bx - 1.1, by + 0.2, bz + 0.3), 0.012, 0.14, dark, verts=6, rot=(0.3, 0, 0))    # joystick
    sphere((bx - 1.1, by + 0.18, bz + 0.38), 0.035, coral, sub=2)


def _poster(x, y, z, w, hgt, bg, kind, frame="#FFF4E0"):
    box((x, y, z), (w + 0.1, 0.04, hgt + 0.1), mat("pframe" + frame, frame, rough=0.5, noise=0.03), 0.015)
    box((x, y - 0.025, z), (w, 0.02, hgt), mat("pbg" + bg, bg, rough=0.8, noise=0.04), 0)
    if kind == "brain":
        brain(x, y - 0.06, z + 0.08 * hgt, w * 0.36, depth=0.03)
        for k in range(3):
            box((x, y - 0.04, z - hgt * 0.36 - k * 0.07), (w * (0.7 - 0.15 * k), 0.01, 0.03), mat("pink_", "#0F6B78", noise=0), 0)
    elif kind == "neuron":
        nm = mat("neuron", "#FFC93C", rough=0.5, noise=0, emit="#FFC93C", emit_strength=0.4)
        c = (x - w * 0.18, y - 0.05, z + hgt * 0.15)
        sphere(c, w * 0.12, nm, scale=(1, 0.3, 1), sub=2)
        for k in range(7):
            a = k / 7 * math.tau + 0.4
            tube([c, (c[0] + math.cos(a) * w * 0.2, c[1], c[2] + math.sin(a) * w * 0.2), (c[0] + math.cos(a + 0.3) * w * 0.3, c[1], c[2] + math.sin(a + 0.3) * w * 0.3)], 0.014, nm)
        tube([c, (x + w * 0.05, y - 0.05, z - hgt * 0.05), (x + w * 0.2, y - 0.05, z - hgt * 0.28), (x + w * 0.32, y - 0.05, z - hgt * 0.34)], 0.022, nm)
        for k in range(3):
            sphere((x + w * (0.3 + 0.03 * k), y - 0.05, z - hgt * (0.3 + 0.05 * k)), 0.03, mat("syn", "#FF6B5B", emit="#FF6B5B", emit_strength=1.0, noise=0), sub=1)
    elif kind == "hand":
        hm = mat("handp", "#FFD9B0", rough=0.6, noise=0)
        box((x, y - 0.04, z - hgt * 0.1), (w * 0.34, 0.02, hgt * 0.3), hm, 0.04)
        for k in range(4):
            box((x - w * 0.13 + k * w * 0.087, y - 0.04, z + hgt * 0.17 + 0.03 * math.sin(k * 1.3 + 0.5)), (w * 0.07, 0.02, hgt * 0.26), hm, 0.03)
        box((x + w * 0.22, y - 0.04, z - hgt * 0.08), (w * 0.07, 0.02, hgt * 0.2), hm, 0.03, (0, math.radians(-35), 0))
        for k in range(3):
            tube([(x - w * 0.36, y - 0.05, z + hgt * (0.3 - k * 0.1)), (x - w * 0.3, y - 0.05, z + hgt * (0.34 - k * 0.1)), (x - w * 0.24, y - 0.05, z + hgt * (0.3 - k * 0.1))], 0.012, mat("zig", "#FF6B5B", noise=0))


def set_lab(variant="day"):
    R = random.Random(41)
    X0, X1, YB, H = -6.0, 6.0, 5.5, 4.2
    # floor: two-tone checker tiles; walls: mint upper, teal dado with a coral stripe
    floor = mat("labfloor", "#F4EFE4", rough=0.3, noise=0.05, bricks={"scale": 1, "c2": "#BFE3E0", "mortar_c": "#D8D2C4", "w": 0.8, "h": 0.8, "mortar": 0.012, "k": 1})
    plane((0, -2, 0), (X1 - X0, 16), floor)
    wall = mat("labwall", "#CDEEE6", rough=0.85, noise=0.04)
    dado = mat("labdado", "#1E8A92", rough=0.6, noise=0.05)
    coral = mat("labcoral", "#FF6B5B", rough=0.5, noise=0.03)
    cream = mat("labcream", "#FFF4E0", rough=0.5, noise=0.03)
    dark = mat("labdark", "#33414E", rough=0.4, noise=0.03)
    steel = mat("labsteel", "#DDE4EA", rough=0.25, metal=0.5, noise=0.03)
    woodm = mat("labwood", "#E0B078", rough=0.5, noise=0.2, scale=5)
    box((0, YB + 0.1, H / 2), (X1 - X0 + 0.4, 0.2, H), wall, 0)
    box((X0 - 0.1, -2, H / 2), (0.2, 16, H), wall, 0)
    box((X1 + 0.1, -2, H / 2), (0.2, 16, H), wall, 0)
    box((0, YB - 0.03, 0.6), (X1 - X0, 0.08, 1.2), dado, 0); box((0, YB - 0.05, 1.24), (X1 - X0, 0.1, 0.09), coral, 0.02)
    for xw in (X0 + 0.03, X1 - 0.03):
        box((xw, -2, 0.6), (0.08, 16, 1.2), dado, 0); box((xw, -2, 1.24), (0.1, 16, 0.09), coral, 0.02)
    box((0, YB - 0.05, 0.07), (X1 - X0, 0.1, 0.14), cream, 0.02)
    plane((0, -2, H), (X1 - X0, 16), mat("labceil", "#FFFFFF", rough=0.9, noise=0), rot=(math.pi, 0, 0))
    # hanging dome lamps
    for (x, y) in ((-2.6, 1.8), (1.0, 1.8), (4.4, 1.8), (-1, 4.2), (3, 4.2)):
        cyl((x, y, H - 0.4), 0.012, 0.8, dark, verts=5, bevel=0)
        cyl((x, y, H - 0.92), 0.36, 0.3, mat("lampshade", "#FFC93C", rough=0.4, noise=0.03), verts=24, r2=0.1)
        sphere((x, y, H - 1.08), 0.13, mat("bulb", "#FFF6E0", emit="#FFF2D0", emit_strength=14, noise=0), sub=2)
        point((x, y, H - 1.25), "#FFF2DA", 130, 0.3)

    # --- right wall: big window with sky, hills, blinds
    xr = X1 - 0.02
    box((xr, 2.2, 2.55), (0.06, 3.4, 2.1), mat("labsky", "#BFE8FF", emit="#BFE8FF", emit_strength=2.6, noise=0), 0)
    for (yy, zz, s, c) in ((1.4, 1.75, 0.9, "#8ED08A"), (2.9, 1.7, 1.2, "#6EBE7E")):
        sphere((xr - 0.02, yy, zz - 0.2), s, mat("hillw" + c, c, emit=c, emit_strength=1.2, noise=0), scale=(0.03, 1.2, 0.6), sub=2)
    sphere((xr - 0.03, 3.2, 3.15), 0.22, mat("sunw", "#FFF2B0", emit="#FFE890", emit_strength=6, noise=0), scale=(0.1, 1, 1), sub=2)
    for yy in (0.5, 2.2, 3.9):
        box((xr - 0.05, yy, 2.55), (0.1, 0.09, 2.2), cream, 0.02)
    for zz in (1.48, 2.55, 3.62):
        box((xr - 0.05, 2.2, zz), (0.1, 3.5, 0.09), cream, 0.02)
    box((xr - 0.12, 2.2, 1.42), (0.3, 3.6, 0.06), cream, 0.02)
    _plant((xr - 0.2, 1.2, 1.45), 0.45, "#FFC93C"); _plant((xr - 0.2, 3.3, 1.45), 0.38, "#FF6B5B")
    area((X1 - 0.5, 2.2, 2.6), (0, 90, 0), 3.0, "#FFF6E0", 700)
    # --- back wall: big brain screen, posters, clock, whiteboard, door
    box((0, YB - 0.06, 2.75), (3.5, 0.1, 2.1), dark, 0.05)
    box((0, YB - 0.12, 2.75), (3.3, 0.02, 1.9), mat("bigscreen", "#0E2A3E", rough=0.25, emit="#123E5A", emit_strength=1.6, noise=0), 0)
    brain(-0.45, YB - 0.2, 2.82, 0.78, depth=0.05, pink="#FF9EB6", fold="#E8708E", hi_cereb=True, emit=0.7)
    wvm = mat("wave", "#5EF2A8", emit="#5EF2A8", emit_strength=4, noise=0)
    for k in range(3):       # EEG traces + data bars beside the brain
        tube([(0.75 + i * 0.065, YB - 0.15, 3.35 - k * 0.3 + 0.09 * math.sin(i * (1.3 + k * 0.7)) * (1 if i % 5 else 2.2)) for i in range(13)], 0.014, wvm, smooth=False)
    for k in range(5):
        hh = 0.2 + 0.3 * abs(math.sin(k * 1.9 + 1))
        box((0.82 + k * 0.17, YB - 0.15, 2.0 + hh / 2), (0.1, 0.02, hh), mat("bar%d" % (k % 2), "#FFC93C" if k % 2 else "#FF6B5B", emit="#FFC93C" if k % 2 else "#FF6B5B", emit_strength=2.5, noise=0), 0)
    tube([(-1.02, YB - 0.2, 2.36), (-1.25, YB - 0.2, 2.1), (-1.0, YB - 0.2, 2.0)], 0.012, mat("lbl", "#FFC93C", emit="#FFC93C", emit_strength=3, noise=0), smooth=False)   # pointer to the cerebellum
    _poster(-3.4, YB - 0.04, 2.7, 1.5, 1.9, "#FFF4E0", "brain")
    _poster(3.2, YB - 0.04, 3.0, 1.3, 1.5, "#103A52", "neuron", "#FFC93C")
    _poster(4.85, YB - 0.04, 2.9, 1.1, 1.4, "#FFE2D8", "hand")
    cyl((-5.1, YB - 0.05, 3.3), 0.34, 0.06, cream, verts=28, rot=(math.radians(90), 0, 0))
    ring((-5.1, YB - 0.08, 3.3), 0.34, 0.03, coral, 1.0).rotation_euler = (math.radians(90), 0, 0)
    box((-5.1, YB - 0.1, 3.4), (0.03, 0.02, 0.22), dark, 0); box((-5.02, YB - 0.1, 3.3), (0.18, 0.02, 0.03), dark, 0)
    # --- back counter with sink, microscope, flasks, centrifuge; wall cabinets
    box((2.9, YB - 0.45, 0.45), (5.8, 0.8, 0.9), mat("cab", "#2A9AA2", rough=0.5, noise=0.04), 0.03)
    box((2.9, YB - 0.47, 0.93), (5.9, 0.9, 0.07), cream, 0.02)
    for k in range(6):
        box((0.5 + k * 0.96, YB - 0.87, 0.48), (0.84, 0.03, 0.68), mat("cabdoor", "#35AEB4", rough=0.5, noise=0.04), 0.02)
        box((0.5 + k * 0.96, YB - 0.9, 0.74), (0.22, 0.03, 0.035), steel, 0.01)
    fl = [("#5ED3B5", 0.6), ("#FF6B5B", 1.05), ("#FFC93C", 1.45), ("#8A6CF0", 1.9)]
    for c, x in fl:    # conical flasks with coloured liquid
        gm = mat("liq" + c, c, rough=0.08, emit=c, emit_strength=0.7, noise=0)
        cyl((x, YB - 0.5, 1.09), 0.13, 0.24, gm, verts=16, r2=0.04, bevel=0)
        cyl((x, YB - 0.5, 1.27), 0.04, 0.14, mat("glassw", "#E8F6FA", rough=0.05, noise=0), verts=12, bevel=0)
    with Group((2.9, YB - 0.5, 0.965)):      # microscope
        box((0, 0, 0.03), (0.34, 0.26, 0.06), dark, 0.02)
        box((0.0, 0.08, 0.25), (0.08, 0.08, 0.42), cream, 0.03)
        cyl((0.0, -0.03, 0.42), 0.045, 0.4, cream, verts=12, rot=(math.radians(-30), 0, 0))
        cyl((0.0, -0.13, 0.25), 0.035, 0.1, steel, verts=12, rot=(math.radians(-30), 0, 0))
        box((0, -0.03, 0.14), (0.24, 0.2, 0.025), steel, 0.005)
        cyl((0.07, 0.08, 0.2), 0.04, 0.05, coral, verts=12, rot=(0, math.radians(90), 0))
    cyl((4.0, YB - 0.5, 1.12), 0.26, 0.3, cream, verts=24, bevel=0.05)   # centrifuge
    cyl((4.0, YB - 0.5, 1.29), 0.2, 0.05, coral, verts=24)
    box((5.1, YB - 0.5, 0.975), (0.75, 0.5, 0.03), steel, 0.01)          # sink + tap
    tube([(5.1, YB - 0.2, 0.97), (5.1, YB - 0.2, 1.35), (5.1, YB - 0.42, 1.38), (5.1, YB - 0.45, 1.25)], 0.025, steel)
    # --- left wall: shelves with books, jars, a model head with EEG cap, cabinet
    xl = X0 + 0.02
    for zz in (1.75, 2.45, 3.15):
        box((xl + 0.22, 1.8, zz), (0.42, 4.2, 0.05), woodm, 0.01)
    for yy in (-0.3, 3.9):
        box((xl + 0.22, yy, 2.45), (0.42, 0.05, 1.6), woodm, 0.01)
    bookc = ["#FF6B5B", "#FFC93C", "#5ED3B5", "#2E5A8C", "#8A6CF0", "#FFF4E0", "#0F6B78", "#F28CC0"]
    yb = -0.2
    while yb < 1.6:
        t = R.uniform(0.07, 0.13); hh = R.uniform(0.34, 0.52); c = R.choice(bookc)
        box((xl + 0.22, yb + t / 2, 1.78 + hh / 2), (0.3, t, hh), mat("book" + c, c, rough=0.6, noise=0.04), 0.01, (R.uniform(-0.06, 0.06) if R.random() < 0.2 else 0, 0, 0))
        yb += t + 0.012
    for k, c in enumerate(("#5ED3B5", "#FFC93C", "#FF6B5B", "#8A6CF0", "#5ED3B5")):
        cyl((xl + 0.22, 2.0 + k * 0.4, 1.95), 0.13, 0.34, mat("jar" + c, c, rough=0.08, emit=c, emit_strength=0.5, noise=0), verts=14)
        cyl((xl + 0.22, 2.0 + k * 0.4, 2.14), 0.135, 0.04, cream, verts=14)
    yb = 1.5
    while yb < 3.7:
        t = R.uniform(0.07, 0.13); hh = R.uniform(0.34, 0.5); c = R.choice(bookc)
        box((xl + 0.22, yb + t / 2, 2.48 + hh / 2), (0.3, t, hh), mat("book" + c, c, rough=0.6, noise=0.04), 0.01)
        yb += t + 0.012
    with Group((xl + 0.25, 0.4, 2.48)):   # model head wearing an EEG cap (featureless mannequin)
        cyl((0, 0, 0.06), 0.08, 0.12, cream, verts=12)
        sphere((0, 0, 0.3), 0.19, cream, scale=(1, 1, 1.15), sub=3)
        sphere((0, 0, 0.36), 0.195, mat("eegcap", "#2E5A8C", rough=0.6, noise=0.03), scale=(1, 1, 0.9), sub=3)
        for k in range(7):
            a = k / 7 * math.tau
            sphere((0.16 * math.cos(a), 0.16 * math.sin(a), 0.44), 0.025, mat("eegdot", "#FFC93C", emit="#FFC93C", emit_strength=2, noise=0), sub=1)
    for k, c in enumerate(("#FFF4E0", "#FF6B5B", "#5ED3B5")):
        box((xl + 0.22, 0.2 + k * 0.5, 3.18 + 0.14), (0.3, 0.4, 0.26), mat("boxf" + c, c, rough=0.7, noise=0.05), 0.02)
    brain(xl + 0.16, 2.6, 3.5, 0.3, depth=0.1)
    _plant((xl + 0.25, 3.5, 3.18), 0.4, "#FFC93C")
    box((xl + 0.35, 4.6, 0.6), (0.7, 1.4, 1.2), mat("cab", "#2A9AA2", rough=0.5, noise=0.04), 0.03)
    box((xl + 0.35, 4.6, 1.22), (0.75, 1.45, 0.05), cream, 0.02)
    _plant((-5.2, 4.6, 1.25), 0.75, "#FF6B5B")

    # --- main bench (action zone): drawers, robot arm at (1.2,1.7), brain model under glass, laptop, clipboard, mug
    BY, BT = 1.7, 0.95
    box((0.3, BY, 0.44), (5.4, 0.9, 0.88), mat("benchbase", "#1E8A92", rough=0.5, noise=0.04), 0.04)
    box((0.3, BY, BT - 0.035), (5.7, 1.1, 0.07), cream, 0.025)
    for k in range(5):
        x = -2.0 + k * 1.08
        box((x, BY - 0.46, 0.62), (0.96, 0.03, 0.32), mat("drawer", "#2AA0A8", rough=0.5, noise=0.04), 0.02)
        box((x, BY - 0.46, 0.25), (0.96, 0.03, 0.34), mat("drawer", "#2AA0A8", rough=0.5, noise=0.04), 0.02)
        for zz in (0.62, 0.25):
            box((x, BY - 0.49, zz + 0.05), (0.3, 0.03, 0.035), cream, 0.01)
    box((0.3, BY - 0.4, 0.04), (5.3, 0.1, 0.08), dark, 0.01)
    _robot_arm((1.2, 1.7, BT))
    with Group((-0.9, 1.8, BT)):         # brain model on a stand under a glass dome
        cyl((0, 0, 0.03), 0.3, 0.06, woodm, verts=28, bevel=0.015)
        cyl((0, 0, 0.14), 0.02, 0.2, steel, verts=8)
        brain(0.0, -0.03, 0.44, 0.24, depth=0.07)
        o = sphere((0, 0, 0.38), 0.36, water_mat("dome", "#DFF6FF", alpha=0.16, rough=0.02), scale=(1, 1, 1.25), sub=3)
        o.visible_shadow = False
    with Group((-2.0, 1.75, BT), (0, 0, 14)):   # laptop showing a trace
        box((0, 0, 0.012), (0.52, 0.36, 0.024), steel, 0.008)
        box((0, 0.19, 0.19), (0.52, 0.02, 0.35), steel, 0.008, (math.radians(-12), 0, 0))
        box((0, 0.175, 0.19), (0.46, 0.01, 0.29), mat("lapscr", "#0E2A3E", emit="#1E6A8A", emit_strength=2.0, noise=0), 0, (math.radians(-12), 0, 0))
        tube([(-0.2 + i * 0.04, 0.165, 0.19 + 0.05 * math.sin(i * 1.7) * (2 if i % 4 == 0 else 1)) for i in range(11)], 0.006, wvm, smooth=False)
    cyl((0.25, 1.5, BT + 0.07), 0.055, 0.13, coral, verts=16)                      # mug
    ring((0.32, 1.5, BT + 0.07), 0.04, 0.012, coral, 1.0).rotation_euler = (math.radians(90), 0, 0)
    box((2.55, 1.55, BT + 0.012), (0.3, 0.4, 0.02), woodm, 0.005, (0, 0, 0.25))     # clipboard
    box((2.55, 1.55, BT + 0.024), (0.26, 0.34, 0.006), mat("paper", "#FFFFFF", noise=0), 0, (0, 0, 0.25))
    for k, c in enumerate(("#5ED3B5", "#8A6CF0")):                                  # test tubes in a rack
        cyl((-0.15 - k * 0.1, 2.05, BT + 0.12), 0.025, 0.22, mat("liq" + c, c, rough=0.08, emit=c, emit_strength=0.7, noise=0), verts=10, bevel=0)
    box((-0.2, 2.05, BT + 0.06), (0.3, 0.1, 0.03), woodm, 0.005)
    # arm rest + screen divider used in the experiment (hand goes under the feather)
    box((2.0, 1.45, BT + 0.03), (0.5, 0.3, 0.06), mat("pad", "#33414E", rough=0.8, noise=0.05), 0.025)
    # stools, rolling cart, floor rug, bin
    for (x, y, c) in ((-1.6, 0.55, "#FF6B5B"), (2.6, 0.5, "#FFC93C")):
        cyl((x, y, 0.36), 0.035, 0.66, steel, verts=10)
        cyl((x, y, 0.03), 0.26, 0.04, steel, verts=20)
        ring((x, y, 0.28), 0.2, 0.014, steel, 1.0)
        cyl((x, y, 0.72), 0.24, 0.09, mat("stool" + c, c, rough=0.5, noise=0.04), verts=24, bevel=0.03)
    with Group((-4.2, 0.9, 0), (0, 0, 18)):   # equipment cart with an oscilloscope
        for zz in (0.25, 0.85):
            box((0, 0, zz), (0.9, 0.6, 0.04), steel, 0.01)
        for sx in (-0.42, 0.42):
            for sy in (-0.27, 0.27):
                cyl((sx, sy, 0.45), 0.02, 0.85, steel, verts=6)
                sphere((sx, sy, 0.04), 0.04, dark, sub=1)
        box((0, 0, 1.08), (0.6, 0.4, 0.42), cream, 0.04)
        box((-0.08, -0.205, 1.1), (0.34, 0.01, 0.26), mat("oscscr", "#0E3A2E", emit="#1E7A5A", emit_strength=2.0, noise=0), 0)
        tube([(-0.22 + i * 0.03, -0.215, 1.1 + 0.07 * math.sin(i * 0.9)) for i in range(10)], 0.007, wvm)
        for k in range(3):
            cyl((0.2, -0.21, 1.2 - k * 0.1), 0.028, 0.03, dark, verts=10, rot=(math.radians(90), 0, 0))
        box((0, 0, 0.36), (0.5, 0.36, 0.18), mat("boxf#5ED3B5", "#5ED3B5", rough=0.7, noise=0.05), 0.02)
    box((0.4, -0.6, 0.008), (5.0, 2.4, 0.016), mat("rug", "#FFE2A8", rough=0.95, noise=0.1), 0.0)
    box((0.4, -0.6, 0.012), (4.6, 2.0, 0.016), mat("rug2", "#FFB8A0", rough=0.95, noise=0.1), 0.0)
    cyl((4.9, 1.0, 0.25), 0.2, 0.5, dark, verts=16, r2=0.24)
    _plant((5.2, -0.2, 0), 1.1, "#FFF4E0")
    # light: bright, soft, cheerful
    world("#EAF6FA", "#FFFFFF", 0.55)
    area((0.5, -4.5, 3.6), (62, 0, 0), 8, "#FFF8EE", 900)
    area((0, 1.5, 4.1), (0, 0, 0), 7, "#FFFFFF", 500)
    area((-5.2, 0, 2.6), (0, -80, 0), 3, "#E0F4FF", 260)


sets.BUILDERS.update({"marsh": set_marsh, "arctic": set_arctic, "castle": set_castle, "lab": set_lab})
