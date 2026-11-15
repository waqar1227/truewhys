# TrueWhys independent channel audit — 15 Nov 2026

Written by the audit session (research and checking only; the production session implements).
Data pulled 15 Nov 2026, 04:20–04:40 UTC. Sources: our YouTube Data + Analytics API (31 videos), the same official API for 22
competitor channels (public data: publish times, lengths, titles, tags, views), public thumbnail/frame images (first frame + 3
frames per video), Metricool best-time data for our brand, and the repository.
Per-video fixes: `docs/audit/metadata_fixes.json`. What was NOT possible: watching competitor videos in motion (YouTube blocks
video downloads from this server; not worked around), and impressions/CTR (not in the API: both metric names return 400).

**Read this first.** The channel is 8 days old (first upload 8 Nov). 11,571 views, 17 subscribers, 31 videos. That is not a
failing channel; it is a channel in its first feed tests. But the data shows five clear, fixable reasons why it is not growing
faster. They are ranked by how much evidence supports them.

---

## 1. The five reasons (evidence, not opinion)

### 1.1 Half of the Shorts were never shown to anyone — they were published too close together
Shorts at least 24 h old (n = 23):

| Group | n | Median views | Under 50 views | 1,000+ views |
|---|---|---|---|---|
| Cut Shorts, published 3 h apart | 15 | **80** | 7 | 2 |
| Standalone Shorts, 6 h+ apart | 8 | **881** | 0 | 4 |
| Any Short with a gap ≤ 3.5 h before it | 12 | **26** | 7 | 1 |
| Any Short with a gap ≥ 5 h before it | 10 | **476** | 0 | 4 |

The dead ones did not fail a test; they got no test. Views from the Shorts feed: "Stomped on Cloth in Old Urine" 1, "Eat a Dead
Man's Sins" 0, "Swallow a Toad" 0, "Dig Up Your Floor" 2, "Church Put Bugs on Trial" 3, "Pig of Falaise" 1.
Same decay in every batch: B-001 123 / 1,730 / 1,387 / 80 / 85 / 8 / 9 · B-002 317 / 134 / 8 / 4 / 15 / 5 / 38 / 318 ·
B-003 so far 41 / 1,029 / 11 / 5 / 0.
Limit: correlation only (topic, style and title differ too). But three batches agree and nothing supports 3 h spacing.
The 10 Nov evening heartbeat already saw this and proposed 6–8 h; the 3 h rule was kept. The data now says change it.

### 1.2 The Shorts that do get tested lose half the viewers at the first frame
- Stayed vs swiped (engagedViews ÷ views, all Shorts): **50 % stayed, 50 % swiped.** Per video 28–56 % (Gong farmer 30 %, King's
  toilet servant 28 %, Hangman 46 %, Brain freeze 49 %, Steel 55 %, Lawyer 56 %).
- YouTube's own "relative retention" (0.5 = the average video of the same length) at the 10 % mark: Quicksand 0.36, Lawyer 0.26,
  Rooster 0.20, Tickle 0.19, King's toilet 0.11; our best are only average (Windows 0.58, Brain freeze 0.53, Steel 0.51).
  **Not one Short has an above-average hook.** That is why each one stops at ~1,100–1,700 views: it passes the first small
  audience and fails the next one.
- Cut Shorts have a cliff 5–7 s in (10 % → 15 % of the video): Ale 1.09 → 0.74, King's toilet 1.00 → 0.59, Gong farmer
  1.16 → 0.76, Lawyer 0.96 → 0.66. That is the moment the new hook line ends and the long video's slower narration starts.
- What the first frame looks like (contact sheets): Style T Shorts open on ONE small character (about 20 % of the frame height)
  standing still in the middle of a dark brown set, bottom 40 % of the frame is empty floor, often without the object named in
  the title (the parrot Short opens with no parrot; the pig Short opens on a pig 5 % of the frame tall).
  Rick's Clips opens mid-action with characters filling 40–60 % of the frame in bright, saturated, detailed sets (pouring the
  oil, sawing the rail). Zack D. Films opens on an extreme close-up of the object doing the thing (plug entering the outlet,
  shark on the whale).
- The daily review of 14 Nov concluded "discovery is a one-burst feed test, not retention". The relative-retention numbers
  say the opposite: the hook is the limit. `yt_stats.py` does not collect these two metrics yet (see §7).

