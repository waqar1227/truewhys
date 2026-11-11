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
