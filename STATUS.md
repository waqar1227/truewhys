# STATUS (read the NEXT list first)

## NEXT (keep this list short; heartbeat does only these)
(19 Nov 10:25 UTC) EPISODE L4 (long video + 3–4 cut Shorts) is made in session_01BQj2Dd62mCxqrytuRaL8gE; the daily heartbeat 08:20 UTC wakes it
(trig_01U9ha9sUaxEmdjvYwdNiuef). Growth review: session_01BQj2Ddx5onh4fxoyVPNSuk (Sonnet) 07:13 UTC (trig_011uF6VcThSztFE5aQ3rWwSv). Old fresh-session tasks
deleted (they had no repo; the 18/19 Nov runs did not happen). Plan: L4 Fri 27 Nov 15:00 UTC; cut Shorts Sat 28 – Tue 1 Dec 16:00 UTC (audit §4).
!! AFTER YOUTUBE QUOTA RESET (08:00 UTC daily) — DO FIRST, before anything else, then tick here:
   [x] 1. AI field = No on ALL 43 videos (17 Nov 08:10; tools/yt_ai_no.py; YouTube's GET hides "false", so proof = docs/audit/ai_no.json, dry run says 0 left).
   [x] 2. thumb_v2 set on the 7 scheduled Shorts (17 Nov; uploaded.json thumbnail_file updated).
   [x] 3. yt_apply_fixes --apply: the 6 B-003 fixes done (17 Nov; script now ignores tag order).
   [~] 4. (20 Nov 09:44: B-001 DONE, caption id saved by YouTube; quotaExceeded again → B-002 + B-003 still to do) SRT captions: files READY (episodes/B-00*/final/captions_en.srt, timing matches live length ±1 s). Quota ran out again 17 Nov ~08:20 →
          after 18 Nov 08:00 UTC: `python3 tools/make_srt.py episodes/B-001-animal-trials --upload 9C-9O0c6VqM`, same for B-002 h2oO3SrSUH8, B-003 Am8epkS94Hw (~400 units each).
   [ ] 5. `python3 docs/audit/verify.py` (needs quota) → commit, push, short message to the owner.
   If quota runs out midway: leave the unticked items here for the next reset.
** L4 = B-004 "Why Everyday Things Are Shaped So Weirdly" (working title) — production session_01BQj2Dd62mCxqrytuRaL8gE, started 19 Nov.
   Style F + cast v2.1, 1920x1080, 6:17 (narration 5:20 + chapter breaks + 20 s end screen), cat 28. Slot Fri 27 Nov 15:00 UTC.
   Cut Shorts (vertical, rewritten, §6.3): C1 coin ridges/Newton · C2 stop signs were yellow · C3 bottle cap 21 teeth → Gillette · C4 round manholes;
   slots Sat 28, Sun 29, Mon 30 Nov, Tue 1 Dec 16:00 UTC.
   DONE 19 Nov: topic.md (10 titles, religion check: clear), sources.md (2+ per claim), lines.txt, Gemini voice ch0–8 (FLAC in voice/; 10 requests used
   19 Nov), make.py (71 shots, 9 chapters, end screen), animatic/stills.jpg checked once. New: lib/flat_shapes.py props, 10 cast v2.1 roles in lib/cast2.py,
   flat2d 16:9 via TW_FLAT_SIZE.
   20 Nov: animatic polished (99 shots, every shot ≤ 5.9 s; GB map, square-lid top view, CLANG cut-away), animatic/animatic.mp4 rendered (6:17, −14.5 LUFS);
   draft thumbs A/B/C (thumbs.py); 4 Shorts scripted + voiced (Gemini 4 req 20 Nov) + composed (shorts/make_short.py C1..C4: frame-1 0.56–0.70, shots ≤ 3 s, 25–30 s, badge, loop).
   NEXT (in order): 1) next reset 08:00 UTC: quota items 4 (B-002, B-003 captions) + 5 first. 2) Polish animatic: split the 24 shots > 5.5 s (`make.py qa` lists them),
   better England map (O04), square-lid fall (C202), bigger characters in street wides; render `make.py animatic`, watch it once.
   3) Shorts: write 4 vertical scripts (20–35 s, frame-1 rule, answer in last 5 s, loop, corner badge) + record hooks with Gemini (≤10 req/day).
   4) 22/23 Nov: `bash tools/daily.sh`, read research/stats/<date>.md (A-009/A-010 48 h) → lock title (shortlist in topic.md), hook, first frames.
   5) Final render (CPU, Style F), 3 thumbnails, seo/upload_meta (ai_disclosure), qa.md, SRT. 6) Upload L4 25 Nov (+captions), Shorts 26–27 Nov (≤5 uploads/day).
