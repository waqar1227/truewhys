"""A-016 "Why Onions Make You Cry" — standalone Short, Style R (close-to-human 3D, audit §6.2), owner A/B test B1.
python episodes/A-016-onion-tears/make.py plan            -> shots.json (timing for the Blender scenes)
python episodes/A-016-onion-tears/make.py sheet|anim|render|qa [renders_dir]
3D frames: scene.py (Blender) renders renders/<shot>/f_0000.png ... (animatic here at low res; finals on Kaggle GPU).
This file lays the frames under captions, title (frame 1), overlays, corner badge, voice, music and SFX via lib/flat2d.Video.
"""
import sys, json, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *

RDIR = Path(sys.argv[2]) if len(sys.argv) > 2 else EP / "renders"
import srplate
plate = lambda name: srplate.plate(RDIR, name)


def card_2002(name):
    base = plate(name)
    def fn(g, c):
        base(g, c)
        g.c.save(); g.c.identity_matrix()
        k = pop(c.t, c.w("2002") if True else 0.2, 0.35)
        if k > 0:
            g.rc(W / 2, 520, 520 * k, 210 * k, "#FFF1DC", INK, lw=10, r=30)
            g.text("2002", W / 2, 540, 150 * k, "#FF6B5B", sw=12)
        k2 = pop(c.t, c.w("Japan"), 0.3)
        if k2 > 0:
            g.rc(W / 2, 700, 330 * k2, 90 * k2, "#14213D", INK, lw=8, r=22)
            g.text("JAPAN", W / 2, 712, 64 * k2, "#FFC93C", sw=8)
        g.c.restore()
    return fn


V = Video(EP, title=("WHY ONIONS", "MAKE YOU CRY"), cap_y=0.74,
          keys={"onion", "fighting", "cells", "chemical", "enzyme", "mix", "gas", "eyes", "nerves", "alarm", "tear", "flood", "2002", "japan",
                "ig", "nobel", "sadness", "defence", "cry"}, music="curious")

SH = []  # (line, part, name, sfx, cap_y)
def S(line, part, name, sfx=(), cap_y=None, fn=None, music=None, tr="punch"):
    SH.append(name)
    V.shot(line, fn or plate(name), part, sfx=list(sfx), cap_y=cap_y, name=name, music=music, tr=tr)

S("H1", (0, "And"), "hook_cut", [(0.05, "chop", 0.55), (0.75, "chop", 0.45)], tr="cut")
S("H1", ("And", 1), "fight_back", [(0.1, "hiss", 0.25)])
S("L01", (0, 1), "slice_macro", [(0.15, "chop", 0.5), (0.4, "pop", 0.25)])
S("L02", (0, "Now"), "cells_apart", [(0.1, "bloop", 0.3)], cap_y=0.80)
S("L02", ("Now", 1), "cells_mix", [(0.05, "pop", 0.35), (0.3, "melt", 0.3)], cap_y=0.80)
S("L03", (0, "drifts"), "gas_rise", [(0.1, "hiss", 0.35)])
S("L03", ("drifts", 1), "gas_to_eyes", [(0.0, "whoosh_soft", 0.3), ("straight", "sting", 0.3)])
S("L04", (0, "nerves"), "eye_hit", [(0.05, "whoosh_soft", 0.25)], cap_y=0.84)
S("L04", ("nerves", 1), "eye_alarm", [("alarm", "alarm", 0.45), (0.05, "zap", 0.25)], cap_y=0.84)
S("L05", (0, 1), "tears", [("flood", "bloop", 0.35), (0.6, "splash", 0.12)], cap_y=0.84)
S("L06", (0, "found"), "lab_2002", [("2002", "pop", 0.4), ("Japan", "ding", 0.3)], fn=card_2002("lab_2002"), music="playful")
S("L06", ("found", 1), "lab_flask", [(0.1, "shimmer", 0.2)])
S("L07", (0, 1), "prize", [("Ig", "shimmer", 0.4), ("Prize", "crowd_cheer", 0.12)])
S("L08", (0, "It's"), "wipe", [(0.2, "hmm", 0.25)])
S("L08", ("It's", 1), "defence", [(0.0, "swell", 0.3)])
S("L09", (0, 1), "loop_q", [(0.1, "whoosh_soft", 0.25)])
V.build()


def write_plan():
    out = []
    for sh in V.shots:
        L = V.T[sh["line"]]
        words = {}
        for i, w in enumerate(L["words"]):
            k = norm_w = "".join(ch for ch in w["w"].lower() if ch.isalnum())
            n = sum(1 for ww in L["words"][:i] if "".join(ch for ch in ww["w"].lower() if ch.isalnum()) == k)
            words[f"{k}#{n}" if n else k] = round(V.voice0[sh["line"]] + w["s"] - sh["start"], 3)
        out.append(dict(id=sh["id"], name=sh["name"], line=sh["line"], start=sh["start"], dur=sh["dur"], frames=int(round(sh["dur"] * FPS)), words=words))
    (EP / "shots.json").write_text(json.dumps(dict(fps=FPS, w=W, h=H, duration=V.duration, shots=out), indent=1))
    print(f"{len(out)} shots, {V.duration:.2f} s, {sum(s['frames'] for s in out)} frames")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "plan"
    if cmd == "plan":
        write_plan()
    elif cmd == "sheet":
        V.sheet(str(EP / "animatic/sheet.jpg"), per_shot=1, cols=7, scale=0.18)
    elif cmd == "qa":
        V.qa_numbers()
    elif cmd == "anim":
        V.load_env(); V.mix()
        V.render(str(EP / "animatic/animatic.mp4"), crf=26, preset="veryfast")
    elif cmd == "render":
        V.load_env(); V.mix()
        (EP / "final").mkdir(exist_ok=True)
        V.render(str(EP / "final/A-016.mp4"))
