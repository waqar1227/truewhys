"""Owner demo (27 Nov 2026): the A-030 string-lights script, old flat read vs the new per-line emotional read, same voice (Charon),
same real music + living-room ambience + real SFX. Uses the saved takes only (no Gemini request):
  old: episodes/A-030-string-lights/voice/ch0.flac      new: docs/voice_samples/emotional_demo/voice/*.flac (3 scene takes)
/opt/c3d/bin/python tools/emotional_demo.py   (run lib/voice_gemini.py docs/voice_samples/emotional_demo 0 first if audio/lines is missing)
-> docs/voice_samples/emotional_demo.mp3 and docs/voice_samples/flat_old_demo.mp3"""
import sys, json, subprocess
from pathlib import Path
import numpy as np, soundfile as sf
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "lib"))
import audio
OUT = ROOT / "docs/voice_samples"
DEMO = OUT / "emotional_demo"


def new_narration(path):
    tm = json.loads((DEMO / "timing.json").read_text())
    parts, t, starts = [], 0.0, {}
    for x in tm:
        a, sr = sf.read(DEMO / f"audio/lines/{x['id']}.wav", dtype="float32")
        starts[x["id"]] = t
        gap = np.zeros(int((0.45 if x["id"] in ("H1", "L03") else 0.3) * sr), np.float32)   # a beat after the hook and the sad drop
        parts += [a, gap]; t += (len(a) + len(gap)) / sr
    sf.write(path, np.concatenate(parts), sr)
    return starts


def mix(voice, out, starts):
    cues = [(starts["L01"] + 1.6, "switch_light", 0.5),     # the string goes dark
            (starts["L03"] + 0.3, "lightbulb_buzz", 0.25),  # the glowing wire
            (starts["L05"] + 3.9, "switch_light", 0.5)]     # push the bulb back in: lights on
    wav = OUT / f"_{out}.wav"
    audio.mix_voice_file(voice, wav, mood="warm", amb="amb_living_room", cues=cues, pad=1.5, seed=3, ep_id="DEMO")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-c:a", "libmp3lame", "-b:a", "160k", str(OUT / f"{out}.mp3")], check=True)
    wav.unlink(); print("ok", out + ".mp3", flush=True)


if __name__ == "__main__":
    nv = DEMO / "audio/narration.wav"
    st = new_narration(nv)
    mix(nv, "emotional_demo", st)
    old = ROOT / "episodes/A-030-string-lights/voice/ch0.flac"
    ot = {t["id"]: 0.0 for t in json.loads((ROOT / "episodes/A-030-string-lights/timing.json").read_text())}
    acc = 0.0
    for t in json.loads((ROOT / "episodes/A-030-string-lights/timing.json").read_text()):
        ot[t["id"]] = acc; acc += t["dur"]
    mix(old, "flat_old_demo", ot)
