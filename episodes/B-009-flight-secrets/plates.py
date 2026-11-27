"""B-009 Style T background plates (3D toon sets from lib/sets9.py). Static plates; the compositor (make.py) adds 2D camera moves,
the 2D cast and graphics. Layered sets render a *_bg plate (without the foreground) and a *_fg plate (foreground only, transparent PNG).
Local animatic quality:  /opt/c3d/bin/python episodes/B-009-flight-secrets/plates.py plates_lo 960 540 32
Kaggle final (GPU):      blender -b --python plates.py -- <out_dir> 1920 1080 128 --gpu [--only key1,key2]
"""
import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(HERE, "..", "..", "lib"), HERE):
    if os.path.isdir(p):
        sys.path.insert(0, p)

PLATES = {
    # key: (set, variant, (pos, tgt, lens))
    "row_night_bg": ("cabin", "night_bg", ((-0.95, 3.8, 1.62), (-0.95, 2.2, 1.02), 26)),
    "row_night_fg": ("cabin", "night_fg", ((-0.95, 3.8, 1.62), (-0.95, 2.2, 1.02), 26)),
    "row_dim_bg": ("cabin", "dim_bg", ((-0.95, 3.8, 1.62), (-0.95, 2.2, 1.02), 26)),
    "row_dim_fg": ("cabin", "dim_fg", ((-0.95, 3.8, 1.62), (-0.95, 2.2, 1.02), 26)),
    "row_day_bg": ("cabin", "day_bg", ((-0.95, 3.8, 1.62), (-0.95, 2.2, 1.02), 26)),
    "row_day_fg": ("cabin", "day_fg", ((-0.95, 3.8, 1.62), (-0.95, 2.2, 1.02), 26)),
    "aisle_day": ("cabin", "day", ((0, -1.4, 1.55), (0, 9, 1.25), 22)),
    "aisle_night": ("cabin", "night", ((0, -1.4, 1.55), (0, 9, 1.25), 22)),
    "aisle_dim": ("cabin", "dim", ((0, -1.4, 1.55), (0, 9, 1.25), 22)),
    "porthole": ("porthole", "day", ((0, -2.2, 0), (0, 0, 0), 40)),
    "cockpit_dusk_bg": ("cockpit", "dusk_bg", ((0, 1.35, 1.2), (0, -0.4, 1.05), 24)),
    "cockpit_dusk_fg": ("cockpit", "dusk_fg", ((0, 1.35, 1.2), (0, -0.4, 1.05), 24)),
    "cockpit_day_bg": ("cockpit", "day_bg", ((0, 1.35, 1.2), (0, -0.4, 1.05), 24)),
    "cockpit_day_fg": ("cockpit", "day_fg", ((0, 1.35, 1.2), (0, -0.4, 1.05), 24)),
    "apron": ("apron", "day", ((2, 2, 62), (2, 2.1, 0), 30)),
    "sky_clouds": ("skyplane", "clouds", ((38, 40, 6), (0, 0, 0), 35)),
    "sky_ocean": ("skyplane", "ocean", ((38, 40, 6), (0, 0, 0), 35)),
    "sky_night": ("skyplane", "night", ((38, 40, 6), (0, 0, 0), 35)),
    "hangar": ("hangar", "night", ((22, 48, 9), (0, 0, 4), 26)),
    "chamber": ("chamber", "day", ((0, -9, 2.2), (0, 0, 1.9), 30)),
    "harbor": ("harbor", "day", ((-1, 0, 38), (-1, 0.1, 0), 30)),
    "doorway": ("doorway", "day", ((-1.4, -6, 1.6), (-0.6, 0, 1.3), 32)),
}


def render(out, W, H, spp, gpu=False, only=None):
    import bpy
    from mathutils import Vector
    import sets, sets9  # noqa
    os.makedirs(out, exist_ok=True)
    for key, (set_id, variant, (pos, tgt, lens)) in PLATES.items():
        if only and key not in only:
            continue
        dst = os.path.join(out, key + ".png")
        if os.path.exists(dst):
            continue
        t0 = time.time()
        cam = sets.build(set_id, variant)
        sets.setup_render(W, H, spp, gpu)
        if variant.endswith("_fg"):
            bpy.context.scene.render.film_transparent = True
            bpy.context.scene.render.image_settings.color_mode = "RGBA"
        cam.location = pos
        cam.rotation_euler = (Vector(tgt) - Vector(pos)).to_track_quat("-Z", "Y").to_euler()
        cam.data.lens = lens
        bpy.context.scene.render.filepath = dst
        bpy.ops.render.render(write_still=True)
        print(f"PLATE {key} {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    out, W, H, spp = args[0], int(args[1]), int(args[2]), int(args[3])
    only = None
    if "--only" in args:
        only = set(args[args.index("--only") + 1].split(","))
    if not os.path.isabs(out):
        out = os.path.join(HERE, out)
    render(out, W, H, spp, gpu="--gpu" in args, only=only)
