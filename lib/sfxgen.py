"""In-house synthesised sound effects (numpy only, original). Importing this registers them with lib/audio (audio.GEN),
so a shot can use them by name like any library sound: freeze, zap, swell, rush, heartbeat, sting, melt, confuse, bloop, click, shimmer, chime."""
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
    return _st(_bell(1318.5, 1.2, 0.4) + 0.6 * _bell(1975.5, 1.0, 0.3), 0.6)


audio.GEN.update(freeze=freeze, zap=zap, swell=swell, rush=rush, heartbeat=heartbeat, sting=sting, melt=melt, confuse=confuse, bloop=bloop,
                 click=click, shimmer=shimmer, chime=chime)
