"""Audio for TrueWhys episodes: voice placement, music with ducking, SFX, loudness -14 LUFS."""
import json, functools, subprocess, math
from pathlib import Path
import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
SR = 44100
SFX_DIR = ROOT / "library/sfx"
SFX = {  # name -> file (CC0: Kenney/OpenGameArt packs, BigSoundBank by Joseph Sardin)
    "shovel": "bsb/trim_shovel.wav", "frog": "bsb/trim_frog.wav", "gulp": "bsb/trim_gulp.wav", "drink": "bsb/trim_drink.wav",
    "splash": "bsb/trim_splash.wav",  # trimmed from the BigSoundBank files listed in bsb/credits.json
    "gavel": "bsb/gavel__gavel-1-blow_1588.mp3", "crowd_murmur": "bsb/crowd__crowd-of-50-60-people-1_3515.mp3",
    "crowd_gasp": "bsb/crowd__outside-talks-2_2969.mp3", "crowd_laugh": "bsb/applause__shouts-and-applauses-of-teens-2_0237.mp3",
    "pig_oink": "bsb/pig__grumpy-pig-2_1659.mp3", "pig_squeal": "bsb/pig__grumpy-pig-1_1658.mp3",
    "rat_squeak": "bsb/mouse__mouse-screams_0459.mp3", "cat_hiss": "bsb/cat__two-cats-fighting_0817.mp3",
    "cat_meow": "bsb/cat__meow-cat-2_1890.mp3", "rooster": "bsb/rooster__song-of-rooster_0283.mp3",
    "church_bell": "bsb/church_bell__church-bell_0135.mp3", "whoosh": "bsb/whoosh__whoosh-4_1796.mp3",
    "whoosh_soft": "bsb/whoosh__whoosh-3_1795.mp3", "coins": "bsb/coins__coins-2_0194.mp3",
    "coin_single": "bsb/coins__coin-in-cup-1_0339.mp3", "paper": "bsb/scroll__road-map-4_2799.mp3",
    "insects": "bsb/fly__bumblebee-1_1000.mp3", "fire": "bsb/fire__big-branching-fire-1_0987.mp3",
    "wind": "bsb/wind__wind_0595.mp3", "birds": "bsb/birds__wake-birds-3_0999.mp3", "owl": "bsb/owl__tawny-owl-2_1764.mp3",
    "drum_hit": "bsb/drum__bass-tom-1_2338.mp3", "chewing": "bsb/rat__rat-nibbling_0185.mp3", "dog": "bsb/dog__barking-dog-2_2954.mp3",
    # B-003 (sea): BigSoundBank CC0
    "waves": "bsb/birds__sea-waves-and-seagulls_0267.mp3", "gulls": "bsb/birds__sea-waves-and-seagulls_0267.mp3",
    "bell": "bsb/bell__small-bell-1_0292.mp3", "crowd_cheer": "bsb/applause__applause-1_2363.mp3",
}
PACK_GLOBS = {"page_turn": "**/bookFlip1.ogg", "quill": "**/scratch_001.ogg", "footsteps": "**/footstep0*.ogg", "door": "**/doorOpen_1.ogg",
              "pop": "**/drop_002.ogg", "ding": "**/confirmation_001.ogg", "sparkle": "**/glass_001.ogg", "boing": "**/spring_01.ogg",
              "thud": "**/wooden_01.ogg", "tick": "**/tick_001.ogg", "hmm": "**/question_001.ogg",
              "creak": "**/creak2.ogg", "flag_flap": "**/cloth3.ogg", "cannon": "**/explosion.ogg"}
AMBIENT = {"crowd_murmur", "wind", "birds", "fire", "insects", "room_tone", "footsteps", "chewing", "waves", "gulls"}


@functools.lru_cache(maxsize=128)
def load(path):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    a = np.frombuffer(out, np.float32).reshape(-1, 2).copy()
    return a


