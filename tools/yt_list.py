"""List every channel upload with its category: python tools/yt_list.py > JSON lines (id, title, categoryId, privacy, publishAt)."""
import sys, json; sys.path.insert(0, "lib")
from youtube import token, api
tok, _ = token()
_, _, b = api("GET", "https://www.googleapis.com/youtube/v3/channels?part=contentDetails&mine=true", tok)
up = json.loads(b)["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
ids, page = [], ""
while True:
    _, _, b = api("GET", f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId={up}{page}", tok)
    d = json.loads(b); ids += [i["contentDetails"]["videoId"] for i in d["items"]]
    if "nextPageToken" not in d: break
    page = "&pageToken=" + d["nextPageToken"]
for i in range(0, len(ids), 50):
    _, _, b = api("GET", "https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=" + ",".join(ids[i:i+50]), tok)
    for v in json.loads(b)["items"]:
        print(json.dumps({"id": v["id"], "title": v["snippet"]["title"], "cat": v["snippet"].get("categoryId"),
                          "privacy": v["status"]["privacyStatus"], "publishAt": v["status"].get("publishAt")}, ensure_ascii=False))
