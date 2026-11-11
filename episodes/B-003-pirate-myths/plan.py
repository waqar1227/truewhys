"""Shot plan for B-003 "pirate myths vs what really happened" (ranked list, items 1 -> 10).
python plan.py  -> shots.json (uses timing.json for exact durations)
Shot kinds: 3d (rendered set + 2D puppets), card (rank card), title, doc, end.
Sets: deck (day | sunset | night | red), islet (day | dig), port (day) from lib/sets5.py; court (town) and study from lib/sets.py.
Every item opens on its strongest image (growth review 11 Nov: hook drop at 10-19 % on every Short).
"""
import json, copy
from pathlib import Path

EP = Path(__file__).parent
T = {t["id"]: t for t in json.loads((EP / "timing.json").read_text())}


def M(pos, tgt, lens):
    return {"pos": pos, "tgt": tgt, "lens": lens}


MK = {
    # deck: main deck z 0 (actors y -1..1 in front of the mainmast at y 1.2), quarterdeck z 1.3, wheel (0,-6.6)
    "dk_hero":  M([2.2, -7.4, 3.0], [-0.2, 3.0, 2.4], 22),
    "dk_deck":  M([1.3, -3.8, 1.5], [0.0, 1.6, 1.1], 28),
    "dk_close": M([0.7, -2.3, 1.35], [0.1, 0.3, 1.12], 30),
    "dk_plank": M([0.6, -0.6, 1.6], [4.2, 2.8, 0.9], 26),
    "dk_flag":  M([2.0, -2.0, 3.0], [0.0, 1.2, 14.2], 30),
    "dk_wheel": M([1.6, -3.4, 2.4], [0.0, -6.6, 2.0], 30),
    "dk_out":   M([-16, -12, 3.0], [0, 1, 5.0], 30),
    "dk_chest": M([-0.3, -1.3, 1.45], [-1.6, -3.4, 0.8], 30),
    "dk_rail":  M([0.4, -1.4, 2.0], [-36, 62, 2.0], 34),
    # islet: sand mound centre (0,3), palm (1.3,4.2); dig: hole (-0.6,2.6)
    "is_hero":  M([0.4, -4.6, 1.4], [0.0, 3.2, 0.9], 26),
    "is_wide":  M([6.0, -14.0, 4.0], [0.0, 4.0, 0.5], 24),
    "is_dig":   M([1.6, -1.6, 1.4], [-0.4, 2.6, 0.55], 30),
    # port market: parrot stall (1.6,2.2), fruit stall (-2.4,2.6)
    "pt_hero":  M([0.2, -4.4, 1.5], [0.4, 3.0, 1.4], 24),
    "pt_cages": M([0.4, -0.8, 1.5], [1.6, 2.2, 1.45], 30),
    # court (B-001/B-002): bench y 7.6, dock (-3.6,1.0)
    "ct_wide":  M([1.5, -9.5, 3.2], [0, 6, 2.0], 22),
    "ct_dock":  M([-2.2, -3.2, 1.6], [-3.6, 1.0, 1.1], 30),
    # study (Wy)
    "st_wy":    M([0.6, -2.6, 1.0], [0.6, 0.55, 0.75], 32),
    "st_close": M([0.6, -2.0, 1.0], [0.6, 0.55, 0.82], 32),
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


def crane(mk, dz=1.0):
    a = MK[mk]
    b = copy.deepcopy(a); b["pos"][2] += dz
    return {"from": a, "to": b, "ease": "inout"}


def shake(mk, amt=0.08, amp=0.03):
    c = push(mk, amt); c["shake"] = amp
    return c


def A(c, at, h=1.5, face="R", expr="neutral", arms="down", **kw):
    d = dict(c=c, at=list(at), h=h, face=face, expr=expr, arms=arms)
    d.update(kw)
    return d


SETS = {"dk": ("deck", "day"), "dkn": ("deck", "night"), "dks": ("deck", "sunset"), "dkr": ("deck", "red"),
        "is": ("islet", "day"), "isd": ("islet", "dig"), "pt": ("port", "day"), "ct": ("court", "town"), "st": ("study", "day")}

WY = lambda expr="happy", arms="down", **kw: A("wy", [0.6, 0.55, 0], 1.25, "R", expr, arms, talk=True, **kw)
CAP = lambda expr="smug", arms="down", at=(-0.8, 0.2, 0), face="R", **kw: A("captain", at, 1.6, face, expr, arms, **kw)
P1 = lambda expr="happy", arms="down", at=(0.9, 0.0, 0), face="L", **kw: A("pirate", at, 1.5, face, expr, arms, **kw)
P2 = lambda expr="smug", arms="down", at=(0.2, -0.3, 0), face="R", **kw: A("pirate2", at, 1.5, face, expr, arms, **kw)
P3 = lambda expr="happy", arms="down", at=(1.7, 0.5, 0), face="L", **kw: A("pirate3", at, 1.45, face, expr, arms, **kw)
QM = lambda expr="neutral", arms="present", at=(-0.9, -2.6, 0), face="R", **kw: A("quartermaster", at, 1.55, face, expr, arms, **kw)
ANNE = lambda expr="smug", arms="down", at=(-0.6, -0.2, 0), face="R", **kw: A("anne", at, 1.45, face, expr, arms, **kw)
MARY = lambda expr="smug", arms="down", at=(0.6, -0.1, 0), face="L", **kw: A("mary", at, 1.45, face, expr, arms, **kw)
MER = lambda expr="worried", arms="down", at=(1.0, 0.0, 0), face="L", **kw: A("merchant", at, 1.5, face, expr, arms, **kw)
CREW = lambda expr="happy", arms="down": [P1(expr, arms, at=(1.0, 0.4, 0)), P2(expr, arms, at=(-0.2, -0.2, 0), face="L"),
                                         P3(expr, arms, at=(1.9, 0.9, 0)), QM(expr, arms if arms != "present" else "down", at=(-1.2, 0.6, 0))]

SHOTS = []


def S(line, kind="3d", set=None, cam=None, chars=(), part=None, **kw):
    sh = dict(line=line, kind=kind, set=SETS[set][0] if set else None, variant=SETS[set][1] if set else None,
              cam=cam, chars=list(chars), part=part)
    sh.update(kw)
    SHOTS.append(sh)


def RANK(line, n, title):
    S(line, "card", num=n, text=title, sub=f"MYTH #{n}" if n < 10 else "AND FINALLY")


# ================================================================ COLD OPEN (ch 0)
S("L01", set="dk", cam=push("dk_close", 0.12), chars=[P2("smug", "point_r", at=(0.3, 0.0, 0))], part=(0, 0.27),
  pop=[(0.05, "EYE PATCHES?")], sfx=[(0, "whoosh", 0.5), (0, "waves", 0.35)], music="adventure")
S("L01", set="pt", cam=push("pt_cages", 0.12), chars=[], part=(0.27, 0.5), pop=[(0.05, "PARROTS?")], sfx=[(0.05, "pop", 0.4)])
S("L01", set="dk", cam=push("dk_plank", 0.12), chars=[MER("worried", "both_up", at=(3.7, 2.6, 1.03), face="L")], part=(0.5, 0.75),
  pop=[(0.05, "THE PLANK?")], sfx=[(0.05, "pop", 0.4)])
S("L01", set="isd", cam=push("is_dig", 0.12), chars=[], part=(0.75, 1), pop=[(0.05, "BURIED TREASURE?")], sfx=[(0.05, "pop", 0.4)])
S("L02", set="dks", cam=pull("dk_out", 0.12), chars=[], tag="THE GOLDEN AGE OF PIRACY", sfx=[(0, "waves", 0.5), (0.3, "gulls", 0.3)])
S("L03", set="st", cam=push("st_close", 0.12), chars=[WY("smug", "point_r")], pop=[(0.5, "BOOKS & MOVIES")], sfx=[(0.45, "pop", 0.4)])
S("L04", "title", text="10 PIRATE \"FACTS\"\nMYTH OR REAL?", sfx=[(0, "whoosh", 0.7), (0.3, "drum_hit", 0.6)], music="curious")
S("L05", set="dk", cam=push("dk_deck", 0.15), chars=CREW("happy") + [CAP("smug", "point_r", at=(-0.6, -1.0, 0))],
  pop=[(0.7, "STRANGER THAN THE MOVIES")], sfx=[(0.6, "riser", 0.4)])

# ================================================================ 1 ARRR (ch 1)
RANK("L06", 1, "PIRATES SAID \"ARRR!\"")
S("L06", set="dk", cam=shake("dk_close", 0.1, 0.02), chars=[CAP("angry", "both_up", at=(0.1, 0.1, 0))], pop=[(0.45, "ARRR!")],
  sfx=[(0.4, "boing", 0.4), (0, "waves", 0.3)], music="playful")
S("L07", set="st", cam=push("st_close", 0.1), chars=[WY("smug", "raise")], pop=[(0.15, "MYTH!")], sfx=[(0.1, "pop", 0.5)])
S("L08", "doc", doc="film1950", sfx=[(0, "paper", 0.6)])
S("L09", set="dk", cam=push("dk_close", 0.1), chars=[CAP("happy", "present", at=(0.1, 0.1, 0))], tag="THE WEST COUNTRY, ENGLAND",
  pop=[(0.7, "\"ARR\" = \"YES\"")], sfx=[(0.65, "ding", 0.4)])
S("L10", set="dk", cam=pan("dk_deck", 0.8), chars=CREW("happy", "wave") + [ANNE("happy", at=(-1.9, 0.9, 0))], pop=[(0.45, "FROM ALL OVER THE WORLD")],
  sfx=[(0.3, "crowd_murmur", 0.3)])
S("L11", set="dk", cam=push("dk_deck", 0.1), chars=CREW("happy"), tag="NO SINGLE PIRATE VOICE")

# ================================================================ 2 PARROTS (ch 1)
RANK("L12", 2, "EVERY PIRATE HAD A PARROT")
S("L12", set="pt", cam=push("pt_cages", 0.15), chars=[CAP("happy", "point_r", at=(0.3, 1.6, 0))], sfx=[(0.2, "birds", 0.5)], music="playful")
S("L13", set="st", cam=push("st_wy", 0.12), chars=[WY("neutral", "shrug")], pop=[(0.2, "MOSTLY A MYTH")], sfx=[(0.15, "hmm", 0.4)])
S("L14", set="pt", cam=push("pt_cages", 0.12), chars=[P1("happy", "present", at=(0.5, 1.6, 0), face="R", hold_l="coins")], part=(0, 0.55),
  sfx=[(0.3, "birds", 0.4)])
S("L14", set="pt", cam=push("pt_cages", 0.1, 1.12), chars=[], part=(0.55, 1), pop=[(0.05, "CARGO TO SELL")], sfx=[(0.05, "coins", 0.5)])
S("L15", set="pt", cam=pan("pt_hero", 0.8), chars=[MER("happy", "present", at=(0.6, 1.2, 0), face="R"), P1("happy", "point_r", at=(-1.2, 1.4, 0), face="R"),
  A("villager2", [-2.4, 1.8, 0], 1.45, "R", "neutral"), A("villager5", [3.0, 2.0, 0], 1.45, "L", "happy")], tag="JAMAICA · 1680s",
  sfx=[(0, "crowd_murmur", 0.4), (0.3, "birds", 0.3)])
S("L16", "doc", doc="book1883", sfx=[(0, "paper", 0.6)])

# ================================================================ 3 EYE PATCHES (ch 2)
RANK("L17", 3, "PIRATES WORE EYE PATCHES")
S("L17", set="dk", cam=push("dk_close", 0.14), chars=[P2("smug", "down", at=(0.2, 0.1, 0))], sfx=[(0, "waves", 0.3)], music="curious")
S("L18", set="st", cam=push("st_close", 0.1), chars=[WY("neutral", "chin")], pop=[(0.6, "BUT WHY?")], sfx=[(0.5, "hmm", 0.4)])
S("L19", set="dkn", cam=push("dk_deck", 0.12), chars=[P2("smug", "point_l", at=(0.2, 0.0, 0))], pop=[(0.55, "ONE EYE READY FOR THE DARK")],
  sfx=[(0.1, "creak", 0.4)], music="mystery")
S("L20", set="dkn", cam=push("dk_close", 0.12), chars=[P2("surprised", "down", at=(0.2, 0.1, 0))], pop=[(0.45, "20+ MINUTES TO ADJUST")],
  sfx=[(0.4, "tick", 0.4)])
S("L21", set="st", cam=push("st_wy", 0.12), chars=[WY("worried", "shrug")], pop=[(0.6, "NO EVIDENCE")], sfx=[(0.55, "thud", 0.4)])
S("L22", set="dk", cam=push("dk_close", 0.1), chars=[P2("neutral", "down", at=(0.2, 0.1, 0))], tag="AN EYE LOST IN A FIGHT", music="curious")

# ================================================================ 4 THE PLANK (ch 2)
RANK("L23", 4, "WALKING THE PLANK")
S("L23", set="dk", cam=push("dk_plank", 0.14), chars=[MER("worried", "both_up", at=(3.7, 2.6, 1.03), face="L"), CAP("angry", "point_r", at=(1.2, 2.2, 0))],
  sfx=[(0.1, "creak", 0.5), (0, "waves", 0.4)], music="tension")
S("L24", set="st", cam=push("st_close", 0.1), chars=[WY("smug", "raise")], pop=[(0.1, "ALMOST NEVER")], sfx=[(0.05, "pop", 0.5)], music="playful")
S("L25", set="dk", cam=pull("dk_plank", 0.12), chars=[], tag="ONLY A HANDFUL OF PROVEN CASES", sfx=[(0, "waves", 0.4)])
S("L26", set="st", cam=push("st_wy", 0.12), chars=[WY("happy", "present", hold_r="scroll")], pop=[(0.35, "STORYBOOKS")], sfx=[(0.3, "paper", 0.5)])
S("L27", set="is", cam=push("is_wide", 0.18), chars=[P1("worried", "down", at=(-0.4, 3.0, 0.32), face="R")], pop=[(0.55, "MAROONED")],
  sfx=[(0, "waves", 0.5), (0.3, "wind", 0.3)], music="mystery")

# ================================================================ 5 BURIED TREASURE (ch 3)
RANK("L28", 5, "BURIED TREASURE, X MARKS THE SPOT")
S("L28", set="isd", cam=push("is_dig", 0.12), chars=[CAP("happy", "present", at=(0.6, 1.6, 0.25), face="L", hold_l="map")], sfx=[(0.2, "shovel", 0.5)], music="adventure")
S("L29", set="st", cam=push("st_close", 0.1), chars=[WY("smug", "raise")], pop=[(0.1, "MYTH!")], sfx=[(0.05, "pop", 0.5)])
S("L30", set="pt", cam=push("pt_hero", 0.12), chars=[P1("happy", "raise", at=(-0.8, 1.0, 0), hold_r="tankard"), P3("happy", "raise", at=(0.6, 1.2, 0), hold_r="coins", face="L"),
  P2("happy", "wave", at=(2.0, 1.6, 0), face="L")], pop=[(0.7, "SPENT FAST")], sfx=[(0.2, "crowd_laugh", 0.4), (0.6, "coins", 0.5)], music="playful")
S("L31", set="isd", cam=push("is_hero", 0.12), chars=[CAP("smug", "present", at=(0.4, 2.0, 0.3), face="L")], tag="CAPTAIN WILLIAM KIDD", music="mystery")
S("L32", set="isd", cam=push("is_dig", 0.14), chars=[CAP("worried", "down", at=(0.6, 1.6, 0.25), face="L", hold_r="shovel")], tag="GARDINERS ISLAND · 1699",
  sfx=[(0.3, "shovel", 0.5)])
S("L33", "doc", doc="kidd1699", sfx=[(0, "paper", 0.6)])
S("L34", set="st", cam=push("st_wy", 0.12), chars=[WY("smug", "present", hold_r="map")], pop=[(0.5, "FROM STORIES")], sfx=[(0.45, "pop", 0.4)])

# ================================================================ 6 JOLLY ROGER (ch 3)
RANK("L35", 6, "THE SKULL AND CROSSBONES")
S("L35", set="dk", cam=push("dk_flag", 0.12), chars=[], sfx=[(0, "wind", 0.5), (0.2, "flag_flap", 0.4)], music="adventure")
S("L36", set="st", cam=push("st_close", 0.1), chars=[WY("happy", "both_up")], pop=[(0.1, "TRUE!")], sfx=[(0.05, "ding", 0.5)])
S("L37", set="dk", cam=push("dk_rail", 0.1), chars=[CAP("angry", "point_l", at=(-0.6, 1.0, 0), face="L")], pop=[(0.6, "SURRENDER NOW!")], sfx=[(0.5, "drum_hit", 0.5)])
S("L38", set="dk", cam=shake("dk_deck", 0.1, 0.02), chars=CREW("worried"), tag="A FIGHT COULD SINK THE PRIZE", sfx=[(0.2, "cannon", 0.4)], music="tension")
S("L39", set="dk", cam=pull("dk_out", 0.1), chars=[], pop=[(0.5, "THEY GAVE UP")], sfx=[(0, "waves", 0.4)])
S("L40", set="dkr", cam=push("dk_flag", 0.14), chars=[], part=(0, 0.6), sfx=[(0.1, "wind", 0.5)], music="tension")
S("L40", set="dkr", cam=shake("dk_deck", 0.1, 0.02), chars=[CAP("angry", "point_l", at=(0.1, 0.2, 0))], part=(0.6, 1), pop=[(0.05, "NO MERCY")],
  sfx=[(0.0, "drum_hit", 0.6)])

# ================================================================ 7 NO RULES (ch 4)
RANK("L41", 7, "PIRATES HAD NO RULES")
S("L41", set="dk", cam=push("dk_deck", 0.12), chars=CREW("angry", "both_up"), sfx=[(0.1, "crowd_murmur", 0.4)], music="playful")
S("L42", "doc", doc="roberts", sfx=[(0, "paper", 0.6)])
S("L43", set="dks", cam=push("dk_deck", 0.12), chars=[CAP("neutral", "point_r", at=(-0.6, 0.0, 0)), P1("tired", "down", at=(0.9, 0.3, 0))], tag="BARTHOLOMEW ROBERTS",
  pop=[(0.75, "LIGHTS OUT: 8 PM")], sfx=[(0.7, "bell", 0.5)])
S("L44", set="dkn", cam=push("dk_deck", 0.1), chars=[P3("happy", "raise", at=(0.6, 0.4, 0), hold_r="tankard"), P1("tired", "down", at=(-0.6, 0.2, 0), face="R")],
  pop=[(0.6, "IN THE DARK")], sfx=[(0.1, "waves", 0.4), (0.4, "drink", 0.4)], music="mystery")
S("L45", set="dk", cam=push("dk_close", 0.1), chars=[P1("angry", "point_l", at=(0.9, 0.2, 0)), P2("angry", "point_r", at=(-0.4, 0.0, 0))],
  pop=[(0.55, "NO GAMBLING · NO FIGHTS")], sfx=[(0.1, "coin_single", 0.5), (0.5, "drum_hit", 0.4)], music="playful")
S("L46", set="is", cam=push("is_hero", 0.12), chars=[P1("angry", "point_l", at=(1.0, 2.6, 0.3)), P2("angry", "point_r", at=(-0.8, 2.6, 0.3))],
  pop=[(0.3, "SETTLE IT ON LAND")], sfx=[(0, "waves", 0.4)])

# ================================================================ 8 INJURY INSURANCE (ch 4)
RANK("L47", 8, "PIRATES GOT INJURY INSURANCE")
S("L47", set="dk", cam=push("dk_close", 0.12), chars=[P2("worried", "down", at=(0.2, 0.1, 0))], sfx=[(0.1, "creak", 0.4)], music="curious")
S("L48", set="st", cam=push("st_close", 0.1), chars=[WY("surprised", "both_up")], pop=[(0.45, "TRUE!")], sfx=[(0.4, "ding", 0.5)])
S("L49", set="dk", cam=push("dk_chest", 0.12), chars=[QM("neutral", "present", at=(-0.7, -2.6, 0), face="L")], tag="BUCCANEERS · 1670s", sfx=[(0.3, "coins", 0.4)])
S("L50", "doc", doc="injuries", sfx=[(0, "paper", 0.6)])
S("L51", set="dk", cam=push("dk_close", 0.12), chars=[P2("happy", "raise", at=(0.2, 0.1, 0), hold_r="coins")], pop=[(0.7, "AN EYE: 100")], sfx=[(0.6, "coins", 0.5)])
S("L52", set="dk", cam=push("dk_chest", 0.14), chars=[QM("happy", "present", at=(-0.7, -2.6, 0), face="L", hold_r="coins")], pop=[(0.4, "A SMALL FORTUNE")],
  sfx=[(0.3, "coins", 0.6)])

# ================================================================ 9 THE CAPTAIN (ch 5)
RANK("L53", 9, "THE CAPTAIN WAS THE BOSS")
S("L53", set="dk", cam=push("dk_wheel", 0.12), chars=[CAP("smug", "present", at=(0.6, -6.3, 1.3), face="L")], sfx=[(0.1, "creak", 0.4)], music="story")
S("L54", set="st", cam=push("st_wy", 0.12), chars=[WY("neutral", "shrug")], pop=[(0.1, "ONLY SOMETIMES")], sfx=[(0.05, "hmm", 0.4)])
S("L55", set="dk", cam=push("dk_deck", 0.12), chars=CREW("happy", "raise") + [CAP("worried", "down", at=(-0.4, -1.2, 0))], pop=[(0.45, "VOTE!")],
  sfx=[(0.4, "crowd_cheer", 0.5)])
S("L56", set="dk", cam=push("dk_chest", 0.12), chars=[QM("smug", "present", at=(-0.7, -2.6, 0), face="L")], tag="THE QUARTERMASTER", part=(0, 0.5),
  sfx=[(0.2, "coins", 0.4)])
S("L56", set="dk", cam=push("dk_close", 0.1), chars=[CAP("angry", "point_r", at=(-0.3, 0.0, 0))], part=(0.5, 1), pop=[(0.1, "BATTLE: CAPTAIN'S WORD")],
  sfx=[(0.1, "drum_hit", 0.4)])
S("L57", set="dk", cam=crane("dk_deck", 0.6), chars=CREW("happy", "raise"), pop=[(0.6, "EVERYONE GETS A VOTE")], sfx=[(0.5, "crowd_cheer", 0.4)])

# ================================================================ 10 WOMEN PIRATES (ch 5)
RANK("L58", 10, "WOMEN PIRATES")
S("L58", set="dk", cam=push("dk_close", 0.12), chars=[ANNE("smug", "down", at=(-0.3, 0.0, 0)), MARY("smug", "down", at=(0.7, 0.1, 0))], sfx=[(0, "waves", 0.3)],
  music="adventure")
S("L59", set="st", cam=push("st_close", 0.1), chars=[WY("happy", "both_up")], pop=[(0.1, "TRUE!")], sfx=[(0.05, "ding", 0.5)])
S("L60", set="dk", cam=push("dk_hero", 0.14), chars=[ANNE("happy", "wave", at=(-0.6, -1.6, 0)), MARY("happy", "down", at=(0.6, -1.4, 0)),
  CAP("smug", "down", at=(1.6, -1.0, 0), face="L")], tag="THE CARIBBEAN · 1720", sfx=[(0, "waves", 0.4)])
S("L61", set="ct", cam=push("ct_wide", 0.12), chars=[A("judge", [0, 7.6, 1.2], 1.6, "L", "angry"), ANNE("worried", at=(-3.9, 1.1, 0.3), cut=[-0.1, 1.05]),
  MARY("worried", at=(-3.2, 1.0, 0.3), cut=[-0.1, 1.05], face="R")], part=(0, 0.5), tag="JAMAICA", sfx=[(0.3, "crowd_murmur", 0.4)], music="tension")
S("L61", "doc", doc="trial1720", part=(0.5, 1), sfx=[(0.1, "gavel", 0.7)])
S("L62", set="ct", cam=push("ct_dock", 0.1), chars=[ANNE("surprised", at=(-3.9, 1.1, 0.3), cut=[-0.1, 1.05]), MARY("surprised", at=(-3.2, 1.0, 0.3), cut=[-0.1, 1.05], face="R")],
  pop=[(0.7, "EXECUTION STOPPED")], sfx=[(0.6, "crowd_gasp", 0.5)])
S("L63", set="dks", cam=pull("dk_out", 0.14), chars=[], pop=[(0.75, "FATE: UNKNOWN")], sfx=[(0, "waves", 0.5), (0.4, "gulls", 0.3)], music="mystery")

# ================================================================ OUTRO (ch 6)
S("L64", set="st", cam=push("st_wy", 0.12), chars=[WY("smug", "shrug")], pop=[(0.2, "MYTHS")], sfx=[(0.15, "pop", 0.4)], music="warm")
S("L65", set="dk", cam=push("dk_deck", 0.12), chars=CREW("happy", "raise") + [ANNE("happy", "wave", at=(-1.9, 0.9, 0))], pop=[(0.6, "ALL REAL!")], sfx=[(0.5, "crowd_cheer", 0.4)])
S("L66", set="dks", cam=crane("dk_hero", 1.0), chars=[], sfx=[(0, "waves", 0.4), (0.3, "gulls", 0.3)])
S("L67", set="st", cam=push("st_close", 0.12), chars=[WY("happy", "point_r")], pop=[(0.55, "WHICH ONE?")], sfx=[(0.5, "pop", 0.4)])
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
        out.append(dict(sh, id=f"S{k:03d}", start=round(t, 3), chapter=6)); t += sh["dur"]; k += 1
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

plan = {"fps": 30, "resolution": [1920, 1080], "style": "T", "episode": "B-003", "duration": round(t, 2), "shots": out}
(EP / "shots.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False))
print(len(out), "shots, duration", round(t, 1), "s =", f"{int(t // 60)}:{int(t % 60):02d}")
