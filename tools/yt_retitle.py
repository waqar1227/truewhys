"""Change only the TITLE of live videos from a list (owner 22 Nov: fix old videos). Keeps description, tags, category.
python tools/yt_retitle.py docs/audit/retitles_2026-11-23.json            -> dry run (1 unit)
python tools/yt_retitle.py docs/audit/retitles_2026-11-23.json --apply    -> videos.update (~50 units each); writes "done" into the file
Each entry: {"id", "old", "new", "why"}. Skips entries already done or whose live title no longer matches "old"."""
import sys, json
from pathlib import Path
sys.path.insert(0, "lib")
from youtube import token, api

G = "https://www.googleapis.com/youtube/v3/"


def main(path, apply=False):
    p = Path(path); L = json.loads(p.read_text())
    todo = [e for e in L if not e.get("done")]
    if not todo:
        print("nothing to do"); return
    tok, _ = token()
    _, _, b = api("GET", G + "videos?part=snippet&id=" + ",".join(e["id"] for e in todo), tok)
    live = {v["id"]: v["snippet"] for v in json.loads(b)["items"]}
    for e in todo:
        sn = live.get(e["id"])
        if not sn:
            print("missing", e["id"]); continue
        if sn["title"].strip() != e["old"].strip():
            print("SKIP (title changed):", e["id"], repr(sn["title"])); continue
        print(("APPLY " if apply else "would ") + e["id"], repr(sn["title"]), "->", repr(e["new"]))
        if apply:
            body = {"id": e["id"], "snippet": {k: sn[k] for k in ("title", "description", "tags", "categoryId", "defaultLanguage") if k in sn}}
            body["snippet"]["title"] = e["new"]
            _, _, r = api("PUT", G + "videos?part=snippet", tok, body)
            e["done"] = json.loads(r)["snippet"]["title"] == e["new"]
            p.write_text(json.dumps(L, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], "--apply" in sys.argv)
