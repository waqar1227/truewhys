"""Channel performance snapshot for the daily growth report.
python lib/yt_stats.py [days=28] -> prints a markdown table and writes research/stats/<date>.json
Uses the Data API (views/likes/comments per video) and the Analytics API (watch time, avg % viewed,
subs gained, impressions + CTR where available). Never prints tokens.
"""
import sys, os, json, datetime as dt, urllib.parse
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import youtube as y

ROOT = Path(__file__).resolve().parent.parent


def get(tok, url):
    import urllib.error
    try:
        st, h, b = y.api("GET", url, tok)
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}
    return st, json.loads(b) if b else {}


def main(days=28):
    tok, _ = y.token()
    end = dt.date.today(); start = end - dt.timedelta(days=days)
    st, ch = get(tok, "https://www.googleapis.com/youtube/v3/channels?part=id,statistics&mine=true")
    chs = ch["items"][0]["statistics"]
    st, s = get(tok, "https://www.googleapis.com/youtube/v3/search?part=id&forMine=true&type=video&maxResults=50&order=date")
    ids = [i["id"]["videoId"] for i in s.get("items", [])]
    vids = {}
    if ids:
        st, v = get(tok, "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,status,contentDetails&id=" + ",".join(ids))
        for it in v["items"]:
            vids[it["id"]] = dict(title=it["snippet"]["title"], published=it["snippet"]["publishedAt"], privacy=it["status"]["privacyStatus"],
                                  publish_at=it["status"].get("publishAt"), duration=it["contentDetails"]["duration"],
                                  views=int(it["statistics"].get("viewCount", 0)), likes=int(it["statistics"].get("likeCount", 0)),
                                  comments=int(it["statistics"].get("commentCount", 0)))
    q = dict(ids="channel==MINE", startDate=str(start), endDate=str(end), dimensions="video", sort="-views", maxResults=50,
             metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained")
    st, an = get(tok, "https://youtubeanalytics.googleapis.com/v2/reports?" + urllib.parse.urlencode(q))
    if st == 200:
        cols = [c["name"] for c in an.get("columnHeaders", [])]
        for row in an.get("rows", []):
            r = dict(zip(cols, row))
            vids.setdefault(r["video"], {}).update({k: r[k] for k in cols if k != "video"})
    else:
        print("analytics:", st, str(an)[:300])
    q2 = dict(q, metrics="impressions,impressionClickThroughRate")  # not offered by the Analytics API for most channels: CTR comes from Studio (owner pastes it)
    st2, im = get(tok, "https://youtubeanalytics.googleapis.com/v2/reports?" + urllib.parse.urlencode(q2))
    if st2 == 200:
        cols = [c["name"] for c in im.get("columnHeaders", [])]
        for row in im.get("rows", []):
            r = dict(zip(cols, row)); vids.setdefault(r["video"], {}).update(impressions=r.get("impressions"), ctr=r.get("impressionClickThroughRate"))
    snap = dict(date=str(end), channel=chs, videos=vids)
    out = ROOT / "research/stats"; out.mkdir(parents=True, exist_ok=True)
    (out / f"{end}.json").write_text(json.dumps(snap, indent=1))
    print(f"Channel: subs {chs.get('subscriberCount')}, views {chs.get('viewCount')}, videos {chs.get('videoCount')}")
    print("| published | len | views | likes | avg % viewed | avg s | subs+ | CTR | title |\n|---|---|---|---|---|---|---|---|---|")
    for vid, v in sorted(vids.items(), key=lambda kv: kv[1].get("published", ""), reverse=True):
        if v.get("privacy") != "public":
            continue
        print(f"| {v.get('published','')[:16]} | {v.get('duration','')} | {v.get('views','')} | {v.get('likes','')} | {v.get('averageViewPercentage','-')} | "
              f"{v.get('averageViewDuration','-')} | {v.get('subscribersGained','-')} | {v.get('ctr','-')} | {v.get('title','')[:55]} |")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 28)
