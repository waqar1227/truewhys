# QA — A-016 Why Onions Make You Cry, Style R (MPFB person, Kaggle GPU) — owner A/B test B1 (16 Nov 2026)
Final: final/A-016.mp4 (not committed; rebuild `/opt/c3d/bin/python episodes/A-016-onion-tears/make.py render episodes/A-016-onion-tears/renders/frames`
after downloading frames from Kaggle kernel truewhys-render-a016 — note: v2 holds 14 shots, v3 the re-made hook_cut + loop_q), 1080×1920, 30 fps, 35.37 s, 32.8 MB.
- [x] Stills + animatic (360×640) checked before the GPU render; final contact sheets (whole video + first/last 2 s) checked 16 Nov.
- [x] First final (v2) FAILED QA: knife hidden behind the forearm in hook_cut, title over the face. Fixed in scene.py (hand/knife
      in front of the onion, camera lower and wider), low-sample stills re-checked, both shots re-rendered (v3). Fixed in the final.
- [x] Final frames: Kaggle 2×T4, Cycles 128 spp + denoise, motion blur (v2 + v3, ≈ 10.9 GPU h). No CPU frames in the final.
- [x] **Audit §6.3 numbers:** frame-1 character height **0.68** (Blender --measure; ≥ 0.45 ✔); first cut **1.8 s**; **16 shots** (longest 3.27 s);
      **end card 0 s** (corner Wy ✓ badge in the final 0.7 s); loop_q ends on hook_cut's camera (same set + framing → loop).
- [x] Frame 1: title "WHY ONIONS / MAKE YOU CRY" above his face, knife and onion clearly on the board (hero prop + question).
- [x] Story: hook → cutting breaks cells → enzyme makes a gas (syn-propanethial-S-oxide) → gas reaches the eye → nerves → tear glands
      flush it → 2002 Nature paper / tearless onion (Ig Nobel 2013) → defence → loop question.
- [x] Voice: Gemini TTS master in voice/; whisper (medium) transcript matches lines.txt. −14.2 LUFS, true peak −2.6 dBTP.
- [x] Facts in sources.md (8 sources: Library of Congress, Nature 2002, PubMed, Live Science, Scientific American, Japan Times, Improbable Research). No health advice.
- [x] Ethics: nothing unethical; religion check clear; no AI field, no AI mention in public text. Stylised original person (no real people, no logos).
- [x] Metadata: title 23 chars, no "#Shorts", 21 tags, 3 hashtags topic first, subscribe line, category 28, playlist "Why Does That Happen?".
      Thumbnail: final/thumb.jpg (hook frame).
Result: PASS → YouTube 2026-11-22 16:00 UTC (then A-017 → 23, A-012 → 24, A-011 → 25, A-013 → 26 Nov).
- [x] AI disclosure (docs/ai_disclosure.md test, 18 Nov): **No**: stylised CG people on a plain studio backdrop, generic TTS narrator, code-made music; nothing could pass as real footage.
