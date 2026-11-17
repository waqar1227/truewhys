"""Audit check V1-V9 against the LIVE channel (read-only, ~5 quota units). Run: /opt/c3d/bin/python docs/audit/verify.py
Prints PASS/FAIL per check and writes docs/audit/verify_<date>.json. Never prints tokens."""
import sys, os, re, json, datetime as dt, urllib.error
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "lib"))
import youtube as y

tok, _ = y.token()
D = "https://www.googleapis.com/youtube/v3/"


def get(u):
    try:
        return json.loads(y.api("GET", D + u, tok)[2])
    except urllib.error.HTTPError as e:
        return {"error": e.code}


ch = get("channels?part=snippet,contentDetails,brandingSettings&mine=true")["items"][0]
up = ch["contentDetails"]["relatedPlaylists"]["uploads"]
ids, page = [], ""
while True:
    d = get(f"playlistItems?part=contentDetails&maxResults=50&playlistId={up}{page}")
    ids += [i["contentDetails"]["videoId"] for i in d.get("items", [])]
    if "nextPageToken" not in d:
        break
    page = "&pageToken=" + d["nextPageToken"]
V = []
for i in range(0, len(ids), 50):
    V += get("videos?part=snippet,status,contentDetails,statistics&id=" + ",".join(ids[i:i + 50])).get("items", [])
PL = get("playlists?part=snippet,contentDetails&mine=true&maxResults=50").get("items", [])
fixes = {f["id"]: f for f in json.load(open(os.path.join(ROOT, "docs/audit/metadata_fixes.json")))["fixes"]}


def secs(s):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s); g = [int(x or 0) for x in m.groups()]; return g[0] * 3600 + g[1] * 60 + g[2]


def ytlen(t): return sum(len(x) + (2 if " " in x else 0) for x in t) + max(len(t) - 1, 0)


now = dt.datetime.now(dt.timezone.utc); res = {}; T = lambda v: v["snippet"]["title"]
short = lambda v: secs(v["contentDetails"]["duration"]) <= 185


def due(v):  # fixes are only expected once their apply time has passed
    a = fixes.get(v["id"], {}).get("apply", "now")
    return a == "now" or now >= dt.datetime.fromisoformat(a.replace("after ", "").replace("Z", "+00:00"))


def chk(k, bad, note=""):
    res[k] = dict(ok=not bad, fail=bad[:12], note=note); print(("PASS " if not bad else "FAIL ") + k, "" if not bad else f"({len(bad)})", note)
    for b in bad[:12]: print("     ", b)


chk("V1a no '#Shorts' in titles", [T(v) for v in V if "#" in T(v) and due(v)])
chk("V1b titles = fixes file (or script-checked variant)", [f"{v['id']} now '{T(v)}' | proposed '{fixes[v['id']]['new_title']}'" for v in V
     if v["id"] in fixes and fixes[v["id"]]["new_title"] and due(v) and T(v) != fixes[v["id"]]["new_title"]], "a differing title is fine if it is an open question and true to the script")
chk("V2a tags: >=15 and 300-500 chars", [f"{v['id']} {len(v['snippet'].get('tags', []))} tags, {ytlen(v['snippet'].get('tags', []))} ch | {T(v)[:40]}" for v in V
     if due(v) and not (len(v["snippet"].get("tags", [])) >= 15 and 300 <= ytlen(v["snippet"].get("tags", [])) <= 500)])
seen = {}
for v in V:
    if short(v): seen.setdefault(tuple(sorted(v["snippet"].get("tags", []))), []).append(v["id"])
chk("V2b no two Shorts share one tag list", [",".join(g) for g in seen.values() if len(g) > 1 and all(due(x) for x in V if x["id"] in g)])
bad = []
for v in V:
    if not due(v): continue
    h = re.findall(r"#\w+", v["snippet"]["description"])
    if len(h) != 3 or any(x[1].isdigit() for x in h) or h[0].lower() in ("#truewhys", "#shorts"): bad.append(f"{v['id']} {h[:6]}")
