# STATUS (read the NEXT list first)

## NEXT (keep this list short; heartbeat does only these)
0. Daily growth review = separate scheduled task (fresh Sonnet session, 07:13 UTC): `bash tools/daily.sh` → entry in research/daily_report.md. Heartbeat does NOT repeat it; it reads the latest entry before any new script/title. 48 h check of A-001/A-004 titles (emoji test): 13–14 Nov.
   A-001 Quicksand: DONE + SCHEDULED on YouTube (MLRRsaV4iUA, public 11 Nov 22:00 UTC = 03:00 PKT 12 Nov, QA pass, thumb set). TikTok SCHEDULED via Metricool 22:30 UTC 11 Nov (id 424053522; final re-composed from Kaggle plates); title "Why Quicksand Can't Actually Swallow You", end caption "Watch the full video on YouTube — @TrueWhys"? (standalone: use "More true whys on YouTube — @TrueWhys").
   A-004 Tickling: DONE + SCHEDULED on YouTube (sdoOC7kAuRU, public 12 Nov 22:00 UTC, QA pass, thumb set; title ends with 🪶 = A/B vs A-001). TikTok SCHEDULED via Metricool 22:30 UTC 12 Nov (id 424045584). Plates: Kaggle truewhys-render-a004.
   NEXT EPISODE = A-002 "Why You Should Never Eat Polar Bear Liver" (shorts_plan.md, category 8 Animals). Same steps as A-004: lines.txt (25–40 s, payoff before 20 s) + sources.md + topic.md → Gemini voice → plan.py + stills sheet → Kaggle (copy notebooks/kaggle_jobs/a004; compose with --w 1080 --h 1920, mkdir final/ first) → QA → YouTube slot 22:00 UTC 13 Nov + TikTok +30 min. Keep animated (step 1) shots few: they double render time. Compare A-001 (no emoji) vs A-004 (emoji) at 48 h before choosing A-002 title style.
   A-002 hook (growth review 11 Nov): show the liver/danger payoff image in the first 2 s; every Short drops hardest at 10–19 %.
Fresh session? Tools install via the environment setup script (tools/setup_env.sh). Rendered plates are not in git: fetch them from Kaggle.
1. DONE 8 Nov 09:30 UTC: B-002 Gemini voice (9 chapters, FLAC masters committed), plan.py (98 shots, 6:11), shorts.py (8 Shorts 38–46 s).
   Still to do when scheduling: `python lib/upload_pkg.py episodes/B-002-worst-jobs <publishAt>`.
2. DONE (comment posted; owner pins): post + pin the B-001 comment on 9C-9O0c6VqM (text: episodes/B-001-animal-trials/upload_meta.json "pinned_comment").
3. DONE 9 Nov 11:00 UTC: B-002 long video composed + QA passed (final/B-002.mp4, 6:11, −14.5 LUFS; qa.md ticked; credits.md written).
   final/B-002.mp4 is NOT in git (200 MB): if a fresh session lacks it, re-fetch plates from Kaggle kernels truewhys-render-b002 / b002b and re-compose.
4. DONE 10 Nov 01:40 UTC: B-002 fully SCHEDULED on YouTube (private + publishAt), QA in qa.md.
   Long h2oO3SrSUH8 PUBLIC since 10 Nov 03:50 UTC (owner published it early; owner runs Test & Compare with thumb_B + thumb_C).
   Shorts moved to follow within 24 h: C8 FbtDoZL8vwk 10 Nov 05:00, C2 66iyJcnwvgY 08:00, C3 WqxkoJY4jy4 11:00, C4 qCgG6Dhqgi4 14:00,
   C5 Wu5-PLKwb48 17:00, C6 kk6I9g5V82Y 20:00, C7 6wDhznnQeKI 23:00, C1 TkNJsIdy7gs 11 Nov 02:00 UTC. Owner: set Related video = the long video on each Short (Studio).
   DONE 10 Nov 04:10 UTC: B-002 comment posted (owner pins it in Studio).
   DONE 10 Nov 10:25 UTC: TikTok for B-002 = 4 Shorts via Metricool (owner: no more): C8 18:00, C2 23:00 UTC 10 Nov, C3 18:00, C4 23:00 UTC 11 Nov
   (ids in social/tiktok_posted.json; Dropbox copies deleted).
5. FACEBOOK PAUSED by owner (8 Nov): no Facebook work until he gives the go-ahead. Posts made with the unpublished Meta app stay hidden
   (owner tested editing + publishing them himself: still hidden). Options if he asks: Meta Business Suite manual packs, or Zapier. (Scheduled B-001 Reels C7–C1 + banner still sit in Facebook's scheduler.)
   Cross-posting B-001 (8 Nov): Facebook Reels C0–C7 scheduled via Page token (lib/fb_post.py, ids in social/posted.json); banner scheduled 21:00 UTC.
   B-001 comment posted on YouTube 15:05 UTC (owner pins it in Studio; the API cannot pin). Trailer NOT made: YouTube blocks downloads from
   this server and the B-001 long plates were overwritten on Kaggle → owner chose to SKIP the B-001 trailer (8 Nov); B-001 Facebook = 7 Reels + banner only.
   C0 published early on owner's request (8 Nov ~15:22 UTC: YouTube public, FB Reel live, TikTok 15:30 UTC = Metricool id 420823459).
   FB first comments BLOCKED: Page token lacks pages_manage_engagement / pages_read_user_content (#200). Waiting for owner's new token;
   then every heartbeat: `python lib/fb_post.py <ep> comments`.
   TikTok: all 7 B-001 Shorts scheduled in Metricool (ids 420686149…420686951, 16:30 UTC 8 Nov → 10:30 UTC 9 Nov), owner gave a one-off fresh
   Dropbox token; Dropbox copies deleted. From B-002 on: TikTok direct API (owner's keys ~10–11 Nov). Owner: set Related video on B-001 Shorts.
6. DONE 10 Nov 01:10 UTC: shorts_plan.md written (7 standalone Shorts A-001…A-007 ranked by hook; A-003 = first Style R test).
   NEXT: for A-001…A-007 in plan order: script + sources.md + topic.md → Kokoro draft → animatics → send all 7 to owner for approval
   → Gemini voice (1 request/Short) → Kaggle vertical plates → compose → QA → schedule on YouTube (22:00 UTC daily slots from 11 Nov)
   AND on TikTok via Metricool (owner 10 Nov: every standalone Short goes to TikTok too, 30 min after its YouTube slot; Dropbox link needs a fresh owner token). Then episode 3
   ("What Did ___ Actually Do All Day?", 8–10 min).

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
