"""Speed up (or slow down) a Short's narration lines without re-spending TTS quota (A-031, 25 Nov 2026).
python tools/tempo_lines.py episodes/<ep> 1.05
Re-cuts audio/lines/*.wav from the chapter take (python lib/voice_gemini.py <ep> 0 first if audio/ is missing), applies ffmpeg atempo
(pitch kept) and scales timing.json (dur + word times). Writes "tempo" into timing.json so it is never applied twice."""
import sys, json, subprocess
from pathlib import Path
ep, f = Path(sys.argv[1]), float(sys.argv[2])
tp = ep / "timing.json"
T = json.loads(tp.read_text())
if any(t.get("tempo") for t in T):
    sys.exit("tempo already applied: re-run lib/voice_gemini.py <ep> 0 first to start from the original take")
for t in T:
    w = ep / f"audio/lines/{t['id']}.wav"
    tmp = w.with_suffix(".tmp.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(w), "-af", f"atempo={f}", str(tmp)], check=True)
    tmp.replace(w)
    t["dur"] = round(t["dur"] / f, 3)
    for x in t["words"]:
        x["s"], x["e"] = round(x["s"] / f, 3), round(x["e"] / f, 3)
    t["tempo"] = f
tp.write_text(json.dumps(T, indent=1))
print("ok", sum(t["dur"] for t in T))
