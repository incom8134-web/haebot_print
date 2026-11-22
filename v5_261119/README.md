# HaebotCase v5 — audited zip-tie + screw edition (261119)

Shell hangs on the RÅSKOG cart with zip ties / hot glue. Doors and vent panels hang on hooks and are held by 2 M4 screws each at the bottom. No aluminium.

**Where to start printing:** `stl_print_order/` (00 = tolerance coupon, then 01…36 bottom to top) and `docs/PRINT_ORDER.md`.

## What was wrong in v4 and is fixed

| # | Error in v4 | Fix in v5 |
|---|---|---|
| 1 | Tray M4 holes were at ±65/±85 mm; the real tray holes (measured in your STEP) are at **±67.6 / ±82.4**, Ø4.5, z=590. | Inserts, bores and shoulder holes moved; all 4 verified. |
| 2 | "15 mm above the cart top" was wrong: only 1 mm. | 6 mm (CAD distance). |
| 3 | Fenders needed ~6800 mm² supports, unclear hold. | Print cap-down, 40° flare: 83 mm² overhang. Tabs hang in plinth slots, tie/glue stops pull-out. |
| 4 | Tie tunnels only along the wall. | Every loop has 2 crossing tunnels (along wall + up/down). |
| 5 | You could see inside the shell down the top channel. | Charcoal ledge at each channel end. |
| 6 | "No supports" was untrue: joint tongues float 3.3 mm above the bed. | Documented: supports build-plate only, tiny. |
| 7 | White share 45 %. | Left skin white: 52 % white. |
| 8 | "ASA final" in table. | PETG. |
| 9 | Upper front door could not lift off its hooks (brow stopped it after 2 mm; hooks need 6). | Upper door and brow each 4 mm shorter: 10 mm lift room, tested for all 4 panels. |
| 10 | Your request: screws instead of magnets. | Hooks on top stay; **2 M4×12 screws at the bottom corners of every panel** (head sunk in the face) into M4 nut pockets printed in the posts. |

## Cart and wheel numbers (change at the top of `cad/v5.py`)

| Item | Value | Source |
|---|---|---|
| Cart L × B × H | 385 × 245 × 540 mm | you |
| Bottom U-tubes | 295 mm wide | you |
| Wheels | Ø120 mecanum, 50 mm wide | Ø from you, width ASSUMED |
| Cart bottom tube above floor | 60 mm | ASSUMED |
| Wheel centres | ±110 mm, long sides | ASSUMED |

## Measured clearances

| Between | Value |
|---|---|
| Shell inner wall ↔ cart | 22 mm front/rear, 32 mm sides |
| Plinth ↔ 295 mm base | ≥ 4 mm |
| Loop / hook / nut-pad blocks ↔ cart | 7.5–9 mm |
| Shoulder ↔ cart top | 6 mm |
| Fender ↔ wheel | 8 mm |
| Wheel ↔ plinth | 2 mm |

0 collisions between all parts, cart and wheels. All parts valid single solids.

## Fixing

| Part | Fixing |
|---|---|
| Posts, rear, left skin, brow, channel caps, plinth | Hidden loops with 2 tunnels (6.5 × 3 mm): along-the-wall tunnel for vertical tubes / through a mesh square, up/down tunnel for horizontal rims. Hot glue optional. |
| Upper ↔ lower halves | 10 mm interrupted tongue, 0.3 mm play. |
| Doors (front) and vent cassettes (right) | 2 hooks on top in blocks printed in the posts + 2 screws at the bottom corners. Open: remove screws, lift 6 mm, pull out. |
| Green shoulder | Splice plates with pins + 2 hanging loops per piece. |
| Fenders | Tabs through plinth slots; tie or glue. |
| Tray | 4 × M4×16 into inserts in the tray mount; mount zip-tied to the front rim. |
| Light bars | Push in, dot of glue. |

## Print settings (Bambu P1S, PETG)

0.4 nozzle, 0.2 layer, 3–4 walls, 15–20 % gyroid. Supports: Auto, build plate only (appear only under 3 mm joint tongues). Posts (215 mm tall): brim 10 mm, slow outer wall. About 4.6 kg, 256 printer-hours (±30 %).

## Hardware

- Zip ties 4.8 × 200 mm: 52 (buy 100)
- M4 × 12 button-head screws 8 + M4 nuts 8 (panels)
- M4 heat-set inserts 4 + M4 × 16 button-head screws 4 (tray)
- Hot glue

## Assembly order

1. Print the coupon first; adjust `CLR` if the 0.30 row is too tight/loose.
2. Wheels/motors/electronics on the cart.
3. Plinth pieces over the axles, tie.
4. Fender tabs into plinth slots, tie or glue.
5. Lower posts, rear, left skin onto the plinth tongue, tie to the cart.
6. Upper parts onto the 10 mm tongue, tie.
7. Brow (light bars first), channel caps, tie.
8. Press an M4 nut into each nut pocket in the posts (dab of glue).
9. Green shoulder: splice plates, tie to the top basket.
10. Tray mount tied to the front rim; tray screwed through the front skirt.
11. Hang doors and vents on hooks, fit 2 screws per panel.

