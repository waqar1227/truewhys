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

## Owner decision (27 Nov 2026)
All 4 voices approved. No fixed voice: each video's production design (topic.md) picks style, characters, voice,
music and sounds to fit its script. Voice per episode: `"voice": "Puck"` in direction.json (TW_GEMINI_VOICE overrides).

## Emotional voice (owner 27 Nov 2026: "real person, no robotic or AI ... mood, expressions, feelings, happy, sad")
1. **direction.json per line:** `{"voice": "Charon", "0": "chapter note", "split": "scenes", "lines": {"H1": "baffled, quick",
   "L01": "hushed suspense, then comic disappointment", "L05": "sad, slower"}}`. Short plain moods; say how pitch/pace/loudness change.
   Optional `"scenes": [["H1","L01"], ["L02","L03"]]` (else consecutive equal moods form a scene) and `"max_takes"` (default 3 per chapter).
2. **Voice:** `python lib/voice_gemini.py episodes/<ep> 0`. One request per scene (Short: 3; long video: ~3 per chapter, so plan the
   quota over 2-3 days). Each request is logged in research/gemini_tts_log.jsonl (commit it) and the script stops at 9 requests a day
   (TW_GEMINI_DAY_CAP), because all sessions share the free 10/day. Takes are FLAC masters in voice/ (named by a hash of the prompt:
   changing one scene's mood re-voices only that scene). Scene takes are loudness-matched and cut inside the pauses with 12 ms fades;
   the mix's ambience bed (lib/audio.py real mode) covers the gaps, so the joins are invisible.
3. **Never** put long [descriptions] in the transcript or quote script words in the notes (tested: read aloud / ad-libbed). Short audio
   tags typed into the line's `||say` text work: `[sigh]` (tested), probably [laughs], [whispering], [short pause].
4. **Check:** `python tools/voice_human_check.py episodes/<ep>` → PASS needed; it lists the weakest lines (flat, or same as their
   neighbour). Re-voice those scenes with a stronger mood (or another voice), then listen to the whole mix before upload.
   Calibration and test notes: docs/voice_samples/calibration.md.
5. **Demo for the owner:** `docs/voice_samples/flat_old_demo.mp3` (A-030 as posted: one flat take) vs `docs/voice_samples/emotional_demo.mp3`
   (same script and voice, 3 scene takes with a mood per line), both with the same real music, living-room ambience and real SFX
   (tools/emotional_demo.py, no Gemini request needed to rebuild).
