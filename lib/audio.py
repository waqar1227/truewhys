"""Audio for TrueWhys episodes: voice placement, music with ducking, SFX, ambience beds, loudness -14 LUFS.

Two sound modes (build_mix):
- "real" (REAL SOUND RULE, owner 27 Nov 2026; default for NEW episodes): real recorded SFX (library/sfx/real, Freesound CC0, then
  BigSoundBank), a real ambience bed under every scene (shot/plan key "amb", sticky like music), real-instrument music by mood
  (library/music/real, Kevin MacLeod CC BY 4.0 -> credit lines written to <ep>/audio/music_credits.txt for the description),
  music ducked ~20 dB under the voice. Synthesised lib/sfxgen.py effects / procedural music only as a fallback, with a WARNING.
- "legacy": the old mix (procedural music + in-house synth effects), so already-posted episodes rebuild exactly as before.
Mode: plan["sound"] > env TW_SOUND > "legacy" if the episode has uploaded.json, else "real"."""
import json, functools, subprocess, math, os
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
    # B-007: short trims of the BigSoundBank CC0 dog bark / cat meow (bsb/credits.json)
    "bark": "bsb/trim_bark.wav", "meow": "bsb/trim_meow.wav",
}
PACK_GLOBS = {"page_turn": "**/bookFlip1.ogg", "quill": "**/scratch_001.ogg", "footsteps": "**/footstep0*.ogg", "door": "**/doorOpen_1.ogg",
              "pop": "**/drop_002.ogg", "ding": "**/confirmation_001.ogg", "sparkle": "**/glass_001.ogg", "boing": "**/spring_01.ogg",
              "thud": "**/wooden_01.ogg", "tick": "**/tick_001.ogg", "hmm": "**/question_001.ogg",
              "creak": "**/creak2.ogg", "flag_flap": "**/cloth3.ogg", "cannon": "**/explosion.ogg"}
GEN = {}  # name -> function returning a stereo float32 array (in-house synthesised effects, see lib/sfxgen.py)
AMBIENT = {"crowd_murmur", "wind", "birds", "fire", "insects", "room_tone", "footsteps", "chewing", "waves", "gulls"}


@functools.lru_cache(maxsize=128)
def load(path):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    a = np.frombuffer(out, np.float32).reshape(-1, 2).copy()
    return a


def sfx(name):
    if name in GEN:
        return GEN[name]()
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


def _build_mix_legacy(ep, plan, out_wav):
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


# =====================================================================================================================
# REAL SOUND (owner 27 Nov 2026)
# =====================================================================================================================
REAL_DIR = SFX_DIR / "real"
MUSIC_REAL = ROOT / "library/music/real"
# old cue names -> real recordings (None = cartoon/synth cue with no real equivalent: dropped in real mode)
ALIAS = {
    "pop": "pop_mouth", "ding": "bell_small", "whoosh": "whoosh_stick", "whoosh_soft": "whoosh_cloth", "shimmer": None, "bloop": "drip",
    "thud": "wood_thud", "click": "click_pen", "sting": None, "drum_hit": "impact_soft", "chime": "bell_small", "tick": "clock_tick",
    "boing": "rubber_band", "creak": "wood_creak", "hmm": None, "swell": None, "zap": None, "sparkle": "tap_glass", "freeze": None,
    "hiss": "spray_bottle", "wind": "amb_wind", "clunk": "metal_clang", "ring_bell": "bell_small", "hum": "lightbulb_buzz",
    "confuse": None, "rumble": "truck_pass", "melt": None, "glass_crack": "glass_break", "beep3": "microwave", "footsteps": "steps_wood",
    "whir": "fan", "power_off": "switch_light", "power_on": "switch_light", "cabin_chime": "elevator_ding", "rush": "whoosh_fast",
    "paper": "paper_rustle", "door": "door_open", "waves": "amb_beach", "gulls": "amb_beach", "riser": None, "meow": "cat_meow",
    "crowd_murmur": "amb_crowd", "bulb_pop": "pop_cork", "bark": "dog_bark", "dog": "dog_bark", "scrape": "metal_scrape",
    "jet_hum": "plane_flyover", "crash": "glass_break", "buzz": "phone_vibrate", "buzz_fast": "phone_vibrate", "alarm": "alarm_bell",
    "purr": "cat_purr", "pour": "pour_water", "coin_single": "coin_drop", "coins": "coins_handful", "chop": "chop_knife",
    "room_tone": "amb_room_quiet", "page_turn": "page_flip", "birds": "amb_park", "drink": "gulp", "quill": "pencil_writing",
    "flag_flap": "whoosh_cloth", "heartbeat": None, "firework": None, "lap": None,
}
MOOD_REAL = {  # legacy procedural mood names -> real music moods
    "curious": "curious", "playful": "light", "story": "warm", "warm": "warm", "tension": "tense", "mystery": "mysterious",
    "dark": "tense", "adventure": "upbeat", "match": "upbeat", "inventive": "curious", "cozy": "warm", "cruise": "warm",
    "travel": "light", "light": "light", "tense": "tense", "upbeat": "upbeat", "mysterious": "mysterious", "festive": "festive",
}
WARNED = set()


