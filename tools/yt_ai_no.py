"""Applies the AI/altered disclosure decision from docs/ai_disclosure.json (owner 18 Nov 2026: per-video decision; today every video is No).
python tools/yt_ai_no.py          -> dry run: lists videos whose field is not yet No (~2 units per 50 videos)
python tools/yt_ai_no.py --apply  -> videos.update part=status (~50 units each); keeps privacy, publishAt, license etc. unchanged."""
import sys, json, datetime as dt
from pathlib import Path
sys.path.insert(0, "lib")
from youtube import token, api

G = "https://www.googleapis.com/youtube/v3/"
LOG = Path("docs/audit/ai_no.json")  # YouTube's GET omits containsSyntheticMedia when it is false, so successful updates are recorded here
KEEP = ("privacyStatus", "publishAt", "selfDeclaredMadeForKids", "embeddable", "license", "publicStatsViewable")


def main(apply, limit):
    tok, _ = token()
    done = json.loads(LOG.read_text()) if LOG.exists() else {}
    _, _, b = api("GET", G + "channels?part=contentDetails&mine=true", tok)
    up = json.loads(b)["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, page = [], ""
    while True:
        _, _, b = api("GET", G + f"playlistItems?part=contentDetails&maxResults=50&playlistId={up}" + (f"&pageToken={page}" if page else ""), tok)
        d = json.loads(b); ids += [i["contentDetails"]["videoId"] for i in d["items"]]
        page = d.get("nextPageToken")
        if not page:
            break
    todo = []
    for i in range(0, len(ids), 50):
        _, _, b = api("GET", G + "videos?part=status,snippet&id=" + ",".join(ids[i:i + 50]), tok)
        todo += [v for v in json.loads(b)["items"] if v["status"].get("containsSyntheticMedia") is True or v["id"] not in done]
    print(f"{len(ids)} videos, {len(todo)} not yet No (by ai_no.json record)")
    for v in todo[:limit]:
        st = {k: v["status"][k] for k in KEEP if k in v["status"]}
        st["containsSyntheticMedia"] = False
        print(v["id"], v["status"].get("privacyStatus"), v["snippet"]["title"][:45])
        if apply:
            _, _, r = api("PUT", G + "videos?part=status", tok, {"id": v["id"], "status": st})
            if json.loads(r)["status"].get("containsSyntheticMedia") is False:
                done[v["id"]] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
                LOG.write_text(json.dumps(done, indent=1))


if __name__ == "__main__":
    lim = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 10**6
    main("--apply" in sys.argv, lim)
