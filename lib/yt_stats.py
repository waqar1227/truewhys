"""Channel performance snapshot for the daily growth report.
python lib/yt_stats.py [days=28] -> prints a markdown table and writes research/stats/<date>.json + <date>.md
(views gained since the last snapshot, traffic sources, retention 10/50/90 % and the biggest drop point)
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
    # traffic sources (channel level): tells discovery problems (few SHORTS/BROWSE views) from packaging/retention problems
    tq = dict(ids="channel==MINE", startDate=str(start), endDate=str(end), dimensions="insightTrafficSourceType", metrics="views", sort="-views")
    st3, tr = get(tok, "https://youtubeanalytics.googleapis.com/v2/reports?" + urllib.parse.urlencode(tq))
    traffic = {r[0]: r[1] for r in tr.get("rows", [])} if st3 == 200 else {}
    # retention curve per public video (Analytics data lags ~2-3 days): where do viewers leave?
    for vid, v in vids.items():
        if v.get("privacy") != "public":
            continue
        rq = dict(ids="channel==MINE", startDate=str(start), endDate=str(end), dimensions="elapsedVideoTimeRatio",
                  metrics="audienceWatchRatio", filters=f"video=={vid}")
        st4, rr = get(tok, "https://youtubeanalytics.googleapis.com/v2/reports?" + urllib.parse.urlencode(rq))
        rows = rr.get("rows", []) if st4 == 200 else []
        if rows:
            at = lambda x: min(rows, key=lambda r: abs(r[0] - x))[1]
            drops = [(rows[i][0], rows[i - 1][1] - rows[i][1]) for i in range(1, len(rows))]
            big = max(drops, key=lambda d: d[1])
            v["ret"] = dict(r10=round(at(0.1), 2), r50=round(at(0.5), 2), r90=round(at(0.9), 2),
                            drop_at=round(big[0], 2), drop=round(big[1], 2))
    # views gained since the previous snapshot (the 24/48 h check)
    out = ROOT / "research/stats"; out.mkdir(parents=True, exist_ok=True)
    prev = sorted(p for p in out.glob("*.json") if p.stem < str(end))
    pv = json.loads(prev[-1].read_text()).get("videos", {}) if prev else {}
    for vid, v in vids.items():
        if vid in pv and "views" in v and "views" in pv[vid]:
            v["gain"] = v["views"] - pv[vid]["views"]
    snap = dict(date=str(end), channel=chs, traffic=traffic, videos=vids)
    (out / f"{end}.json").write_text(json.dumps(snap, indent=1))
    lines = [f"# Stats {end} ({days} d window; since {prev[-1].stem if prev else '-'})",
             f"Channel: subs {chs.get('subscriberCount')}, views {chs.get('viewCount')}, videos {chs.get('videoCount')}",
             "Traffic: " + ", ".join(f"{k} {n}" for k, n in traffic.items()),
             "Retention = audience watch ratio at 10/50/90 % of the video (Shorts loop, so >1 is possible); drop = biggest fall and where.",
             "CTR/impressions: not in the API, owner pastes them from Studio.", "",
             "| published | len | views | +since | likes | avg % | avg s | subs+ | ret 10/50/90 | drop@ | title |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for vid, v in sorted(vids.items(), key=lambda kv: kv[1].get("published", ""), reverse=True):
        if v.get("privacy") != "public":
            continue
        r = v.get("ret"); rs = f"{r['r10']}/{r['r50']}/{r['r90']}" if r else "-"; ds = f"{r['drop_at']:.0%} (-{r['drop']})" if r else "-"
        lines.append(f"| {v.get('published','')[:16]} | {v.get('duration','')} | {v.get('views','')} | {v.get('gain','-')} | {v.get('likes','')} | "
                     f"{v.get('averageViewPercentage','-')} | {v.get('averageViewDuration','-')} | {v.get('subscribersGained','-')} | {rs} | {ds} | {v.get('title','')[:50]} |")
    md = "\n".join(lines) + "\n"
    (out / f"{end}.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 28)
