"""Toon sets for B-003 (pirate myths). Registered into sets.BUILDERS on import.
Metres, Z up. Same conventions as sets3 (vertical and horizontal marks both work; camera clip_end 100 m).

deck  (day | sunset | night | red)   A 1710s pirate ship at sea, seen from on board. Long axis along +y (bow at +y).
    Main deck z=0, x -2.8..2.8, y -4.6..8.5; bulwarks (rails) at x=+-2.85, top z 0.95, 3 cannons each side.
    Quarterdeck (raised, z 1.3) y -8.2..-4.6 with the ship's wheel (0,-6.6) and stairs at x 1.9.
    Masts: fore (0,6.6) top z~12, main (0,1.2) top z~15 (crow's nest z 10.5), mizzen (0,-6.4) top z~10.
    Jolly Roger at the main top (red variant: plain red flag). Treasure chest (-1.7,-3.4), barrels/crates (1.9,-3.6),
    cannonball stack (-2.1,4.6), coiled rope (1.6,5.6), THE PLANK sticking out over the starboard rail at y=2.6 (x 2.9..5.4, z 0.97).
    Night: lit lanterns + cabin windows, moon and stars; sunset: low warm sun at the stern.
    Camera marks (horizontal 16:9):
      hero    pos (2.2,-7.4,3.0)  tgt (-0.2,3.0,2.4)  lens 22   from the quarterdeck over the main deck to the bow, sails above
      deck    pos (0.6,-3.2,1.45) tgt (0.0,2.2,1.05)  lens 28   eye level on the main deck (actors at y 0..2)
      plank   pos (0.6,-0.6,1.6)  tgt (4.2,2.8,0.9)   lens 26   across the deck to the plank and the sea
      flag    pos (2.0,-2.0,3.0)  tgt (0.0,1.2,14.2)  lens 30   looking up the mainmast to the flag
      wheel   pos (1.6,-3.4,2.4)  tgt (0.0,-6.6,2.0)  lens 30   back towards the wheel and the quarterdeck
      outside pos (-16,-12,3.0)   tgt (0,1,5.0)       lens 30   the whole ship from the sea

islet (day | dig | sunset)   A tiny sandy island in open sea. Sand mound centre (0,3), radius ~3.6, top z ~0.35; one palm (1.3,4.2).
    dig: a hole (-0.6,2.6) with a chest half out, a shovel and a sand heap. Distant ship (-30,60).
    Camera marks: hero pos (0.4,-4.6,1.4) tgt (0,3.2,0.9) lens 26 · wide pos (6,-14,4) tgt (0,4,0.5) lens 24

port  (day)   Caribbean port market (Port Royal style). Cobbled street y -2..6, colourful houses behind (y 9..12),
    harbour with ships at left (x<-9). Stalls: parrot stall (1.6,2.2) with 3 cages (3D parrots), fruit stall (-2.4,2.6).
    Camera marks: hero pos (0.2,-4.4,1.5) tgt (0.4,3,1.4) lens 24 · cages pos (0.4,-0.8,1.5) tgt (1.6,2.2,1.45) lens 30
"""
import math, random
import bpy
import sets
from sets import mat, box, cyl, sphere, plane, sun, area, point, barrel, crate, house, cobbles
from sets3 import (tube, loft, ring, disc, rock, rope, glow, water_mat, sky3, stars, moon, cloud, Group, mesh)


# ---------------------------------------------------------------- shared pieces

