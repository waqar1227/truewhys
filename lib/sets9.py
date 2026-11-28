"""Toon sets for B-009 (L9 "Why Planes Dim the Lights to Land"). Registered into sets.BUILDERS on import. TrueWhys original.
Metres, Z up. Palette (episodes/B-009-flight-secrets/look.md): indigo #1B2550, amber #F2A33A, bone #ECE3CF, petrol #2C6E73, red #D64A3B.
Variants may end in "_bg" (hide collection FG) or "_fg" (only collection FG, transparent film) for 2D-cast compositing layers.

cabin  (day | night | dim)   Airliner cabin, aisle along +y (nose at +y). Floor z=0, cabin x -1.85..1.85, ceiling z 2.15.
    Seat rows (3+3) at y = ROW_Y[k] (k=0..9, 0.82 m pitch, row 0 at y=0); seats face +y; aisle x -0.28..0.28.
    Seat centres x: left -1.38,-0.88,-0.43 (window, middle, aisle) / right 0.43,0.88,1.38. Seat cushion top z 0.46, back top z 1.12.
    Oval windows on both walls at each row, centre z 1.12. Overhead bins z 1.62..2.02. Floor-path light strips at x=+-0.30.
    day = bright ceiling wash + sunlight through windows; night = warm reading lights, dark windows with city lights;
    dim = landing at night: ceiling off, faint blue, only floor strips + exit signs glow.
    FG collection = the row in front of row 3 (row 4 seat backs) for the "row" mark.
    Camera marks (16:9):
      aisle    pos (0,-1.4,1.55)   tgt (0,9,1.25)    lens 22   down the aisle from the back
      row      pos (-0.95,3.8,1.62) tgt (-0.95,2.2,1.02) lens 26   facing row 3 (left block); FG = camera-facing seat backs at y 3.18
      window   pos (-0.95,2.75,1.2) tgt (-1.85,2.6,1.15) lens 30  over the shoulder at the row-3 window
"""
import math, random
import bpy
import sets
from sets import mat, cyl, sphere, world, sun, area, point, hexrgb


def box(loc, half, m, bevel=0.04, rot=(0, 0, 0)):
    """Box from half-extents (sets.box takes full sizes)."""
    return sets.box(loc, [2 * h for h in half], m, bevel, rot)


def plane(loc, half, m, rot=(0, 0, 0)):
    return sets.plane(loc, [2 * half[0], 2 * half[1]], m, rot)

INDIGO, AMBER, BONE, PETROL, RED = "#1B2550", "#F2A33A", "#ECE3CF", "#2C6E73", "#D64A3B"
ROW_Y = [k * 0.82 for k in range(10)]
SEAT_X = [-1.38, -0.88, -0.43, 0.43, 0.88, 1.38]


