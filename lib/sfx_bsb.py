"""Fetch CC0 sounds from BigSoundBank (Joseph Sardin, CC0). python lib/sfx_bsb.py [name=query ...]
With arguments only those sounds are fetched; credits.json is merged, never overwritten."""
import re, json, urllib.request, urllib.parse, time, sys
from pathlib import Path
OUT = Path("library/sfx/bsb"); OUT.mkdir(parents=True, exist_ok=True)
Q = {"pig": "pig", "rooster": "rooster", "crowd": "crowd", "crowd_murmur": "murmur", "church_bell": "church bell", "bell": "bell",
     "fire": "fire", "birds": "birds", "wind": "wind", "mouse": "mouse", "rat": "rat", "cat": "cat", "insects": "insects", "fly": "fly",
     "owl": "owl", "footsteps": "footsteps cobblestones", "gavel": "gavel", "hammer": "hammer wood", "coins": "coins", "crowd_laugh": "laugh crowd",
     "gasp": "surprise crowd", "applause": "applause", "drum": "drum", "whoosh": "whoosh", "dog": "dog", "chewing": "chewing", "scroll": "parchment", "quill": "quill"}
if len(sys.argv) > 1:
    Q = dict(a.split("=", 1) for a in sys.argv[1:])
cred = json.loads((OUT / "credits.json").read_text()) if (OUT / "credits.json").exists() else {}
UA = {"User-Agent": "Mozilla/5.0 (TrueWhys research)"}
for name, q in Q.items():
    html = urllib.request.urlopen(urllib.request.Request("https://bigsoundbank.com/search?q=" + urllib.parse.quote(q), headers=UA), timeout=30).read().decode("utf8", "ignore")
    hits = re.findall(r"<a href='/([a-z0-9\-]+)-s(\d+)\.html'>", html)
    seen = []
    for slug, sid in hits:
        if sid not in [s for _, s in seen]:
            seen.append((slug, sid))
    for slug, sid in seen[:3]:
        f = OUT / f"{name}__{slug}_{sid}.mp3"
        if not f.exists():
            try:
                f.write_bytes(urllib.request.urlopen(urllib.request.Request(f"https://bigsoundbank.com/UPLOAD/mp3/{sid}.mp3", headers=UA), timeout=60).read())
            except Exception as e:
                print("fail", sid, e); continue
            time.sleep(0.5)
        cred[f.name] = dict(title=slug, url=f"https://bigsoundbank.com/{slug}-s{sid}.html", author="Joseph Sardin (BigSoundBank)", license="CC0")
    print(name, [s for s, _ in seen[:3]])
(OUT / "credits.json").write_text(json.dumps(cred, indent=1))
