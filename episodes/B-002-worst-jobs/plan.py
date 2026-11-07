"""Shot plan for B-002 "Would You Survive These 8 Jobs From Old England?" (ranked list, #8 -> #1).
python plan.py  -> shots.json (uses timing.json for exact durations)
Shot kinds: 3d (rendered set + 2D puppets), card (rank card), title, map, doc, end.
Sets: palace, yard (tannery/fullers), fair, backyard (night), cottage (wake/tavern/stable) from lib/sets2.py,
plus square, court and study from lib/sets.py.
"""
import json, copy
from pathlib import Path

EP = Path(__file__).parent
T = {t["id"]: t for t in json.loads((EP / "timing.json").read_text())}


def M(pos, tgt, lens):
    return {"pos": pos, "tgt": tgt, "lens": lens}


MK = {
    # square (from B-001): platform centre (2,5) top z=1.2
    "sq_wide":   M([0, -13, 4.5], [1, 8, 2.5], 24),
    "sq_wide2":  M([-3, -11, 3.2], [2, 7, 2.2], 26),
    "sq_crowd":  M([1, -5.5, 1.5], [1.5, 2, 1.2], 30),
    "sq_street": M([-2.5, -6.5, 1.6], [-1, 3, 1.3], 28),
    # court: bench y 7.6, dock (-3.6,1.0)
    "ct_wide":   M([1.5, -9.5, 3.2], [0, 6, 2.0], 22),
    "ct_judge":  M([0.3, 4.6, 2.5], [0, 8.0, 2.45], 30),
    "ct_dock":   M([-2.2, -3.2, 1.6], [-3.6, 1.0, 1.1], 30),
    # study (Wy)
    "st_wide":   M([0.5, -3.8, 1.4], [0.4, 3, 1.15], 24),
    "st_wy":     M([0.6, -2.6, 1.0], [0.6, 0.55, 0.75], 32),
    "st_close":  M([0.6, -2.0, 1.0], [0.6, 0.55, 0.82], 32),
    # palace: close stool (-2.2,1.2), bed (3.6,2.0), fireplace (0,5.5), table (0.6,-0.6)
    "pl_wide":   M([0, -5.2, 1.7], [0, 3, 1.4], 24),
    "pl_stool":  M([-0.6, -1.9, 1.35], [-2.0, 1.3, 0.75], 30),
    "pl_bed":    M([0.8, -2.6, 1.6], [3.0, 2.0, 1.15], 28),
    "pl_fire":   M([0.4, -1.6, 1.55], [0.0, 5.0, 1.25], 28),
    "pl_night":  M([1.5, -4.5, 1.6], [-1, 2, 1.0], 26),
    # yard: tannery pits x -1.5..2.7, y 1.4..3.5; frames x 5.5/8; dung bucket (-2.6,-0.4); river y 9.5
    "yd_wide":   M([2, -7.5, 3.2], [0.5, 4, 0.6], 24),
    "yd_pits":   M([0.6, -2.4, 1.8], [0.6, 2.4, 0.45], 28),
    "yd_bucket": M([-1.6, -2.0, 1.1], [-2.6, -0.3, 0.45], 32),
    "yd_river":  M([1.0, -3.0, 2.2], [0.0, 12.0, 1.8], 26),
    # fullers: tubs (-1.2,2.6), (1.5,2.6), (0.2,0.4) rim z 0.91
    "fl_wide":   M([2, -7.0, 3.0], [0.5, 3.0, 0.6], 24),
    "fl_tub":    M([1.4, -2.6, 1.7], [0.2, 0.6, 0.95], 30),
    "fl_frames": M([5.2, -2.8, 1.5], [6.6, 2.4, 1.0], 28),
    # fair: wagon stage centre (0,4) top z 1.2
    "fr_wide":   M([0, -7.5, 1.8], [0, 3.5, 1.9], 26),
    "fr_stage":  M([0.4, -2.0, 1.75], [0.2, 4.0, 1.95], 30),
    "fr_low":    M([0.6, -1.0, 0.8], [0.4, 4.0, 2.1], 24),
    # backyard (night): privy (-1.5,3.8), hatch (0.6,3.4), cart (3.6,1.6)
    "by_wide":   M([1.5, -4.5, 1.8], [0.5, 3.5, 1.0], 24),
    "by_hatch":  M([1.0, -0.4, 1.6], [0.6, 3.2, 0.3], 30),
    "by_privy":  M([-0.8, -1.0, 1.35], [-1.5, 3.4, 1.2], 30),
    "by_cart":   M([1.4, -1.8, 1.5], [3.4, 1.6, 0.95], 28),
    # cottage: table (-0.6,0.6) top 0.85, bed (-2.6,2.8), hearth (2.6,4.1); tavern counter (-3.4,2.6)
    "co_wide":   M([1.5, -3.8, 1.6], [-1.5, 2.5, 0.8], 22),
    "co_table":  M([0.7, -1.7, 1.45], [-0.6, 0.8, 0.95], 30),
    "co_bed":    M([-0.2, -0.8, 1.5], [-2.6, 2.8, 0.75], 28),
    "co_counter":M([-0.5, -1.8, 1.6], [-3.0, 2.2, 1.1], 28),
    # stable: dug soil (1.2,-0.8), shovel (2.6,-1.4), nest boxes x -4.5
    "sb_wide":   M([1.5, -3.8, 1.6], [-1, 1.5, 0.6], 22),
    "sb_dig":    M([3.0, -3.4, 1.5], [1.2, -0.7, 0.45], 30),
    "sb_nests":  M([-1.0, -2.6, 1.8], [-4.5, -1.6, 2.6], 28),
}


