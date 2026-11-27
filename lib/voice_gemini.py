"""Gemini TTS narration (free tier: 10 requests/day/model, shared by all sessions: every request is logged in
research/gemini_tts_log.jsonl and the script stops at TW_GEMINI_DAY_CAP=9 for the day).
python lib/voice_gemini.py episodes/<ep> [chapters e.g. 0,1,2 | shorts]
HUMAN, EMOTIONAL VOICE (owner 27 Nov 2026): direction.json can give every line its own mood
  {"voice": "Charon", "0": "chapter note", "lines": {"H1": "hushed, curious", "L03": "excited, smiling", "L05": "sad, slower"}}
  default split "take": the whole chapter in ONE request, moods given as one mood arc in the notes (1 request; tested 27 Nov:
  flatter, the model tends to perform the arc in an ad-lib it adds; the splitter drops the ad-lib, voice_human_check judges it);
  "split": "scenes" (+ "max_takes": 3 or explicit "scenes": [[ids], ...]): consecutive lines with one mood = one request,
  takes are loudness-matched and cut in the pauses so the joins are invisible. Then run tools/voice_human_check.py <ep>.
The API key is injected by the network proxy (header x-goog-api-key) or read from GEMINI_API_KEY.
Each chapter is read in one take (natural flow), then split into lines with faster-whisper word
timestamps aligned to the script, and checked: any line whose words don't match is reported.
Writes audio/lines/<id>.wav (24 kHz) and timing.json (same format as lib/voice.py).
"""
import sys, os, json, base64, re, difflib, urllib.request, urllib.error, time
from pathlib import Path
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voice import parse_lines, norm, align

MODEL = os.environ.get("TW_GEMINI_MODEL", "gemini-3.8-flash-tts")
VOICE = os.environ.get("TW_GEMINI_VOICE", "Charon")
DIRECTION = {
    0: "Start hushed and suspenseful, slow down slightly before reveals, sound amused and playful on 'was a pig', genuinely curious on the questions, friendly and upbeat on the last line.",
    1: "Story mode: vivid and serious about the sad facts (gentle, never comic about the child), dry humour on the gloves, surprised on 'Falaise wasn't unusual at all'.",
    2: "Clear explainer tone, building intrigue towards 'a fair trial needs a lawyer', with a little smile on that line.",
    3: "Playful and amused: this lawyer is clever. Theatrical on the excuses, comic suspense on 'full of cats', warm and thoughtful on the last two sentences.",
    4: "Darker and more serious. Eerie on the basilisk legend, calm and reassuring on the science line.",
    5: "Light, witty, delighted by the absurdity. Comic timing on 'turned the offer down' and a slow mysterious delivery on the last line.",
    6: "Thoughtful and clear, like revealing the answer to a mystery; slightly conspiratorial on 'Here's the trick'.",
    7: "Warm wrap-up; a playful joke on the homework line; friendly, upbeat sign-off.",
}



def master(cw):
    """Gemini takes are kept in git as FLAC (episodes/<ep>/voice/), so a fresh session never re-spends the daily quota."""
    import subprocess
    fl = cw.parent.parent.parent / "voice" / (cw.stem + ".flac")
    if not cw.exists() and fl.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(fl), str(cw)], check=True)
    elif cw.exists() and not fl.exists():
        fl.parent.mkdir(exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(cw), "-compression_level", "8", str(fl)], check=True)

def _silence(a, sr, lo, hi, thr=0.035):
    """Longest quiet stretch (start, end) in seconds between lo and hi, or None if there is no real pause."""
    hop = int(0.01 * sr)
    i0, i1 = max(0, int(lo * sr)), min(len(a), int(hi * sr))
    n = (i1 - i0) // hop
    if n < 8:
        return None
    rms = np.sqrt((a[i0:i0 + n * hop].reshape(n, hop) ** 2).mean(1))
    quiet = rms < thr * (np.percentile(np.abs(a), 99) or 1.0)
    best, cur = None, None
    for k in range(n + 1):
        if k < n and quiet[k]:
            cur = (cur[0], k + 1) if cur else (k, k + 1)
        else:
            if cur and (best is None or cur[1] - cur[0] > best[1] - best[0]):
                best = cur
            cur = None
    if not best or (best[1] - best[0]) < 10:
        return None
    return (i0 / sr + best[0] * 0.01, i0 / sr + best[1] * 0.01)


