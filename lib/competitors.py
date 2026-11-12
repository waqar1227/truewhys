"""Daily competitor snapshot (no AI needed, no API key): latest uploads + view counts of the model channels via yt-dlp.
python lib/competitors.py [--force] -> research/competitors/<date>.json (cache: reused if today's exists) + <date>.md
The .md lists breakouts (>= 500k views), fastest growers since the last snapshot and new uploads, so the daily report
only needs a short human-style analysis on top. Format study only: never copy titles, characters or art.
"""
import sys, json, subprocess, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "research/competitors"
CHANNELS = {  # name: (url, how many latest items)
    "Rick's Clips": ("https://www.youtube.com/@RicksClips3000/shorts", 30),
    "Zack D. Films": ("https://www.youtube.com/@zackdfilms/shorts", 30),
    "Ink Explainer": ("https://www.youtube.com/@Inkexplainer96/videos", 15),
}
import os, shutil
YTDLP = "/opt/c3d/bin/yt-dlp" if os.path.exists("/opt/c3d/bin/yt-dlp") else (shutil.which("yt-dlp") or "yt-dlp")
BREAKOUT = 500_000


def fetch(url, n):
    r = subprocess.run([YTDLP, "--flat-playlist", "-J", "--playlist-end", str(n), url], capture_output=True, text=True, timeout=180)
    if r.returncode:
        return None, r.stderr.strip()[-200:]
    d = json.loads(r.stdout)
    return [dict(id=e.get("id"), title=e.get("title"), views=e.get("view_count"), dur=e.get("duration")) for e in d.get("entries", [])], None


def main(force=False):
    OUT.mkdir(parents=True, exist_ok=True)
    today = str(dt.date.today())
    f = OUT / f"{today}.json"
    if f.exists() and not force:
        snap = json.loads(f.read_text())
    else:
        snap = {"date": today, "channels": {}}
        for name, (url, n) in CHANNELS.items():
            items, err = fetch(url, n)
            snap["channels"][name] = items if items is not None else {"error": err}
        f.write_text(json.dumps(snap, indent=1))
    prev = sorted(p for p in OUT.glob("*.json") if p.stem < today)
    old = json.loads(prev[-1].read_text())["channels"] if prev else {}
    days = (dt.date.fromisoformat(today) - dt.date.fromisoformat(prev[-1].stem)).days if prev else 0
    L = [f"# Competitors {today} (vs {prev[-1].stem if prev else 'none'})", ""]
    for name, items in snap["channels"].items():
        if isinstance(items, dict):
            L.append(f"## {name}: fetch failed ({items.get('error')})"); continue
        before = {i["id"]: i for i in old.get(name, []) if isinstance(old.get(name), list)}
        L.append(f"## {name}")
        newi = [i for i in items if before and i["id"] not in before]
        grow = sorted((((i["views"] or 0) - (before[i["id"]]["views"] or 0), i) for i in items if i["id"] in before), key=lambda t: t[0])
        grow = [g for g in grow[::-1] if g[0] > 0][:3]
        top = sorted((i for i in items if (i["views"] or 0) >= BREAKOUT), key=lambda i: -(i["views"] or 0))[:5]
        L.append("- Breakouts (latest uploads): " + ("; ".join(f"\"{i['title']}\" {i['views']/1e6:.1f} M" for i in top) or "none"))
        if newi:
            L.append("- New since last check: " + "; ".join(f"\"{i['title']}\" {(i['views'] or 0)/1e3:.0f} k" for i in newi))
        if grow:
            L.append(f"- Fastest growth (+views in {days} d): " + "; ".join(f"\"{i['title']}\" +{g/1e3:.0f} k" for g, i in grow))
        L.append("")
    md = "\n".join(L)
    (OUT / f"{today}.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main("--force" in sys.argv)
