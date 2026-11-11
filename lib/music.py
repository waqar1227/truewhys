"""Original procedural music for TrueWhys (medieval-flavoured, no samples, fully ours).
python lib/music.py <out_dir> [seconds]  -> <mood>.wav for each mood (stereo 44.1 kHz)
Instruments are synthesised: Karplus-Strong lute/harp, breathy recorder, warm pad, frame drum,
shaker, low bell. Modes + chord loops per mood; melodies are seeded random walks with motif repeats.
"""
import sys, math
import numpy as np
from scipy.signal import fftconvolve, butter, lfilter
import soundfile as sf

SR = 44100
RNG = np.random.default_rng(11)


def midi_hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def adsr(n, a=0.01, d=0.1, s=0.7, r=0.2):
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    e = np.ones(n) * s
    e[:a] = np.linspace(0, 1, max(a, 1))[:min(a, n)] if a else 1
    if a + d < n:
        e[a:a + d] = np.linspace(1, s, d)
    if r < n:
        e[-r:] *= np.linspace(1, 0, r)
    return e


def pluck(freq, dur, bright=0.5, decay=0.996):
    """Karplus-Strong string."""
    n = int(dur * SR)
    p = max(2, int(SR / freq))
    buf = RNG.uniform(-1, 1, p)
    # soften attack for lute-like tone
    b, a = butter(1, min(0.99, 0.15 + bright * 0.7))
    buf = lfilter(b, a, buf)
    out = np.zeros(n)
    idx = 0
    for i in range(n):
        v = buf[idx]
        nxt = buf[(idx + 1) % p]
        buf[idx] = decay * 0.5 * (v + nxt)
        out[i] = v
        idx = (idx + 1) % p
    return out * np.linspace(1, 0.0, n) ** 0.3


def pluck_fast(freq, dur, bright=0.5, decay=0.996):
    """Vectorised approximation of K-S (block processing) for speed."""
    n = int(dur * SR)
    p = max(2, int(round(SR / freq)))
    reps = n // p + 2
    buf = RNG.uniform(-1, 1, p)
    b, a = butter(1, min(0.99, 0.15 + bright * 0.7))
    buf = lfilter(b, a, buf)
    rows = [buf]
    for _ in range(reps - 1):
        buf = decay * 0.5 * (buf + np.roll(buf, -1))
        rows.append(buf)
    out = np.concatenate(rows)[:n]
    return out * np.linspace(1, 0, n) ** 0.4


