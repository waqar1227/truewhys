"""A-021 "Why Can't You Play GTA 6 on PC Yet?" — standalone Short, Style R (close-to-human 3D), owner request 21 Nov 2026 (2nd GTA 6 Short).
python episodes/A-021-gta6-pc/make.py plan            -> shots.json (timing for the Blender scenes in scene.py)
python episodes/A-021-gta6-pc/make.py sheet|anim|render|qa [renders_dir]
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


V = Video(EP, title=("WHY CAN'T YOU PLAY", "GTA 6 ON PC YET?"), cap_y=0.74,
          keys={"pc", "gta", "nothing", "2013", "2015", "2018", "console", "later", "first", "2027", "official", "pattern", "waiting"}, music="curious")

SH = []
def Z(line, part, name, sfx=(), focus=(540, 900), fn=None):
    V.shot(line, fn or zplate(name, focus=focus), part, sfx=list(sfx), name=name + "#z", tr="cut")


def S(line, part, name, sfx=(), cap_y=None, fn=None, music=None, tr="punch"):
    SH.append(name)
    V.shot(line, fn or plate(name), part, sfx=list(sfx), cap_y=cap_y, name=name, music=music, tr=tr)

S("H1", (0, 1), "hook_pc", [(0.05, "click", 0.3)], tr="cut")
CW = [("november", "NOV 19, 2026", W / 2, 470, 96, PAL["yellow"]), ("playstation", "PS5 + XBOX", W / 2, 590, 80, PAL["cream"])]
S("L01", (0, "GTA"), "console_win", [(0.2, "swell", 0.35)], fn=tag("console_win", CW))
Z("L01", ("GTA", "PC"), "console_win", focus=(560, 1000), fn=tag("console_win", CW, base=zplate("console_win", focus=(560, 1000))))
S("L01", ("PC", 1), "pc_nothing", [("nothing", "drum_hit", 0.4)], fn=tag("pc_nothing", [("nothing", "PC: NOTHING", W / 2, 470, 104, "#FF6B5B")]))
S("L02", (0, "GTA"), "shrug_pc", [(0.1, "hmm", 0.3)])
PA = [("2013", "CONSOLE 2013", 300, 560, 70, PAL["cream"]), ("2015", "PC 2015", 790, 560, 70, PAL["yellow"])]
S("L02", ("GTA", "PC"), "pedestals_a", [("2013", "pop", 0.4)], fn=tag("pedestals_a", PA))
Z("L02", ("PC", 1), "pedestals_a", [("2015", "pop", 0.4)], focus=(760, 1000), fn=tag("pedestals_a", PA, base=zplate("pedestals_a", focus=(760, 1000))))
S("L03", (0, 1), "pedestals_b", [("2018", "pop", 0.4), ("later", "pop", 0.4)],
  fn=tag("pedestals_b", [("2018", "CONSOLE 2018", 300, 560, 70, PAL["cream"]), ("later", "PC 2019", 790, 560, 70, PAL["yellow"])]))
BS = [("console", "CONSOLE FIRST", W / 2, 470, 96, PAL["yellow"])]
S("L04", (0, "to"), "boss", [(0.1, "whoosh_soft", 0.3)], fn=tag("boss", BS))
Z("L04", ("to", 1), "boss", focus=(540, 820), fn=tag("boss", BS, base=zplate("boss", focus=(540, 820))))
RP = [("2027", "PC: EARLY 2027?", W / 2, 470, 90, PAL["cream"]), ("official", "NOT OFFICIAL", W / 2, 600, 90, "#FF6B5B")]
S("L05", (0, "But"), "report_2027", [("2027", "ding", 0.4)], fn=tag("report_2027", RP))
Z("L05", ("But", 1), "report_2027", [("official", "hmm", 0.3)], focus=(540, 950), fn=tag("report_2027", RP, base=zplate("report_2027", focus=(540, 950))))
S("L06", (0, "It's"), "loop_q", [(0.1, "whoosh_soft", 0.25)])
Z("L06", ("It's", 1), "loop_q", focus=(500, 900))
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
        V.render(str(EP / "final/A-021.mp4"))
