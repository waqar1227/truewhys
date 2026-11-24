# STATUS (read the NEXT list first)

## NEXT (keep this list short; heartbeat does only these)
(22 Nov) Read only: this list, CLAUDE.md, and the files a task names. Older notes: docs/status_archive_2026-11-22.md.
Rules added 22 Nov (all in CLAUDE.md): 5 posts/week, 1 per day, Mon+Wed free, long Sun 17:00, Shorts Tue/Thu/Fri/Sat 18:00 UTC
(docs/posting_times.md) · trend swap allowed · NO burned-in captions (SRT upload) · research/why_not_viral.md production rules ·
docs/growth_strategy.md · docs/competitor_targeting.md (never creator names in metadata) · cast v2.2 (arms/turns) · 30 days scheduled → STOP.

CALENDAR (UTC). Scheduled: Sun 22 A-021 · Mon 23 16:00 A-025 T3CvD2HqRaE (trend swap, owner 23 Nov; A-017 moved to Tue 22 Dec 18:00) · Tue 24 A-012 · Wed 25 A-011 · Thu 26 A-013 · Fri 27 A-018 · Sun 29 17:00 L4 dgmYB0zPALw ·
Tue 1 Dec 18:00 L4-C1 PtETjFRHH24 · Thu 3 Dec 16:00 A-010 · Fri 4 Dec 18:00 L4-C2 cXgM0GJELw0 · Sat 5 Dec 18:00 A-019 1I_m4OaiQzE · Sun 6 Dec 16:00 A-016 · Fri 11 Dec 18:00 A-022 VAUl6EfZebw · Fri 18 Dec 18:00 A-023 3ZAI7vLZZkE (foot asleep, Style F) · Tue 22 Dec 18:00 A-017 S8zIxiPXHpE (moved).
IN PRODUCTION (22 Nov): Mon 7 Dec 17:00 L5 + teaser post (own session session_01BQj2DeXWy7q3QfcuAZWsgi) · Tue 8 + Thu 10 Dec 18:00 L5 cut Shorts (L5 session).
IN PRODUCTION (23 Nov): Sat 19 Dec 18:00 A-024 microwave mesh (Kaggle a024) (next: re-render hook_pov,loop_pov on Kaggle, then QA + upload). DONE: A-025 T3CvD2HqRaE scheduled Mon 23 Nov 16:00 UTC, SRT up.
FREED: Tue 15 Dec 18:00 slot (needs a standalone Short). Each: renders → `make.py render renders` → QA → thumb → upload → SRT → registers.
TO MAKE (plan 24 Nov, 30 days = to Thu 24 Dec): · L6 Sun 13 Dec 17:00 + teaser (post Fri 11 Dec) + cut Short Thu 17 Dec 18:00 → own session session_01BQj2Df4JPxwNVo9AyHLbzz ·
Production session: A-024 fix render (Kaggle a024 v2, 24 Nov) → upload Sat 19 Dec · Shorts A-026 Tue 15 Dec + A-027 Thu 24 Dec 18:00 → own session session_01BQj2De9mH8PfbfkZem9mEC ·
L7 Sun 20 Dec 17:00 → start its own fresh session when L6 is done · then STOP until the schedule drops below 30 days (heartbeat adds the next slot each day).
Spare (made, not scheduled): L4-C3 caps, L4-C4 manholes.

TASKS in order:
0. L4 UPLOADED dgmYB0zPALw (Sun 29 Nov 17:00 UTC, SRT up, thumb A). After it is public (29 Nov 17:00): give the owner the pinned comment
   (upload_meta.json pinned_comment) and send thumbs B/C (final/) for Test & Compare.
1. OWNER (told 22 Nov): Studio → Related video = L4 (dgmYB0zPALw) on PtETjFRHH24 and cXgM0GJELw0.
2. 48-h checks into topic_results.md (stayed %, rel. retention 10 %, drop point): A-021 on 24 Nov, A-017 25 Nov, A-012 26, A-011 27, A-013 28,
   A-018 29 Nov (`python3 lib/yt_stats.py 7`). Compare Style R (A-016/17/18/21) vs Style F.
3. DONE 23 Nov: A-019 + A-022 uploaded (private + publishAt, thumb, SRT, AI field No, registers). Kaggle: a019+a022 v1+v2 used ≈ 3.7 h session time (render_log.md).
4. L5 DONE (23 Nov): B-005 "Why Toast Lands Butter-Side Down, Shoelaces Untie and Earbuds Tangle" UPLOADED l_w8yDvCZiI (Mon 7 Dec 17:00 UTC, SRT, thumb A);
   cut Shorts C1 toast 7LX7R8f7GB4 (Tue 8 Dec 18:00) + C2 spaghetti Ydk7QtOzx7M (Thu 10 Dec 18:00), SRT + thumbs. OWNER: Related video = L5 on both;
   post the teaser (episodes/B-005-annoying-science/social/post) Sat 5 Dec. After 7 Dec 17:00: pinned comment (upload_meta.json) + send thumbs B/C.
5. Trending standalone Shorts: pick on the day from Google Trends/competitor radar; trend swap rule if something goes viral.
Never: change A-020 (owner edited) · move scheduled videos except a trend swap · creator names in metadata.

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
