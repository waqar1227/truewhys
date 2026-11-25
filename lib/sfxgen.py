"""In-house synthesised sound effects (numpy only, original). Importing this registers them with lib/audio (audio.GEN),
so a shot can use them by name like any library sound: chop, alarm, hiss, freeze, zap, swell, rush, heartbeat, sting, melt, confuse, bloop, click, shimmer, chime."""
import functools
import numpy as np
import audio

SR = audio.SR


def _st(x, peak=0.8):
    x = np.asarray(x, np.float64)
    m = np.abs(x).max() or 1.0
    x = x / m * peak
    return np.stack([x, x], 1).astype(np.float32)


def _t(dur):
    return np.arange(int(dur * SR)) / SR


def _bell(f, dur, decay):
    t = _t(dur)
    return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / (decay * 0.4))) * np.exp(-t / decay)


def _put(x, y, at):
    i = int(at * SR); n = min(len(y), len(x) - i)
    if n > 0: x[i:i + n] += y[:n]


@functools.lru_cache(maxsize=None)
def freeze():
    """Icy crackle with rising glassy glints."""
    rng = np.random.default_rng(5)
    x = np.zeros(int(1.2 * SR))
    for k in range(70):
        f = rng.uniform(2500, 7500); d = _t(0.03)
        _put(x, np.sin(2 * np.pi * f * d) * np.exp(-d / 0.006) * rng.uniform(0.2, 0.8), rng.uniform(0, 0.75) ** 1.4)
    for j, f in enumerate((1568, 2093, 2637, 3136)):
        _put(x, 0.4 * _bell(f, 0.9, 0.22), 0.04 + j * 0.085)
    return _st(x)


@functools.lru_cache(maxsize=None)
def zap():
    """Quick rising electric chirp (a nerve signal)."""
    t = _t(0.32)
    f = 380 + 1500 * (t / t[-1]) ** 1.6
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sign(np.sin(ph)) * 0.35 + np.sin(ph) * 0.65
    x *= (0.6 + 0.4 * np.sin(2 * np.pi * 38 * t)) * np.exp(-((t - 0.12) / 0.16) ** 2)
    return _st(x, 0.6)


@functools.lru_cache(maxsize=None)
def swell():
    """Low tone that swells and bulges (something widening)."""
    t = _t(0.95)
    f = 70 + 95 * (t / t[-1]) ** 2
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.tanh(2.2 * np.sin(ph)) * (t / t[-1]) ** 1.3 * np.minimum(1, (t[-1] - t) / 0.08)
    x += 0.25 * np.sin(2 * ph) * (t / t[-1]) ** 2 * np.minimum(1, (t[-1] - t) / 0.08)
    return _st(x)


@functools.lru_cache(maxsize=None)
def rush():
    """Whooshing stream with a pulse (blood rushing in)."""
    from scipy.signal import butter, lfilter
    t = _t(1.25)
    n = np.random.default_rng(7).normal(0, 1, len(t))
    b, a = butter(2, [500 / (SR / 2), 2600 / (SR / 2)], "band")
    x = lfilter(b, a, n) * np.sin(np.pi * t / t[-1]) ** 1.5 * (0.7 + 0.3 * np.sin(2 * np.pi * 7 * t))
    x = x / (np.abs(x).max() or 1) + 0.5 * np.sin(2 * np.pi * 62 * t) * np.sin(np.pi * t / t[-1]) ** 2 * (0.5 + 0.5 * np.sin(2 * np.pi * 3.2 * t))
    return _st(x, 0.7)


@functools.lru_cache(maxsize=None)
def heartbeat():
    x = np.zeros(int(1.3 * SR))
    for at, g in ((0.0, 1.0), (0.26, 0.75), (0.66, 1.0), (0.92, 0.75)):
        t = _t(0.22)
        _put(x, g * np.sin(2 * np.pi * (58 + 30 * np.exp(-t / 0.03)) * t) * np.exp(-t / 0.07), at)
    return _st(x)


