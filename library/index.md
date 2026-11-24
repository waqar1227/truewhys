# TrueWhys reusable library

## Cast (lib/cast.py — vector cutout puppets: head/body/arms layers, 8 expressions, 4 mouth shapes, blinks)
- Wy (mascot/narrator), judge, lawyer, bishop, town crier, mother, farmer, monk, magistrate, villager0–7 (generated variety)
- Animals: pig (+ man's clothes outfit), rat, cat, rooster, weevil, basilisk (legend), dog, bull, horse, locust
- Props: gavel, scroll, quill, staff, torch, coin, egg, gloves, tithe sack, barley sheaf, church painting

## 3D sets (lib/sets.py — procedural Blender, Cycles)
- square (day / dusk / alpine): medieval town square, town hall with clock tower, half-timbered houses, stalls, well, scaffold
- court (town / church): stone courtroom with judge's bench, dock, pews, chandelier; church variant with stained glass, candles, cross
- land (barley / vineyard / night): patchwork countryside with village; alpine vineyard rows; night hill with city wall, torches, moon
- study: Wy's home set (round window, bookshelf, desk, globe, lamp, map board) — used in every episode

## Motion graphics (lib/gfx.py)
- chapter card, title card, Europe map with pins (Natural Earth), split screen, parchment documents (typewriter text, wax seal, torn/bitten edge), location tag, pop words, highlighted captions, end screen

## Audio
- Music: library/music/procedural/{mystery,curious,story,playful,tension,dark,warm}.wav (original, lib/music.py)
- SFX: library/sfx (CC0, mapping in lib/audio.py)

## Sets added for B-002 (lib/sets2.py)
| Set | Variants | Use |
|---|---|---|
| palace | day, night | Tudor chamber: oak panelling, tapestries, leaded window, fireplace, four-poster bed, close stool, chest |
| yard | tannery, fullers | Riverside workshop yard by the town wall: tanning pits + hide frames + pigeon loft / fulling tubs + tenter frames + cloth bolts |
| fair | day | Fairground: quack's wagon stage with striped awning and bottles, tents, stalls, bunting |
| backyard | night | Back lane: privy with half-moon door, cesspit hatch, cart with barrels, lanterns, moon |
| cottage | wake, tavern, stable | Cottage interior: hearth, table/bench; wake (covered body, bread + bowl, candles), tavern (counter, barrels, tankards), stable (hay, stalls, nest boxes, dug soil, shovel) |
Helpers: `flames()` toon fire, `candle()`, `panel_wall()`, `tapestry()`.

## Cast and props added for B-002 (lib/cast.py)
- Characters: king (generic Tudor king, not a likeness), groom, quack, toadboy, aleconner, saltpetre, gongfarmer, tanner, fuller, sineater.
- Hats: tudor_cap (flat cap + feather), brim_hat (1600s wide brim), leather_cap; work apron for non-robed characters.
- Props: toad, tankard, bucket, shovel, bread, bowl, bottle, cloth.

## Added 7 Nov 2026
- Sounds (CC0, BigSoundBank, trimmed): `shovel`, `frog`, `gulp`, `drink`, `splash` (lib/audio.py SFX; sources in library/sfx/bsb/credits.json). Extra raw: sheep, splash-big, frogs pond.
- Graphics: `map_frame(view=(lon, lat, span))` for any region (England views used in B-002); places London, Colchester, Hereford, Wales, Westminster.
- Doc cards: aleassize, toady, aubrey, order1627, surnames, colchester, coroner1326 (lib/gfx.py DOCS).
- Rank cards: `card` shots take `sub` ("NUMBER 8") for ranked-list episodes.
- land/night: readable city wall (battlements, pointed roofs, lit windows, torches).

## Added 10 Nov 2026 (A-004 tickling)
- Set `lab` (lib/sets3.py, variant day): bright cartoon neuroscience lab — bench with a tickle robot arm holding a big feather, brain model under glass,
  big brain screen (cerebellum highlighted) on the back wall, posters, shelves, window; yellow stool (3.0,0.95) seat z 0.77 for Wy to stand on.
  Camera marks in the sets3 docstring; A-004 plan.py has tested marks (HOOK, ROBOT, SCREEN, POINT, WIDE).
- Set animation hook: `sets.ANIMATORS[set](t, shot)` is called per frame by lib/render_bg.py when a shot has `"anim"`.
  Lab: `anim={"robot": "stroke", "amp": 14, "hz": 2.4, "t0": 0}` makes the robot wrist (`robo_wrist`) stroke the feather.
- Brain prop `sets3.brain(cx, cy, cz, s, hi_cereb=True)`: cartoon side-view brain (cerebrum, cerebellum, stem) for screens/posters/cutaways.
- Puppet motion (lib/compose.py): arms `"tickle"` (both hands on the tummy, fast wiggle); `laugh=True` or `laugh=<seconds>` (ha-ha mouth cycle, head bounce, shaking arms).
- Procedural music is not in git: rebuild with `python lib/music.py library/music/procedural` (seeded, identical every time).

## Added 11 Nov 2026 (A-002 polar bear liver)
- Set `arctic` (lib/sets3.py, variant night): 1590s Arctic camp — fire with tripod + pot at (0.6, 1.2), tent, sledge, crates, log seats,
  ship held in the ice at (4.5, 17), pressure ridges, icebergs, aurora + moon. Tested camera marks in episodes/A-002-polar-bear-liver/plan.py
  (HOOK two-shot by the fire, TIGHT sailor close, CAMP, WIDE ship + aurora, BEAR on the path to the ship with the ship behind, WYC).
- Magnifier scenes for any 3D shot (`lens=dict(name=..., labels=[[text, x, y, t_in]], at=[x, y], rad=0.34)`, lib/gfx.LENS_SCENES):
  `foodchain` (fish → seal → polar bear, yellow nutrient dots pile up, liver glows), `peel` (friendly cartoon hand, skin flakes drift off; no gore),
  `dose` (gauge with a needle swinging past a red "limit" + a small liver cube). Helper `gfx._svg_tile(body, R, bg)` draws any SVG lens scene.
- Cast in use: `sailor` (wool cap, 1590s) with `hold="liver"` (prop) and arms `"raise"` = liver at the mouth; animals `polar_bear`, `seal`, `fish`.
- Puppet option `posed=True` (lib/compose.py): arms start already in the target pose at frame 0 (use on hook shots so the key prop is in place instantly).

## Added 11 Nov 2026 (A-005 brain freeze)
- Magnifier scenes `headx_cold`, `headx_vessel`, `headx_nerve` (lib/gfx.LENS_SCENES): side cross-section of a cartoon head with brain, palate,
  an artery under the brain and the facial nerve; cold spreads on the palate / the artery swells with blood + pressure arrows / the nerve lights to the forehead.
  Reusable for any "inside your head/body" explainer (headaches, sinuses, hiccups).
- Cast expression `"pain"` (lib/cast.py): eyes squeezed shut (> <), brows pinched, gritted-teeth grimace. Study close mark STC in A-005 plan.py.

## Added 11 Nov 2026 (B-003 pirate myths)
- lib/sets5.py (imported by render_bg): set `deck` (day | sunset | night | red): 1710s pirate ship deck at sea, cannons, wheel on the
  quarterdeck, 3 masts with billowing sails + rigging, crow's nest, Jolly Roger (red variant = red flag), chest, barrels, cannonballs,
  coiled rope, THE PLANK over the starboard rail, horizon island + merchant ship. Set `islet` (day | dig | sunset): tiny palm island
  (dig = hole, half-buried chest with gold, shovel). Set `port` (day): Caribbean port market with 3D parrots in cages, fruit stall, harbour.
  Camera marks in the sets5 docstring and B-003 plan.py. Helpers: `palm()`, `sail_mesh()`, `far_ship()`, `_parrot3d()`, `_cage()`.
- Cast (lib/cast.py): captain (tricorn, red coat), pirate / pirate2 (eye patch) / pirate3 (bandanas), quartermaster, anne, mary
  (long hair + bandana / tricorn), merchant. New hair styles tricorn, tricorn_long, bandana, bandana_long; `patch=True` spec flag.
  Props: map (treasure map with X), coins (gold pile), flag (small Jolly Roger).
- Docs (lib/gfx.DOCS): film1950, book1883, kidd1699, roberts, injuries, trial1720.
- Sounds (lib/audio.py, CC0): waves, gulls (BigSoundBank sea waves + seagulls), bell (small bell), crowd_cheer (applause), creak, flag_flap, cannon (Kenney/OpenGameArt packs).
- Music mood `adventure` (lib/music.py): jaunty sea-shanty feel, original, code-generated.

## Style F (flat 2D, drawn in code, CPU only) — added 12–13 Nov 2026 (A-005, A-007, A-006, A-003)
All original (TrueWhys). One episode = `episodes/<ep>/make.py` (`sheet` | `big <t,t>` | `render`); needs `timing.json` + `audio/lines` from lib/voice_gemini.py.
- **Engine `lib/flat2d.py`:** cairo vector drawing (`G`: circle, rect, poly, path strings, limb, glow, rings, text with sticker outline), easing/pop/keyframes,
  path sampling (`path_at`, `path_part`), camera helpers (`roi`, `push`, `look_at`, parallax `g.layer`), `Video` (shots split by spoken words:
  `part=(0, "word")`, `"word#1"` = second match; SFX by word; music moods), word-by-word captions (Lilita One, yellow key words), hook title block,
  transitions (punch, flash, iris), Wy end card (`end_card`), contact sheets (`V.sheet`), parallel render + mix (`V.render`), `measure(mp4)` for qa.md.
- **Cast `lib/flat_cast.py`:** `Char(...)` chunky characters: 20 expressions (`EXPR`), arm poses (`ARM`, `amix`), held props, blinks, breathing, hats (headband,
  beanie, cap, pilot, hardhat, kettle helmet, crown, top hat, chef, goggles), hair styles, beard/moustache/glasses, outfit layers (apron, collar, coat, tie, belt,
  buttons, badge, stripes, tunic, armor, scarf). `WY` (full-body mascot) and `wy_bust` (exactly the logo drawing, blinks and talks).
- **Effects `lib/flat_fx.py`:** wall tiles, `room`, pendant `lamp`, snow/flakes, sparkles, bolts, pain marks, chunky `arrow`, steam, burst, `ring_wave`, `flame`,
  `no_sign`, pressure `gauge`, `qmark`.
- **Winter + Arctic `lib/flat_winter.py` (24 Nov 2026, A-026/A-027, TrueWhys original):** `winter_yard` (snowy school yard, brick wall, fence, falling snow),
  `metal_pole`, `tongue`, `beanie` + `scarf` (winter clothes over any cast v2.2 figure), `tundra_night` (stars, `aurora`, mountains, spruce),
  `tundra_summer` (midnight sun), `reindeer` (side view, walk/head/eye glow) + `reindeer_face` (front, glowing eyes), `torch` + `torch_beam`;
  helpers `mouth_pt`, `hand_pt`, `head_pt` give exact char2 mouth/hand positions. Cast v2.2 additions in lib/cast2.py: `friend`, `herder`.
- **`lib/write_shots.py <ep>`:** writes shots.json from a Style F make.py so `tools/make_srt.py` can build/upload the SRT.
- **Sets and props `lib/flat_sets.py`:** `parlour` (ice-cream shop), `lab` + `monitor`, `xray_bg`, head `cutaway` (brain, skull, artery, nerve, tongue; animatable
  state), `sky` + `cloud`, side-view `plane` (square or round windows), `fuselage_skin` + `big_window` + `crack`, `hangar` + water `tank_back/tank_front`,
  `stress_field` (flow lines round a square/rounded opening), `newspaper`, castle: `castle_wall` (garderobe box + chute, or gate with drawbridge), `garderobe_room`,
  `chute_section`, `castle_hill`, `tent`, `crowd`, `torch`, `moon`, `stone`, `merlons`; aviation: `cabin` + `seat`, `tube_section`, `plug_diagram`, `air_dots`;
  `elephant`. Props for hands: `cone`, `mug`, `cup_straw`.
- **Sounds `lib/sfxgen.py`:** in-house synthesised effects registered with lib/audio (use by name): siren, siren_yelp (generic emergency siren wail / yelp, A-019), freeze, zap, swell, rush, heartbeat, sting, melt, confuse,
  bloop, click, shimmer, chime.
- **Tools:** `tools/voice_check.py <ep>` (finds clipped or misheard narration lines before rendering), `tools/yt_finish.py <ep>` (retry thumbnail/playlist after an `tools/short_thumb.py` (Shorts thumbnail: clean frame + one hook/suspense line, owner rule 16 Nov), `tools/yt_ai_no.py` (sets the AI/altered field to No on every video).
  API quota error), `lib/voice_gemini.py` now cuts lines at the real pauses (it used to drop a line's first word when whisper swallowed it).

## Comedy sounds (added 13 Nov 2026, BigSoundBank CC0, credits in library/sfx/bsb/credits.json)
- laugh__* (5 real laughter clips: layer 2–3 for an audience laugh), honk__trumpet-horn-for-bike-* (cartoon honk; cut single honks), burp__*, boing__boing-cartoon-*,
  wings__* (bird wing flaps), skid__screeching-tires-4 (cartoon skid), scream__howling-of-a-boy, ducks__ducks. Example use: comedy/sample2/make_sample2.py (build_audio).
- Comedy cast (sample only, not final): comedy/sample2/toon.py — Benny (TrueWhys egg-head style, run/walk poses) and the Goose (run, flap, munch, phone).
- lib/cast2.py (owner-approved direction D3, 15 Nov 2026; v2.1 after owner feedback: fairer skin, head ~1/4, irises, ears, lips, fingers): cast v2 vector puppets (lids + brows,
  nose, neck, hands with thumb, no cheeks). `figure_svg(cid, expr, pose_l, pose_r)`, `png(svg, viewbox, scale)`; cast: wy, captain, doctor,
  worker, guard, noble, modern; expressions deadpan/smug/suspicious/shocked/bored/angry. Sample sheet: library/cast/cast_v2_sheet.jpg
  (`python lib/cast2.py <out>`). Original, code-drawn (TrueWhys). APPROVED by the owner 15 Nov (v2.1): use for all new videos.
  **v2.2 (22 Nov, owner: arms + turns):** smooth bent sleeves with a hand turned along the forearm; poses down, hold, hip, point, up, wave, shrug,
  explain, count, think, reach_r, reach_l (cast2.ARM); blends (a, b, u); `char2(..., view="3q")` 3/4 turn (auto for figures in the outer third
  facing the middle); automatic 0.25 s easing of pose changes; `cast2_flat.pose_at(t, keys)` for timed gestures; `turn_at(t, t0)` for a real
  right→front→left turn instead of a mirror flip. Pose sheet: library/cast/cast_v22_poses.jpg.
- **New standards in the composers (15 Nov 2026, audit §6.3, owner D2/D3):** `lib/cast2_flat.py` `char2(g, cid, x, y, h, expr, pose_l, pose_r, t=c.gt, flip)`
  draws cast v2.1 inside Style F (cached raster, auto blink + breathing; extra expressions blink/worried/curious). `flat2d.Video` has no end card by default
  (`endcard=False`; small Wy ✓ corner badge in the final 0.7 s, `badge=`); `V.qa_numbers("frame1.jpg")` prints frame-1 character height (must be ≥ 0.45),
  first cut, shot count, end-card seconds (0) for qa.md. `lib/shorts.py` (Style T cut Shorts): no end card unless shorts.json `"endcard": true`, corner badge
  in the last 0.7 s (compose.py), hook shot re-aimed so the subject fills 48 % of the height. Style T still uses the 3D cast v1: a 3D cast v2 is needed
  before new Style T videos (until then new videos are Style F).

## Added 19–20 Nov 2026 (B-004, A-018)
- `lib/flat_shapes.py` (Style F props): coin (ridged/smooth/clipped), coin_edge (ridged/trimmed/clad), scissors, candle, steam, manhole (circle/square/Reuleaux),
  road_sign (octagon/circle/diamond/square/rect, fade), paper_bag (envelope or flat-bottomed), bottle (cork/crown, fizz), bottle_cap (n teeth, counting highlight),
  cracker (holes, puff), razor_blade, ngon_pts, reuleaux_pts. Original (TrueWhys).
- `lib/flat2d.py`: 16:9 long videos with `TW_FLAT_SIZE=1920x1080` (set before import); `Video(cap_size=…)`.
- `lib/cast2.py`: 10 more cast v2.1 roles (clipper, newton, chaloner, engineer, sewer, knight, annan, painter, gillette, baker) + hats periwig, fedora, hardhat, chef, flatcap.
- `episodes/B-004-shape-secrets/shorts/make_short.py` `split_long(V)`: splits long Short shots into 1.5–2.5 s cuts with alternating framings, story clock and SFX kept.
- `lib/style_r/sr_walls.py` (Style R): wavy_wall (crinkle-crankle, running bond, per-brick colour), straight_wall (1–2 bricks, piers, topple pivot),
  paper_sheet (flat or zigzag), fruit_tree (espalier), sun_disc, arrow3d. `lib/srplate.py` plate(zoom=, t0=): punch-in cuts inside one rendered shot.
- **Style R vehicles + real mirror (A-019, `episodes/A-019-ambulance/scene.py`):** `ambulance(F, x, n)` generic box ambulance (mirrored 3D word, flashing red/blue
  lights via `flasher()`), `car(CF, n, mirror_to, eye)` hatchback whose rear-view mirror is aimed to reflect a point into an eye (ray-traced, reads correctly),
  `text3d()` 3D block lettering (Poppins ExtraBold; mirror/both-sides), `set_stage(road=True)` studio + road strip. Copy into lib/style_r when reused.
- lib/flat_annoy.py (B-005, 22 Nov 2026): Style F everyday-science props: toast (side/top, buttered), plate, table_side, ruler_v (height marker),
  sneaker + bow_knot (loosen / swing / twist=weak knot / undone), earbud(s) (neat → tangled), tumble_box (rotating clear box with string),
  spaghetti (bend, twist stripes) + fist, curtain (shower curtain with bulge/weights), mug, coffee_drop (drying ring or even stain), cereal_loop, bowl_top.
  `from flat_annoy import *` (TW_FLAT_SIZE set before import). Original, code-drawn (TrueWhys).
- lib/flat_brain.py (B-006, 24 Nov 2026): Style F psychology/brain props: brain mascot (happy, alarm, confused, smug, shout, sleepy, worried),
  doorway, thought cloud, vr_grid (wire-frame virtual room), phone (generic, lit screen/'0 NEW'), buzz (vibration marks), sound_wave, note (music),
  headphones (two-colour cups), gum (generic pack), book (+ empty slot), library_card, aglet_lace, pie chart, clock_face, mri, meg_helmet,
  pareidolia faces (socket, house_face, car_face, cloud_face, pizza_face), party_crowd. `from flat_brain import *`. Original, code-drawn (TrueWhys).
- lib/cast2.py new cast (B-006): `mira` (teal jumper, bun, phone) and `student` (yellow hoodie). lib/sfxgen.py new synth: `buzz` (phone on vibrate).
- lib/cast2.py additions (B-005, 22 Nov): "physicist" (lab coat, glasses) and "runner" (bun, coral sports top). Same v2.1/v2.2 rules.
- episodes/B-005-annoying-science/make.py sets reusable by copy: kitchen_am (morning kitchen), lab (physics lab wall), night_kitchen, bathroom + tub
  + bath_cut (side cut-away of a shower with vortex), cafe (top-view wooden table), breakfast (tablecloth), drop_cut (cross-section of a drying drop),
  milk_side (meniscus cross-section).