def sfx(name):
    if name == "riser":
        n = int(2.0 * SR); t = np.arange(n) / SR
        x = np.random.default_rng(1).normal(0, 1, n) * (t / 2.0) ** 2
        from scipy.signal import butter, lfilter
        y = np.zeros(n)
        for k in range(0, n, 2048):  # sweeping band
            f = 300 + 4000 * (k / n) ** 2
            b, a = butter(2, [f / (SR / 2), min(0.99, f * 1.6 / (SR / 2))], "band")
            y[k:k + 2048] = lfilter(b, a, x[k:k + 2048])
        y /= np.abs(y).max() + 1e-9
        return np.stack([y, y], 1).astype(np.float32) * 0.7
    if name == "room_tone":
        n = int(8 * SR)
        b = np.cumsum(np.random.default_rng(2).normal(0, 1, n)); b -= np.convolve(b, np.ones(4000) / 4000, "same")
        b /= np.abs(b).max() + 1e-9
        return np.stack([b, b], 1).astype(np.float32) * 0.15
    if name in SFX:
        return load(SFX_DIR / SFX[name])
    if name in PACK_GLOBS:
        fs = sorted((SFX_DIR / "packs").glob(PACK_GLOBS[name]))
        if fs:
            if name == "footsteps":
                seq = []
                for k in range(10):
                    a = load(fs[k % len(fs)]); seq.append(a); seq.append(np.zeros((int(0.38 * SR) - min(len(a), int(0.38 * SR)), 2), np.float32))
                return np.concatenate(seq)
            return load(fs[0])
    return None


def norm_peak(a, peak=0.9):
    m = np.abs(a).max()
    return a * (peak / m) if m > 0 else a


def line_starts(plan):
    st = {}
    for sh in plan["shots"]:
        if sh.get("line") and sh["line"] not in st:
            st[sh["line"]] = sh["line_start"] + 0.05
    return st


@functools.lru_cache(maxsize=4)
def _voice_track(ep_s, plan_s):
    ep = Path(ep_s); plan = json.loads(plan_s)
    total = int((plan["duration"] + 1) * SR)
    v = np.zeros(total, np.float32)
    for lid, t0 in line_starts(plan).items():
        p = ep / f"audio/lines/{lid}.wav"
        if not p.exists():
            continue
        a, sr = sf.read(p, dtype="float32")
        if a.ndim > 1:
            a = a.mean(1)
        if sr != SR:
            idx = np.arange(0, len(a), sr / SR)
            a = np.interp(idx, np.arange(len(a)), a).astype(np.float32)
        i = int(t0 * SR)
        j = min(total, i + len(a))
        v[i:j] += a[:j - i]
    return v


def voice_env(ep, plan):
    v = _voice_track(str(ep), json.dumps(plan))
    hop = SR // 100
    n = len(v) // hop
    rms = np.sqrt((v[:n * hop].reshape(n, hop) ** 2).mean(1))
    ref = np.percentile(rms[rms > 1e-4], 95) if (rms > 1e-4).any() else 1
    e = np.clip(rms / ref, 0, 1)
    def f(t):
        i = int(t * 100)
        return float(e[i]) if 0 <= i < n else 0.0
    return f