** 16 Nov 11:20 UTC (production session_01BQj2DdBXfG9cs6NCxGLzLV; old heartbeat disabled 17 Nov):
   STYLE A/B TEST SETTLED. A-016 v3 (fixed hook_cut + loop_q) QA PASS; A-017 QA PASS. Rescheduled A-012 1r8faDAYoTQ → 24 Nov, A-011 yyBUc7aM2lA → 25,
   A-013 bHC7F6nNwWM → 26. UPLOADED A-016 pwVCqe756X8 → 22 Nov 16:00 UTC, A-017 S8zIxiPXHpE → 23 Nov 16:00 UTC ("thumbnail": true, playlist Why Does That Happen?).
   Schedule: A-009 20 · A-010 21 · A-016 22 · A-017 23 · A-012 24 · A-011 25 · A-013 26 Nov (all 16:00 UTC). Buffer to 26 Nov.
   OWNER RULES 16 Nov (saved in CLAUDE.md): AI field always No (lib/youtube.py sends containsSyntheticMedia=false); Shorts get a custom thumbnail with
   ONE hook/suspense line (tools/short_thumb.py → final/thumb_v2.jpg, made for A-009..A-013, A-016, A-017). YouTube quota ran out 16 Nov →
   17 Nov 08:05 UTC reminder: yt_apply_fixes --apply, SRT captions, `tools/yt_ai_no.py --apply` (43 videos), thumbnails.set thumb_v2 on the 7 Shorts. Audit session asked for NO messages until its 17 Nov 12:00 check (it reads the branch itself).
   17 Nov 08:05–12:00 UTC (quota resets 08:00; audit cross-check 12:00): SRT captions for the 3 long videos; `python tools/yt_apply_fixes.py --apply` (6 B-003 fixes); B1/B2 schedule settled.
   Wave 2 (27 Nov–3 Dec) only after 48 h data on A-009/A-010 (A-010 public 21 Nov 16:00 → data 23 Nov).
