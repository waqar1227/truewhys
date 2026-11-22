# AI / "altered or synthetic content" disclosure — TrueWhys (Production Manager decision, owner authority 18 Nov 2026)

Owner (18 Nov 2026): decide Yes or No **per video** from YouTube's official rules and the video's actual content; check all past videos and every
future one; never "Yes just because AI tools were used" and never "No just because it looks original". Re-check when YouTube changes the policy.

## YouTube's rule (official Help page "Disclosing use of GenAI content", support.google.com/youtube/answer/14328491, read 18 Nov 2026)
- **Disclose (Yes)** AI-made or altered content that **seems realistic**: makes a real person appear to say/do something they didn't;
  alters footage of a real event or place; generates a realistic scene that didn't happen; AI-created music that is the main focus.
- **No disclosure needed:** non-realistic content (animation; the page's own example is an AI animated missile "in a fully animated video"),
  minor/aesthetic edits, production assistance (script, outline, thumbnail, title, captions, idea generation), voice/audio repair, audio effects.
- Disclosing does not limit reach or monetisation; YouTube may add a label itself (its tools, C2PA metadata, detection) and penalise creators
  who consistently fail to disclose realistic AI content. The page is silent on a generic TTS narrator; ours imitates no real person and speaks
  over clearly animated pictures, so it is not "realistic content that could mislead".

## Decision test (apply to every video, record in its qa.md + upload_meta.json "ai_disclosure")
Answer **Yes** if ANY is true, else **No**:
1. Could a viewer mistake any shot for real camera footage of a real person, place or event (photoreal AI image/video, photoreal 3D people or places)?
2. Does a real, identifiable person appear to say or do something they didn't (including a cloned or sound-alike voice of a real person)?
3. Is real footage of a real event/place altered beyond minor aesthetic edits?
4. Is AI-generated music the main focus?
Our current styles: F (flat 2D cartoon), T (3D toon), R (stylised CG people on a plain studio backdrop) + Gemini TTS narrator "Charon" +
code-made music → **No**. A future photoreal Style R, AI-generated photoreal images/video, real footage edits or any voice clone → re-test, likely **Yes**.
Unsure → **Yes** (disclosing never hurts reach or money; a missing disclosure risks penalties).

## Register (all 43 channel videos, decided 18 Nov 2026; machine copy docs/ai_disclosure.json; applied on YouTube 17 Nov, proof docs/audit/ai_no.json)
| Video | Episode | Title | Style | Decision |
|---|---|---|---|---|
| MLRRsaV4iUA | A-001-quicksand | Why Quicksand Can't Actually Swallow You | T | **No** |
| o-dGmxKGKoY | A-002-polar-bear-liver | Why You Should Never Eat Polar Bear Liver | T | **No** |
| bE1TP9JlAzs | A-003-plane-door | Why a Plane Door Won't Open Mid-Flight | F | **No** |
| sdoOC7kAuRU | A-004-tickle | Why You Can't Tickle Yourself 🪶 | T | **No** |
| 8hsKNMLOhAw | A-005-brain-freeze | What Brain Freeze Does Inside Your Head | T | **No** |
| iW60L9Pap5k | A-006-castle-toilets | The Castle Toilet That Let an Army In | F | **No** |
| WHd_m81cbpE | A-007-square-windows | Why Plane Windows Are Never Square | F | **No** |
| zCkUEA4t5iQ | A-008-steel | The Accident That Invented Steel | F | **No** |
| 5XdQYTPzwxU | A-009-vending-machine | Why You Should Never Shake a Vending Machine | F | **No** |
| AshEYTYzMyI | A-010-wrinkly-fingers | Why Your Fingers Wrinkle but Your Face Doesn' | F | **No** |
| yyBUc7aM2lA | A-011-first-traffic-light | The Traffic Light That Exploded | F | **No** |
| 1r8faDAYoTQ | A-012-pen-cap-hole | Why Pen Caps Have a Tiny Hole | F | **No** |
| bHC7F6nNwWM | A-013-falling-cat | The Falling Cat That Broke Physics | F | **No** |
| pwVCqe756X8 | A-016-onion-tears | Why Onions Make You Cry | R | **No** |
| S8zIxiPXHpE | A-017-cloudy-ice | Why Ice Cubes Are Cloudy | R | **No** |
| jN10Y403ZOA | A-018-wavy-walls | Why Is This English Wall So Wiggly? | R | **No** |
| jIFcT7oUqlw | A-020-gta6-wait | Why We Waited 13 Years for GTA 6 | F | **No** |
| sx0H9Hm0KxA | A-021-gta6-pc | Why Can't You Play GTA 6 on PC Yet? | R | **No** |
| 9C-9O0c6VqM | B-001-animal-trials | Why Medieval Courts Put Animals on Trial | T | **No** |
| 5YqYpWmY7EA | B-001-animal-trials/C0 | Why a Pig Was Executed in a Man's Clothes | T | **No** |
| 33UzHb61eKc | B-001-animal-trials/C1 | Why a French Town Put a Pig on Trial | T | **No** |
| ypKUcSlisP0 | B-001-animal-trials/C3 | The Lawyer Who Defended Rats in Court | T | **No** |
| 23cFCmyvtKI | B-001-animal-trials/C4 | Why a Rooster Was Burned for Laying an Egg | T | **No** |
| sJ0HEbnwoj8 | B-001-animal-trials/C5 | Why a Court Offered Weevils Their Own Land | T | **No** |
| RI7u-NzEj5E | B-001-animal-trials/C6 | Why the Church Put Bugs on Trial | T | **No** |
| CPPa366kvr8 | B-001-animal-trials/C7 | Why the Hangman Got New Gloves | T | **No** |
| h2oO3SrSUH8 | B-002-worst-jobs | Would You Survive These 8 Jobs From Old Engla | T | **No** |
| TkNJsIdy7gs | B-002-worst-jobs/C1 | Why Everyone Hated the Man Paid to Taste Ale | T | **No** |
| 66iyJcnwvgY | B-002-worst-jobs/C2 | Why the King's Toilet Servant Was So Powerful | T | **No** |
| WqxkoJY4jy4 | B-002-worst-jobs/C3 | The Toad-Swallowing Job Behind the Word "Toad | T | **No** |
| qCgG6Dhqgi4 | B-002-worst-jobs/C4 | The Man Paid to Eat a Dead Man's Sins | T | **No** |
| Wu5-PLKwb48 | B-002-worst-jobs/C5 | Why the King's Men Could Dig Up Your Floor | T | **No** |
| kk6I9g5V82Y | B-002-worst-jobs/C6 | Why Workers Stomped on Cloth in Old Urine | T | **No** |
| 6wDhznnQeKI | B-002-worst-jobs/C7 | Why Towns Pushed Tanners Outside the Walls | T | **No** |
| FbtDoZL8vwk | B-002-worst-jobs/C8 | Why Gong Farmers Could Only Work at Night | T | **No** |
| Am8epkS94Hw | B-003-pirate-myths | 10 Pirate Myths You Still Believe (And What W | T | **No** |
| 4WCGHoL-cAM | B-003-pirate-myths/C1 | Pirates Never Actually Said "Arrr" #Shorts | T | **No** |
| e3VksvQ5-Gk | B-003-pirate-myths/C10 | The Two Pirates Who Escaped the Noose | T | **No** |
| 50PTfQtFLqo | B-003-pirate-myths/C2 | Why Pirates Didn't Really Have Parrots #Short | T | **No** |
| 9xDx3zIt27k | B-003-pirate-myths/C3 | The Real Reason Pirates Wore Eye Patches #Sho | T | **No** |
| nd7RqqpeDfE | B-003-pirate-myths/C4 | Pirates Almost Never Made Anyone Walk the Pla | T | **No** |
| iSMOk8JC7_Q | B-003-pirate-myths/C5 | Why Pirates Almost Never Buried Treasure #Sho | T | **No** |
| SVAKhIs2w0Y | B-003-pirate-myths/C6 | Why Pirates Really Flew the Skull and Crossbo | T | **No** |
| PQDcJuv570Y | B-003-pirate-myths/C7 | Why One Pirate Captain Gave His Crew a Bedtime | T | **No** |
| cLtK1MIprGs | B-003-pirate-myths/C8 | Why Pirates Got Paid for Losing an Arm | T | **No** |
| YL5gMoQVH7w | B-003-pirate-myths/C9 | How Pirate Crews Could Vote Out Their Captain | T | **No** |

## Second check, 19 Nov 2026 (owner: "double check ... I just not want any trouble")
- Re-read YouTube Help 14328491 + "How this content was made" 15447836: no 2026 change; disclosure is for content that **seems realistic**;
  "non-realistic content that's made with AI" needs none; non-photorealistic/animated AI content may only get a description label.
- Looked at a frame of every episode (one contact sheet): all flat 2D / 3D toon cartoons; A-016/A-017 are plainly computer-made people on a
  plain studio backdrop doing generic actions (no real person, place or event) → cannot be mistaken for real footage.
- Searched code and credits: no AI image/video generation anywhere, no photos or real footage, no voice clone or "sound like X" prompt
  (Gemini TTS "Charon" / Kokoro, generic narrator), music code-generated (lib/music.py), maps = Natural Earth outlines drawn as cartoons.
- Live check: 43/43 videos read from the API, none marked Yes by YouTube.
- **Result: all 43 stay No.** If YouTube ever auto-labels a video (its detection may notice synthetic narration), **leave YouTube's label as it is**:
  a label never limits reach or money, and accepting it avoids any dispute. Re-check this register whenever the Help page changes.

## Owner's ChatGPT advice, checked independently 19 Nov 2026
Same conclusion reached on our own evidence (above): cartoon/stylised videos with a generic TTS narrator → **No**; realistic fabricated footage
or a real person's voice → Yes. Its extra point is right and separate: YouTube's monetization rule on "inauthentic" (mass-produced/repetitive)
content (support.google.com/youtube/answer/1311392, renamed from "repetitious content" 15 Jul 2025). Added as a QA rule in CLAUDE.md + skill §9.
