"""Does the narration sound like a real person? (owner 27 Nov 2026: "no robotic or AI ... mood, expressions, feelings").
/opt/c3d/bin/python tools/voice_human_check.py episodes/<ep>        -> per-line + overall report, PASS/FAIL, <ep>/voice_check.json
/opt/c3d/bin/python tools/voice_human_check.py some.wav other.flac  -> the same checks on loose files (calibration, samples)
Add --quiet to print only the verdict line.

Measures (no AI, plain signal analysis):
  pitch (F0, autocorrelation tracker)  range p5-p95 and std in semitones; flat = monotone
  monotone stretches                   longest run of >= 2.5 s speech whose pitch hardly moves (std < 1.3 st)
  pace                                 syllable rate per phrase (loudness peaks), variation (CV) across phrases and lines
  pauses                               count per minute, mean, variation (CV): a real reader pauses unevenly
  energy                               phrase-to-phrase loudness spread (dB) and in-phrase dynamics
  mood contrast                        how much pitch / pace / loudness change BETWEEN lines (the delivery follows the story)
  artefacts                            clipping, clicks, drop-outs inside words, loudness or pitch jumps at the joins of scene takes
Thresholds were calibrated on 27 Nov 2026 (docs/voice_samples/calibration.md): our Gemini masters (direction-led reads) vs
Kokoro, espeak-ng and pitch-flattened copies of our own takes, which all sound flat/robotic. A FAIL means "listen: this sounds flat".
The number check is not a replacement for listening: the QA gate needs PASS here AND a listen-check of the final mix.
"""
import sys, json, re
from pathlib import Path
import numpy as np, soundfile as sf
from scipy.signal import resample_poly, butter, sosfiltfilt, find_peaks

SR = 16000
HOP = 160                      # 10 ms
WIN = 640                      # 40 ms

# --- thresholds (see calibration.md). "fail" values = clearly flat; "warn" = weak, worth a listen
T = dict(
    pitch_std_st=(2.6, 3.6),        # overall pitch std (semitones): robot/espeak 1.0-2.1, Kokoro ~3.5, our Gemini masters 3.5-5.1
    pitch_range_st=(8.0, 12.0),     # p5..p95 range (semitones): robot 1.2-1.9, espeak ~6, Kokoro 10.6-11.8, Gemini 11.4-16.2
    mono_longest_s=(3.0, 1.5),      # longest monotone run (s of speech; larger is worse): robots 2.4-7.5, every Gemini master 0
    mono_frac=(0.15, 0.05),         # share of speech inside monotone runs (larger is worse): robots 0.38-0.98, Gemini 0
    rate_cv=(0.05, 0.08),           # pace variation across phrases: A-030 0.043 (steady), most masters 0.10-0.30
    pause_cv=(0.15, 0.25),          # pause-length variation (>= 4 pauses): espeak 0.07-0.20, Kokoro 0.18-0.33, Gemini 0.25-0.63
    energy_std_db=(0.4, 0.7),       # phrase loudness spread (dB): espeak 0.4-0.6, Gemini 0.45-3.0
    contrast=(1.0, 1.3),            # mood contrast between lines: robot 0.4-0.8, Kokoro 0.5-0.97, A-030/A-031 0.5, best masters 1.5-2.0
)
LOWER_IS_WORSE = {"pitch_std_st", "pitch_range_st", "rate_cv", "pause_cv", "energy_std_db", "contrast"}


