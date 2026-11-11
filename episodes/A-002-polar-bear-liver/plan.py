"""A-002 "Why You Should Never Eat Polar Bear Liver" (standalone Short, Style T, 9:16).
Set: arctic:night (lib/sets3.set_arctic): camp fire at (0.6, 1.2), tent, sledge, ship held in the ice at (4.5, 17), aurora.
New for this Short: magnifier scenes "foodchain", "peel" (cartoon flakes, no gore), "dose" (gauge) in lib/gfx.LENS_SCENES.
Growth review 11 Nov: payoff image (the liver at the sailor's mouth + Wy's STOP) from frame 1; 25-40 s.
python episodes/A-002-polar-bear-liver/plan.py -> shots.json
"""
import sys
from pathlib import Path
EP = Path(__file__).parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from ashort import M, push, pull, pan, crane, shake, A, S, finish

HOOK = M([0.6, -1.6, 1.0], [0.6, 0.55, 1.05], 26)      # sailor with the liver at his mouth (left), Wy lunging in (right), fire between
TIGHT = M([0.3, -0.6, 1.12], [0.12, 0.55, 1.05], 26)     # close on the sailor + liver
WIDE = M([-3.5, -5.5, 2.4], [3.0, 14.0, 2.6], 24)        # camp in the foreground, ship held in the ice + aurora behind
CAMP = M([1.1, -1.4, 1.25], [0.25, 1.1, 0.95], 28)         # the camp, sailor by the fire pot
BEAR = M([3.5, 5.6, 1.05], [2.8, 9.4, 0.9], 30)        # polar bear on the ice beyond the camp
WYC = M([2.2, -1.2, 1.05], [1.6, 1.4, 0.95], 30)         # Wy close by the fire

def SAILOR(expr="happy", arms="chin", at=(0.05, 0.55, 0), **kw):
    return A("sailor", list(at), 1.45, "R", expr, arms, hold="liver", **kw)

def SICK(expr="tired", arms="down", at=(0.05, 0.55, 0), **kw):
    return A("sailor", list(at), 1.45, "R", expr, arms, **kw)

def WY(expr="surprised", arms="both_up", at=(1.6, 1.05, 0), face="L", **kw):
    return A("wy", list(at), 1.25, face, expr, arms, **kw)

def PB(at=(3.0, 8.7, 0), face="R", expr="neutral", **kw):
    return A("polar_bear", list(at), 1.3, face, expr, **kw)

# hook: the payoff image from frame 1: liver at the sailor's mouth, Wy lunging "STOP!"
S("H1", set="arctic:night", cam=push(HOOK, 0.18), chars=[SAILOR("happy", "raise", posed=True), WY("surprised", "both_up", at=(1.15, 0.5, 0), blink_fast=True)], part=(0, 0.55),
  pop=[[0.02, "DON'T EAT IT!", 1.4]], sfx=[[0, "whoosh_soft", 0.5], [0.05, "boing", 0.35], [0, "wind", 0.3]], music="tension")
S("H1", set="arctic:night", cam=push(TIGHT, 0.12), chars=[SAILOR("surprised", "raise")], part=(0.55, 1),
  pop=[[0.05, "POLAR BEAR LIVER", 1.0]], sfx=[[0.05, "hmm", 0.4]])
S("L01", set="arctic:night", cam=pan(WIDE, 1.4, 0.0), chars=[SAILOR("neutral", "hold")], part=(0, 0.5),
  tag="THE ARCTIC, 1597", sfx=[[0.05, "wind", 0.45], [0.2, "whoosh_soft", 0.3]], music="curious")
S("L01", set="arctic:night", cam=push(CAMP, 0.12), chars=[SAILOR("happy", "hold", at=(-0.1, 1.0, 0))], part=(0.5, 1),
  pop=[[0.25, "COOKED IT", 1.15]], sfx=[[0.1, "pop", 0.35]])
S("L02", set="arctic:night", cam=push(TIGHT, 0.1, lens_mult=1.15), chars=[SICK("worried", "down")], part=(0, 0.42),
  pop=[[0.05, "DAYS LATER...", 1.1]], sfx=[[0.1, "gulp", 0.4]], music="tension")
S("L02", set="arctic:night", cam=pull(TIGHT, 0.1), chars=[SICK("tired", "down")], part=(0.42, 1),
  lens=dict(name="peel", at=[0.5, 0.42], rad=0.34), pop=[[0.2, "SKIN PEELING", 1.0]], sfx=[[0.15, "hmm", 0.35]])
S("L03", set="arctic:night", cam=push(WYC, 0.15), chars=[WY("surprised", "point_l", at=(1.6, 1.05, 0), talk=True)], part=(0, 0.33),
  pop=[[0.15, "VITAMIN A", 1.3]], sfx=[[0.1, "ding", 0.4]], music="curious")
S("L03", set="arctic:night", cam=push(BEAR, 0.1), chars=[PB()], part=(0.33, 1),
  lens=dict(name="foodchain", labels=[["FISH", -0.34, 0.86, 0.5], ["SEAL", -0.42, -0.12, 1.75], ["BEAR", 0.26, -0.52, 3.0]], at=[0.5, 0.45]),
  sfx=[[0.15, "pop", 0.3], [1.45, "pop", 0.3], [2.7, "pop", 0.35]])
S("L04", set="arctic:night", cam=push(BEAR, 0.12, lens_mult=1.1), chars=[PB(expr="happy")], part=(0, 0.4),
  pop=[[0.2, "IN THE LIVER", 1.15]], sfx=[[0.1, "riser", 0.3]])
S("L04", set="arctic:night", cam=push(TIGHT, 0.1), chars=[SAILOR("surprised", "hold")], part=(0.4, 1),
  lens=dict(name="dose", labels=[["DAILY LIMIT", 0.42, -0.82, 0.6], ["1 GRAM", 0.42, 0.62, 0.3]], at=[0.5, 0.4], rad=0.34),
  sfx=[[0.3, "riser", 0.35], [1.9, "ding", 0.4]], music="tension")
S("L05", set="arctic:night", cam=shake(TIGHT, 0.1, 0.02), chars=[SICK("tired", "down")], part=(0, 0.5),
  pop=[[0.1, "NO QUICK FLUSH", 1.0]], sfx=[[0.1, "gulp", 0.35]])
S("L05", set="arctic:night", cam=pull(CAMP, 0.12), chars=[SICK("worried", "down", at=(-0.1, 1.0, 0))], part=(0.5, 1),
  pop=[[0.15, "SERIOUSLY ILL", 1.15]], sfx=[[0.1, "thud", 0.4]])
S("L06", set="arctic:night", cam=pan(BEAR, -0.5, 0.0), chars=[PB(face="L", walk={"to": [2.3, 9.2, 0]})], part=(0, 0.6),
  tag="ARCTIC HUNTERS KNEW", sfx=[[0.05, "wind", 0.35]], music="warm")
S("L06", set="arctic:night", cam=push(WYC, 0.12, lens_mult=1.2), chars=[WY("smug", "point_r", talk=True)], part=(0.6, 1),
  pop=[[0.1, "WOULD YOU?", 1.25]], sfx=[[0.05, "hmm", 0.4]])

finish(EP, "Why You Should Never Eat Polar Bear Liver")
