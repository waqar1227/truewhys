"""Voice: Kokoro TTS per script line + word timings (faster-whisper alignment).
Usage: python lib/voice.py episodes/<ep>  -> audio/lines/*.wav, audio/voice.wav, timing.json
"""
import sys, json, re, difflib, os
from pathlib import Path
import numpy as np, soundfile as sf

SR = 24000
VOICE = os.environ.get("TW_VOICE", "am_michael")
SPEED = float(os.environ.get("TW_SPEED", "1.0"))

def parse_lines(path):
    out = []
    for raw in Path(path).read_text().splitlines():
        if not raw.strip() or raw.startswith("#"):
            continue
        main, _, say = raw.partition("||")
        lid, ch, text = main.split("|", 2)
        out.append(dict(id=lid.strip(), chapter=int(ch), text=text.strip(), say=(say or text).strip()))
    return out

def norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())

def align(text, wwords, dur):
    """Map caption words to whisper word times; interpolate the unmatched ones."""
    cap = text.split()
    cn = [norm(w) for w in cap]
    wn = [norm(w["w"]) for w in wwords]
    times = [None] * len(cap)
    sm = difflib.SequenceMatcher(a=cn, b=wn, autojunk=False)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            times[a + k] = (wwords[b + k]["s"], wwords[b + k]["e"])
    # fill gaps proportional to word length
    s0 = wwords[0]["s"] if wwords else 0.05
    e_last = wwords[-1]["e"] if wwords else dur - 0.05
    i = 0
    while i < len(cap):
        if times[i] is not None:
            i += 1; continue
        j = i
        while j < len(cap) and times[j] is None:
            j += 1
        t0 = times[i - 1][1] if i > 0 else s0
        t1 = times[j][0] if j < len(cap) else e_last
        if t1 <= t0: t1 = t0 + 0.12 * (j - i)
        L = [max(1, len(cn[k])) for k in range(i, j)]
        tot = sum(L); acc = t0
        for k, l in zip(range(i, j), L):
            d = (t1 - t0) * l / tot
            times[k] = (acc, acc + d); acc += d
        i = j
    return [dict(w=w, s=round(t[0], 3), e=round(t[1], 3)) for w, t in zip(cap, times)]

def main(ep):
    ep = Path(ep)
    lines = parse_lines(ep / "lines.txt")
    (ep / "audio/lines").mkdir(parents=True, exist_ok=True)
    from kokoro_onnx import Kokoro
    tts = Kokoro("/opt/kokoro/kokoro-v1.0.onnx", "/opt/kokoro/voices-v1.0.bin")
    from faster_whisper import WhisperModel
    wm = WhisperModel("small.en", device="cpu", compute_type="int8")
    only = set(sys.argv[2:])
    timing_path = ep / "timing.json"
    old = {t["id"]: t for t in json.loads(timing_path.read_text())} if timing_path.exists() else {}
    res = []
    for ln in lines:
        wav = ep / f"audio/lines/{ln['id']}.wav"
        if ln["id"] in old and wav.exists() and (not only or ln["id"] not in only) and old[ln["id"]]["text"] == ln["text"]:
            res.append(old[ln["id"]]); continue
        audio, sr = tts.create(ln["say"], voice=VOICE, speed=SPEED, lang="en-us")
        audio = np.asarray(audio, dtype=np.float32)
        # trim silence, keep 60 ms pads
        idx = np.where(np.abs(audio) > 0.01)[0]
        if len(idx):
            a = max(0, idx[0] - int(0.06 * sr)); b = min(len(audio), idx[-1] + int(0.12 * sr))
            audio = audio[a:b]
        sf.write(wav, audio, sr)
        segs, _ = wm.transcribe(str(wav), word_timestamps=True, language="en", initial_prompt=ln["text"])
        ww = [dict(w=w.word.strip(), s=w.start, e=w.end) for s in segs for w in (s.words or [])]
        heard = " ".join(w["w"] for w in ww)
        dur = len(audio) / sr
        res.append(dict(id=ln["id"], chapter=ln["chapter"], text=ln["text"], dur=round(dur, 3),
                        words=align(ln["text"], ww, dur), heard=heard))
        print(ln["id"], round(dur, 2), "|", heard, flush=True)
    timing_path.write_text(json.dumps(res, indent=1))
    print("total speech s:", round(sum(r["dur"] for r in res), 1))

if __name__ == "__main__":
    main(sys.argv[1])