### 1.3 The end card throws away the ending and the loop
Watch ratio in the last tenth of the video: Brain freeze 0.67 → **0.09**, Quicksand 0.28 → **0.08**, Steel 0.48 → 0.21,
Rooster 0.45 → 0.17. The last ~2.6 s is a still card ("Follow for more true whys") = 7–11 % of a 23–40 s Short.
Rick's Clips and Zack D. Films have no end card: their frame near the end is still story (Zack says his sign-off over moving
picture). Our one Short whose ending flows back into its opening shot (Plane windows) has **146 % average viewed**.

### 1.4 Long videos have no way to be found, and the Shorts do not send anyone to them
- All long-video views so far: **57** (Analytics) / 78 (public counter). 99.3 % of channel views are Shorts.
- Where long views come from: subscribers (41 of 57) and the channel page. Search + suggested ≈ 9.
- Shorts → long video link clicks: **1 view from 8,018 Shorts views.**
- Retention: B-001 15 % average viewed (64 s of 7:02), B-002 22 % (82 s of 6:12). Sample is tiny and mostly the same few
  subscribers, so no firm conclusion on the content itself. B-003 has no data yet.
- This is normal for week 1 (Ink Explainer's breakout was its 14th video, four months after it started). It will
  not fix itself through Shorts. Long videos need their own discovery: search-led topics, a series, a fixed weekly slot, and
  stronger first 30 seconds.

### 1.5 The channel looks like it is for small children; the audience is adult men
- Viewers: 68 % male; **61 % are 25–44**; 13–17 is 11 %. Top countries: US 27 %, Philippines 7 %, UK 6 %, Canada 4.5 %,
  Australia 3.4 %. Best retention: Australia 89 %, Canada 82 %, US 66 %, UK 64 %. Android 68 %.
- Our cast: egg heads, very large round eyes, rosy cheeks, toddler proportions, a child mascot presenting from a desk.
  Every successful channel for this audience (Rick's Clips, Ink Explainer, The Paint Explainer, Casually Explained,
  Sam O'Nella) uses dry, deadpan, adult-humour characters. A swiping adult decides in under a second whether "this is for me".
- No copying: Rick's = white round heads with stick limbs, Ink = messy-hair stick people, Zack = semi-realistic 3D humans.
  We need our own older, drier look (see §6.1).

### Smaller things that also cost views
- **Titles that give the answer away.** Median views by title shape (our Shorts, 24 h+): starts with Why/What/How **636**
  (n = 9) · "The X That/Who…" 134 (n = 9) · plain statement or label **38** (n = 5). Example inside one batch:
  "Why Pirates Didn't Really Have Parrots" 1,029 vs "Pirates Almost Never Made Anyone Walk the Plank" 5.
- **"#Shorts" in the title** on all 20 cut Shorts, although the 10 Nov review decided to drop it. `lib/upload_shorts.py:37`
  still adds it. No competitor that matters has it; none of our 4 best standalone Shorts has it.
- **The same 11 tags on every Short of an episode** (127–159 characters of 500); nothing specific to the Short.
- **B-002 description bug:** chapter lines "#8 The ale conner … #1" turn into hashtags, so "#8 #7 #6" is what shows above the
  title. Two Wikipedia links are broken (missing ")") and Wikipedia is used as a source.
- **Channel description promises** "Shorts every day" and "8–12 minute" videos. Our rule is no schedule promises, and the
  videos are 5:38–7:02.
- **B-003 long video is not in the "Full Stories" playlist** (2 items). Only two playlists exist.
- **Zero shares, zero viewer comments** on every video. Nothing in the videos asks a question people want to argue about
  (Rick's "The Job Nobody Wants in Japan": 11,419 comments).
- `topic_results.md` and `branding/TrueWhys_channel_text.md` are required by CLAUDE.md but do not exist.

### What is working (keep it)
- Subscribers per 1,000 views: ours 1.5; Rick's Clips 0.4; Zack D. Films 0.36. Viewers who stay do subscribe.
- Style F (flat 2D, made on CPU, no Kaggle) holds viewers better than Style T: average viewed 72 % (Steel), 94 % (Brain
  freeze), 146 % (Windows) vs 56–58 % (Style T standalone) and 42–61 % (Style T cut Shorts). Style F frames are brighter,
  closer, and put the title on frame 1.
- Topics: "Why [everyday object] …" (windows, plane door, quicksand, brain freeze) and one-odd-object history (hangman's
  gloves, rats' lawyer) start best. The research and sourcing are good; keep 2+ sources per claim.
- Long-video thumbnails A are clean and readable.

---

## 2. Competitors: what the numbers say (official API, 15 Nov)

| Channel | Subs | Format | Cadence (recent) | Length (median) | Posts (US Eastern) | Title | Tags / description |
|---|---|---|---|---|---|---|---|
| Zack D. Films | 29.7 M | realistic-cartoon 3D Shorts | **5 per day**, every day | 36 s (27–53) | 8:30, 10:30, 13:30, 15:30, 17:30 | ~7 words + 1 emoji, never "#" | **0 tags, empty description** |
| Rick's Clips (explainer phase, since 7 Oct) | 182 K | flat cast on 3D sets, Shorts only | daily in Oct, now every 2–3 days | **64 s** (55–67) | irregular (late night / early morning) | 4–7 words, no emoji, no "#" | 0 tags, description = title |
| Nutshell Animations | 11.1 M | Shorts | 3 per day | 18 s | 12:00–18:00, peak 16:00–17:00 | — | 0 tags |
| Ink Explainer | 170 K | long only | 1 per 9–10 days | **11:13** (8–15 min) | 15:00–16:00, Tue/Thu/Fri/Sat/Sun | 8 words, a question | 3 tags, 4,600-char description with sources |
| The Paint Explainer | 2.0 M | long only | ~1 per week | 13:36 | 12:00, Sun/Tue | 8 words | 0 tags |
| History Matters | 1.9 M | long | 1 per 2–3 weeks | 8:50 | 13:00 | 10 words, a "Why" question | 0 tags |
| Simple History | 5.1 M | long + Shorts | 1.4 long, 5 Shorts/week | 9:57 / 106 s | **10:00**, long on Tue + Fri | 6–7 words | 13–27 tags |
| TED-Ed | 23 M | long | 2 per week | 5:51 | **11:00, Tue + Thu** | 10 words | 36 tags |
| Kurzgesagt | 25.8 M | long + Shorts | 0.4 long/week | 14:53 / 72 s | **10:00, Tue** | — | 35 tags |
| Weird History | 4.7 M | long | 2.5 per week | 15:33 | 10:00, Wed/Fri/Sun | 8 words | 17 tags |
| Chill Dude Explains | 759 K | long | 17 per week | 10:43 | 10:00 and 18:00 | 8 words | 0 tags |

What follows from this:
1. **Time of day barely matters; a fixed habit does.** Zack's median views are the same in all five slots (11–13 M) and on all
   seven days (10–14 M). Every big channel posts at the same clock time each time: long videos 10:00–16:00 US Eastern
   (15:00–21:00 UTC), Shorts 08:30–17:30 Eastern. Metricool's best-time data for our brand agrees: activity peaks
   14:00–17:00 UTC (highest 16:00 UTC, Wed/Thu), and is five times lower at 00:00–04:00 UTC. Four of our slots (22:00,
   01:00, 04:00, 07:00 UTC) sit in the low part.
2. **Length is not the problem; pace is.** Rick's hits are 60–67 s. In Zack's data the longer Shorts do better (40–59 s: median
   13.8 M; 20–39 s: 10.3 M). Our rule "30–45 s" is fine for now because our hooks are weak, not because short is better.
3. **Titles:** Zack's first words: How (59 of 200), The (45), Why (31). Rick: Why / How / The … That. 4–8 words. Never "#Shorts".
4. **Tags do almost nothing.** Five of the eight biggest channels use zero tags. YouTube's own help page says tags "play a
   minimal role" and mainly help with misspellings. We will still fill them properly (it is free and the owner asked), but no
   one should expect views from tags. Title, first frame and retention are what move a video.
5. **Rick's Clips is the proof that our niche works**: 29 explainer Shorts in 5 weeks, 3.5–34 M views each, with exactly our
   kind of topic. It also only took off after it dropped reused content for original stories.
6. **Long form:** the channels that live on long videos run 8–15 min, one video per week or slower, one repeatable series.

Visual study (first frame + 3 frames of the top 12 Rick's and Zack's videos, 5 Ink Explainer videos, all 31 of ours):

| | Rick's Clips | Zack D. Films | TrueWhys now |
|---|---|---|---|
| First frame | action already happening, the strange object in hand | extreme close-up of the object doing the thing | one character standing, object often missing |
| Character size | 40–60 % of frame height, 2–4 characters interacting | hero fills the frame; hands, faces, cutaways | ~20 %, usually alone, centred |
| Sets | bright, saturated, dense detail, strong depth | clean single-colour studio backdrop + one hero prop | dark brown/grey, large empty floor |
| Shot variety | low angles, over-shoulder, close-up, wide, map | macro → person → cross-section → result | mostly the same medium shot |
| Captions | 1–2 words, centre, small | short phrase, lower third, small | fine; keep |
| Ending | story until the last frame | story until the last frame, spoken sign-off | 2.6 s still card |
| Characters | deadpan adults, role by hat/uniform | semi-realistic humans with slightly big heads and eyes, toy-like poses | toddler-like, rosy cheeks |

Ink Explainer thumbnails show a whole relatable scene (a man relaxing: "NO JOBS"; a family in a cave: "RAINED ALL WEEK") with
2–3 plain words; inside the video almost every shot is a new drawn scene with several characters, never a presenter at a desk.
Our long videos return to Wy standing at his desk again and again.

About the Zack D. Films look the owner asked about: it is not full realism. It is clean stylised 3D people (smooth skin,
simple clothes, slightly enlarged head and eyes) placed like toys in front of a plain coloured backdrop, with the camera almost
always on the OBJECT, plus cross-sections. That is cheap to render because there is no big set. See §6.2 for how to build our
own version with free CC0 parts.

---

## 3. Resources: what we have, what is unused, what is free and safe

Checked from the audit session on 15 Nov:

| Resource | State | Better use |
|---|---|---|
| YouTube Data API | works; 10,000 units/day (upload 1,600 → ~6 uploads/day; edit 50; thumbnail 50; caption upload 400) | Never plan more than 5 uploads a day; do metadata edits on days without uploads |
| YouTube Analytics API | works | **Unused metrics:** `engagedViews` (stayed vs swiped), `relativeRetentionPerformance`, per-video traffic source, country, age/gender, search terms. Add to `yt_stats.py` |
| Impressions / CTR | not in the API (400 on both names) | Owner pastes Studio numbers for long videos only |
| Captions upload (SRT) | never used | Upload exact English captions for the long videos from `lines.txt` + `timing.json` (helps search and auto-translate) |
| Playlists | 2 exist | Topic playlists (§5) |
| Metricool connector | works; free best-time data used above | Re-check best times monthly; TikTok stays paused |
| Kaggle | **the CLI answered "Authentication required" from the audit session** | Production: run one read-only `kernels list --mine`. If it fails there too, the owner needs a new token. Also: Kaggle **CPU** notebooks cost no GPU hours and can run long Style F composes |
| Gemini | TTS works. Image models: free-tier limit is 0 (needs billing, so not usable). Music (Lyria) not tested, assume the same | Keep TTS as is |
| Freesound | **403 on every page from this server, even without a key** (the site blocks this address; the key is not the problem) | Use BigSoundBank, Kenney, OpenGameArt (CC0) until it answers again |
| Sketchfab token | works | CC0 / CC-BY props and rigged people for Style R |
| Pixabay key | works (images and videos) | Sky plates and textures only, as the rules say |
| Descript, HyperFrames (HeyGen), Zoom connectors | connected | Not needed: our pipeline is code; HyperFrames cannot compose or render from a Claude Code session |

Free sources that answered and are copyright-safe (keep the licence proof in `credits.md`: URL, date, licence):

| Need | Source | Licence |
|---|---|---|
| 3D people close to human | **MPFB 2 (MakeHuman for Blender)** | output and bundled assets CC0 |
| 3D base bodies | Blender Studio Human Base Meshes | CC0 |
| Body animations (no Mixamo) | **Quaternius Universal Animation Library 1 + 2** (~250 moves on one rig) | CC0 |
| Low-poly people, animals, props | Quaternius, Kenney, KayKit | CC0 |
| HDRIs, textures, models | Poly Haven, ambientCG | CC0 |
| Real historical pictures, maps, documents (1–2 s "this is the real one" inserts) | Library of Congress, Smithsonian Open Access (API), Rijksmuseum, NASA images, Internet Archive, Project Gutenberg | public domain / CC0 (check each item) |
| Music with more moods | own procedural (default); Incompetech (Kevin MacLeod) | CC-BY 4.0, credit line needed |
| Sound effects | BigSoundBank, Kenney, OpenGameArt | CC0 |
| Fonts | Google Fonts | OFL |

Did not answer today (retry later, do not depend on them): Wikimedia Commons API (429, needs a slow rate and a proper
User-Agent), Openverse (504), The Met API (410), CMU motion capture (no reply), Musopen (403).
Never use: anything NC, ND or "editorial"; "royalty-free" music pools that often trigger Content ID claims; real people,
logos, film or game footage.

---

## 4. Strategy for the next 4 weeks (16 Nov – 13 Dec), then review

The owner's rule stays: long videos come first. The plan below makes fewer, better Shorts and gives every upload room.

| Item | Recommendation | Why |
|---|---|---|
| Long video | **1 per week, 6–8 min**, Style T (or F), one series at a time | Ink / Paint / History Matters post weekly or slower. Go to 8–10 min only after two long videos in a row hold ≥ 40 % average viewed |
| Long video slot | **Friday 15:00 UTC** (10:00 US Eastern, 15:00 UK, 20:00 PKT), same slot every week | 10:00 Eastern is the commonest long-video slot (Simple History, Kurzgesagt, Weird History, Chill Dude); Friday gives the weekend |
| Cut Shorts per long video | **3–4, not 8–10**: only items with a real open question and a strong object | 5 of 20 cut Shorts passed 300 views; the rest cost Kaggle hours (B-002 Shorts: 6.6 GPU h) and upload quota for nothing |
| Cut Shorts timing | **1 per day** on Sat, Sun, Mon, Tue after the long video | §1.1 |
| Cut Short length | 20–35 s, starts on the answer's strangest picture, fully re-timed (no slow carry-over lines) | cliff at 5–7 s in §1.2 |
| Standalone Shorts | **3 per week** (Wed, Thu + one spare day), Style F by default | Style F holds viewers better and needs no Kaggle |
| Standalone length | 30–45 s now. 50–65 s "story" Shorts only when the script has setup → turn → twist and the animatic holds | Rick's 60–67 s hits; our hooks are not ready for it yet |
| Total | **7 Shorts a week = 1 per day**, never two within 12 h | §1.1. Go to 2 per day (≥ 8 h apart) only after the median Short passes 5,000 views for two weeks |
| Shorts slot | **16:00 UTC daily** (11:00 US Eastern, 16:00 UK, 21:00 PKT). A future second slot: 22:00 UTC. Never 00:00–11:00 UTC | Metricool peak for our brand; inside every big channel's posting window; US is our biggest audience |
| Style R (Zack-like) | 1 test Short every 2 weeks as now, built as in §6.2 | owner's interest; cheap "studio backdrop" look |
| Compilation | after 4 weeks, only from Shorts that held ≥ 70 % average viewed | do not compile weak Shorts |
| Topics | 60 % "Why [everyday object / body / machine] …", 40 % one-odd-object history; long-video series built around the Shorts topic that wins | §1 "what is working" |

Week shape: Fri long video → Sat/Sun/Mon/Tue cut Shorts → Wed/Thu standalone Shorts → Fri next long video (its slot replaces
that day's Short; the Short moves to the spare day).

Targets to judge the 4 weeks (all measurable in the API):
- stayed vs swiped ≥ 65 % (now 50 %)
- relative retention at 10 % ≥ 0.6 (now 0.11–0.58)
- average viewed ≥ 75 % on Shorts (now 66 %)
- no Short under 100 views after 48 h (now 9 of 23)
- long video: ≥ 35 % average viewed and at least 50 views from search + suggested

Honest expectation: these changes should lift the floor (no more dead Shorts) and the median. Nobody can promise a breakout:
Ink Explainer needed 14 long videos, and Rick's Clips already had about 120 earlier Shorts and an audience before its
explainers took off.

---

## 5. Existing videos: what to change

Exact titles, tags (338–429 characters each, counted YouTube's way) and the 3 hashtags for all 31 videos are in
`docs/audit/metadata_fixes.json`. Rules used:

- **Titles:** open question (Why / How / The X That…), 4–8 words, under 50 characters, the object named, no "#Shorts", true to
  the script (hedged where the script hedges: "Probably Never Said Arrr"). 18 cut-Short titles change; standalone and long
  titles stay.
- **Do not touch a video in its first 48 h** (the feed may still be testing it; "Parrots" had 1,029 views in 9 h). Each fix has
  an `apply` time.
- **Tags:** specific first (the object, the person, the place, the question people type, common misspellings), then the
  episode, then 6–8 broad ones. No two Shorts with identical tags.
- **Hashtags:** exactly 3 at the end of the description, topic first; `#TrueWhys` never in the first three (the first three
  show above the title).
- **Descriptions:** line 1 = the hook sentence with the main search words (first 140 characters); cut Shorts keep the
  "▶ Full story" link; add one line `More true whys: https://www.youtube.com/@truewhys?sub_confirmation=1`; sources stay.
- **B-002 long:** chapters "8. The ale conner" (no "#"), fix both broken links, replace Wikipedia with the primary sources in
  `sources.md`.
- **Long-video titles** stay. For Studio's Test & Compare (owner): B-002 → "The Worst Jobs in English History, Ranked" /
  "Why Nobody Wanted These 8 Jobs in Old England"; B-003 → "Why Half of What You Know About Pirates Is Wrong" /
  "What Pirates Were Really Like (10 Myths Checked)".
- **Thumbnails:** long thumbnails A are fine; keep testing B and C. Next ones: a small scene with a situation, not only a face
  (Ink style: who + where + 2–3 plain words).
- **Captions:** upload English SRT for the 3 long videos (400 units each; do it on a day with no uploads).
- **Playlists:** add B-003 to "Full Stories". Create "Pirate Myths", "Worst Jobs in History", "Animals on Trial",
  "Why Does That Happen? (Science and Body)", "Strange History". Each long video first in its playlist, then its Shorts.
- **Channel page:** remove "Shorts every day" and "8–12 minute" from the description; keep the keywords.
- **Expectation:** renaming a Short that already finished its feed test rarely revives it. The reason to do it is search,
  a tidy channel page, and so new viewers who open the channel see strong titles. The 7 Shorts that never got a feed test are
  good topics (sin eater, toad eater, saltpetre man, fuller): **remake the best 2–3 later as new standalone Shorts with new
  hooks**; do not re-upload the same file.

Owner jobs in Studio (the API cannot do these): set "Related video" on every cut Short; pin the comments; add end screens
(best-for-viewer + subscribe) to the 3 long videos; choose the channel trailer / featured video (use the best Short for now)
and name the home sections; run Test & Compare.

### 5.1 Two rule checks for the owner (his decision, not production's)
1. **Religion rule.** B-001 long (chapter "The real why"), and the Shorts "Why the Church Put Bugs on Trial" (hook: "Follow the
   money") and "The Weevils Who Were Offered Their Own Land", present an economist's theory that church courts used pest trials
   to win back unpaid tithes ("Either way, the church's power looked stronger, and more people paid"). It is attributed to
   Peter Leeson and is about a medieval institution, not the faith, but the tone is close to criticism. CLAUDE.md says: neutral
   and factual, and "if a topic could offend religious viewers, skip it". Options: keep (attributed history), soften the title
   and hook (done in the fixes file), or set the one Short private. Future topics: avoid motives of religious institutions.
2. **"Altered content" field.** Cartoon videos do not need it, so leaving it out is correct for Style T and F. For a Style R
   Short that could be mistaken for real footage, YouTube's policy requires the box to say Yes. Either keep Style R clearly
   stylised (recommended, §6.2) or the owner accepts that rule for those videos. Zack D. Films labels invented stories
   "(fiction)" in the title.

---

## 6. Production standards for every new video

### 6.1 Characters (2D cast v2)
- Older proportions: head about 1/3 of body height (not 1/2), smaller eyes with eyelids and brows that can look bored, smug,
  suspicious, shocked; no rosy cheeks; shoulders and neck; hands that hold things.
- Default expression is dry/deadpan; emotion spikes on the key word. Humour comes from faces and props, not from a presenter.
- Role by hat, uniform and one prop. 2–3 characters reacting to each other in most shots.
- **Wy stays the brand** (logo, avatar, end of long videos) but stops presenting from the desk. In Shorts, Wy appears only when
  he is the one the strange thing happens to. Give Wy the same older proportions so the brand matches.
- Must not look like Rick's (white round heads, stick limbs) or Ink's (messy-hair stick people). Keep our skin tones, thick
  dark outline and brand palette.

### 6.2 Style R, our own "close to human" 3D (the Zack-type look, built free)
- People: MPFB 2 humans with stylised proportions (head ~15 % bigger, larger eyes, simple clothes, flat clean materials), saved
  once as a small cast in `library/characters/` (6 people, varied). Motion: Quaternius Universal Animation Library retargeted
  to the rig; poses can be toy-like and snappy. No lip-sync (narration only).
- Staging: plain studio backdrop in our own colours (deep navy to coral or cream gradient, NOT Zack's cyan) + one hero prop
  from Poly Haven / Sketchfab CC0. No big sets. Shot order: macro of the object → person using it → cross-section or X-ray →
  result.
- Render on Kaggle GPU; this look needs few samples and few plates, so one Short should fit in about 1 GPU hour.
- First tests: three "How [everyday thing] works inside" topics that we already know start well.

### 6.3 Shorts: the first two seconds and the last two
- **Frame 1 = the title's strange object, in action, with a character reacting, filling the frame** (character ≥ 45 % of frame
  height or a close-up of the object). Title words on screen from frame 1 (Style F already does this).
- First spoken line ≤ 2 s and it opens a question; it never gives the answer. Second line raises the stakes ("but", "so").
- New picture every 1.5–2.5 s; a camera move or pose change on every key word; never the same framing twice in a row.
- Bright, saturated sets; no frame with more than a quarter of empty floor or wall.
- Cut Shorts are rewritten for the Short (new lines where the long video is slow); the answer lands in the last 5 s.
- **No full-screen end card.** The story runs to the last frame; the last shot matches the first so the video loops; the
  sign-off is a small Wy ✓ badge in a corner during the final line (0.7 s at most). This needs the owner to change the
  "last 2 s = Wy card" rule.
- One line that invites an argument or a choice ("Would you have climbed it?" is good; keep doing this) → comments.
- QA numbers to record in `qa.md`: character height on frame 1, seconds until the first cut, number of shots, seconds of
  end card (0).

### 6.4 Scripts
- Start inside the scene ("In 1204 a French soldier is climbing up a castle toilet"), never "Today we check ten…".
- One person, one place, one year, one object. A turn every 5–7 s. Numbers people can picture.
- Short spoken sentences; the last line answers the title and points back to the first picture.
- Long videos: the first 30 s is the single strangest story told as a scene, then the promise. No greeting, no "I'm Wy".
  A new reveal at least every 40 s. Each list item starts with its picture and question, not with "Number seven:".
- Titles before scripts: write 10 titles, keep the one that passes "would an adult stop for this?", then write to it.

### 6.5 Long-video visuals
- Every shot is a scene from the story with 2+ characters and the object; the desk returns at most once per chapter.
- Mix: wide (where) → medium (who) → close (the object) → insert (map, real public-domain document or picture, diagram).
- Real evidence inserts (Library of Congress / Smithsonian public-domain items) for 1–2 s where a source exists.

### 6.6 Titles, descriptions, tags, thumbnails (all new uploads)
As §5. Plus: `lib/upload_shorts.py` must stop adding "#Shorts" to titles and must build tags per Short; chapters never start
with "#"; upload SRT captions with every long video.

### 6.7 Publishing
Slots as §4. Never two uploads within 12 h. `publishAt` always on the fixed slot. Max 5 uploads per day for quota.
Public text never promises a schedule (existing rule).

### 6.8 Measuring
`yt_stats.py` adds per video: stayed % (`engagedViews ÷ views`), relative retention at 10/50/90 %, Shorts-feed views, top
countries. The daily review diagnoses with them: no feed views → spacing/seeding; feed views but stayed < 60 % → first frame;
stayed fine but relative retention < 0.5 → pacing; all fine but no growth → topic. Start `topic_results.md`.

---

## 7. Prioritised plan for the production session

**P0 — today, no new production needed**
1. C6–C10: Why/How titles without "#Shorts" (done on your side); publish 1 per day at 16:00 UTC if the owner agrees.
2. Kaggle: one read-only `kernels list --mine`; report to the owner if it fails. Freesound: note the 403.
3. Ask the owner for decisions D1–D5 (below) in one short message.

**P1 — this week, existing content only (edits are reversible; ~50 quota units each, do them on days without uploads)**
4. Apply `metadata_fixes.json` (titles after checking each against the script, tags, 3 hashtags, description line 1 +
   subscribe line), respecting each `apply` time. Write a small script `tools/yt_apply_fixes.py` that reads the JSON, does
   `videos.update`, and saves before/after to `docs/audit/applied.json`. No AI/altered field, as always.
5. B-002 description: chapters without "#", fix links, primary sources.
6. Channel description: remove the schedule promise. Add `branding/TrueWhys_channel_text.md`.
7. Playlists: B-003 into "Full Stories"; create the 5 topic playlists and fill them.
8. SRT captions for the 3 long videos.
9. Code: `lib/upload_shorts.py` (no "#Shorts" in titles, per-Short tags, 3 hashtags); `lib/yt_stats.py` (§6.8);
   start `topic_results.md` from the saved stats; trim `STATUS.md` to the live items.
10. Update CLAUDE.md and the skill with the rules the owner approves (D1–D5), and move old text to `docs/rules_history.md`.

**P2 — when the owner allows new production**
11. Cast v2 (§6.1): model sheet for 6 characters + Wy, one contact sheet to the owner before any episode uses it.
12. First-frame and no-end-card rules in `flat2d.py`, `compose.py`, `shorts.py` (§6.3); QA numbers in `qa.md`.
13. One week on the §4 calendar: 1 long (Fri 15:00 UTC), 3–4 cut Shorts, 3 standalone, 1 per day at 16:00 UTC.
14. Remake 2–3 of the never-tested topics as new standalone Shorts.
15. Style R test as §6.2 (MPFB 2 + Quaternius, studio backdrop).
16. After 4 weeks: review against the §4 targets; then decide Shorts per day and long-video length.

**Decisions only the owner can make**
- D1 Spacing: 1 Short per day (never two within 12 h) instead of "3 h apart, all within 24 h".
- D2 End card: story to the last frame + small corner badge instead of the 2 s Wy card.
- D3 Cast v2: older, drier characters; Wy stays as brand but stops presenting in Shorts.
- D4 Religion-rule review of the three B-001 items (§5.1).
- D5 Fewer cut Shorts (3–4 per long video) and the fixed slots (long Fri 15:00 UTC, Shorts 16:00 UTC).

**How the audit session will verify (it re-pulls the live data; it does not take anyone's word)**
- V1 No public title contains "#Shorts"; every changed title equals the fixes file or a script-checked variant.
- V2 Every video: ≥ 15 tags, 300–500 characters, no two Shorts with the same tag list.
- V3 Every description: exactly 3 hashtags, none starting with a digit, first one a topic; cut Shorts contain the long-video link.
- V4 B-002 description has no "#8…#1" and no broken link.
- V5 Channel description has no "every day" and no "8–12 minute".
- V6 B-003 long is in "Full Stories"; the topic playlists exist and are not empty.
- V7 No two future `publishAt` times closer than 12 h (if D1 is approved); Shorts on 16:00 UTC, long on Fri 15:00 UTC.
- V8 `lib/upload_shorts.py` no longer adds "#Shorts"; `yt_stats.py` outputs stayed % and relative retention;
  `topic_results.md` and `branding/TrueWhys_channel_text.md` exist.
- V9 No video carries the altered/synthetic field; no AI wording in any public text.
- V10 After new production: frame 1 of each new Short (public frame image) shows the object and a character ≥ 45 % of the
  height; the last frame is not a full-screen card (if D2 is approved).
- V11 Two weeks later: the §4 targets, from the Analytics API.

---

## 8. Addendum 15 Nov 06:05 UTC — the 14-day buffer (as reported by the production session)

The production session reports that the owner decided: follow the audit, and keep 14 days of content scheduled ahead, then stop.
C6–C10 now run one per day, 15–19 Nov at 16:00 UTC. The buffer therefore covers **20 Nov – 3 Dec**:

| Date (UTC) | 15:00 | 16:00 |
|---|---|---|
| Fri 20 Nov | Long video L4 | — |
| Sat 21 – Tue 24 Nov | | L4 cut Shorts 1–4 (3 if only 3 are strong; then a standalone on Tue) |
| Wed 25, Thu 26 Nov | | Standalone S1, S2 |
| Fri 27 Nov | Long video L5 | — |
| Sat 28 Nov – Tue 1 Dec | | L5 cut Shorts 1–4 |
| Wed 2, Thu 3 Dec | | Standalone S3, S4 |

Total: 2 long videos, 6–8 cut Shorts, 4–6 standalone Shorts.

How to fill it without losing the learning loop (important):
1. **Standards before volume.** First the composer changes (first frame, no end card if D2 is approved) and the cast v2 sheet
   (if D3 is approved). Nothing for the buffer is rendered in the old look.
2. **Two waves, not one batch.** Wave 1 = 20–26 Nov. Wave 2 = 27 Nov – 3 Dec, and its scripts and first frames are only locked
   after the first 2–3 new-standard Shorts have 48 h of data (stayed %, relative retention at 10 %). If 14 days are produced
   blind and the new first frames still lose 50 % of viewers, all 14 days repeat the same mistake.
3. **Quality beats the date** (rule number 1). If L4 is not ready for Fri 20 Nov, standalone Shorts (Style F, no Kaggle) keep the
   daily 16:00 slot and L4 moves to Fri 27 Nov. Never fill a slot with a video that fails the §6.3 numbers.
4. **Quota:** at most 5 uploads per day; spread the buffer uploads over several days; do the P1 edits on the lighter days.
5. Topics for the buffer: standalone = "Why [everyday object / body / machine] …"; long videos = one series, chosen so that at
   least 3 items are strong enough to stand alone as Shorts.
Check V7 in `verify.py` already tests this calendar (≥ 12 h apart, Shorts 16:00 UTC, long Fri 15:00 UTC).
