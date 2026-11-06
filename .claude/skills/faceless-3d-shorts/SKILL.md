---
name: "faceless-3d-shorts"
description: "Make videos for TrueWhys (@truewhys), a faceless animated curiosity channel modelled on Rick's Clips, Ink Explainer and Zack D. Films, with free tools only: long videos first, Shorts cut from them, standalone Shorts, compilations, topic testing."
---

# TrueWhys — faceless animated curiosity channel (free tools only)

Channel: **TrueWhys** (@truewhys). Tagline: "The real story behind life's weirdest whys".
Three reference channels were studied in Nov 2026. We copy their FORMAT, never their
videos, scripts, titles, characters, art, voice or branding.

---

## 1. What the research showed

### Rick's Clips (@RicksClips3000) — Shorts model
- 139K subscribers, 147 Shorts, **no long videos**, ~1 upload per day (Oct–Nov 2026).
- The channel went through three phases. Only the last one exploded:

| Phase | What it was | Videos | Median views | Lesson |
|---|---|---|---|---|
| 1 (oldest) | Movie clips with "#shorts #movie" | 7 | 0.04M | Reused footage: copyright risk, weak. Never do this. |
| 2 | Comedy skits and other artists' comics read aloud over game footage, emoji titles 💀😭🤣 | 115 | 0.53M | Reused comics = reused content. Never do this. |
| 3 (now) | Original cartoon characters explaining a curious real-world story | 25 | **7.3M** (16 of 25 above 5M; 198.5M views in total) | **This is the format we make.** |

- Phase-3 top videos: The Ancient Jar That Warned an Empire (31M), Why Perfect Railroads
  Don't Work (19M), The Job Nobody Wants in Japan (16M), The Window That Breaks Japan's
  Gambling Law (13M), Your Brain's Secret Idea Zone (13M), Why Sailors Carried Storm Oil
  (12M), What the Grave Bell Really Meant (11M), Levels of Pirate Cannonballs (8.8M),
  An Unstoppable Spear vs an Unbreakable Shield (8.7M), Why Humans Can't Pick Random Numbers (8.3M).
- **Look:** flat 2D cartoon characters (simple heads, thin outlines, role shown by hat,
  uniform and props) composited on colourful, stylised 3D-rendered rooms and places
  (prison, pier, ship deck, casino, office, castle, shop). Captions: one big bold word at a
  time, white with a black outline, in the middle of the frame. One narrator.
- **Titles that won (median views):** "The … That/Who …" 10.5M · "Why …" 8.3M ·
  "Levels of …" / "X vs Y" 8.8M · "What If / Would You" 5.2M · "How …" 2.6M. No emojis.

### Zack D. Films (@zackdfilms) — secondary model
- ~29M subscribers, ~4,100 videos, ~2 per day, mostly Shorts plus ~9-minute long videos.
- Realistic 3D (Blender, team, render farm). Body/medicine, survival, disasters, brands.
- Titles: Title Case + one emoji (🤔😨😢😮🙂). Long videos: disasters, company mistakes,
  compilations ("… Unreleased Videos", "… Creepiest Stories (Compilation)").

### Ink Explainer (@Inkexplainer96) — long-video model
- 161K subscribers, **20 long videos, no Shorts**, about 6–7 months old, ~1 upload every
  9–10 days. 27.7M views in total. Length 4–21 min, median **9.9 min**.
- Hand-drawn-look cartoon: simple characters with messy hair and fur clothes on painted,
  detailed backgrounds (savanna, caves, snow, cities). Narrated explainer, sources linked in
  every description ("researched using published studies… actually accurate").
- **One series made the channel:** 16 of 20 videos are about ancient/early humans and they
  hold 26.8M of the 27.7M views. The breakout, **What Did Ancient Humans Actually Do All Day?**
  (11.2 min), has **18M views = 65% of the channel**. Others: What Did Ancient Humans Do When
  It Rained All Week? (1.9M), Why Are We the Only Human Species Left? (1.6M), The Disturbing
  Ways Ancient Humans Survived Winter (1.4M).
