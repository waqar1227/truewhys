"""Facebook + TikTok packages for an episode (YouTube first, then cross-post).

python lib/crosspost.py episodes/<ep>  -> episodes/<ep>/social/plan.json + social/README.md
Uses the YouTube ids in uploaded.json (long video) and shorts/<CID>/uploaded.json (Shorts) when they exist;
otherwise the link stays as {LONG_URL}/{SHORT_URL} and is filled in once YouTube has them.
Owner rule (7 Nov 2026): goal is YouTube views. Facebook text carries the clickable YouTube link; TikTok captions
(no clickable links) end with "Watch the full video on YouTube — @TrueWhys".
Timing: each Short -> TikTok + Facebook Reel 30 min after its YouTube slot (Reel: CTA in caption, YouTube link in first comment);
long video -> NOT uploaded in full to Facebook: a 60-90 s trailer (social/trailer.mp4, cut + QA'd) with the clickable link, 30 min after the premiere.
"""
import sys, json, datetime as dt
from pathlib import Path

CTA_TT = "Watch the full video on YouTube — @TrueWhys"
ep = Path(sys.argv[1])
seo = json.loads((ep / "seo.json").read_text())
cfg = json.loads((ep / "shorts.json").read_text())
long_meta = json.loads((ep / "upload_meta.json").read_text())
up = json.loads((ep / "uploaded.json").read_text()) if (ep / "uploaded.json").exists() else {}
long_url = f"https://youtu.be/{up['video_id']}" if up.get("video_id") else "{LONG_URL}"


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


tags = [h for h in seo["hashtags"] if h.lower() != "#truewhys"]
posts = []
for c in cfg["shorts"]:
    d = ep / "shorts" / c["id"]
    m = json.loads((d / "upload_meta.json").read_text())
    u = json.loads((d / "uploaded.json").read_text()) if (d / "uploaded.json").exists() else {}
    when = parse(m["publishAt"]) + dt.timedelta(minutes=30)
    title = c["title"]
    hook = c["hook"]["text"]
    tt = f"{hook} 🤯\n\n{title}.\n\n{CTA_TT}\n\n" + " ".join(["#history", "#learnontiktok", "#weirdhistory"] + [t.lower() for t in tags[:1]] + ["#truewhys"])
    fb = f"{hook}\n\n{CTA_TT}\n\n" + " ".join(seo["hashtags"])
    file = str(d / "final.mp4")
    posts.append(dict(platform="tiktok", kind="video", short=c["id"], file=file, when=iso(when), text=tt, title=title[:90],
                      youtube_short=f"https://youtube.com/shorts/{u['video_id']}" if u.get("video_id") else None))
    posts.append(dict(platform="facebook", kind="reel", short=c["id"], file=file, when=iso(when), text=fb,
                      first_comment=f"▶ Full story on YouTube: {long_url}"))
if long_meta.get("publishAt"):
    when = parse(long_meta["publishAt"]) + dt.timedelta(minutes=30)
    fbl = f"{seo['hook']}\n\n{seo['summary']}\n\n▶ Watch the full video on YouTube: {long_url}\n\n" + " ".join(seo["hashtags"])
    posts.append(dict(platform="facebook", kind="trailer", short=None, file=str(ep / "social" / "trailer.mp4"),
                      when=iso(when), title=seo["title"], text=fbl, thumb=str(ep / "final" / "thumb_A.jpg")))
posts.sort(key=lambda p: p["when"])
out = ep / "social"; out.mkdir(exist_ok=True)
(out / "plan.json").write_text(json.dumps(dict(long_url=long_url, posts=posts), indent=1, ensure_ascii=False))
md = [f"# Facebook + TikTok plan — {seo['title']}", "", f"YouTube long video: {long_url}", "",
      "| When (UTC) | Platform | What | File |", "|---|---|---|---|"]
md += [f"| {p['when']} | {p['platform']} | {p['kind']} {p.get('short') or ''} | {Path(p['file']).relative_to(ep)} |" for p in posts]
md += ["", "## Captions", ""]
for p in posts:
    md += [f"### {p['when']} · {p['platform']} {p['kind']} {p.get('short') or ''}", "```", p["text"], "```", ""]
(out / "README.md").write_text("\n".join(md))
print(len(posts), "posts;", long_url)
