# Render log

| Date (UTC) | Episode | Job | Where | Resolution / samples | Frames | GPU min | Notes |
|---|---|---|---|---|---|---|---|
| 2026-11-06 | B-001 | stills (framing check) | session CPU | 480×270 / 12 | 103 | 0 | contact sheets |
| 2026-11-06 | B-001 | v1–v2 chapter 0 | Kaggle 2×T4 | 1920×1080 / 128 | 0 | ~2 | failed setup: dataset sub-folder skipped; OptiX denoiser weights missing → switched to OIDN |

## 6 Nov 2026: frame interpolation test (local, S003 640x360)
- Every frame rendered vs. every 2nd frame + motion-compensated interpolation (ffmpeg minterpolate mci/aobmc/bidir):
  SSIM 0.994, PSNR avg 46.1 dB, worst frame 42.5 dB → visually identical for slow camera moves.
- Rule (lib/render_bg.py `--interp`): only for smooth moves < 0.6 m/s, never for orbits or shake; static shots render 1 frame.
- Frames to render: long video 10,575 → 6,397; Shorts 8,398 → 4,876.

## 6 Nov 2026: Kaggle chapter 0 benchmark (kernel v3, 2×T4, 1920×1080, 128 samples, OIDN)
- Wall 176 min (~2.9 GPU-session hours). 13 shots, 1,122 frames.
- Seconds per frame: court 25–26, study 22, square 11.7, vineyard 8. Far too slow for the whole episode (~20 h).
- Plates look clean (no noise), but they use the old sets/shots → chapter 0 must be re-rendered anyway.
- Next: diagnostic kernel (truewhys-diag) to find the bottleneck (device, samples, denoiser, bounces).

## 6 Nov 2026: diagnostic (truewhys-diag, 1×T4, ~12 min)
- GPU is used (OptiX). Time is linear in samples: 128 spp ≈ 27 s, 64 spp ≈ 16 s per 1080p frame (court/study).
- Denoiser cost ≈ 0; fewer bounces ≈ no gain. 64 spp vs 128 spp: PSNR 52 dB (identical after OIDN). → 64 spp, adaptive threshold 0.03.

## 6 Nov 2026 16:49 UTC: B-001 final long-video plates started
- truewhys-render-b001 v4 (chapters 0–3, ~3,450 frames) and truewhys-render-b001b v1 (chapters 4–7, ~2,950 frames), each 2×T4.
- 1920×1080, 64 spp, OIDN, every 2nd frame + interpolation on slow moves. Expected ~6–7 h each.

## 6 Nov 2026 22:00 UTC: truewhys-render-b001b done (chapters 4–7)
- 36/36 plates, 0 errors. Wall 310.9 min (5.2 h session, 2×T4; 9.6 GPU-h of Blender time). 1920×1080 30 fps.
- QA: contact sheet + 1:1 crops (night street, court) clean, no noise. To check: dark blocks behind houses in land/night (S057/S061/S064/S066).
- Week so far: ~5.2 h session (b001b) + benchmark/diag; b001 (chapters 0–3) still running.
- 22:25 UTC: land/night city wall rebuilt (lighter stone, battlements, pointed roofs, lit windows, wall torches) after QA found
  black slabs; re-render S057/S061/S064/S066 pushed as truewhys-render-b001b v2 (~1,900 Blender-s, est. 20–25 min). Dataset now has sets2.py too.
- 22:29 UTC: b001b v2 done: 4 night plates, wall 23.0 min (0.4 h session, 2×T4). Checked: wall reads clearly. Plates replaced in renders/.

## 6 Nov 2026 23:31 UTC: truewhys-render-b001 done (chapters 0–3)
- 46/46 plates, 0 errors. Wall 400.9 min (6.7 h session, 2×T4). Contact sheet checked: clean, matches animatic.
- **B-001 long-video plates complete: 82/82.** Sessions this week ≈ 6.7 + 5.2 + 0.4 h + benchmark/diag (~1.5 h) ≈ 13.8 h of ~30 h.
- Next: Shorts plates (1080×1920, ~4,900 frames, est. ~7 h) after hook voice exists (7 Nov).

## 7 Nov 2026 03:05 UTC: B-002 final plates, part 1 started
- Dataset waqarahmed51/truewhys-ep-b002 (flat: render_bg, sets, sets2, camera, shots.json, job_C/job_D).
- truewhys-render-b002 v1: chapters 0–3 (~4,170 frames before step/interp savings), 2×T4, 64 spp, thr 0.03, step 2 + interp.
- Chapters 4–8 (job_D, ~5,170 frames) after the weekly GPU reset, to keep this week ≤ ~30 h (B-001 Shorts still to render, ~7 h).