def push(mk, amt=0.12, lens_mult=1.0, dz=0.0):
    a = MK[mk]
    p, t = a["pos"], a["tgt"]
    b = {"pos": [p[i] + (t[i] - p[i]) * amt + (dz if i == 2 else 0) for i in range(3)], "tgt": t, "lens": a["lens"] * lens_mult}
    return {"from": a, "to": b, "ease": "inout"}


def pull(mk, amt=0.12):
    c = push(mk, amt)
    return {"from": c["to"], "to": c["from"], "ease": "inout"}


def pan(mk, dx=1.0, dy=0.0):
    a = MK[mk]
    b = {"pos": [a["pos"][0] + dx, a["pos"][1] + dy, a["pos"][2]], "tgt": [a["tgt"][0] + dx, a["tgt"][1] + dy, a["tgt"][2]], "lens": a["lens"]}
    return {"from": a, "to": b, "ease": "inout"}


def orbit(mk, deg=8):
    return {"from": MK[mk], "orbit": deg, "ease": "inout"}


def crane(mk, dz=1.0):
    a = MK[mk]
    b = copy.deepcopy(a); b["pos"][2] += dz
    return {"from": a, "to": b, "ease": "inout"}


def shake(mk, amt=0.08, amp=0.03):
    c = push(mk, amt); c["shake"] = amp
    return c


def A(c, at, h=1.5, face="R", expr="neutral", arms="down", **kw):
    d = dict(c=c, at=at, h=h, face=face, expr=expr, arms=arms)
    d.update(kw)
    return d


SETS = {"sq": ("square", "day"), "sqd": ("square", "dusk"), "ct": ("court", "town"), "st": ("study", "day"),
        "pl": ("palace", "day"), "pln": ("palace", "night"), "tn": ("yard", "tannery"), "fl": ("yard", "fullers"),
        "fr": ("fair", "day"), "by": ("backyard", "night"), "wk": ("cottage", "wake"), "tv": ("cottage", "tavern"),
        "sb": ("cottage", "stable")}

WY = lambda expr="happy", arms="down", **kw: A("wy", [0.6, 0.55, 0], 1.25, "R", expr, arms, talk=True, **kw)
KING = lambda expr="neutral", arms="down", at=(-3.1, 1.9, 0), face="R", **kw: A("king", list(at), 1.6, face, expr, arms, **kw)
GROOM = lambda expr="neutral", arms="down", at=(-1.2, 1.0, 0), face="L", **kw: A("groom", list(at), 1.5, face, expr, arms, **kw)
CROWD_SQ = [A(f"villager{i}", [x, y, 0], 1.45, "R" if x < 2 else "L", "neutral")
            for i, (x, y) in enumerate([(-3.5, 1.5), (-2.4, 0.4), (-1.0, 1.8), (5.0, 1.5), (7.0, 0.2), (4.6, -0.2), (-4.6, -0.6)])]
CROWD_FR = [A(f"villager{i}", [x, y, 0], 1.45, "R" if x < 0 else "L", "surprised")
            for i, (x, y) in enumerate([(-2.8, 1.0), (-1.6, 0.2), (-0.4, 1.2), (1.2, 0.4), (2.6, 1.1), (3.4, -0.2)])]