chk("V3a exactly 3 hashtags, topic first", bad)
longs = [v for v in V if not short(v)]
chk("V3b cut Shorts link a long video", [v["id"] for v in V if short(v) and fixes.get(v["id"], {}).get("kind") == "cut" and "youtu.be/" not in v["snippet"]["description"]])
b2 = next((v for v in V if v["id"] == "h2oO3SrSUH8"), None)
chk("V4 B-002 description clean", ([] if b2 is None else [x for x in (["'#8' style chapters"] if re.search(r"#\d", b2["snippet"]["description"]) else []) +
     (["broken wikipedia link"] if re.search(r"wikipedia\.org/wiki/\S*\([^)\s]*(\s|$)", b2["snippet"]["description"]) else [])]))
cd = ch["brandingSettings"]["channel"].get("description", "")
chk("V5 channel text has no schedule promise", [w for w in ("every day", "8–12 minute", "8-12 minute", "daily") if w in cd.lower()])
names = {p["snippet"]["title"]: p["contentDetails"]["itemCount"] for p in PL}
fs = next((p["id"] for p in PL if p["snippet"]["title"] == "Full Stories"), None)
inl = [i["contentDetails"]["videoId"] for i in get(f"playlistItems?part=contentDetails&maxResults=50&playlistId={fs}").get("items", [])] if fs else []
chk("V6a every long video in 'Full Stories'", [T(v) for v in longs if v["id"] not in inl and v["status"]["privacyStatus"] == "public"])
chk("V6b at least 5 topic playlists, none empty", ([f"only {len(names) - 2} topic playlists: {list(names)}"] if len(names) < 7 else []) + [n for n, c in names.items() if c == 0])
fut = sorted((dt.datetime.fromisoformat(v["status"]["publishAt"].replace("Z", "+00:00")), T(v), short(v)) for v in V if v["status"].get("publishAt") and v["status"]["privacyStatus"] == "private")
bad = [f"{a[0]:%d %b %H:%M} '{a[1][:30]}' and {b[0]:%d %b %H:%M} '{b[1][:30]}' are {(b[0] - a[0]).total_seconds() / 3600:.0f} h apart" for a, b in zip(fut, fut[1:]) if (b[0] - a[0]).total_seconds() < 12 * 3600]
bad += [f"{t:%a %d %b %H:%M} UTC '{n[:30]}' is off the slot" for t, n, s in fut if (s and (t.hour, t.minute) != (16, 0)) or (not s and (t.weekday(), t.hour, t.minute) != (4, 15, 0))]
chk("V7 schedule: >=12 h apart, Shorts 16:00 UTC, long Fri 15:00 UTC", bad, f"{len(fut)} scheduled; applies only if the owner approved D1/D5")
src = open(os.path.join(ROOT, "lib/upload_shorts.py")).read(); st = open(os.path.join(ROOT, "lib/yt_stats.py")).read()
chk("V8 code + files", [x for x, c in (("upload_shorts.py still adds #Shorts to titles", 'title += " #Shorts"' in src), ("yt_stats.py lacks engagedViews", "engagedViews" not in st),
     ("yt_stats.py lacks relativeRetentionPerformance", "relativeRetentionPerformance" not in st), ("topic_results.md missing", not os.path.exists(os.path.join(ROOT, "topic_results.md"))),
     ("branding/TrueWhys_channel_text.md missing", not os.path.exists(os.path.join(ROOT, "branding/TrueWhys_channel_text.md")))) if c])
AI = re.compile(r"\b(AI|A\.I\.|artificial intelligence|AI-generated|generated by)\b")
chk("V9 synthetic-media field = No (owner 16 Nov), no AI wording", [f"{v['id']} field Yes" for v in V if v["status"].get("containsSyntheticMedia") is True] + [f"{v['id']} No not recorded" for v in V if v["id"] not in json.load(open("docs/audit/ai_no.json"))] + [f"{v['id']} wording" for v in V if AI.search(T(v) + " " + v["snippet"]["description"])] + (["channel text wording"] if AI.search(cd) else []))
ok = sum(r["ok"] for r in res.values())
print(f"\n{ok}/{len(res)} checks pass · {len(V)} videos · {now:%d %b %Y %H:%M} UTC")
json.dump(dict(at=now.isoformat(), videos=len(V), checks=res), open(os.path.join(ROOT, f"docs/audit/verify_{now:%Y-%m-%d}.json"), "w"), indent=1, ensure_ascii=False)