** 15 Nov 17:10 UTC — OWNER STYLE A/B TEST (relayed by the audit session, owner's words in its chat): 4 standalone "Why [everyday thing]" Shorts, cat 28, 30–40 s,
   same title pattern/hook/voice/music/no end card/16:00 UTC, 4 different topics + separately written scripts. Order A-B-B-A, right after the pirate Shorts:
   Sat 21 Nov A1 = A-010 Wrinkly fingers (2D cast v2.1, already scheduled; 45 s) · Sun 22 Nov B1 = Style R 3D "Why onions make you cry" (A-016, TO MAKE) ·
   Mon 23 Nov B2 = Style R 3D "Why ice cubes are cloudy" (A-017, TO MAKE) · Tue 24 Nov A2 = A-012 Pen cap hole (2D, now scheduled 23 Nov → move to 24 Nov).
   Then A-011 Traffic light 22 Nov → 25 Nov and A-013 Falling cat 24 Nov → 26 Nov. RESCHEDULE ONLY WHEN B1+B2 HAVE PASSED QA (videos.update status.publishAt,
   ~50 units each; order: A-013→26, A-012→24, A-011→25, then upload B1/B2 at 22/23). If a B Short can't pass QA by its day, swap with the next A and tell the owner.
   Style R build (owner-APPROVED sheet): docs/audit/style_r/ (README, build.py, specs, zipls.py; MPFB 2.0.18 + MakeHuman CC0 assets, asset server slow → zipls.py),
   docs/audit/review/style_r_cast_sheet.jpg. Audit §6.2: studio backdrop in our colours (navy→coral/cream, NOT cyan), one hero prop, shots macro → person → cross-section → result;
   stylised CG only (no photoreal skin/real likeness); poses must move (keyframed rig bones/expressions; no frozen characters); stills/animatic here, FINALS ON KAGGLE GPU
   (anam318, tools/kaggle_px.py, shared: never touch other kernels), ~1 GPU h per Short. Same Gemini voice + music level as the 2D Shorts; frame-1 rule; corner badge, no end card.
   Record all 4 in topic_results.md (style tag F-v2.1 vs R); compare at 48 h and 7 d (views, stayed %, avg % viewed, rel. retention 10 %, subs, likes, comments) → report to owner.
** A-014 Golf-ball dimples: script, sources, voice (voice/ch0.flac) and animatic done (episodes/A-014-golf-ball-dimples, stills checked once, not yet fixed/rendered).
   PARKED: it would fall in wave 2 (after 26 Nov) → finish/render only after the 48 h data on the new-standard Shorts (≈ 23 Nov), then schedule.
** 15 Nov 13:40 UTC (production session): STANDARDS DONE + WAVE 1 HALF SCHEDULED. Composers: lib/cast2_flat.py (cast v2.1 in Style F), no end card (corner badge),
   `V.qa_numbers()` frame-1 check (library/index.md). Style T still has the 3D cast v1 → new videos are Style F until a 3D cast v2 exists.
   Long video can't pass QA by Fri 20 Nov → per order: Style F standalone Shorts hold 20–26 Nov 16:00 UTC; long video L4 → Fri 27 Nov 15:00 UTC.
   SCHEDULED (private + publishAt, thumbs, playlists): A-009 Vending machine 5XdQYTPzwxU 20 Nov · A-010 Wrinkly fingers AshEYTYzMyI 21 Nov ·
   A-011 First traffic light yyBUc7aM2lA 22 Nov · A-012 Pen cap hole 1r8faDAYoTQ 23 Nov · A-013 Falling cat bHC7F6nNwWM 24 Nov (all 16:00 UTC). Buffer to 24 Nov.
   NEXT (5 uploads used 15 Nov = quota limit; upload again 16 Nov after 08:00 UTC): A-014 golf-ball dimples (9 Science) 25 Nov · A-015 onions/tears (7 Body) 26 Nov (template: episodes/A-009 make.py).
   16 Nov after 08:00 UTC: P1 (`python tools/yt_apply_fixes.py` dry run → `--apply`, B-002 description, channel text, playlists, yt_stats, topic_results, SRT, verify.py)
   then tell audit session_01BQj2DeVVBA9LqPEcBBQjhd "P1 done". Wave 2 (L4 long + cut Shorts + 2 standalone, 27 Nov–3 Dec) only after 48 h data on A-009/A-010 (≈ 23 Nov).
** 15 Nov owner: GO for new production, strictly per the audit (docs/audit/2026-11-15_channel_audit.md §4, §6, §7, §8). Always keep ≥14 days scheduled.
   Cast v2.1 APPROVED (lib/cast2.py, library/cast/cast_v2_sheet.jpg). D2 no end card, D3 cast v2, D4 posted stay + strict religion screen.
   Scheduled now: B-003 Shorts to 19 Nov 16:00 UTC. Wave 1 = 20–26 Nov (long Fri 20 Nov 15:00 UTC if ready, else Style F Shorts hold slots and
   the long moves to Fri 27); Shorts daily 16:00 UTC, never two within 12 h. Wave 2 (27 Nov–3 Dec) only after 48 h data on 2–3 new-standard Shorts.
   16 Nov after 08:00 UTC: P1 (`python tools/yt_apply_fixes.py --apply`, B-002 description, channel text, playlists, yt_stats, SRT) then tell audit "P1 done".
** AUDIT PLAN (docs/audit/2026-11-15_channel_audit.md §7–8): P1 housekeeping from 16 Nov (python tools/yt_apply_fixes.py --apply after 08:00 UTC;
   B-002 description, channel text, playlists, SRT captions, yt_stats). Buffer 20 Nov–3 Dec in 2 waves (wave 1 = 20–26 Nov; wave 2 only after 48 h data
   on 2–3 new-standard Shorts). Standards first: waiting for owner D1–D5 (asked 15 Nov 06:10) before any buffer render. Tell audit "P1 done" + approved D-items.
** 14 Nov growth review: "Why [everyday object] …" Shorts start best (windows 1 108, plane door 436); name the object + Why/How claim in B-003 cut-Short titles (research/daily_report.md).
** 15 Nov owner: follow the AUDIT session strictly (wait for its report, branch claude/zen-knuth-ypcfhk docs/audit/); keep 14 days of content scheduled ahead, produce only until then. (old 14 Nov: no new production —replaced) Only finish B-003 (long + 10 cut Shorts) and its uploads. Test & Compare package sent (3 thumbs + 3 titles).
** 13 Nov owner: TikTok PAUSED (no posts, no Dropbox requests) until he asks. Kaggle is shared with other sessions: never stop/delete their kernels.
** B-003 pirates: DONE. Long Am8epkS94Hw (public 14 Nov; thumbnail via Studio; comment posted, owner pins). Cut Shorts C1–C5 public/scheduled 14–15 Nov;
   C6 SVAKhIs2w0Y 15 Nov, C7 PQDcJuv570Y 16, C8 cLtK1MIprGs 17, C9 YL5gMoQVH7w 18, C10 e3VksvQ5-Gk 19 Nov, all 16:00 UTC (no end card, D2).
   Scheduled content runs to 19 Nov. NEXT (audit plan): 16 Nov after 08:00 UTC `python tools/yt_apply_fixes.py --apply` + other P1 items;
   cast v2 sheet sent to owner (library/cast/cast_v2_sheet.jpg) → on approval, composer rules (first frame, no end card) → buffer wave 1 (20–26 Nov).
** 13 Nov growth review: body/science Shorts with one named object start fastest (Brain freeze 1 125 views in 15 h); emoji A/B (A-004 🪶) is inconclusive (different topic/timing), don't change A-002's title on it (research/daily_report.md).
** FABLE SPRINT (Style F, flat 2D) — STOPPED 13 Nov 08:30 UTC on the owner's instruction ("finish what is started, no new work"). 4 Shorts made:
   A-005 Brain freeze: YouTube 8hsKNMLOhAw PUBLIC 12 Nov 16:00 UTC; TikTok Metricool 425987798 (posted 12 Nov 17:40 UTC).
   A-007 Square windows: YouTube WHd_m81cbpE PUBLIC 13 Nov 04:00 UTC (thumb, playlist, category 28 set); TikTok Metricool 426509053 (13 Nov 04:30 UTC).
   A-006 Castle toilet: YouTube iW60L9Pap5k scheduled 13 Nov 10:00 UTC (thumb, playlist, category 24). TikTok NOT yet posted (see below).
   A-003 Plane door: YouTube bE1TP9JlAzs scheduled 13 Nov 16:00 UTC (thumb, playlist, category 28). TikTok NOT yet posted (see below).
   Still taken: A-002 13 Nov 22:00 UTC. Free standalone slots left unused: 14 Nov 04:00, 10:00, 16:00, 22:00 (no new sprint videos unless the owner asks).
   OPEN (13 Nov 13:30 UTC): TikTok for A-006 and A-003. Files ARE on Dropbox already (fresh token 13 Nov 13:29 UTC; public links stay valid
   until the files are deleted): A-006 https://www.dropbox.com/scl/fi/w5oc17vvy71z6mn5k4nun/A-006.mp4?rlkey=ooy8sm3ka8tiqwoz9pda145h1&dl=1
   A-003 https://www.dropbox.com/scl/fi/48gg2tgzbmhw2n0cp9wzz/A-003.mp4?rlkey=yuh94dfmrhhyzjisxvij4uh81&dl=1
   BLOCKED: the Metricool connector failed to connect (503) after the model switch. Owner: reconnect Metricool at claude.ai/customize/connectors and start
   a new session (or retry here). Then Metricool createScheduledPost (brand 7942824, Asia/Karachi, TikTok only, text = upload_meta.json "tiktok_caption",
   tiktokData.title = YouTube title, never set isAigc): A-003 at 16:30 UTC 13 Nov if still ahead (else next free time); A-006 slot 10:30 UTC is past →
   19:30 UTC 13 Nov suggested (US/UK evening, 3 h from other TikToks). Record ids in episodes/<ep>/social/tiktok_posted.json, then
   `python lib/dropbox_host.py rm A-006.mp4` / `A-003.mp4` (needs a valid Dropbox token; else the owner deletes them in Dropbox). Old A-007 copy deleted.
   Style F engine and assets: library/index.md ("Style F" section). Scripted but not made: none. Ideas noted for later: dazzle ships, Centralia, cat righting reflex.
** 12 Nov growth review: titles with ONE named object + "Why/Accident" claim get the fastest starts (A-001, A-008); name the object in cut-Short titles of B-003, avoid vague "job" titles (research/daily_report.md).
** 12 Nov 17:35 UTC: KAGGLE WORKS again (anam318 phone-verified; max 2 GPU sessions at once). B-003 kernels b003 + b003b v2 RUNNING; then push kernel_b003c.
** 12 Nov 07:00 UTC (old): KAGGLE PAUSED. Owner: Fable 5.2 sprint in Style F (flat 2D, like A-008), videos scheduled
   12–14 Nov only: docs/fable_sprint.md. Style T work (A-005 3D, B-003 pirates) is saved below; resume when Kaggle works.
0. Daily growth review = separate scheduled task (fresh Sonnet session, 07:13 UTC): `bash tools/daily.sh` → entry in research/daily_report.md. Heartbeat does NOT repeat it; it reads the latest entry before any new script/title. 48 h check of A-001/A-004 titles (emoji test): 13–14 Nov.
   A-001 Quicksand: DONE + SCHEDULED on YouTube (MLRRsaV4iUA, public 11 Nov 22:00 UTC = 03:00 PKT 12 Nov, QA pass, thumb set). TikTok SCHEDULED via Metricool 22:30 UTC 11 Nov (id 424053522; final re-composed from Kaggle plates); title "Why Quicksand Can't Actually Swallow You", end caption "Watch the full video on YouTube — @TrueWhys"? (standalone: use "More true whys on YouTube — @TrueWhys").
   A-004 Tickling: DONE + SCHEDULED on YouTube (sdoOC7kAuRU, public 12 Nov 22:00 UTC, QA pass, thumb set; title ends with 🪶 = A/B vs A-001). TikTok SCHEDULED via Metricool 22:30 UTC 12 Nov (id 424045584). Plates: Kaggle truewhys-render-a004.
   A-002 Polar bear liver: DONE + SCHEDULED (o-dGmxKGKoY, public 13 Nov 22:00 UTC, QA pass, thumb set, no emoji in title). TikTok SCHEDULED 22:30 UTC 13 Nov (Metricool 424396234). Plates: Kaggle truewhys-render-a002.
   If the A-001/A-004 48 h emoji test (13–14 Nov) favours the emoji, edit the A-002 title.
   A-008 Steel (owner-made, flat 2D): end card swapped to the Wy ✓ card; YouTube zCkUEA4t5iQ public 11 Nov 14:00 UTC; TikTok 15:00 UTC (Metricool 424394467).
   A-005 Brain freeze (IN PROGRESS 11 Nov): script v2 (32 s), Gemini voice, plan.py (14 shots), stills checked, Kaggle truewhys-render-a005 pushed 15:32 UTC.
   NEXT: fetch plates → compose --w 1080 --h 1920 → QA → YouTube 22:00 UTC 14 Nov (upload_meta ready) → TikTok 22:30 UTC.
   EPISODE 3 (owner 11 Nov: start right after A-005, in parallel with the remaining Shorts): pirate myths vs truth, Ranked List
   (topic research in research/format_study.md, 11 Nov). Folder episodes/B-003-pirate-myths.
   DONE 11 Nov 15:40 UTC: script v1 (10 items, 67 lines), sources.md (2+ per claim), topic.md, Gemini voice ch0–6 (4:31) + timing.json.
   DONE 11 Nov: sets5.py (deck/islet/port), pirate cast, docs, SFX, adventure music, plan.py (85 shots, 5:37 + 20 s end), stills checked + fixed.
   BLOCKED 11 Nov ~16:50 UTC: Kaggle rejects KAGGLE_API_TOKEN ("Authentication required"). Owner must make a new token (kaggle.com → Settings → API →
   Generate New Token) and save it (secure form for host api.kaggle.com, or update KAGGLE_API_TOKEN in the environment).
   12 Nov: Kaggle account is now anam318 (owner). Token = network secret for api.kaggle.com; use `/opt/c3d/bin/python tools/kaggle_px.py <kaggle args>`.
   Old waqarahmed51 A-005 output unreachable → A-005 re-rendered: anam318/truewhys-render-a005 v1 RUNNING. B-003: dataset anam318/truewhys-ep-b003 ready,
   kernels truewhys-render-b003 + b003b v1 pushed 12 Nov. ALL 3 FAILED (no GPU, no internet): owner must PHONE-VERIFY anam318
   (kaggle.com → Settings → Phone verification). Then re-push kernel_a005, kernel_b003, kernel_b003b (datasets are ready). Waiter: `tools/kaggle_wait.sh k=dir ...`. Then push notebooks/kaggle_jobs/b003/kernel_b003c (Shorts).
   THEN: (1) A-005: `kaggle kernels output waqarahmed51/truewhys-render-a005 -p episodes/A-005-brain-freeze/renders` (pushed 15:32 UTC), compose, QA,
   YouTube 22:00 UTC 14 Nov + TikTok. (2) B-003: dataset truewhys-ep-b003 (flat: render_bg, sets, sets2, sets3, sets5, camera, shots.json, job_A/B)
   → push kernels notebooks/kaggle_jobs/b003/kernel_b003 (ch 0–3) + kernel_b003b (ch 4–6), ~4–5 h each in parallel.
   DONE 12 Nov: shorts.json (10 cut Shorts C1–C10, 21–31 s, one per myth), hook voice (voice/hooks.flac, 1 Gemini request), lib/shorts.py plans.
   NOTE hooks: whisper split put the end of "Seriously" (H8) at the start of H9. If audio/lines is rebuilt from hooks.flac, move the first
   0.6 s of H9.wav onto the end of H8.wav (timing_hooks.json already has the corrected timings).
   Shorts plates need a 3rd Kaggle job (shorts/all_shots.json, 1080×1920) after the long-video plates.
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
