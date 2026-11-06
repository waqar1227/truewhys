"""Gemini TTS narration, one request per chapter (free tier: 10 requests/day/model).
python lib/voice_gemini.py episodes/<ep> [chapters e.g. 0,1,2 | shorts]
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


def prompt_for(chapter, says):
    return ("# AUDIO PROFILE: The Narrator\nA warm, charismatic male storyteller for a hit animated history channel.\n\n"
            "## THE SCENE\nA cosy studio. He is telling a true, astonishing story to a friend, half amazed himself.\n\n"
            "### DIRECTOR'S NOTES\n"
            f"Style: gripping, vivid and warm. {DIRECTION.get(chapter, '')}\n"
            "Pace: lively and natural, about 165 words per minute, with brief dramatic pauses at the ellipses and a short pause between sentences.\n"
            "Accent: neutral American.\n\n#### TRANSCRIPT\n" + "\n".join(says))


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


def main(ep, chapters):
    ep = Path(ep)
    lines = parse_lines(ep / "lines.txt")
    from faster_whisper import WhisperModel
    wm = WhisperModel("small.en", device="cpu", compute_type="int8")
    tpath = ep / "timing.json"
    timing = {t["id"]: t for t in json.loads(tpath.read_text())} if tpath.exists() else {}
    (ep / "audio/chapters").mkdir(parents=True, exist_ok=True)
    (ep / "audio/lines").mkdir(parents=True, exist_ok=True)
    report = []
    for ch in chapters:
        L = [l for l in lines if l["chapter"] == ch]
        cw = ep / f"audio/chapters/ch{ch}.wav"
        if not cw.exists():
            try:
                tts(prompt_for(ch, [l["say"] for l in L]), cw)
            except urllib.error.HTTPError as e:
                print("HTTP", e.code, e.read()[:300]); break
        a, sr = sf.read(cw, dtype="float32")
        segs, _ = wm.transcribe(str(cw), word_timestamps=True, language="en", initial_prompt=" ".join(l["text"] for l in L))
        ww = [dict(w=w.word.strip(), s=w.start, e=w.end) for s in segs for w in (s.words or [])]
        # align all caption words of the chapter to whisper words
        cap_words, owner = [], []
        for i, l in enumerate(L):
            for w in l["text"].split():
                cap_words.append(w); owner.append(i)
        al = align(" ".join(cap_words), ww, len(a) / sr)
        # line boundaries: cut in the middle of the gap between lines
        firsts = [next(k for k, o in enumerate(owner) if o == i) for i in range(len(L))]
        lasts = [max(k for k, o in enumerate(owner) if o == i) for i in range(len(L))]
        cuts = [0.0]
        for i in range(len(L) - 1):
            cuts.append((al[lasts[i]]["e"] + al[firsts[i + 1]]["s"]) / 2)
        cuts.append(len(a) / sr)
        heard_all = " ".join(w["w"] for w in ww)
        for i, l in enumerate(L):
            s0, s1 = cuts[i], cuts[i + 1]
            # trim to speech with small pads
            w0, w1 = al[firsts[i]]["s"], al[lasts[i]]["e"]
            s0 = max(s0, w0 - 0.08); s1 = min(s1, w1 + 0.18)
            seg = a[int(s0 * sr):int(s1 * sr)]
            sf.write(ep / f"audio/lines/{l['id']}.wav", seg, sr)
            words = [dict(w=al[k]["w"], s=round(al[k]["s"] - s0, 3), e=round(al[k]["e"] - s0, 3)) for k in range(firsts[i], lasts[i] + 1)]
            heard = " ".join(w["w"] for w in ww if s0 <= w["s"] < s1)
            r = difflib.SequenceMatcher(a=[norm(x) for x in l["text"].split()], b=[norm(x) for x in heard.split()]).ratio()
            timing[l["id"]] = dict(id=l["id"], chapter=ch, text=l["text"], dur=round(len(seg) / sr, 3), words=words, heard=heard, match=round(r, 3))
            if r < 0.8:
                report.append((l["id"], r, l["text"], heard))
        print(f"chapter {ch}: {len(a)/sr:.1f}s, {len(L)} lines", flush=True)
        time.sleep(2)
    tpath.write_text(json.dumps([timing[l["id"]] for l in lines if l["id"] in timing], indent=1))
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
    if not cw.exists():
        txt = ("# AUDIO PROFILE: The Narrator\nA warm, charismatic male storyteller for a hit animated history channel.\n\n"
               "## THE SCENE\nHe is recording the opening lines of short videos: each line must grab a scrolling viewer instantly.\n\n"
               "### DIRECTOR'S NOTES\nStyle: punchy, intriguing, amazed, a little playful; each line is its own separate take with a full one-second pause between lines. "
               "The last line is a friendly, upbeat sign-off.\nPace: lively, about 170 words per minute, short dramatic pause at each ellipsis.\n"
               "Accent: neutral American.\n\n#### TRANSCRIPT\n" + "\n".join(l["say"] for l in L))
        tts(txt, cw)
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
    chs = [int(c) for c in sys.argv[2].split(",")] if len(sys.argv) > 2 else list(range(8))
    main(sys.argv[1], chs)