def palm(loc, s=1.0, lean=12.0, rz=0.0):
    trunk = mat("palmtrunk", "#9A7350", rough=0.9, noise=0.35, scale=6)
    leaf = mat("palmleaf", "#3E9E4A", rough=0.75, noise=0.25)
    leaf2 = mat("palmleaf2", "#2E8040", rough=0.75, noise=0.25)
    x, y, z = loc
    la = math.radians(lean); ca, sa = math.cos(math.radians(rz)), math.sin(math.radians(rz))
    pts = []
    for i in range(9):
        t = i / 8
        d = s * 4.2 * t
        off = math.sin(la) * d * (0.6 + 0.4 * t)
        pts.append((x + off * ca, y + off * sa, z + math.cos(la) * d))
    tube(pts, 0.17 * s, trunk, radii=[0.2 * s * (1 - 0.35 * i / 8) for i in range(9)])
    for k in range(5):
        ring(pts[1 + k], 0.2 * s * (1 - 0.06 * k), 0.035 * s, mat("palmring", "#7A5636", noise=0.2), 0.3)
    tx, ty, tz = pts[-1]
    for k in range(9):
        a = k / 9 * math.tau
        fr = []
        for j in range(6):
            u = j / 5
            r = s * 2.3 * u
            fr.append((tx + r * math.cos(a), ty + r * math.sin(a), tz + s * (0.35 * math.sin(u * math.pi) - 0.9 * u * u)))
        tube(fr, 0.16 * s, leaf if k % 2 else leaf2, radii=[0.05 * s, 0.22 * s, 0.26 * s, 0.22 * s, 0.14 * s, 0.03 * s])
    for k in range(3):
        sphere((tx + 0.18 * s * math.cos(k * 2.1), ty + 0.18 * s * math.sin(k * 2.1), tz - 0.15 * s), 0.13 * s, mat("coconut", "#6B4A2E", noise=0.3))


def sea(variant, z=-2.4, size=260):
    col = {"day": "#1E8FB8", "sunset": "#2B6E9A", "night": "#0E2A4A", "red": "#1E8FB8", "dig": "#1E8FB8"}.get(variant, "#1E8FB8")
    m = water_mat("sea_" + variant, col, alpha=1.0, rough=0.08, wave=0.35, wave_scale=0.9, emit=0.08 if variant == "night" else 0.0)
    plane((0, 40, z), (size, size), m)


def sky_for(variant, R):
    if variant == "night":
        sky3([(0.0, "#22406E"), (0.08, "#16305A"), (0.35, "#0C1D40"), (1.0, "#050B20")], 0.7)
        stars(R, 160, 92, (-90, 90), (6, 70), 9)
        moon((24, 88, 40), 3.2, 6.0, 4.5)
        sun((52, 0, 150), "#A8C4FF", 2.0, 5)
        area((0, -10, 9), (55, 0, 0), 16, "#6E96E0", 450)
    elif variant == "sunset":
        sky3([(0.0, "#FFB070"), (0.06, "#FF8A5C"), (0.22, "#C8607A"), (0.5, "#5E4A8C"), (1.0, "#22305E")], 1.0)
        sun((8, 0, 185), "#FFB070", 4.0, 3)
        area((0, -12, 8), (55, 0, 0), 16, "#FFC8A0", 380)
        glow((-6, -80, 4), 9, "#FFC070", 2.4, 2.4, facing="y")
    else:
        sky3([(0.0, "#FFF0D0"), (0.05, "#BDE6F6"), (0.3, "#7CC6EE"), (1.0, "#3E8ED8")], 1.0)
        sun((48, 0, 30), "#FFE6B8", 4.6, 3)
        area((0, -12, 8), (55, 0, 0), 16, "#FFF1D6", 340)
        cm = mat("cloudw", "#FFFFFF", rough=0.9, noise=0.05, emit="#FFFFFF", emit_strength=0.35)
        for (cx, cy, cz, s) in ((-30, 85, 22, 4), (18, 88, 28, 5), (45, 80, 18, 3.5), (-60, 70, 14, 3), (65, 62, 12, 3)):
            cloud((cx, cy, cz), s, cm)


def sail_mesh(name, cx, y, z0, z1, w0, w1, bulge, m, n=8):
    """Square sail billowing towards +y: bottom width w0 at z0, top width w1 at z1."""
    verts, faces = [], []
    for j in range(n + 1):
        v = j / n
        z = z0 + (z1 - z0) * v
        w = w0 + (w1 - w0) * v
        for i in range(n + 1):
            u = i / n
            x = cx - w / 2 + w * u
            b = bulge * math.sin(math.pi * u) * (0.35 + 0.65 * math.sin(math.pi * min(1.0, v * 1.15)))
            verts.append((x, y + b, z))
    for j in range(n):
        for i in range(n):
            a = j * (n + 1) + i
            faces.append((a, a + 1, a + n + 2, a + n + 1))
    o = mesh(name, verts, faces, m, smooth=True)
    mod = o.modifiers.new("sol", "SOLIDIFY"); mod.thickness = 0.03
    return o


