"""Teaser Community post image (1080x1080) for L6. python episodes/B-006-brain-glitches/social/post/post.py"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1080x1080"
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "lib"))
import cairocffi as cairo
from flat2d import *
from cast2_flat import char2
from flat_fx import qmark
from flat_brain import *
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); g = G(surf)
g.fill_all(g.rgrad(W * 0.6, H * 0.45, W * 0.8, "#B8732E", "#5A3416", "#0E0703"))
for i in range(16):
    a0 = i * TAU / 16
    g.poly([(W * 0.6, H * 0.45), (W * 0.6 + 2000 * math.cos(a0), H * 0.45 + 2000 * math.sin(a0)),
            (W * 0.6 + 2000 * math.cos(a0 + 0.12), H * 0.45 + 2000 * math.sin(a0 + 0.12))], "#FFFFFF", None, a=0.06)
doorway(g, 700, 930, 1.45, 0.9, wall="#3A2A1E", inside="#FFE7B0", light=1.0)
char2(g, "student", 700, 960, 720, "shocked", "down", "think", t=None, breathe=False, blink=False, view="front")
thought(g, 330, 330, 330, 220, 1.0, tail=(1, 1))
qmark(g, 330, 330, 170, "#FF6B5B", 0.08, 1.0)
g.text("WHY AM I HERE?", W / 2, 110, 110, PAL["yellow"], sw=24, depth=10, rot=-0.04)
g.text("BLAME THE DOOR?", W / 2, 1010, 90, "#FFFFFF", sw=20, depth=8, rot=-0.03)
from PIL import Image
Image.frombuffer("RGBA", (W, H), bytes(surf.get_data()), "raw", "BGRA", 0, 1).convert("RGB").save(HERE / "post.jpg", quality=92)
print("ok")
