"""Rebuild the measured columns of topic_results.md from research/stats/*.json (daily snapshots, ~07:15 UTC).
python tools/topic_results.py  -> rewrites topic_results.md (tags table TAGS below; add one row per new upload).
48 h / 7 d = views in the first snapshot at least 48 h / 7 d after publishing (age shown), '-' until it exists. No invented numbers."""
import json, glob, datetime as dt
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
# id: (episode, type, category, style, title pattern)
TAGS = {
 "9C-9O0c6VqM": ("B-001", "B long", "1 History", "T", "Why …"),
 "5YqYpWmY7EA": ("B-001 C", "C cut", "1 History", "T", "The … That …"), "CPPa366kvr8": ("B-001 C", "C cut", "1 History", "T", "Why …"),
 "ypKUcSlisP0": ("B-001 C", "C cut", "1 History", "T", "The … Who …"), "23cFCmyvtKI": ("B-001 C", "C cut", "1 History", "T", "The … That …"),
 "sJ0HEbnwoj8": ("B-001 C", "C cut", "1 History", "T", "The … Who …"), "RI7u-NzEj5E": ("B-001 C", "C cut", "1 History", "T", "Why …"),
 "33UzHb61eKc": ("B-001 C", "C cut", "1 History", "T", "The …"),
 "h2oO3SrSUH8": ("B-002", "B long", "11 Daily life", "T", "Would You"),
 "FbtDoZL8vwk": ("B-002 C", "C cut", "11 Daily life", "T", "The …"), "66iyJcnwvgY": ("B-002 C", "C cut", "11 Daily life", "T", "The … Who …"),
 "WqxkoJY4jy4": ("B-002 C", "C cut", "11 Daily life", "T", "The … Where …"), "qCgG6Dhqgi4": ("B-002 C", "C cut", "11 Daily life", "T", "The … Who …"),
 "Wu5-PLKwb48": ("B-002 C", "C cut", "11 Daily life", "T", "The … Who …"), "kk6I9g5V82Y": ("B-002 C", "C cut", "11 Daily life", "T", "Why …"),
 "6wDhznnQeKI": ("B-002 C", "C cut", "11 Daily life", "T", "The …"), "TkNJsIdy7gs": ("B-002 C", "C cut", "11 Daily life", "T", "The … Where …"),
 "zCkUEA4t5iQ": ("A-008", "A standalone", "9 Science", "F", "The … That …"), "MLRRsaV4iUA": ("A-001", "A standalone", "8 Nature", "T", "Why …"),
 "8hsKNMLOhAw": ("A-005", "A standalone", "7 Body", "F", "What … Does"), "sdoOC7kAuRU": ("A-004", "A standalone", "7 Body", "T", "Why … (emoji)"),
 "WHd_m81cbpE": ("A-007", "A standalone", "9 Science", "F", "Why …"), "iW60L9Pap5k": ("A-006", "A standalone", "1 History", "F", "The … That …"),
 "bE1TP9JlAzs": ("A-003", "A standalone", "9 Science", "F", "Why …"), "o-dGmxKGKoY": ("A-002", "A standalone", "8 Nature", "T", "Why …"),
 "Am8epkS94Hw": ("B-003", "B long", "5 Ranked list", "T", "Ranked list"),
 # wave 1 + owner style A/B test (F-v2.1 = Style F with cast v2.1; R = Style R close-to-human 3D)
 "5XdQYTPzwxU": ("A-009", "A standalone", "2 Rules", "F-v2.1", "Why …"), "AshEYTYzMyI": ("A-010 (A/B: A1)", "A standalone", "7 Body", "F-v2.1", "Why …"),
 "yyBUc7aM2lA": ("A-011", "A standalone", "1 History", "F-v2.1", "The … That/Why …"), "1r8faDAYoTQ": ("A-012 (A/B: A2)", "A standalone", "10 Objects", "F-v2.1", "Why …"),
 "bHC7F6nNwWM": ("A-013", "A standalone", "8 Nature", "F-v2.1", "Why …"),
}
snaps = {}
for p in sorted(glob.glob(str(ROOT / "research/stats/*.json"))):
    snaps[dt.datetime.fromisoformat(Path(p).stem + "T07:15:00+00:00")] = json.load(open(p)).get("videos", {})
last = max(snaps) if snaps else None


def at(vid, pub, hours):
    for t in sorted(snaps):
        if (t - pub).total_seconds() >= hours * 3600 and vid in snaps[t]:
            return f"{snaps[t][vid].get('views', '-')} ({(t - pub).total_seconds() / 3600:.0f} h)"
    return "-"


rows = []
for vid, (ep, typ, cat, sty, pat) in TAGS.items():
    v = snaps[last].get(vid, {}) if last else {}
    pubs = v.get("published") or v.get("publish_at")
    pub = dt.datetime.fromisoformat(pubs.replace("Z", "+00:00")) if pubs else None
    rel = v.get("rel") or {}
    rows.append((pubs or "scheduled", f"| {(pubs or 'scheduled')[:16]} | {ep} | {v.get('title', '(scheduled)')[:55]} | {typ} | {cat} | {sty} | {pat} | "
                 f"{at(vid, pub, 48) if pub else '-'} | {at(vid, pub, 168) if pub else '-'} | {v.get('averageViewPercentage') and round(v['averageViewPercentage'], 1) or '-'} | "
                 f"{v.get('stayed', '-')} | {rel.get('r10', '-')} | {v.get('likes', '-')} |"))
md = ["# Topic results (CLAUDE.md \"Topic testing\"; audit §6.8). Rebuilt by `python tools/topic_results.py` from research/stats/ snapshots.",
      f"Last snapshot: {last.date() if last else '-'}. 48 h / 7 d = views in the first daily snapshot at least that old (age in brackets). Avg % / stayed % / rel 10 % / likes = latest snapshot.",
      "Style: T = 3D toon v1, F = flat 2D (cast v1), F-v2.1 = flat 2D with cast v2.1, R = close-to-human 3D (owner A/B test 21–24 Nov: A1 F-v2.1, B1 R, B2 R, A2 F-v2.1).",
      "CTR/impressions: only from Studio numbers the owner pastes.", "",
      "| published (UTC) | ep | title | type | category | style | title pattern | 48 h views | 7 d views | avg % viewed | stayed % | rel ret 10 % | likes |",
      "|---|---|---|---|---|---|---|---|---|---|---|---|---|"] + [r for _, r in sorted(rows)]
md += ["", "Owner style A/B test rows to add when uploaded: A-016 Why Onions Make You Cry (B1, 8 Nature, R, 22 Nov) · A-017 Why Ice Cubes Are Cloudy (B2, 9 Science, R, 23 Nov).",
       "Compare at 48 h and 7 d: views, stayed %, avg % viewed, rel. retention 10 %, subs, likes, comments → report to the owner."]
(ROOT / "topic_results.md").write_text("\n".join(md) + "\n")
print("\n".join(md[:12]))