@functools.lru_cache(maxsize=None)
def sting():
    """Short cartoon 'ouch' stab."""
    t = _t(0.5)
    x = sum(((2 * ((f * t) % 1) - 1) for f in (233.1, 246.9, 466.2))) * np.exp(-t / 0.13)
    x += 0.6 * np.sin(2 * np.pi * 90 * t) * np.exp(-t / 0.06)
    from scipy.signal import butter, lfilter
    b, a = butter(2, 2400 / (SR / 2))
    return _st(lfilter(b, a, x), 0.65)


@functools.lru_cache(maxsize=None)
def melt():
    """Soft descending chime (relief, melting)."""
    x = np.zeros(int(1.5 * SR))
    for j, f in enumerate((1567.98, 1318.51, 1046.5, 783.99)):
        _put(x, 0.5 * _bell(f, 1.1, 0.35), j * 0.11)
    return _st(x, 0.6)


@functools.lru_cache(maxsize=None)
def confuse():
    """Wobbly sliding tone (confused)."""
    t = _t(0.9)
    f = 430 + 150 * np.sin(2 * np.pi * 2.6 * t) * np.exp(-t / 0.9) - 120 * t
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.03 * np.sin(2 * np.pi * 11 * t))) / SR
    x = (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.minimum(1, t / 0.03) * np.minimum(1, (t[-1] - t) / 0.2)
    return _st(x, 0.55)


@functools.lru_cache(maxsize=None)
def bloop():
    t = _t(0.16)
    f = 330 + 500 * (t / t[-1])
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.07) * np.minimum(1, t / 0.004)
    return _st(x, 0.6)


@functools.lru_cache(maxsize=None)
def click():
    """Metal lock click."""
    rng = np.random.default_rng(3)
    x = np.zeros(int(0.3 * SR))
    for at, f in ((0.0, 2100), (0.07, 1500)):
        t = _t(0.06)
        _put(x, (np.sin(2 * np.pi * f * t) + 0.6 * rng.normal(0, 1, len(t))) * np.exp(-t / 0.012), at)
    return _st(x, 0.7)


@functools.lru_cache(maxsize=None)
def shimmer():
    rng = np.random.default_rng(9)
    x = np.zeros(int(1.4 * SR))
    for k in range(14):
        _put(x, 0.4 * _bell(rng.choice([1567.98, 1760, 2093, 2349.3, 2637, 3136]), 0.8, 0.2), rng.uniform(0, 0.7))
    return _st(x, 0.55)


@functools.lru_cache(maxsize=None)
def chime():
    a = _bell(1318.5, 1.2, 0.4); b = _bell(1975.5, 1.0, 0.3)
    a[:len(b)] += 0.6 * b          # second bell is shorter: add it onto the start (fixed 20 Nov)
    return _st(a, 0.6)


@functools.lru_cache(maxsize=None)
def chop():
    """Knife through something crisp onto a wooden board: wet crunch + low wooden knock."""
    rng = np.random.default_rng(12)
    x = np.zeros(int(0.35 * SR)); t = _t(0.35)
    crunch = rng.normal(0, 1, int(0.06 * SR)) * np.exp(-_t(0.06) / 0.018)
    from scipy.signal import butter, lfilter
    b, a = butter(2, [1800 / (SR / 2), 7000 / (SR / 2)], "band"); _put(x, lfilter(b, a, crunch) * 1.2, 0.0)
    knock = (np.sin(2 * np.pi * 180 * t) + 0.5 * np.sin(2 * np.pi * 410 * t)) * np.exp(-t / 0.035)
    _put(x, knock * 0.9, 0.045)
    return _st(x, 0.8)


