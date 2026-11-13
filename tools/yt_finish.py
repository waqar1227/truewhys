"""Finish an upload whose thumbnail/playlist step failed (e.g. API quota): python tools/yt_finish.py episodes/<ep> [thumb.jpg]
Sets the thumbnail, adds the video to its playlist, and records both in uploaded.json. Safe to run again."""
import sys, json, urllib.error
from pathlib import Path
sys.path.insert(0, "lib")
from youtube import token, api, playlist_id
ep = Path(sys.argv[1])
up = json.loads((ep / "uploaded.json").read_text()); m = json.loads((ep / "upload_meta.json").read_text())
thumb = Path(sys.argv[2]) if len(sys.argv) > 2 else ep / "final/thumb.jpg"
tok, _ = token(); vid = up["video_id"]
try:
    if up.get("thumbnail") is not True:
        api("POST", f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}", tok, raw=thumb.read_bytes(), ctype="image/jpeg")
        up["thumbnail"] = True; print("thumbnail set")
    if m.get("playlist") and up.get("playlist") is not True:
        pl = playlist_id(tok, m["playlist"])
        api("POST", "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet", tok,
            {"snippet": {"playlistId": pl, "resourceId": {"kind": "youtube#video", "videoId": vid}}})
        up["playlist"] = True; print("added to playlist", m["playlist"])
except urllib.error.HTTPError as e:
    print("FAILED", e.code, "quota" if b"quota" in e.read() else "")
(ep / "uploaded.json").write_text(json.dumps(up, indent=1))
print(json.dumps(up))