def warn(msg):
    if msg not in WARNED:
        WARNED.add(msg); print("WARNING (real sound):", msg, flush=True)


@functools.lru_cache(maxsize=1)
def real_index():
    p = REAL_DIR / "credits.json"
    d = json.loads(p.read_text()) if p.exists() else {}
    return {k: REAL_DIR / v["file"] for k, v in d.items() if (REAL_DIR / v["file"]).exists()}


def resolve_real(name):
    """name -> (array, is_ambience, source) using real recordings first; synth only as a warned fallback; None if dropped."""
    idx = real_index()
    nm = name
    if nm not in idx and nm in ALIAS:
        if ALIAS[nm] is None:
            warn(f"cue '{name}' is a cartoon/synth effect with no real equivalent: dropped (fewer, real effects)")
            return None
        nm = ALIAS[nm]
    if nm in idx:
        return load(idx[nm]), nm.startswith("amb_"), "real"
    if name in SFX:                                   # BigSoundBank: real recordings (CC0)
        return load(SFX_DIR / SFX[name]), name in AMBIENT, "bsb"
    a = sfx(name)                                     # Kenney packs / sfxgen / synthesised
    if a is not None:
        warn(f"no real recording for '{name}': using the synthesised/pack fallback")
        return a, name in AMBIENT, "synth"
    warn(f"unknown cue '{name}': skipped")
    return None


def music_tracks(mood):
    if "/" in mood:                                    # explicit track "curious/onion_capers"
        f = MUSIC_REAL / f"{mood}.ogg"
        return [f] if f.exists() else []
    m = MOOD_REAL.get(mood, mood)
    return sorted((MUSIC_REAL / m).glob("*.ogg"))


def pick_track(mood, ep_id):
    fs = music_tracks(mood)
    if not fs:
        return None
    import zlib
    return fs[zlib.crc32(f"{ep_id}|{mood}".encode()) % len(fs)]   # varies between episodes (anti-template), stable per episode


def music_credit(path):
    p = MUSIC_REAL / "credits.json"
    d = json.loads(p.read_text()) if p.exists() else {}
    key = f"{path.parent.name}/{path.stem}"
    return d.get(key, {}).get("credit")


def _vary(a, rng, pitch=0.04):
    """Natural variation for repeated real effects: small pitch/speed change (resample) + gain."""
    f = 1 + rng.uniform(-pitch, pitch)
    n = int(len(a) / f)
    if n < 8:
        return a
    x = np.linspace(0, len(a) - 1, n)
    out = np.stack([np.interp(x, np.arange(len(a)), a[:, c]) for c in range(a.shape[1])], 1).astype(np.float32)
    return out * float(10 ** (rng.uniform(-1.5, 1.5) / 20))