def load(path):
    a, sr = sf.read(str(path), dtype="float32")
    if a.ndim > 1:
        a = a.mean(1)
    if sr != SR:
        from math import gcd
        g = gcd(sr, SR)
        a = resample_poly(a, SR // g, sr // g).astype(np.float32)
    return a


def frames(a):
    n = max(0, 1 + (len(a) - WIN) // HOP)
    idx = np.arange(WIN)[None, :] + HOP * np.arange(n)[:, None]
    return a[idx] if n else np.zeros((0, WIN), np.float32)


def f0_track(a):
    """Per 10 ms frame: f0 in Hz (0 = unvoiced), periodicity, rms dB."""
    fr = frames(a)
    rms = np.sqrt((fr ** 2).mean(1) + 1e-12)
    db = 20 * np.log10(rms + 1e-9)
    w = fr - fr.mean(1, keepdims=True)
    w = w * np.hanning(WIN)[None, :]
    X = np.fft.rfft(w, 2048, axis=1)
    ac = np.fft.irfft(np.abs(X) ** 2, axis=1)[:, :WIN]
    # normalise by the window's own autocorrelation so long lags are not penalised
    hw = np.hanning(WIN)
    wac = np.correlate(hw, hw, "full")[WIN - 1:]
    ac = ac / (ac[:, :1] + 1e-12) / (wac / wac[0] + 1e-6)
    lo, hi = SR // 400, SR // 60
    seg = ac[:, lo:hi]
    k = seg.argmax(1)
    peak = seg[np.arange(len(seg)), k]
    # parabolic interpolation
    kk = np.clip(k, 1, seg.shape[1] - 2)
    y0, y1, y2 = seg[np.arange(len(seg)), kk - 1], seg[np.arange(len(seg)), kk], seg[np.arange(len(seg)), kk + 1]
    den = (y0 - 2 * y1 + y2)
    off = np.where(np.abs(den) > 1e-9, 0.5 * (y0 - y2) / den, 0)
    lag = lo + kk + np.clip(off, -1, 1)
    f0 = SR / lag
    loud = db > (np.percentile(db, 95) - 30)
    voiced = (peak > 0.5) & loud
    f0 = np.where(voiced, f0, 0.0)
    # octave-jump cleanup: compare with a running median of voiced frames
    v = np.where(f0 > 0)[0]
    if len(v) > 10:
        med = np.median(f0[v])
        for i in v:
            r = f0[i] / med
            if r > 1.8:
                f0[i] /= 2
            elif r < 0.55:
                f0[i] *= 2
        # 5-frame median smoothing inside voiced runs
        g = f0.copy()
        for i in v:
            w5 = f0[max(0, i - 2):i + 3]
            w5 = w5[w5 > 0]
            g[i] = np.median(w5)
        f0 = g
    return f0, peak, db


def speech_mask(db):
    """Speech frames (with 60 ms hangover) vs silence: silence = 32 dB under the loud level."""
    thr = np.percentile(db, 95) - 32
    s = db > thr
    out = s.copy()
    for k in range(1, 7):
        out[:-k] |= s[k:]
        out[k:] |= s[:-k]
    return out


def runs(mask):
    """[(start, end)] frame index runs where mask is True."""
    m = np.concatenate([[0], mask.astype(int), [0]])
    d = np.diff(m)
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))


def syllable_peaks(a):
    sos = butter(4, [300, 3000], "bandpass", fs=SR, output="sos")
    env = np.abs(sosfiltfilt(sos, a))
    sos2 = butter(2, 12, "lowpass", fs=SR, output="sos")
    env = sosfiltfilt(sos2, env)[::HOP]
    envdb = 20 * np.log10(np.maximum(env, 1e-6))
    pk, _ = find_peaks(envdb, distance=9, prominence=3.5, height=np.percentile(envdb, 95) - 25)
    return pk


