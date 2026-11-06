"""More reusable toon sets (added for B-002). Registered into sets.BUILDERS on import.
palace (day/night) · yard (tannery/fullers) · fair (day) · backyard (night) · cottage (wake/tavern/stable)
All coordinates: floor at z=0, camera usually looks towards +y."""
import math, random
import sets
from sets import mat, box, cyl, sphere, plane, prism_roof, world, sun, area, point, tree, lantern, barrel, crate, bunting, house, sign, torch_sconce

R = random.Random(7)


def flames(cx, cy, z, w=1.0, n=7, light=None):
    """Toon fire: layered tapered tongues (orange outside, yellow inside) instead of blobs."""
    for k in range(n):
        x = cx + (k - (n - 1) / 2) * 0.16 * w
        h = (0.35 + 0.35 * math.sin(k * 2.3) ** 2) * w
        cyl((x, cy, z + h / 2), 0.11 * w, h, mat("fireO", "#FF7A2C", emit="#FF6A1C", emit_strength=10), verts=8, r2=0.01)
        cyl((x, cy - 0.05, z + h * 0.35), 0.06 * w, h * 0.65, mat("fireY", "#FFD24A", emit="#FFC23A", emit_strength=14), verts=8, r2=0.005)
    if light:
        point((cx, cy - 0.5, z + 0.4), "#FF8A3C", light, 0.3)


def candle(p, h=0.25, light=True, e=30):
    cyl((p[0], p[1], p[2] + h / 2), 0.045, h, mat("candle", "#FFF4E0"))
    sphere((p[0], p[1], p[2] + h + 0.04), 0.035, mat("flame", "#FFD27A", emit="#FFB84D", emit_strength=20))
    if light:
        point((p[0], p[1] - 0.1, p[2] + h + 0.1), "#FFB060", e, 0.05)


def panel_wall(x0, x1, y, h, base="#7A4A2B", rim="#5B3A29", rot=False):
    """Tudor oak panelling: a dark backing with raised panels in a grid."""
    w = x1 - x0
    if not rot:
        box(((x0 + x1) / 2, y, h / 2), (w, 0.3, h), mat("oakback", rim, noise=0.2), 0.02)
    else:
        box((y, (x0 + x1) / 2, h / 2), (0.3, w, h), mat("oakback", rim, noise=0.2), 0.02)
    n = max(1, int(w / 0.9))
    pw = w / n
    for i in range(n):
        for j, (z0, z1) in enumerate(((0.25, 1.05), (1.2, 2.6))):
            c = (x0 + pw * (i + 0.5), (z0 + z1) / 2)
            if not rot:
                box((c[0], y - 0.17, c[1]), (pw * 0.78, 0.06, z1 - z0), mat("oakpanel", base, noise=0.25, rough=0.5), 0.03)
            else:
                s = -1 if y > 0 else 1
                box((y + 0.17 * s, c[0], c[1]), (0.06, pw * 0.78, z1 - z0), mat("oakpanel", base, noise=0.25, rough=0.5), 0.03)


def tapestry(loc, w, h, c1, c2, rot_z=0.0):
    box(loc, (w, 0.05, h), mat("tap" + c1, c1, rough=0.95, noise=0.3, scale=6), 0.01, (0, 0, rot_z))
    box((loc[0], loc[1] - 0.03, loc[2]), (w * 0.8, 0.05, h * 0.8), mat("tapin" + c2, c2, rough=0.95, noise=0.35, scale=8), 0.01, (0, 0, rot_z))
    cyl((loc[0], loc[1] - 0.04, loc[2] + h / 2 + 0.05), 0.04, w + 0.3, mat("gold", "#FFC93C", rough=0.35, metal=0.6), rot=(0, math.radians(90), rot_z))