QUACK = lambda expr="smug", arms="present", **kw: A("quack", [-0.9, 4.0, 1.2], 1.55, "R", expr, arms, **kw)
TOADBOY = lambda expr="happy", arms="down", **kw: A("toadboy", [0.6, 3.7, 1.2], 1.3, "L", expr, arms, **kw)
GONG = lambda expr="neutral", arms="down", at=(1.6, 2.4, 0), face="L", **kw: A("gongfarmer", list(at), 1.5, face, expr, arms, **kw)

SHOTS = []


def S(line, kind="3d", set=None, cam=None, chars=(), part=None, **kw):
    sh = dict(line=line, kind=kind, set=SETS[set][0] if set else None, variant=SETS[set][1] if set else None,
              cam=cam, chars=list(chars), part=part)
    sh.update(kw)
    SHOTS.append(sh)


def RANK(line, n, title):
    S(line, "card", num=n, text=title, sub=f"NUMBER {n}")

# ================================================================ COLD OPEN (ch 0)
S("L01", set="by", cam=push("by_wide", 0.18), chars=[GONG("neutral", "raise", at=(0.2, 1.6, 0), hold_r="torch")],
  tag="ENGLAND · LONG AGO", sfx=[(0, "owl", 0.5), (0.3, "wind", 0.4)], music="mystery")
S("L02", set="by", cam=push("by_cart", 0.12), chars=[GONG("worried", "down", at=(2.4, 1.0, 0), hold_r="bucket")], silhouette=True,
  sfx=[(0.2, "footsteps", 0.4)])
S("L03", set="pl", cam=push("pl_stool", 0.15), chars=[KING("smug", "down"), GROOM("happy", "present", hold_r="cloth")],
  pop=[(0.8, "THE TOILET?!")], sfx=[(0.75, "boing", 0.5)])
S("L04", set="fr", cam=push("fr_stage", 0.15, 1.08), chars=[QUACK("smug", "point_r"), TOADBOY("worried", "raise", hold_r="toad")],
  pop=[(0.6, "A TOAD?!")], sfx=[(0.5, "crowd_gasp", 0.5)])
S("L05", "map", view=(-2.0, 53.2, 12), pins=[("London", 0.6), ("Colchester", 1.0), ("Hereford", 1.4)], sfx=[(0.6, "pop", 0.5), (1.0, "pop", 0.5), (1.4, "pop", 0.5)])
S("L06", "title", text="WOULD YOU SURVIVE THESE\n8 JOBS FROM OLD ENGLAND?", sfx=[(0, "whoosh", 0.7), (0.3, "drum_hit", 0.6)], music="curious")
S("L07", set="st", cam=push("st_close", 0.12), chars=[WY("smug", "point_r")], sfx=[(0.3, "riser", 0.4)])

# ================================================================ #8 ALE CONNER (ch 1)
RANK("L08", 8, "THE ALE CONNER")
S("L08", set="tv", cam=push("co_wide", 0.12), chars=[A("aleconner", [-1.0, 1.6, 0], 1.5, "R", "happy", "raise", hold_r="tankard")],
  sfx=[(0, "crowd_murmur", 0.3)], music="playful")
S("L09", set="sq", cam=push("sq_street", 0.12), chars=[A("aleconner", [-1.2, 1.2, 0], 1.5, "R", "happy", "raise", hold_r="tankard", walk={"to": [0.4, 1.4, 0]})],
  pop=[(0.6, "BEST JOB EVER?")], sfx=[(0.5, "ding", 0.4)])
S("L10", set="sq", cam=pan("sq_crowd", 1.2), chars=[A("villager0", [-0.4, 1.5, 0], 1.45, "R", "neutral"), A("villager1", [3.4, 1.8, 0], 1.45, "L", "neutral")] + [A("aleconner", [-0.5, 0.0, 0], 1.5, "R", "happy", walk={"to": [1.8, 0.2, 0]})],
  tag="MEDIEVAL ENGLAND", sfx=[(0, "footsteps", 0.5)])
S("L11", set="tv", cam=push("co_table", 0.15), chars=[A("aleconner", [-0.2, 1.3, 0], 1.5, "L", "happy_closed", "hold", hold_r="tankard")],
  sfx=[(0.25, "drink", 0.6)])
