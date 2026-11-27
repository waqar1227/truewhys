"""Narration voice samples for the owner (REAL SOUND RULE, 27 Nov 2026): the SAME ~20 s text read by 3 Gemini voices + Kokoro.
/opt/c3d/bin/python tools/voice_samples.py takes   -> docs/voice_samples/takes/<voice>.flac (1 Gemini request per voice; kept, never re-spent)
/opt/c3d/bin/python tools/voice_samples.py mix     -> docs/voice_samples/<n>_<voice>.mp3 (voice + real music + real SFX + room ambience)
Prebuilt Gemini voices only; never imitate a real person."""
import sys, os, subprocess
from pathlib import Path
import numpy as np, soundfile as sf
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "lib"))
OUT = ROOT / "docs/voice_samples"
TAKES = OUT / "takes"
TEXT = ("How did a failed wallpaper become bubble wrap? Nobody wanted it on their walls... and it almost ended up in the trash. "
        "In 1957, two engineers sealed two shower curtains together, trapping rows of air bubbles inside, and sold it as fancy, "
        "textured wallpaper. So they tried it as greenhouse insulation. That flopped too.")
GEMINI = ["Charon", "Puck", "Achird"]      # informative / upbeat / friendly (Gemini prebuilt voices)
KOKORO = "am_michael"


def takes():
    import voice_gemini as vg
    TAKES.mkdir(parents=True, exist_ok=True)
    for v in GEMINI:
        out = TAKES / f"gemini_{v.lower()}.flac"
        if out.exists():
            continue
        vg.VOICE = v
        wav = TAKES / f"gemini_{v.lower()}.wav"
        try:
            vg.tts(vg.NATURAL.format(note="") + TEXT, wav)
        except Exception as e:
            print("FAIL", v, type(e).__name__, getattr(e, "code", ""), flush=True); continue
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-compression_level", "8", str(out)], check=True); wav.unlink()
        print("ok", v, flush=True)
    out = TAKES / f"kokoro_{KOKORO}.flac"
    if not out.exists():
        from kokoro_onnx import Kokoro
        k = Kokoro("/opt/kokoro/kokoro-v1.0.onnx", "/opt/kokoro/voices-v1.0.bin")
        a, sr = k.create(TEXT, voice=KOKORO, speed=1.0, lang="en-us")
        sf.write(out, a, sr); print("ok kokoro", flush=True)


def mix():
    import audio
    files = sorted(TAKES.glob("gemini_*.flac")) + sorted(TAKES.glob("kokoro_*.flac"))
    for n, f in enumerate(files, 1):
        v, sr = sf.read(f, dtype="float32")
        if v.ndim > 1: v = v.mean(1)
        dur = len(v) / sr
        cues = [(0.05, "bubble_wrap", 0.5), (dur * 0.30, "paper_crumple", 0.35), (dur * 0.42, "metal_small", 0.4),
                (dur * 0.60, "plastic_crinkle", 0.35)]
        wav = OUT / f"_{f.stem}.wav"
        audio.mix_voice_file(f, wav, mood="light", amb="amb_living_room", cues=cues, pad=1.5, seed=n)
        name = OUT / f"{n}_{f.stem}.mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-c:a", "libmp3lame", "-b:a", "160k", str(name)], check=True)
        wav.unlink(); print("ok", name.name, round(dur, 1), "s", flush=True)


if __name__ == "__main__":
    {"takes": takes, "mix": mix}[sys.argv[1]]()
