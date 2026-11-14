# Daily growth & competitor report (newest first)
Data: `python lib/yt_stats.py` (snapshot saved in research/stats/<date>.json). CTR/impressions are Studio-only: owner pastes them when he can.
YouTube Analytics lags 2–3 days, so retention for new videos appears later.

## 10 Nov 2026
**Channel:** 6 subs, 3,277 views, 13 videos (2 long, 11 Shorts).

**What worked**
- 2 Shorts broke out: "Why the Hangman Got New Gloves" 1,700 views (24 s!) and "The Lawyer Who Defended Rats in Court" 1,382 (54 s).
  "The Worst Job in Old England: The Gong Farmer" has 220 views in ~9 h (on track to be our 3rd best).
- Common thread: **one specific person + one odd object/act** (hangman + gloves, lawyer + rats, gong farmer + toilets), a "Why…/The X Who…" title,
  and a hook that states the weird fact in the first second.

**What failed**
- Long videos: B-001 1 view (37 % average viewed), B-002 6 views. A brand-new channel gets almost no browse traffic for long videos;
  Shorts viewers are not clicking through yet.
- Shorts about a group/abstract idea ("Why the Church Put Bugs on Trial" 7, "The Pig of Falaise" 6, "The King's Toilet Servant" 10 so far) stall.
  They open on context, not on a single striking image + person.

**Competitors (latest uploads, yt-dlp)**
- Rick's Clips: 3–33 M per Short. Titles are 4–7 words, a concrete object + mystery, no "#Shorts" in the title:
  "The Ancient Jar That Warned an Empire" (33 M), "Why Perfect Railroads Don't Work" (27 M), "The Job Nobody Wants in Japan" (17 M), "The Burglar Who Only Moved Furniture" (9 M).
- Zack D. Films: 3–16 M; "What If Humans Had Hummingbird Hearts" (16 M), "How To Build A Matchbox Camera" (11 M); every title ends with one emoji.
- Ink Explainer (long): "What Did Ancient Humans Actually Do All Day?" 18 M is still the outlier; follow-ups in the same series get 0.1–2 M.
  The "Daily Life Back Then" format is the proven long-video winner (we must use other eras/groups, never ancient humans).

**Changes we apply from now**
1. Shorts titles: 4–7 words, "The [person/object] That/Who …" or "Why …", **drop "#Shorts" from the title** (keep it in the description). Test one emoji at the end on half the A-series Shorts (A/B by alternate Short).
2. Every Short opens on ONE person + ONE strange object in frame, with the weird fact said in the first 1.5 s (A-001 already does: Wy sinking + "SINKING?!").
3. Long videos: episode 3 uses the proven "What Did ___ Actually Do All Day?" format (medieval knights/castle servants/pirates), with a stronger
   thumbnail (face ≥ 35 %, one object, 2–3 words). Each new long video is linked from every cut Short and its pinned comment.
4. Standalone Shorts batch A-001…A-007 goes ahead; their 48 h numbers decide which categories get 80 % of output.

**Next check:** 12 Nov (48 h numbers for all B-002 Shorts + A-001).

## 10 Nov 2026 20:45 UTC (evening heartbeat)
- **Data (yt_stats 7 d):** subs 7, views 3 277. Retention vs length is the clearest signal: Hangman gloves 24 s → 86 % viewed → 1 565 views; Lawyer rats 54 s → 46 % → 1 350; Weevils 56 s → 54 % → 33; Rooster 48 s → 51 % → 17. Long videos: B-001 7:02 keeps only 16.6 % (avg 70 s), B-002 10 views in 17 h.
- **B-002 Shorts:** Gong farmer 226 views in 16 h; the next four (C2–C5) only 3–12 views each 3–12 h after release. Likely cause: four Shorts from the same video every 3 h compete with each other and the feed tests each one on a tiny seed audience; titles C2–C5 are vaguer (no single gross/strange object up front).
- **Changes:** (1) Standalone Shorts aim at 25–40 s with a payoff before 20 s (A-001 is 40 s: watch whether it beats the 50 % line). (2) Next long video must hook harder in the first 30 s (B-001 lost most viewers by 70 s): open on the strangest moment, not context. (3) Proposal for the next episode's cut Shorts: space them 6–8 h apart instead of 3 h, and lead with the single strangest one. Owner rule says within 24 h, so 3–4 Shorts per day max; raise with owner before changing.
- Competitor check: done this morning (see above), unchanged; next on 11 Nov.

