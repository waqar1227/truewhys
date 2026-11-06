"""Shot plan for B-001 "Why Medieval Courts Put Animals on Trial".
python plan.py  -> shots.json (uses timing.json for exact durations)
Shot kinds: 3d (rendered set + 2D puppets), card (chapter), title, map, split, doc, end.
"""
import json, copy
from pathlib import Path

EP = Path(__file__).parent
T = {t["id"]: t for t in json.loads((EP / "timing.json").read_text())}

# ---------------------------------------------------------------- camera marks (pos, tgt, lens)
def M(pos, tgt, lens):
    return {"pos": pos, "tgt": tgt, "lens": lens}

MK = {
    # square: platform centre (2,5) top z=1.2; crowd in front y -1..2
    "sq_wide":   M([0, -13, 4.5], [1, 8, 2.5], 24),
    "sq_wide2":  M([-3, -11, 3.2], [2, 7, 2.2], 26),
    "sq_crowd":  M([1, -5.5, 1.5], [1.5, 2, 1.2], 30),
    "sq_plat":   M([2.8, -2.6, 1.6], [2, 5, 1.7], 32),
    "sq_low":    M([1.0, -1.2, 0.6], [2, 5, 1.9], 24),
    "sq_hall":   M([4, -4, 2.0], [3, 10.5, 2.4], 28),
    "sq_alpine": M([0, -12, 3.0], [1, 10, 5.0], 22),
    # court: bench y 7.6 (top z 2.25), dais z 1.0; dock (-3.6,1.0) rail z 1.2; pews x 2..6
    "ct_wide":   M([1.5, -9.5, 3.2], [0, 6, 2.0], 22),
    "ct_bench":  M([0.3, 2.5, 2.3], [0, 8.0, 2.3], 30),
    "ct_judge":  M([0.3, 4.6, 2.5], [0, 8.0, 2.45], 30),
    "ct_dock":   M([-2.2, -3.2, 1.6], [-3.6, 1.0, 1.1], 30),
    "ct_lawyer": M([-0.4, -2.0, 1.5], [-1.4, 2.6, 1.2], 32),
    "ct_side":   M([5.5, -2.0, 2.0], [-2, 5, 1.6], 26),
    "ct_table":  M([2.4, 2.6, 1.6], [2.3, 4.2, 0.9], 30),
    # land: path along +y, village at (8,46)
    "ld_wide":   M([1.5, -8, 2.2], [2, 20, 2.5], 26),
    "ld_field":  M([3, -2, 1.2], [5, 6, 0.6], 28),
    "ld_low":    M([0.6, -1.5, 0.5], [0.6, 6, 0.9], 24),
    "ld_village":M([2, 10, 3], [8, 46, 4], 40),
    # vineyard
    "vn_wide":   M([0, -6, 2.5], [0, 20, 4], 24),
    "vn_rows":   M([1.5, 1.0, 1.0], [3, 5.6, 0.7], 34),
    "vn_close":  M([3.0, 1.6, 1.3], [3.0, 3.6, 0.95], 34),
    "vn_mid":    M([0.6, -3.2, 1.7], [1.6, 4.0, 1.0], 28),
    # night hill
    "nt_wide":   M([0, -6, 1.8], [0, 20, 4], 24),
    "nt_crowd":  M([0.5, -3, 1.2], [0, 6, 1.3], 30),
    # study
    "st_wide":   M([0.5, -3.8, 1.4], [0.4, 3, 1.15], 24),
    "st_wy":     M([0.6, -2.6, 1.0], [0.6, 0.55, 0.75], 32),
    "st_close":  M([0.6, -2.0, 1.0], [0.6, 0.55, 0.82], 32),
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

# ---------------------------------------------------------------- actors
def A(c, at, h=1.5, face="R", expr="neutral", arms="down", **kw):
    d = dict(c=c, at=at, h=h, face=face, expr=expr, arms=arms)
    d.update(kw)
    return d

SETS = {"sq": ("square", "day"), "sqd": ("square", "dusk"), "sqa": ("square", "alpine"), "ct": ("court", "town"),
        "ch": ("court", "church"), "ld": ("land", "barley"), "vn": ("land", "vineyard"), "nt": ("land", "night"),
        "st": ("study", "day")}

CROWD_SQ = [A(f"villager{i}", [x, y, 0], 1.45, "R" if x < 2 else "L", "worried" if i % 3 else "surprised")
            for i, (x, y) in enumerate([(-3.5, 1.5), (-2.4, 0.4), (-1.0, 1.8), (5.0, 1.5), (7.0, 0.2), (4.6, -0.2), (-4.6, -0.6)])]
JUDGE = lambda expr="neutral", arms="down", **kw: A("judge", [0, 8.0, 1.5], 1.6, "R", expr, arms, cut=[7.15, 2.22], **kw)
BISHOP = lambda expr="neutral", arms="down", **kw: A("bishop", [0, 8.0, 1.5], 1.6, "R", expr, arms, cut=[7.15, 2.22], **kw)
PIG_DOCK = lambda expr="worried", **kw: A("pig", [-3.6, 1.1, 0.3], 0.85, "R", expr, cut=[-0.1, 0.75], **kw)
WY = lambda expr="happy", arms="down", **kw: A("wy", [0.6, 0.55, 0], 1.25, "R", expr, arms, talk=True, **kw)
LAWYER = lambda expr="smug", arms="down", at=(-1.4, 2.6, 0), **kw: A("lawyer", list(at), 1.5, "L", expr, arms, **kw)


SHOTS = []


def S(line, kind="3d", set=None, cam=None, chars=(), part=None, **kw):
    sh = dict(line=line, kind=kind, set=SETS[set][0] if set else None, variant=SETS[set][1] if set else None,
              cam=cam, chars=list(chars), part=part)
    sh.update(kw)
    SHOTS.append(sh)

# ================================================================ COLD OPEN (ch 0)
S("L01", set="sqd", cam=push("sq_wide", 0.18), chars=CROWD_SQ, tag="FALAISE, FRANCE · 1386", sfx=[(0, "crowd_murmur", 0.5), (0.2, "church_bell", 0.5)], music="mystery")
S("L02", set="ct", cam=push("ct_wide", 0.15), chars=[JUDGE("angry", "down", hold="scroll")], sfx=[(0, "room_tone", 0.4)])
S("L03", set="ct", cam=push("ct_judge", 0.1, 1.05), chars=[JUDGE("angry", "raise", hold_r="gavel", gest=[(0.6, "slam")])], sfx=[(0.75, "gavel", 1.0)])
S("L04", set="sqd", cam=push("sq_crowd", 0.15), chars=CROWD_SQ[:4], sfx=[(0, "footsteps", 0.6), (0.4, "crowd_murmur", 0.4)], silhouette=True)
S("L05", set="sqd", cam=push("sq_plat", 0.2, 1.1), chars=[A("pig", [2, 5, 1.2], 0.9, "L", "worried", outfit="clothes", blink_fast=True)],
  pop=[(0.45, "A PIG?!")], sfx=[(0.35, "drum_hit", 0.8), (0.5, "pig_oink", 0.9), (0.9, "crowd_gasp", 0.6)])
S("L06", "map", pins=[("Falaise", 1), ("Autun", 1.4), ("Basel", 1.8), ("St-Julien", 2.2), ("", 2.4)], sfx=[(1.0, "pop", 0.5), (1.4, "pop", 0.5), (1.8, "pop", 0.5), (2.2, "pop", 0.5)])
for i, (who, w0) in enumerate([("pig", 0), ("bull", 1), ("rat", 2), ("weevil", 4)]):
    pass
S("L07", set="ct", cam=push("ct_dock", 0.1), chars=[PIG_DOCK("worried")], part=(0, 0.25), sfx=[(0, "pig_oink", 0.7)])
S("L07", set="ct", cam=push("ct_dock", 0.1), chars=[A("bull", [-3.6, 1.2, 0.3], 1.1, "R", "angry", cut=[-0.1, 0.8])], part=(0.25, 0.5), sfx=[(0, "thud", 0.5)], label="BULL")
S("L07", set="ct", cam=push("ct_dock", 0.1), chars=[A("rat", [-3.9, 1.1, 0.3], 0.6, "R", "sly", cut=[-0.1, 0.55]), A("rat", [-3.3, 1.3, 0.3], 0.55, "L", "worried", cut=[-0.1, 0.55])], part=(0.5, 0.75), sfx=[(0, "rat_squeak", 0.7)])
S("L07", set="ct", cam=push("ct_dock", 0.18), chars=[A("weevil", [-3.6, 1.1, 1.22], 0.25, "R", "surprised")], part=(0.75, 1.0), pop=[(0.2, "INSECTS?!")], sfx=[(0, "boing", 0.6)])
S("L08", set="ct", cam=orbit("ct_lawyer", 10), chars=[LAWYER("smug", "point_r"), A("rat", [-2.3, 2.2, 0], 0.5, "R", "smug")], part=(0, 0.33), sfx=[(0, "whoosh_soft", 0.5)])
S("L08", "doc", doc="summons", part=(0.33, 0.66), sfx=[(0, "paper", 0.6)])
S("L08", set="vn", cam=push("vn_rows", 0.15), chars=[A("weevil", [3.0, 4.4, 0.0], 0.35, "R", "happy"), A("weevil", [3.6, 4.6, 0.0], 0.3, "L", "happy")], part=(0.66, 1.0), sfx=[(0, "sparkle", 0.5)])
S("L09", set="st", cam=push("st_wy", 0.15), chars=[WY("surprised", "shrug")], sfx=[(0, "hmm", 0.4)], music="curious")
S("L10", set="st", cam=push("st_close", 0.1), chars=[WY("smug", "point_r")], props=[("coin", [1.25, 1.2, 1.12], 0.12), ("coin", [1.35, 1.25, 1.12], 0.12)], pop=[(0.75, "MONEY")], sfx=[(0.7, "coins", 0.8)])
S("L11", "title", text="WHY MEDIEVAL COURTS PUT\nANIMALS ON TRIAL", sfx=[(0, "whoosh", 0.7), (0.3, "drum_hit", 0.6)])

# ================================================================ CH 1 The Pig of Falaise
S("L12", "card", num=1, text="THE PIG OF FALAISE", music="story")
S("L13", set="sq", cam=pan("sq_wide2", 1.2), chars=[A("mother", [-1.5, 0.5, 0], 1.45, "R", "sad"), A("villager2", [0.2, 1.2, 0], 1.45, "L", "worried"), A("pig", [5.5, 2.5, 0], 0.7, "L", "neutral")], sfx=[(0, "wind", 0.3)])
S("L14", set="st", cam=push("st_wy", 0.1), chars=[WY("sad", "shrug")], part=(0, 0.48))
S("L14", set="sq", cam=push("sq_hall", 0.15), chars=[A("crier", [2.5, 6.5, 0], 1.5, "R", "angry", "point_r"), A("villager4", [5.5, 5.5, 0], 1.45, "L", "angry", "raise")], part=(0.48, 1.0), pop=[(0.75, "MURDER")], sfx=[(0.55, "drum_hit", 0.6)])
S("L15", set="ct", cam=push("ct_wide", 0.2), chars=[JUDGE("neutral"), PIG_DOCK("worried"), A("crier", [-1.5, 3.0, 0], 1.5, "R", "neutral", hold="scroll")], tag="THE TOWN'S CRIMINAL COURT", sfx=[(0, "crowd_murmur", 0.3)])
S("L16", set="ct", cam=push("ct_judge", 0.12, 1.08), chars=[JUDGE("angry", "point_l")], pop=[(0.55, "AN EYE FOR AN EYE")], sfx=[(0.5, "drum_hit", 0.7), (0.55, "gavel", 0.6)])
S("L17", "doc", doc="sentence", sfx=[(0, "quill", 0.5)])
S("L18", set="sqd", cam=pan("sq_wide2", -1.5), chars=CROWD_SQ[:5] + [A("pig", [0.5, 3.5, 0], 0.85, "R", "worried", outfit="clothes", walk={"to": [2.0, 3.0, 0]})], sfx=[(0, "crowd_murmur", 0.5), (0, "footsteps", 0.4)])
S("L19", set="ct", cam=push("ct_table", 0.2), props=[("coin", [2.1, 4.1, 0.9], 0.1, {"drop": 0.2}), ("coin", [2.3, 4.2, 0.9], 0.1, {"drop": 0.45}), ("coin", [2.5, 4.05, 0.9], 0.1, {"drop": 0.7})],
  pop=[(0.4, "10 SOUS + 10 DENIERS")], sfx=[(0.2, "coin_single", 0.7), (0.45, "coin_single", 0.7), (0.7, "coins", 0.6)])
S("L20", set="ct", cam=push("ct_table", 0.3, 1.1), props=[("gloves", [2.3, 4.15, 0.95], 0.28, {"pop": 0.1})], pop=[(0.5, "+ NEW GLOVES")], sfx=[(0.15, "sparkle", 0.7)])
S("L21", set="st", cam=push("st_wy", 0.12), chars=[WY("happy", "raise", hold_r="gloves")], sfx=[(0.1, "ding", 0.5)])
S("L22", set="sq", cam=push("sq_hall", 0.1), chars=[A("crier", [2.6, 6.0, 0], 1.55, "R", "smug", "present", hold_l="staff")], tag="OFFICER OF THE LAW")
S("L23", set="ch", cam=pan("ct_side", -1.0), chars=[A("monk", [2.5, 3.0, 0], 1.45, "L", "surprised", "point_l")], props=[("painting", [-2.6, 10.4, 4.6], 2.6, {"pop": 0.25})], sfx=[(0, "room_tone", 0.3)])
S("L24", set="st", cam=push("st_close", 0.15), chars=[WY("surprised", "both_up")], sfx=[(0.3, "boing", 0.4)])
S("L25", set="sq", cam=orbit("sq_wide2", -10), chars=[A("pig", [-2, 1, 0], 0.7, "R", "happy"), A("pig", [3.5, 2, 0], 0.65, "L", "smug"), A("pig", [6.5, -0.5, 0], 0.7, "L", "neutral"), A("villager5", [0.8, 0, 0], 1.45, "L", "worried")], sfx=[(0.3, "pig_oink", 0.6), (1.5, "pig_squeal", 0.4)])

# ================================================================ CH 2 Two Kinds of Court
S("L26", "card", num=2, text="TWO KINDS OF COURT", music="story")
S("L26", "split", part=None, alias="L26b", skip=True)
S("L27", "split", side="left", items=["pig", "bull", "horse", "dog"], heading="GROUP 1: HURT A PERSON", sfx=[(0, "whoosh_soft", 0.5)])
S("L28", set="ct", cam=push("ct_wide", 0.18), chars=[JUDGE("angry", "point_l"), PIG_DOCK("worried")], sfx=[(0.8, "gavel", 0.6)])
S("L29", "split", side="right", items=["rat", "mouse", "locust", "weevil"], heading="GROUP 2: ATE THE CROPS", sfx=[(0, "whoosh_soft", 0.5), (0.6, "insects", 0.4)])
S("L30", set="ld", cam=push("ld_field", 0.15), chars=[A("farmer", [3.4, 3.6, 0], 1.5, "R", "worried", "shrug")] + [A("rat", [4 + 0.7 * k, 4 + 0.5 * (k % 3), 0], 0.35, "L", "sly") for k in range(5)], sfx=[(0, "chewing", 0.6), (0, "birds", 0.3)])
S("L31", set="ld", cam=pull("ld_wide", 0.2), chars=[A("rat", [-4 + 0.45 * (k % 18) + 0.2 * (k // 18), 3 + (k // 18) * 1.3 + 0.3 * (k % 3), 0], 0.4, "R" if k % 2 else "L", "sly") for k in range(54)], part=(0, 0.55), pop=[(0.3, "10,000 RATS")], sfx=[(0.2, "rat_squeak", 0.6)])
S("L31", set="ch", cam=push("ct_wide", 0.15), chars=[BISHOP("neutral")], part=(0.55, 1.0), tag="THE CHURCH COURT", sfx=[(0, "church_bell", 0.4)])
S("L32", set="ch", cam=push("ct_judge", 0.12, 1.06), chars=[BISHOP("angry", "both_up")], pop=[(0.55, "ANATHEMA")], sfx=[(0.5, "riser", 0.5), (0.9, "drum_hit", 0.5)])
S("L33", set="ch", cam=pan("ct_lawyer", 0.6), chars=[LAWYER("happy", "present", at=(-1.0, 2.6, 0))], sfx=[(0.7, "ding", 0.4)])

# ================================================================ CH 3 The Lawyer for the Rats
S("L34", "card", num=3, text="THE LAWYER FOR THE RATS", music="playful")
S("L34", set="ld", cam=push("ld_wide", 0.2), chars=[A("rat", [1.5 + 0.8 * k, 3 + (k % 3), 0], 0.4, "L", "happy") for k in range(6)], tag="AUTUN, FRANCE · EARLY 1500s", sfx=[(0.3, "chewing", 0.6)])
S("L35", set="ch", cam=push("ct_wide", 0.12), chars=[BISHOP("neutral", "point_l"), A("rat", [-3.6, 1.1, 0.3], 0.5, "R", "worried", cut=[-0.1, 0.55])])
S("L36", set="ch", cam=push("ct_lawyer", 0.15), chars=[LAWYER("smug", "down", hold_r="scroll")], tag="BARTHOLOMEW CHASSENÉE · LAWYER", sfx=[(0, "sparkle", 0.4)])
S("L37", set="ch", cam=orbit("ct_lawyer", 8), chars=[LAWYER("neutral", "chin")])
S("L38", "map", pins=[("Autun", 0.2)], villages=True, sfx=[(0.4, "pop", 0.4), (0.7, "pop", 0.4), (1.0, "pop", 0.4)])
S("L39", set="ch", cam=push("ct_judge", 0.1), chars=[BISHOP("happy", "raise")], part=(0, 0.45), sfx=[(0.3, "gavel", 0.5)])
S("L39", set="sq", cam=push("sq_hall", 0.12), chars=[A("crier", [2.5, 5.8, 0], 1.5, "R", "happy", "raise", hold_r="scroll")] + CROWD_SQ[2:5], part=(0.45, 1.0), sfx=[(0, "church_bell", 0.5)])
S("L40", set="ch", cam=push("ct_dock", 0.1), chars=[], part=(0, 0.5), sfx=[(0, "tick", 0.5)], label="EMPTY")
S("L40", set="ch", cam=push("ct_lawyer", 0.12), chars=[LAWYER("smug", "point_r")], part=(0.5, 1.0))
S("L41", set="ld", cam=push("ld_low", 0.12), chars=[A("rat", [0.2, 3.0, 0], 0.4, "R", "worried"), A("rat", [1.0, 3.4, 0], 0.4, "L", "worried")], sfx=[(0, "wind", 0.4)])
S("L42", set="ld", cam=push("ld_low", 0.2, 1.1), chars=[A("cat", [-0.5, 4.5, 0], 0.7, "R", "sly"), A("cat", [1.8, 5.5, 0], 0.65, "L", "sly"), A("cat", [-1.6, 7.0, 0], 0.6, "R", "sly")], pop=[(0.3, "CATS")], sfx=[(0.3, "cat_hiss", 0.7), (1.2, "cat_meow", 0.4)], music="tension")
S("L43", set="ch", cam=orbit("ct_lawyer", -8), chars=[LAWYER("happy", "both_up")], sfx=[(1.0, "crowd_laugh", 0.3)], music="playful")
S("L44", set="ch", cam=push("ct_wide", 0.15), chars=[BISHOP("tired", "shrug"), LAWYER("happy", "raise", at=(-1.0, 2.6, 0))], sfx=[(0.6, "crowd_murmur", 0.3)])
S("L45", set="ct", cam=push("ct_judge", 0.08), chars=[A("lawyer", [0, 8.0, 1.5], 1.6, "R", "neutral", "down", cut=[7.15, 2.22], old=True)], part=(0, 0.5), tag="YEARS LATER")
S("L45", set="ct", cam=push("ct_side", 0.12), chars=[A("villager6", [2.5, 3.0, 0], 1.5, "L", "worried", "point_l"), A("lawyer", [0.6, 3.6, 0], 1.5, "R", "happy")], part=(0.5, 1.0))

# ================================================================ CH 4 The Rooster of Basel
S("L46", "card", num=4, text="THE ROOSTER OF BASEL", music="dark")
S("L46", set="nt", cam=push("nt_wide", 0.12), chars=[], tag="BASEL, SWITZERLAND · 1474", sfx=[(0, "owl", 0.5), (0, "wind", 0.4)])
S("L47", set="ct", cam=push("ct_dock", 0.12), chars=[A("rooster", [-3.6, 1.1, 0.3], 0.7, "R", "surprised", cut=[-0.1, 0.7])], sfx=[(0.2, "rooster", 0.6), (1.5, "gavel", 0.5)])
S("L48", set="ct", cam=push("ct_dock", 0.25, 1.15), chars=[A("rooster", [-3.6, 1.1, 0.3], 0.7, "R", "surprised", cut=[-0.1, 0.7])], props=[("egg", [-3.15, 0.85, 0.78], 0.16, {"pop": 0.3})], pop=[(0.45, "LAYING AN EGG")], sfx=[(0.3, "pop", 0.7), (0.5, "crowd_gasp", 0.5)])
S("L49", set="st", cam=push("st_wy", 0.12), chars=[WY("happy", "shrug")], part=(0, 0.45))
S("L49", set="nt", cam=push("nt_crowd", 0.12), chars=[A(f"villager{i}", [x, 3.0 + (i % 2), 0], 1.45, "R" if x < 0 else "L", "worried") for i, x in enumerate([-2.2, -1.0, 1.0, 2.3])], part=(0.45, 1.0), sfx=[(0, "crowd_murmur", 0.4)])
S("L50", "doc", doc="basilisk", sfx=[(0.3, "riser", 0.5), (1.6, "cat_hiss", 0.3)])
S("L51", "doc", doc="potion", sfx=[(0.2, "sparkle", 0.4)])
S("L52", set="nt", cam=crane("nt_crowd", 0.8), chars=[A(f"villager{i}", [x, 4 + (i % 3) * 0.6, 0], 1.45, "R" if x < 0 else "L", "surprised", glow=True) for i, x in enumerate([-3.0, -1.8, -0.6, 0.7, 1.9, 3.1])], sfx=[(0, "fire", 0.6), (0, "crowd_murmur", 0.4)])
S("L53", set="ld", cam=push("ld_field", 0.15), chars=[A("rooster", [3.4, 2.8, 0], 0.6, "L", "neutral"), A("rooster", [5.0, 3.4, 0], 0.55, "L", "happy", hen=True)], tag="SCIENCE TODAY", sfx=[(0.5, "rooster", 0.4), (0, "birds", 0.3)], music="curious")
S("L54", set="nt", cam=push("nt_crowd", 0.15), chars=[A("magistrate", [0, 3.4, 0], 1.55, "R", "angry", "point_r")], sfx=[(0, "fire", 0.4)], music="dark")

# ================================================================ CH 5 The Weevils' Land Deal
S("L55", "card", num=5, text="THE WEEVILS' LAND DEAL", music="playful")
S("L55", set="st", cam=push("st_close", 0.12), chars=[WY("smug", "point_r")])
S("L56", set="vn", cam=push("vn_wide", 0.15), chars=[], tag="SAINT-JULIEN, ALPS", sfx=[(0, "birds", 0.4), (0, "wind", 0.3)])
S("L57", set="vn", cam=push("vn_close", 0.2), chars=[A("weevil", [2.7, 3.45, 0.55], 0.32, "R", "smug"), A("weevil", [3.3, 3.5, 0.7], 0.28, "L", "happy")], tag="1545", sfx=[(0.3, "chewing", 0.6)])
S("L58", set="ch", cam=push("ct_wide", 0.15), chars=[BISHOP("neutral"), A("weevil", [-3.6, 1.1, 1.22], 0.22, "R", "smug"), LAWYER("smug", "point_r", at=(-1.8, 2.4, 0)), A("lawyer", [-0.8, 2.8, 0], 1.45, "L", "happy", "raise")], pop=[(0.75, "TWO LAWYERS")])
S("L59", set="ch", cam=push("ct_judge", 0.12), chars=[BISHOP("neutral", "raise")], sfx=[(0.6, "hmm", 0.3)])
S("L60", set="ch", cam=orbit("ct_judge", 6), chars=[BISHOP("happy", "both_up")], sfx=[(0, "church_bell", 0.3)])
S("L61", set="ch", cam=push("ct_judge", 0.15, 1.1), chars=[BISHOP("smug", "point_l")], props=[("sack", [0.9, 7.0, 2.3], 0.35, {"pop": 0.2})], pop=[(0.45, "PAY YOUR TITHES")], sfx=[(0.4, "coins", 0.7)])
S("L62", set="vn", cam=push("vn_mid", 0.12), chars=[A("monk", [0.4, 1.0, 0], 1.45, "R", "happy", "both_up"), A("villager1", [-0.6, 0.6, 0], 1.45, "R", "happy"), A("weevil", [2.4, 3.2, 0.5], 0.5, "R", "worried", walk={"to": [4.5, 3.2, 0.6]})], sfx=[(0, "church_bell", 0.4), (1.0, "whoosh_soft", 0.4)])
S("L63", set="vn", cam=push("vn_close", 0.15), chars=[A("weevil", [2.4 + 0.3 * k, 3.45 + 0.05 * (k % 2), 0.45 + 0.08 * (k % 3)], 0.28, "R" if k % 2 else "L", "smug") for k in range(5)], tag="1587", pop=[(0.3, "THEY'RE BACK")], sfx=[(0.3, "insects", 0.6)])
S("L64", set="st", cam=push("st_wy", 0.1), chars=[WY("smug", "chin")])
S("L65", set="sqa", cam=push("sq_alpine", 0.15), chars=[A(f"villager{i}", [x, y, 0], 1.45, "R" if x < 2 else "L", "happy", "raise" if i % 2 else "down") for i, (x, y) in enumerate([(-3, 1), (-1.8, 2.2), (-0.5, 0.6), (4.5, 1.6), (6, 0.4), (3.2, 2.6)])] + [A("crier", [2, 5, 1.2], 1.5, "L", "happy", "present", hold_r="scroll")], sfx=[(0, "church_bell", 0.5), (1.5, "crowd_murmur", 0.4)])
S("L66", "doc", doc="deed", sfx=[(0, "paper", 0.5), (1.0, "quill", 0.4)])
S("L67", set="ch", cam=push("ct_lawyer", 0.15), chars=[LAWYER("angry", "point_r", hold_l="scroll"), A("weevil", [-2.3, 2.2, 0.0], 0.25, "R", "angry")], pop=[(0.6, "TOO POOR!")], sfx=[(0.4, "thud", 0.4)])
S("L68", set="vn", cam=pan("vn_wide", 1.5), chars=[A("villager4", [0.5, 1.5, 0], 1.45, "R", "neutral", "point_r"), A("villager6", [1.6, 2.0, 0], 1.45, "R", "neutral", hold_r="scroll")], sfx=[(0, "footsteps", 0.4)])
S("L69", set="ch", cam=push("ct_judge", 0.15, 1.1), chars=[BISHOP("neutral", "down")], pop=[(0.65, "NOBODY KNOWS")], sfx=[(0.3, "drum_hit", 0.5)])
S("L70", "doc", doc="eaten", sfx=[(0.3, "chewing", 0.6), (1.5, "rat_squeak", 0.4)])

# ================================================================ CH 6 The Real Why
S("L71", "card", num=6, text="THE REAL WHY", music="curious")
S("L71", set="st", cam=push("st_wide", 0.18), chars=[WY("neutral", "chin")])
S("L72", set="sq", cam=push("sq_wide", 0.12), chars=CROWD_SQ[:6] + [A("crier", [2, 5, 1.2], 1.5, "L", "neutral", "raise", hold_r="scroll")], part=(0, 0.45), tag="IDEA 1: ORDER")
S("L72", set="ct", cam=orbit("ct_wide", 6), chars=[JUDGE("neutral", "raise", hold_r="gavel"), PIG_DOCK("worried")], part=(0.45, 1.0), sfx=[(0.6, "gavel", 0.4)])
S("L73", set="st", cam=push("st_close", 0.12), chars=[WY("smug", "raise", hold_r="coin")], tag="IDEA 2: MONEY", sfx=[(0.3, "coin_single", 0.6)])
S("L74", set="ch", cam=push("ct_judge", 0.1), chars=[BISHOP("smug", "point_l")], props=[("sack", [0.9, 7.0, 2.3], 0.35, {})], sfx=[(0, "whoosh_soft", 0.4)])
S("L75", "doc", doc="tithe", sfx=[(0.2, "coins", 0.5)])
S("L76", "doc", doc="paper2013", sfx=[(0, "page_turn", 0.5)])
S("L77", set="st", cam=push("st_wy", 0.12), chars=[WY("happy", "point_r")], sfx=[(0.2, "ding", 0.4)])
S("L78", set="vn", cam=push("vn_mid", 0.12), chars=[A("bishop", [0.2, 1.0, 0], 1.5, "R", "happy", "both_up"), A("weevil", [2.4, 3.2, 0.5], 0.5, "R", "worried", walk={"to": [4.6, 3.3, 0.6]})], pop=[(0.75, "IT WORKED!")], sfx=[(0.6, "sparkle", 0.5)])
S("L79", set="vn", cam=push("vn_mid", 0.12), chars=[A("bishop", [0.2, 1.0, 0], 1.5, "R", "angry", "point_r"), A("farmer", [-0.9, 0.6, 0], 1.45, "R", "worried"), A("weevil", [2.4, 3.2, 0.5], 0.5, "L", "smug")], pop=[(0.65, "YOUR SINS!")], sfx=[(0.4, "drum_hit", 0.4)])
S("L80", set="ch", cam=pull("ct_wide", 0.15), chars=[BISHOP("happy", "both_up")] + [A(f"villager{i}", [2.5 + (i % 3) * 1.2, 1.5 - (i // 3) * 2.0, 0.0], 1.4, "L", "neutral", "present", hold_r="sack") for i in range(4)], sfx=[(0.3, "coins", 0.5), (1.0, "coins", 0.4)])
S("L81", set="st", cam=push("st_close", 0.12), chars=[WY("neutral", "chin")], pop=[(0.75, "BELIEF")], music="story")

# ================================================================ CH 7 Ending
S("L82", "card", num=7, text="THE END OF ANIMAL TRIALS", music="warm")
S("L82", set="sq", cam=crane("sq_wide", 1.5), chars=[A("pig", [0, 2, 0], 0.7, "R", "happy"), A("villager1", [-2, 1.5, 0], 1.45, "R", "happy")], sfx=[(0, "birds", 0.4)])
S("L83", set="sqd", cam=push("sq_wide2", 0.12), chars=[A("rooster", [-1.5, 1.2, 0], 0.55, "R", "neutral"), A("villager3", [0.5, 1.0, 0], 1.45, "L", "surprised")], tag="STILL HAPPENING IN THE 1700s")
S("L84", set="st", cam=push("st_wy", 0.12), chars=[WY("happy", "point_r"), A("dog", [1.8, 0.4, 0], 0.5, "L", "happy")], sfx=[(1.2, "boing", 0.4)])
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
    if sh.get("skip"):
        continue
    if sh["kind"] == "card":
        d = CARD
        out.append(dict(sh, id=f"S{k:03d}", start=round(t, 3), dur=d, line=None, chapter=int(sh["num"])))
        t += d; k += 1
        continue
    if sh["kind"] == "end":
        out.append(dict(sh, id=f"S{k:03d}", start=round(t, 3), chapter=7)); t += sh["dur"]; k += 1
        continue
    L = T[sh["line"]]
    p0, p1 = sh["part"] or (0, 1)
    gap = GAP + (0.25 if L["text"].rstrip().endswith(("?", "...")) else 0) + (0.2 if L["text"].endswith(("money.", "pig.")) else 0)
    full = L["dur"] + gap
    if sh["line"] != prev_line:
        line_start = t
        prev_line = sh["line"]
    s0 = line_start + full * p0
    s1 = line_start + full * p1
    d = s1 - s0
    out.append(dict(sh, id=f"S{k:03d}", start=round(s0, 3), dur=round(d, 3), chapter=L["chapter"], line_start=round(line_start, 3)))
    if p1 >= 0.999:
        t = line_start + full
    k += 1

plan = {"fps": 30, "resolution": [1920, 1080], "style": "T", "episode": "B-001", "duration": round(t, 2), "shots": out}
(EP / "shots.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False))
print(len(out), "shots, duration", round(t, 1), "s =", f"{int(t // 60)}:{int(t % 60):02d}")
