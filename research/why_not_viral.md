# Why our videos don't go viral yet — diagnosis (22 Nov 2026) and what changes

Data: research/stats/2026-11-22.md (our 38 videos), competitor Shorts via the Data API (15 latest each, 22 Nov).

## 1. The pattern: a "1 000-view wall"
Our best Shorts all stop at 1 000–1 700 views within ~15 h (Hangman 1 735, Rats lawyer 1 392, Quicksand 1 319, Steel 1 290, Brain freeze 1 160,
Plane windows 1 135, Vending machine 1 135, GTA 6 1 707). That is the size of YouTube's first test audience for a small channel. A Short only gets
the next, bigger audience when the test viewers (a) don't swipe it away and (b) watch it to the end or loop it, BETTER than similar Shorts.

## 2. Where we lose (numbers)
| signal | our winners | our losers | needed to break out (typical viral Shorts) |
|---|---|---|---|
| stayed (viewed vs swiped) | 50–60 % | 25–35 % | 70 %+ |
| relative retention at 10 % (0.5 = average) | 0.45–0.53 | 0.1–0.35 | > 0.6 |
| biggest drop | 13–21 % into the video | same | no early cliff |
| avg % viewed | 66–93 % | 40–55 % | 90–100 %+ (loops) |
Likes per view are close to competitors (ours 1.1–1.6 %, Rick's Clips ~2 %, Zack D ~3.4 %), so people who watch like it: **the problem is the
first second and the line right after the hook**, not the idea of the channel. Length is not the problem (Rick's Shorts ~64 s, Zack's ~34 s).

## 3. Root causes (ranked)
1. **Frame 1 had no surprise.** Old openings: a calm scene + a text title. Viral Shorts start mid-action with something visibly wrong/odd.
2. **The second line was background** ("London, 1696…", "In the Middle Ages…"): that is exactly where the 13–21 % drop sits.
3. **Topics too niche or repeated:** medieval jobs and 7 pirate Shorts in a row (5–200 views) vs everyday-object/body/"you" topics (1 000+).
4. **Flooding in week 1** (up to 8 Shorts a day on 10 Nov) split the test audiences; those videos got 5–40 views.
5. **Visual simplicity:** flat 2D puppets read less "wow" in the feed than the competitors' 3D; testing Style R now (A-016/A-017/A-018/A-021).
6. **Long videos have no traffic source:** 0 % from the Shorts feed, almost no browse; retention 0.2–0.4 at 10 % = weak cold open.

## 4. Decisions for every new video (production rules)
1. **Frame 1 = action already happening** (motion from frame 0, a sound hit at 0.0 s), the object + a face with a strong emotion + a ≤ 4-word
   question. Voice states the strange claim in ≤ 2 s.
2. **Line 2 raises the stakes, never background.** Context (year/place) goes on screen as a small label while the story moves.
3. **Open loop to the end:** the answer/twist lands in the last 3 s, then the last frame matches the first (loop).
4. **Topic filter:** everyday object / body / "would you" / trending-now; ≤ 2 of one theme in a row; skip niche history unless the hook is universal.
5. **Shorts 25–40 s,** a new visual every 1.5–2.5 s, no dead air.
6. **Style test:** compare Style R (3D) and Style F (2D) Shorts on stayed % and avg % viewed after 48 h; shift to the winner.
7. **Long videos:** cold open from the most dramatic moment (L4 "Hanged for this?"), a new mini-mystery every 30–45 s, each cut Short sets the
   long video as its Related video (owner, Studio).
8. **48-h check on every video** (topic_results.md): stayed %, rel. retention 10 %, drop point, avg % viewed. If stayed < 60 % → the hook failed
   → change the hook pattern next time; if the drop is at 13–21 % → line 2 failed.

## 5. Old videos
Most old Shorts already got their test audience; a new title rarely restarts the feed, so effort goes to new videos. Fixed 22 Nov: 3 titles
(docs/audit/retitles_2026-11-23.json: religion-neutral wording for RI7u-NzEj5E, clearer claims for Wu5-PLKwb48 and kk6I9g5V82Y).