def recorder(freq, dur, vib=5.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    v = 1 + 0.006 * np.sin(2 * np.pi * vib * t) * np.clip(t / 0.25, 0, 1)
    ph = 2 * np.pi * freq * np.cumsum(v) / SR
    tone = np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    breath = lfilter(*butter(2, [min(0.98, freq * 1.5 / (SR / 2)), min(0.99, freq * 4 / (SR / 2))], "band"), RNG.normal(0, 1, n)) * 0.08
    return (tone + breath) * adsr(n, 0.06, 0.1, 0.8, 0.12)


def pad(freqs, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for f in freqs:
        for det in (-0.25, 0.0, 0.3):
            ph = 2 * np.pi * f * (1 + det / 100) * t
            out += (2 * (ph / (2 * np.pi) % 1) - 1) * 0.3  # saw
    b, a = butter(2, 900 / (SR / 2))
    out = lfilter(b, a, out)
    return out * adsr(n, dur * 0.3, 0.2, 0.9, dur * 0.3) / max(1, len(freqs))


def drum(dur=0.5, pitch=90):
    n = int(dur * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * pitch * t * (1 + 0.6 * np.exp(-t * 30))) * np.exp(-t * 9)
    skin = lfilter(*butter(2, [300 / (SR / 2), 2500 / (SR / 2)], "band"), RNG.normal(0, 1, n)) * np.exp(-t * 35) * 0.4
    return body + skin


def shaker(dur=0.12):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return lfilter(*butter(2, 5000 / (SR / 2), "high"), RNG.normal(0, 1, n)) * np.exp(-t * 40) * 0.25


def bell(freq, dur=3.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = sum(a * np.sin(2 * np.pi * freq * r * t) * np.exp(-t * d) for r, a, d in [(1, 1, 1.2), (2.76, 0.5, 2), (5.4, 0.25, 3.5), (0.5, 0.4, 0.8)])
    return out * 0.5


def reverb(x, sec=2.2, wet=0.25):
    n = int(sec * SR)
    t = np.arange(n) / SR
    ir = RNG.normal(0, 1, n) * np.exp(-t * 6.5 / sec)
    ir = lfilter(*butter(1, 5000 / (SR / 2)), ir)
    ir /= np.sqrt((ir ** 2).sum())
    y = fftconvolve(x, ir)[:len(x)]
    return x * (1 - wet) + y * wet * 1.3


MODES = {"aeolian": [0, 2, 3, 5, 7, 8, 10], "dorian": [0, 2, 3, 5, 7, 9, 10], "mixolydian": [0, 2, 4, 5, 7, 9, 10],
         "ionian": [0, 2, 4, 5, 7, 9, 11], "lydian": [0, 2, 4, 6, 7, 9, 11]}

MOODS = {
    #           root  mode         bpm  chords (scale degrees)      melody  drums  pad  lute pattern
    "mystery": (50, "aeolian", 72, [0, 5, 3, 4], 0.35, 0, 1, "arp_slow"),
    "curious": (55, "mixolydian", 96, [0, 6, 3, 0], 0.7, 1, 0, "bounce"),
    "story":   (50, "dorian", 92, [0, 6, 2, 3], 0.8, 1, 1, "lute68"),
    "playful": (53, "ionian", 112, [0, 3, 4, 0], 0.9, 2, 0, "staccato"),
    "tension": (57, "aeolian", 84, [0, 0, 5, 4], 0.25, 3, 1, "ostinato"),
    "dark":    (48, "aeolian", 64, [0, 5, 0, 4], 0.2, 0, 1, "toll"),
    "warm":    (50, "ionian", 88, [0, 4, 5, 3], 0.8, 1, 1, "lute68"),
    "adventure": (52, "dorian", 126, [0, 6, 3, 4], 0.95, 2, 1, "lute68"),   # jaunty sea-shanty feel (B-003)
}


def chord(root, mode, deg):
    sc = MODES[mode]
    return [root + sc[(deg + k) % 7] + 12 * ((deg + k) // 7) for k in (0, 2, 4)]


def compose(mood, seconds=90):
    root, mode, bpm, prog, mel_amt, drums, use_pad, pat = MOODS[mood]
    beat = 60 / bpm
    bar = beat * (3 if pat == "lute68" else 4)
    nbars = int(seconds / bar) + 1
    L = int(nbars * bar * SR) + SR * 3
    mixL, mixR = np.zeros(L), np.zeros(L)

    def add(sig, t, gain=1.0, pan=0.0):
        i = int(t * SR)
        j = min(L, i + len(sig))
        if i >= L:
            return
        s = sig[:j - i] * gain
        mixL[i:j] += s * math.cos((pan + 1) * math.pi / 4)
        mixR[i:j] += s * math.sin((pan + 1) * math.pi / 4)

    sc = MODES[mode]
    scale_notes = [root + 12 + sc[k % 7] + 12 * (k // 7) for k in range(14)]
    motif = None
    for b in range(nbars):
        t0 = b * bar
        deg = prog[b % len(prog)]
        ch = chord(root, mode, deg)
        # bass
        add(pluck_fast(midi_hz(ch[0] - 12), bar * 0.95, 0.3, 0.998), t0, 0.55, -0.1)
        if use_pad:
            add(pad([midi_hz(n) for n in ch], bar * 1.05), t0, 0.22, 0.0)
        # lute / harp pattern
        if pat == "lute68":
            steps = [(0, ch[0]), (1, ch[1] + 12), (2, ch[2]), (3, ch[1] + 12), (4, ch[2] + 12), (5, ch[1] + 12)]
            for k, n in steps:
                add(pluck_fast(midi_hz(n), beat * 0.9, 0.55), t0 + k * beat / 2, 0.30, 0.3)
        elif pat == "arp_slow":
            for k, n in enumerate([ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 24]):
                add(pluck_fast(midi_hz(n), beat * 2, 0.7, 0.999), t0 + k * beat, 0.25, 0.35)
        elif pat == "bounce":
            for k in range(8):
                n = ch[k % 3] + (12 if k % 2 else 0)
                add(pluck_fast(midi_hz(n), beat * 0.5, 0.6, 0.99), t0 + k * beat / 2, 0.25 if k % 2 else 0.32, 0.25)
        elif pat == "staccato":
            for k in range(8):
                if k in (1, 5):
                    continue
                n = ch[(k * 2) % 3] + 12
                add(pluck_fast(midi_hz(n), beat * 0.3, 0.75, 0.985), t0 + k * beat / 2, 0.3, 0.3 if k % 2 else -0.3)
        elif pat == "ostinato":
            for k in range(8):
                n = ch[0] + (0 if k % 4 else 12) + (3 if k == 6 else 0)
                add(pluck_fast(midi_hz(n), beat * 0.45, 0.4, 0.993), t0 + k * beat / 2, 0.32, -0.2)
        elif pat == "toll":
            if b % 2 == 0:
                add(bell(midi_hz(ch[0])), t0, 0.25, -0.2)
            add(pluck_fast(midi_hz(ch[2] + 12), beat * 3, 0.5, 0.999), t0 + 2 * beat, 0.18, 0.3)
        # drums
        if drums == 1:
            for k in range(int(bar / beat)):
                add(drum(0.5, 85 if k == 0 else 110), t0 + k * beat, 0.32 if k == 0 else 0.16, 0)
                add(shaker(), t0 + k * beat + beat / 2, 0.5, 0.4)
        elif drums == 2:
            for k in range(8):
                add(shaker(0.06), t0 + k * beat / 2, 0.6, -0.3 if k % 2 else 0.3)
            add(drum(0.4, 120), t0, 0.25); add(drum(0.4, 150), t0 + 2 * beat, 0.18)
        elif drums == 3:  # heartbeat
            for k in (0, 2):
                add(drum(0.5, 60), t0 + k * beat, 0.4); add(drum(0.5, 55), t0 + k * beat + 0.22, 0.28)
        # melody on recorder: phrases of 4 bars, motif repeats (A A' B A)
        if mel_amt > 0 and (b % 8) >= (0 if mood in ("story", "warm", "playful", "curious") else 4):
            phrase = (b // 4) % 4
            if motif is None or (b % 4 == 0 and phrase == 2):
                cur = 4 + scale_notes.index(min(scale_notes, key=lambda x: abs(x - (ch[0] + 24)))) % 7
                mot = []
                for k in range(int(bar / beat) * 2):
                    if RNG.random() < mel_amt * 0.55:
                        cur = int(np.clip(cur + RNG.choice([-2, -1, -1, 1, 1, 2, 0]), 0, 13))
                        mot.append((k, cur, RNG.choice([1, 1, 2, 2, 3])))
                motif = mot if phrase != 2 else motif
                bmot = mot
            use = bmot if phrase == 2 else motif
            for k, deg_i, ln in use:
                n = scale_notes[deg_i]
                # pull strong beats to chord tones
                if k % 4 == 0:
                    n = min(ch, key=lambda c: abs((c + 24) - n)) + 24
                add(recorder(midi_hz(n), beat / 2 * ln * 0.95), t0 + k * beat / 2, 0.16, 0.1)
    mix = np.stack([mixL, mixR], 1)
    mix = np.stack([reverb(mix[:, 0], 2.4, 0.3), reverb(mix[:, 1], 2.5, 0.3)], 1)
    mix = mix[:int(seconds * SR)]
    fade = int(1.5 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    mix /= np.abs(mix).max() + 1e-9
    return (mix * 0.89).astype(np.float32)


if __name__ == "__main__":
    out = sys.argv[1]
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 90
    import os
    os.makedirs(out, exist_ok=True)
    for m in (sys.argv[3].split(",") if len(sys.argv) > 3 else MOODS):
        sf.write(f"{out}/{m}.wav", compose(m, secs), SR)
        print("ok", m, flush=True)