def analyse(a, words=None):
    """Feature dict for one mono 16 kHz signal."""
    f0, per, db = f0_track(a)
    n = len(db)
    sp = speech_mask(db)
    rr = runs(sp)
    if not rr:
        return dict(dur=len(a) / SR, speech=0)
    first, last = rr[0][0], rr[-1][1]
    # pauses = gaps >= 120 ms between speech runs
    pauses = [(e, s2) for (s1, e), (s2, e2) in zip(rr, rr[1:]) if s2 - e >= 12]
    # phrases = speech between pauses
    bounds = [first] + [p for g in pauses for p in g] + [last]
    phrases = [(bounds[i], bounds[i + 1]) for i in range(0, len(bounds), 2)]
    voiced = np.where(f0 > 0)[0]
    st = 12 * np.log2(f0[voiced] / np.median(f0[voiced])) if len(voiced) > 20 else np.zeros(1)
    pk = syllable_peaks(a)
    rates, plouds, pdyn = [], [], []
    for s, e in phrases:
        dur = (e - s) / 100
        if dur < 0.6:
            continue
        nsyl = ((pk >= s) & (pk < e)).sum()
        rates.append(nsyl / dur)
        seg = db[s:e][sp[s:e]]
        plouds.append(10 * np.log10(np.mean(10 ** (seg / 10))))
        pdyn.append(np.percentile(seg, 90) - np.percentile(seg, 20))
    # monotone runs: slide 2.5 s of voiced speech, std < 1.3 st
    mono = np.zeros(n, bool)
    if len(voiced) > 250:
        W = 250
        stf = np.zeros(n); stf[voiced] = st
        for i in range(0, len(voiced) - W, 10):
            idx = voiced[i:i + W]
            if idx[-1] - idx[0] > 600:      # too spread out (long pauses inside): not one stretch
                continue
            if np.std(stf[idx]) < 1.3:
                mono[idx[0]:idx[-1] + 1] = True
    mono &= sp
    mr = runs(mono)
    speech_s = sp[first:last].sum() / 100
    pl = [(e - s) / 100 for s, e in pauses]
    # artefacts
    clip = float((np.abs(a) > 0.985).mean())
    d = np.abs(np.diff(a))
    loc = np.convolve(d, np.ones(400) / 400, "same") + 1e-4
    clicks = int(((d > 0.25) & (d > 25 * loc)).sum())
    # drop-outs: a 20-60 ms hole in the middle of a voiced stretch
    drop = 0
    for s, e in runs(~sp[first:last]):
        if 2 <= e - s <= 6:
            a0, a1 = first + s - 3, first + e + 3
            if a0 > 0 and a1 < n and f0[a0] > 0 and f0[a1] > 0:
                drop += 1
    return dict(
        dur=round(len(a) / SR, 2), speech=round(speech_s, 2),
        f0_median=round(float(np.median(f0[voiced])), 1) if len(voiced) else 0,
        pitch_std_st=round(float(np.std(st)), 2),
        pitch_range_st=round(float(np.percentile(st, 95) - np.percentile(st, 5)), 2),
        mono_longest_s=round(max([(e - s) / 100 for s, e in mr], default=0), 2),
        mono_frac=round(float(mono.sum() / max(1, sp[first:last].sum())), 3),
        rate=round(float(np.median(rates)), 2) if rates else 0,
        rate_cv=round(float(np.std(rates) / np.mean(rates)), 3) if len(rates) >= 3 else None,
        pauses_per_min=round(len(pauses) / max(speech_s, 1) * 60, 1),
        pause_mean=round(float(np.mean(pl)), 3) if pl else 0,
        pause_cv=round(float(np.std(pl) / np.mean(pl)), 3) if len(pl) >= 4 else None,
        energy_std_db=round(float(np.std(plouds)), 2) if len(plouds) >= 3 else None,
        dyn_db=round(float(np.median(pdyn)), 2) if pdyn else 0,
        clip_frac=round(clip, 5), clicks=clicks, dropouts=drop,
        _st=st, _f0=f0, _db=db, _sp=sp, _pk=pk,
    )


def line_stats(a):
    """Short per-line numbers (used for weakest lines and mood contrast)."""
    r = analyse(a)
    if not r.get("speech"):
        return None
    f0 = r["_f0"]; v = f0[f0 > 0]
    sp = r["_sp"]; db = r["_db"]
    loud = 10 * np.log10(np.mean(10 ** (db[sp] / 10))) if sp.any() else -60
    nsyl = len(r["_pk"])
    return dict(dur=r["dur"], f0_med=float(np.median(v)) if len(v) else 0, pitch_std_st=r["pitch_std_st"],
                pitch_range_st=r["pitch_range_st"], mono_longest_s=r["mono_longest_s"], rate=round(nsyl / max(r["speech"], 0.3), 2),
                loud_db=round(float(loud), 2), pauses=len([1 for x in runs(~sp) if x[1] - x[0] >= 12]) - 0)


def contrast(ls):
    """Mood contrast between lines: spread of line pitch (st), pace (CV) and loudness (dB), combined into one score."""
    ls = [x for x in ls if x and x.get("f0_med", 0) > 0]
    if len(ls) < 4:
        return None, {}
    f = np.array([x["f0_med"] for x in ls]); st = 12 * np.log2(f / np.median(f))
    rate = np.array([x["rate"] for x in ls]); loud = np.array([x["loud_db"] for x in ls])
    rng = np.array([x["pitch_range_st"] for x in ls])
    parts = dict(line_pitch_sd_st=round(float(np.std(st)), 2), line_rate_cv=round(float(np.std(rate) / np.mean(rate)), 3),
                 line_loud_sd_db=round(float(np.std(loud)), 2), line_range_sd_st=round(float(np.std(rng)), 2))
    score = parts["line_pitch_sd_st"] / 0.9 + parts["line_rate_cv"] / 0.09 + parts["line_loud_sd_db"] / 1.5 + parts["line_range_sd_st"] / 2.0
    return round(score / 4, 2), parts