def set_palace(variant="day"):
    night = variant == "night"
    W, D, H = 12, 12, 6
    plane((0, 0, 0), (W, D), mat("pfloor", "#8E6A44", rough=0.55, noise=0.25, bricks={"scale": 2, "c2": "#7E5C3A", "mortar_c": "#4E3420", "w": 0.6, "h": 0.6, "mortar": 0.008, "k": 1}))
    panel_wall(-W / 2, W / 2, D / 2, 2.9)
    panel_wall(-D / 2, D / 2, -W / 2, 2.9, rot=True)
    panel_wall(-D / 2, D / 2, W / 2, 2.9, rot=True)
    plaster = mat("pplaster", "#E9DCC0", rough=0.9, noise=0.1)
    box((0, D / 2, (2.9 + H) / 2), (W, 0.3, H - 2.9), plaster, 0.01)
    box((-W / 2, 0, (2.9 + H) / 2), (0.3, D, H - 2.9), plaster, 0.01)
    box((W / 2, 0, (2.9 + H) / 2), (0.3, D, H - 2.9), plaster, 0.01)
    # ceiling with gilded ribs
    plane((0, 0, H), (W, D), mat("pceil", "#F3E6C8"), rot=(math.pi, 0, 0))
    for k in range(-5, 6, 2):
        box((k, 0, H - 0.08), (0.12, D, 0.16), mat("gold", "#FFC93C", rough=0.35, metal=0.6), 0.02)
        box((0, k, H - 0.08), (W, 0.12, 0.16), mat("gold", "#FFC93C", rough=0.35, metal=0.6), 0.02)
    # leaded window on the left wall
    xL = -W / 2 + 0.1
    glass = mat("pglass", "#CFE6F0", rough=0.1, emit="#FFF2D0" if not night else "#4A5E9A", emit_strength=2.0 if not night else 0.6)
    box((xL, 1.0, 3.6), (0.1, 2.4, 2.4), glass, 0)
    lead = mat("lead", "#3A3A42", rough=0.5, metal=0.4)
    for k in range(-3, 4):
        box((xL + 0.03, 1.0 + k * 0.34, 3.6), (0.04, 0.03, 2.4), lead, 0, (math.radians(35), 0, 0))
        box((xL + 0.03, 1.0 + k * 0.34, 3.6), (0.04, 0.03, 2.4), lead, 0, (math.radians(-35), 0, 0))
    box((xL + 0.05, 1.0, 3.6), (0.12, 2.6, 0.12), mat("stone", "#CFC2A8"), 0.01)
    # tapestries on the back wall
    tapestry((-3.2, D / 2 - 0.2, 4.3), 2.4, 2.4, "#7A1E2C", "#C0563A")
    tapestry((3.2, D / 2 - 0.2, 4.3), 2.4, 2.4, "#1E3E6E", "#3E7E8E")
    # great fireplace, centre back
    st = mat("fstone", "#CDBFA3", rough=0.9, noise=0.15, bricks={"scale": 2.4, "c2": "#BBAD90", "mortar_c": "#8E7E66", "w": 0.6, "h": 0.3, "k": 1})
    box((0, D / 2 - 0.5, 1.2), (3.2, 0.9, 2.4), st, 0.03)
    box((0, D / 2 - 0.9, 0.85), (2.0, 0.2, 1.5), mat("soot", "#1E1414", rough=0.9), 0.02)
    box((0, D / 2 - 0.5, 2.55), (3.6, 1.0, 0.3), st, 0.03)
    for k in range(5):
        cyl((-0.6 + k * 0.3, D / 2 - 1.0, 0.18), 0.08, 0.9, mat("log", "#5B3A29", noise=0.3), rot=(0, math.radians(90), math.radians(R.uniform(-20, 20))), verts=10)
    flames(0, D / 2 - 1.05, 0.2, 1.0, 7, 220 if night else 120)
    # four-poster bed (right)
    bed = mat("bedwood", "#5B3A29", noise=0.2)
    red = mat("velvet", "#8E1E2E", rough=0.85, noise=0.1)
    box((3.6, 2.0, 0.45), (2.4, 2.8, 0.5), bed, 0.04)
    box((3.6, 2.0, 0.8), (2.3, 2.7, 0.25), mat("linen", "#FFF4E0", rough=0.9), 0.08)
    box((3.6, 2.0, 0.95), (2.35, 2.0, 0.12), red, 0.04)
    for (x, y) in ((2.45, 0.65), (4.75, 0.65), (2.45, 3.35), (4.75, 3.35)):
        cyl((x, y, 1.6), 0.08, 3.2, bed, verts=12)
    box((3.6, 2.0, 3.25), (2.6, 3.0, 0.2), red, 0.03)
    for x in (2.4, 4.8):
        box((x, 2.0, 2.4), (0.05, 2.9, 1.6), red, 0.01)
    # the close stool (box toilet with velvet cushion) — the star prop of the Groom of the Stool item
    cs = (-2.2, 1.2)
    box((cs[0], cs[1], 0.3), (0.75, 0.6, 0.6), red, 0.05)
    box((cs[0], cs[1], 0.63), (0.8, 0.65, 0.08), mat("gold", "#FFC93C", rough=0.35, metal=0.6), 0.02)
    box((cs[0], cs[1], 0.7), (0.62, 0.5, 0.1), mat("cushion", "#B3262E", rough=0.9), 0.05)
    for dx in (-0.3, 0.3):
        for dy in (-0.22, 0.22):
            sphere((cs[0] + dx, cs[1] + dy, 0.02), 0.05, mat("gold", "#FFC93C", rough=0.35, metal=0.6))
    # chest, table with ewer and candles, rug
    box((-4.2, 3.8, 0.4), (1.4, 0.7, 0.8), mat("chest", "#6B3F25", noise=0.25), 0.05)
    box((-4.2, 3.8, 0.82), (1.45, 0.75, 0.06), mat("gold", "#FFC93C", rough=0.35, metal=0.6), 0.01)
    box((0.6, -0.6, 0.85), (1.6, 0.9, 0.08), mat("ptable", "#7A4A2B", noise=0.2), 0.02)
    for (x, y) in ((-0.1, -0.95), (1.3, -0.95), (-0.1, -0.25), (1.3, -0.25)):
        cyl((x, y, 0.42), 0.05, 0.84, mat("ptable", "#7A4A2B", noise=0.2), verts=10)
    cyl((0.9, -0.5, 1.05), 0.12, 0.32, mat("gold", "#FFC93C", rough=0.35, metal=0.6), r2=0.07)
    candle((0.2, -0.6, 0.89), light=night, e=40)
    box((0, -1.0, 0.012), (5.5, 3.5, 0.02), mat("prug", "#1E3E6E", rough=0.95, noise=0.2), 0)
    box((0, -1.0, 0.016), (5.0, 3.0, 0.02), mat("prug2", "#C0563A", rough=0.95, noise=0.25, scale=5), 0)
    for y in (-3, 3):
        torch_sconce((-W / 2 + 0.4, y, 2.3), math.radians(90))
    if night:
        world("#1E2A4A", "#3A3050", 0.15)
        point((0, -2, 4.5), "#FFB060", 120, 1.0)
        area((2, -5, 4.0), (60, 0, 20), 6, "#7A8ED0", 120)
    else:
        world("#9FD0E8", "#FFF1D6", 0.35)
        area((-4.5, 1.0, 3.6), (90, 0, -90), 3, "#FFF1D6", 450)
        area((2, -5, 4.5), (55, 0, 20), 7, "#FFE7C8", 650)
        area((0, 0, 5.8), (0, 0, 0), 6, "#FFF1D6", 200)