## 11 Nov 2026 07:15 UTC (daily growth review)
Data: research/stats/2026-11-11.md · research/competitors/2026-11-11.md
1. **Channel performance:** subs 7, views 3 658 (+381 since 10 Nov). B-002 Short C1 "Medieval Job Where You Drank Ale" 215 views in ~5 h; C2–C7 still 3–28 views; Gong farmer stalled (233, +7). B-002 long 13 views (+3). Traffic: SHORTS feed 2 947 of ~3 080 (96 %); search 29, related 7. No retention yet for 10–11 Nov uploads.
2. **Competitor intelligence:** first snapshot (no baseline). Rick's Clips breakouts = one strange real object/custom ("Ancient Jar That Warned an Empire" 33 M, "Why Sailors Carried Storm Oil" 15 M). Zack D. "What If"/"How" titles all end in an emoji (🤔/😱), 9.7–18 M. Ink Explainer = ancient humans (off-limits for us).
3. **What worked:** Short-and-tight still wins: Hangman gloves 24 s → 86 % viewed → 1 565 views (best). C1 broke out although it came 3 h after C7, so feed seeding, not only spacing, decides which cut Short takes off.
4. **What failed and why:** C2–C7 = discovery problem (SHORTS feed gave them tiny seed audiences; no retention data yet to blame the hook). Long videos: discovery too (search+related = 36 views total) and B-001 hook (0.29 at 10 %). Every Short with data has its biggest drop at 10–19 % → hook is the shared weak spot.
5. **Next improvements:** (a) A-002 Polar bear liver: show the payoff image (liver/danger) in the first 2 s and keep 25–40 s (evidence: all drops at 10–19 %; 24 s Short = 86 %). (b) Keep the A-001 (no emoji) vs A-004 (🪶) test; Zack D. emoji titles support it, decide at 48 h (13–14 Nov). (c) Owner set the spacing rule 11 Nov: cut Shorts ≥ 3 h apart, standalone ≥ 6 h.
6. **Usage:** daily.sh only; competitor snapshot via yt-dlp script, no web search, no images viewed. Run cost $0.48 (ran on the main model: Sonnet setting not applied; push failed, no repo attached → fixed by moving the review to a dedicated session with the repo).
7. **Open checks:** CTR/impressions unknown (no Studio numbers pasted); C1 retention arrives in ~48 h; competitor "breakouts" are from one snapshot, growth rates start tomorrow.

