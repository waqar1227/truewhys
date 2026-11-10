"""YouTube upload (Data API v3). Keys from env: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
(sent only to oauth2.googleapis.com / www.googleapis.com). Never prints tokens.

python lib/youtube.py check                      -> verifies the refresh token and scopes
python lib/youtube.py upload <video.mp4> <meta.json> [thumb.jpg] [--long <video id>]
python lib/youtube.py comment <meta.json>         -> posts "pinned_comment" once the video is live
  --long fills {LONG_URL} in the description (cut Shorts). Writes uploaded.json next to meta.json and refuses to
  upload the same meta twice. Optional meta keys: "playlist" (added, created if missing), "pinned_comment" (posted;
  pinning itself is done in YouTube Studio, the API cannot pin).
meta.json: {"title","description","tags":[...],"categoryId":"27","publishAt":"2026-11-08T15:00:00Z",
            "playlist": "Full Stories" (optional, needs youtube scope)}
Status: private + publishAt, madeForKids false, AI/altered field not sent (owner rule: leave unset; if required, No).
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


def playlist_id(tok, title):
    _, _, b = api("GET", "https://www.googleapis.com/youtube/v3/playlists?part=snippet&mine=true&maxResults=50", tok)
    for it in json.loads(b).get("items", []):
        if it["snippet"]["title"] == title:
            return it["id"]
    _, _, b = api("POST", "https://www.googleapis.com/youtube/v3/playlists?part=snippet,status", tok,
                  {"snippet": {"title": title}, "status": {"privacyStatus": "public"}})
    return json.loads(b)["id"]


def extras(tok, vid, m):
    if m.get("playlist"):
        try:
            pl = playlist_id(tok, m["playlist"])
            api("POST", "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet", tok,
                {"snippet": {"playlistId": pl, "resourceId": {"kind": "youtube#video", "videoId": vid}}})
            print("added to playlist", m["playlist"])
        except urllib.error.HTTPError as e:
            print("playlist failed", e.code, e.read()[:200])
    if m.get("pinned_comment"):
        try:
            api("POST", "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet", tok,
                {"snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": m["pinned_comment"]}}}})
            print("comment posted (pin it in YouTube Studio)")
        except urllib.error.HTTPError as e:
            print("comment failed (comments open only after publish on some channels)", e.code, e.read()[:200])


def upload(video, meta, thumb=None, long_id=None):
    thumb_ok = None if thumb else "none given"
    done = os.path.join(os.path.dirname(os.path.abspath(meta)), "uploaded.json")
    if os.path.exists(done):
        sys.exit(f"already uploaded: {done}")
    tok, scope = token()
    m = json.load(open(meta))
    if "{LONG_URL}" in m["description"]:
        if not long_id:
            sys.exit("this description needs --long <long video id>")
        m["description"] = m["description"].replace("{LONG_URL}", "https://youtu.be/" + long_id)
    status = {"privacyStatus": "private", "selfDeclaredMadeForKids": False}  # AI/altered field left unset (owner rule); if ever required: False, never True
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
            print("thumbnail set"); thumb_ok = True
        except urllib.error.HTTPError as e:
            thumb_ok = f"FAILED {e.code}: {e.read()[:200]}"
            print("THUMBNAIL FAILED — tell the owner (custom thumbnails need a phone-verified channel: youtube.com/verify)", thumb_ok)
    json.dump({"video_id": vid, "publishAt": m.get("publishAt"), "title": m["title"], "thumbnail": thumb_ok}, open(done, "w"), indent=1)
    extras(tok, vid, m)
    return vid


if __name__ == "__main__":
    if sys.argv[1] == "check":
        tok, scope = token()
        print("token ok; scopes:", scope)
    elif sys.argv[1] == "upload":
        a = sys.argv[2:]
        long_id = None
        if "--long" in a:
            i = a.index("--long"); long_id = a[i + 1]; del a[i:i + 2]
        upload(a[0], a[1], a[2] if len(a) > 2 else None, long_id)
    elif sys.argv[1] == "comment":  # python lib/youtube.py comment <meta.json>: post pinned_comment after the video is live
        import pathlib
        mp = pathlib.Path(sys.argv[2]); m = json.loads(mp.read_text()); up = json.loads((mp.parent / "uploaded.json").read_text())
        tok, _ = token()
        api("POST", "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet", tok,
            {"snippet": {"videoId": up["video_id"], "topLevelComment": {"snippet": {"textOriginal": m["pinned_comment"]}}}})
        print("comment posted on", up["video_id"], "(owner pins it in Studio)")