def judge(feat):
    """[(metric, value, 'FAIL'|'WARN')] for the overall features."""
    out = []
    for k, (fail, warn) in T.items():
        v = feat.get(k)
        if v is None:
            continue
        if k in LOWER_IS_WORSE:
            lvl = "FAIL" if v < fail else "WARN" if v < warn else None
        else:
            lvl = "FAIL" if v > fail else "WARN" if v > warn else None
        if lvl:
            out.append((k, v, lvl))
    if feat.get("speech", 0) > 8 and feat.get("pauses_per_min", 99) < 4:
        out.append(("pauses_per_min", feat["pauses_per_min"], "FAIL"))     # reads on without breathing: espeak-like
    if feat.get("clip_frac", 0) > 0.0005:
        out.append(("clip_frac", feat["clip_frac"], "FAIL"))
    if feat.get("clicks", 0) > 3:
        out.append(("clicks", feat["clicks"], "WARN"))
    for j in feat.get("joins", []):
        if j["loud_jump_db"] > 4 or j["pitch_jump_st"] > 7 or j["floor_jump_db"] > 10:   # a mood change may move pitch: only big jumps
            out.append((f"join {j['at']}", j, "WARN"))
    return out


def line_weakness(x):
    """0 (lively) .. higher = flatter, for ranking lines."""
    if not x:
        return 0
    w = max(0, 3.2 - x["pitch_std_st"]) / 3.2 + max(0, 10 - x["pitch_range_st"]) / 10 + min(x["mono_longest_s"], 4) / 4
    return round(w, 2)


def clean(d):
    return {k: v for k, v in d.items() if not k.startswith("_")}


def check_signal(a, line_segs=None, takes=None):
    """a: whole narration; line_segs: [(id, start_s, end_s, direction)]; takes: [start_s of each new request take]."""
    feat = analyse(a)
    if not line_segs:          # loose file: phrases between pauses >= 0.3 s stand in for script lines
        sp = feat["_sp"]; rr = runs(sp); cur = None; line_segs = []
        for s, e in rr:
            if cur and s - cur[1] < 30:
                cur = (cur[0], e)
            else:
                if cur: line_segs.append(cur)
                cur = (s, e)
        if cur: line_segs.append(cur)
        line_segs = [(f"p{i+1}", s / 100, e / 100, "") for i, (s, e) in enumerate(line_segs) if e - s >= 80]
    lines = []
    for lid, s0, s1, dr in (line_segs or []):
        seg = a[int(s0 * SR):int(s1 * SR)]
        x = line_stats(seg) if len(seg) > SR * 0.4 else None
        lines.append(dict(id=lid, direction=dr, **(x or {}), weak=line_weakness(x)))
    # "sounds the same as the line next to it" (no mood change): adds to the weakness of that line
    ok = [l for l in lines if l.get("f0_med")]
    if len(ok) >= 3:
        med = np.median([l["f0_med"] for l in ok])
        for i, l in enumerate(ok):
            d = []
            for m in (ok[i - 1] if i else None, ok[i + 1] if i + 1 < len(ok) else None):
                if m:
                    d.append(np.sqrt((12 * np.log2(l["f0_med"] / m["f0_med"])) ** 2 + ((l["rate"] - m["rate"]) / 0.4) ** 2
                                     + ((l["loud_db"] - m["loud_db"]) / 1.5) ** 2))
            l["same"] = round(float(max(0, 1 - min(d))), 2)
            l["weak"] = round(l["weak"] + l["same"], 2)
    c, parts = contrast(lines) if lines else (None, {})
    feat["contrast"] = c
    feat.update(parts)
    joins = []
    for t in (takes or [])[1:]:
        k = int(t * 100); db = feat["_db"]; f0 = feat["_f0"]; sp = feat["_sp"]
        pre, post = slice(max(0, k - 150), k), slice(k, k + 150)
        def lvl(sl): s = db[sl][sp[sl]]; return 10 * np.log10(np.mean(10 ** (s / 10))) if len(s) else -60
        def flo(sl): s = db[sl][(~sp[sl]) & (db[sl] > -150)]; return float(np.median(s)) if len(s) else None   # not the digital-zero gaps
        def pit(sl): v = f0[sl][f0[sl] > 0]; return float(np.median(v)) if len(v) else 0
        p1, p2 = pit(pre), pit(post)
        joins.append(dict(at=round(t, 2), loud_jump_db=round(float(abs(lvl(pre) - lvl(post))), 2),
                          floor_jump_db=round(abs(flo(pre) - flo(post)), 2) if flo(pre) is not None and flo(post) is not None else 0,
                          pitch_jump_st=round(float(abs(12 * np.log2(p2 / p1))), 2) if p1 and p2 else 0))
    feat["joins"] = joins
    issues = judge(feat)
    fails = [i for i in issues if i[2] == "FAIL"]
    weakest = sorted([l for l in lines if l.get("weak")], key=lambda l: -l["weak"])[:3]
    return dict(verdict="FAIL" if fails else "PASS", issues=[[i[0], i[1], i[2]] for i in issues],
                overall=clean(feat), lines=lines, weakest=[w["id"] for w in weakest if w["weak"] >= 0.5])


