# Sound upgrade: real sound for every new video (27 Nov 2026)

Why: viewer comments "these AI sounds are ass" / "AI slop" (owner, 27 Nov). Rule: CLAUDE.md REAL SOUND RULE.

## What made the old mix sound synthetic (A-032 bubble wrap, measured 27 Nov)
- **Cartoon/synth cues everywhere.** Across all episode make.py files the most used cues are `pop` (214×), `ding` (101), `whoosh`,
  `shimmer` (62, synth), `bloop` (61, synth), `sting` (53, synth), `chime` (45, synth), `boing` (36), `hmm` (27), `swell`, `zap`.
  These are near-pure tones: in the spectrum 84–99 % of each effect's energy sits in ≤ 5 frequency bins (sting 73 %, shimmer 84 %,
  bloop 97 %, chime 99 %, Kenney pop/ding 96–97 %). Real foley is noise-like (bubble wrap 6 %, plastic crinkle 6 %). The ear reads
  pure-tone "blips" on every cut as cheap/AI.
- **Too many cues.** A-032 had 37 cues in 31 s (more than one per second), many decorative (sparkle, ding, hmm, boing, confuse).
- **No room.** No ambience bed: between lines only synthetic music was left (gap spectral flatness 0.002 = pure tones; quietest
  gaps -33 dBFS of synth pads). Nothing sounded like a real place.
- **Procedural music**: the same code-generated timbres in every video, and 3 mood changes inside one 31 s Short.
- Music ducking was -14…-22 dB; fine, kept similar (-20 dB under the voice now).

## What changed
- `library/sfx/real/` 167 real recordings (Freesound CC0) incl. 33 ambience beds; `library/music/real/` 27 real-instrument tracks
  (Kevin MacLeod, CC BY 4.0). Index: library/index.md "Audio — REAL SOUND".
- `lib/audio.py` "real" mode (default for new episodes): real SFX first (old names mapped, e.g. pop→pop_mouth, whoosh→whoosh_stick,
  thud→wood_thud), repeated effects get a small natural pitch/gain variation, cartoon cues dropped, a real ambience bed under every scene
  (~24 dB under the voice), one real music track per Short (~20 dB under the voice, -9 dB in pauses), CC BY credits written to
  `episodes/<ep>/audio/music_credits.txt` (lib/youtube.py refuses an upload whose description lacks them). Synth/procedural only as a
  printed WARNING fallback. Uploaded episodes rebuild in "legacy" mode exactly as before (`TW_SOUND=legacy|real` overrides).
- `lib/flat2d.py`: `Video(..., amb=..., sound=...)`, `shot(..., amb=...)`.
- `lib/voice_gemini.py`: new natural conversational direction for all new narration (talk to one friend, natural pauses, varied pace,
  no announcer tone); per-episode notes from direction.json are added to it.

## How to sound-design a new video (checklist)
1. Pick one ambience per location: `Video(EP, music="curious", amb="amb_living_room")`, change with `shot(..., amb="amb_street")`.
2. 1 cue per shot at most, only for something we SEE happen (a door, a pop, a drop, paper). No cue on every cut. No decorative stings.
3. Cue names: library/sfx/real/credits.md. If a needed sound is missing: add it to tools/fetch_real_sfx.py WANT and run it.
4. Music: one track per Short (mood or exact `"mood/track"`); long videos may change mood per chapter.
5. Read the mix log: no `WARNING (real sound)` lines in a final mix; copy audio/music_credits.txt into the description.

## Samples for the owner (docs/voice_samples/)
- `1_gemini_achird.mp3`, `2_gemini_charon.mp3`, `3_gemini_puck.mp3`, `4_kokoro_am_michael.mp3`: the same ~22 s text, natural direction,
  with real music (light), living-room ambience and real SFX. Raw takes kept in docs/voice_samples/takes/ (never re-spend quota).
- `demo_old_sound.mp4` vs `demo_new_sound.mp4`: A-032's first 21 s, old mix vs new mix (same picture and voice). MP4s are not in git
  (sent to the owner directly); rebuild: copy the episode, `voice_gemini.py <copy> 0`, `tempo_lines.py <copy> 1.04`, mix with TW_SOUND.
