"""Teaser Community post image (1080x1080) for L5. python episodes/B-005-annoying-science/social/post/post.py"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1080x1080"
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "lib"))
import cairocffi as cairo
from flat2d import *
from cast2_flat import char2
from flat_annoy import *
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); g = G(surf)
g.fill_all(g.rgrad(W * 0.6, H * 0.45, W * 0.8, "#3E8FB0", "#1E4A60", "#0B1620"))
for i in range(16):
    a0 = i * TAU / 16
    g.poly([(W * 0.6, H * 0.45), (W * 0.6 + 2000 * math.cos(a0), H * 0.45 + 2000 * math.sin(a0)),
            (W * 0.6 + 2000 * math.cos(a0 + 0.12), H * 0.45 + 2000 * math.sin(a0 + 0.12))], "#FFFFFF", None, a=0.06)
table_side(g, 560, 640, 520, "#C97B4A", 300)
plate(g, 560, 634, 260)
for j, (x, y, r) in enumerate(((790, 600, 0.6), (850, 720, 1.6), (900, 860, 3.0))):
    with g.group(0.3 + 0.35 * j):
        toast(g, x, y, 0.9, r)
char2(g, "modern", 250, 1250, 1150, "shocked", "up", "down", t=None, breathe=False, blink=False)
g.text("BAD LUCK?", W / 2 + 120, 130, 130, PAL["yellow"], sw=28, depth=12, rot=-0.05)
g.text("OR PHYSICS?", W / 2 + 140, 1000, 110, "#FFFFFF", sw=24, depth=10, rot=-0.04)
from PIL import Image
Image.frombuffer("RGBA", (W, H), bytes(surf.get_data()), "raw", "BGRA", 0, 1).convert("RGB").save(HERE / "post.jpg", quality=92)
print("ok")