def _coll(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def _to(coll, objs):
    for o in objs:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        coll.objects.link(o)


def _emit(name, color, strength):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = hexrgb(color); e.inputs["Strength"].default_value = strength
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(e.outputs[0], o.inputs[0])
    return m


def seat(x, y, m_seat, m_cover, m_frame):
    objs = []
    objs.append(box((x, y, 0.40), (0.24, 0.25, 0.07), m_seat, bevel=0.05))                           # cushion
    objs.append(box((x, y - 0.24, 0.80), (0.24, 0.06, 0.34), m_seat, bevel=0.05, rot=(math.radians(-8), 0, 0)))  # back
    objs.append(box((x, y - 0.21, 1.06), (0.16, 0.035, 0.07), m_cover, bevel=0.03, rot=(math.radians(-8), 0, 0)))  # headrest cover
    objs.append(box((x, y - 0.31, 0.78), (0.18, 0.01, 0.12), m_frame, bevel=0.01, rot=(math.radians(-8), 0, 0)))   # tray (stowed)
    for sx in (-0.25, 0.25):
        objs.append(box((x + sx, y - 0.02, 0.58), (0.025, 0.2, 0.025), m_frame, bevel=0.01))      # armrest
    objs.append(box((x, y, 0.17), (0.2, 0.2, 0.17), m_frame, bevel=0.02))                            # base
    return objs


def seat_rear(x, yb, m_seat, m_cover, m_frame):
    """The back of a seat seen from the row behind (tray table, pocket, latch), its rear face towards -y at y=yb."""
    o = [box((x, yb + 0.06, 0.78), (0.24, 0.06, 0.36), m_seat, bevel=0.05)]
    o.append(box((x, yb - 0.005, 0.86), (0.18, 0.012, 0.13), mat("tray", "#3F8086", rough=0.6, noise=0.05), bevel=0.012))   # tray (stowed)
    o.append(box((x, yb - 0.015, 1.0), (0.04, 0.008, 0.012), m_frame, bevel=0.003))                                        # latch
    o.append(box((x, yb - 0.01, 0.55), (0.19, 0.02, 0.09), mat("pocket", "#24585C", rough=0.9, noise=0.1), bevel=0.02))     # pocket
    o.append(box((x - 0.05, yb - 0.03, 0.6), (0.06, 0.004, 0.08), mat("card", "#FFF4E0", rough=0.6, noise=0.0), bevel=0.0, rot=(0, 0.08, 0)))
    o.append(box((x, yb + 0.06, 1.16), (0.17, 0.05, 0.05), m_cover, bevel=0.03))
    o.append(box((x, yb + 0.3, 0.38), (0.24, 0.3, 0.08), m_seat, bevel=0.05))          # its cushion (seen from behind)
    o.append(box((x, yb + 0.3, 0.16), (0.2, 0.24, 0.16), m_frame, bevel=0.02))         # base
    return o


def set_cabin(variant):
    base = variant.split("_")[0]
    layer = variant.split("_")[1] if "_" in variant else None
    night = base in ("night", "dim")
    m_floor = mat("carpet", "#3A3F5C", rough=0.95, noise=0.25, scale=40)
    m_aisle = mat("aisle", "#7A2E33", rough=0.95, noise=0.2, scale=50)
    m_wall = mat("wall", BONE, rough=0.6, noise=0.04)
    m_bin = mat("bin", "#F4EFE3", rough=0.45, noise=0.03)
    m_seat = mat("seat", PETROL, rough=0.85, noise=0.15, scale=30)
    m_cover = mat("cover", "#F6F1E6", rough=0.8, noise=0.05)
    m_frame = mat("frame", "#5B5F6B", rough=0.4, noise=0.02, metal=0.3)
    m_glassdark = _emit("win_night", "#0E1A3A", 0.6) if night else _emit("win_day", "#BFE4FF", 3.0)
    m_strip = _emit("strip", AMBER, 14.0 if base == "dim" else 1.5)
    m_exit = _emit("exit", "#6BFF8E", 8.0 if base == "dim" else 3.0)
    m_ceilglow = _emit("ceil", "#FFF3DA", {"day": 4.0, "night": 1.6, "dim": 0.0}[base])
    m_reading = _emit("read", "#FFE2A8", 6.0) if base == "night" else mat("readoff", "#CFC8B8", rough=0.4, noise=0.0)
    L = len(ROW_Y) * 0.82 + 3
    plane((0, L / 2 - 2, 0), (1.85, L / 2 + 2, 1), m_floor)
    plane((0, L / 2 - 2, 0.002), (0.28, L / 2 + 2, 1), m_aisle)
    for sx in (-1, 1):
        # lower wall (sloped), window belt, upper wall
        box((sx * 1.9, L / 2 - 2, 0.55), (0.05, L / 2 + 2, 0.55), m_wall, bevel=0.0)
        box((sx * 1.86, L / 2 - 2, 1.38), (0.05, L / 2 + 2, 0.32), m_wall, bevel=0.0)
        for k, y in enumerate(ROW_Y + [ROW_Y[-1] + 0.82]):
            fr = box((sx * 1.835, y - 0.12, 1.22), (0.03, 0.17, 0.25), mat("winframe", "#D9D0BC", rough=0.5, noise=0.02), bevel=0.12)
            w = box((sx * 1.80, y - 0.12, 1.22), (0.02, 0.12, 0.185), m_glassdark, bevel=0.09)
        # overhead bins (slanted fronts)
        box((sx * 1.45, L / 2 - 2, 1.82), (0.42, L / 2 + 2, 0.2), m_bin, bevel=0.06)
        box((sx * 1.05, L / 2 - 2, 1.66), (0.03, L / 2 + 2, 0.05), m_frame, bevel=0.01)
        for k, y in enumerate(ROW_Y):
            box((sx * 1.05, y + 0.3, 1.72), (0.035, 0.08, 0.02), m_frame, bevel=0.005)        # bin latches
            if not (sx < 0 and abs(y - 0.05 - 3.8) < 1.9):   # no bulb right in front of the row camera (-0.95, 3.8, 1.62)
                sphere((sx * 1.0, y - 0.05, 1.6), 0.03, m_reading)                             # reading lights
        # floor-path light strip
        box((sx * 0.31, L / 2 - 2, 0.006), (0.015, L / 2 + 2, 0.006), m_strip, bevel=0.0)
    # ceiling + light cove
    box((0, L / 2 - 2, 2.2), (1.9, L / 2 + 2, 0.05), m_wall, bevel=0.0)
    box((0, L / 2 - 2, 2.14), (0.5, L / 2 + 2, 0.01), m_ceilglow, bevel=0.0)
    # bulkhead + exit sign at the front
    box((0, ROW_Y[-1] + 1.6, 1.1), (1.9, 0.05, 1.1), m_wall, bevel=0.0)
    box((0, ROW_Y[-1] + 1.57, 0.95), (0.4, 0.02, 0.95), mat("door", "#C9C0AC", rough=0.5, noise=0.03), bevel=0.02)
    box((0, ROW_Y[-1] + 1.55, 2.02), (0.2, 0.02, 0.07), m_exit, bevel=0.0)
    fg = []
    for k, y in enumerate(ROW_Y):
        for x in SEAT_X:
            objs = seat(x, y, m_seat, m_cover, m_frame)
            if k == 4 and x < 0:
                for o in objs:
                    o.hide_render = True        # row 4 (left block) is replaced by camera-facing seat backs (FG)
    for x in SEAT_X[:3]:
        fg += seat_rear(x, ROW_Y[3] + 0.72, m_seat, m_cover, m_frame)
    if fg:
        _to(_coll("FG"), fg)
    # lights + world
    if base == "day":
        world("#9FD8FF", "#FFF3DA", 0.4)
        area((0, 4, 2.05), (0, 0, 0), 3.0, "#FFF6E8", 260)
        area((0, -1, 2.05), (0, 0, 0), 2.0, "#FFF6E8", 120)
        sun((60, 0, -70), "#FFE7C2", 3.0, 3.0)
    elif base == "night":
        world("#0B1430", "#1B2550", 0.15)
        area((0, 4, 2.05), (0, 0, 0), 3.0, "#FFD9A0", 70)
        area((0, -1, 2.05), (0, 0, 0), 2.0, "#FFD9A0", 30)
    else:
        world("#0B1430", "#1B2550", 0.25)
        area((0, 4, 2.05), (0, 0, 0), 3.0, "#6F8BD8", 28)
        area((0, -1, 2.05), (0, 0, 0), 2.0, "#6F8BD8", 12)
        for k, y in enumerate(ROW_Y[::2]):
            for sx in (-1, 1):
                point((sx * 0.31, y, 0.08), AMBER, 3.0, 0.05)
    if layer == "bg":
        for o in fg:
            o.hide_render = True
    elif layer == "fg":
        keep = set(fg)
        for o in bpy.context.scene.objects:
            if o.type == "MESH" and o not in keep:
                o.visible_camera = False        # still lights/shadows the FG seats, but not rendered
        bpy.context.scene.render.film_transparent = True


sets.BUILDERS.update({"cabin": set_cabin})


# ---------------------------------------------------------------- shared props
def airliner(loc=(0, 0, 0), rz=0.0, s=1.0, decks=1, lit=0.0, livery=PETROL, doors_open=()):
    """Generic toon airliner in our colours (no logos). Nose towards +y before rotation rz (radians). Returns objects."""
    m_body = mat("fuselage", "#F4F1EA", rough=0.35, noise=0.02)
    m_liv = mat("livery", livery, rough=0.4, noise=0.02)
    m_win = _emit("plwin", "#FFE6A8", 3.0) if lit else mat("plwin_d", "#1E2A44", rough=0.2, noise=0.0)
    m_eng = mat("engine", "#C9CED6", rough=0.35, noise=0.02, metal=0.4)
    m_cock = mat("cockpit_win", "#16203A", rough=0.15, noise=0.0)
    objs = []
    R = 2.0 * s if decks == 1 else 3.1 * s
    Lh = 18 * s
    objs.append(cyl((0, 0, 0), R, 2 * Lh, m_body, verts=48, bevel=0.0, rot=(math.radians(90), 0, 0)))
    objs.append(sphere((0, Lh, 0), R, m_body, scale=(1, 1.6, 1)))                      # nose
    objs.append(cyl((0, -Lh - 3.5 * s, 0.9 * s), R, 7 * s, m_body, verts=48, bevel=0.0, rot=(math.radians(90), 0, 0), r2=0.35 * s))  # tail cone
    objs.append(box((0, -Lh - 4 * s, R + 3.0 * s), (0.18 * s, 3.2 * s, 3.2 * s), m_liv, bevel=0.15 * s, rot=(math.radians(-28), 0, 0)))  # fin
    objs.append(box((0, 0, -R * 0.25), (R * 1.01, Lh * 0.98, 0.18 * s), m_liv, bevel=0.0))  # belly stripe
    for sx in (-1, 1):
        objs.append(box((sx * 9 * s, -2 * s, -R * 0.4), (8 * s, 2.4 * s, 0.25 * s), m_body, bevel=0.2 * s, rot=(0, 0, sx * math.radians(-18))))  # wing
        objs.append(cyl((sx * 6 * s, 1.2 * s, -R * 0.85), 0.9 * s, 3.6 * s, m_eng, verts=32, bevel=0.05, rot=(math.radians(90), 0, 0)))
        objs.append(box((sx * 3.6 * s, -Lh - 3 * s, 0.9 * s), (3.2 * s, 1.2 * s, 0.15 * s), m_body, bevel=0.1 * s))   # tailplane
        rows = [0.35] if decks == 1 else [0.25, 0.62]
        for rz_ in rows:
            for i in range(26):
                y = -Lh * 0.85 + i * (Lh * 1.65 / 25)
                objs.append(box((sx * R * 0.985, y, R * rz_ - R * 0.1), (0.05 * s, 0.17 * s, 0.24 * s), m_win, bevel=0.08 * s))
    objs.append(box((0, Lh + 1.5 * s, R * 0.35), (R * 0.7, 0.6 * s, 0.35 * s), m_cock, bevel=0.2 * s, rot=(math.radians(25), 0, 0)))
    e = bpy.data.objects.new("airliner", None); bpy.context.collection.objects.link(e)
    for o in objs:
        o.parent = e
    e.location = loc; e.rotation_euler = (0, 0, rz)
    return e


def ground(m, size=400):
    return plane((0, 0, 0), (size, size), m)


# ---------------------------------------------------------------- cockpit (dusk)
def set_cockpit(variant):
    """Cockpit seen from the instrument panel looking back at the captain's seat; windows at the sides show the sky.
    The captain (2D) is composited sitting at x 0, y 0 (seat back at y -0.35). FG = instrument panel (x -1.2..1.2, y 0.55, top z 0.98).
    Marks: pilot pos (0,1.35,1.2) tgt (0,-0.4,1.05) lens 24."""
    base = variant.split("_")[0]
    layer = variant.split("_")[1] if "_" in variant else None
    sky_top, sky_low = {"dusk": ("#3A2E6E", "#F29E5C"), "day": ("#2E78C8", "#BFE6FF"), "night": ("#060B1C", "#1B2550")}.get(base, ("#3A2E6E", "#F29E5C"))
    world(sky_top, sky_low, 1.2)
    m_wall = mat("cpwall", "#3A404C", rough=0.6, noise=0.05)
    m_seat = mat("cpseat", "#2A2F3A", rough=0.8, noise=0.1, scale=20)
    m_panel = mat("panel", "#22262E", rough=0.5, noise=0.04)
    m_screen = _emit("screen", "#3C8DD8", 2.5)
    m_screen2 = _emit("screen2", "#7FE0FF", 1.8)
    for sx in (-1, 1):
        box((sx * 1.35, 0, 1.2), (0.05, 1.4, 1.2), m_wall, bevel=0.0)
        # side window (opening = frame boxes around a hole)
        box((sx * 1.36, 0.6, 1.45), (0.06, 0.55, 0.06), m_wall, bevel=0.02)
        box((sx * 1.36, 0.6, 0.95), (0.06, 0.55, 0.06), m_wall, bevel=0.02)
    # remove wall where windows are: simplest = put sky-coloured emissive panes in front of the wall
    for sx in (-1, 1):
        box((sx * 1.3, -0.2, 1.35), (0.01, 0.9, 0.45), _emit("cpsky%d" % sx, sky_low, 2.2), bevel=0.15)
        box((sx * 1.29, -0.2, 1.55), (0.012, 0.88, 0.2), _emit("cpskyt%d" % sx, sky_top, 1.6), bevel=0.1)
    box((0, -1.4, 1.2), (1.4, 0.05, 1.2), m_wall, bevel=0.0)
    box((0, 0, 2.35), (1.4, 1.4, 0.05), m_wall, bevel=0.0)
    plane((0, 0, 0), (1.4, 1.4), mat("cpfloor", "#1E222A", rough=0.9, noise=0.2, scale=20))
    box((0, -0.35, 0.95), (0.32, 0.12, 0.5), m_seat, bevel=0.1)                      # captain seat back
    box((0, -0.35, 1.55), (0.2, 0.1, 0.14), m_seat, bevel=0.06)                      # headrest
    box((0, -0.05, 0.42), (0.32, 0.3, 0.08), m_seat, bevel=0.06)
    box((0.95, -0.4, 0.95), (0.28, 0.1, 0.45), m_seat, bevel=0.1)                    # first officer seat (empty, side)
    fg = []
    fg.append(box((0, 0.6, 0.62), (1.3, 0.12, 0.36), m_panel, bevel=0.04))
    for i, x in enumerate((-0.8, -0.32, 0.32, 0.8)):
        fg.append(box((x, 0.47, 0.8), (0.2, 0.01, 0.14), m_screen if i % 2 else m_screen2, bevel=0.01))
    for i in range(12):
        fg.append(sphere((-0.15 + (i % 6) * 0.06, 0.48, 0.6 + (i // 6) * 0.06), 0.012,
                         _emit("btn%d" % (i % 3), ["#FF5B4B", "#7DFF9A", "#FFC93C"][i % 3], 4.0)))
    fg.append(cyl((0.0, 0.42, 0.98), 0.03, 0.25, m_panel, rot=(math.radians(80), 0, 0)))    # glare shield edge
    _to(_coll("FG"), fg)
    area((0, 0.3, 2.2), (0, 0, 0), 1.6, "#FFD8B0" if base == "dusk" else "#FFFFFF", 160)
    area((0, 1.2, 1.1), (math.radians(90), 0, 0), 1.4, "#9FD8FF", 80)                  # screen glow on the pilot
    area((-1.1, -0.3, 1.4), (0, math.radians(-90), 0), 1.0, sky_low, 120)             # window light (rim)
    area((1.1, -0.3, 1.4), (0, math.radians(90), 0), 1.0, sky_low, 120)
    _layers(layer, fg)


def _layers(layer, fg):
    if layer == "bg":
        for o in fg:
            o.hide_render = True
    elif layer == "fg":
        keep = set(fg)
        for o in bpy.context.scene.objects:
            if o.type == "MESH" and o not in keep:
                o.visible_camera = False
        bpy.context.scene.render.film_transparent = True


# ---------------------------------------------------------------- apron (top-down gate)
def set_apron(variant):
    """Gate seen from above (nose towards +y). Terminal along x<-14 with a jet bridge to the LEFT front door;
    belt loader, fuel truck and catering truck on the RIGHT. Mark: top pos (2,2,62) tgt (2,2.1,0) lens 30."""
    world("#9FD8FF", "#FFF3DA", 0.6)
    sun((40, 10, -30), "#FFE7C2", 4.0, 2.0)
    ground(mat("tarmac", "#6E7684", rough=0.9, noise=0.25, scale=6))
    m_line = mat("yline", AMBER, rough=0.6, noise=0.0)
    for i in range(-20, 20):
        box((0.0, i * 2.2, 0.01), (0.12, 0.6, 0.005), m_line, bevel=0.0)
    box((-22, 0, 4), (6, 40, 4), mat("terminal", "#C9D6E8", rough=0.4, noise=0.04), bevel=0.2)
    box((-15.8, 0, 4.6), (0.1, 38, 2.5), _emit("termglass", "#7FC8E8", 0.8), bevel=0.0)
    airliner((0, 0, 3.0), 0.0, 1.0)
    # jet bridge to the left front door (x -2, y 12)
    box((-9.5, 12, 3.6), (6.2, 1.3, 1.3), mat("bridge", "#B8C2CC", rough=0.5, noise=0.03), bevel=0.15)
    box((-3.0, 12, 3.6), (1.0, 1.5, 1.5), mat("bridgehead", "#9AA3AD", rough=0.5, noise=0.03), bevel=0.15)
    # trucks on the right
    def truck(x, y, rz, col, tank=False, belt=False):
        b = box((x, y, 1.0), (1.2, 3.0, 1.0), mat("truck" + col, col, rough=0.5, noise=0.03), bevel=0.2, rot=(0, 0, rz))
        box((x + 2.6 * math.sin(-rz), y + 2.6 * math.cos(rz), 1.2), (1.2, 1.0, 1.2), mat("cab", "#E8EEF2", rough=0.4, noise=0.02), bevel=0.2, rot=(0, 0, rz))
        if tank:
            cyl((x, y, 1.9), 1.0, 5.0, mat("tank", "#F4F1EA", rough=0.3, noise=0.01, metal=0.3), rot=(math.radians(90), 0, rz))
        if belt:
            box((x - 1.4, y + 3.5, 2.2), (0.6, 4.0, 0.12), mat("belt", "#2A2F3A", rough=0.8, noise=0.1), bevel=0.05, rot=(math.radians(18), 0, rz))
    truck(6.5, 13.5, 0.0, AMBER)                    # catering at the right front door
    truck(13.0, -1.0, math.radians(10), "#E8EEF2", tank=True)     # fuel under the right wing
    truck(5.8, 5.0, math.radians(-25), PETROL, belt=True)        # belt loader
    for i in range(3):
        box((9.0 + i * 3.2, 7.5, 0.7), (1.2, 0.9, 0.5), mat("cart", "#3E7CB1", rough=0.5, noise=0.03), bevel=0.1)
        box((9.0 + i * 3.2, 7.5, 1.35), (1.0, 0.7, 0.25), mat("bags", "#FF8A3D", rough=0.6, noise=0.1), bevel=0.1)


# ---------------------------------------------------------------- plane in the sky (exterior)
def set_skyplane(variant):
    """Our airliner flying, seen from the side-front. variants: clouds (noon above a cloud sea), ocean (dusk over water),
    night (approach over city lights + runway). Mark: side pos (38,40,6) tgt (0,0,0) lens 35; wide pos (70,60,12) tgt (0,-10,-6) lens 28."""
    base = variant.split("_")[0]
    if base == "clouds":
        world("#2E78C8", "#DDF2FF", 1.0); sun((70, 0, 40), "#FFF4DA", 4.5, 2.0)
        m_cloud = mat("cloud", "#FFFFFF", rough=1.0, noise=0.05)
        rnd = random.Random(9)
        for i in range(160):
            x, y = rnd.uniform(-120, 120), rnd.uniform(-120, 120)
            sphere((x, y, -18 + rnd.uniform(-1, 1)), rnd.uniform(4, 9), m_cloud, scale=(1.6, 1.2, 0.55), sub=2)
    elif base == "ocean":
        world("#3A2E6E", "#F29E5C", 1.0); sun((84, 0, -150), "#FFB070", 4.0, 3.0)
        plane((0, 0, -40), (300, 300), mat("sea", "#1E4F7A", rough=0.25, noise=0.15, scale=0.5))
    else:
        world("#060B1C", "#1B2550", 0.25)
        plane((0, 0, -40), (300, 300), mat("land", "#0B1530", rough=0.9, noise=0.1))
        rnd = random.Random(4)
        m_l = _emit("citylight", AMBER, 12.0)
        for i in range(500):
            sphere((rnd.uniform(-150, 150), rnd.uniform(-60, 150), -39.8), rnd.uniform(0.15, 0.35), m_l, sub=1)
        m_r = _emit("rwy", "#FFF4C0", 25.0)
        for i in range(40):
            for sx in (-1, 1):
                sphere((sx * 10, 60 + i * 6, -39.7), 0.35, m_r, sub=1)
    airliner((0, 0, 0), math.radians(-90), 1.0, lit=1.0 if base == "night" else 0.0)
    if base == "night":
        area((20, 25, 12), (math.radians(60), 0, math.radians(140)), 20, "#9FB8FF", 9000)
        point((0, 19.5, -1.5), "#FFFFFF", 300, 0.3)                                     # landing light
    if base == "ocean":
        area((25, 30, 10), (math.radians(60), 0, math.radians(140)), 20, "#FFB070", 4000)


# ---------------------------------------------------------------- hangar evacuation test (night)
def set_hangar(variant):
    """Night hangar with a double-deck airliner (nose -x) and 4 yellow slides on the near side (x>0 side faces the camera).
    Mark: wide pos (22,48,9) tgt (0,0,4) lens 26."""
    world("#0E1A2E", "#22324A", 0.3)
    ground(mat("hfloor", "#2A3446", rough=0.7, noise=0.15, scale=3))
    box((0, -40, 15), (60, 0.5, 15), mat("hwall", "#1C2638", rough=0.7, noise=0.05), bevel=0.0)
    for i in range(6):
        area((-30 + i * 12, 0, 28), (0, 0, 0), 8, "#CFE6FF", 900)
    airliner((0, 0, 6.5), math.radians(90), 1.0, decks=2, lit=1.0)
    m_slide = mat("slide", "#FFC93C", rough=0.4, noise=0.02)
    import bmesh
    for x, z in ((-11, 5.4), (3, 5.4), (-4, 7.9), (10, 7.9)):
        y0, y1 = 3.0, 3.0 + z * 1.3
        me = bpy.data.meshes.new("slide"); bm = bmesh.new()
        v = [bm.verts.new(p) for p in [(x - 1.1, y0, z), (x + 1.1, y0, z), (x + 1.3, y1, 0.3), (x - 1.3, y1, 0.3),
                                         (x - 1.1, y0, z - 0.35), (x + 1.1, y0, z - 0.35), (x + 1.3, y1, 0.0), (x - 1.3, y1, 0.0)]]
        for f in [(0, 1, 2, 3), (7, 6, 5, 4), (0, 3, 7, 4), (1, 5, 6, 2), (3, 2, 6, 7), (0, 4, 5, 1)]:
            bm.faces.new([v[i] for i in f])
        bm.to_mesh(me); bm.free()
        o = bpy.data.objects.new("slide", me); bpy.context.collection.objects.link(o); sets.obj_from(o, m_slide, 0.08, smooth=False)
        box((x, y0 + 0.2, z + 0.9), (0.9, 0.15, 0.9), _emit("doorlight", "#FFE6A8", 4.0), bevel=0.1)
    area((15, 40, 14), (math.radians(60), 0, math.radians(160)), 16, "#FFFFFF", 6000)


# ---------------------------------------------------------------- taste chamber
def set_chamber(variant):
    """Big steel low-pressure chamber holding a slice of airliner cabin (seen through the open front).
    Mark: front pos (0,-9,2.2) tgt (0,0,1.9) lens 30."""
    world("#22324A", "#33415A", 0.4)
    ground(mat("labfloor", "#1A202C", rough=0.6, noise=0.1, scale=4))
    box((0, 8, 4), (14, 0.3, 4), mat("labwall", "#2A3446", rough=0.7, noise=0.05), bevel=0.0)
    m_steel = mat("steel", "#8A96A8", rough=0.35, noise=0.04, metal=0.6)
    for i in range(12):
        a = math.radians(i * 15 - 0)
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=2.6, depth=7.0, location=(0, 0.5, 2.3), rotation=(math.radians(90), 0, 0), end_fill_type="NOTHING")
    o = bpy.context.active_object; sets.obj_from(o, m_steel, 0)
    sol = o.modifiers.new("sol", "SOLIDIFY"); sol.thickness = 0.12
    for y in (-2.9, -1.0, 1.0, 2.9):
        cyl((0, y + 0.5, 2.3), 2.7, 0.18, mat("ring", "#6E7A8C", rough=0.4, noise=0.02, metal=0.6), verts=64, rot=(math.radians(90), 0, 0))
    plane((0, 0.5, 0.75), (1.9, 3.3), mat("cfloor", "#5A6A80", rough=0.9, noise=0.2))
    m_seat = mat("seat", PETROL, rough=0.85, noise=0.15, scale=30)
    for x in (-1.0, 0.0, 1.0):
        box((x, 1.2, 1.25), (0.3, 0.3, 0.08), m_seat, bevel=0.05)
        box((x, 0.95, 1.7), (0.3, 0.07, 0.42), m_seat, bevel=0.06)
    area((0, 0.5, 3.9), (0, 0, 0), 2.0, "#FFF0D8", 600)
    point((0, -2.0, 2.4), "#FFF0D8", 400, 0.5)
    area((0, 1.0, 3.9), (0, 0, 0), 2.5, "#FFF6E8", 250)
    area((0, -10, 6), (math.radians(60), 0, 0), 8, "#CFE0FF", 1500)
    for x, col in ((-5.5, "#FF5B4B"), (5.5, "#7DFF9A")):
        cyl((x, -0.5, 1.4), 0.5, 0.15, mat("gauge", "#F4F1EA", rough=0.4, noise=0.0), rot=(math.radians(90), 0, 0))
        box((x, -0.6, 0.7), (0.08, 0.08, 0.7), m_steel, bevel=0.02)


# ---------------------------------------------------------------- harbour (top-down)
def set_harbor(variant):
    """An old sailing ship tied up with its LEFT (port) side to a wooden dock, seen from above, bow towards +y.
    Mark: top pos (-1,0,38) tgt (-1,0.1,0) lens 30."""
    world("#9FD8FF", "#FFF3DA", 0.6); sun((35, 10, -40), "#FFE7C2", 4.0, 2.0)
    plane((0, 0, -0.5), (200, 200), mat("water", "#2E7DA8", rough=0.2, noise=0.2, scale=0.3))
    m_wood = mat("dock", "#9A6A3E", rough=0.8, noise=0.3, scale=2)
    box((-14, 0, 0.3), (8, 40, 0.4), m_wood, bevel=0.05)
    for y in range(-30, 31, 6):
        cyl((-6.2, y, 0.5), 0.35, 1.6, mat("bollard", "#5B3A29", rough=0.7, noise=0.1))
    m_hull = mat("hull", "#8E5A2A", rough=0.6, noise=0.2, scale=3)
    hull = sphere((0, 0, 0.2), 1.0, m_hull, scale=(3.2, 11.5, 1.6), sub=4)
    plane((0, 0, 1.4), (2.6, 9.5), mat("deck", "#C9925A", rough=0.7, noise=0.25, scale=4))
    for y in (-5, 1, 6):
        cyl((0, y, 6), 0.25, 11, mat("mast", "#5B3A29", rough=0.6, noise=0.1))
        box((0, y, 9), (3.5, 0.1, 1.8), mat("sail", "#F4F1EA", rough=0.9, noise=0.05), bevel=0.05)
    m_rope = mat("rope", "#E8D2A0", rough=0.9, noise=0.1)
    for y0, y1 in ((-8, -12), (8, 12)):
        cyl(((-3.2 - 6.2) / 2, (y0 + y1) / 2, 1.0), 0.06, math.hypot(3.0, y1 - y0) + 1.5, m_rope,
            rot=(math.radians(90), 0, math.atan2(-3.0, y1 - y0)))


# ---------------------------------------------------------------- bright room / dark doorway
def set_doorway(variant):
    """A bright sunny room (left) with an open door to a pitch-dark room (right). Mark: front pos (-1.4,-6,1.6) tgt (-0.6,0,1.3) lens 32.
    The 2D character walks along y=0 from x -2.2 to x 1.6."""
    world("#FFF3DA", "#FFF3DA", 0.4)
    plane((-3, 0, 0), (3, 6), mat("wood", "#D9B584", rough=0.6, noise=0.2, scale=3))
    plane((3, 0, 0), (3, 6), mat("darkfloor", "#07090F", rough=0.9, noise=0.0))
    box((-3, 2.0, 1.6), (3.0, 0.05, 1.6), mat("roomwall", "#FFF4E0", rough=0.7, noise=0.04), bevel=0.0)
    box((0.15, 0.0, 1.6), (0.12, 3.0, 1.6), mat("partition", "#F2E3C4", rough=0.7, noise=0.04), bevel=0.0)
    box((0.15, -0.2, 1.05), (0.14, 0.55, 1.05), _emit("void", "#020306", 0.0), bevel=0.0)   # doorway opening into the dark
    box((0.15, -0.2, 2.15), (0.16, 0.6, 0.06), mat("doorframe", "#C9A27A", rough=0.5, noise=0.05), bevel=0.02)
    sun((50, 0, 60), "#FFF0D0", 5.0, 3.0)
    area((-3, -1, 3.0), (0, 0, 0), 3, "#FFF6E8", 400)
    box((-4.5, 1.9, 1.6), (0.9, 0.06, 0.7), _emit("window", "#FFFFFF", 6.0), bevel=0.05)


# ---------------------------------------------------------------- window close-up (cruise)
def set_porthole(variant):
    """Close-up of one cabin window at cruising height: bone wall, bevelled frame, clouds far below, sun.
    Mark: close pos (0,-2.2,0) tgt (0,0,0) lens 40 (window centred, ~45 % of the frame height)."""
    world("#2E78C8", "#BFE6FF", 1.0)
    m_wall = mat("wallc", BONE, rough=0.6, noise=0.04)
    for (x, z, hx, hz) in ((-1.4, 0, 1.0, 1.6), (1.4, 0, 1.0, 1.6), (0, 1.2, 0.5, 0.6), (0, -1.2, 0.5, 0.6)):
        box((x, 0.05, z), (hx, 0.05, hz), m_wall, bevel=0.0)
    fr = box((0, 0.0, 0), (0.42, 0.06, 0.58), mat("framec", "#D9D3C7", rough=0.5, noise=0.02), bevel=0.25)
    bpy.context.view_layer.objects.active = fr
    cut = box((0, 0, 0), (0.3, 0.3, 0.44), None, bevel=0.2)
    mod = fr.modifiers.new("hole", "BOOLEAN"); mod.object = cut; mod.operation = "DIFFERENCE"; cut.hide_render = True; cut.hide_viewport = True
    sun((60, 0, 20), "#FFF4DA", 4.5, 2.0)
    m_cloud = mat("cloudc", "#FFFFFF", rough=1.0, noise=0.05)
    rnd = random.Random(3)
    for i in range(60):
        sphere((rnd.uniform(-40, 40), rnd.uniform(25, 80), -14 + rnd.uniform(-1, 1)), rnd.uniform(3, 6), m_cloud, scale=(1.6, 1.2, 0.5), sub=2)
    area((0, -1.5, 0.6), (math.radians(70), 0, 0), 2, "#FFF6E8", 60)


sets.BUILDERS.update({"cockpit": set_cockpit, "apron": set_apron, "skyplane": set_skyplane, "hangar": set_hangar,
                      "chamber": set_chamber, "harbor": set_harbor, "doorway": set_doorway, "porthole": set_porthole})
