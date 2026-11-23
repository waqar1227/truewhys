"""English SRT captions for a long video from its own timeline (shots.json line_start + timing.json word times + lines.txt text).
python tools/make_srt.py <episode dir>                 -> writes <ep>/final/captions_en.srt
python tools/make_srt.py <episode dir> --upload <id>   -> also captions.insert (language en, name "English"; ~400 quota units)"""
import sys, json, re, uuid
from pathlib import Path

MAXC, MAXW = 42, 8


def ts(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build(ep):
    ep = Path(ep)
    plan = json.loads((ep / "shots.json").read_text())
    T = {L["id"]: L for L in json.loads((ep / "timing.json").read_text())}
    starts = {}
    for sh in plan["shots"]:
        if sh.get("line") and "line_start" in sh:
            starts.setdefault(sh["line"], sh["line_start"])
        elif sh.get("line") and isinstance(sh.get("words"), dict) and sh["words"] and sh["line"] in T:
            # Style R / flat2d plans (23 Nov): words = {word: time relative to shot start}; earliest = the line's first word
            starts.setdefault(sh["line"], sh["start"] + min(sh["words"].values()) - T[sh["line"]]["words"][0]["s"])
    cues = []
    for lid, t0 in sorted(starts.items(), key=lambda kv: kv[1]):
        L = T[lid]; words = L["words"]; text = L["text"].split()
        if len(words) != len(text):            # caption text wins; spread its words over the spoken span
            a, b = words[0]["s"], words[-1]["e"]
            words = [{"w": w, "s": a + (b - a) * i / len(text), "e": a + (b - a) * (i + 1) / len(text)} for i, w in enumerate(text)]
        else:
            words = [dict(w, w=text[i]) for i, w in enumerate(words)]
        cur = []
        for i, w in enumerate(words):
            cur.append(w)
            line = " ".join(x["w"] for x in cur)
            last = i == len(words) - 1
            nxt = "" if last else " " + words[i + 1]["w"]
            if last or len(cur) >= MAXW or len(line + nxt) > MAXC or (re.search(r"[.?!]$", w["w"]) and len(cur) >= 3):
                s = t0 + cur[0]["s"]; e = t0 + max(cur[-1]["e"], cur[-1]["s"] + 0.3)
                if last:
                    e = max(e, t0 + L["dur"])
                cues.append([s, e, line]); cur = []
    for a, b in zip(cues, cues[1:]):          # no overlaps, short gaps closed
        a[1] = min(max(a[1], a[0] + 0.7), b[0]) if b[0] - a[1] < 0.6 else min(a[1], b[0])
    srt = "\n".join(f"{i}\n{ts(s)} --> {ts(e)}\n{t}\n" for i, (s, e, t) in enumerate(cues, 1))
    out = ep / "final/captions_en.srt"; out.parent.mkdir(exist_ok=True); out.write_text(srt)
    print(out, len(cues), "cues, last ends", ts(cues[-1][1]), "| plan duration", plan.get("duration"))
    return out


def upload(path, vid):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
    from youtube import token, api
    tok, _ = token()
    _, _, b = api("GET", f"https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={vid}", tok)
    for c in json.loads(b)["items"]:
        if c["snippet"].get("trackKind") == "standard" and c["snippet"]["language"].startswith("en") and c["snippet"].get("name") == "English":
            print("English track already there:", c["id"]); return
    bd = uuid.uuid4().hex
    meta = json.dumps({"snippet": {"videoId": vid, "language": "en", "name": "English", "isDraft": False}})
    body = (f"--{bd}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{meta}\r\n--{bd}\r\nContent-Type: application/octet-stream\r\n\r\n"
            ).encode() + Path(path).read_bytes() + f"\r\n--{bd}--\r\n".encode()
    st, _, r = api("POST", "https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet", tok,
                   raw=body, ctype=f"multipart/related; boundary={bd}")
    print("uploaded caption", st, json.loads(r)["id"])


if __name__ == "__main__":
    p = build(sys.argv[1])
    if "--upload" in sys.argv:
        upload(p, sys.argv[sys.argv.index("--upload") + 1])
