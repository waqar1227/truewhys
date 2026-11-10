"""A-001 "What Happens If You Step Into Quicksand?" (standalone Short, Style T, 9:16).
Sets: marsh:tide (pit at (0,2), Wy sinks there, cut at the sand surface z 0.02) and study (Wy at his desk).
python episodes/A-001-quicksand/plan.py -> shots.json
"""
import sys, os
from pathlib import Path
EP = Path(__file__).parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from ashort import M, push, pull, pan, crane, shake, A, S, finish

PIT = (0.0, 2.0)
CLOSE = M([0.15, -0.6, 0.75], [0.0, 2.0, 0.35], 30)      # Wy waist-deep, eye level
LOW = M([0.4, -0.2, 0.25], [0.0, 2.0, 0.15], 26)         # sand-level close, ripples
WIDE = M([1.2, -5.5, 2.2], [0.0, 3.5, 0.4], 24)          # pit + sea + tide behind
TIDE = M([0.8, -2.5, 1.0], [0.3, 11.0, 0.6], 26)          # looking over Wy to the incoming tide
ST_WY = M([0.6, -2.4, 1.0], [0.6, 0.55, 0.78], 30)


def WY(z=-0.55, expr="surprised", arms="both_up", face="R", **kw):
    return A("wy", [PIT[0], PIT[1], z], 1.25, face, expr, arms, cut=[PIT[1], 0.02], **kw)


WYS = lambda expr="happy", arms="down", **kw: A("wy", [0.6, 0.55, 0], 1.25, "R", expr, arms, talk=True, **kw)

S("H1", set="marsh:tide", cam=push(CLOSE, 0.15), chars=[WY(-0.35, "surprised", "both_up", blink_fast=True, walk={"to": [0, 2.0, -0.6]})],
  pop=[[0.02, "SINKING?!", 1.45]], sfx=[[0, "whoosh_soft", 0.5], [0.1, "splash", 0.4], [0, "wind", 0.3]], music="tension")
S("L01", set="marsh:tide", cam=push(CLOSE, 0.08), chars=[WY(-0.75, "worried", "both_up", walk={"to": [0, 2.0, -0.95]})], part=(0, 0.5),
  pop=[[0.15, "IN MOVIES...", 1.0]], sfx=[[0.1, "gulp", 0.4]])
S("L01", set="marsh:tide", cam=pull(CLOSE, 0.1), chars=[WY(-0.95, "surprised", "shrug", walk={"to": [0, 2.0, -0.55]})], part=(0.5, 1),
  pop=[[0.25, "REAL LIFE: NO", 1.1]], sfx=[[0.1, "boing", 0.4]])
S("L02", set="marsh:tide", cam=push(LOW, 0.12), chars=[], tag="SAND + WATER", sfx=[[0.2, "splash", 0.3]], music="curious")
S("L03", set="marsh:tide", cam=push(WIDE, 0.2), chars=[WY(-0.55, "neutral", "shrug")], part=(0, 0.55), pop=[[0.3, "2× DENSER THAN YOU", 1.0]],
  sfx=[[0.2, "pop", 0.4]])
S("L03", set="marsh:tide", cam=crane(CLOSE, 0.25, -0.05), chars=[WY(-0.55, "happy", "down")], part=(0.55, 1), tag="STOPS AT THE WAIST",
  sfx=[[0.3, "ding", 0.3]])
S("L04", set="marsh:tide", cam=shake(CLOSE, 0.06, 0.025), chars=[WY(-0.55, "angry", "both_up", blink_fast=True)], pop=[[0.55, "= LIFTING A CAR", 1.15]],
  sfx=[[0.4, "thud", 0.5], [0.6, "riser", 0.3]], music="tension")
S("L05", set="study", cam=push(ST_WY, 0.12), chars=[WYS("neutral", "point_r")], part=(0, 0.35), pop=[[0.1, "DON'T YANK", 1.1]], sfx=[[0.05, "tick", 0.4]], music="playful")
S("L05", set="marsh:tide", cam=push(CLOSE, 0.1), chars=[WY(-0.55, "neutral", "shrug")], part=(0.35, 1), pop=[[0.05, "WIGGLE · LEAN BACK · SPREAD OUT", 0.9]],
  sfx=[[0.2, "splash", 0.3]])
S("L06", set="marsh:tide", cam=pan(WIDE, 0.8, 0.4), chars=[WY(-0.5, "happy", "shrug", walk={"to": [1.7, 0.9, -0.15]})], tag="INCH BY INCH",
  sfx=[[0.1, "splash", 0.25], [0, "birds", 0.3]])
S("L07", set="marsh:tide", cam=push(TIDE, 0.12), chars=[WY(-0.55, "worried", "down", face="L")], part=(0, 0.6), pop=[[0.45, "THE TIDE", 1.3]],
  sfx=[[0.1, "wind", 0.4], [0.4, "riser", 0.35]], music="tension")
S("L07", set="study", cam=push(ST_WY, 0.1), chars=[WYS("happy", "present")], part=(0.6, 1), pop=[[0.1, "WOULD YOU?", 1.2]], sfx=[[0.05, "hmm", 0.4]])

finish(EP, "What Happens If You Step Into Quicksand?")
