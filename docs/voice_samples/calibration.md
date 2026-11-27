# voice_human_check calibration (27 Nov 2026)

Tool: `tools/voice_human_check.py` (plain signal analysis, no AI). Thresholds are in its `T` table, chosen from the numbers below.

## What was measured
- **Flat / robotic references (all must FAIL):** espeak-ng (normal + `range="x-low"`), Kokoro am_michael on 4 of our scripts + the owner
  sample, and "robot" copies of our own Gemini takes (same words, pauses and loudness, pitch replaced by one steady note via LPC
  resynthesis). 23 files: **23 FAIL**.
- **Our Gemini voices (docs/voice_samples/takes):** Achird, Charon, Puck: **PASS**.
- **All 48 episode masters (voice/*.flac + timing.json):** 41 PASS, **7 FAIL**: A-006, A-019, A-024, A-027, A-028, A-030, A-031.
  The failures are mostly the latest Shorts (A-019...A-031), the period of the "AI sounds" viewer comments. They fail on **mood contrast**
  (every line read with the same pitch, pace and loudness) and A-030 also on pace (rate CV 0.043: a steady metronome read).

| metric | robot / espeak | Kokoro | Gemini masters | FAIL / WARN below (or above) |
|---|---|---|---|---|
| pitch range p5–p95 (semitones) | 1.2–1.9 / ~6 | 10.6–11.8 | 11.4–16.2 | < 8 / < 12 |
| pitch std (st) | 1.0–2.1 | ~3.5 | 3.5–5.1 | < 2.6 / < 3.6 |
| longest monotone run (s) | 2.4–7.5 | 0 | 0 | > 3.0 / > 1.5 |
| pause-length CV | espeak 0.07–0.20 | 0.18–0.33 | 0.25–0.63 | < 0.15 / < 0.25 |
| pace CV across phrases | 0.06–0.18 | 0.10–0.16 | 0.04–0.31 | < 0.05 / < 0.08 |
| phrase loudness spread (dB) | 0.4–0.6 | 0.55–1.1 | 0.45–3.0 | < 0.4 / < 0.7 |
| **mood contrast** between lines | 0.4–0.8 | 0.5–0.97 | 0.5 (A-030/31) … 2.0 | < 1.0 / < 1.3 |
| pauses per minute (> 8 s speech) | espeak ~0 | | 15–30 | < 4 = FAIL |

Mood contrast = mean of (line pitch SD / 0.9 st, line pace CV / 0.09, line loudness SD / 1.5 dB, SD of line pitch ranges / 2 st).
Loose files (no lines.txt) use phrases between pauses ≥ 0.3 s as lines. Artefacts: clipping > 0.05 % = FAIL; clicks; at the joins of
scene takes, loudness jump > 4 dB, noise-floor jump > 10 dB or pitch jump > 7 st = WARN.

**A number is not an ear.** PASS means "nothing measurably flat"; the QA gate still needs a listen-check of the final mix.

## Gemini direction tests (27 Nov, 5 requests, logged in research/gemini_tts_log.jsonl)
1. **Long [mood descriptions] inside the transcript: READ ALOUD** (63 s take, the directions spoken). Never do this.
2. **Moods listed line by line in the notes, quoting each line's first words: the model ad-libbed** a 68 s preamble (it read the profile,
   performed the moods on invented text, even said "wired in parallel"), then read the real transcript flatly. The splitter kept only
   the real lines; voice_human_check: contrast 0.70, FAIL. One-take-per-chapter with per-line moods is therefore NOT the default for
   emotional work; scenes are.
3. **Scenes (3 requests, 2 lines each), one plain mood arc per request, no quotes: clean takes, exact words, PASS** (contrast 0.53 → 1.20,
   pace CV 0.043 → 0.121, pause CV 0.32 → 0.54, loudness spread 0.51 → 1.21 dB vs the old A-030 take).
4. **Short audio tag `[sigh]` typed inside a line: works** (not spoken; a 1.3 s pause with a soft exhale). Keep tags short and known
   ([sigh], [laughs], [whispering], [short pause]); test a new tag once before relying on it.
Rule of thumb: whisper checks every take; `CHECK take ...: words heard that are not in the script` means a direction was spoken.