def far_ship(loc, rz=0.0, s=1.0, sailc="#F4EBD6"):
    hull = mat("farhull", "#5B3A29", rough=0.8, noise=0.2)
    sl = mat("farsail" + sailc, sailc, rough=0.9, noise=0.05, emit=sailc, emit_strength=0.15)
    with Group(loc, (0, 0, rz)):
        box((0, 0, 0.6 * s), (1.6 * s, 7 * s, 1.4 * s), hull, 0.2 * s)
        box((0, -3.0 * s, 1.6 * s), (1.5 * s, 1.4 * s, 0.9 * s), hull, 0.1 * s)
        for (yy, h) in ((2.2, 7.5), (0, 9), (-2.2, 6.5)):
            cyl((0, yy * s, h * s / 2 + 1.0 * s), 0.08 * s, h * s, hull, verts=6)
            for k in range(2):
                box((0, yy * s + 0.2 * s, (2.6 + k * 2.4) * s + (h - 7.5) * 0.4 * s), (2.8 * s * (1 - 0.18 * k), 0.12 * s, 2.0 * s), sl, 0.1 * s)


# ---------------------------------------------------------------- deck

def _cannon(x, y, side):
    iron = mat("cannon", "#2A2A30", rough=0.4, metal=0.6, noise=0.1)
    wood = mat("carriage", "#7A4E32", noise=0.25)
    box((x - side * 0.35, y, 0.25), (0.9, 0.7, 0.28), wood, 0.04)
    for dy in (-0.32, 0.32):
        cyl((x - side * 0.15, y + dy, 0.2), 0.18, 0.06, wood, rot=(0, 0, 0), verts=14)
    # barrel points outward through the rail: muzzle (r2) at +side, breech knob inboard
    cyl((x + side * 0.2, y, 0.6), 0.16, 1.5, iron, verts=16, rot=(0, math.radians(side * 90 - side * 4), 0), r2=0.12)
    sphere((x - side * 0.58, y, 0.6), 0.13, iron, sub=2)


def _jolly(loc, red=False):
    """Flag on the main top, flying towards +x (seen from the deck). Black with a white skull and crossed bones."""
    x, y, z = loc
    if red:
        box((x + 1.3, y, z), (2.6, 0.04, 1.7), mat("redflag", "#C8282C", rough=0.85, noise=0.1, emit="#C8282C", emit_strength=0.15), 0.01)
        return
    box((x + 1.3, y, z), (2.6, 0.04, 1.7), mat("blackflag", "#141418", rough=0.9, noise=0.08), 0.01)
    wm = mat("bone", "#F4F0E6", rough=0.6, noise=0.05, emit="#F4F0E6", emit_strength=0.25)
    ink = mat("blackflag", "#141418", rough=0.9, noise=0.08)
    for sgn in (-1, 1):
        sphere((x + 1.3, y - sgn * 0.035, z + 0.22), 0.36, wm, scale=(1.0, 0.08, 1.0), sub=2)               # skull
        box((x + 1.3, y - sgn * 0.035, z - 0.12), (0.4, 0.06, 0.2), wm, 0.04)                               # jaw
        for ex in (-0.13, 0.13):
            sphere((x + 1.3 + ex, y - sgn * 0.06, z + 0.2), 0.09, ink, scale=(1.0, 0.1, 1.15), sub=1)       # eye holes
        for a in (35, -35):                                                                                 # crossed bones
            box((x + 1.3, y - sgn * 0.03, z - 0.5), (1.4, 0.05, 0.11), wm, 0.04, rot=(0, math.radians(a), 0))
            for e in (-1, 1):
                sphere((x + 1.3 + e * 0.66 * math.cos(math.radians(a)), y - sgn * 0.035, z - 0.5 - e * 0.66 * math.sin(math.radians(a))), 0.09, wm, sub=1)