NATURAL = ("# AUDIO PROFILE: The Narrator\nA real person, not an announcer: a curious, warm person telling a friend something "
           "surprising he just found out.\n\n## THE SCENE\nSitting across a kitchen table from ONE friend, talking quietly and naturally, "
           "half amazed himself. No microphone voice, no radio or trailer tone, no sing-song.\n\n### DIRECTOR'S NOTES\n"
           "Style: conversational and genuine, like a real chat. Small natural pauses where a person would think or let something land; "
           "vary the pace (quicker on the easy bits, slower on the surprising facts); a little smile in the voice on the funny parts. "
           "Never over-act, never shout, never stretch words.{note}\n"
           "Pace: natural, about 160 words per minute on average.\nAccent: neutral American.\n\n#### TRANSCRIPT\n")


def prompt_for(chapter, says):
    """REAL SOUND RULE (27 Nov 2026): natural conversational read for all new narration (talk to one friend)."""
    note = DIRECTION.get(chapter, "")
    return NATURAL.format(note=(" " + note) if note else "") + "\n".join(says)


def tts(text, out):
    body = {"contents": [{"parts": [{"text": text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}}}}
    hdr = {"Content-Type": "application/json"}
    if os.environ.get("GEMINI_API_KEY"):
        hdr["x-goog-api-key"] = os.environ["GEMINI_API_KEY"]
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
                                 data=json.dumps(body).encode(), headers=hdr)
    d = json.load(urllib.request.urlopen(req, timeout=300))
    raw = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
    if raw[:4] == b"RIFF":
        Path(out).write_bytes(raw)
    else:
        sf.write(out, np.frombuffer(raw, np.int16).astype(np.float32) / 32768, 24000)


EMO = ("# AUDIO PROFILE: The Narrator\nA real person, not an announcer: a curious, warm person telling ONE friend a true story "
       "he just found out, and he feels it as he tells it.\n\n## THE SCENE\nSitting across a kitchen table from a friend, talking "
       "naturally. No microphone voice, no radio or trailer tone, no sing-song, no even 'reading' rhythm.\n\n### DIRECTOR'S NOTES\n"
       "Emotion: every line has its own mood (below). Act that mood with the whole voice: pitch, pace, "
       "loudness and breath. Happy lines smile, excited lines speed up and lift, sad lines drop and slow down, tense lines get quieter "
       "and tighter, whispered lines are breathy and close, surprised lines jump. Let the mood change clearly from one line to the "
       "next, like a real person reacting to their own story. Natural breaths and pauses where a person would think or let something "
       "land; vary the pace.{note}\n"
       "Pace: natural and varied, about 160 words per minute on average.\nAccent: neutral American.\n{context}\n"
       "{moods}\nSpeak ONLY the transcript below, word for word, nothing else.\n\n#### TRANSCRIPT\n")
LOG = Path(__file__).resolve().parent.parent / "research/gemini_tts_log.jsonl"
DAY_CAP = int(os.environ.get("TW_GEMINI_DAY_CAP", "9"))      # free tier 10/day/model, shared by ALL sessions: keep one spare


def used_today():
    """Requests logged today (UTC day starting at the 08:00 reset is close enough: count the calendar day). Pull first: other sessions log too."""
    if not LOG.exists():
        return 0
    day = time.strftime("%Y-%m-%d", time.gmtime())
    return sum(1 for r in LOG.read_text().splitlines() if r.strip() and json.loads(r).get("day") == day and json.loads(r).get("model") == MODEL)


def log_request(ep, take, chars, ok):
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps(dict(day=time.strftime("%Y-%m-%d", time.gmtime()), t=time.strftime("%H:%M", time.gmtime()), model=MODEL,
                                voice=VOICE, ep=Path(ep).name, take=take, chars=chars, ok=ok)) + "\n")


def load_direction(ep):
    """direction.json: {"voice": "Charon", "0": "chapter note", "lines": {"H1": "hushed, curious", ...},
    "split": "take" | "scenes", "max_takes": 3, "scenes": [["H1", "L01"], ...]}. Old files (chapter notes only) work as before."""
    global VOICE
    dj = json.loads((ep / "direction.json").read_text()) if (ep / "direction.json").exists() else {}
    VOICE = os.environ.get("TW_GEMINI_VOICE") or dj.get("voice", VOICE)   # per-video voice (owner 27 Nov 2026)
    DIRECTION.update({int(k): v for k, v in dj.items() if k.isdigit()})
    return dj


