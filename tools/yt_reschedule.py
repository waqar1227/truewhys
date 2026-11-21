"""Move a scheduled (private) video to a new publishAt. Keeps privacy, AI field (No), licence etc. (~51 quota units).
python tools/yt_reschedule.py <video_id> <YYYY-MM-DDTHH:MM:SSZ> [episode_dir]   -> also updates <episode_dir>/uploaded.json publishAt
Refuses times less than 1 hour ahead (owner rule) and public videos."""
import sys, json, datetime as dt
from pathlib import Path
sys.path.insert(0, "lib")
from youtube import token, api

G = "https://www.googleapis.com/youtube/v3/"
KEEP = ("privacyStatus", "selfDeclaredMadeForKids", "embeddable", "license", "publicStatsViewable")


def main(vid, when, ep=None):
    t = dt.datetime.strptime(when, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    if t < dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=1):
        sys.exit("refused: publishAt must be at least 1 hour ahead")
    tok, _ = token()
    _, _, b = api("GET", G + f"videos?part=status,snippet&id={vid}", tok)
    v = json.loads(b)["items"][0]
    if v["status"]["privacyStatus"] != "private":
        sys.exit(f"refused: {vid} is {v['status']['privacyStatus']}")
    st = {k: v["status"][k] for k in KEEP if k in v["status"]}
    st["publishAt"] = when; st["containsSyntheticMedia"] = False
    _, _, r = api("PUT", G + "videos?part=status", tok, {"id": vid, "status": st})
    got = json.loads(r)["status"].get("publishAt")
    print(vid, v["snippet"]["title"][:50], "->", got)
    if ep:
        p = Path(ep) / "uploaded.json"
        if p.exists():
            u = json.loads(p.read_text()); u["publishAt"] = got; u.setdefault("reschedules", []).append(dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"))
            p.write_text(json.dumps(u, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