def set_deck(variant="day"):
    R = random.Random(31)
    night = variant == "night"
    plank_m = mat("deckplank", "#E2B47E", rough=0.75, noise=0.2,
                  bricks={"scale": 1.5, "c2": "#D2A26C", "mortar_c": "#6A4A30", "w": 2.4, "h": 0.2, "mortar": 0.012, "k": 1})
    hull = mat("piratehull", "#5E3A26", rough=0.8, noise=0.3)
    wale = mat("piratewale", "#2B1E18", rough=0.7, noise=0.2)
    trim = mat("piratetrim", "#C8962E", rough=0.5, noise=0.15, metal=0.2)
    rail = mat("piraterail", "#8A5A3B", rough=0.75, noise=0.25)
    spar = mat("piratespar", "#7A5236", rough=0.8, noise=0.2)
    rig = mat("piraterig", "#2E2420", rough=0.9, noise=0)
    sailm = mat("piratesail", "#F2E8D2", rough=0.9, noise=0.12, emit="#F2E8D2", emit_strength=0.06)
    sea(variant)
    # hull below the deck (seen from outside and over the rails)
    def half_w(y):
        if y > 6.0:
            return 2.85 * max(0.05, math.cos((y - 6.0) / 4.4 * math.pi / 2) ** 0.7)
        return 2.85
    ys = [-8.4 + i * 0.6 for i in range(32)]
    rings = []
    for y in ys:
        w = half_w(y)
        zt = -0.12                       # hull closes just under the deck (the loft joins its last and first point)
        rings.append([(-w, y, zt), (-w * 1.05, y, -1.2), (-w * 0.6, y, -2.8), (0, y, -3.1), (w * 0.6, y, -2.8), (w * 1.05, y, -1.2), (w, y, zt)])
    o = loft([[(p[0], p[1], p[2]) for p in r] for r in rings], hull, caps=True)
    for zz, m in ((-0.6, wale), (0.2, trim)):
        for sgn in (-1, 1):
            tube([(sgn * half_w(y) * (1.06 if zz < 0 else 1.01), y, zz) for y in ys], 0.08, m)
    # main deck and quarterdeck
    for y0 in range(0, 13):
        y = -4.6 + y0 + 0.5
        w = half_w(y)
        box((0, y, -0.05), (2 * w - 0.05, 1.0, 0.1), plank_m, 0.0)
    box((0, -6.4, 0.6), (5.6, 3.6, 1.3), plank_m, 0.02)
    box((0, -4.6, 0.65), (5.6, 0.12, 1.3), rail, 0.02)                                # quarterdeck front face
    for k in range(9):                                                                # balustrade
        cyl((-2.4 + k * 0.6, -4.62, 1.6), 0.05, 0.6, rail, verts=8)
    box((0, -4.62, 1.92), (5.5, 0.14, 0.08), rail, 0.02)
    for k in range(5):                                                                # stairs (starboard)
        box((1.95, -4.15 - k * 0.0, 0.13 + k * 0.26), (0.9, 0.9 - k * 0.16, 0.26), plank_m, 0.01)
    door = mat("cabindoor", "#4E3420", noise=0.2)
    box((-1.2, -4.53, 0.55), (0.75, 0.05, 1.05), door, 0.02)
    win = mat("cabinwin", "#FFD88A", rough=0.3, emit="#FFB850", emit_strength=6 if night else 0.6, noise=0)
    box((0.2, -4.53, 0.75), (0.4, 0.05, 0.35), win, 0.01)
    # bulwarks with rail caps along both sides
    for sgn in (-1, 1):
        pts = [(sgn * (half_w(y) - 0.06), y, 0.5) for y in [-4.6 + i * 0.5 for i in range(30)] if y < 10.2]
        for (px, py, pz) in pts[:-1]:
            box((px, py + 0.25, pz), (0.12, 0.52, 0.95), rail, 0.01)
        tube([(sgn * half_w(y), y, 0.98) for y in [-4.6 + i * 0.5 for i in range(30)] if y < 10.2], 0.07, wale)
        for y in (-1.8, 0.6, 3.6):
            _cannon(sgn * 2.35, y, sgn)
        box((sgn * 2.85, -6.4, 1.75), (0.12, 3.6, 0.9), rail, 0.01)                   # quarterdeck rails
    # wheel
    wheelm = mat("wheel", "#7A4E32", noise=0.2)
    box((0, -6.75, 1.75), (0.35, 0.3, 0.9), wheelm, 0.03)
    with Group((0, -6.55, 2.3), (math.radians(90), 0, 0)):
        ring((0, 0, 0), 0.55, 0.05, wheelm, 1.0)
        for k in range(8):
            a = k / 8 * math.tau
            cyl((0.35 * math.cos(a), 0.35 * math.sin(a), 0), 0.025, 0.7, wheelm, verts=6, rot=(0, math.radians(90), a))
            cyl((0.68 * math.cos(a), 0.68 * math.sin(a), 0), 0.03, 0.22, wheelm, verts=6, rot=(0, math.radians(90), a))
        cyl((0, 0, 0), 0.09, 0.12, trim, verts=12)
    # masts, yards, sails, rigging, crow's nest
    tops = {}
    for name, my, h, yards in (("fore", 6.6, 12.0, (5.0, 3.8)), ("main", 1.2, 15.0, (6.2, 4.6, 3.0)), ("mizzen", -6.4, 10.0, (3.4,))):
        zb = 1.3 if my < -4.6 else 0.0
        cyl((0, my, zb + h / 2), 0.2, h, spar, verts=12, r2=0.1)
        tops[name] = (my, zb + h)
        for k, yw in enumerate(yards):
            zz = zb + h * (0.42 + 0.24 * k)
            cyl((0, my + 0.15, zz), 0.08, yw, spar, verts=8, rot=(0, math.radians(90), 0))
            nxt = zb + h * (0.42 + 0.24 * (k - 1)) if k else zb + 2.4
            sail_mesh(f"sail_{name}{k}", 0, my + 0.2, nxt + 0.25, zz - 0.1, yw * 0.98, yw * 0.88, 0.75 - 0.15 * k, sailm)
            for sgn in (-1, 1):
                tube([(sgn * yw / 2, my + 0.15, zz), (0, my, zz + h * 0.18)], 0.02, rig, smooth=False)
        if name == "main":
            cyl((0, my, zb + h * 0.7), 0.75, 0.12, spar, verts=16)
            cyl((0, my, zb + h * 0.7 + 0.45), 0.72, 0.8, rail, verts=16)                  # crow's nest
        for sgn in (-1, 1):                                                             # shrouds with ratlines
            for dy in (-0.6, 0.0, 0.6):
                tube([(0, my, zb + h * 0.68), (sgn * 2.8, my + dy, zb + 1.0)], 0.022, rig, smooth=False)
            for kk in range(7):
                u = (kk + 1) / 8
                zz = zb + 1.0 + (h * 0.68 - 1.0) * u
                xx = sgn * 2.8 * (1 - u)
                tube([(xx, my - 0.6 * (1 - u), zz), (xx, my + 0.6 * (1 - u), zz)], 0.012, rig, smooth=False)
    cyl((0, 11.4, 2.2), 0.14, 6.0, spar, verts=10, rot=(math.radians(-62), 0, 0))     # bowsprit
    tube([(0, 13.8, 3.6), (0, tops["fore"][0], tops["fore"][1] - 0.4)], 0.025, rig, smooth=False)
    tube([(0, tops["fore"][0], tops["fore"][1] - 0.3), (0, tops["main"][0], tops["main"][1] - 1.5)], 0.025, rig, smooth=False)
    tube([(0, tops["main"][0], tops["main"][1] - 0.4), (0, tops["mizzen"][0], tops["mizzen"][1] - 0.3)], 0.025, rig, smooth=False)
    _jolly((0.1, tops["main"][0], tops["main"][1] - 0.6), red=(variant == "red"))
    # props on deck
    chest = mat("chest", "#7A4E32", noise=0.25)
    with Group((-1.7, -3.4, 0), (0, 0, math.radians(15))):
        box((0, 0, 0.3), (1.0, 0.62, 0.6), chest, 0.04)
        cyl((0, 0.0, 0.62), 0.31, 1.0, chest, verts=16, rot=(0, math.radians(90), 0))
        for x in (-0.35, 0.35):
            box((x, 0, 0.5), (0.08, 0.66, 0.95), trim, 0.01)
        box((0, -0.32, 0.55), (0.14, 0.04, 0.16), trim, 0.01)
    for (x, y, s) in ((1.9, -3.6, 0.85), (2.2, -2.8, 0.75), (1.4, -3.9, 0.7)):
        barrel((x, y, 0), s)
    crate((2.1, 6.4, 0), 0.7, 0.3); crate((-2.0, 7.0, 0), 0.6, -0.2)
    ballm = mat("cannonball", "#26262C", rough=0.4, metal=0.6)
    for (bx, by, bz) in [(i * 0.26 - 0.26, j * 0.26 - 0.13, 0.13) for i in range(3) for j in range(2)] + [(-0.13, 0, 0.34), (0.13, 0, 0.34)]:
        sphere((-2.1 + bx, 4.6 + by, bz), 0.13, ballm, sub=2)
    ropem = mat("rope", "#B89A6A", rough=0.9, noise=0.3, scale=8)
    for k in range(4):
        ring((1.6, 5.6, 0.05 + k * 0.07), 0.38 - k * 0.05, 0.05, ropem, 1.0)
    # the plank over the starboard rail
    pm = mat("plank", "#B07A4A", rough=0.8, noise=0.25, scale=5)
    box((4.1, 2.6, 0.99), (3.0, 0.42, 0.07), pm, 0.01)
    box((2.5, 2.6, 1.1), (0.25, 0.5, 0.18), mat("plankrope", "#B89A6A", rough=0.9), 0.02)
    # lanterns
    for (lx, ly, lz) in ((0.4, -4.7, 2.5), (-0.4, 1.0, 3.0), (0.0, 6.2, 2.6)):
        cyl((lx, ly, lz), 0.12, 0.26, mat("lanternglass", "#FFD27A", emit="#FFB84D", emit_strength=9 if night else 0.8, noise=0), verts=8)
        cyl((lx, ly, lz + 0.18), 0.15, 0.08, wale, verts=8, r2=0.04)
        if night:
            point((lx, ly - 0.25, lz), "#FFB060", 140, 0.15)
    if night:
        point((0, -4.0, 1.2), "#FFB060", 160, 0.3)
    # horizon: island with palms, a merchant ship
    sand = mat("islesand", "#F2D9A2", rough=0.9, noise=0.2)
    sphere((34, 70, -3.4), 9, sand, scale=(1.6, 1.0, 0.32), sub=3)
    for (px, py) in ((30, 66), (36, 68), (40, 72)):
        palm((px, py, -1.2), 1.6, R.uniform(6, 16), R.uniform(0, 360))
    far_ship((-36, 62, -2.6), math.radians(70), 1.0)
    sky_for("day" if variant == "red" else variant, R)
    fill = {"night": ("#7E9EE8", 260), "sunset": ("#FFC8A0", 520)}.get(variant, ("#FFF1D6", 700))
    area((0, 0.5, 9.5), (0, 0, 0), 12, fill[0], fill[1])          # soft fill under the sails so the deck and actors read
    area((0, -12, 3.5), (78, 0, 0), 10, fill[0], fill[1] * 0.5)


