# STATUS (read the NEXT list first)

## NEXT (keep this list short; heartbeat does only these)
1. B-001 Shorts C0–C7: after re-compose finishes, quick QA (one small sheet), then upload each:
   `python lib/youtube.py upload episodes/B-001-animal-trials/shorts/<CID>/final.mp4 episodes/B-001-animal-trials/shorts/<CID>/upload_meta.json --long 9C-9O0c6VqM`
   then `python lib/crosspost.py episodes/B-001-animal-trials`.
2. Sun 8 Nov ≥ 08:00 UTC: B-002 Gemini chapter voice (`python lib/voice_gemini.py episodes/B-002-worst-jobs`, 9 requests) → `plan.py` → `lib/shorts.py`.
3. Sun 8 Nov ≥ 15:00 UTC: post + pin the B-001 comment (text in upload_meta.json "pinned_comment").
4. Mon 9 Nov ≥ 00:30 UTC: B-002 part 2 plates on Kaggle (dataset truewhys-ep-b002, kernel truewhys-render-b002 with JOB='job_D.json').
5. Waiting on owner: Facebook long-lived Page token; hosting choice for Metricool (A file host / B manual). Packages in episodes/<ep>/social/.

## History

## Now: B-001 "Why Medieval Courts Put Animals on Trial" (7:38)
- [x] Research, script (85 lines), sources, topic
- [x] Shot plan (103 shots), sets, cast, compositor, music, SFX
- [x] Thumbnails A/B (final/thumb_A.jpg, thumb_B.jpg)
- [x] Kaggle final plates: 82/82 (6 Nov 23:31 UTC), in renders/ (not committed)
- [ ] Gemini voice ch0–7 after quota reset (08:00 UTC 7 Nov): `python lib/voice_gemini.py episodes/B-001-animal-trials` → `python episodes/B-001-animal-trials/plan.py`
- [ ] Final compose: `python lib/compose.py episodes/B-001-animal-trials --plates episodes/B-001-animal-trials/renders --out episodes/B-001-animal-trials/final/B-001.mp4`
- [ ] QA (qa.md), upload package: `python lib/upload_pkg.py episodes/B-001-animal-trials 2026-11-08T15:00:00Z`
- [ ] Upload private + publishAt 2026-11-08T15:00:00Z (lib/youtube.py), containsSyntheticMedia=false
- [ ] Cut Shorts C0–C7: vertical 1080×1920 plates on Kaggle, compose, QA — must be finished BEFORE scheduling B-001

## Release plan
- **Owner rule (7 Nov): schedule every QA-passed episode + its Shorts on YouTube immediately; never hold finished videos; no owner preview needed.**
- B-001 long video → all its cut Shorts (C0–C7) within the next 24 h, ~1 every 3 h (rendered + QA'd before the long video goes live) → standalone Shorts (new categories) in the following days → then B-002.
- No fixed dates: B-001 publishes only after every shot passes QA. Target Sun 8 Nov 15:00 UTC if QA passes.

## Quality upgrades before the B-001 final (owner: first impression matters)
- [x] Puppet shading: soft cel shadow + rim light matched to each set's key light
- [x] More set dressing (props, banners, plants, crowd depth) in square/court/vineyard
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
- B-002 draft written (episodes/B-002-worst-jobs): "Would You Survive These 8 Jobs From Old England?" — ranked list, category 3,
  987-word script v1, sources table (2+ per claim). Owner approved (6 Nov); title chosen: "Would You Survive These 8 Jobs From Old England?".
  Gemini quota: B-001 uses 9 requests on 7 Nov, so B-002 voice (9 requests) is 8 Nov at the earliest.

## Update 6 Nov 2026, 20:50 UTC
- Kaggle final plates still running (both kernels), expected ~23:30 UTC; waiter armed.
- Shorts upload packages ready: `python lib/upload_shorts.py episodes/B-001-animal-trials <long publishAt>` →
  shorts/<CID>/upload_meta.json + upload_shorts.md (C0 +1 h, then every 3 h, all within 24 h).
- lib/youtube.py: `--long <id>` fills the full-story link, adds to playlist, posts the pinned comment, writes uploaded.json (no double uploads).
  Related video on each Short is set in YouTube Studio (not in the API) — tell the owner after upload.

## Update 7 Nov 2026, 02:50 UTC
- B-001: all 82 long-video plates rendered + QA'd (night wall rebuilt, two edge-cropped characters fixed). Test edit of ch 4 sent to owner.
- B-001 next: Gemini voice after ~08:00 UTC (9 requests) → plan.py → shorts.py → Shorts plates on Kaggle → final compose, mix, QA.
- B-002: Kokoro guide voice, shot plan (98 shots, 6:41), preview stills, **animatic v1 sent to owner for approval**
  (episodes/B-002-worst-jobs/animatic/animatic_v1_kokoro.mp4, not committed: 60 MB). Coroners' Roll fact verified.
- Shorts upload packages ready (lib/upload_shorts.py); uploader handles playlist, comment, long-video link.

## How to resume in a new Claude Code account (if access is ever lost)
1. Connect GitHub and open the private repo **TrueWhys**, branch `claude/laughing-newton-g4f09n` (all work is here).
2. Create a cloud environment "TrueWhys" (network Full) and re-enter the keys: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN,
   KAGGLE_USERNAME, KAGGLE_API_TOKEN, FREESOUND_API_KEY, PIXABAY_API_KEY, SKETCHFAB_API_TOKEN, and the Gemini key as a network secret.
3. Ask Claude to read CLAUDE.md and STATUS.md, run setup.sh, regenerate music (`python lib/music.py library/music/procedural`),
   and re-create the scheduled heartbeat (every 4 h).
4. Rendered plates: re-download from Kaggle (`kaggle kernels output waqarahmed51/truewhys-render-<id>`) into episodes/<id>/renders/.
   Voices: regenerate with lib/voice_gemini.py (or Kokoro lib/voice.py). Uploaded videos live on YouTube.

## Update 7 Nov 2026, 18:10 UTC
- **B-001 uploaded and scheduled on YouTube:** https://youtu.be/9C-9O0c6VqM — private, publishAt 2026-11-08T15:00:00Z, thumb_A, playlist Full Stories.
  TODO after 15:00 UTC 8 Nov: post + pin the comment (API refused before publish); owner sets nothing else.
- B-001 Shorts: composed, QA'd; 5 re-composed with pop-word fit fix → then upload with `--long 9C-9O0c6VqM` (slots +1 h, every 3 h).
- Facebook: Page ID/name in env, token as network secret for graph.facebook.com — **token expired 7 Nov 17:00 UTC (short-lived)**; owner must save a long-lived Page token.
- TikTok: connected in Metricool (brand id 7942824, account "truewhys", timezone Asia/Karachi). Metricool needs a public video URL.
- Social packages: `python lib/crosspost.py episodes/<ep>` → social/plan.json + README.md (captions, times, files). B-001: 15 posts ready
  (7 TikTok + 7 Facebook Reels from 16:30 UTC 8 Nov, long video on Facebook 15:00 UTC 9 Nov). Waiting for: Facebook long-lived token,
  owner's choice of hosting for Metricool (A: file host, B: manual upload).
- B-002 part 2 plates (chapters 4–8, job_D, ~5 h): start Mon 9 Nov ≥ 00:30 UTC (new Kaggle week; this week ≈ 26.6 h used).
- B-002 Gemini chapter voice: 8 Nov after 08:00 UTC (9 requests), then plan.py, compose, QA, schedule.
