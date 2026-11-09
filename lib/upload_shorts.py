"""Upload packages for the Shorts cut from a long video.

python lib/upload_shorts.py episodes/<ep> <long publishAt ISO> [first_offset_h=1] [gap_h=3]
-> episodes/<ep>/shorts/<CID>/upload_meta.json for every Short + episodes/<ep>/upload_shorts.md
Release plan (owner, 6 Nov 2026): every cut Short goes live within 24 h after the long video, about one every 3 h.
The description holds {LONG_URL}; lib/youtube.py fills it with the long video's link at upload time (--long <video id>).
YouTube's "Related video" field is not in the Data API: it is set in YouTube Studio (listed in upload_shorts.md).
"""
import sys, json, datetime as dt
from pathlib import Path

ep = Path(sys.argv[1])
long_at = dt.datetime.fromisoformat(sys.argv[2].replace("Z", "+00:00"))
first = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
gap = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0
cfg = json.loads((ep / "shorts.json").read_text())
seo = json.loads((ep / "seo.json").read_text())
lines = {}
for ln in (ep / "lines.txt").read_text().splitlines():
    if ln and not ln.startswith("#"):
        p = ln.split("|")
        lines[p[0]] = p[2]

base_tags = [t for t in seo["tags"] if len(t) < 30][:10]
rows = []
for i, c in enumerate(cfg["shorts"]):
    at = long_at + dt.timedelta(hours=first + gap * i)
    assert at - long_at <= dt.timedelta(hours=24), f"{c['id']} would go out more than 24 h after the long video"
    body = " ".join(lines[l] for l in c["lines"][:2])
    if len(body) > 220:
        body = body[:217].rsplit(" ", 1)[0] + "…"
    if body[-1] in ":;,":
        body = body[:-1] + "…"
    title = c["title"]
    if len(title) + 8 <= 100:
        title += " #Shorts"
    desc = f"""{c['hook']['text']} {body}

▶ Full story: {seo['title']} — {{LONG_URL}}

Sources and credits are in the full video's description. Animation and music: TrueWhys (original).
TrueWhys — the real story behind life's weirdest whys.
#Shorts {' '.join(seo['hashtags'])}"""
    meta = {"title": title, "description": desc, "tags": ["shorts"] + base_tags, "categoryId": "27",
            "publishAt": at.strftime("%Y-%m-%dT%H:%M:%SZ"), "playlist": "Shorts", "short": c["id"],
            "video": f"shorts/{c['id']}/final.mp4", "related": "long video (set in YouTube Studio)"}
    d = ep / "shorts" / c["id"]; d.mkdir(parents=True, exist_ok=True)
    (d / "upload_meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    rows.append((c["id"], meta["publishAt"], title, len(desc)))

md = [f"# Shorts upload — cut from \"{seo['title']}\"", "",
      f"Long video publishAt: {sys.argv[2]}. Shorts: +{first:g} h, then every {gap:g} h (all within 24 h). Owner rule 6 Nov 2026.", "",
      "Each Short: private + publishAt, made for kids No, altered/synthetic field left unset, playlist \"Shorts\".",
      "After upload: in YouTube Studio set **Related video = the long video** on each Short (not available in the API).", "",
      "| Short | publishAt (UTC) | Title | Desc chars |", "|---|---|---|---|"]
md += [f"| {a} | {b} | {t} | {n} |" for a, b, t, n in rows]
md += ["", "Upload: `python lib/youtube.py upload episodes/<ep>/shorts/<CID>/final.mp4 episodes/<ep>/shorts/<CID>/upload_meta.json --long <long video id>`"]
(ep / "upload_shorts.md").write_text("\n".join(md) + "\n")
print("\n".join(f"{a}  {b}  {t}" for a, b, t, n in rows))
