# QA — B-003 10 Pirate Myths You Still Believe (And What Was Real)
Final: final/B-003.mp4 (not committed, ~5:37, 1920×1080 30 fps, H.264/AAC). Rebuild: fetch plates from Kaggle kernels
anam318/truewhys-render-b003 + b003b into renders/plates, rebuild voice lines (`python lib/voice_gemini.py <ep> 0,1,2,3,4,5,6`, uses the FLAC
masters, then restore timing.json from git), music (`python lib/music.py library/music/procedural`), then compose.

- [x] Animatic/stills check: every shot's still checked before the Kaggle render (11–12 Nov: plank, chest, rail, port close-ups fixed and re-planned).
      Owner approved the episode and its production through scheduling (handover 12 Nov); standing permission to upload without preview.
- [x] Hook: frame 1 = eye-patch pirate + "EYE PATCHES?" on screen; each item opens on its strongest image (growth review 11 Nov).
- [x] Visual change at least every 5 s (85 shots in 5:37, avg 4.0 s; only the 20 s end screen is longer); rank cards 1→10 every ~25–30 s.
- [x] Final frames are full-resolution Kaggle GPU renders (71/71 3D plates); nothing blurry or upscaled.
- [x] Consistent cast, lighting and colour; captions readable, in brand style, not covering faces (contact sheet 13 Nov, 20 frames).
- [x] Voice checked against the script (faster-whisper on 2:30–3:10 matches lines; voice rebuilt from the Gemini masters, per-line starts
      from the committed timing.json). Loudness −14.5 LUFS integrated, true peak −2.4 dBFS.
- [x] Every claim in sources.md (2+ sources each); every asset in credits.md (all original or CC0).
- [x] Ethics: nothing against any religion, no mockery of groups, no gore; violence only implied (flags, "no mercy" card); no real faces/logos.
- [x] End screen: 20 s with the TrueWhys wordmark, Watch next / More true whys / Subscribe areas.
- [x] YouTube category 24 (Entertainment, owner rule 12 Nov); no AI/altered field; no AI mention in title, description or tags.
- [x] 3 very different thumbnails (final/thumb_A "NOT BLIND?!" eye patch, B "NO TREASURE?!" captain + coins, C "VOTED OUT?!"), readable at 168×94.
Result: PASS → YouTube private + publishAt 2026-11-14T15:00:00Z with thumb_A; owner gets A/B/C for Test & Compare.
