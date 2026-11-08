import sys
sys.path.insert(0, "/home/user/truewhys/lib")
import bpy, sets, sets2
from mathutils import Vector
for name, (sid, var, pos, tgt, lens) in {
    "THUMB_BACKYARD": ("backyard", "night", [0.4, -2.6, 1.3], [-0.6, 3.4, 1.2], 26),
    "THUMB_FAIR": ("fair", "day", [0.3, -3.2, 1.6], [0.2, 4.0, 2.2], 26)}.items():
    cam = sets.build(sid, var); sets.setup_render(1280, 720, 96)
    cam.location = pos; cam.rotation_euler = (Vector(tgt) - Vector(pos)).to_track_quat("-Z", "Y").to_euler(); cam.data.lens = lens
    bpy.context.scene.render.filepath = f"/tmp/claude-0/thumbplates/{name}.png"
    bpy.ops.render.render(write_still=True); print("OK", name, flush=True)
