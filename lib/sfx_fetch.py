"""Fetch CC0 sound effects from Freesound (API key from FREESOUND_API_KEY, sent only to freesound.org).
python lib/sfx_fetch.py  -> library/sfx/<name>.mp3 + library/sfx/sfx_credits.json"""
import os, json, urllib.request, urllib.parse, time
from pathlib import Path
KEY = os.environ["FREESOUND_API_KEY"]
OUT = Path("library/sfx"); OUT.mkdir(parents=True, exist_ok=True)
WANT = {
 "gavel": "gavel hit", "crowd_murmur": "crowd murmur medieval", "crowd_gasp": "crowd gasp", "crowd_laugh": "crowd laugh",
 "pig_oink": "pig oink", "pig_squeal": "pig grunt", "rat_squeak": "mouse squeak", "cat_hiss": "cat hiss", "cat_meow": "cat meow",
 "rooster": "rooster crow", "church_bell": "church bell single", "whoosh": "whoosh swish", "whoosh_soft": "soft whoosh transition",
 "coins": "coins drop", "coin_single": "coin drop single", "paper": "paper scroll unroll", "page_turn": "page turn", "quill": "quill writing",
 "insects": "insects buzzing swarm", "fire": "bonfire crackling", "wind": "wind gentle", "birds": "birds morning countryside",
 "footsteps": "footsteps cobblestone", "door": "wooden door creak", "pop": "pop cartoon", "ding": "ding bell small",
 "sparkle": "sparkle chime", "drum_hit": "dramatic drum hit", "riser": "riser tension", "boing": "cartoon boing",
 "gulp": "gulp swallow", "thud": "wood thud", "tick": "clock ticking", "owl": "owl hoot night", "chain": "chain rattle",
 "room_tone": "indoor room tone", "market": "market crowd ambience", "chewing": "insect chewing crunch", "hmm": "cartoon question",
}
H = {"Authorization": "Token " + KEY}
cred = json.loads((OUT / "sfx_credits.json").read_text()) if (OUT / "sfx_credits.json").exists() else {}
for name, q in WANT.items():
    if (OUT / f"{name}.mp3").exists():
        continue
    url = "https://freesound.org/apiv2/search/text/?" + urllib.parse.urlencode({
        "query": q, "filter": 'license:"Creative Commons 0" duration:[0.2 TO 30]', "sort": "rating_desc",
        "fields": "id,name,username,license,url,previews,duration,avg_rating,num_ratings", "page_size": 8})
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=30))
    except Exception as e:
        print("search fail", name, e); time.sleep(2); continue
    res = [x for x in r.get("results", []) if "Creative Commons 0" in x["license"] or "publicdomain/zero" in x["license"]]
    if not res:
        print("none", name); continue
    x = res[0]
    try:
        data = urllib.request.urlopen(urllib.request.Request(x["previews"]["preview-hq-mp3"], headers=H), timeout=60).read()
    except Exception as e:
        print("dl fail", name, e); continue
    (OUT / f"{name}.mp3").write_bytes(data)
    cred[name] = dict(id=x["id"], title=x["name"], author=x["username"], license=x["license"], url=x["url"], duration=x["duration"])
    print("ok", name, x["name"], x["username"], round(x["duration"], 1))
    time.sleep(1.2)
(OUT / "sfx_credits.json").write_text(json.dumps(cred, indent=1))