def episode_audio(ep):
    """Narration of an episode as one signal + line segments + take starts.
    Prefers audio/lines/<id>.wav (what the mix uses); falls back to the voice/ FLAC masters split by timing.json durations."""
    ep = Path(ep)
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
    from voice import parse_lines
    lines = parse_lines(ep / "lines.txt")
    timing = {t["id"]: t for t in json.loads((ep / "timing.json").read_text())} if (ep / "timing.json").exists() else {}
    dj = json.loads((ep / "direction.json").read_text()) if (ep / "direction.json").exists() else {}
    dirs = dj.get("lines", {})
    gap = np.zeros(int(0.35 * SR), np.float32)
    parts, segs, takes, t = [], [], [], 0.0
    if all((ep / f"audio/lines/{l['id']}.wav").exists() for l in lines):
        tk = json.loads((ep / "audio/takes.json").read_text()) if (ep / "audio/takes.json").exists() else {}
        last_take = None
        for l in lines:
            x = load(ep / f"audio/lines/{l['id']}.wav")
            if tk.get(l["id"]) != last_take:
                takes.append(t); last_take = tk.get(l["id"])
            segs.append((l["id"], t, t + len(x) / SR, dirs.get(l["id"], ""))); parts += [x, gap]; t += (len(x) + len(gap)) / SR
        return np.concatenate(parts), segs, takes if tk else []
    for ch in sorted({l["chapter"] for l in lines}):
        fl = ep / f"voice/ch{ch}.flac"
        if not fl.exists():
            continue
        x = load(fl)
        L = [l for l in lines if l["chapter"] == ch]
        db = f0_track(x)[2]; rr = runs(speech_mask(db))
        p = rr[0][0] / 100 - 0.08 if rr else 0
        for l in L:
            d = timing.get(l["id"], {}).get("dur", 0)
            if d:
                segs.append((l["id"], t + max(0, p), t + p + d, dirs.get(l["id"], ""))); p += d
        parts += [x, gap]; t += (len(x) + len(gap)) / SR
    if not parts:
        raise SystemExit(f"no narration audio found in {ep} (audio/lines/*.wav or voice/ch*.flac)")
    return np.concatenate(parts), segs, []


def report(name, res, quiet=False):
    o = res["overall"]
    if not quiet:
        print(f"== {name}")
        print(f"   pitch std {o.get('pitch_std_st')} st, range {o.get('pitch_range_st')} st | monotone longest {o.get('mono_longest_s')} s "
              f"({o.get('mono_frac')}) | pace {o.get('rate')} syl/s cv {o.get('rate_cv')} | pauses {o.get('pauses_per_min')}/min "
              f"cv {o.get('pause_cv')} | energy sd {o.get('energy_std_db')} dB | mood contrast {o.get('contrast')}")
        for l in res["lines"]:
            if "f0_med" in l:
                print(f"   {l['id']:>5} weak {l['weak']:.2f} same {l.get('same', 0):.2f} | pitch sd {l['pitch_std_st']:.1f} range {l['pitch_range_st']:.1f} st"
                      f" | {l['rate']:.1f} syl/s | {l['loud_db']:.1f} dB | {l['direction'][:40]}")
        for i in res["issues"]:
            print("  ", i[2], i[0], i[1])
    print(f"{res['verdict']} {name}" + (f"  weakest lines: {', '.join(res['weakest'])}" if res["weakest"] else ""))


def main(args):
    quiet = "--quiet" in args
    args = [a for a in args if a != "--quiet"]
    bad = 0
    for p in args:
        p = Path(p)
        if p.is_dir():
            a, segs, takes = episode_audio(p)
            res = check_signal(a, segs, takes)
            (p / "voice_check.json").write_text(json.dumps(res, indent=1, default=float))
        else:
            res = check_signal(load(p))
        report(str(p), res, quiet)
        bad += res["verdict"] == "FAIL"
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