def plan_takes(L, dj):
    """Split one chapter's lines into takes (one request each).
    - no per-line moods: one take, old prompt (keeps the existing masters valid)
    - split "take" (default): ONE take, every line carries its own [mood] tag: one request, one-take naturalness
    - split "scenes": consecutive lines with the same mood (or the explicit "scenes" lists) form a scene; neighbouring scenes are
      merged until there are at most max_takes (default 3) so the daily quota holds."""
    moods = dj.get("lines", {})
    if not moods:
        return [L]
    if dj.get("split", "take") != "scenes":
        return [L]
    ids = [l["id"] for l in L]
    if dj.get("scenes"):
        where = {lid: k for k, sc in enumerate(dj["scenes"]) for lid in sc}
        key = [where.get(i, -1) for i in ids]
    else:
        key = [moods.get(i, "") for i in ids]
    groups = []
    for l, k in zip(L, key):
        if groups and groups[-1][0] == k:
            groups[-1][1].append(l)
        else:
            groups.append([k, [l]])
    groups = [g[1] for g in groups]
    mx = max(1, int(dj.get("max_takes", 3)))
    while len(groups) > mx:                       # merge the smallest neighbouring pair (keeps big mood changes as real cuts)
        k = min(range(len(groups) - 1), key=lambda i: len(groups[i]) + len(groups[i + 1]))
        groups[k:k + 2] = [groups[k] + groups[k + 1]]
    return groups


def take_prompt(ch, T, dj, prev=None, nxt=None):
    moods = dj.get("lines", {})
    note = DIRECTION.get(ch, "")
    if not moods:
        return prompt_for(ch, [l["say"] for l in T])
    # 27 Nov 2026 tests: the model READS ALOUD long [descriptions] put in the transcript, and it ad-libs when the notes quote
    # script words. So: moods go in the notes as one plain "mood arc" (no quotes, no numbers), the transcript stays clean
    # (short audio tags typed in lines.txt pass through), and a scene take only says where it sits in the story.
    ms = [moods.get(l["id"], "") for l in T]
    uniq = [m for i, m in enumerate(ms) if m and m not in ms[:i]]
    ml = ("Mood: " + uniq[0] + "." if len(uniq) == 1 else
          "Mood arc, in the order of the transcript: " + "; then ".join(uniq) + "." if uniq else "Mood: natural, follow the story.")
    ctx = ""
    if prev or nxt:
        ctx = ("This is one scene of a longer story" + (", in the middle" if prev and nxt else ", the opening" if nxt else ", the ending")
               + ". Speak only the transcript.\n")
    body = "\n".join(l["say"] for l in T)
    return EMO.format(note=(" " + note) if note else "", context=ctx, moods=ml) + body


def take_name(ch, T, prompt, dj):
    import hashlib
    if not dj.get("lines"):
        return f"ch{ch}"                               # old chapter take (masters already in git)
    return f"ch{ch}_{T[0]['id']}_{hashlib.sha1((VOICE + prompt).encode()).hexdigest()[:6]}"