@functools.lru_cache(maxsize=None)
def alarm():
    """Two short soft alert beeps (nerve 'alarm'), not harsh."""
    x = np.zeros(int(0.7 * SR))
    for k in range(2):
        d = _t(0.14); _put(x, np.sin(2 * np.pi * 880 * d) * np.minimum(1, d / 0.01) * np.exp(-d / 0.09), 0.05 + k * 0.25)
    return _st(x, 0.5)


@functools.lru_cache(maxsize=None)
def hiss():
    """Soft rising gas hiss."""
    rng = np.random.default_rng(13)
    n = int(1.6 * SR); t = np.arange(n) / SR
    from scipy.signal import butter, lfilter
    b, a = butter(2, [3000 / (SR / 2), 9000 / (SR / 2)], "band")
    y = lfilter(b, a, rng.normal(0, 1, n)) * np.minimum(1, t / 0.6) * np.exp(-np.maximum(0, t - 1.0) / 0.25)
    return _st(y, 0.4)


audio.GEN.update(chop=chop, alarm=alarm, hiss=hiss)
audio.GEN.update(freeze=freeze, zap=zap, swell=swell, rush=rush, heartbeat=heartbeat, sting=sting, melt=melt, confuse=confuse, bloop=bloop,
                 click=click, shimmer=shimmer, chime=chime)


@functools.lru_cache(maxsize=None)
def siren():
    """Generic emergency siren (original synth, 2.4 s): rising-falling 'wail' with soft harmonics and a slight doppler swell. Not any real service's tone."""
    t = _t(2.4)
    f = 700 + 450 * (0.5 - 0.5 * np.cos(2 * np.pi * t / 1.2))          # wail 700-1150 Hz, 1.2 s cycle
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)
    env = np.minimum(1, t / 0.15) * (0.75 + 0.25 * np.sin(np.pi * t / 2.4)) * np.minimum(1, (2.4 - t) / 0.3)
    return _st(y * env, 0.45)


@functools.lru_cache(maxsize=None)
def siren_yelp():
    """Fast 'yelp' siren burst (original synth, 0.9 s) for a hit at frame 0."""
    t = _t(0.9)
    f = 750 + 400 * (0.5 - 0.5 * np.cos(2 * np.pi * t / 0.18))
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.minimum(1, t / 0.02) * np.minimum(1, (0.9 - t) / 0.2)
    return _st(y, 0.5)


audio.GEN.update(siren=siren, siren_yelp=siren_yelp)


@functools.lru_cache(maxsize=None)
def hum():
    """Appliance hum (original synth, 2.5 s): 120 Hz transformer buzz + soft fan air, fades in/out (microwave running)."""
    from scipy.signal import butter, lfilter
    t = _t(2.5); rng = np.random.default_rng(21)
    buzz = np.sign(np.sin(2 * np.pi * 120 * t)) * 0.25 + np.sin(2 * np.pi * 120 * t) * 0.5 + 0.2 * np.sin(2 * np.pi * 240 * t)
    b, a = butter(2, [300 / (SR / 2), 1800 / (SR / 2)], "band"); air = lfilter(b, a, rng.normal(0, 1, len(t)))
    air /= (np.abs(air).max() or 1)
    env = np.minimum(1, t / 0.25) * np.minimum(1, (2.5 - t) / 0.4)
    return _st((0.6 * buzz + 0.5 * air) * env, 0.4)


@functools.lru_cache(maxsize=None)
def beep3():
    """Three short appliance 'done' beeps (original synth, 1.1 s)."""
    x = np.zeros(int(1.1 * SR))
    for k in range(3):
        d = _t(0.18); _put(x, np.sin(2 * np.pi * 2000 * d) * np.minimum(1, d / 0.005) * np.minimum(1, (0.18 - d) / 0.02), 0.02 + k * 0.32)
    return _st(x, 0.45)


audio.GEN.update(hum=hum, beep3=beep3)


