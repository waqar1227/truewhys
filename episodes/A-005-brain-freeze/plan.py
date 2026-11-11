"""A-005 "What Brain Freeze Does Inside Your Head" (standalone Short, Style T, 9:16).
Sets: study (Wy at his desk, as A-001/A-004) and lab (brain screen + brain model under glass, marks from A-004).
New for this Short: magnifier scenes headx_cold / headx_vessel / headx_nerve (lib/gfx.LENS_SCENES), puppet posed=True on the hook.
Growth review 11 Nov: payoff image (Wy mid brain-freeze with the ice cream) from frame 1; 25-40 s.
python episodes/A-005-brain-freeze/plan.py -> shots.json
"""
import sys
from pathlib import Path
EP = Path(__file__).parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from ashort import M, push, pull, pan, crane, shake, A, S, finish

ST_WY = M([0.6, -2.4, 1.0], [0.6, 0.55, 0.78], 30)       # study: Wy at his desk (A-001/A-004 mark)
SCREEN = M([-0.3, 2.6, 2.2], [-0.4, 5.4, 2.72], 30)       # lab: close on the brain screen
POINT = M([1.3, -2.2, 1.2], [-0.2, 5.4, 1.75], 30)        # lab: Wy in the foreground pointing at the screen
STC = M([0.62, -0.95, 1.0], [0.6, 0.55, 0.95], 30)        # study: Wy close, face at ~0.44 of the frame
BRAIN = M([-0.55, -0.15, 1.45], [-0.9, 1.8, 1.3], 32)    # lab: brain model under glass

WYS = lambda expr="happy", arms="down", **kw: A("wy", [0.6, 0.55, 0], 1.25, "R", expr, arms, talk=True, **kw)
WYP = lambda expr="neutral", arms="point_l", **kw: A("wy", [0.9, 0.6, 0], 1.25, "L", expr, arms, talk=True, **kw)
CONE = dict(hold="icecream")

# hook: payoff image from frame 1: Wy mid brain-freeze, ice cream at his mouth
S("H1", set="study", cam=push(STC, 0.12), chars=[WYS("pain", "point_r", posed=True, blink_fast=True, **CONE)], part=(0, 0.5),
  pop=[[0.02, "BRAIN FREEZE!", 1.4]], sfx=[[0, "whoosh_soft", 0.5], [0.05, "boing", 0.35]], music="playful")
S("H1", set="lab", cam=push(SCREEN, 0.15), chars=[], part=(0.5, 1), pop=[[0.05, "INSIDE YOUR HEAD", 1.05]], sfx=[[0.05, "ding", 0.35]])
S("L01", set="study", cam=push(ST_WY, 0.1), chars=[WYS("surprised", "raise", **CONE)], lens=dict(name="headx_cold", at=[0.5, 0.42], rad=0.34),
  pop=[[0.1, "ICE COLD!", 1.15]], sfx=[[0.1, "pop", 0.35]], music="curious")
S("L02", set="lab", cam=push(BRAIN, 0.15), chars=[], part=(0, 0.35), tag="SCIENTISTS FOUND", sfx=[[0.05, "tick", 0.35]])
S("L02", set="study", cam=push(ST_WY, 0.08), chars=[WYS("worried", "down")], part=(0.35, 1), lens=dict(name="headx_vessel", at=[0.5, 0.42], rad=0.34),
  pop=[[0.4, "BLOOD RUSHES IN", 1.0]], sfx=[[0.3, "riser", 0.35]], music="tension")
S("L03", set="lab", cam=pull(BRAIN, 0.12), chars=[], part=(0, 0.55), pop=[[0.25, "CLOSED BOX", 1.15]], sfx=[[0.1, "thud", 0.4]])
S("L03", set="study", cam=shake(STC, 0.1, 0.03), chars=[WYS("angry", "chin", blink_fast=True)], part=(0.55, 1), pop=[[0.05, "OUCH!", 1.4]],
  sfx=[[0.0, "boing", 0.4]])
S("L04", set="study", cam=push(ST_WY, 0.1, lens_mult=1.15), chars=[WYS("neutral", "down")], lens=dict(name="headx_nerve", at=[0.5, 0.42], rad=0.34),
  tag="SAME NERVE", sfx=[[0.2, "whoosh_soft", 0.3], [1.6, "ding", 0.35]], music="curious")
S("L05", set="study", cam=push(STC, 0.12), chars=[WYS("surprised", "chin")], pop=[[0.1, "WRONG PLACE!", 1.15]], sfx=[[0.05, "boing", 0.4]])
S("L06", set="study", cam=push(STC, 0.1), chars=[WYS("happy", "present")], part=(0, 0.5), pop=[[0.1, "TONGUE UP", 1.2]], sfx=[[0.05, "pop", 0.35]],
  music="playful")
S("L06", set="study", cam=pull(STC, 0.1), chars=[WYS("happy", "hold", hold="bowl")], part=(0.5, 1), pop=[[0.05, "SIP SOMETHING WARM", 0.95]],
  sfx=[[0.1, "drink", 0.4]])
S("L07", set="lab", cam=pull(SCREEN, 0.12), chars=[], part=(0, 0.5), pop=[[0.1, "NOT FROZEN", 1.15]], sfx=[[0.05, "tick", 0.35]], music="warm")
S("L07", set="study", cam=push(STC, 0.12), chars=[WYS("smug", "point_r")], part=(0.5, 1), pop=[[0.1, "YOU TOO?", 1.3]],
  sfx=[[0.05, "hmm", 0.4]])

finish(EP, "What Brain Freeze Does Inside Your Head")