## Part table

| File | Qty | Colour | Print X × Y × Z (mm) | Orientation | g each | h each |
|---|---|---|---|---|---|---|
| door_lo | 1 | warm white | 175 × 202 × 13 | outer face down on textured PEI | 143 | 7.9 |
| door_up | 1 | warm white | 175 × 163 × 13 | outer face down on textured PEI | 115 | 6.4 |
| vent_lo | 1 | charcoal | 202 × 176 × 13 | outer face down | 107 | 5.9 |
| vent_up | 1 | charcoal | 202 × 176 × 13 | outer face down | 107 | 5.9 |
| post_FL_lo | 1 | warm white | 92 × 128 × 215 | print upright as assembled; gussets under blocks, no supports | 166 | 9.2 |
| post_FL_up | 1 | warm white | 92 × 128 × 213 | print upright as assembled; gussets under blocks, no supports | 173 | 9.6 |
| post_BL_lo | 1 | warm white | 68 × 128 × 215 | print upright as assembled; gussets under blocks, no supports | 144 | 8.0 |
| post_BL_up | 1 | warm white | 68 × 128 × 213 | print upright as assembled; gussets under blocks, no supports | 150 | 8.4 |
| post_FR_lo | 1 | warm white | 92 × 152 × 215 | print upright as assembled; gussets under blocks, no supports | 191 | 10.6 |
| post_FR_up | 1 | warm white | 92 × 152 × 213 | print upright as assembled; gussets under blocks, no supports | 198 | 11.0 |
| post_BR_lo | 1 | warm white | 68 × 152 × 215 | print upright as assembled; gussets under blocks, no supports | 169 | 9.4 |
| post_BR_up | 1 | warm white | 68 × 152 × 213 | print upright as assembled; gussets under blocks, no supports | 176 | 9.8 |
| rear_lo | 1 | warm white | 175 × 215 × 16 | outer face down | 159 | 8.8 |
| rear_up | 1 | warm white | 175 × 213 × 16 | outer face down | 165 | 9.2 |
| side_L_lo | 1 | warm white | 215 × 176 × 16 | outer face down | 142 | 7.9 |
| lightbar_side | 4 | green | 90 × 16 × 5 | push in from inside, dot of hot glue on flange | 6 | 0.3 |
| side_L_up | 1 | warm white | 213 × 176 × 16 | outer face down | 143 | 8.0 |
| channel_cap_L | 1 | charcoal | 28 × 130 × 29 | outer face down | 27 | 1.5 |
| channel_cap_R | 1 | charcoal | 28 × 130 × 29 | outer face down | 27 | 1.5 |
| brow | 1 | smoked black | 175 × 39 × 16 | front face down; smoked/black PETG | 28 | 1.6 |
| lightbar_brow | 2 | green | 38 × 10 × 5 | push in from inside, dot of hot glue | 1 | 0.1 |
| shoulder_FL | 1 | green | 156 × 152 × 55 | top face down, skirts up | 146 | 8.1 |
| shoulder_BL | 1 | green | 156 × 152 × 55 | top face down, skirts up | 146 | 8.1 |
| shoulder_FR | 1 | green | 156 × 152 × 55 | top face down, skirts up | 146 | 8.1 |
| shoulder_BR | 1 | green | 156 × 152 × 55 | top face down, skirts up | 146 | 8.1 |
| splice_shoulder | 2 | charcoal | 30 × 105 × 6 | pins up; dot of glue in each pin hole | 13 | 0.7 |
| plinth_FL | 1 | charcoal | 156 × 216 × 118 | print upright, chamfered edge on bed | 176 | 9.8 |
| plinth_BL | 1 | charcoal | 156 × 216 × 118 | print upright, chamfered edge on bed | 178 | 9.9 |
| plinth_FR | 1 | charcoal | 156 × 216 × 118 | print upright, chamfered edge on bed | 176 | 9.8 |
| plinth_BR | 1 | charcoal | 156 × 216 × 118 | print upright, chamfered edge on bed | 178 | 9.9 |
| fender_FL | 1 | medium grey | 100 × 156 × 81 | PRINT cap-down (axis vertical); flare 40 deg from vertical, no supports | 131 | 7.3 |
| fender_BL | 1 | medium grey | 100 × 156 × 81 | PRINT cap-down (axis vertical); flare 40 deg from vertical, no supports | 131 | 7.3 |
| fender_FR | 1 | medium grey | 100 × 156 × 81 | PRINT cap-down (axis vertical); flare 40 deg from vertical, no supports | 131 | 7.3 |
| fender_BR | 1 | medium grey | 100 × 156 × 81 | PRINT cap-down (axis vertical); flare 40 deg from vertical, no supports | 131 | 7.3 |
| tray_mount | 1 | charcoal | 177 × 42 × 21 | plate face down | 105 | 5.9 |
| tray | 1 | medium grey | 146 × 240 × 33 | original v1 tray geometry, moved +2.5 mm X / +45 mm Z | 102 | 5.6 |

## Still to check on the real cart
- 3 assumed numbers above; motor bracket size (plinth axle slots are 30 mm); real tube/wire positions for the loops.