def build_mix(ep, plan, out_wav):
    ep = Path(ep)
    total = int((plan["duration"] + 0.5) * SR)
    voice = _voice_track(str(ep), json.dumps(plan))[:total]
    voice = np.pad(voice, (0, max(0, total - len(voice))))
    # voice: gentle compression + presence
    from scipy.signal import butter, lfilter
    b, a = butter(1, 80 / (SR / 2), "high"); voice = lfilter(b, a, voice).astype(np.float32)
    env = np.convolve(np.abs(voice), np.ones(441) / 441, "same")
    thr = np.percentile(env[env > 1e-4], 70) if (env > 1e-4).any() else 0.1
    gain = np.where(env > thr, (thr / np.maximum(env, 1e-6)) ** 0.35, 1.0)
    voice = voice * np.convolve(gain, np.ones(882) / 882, "same").astype(np.float32)
    voice = norm_peak(voice, 0.7)
    mix = np.stack([voice, voice], 1)
    # ---- music by mood with crossfades and ducking
    music = np.zeros((total, 2), np.float32)
    segs = []
    mood = "mystery"
    for sh in plan["shots"]:
        if sh.get("music"):
            mood = sh["music"]
        if segs and segs[-1][0] == mood:
            segs[-1][2] = sh["start"] + sh["dur"]
        else:
            segs.append([mood, sh["start"], sh["start"] + sh["dur"]])
    xf = int(1.6 * SR)
    pos = {}
    for m, t0, t1 in segs:
        tr = load(ROOT / f"library/music/procedural/{m}.wav")
        i0, i1 = max(0, int(t0 * SR) - xf // 2), min(total, int(t1 * SR) + xf // 2)
        n = i1 - i0
        off = pos.get(m, 0)
        idx = (np.arange(n) + off) % len(tr)
        seg = tr[idx]
        pos[m] = off + n
        fade = np.ones(n, np.float32)
        k = min(xf, n // 2)
        fade[:k] = np.linspace(0, 1, k); fade[-k:] = np.linspace(1, 0, k)
        music[i0:i1] += seg * fade[:, None]
    venv = np.convolve(np.abs(voice), np.ones(2205) / 2205, "same")
    active = (venv > 0.01).astype(np.float32)
    active = np.convolve(active, np.ones(int(0.4 * SR)) / int(0.4 * SR), "same")
    duck_db = -14 + (-22 + 14) * np.clip(active, 0, 1)
    for sh in plan["shots"]:  # cards and end screen: music forward
        if sh["kind"] in ("card", "end", "title"):
            i0, i1 = int(sh["start"] * SR), min(total, int((sh["start"] + sh["dur"]) * SR))
            duck_db[i0:i1] = np.maximum(duck_db[i0:i1], -9)
    music *= (10 ** (duck_db / 20))[:, None].astype(np.float32)
    mix += music
    # ---- SFX
    for sh in plan["shots"]:
        d = sh["dur"]
        if sh["kind"] == "card":
            for nm, off, g in (("whoosh", 0.0, 0.5), ("drum_hit", 0.25, 0.35)):
                a = sfx(nm)
                if a is not None:
                    i = int((sh["start"] + off) * SR); j = min(total, i + len(a)); mix[i:j] += norm_peak(a[:j - i]) * g * 0.6
        for (off, nm, g) in sh.get("sfx", []):
            a = sfx(nm)
            if a is None:
                continue
            a = norm_peak(a)
            t0 = sh["start"] + (off * d if off <= 1 else off)
            i = int(t0 * SR)
            if nm in AMBIENT:
                n = int((sh["start"] + d - t0) * SR)
                if n <= 0:
                    continue
                reps = int(np.ceil(n / len(a)))
                a = np.tile(a, (reps, 1))[:n]
                fd = min(int(0.3 * SR), n // 2)
                f = np.ones(n, np.float32); f[:fd] = np.linspace(0, 1, fd); f[-fd:] = np.linspace(1, 0, fd)
                a = a * f[:, None]
                g *= 0.35
            else:
                a = a[:int(4 * SR)]
                fd = min(int(0.2 * SR), len(a) // 2)
                a = a.copy(); a[-fd:] *= np.linspace(1, 0, fd)[:, None]
                g *= 0.55
            j = min(total, i + len(a))
            if j > i:
                mix[i:j] += a[:j - i] * g
    # ---- loudness -14 LUFS, soft limit
    import pyloudnorm as pyln
    meter = pyln.Meter(SR)
    lufs = meter.integrated_loudness(mix)
    mix = mix * (10 ** ((-14 - lufs) / 20))
    # look-ahead brickwall limiter to -3 dBFS sample peak (leaves room for AAC overshoot)
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    ceil = 10 ** (-3 / 20)
    peak = np.abs(mix).max(1)
    g = np.minimum(1.0, ceil / np.maximum(peak, 1e-9))
    la = int(0.005 * SR)
    g = minimum_filter1d(g, size=2 * la + 1)
    g = uniform_filter1d(g, size=la)
    g = np.minimum(g, minimum_filter1d(np.minimum(1.0, ceil / np.maximum(peak, 1e-9)), size=3))
    mix = mix * g[:, None]
    sf.write(out_wav, mix.astype(np.float32), SR)
    print("mix LUFS before norm", round(lufs, 1), "-> -14", flush=True)