@functools.lru_cache(maxsize=None)
def buzz():
    """Phone on vibrate (original synth, 1.0 s): two 0.3 s pulses of a ~170 Hz motor rattle (B-006)."""
    t = _t(0.3)
    motor = np.sign(np.sin(2 * np.pi * 172 * t)) * 0.5 + np.sin(2 * np.pi * 172 * t) * 0.6 + 0.25 * np.sin(2 * np.pi * 344 * t + 0.3)
    motor *= (0.85 + 0.15 * np.sin(2 * np.pi * 23 * t)) * np.minimum(1, t / 0.01) * np.minimum(1, (0.3 - t) / 0.03)
    x = np.zeros(int(1.0 * SR))
    _put(x, motor, 0.0); _put(x, motor, 0.45)
    return _st(x, 0.5)


audio.GEN.update(buzz=buzz)


@functools.lru_cache(maxsize=None)
def glass_crack():
    """Glass cracking (original synth, 0.9 s, A-028): a sharp snap, then a fast run of tiny ticks and a ringing glassy tail."""
    rng = np.random.default_rng(28)
    x = np.zeros(int(0.9 * SR))
    snap = rng.normal(0, 1, int(0.02 * SR)) * np.exp(-_t(0.02) / 0.003)
    _put(x, snap * 1.0, 0.0)
    for k in range(55):                                   # the crack running: ticks that thin out
        at = 0.01 + (k / 55) ** 1.6 * 0.6
        f = rng.uniform(2000, 6500); d = _t(0.012)
        _put(x, np.sin(2 * np.pi * f * d) * np.exp(-d / 0.003) * rng.uniform(0.3, 0.9) * (1 - k / 70), at)
    for f in (3150, 4420, 5980):
        _put(x, 0.12 * _bell(f, 0.8, 0.18), 0.0)
    return _st(x, 0.85)


@functools.lru_cache(maxsize=None)
def scrape():
    """Ice scraper on a windshield (original synth, 1.2 s): three gritty strokes."""
    from scipy.signal import butter, lfilter
    rng = np.random.default_rng(29)
    x = np.zeros(int(1.2 * SR))
    b, a = butter(2, [1200 / (SR / 2), 6000 / (SR / 2)], "band")
    for k in range(3):
        n = int(0.3 * SR); t = np.arange(n) / SR
        grit = lfilter(b, a, rng.normal(0, 1, n)) * (0.6 + 0.4 * (rng.random(n) > 0.85))
        _put(x, grit * np.sin(np.pi * t / 0.3) ** 0.6, 0.02 + k * 0.38)
    return _st(x, 0.5)


@functools.lru_cache(maxsize=None)
def pour():
    """Water pouring from a kettle (original synth, 1.4 s): bubbly filtered noise with a gurgle."""
    from scipy.signal import butter, lfilter
    rng = np.random.default_rng(30)
    n = int(1.4 * SR); t = np.arange(n) / SR
    b, a = butter(2, [500 / (SR / 2), 3500 / (SR / 2)], "band")
    y = lfilter(b, a, rng.normal(0, 1, n)) * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * t + 3 * np.sin(2 * np.pi * 2.3 * t)))
    for k in range(14):
        f = rng.uniform(300, 900); d = _t(0.05)
        _put(y, 2.5 * np.sin(2 * np.pi * f * (1 + 3 * d) * d) * np.exp(-d / 0.015), rng.uniform(0.05, 1.2))
    return _st(y * np.minimum(1, t / 0.08) * np.minimum(1, (1.4 - t) / 0.3), 0.45)


audio.GEN.update(glass_crack=glass_crack, scrape=scrape, pour=pour)


# ---- B-007 cats vs dogs (25 Nov 2026), original synths
@functools.lru_cache(maxsize=None)
def ring_bell():
    """Boxing-style round bell, two strikes (original synth, 1.4 s)."""
    x = np.zeros(int(1.4 * SR))
    for at in (0.0, 0.32):
        b = _bell(1180, 1.0, 0.35) + 0.6 * _bell(2950, 1.0, 0.2) + 0.3 * _bell(4720, 1.0, 0.12)
        _put(x, b, at)
    return _st(x, 0.6)


