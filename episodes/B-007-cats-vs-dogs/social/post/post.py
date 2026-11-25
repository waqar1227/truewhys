"""Teaser Community post image (1080x1080) for L7. python episodes/B-007-cats-vs-dogs/social/post/post.py"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1080x1080"
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "lib"))
import cairocffi as cairo
from flat2d import *
from flat_pets import *
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); g = G(surf)
g.fill_all(g.rgrad(W * 0.5, H * 0.5, W * 0.8, "#2F4F6F", "#16233D", "#060B14"))
for i in range(16):
    a0 = i * TAU / 16
    g.poly([(W * 0.5, H * 0.5), (W * 0.5 + 2000 * math.cos(a0), H * 0.5 + 2000 * math.sin(a0)),
            (W * 0.5 + 2000 * math.cos(a0 + 0.12), H * 0.5 + 2000 * math.sin(a0 + 0.12))], "#FFFFFF", None, a=0.05)
for i, col in enumerate(("#FF6B5B", "#FFC93C", "#5ED3B5")):
    g.line([(-20, 690 + i * 60), (W + 20, 690 + i * 60)], col, 14)
dog_sit(g, 270, 1010, 0.82, 0.0, "happy", tongue=0.6, look=(0.8, 0), blink=0.0)
cat_sit(g, 820, 1010, 0.95, 0.0, "smug", look=(-0.8, 0), blink=0.0, breathe=False)
with g.at(W / 2, 300, -0.03):
    g.rc(0, 0, 520, 210, PAL["navy"], INK, lw=12, r=30)
    g.rc(0, 0, 480, 170, "#0B1A2B", None, r=24)
    g.text("? : ?", 0, 12, 140, PAL["yellow"], sw=12)
g.text("WHO WINS?", W / 2, 110, 120, PAL["yellow"], sw=24, depth=10, rot=-0.04)
from PIL import Image
Image.frombuffer("RGBA", (W, H), bytes(surf.get_data()), "raw", "BGRA", 0, 1).convert("RGB").save(HERE / "post.jpg", quality=92)
print("ok")