S("L12", "doc", doc="aleassize", sfx=[(0, "paper", 0.6)])
S("L13", set="ct", cam=push("ct_dock", 0.1), chars=[A("villager2", [-3.6, 1.1, 0.3], 1.45, "R", "worried", cut=[-0.1, 1.05]),
  A("aleconner", [-2.2, 0.6, 0], 1.5, "L", "angry", "point_l")], sfx=[(0.6, "gavel", 0.8)])
S("L14", set="st", cam=push("st_wy", 0.12), chars=[WY("neutral", "chin")], sfx=[(0.2, "hmm", 0.4)])
S("L15", set="sq", cam=push("sq_crowd", 0.12), chars=[A(f"villager{i}", [x, y, 0], 1.45, "L", "angry", "point_l" if i == 1 else "down") for i, (x, y) in enumerate([(2.6, 1.0), (3.6, 0.2), (4.4, 1.4)])]
  + [A("aleconner", [0.0, 0.6, 0], 1.5, "R", "worried", hold_r="tankard")], sfx=[(0.4, "crowd_murmur", 0.4)])
S("L16", set="tv", cam=push("co_counter", 0.12), chars=[A("aleconner", [-2.2, 1.4, 0], 1.5, "R", "surprised", "down")], pop=[(0.7, "LEATHER TROUSERS?")],
  sfx=[(0.6, "boing", 0.4)])
S("L17", set="st", cam=push("st_close", 0.1), chars=[WY("smug", "raise")], pop=[(0.55, "MYTH!")], sfx=[(0.5, "pop", 0.5)])
S("L18", set="sq", cam=crane("sq_wide2", 1.0), chars=CROWD_SQ[:5] + [A("aleconner", [1.0, 2.6, 0], 1.5, "R", "happy", "wave", hold_r="tankard")],
  tag="STILL DONE TODAY, FOR FUN", sfx=[(0, "crowd_laugh", 0.4), (0.2, "birds", 0.3)])

# ================================================================ #7 GROOM OF THE STOOL (ch 2)
RANK("L19", 7, "THE GROOM OF THE STOOL")
S("L19", set="pl", cam=push("pl_wide", 0.12), chars=[KING("neutral", at=(-0.6, 1.6, 0)), GROOM("neutral", at=(1.2, 1.0, 0))], music="story")
S("L20", set="pl", cam=push("pl_stool", 0.15), chars=[], tag="TUDOR ENGLAND", pop=[(0.65, "THE KING'S TOILET")], sfx=[(0.6, "ding", 0.4)])
S("L21", set="pl", cam=push("pl_stool", 0.1), chars=[KING("neutral"), GROOM("worried", "present", hold_r="cloth")], sfx=[(0.3, "whoosh_soft", 0.3)])
S("L22", set="st", cam=push("st_wy", 0.12), chars=[WY("smug", "raise")], sfx=[(0.4, "riser", 0.4)])
S("L23", set="pl", cam=push("pl_bed", 0.12), chars=[KING("happy", "present", at=(2.6, 2.6, 0)), GROOM("happy", at=(1.5, 2.0, 0), face="R", talk=True)],
  sfx=[(0.3, "fire", 0.3)])
S("L24", set="pl", cam=push("pl_fire", 0.12), chars=[GROOM("smug", "raise", at=(-0.6, 1.6, 0), face="R", hold_r="coin"), KING("neutral", at=(1.2, 2.4, 0), face="L")],
  tag="HENRY VIII", sfx=[(0.3, "coin_single", 0.5), (1.4, "coins", 0.4)])
S("L25", set="pl", cam=push("pl_wide", 0.15), chars=[A("magistrate", [-1.2, 0.6, 0], 1.5, "R", "angry", "point_r"), A("lawyer", [1.0, 0.6, 0], 1.5, "L", "angry", "point_l"),
  A("crier", [2.4, 1.2, 0], 1.5, "L", "angry", "raise")], pop=[(0.5, "ME!"), (0.75, "NO, ME!")], sfx=[(0.4, "crowd_murmur", 0.4)])
S("L26", set="pln", cam=push("pl_night", 0.15), chars=[KING("angry", at=(-1.0, 1.8, 0))], sfx=[(0.2, "fire", 0.4)], music="tension")
S("L27", set="pln", cam=push("pl_night", 0.1), chars=[KING("angry", "point_r", at=(-1.6, 1.8, 0)), GROOM("worried", at=(0.6, 1.0, 0), face="L")], tag="1536",
  sfx=[(0.5, "drum_hit", 0.5)])