def murky_water(size, loc, color):
    plane(loc, size, mat("water" + color, color, rough=0.15, noise=0.2, scale=2))


def set_yard(variant="tannery"):
    tan = variant == "tannery"
    ground = "#8E7A5A" if tan else "#9A8E6A"
    plane((0, 0, 0), (60, 60), mat("yground" + variant, ground, rough=0.95, noise=0.3, scale=1.5))
    # river along the back, town wall beyond
    murky_water((60, 5), (0, 9.5, -0.15), "#5E6E3A" if tan else "#4E8E9A")
    box((0, 7.0, -0.05), (60, 0.5, 0.3), mat("bank", "#6B5A40", noise=0.3), 0.05)
    wall = mat("twall", "#BBAD90", rough=0.9, noise=0.15, bricks={"scale": 2, "c2": "#A89A7E", "mortar_c": "#7E6E56", "w": 0.8, "h": 0.4, "k": 1})
    box((0, 14.0, 2.5), (60, 1.2, 5.0), wall, 0.03)
    for x in range(-24, 25, 3):
        box((x, 14.0, 5.3), (1.4, 1.2, 0.7), wall, 0.03)
    box((-6, 14.2, 4.0), (3.0, 3.0, 8.0), wall, 0.03)
    prism_roof((-6, 14.2, 8.0), 3.4, 3.4, 2.0, mat("roof", "#A84A32", noise=0.2))
    for x, d in ((4, 1), (12, 1.3), (-14, 1.1)):
        house((x, 18, 0), 4, 3, 5.5 * d, timber=True, floors=2)
    # workshop shed (left)
    shed_w = mat("shed", "#8A5A3B", noise=0.3, bricks={"scale": 3, "c2": "#7A4E32", "mortar_c": "#4E3420", "w": 0.25, "h": 3.0, "mortar": 0.01, "k": 1})
    box((-6.5, 2.5, 1.6), (4.5, 3.5, 3.2), shed_w, 0.03)
    prism_roof((-6.5, 2.5, 3.2), 4.9, 3.9, 1.6, mat("thatch", "#C9A65E", rough=0.95, noise=0.4))
    box((-4.24, 2.0, 1.0), (0.06, 1.2, 2.0), mat("door", "#4E3420"), 0.01)
    if tan:
        # sunken tanning pits (rows of square vats with murky liquid)
        rim = mat("pitrim", "#6B4A30", noise=0.25)
        for i, (x, y) in enumerate([(-1.5, 3.5), (0.6, 3.5), (2.7, 3.5), (-1.5, 1.4), (0.6, 1.4), (2.7, 1.4)]):
            for (bx, by, sx, sy) in ((x, y - 0.82, 1.8, 0.16), (x, y + 0.82, 1.8, 0.16), (x - 0.82, y, 0.16, 1.8), (x + 0.82, y, 0.16, 1.8)):
                box((bx, by, 0.12), (sx, sy, 0.24), rim, 0.03)
            liquid = ["#6E5A2E", "#7E6A3A", "#5E4A26", "#8E7A4A"][i % 4]
            box((x, y, 0.205), (1.5, 1.5, 0.02), mat("pit" + liquid, liquid, rough=0.15, noise=0.3, scale=3), 0)  # liquid surface just inside the rim
            if i % 2 == 0:
                box((x + 0.2, y, 0.225), (1.0, 0.7, 0.03), mat("hide", "#B08A5E", rough=0.8, noise=0.3), 0.02, (0, 0.1, 0.3))
        # drying frames with hides
        frame = mat("frame", "#5B3A29", noise=0.2)
        for x in (5.5, 8.0):
            for dx in (-0.9, 0.9):
                cyl((x + dx, 2.0, 1.1), 0.06, 2.2, frame, verts=8)
            cyl((x, 2.0, 2.15), 0.05, 2.0, frame, verts=8, rot=(0, math.radians(90), 0))
            box((x, 2.0, 1.35), (1.5, 0.05, 1.5), mat("hide2", "#C49A6A", rough=0.8, noise=0.35, scale=4), 0.08)
        # dung bucket + pigeon loft
        cyl((-2.6, -0.4, 0.3), 0.32, 0.6, mat("bucket", "#7A5A3B", noise=0.2), verts=16, r2=0.38)
        cyl((-2.6, -0.4, 0.58), 0.3, 0.04, mat("dung", "#4E3A22", rough=1.0, noise=0.4), verts=16)
        box((-9.5, 5.5, 2.5), (1.4, 1.4, 1.6), mat("loft", "#E9DCC0", noise=0.1), 0.03)
        cyl((-9.5, 5.5, 0.9), 0.12, 1.8, frame, verts=8)
        prism_roof((-9.5, 5.5, 3.3), 1.6, 1.6, 0.7, mat("roof", "#A84A32", noise=0.2))
        for k in range(3):
            box((-8.78, 5.0 + k * 0.5, 2.5), (0.04, 0.25, 0.3), mat("hole", "#2A1C1E"), 0)
    else:
        # fulling tubs with pale yellow liquid, cloth bolts, tenter frames
        for x, y in ((-1.2, 2.6), (1.5, 2.6), (0.2, 0.4)):
            cyl((x, y, 0.45), 0.85, 0.9, mat("tub", "#8A5A3B", noise=0.25, bricks={"scale": 4, "c2": "#7A4E32", "mortar_c": "#3E2A1A", "w": 0.12, "h": 4, "mortar": 0.02, "k": 1}), verts=28)
            cyl((x, y, 0.91), 0.8, 0.02, mat("lant", "#D8C46A", rough=0.15, noise=0.2), verts=28)
            for z in (0.2, 0.7):
                cyl((x, y, z), 0.87, 0.06, mat("iron", "#2A1C1E", rough=0.5, metal=0.5), verts=28)
            box((x + 0.2, y - 0.1, 0.925), (0.9, 0.5, 0.03), mat("wool", "#EDE4D0", rough=0.95, noise=0.3), 0.03, (0, 0, 0.4))
        tf = mat("tframe", "#5B3A29", noise=0.2)
        for x in (5.0, 8.5):
            for dx in (-1.4, 1.4):
                cyl((x + dx, 2.4, 0.8), 0.05, 1.6, tf, verts=8)
            cyl((x, 2.4, 1.55), 0.04, 2.9, tf, verts=8, rot=(0, math.radians(90), 0))
            cyl((x, 2.4, 0.35), 0.04, 2.9, tf, verts=8, rot=(0, math.radians(90), 0))
            box((x, 2.4, 0.95), (2.7, 0.03, 1.1), mat("cloth" + str(x), "#C0563A" if x < 6 else "#2E5A8C", rough=0.95, noise=0.2), 0.0)
        for k in range(4):
            cyl((-3.2 + k * 0.05, -0.6 + k * 0.4, 0.2 + (k % 2) * 0.35), 0.2, 1.1, mat("bolt" + str(k), ["#EDE4D0", "#C0563A", "#2E5A8C", "#5E9E4A"][k], rough=0.95, noise=0.15), rot=(0, math.radians(90), 0), verts=16)
        for k in range(3):
            cyl((-4.5 + k * 0.5, 4.5, 0.25), 0.2, 0.5, mat("pot", "#B07A48"), r2=0.15, verts=14)
    for p in ((-3.5, 5.5), (10.5, 4.5), (-11, -1)):
        tree((p[0], p[1], 0), 1.1)
    for k in range(14):  # grass tufts and puddles so the ground isn't flat
        x, y = R.uniform(-10, 11), R.uniform(-4, 6.5)
        sphere((x, y, 0.02), R.uniform(0.2, 0.4), mat("tuft", "#7E9E4A", rough=0.9, noise=0.4), (1.4, 1, 0.5), sub=2)
    for k in range(5):
        x, y = R.uniform(-3, 9), R.uniform(-3, 0.5)
        cyl((x, y, 0.012), R.uniform(0.4, 0.9), 0.01, mat("puddle" + variant, "#6E7A5A" if tan else "#8A9AA0", rough=0.1), verts=24)
    box((0, -1.8, 0.015), (20, 0.5, 0.01), mat("rut", "#6E5E44", rough=1, noise=0.4), 0)
    box((0, -2.6, 0.015), (20, 0.5, 0.01), mat("rut", "#6E5E44", rough=1, noise=0.4), 0)
    barrel((3.8, -0.8, 0), 0.9); barrel((4.6, -0.4, 0), 0.8); crate((-4.0, 0.6, 0), 0.7, 0.3)
    world("#8FC9E8", "#FFE9C7", 0.9)
    sun((52, 0, -35), "#FFE2B8", 4.0, 4)
    area((0, -8, 6), (50, 0, 0), 10, "#FFE7C8", 300)