## 7 Nov 2026: B-002 part 1 done; B-001 Shorts started
- 08:00 UTC truewhys-render-b002 v1 done: chapters 0–3, 35/35 plates, 0 errors, wall 243.2 min (4.1 h, 2×T4). Contact sheet clean.
- 08:40 UTC B-001 Shorts plates (1080×1920, 64 shots, 7,427 frames) split in two balanced jobs (~3,710 frames each):
  truewhys-render-b001 v5 (job_S) and truewhys-render-b001b v3 (job_S2). Week so far ≈ 13.8 + 4.1 h = 17.9 h before the Shorts.
- 12:55 UTC B-001 Shorts plates done: b001 v5 249.2 min + b001b v3 273.6 min (8.7 h, 2×T4 each), 64/64, 0 errors. Week ≈ 26.6 h.

## 9 Nov 2026 00:36 UTC: truewhys-render-b002b v1 started (B-002 chapters 4–8, job_D, 2×T4, est. ~5 h). New Kaggle week.
## 9 Nov 2026 09:05 UTC: B-002 Shorts plates: truewhys-render-b002s1 (C5–C8, 31 shots) + b002s2 (C1–C4, 39 shots), 1080×1920, 64 spp, 2×T4 each. Part 2 (b002b) finished overnight.
- 20:45 UTC B-002 Shorts plates done: b002s1 31/31 (~2.7 h), b002s2 39/39 (~3.9 h), 0 errors → ≈ 6.6 Kaggle h for the Shorts.
## 10 Nov 2026 14:20 UTC: truewhys-render-a001 v1 (A-001 quicksand Short, 12 plates, 1080×1920, 64 spp, step 2 + interp, 2×T4)
- 16:45 UTC done: 12/12, 0 errors, render wall 61.8 min on 2 GPUs (≈ 2.1 GPU h incl. setup).
## 10 Nov 2026 21:53 UTC: truewhys-render-a004 v1 (A-004 tickling Short, 15 plates, 1080×1920, 64 spp, step 2 + interp; robot-feather shots step 1, 2×T4)
- 11 Nov 00:17 UTC done: 15/15, 0 errors, render wall 143.2 min on 2 GPUs (≈ 4.9 GPU h incl. setup). Animated shots (step 1) cost ~2× per second, so keep animation to the shots that need it.

## 11 Nov 2026 11:10 UTC: truewhys-render-a002 v1 (A-002 polar bear liver Short, 15 plates, 1080×1920, 64 spp, step 2 + interp, no step-1 shots, 2×T4)
- 11 Nov 12:10 UTC done: 14/14 plates (+ 2D end card), 0 errors, render wall 55.6 min on 2 GPUs (≈ 2.0 GPU h incl. setup). No step-1 shots → half the A-004 time.
- dataset waqarahmed51/truewhys-ep-a002 (flat: render_bg, sets, sets2, sets3, camera, shots.json, job_A.json).

## 11 Nov 2026 15:32 UTC: truewhys-render-a005 v1 (A-005 brain freeze Short, 13 plates, 1080×1920, 64 spp, step 2 + interp, no step-1 shots, 2×T4)
- running; dataset waqarahmed51/truewhys-ep-a005.

## 12 Nov 2026: account switch to anam318 (owner; old waqarahmed51 token gone, its A-005 v1 output unreachable)
- Kaggle token is a proxy-injected network secret for api.kaggle.com; run the CLI via `tools/kaggle_px.py` (same args as `kaggle`).
- truewhys-render-a005 v1 (anam318): re-render of the 13 A-005 plates, 1080×1920, 64 spp, step 2 + interp; dataset anam318/truewhys-ep-a005. Running.
- truewhys-render-b003 v1 (ch 0–3) + truewhys-render-b003b v1 (ch 4–6): B-003 long plates, 1920×1080, 64 spp, step 2 + interp; dataset anam318/truewhys-ep-b003 (also holds shorts_shots.json + job_C.json). Running.
- Next: truewhys-render-b003c (job_C, 10 cut Shorts, 1080×1920) once a GPU slot frees.
- 12 Nov ~03:36 UTC: all 3 v1 runs (a005, b003, b003b) ERROR after ~30 s: no GPU (nvidia-smi not found) and no internet (Blender download failed).
  Cause: account anam318 is not phone-verified on Kaggle (needed for GPU + internet). 0 GPU h used. Re-push the same 3 kernels once verified.
