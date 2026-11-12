"""Change a video's YouTube category, keeping title/description/tags: python tools/yt_category.py <videoId> <categoryId> [...pairs]"""
import sys, json; sys.path.insert(0, "lib")
from youtube import token, api
tok, scope = token()
a = sys.argv[1:]
for vid, cat in zip(a[::2], a[1::2]):
    _, _, b = api("GET", f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={vid}", tok)
    s = json.loads(b)["items"][0]["snippet"]
    if s.get("categoryId") == cat: print(vid, "already", cat); continue
    body = {"id": vid, "snippet": {k: s[k] for k in ("title", "description", "tags", "categoryId", "defaultLanguage", "defaultAudioLanguage") if k in s}}
    body["snippet"]["categoryId"] = cat
    _, _, b = api("PUT", "https://www.googleapis.com/youtube/v3/videos?part=snippet", tok, body)
    print(vid, "->", json.loads(b)["snippet"]["categoryId"])
