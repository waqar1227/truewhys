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
- [ ] Cut Shorts C0–C7 (vertical 1080×1920 renders on Kaggle)

## Notes
- Freesound and kenney.nl block this server (403). Use BigSoundBank (CC0) and OpenGameArt CC0 packs.
- Kaggle: dataset must be flat (no sub-folders); use OIDN denoiser (OptiX weights missing).
- Gemini TTS free tier: 10 requests/day/model; Pro TTS has no free quota.
- YouTube token scopes: upload, force-ssl (comments/playlists), analytics read-only.
