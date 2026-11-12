"""Check split narration lines: python tools/voice_check.py episodes/<ep>
Transcribes every audio/lines/<id>.wav WITHOUT hints and prints lines whose words differ from lines.txt, plus zero-length words in timing.json
(a zero-length first word usually means the splitter cut it off: re-cut from audio/chapters/ch0.wav)."""
import sys, json, difflib, re
from pathlib import Path
from faster_whisper import WhisperModel
ep = Path(sys.argv[1])
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())
wm = WhisperModel("small.en", device="cpu", compute_type="int8")
bad = 0
for t in json.loads((ep / "timing.json").read_text()):
    f = ep / f"audio/lines/{t['id']}.wav"
    if not f.exists(): continue
    segs, _ = wm.transcribe(str(f), language="en")
    heard = " ".join(s.text.strip() for s in segs)
    r = difflib.SequenceMatcher(a=[norm(x) for x in t["text"].split()], b=[norm(x) for x in heard.split()]).ratio()
    zero = [w["w"] for w, n in zip(t["words"], t["words"][1:]) if n["s"] - w["s"] < 0.03]
    if r < 0.93 or zero:
        bad += 1
        print(f"CHECK {t['id']} match {r:.2f} zero-length {zero}\n   text : {t['text']}\n   heard: {heard}")
print("lines to check:", bad)
