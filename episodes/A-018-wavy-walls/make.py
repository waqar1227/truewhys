"""A-018 "Why Is This English Wall So Wiggly?" — standalone Short, Style R (close-to-human 3D, audit §6.2), owner request 20 Nov 2026.
python episodes/A-018-wavy-walls/make.py plan            -> shots.json (timing for the Blender scenes in scene.py)
python episodes/A-018-wavy-walls/make.py sheet|anim|render|qa [renders_dir]
3D frames come from scene.py (animatic here at low res; finals on Kaggle GPU). This file adds captions, title (frame 1), 2D labels,
corner badge, voice, music and SFX via lib/flat2d.Video.
"""
import sys, json, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *

RDIR = Path(sys.argv[2]) if len(sys.argv) > 2 else EP / "renders"
import srplate
plate = lambda name: srplate.plate(RDIR, name)


def tag(name, items):
    """Plate + popping labels: items = [(word, text, x, y, size, colour)]."""
    base = plate(name)
    def fn(g, c):
        base(g, c)
        with g.screen():
            for wd, txt, x, y, size, col in items:
                try:
                    t0 = c.w(wd) - 0.1
                except KeyError:
                    t0 = 0.15
                k = pop(c.t, t0, 0.32)
                if k > 0:
                    g.text(txt, x, y, size, col, sw=size * 0.2, depth=size * 0.08, sc=k, rot=-0.03)
    return fn


V = Video(EP, title=("WHY IS THIS ENGLISH WALL", "SO WIGGLY?"), cap_y=0.74,
          keys={"wiggly", "one", "brick", "thick", "fall", "blow", "two", "pillars", "curve", "braces", "paper", "sun", "fruit", "fewer", "bricks", "agree"},
          music="curious")

SH = []
def S(line, part, name, sfx=(), cap_y=None, fn=None, music=None, tr="punch"):
    SH.append(name)
    V.shot(line, fn or plate(name), part, sfx=list(sfx), cap_y=cap_y, name=name, music=music, tr=tr)

S("H1", (0, 1), "hook_wall", [(0.05, "thud", 0.25)], tr="cut")
S("L01", (0, "But"), "aerial_snake", [(0.1, "whoosh_soft", 0.3)])
S("L01", ("But", 1), "push_test", [("fall", "thud", 0.3)], fn=tag("push_test", [("one", "1 BRICK THICK", W / 2, 470, 96, PAL["yellow"])]))
S("L02", (0, "It"), "thin_topple", [(0.35, "rush", 0.3), ("over", "thud", 0.5)])
S("L02", ("It", 1), "thick_pillars", [("two", "pop", 0.35), ("pillars", "pop", 0.35)],
  fn=tag("thick_pillars", [("two", "2 BRICKS", 300, 520, 90, PAL["cream"]), ("pillars", "+ PILLARS", 780, 620, 90, PAL["yellow"])]))
S("L03", (0, "like"), "brace_top", [("braces", "ding", 0.35)], cap_y=0.80)
S("L03", ("like", 1), "paper_demo", [("paper", "page_turn", 0.35)])
S("L04", (0, 1), "sun_pockets", [(0.1, "shimmer", 0.3), ("fruit", "pop", 0.3)], music="playful")
S("L05", (0, "Wiggly#1"), "brick_count", [("fewer", "ding", 0.45)],
  fn=tag("brick_count", [("stands", "STANDS ALONE", W / 2, 470, 90, PAL["cream"]), ("fewer", "FEWER BRICKS", W / 2, 600, 104, PAL["yellow"])]))
S("L05", ("Wiggly#1", 1), "loop_q", [(0.1, "whoosh_soft", 0.25)])
V.build()


def write_plan():
    out = []
    for sh in V.shots:
        L = V.T[sh["line"]]
        words = {}
        for i, w in enumerate(L["words"]):
            k = "".join(ch for ch in w["w"].lower() if ch.isalnum())
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
        V.sheet(str(EP / "animatic/sheet.jpg"), per_shot=1, cols=6, scale=0.16)
    elif cmd == "qa":
        V.qa_numbers()
    elif cmd == "anim":
        V.load_env(); V.mix()
        V.render(str(EP / "animatic/animatic.mp4"), crf=26, preset="veryfast")
    elif cmd == "render":
        V.load_env(); V.mix()
        (EP / "final").mkdir(exist_ok=True)
        V.render(str(EP / "final/A-018.mp4"))