S("L28", set="pln", cam=pull("pl_night", 0.15), chars=[GROOM("worried", at=(0.2, 1.4, 0), face="R")], silhouette=True, pop=[(0.3, "FALSE CHARGES")],
  sfx=[(0, "church_bell", 0.5)])

# ================================================================ #6 TOAD EATER (ch 3)
RANK("L29", 6, "THE TOAD EATER")
S("L29", set="fr", cam=push("fr_wide", 0.1), chars=CROWD_FR + [QUACK("smug", "present"), TOADBOY("happy")], sfx=[(0, "crowd_murmur", 0.4)], music="playful")
S("L30", set="fr", cam=push("fr_wide", 0.12), chars=CROWD_FR[:4] + [QUACK("smug", "present", hold_r="bottle")], tag="THE 1600s", sfx=[(0.4, "sparkle", 0.4)])
S("L31", set="fr", cam=push("fr_stage", 0.12), chars=[QUACK("smug", "point_r"), TOADBOY("happy", "wave")], sfx=[(0.3, "boing", 0.3)])
S("L32", set="fr", cam=push("fr_low", 0.12), chars=[TOADBOY("worried", "raise", hold_r="toad")], pop=[(0.65, "DEADLY POISON?")], sfx=[(0.2, "frog", 0.6), (0.5, "crowd_gasp", 0.5)])
S("L33", set="fr", cam=push("fr_stage", 0.15, 1.1), chars=[QUACK("smug", "present"), TOADBOY("happy_closed", "raise", hold_r="toad")], pop=[(0.8, "GULP!")],
  sfx=[(0.75, "gulp", 0.8), (0.85, "crowd_gasp", 0.6)])
S("L34", set="fr", cam=shake("fr_stage", 0.08, 0.04), chars=[QUACK("surprised", "both_up"), TOADBOY("worried", "both_up", blink_fast=True)], sfx=[(0.2, "drum_hit", 0.4), (0.6, "crowd_gasp", 0.5)])
S("L35", set="fr", cam=push("fr_stage", 0.12), chars=[QUACK("smug", "present", hold_r="bottle"), TOADBOY("worried")], pop=[(0.7, "MIRACLE MEDICINE")], sfx=[(0.6, "sparkle", 0.5)])
S("L36", set="fr", cam=push("fr_wide", 0.15), chars=[A(c["c"], c["at"], c["h"], c["face"], "happy", "raise", hold_r="coin", walk={"to": [c["at"][0] * 0.7, c["at"][1] + 1.0, 0]}) for c in CROWD_FR]
  + [QUACK("happy", "present", hold_r="bottle"), TOADBOY("happy", "both_up")], pop=[(0.2, "CURED!")], sfx=[(0.1, "sparkle", 0.5), (0.5, "crowd_laugh", 0.5), (0.9, "coins", 0.5)])
S("L37", set="st", cam=push("st_wy", 0.12), chars=[WY("happy", "point_r")], sfx=[(0.2, "page_turn", 0.4)])
S("L38", "doc", doc="toady", sfx=[(0, "quill", 0.5)])
S("L39", set="st", cam=push("st_close", 0.1), chars=[WY("smug", "raise")], pop=[(0.6, "TOADY")], sfx=[(0.55, "pop", 0.5)])

# ================================================================ #5 SIN EATER (ch 4)
RANK("L40", 5, "THE SIN EATER")
S("L40", set="wk", cam=push("co_wide", 0.12), chars=[A("sineater", [-0.8, 1.6, 0], 1.5, "R", "neutral")], silhouette=True, sfx=[(0, "wind", 0.4)], music="dark")
S("L41", set="wk", cam=crane("co_wide", -0.4), chars=[], sfx=[(0.2, "owl", 0.4)])
S("L42", "map", view=(-2.6, 52.4, 6), pins=[("Wales", 0.8), ("Hereford", 1.4)], part=(0, 0.4), sfx=[(0.8, "pop", 0.4), (1.4, "pop", 0.4)])
S("L42", "doc", doc="aubrey", part=(0.4, 1.0), sfx=[(0, "page_turn", 0.5)])
S("L43", set="wk", cam=push("co_wide", 0.12), chars=[A("sineater", [1.6, -0.6, 0], 1.5, "L", "neutral", walk={"to": [0.4, 0.4, 0]}), A("mother", [-1.6, 1.4, 0], 1.45, "R", "worried")],
  sfx=[(0.1, "door", 0.5), (0.4, "footsteps", 0.4)])
