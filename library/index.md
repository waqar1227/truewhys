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