## 12 Nov 2026 (daily growth review)
Data: research/stats/2026-11-12.md · research/competitors/2026-11-12.md
1. **Channel performance:** subs 10 (+3), views 4 170 (+512 since 11 Nov). A-001 Quicksand 730 views in ~9 h; A-008 Steel 1 235 views / 20 likes in ~17 h; C1 Ale 296 (+92). C2–C7 still 4–123 views; B-002 long 2 views, B-001 long 29 (+5). Traffic: SHORTS feed 3 318 of ~3 476 (95 %), search 43, related 8. No retention data yet for 10–11 Nov uploads.
2. **Competitor intelligence:** growth deltas now exist. Rick's Clips fastest: "This Shape Saved Roller Coasters" +1.1 M, "Why Perfect Railroads Don't Work" +1.0 M (one engineering object + a "why it works/doesn't" claim). Zack D.: "The Eel That Burst Through A Heron's Body 😵" +4.6 M, "Why Your Brain Focuses On Negative Things 🤔" +4.0 M (body/biology curiosities, emoji at end). Ink Explainer: ancient humans only (off-limits).
3. **What worked:** A-001 (41 s, one object + strange fact in 1.5 s, no #Shorts in title) and A-008 Steel (51 s, "The Accident That Invented…") are the two fastest starters since the Hangman Short, so the "one object + one strange claim" title/hook change is working on discovery (no retention yet to confirm).
4. **What failed and why:** C2–C7 = discovery (4–10 views each, same pattern as yesterday; vague titles and several Shorts from one video competing). B-002 long = discovery (2 views, search/related ~0). Gong farmer shows −130 vs yesterday: likely a YouTube recount/data glitch, not real loss.
5. **Next improvements:** (a) Keep standalone Shorts in the A-001/A-008 style (one named object + "Why/Accident" claim) and lean to body/biology topics: A-005 Brain freeze and A-004 Tickling match Zack D.'s fastest growers. (b) Decide the emoji A/B (A-001 none vs A-004 🪶) at 48 h on 13–14 Nov using views + avg % viewed. (c) Cut Shorts for B-003: use the specific-object titles, not generic job titles (evidence: C1 vs C2–C7).
6. **Usage:** daily.sh only; no web search, no images. Fixed a crash in lib/competitors.py (sorting dicts on ties).
7. **Open checks:** CTR/impressions unknown (no Studio numbers pasted); A-001/A-008 retention arrives in ~24–48 h; emoji test not yet readable.

## 13 Nov 2026 (daily growth review)
Data: research/stats/2026-11-13.md · research/competitors/2026-11-13.md
1. **Channel performance:** subs 12 (+2), views 7 742 (+3 572 in 24 h, 22 videos). New: A-005 Brain freeze 1 125 views in ~15 h; A-007 Square windows 176 in ~4 h; A-001 Quicksand 1 118 (+388); A-004 Tickling 🪶 only 23 in ~9 h. A-008 Steel stalled at 1 262 (+27). Traffic: SHORTS feed 3 793 of ~4 020 (94 %), search 60, related 9. B-002 long 14 views (+12), B-001 29.
2. **Competitor intelligence:** Rick's Clips fastest: "How One Cart Stopped an Entire Army" +1.7 M, "Why Sailors Carried Storm Oil" +1.0 M (one object + a surprising use/claim). Zack D. fastest: "The Tires That Won't Crush You 🤯" +5.6 M, "What If Humans Had Hummingbird Hearts 🤔" +3.0 M; new hits are body/psychology ("How Fear Can Turn Into Attachment", "How Food Companies Make You Eat More"). All still end in an emoji.
3. **What worked:** Body/science Shorts with one named object start fast: Brain freeze 1 125 in 15 h (vs 4–10 views for the C2–C7 "job" Shorts), Quicksand +388 on day 2. Matches Zack D.'s body/psychology growers.
4. **What failed and why:** A-004 🪶 is far behind A-001 at the same age (23 vs ~730 views at ~9 h), but this is NOT a clean emoji test: different topic, and it launched 6 h after A-005 took the feed. Discovery/topic or timing, not proven emoji. Gong farmer/ale cut Shorts: still low; ale 12 % drop = hook (ret 10 % = 1.11, 50 % = 0.43). Steel stalled after ~17 h: one-day burst only.
5. **Next improvements:** (a) Do not edit A-002's title yet: wait for A-004 at 48 h (14 Nov) and treat emoji result as inconclusive unless the gap persists on equal topics. (b) Next Shorts: body/science with one named object ("Why …", "What … Does Inside Your Head"); evidence: Brain freeze 1 125 vs C-series ≤ 244. (c) Keep standalone Shorts ≥ 6 h apart (owner rule): A-004 sat 6 h after a fast Short.
6. **Usage:** daily.sh only; no web search, no images viewed.
7. **Open checks:** CTR/impressions unknown (none pasted); no retention yet for A-001/A-005/A-007/A-008; the emoji test needs a same-topic pair.

## 14 Nov 2026 (daily growth review)
Data: research/stats/2026-11-14.md · research/competitors/2026-11-14.md
1. **Channel performance:** subs 16 (+4), views 9 536 (+1 794 in 24 h, 25 videos). New Shorts: Square windows 1 108 (~27 h, +932), Plane door 436 (~15 h), Castle toilet 177 (~21 h), Polar bear liver 160 (~9 h), Tickling 🪶 142 (+119, ~33 h). Brain freeze flat at 1 132 (+7). Traffic: SHORTS 5 984 of ~6 330 (95 %), search 126 (+66), related 9.
2. **Competitor intelligence:** Rick's Clips fastest: "How One Cart Stopped an Entire Army" +1.2 M, "Your Brain's Secret Idea Zone" +1.0 M (brain/psychology angle again). Zack D. fastest: "How Food Companies Make You Eat More 🤤" +4.4 M, "Baby Falls 60 Feet And Survives 😱" +2.3 M; new uploads "How Free Favors Become Expectations", "How Dragonfly Wings Kill Bacteria" (psychology + nature mechanisms; emoji titles).
3. **What worked:** Retention is now measurable and good: Steel avg 72 % viewed (ret 10/50/90 % = 1.06/0.78/0.48), Quicksand 60 % (1.12/0.53/0.30). Both hold above ~0.5 at midpoint, unlike the old "job" Shorts (0.31–0.45). Everyday-object "Why …" Shorts (windows, plane door) are the best starters of day 2: windows 1 108.
4. **What failed and why:** Each Short peaks in the first ~15 h then stalls (Brain freeze +7, Steel −20): discovery is a one-burst feed test, not retention. Tickling 🪶 142 at ~33 h vs Quicksand ~1 100 at the same age: gap persists, but topic and 6 h slot differ, so still not proof the emoji hurts. Castle toilet/polar bear liver start slower (160–177) than windows/door: topic less relatable, not a hook problem (no retention yet). Old C2–C7 job Shorts remain 4–10 views.
5. **Next improvements:** (a) When production resumes, favour "Why [everyday object] …" topics (windows 1 108, plane door 436 vs castle toilet 177). (b) Cut-Short titles for B-003: name the object and the "Why/How" claim, matching Rick's "How One Cart Stopped an Entire Army". (c) Run the emoji test as a same-topic pair before changing any title.
6. **Usage:** daily.sh only; no web search, no images viewed.
7. **Open checks:** CTR/impressions unknown (none pasted); no retention yet for the 13 Nov Shorts; B-003 long (15:00 UTC today) not yet measurable. Owner paused new production, so (a) applies only after go-ahead.