- 12 Nov ~12:35 UTC: retried truewhys-render-a005 (v2): same ERROR (no GPU, no internet). anam318 still not phone-verified. 0 GPU h.
- 12 Nov ~17:25 UTC: owner phone-verified anam318 → GPU works. a005 v3 ran ~5 min then was DELETED (A-005 already published in Style F by the Fable sprint; plates not needed).
- 12 Nov ~17:35 UTC: truewhys-render-b003 v2 (ch 0–3) + truewhys-render-b003b v2 (ch 4–6) RUNNING on 2×T4 sessions (Kaggle limit: 2 GPU sessions at once). b003c (Shorts) waits for a free slot.
- 13 Nov 03:40 UTC: b003 v2 COMPLETE (202 min, 2×T4, 43 plates) + b003b v2 COMPLETE (143 min, 28 plates) → renders/plates (71/71 3d shots). ~11.5 GPU h.
- 13 Nov 03:41 UTC: truewhys-render-b003c v1 (10 cut Shorts, shorts_shots.json, 1080×1920) RUNNING.

## 16 Nov 2026 02:54 UTC: Style R test Shorts (owner A/B test B1/B2), first Style R runs with MPFB people
- truewhys-render-a016 v1 (A-016 onions, 16 shots, 1060 frames) + truewhys-render-a017 v1 (A-017 cloudy ice, 16 shots, 1194 frames):
  1080×1920, Cycles 128 spp adaptive + denoise, motion blur, JPEG q95, 2×T4 each (shots split by --part), deadline 10.5 h.
  Datasets anam318/truewhys-ep-a016 / -a017 (scene.py, shots.json, lib/style_r/sr_*.py, camera.py, mpfb.zip, job.json); kernel notebooks/kaggle_jobs/style_r/render.py
  (built by tools/kaggle_style_r.sh). Fix: tools/kaggle_px.py re-authenticates after its patch (kaggle 2.2.5 authenticates at import).
- 16 Nov ~03:00 UTC: a016 v1 ERROR after ~2 min (Kaggle auto-extracted mpfb.zip → "No such file"). Fix: upload as mpfb_zip.bin + folder fallback in render.py. a016 v2 pushed.
- 16 Nov 04:43 UTC: a017 v1 COMPLETE (96 min, 2×T4 ≈ 3.2 GPU h) but only the 6 shots without people rendered (same MPFB bug):
  cube_macro, no_room, xsec_start, xsec_trapped, scatter, lake_clear → renders/frames (kept locally; Kaggle keeps only the latest output).
- 16 Nov 05:15 UTC: a017 v2 pushed with the fixed kernel, job "shots" = the 10 missing shots.
- 16 Nov ~08:45 UTC: a016 v2 COMPLETE (302.5 min, 2×T4 ≈ 10.1 GPU h, all 16 shots) + a017 v2 COMPLETE (166.3 min, 2×T4 ≈ 5.5 GPU h, the 10 missing shots).
  All frames in renders/frames (A-016 1060, A-017 1194). Total Style R test this week ≈ 18.8 GPU h.
- 16 Nov ~10:35 UTC: a016 v3 pushed (job "shots" = hook_cut, loop_q after the QA fix: knife in front, title clear of face).
  11:02 UTC COMPLETE (22.7 min, 2×T4 ≈ 0.8 GPU h; hook_cut 54 + loop_q 80 frames). Total this week ≈ 19.6 GPU h.
- 20 Nov 17:01 UTC: a018 v1 pushed (A-018 wavy walls, Style R, 10 shots / 955 frames, 1080×1920, Cycles 64 spp + motion blur, 2×T4). Dataset anam318/truewhys-ep-a018, kernel truewhys-render-a018.
- 20 Nov 18:09 UTC: a018 v1 COMPLETE (2×T4, part0 54 min + part1 51 min ≈ 1.75 GPU h, all 10 shots, 955 frames) → episodes/A-018-wavy-walls/renders.
- 20 Nov 18:13 UTC: a018 v2 pushed (QA fixes: brighter studio, no black backdrop edges, coral brace arrows, hand rests on the wall; all 10 shots).
- 20 Nov 19:50 UTC: a018 v2 COMPLETE (2×T4, 82 + 71 min ≈ 2.55 GPU h, 955 frames). Week total Style R ≈ 23.9 GPU h.
- 22 Nov 02:04 UTC: a021 v1 pushed (A-021 GTA 6 PC, Style R, 9 shots / 1174 frames, 1080×1920, 64 spp + mblur, 2×T4).
- 22 Nov 04:02 UTC: a021 v1 COMPLETE (109.4 min wall, 2×T4 ≈ 3.65 GPU h, all 9 shots / 1174 frames) → episodes/A-021-gta6-pc/renders. QA FAIL (clothing clipping, barefoot, close-up) → not uploaded.
- 22 Nov ~04:4x UTC: a021 v2 pushed (QA fixes; shots pc_nothing, console_win, pedestals_a, pedestals_b, report_2027). Next: v3 hook_pc + loop_q (arms down, tighter camera).
- 22 Nov 04:4x UTC: a021b v1 COMPLETE (24.6 min wall, 2×T4 ≈ 0.8 GPU h; hook_pc 97 + loop_q 151 frames) → renders.
