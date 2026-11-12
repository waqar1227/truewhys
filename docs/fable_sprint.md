# Fable 5.2 sprint: Style F (flat 2D), 12–14 Nov 2026 (owner instruction, 12 Nov 2026 ~07:00 UTC)

Why: Kaggle GPU is blocked (account anam318 not phone-verified), so Style T 3D finals cannot be rendered.
Owner (update 12 Nov): Fable picks the best style (flat 2D, Style T 3D on CPU if it reaches pro quality in time, or a mix). Was: in the same flat 2D
style as A-008 "The Accident That Invented Steel" (that Short was made solely by Fable 5.2). All scheduled 12–14 Nov, none later.

## Style F (flat 2D), reference: episodes/A-008-steel/final/thumb.jpg
- Clean flat vector look drawn in code (Pillow/numpy/cairo-style shapes, or SVG → PNG), thick dark outlines, soft flat shading,
  dark teal/brown backgrounds with warm glows, round chunky characters with big white eyes and blush cheeks.
- Big word-by-word captions in Lilita One (yellow key words, white others, thick dark outline), title block at top in the hook.
- Hook visible from frame 1 (character + strange object + title words). Smooth motion: easing, squash/stretch, camera push-ins,
  particles, glows; never a static slideshow. Wy (branding/) can appear; end card = last 2 s Wy ✓ "Follow for more true whys".
- Renders fully on CPU here (no GPU needed, no Kaggle). 1080×1920 30 fps for Shorts; 1920×1080 for long videos.
- Voice: Gemini TTS via lib/voice_gemini.py (proxy key; 10 requests/day/model, one per Short/chapter; FLAC masters in voice/),
  Kokoro am_michael fallback. Logo/colours/fonts: branding/. Music: library/music or lib/music.py. SFX: CC0 / in-house.
- All CLAUDE.md rules still apply: ethics, 2+ sources per claim, qa.md fully ticked, −14 LUFS, no AI fields, never mention AI.

## Ready material (scripts + sources already written; reuse, don't redo)
- A-005 brain freeze: script v2, sources, Gemini voice (voice/ch0.flac), timing.json, upload_meta.json (was 3D; remake as Style F).
- A-003 plane door, A-006 castle toilets, A-007 square windows: lines.txt, sources.md, timing.json, topic.md (voice not yet made).

## Slots (UTC). Already taken: A-004 12 Nov 22:00, A-002 13 Nov 22:00.
Standalone Shorts need ≥6 h from any other video: 12 Nov 16:00 (only if uploaded by 15:00), 13 Nov 04:00, 10:00, 16:00,
14 Nov 04:00, 10:00, 16:00, 22:00. A long video (max 1/day) + cut Shorts (≥3 h apart, within 24 h) may replace some of these;
keep every timing rule in CLAUDE.md. publishAt ≥1 h after upload. Nothing after 14 Nov 23:59 UTC. TikTok 30 min after each Short.

## Resume Style T / Kaggle later (do not lose)
STATUS.md NEXT list + render_log.md: datasets anam318/truewhys-ep-a005 and truewhys-ep-b003 are uploaded; once anam318 is phone-verified
re-push kernel_a005, kernel_b003, kernel_b003b (then kernel_b003c for the 10 B-003 Shorts) with tools/kaggle_px.py.
