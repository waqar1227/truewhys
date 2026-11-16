# QA — A-017 Why Ice Cubes Are Cloudy, Style R (MPFB person, Kaggle GPU) — owner A/B test B2 (16 Nov 2026)
Final: final/A-017.mp4 (not committed; rebuild `/opt/c3d/bin/python episodes/A-017-cloudy-ice/make.py render episodes/A-017-cloudy-ice/renders/frames`
after downloading frames from Kaggle kernel truewhys-render-a017 — note: v1 holds 6 prop shots, v2 the other 10), 1080×1920, 30 fps, 39.80 s, 27.9 MB.
- [x] Stills (2 rounds) + animatic (360×640, every 3rd frame) checked before the GPU render; final contact sheet (one frame per shot) checked 16 Nov.
- [x] Final frames: Kaggle 2×T4, Cycles 128 spp + denoise, motion blur (v1 + v2, ≈ 8.7 GPU h). No CPU frames in the final.
- [x] **Audit §6.3 numbers:** frame-1 character height **0.71** (Blender --measure; ≥ 0.45 ✔); first cut **2.9 s**; **16 shots** (longest 3.4 s);
      **end card 0 s** (corner Wy ✓ badge in the final 0.7 s); last shot matches frame 1 (same set + camera → loop).
- [x] Frame 1: title "WHY ICE CUBES / ARE CLOUDY" above her face, cloudy cube in her hand, tray + glass on the counter (hero prop + question).
- [x] Story: hook question → dissolved air → freezes outside-in (cross-section) → trapped bubbles scatter light → lake top-down → one-side trick → loop question.
- [x] Voice: Gemini TTS master voice/ch0.flac; whisper small transcript matches lines.txt word for word. −14.2 LUFS, true peak −2.7 dBTP.
- [x] Facts in sources.md (2+ each: Purdue MSE, Indiana Public Media, Cook's Illustrated, Science ABC, Hackaday). No medical/safety claims.
- [x] Ethics: nothing unethical; religion check clear; no AI field, no AI mention in public text. Stylised original person (no real people, no logos).
- [x] Metadata (audit §5/§6.6): title 24 chars, no "#Shorts", 20 tags, 3 hashtags topic first, subscribe line, category 28, playlist "Why Does That Happen?".
      Thumbnail: final/thumb.jpg (hook frame).
Result: PASS → YouTube 2026-11-23 16:00 UTC (after A-016 passes too; then A-012 → 24, A-011 → 25, A-013 → 26 Nov).
