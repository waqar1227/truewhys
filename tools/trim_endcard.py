"""Owner D2 (15 Nov 2026): remove the full-screen end card from a composed Short, keep the story to the last frame,
and show a small Wy check badge in the top-right corner during the final 0.7 s.
python tools/trim_endcard.py <short_dir>   (reads shots.json + final.mp4, writes final_d2.mp4)"""
import sys, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
d = Path(sys.argv[1])
sh = json.loads((d / "shots.json").read_text()); sh = sh["shots"] if isinstance(sh, dict) else sh
end = [x for x in sh if x["kind"] == "end"]
cut = end[0]["start"] if end else None
if cut is None:
    sys.exit("no end card in " + str(d))
# badge: yellow disc, ink outline, check mark (brand colours)
S = 150; im = Image.new("RGBA", (S, S)); g = ImageDraw.Draw(im)
g.ellipse((8, 8, S - 8, S - 8), fill="#FFC93C", outline="#22181B", width=10)
g.line([(42, 78), (66, 102), (110, 52)], fill="#22181B", width=14, joint="curve")
badge = d / "_badge.png"; im.save(badge)
t0 = max(0, cut - 0.7)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(d / "final.mp4"), "-i", str(badge), "-t", f"{cut:.3f}",
                "-filter_complex", f"[0:v][1:v]overlay=W-w-48:150:enable='gte(t,{t0:.3f})'[v];[0:a]afade=t=out:st={cut-0.3:.3f}:d=0.3[a]",
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", str(d / "final_d2.mp4")], check=True)
badge.unlink()
print(d.name, "cut at", round(cut, 2), "s")
