"""A-017 "Why Ice Cubes Are Cloudy" — standalone Short, Style R (close-to-human 3D, audit §6.2), owner A/B test B2.
python episodes/A-017-cloudy-ice/make.py plan | sheet | anim | render | qa  [renders_dir]
3D frames: scene.py (Blender) -> renders/<shot>/f_####.png (animatic here; finals on Kaggle GPU). Captions, title, badge, sound: lib/flat2d.Video.
"""
import sys, json
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
import srplate

RDIR = Path(sys.argv[2]) if len(sys.argv) > 2 else EP / "renders"
plate = lambda name: srplate.plate(RDIR, name)

V = Video(EP, title=("WHY ICE CUBES", "ARE CLOUDY"), cap_y=0.74,
          keys={"clear", "cloudy", "air", "dissolved", "ice", "room", "outside", "in", "layer", "middle", "nowhere", "bubbles", "light", "cloud",
                "lake", "top", "escapes", "one", "side", "drink"}, music="curious")


def S(line, part, name, sfx=(), cap_y=None, music=None, tr="punch"):
    V.shot(line, plate(name), part, sfx=list(sfx), cap_y=cap_y, name=name, music=music, tr=tr)

S("H1", (0, "So"), "hook_cube", [(0.05, "click", 0.3)], tr="cut")
S("H1", ("So", 1), "cube_macro", [(0.1, "freeze", 0.3)])
S("L01", (0, 1), "water_air", [(0.2, "bloop", 0.25), ("dissolved", "shimmer", 0.2)])
S("L02", (0, 1), "no_room", [("no", "boing", 0.25)], cap_y=0.82)
S("L03", (0, "freezes"), "freezer", [(0.05, "door", 0.3), (0.4, "freeze", 0.25)])
S("L03", ("freezes", 1), "xsec_start", [(0.1, "freeze", 0.25)], cap_y=0.82)
S("L04", (0, 1), "xsec_layers", [(0.1, "freeze", 0.2), ("middle", "pop", 0.2)], cap_y=0.82)
S("L05", (0, 1), "xsec_trapped", [("nowhere", "sting", 0.3)], cap_y=0.82)
S("L06", (0, "they"), "bubbles_macro", [(0.1, "bloop", 0.25)])
S("L06", ("they", 1), "scatter", [("scatter", "shimmer", 0.35), ("cloud", "ding", 0.3)])
S("L07", (0, "The#1"), "lake_down", [(0.1, "wind", 0.15)], music="warm")
S("L07", ("The#1", 1), "lake_clear", [("escapes", "bloop", 0.25)])
S("L08", (0, "freeze"), "one_side", [(0.1, "freeze", 0.25)], cap_y=0.82)
S("L08", ("freeze", 1), "clear_cube", [(0.1, "sparkle", 0.35)])
S("L09", (0, "Did"), "drink_loop", [(0.05, "drink", 0.2)])
S("L09", ("Did", 1), "loop_end", [("know", "pop", 0.25)])
V.build()


def write_plan():
    out = []
    for sh in V.shots:
        L = V.T[sh["line"]]; words = {}
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
        V.sheet(str(EP / "animatic/sheet.jpg"), per_shot=1, cols=8, scale=0.18)
    elif cmd == "qa":
        V.qa_numbers()
    elif cmd == "anim":
        V.load_env(); V.mix(); V.render(str(EP / "animatic/animatic.mp4"), crf=26, preset="veryfast")
    elif cmd == "render":
        V.load_env(); V.mix(); (EP / "final").mkdir(exist_ok=True); V.render(str(EP / "final/A-017.mp4"))
