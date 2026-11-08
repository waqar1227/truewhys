"""Facebook Page posting with the Page token (Graph API only; token injected by the proxy, never seen here).

python lib/fb_post.py <episode_dir> schedule   -> schedules every facebook post in social/plan.json that is not yet in social/posted.json
python lib/fb_post.py <episode_dir> comments   -> adds the YouTube-link first comment to Reels that are live and have none yet

Reels: video_reels start -> rupload (file bytes sent directly) -> finish with video_state=SCHEDULED.
Trailer: /videos multipart source, scheduled. Banner: /photos multipart source, scheduled. No hosting needed. Times must be >= 15 min ahead.
"""
import sys, json, time, datetime as dt
from pathlib import Path
import requests
sys.path.insert(0, str(Path(__file__).parent))

G = "https://graph.facebook.com/v21.0"
import os
PAGE = os.environ["FACEBOOK_PAGE_ID"]


def ts(iso):
    return int(dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp())


def post(url, **kw):
    r = requests.post(url, timeout=600, **kw)
    if r.status_code >= 400:
        raise RuntimeError(f"{url.split('?')[0]} -> {r.status_code} {r.text[:300]}")
    return r.json()


def reel(file, text, when):
    v = post(f"{G}/{PAGE}/video_reels", data={"upload_phase": "start"})
    vid = v["video_id"]
    data = Path(file).read_bytes()
    post(v["upload_url"], headers={"offset": "0", "file_size": str(len(data))}, data=data)
    post(f"{G}/{PAGE}/video_reels", data={"upload_phase": "finish", "video_id": vid, "video_state": "SCHEDULED",
                                         "scheduled_publish_time": ts(when), "description": text})
    return dict(id=vid)


def video(file, text, title, when):
    with open(file, "rb") as f:
        r = post(f"{G}/{PAGE}/videos", files={"source": (Path(file).name, f, "video/mp4")},
                 data={"description": text, "title": title or "", "published": "false", "scheduled_publish_time": ts(when)})
    return dict(id=r["id"])


def photo(file, text, when):
    with open(file, "rb") as f:
        r = post(f"{G}/{PAGE}/photos", files={"source": (Path(file).name, f, "image/jpeg")},
                 data={"caption": text, "published": "false", "scheduled_publish_time": ts(when)})
    return dict(id=r.get("post_id") or r["id"])


def main(ep, mode):
    ep = Path(ep)
    plan = json.loads((ep / "social/plan.json").read_text())
    pp = ep / "social/posted.json"
    done = json.loads(pp.read_text()) if pp.exists() else {}
    now = time.time()
    for p in plan["posts"]:
        if p["platform"] != "facebook":
            continue
        key = f"facebook:{p['kind']}:{p.get('short') or 'long'}"
        if mode == "schedule" and key not in done:
            if not Path(p["file"]).exists():
                print("missing file, skipped:", key, p["file"]); continue
            if ts(p["when"]) < now + 15 * 60:
                print("slot too close or past, skipped:", key, p["when"]); continue
            if p["kind"] == "reel":
                r = reel(p["file"], p["text"], p["when"])
            elif p["kind"] == "banner":
                r = photo(p["file"], p["text"], p["when"])
            else:
                r = video(p["file"], p["text"], p.get("title"), p["when"])
            r.update(when=p["when"], first_comment=p.get("first_comment"), commented=False)
            done[key] = r
            print("scheduled", key, p["when"], r["id"])
        elif mode == "comments" and key in done and done[key].get("first_comment") and not done[key]["commented"]:
            if ts(done[key]["when"]) > now:
                continue
            post(f"{G}/{done[key]['id']}/comments", data={"message": done[key]["first_comment"]})
            done[key]["commented"] = True
            print("commented", key)
        pp.write_text(json.dumps(done, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