- **The winning idea:** an everyday, relatable question ("what did they do all day / when it
  rained / at night / for fun?") asked about a time or group nobody pictures in daily life.
- **Warning sign:** after the 18M hit, 6 near-copies (all night, for pleasure, predators…) have
  a median of only 0.10M so far, versus 0.46M before it. Repeating the exact title with one
  word changed gives diminishing returns.
- **Thumbnails:** one big expressive character + a simple scene + **1–3 words in bold caps**,
  usually a question: "NO JOBS", "RAINED ALL WEEK", "WHY AFRICA?", "STILL SURVIVED?".

### What this means for us
- **Style T (Toon) is our main style**: original 2D cast on 3D toon backgrounds. It needs
  no GPU — tested: one 1080×1920 background renders in ~2 min on CPU, a 20 s Short composes
  in ~1 min. Everything runs inside the Claude Code session.
- **Style R (Realistic 3D)** is a test every 2 weeks only (needs Kaggle GPU).
- **Long videos come first (owner's rule: not a Shorts-only channel).** Rick has no long
  videos; Zack's long videos (~9 min, disasters, company mistakes, compilations) show the long
  format works, and Ink Explainer grew to 161K with long videos only. Neither Ink nor Rick
  cuts Shorts from long videos: that is our edge. Each long video is a Shorts mine: cut as
  many stand-alone Shorts from it as the content supports.
- Quality beats frequency for long videos: Ink grew posting every 9–10 days.
- When a long video breaks out, build a **series around the idea, not the exact title**:
  change the era, group or angle (see §7 "Daily Life Back Then"), and keep testing other formats.
- Topics: curious real-world mechanisms, loopholes, odd jobs, hidden history,
  psychology, "levels of", "X vs Y". Make the viewer go "wait, why?" in the title.

---

## 2. Hard rules (never skip)

1. **Original only.** Own scripts, own research, own cast, own backgrounds. If Rick, Ink or Zack
   covered a topic, use a clearly different angle and different visuals, or skip it.
2. **Never use** movie/TV clips, other creators' comics or art, game footage, or anyone's
   voice. That is what made Rick's early phases weak and risky.
3. **Our cast must not look like Rick's or Ink Explainer's.** No plain white round heads with
   dot eyes and stick limbs, no stick-figure cavemen. Use the cast bible (§4).
   Don't start an "ancient humans / Stone Age" series: that is Ink Explainer's territory.
4. **Facts must be true.** 2+ reliable sources per claim in `sources.md`. Health topics: no
   advice or dosages, add "not medical advice". Real companies: documented facts only.
5. **Free, licensed assets only**, every one in `credits.md`.
6. **No real people's likeness, no logos, no gore.**
7. **Variety:** rotate categories, backgrounds, cast and title patterns.
8. **Disclosure:** tick "altered or synthetic content" only for realistic footage that
   could be mistaken for real events (Style R). Cartoon (Style T) normally doesn't need it.

---

## 2b. Professional quality first (owner's rule number 1)

Quality beats length and posting frequency, always. If a tool can't deliver the quality,
make the episode **shorter** or take **longer** (a long video may take 2–3 days). Never ship
something that looks amateur to keep a schedule.

**What "professional" means for every video:**
- **Story:** a hook in the first 3 s (Shorts) or 30 s (long), a clear question, a payoff, no filler.
  Long videos get a retention beat every 30–45 s (new reveal, question or visual surprise).
- **Animation:** 30 fps; eased motion (no linear moves); characters always alive (breathing,
  blinks, small head moves); a gesture or expression change on every key word; 3–5 mouth
  shapes timed to the voice; real 3D camera moves through the scene (dolly, orbit, parallax),
  not only zooms on a flat picture; motion blur on fast moves.
- **Look:** consistent cast and art style, warm key light + rim light, soft shadows, one
  colour grade per episode from the brand palette, clean outlines, no stretched or blurry
  images, 1080p minimum (renders at full resolution, never upscaled for finals).
- **Sound:** clean voice (pauses at commas, emphasis on key words, re-generate any line that
  sounds robotic), 2–4 layered SFX per shot, music that changes with the mood, voice peaks
  −3 dB, music −18 to −22 dB under voice, final loudness ≈ −14 LUFS.
- **Text:** captions in brand style with the current word highlighted; chapter cards and
  lower-thirds animated in, not just appearing.

**Production stages (every video):**
1. Script + sources → owner approves the topic and title.
2. **Voice + animatic** in this session: low-res frames for every shot, timed to the real voice
   (`animatic.mp4`). The owner approves it before any final render. Fix pacing here, it's cheap.
3. **Final render on Kaggle GPU** (§6 settings). Render chapter by chapter; check a contact
   sheet of frames after each chapter.
4. **Finish** in this session: compositing, captions, sound design, colour, end screen, thumbnails.
5. **QA gate** (§9), with `qa.md` filled in. Any failed item is fixed before upload.

**Typical schedule at the start (no rush):**

| Day | Long video (5–8 min) | Shorts |
|---|---|---|
| 1 | Research, script, voice, animatic → owner approval | — |
| 2 | New reusable assets, Kaggle final render by chapter | — |
| 3 | Finish, sound, QA, thumbnails, upload | Cut Shorts re-composed and queued |

**Asset library (`library/index.md`):** every episode adds 1–2 reusable sets, props, poses or
sounds (for example: castle hall, ship deck, market street, lab, classroom, forest). As the
library grows, episodes get longer and faster to make without losing quality.

---

## 3. Video types

| Type | Length | Made how |
|---|---|---|
| **B. Long video (priority)** | 5–8 min at the start, 8–12 min once the asset library is big | Style T, 5–10 chapters or list items |
| **C. Shorts cut from B** | 20–55 s, **5–10 per long video** (as many as stand alone) | Re-compose B's moments in 9:16 from the same assets (not a crop), new hook line |
| A. Standalone Short | 35–55 s | Separate topic, Style T (or Style R test) |
| D. Compilation | 8–15 min | 10–20 of our own Shorts by theme, vertical on blurred 16:9 background, narrated links |

**Cadence (quality first, no fixed schedule):**
- Start: 1 × B every 2–3 days at most (often 1 per week), each giving 5–10 × C, plus A Shorts
  only when they meet the same quality bar.
- Increase B only when quality is consistently there and Kaggle hours allow. Public text
  (banner, description) says "Full stories" with no fixed schedule.
- Style R test every 2 weeks; D every 4 weeks once 20+ Shorts exist.
- Posting: B first, then its C clips 1–2 per day over the following days (never two clips from
  the same B in a row), A Shorts in between. Target 1–2 Shorts per day.

---

## 4. Cast bible (create once in `library/cast/`)

- Build an original recurring cast of 6–8 characters in `library/cast/cast.md` + one
  Python drawing module per character in `library/cast/*.py`.
- Our design language (different from Rick's and Ink's): wide egg-shaped heads in varied warm skin
  tones, big oval eyes with white highlights, eyebrows, rosy cheeks, rounded bean bodies
  with short rounded arms and legs, thick dark outline. Role shown by hat, uniform, props.
- Each character needs: mouth shapes (closed, small, open, wide), blink, 4 expressions
  (neutral, surprised, worried, smug), arm poses (down, point, raise, shrug), facing left/right.
- Mascot and narrator character: **Wy** — egg head in warm skin tone, big curious eyes looking up,
  brown hair curl shaped like a question mark, coral shirt with cream collar, yellow ✓ badge.
  Appears in hooks and in the last 2 s of every Short ("Follow for more true whys").
  The reference drawing is in `branding/TrueWhys_logo.svg`; match it exactly.
- Brand colours: teal #0F6B78, deep teal #0B3F4C, navy #10263B, yellow #FFC93C, coral #FF6B5B,
  cream #FFF4E0, ink #2A1C1E, mint #5ED3B5. Fonts: Lilita One (titles, thumbnails), Fredoka
  (taglines), Poppins Bold (captions). Channel text: `branding/TrueWhys_channel_text.md`.
- Start from `examples/toon_poc/make_short.py` (radio officer) and improve it.

---

## 5. Pipeline — Style T Short (runs fully in the session)

Folder: `episodes/A-<NNN>-<slug>/`

1. **Topic (`topic.md`)** — 10 candidates, pick 1. Category tag (§8). Title in a winning
   pattern (§1). Premise + twist.
2. **Research (`sources.md`)** — 2+ sources per claim.
3. **Script (`script.md`)** — 100–140 words (35–50 s). Line 1 = the title's question or claim.
   Then: setup (who/where/when) → the strange detail → the explanation → the twist or a
   "so next time you…" ending. Short spoken sentences. Tag lines with shots `[S03]`.
4. **Shot list (`shots.json`)** — new shot every 2–3 s: background id, camera move
   (push-in, pan, cut-in close-up), characters, pose, expression, props, caption keywords.
5. **Backgrounds (`library/backgrounds/`)** — Blender scripts, bright toon materials, warm
   lights, 1080×1920 for Shorts and 1920×1080 for long videos, 16–24 samples + denoise.
   Reuse and re-dress existing rooms; one new place per episode at most.
6. **Voice (`audio/voice.wav`)** — Kokoro, one call per line, record each line's duration
   for word timings. Default voice `am_michael`, speed ~1.08.
7. **Compose** — animatic and previews here; final frames from Kaggle (§2b, §6). Python (Pillow + numpy) + ffmpeg:
   background crop/zoom per shot, characters with mouth from the audio level, blinks, bob,
   gestures on key words, soft shadows; captions 1–2 words, current word highlighted, bold
   font with thick outline, at ~38–42% of the height (above faces), never in the top or
   bottom 15%. Add SFX on cuts and actions, very quiet music.
   Encode H.264 `-preset veryfast -crf 20`, AAC 192k, 30 fps. Audio ≈ −14 LUFS.
8. **QA (§9)** → **`upload.md`** (Related video: the closest long video): title, description from the upload-default template in
   `branding/TrueWhys_channel_text.md` (2 lines + sources + credits), 3–5 hashtags incl.
   #shorts and #TrueWhys, pinned comment ("What why should Wy answer next?"), playlist name.

## 6. Pipeline — Style R realistic Short (test every 2 weeks)
Same steps 1–4 and 6, then realistic Blender scenes per shot (Blender-made or Sketchfab characters, Poly
Haven HDRIs/props, X-ray and cutaway looks, rigid-body physics), rendered on Kaggle GPU
with `notebooks/render_kaggle.ipynb`. Captions and edit as §5. Tick the
"altered or synthetic content" box at upload when footage could pass as real.

**Looks that render well without heavy simulation:** X-ray / cutaway (fresnel-emission
skin, opaque organs), slow motion (stretched keys + motion blur), scale shots (tiny
human, giant object, low wide lens), rigid-body falls and collisions (bake first),
miniature/tilt-shift overviews for disasters and cities. Avoid early on: cloth, fluids,
smoke, crowds, lip-sync.

**Render settings**

| Where | Engine | Settings | Measured |
|---|---|---|---|
| Claude Code session (4 vCPU, no GPU) | Cycles CPU | **Animatics and previews only**: 540×960 / 960×540, 8–16 samples + denoise | ~2 min per 1080×1920 still at 24 samples (tested) |
| Kaggle free GPU (2×T4, ≈30 h/week, 12 h per run) | Cycles GPU (OptiX/CUDA) | **All finals**: Style T 1920×1080 (long) / 1080×1920 (Shorts), 64–128 samples + denoise, motion blur, real 3D camera moves; Style R 128+ samples | measure on the first episode, log it |

If the week's Kaggle hours can't cover an episode at full quality: shorten it, split it into
Part 1 / Part 2, or wait for the reset. Never drop to CPU finals or lower samples to "fit".

EEVEE needs a GPU with OpenGL; headless, use Cycles. Set
`scene.render.use_persistent_data = True`; render only the frames needed.

## 7. Pipeline — B long video (priority), C cut Shorts, D compilations

### B. Long video (8–12 min) — `episodes/B-<NNN>-<slug>/`
1. **Pick a format that clips well:**
   - **Full Story** — one story with a turning point (disaster, company mistake, odd invention,
     strange law, history mystery), 6–8 chapters.
   - **Ranked List** — "12 Strangest Laws Still Active, Explained": every item is a Short. Best for clipping.
   - **Levels Of …** — "Every Level of Medieval Armour": every level is a Short.
   - **X vs Y** — a deep comparison with rounds.
   - **Daily Life Back Then** — an everyday question about a past group or place:
     "What Did Medieval Knights Actually Do All Day?", "What Did Sailors Do When the Wind
     Stopped?", "A Normal Day in Ancient Rome's Fire Brigade". Every hour or activity is a Short.
     (Not Stone Age/ancient humans — see rule 3.)
2. **Research** — timeline or item list, 2+ sources for each claim.
3. **Outline (`outline.md`)** — cold open with the strangest moment (0:00–0:30), then chapters
   of 60–90 s that each end on a mini-cliffhanger, and a "what happened next" ending.
   **Mark every clip candidate** (each chapter or item, the cold open, any single fact that
   stands alone) with an id `C1…Cn`.
4. **Script** — 1,300–1,900 words (~2.6 words/s). Third person for history and brands, "you"
   for scenarios. Each chapter or item must also make sense on its own.
5. **Shot list** — new shot every 3–5 s; shots tagged with `chapter` and `short_cut`.
6. **Animatic first** (voice + low-res frames, owner approval), then **final render on Kaggle
   one chapter at a time**, then compose and join with ffmpeg. Chapter title cards, quiet music bed (−20 dB under
   voice), 20 s end screen with the wordmark.
7. **Thumbnails** — 2 options at 1280×720: one big expressive cast member + the strange
   object or place + **1–3 words in bold caps**, usually a question ("NO WIND?", "WHY CROOKED?"),
   Lilita One in yellow/cream with ink outline. For YouTube's thumbnail test.
8. **`upload.md`** — title, description with clickable chapters (first at 0:00), sources,
   credits, pinned comment ("Which part surprised you most?"), playlist "Full Stories".

### C. Shorts cut from B — as many as stand alone (usually 5–10)
- For each `C` id: new 1-line hook recorded fresh (the title's question), 20–55 s of the
  moment, re-composed at 1080×1920 (move characters and captions for the vertical frame).
- Types: **chapter clip** (35–55 s), **list-item clip** (30–45 s), **cold-open teaser**
  (20–35 s), **quick fact** (20–30 s, one surprising number or detail).
- Must make sense with no context. End line: "Full story on TrueWhys." `upload.md` notes the
  **Related video** = the long video.
- Skip moments that need the earlier chapters to make sense.

### D. Compilations — see §3.

## 8. Topic categories (rotate evenly for the first 4 weeks)
1. Hidden history & ancient mysteries (jars, bells, castles, empires)
2. Strange laws, loopholes & rules
3. Odd jobs & how money really works (lotteries, casinos, shops)
4. Psychology & brain tricks
5. "Levels of …" and "X vs Y" (pirates, knights, weapons, inventions)
6. Survival scenarios & what-ifs
7. Human body & health facts
8. Animals & nature
9. Science & strange experiments
10. Company & brand stories
11. Daily life back then (eras, jobs, places — not Stone Age)
No category twice in a row. Log results in `topic_results.md` (date, title, type B/C/A,
long-video format or Short type, category, style, title pattern, views at 48 h and 7 d,
average % viewed, likes; for B also where retention drops). After 4 weeks: rank long-video
formats, Short types, categories, styles and title patterns; shift 80% of output to the
winners, keep 20% for tests.

## 9. QA checklist (professional gate, fill in `qa.md`)
- [ ] Owner approved the animatic before the final render
- [ ] Hook in the first 3 s (Shorts) / 30 s (long); title question answered by the end; no filler
- [ ] A visual change at least every 3 s (Shorts) / 5 s (long); retention beat every 30–45 s (long)
- [ ] Motion is eased and smooth; no frozen characters; mouths in sync; no jitter or popping
- [ ] Final frames are full-resolution Kaggle renders; no blurry, stretched or upscaled images
- [ ] Consistent cast, lighting and colour across all shots
- [ ] Captions readable, in brand style, inside the safe area, not covering faces
- [ ] Voice natural (no robotic lines left), SFX on actions, music fits; loudness ≈ −14 LUFS, no clipping
- [ ] Every fact in `sources.md`; every asset in `credits.md`
- [ ] Cast is ours; no reused clips, comics or art; no logos or real faces
- [ ] Contact sheet of frames checked, and the full video reviewed start to finish
- [ ] Thumbnail (long) readable at phone size; 2 options made

## 10. Competitor check (monthly)
Channels: @RicksClips3000 (`/shorts`), @zackdfilms (`/shorts` and `/videos`), @Inkexplainer96 (`/videos`).
`yt-dlp --flat-playlist -J https://www.youtube.com/@<handle>/shorts` (or `/videos`) lists titles, views and lengths
(works from the session; opening single videos is blocked by YouTube's bot check, so
don't try). Save a summary in `research/<handle>-<date>.md`: new top titles, patterns,
anything we should test. Never copy a title or topic angle.

## 11. Free tool stack (only the Claude plan is paid)

| Job | Tool | Notes |
|---|---|---|
| 3D backgrounds and Style R scenes | Blender as Python package `bpy` (`/opt/c3d/bin/python`) | Installed by `setup.sh` |
| 2D cast, compositing, captions | Pillow + numpy, fonts in `/usr/share/fonts` (Poppins Bold) | Tested in `examples/toon_poc` |
| Narration | Kokoro via `kokoro-onnx` + `/opt/kokoro/kokoro-v1.0.onnx`, `voices-v1.0.bin` | Apache-2.0, no watermark. English `am_michael`, `af_heart`; Hindi voices `hm_omega`, `hf_alpha` (lang `hi`, write Devanagari). The `kokoro` package needs Python ≤3.12, so use `kokoro-onnx` |
| Editing, mixing, encoding | ffmpeg | Pad audio with `-af apad -shortest` when piping frames |
| HDRIs, textures, props | Poly Haven API, ambientCG | CC0, downloaded in the session |
| Extra textures, sky plates, reference | Pixabay API (`PIXABAY_API_KEY`), images and videos only | Download (no hotlinking), cache searches 24 h, no mass downloads, ≤100 requests/min; no real people, logos or brands; never replaces our own cast or art |
| Sound effects | Freesound API (`FREESOUND_API_KEY` environment variable) | CC0 only, credit in `credits.md` |
| Music | YouTube Audio Library tracks in `library/music` | No API: the owner downloads them |
| Style R characters, animals, anatomy | Blender-made stylised characters first; Sketchfab API (`SKETCHFAB_API_TOKEN`, CC0 / CC-BY, downloadable, `animated=true` for moving people); free CC0 packs such as Quaternius. **No Mixamo** (owner's choice) | CC-BY needs a credit line; skip NC, ND, Editorial, NoAI |
| Final GPU rendering (Style T and R) | Kaggle via API: `kaggle` CLI ≥ 1.8 with `KAGGLE_API_TOKEN` | Episode files go up as a private dataset, a private kernel with `enable_gpu` + `--accelerator NvidiaTeslaT4` renders, `kaggle kernels output` brings frames back. Manual notebook is the fallback |
| Competitor lists | yt-dlp `--flat-playlist` | Listing only (§10) |

## 12. `shots.json` schema

```json
{
  "fps": 30,
  "resolution": [1080, 1920],
  "style": "T",
  "shots": [
    {
      "id": "S01",
      "duration_s": 2.5,
      "line": "Why do pilots shout Mayday when they're in trouble?",
      "background": "radio_room",
      "camera": {"type": "push_in", "zoom": [1.0, 1.06], "focus": [0.5, 0.55]},
      "characters": [{"id": "radio_officer", "x": 0.64, "scale": 1.3, "pose": "arm_down", "expression": "worried", "facing": "left"}],
      "props": [],
      "sfx": ["radio_static"],
      "caption_keywords": ["Mayday"],
      "chapter": null,
      "short_cut": null
    }
  ]
}
```
For long videos add `"chapter": 3` and `"short_cut": "C2"` on shots that feed a cut Short.
Style R shots use `"set"`, `"subject"`, `"action"`, `"special_view"` (e.g. "xray") and a lens in `camera`.

## 13. Folder layout
```
TrueWhys/   (GitHub repo)
  branding/ logo, banner, watermark, wordmark, channel text (TrueWhys)
  library/  cast/  backgrounds/  characters/ (3D people for Style R)  hdri/  textures/  sfx/  music/
  lib/      toon.py (compositor)  captions.py  voice.py  blender_lib.py
  examples/toon_poc/      working test from setup (radio officer, Mayday)
  notebooks/render_kaggle.ipynb   (Style R and heavy long-video renders only)
  episodes/A-001-<slug>/ … B-001-<slug>/ … C-001-<slug>/ … D-001-<slug>/
  research/  topic_results.md  render_log.md
```
