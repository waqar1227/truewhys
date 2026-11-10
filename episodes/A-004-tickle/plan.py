"""A-004 "Why You Can't Tickle Yourself" (standalone Short, Style T, 9:16).
Sets: lab (robot arm with a feather on the bench, brain screen on the back wall, brain model under glass) and study (Wy at his desk).
New for this Short: Wy arms "tickle" (self-tickling wiggle), "laugh" flag (lib/compose.py), robot feather stroke (anim, lib/sets3.anim_lab).
python episodes/A-004-tickle/plan.py -> shots.json
"""
import sys
from pathlib import Path
EP = Path(__file__).parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from ashort import M, push, pull, pan, crane, shake, A, S, finish

HOOK = M([2.35, -0.95, 1.75], [2.65, 1.3, 1.62], 30)        # Wy on the stool tickling himself, the robot's feather right beside him
ROBOT = M([2.5, -1.55, 1.7], [2.6, 1.3, 1.58], 30)        # Wy on the stool, hand under the robot's feather (faces below the captions)
SCREEN = M([-0.3, 2.6, 2.2], [-0.4, 5.4, 2.72], 30)       # close on the brain screen, cerebellum glowing (brain below the captions)
POINT = M([1.3, -2.2, 1.2], [-0.2, 5.4, 1.75], 30)        # Wy in the foreground pointing at the screen
BRAIN = M([-0.55, -0.15, 1.45], [-0.9, 1.8, 1.3], 32)    # brain model under glass
WIDE = M([0.4, -1.6, 1.65], [1.4, 1.6, 1.45], 26)        # the robot test rig: robot + Wy on the stool (pans right)
ST_WY = M([0.6, -2.4, 1.0], [0.6, 0.55, 0.78], 30)       # study: Wy at his desk (as A-001)

STROKE = {"robot": "stroke", "amp": 14, "hz": 2.4}


def WYR(expr="neutral", arms="point_l", **kw):            # Wy standing on the yellow stool by the robot, hand reaching under the feather
    return A("wy", [3.0, 0.95, 0.77], 1.25, "L", expr, arms, **kw)


WYL = lambda expr="neutral", arms="down", **kw: WYR(expr, arms, **kw)


WYS = lambda expr="happy", arms="down", **kw: A("wy", [0.6, 0.55, 0], 1.25, "R", expr, arms, talk=True, **kw)

# hook: one person + one strange object from frame 1 (Wy tickling himself, deadpan, the tickle robot right beside him)
S("H1", set="lab", cam=push(HOOK, 0.16), chars=[WYL(expr="tired", arms="tickle")], part=(0, 0.52),
  pop=[[0.02, "WHY NOT?!", 1.45]], sfx=[[0, "whoosh_soft", 0.5], [0.15, "tick", 0.35]], music="playful")
S("H1", set="lab", cam=push(HOOK, 0.12, lens_mult=1.25), chars=[WYL(expr="worried", arms="shrug")], part=(0.52, 1),
  pop=[[0.05, "NOTHING.", 1.1]], sfx=[[0.1, "hmm", 0.4]])
S("L01", set="lab", cam=shake(ROBOT, 0.1, 0.02), chars=[WYR("surprised", "point_l", laugh=0.6)], anim=dict(STROKE, t0=0.25),
  pop=[[0.55, "SURPRISE!", 1.25]], sfx=[[0.2, "whoosh_soft", 0.35], [0.6, "boing", 0.4]])
S("L02", set="lab", cam=push(POINT, 0.12), chars=[A("wy", [0.9, 0.6, 0], 1.25, "L", "neutral", "point_l", talk=True)], part=(0, 0.45),
  tag="YOUR BRAIN", sfx=[[0.1, "pop", 0.35]], music="curious")
S("L02", set="lab", cam=push(SCREEN, 0.18), chars=[], part=(0.45, 1),
  pop=[[0.2, "CEREBELLUM", 1.15]], sfx=[[0.15, "ding", 0.35]])
S("L03", set="lab", cam=push(BRAIN, 0.15), chars=[], part=(0, 0.5), pop=[[0.2, "FEELING: TURNED DOWN", 1.0]], sfx=[[0.1, "tick", 0.35]])
S("L03", set="lab", cam=pull(HOOK, 0.1), chars=[WYL(expr="tired", arms="tickle")], part=(0.5, 1), tag="NO SURPRISE")
S("L04", set="lab", cam=pan(WIDE, 0.9, 0.0), chars=[WYR("happy", "down")], part=(0, 0.4), pop=[[0.15, "THE ROBOT TEST", 1.1]],
  sfx=[[0.05, "whoosh_soft", 0.4], [0.3, "riser", 0.25]])
S("L04", set="lab", cam=push(ROBOT, 0.12), chars=[WYR("neutral", "point_l")], part=(0.4, 1), anim=dict(STROKE, t0=1.2),
  tag="YOU MOVE, IT COPIES", sfx=[[1.2, "whoosh_soft", 0.25]])
S("L05", set="lab", cam=push(ROBOT, 0.1, lens_mult=1.2), chars=[WYR("tired", "point_l")], part=(0, 0.42), anim=STROKE,
  pop=[[0.05, "NO DELAY: MEH", 1.05]], sfx=[[0.1, "tick", 0.3]])
S("L05", set="lab", cam=push(ROBOT, 0.22, lens_mult=1.45), chars=[WYR("surprised", "point_l")], part=(0.42, 1),
  pop=[[0.35, "0.2 s DELAY", 1.3]], sfx=[[0.2, "riser", 0.4]], music="tension")
S("L06", set="lab", cam=shake(ROBOT, 0.14, 0.03), chars=[WYR("happy", "both_up", laugh=True)], part=(0, 0.5), anim=dict(STROKE, amp=18, hz=2.8),
  pop=[[0.05, "IT TICKLES!", 1.25]], sfx=[[0.0, "boing", 0.45], [0.3, "pop", 0.3]], music="playful")
S("L06", set="lab", cam=pull(SCREEN, 0.12), chars=[], part=(0.5, 1), pop=[[0.15, "GUESS: WRONG", 1.15]], sfx=[[0.1, "ding", 0.3]])
S("L07", set="study", cam=push(ST_WY, 0.12), chars=[WYS("happy", "present")], part=(0, 0.68), tag="IT MUTES WHAT IT EXPECTS",
  sfx=[[0.05, "whoosh_soft", 0.3]], music="warm")
S("L07", set="study", cam=push(ST_WY, 0.1, lens_mult=1.25), chars=[WYS("smug", "point_r")], part=(0.68, 1), pop=[[0.1, "ARE YOU?", 1.25]],
  sfx=[[0.05, "hmm", 0.4]])

finish(EP, "Why You Can't Tickle Yourself")