def _loop_to(a, n, start=0):
    if len(a) == 0 or n <= 0:
        return np.zeros((max(n, 0), 2), np.float32)
    idx = (np.arange(n) + start) % len(a)
    return a[idx]


def _fade(n, fi, fo):
    f = np.ones(n, np.float32)
    fi, fo = min(fi, n // 2), min(fo, n // 2)
    if fi: f[:fi] = np.linspace(0, 1, fi)
    if fo: f[-fo:] = np.linspace(1, 0, fo)
    return f[:, None]


def _db(x):
    return 10 ** (np.asarray(x) / 20)


def _voice_chain(voice):
    from scipy.signal import butter, lfilter
    b, a = butter(2, 75 / (SR / 2), "high"); voice = lfilter(b, a, voice).astype(np.float32)
    env = np.convolve(np.abs(voice), np.ones(441) / 441, "same")
    thr = np.percentile(env[env > 1e-4], 70) if (env > 1e-4).any() else 0.1
    gain = np.where(env > thr, (thr / np.maximum(env, 1e-6)) ** 0.35, 1.0)
    voice = voice * np.convolve(gain, np.ones(882) / 882, "same").astype(np.float32)
    return norm_peak(voice, 0.7)


def _voice_activity(voice):
    venv = np.convolve(np.abs(voice), np.ones(2205) / 2205, "same")
    act = (venv > 0.01).astype(np.float32)
    # fast attack (music dips before the word), slow release (stays down through short pauses)
    from scipy.ndimage import maximum_filter1d, uniform_filter1d
    act = maximum_filter1d(act, size=int(0.45 * SR))
    return np.clip(uniform_filter1d(act, size=int(0.25 * SR)), 0, 1)


def _finish(mix, out_wav, tag):
    import pyloudnorm as pyln
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    lufs = pyln.Meter(SR).integrated_loudness(mix)
    mix = mix * (10 ** ((-14 - lufs) / 20))
    ceil = 10 ** (-3 / 20)
    peak = np.abs(mix).max(1)
    g0 = np.minimum(1.0, ceil / np.maximum(peak, 1e-9))
    la = int(0.005 * SR)
    g = uniform_filter1d(minimum_filter1d(g0, size=2 * la + 1), size=la)
    g = np.minimum(g, minimum_filter1d(g0, size=3))
    mix = mix * g[:, None]
    sf.write(out_wav, mix.astype(np.float32), SR)
    print(f"mix ({tag}) LUFS before norm", round(lufs, 1), "-> -14", flush=True)


def _music_bed(segs, total, ep_id, voice_lufs, act, forward=()):
    """segs: [mood, t0, t1]. Real tracks with 1.6 s crossfades; -20 dB under the voice, -9 dB in gaps, -6 dB on cards/end."""
    music = np.zeros((total, 2), np.float32)
    xf = int(1.6 * SR)
    pos, used = {}, []
    for m, t0, t1 in segs:
        f = pick_track(m, ep_id)
        if f is None:
            pm = ROOT / f"library/music/procedural/{m}.wav"
            if not pm.exists():
                warn(f"no music for mood '{m}'"); continue
            warn(f"no real track for mood '{m}': procedural fallback (keep it quiet)")
            tr, base = load(pm), -18 - 4
        else:
            tr, base = load(f), -18                     # real tracks are stored at -18 LUFS
            if f not in used: used.append(f)
        i0, i1 = max(0, int(t0 * SR) - xf // 2), min(total, int(t1 * SR) + xf // 2)
        n = i1 - i0
        key = str(f)
        seg = _loop_to(tr, n, pos.get(key, 0)); pos[key] = pos.get(key, 0) + n
        music[i0:i1] += seg * _fade(n, xf if t0 > 0 else int(0.05 * SR), xf)
    # level: music LUFS target relative to the voice
    under, gap = voice_lufs - 20, voice_lufs - 9
    db = gap + (under - gap) * act - (-18)
    for i0, i1 in forward:
        db[i0:i1] = np.maximum(db[i0:i1], voice_lufs - 6 + 18)
    music *= _db(db)[:, None].astype(np.float32)
    return music, used


def _amb_bed(amb_segs, total, ep_id, voice_lufs, act):
    """Real ambience bed: about 24 dB under the voice, 3 dB lower while the voice talks, 0.6 s crossfades between scenes."""
    bed = np.zeros((total, 2), np.float32)
    xf = int(0.6 * SR)
    import zlib
    for nm, t0, t1 in amb_segs:
        r = resolve_real(nm)
        if r is None:
            continue
        a = r[0]
        i0, i1 = max(0, int(t0 * SR) - xf // 2), min(total, int(t1 * SR) + xf // 2)
        n = i1 - i0
        st = zlib.crc32(f"{ep_id}|{nm}|{t0:.2f}".encode()) % max(1, len(a))
        bed[i0:i1] += _loop_to(a, n, st) * _fade(n, xf, xf)
    # library ambiences are stored at RMS -26 dBFS (~ -26 LUFS); target voice-24 dB
    g = _db(voice_lufs - 24 - (-26) - 3 * act)
    return bed * g[:, None].astype(np.float32)


def _place_sfx(mix, total, t0, name, g, rng, shot_end=None, counts=None):
    r = resolve_real(name)
    if r is None:
        return
    a, is_amb, src = r
    i = int(t0 * SR)
    if i >= total:
        return
    if is_amb:
        n = int(((shot_end or t0 + 4) - t0) * SR)
        if n <= 0:
            return
        a = _loop_to(a, n) * _fade(n, int(0.3 * SR), int(0.3 * SR)) * 0.5
    else:
        a = norm_peak(a, 0.9)
        if counts is not None:
            counts[name] = counts.get(name, 0) + 1
            if counts[name] > 1:
                a = _vary(a, rng)
        a = a[:int(3.0 * SR)].copy()
        fd = min(int(0.25 * SR), len(a) // 2)
        a[-fd:] *= np.linspace(1, 0, fd)[:, None]
        g *= 0.55
    j = min(total, i + len(a))
    mix[i:j] += a[:j - i] * g


def sound_mode(ep, plan):
    m = plan.get("sound") or os.environ.get("TW_SOUND")
    if m:
        return m
    return "legacy" if (Path(ep) / "uploaded.json").exists() else "real"


def _build_mix_real(ep, plan, out_wav):
    ep = Path(ep)
    ep_id = plan.get("episode") or ep.name[:5]
    total = int((plan["duration"] + 0.5) * SR)
    voice = _voice_track(str(ep), json.dumps(plan))[:total]
    voice = _voice_chain(np.pad(voice, (0, max(0, total - len(voice)))))
    act = _voice_activity(voice)
    import pyloudnorm as pyln
    vs = np.stack([voice, voice], 1)
    voice_lufs = pyln.Meter(SR).integrated_loudness(vs) if np.abs(voice).max() > 0 else -20.0
    if not np.isfinite(voice_lufs): voice_lufs = -20.0
    mix = vs.copy()
    # music segments (sticky mood)
    segs, mood = [], plan.get("music") or "curious"
    for sh in plan["shots"]:
        if sh.get("music"): mood = sh["music"]
        if segs and segs[-1][0] == mood: segs[-1][2] = sh["start"] + sh["dur"]
        else: segs.append([mood, sh["start"], sh["start"] + sh["dur"]])
    if len(segs) > 1 and plan["duration"] < 75 and not plan.get("music_changes"):
        # a Short keeps ONE real track (an editor would not jump between 3 songs in 30 s); plan["music_changes"]=True to allow it
        print("note: Short -> one music track for the whole video (mood", segs[0][0] + ")", flush=True)
        segs = [[segs[0][0], 0.0, plan["duration"]]]
    fwd = [(int(sh["start"] * SR), min(total, int((sh["start"] + sh["dur"]) * SR))) for sh in plan["shots"] if sh["kind"] in ("card", "end", "title")]
    music, used = _music_bed(segs, total, ep_id, voice_lufs, act, fwd)
    mix += music
    # ambience bed (sticky "amb"); default: a quiet real room tone so no scene is ever dead silent
    amb_segs, amb = [], plan.get("amb")
    if not amb and not any(sh.get("amb") for sh in plan["shots"]):
        warn("no ambience set (Video(amb=...) or shot(amb=...)): using amb_room_quiet under every scene")
        amb = "amb_room_quiet"
    for sh in plan["shots"]:
        if sh.get("amb"): amb = sh["amb"]
        if amb in (None, "none"): continue
        if amb_segs and amb_segs[-1][0] == amb and abs(amb_segs[-1][2] - sh["start"]) < 1e-3: amb_segs[-1][2] = sh["start"] + sh["dur"]
        else: amb_segs.append([amb, sh["start"], sh["start"] + sh["dur"]])
    mix += _amb_bed(amb_segs, total, ep_id, voice_lufs, act)
    # SFX: real recordings, natural variation on repeats; SFX bus about 6 dB under the voice peak
    rng = np.random.default_rng(abs(hash(ep_id)) % (2 ** 32))
    counts, sfxbus = {}, np.zeros((total, 2), np.float32)
    for sh in plan["shots"]:
        d = sh["dur"]
        if sh["kind"] == "card":
            _place_sfx(sfxbus, total, sh["start"], "whoosh_cloth", 0.45, rng, counts=counts)
        for (off, nm, g) in sh.get("sfx", []):
            t0 = sh["start"] + (off * d if off <= 1 else off)
            _place_sfx(sfxbus, total, t0, nm, g, rng, shot_end=sh["start"] + d, counts=counts)
    mix += sfxbus * float(_db(voice_lufs + 20))   # scaled to the voice loudness (same level as the legacy mix)
    # music credits for the description (CC BY 4.0)
    cr = [c for c in (music_credit(f) for f in used) if c]
    if cr:
        (ep / "audio").mkdir(exist_ok=True)
        (ep / "audio/music_credits.txt").write_text("\n\n".join(cr) + "\n")
        print("MUSIC CREDIT (put in the description):", "; ".join(c.splitlines()[0] for c in cr), flush=True)
    _finish(mix, out_wav, "real")
    return used


def build_mix(ep, plan, out_wav):
    mode = sound_mode(ep, plan)
    print("sound mode:", mode, flush=True)
    if mode == "legacy":
        return _build_mix_legacy(ep, plan, out_wav)
    return _build_mix_real(ep, plan, out_wav)


def mix_voice_file(voice_path, out_wav, mood="light", amb="amb_room_quiet", cues=(), pad=1.5, seed=1, ep_id="SAMPLE"):
    """Stand-alone mix of one narration file with real music + ambience + SFX cues [(t, name, gain)] (voice samples, demos)."""
    v, sr = sf.read(voice_path, dtype="float32")
    if v.ndim > 1: v = v.mean(1)
    if sr != SR:
        v = np.interp(np.arange(0, len(v), sr / SR), np.arange(len(v)), v).astype(np.float32)
    p0 = int(0.6 * SR)
    total = p0 + len(v) + int(pad * SR)
    voice = np.zeros(total, np.float32); voice[p0:p0 + len(v)] = v
    voice = _voice_chain(voice)
    act = _voice_activity(voice)
    import pyloudnorm as pyln
    vs = np.stack([voice, voice], 1)
    vl = pyln.Meter(SR).integrated_loudness(vs)
    music, used = _music_bed([[mood, 0, total / SR]], total, ep_id, vl, act)
    music *= _fade(total, 1, int(1.2 * SR))
    mix = vs + music + _amb_bed([[amb, 0, total / SR]], total, ep_id, vl, act)
    rng = np.random.default_rng(seed)
    bus, counts = np.zeros((total, 2), np.float32), {}
    for t, nm, g in cues:
        _place_sfx(bus, total, t + p0 / SR, nm, g, rng, counts=counts)
    mix += bus * float(_db(vl + 20))
    _finish(mix, out_wav, "real")
    return used