S("L44", set="wk", cam=push("co_table", 0.12), chars=[A("mother", [-1.6, 1.4, 0], 1.45, "R", "worried", "present", hold_r="bread"), A("sineater", [0.3, 1.2, 0], 1.5, "L", "neutral")],
  sfx=[(0.3, "whoosh_soft", 0.3)])
S("L45", set="wk", cam=push("co_table", 0.15, 1.08), chars=[A("sineater", [0.2, 1.2, 0], 1.5, "L", "happy_closed", "hold", hold_r="bowl")], sfx=[(0.3, "chewing", 0.5)])
S("L46", set="wk", cam=push("co_bed", 0.1), chars=[A("mother", [-1.2, 1.8, 0], 1.45, "L", "happy_closed")], pop=[(0.7, "REST IN PEACE")], sfx=[(0.4, "sparkle", 0.3)])
S("L47", set="wk", cam=push("co_wide", 0.1), chars=[A("sineater", [0.6, 0.4, 0], 1.5, "R", "neutral", "hold", hold_r="coin")], part=(0, 0.5), sfx=[(0.3, "coin_single", 0.5)])
S("L47", set="sqd", cam=push("sq_street", 0.1), chars=[A("villager1", [0.6, 1.8, 0], 1.45, "L", "worried"), A("villager2", [1.6, 1.4, 0], 1.45, "L", "worried"),
  A("sineater", [-1.6, 0.8, 0], 1.5, "R", "neutral", walk={"to": [-0.8, 1.0, 0]})], part=(0.5, 1.0), sfx=[(0, "wind", 0.4)])
S("L48", set="st", cam=push("st_wy", 0.12), chars=[WY("neutral", "chin")], tag="HISTORIANS DISAGREE")
S("L49", set="wk", cam=push("co_table", 0.2), chars=[A("sineater", [0.2, 1.2, 0], 1.5, "L", "neutral", hold_r="bread")], silhouette=True, sfx=[(0.3, "wind", 0.3)])

# ================================================================ #4 SALTPETRE MAN (ch 5)
RANK("L50", 4, "THE SALTPETRE MAN")
S("L50", set="sb", cam=push("sb_wide", 0.12), chars=[A("saltpetre", [0.4, -0.4, 0], 1.55, "R", "smug", "raise", hold_r="shovel")], music="tension")
S("L51", set="st", cam=push("st_close", 0.1), chars=[WY("neutral", "present")], pop=[(0.45, "GUNPOWDER")], sfx=[(0.4, "thud", 0.5)])
S("L52", set="sb", cam=push("sb_dig", 0.15), chars=[], pop=[(0.75, "ANIMAL WASTE")], sfx=[(0.7, "boing", 0.3)])
S("L53", set="sb", cam=pan("sb_wide", -0.8), chars=[A("rooster", [-2.2, 0.6, 0], 0.55, "R", "surprised")], sfx=[(0.3, "rooster", 0.4)])
S("L54", set="sb", cam=push("sb_wide", 0.12), chars=[A("saltpetre", [0.6, -0.6, 0], 1.55, "L", "smug", "present", hold_r="scroll"), A("farmer", [-1.4, 0.4, 0], 1.45, "R", "worried")],
  sfx=[(0.3, "paper", 0.5)])
S("L55", "doc", doc="order1627", sfx=[(0, "paper", 0.6)])
S("L56", set="sb", cam=push("sb_wide", 0.1), chars=[A("saltpetre", [1.4, -0.6, 0], 1.55, "L", "smug", "raise", hold_r="shovel", gest=[(0.3, "slam"), (0.65, "slam")])],
  sfx=[(0.3, "shovel", 0.7), (0.65, "shovel", 0.7)])
S("L57", set="sb", cam=push("sb_wide", 0.15), chars=[A("farmer", [-1.4, 0.4, 0], 1.45, "R", "angry", "point_r"), A("saltpetre", [0.8, -0.6, 0], 1.55, "L", "smug", hold_r="shovel")],
  pop=[(0.75, "NO CHOICE")], sfx=[(0.1, "door", 0.4)])
S("L58", set="sq", cam=push("sq_crowd", 0.12), chars=[A(f"villager{i}", [x, y, 0], 1.45, "L", "angry") for i, (x, y) in enumerate([(2.6, 1.0), (3.6, 0.2), (4.4, 1.4)])]
  + [A("saltpetre", [0.0, 0.6, 0], 1.55, "R", "smug", hold_r="shovel")], pop=[(0.6, "HATED")], sfx=[(0.5, "crowd_murmur", 0.5)])