@functools.lru_cache(maxsize=None)
def purr():
    """Cat purr (original synth, 1.6 s): ~26 Hz amplitude pulses on low filtered noise, in/out breaths."""
    t = _t(1.6)
    n = np.random.default_rng(7).normal(0, 1, len(t))
    k = np.ones(60) / 60
    low = np.convolve(n, k, "same") * 6
    pul = (0.5 + 0.5 * np.sin(2 * np.pi * 26 * t)) ** 3
    breath = 0.65 + 0.35 * np.sin(2 * np.pi * 0.9 * t)
    x = low * pul * breath + 0.3 * np.sin(2 * np.pi * 52 * t) * pul
    x *= np.minimum(1, t / 0.15) * np.minimum(1, (1.6 - t) / 0.2)
    return _st(x, 0.55)


@functools.lru_cache(maxsize=None)
def lap():
    """Four quick tongue flicks on water (original synth, 1.0 s)."""
    x = np.zeros(int(1.0 * SR))
    for i in range(4):
        tt = _t(0.06)
        f = 900 + 1400 * tt / 0.06
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 60)
        _put(x, s, i * 0.25)
    return _st(x, 0.5)


audio.GEN.update(ring_bell=ring_bell, purr=purr, lap=lap)


# ---- A-029 / A-030 / A-031 (25 Nov 2026), original synths
@functools.lru_cache(maxsize=None)
def rumble():
    """Controller rumble motor (original synth, 0.9 s): a lopsided weight spinning ~38 Hz, low gritty rattle."""
    t = _t(0.9)
    f = 30 + 10 * np.minimum(1, t / 0.15)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) + 0.5 * np.sign(np.sin(ph)) + 0.35 * np.sin(3 * ph)
    rattle = np.random.default_rng(40).normal(0, 1, len(t)) * (0.5 + 0.5 * np.sin(ph)) ** 4
    x = (body + 0.35 * np.convolve(rattle, np.ones(12) / 12, "same")) * np.minimum(1, t / 0.03) * np.minimum(1, (0.9 - t) / 0.12)
    return _st(x, 0.6)


@functools.lru_cache(maxsize=None)
def buzz_fast():
    """Light rumble weight (original synth, 0.6 s): a thin, fast ~140 Hz buzz."""
    t = _t(0.6)
    x = np.sign(np.sin(2 * np.pi * 140 * t)) * 0.4 + np.sin(2 * np.pi * 140 * t) * 0.6
    x *= (0.8 + 0.2 * np.sin(2 * np.pi * 31 * t)) * np.minimum(1, t / 0.01) * np.minimum(1, (0.6 - t) / 0.06)
    return _st(x, 0.45)


@functools.lru_cache(maxsize=None)
def whir():
    """Small motor spinning up (original synth, 1.0 s)."""
    t = _t(1.0)
    f = 60 + 520 * (t / t[-1]) ** 0.7
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.15 * np.sign(np.sin(ph))) * np.minimum(1, t / 0.05) * np.minimum(1, (1.0 - t) / 0.1)
    return _st(x, 0.4)


@functools.lru_cache(maxsize=None)
def crash():
    """Cartoon car crash (original synth, 1.1 s): a thump, a metal clang and rattling bits."""
    rng = np.random.default_rng(41)
    x = np.zeros(int(1.1 * SR))
    tt = _t(0.25)
    _put(x, np.sin(2 * np.pi * (90 - 200 * tt) * tt) * np.exp(-tt / 0.06) * 1.4, 0.0)
    _put(x, rng.normal(0, 1, len(tt)) * np.exp(-tt / 0.05) * 0.9, 0.0)
    for f in (420, 655, 1130, 1720):
        _put(x, 0.35 * _bell(f, 0.8, 0.16), 0.01)
    for k in range(16):
        d = _t(0.04); f = rng.uniform(1500, 5000)
        _put(x, np.sin(2 * np.pi * f * d) * np.exp(-d / 0.008) * rng.uniform(0.2, 0.6), 0.08 + rng.uniform(0, 0.8) ** 1.5)
    return _st(x, 0.85)


