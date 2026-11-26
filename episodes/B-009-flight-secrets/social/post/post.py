"""Teaser Community post image (1080x1080) for L9: the dark cabin, a passenger looking up as the lights go off. python episodes/B-009-flight-secrets/social/post/post.py"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1080x1080"
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "lib"))
import cairocffi as cairo
from flat2d import *
from cast2_flat import char2
from flat_flight import *
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); g = G(surf)
g.fill_all(g.lgrad(0, 0, 0, H, "#1E2C4A", "#0A1226"))
g.poly([(-50, -40), (1130, -40), (1130, 130), (-50, 170)], "#2A3A5C", INK, lw=7)
for x in (200, 540, 880):
    g.glow(x, 160, 70, "#FFE29A", 0.25); g.circle(x, 160, 14, "#5A5040", INK, lw=4)
oval_window(g, 150, 470, 150, 220, 0.0, night=True)
seat_front(g, 560, 330, 1000, 380, SEAT_D)
char2(g, "kai", 560, 1180, 900, "shocked", "down", "hold", t=None, view="3q", breathe=False, blink=False)
seat_back_view(g, 560, 860, 420, tray=0.0, card=True)
for i in range(6):
    g.glow(60 + i * 200, 1060, 50, "#FFB347", 0.6)
g.rc(930, 260, 170, 64, "#1B3A2A", INK, lw=6, r=10); g.glow(930, 260, 140, "#7DFF9A", 0.4)
g.text("EXIT", 930, 264, 44, "#7DFF9A", stroke=None)
g.text("LIGHTS OFF?", W / 2 + 120, 120, 104, PAL["yellow"], sw=22, depth=9, rot=-0.04)
from PIL import Image
Image.frombuffer("RGBA", (W, H), bytes(surf.get_data()), "raw", "BGRA", 0, 1).convert("RGB").save(HERE / "post.jpg", quality=92)
print("ok")