# ---------------------------------------------------------------- islet

def set_islet(variant="day"):
    R = random.Random(37)
    sea("day" if variant == "dig" else variant, z=-0.25, size=240)
    sand = mat("isletsand", "#F4DCA6", rough=0.92, noise=0.25, scale=2)
    wet = mat("isletwet", "#D8BC86", rough=0.6, noise=0.2)
    sphere((0, 3, -1.65), 4.4, wet, scale=(1.25, 1.0, 0.45), sub=4)
    sphere((0, 3, -1.55), 4.1, sand, scale=(1.2, 0.95, 0.46), sub=4)
    palm((1.3, 4.2, 0.2), 1.0, 14, 200)
    for (x, y, s) in ((-2.4, 4.4, 0.35), (2.6, 1.8, 0.25), (-1.0, 5.6, 0.3)):
        rock((x, y, 0.0), s, mat("islerock", "#8A8478", noise=0.3), R.uniform(0, 3), 0.6)
    for k in range(5):
        disc((R.uniform(-2.5, 2.5), R.uniform(1.2, 5.0), 0.31), R.uniform(0.06, 0.1), mat("shell", "#FFE8E0", noise=0.1), (0.9, 1.3, 1))
    if variant == "dig":
        disc((-0.6, 2.6, 0.33), 0.75, mat("hole", "#8A6A40", rough=1.0, noise=0.3), (1.2, 1, 1))
        sphere((0.6, 2.2, 0.2), 0.7, sand, scale=(1.3, 1.0, 0.5), sub=3)
        chest = mat("chest", "#7A4E32", noise=0.25)
        trim = mat("piratetrim", "#C8962E", rough=0.5, noise=0.15, metal=0.2)
        with Group((-0.6, 2.6, 0.1), (math.radians(-10), 0, math.radians(20))):
            box((0, 0, 0.25), (0.9, 0.56, 0.5), chest, 0.04)
            for x in (-0.3, 0.3):
                box((x, 0, 0.3), (0.07, 0.6, 0.52), trim, 0.01)
            with Group((0, 0.28, 0.5), (math.radians(-55), 0, 0)):
                box((0, -0.28, 0.08), (0.9, 0.56, 0.12), chest, 0.03)
            gold = mat("gold", "#FFC93C", rough=0.3, metal=0.8, emit="#FFB020", emit_strength=0.4)
            for k in range(14):
                cyl((R.uniform(-0.35, 0.35), R.uniform(-0.2, 0.2), 0.48 + R.uniform(0, 0.06)), 0.06, 0.015, gold, verts=12)
        sh = mat("shovelwood", "#9A6A40", noise=0.2)
        cyl((1.1, 2.5, 0.75), 0.03, 1.4, sh, verts=6, rot=(math.radians(20), math.radians(-15), 0))
        box((1.3, 2.75, 0.15), (0.26, 0.04, 0.3), mat("shovelblade", "#6A6A70", metal=0.6, rough=0.4), 0.02, (math.radians(20), 0, 0))
    far_ship((-30, 60, -0.6), math.radians(60), 1.0)
    sky_for("sunset" if variant == "sunset" else "day", R)


