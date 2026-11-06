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