def set_fair(variant="day"):
    plane((0, 0, 0), (70, 70), mat("fgrass", "#7EB85A", rough=0.95, noise=0.35, scale=1.2))
    box((0, 0, 0.01), (14, 9, 0.02), mat("trodden", "#B9A07A", rough=1.0, noise=0.4, scale=1.5), 0)
    # quack's wagon stage (centre back)
    wood = mat("stage", "#8A5A3B", noise=0.25, bricks={"scale": 3, "c2": "#7A4E32", "mortar_c": "#4E3420", "w": 2.0, "h": 0.22, "mortar": 0.01, "k": 1})
    box((0, 4.0, 0.6), (5.0, 2.6, 1.2), wood, 0.04)
    for x in (-2.0, 2.0):
        cyl((x, 2.75, 0.55), 0.55, 0.15, mat("wheel", "#5B3A29"), rot=(math.radians(90), 0, 0), verts=24)
        cyl((x, 2.7, 0.55), 0.1, 0.2, mat("iron", "#2A1C1E", rough=0.5, metal=0.5), rot=(math.radians(90), 0, 0), verts=12)
    box((0, 5.2, 2.6), (5.0, 0.15, 2.8), mat("backdrop", "#6E3A8C", rough=0.9, noise=0.1), 0.02)
    for k in range(9):
        c = "#FFC93C" if k % 2 else "#FF6B5B"
        box((-2.2 + k * 0.55, 3.0, 3.7), (0.55, 2.4, 0.06), mat("awn" + c, c, rough=0.8), 0.01, (math.radians(-12), 0, 0))
    for x in (-2.4, 2.4):
        cyl((x, 2.85, 2.4), 0.06, 2.6, mat("pole", "#5B3A29"), verts=8)
    sign((0, 5.1, 3.4), "#FFC93C")
    # table of "miracle" bottles on the stage
    box((1.3, 3.9, 1.6), (1.4, 0.6, 0.08), mat("ftable", "#B5824E", noise=0.2), 0.02)
    for k in range(6):
        c = ["#5ED3B5", "#FF6B5B", "#FFC93C", "#2E8CB8", "#5ED3B5", "#B3262E"][k]
        cyl((0.8 + k * 0.2, 3.9 + (k % 2) * 0.12, 1.78), 0.06, 0.26, mat("bottle" + c, c, rough=0.1, emit=c, emit_strength=0.4), r2=0.035, verts=12)
    # tents and stalls around
    for (x, y, c) in ((-9, 7, "#FF6B5B"), (9, 8, "#0F6B78"), (-14, 2, "#FFC93C"), (14, 1, "#5ED3B5")):
        cyl((x, y, 1.4), 2.0, 2.8, mat("tentw" + c, "#FFF4E0", rough=0.9), verts=16)
        cyl((x, y, 3.6), 2.2, 1.6, mat("tent" + c, c, rough=0.85), verts=16, r2=0.05)
    for (x, y) in ((-6, 1), (6, 0)):
        box((x, y, 0.5), (2.0, 1.0, 1.0), mat("stall", "#B5824E", noise=0.2), 0.03)
        for k in range(4):
            sphere((x - 0.6 + k * 0.4, y, 1.1), 0.14, mat("fruit" + str(k), ["#FF6B5B", "#FFC93C", "#5E9E4A", "#FF9A3C"][k]))
    bunting((-12, 8, 4.5), (12, 8, 4.5), 1.0, 30)
    bunting((-7, 3, 3.4), (7, 3, 3.4), 0.6, 20)
    for p in ((-18, 12), (-11, 15), (16, 14), (20, 6), (-20, -2)):
        tree((p[0], p[1], 0), 1.3)
    for x in (-25, -8, 8, 25):
        house((x, 26, 0), 5, 4, 6, timber=True, floors=2)
    world("#8FD3F4", "#FFE9C7", 1.0)
    sun((50, 0, -30), "#FFE2B8", 4.5, 4)
    area((0, -8, 6), (55, 0, 0), 12, "#FFF1D6", 300)


