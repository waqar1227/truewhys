"""Build upload.md + upload_meta.json for a long video from shots.json, seo.json, sources.md and credits.
python lib/upload_pkg.py episodes/<ep> [publishAt ISO]"""
import sys, json, re
from pathlib import Path
ep = Path(sys.argv[1]); publish = sys.argv[2] if len(sys.argv) > 2 else None
plan = json.loads((ep / "shots.json").read_text()); seo = json.loads((ep / "seo.json").read_text())
starts = {}
for sh in plan["shots"]:
    c = sh.get("chapter")
    if c is not None and str(c) not in starts:
        starts[str(c)] = sh["start"]
starts["0"] = 0.0
def ts(t): t = int(t); return f"{t // 60}:{t % 60:02d}"
chap = "\n".join(f"{ts(starts[k])} {v}" for k, v in sorted(seo["chapters"].items(), key=lambda kv: starts.get(kv[0], 0)) if k in starts)
src = (ep / "sources.md").read_text()
urls = sorted(set(re.findall(r"https?://[^\s)|]+", src)))
extra_credit = ("\n" + seo["credits_extra"]) if seo.get("credits_extra") else ""
desc = f"""{seo['hook']}

{seo['summary']}

Chapters
{chap}

Sources
""" + "\n".join("• " + b for b in seo.get("sources", [])) + "\n" + "\n".join("• " + u for u in urls if "gutenberg" not in u) + f"""

Credits
Animation, 3D sets, characters and music: TrueWhys (original)..
Sound effects: CC0 — Kenney & OpenGameArt contributors; BigSoundBank (Joseph Sardin). Map data: Natural Earth (public domain).{extra_credit}

TrueWhys — the real story behind life's weirdest whys.
{' '.join(seo['hashtags'])}"""
meta = {"title": seo["title"], "description": desc, "tags": seo["tags"], "categoryId": "27", "publishAt": publish, "playlist": seo.get("playlist"),
        "pinned_comment": seo["pinned"]}
(ep / "upload_meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
(ep / "upload.md").write_text(f"""# Upload — {seo['title']}

- **Title:** {seo['title']}
- **Alt title (A/B):** {seo['title_alt']}
- **Thumbnails:** final/thumb_A.jpg ("GUILTY?"), final/thumb_B.jpg ("ON TRIAL?!") — use YouTube's Test & Compare
- **Schedule:** private → publishAt {publish}
- **Category:** Education (27) · Made for kids: No · Altered/synthetic field: left unset
- **Playlist:** {seo.get('playlist')}
- **Tags:** {', '.join(seo['tags'])}
- **Pinned comment:** {seo['pinned']}
- **End screen:** 20 s at the end (two video boxes on the right, subscribe circle bottom-left)

## Description
```
{desc}
```
""")
print(len(desc), "chars;", chap)
