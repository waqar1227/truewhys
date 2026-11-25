"""Push the description + tags of an episode's upload_meta.json to its already-uploaded video (title and category kept from the meta).
python tools/yt_update_meta.py episodes/<ep>            -> dry run (1 quota unit): shows live vs new
python tools/yt_update_meta.py episodes/<ep> --apply    -> videos.update part=snippet (~50 units). Status/publishAt/AI field untouched."""
import sys, json
from pathlib import Path
sys.path.insert(0, "lib")
from youtube import token, api

G = "https://www.googleapis.com/youtube/v3/"
ep = Path(sys.argv[1]); apply = "--apply" in sys.argv
m = json.loads((ep / "upload_meta.json").read_text()); vid = json.loads((ep / "uploaded.json").read_text())["video_id"]
assert len(",".join(m["tags"])) <= 480, "tags too long"
tok, _ = token()
_, _, b = api("GET", G + f"videos?part=snippet&id={vid}", tok)
sn = json.loads(b)["items"][0]["snippet"]
print("live tags:", len(sn.get("tags", [])), "| new tags:", len(m["tags"]))
print("new description ends:", m["description"][-120:].replace("\n", " / "))
if apply:
    new = {"title": m["title"], "description": m["description"], "tags": m["tags"], "categoryId": m["categoryId"],
           "defaultLanguage": sn.get("defaultLanguage", "en"), "defaultAudioLanguage": sn.get("defaultAudioLanguage", "en")}
    st, _, r = api("PUT", G + "videos?part=snippet", tok, {"id": vid, "snippet": new})
    got = json.loads(r)["snippet"]
    print("updated", vid, st, "| tags now", len(got.get("tags", [])))