def set_backyard(variant="night"):
    plane((0, 0, 0), (50, 50), mat("bground", "#5E5A44", rough=0.95, noise=0.35, scale=1.5))
    box((0, 0, 0.01), (6, 30, 0.02), mat("lane", "#6E6650", rough=1.0, noise=0.4, scale=2), 0)
    # back of the houses
    for x, h in ((-7, 6.5), (-2, 7.2), (3.5, 6.2), (9, 7.0)):
        house((x, 8.0, 0), 5, 4, h, timber=True, floors=2)
    # privy shed with half-moon door; pit hatch beside it
    pw = mat("privy", "#6B4A30", noise=0.3, bricks={"scale": 3, "c2": "#5E4026", "mortar_c": "#3A2616", "w": 0.22, "h": 3.0, "mortar": 0.012, "k": 1})
    box((-1.5, 3.8, 1.1), (1.4, 1.4, 2.2), pw, 0.03)
    prism_roof((-1.5, 3.8, 2.2), 1.7, 1.7, 0.6, mat("roofb", "#5A3A30", noise=0.2))
    box((-1.5, 3.08, 1.0), (0.8, 0.04, 1.8), mat("pdoor", "#4E3420", noise=0.2), 0.01)
    cyl((-1.5, 3.05, 1.6), 0.12, 0.05, mat("moonhole", "#1A1210"), rot=(math.radians(90), 0, 0), verts=16)
    box((0.6, 3.4, 0.05), (1.6, 1.6, 0.1), mat("hatchrim", "#4E3A26"), 0.02)
    box((0.6, 3.4, 0.07), (1.3, 1.3, 0.06), mat("pitdark", "#2A2416", rough=0.3), 0)
    box((0.6, 2.4, 0.09), (1.4, 0.7, 0.06), mat("plank", "#7A5A3B", noise=0.3), 0.01, (0, 0, 0.15))
    # gong farmers' cart with barrels, ladder, shovel, buckets
    box((3.6, 1.6, 0.85), (2.2, 1.3, 0.12), mat("cart", "#7A5A3B", noise=0.25), 0.03)
    for y in (1.0, 2.2):
        cyl((3.0, y, 0.45), 0.45, 0.1, mat("wheel", "#5B3A29"), rot=(0, math.radians(90), 0), verts=20)
    for k in range(3):
        barrel((3.0 + k * 0.6, 1.6, 0.9), 0.7)
    for k in range(2):
        cyl((-0.2 + k * 0.45, 2.0, 0.22), 0.2, 0.44, mat("bucket", "#7A5A3B", noise=0.2), r2=0.24, verts=14)
    box((1.6, 4.4, 1.0), (0.1, 0.5, 2.6), mat("ladder", "#8A6A4E"), 0.01, (math.radians(20), 0, 0))
    # lanterns (the only light: night work), moon
    for p in ((-0.4, 2.6, 0), (3.6, 0.6, 0)):
        cyl((p[0], p[1], 0.9), 0.03, 1.8, mat("iron", "#2A1C1E", rough=0.5, metal=0.5), verts=6)
        box((p[0], p[1], 1.9), (0.22, 0.22, 0.3), mat("lglass", "#FFD27A", emit="#FFB84D", emit_strength=8), 0.02)
        point((p[0], p[1] - 0.2, 1.9), "#FFB060", 260, 0.1)
    sphere((-14, 40, 18), 2.2, mat("moon", "#FFF4E0", emit="#FFF4E0", emit_strength=4))
    for p in ((-12, 4), (12, 3), (-9, -6)):
        tree((p[0], p[1], 0), 1.1, "#2E5A3A")
    world("#1A2A4A", "#33406A", 0.6)
    sun((40, 0, 150), "#9FB8F0", 1.2, 6)
    area((-3, -6, 7), (50, 0, -10), 12, "#6A80C8", 420)


