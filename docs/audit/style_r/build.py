"""Build one stylised close-to-human character with MPFB (CC0 assets) and render a still.
usage: python build.py <spec.json> <out.png> [samples]"""
import bpy, sys, json, os, math
spec = json.load(open(sys.argv[1])); out = sys.argv[2]; SAMPLES = int(sys.argv[3]) if len(sys.argv) > 3 else 32
A = spec["assets"]
import addon_utils
addon_utils.enable("bl_ext.user_default.mpfb", default_set=True)
from bl_ext.user_default.mpfb.services.humanservice import HumanService
from bl_ext.user_default.mpfb.services.targetservice import TargetService
from bl_ext.user_default.mpfb.services.locationservice import LocationService
bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("bl_ext.user_default.mpfb", default_set=True)
macro = TargetService.get_default_macro_info_dict()
macro.update({k: v for k, v in spec["macro"].items() if k != "race"})
macro["race"] = spec["macro"].get("race", {"asian": 0.0, "caucasian": 1.0, "african": 0.0})
human = HumanService.create_human(macro_detail_dict=macro)
tdir = os.path.join(LocationService.get_mpfb_data("targets"))
for t, w in spec.get("targets", {}).items():
    TargetService.load_target(human, os.path.join(tdir, t + ".target.gz"), weight=w, name=t.replace("/", "_"))
# rig + relax the arms from A-pose
HumanService.add_builtin_rig(human, "default")
rig = human.parent
if rig:
    bpy.context.view_layer.objects.active = rig; bpy.ops.object.mode_set(mode="POSE")
    for side, sgn in (("l", 1), ("r", -1)):
        for bn, ang in ((f"upperarm01.{side.upper()}", 0), (f"shoulder01.{side.upper()}", 0)):
            pass
    for b in rig.pose.bones:
        b.rotation_mode = "XYZ"
    for name, rot in spec.get("pose", {}).items():
        if name in rig.pose.bones:
            rig.pose.bones[name].rotation_euler = [math.radians(a) for a in rot]
    bpy.ops.object.mode_set(mode="OBJECT")
def mat(name, rgb, rough=0.55, sss=0.0, sheen=0.0, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*rgb, 1); p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    if sss:
        p.inputs["Subsurface Weight"].default_value = sss; p.inputs["Subsurface Radius"].default_value = (1.0, 0.35, 0.2); p.inputs["Subsurface Scale"].default_value = 0.012
    if sheen: p.inputs["Sheen Weight"].default_value = sheen
    return m
def srgb(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)
dg0 = bpy.context.evaluated_depsgraph_get(); ev0 = human.evaluated_get(dg0); m0 = ev0.to_mesh()
H = max((ev0.matrix_world @ v.co).z for v in m0.vertices); ev0.to_mesh_clear()
skin = mat("skin", srgb(spec["skin"]), 0.48, sss=0.12)
human.data.materials.clear(); human.data.materials.append(skin)
for i, p in enumerate(human.data.polygons): p.material_index = 0
objs = []
for kind, rel, colour in spec["parts"]:
    f = os.path.join(A, rel)
    if not os.path.exists(f) or (kind in ("Hair", "Eyebrows", "Eyelashes") and not any(x.endswith(".png") for x in os.listdir(os.path.dirname(f)))):
        print("MISSING", rel); continue
    before = set(bpy.data.objects)
    try:
        HumanService.add_mhclo_asset(f, human, asset_type=kind, subdiv_levels=1, material_type="PROCEDURAL_EYES" if kind == "Eyes" else "MAKESKIN")
    except Exception as e:
        print("ASSET ERR", rel, e); continue
    new = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
    for o in new:
        if kind != "Eyes":
            o.data.materials.clear()
            if "|" in colour:
                top_c, bot_c, _zs = colour.split("|")
                mt, mb = mat(rel + "_top", srgb(top_c), 0.72, sheen=0.3), mat(rel + "_bot", srgb(bot_c), 0.72, sheen=0.3)
                o.data.materials.append(mt); o.data.materials.append(mb)
                import bmesh as _bm
                bm = _bm.new(); bm.from_mesh(o.data); bm.faces.ensure_lookup_table()
                seen = set()
                for f0 in bm.faces:
                    if f0.index in seen: continue
                    isl, stack = [], [f0]; seen.add(f0.index)
                    while stack:
                        f1 = stack.pop(); isl.append(f1)
                        for e in f1.edges:
                            for f2 in e.link_faces:
                                if f2.index not in seen: seen.add(f2.index); stack.append(f2)
                    zc = sum(v.co.z for f1 in isl for v in f1.verts) / sum(len(f1.verts) for f1 in isl)
                    zc = (o.matrix_world @ __import__("mathutils").Vector((0, 0, zc))).z
                    for f1 in isl: f1.material_index = 0 if zc > 0.5 * H else 1
                bm.to_mesh(o.data); bm.free()
            elif kind in ("Hair", "Eyebrows", "Eyelashes"):
                m = mat(rel, srgb(colour), 0.45); nt = m.node_tree; P = nt.nodes["Principled BSDF"]
                png = [os.path.join(os.path.dirname(f), x) for x in os.listdir(os.path.dirname(f)) if x.endswith(".png")]
                if png:
                    tx = nt.nodes.new("ShaderNodeTexImage"); tx.image = bpy.data.images.load(png[0]); nt.links.new(tx.outputs["Alpha"], P.inputs["Alpha"])
                    try: m.blend_method = "HASHED"
                    except Exception: pass
                o.data.materials.append(m)
            else:
                o.data.materials.append(mat(rel, srgb(colour), 0.72, sheen=0.3))
        objs.append(o)
