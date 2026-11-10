"""Realistic right hand + forearm gripping a bar, for Style R close-ups.

Mesh: "First Person hands rigged" by David Fischer (Sketchfab, CC BY 4.0), library/models/hand_fp/.
We pose the rig's fingers into a grip, bake the right arm to a static mesh, give it our own skin
material and return it aligned so that the gripped bar runs along local X through the origin:
  local +X = index -> little finger, local +Y = back of the hand (dorsal), local -Z... see build_hand().
"""
import math, os
import bpy, bmesh
from mathutils import Vector, Matrix
import sr_common as C

_HERE = os.path.dirname(os.path.abspath(__file__))
GLB = "first_person_hands_rigged.glb"


def find_glb():
    cands = [os.path.join(_HERE, GLB),
             os.path.join(_HERE, "..", "..", "library", "models", "hand_fp", GLB),
             os.path.join(os.environ.get("TW_ASSETS", ""), GLB)]
    for c in cands:
        if os.path.exists(c):
            return os.path.abspath(c)
    import glob
    g = glob.glob("/kaggle/input/**/" + GLB, recursive=True)
    if g:
        return g[0]
    raise FileNotFoundError(GLB)


def skin_mat():
    m = C.pbr("skin", "#C9906F", rough=0.46, bump="cells", bscale=1400.0, bstr=0.12, cvar=0.10, cscale=40.0,
              sss=0.28, sss_radius=(1.0, 0.36, 0.2), sss_scale=0.008)
    return m


def build_hand(curl=(62, 78, 48), thumb=(18, 28, 30), spread=0.0):
    """Returns an Empty 'hand'. In its local frame the gripped bar is the X axis through the origin,
    the fingers wrap around it, the back of the hand faces local +Z and the wrist/forearm leave towards -Y."""
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=find_glb())
    new = [o for o in bpy.data.objects if o not in before]
    arm = [o for o in new if o.type == "ARMATURE"][0]
    for pb in arm.pose.bones:
        n = pb.name
        if ".R" not in n:
            continue
        pb.rotation_mode = "XYZ"
        for j in (1, 2, 3):
            if n.startswith("f_") and f".0{j}." in n:
                pb.rotation_euler = (math.radians(curl[j - 1]), 0, 0)
            if n.startswith("thumb") and f".0{j}." in n:
                pb.rotation_euler = (math.radians(thumb[j - 1]), 0, math.radians(-10 if j == 1 else 0))
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    mw = arm.matrix_world

    def head(prefix):
        for pb in arm.pose.bones:
            if pb.name.startswith(prefix):
                return mw @ pb.head
        raise KeyError(prefix)
    kn = {f: head(f"f_{f}.01.R") for f in ("index", "middle", "ring", "pinky")}
    j2 = {f: head(f"f_{f}.02.R") for f in kn}
    j3 = {f: head(f"f_{f}.03.R") for f in kn}
    wrist = head("hand.R")
    mean = lambda d: sum(d.values(), Vector()) / len(d)
    K, J2, J3 = mean(kn), mean(j2), mean(j3)
    ax = (kn["pinky"] - kn["index"]).normalized()           # along the bar
    fwd = (K - wrist); fwd = (fwd - ax * fwd.dot(ax)).normalized()
    palm = (J3 - K); palm = (palm - ax * palm.dot(ax))
    dors = ax.cross(fwd).normalized()
    if dors.dot(palm) > 0:
        dors = -dors
    # grip centre: inside the curl of the fingers
    cen = (K + J2 + J3) / 3.0 - dors * 0.0
    cen = cen + (kn["index"] - K).dot(ax) * 0 * ax
    # bake meshes (right arm only)
    parts = []
    skin = skin_mat()
    nail = C.pbr("nail", "#E2B9A6", rough=0.22, coat=0.4)
    for o in new:
        if o.type != "MESH" or len(o.data.vertices) < 100:
            continue
        ev = o.evaluated_get(dg)
        me = bpy.data.meshes.new_from_object(ev)
        me.transform(o.matrix_world)
        bm = bmesh.new(); bm.from_mesh(me)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.x > 0], context="VERTS")
        bm.to_mesh(me); bm.free()
        me.materials.clear()
        me.materials.append(nail if len(o.data.vertices) < 1000 else skin)
        for p in me.polygons:
            p.use_smooth = True
        parts.append(me)
    for o in new:
        bpy.data.objects.remove(o, do_unlink=True)
    # model space -> grip space (bar = X, dorsal = +Z, forward (wrist->knuckles) = +Y), centimetres -> metres
    y = fwd; z = ax.cross(y).normalized()
    if z.dot(dors) < 0:
        ax = -ax; z = ax.cross(y).normalized()
    R = Matrix((ax, y, z)).to_4x4()          # rows = new basis
    T = Matrix.Scale(0.01, 4) @ R @ Matrix.Translation(-cen)
    root = C.empty("hand")
    for i, me in enumerate(parts):
        me.transform(T)
        if T.determinant() < 0:
            me.flip_normals()
        o = bpy.data.objects.new(f"hand_mesh{i}", me)
        C.link(o, root)
        s = o.modifiers.new("sub", "SUBSURF"); s.levels = 2; s.render_levels = 2
    return root
