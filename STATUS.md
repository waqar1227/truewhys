# STATUS (read first on every heartbeat)

## Now: B-001 "Why Medieval Courts Put Animals on Trial" (7:38)
- [x] Research, script (85 lines), sources, topic
- [x] Shot plan (103 shots), sets, cast, compositor, music, SFX
- [x] Thumbnails A/B (final/thumb_A.jpg, thumb_B.jpg)
- [ ] Kaggle final plates: chapter 0 benchmark running (kernel waqarahmed51/truewhys-render-b001) → then chapters 1–7
- [ ] Gemini voice ch0–7 after quota reset (08:00 UTC 7 Nov): `python lib/voice_gemini.py episodes/B-001-animal-trials` → `python episodes/B-001-animal-trials/plan.py`
- [ ] Final compose: `python lib/compose.py episodes/B-001-animal-trials --plates episodes/B-001-animal-trials/renders --out episodes/B-001-animal-trials/final/B-001.mp4`
- [ ] QA (qa.md), upload package: `python lib/upload_pkg.py episodes/B-001-animal-trials 2026-11-08T15:00:00Z`
- [ ] Upload private + publishAt 2026-11-08T15:00:00Z (lib/youtube.py), containsSyntheticMedia=false
- [ ] Cut Shorts C0–C7: vertical 1080×1920 plates on Kaggle, compose, QA — must be finished BEFORE scheduling B-001

## Release plan
- B-001 long video → all its cut Shorts (C0–C7) within the next 24 h, ~1 every 3 h (rendered + QA'd before the long video goes live) → standalone Shorts (new categories) in the following days → then B-002.
- No fixed dates: B-001 publishes only after every shot passes QA. Target Sun 8 Nov 15:00 UTC if QA passes.

## Quality upgrades before the B-001 final (owner: first impression matters)
- [ ] Puppet shading: soft cel shadow + rim light matched to each set's key light
- [ ] More set dressing (props, banners, plants, crowd depth) in square/court/vineyard
- [ ] Motion: camera moves checked in animatic; no static moments > 5 s
- [ ] Sound pass: listen-test by measurement (loudness, ducking, SFX levels)
- [ ] Full watch-through QA of the final at 1080p, contact sheet of every shot

## Notes
- Freesound and kenney.nl block this server (403). Use BigSoundBank (CC0) and OpenGameArt CC0 packs.
- Kaggle: dataset must be flat (no sub-folders); use OIDN denoiser (OptiX weights missing).
- Gemini TTS free tier: 10 requests/day/model; Pro TTS has no free quota.
- YouTube token scopes: upload, force-ssl (comments/playlists), analytics read-only.

## Update 6 Nov 2026, 16:50 UTC
- Final long-video plates rendering on Kaggle (2 runs in parallel, chapters 0–3 and 4–7), expected done ~23:30 UTC.
- Vertical Shorts generator done (lib/shorts.py): 7 Shorts planned, 28–63 s, re-aimed 9:16 cameras, hooks open on the strongest shot,
  documents zoomed for phones, Wy end card. Short plates render on Kaggle after the hook voice exists (7 Nov).
- 7 Nov after ~08:00 UTC: Gemini voice for chapters 0–7 (8 requests) + all hooks/outro (1 request), then plan.py, final compose, QA.