# ---------------------------------------------------------------- port market

def _parrot3d(loc, s=1.0, body="#E8392E", wing="#2E7FD8", rz=0.0):
    with Group(loc, (0, 0, math.radians(rz))):
        bm = mat("parrot" + body, body, rough=0.6, noise=0.1)
        wm = mat("parrotw" + wing, wing, rough=0.6, noise=0.1)
        sphere((0, 0, 0.18 * s), 0.13 * s, bm, scale=(0.9, 0.85, 1.25), sub=2)
        sphere((0, 0.04 * s, 0.38 * s), 0.1 * s, bm, sub=2)
        sphere((0.07 * s, 0.1 * s, 0.4 * s), 0.035 * s, mat("parroteye", "#FFFFFF", noise=0), sub=1)
        sphere((0.085 * s, 0.13 * s, 0.4 * s), 0.018 * s, mat("parrotpup", "#1E1A24", noise=0), sub=1)
        cyl((0, 0.13 * s, 0.34 * s), 0.045 * s, 0.1 * s, mat("beak", "#F4E8C8", noise=0.05), verts=8, rot=(math.radians(-70), 0, 0), r2=0.005)
        for sgn in (-1, 1):
            sphere((sgn * 0.11 * s, -0.02 * s, 0.17 * s), 0.08 * s, wm, scale=(0.4, 0.9, 1.4), sub=2)
        box((0, -0.12 * s, -0.04 * s), (0.08 * s, 0.05 * s, 0.32 * s), wm, 0.02 * s, (math.radians(-20), 0, 0))


