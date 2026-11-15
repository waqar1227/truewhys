"""Apply the audit's metadata fixes (docs/audit/metadata_fixes.json) to live videos.
python tools/yt_apply_fixes.py            -> dry run: prints what would change (1 quota unit per 50 videos)
python tools/yt_apply_fixes.py --apply    -> videos.update (~50 units each), before/after saved to docs/audit/applied.json
Rules (audit §5): only fixes whose `apply` time has passed; title only if the script supports it (OVERRIDE below);
tags replaced; description keeps its text, every hashtag is removed, then the subscribe line + exactly 3 hashtags are added.
Never sends the altered/synthetic field. Skips videos waiting for an owner decision (HOLD)."""
import sys, json, re, datetime as dt
from pathlib import Path
sys.path.insert(0, "lib")
from youtube import token, api

FIX = json.loads(Path("docs/audit/metadata_fixes.json").read_text())["fixes"]
OUT = Path("docs/audit/applied.json")
SUB = "More true whys: https://www.youtube.com/@truewhys?sub_confirmation=1"
# script check 15 Nov: the script never says the ale conner was hated (it says saltpetre men were) -> keep the old title without #Shorts
OVERRIDE = {"TkNJsIdy7gs": "The Medieval Job Where You Drank Ale for Work"}
HOLD = {"RI7u-NzEj5E": "owner decision D4 (religion rule review)"}
TAG = re.compile(r"(?<![\w/#])#[A-Za-z][\w]*")  # hashtags only; '#8' chapter markers and URL fragments are left alone


def due(a):
    if a == "now":
        return True
    t = dt.datetime.fromisoformat(a.replace("after ", "").replace("Z", "+00:00"))
    return dt.datetime.now(dt.timezone.utc) >= t


def new_desc(d, tags):
    d = TAG.sub("", d)
    d = d.replace(SUB, "")
    lines = [l.rstrip() for l in d.splitlines()]
    d = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    return f"{d}\n\n{SUB}\n\n{' '.join(tags)}"


def main(apply):
    tok, _ = token()
    todo = [f for f in FIX if due(f["apply"]) and f["id"] not in HOLD]
    done = json.loads(OUT.read_text()) if OUT.exists() else {}
    for i in range(0, len(todo), 50):
        ids = ",".join(f["id"] for f in todo[i:i + 50])
        _, _, b = api("GET", f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={ids}", tok)
        cur = {v["id"]: v["snippet"] for v in json.loads(b)["items"]}
        for f in todo[i:i + 50]:
            s = cur[f["id"]]
            title = OVERRIDE.get(f["id"]) or f["new_title"] or s["title"]
            title = re.sub(r"\s*#Shorts\b", "", title).strip()
            body = {k: s[k] for k in ("title", "description", "tags", "categoryId", "defaultLanguage", "defaultAudioLanguage") if k in s}
            body.update(title=title, tags=f["tags"], description=new_desc(s["description"], f["hashtags"]))
            ch = [k for k in ("title", "tags", "description") if body.get(k) != s.get(k)]
            print(f["id"], f["episode"], f["kind"], "changes:", ch, "|", s["title"][:45], "->", title[:45])
            if apply and ch:
                api("PUT", "https://www.googleapis.com/youtube/v3/videos?part=snippet", tok, {"id": f["id"], "snippet": body})
                done[f["id"]] = {"at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                                 "before": {k: s.get(k) for k in ch}, "after": {k: body[k] for k in ch}}
                OUT.write_text(json.dumps(done, indent=1, ensure_ascii=False))
    skipped = [(f["id"], f["apply"]) for f in FIX if not due(f["apply"])] + [(k, v) for k, v in HOLD.items()]
    print("not yet / held:", skipped)


if __name__ == "__main__":
    main("--apply" in sys.argv)