# smooth shading everywhere
for o in [human] + objs:
    for p in o.data.polygons: p.use_smooth = True
# studio: one-colour curved backdrop (cyc) + key/fill/rim aimed at the character
import bmesh
prof=[(-12,0)]+[(2+3*math.sin(math.radians(a)),3-3*math.cos(math.radians(a))) for a in range(0,91,6)]+[(5,14)]
me=bpy.data.meshes.new("cyc"); bm=bmesh.new()
rows=[[bm.verts.new((x,y,z)) for (y,z) in prof] for x in (-15,15)]
for i in range(len(prof)-1): bm.faces.new((rows[0][i],rows[0][i+1],rows[1][i+1],rows[1][i]))
bm.to_mesh(me); cyc=bpy.data.objects.new("cyc",me); bpy.context.collection.objects.link(cyc)
for p in me.polygons: p.use_smooth=True
cyc.data.materials.append(mat("bg", srgb(spec.get("bg", "#0F6B78")), 0.85))
bpy.ops.object.empty_add(location=(0,0,0.95)); tgt=bpy.context.object
def light(loc, energy, size, rgb=(1,1,1)):
    bpy.ops.object.light_add(type="AREA", location=loc); L=bpy.context.object; L.data.energy=energy; L.data.color=rgb; L.data.size=size
    c=L.constraints.new("TRACK_TO"); c.target=tgt; c.track_axis="TRACK_NEGATIVE_Z"; c.up_axis="UP_Y"
light((-2.4,-3.2,3.0), spec.get("key_light",420), 3.0, (1,0.96,0.9)); light((3.0,-2.6,1.4), 140, 4, (0.86,0.92,1)); light((1.8,2.2,3.0), 380, 1.6, (1,0.88,0.78)); light((-1.8,2.0,2.6), 220, 1.6, (0.8,0.9,1))
world = bpy.data.worlds.new("w"); bpy.context.scene.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (*srgb(spec.get("bg", "#0F6B78")), 1); world.node_tree.nodes["Background"].inputs[1].default_value = 0.4
# camera framing
dg = bpy.context.evaluated_depsgraph_get(); ev = human.evaluated_get(dg); me_ev = ev.to_mesh()
zs = [(ev.matrix_world @ v.co).z for v in me_ev.vertices]; top = max(zs); ev.to_mesh_clear()
eye_z = None
for o in objs:
    if "high-poly" in o.name.lower() or "low-poly" in o.name.lower():
        e2 = o.evaluated_get(dg); m2 = e2.to_mesh(); eye_z = sum((e2.matrix_world @ v.co).z for v in m2.vertices) / max(len(m2.vertices), 1); e2.to_mesh_clear(); break
cam_d = spec.get("cam", {})
# badge or extra simple props: [["sphere"|"disc", [x,y,z], size, "#hex"]]
def front_y(x, z):
    best = None
    for o in [human] + objs:
        e = o.evaluated_get(dg); mm = e.to_mesh()
        for v in mm.vertices:
            w = e.matrix_world @ v.co
            if abs(w.x - x) < 0.025 and abs(w.z - z) < 0.025 and (best is None or w.y < best): best = w.y
        e.to_mesh_clear()
    return best if best is not None else -0.12
for kind_, loc_, size_, col_ in spec.get("props", []):
    loc_ = list(loc_); loc_[2] = loc_[2] * top if loc_[2] <= 1.0 else loc_[2]
    if loc_[1] is None: loc_[1] = front_y(loc_[0], loc_[2]) - size_ * 0.12
    if kind_ == "disc":
        bpy.ops.mesh.primitive_cylinder_add(radius=size_, depth=size_ * 0.25, location=loc_, rotation=(math.radians(90), 0, 0))
    else:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=size_, location=loc_)
    pr = bpy.context.object; pr.data.materials.append(mat("prop", srgb(col_), 0.35))
    for p in pr.data.polygons: p.use_smooth = True
mode = cam_d.get("mode", "full")
bpy.ops.object.camera_add(); cam = bpy.context.object; bpy.context.scene.camera = cam
cam.data.lens = 85
if mode == "full":
    tz = top * 0.52; dist = top * 3.3
else:  # head and shoulders
    tz = (eye_z if eye_z else top * 0.93) - 0.06; dist = top * 0.95
cam.location = (cam_d.get("x", 0.0), -dist, tz); cam.rotation_euler = (math.radians(90), 0, 0)
if cam_d.get("yaw"):
    a = math.radians(cam_d["yaw"]); cam.location = (math.sin(a) * dist, -math.cos(a) * dist, tz); cam.rotation_euler = (math.radians(90), 0, a)
sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = cam_d.get("res", (600, 1000)); sc.render.filepath = out
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "Medium High Contrast"; sc.view_settings.exposure = -0.35
bpy.ops.render.render(write_still=True)
print("DONE", out, "top", round(top, 3), "eye", eye_z)
