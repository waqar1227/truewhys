# A-035 QA

## v1 final — 27 Nov 2026 — PASS
Style R, Kaggle GPU render (kernel truewhys-render-a035 v1, 2×T4, Cycles 64 spp + motion blur, 9 shots / 1044 frames, wall 89 min, render_log.md),
composed here (make.py render), 1080×1920, 30 fps, 34.8 s, −14.5 LUFS, true peak −2.5 dB. Gemini voice Puck, 3 scene takes (voice/ch0-2.flac), tempo 1.04,
scene-3 lines level-matched (+2…+3 dB, L04 −1.5 dB) after the listen check found a 4.5 dB drop at the take join.
Contact sheets checked: animatic (2 rounds of fixes) and 18 frames of the final MP4.
- [x] Script researched, 2+ sources per claim (sources.md: Scientific American, Guinness World Records record page + 2025 article, Science News, NASA, Burj Khalifa)
- [x] Animatic checked and fixed: hook title moved off Gus's face (over his sweater, out at 2.4 s), face turned toward camera in frame 1, block hands
      left/right corrected, block enlarged with its fold edge to camera, page-edge bands on the stacks, Moon shot opens on the Earth, corridor strip contrast,
      "holding the block" pose changed from two clasped hands (looked like praying) to one hand
- [x] Frame 1: Gus mid-push, strained face toward us, block squashing (paper crumple at 0.0 s) + "ONE MORE FOLD?" (3 words); last frame = frame 1 pose and framing (loop)
- [x] Line 2 raises stakes ("you'll get stuck at about seven"); open loop "so why can't you?" answered in the last 10 s, punchline in the last 3 s
- [x] New visual every ≤ 2.5–5 s (9 shots, each with its own motion: squash, macro push, doubling stack, rising column, tilt to the Moon, glowing bends, glide)
- [x] No burned-in captions (SRT to upload); in-picture English only short labels (7 FOLDS, 10 FOLDS = 10 cm, 23 FOLDS = 839 m, 42 FOLDS = 440,000 km, x4 PAPER, 2002, 12 FOLDS, 1.2 km)
- [x] Cast/arms check: Gus (MPFB, stylised, no real person) — both palms on the block (left hand world −X, correct for a person facing camera), no clipping
      or mirror flip seen; one-hand hold in desk_ask; minor: knit top shows some chest shading (accepted at phone size)
- [x] Voice: tools/voice_human_check.py **PASS** (pitch sd 4.07 st, range 13.4 st, no monotone run, pace cv 0.24, pause cv 0.54, mood contrast 1.38);
      listen check of the final mix: every word heard (whisper transcript of the MP4), moods change line by line, music under the voice, no synth cues
- [x] Real sound: real Freesound CC0 SFX (paper crumple/rustle, page flip, book close, table slap, chair creak, paper whoosh) + ambience beds
      (room quiet, city, night, school corridor) + real-instrument music "Mischief Maker" (Kevin MacLeod, CC BY 4.0, credit in the description); no WARNING lines
- [x] Variety check (last 3 uploads in calendar order: A-034 bell Sun 3 Jan Style F · L8-C1 candy/microwave Tue 5 Jan Style F · L9-C1 oxygen mask Thu 7 Jan
      Style T cabin): vs L9-C1 differs in style (R vs T), lead (new Gus vs Kai/Rosa), set (night study/city/space/corridor vs airliner cabin), camera
      (desk-height push-ins + upward match cuts), music mood (plucky curious vs travel), structure (test-experiment vs why-explainer), title shape
      (number claim, not "Why"), thumbnail layout → 8 of 8. Not 3 of one style in a row; not the same lead twice; "Why" titles in a row: 1.
- [x] Look: own look.md, palette checked vs the last 5 uploads, logged in docs/looks_register.md
- [x] Originality: own research, script, sets, cast, staging; no clips reused; no creator names in metadata
- [x] Ethics + religion check: clear
- [x] Thumbnail: final/thumb_v2.jpg (amazed look-up frame + "42 FOLDS TO THE MOON?", not the title word for word; readable at 94×168)
- [x] AI disclosure: YES — realistic CG paper macros, city skyline, Earth/Moon and corridor could be taken for real footage at a glance (docs/ai_disclosure.md, unsure → Yes); upload_meta.json + register
- [x] credits.md, sources.md, upload_meta.json (cat 28, publishAt 2027-01-08T18:00:00Z)
- [x] Schedule: Fri 8 Jan 2027 18:00 UTC (24 h after L9-C1 Thu 7 Jan 18:00, 23 h before L10 Sat 9 Jan 17:00)