def _cage(loc, s=1.0, bird=("#E8392E", "#2E7FD8")):
    wire = mat("cagewire", "#C8962E", rough=0.4, metal=0.7)
    x, y, z = loc
    cyl((x, y, z), 0.3 * s, 0.05 * s, wire, verts=16)
    for k in range(12):
        a = k / 12 * math.tau
        tube([(x + 0.29 * s * math.cos(a), y + 0.29 * s * math.sin(a), z), (x + 0.29 * s * math.cos(a), y + 0.29 * s * math.sin(a), z + 0.55 * s),
              (x + 0.05 * s * math.cos(a), y + 0.05 * s * math.sin(a), z + 0.78 * s)], 0.008 * s, wire)
    ring((x, y, z + 0.8 * s), 0.07 * s, 0.015 * s, wire, 1.0)
    cyl((x, y, z + 0.25 * s), 0.012 * s, 0.56 * s, wire, verts=6, rot=(0, math.radians(90), 0))
    _parrot3d((x, y, z + 0.25 * s), 0.85 * s, bird[0], bird[1], rz=200)


def set_port(variant="day"):
    R = random.Random(41)
    cobbles(60, "#C9B48E", "#B6A07C")
    sea("day", z=-0.8, size=200)
    box((-9.5, 10, -0.4), (1.0, 40, 0.9), mat("quay", "#A89C88", noise=0.3), 0.02)
    cols = ["#FFD27A", "#7FD4C8", "#FF9A7A", "#F4F0E6", "#9FC8F0", "#F2B8D0"]
    for k, x in enumerate((-6.5, -2.5, 1.5, 5.5, 9.5, 13.5)):
        house((x, 11, 0), 3.8, 3.2, 5.5 + (k % 2) * 1.2, wall=cols[k], roof="#B85A3A" if k % 2 else "#8A4A3A", timber=False, floors=2)
    for (x, y, rz) in ((-16, 14, 80), (-22, 26, 100), (-14, 34, 60)):
        far_ship((x, y, -1.4), math.radians(rz), 0.9)
    for (px, py) in ((-8.2, 5.5), (8.6, 7.2), (12, 4.4), (-7.6, 8.8)):
        palm((px, py, 0), 1.1, R.uniform(6, 14), R.uniform(0, 360))
    wood = mat("stallwood", "#9A6A40", noise=0.25)
    for (sx, sy, awn) in ((1.6, 2.2, ("#FF6B5B", "#FFF4E0")), (-2.4, 2.6, ("#2E8CB8", "#FFF4E0"))):
        box((sx, sy, 0.45), (2.4, 0.9, 0.9), wood, 0.03)
        box((sx, sy - 0.05, 0.92), (2.5, 1.0, 0.06), mat("stalltop", "#B5824E", noise=0.2), 0.01)
        for dx in (-1.15, 1.15):
            cyl((sx + dx, sy + 0.45, 1.25), 0.05, 2.5, wood, verts=8)
            cyl((sx + dx, sy - 0.45, 1.0), 0.05, 2.0, wood, verts=8)
        for k in range(8):
            c = awn[k % 2]
            box((sx - 1.1 + k * 0.315, sy, 2.25), (0.315, 1.4, 0.04), mat("awn" + c, c, rough=0.8), 0.005, (math.radians(-14), 0, 0))
    for k, (dx, bird) in enumerate(((-0.7, ("#E8392E", "#2E7FD8")), (0.0, ("#2EAE5A", "#FFC93C")), (0.7, ("#2E8CD8", "#FFC93C")))):
        _cage((1.6 + dx, 2.1, 0.95), 0.9, bird)
    _parrot3d((2.75, 2.0, 1.95), 0.9, "#FFC93C", "#2EAE5A", rz=210)                        # one on the awning pole
    for k in range(7):
        sphere((-3.2 + k * 0.26, 2.4 + (k % 2) * 0.12, 1.06), 0.12, mat("fruit" + str(k % 4), ["#FF9A3C", "#FFC93C", "#5E9E4A", "#FF6B5B"][k % 4]))
    for k in range(3):
        barrel((-4.6 + k * 0.1, 3.6 + k * 0.7, 0), 0.8)
    crate((4.2, 3.4, 0), 0.7, 0.4)
    sky_for("day", R)


sets.BUILDERS.update({"deck": set_deck, "islet": set_islet, "port": set_port})