# ================================================================ #3 FULLER (ch 6)
RANK("L59", 3, "THE FULLER")
S("L59", set="fl", cam=push("fl_wide", 0.12), chars=[A("fuller", [0.2, 0.4, 0.5], 1.5, "R", "neutral", cut=[-0.45, 0.91])], music="curious")
S("L60", set="fl", cam=push("fl_frames", 0.12), chars=[A("fuller", [4.9, 1.2, 0], 1.5, "R", "neutral", "present", hold_r="cloth")], sfx=[(0.3, "whoosh_soft", 0.3)])
S("L61", set="fl", cam=push("fl_tub", 0.05), chars=[A("fuller", [-0.4, -0.5, 0], 1.5, "R", "surprised")], pop=[(0.6, "URINE?!")], sfx=[(0.55, "boing", 0.5)])
S("L62", set="fl", cam=push("fl_tub", 0.04), chars=[A("villager3", [1.4, -0.4, 0], 1.45, "L", "worried", "present", hold_r="bucket"), A("fuller", [-0.4, -0.5, 0], 1.5, "R", "neutral")],
  tag="LEFT FOR DAYS", sfx=[(0.5, "splash", 0.6)])
S("L63", set="fl", cam=push("fl_tub", 0.1), chars=[A("fuller", [0.2, 0.4, 0.5], 1.5, "R", "worried", "both_up", cut=[-0.45, 0.91], bob=True)],
  pop=[(0.8, "FOR HOURS")], sfx=[(0.3, "footsteps", 0.6)])
S("L64", set="st", cam=push("st_wy", 0.12), chars=[WY("happy", "point_r")], pop=[(0.45, "AMMONIA")], sfx=[(0.4, "sparkle", 0.4)])
S("L65", set="fl", cam=pull("fl_wide", 0.12), chars=[], tag="WATER MILLS", sfx=[(0, "wind", 0.3)])
S("L66", "doc", doc="surnames", sfx=[(0, "quill", 0.5)])

# ================================================================ #2 TANNER (ch 7)
RANK("L67", 2, "THE TANNER")
S("L67", set="tn", cam=push("yd_wide", 0.12), chars=[A("tanner", [0.6, 0.0, 0], 1.5, "R", "neutral", hold_r="staff")], sfx=[(0, "insects", 0.3)], music="story")
S("L68", set="tn", cam=push("yd_pits", 0.04), chars=[A("tanner", [-0.5, 0.2, 0], 1.5, "R", "neutral", "hold", hold_r="staff"), A("villager2", [1.4, -0.2, 0], 1.45, "L", "worried")],
  pop=[(0.75, "PHEW!")], sfx=[(0.3, "insects", 0.4)])
S("L69", set="tn", cam=push("yd_pits", 0.07), chars=[A("tanner", [-0.5, 0.2, 0], 1.5, "R", "neutral", "hold", hold_r="staff")], tag="SOAKED FOR MONTHS", sfx=[(0.3, "tick", 0.4)])
S("L70", set="tn", cam=push("yd_bucket", 0.15), chars=[A("dog", [-2.1, 0.1, 0], 0.5, "L", "happy")], pop=[(0.5, "DOG DUNG")], sfx=[(0.3, "dog", 0.4)])
S("L71", set="tn", cam=push("yd_river", 0.12), chars=[A("tanner", [-0.6, 3.0, 0], 1.5, "R", "neutral", hold_r="staff")], tag="OUTSIDE THE WALLS", sfx=[(0, "birds", 0.3)])
S("L72", "map", view=(-0.4, 52.2, 7.0), pins=[("Colchester", 0.6)], part=(0, 0.35), sfx=[(0.6, "pop", 0.5)])
S("L72", "doc", doc="colchester", part=(0.35, 1.0), sfx=[(0, "paper", 0.5)])
S("L73", set="sq", cam=push("sq_wide2", 0.12), chars=CROWD_SQ[:4] + [A("villager5", [1.6, 2.4, 0], 1.45, "R", "happy", "present", hold_r="bucket")], pop=[(0.3, "SHOES · BELTS · SADDLES")],
  sfx=[(0, "crowd_murmur", 0.3)])