def set_cottage(variant="wake"):
    tavern, stable = variant == "tavern", variant == "stable"
    W, D, H = 10, 9, 4.2
    floor = mat("cfloor" + variant, "#6E5A40" if stable else "#9A7A54", rough=0.95, noise=0.35 if stable else 0.2,
                bricks=None if stable else {"scale": 2, "c2": "#8A6A46", "mortar_c": "#5A4228", "w": 1.4, "h": 0.25, "mortar": 0.01, "k": 1})
    plane((0, 0, 0), (W, D), floor)
    wall = mat("cwall", "#D9C9A6", rough=0.95, noise=0.18)
    box((0, D / 2, H / 2), (W, 0.4, H), wall, 0.03)
    box((-W / 2, 0, H / 2), (0.4, D, H), wall, 0.03)
    box((W / 2, 0, H / 2), (0.4, D, H), wall, 0.03)
    beam = mat("cbeam", "#4E3420", noise=0.25)
    for x in (-3, 0, 3):
        box((x, 0, H - 0.2), (0.3, D, 0.35), beam, 0.03)
    for x in (-4.6, -1.5, 1.5, 4.6):
        box((x, D / 2 - 0.22, H / 2), (0.25, 0.1, H), beam, 0.02)
    plane((0, 0, H), (W, D), mat("cceil", "#8A6A4E", noise=0.2), rot=(math.pi, 0, 0))
    # small window, left wall
    box((-W / 2 + 0.15, 0.8, 2.3), (0.1, 1.2, 1.0), mat("cwin", "#BFE3F0", emit="#FFF2D0" if variant != "wake" else "#6A7AB0", emit_strength=1.6 if variant != "wake" else 0.6), 0)
    box((-W / 2 + 0.2, 0.8, 2.3), (0.08, 0.08, 1.0), beam, 0)
    if stable:
        # earth floor, hay, stalls, dovecote boxes: where saltpetre men dug
        hay = mat("hay", "#D8B45A", rough=1, noise=0.45, scale=6)
        for (hx, hy) in ((-3.6, 3.0), (-1.0, 3.2), (2.2, 3.1), (4.0, 0.5)):
            for k in range(7):
                sphere((hx + R.uniform(-0.6, 0.6), hy + R.uniform(-0.4, 0.4), 0.15 + R.uniform(0, 0.35)), R.uniform(0.3, 0.5), hay, (1.3, 1, 0.8), sub=2)
        for k in range(3):
            box((-3.8 + k * 0.05, -2.6, 0.3 + k * 0.6), (1.2, 0.8, 0.6), hay, 0.12, (0, 0, k * 0.1))
        for x in (-2.5, 0.5, 3.5):
            box((x, 2.5, 0.6), (0.15, 3.0, 1.2), beam, 0.02)
        box((0.5, 3.9, 0.6), (6.2, 0.15, 1.2), beam, 0.02)
        for i in range(3):
            for j in range(4):
                box((-4.8 + 0.3, -2.5 + j * 0.55, 2.4 + i * 0.5), (0.3, 0.45, 0.4), mat("nest", "#2A1C1E"), 0.01)
        box((1.2, -0.8, 0.02), (2.0, 1.4, 0.04), mat("dugsoil", "#4E3A26", rough=1, noise=0.5), 0.05)
        for k in range(5):
            sphere((0.4 + k * 0.4, -1.8, 0.1), 0.28, mat("soilpile", "#5A4430", rough=1, noise=0.5), (1, 1, 0.6), sub=2)
        cyl((2.6, -1.4, 0.7), 0.04, 1.4, mat("shovel", "#8A6A4E"), verts=6, rot=(math.radians(15), 0, 0))
        box((2.6, -1.62, 0.05), (0.28, 0.05, 0.35), mat("iron", "#2A1C1E", rough=0.5, metal=0.5), 0.01, (math.radians(15), 0, 0))
    else:
        # hearth on the back wall
        st = mat("hearth", "#BBAD90", rough=0.9, noise=0.15, bricks={"scale": 2.4, "c2": "#A89A7E", "mortar_c": "#7E6E56", "w": 0.6, "h": 0.3, "k": 1})
        box((2.6, D / 2 - 0.45, 1.0), (2.2, 0.7, 2.0), st, 0.03)
        box((2.6, D / 2 - 0.8, 0.7), (1.3, 0.1, 1.0), mat("soot", "#1E1414", rough=0.9), 0.02)
        box((2.6, D / 2 - 0.45, 2.9), (1.2, 0.6, 1.8), st, 0.03)
        flames(2.6, D / 2 - 0.95, 0.2, 0.8, 5, 100)
        tab = mat("ctable", "#8A5A3B", noise=0.25)
        box((-0.6, 0.6, 0.8), (2.6, 1.0, 0.1), tab, 0.03)
        for (x, y) in ((-1.7, 0.25), (0.5, 0.25), (-1.7, 0.95), (0.5, 0.95)):
            cyl((x, y, 0.38), 0.06, 0.76, tab, verts=10)
        box((-0.6, -0.2, 0.45), (2.4, 0.35, 0.08), tab, 0.02)
        if tavern:
            # counter, barrels on a rack, tankards
            box((-3.4, 2.6, 0.55), (0.9, 3.2, 1.1), mat("counter", "#6B3F25", noise=0.25), 0.03)
            for k in range(3):
                barrel((-4.4, 1.6 + k * 0.9, 1.1), 0.75)
            for k in range(4):
                cyl((-1.6 + k * 0.5, 0.6, 0.98), 0.09, 0.26, mat("tankard", "#8E8E96", rough=0.35, metal=0.7), verts=14)
            sign((0, D / 2 - 0.25, 3.0), "#FFC93C")
            world("#9FD0E8", "#FFF1D6", 0.35)
            area((2, -4, 3.8), (50, 0, 20), 6, "#FFE7C8", 520)
        else:
            # wake: covered body on a bed (no face, no gore), bread loaf + wooden bowl, candles
            box((-2.6, 2.8, 0.35), (2.2, 1.1, 0.5), mat("cbed", "#6B4A30", noise=0.2), 0.04)
            sphere((-2.6, 2.8, 0.7), 0.5, mat("sheet", "#EDE4D0", rough=0.95), (2.0, 0.85, 0.35), sub=3)
            sphere((-3.55, 2.8, 0.75), 0.24, mat("sheet", "#EDE4D0", rough=0.95), (1, 1, 0.8), sub=3)
            sphere((-0.9, 0.55, 0.92), 0.16, mat("bread", "#C98A4A", rough=0.8, noise=0.2), (1.4, 1, 0.7), sub=2)
            cyl((-0.3, 0.65, 0.9), 0.17, 0.1, mat("bowl", "#7A5A3B", noise=0.2), r2=0.11, verts=18)
            for p in ((-1.4, 2.4, 0.6), (-3.8, 3.3, 0.6), (0.1, 0.9, 0.85)):
                candle(p, 0.25, True, 35)
            world("#1E2A4A", "#3A3050", 0.12)
            area((1, -4, 3.8), (50, 0, 20), 6, "#8A9AD0", 90)
            point((-1.2, 0.5, 2.6), "#FFB060", 60, 0.6)
    if stable:
        world("#9FD0E8", "#FFF1D6", 0.35)
        area((-4.6, 0.8, 2.3), (90, 0, -90), 1.5, "#FFF1D6", 220)
        area((2, -4, 3.8), (50, 0, 20), 6, "#FFE7C8", 450)


sets.BUILDERS.update({"palace": set_palace, "yard": set_yard, "fair": set_fair, "backyard": set_backyard, "cottage": set_cottage})
SET_VARIANTS = {"palace": ["day", "night"], "yard": ["tannery", "fullers"], "fair": ["day"], "backyard": ["night"], "cottage": ["wake", "tavern", "stable"]}
