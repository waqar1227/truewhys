"""YouTube upload (Data API v3). Keys from env: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
(sent only to oauth2.googleapis.com / www.googleapis.com). Never prints tokens.

python lib/youtube.py check                      -> verifies the refresh token and scopes
python lib/youtube.py upload <video.mp4> <meta.json> [thumb.jpg]
meta.json: {"title","description","tags":[...],"categoryId":"27","publishAt":"2026-11-08T15:00:00Z",
            "playlist": "Full Stories" (optional, needs youtube scope)}
Status: private + publishAt, madeForKids false, containsSyntheticMedia false (owner rule: cartoon = No).
"""
import os, sys, json, urllib.request, urllib.parse, urllib.error


def token():
    data = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                   "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    try:
        r = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data=data, timeout=30))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "invalid_grant" in body:
            sys.exit("invalid_grant: the YouTube refresh token needs renewing (guide Part 10.4)")
        sys.exit(f"token error {e.code}: {json.loads(body).get('error')}")
    return r["access_token"], r.get("scope", "")


def api(method, url, tok, body=None, ctype="application/json", raw=None):
    h = {"Authorization": "Bearer " + tok}
    data = None
    if body is not None:
        data = json.dumps(body).encode(); h["Content-Type"] = ctype
    if raw is not None:
        data = raw; h["Content-Type"] = ctype
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=600) as r:
        return r.status, dict(r.headers), r.read()


def upload(video, meta, thumb=None):
    tok, scope = token()
    m = json.load(open(meta))
    status = {"privacyStatus": "private", "selfDeclaredMadeForKids": False, "containsSyntheticMedia": False}
    if m.get("publishAt"):
        status["publishAt"] = m["publishAt"]
    body = {"snippet": {"title": m["title"][:100], "description": m["description"][:5000], "tags": m.get("tags", [])[:30],
                        "categoryId": m.get("categoryId", "27"), "defaultLanguage": "en", "defaultAudioLanguage": "en"},
            "status": status}
    size = os.path.getsize(video)
    st, hd, _ = api("POST", "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status", tok, body,
                    "application/json; charset=UTF-8")
    loc = hd.get("Location") or hd.get("location")
    with open(video, "rb") as f:
        data = f.read()
    req = urllib.request.Request(loc, data=data, method="PUT", headers={"Authorization": "Bearer " + tok, "Content-Type": "video/mp4",
                                                                       "Content-Length": str(size)})
    r = json.load(urllib.request.urlopen(req, timeout=3600))
    vid = r["id"]
    print("uploaded video id", vid, "status", r.get("status", {}).get("privacyStatus"), r.get("status", {}).get("publishAt"))
    if thumb:
        try:
            ct = "image/png" if thumb.endswith(".png") else "image/jpeg"
            api("POST", f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}", tok, raw=open(thumb, "rb").read(), ctype=ct)
            print("thumbnail set")
        except urllib.error.HTTPError as e:
            print("thumbnail failed", e.code, e.read()[:200])
    return vid


if __name__ == "__main__":
    if sys.argv[1] == "check":
        tok, scope = token()
        print("token ok; scopes:", scope)
    elif sys.argv[1] == "upload":
        upload(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
