"""Rebuild the human-readable credits for the real sound + music libraries from their credits.json files.
/opt/c3d/bin/python tools/real_audio_credits.py  -> library/sfx/real/credits.md, library/music/real/credits.md"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
s = json.loads((ROOT / "library/sfx/real/credits.json").read_text())
out = ["# Real sound effects + ambiences (library/sfx/real)", "",
       "All CC0 1.0 (public domain) recordings from Freesound.org; credit not required but kept here. Processed: 48 kHz, silence trimmed,",
       "SFX peak -1 dBFS (max 6 s), ambiences RMS -26 dBFS (loopable, max 58 s). Fetch/refresh: tools/fetch_real_sfx.py.", "",
       "| name | category | Freesound title | author | sec | link |", "|---|---|---|---|---|---|"]
for k, v in sorted(s.items(), key=lambda kv: (kv[1]["category"], kv[0])):
    out.append(f"| `{k}` | {v['category']} | {v['title'].replace('|', '/')} | {v['author']} | {v['seconds']} | {v['url']} |")
(ROOT / "library/sfx/real/credits.md").write_text("\n".join(out) + "\n")
m = json.loads((ROOT / "library/music/real/credits.json").read_text())
out = ["# Real-instrument music (library/music/real)", "",
       "Kevin MacLeod (incompetech.com), licence CC BY 4.0. **Every video that uses a track must have its exact credit in the description**",
       "(lib/audio writes the used lines to episodes/<ep>/audio/music_credits.txt; lib/youtube.py refuses an upload without them).",
       "Processed: 48 kHz stereo, -18 LUFS, max 4 min. Fetch/refresh: tools/fetch_real_music.py.", ""]
for k, v in sorted(m.items()):
    out += [f"## {k}  ({v['instruments']}; {v['feel']}; {v['seconds']} s)", "```", v["credit"], "```", ""]
(ROOT / "library/music/real/credits.md").write_text("\n".join(out))
print(len(s), "sfx,", len(m), "tracks")
