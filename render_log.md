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