S("L74", set="sq", cam=push("sq_crowd", 0.12), chars=[A("tanner", [0.0, 0.6, 0], 1.5, "R", "worried", hold_r="staff")]
  + [A(f"villager{i}", [x, y, 0], 1.45, "R", "worried", walk={"to": [x + 1.6, y, 0]}) for i, (x, y) in enumerate([(2.0, 1.0), (2.8, 0.2)])], sfx=[(0.3, "footsteps", 0.4)])

# ================================================================ #1 GONG FARMER (ch 8)
RANK("L75", 1, "THE GONG FARMER")
S("L75", set="by", cam=push("by_wide", 0.15), chars=[GONG("neutral", "raise", hold_r="shovel")], sfx=[(0, "owl", 0.4), (0.2, "drum_hit", 0.5)], music="dark")
S("L76", set="by", cam=push("by_privy", 0.15), chars=[], pop=[(0.35, "GONG = TOILET")], sfx=[(0.3, "door", 0.4)])
S("L77", set="by", cam=push("by_wide", 0.22), chars=[GONG("neutral", "present", at=(1.6, 2.4, 0), hold_r="bucket")], sfx=[(0.3, "shovel", 0.6)])
S("L78", set="by", cam=push("by_wide", 0.12), chars=[GONG("neutral", "raise", at=(0.0, 1.2, 0), face="R", hold_r="torch", walk={"to": [1.4, 1.6, 0]})], tag="\"NIGHT SOIL\"",
  sfx=[(0.2, "footsteps", 0.4), (0.5, "owl", 0.3)])
S("L79", set="by", cam=shake("by_hatch", 0.03, 0.03), chars=[GONG("worried", "both_up", at=(1.8, 2.2, 0), blink_fast=True)], pop=[(0.55, "TOXIC FUMES")], sfx=[(0.4, "riser", 0.4)])
S("L80", "doc", doc="coroner1326", part=(0, 0.55), sfx=[(0, "paper", 0.5)])
S("L80", set="by", cam=push("by_privy", 0.12), chars=[], part=(0.55, 1.0), tag="LONDON · 1326", sfx=[(0.3, "thud", 0.5)])
S("L81", set="st", cam=push("st_wy", 0.12), chars=[WY("neutral", "chin")], sfx=[(0.2, "hmm", 0.4)])
S("L82", set="by", cam=push("by_cart", 0.12), chars=[GONG("happy", "raise", at=(2.2, 1.0, 0), hold_r="sack")], pop=[(0.3, "MONEY")], sfx=[(0.3, "coins", 0.6)], music="warm")
S("L83", set="st", cam=push("st_close", 0.1), chars=[WY("neutral", "present")])
S("L84", set="st", cam=push("st_wy", 0.12), chars=[WY("happy", "point_r")], pop=[(0.6, "COMMENT BELOW")], sfx=[(0.5, "pop", 0.5)])
S("L85", set="st", cam=push("st_close", 0.1), chars=[WY("happy", "wave")])
S(None, "end", dur=20.0, music="warm")

# ---------------------------------------------------------------- timeline
GAP = 0.32
out = []
t = 0.0
CARD = 2.4
k = 0
prev_line = None
for sh in SHOTS:
    if sh["kind"] == "card":
        out.append(dict(sh, id=f"S{k:03d}", start=round(t, 3), dur=CARD, line=None, chapter=T[sh["line"]]["chapter"]))
        t += CARD; k += 1
        continue
    if sh["kind"] == "end":
        out.append(dict(sh, id=f"S{k:03d}", start=round(t, 3), chapter=8)); t += sh["dur"]; k += 1
        continue
    L = T[sh["line"]]
    p0, p1 = sh["part"] or (0, 1)
    gap = GAP + (0.25 if L["text"].rstrip().endswith(("?", "...")) else 0)
    full = L["dur"] + gap
    if sh["line"] != prev_line:
        line_start = t
        prev_line = sh["line"]
    s0 = line_start + full * p0
    s1 = line_start + full * p1
    out.append(dict(sh, id=f"S{k:03d}", start=round(s0, 3), dur=round(s1 - s0, 3), chapter=L["chapter"], line_start=round(line_start, 3)))
    if p1 >= 0.999:
        t = line_start + full
    k += 1

plan = {"fps": 30, "resolution": [1920, 1080], "style": "T", "episode": "B-002", "duration": round(t, 2), "shots": out}
(EP / "shots.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False))
print(len(out), "shots, duration", round(t, 1), "s =", f"{int(t // 60)}:{int(t % 60):02d}")
