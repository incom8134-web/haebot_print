# HaebotCase v5 — audited zip-tie edition (261119)

v5 = v4 after a full re-check. Real errors were found and fixed (list below). Shell hangs on the RÅSKOG cart with zip ties / hot glue, magnets and hooks. No aluminium, no screws in the body (only 4 M4 in the tray).

## What was wrong in v4 and is fixed

| # | Error in v4 | Fix in v5 |
|---|---|---|
| 1 | Tray M4 holes (shoulder + insert mount) were at ±65/±85 mm; the real tray holes (measured in your STEP) are at **±67.6 / ±82.4**, Ø4.5, z=590. Screws would not have lined up (2.4–2.6 mm off). | Mount inserts, relief bores and shoulder holes moved to the measured positions (verified, all 4 axes match). |
| 2 | I wrote "15 mm above the cart top". Real: shoulder fins/loops were only **1 mm** above. | 6–7 mm clearance (measured by CAD distance). |
| 3 | Fenders needed ~6800 mm² of tree supports and had no clear hold. | Print cap-down with a 40° flare: **83 mm² overhang** (no supports). Hood bore r68 (8 mm to the wheel), tabs hang in plinth slots (gravity) + tie/glue stops pull-out. |
| 4 | Tie tunnels only ran along the wall; they cannot wrap a horizontal basket rim. | Every wall loop now has 2 crossing tunnels (along the wall + up/down), standoff 13 mm. Tray-mount arms too. |
| 5 | Looking down the top channel you saw the inside of the shell next to the cart. | Charcoal ledge at each channel end (6 mm clear of the cart). |
| 6 | "No supports" was not true: the joint tongues float 3.3 mm above the bed on the outer-face-down panels. | Documented: supports = build-plate only, they appear only under the tongues (3 mm tall). |
| 7 | White share 45 % (target 60 %). | Left skin now white: 52.4 % white, 22.8 % charcoal, 11.0 % green, 13.1 % grey. |
| 8 | Material column said "ASA final". | PETG everywhere. |

## Cart and wheel numbers used (change at the top of `cad/v5.py`)

| Item | Value | Source |
|---|---|---|
| Cart L × B × H | 385 × 245 × 540 mm | you measured |
| Bottom U-tubes | 295 mm wide | you |
| Wheels | Ø120 mecanum, 50 mm wide | Ø from you, width ASSUMED |
| Cart bottom tube above floor | 60 mm | ASSUMED |
| Wheel centres | ±110 mm from middle, long sides | ASSUMED |

## Measured clearances (CAD distance, not estimates)

| Between | Value |
|---|---|
| Shell inner wall ↔ cart | 22 mm front/rear, 32 mm left/right |
| Plinth ↔ 295 mm base | ≥ 4 mm |
| Tie-loop blocks / hook blocks ↔ cart | 7.5–9 mm (they are the contact points) |
| Shoulder (fins, loops) ↔ cart top | 6 mm |
| Fender ↔ wheel | 8 mm |
| Wheel ↔ plinth | 2 mm |
| Tray mount arm tip ↔ cart front | 0.7 mm (tie pulls it in) |

Collision check, all part pairs + cart + wheels: **0 collisions**. All parts are valid single solids.

## Fixing

| Part | Fixing |
|---|---|
| Posts, rear, left skins, brow, channel caps, plinth | Hidden loops with 2 tunnels (6.5 × 3 mm). Pick the tunnel that suits the wire/tube: along-the-wall tunnel for vertical tubes or through a mesh square, up/down tunnel for horizontal rims. Hot glue optional. |
| Upper ↔ lower halves | 10 mm interrupted tongue, 0.3 mm play, drops in. |
| Doors / vent cassettes | 2 hooks into blocks printed in the posts + 2 magnets 10×3 at the bottom. |
| Green shoulder (4) | Splice plates with pins + 2 hanging loops each (+-shaped hole). |
| Fenders | Tabs through plinth slots; tie through tab hole to a cart wire, or dot of glue. |
| Tray | 4 × M4×16 from inside the tray into inserts in the tray mount; mount zip-tied to the front basket rim (2 arms, 2 tunnels each). |
| Light bars | Push in from inside, dot of glue. |

## Print settings (Bambu P1S, PETG)

- 0.4 nozzle, 0.2 layer, 3–4 walls, 15–20 % gyroid, textured PEI.
- Supports: Auto, **build plate only**. They appear only under the 3 mm joint tongues. No supports for fenders/posts.
- Posts (215 mm tall, thin): brim 10 mm, slow outer wall, no fan above 60 % early layers.
- Parts are oriented in `stl/`; per-colour plates in `3mf/`.
- 36 part files, 41 pieces, largest 240 mm (fits 245). About 4.6 kg and 256 printer-hours (estimate ±30 %).

## Hardware

- Zip ties 4.8 × 200 mm: 52 (buy 100)
- Magnets 10 × 3 mm: 16 (check polarity: pairs must attract)
- M4 heat-set insert 4 + M4 × 16 button head 4 (tray only)
- Hot glue (or CA gel for fenders)

## Assembly order

1. Print `coupon/tolerance_coupon.stl`; adjust `CLR` if the 0.30 row is too tight/loose.
2. Wheels/motors/electronics on the cart.
3. Plinth pieces down over the axles, tie.
4. Fender tabs into plinth slots, tie or glue.
5. Lower posts, rear, left skin onto the plinth tongue, tie to cart.
6. Upper parts onto the 10 mm tongue, tie.
7. Brow (light bars first), channel caps, tie.
8. Glue magnets (check polarity first).
9. Green shoulder: splice plates, then tie to the top basket.
10. Tray mount: tie to front rim; screw tray through the front skirt (4 × M4).
11. Hang doors and vents on hooks; magnets close them.

## Part table

| File | Qty | Colour | Print X × Y × Z (mm) | Orientation | g each | h each |
|---|---|---|---|---|---|---|
| door_lo | 1 | warm white | 175 × 202 × 13 | outer face down on textured PEI | 143 | 7.9 |
| door_up | 1 | warm white | 175 × 167 × 13 | outer face down on textured PEI | 118 | 6.6 |
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
| brow | 1 | smoked black | 175 × 43 × 16 | front face down; smoked/black PETG | 30 | 1.7 |
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
- 3 assumed numbers above (bottom height, wheel centres, wheel width).
- Motor bracket size: plinth axle slots are 30 mm wide.
- Real wire/tube positions: loops are generic; tell me where the vertical tubes are and I will place loops exactly.
