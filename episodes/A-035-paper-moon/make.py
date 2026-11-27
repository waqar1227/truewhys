"""A-035 "Fold Paper 42 Times and It Would Reach the Moon" — standalone Short, Style R, 27 Nov 2026. Slot Fri 8 Jan 2027 18:00 UTC.
python episodes/A-035-paper-moon/make.py plan            -> shots.json (timing for the Blender scenes in scene.py)
python episodes/A-035-paper-moon/make.py sheet|anim|render|qa [renders_dir]
3D frames come from scene.py (animatic here at low res; finals on Kaggle GPU). This file adds the title (frame 1), a few 2D labels,
corner badge, voice, music and SFX via lib/flat2d.Video. No captions (owner 22 Nov).
"""
import sys, json, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *

RDIR = Path(sys.argv[2]) if len(sys.argv) > 2 else EP / "renders"
import srplate
plate = lambda name: srplate.plate(RDIR, name)


def start_of(name):
    return lambda c: min(sh["start"] for sh in c.V.shots if sh["name"] == name)


def zplate(name, z=(1.16, 1.22), focus=(540, 900)):
    return srplate.plate(RDIR, name, zoom=(z[0], z[1], focus), t0=start_of(name))


def tag(name, items, base=None):
    """Plate + popping labels: items = [(word, text, x, y, size, colour)]."""
    base = base or plate(name)
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


CREAM, TANG, LIME = "#EFE6D2", "#F08A24", "#B5D33D"
V = Video(EP, title=("ONE MORE", "FOLD?"), keys=set(), music="curious/mischief_maker", amb="amb_room_quiet", title_out=2.4)
V.title_y = 0.60          # over his sweater: face above, block below stay clear


def count(name, word, n, rest, y=1480):
    """Fold counter label (look.md): lime number + cream text, slides up from below. Short labels only (no captions)."""
    return tag(name, [(word, n, W / 2, y, 150, LIME), (word, rest, W / 2, y + 150, 92, CREAM)])


def S(line, part, name, sfx=(), fn=None, music=None, tr="punch", amb=None):
    V.shot(line, fn or plate(name), part, sfx=list(sfx), name=name, music=music, tr=tr, amb=amb)


S("H1", (0, 1), "hook_press", [(0.0, "paper_crumple", 0.55), (0.05, "slap_table", 0.35), ("Moon", "paper_rustle", 0.3)], tr="cut")
S("L01", (0, 1), "stuck_macro", [("stuck", "paper_crumple", 0.4)], fn=tag("stuck_macro", [("seven", "7 FOLDS", W / 2, 1520, 140, LIME)]))
S("L02", (0, 1), "stack_desk", [("doubles", "page_flip", 0.4), ("centimetres", "book_close", 0.3)],
  fn=count("stack_desk", "Ten", "10 FOLDS", "= 10 cm"))
S("L03", (0, 1), "stack_city", [(0.0, "whoosh_paper", 0.35)], amb="amb_city", tr="cut",
  fn=count("stack_city", "folds", "23 FOLDS", "= 839 m", y=1500))
S("L04", (0, 1), "stack_moon", [(0.0, "whoosh_paper", 0.3)], amb="amb_night", tr="cut",
  fn=count("stack_moon", "Moon", "42 FOLDS", "= 440,000 km", y=1500))
S("L05", (0, "Each"), "desk_ask", [(0.1, "chair_creak", 0.3)])
S("L05", ("Each", 1), "fold_curve", [("halves", "paper_rustle", 0.4), ("bend", "paper_crumple", 0.3)],
  fn=tag("fold_curve", [("swallows", "x4 PAPER", W / 2, 1520, 140, LIME)]))
S("L06", (0, 1), "long_strip", [(0.1, "paper_rustle", 0.35)], amb="amb_school",
  fn=tag("long_strip", [("2002", "2002", W / 2, 360, 120, CREAM), ("twelve", "12 FOLDS", W / 2, 1480, 140, LIME), ("kilometre", "1.2 km", W / 2, 1630, 110, CREAM)]))
S("L07", (0, 1), "loop_press", [("paper", "paper_crumple", 0.5)], tr="cut")
V.build()


def write_plan():
    """One Blender shot per rendered name; zoom cuts (name '<shot>#z') extend the duration of the shot they belong to."""
    def wkeys(L, base, out_d):
        for i, w in enumerate(L["words"]):
            k = "".join(ch for ch in w["w"].lower() if ch.isalnum())
            n = sum(1 for ww in L["words"][:i] if "".join(ch for ch in ww["w"].lower() if ch.isalnum()) == k)
            out_d.setdefault(f"{k}#{n}" if n else k, round(V.voice0[L["id"]] + w["s"] - base, 3))
    out = []
    for sh in V.shots:
        L = V.T[sh["line"]]
        if "#" in sh["name"]:
            prev = out[-1]; prev["dur"] = round(sh["start"] + sh["dur"] - prev["start"], 4); prev["frames"] = int(round(prev["dur"] * FPS))
            wkeys(L, prev["start"], prev["words"]); continue
        words = {}; wkeys(L, sh["start"], words)
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
        V.render(str(EP / "final/A-035.mp4"))
