"""Toon sets for standalone Shorts batch 1 (A-001..A-007). Registered into sets.BUILDERS on import.
marsh  (tide|dusk) : tidal quicksand flat, wet glossy sand, pit with ripple rings at (0,2), sea and incoming tide at y>9
arctic (night)     : ice camp under aurora: tent, sledge, campfire at (0.6,1.2), ice ridges, sea ice
castle (night|day) : curtain wall with a corbelled garderobe at x=0 (seat z 6.2), chute to the moat, keep, torches
lab    (day)       : bright science lab: bench at y 1.6 top z 0.95, robot arm on bench (1.2,1.6), screens, shelves
"""
import math, random
import bpy
import sets
from sets import (mat, box, cyl, sphere, plane, prism_roof, world, sun, area, point, tree, barrel, crate, torch_sconce, hexrgb)
from sets2 import flames


def ring(loc, r, w, m, z=0.0):
    bpy.ops.mesh.primitive_torus_add(location=loc, major_radius=r, minor_radius=w, major_segments=48, minor_segments=6)
    o = bpy.context.active_object
    o.scale = (1, 1, 0.25)
    o.data.materials.append(m)
    bpy.ops.object.shade_smooth()
    return o


def disc(loc, r, m, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_cylinder_add(location=loc, radius=r, depth=0.02, vertices=48)
    o = bpy.context.active_object
    o.scale = scale
    o.data.materials.append(m)
    return o


def rock(loc, s, m, rz=0.0):
    o = sphere(loc, s, m, scale=(1.3, 1.0, 0.6), sub=2)
    o.rotation_euler = (0, 0, rz)
    return o


# ---------------------------------------------------------------- marsh (A-001 quicksand)
def set_marsh(variant="tide"):
    R = random.Random(11)
    dusk = variant == "dusk"
    sand = mat("wetsand", "#C9A877", rough=0.55, noise=0.25, scale=2.5)
    dry = mat("drysand", "#E2C894", rough=0.95, noise=0.3, scale=1.5)
    plane((0, 0, 0), (80, 80), sand)
    # dry dunes behind (left/right) with grass tufts
    for x, y, s in ((-9, 6, 3.5), (-14, 2, 4.5), (10, 7, 3.8), (15, 1, 5.0), (-5, 14, 3), (6, 15, 3.2)):
        sphere((x, y, -s * 0.55), s, dry, scale=(1.8, 1.2, 0.55), sub=3)
    grass = mat("dunegrass", "#7FA05A", rough=0.8, noise=0.2)
    for _ in range(40):
        x, y = R.uniform(-16, 16), R.uniform(0, 16)
        if abs(x) < 6.5 and y < 9:
            continue
        for k in range(3):
            box((x + k * 0.07, y, 0.35), (0.03, 0.03, 0.7 + R.random() * 0.3), grass, 0, (R.uniform(-0.4, 0.4), R.uniform(-0.4, 0.4), 0))
    # glossy wet patches and shallow channels
    wet = mat("wetshine", "#9C8360", rough=0.12, noise=0.15, scale=4)
    for _ in range(14):
        disc((R.uniform(-7, 7), R.uniform(-4, 9), 0.006), R.uniform(0.4, 1.6), wet, (1.0, R.uniform(0.3, 0.7), 1))
    # the quicksand pit: darker, glossier, with ripple rings around the sinking spot
    qs = mat("quicksand", "#8F7350", rough=0.18, noise=0.35, scale=6)
    disc((0, 2, 0.012), 1.9, qs, (1.25, 1.0, 1))
    ripple = mat("ripple", "#B49468", rough=0.2)
    for r in (0.55, 0.9, 1.3):
        ring((0, 2, 0.02), r, 0.025, ripple)
    # sea + incoming tide line (white foam), far edge
    sea = mat("sea", "#3F8FA8", rough=0.06, noise=0.12, scale=1)
    box((0, 24, -0.02), (80, 26, 0.04), sea, 0)
    foam = mat("foam", "#F4F7F2", rough=0.4, emit="#FFFFFF", emit_strength=0.3)
    for k, y in enumerate((11.0, 11.6, 12.4)):
        box((0, y, 0.01), (80, 0.18 - k * 0.04, 0.02), foam, 0, (0, 0, R.uniform(-0.01, 0.01)))
    # props: driftwood, warning post with an (unreadable) sign, rocks, seagull-height posts
    wood = mat("drift", "#9C8466", rough=0.9, noise=0.4)
    cyl((-3.2, 0.4, 0.08), 0.09, 2.2, wood, rot=(0, math.radians(90), math.radians(25)), verts=10)
    cyl((3.6, 4.2, 0.07), 0.07, 1.6, wood, rot=(0, math.radians(90), math.radians(-40)), verts=10)
    cyl((2.6, -0.6, 0.7), 0.05, 1.4, wood, verts=8)
    box((2.6, -0.62, 1.35), (0.7, 0.05, 0.45), mat("signboard", "#F2C230", rough=0.6), 0.02)
    box((2.6, -0.65, 1.35), (0.5, 0.01, 0.06), mat("signstripe", "#1E1A18"), 0)
    rk = mat("rock", "#6E6A62", rough=0.8, noise=0.4, scale=3)
    for p in ((-4.5, 5, 0.3), (5.5, 2, 0.4), (-2, 8, 0.25), (4.2, 9, 0.35)):
        rock((p[0], p[1], 0.05), p[2], rk, R.random() * 3)
    for p in ((-6, 9.5), (-5.2, 9.7), (6.8, 10)):
        cyl((p[0], p[1], 0.6), 0.08, 1.2, wood, verts=8)
    if dusk:
        world("#FF9E6B", "#FFD8A8", 0.9)
        sun((80, 0, 200), "#FFB070", 4.0, 3)
        area((0, -8, 6), (60, 0, 0), 10, "#8FB0FF", 300)
    else:
        world("#7EC8F0", "#FFF1D6", 1.1)
        sun((55, 0, 210), "#FFE6C0", 4.5, 3)
        area((-4, -8, 6), (60, 0, -20), 10, "#BFD8FF", 260)
    # low clouds over the sea
    cl = mat("cloud", "#FFFFFF", rough=1.0, emit="#FFFFFF", emit_strength=0.6)
    for x, z, s in ((-12, 7, 2.5), (-4, 8.5, 3.0), (8, 7.5, 2.8), (16, 9, 3.4)):
        for k in range(3):
            sphere((x + k * s * 0.7, 45, z + (k % 2) * 0.6), s * (0.8 + 0.2 * k), cl, scale=(1.6, 0.6, 0.7), sub=2)


# ---------------------------------------------------------------- arctic (A-002 polar bear liver)
def set_arctic(variant="night"):
    R = random.Random(23)
    snow = mat("snow", "#E8F1FA", rough=0.75, noise=0.18, scale=2)
    plane((0, 0, 0), (90, 90), snow)
    ice = mat("ice", "#9FD3EA", rough=0.15, noise=0.2, scale=3)
    # pressure ridges and ice blocks
    for _ in range(26):
        x, y = R.uniform(-18, 18), R.uniform(5, 22)
        box((x, y, 0.3), (R.uniform(0.6, 2.2), R.uniform(0.5, 1.4), R.uniform(0.5, 1.8)), ice, 0.08,
            (R.uniform(-0.3, 0.3), R.uniform(-0.3, 0.3), R.uniform(0, 3)))
    for x, y, s in ((-11, 9, 3), (12, 11, 3.6), (-4, 18, 4), (6, 20, 4.5)):
        sphere((x, y, -s * 0.5), s, snow, scale=(2.0, 1.2, 0.7), sub=3)
    # camp: canvas tent, sledge with crates, barrels, oars (1590s sailors' camp, generic)
    canvas = mat("canvas", "#C9B48E", rough=0.9, noise=0.25)
    prism_roof((-2.6, 2.6, 0), 2.6, 3.0, 2.0, canvas, overhang=0.0)
    box((-2.6, 1.08, 0.7), (0.7, 0.03, 1.3), mat("tentdoor", "#3A2C20"), 0)
    sl = mat("sledge", "#7A5A3B", noise=0.3)
    box((2.8, 3.2, 0.42), (2.2, 0.9, 0.08), sl, 0.02)
    for y in (2.8, 3.6):
        box((2.8, y, 0.2), (2.4, 0.06, 0.08), sl, 0.02)
    crate((2.5, 3.2, 0.75), 0.55, 0.2)
    barrel((3.3, 3.2, 0.48), 0.6)
    for k in range(3):
        cyl((-0.4 + k * 0.3, 4.4, 0.9), 0.04, 2.0, sl, rot=(math.radians(8 * (k - 1)), 0, 0), verts=8)
    # campfire with stones, a spit, glow on the snow
    st = mat("stone", "#5A5650", rough=0.8, noise=0.3)
    for k in range(9):
        a = k / 9 * math.tau
        sphere((0.6 + 0.45 * math.cos(a), 1.2 + 0.45 * math.sin(a), 0.07), 0.12, st, scale=(1.2, 1, 0.7), sub=2)
    flames(0.6, 1.2, 0.05, 0.75, light=True)
    for x in (0.0, 1.2):
        cyl((x, 1.2, 0.45), 0.03, 0.9, sl, verts=6)
    cyl((0.6, 1.2, 0.88), 0.025, 1.4, mat("iron", "#2A1C1E", rough=0.5, metal=0.5), rot=(0, math.radians(90), 0), verts=6)
    glow = mat("snowglow", "#FFC890", rough=0.8, emit="#FF9A50", emit_strength=0.25)
    disc((0.6, 1.2, 0.004), 1.6, glow)
    # ship frozen in the ice far behind (silhouette): hull, masts
    hull = mat("hull", "#3A2A22", noise=0.2)
    box((-8, 16, 1.2), (7, 2.0, 2.0), hull, 0.3, (0, 0, math.radians(-8)))
    for x in (-10, -7.5, -5.2):
        cyl((x, 16, 5), 0.12, 7.5, hull, verts=8)
        box((x, 16, 6.5), (2.6, 0.08, 0.1), hull, 0)
    # aurora curtains + stars + moon
    for k, (c, x) in enumerate((("#5EF2A8", -8), ("#4ED6C8", 0), ("#9A7BFF", 9))):
        box((x, 40, 14 + k), (16, 0.1, 9), mat(f"aurora{k}", c, rough=1, emit=c, emit_strength=2.2), 0, (0, 0, math.radians(8 * (k - 1))))
    starm = mat("star", "#FFFFFF", emit="#FFFFFF", emit_strength=6)
    for _ in range(90):
        sphere((R.uniform(-50, 50), 55, R.uniform(8, 40)), R.uniform(0.04, 0.1), starm, sub=1)
    sphere((16, 50, 22), 1.6, mat("moon", "#FFF4E0", emit="#FFF4E0", emit_strength=4))
    world("#0E1A3A", "#2A3E6E", 0.55)
    sun((35, 0, 160), "#9FC0FF", 1.4, 6)
    area((-3, -6, 7), (50, 0, -10), 12, "#6A90D8", 520)
    point((0.6, 0.6, 1.0), "#FFA060", 420, 0.3)


# ---------------------------------------------------------------- castle (A-006 garderobes)
def set_castle(variant="night"):
    night = variant == "night"
    R = random.Random(37)
    plane((0, 0, -1.2), (90, 90), mat("grassn", "#3E5A36" if night else "#6E9E4E", rough=0.95, noise=0.3, scale=1.5))
    # moat in front of the wall
    box((0, 1.0, -0.6), (40, 4.0, 0.2), mat("moat", "#24443E" if night else "#3F7F78", rough=0.05, noise=0.15), 0)
    stone = mat("cwall", "#8C8478", noise=0.25, bricks={"scale": 1.2, "c2": "#7A7266", "mortar_c": "#5E574E", "w": 0.6, "h": 0.32, "mortar": 0.02, "k": 1})
    # curtain wall (y=4) with battlements; garderobe turret corbelled out at x=0
    box((0, 4.2, 4.0), (30, 2.0, 10.0), stone, 0.05)
    for k in range(-14, 15, 2):
        box((k, 3.3, 9.4), (1.0, 0.6, 0.9), stone, 0.03)
    box((0, 2.6, 6.8), (1.8, 1.4, 1.8), stone, 0.04)          # garderobe box
    prism_roof((0, 2.6, 7.7), 2.0, 1.6, 0.8, mat("slate", "#4E5664", noise=0.2))
    for x in (-0.6, 0.0, 0.6):                                 # corbels
        box((x, 2.4, 5.7), (0.3, 1.0, 0.4), stone, 0.02, (math.radians(-20), 0, 0))
    box((0, 2.0, 2.7), (0.7, 0.35, 6.0), mat("chute", "#2A2622", rough=0.9), 0.02)  # chute down the wall
    box((0, 1.82, 2.7), (0.45, 0.02, 5.8), mat("chutein", "#151210"), 0)
    box((0, 1.95, 6.9), (0.25, 0.05, 0.5), mat("slit", "#FFC870" if night else "#1A1614", emit="#FFB050" if night else None,
                                                emit_strength=4 if night else 0), 0)
    # keep and towers behind
    for x, h in ((-9, 13), (9, 12)):
        cyl((x, 5.0, h / 2 - 1), 2.4, h, stone, verts=24)
        for k in range(10):
            a = k / 10 * math.tau
            box((x + 2.3 * math.cos(a), 5.0 + 2.3 * math.sin(a), h - 0.6), (0.6, 0.6, 0.8), stone, 0.02, (0, 0, a))
    box((2, 10, 7), (8, 6, 16), stone, 0.05)
    # torches on the wall, ladders/siege kit at the foot (attackers' side)
    for x in (-5, 5):
        torch_sconce((x, 3.15, 5.5))
    wood = mat("ladder", "#7A5A3B", noise=0.3)
    for x in (-2.5, 2.8):
        box((x, 2.2, 2.0), (0.5, 0.1, 6.0), wood, 0.01, (math.radians(-12), 0, 0))
    for p in ((-4, -2.5), (3.5, -3), (6, -1.5)):
        tree((p[0], p[1] - 6, -1.2), 1.2, "#2E5A3A" if night else "#4E8A3E")
    if night:
        world("#141E3A", "#2A3866", 0.5)
        sun((35, 0, 200), "#9FB8F0", 1.2, 6)
        area((0, -10, 10), (55, 0, 0), 14, "#6A80C8", 900)
        sphere((-14, 40, 22), 2.4, mat("moon", "#FFF4E0", emit="#FFF4E0", emit_strength=4))
        point((0, 1.6, 6.9), "#FFB060", 160, 0.2)
    else:
        world("#8FD3F4", "#FFE9C7", 1.0)
        sun((50, 0, 200), "#FFE2B8", 4.0, 3)


# ---------------------------------------------------------------- lab (A-004 tickling)
def set_lab(variant="day"):
    floor = mat("labfloor", "#DDE6EA", rough=0.35, noise=0.06, bricks={"scale": 1, "c2": "#CFDADF", "mortar_c": "#B8C4CA", "w": 0.6, "h": 0.6, "mortar": 0.01, "k": 0})
    plane((0, 0, 0), (30, 30), floor)
    wall = mat("labwall", "#BFE3E8", rough=0.8, noise=0.05)
    box((0, 5.0, 2.0), (16, 0.2, 4.0), wall, 0)
    box((-6, 0, 2.0), (0.2, 12, 4.0), wall, 0)
    box((0, 4.85, 0.6), (16, 0.08, 1.2), mat("wainscot", "#0F6B78", rough=0.6), 0)
    # long bench with drawers, the robot arm, monitors with brain graphics, shelves with jars
    bench = mat("bench", "#F4F1EA", rough=0.4)
    box((0.5, 1.6, 0.47), (5.0, 1.0, 0.94), mat("benchbase", "#5B7C8A", rough=0.6), 0.03)
    box((0.5, 1.6, 0.97), (5.2, 1.1, 0.06), bench, 0.02)
    metal = mat("robotmetal", "#E8ECEF", rough=0.25, metal=0.6)
    joint = mat("robotjoint", "#FF6B5B", rough=0.4)
    cyl((1.2, 1.7, 1.06), 0.22, 0.12, joint, verts=24)
    cyl((1.2, 1.7, 1.4), 0.07, 0.6, metal, verts=16)
    sphere((1.2, 1.7, 1.72), 0.11, joint)
    cyl((1.45, 1.7, 1.86), 0.06, 0.55, metal, rot=(0, math.radians(60), 0), verts=16)
    sphere((1.7, 1.7, 2.0), 0.09, joint)
    cyl((1.85, 1.7, 1.85), 0.05, 0.4, metal, rot=(0, math.radians(140), 0), verts=16)
    box((1.98, 1.7, 1.68), (0.06, 0.06, 0.12), mat("feather", "#FFC93C", emit="#FFC93C", emit_strength=0.4), 0.02)
    scr = mat("screen", "#0D2A3A", rough=0.2, emit="#38B6D8", emit_strength=1.4)
    for x in (-1.4, 3.0):
        box((x, 2.0, 1.5), (1.1, 0.06, 0.7), mat("bezel", "#22262A"), 0.02)
        box((x, 1.96, 1.5), (1.0, 0.01, 0.6), scr, 0)
        cyl((x, 2.0, 1.1), 0.04, 0.3, mat("bezel", "#22262A"), verts=8)
    shelf = mat("shelf", "#E8E2D4", rough=0.6)
    jar = mat("jar", "#7FD6C8", rough=0.05, emit="#7FD6C8", emit_strength=0.3)
    for z in (2.2, 2.9):
        box((-2.6, 4.75, z), (3.0, 0.4, 0.05), shelf, 0.01)
        for k in range(6):
            cyl((-3.8 + k * 0.48, 4.75, z + 0.18), 0.1, 0.3, jar, verts=12)
    box((4.2, 4.8, 2.4), (2.6, 0.06, 1.4), mat("board", "#FFFFFF", rough=0.5), 0.02)
    for k in range(4):
        box((4.2 - 0.9 + k * 0.6, 4.76, 2.4 + 0.3 * math.sin(k)), (0.4, 0.01, 0.04), mat("ink", "#0F6B78"), 0)
    # stools, plant, window light
    for x in (-1.0, 2.2):
        cyl((x, 0.3, 0.35), 0.04, 0.7, metal, verts=8)
        cyl((x, 0.3, 0.72), 0.22, 0.06, mat("stool", "#FF6B5B", rough=0.5), verts=20)
    tree((-4.8, 3.8, 0), 0.35, "#5E9E4A")
    box((-5.88, 1.5, 2.3), (0.05, 2.4, 1.6), mat("labwin", "#FFF6E0", emit="#FFF6E0", emit_strength=2.5), 0)
    world("#EAF6FA", "#FFFFFF", 0.9)
    area((-4, 1.5, 3.5), (0, -70, 0), 3, "#FFF2DA", 900)
    area((1, -5, 4), (60, 0, 0), 8, "#F4FAFF", 700)
    point((0.5, 1.0, 3.6), "#FFFFFF", 240, 0.6)


sets.BUILDERS.update({"marsh": set_marsh, "arctic": set_arctic, "castle": set_castle, "lab": set_lab})