def speech_level(a, sr):
    hop = int(0.01 * sr); n = len(a) // hop
    if n < 10:
        return None
    db = 20 * np.log10(np.sqrt((a[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    act = db[db > np.percentile(db, 95) - 25]
    return float(10 * np.log10(np.mean(10 ** (act / 10))))


def split_take(cw, L, ch, wm, ep, timing, report):
    """Whisper-align one take to its script lines and cut it at the real pauses into audio/lines/<id>.wav."""
    a, sr = sf.read(cw, dtype="float32")
    if a.ndim > 1:
        a = a.mean(1)
    prompt = None if os.environ.get("TW_WHISPER_NOPROMPT") else " ".join(l["text"] for l in L)   # set it when the prompt derails whisper
    segs, _ = wm.transcribe(str(cw), word_timestamps=True, language="en", initial_prompt=prompt)
    ww = [dict(w=w.word.strip(), s=w.start, e=w.end) for s in segs for w in (s.words or [])]
    if len(ww) < 0.6 * sum(len(l["text"].split()) for l in L):      # whisper sometimes derails on the prompt: retry plain
        segs, _ = wm.transcribe(str(cw), word_timestamps=True, language="en")
        ww = [dict(w=w.word.strip(), s=w.start, e=w.end) for s in segs for w in (s.words or [])]
    cap_words, owner = [], []
    for i, l in enumerate(L):
        for w in l["text"].split():
            cap_words.append(w); owner.append(i)
    al = align(" ".join(cap_words), ww, len(a) / sr)
    # line boundaries: cut inside the real pause between lines (found by loudness), not at whisper's word times:
    # whisper sometimes swallows the first word of a line (zero length), which used to cut that word off.
    firsts = [next(k for k, o in enumerate(owner) if o == i) for i in range(len(L))]
    lasts = [max(k for k, o in enumerate(owner) if o == i) for i in range(len(L))]
    bounds = []
    for i in range(len(L) - 1):
        f = firsts[i + 1]
        zero = f < lasts[i + 1] and al[f + 1]["s"] - al[f]["s"] < 0.03
        sil = _silence(a, sr, al[lasts[i]]["e"] - 0.05, (al[f + 1]["s"] if zero else al[f]["s"]) + 0.05)
        if sil:
            e_i, s_n = min(sil[1], sil[0] + 0.18), max(sil[0], sil[1] - 0.08)
            if zero:
                al[f]["s"], al[f]["e"] = round(s_n + 0.08, 3), al[f + 1]["s"]
        else:
            mid = (al[lasts[i]]["e"] + al[f]["s"]) / 2
            e_i, s_n = min(mid, al[lasts[i]]["e"] + 0.18), max(mid, al[f]["s"] - 0.08)
        bounds.append((e_i, s_n))
    cnorm = {norm(w) for l in L for w in l["text"].split()}
    out = {}
    for i, l in enumerate(L):
        s0 = max(0.0, al[firsts[0]]["s"] - 0.08) if i == 0 else bounds[i - 1][1]
        s1 = min(len(a) / sr, al[lasts[-1]]["e"] + 0.18) if i == len(L) - 1 else bounds[i][0]
        seg = a[int(s0 * sr):int(s1 * sr)].copy()
        out[l["id"]] = seg
        words = [dict(w=al[k]["w"], s=round(al[k]["s"] - s0, 3), e=round(al[k]["e"] - s0, 3)) for k in range(firsts[i], lasts[i] + 1)]
        heard = " ".join(w["w"] for w in ww if s0 <= w["s"] < s1)
        r = difflib.SequenceMatcher(a=[norm(x) for x in l["text"].split()], b=[norm(x) for x in heard.split()]).ratio()
        timing[l["id"]] = dict(id=l["id"], chapter=ch, text=l["text"], dur=round(len(seg) / sr, 3), words=words, heard=heard, match=round(r, 3))
        if r < 0.8:
            report.append((l["id"], r, l["text"], heard))
    extra = [norm(w["w"]) for w in ww if norm(w["w"]) and norm(w["w"]) not in cnorm]
    return out, sr, len(a) / sr, extra


def main(ep, chapters):
    ep = Path(ep)
    dj = load_direction(ep)
    print("voice:", VOICE, "| per-line moods:", len(dj.get("lines", {})), "| split:", dj.get("split", "take"), flush=True)
    lines = parse_lines(ep / "lines.txt")
    from faster_whisper import WhisperModel
    wm = WhisperModel("small.en", device="cpu", compute_type="int8")
    tpath = ep / "timing.json"
    timing = {t["id"]: t for t in json.loads(tpath.read_text())} if tpath.exists() else {}
    (ep / "audio/chapters").mkdir(parents=True, exist_ok=True)
    (ep / "audio/lines").mkdir(parents=True, exist_ok=True)
    tjson = ep / "audio/takes.json"
    takemap = json.loads(tjson.read_text()) if tjson.exists() else {}
    report, stop = [], False
    for ch in chapters:
        L = [l for l in lines if l["chapter"] == ch]
        takes = plan_takes(L, dj)
        cut, lv = {}, {}
        for k, T in enumerate(takes):
            prev = takes[k - 1][-1]["say"] if k else None
            nxt = takes[k + 1][0]["say"] if k + 1 < len(takes) else None
            pr = take_prompt(ch, T, dj, prev, nxt)
            name = take_name(ch, T, pr, dj)
            cw = ep / f"audio/chapters/{name}.wav"
            master(cw)
            if not cw.exists():
                if used_today() >= DAY_CAP and not os.environ.get("TW_GEMINI_FORCE"):
                    print(f"STOP: {used_today()} Gemini TTS requests logged today (cap {DAY_CAP}, shared by all sessions). "
                          "Run again after the reset.", flush=True)
                    stop = True; break
                try:
                    tts(pr, cw); log_request(ep, name, len(pr), True)
                except urllib.error.HTTPError as e:
                    log_request(ep, name, len(pr), False)
                    print("HTTP", e.code, e.read()[:300]); stop = True; break
                master(cw)
            segs, sr, dur, extra = split_take(cw, T, ch, wm, ep, timing, report)
            if dj.get("lines") and len(extra) > 2:
                print(f"CHECK take {name}: words heard that are not in the script (a [mood] tag read aloud?): {' '.join(extra[:12])}")
            for lid, seg in segs.items():
                cut[lid] = seg; takemap[lid] = name
            lv[name] = speech_level(np.concatenate(list(segs.values())), sr)
            print(f"chapter {ch} take {name}: {dur:.1f}s, {len(T)} lines", flush=True)
            time.sleep(1)
        if stop:
            break
        # several takes in one chapter: match their loudness so the joins are invisible (mood stays in the dynamics INSIDE a take)
        ref = float(np.median([v for v in lv.values() if v is not None])) if len(lv) > 1 else None
        for lid, seg in cut.items():
            g = 10 ** ((ref - lv[takemap[lid]]) / 20) if ref is not None and lv[takemap[lid]] is not None else 1.0
            seg = seg * g
            f = min(len(seg) // 4, int(0.012 * sr))          # 12 ms fades: no clicks at the cuts
            if f:
                seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
            sf.write(ep / f"audio/lines/{lid}.wav", seg, sr)
    tpath.write_text(json.dumps([timing[l["id"]] for l in lines if l["id"] in timing], indent=1))
    tjson.write_text(json.dumps(takemap, indent=1))
    for r in report:
        print("CHECK", r)


def shorts(ep):
    """All Short hooks + the outro in ONE request (saves free-tier quota), split with whisper like a chapter."""
    ep = Path(ep)
    cfg = json.loads((ep / "shorts.json").read_text())
    L = [dict(id=c["hook"]["id"], text=c["hook"]["text"], say=c["hook"].get("say", c["hook"]["text"])) for c in cfg["shorts"]]
    L.append(dict(id=cfg["outro"]["id"], text=cfg["outro"]["text"], say=cfg["outro"].get("say", cfg["outro"]["text"])))
    cw = ep / "audio/chapters/hooks.wav"
    cw.parent.mkdir(parents=True, exist_ok=True); (ep / "audio/lines").mkdir(parents=True, exist_ok=True)
    master(cw)
    if not cw.exists():
        txt = ("# AUDIO PROFILE: The Narrator\nA warm, charismatic male storyteller for a hit animated history channel.\n\n"
               "## THE SCENE\nHe is recording the opening lines of short videos: each line must grab a scrolling viewer instantly.\n\n"
               "### DIRECTOR'S NOTES\nStyle: punchy, intriguing, amazed, a little playful; each line is its own separate take with a full one-second pause between lines. "
               "The last line is a friendly, upbeat sign-off.\nPace: lively, about 170 words per minute, short dramatic pause at each ellipsis.\n"
               "Accent: neutral American.\n\n#### TRANSCRIPT\n" + "\n".join(l["say"] for l in L))
        tts(txt, cw)
    master(cw)
    from faster_whisper import WhisperModel
    wm = WhisperModel("small.en", device="cpu", compute_type="int8")
    a, sr = sf.read(cw, dtype="float32")
    segs, _ = wm.transcribe(str(cw), word_timestamps=True, language="en", initial_prompt=" ".join(l["text"] for l in L))
    ww = [dict(w=w.word.strip(), s=w.start, e=w.end) for sg in segs for w in (sg.words or [])]
    cap, owner = [], []
    for i, l in enumerate(L):
        for w in l["text"].split():
            cap.append(w); owner.append(i)
    al = align(" ".join(cap), ww, len(a) / sr)
    out = []
    for i, l in enumerate(L):
        ks = [k for k, o in enumerate(owner) if o == i]
        s0 = max(0, al[ks[0]]["s"] - 0.08); s1 = min(len(a) / sr, al[ks[-1]]["e"] + 0.2)
        seg = a[int(s0 * sr):int(s1 * sr)]
        sf.write(ep / f"audio/lines/{l['id']}.wav", seg, sr)
        heard = " ".join(w["w"] for w in ww if s0 <= w["s"] < s1)
        r = difflib.SequenceMatcher(a=[norm(x) for x in l["text"].split()], b=[norm(x) for x in heard.split()]).ratio()
        out.append(dict(id=l["id"], chapter=None, text=l["text"], dur=round(len(seg) / sr, 3),
                        words=[dict(w=al[k]["w"], s=round(al[k]["s"] - s0, 3), e=round(al[k]["e"] - s0, 3)) for k in ks], heard=heard, match=round(r, 3)))
        print(l["id"], round(len(seg) / sr, 2), "s match", round(r, 2), "" if r >= 0.8 else "CHECK: " + heard)
    (ep / "timing_hooks.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "shorts":
        shorts(sys.argv[1]); sys.exit()
    chs = [int(c) for c in sys.argv[2].split(",")] if len(sys.argv) > 2 else sorted({l["chapter"] for l in parse_lines(Path(sys.argv[1]) / "lines.txt")})
    main(sys.argv[1], chs)
