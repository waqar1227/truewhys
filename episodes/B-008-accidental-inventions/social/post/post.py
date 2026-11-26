"""Teaser Community post image (1080x1080) for L8. python episodes/B-008-accidental-inventions/social/post/post.py
Curiosity gap: 7 covered museum exhibits, one lit up with a melting candy bar; no answers shown."""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1080x1080"
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "lib"))
import cairocffi as cairo
from flat2d import *
from flat_invent import *
from cast2_flat import char2
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); g = G(surf)
g.fill_all(g.rgrad(W * 0.5, H * 0.45, W * 0.8, "#7A3050", "#4A1A2E", "#14050C"))
for i in range(16):
    a0 = i * TAU / 16
    g.poly([(W * 0.5, H * 0.45), (W * 0.5 + 2000 * math.cos(a0), H * 0.45 + 2000 * math.sin(a0)),
            (W * 0.5 + 2000 * math.cos(a0 + 0.12), H * 0.45 + 2000 * math.sin(a0 + 0.12))], "#FFFFFF", None, a=0.05)
g.rect(-20, 860, W + 40, 260, "#5A2E18", INK, lw=8)
for i in range(7):                                    # 7 covered exhibits, #2 uncovered
    x = 90 + i * 150
    g.rc(x, 820, 120, 90, "#6B3A22", INK, lw=6, r=8)
    g.text(f"#{7 - i}", x, 822, 40, "#FFC93C", sw=5)
    if 7 - i == 2:
        continue
    g.path(f"M{x - 60} 775 Q{x - 66} 640 {x} 630 Q{x + 66} 640 {x + 60} 775 Z", "#B03A4A", INK, lw=6)
    g.text("?", x, 715, 60, PAL["cream"], sw=6)
x2 = 90 + 5 * 150
g.glow(x2, 560, 240, "#FFE29A", 0.55)
candy_bar(g, x2, 470, 0.75, 0.6, 0.7, rot=0.06)
char2(g, "wy", 170, 1075, 470, "smile", "down", "point", t=None, view="3q", blink=False)
g.text("7 ACCIDENTS", W / 2, 120, 118, PAL["yellow"], sw=24, depth=10, rot=-0.04)
g.text("YOU USE EVERY DAY", W / 2, 250, 66, PAL["cream"], sw=12, rot=-0.04)
from PIL import Image
Image.frombuffer("RGBA", (W, H), bytes(surf.get_data()), "raw", "BGRA", 0, 1).convert("RGB").save(HERE / "post.jpg", quality=92)
print("ok")
