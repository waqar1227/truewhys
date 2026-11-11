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
