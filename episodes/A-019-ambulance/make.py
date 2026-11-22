"""A-019 "Why Is AMBULANCE Written Backwards?" — standalone Short, Style R (close-to-human 3D), 22 Nov 2026.
python episodes/A-019-ambulance/make.py plan            -> shots.json (timing for the Blender scenes in scene.py)
python episodes/A-019-ambulance/make.py sheet|anim|render|qa [renders_dir]
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


def start_of(name):
    return lambda c: min(sh["start"] for sh in c.V.shots if sh["name"] == name)


def zplate(name, z=(1.16, 1.22), focus=(540, 900)):
    """Second camera cut inside one rendered shot: punch-in on the same frames, clock continues from the rendered shot."""
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


V = Video(EP, title=("WHY IS IT", "BACKWARDS?"), keys=set(), music="curious")

SH = []
def Z(line, part, name, sfx=(), focus=(540, 900), fn=None, z=(1.16, 1.22)):
    V.shot(line, fn or zplate(name, z=z, focus=focus), part, sfx=list(sfx), name=name + "#z", tr="cut")


def S(line, part, name, sfx=(), cap_y=None, fn=None, music=None, tr="punch"):
    SH.append(name)
    V.shot(line, fn or plate(name), part, sfx=list(sfx), cap_y=cap_y, name=name, music=music, tr=tr)


S("H1", (0, 1), "hook_front", [(0.0, "siren_yelp", 0.55), (0.6, "siren", 0.35)], tr="cut")
Z("L01", (0, "It's#1"), "hook_front", [(0.1, "drum_hit", 0.3)], focus=(330, 1000), z=(1.3, 1.38),
  fn=tag("hook_front", [("mistake", "NOT A MISTAKE", W / 2, 430, 96, PAL["yellow"])], base=zplate("hook_front", z=(1.3, 1.38), focus=(330, 1000))))
S("L01", ("It's#1", "the"), "behind_car", [(0.05, "whoosh_soft", 0.3)], fn=tag("behind_car", [("one", "1 PERSON", W / 2, 470, 104, PAL["yellow"])]))
S("L01", ("the", 1), "driver_car", [(0.1, "siren", 0.25)])
Z("L02", (0, "You#2"), "driver_car", [("screams", "siren_yelp", 0.45)], focus=(540, 860), z=(1.18, 1.26))
S("L02", ("You#2", 1), "glance_mirror", [("mirror", "ding", 0.3)])
S("L03", (0, "A#1"), "mirror_demo", [("flips", "whoosh_soft", 0.35)],
  fn=tag("mirror_demo", [("left", "LEFT \u2194 RIGHT", W / 2, 430, 96, PAL["yellow"])]))
Z("L03", ("A#1", 1), "mirror_demo", [("backwards", "pop", 0.35)], focus=(628, 940), z=(1.45, 1.55))
S("L04", (0, "The#1"), "print_flip", [("flipped", "whoosh_soft", 0.4)])
S("L04", ("The#1", 1), "spec", [("requires", "ding", 0.35)],
  fn=tag("spec", [("official", "US AMBULANCE SPEC", W / 2, 430, 84, PAL["cream"]), ("requires", "\"MIRROR IMAGED\"", W / 2, 560, 92, PAL["yellow"])]))
S("L05", (0, "but"), "back_van", [(0.05, "whoosh_soft", 0.3)])
S("L05", ("but", "Did"), "reveal_mirror", [("reads", "shimmer", 0.4)])
S("L05", ("Did", 1), "loop_q", [(0.0, "siren", 0.2)])
V.build()


def write_plan():
    """One Blender shot per rendered name; zoom cuts (name '<shot>#z') extend the duration of the shot they belong to."""
    out = []
    for sh in V.shots:
        if "#" in sh["name"]:
            prev = out[-1]; prev["dur"] = round(sh["start"] + sh["dur"] - prev["start"], 4); prev["frames"] = int(round(prev["dur"] * FPS))
            L = V.T[sh["line"]]
            for i, w in enumerate(L["words"]):
                k = "".join(ch for ch in w["w"].lower() if ch.isalnum())
                n = sum(1 for ww in L["words"][:i] if "".join(ch for ch in ww["w"].lower() if ch.isalnum()) == k)
                prev["words"].setdefault(f"{k}#{n}" if n else k, round(V.voice0[sh["line"]] + w["s"] - prev["start"], 3))
            continue
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
        V.render(str(EP / "final/A-019.mp4"))