@functools.lru_cache(maxsize=None)
def bulb_pop():
    """A tiny bulb filament snapping (original synth, 0.5 s): a small pop and a glassy tink."""
    rng = np.random.default_rng(42)
    x = np.zeros(int(0.5 * SR))
    _put(x, rng.normal(0, 1, int(0.012 * SR)) * np.exp(-_t(0.012) / 0.002), 0.0)
    _put(x, 0.5 * _bell(3700, 0.45, 0.08) + 0.3 * _bell(5200, 0.45, 0.05), 0.005)
    return _st(x, 0.6)


@functools.lru_cache(maxsize=None)
def power_off():
    """Lights going out (original synth, 0.9 s): an electric hum that drops in pitch and fades."""
    t = _t(0.9)
    f = 120 * np.exp(-t / 0.35) + 30
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sign(np.sin(ph))) * np.exp(-t / 0.4)
    return _st(x, 0.5)


@functools.lru_cache(maxsize=None)
def power_on():
    """Lights coming on (original synth, 1.0 s): a rising hum and a soft bright chime."""
    t = _t(1.0)
    f = 40 + 180 * np.minimum(1, t / 0.5)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.minimum(1, t / 0.2) * np.exp(-np.maximum(0, t - 0.5) / 0.2) * 0.6
    for j, ff in enumerate((1318, 1760, 2637)):
        _put(x, 0.35 * _bell(ff, 0.6, 0.18), 0.35 + j * 0.06)
    return _st(x, 0.55)


@functools.lru_cache(maxsize=None)
def firework():
    """Firework (original synth, 1.6 s): a whistle up, a soft boom and crackles."""
    rng = np.random.default_rng(43)
    x = np.zeros(int(1.6 * SR))
    tw = _t(0.5)
    _put(x, 0.25 * np.sin(2 * np.pi * np.cumsum(900 + 1800 * tw / 0.5) / SR) * np.minimum(1, tw / 0.05), 0.0)
    tb = _t(0.6)
    _put(x, (np.sin(2 * np.pi * (70 - 50 * tb) * tb) + 0.6 * rng.normal(0, 1, len(tb)) * np.exp(-tb / 0.03)) * np.exp(-tb / 0.18), 0.5)
    for k in range(40):
        d = _t(0.02); f = rng.uniform(2000, 7000)
        _put(x, np.sin(2 * np.pi * f * d) * np.exp(-d / 0.004) * rng.uniform(0.1, 0.4), 0.6 + rng.uniform(0, 0.9))
    return _st(x, 0.7)


@functools.lru_cache(maxsize=None)
def clunk():
    """A big ball dropping down a mast and stopping (original synth, 0.7 s): slide, then a wooden clunk."""
    rng = np.random.default_rng(44)
    x = np.zeros(int(0.7 * SR))
    ts = _t(0.35)
    _put(x, rng.normal(0, 1, len(ts)) * 0.15 * np.minimum(1, ts / 0.3), 0.0)
    tc = _t(0.3)
    _put(x, (np.sin(2 * np.pi * 160 * tc) + 0.5 * np.sin(2 * np.pi * 410 * tc)) * np.exp(-tc / 0.05), 0.35)
    return _st(x, 0.7)


audio.GEN.update(rumble=rumble, buzz_fast=buzz_fast, whir=whir, crash=crash, bulb_pop=bulb_pop, power_off=power_off,
                 power_on=power_on, firework=firework, clunk=clunk)
