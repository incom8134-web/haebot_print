# HaebotCase v2 — zip-tie edition (261119)

The shell hangs on your IKEA RÅSKOG cart. **No aluminium, no screws in the body.** Everything is held by hidden zip-tie loops (or hot glue), printed hooks and magnets.

## Cart and wheel numbers used (change in `cad/v4.py`, top of file)

| Item | Value | Source |
|---|---|---|
| Cart L × B × H | 385 × 245 × 540 mm | you measured |
| Bottom U-tubes | 295 mm wide | you (5 cm more than breadth) |
| Wheels | Ø120 mecanum, 50 mm wide | Ø from you, width ASSUMED |
| Cart bottom tube height | 60 mm above floor (axle height) | ASSUMED |
| Wheel centres | ±110 mm from the middle, on the long sides | ASSUMED |

Wiggle room to the cart: ~22 mm front/rear, ~32 mm left/right, 6 mm at the 295 mm base, 15 mm above the top.

## Outside size
315 × 435 mm, plinth bottom 40 mm, top of green shoulder 615 mm. Front = short end (door, smoked brow + camera, tray). Right long side = vent cassette. Left long side = charcoal skin + 4 green light windows.

## How every part is fixed

| Part | Fixing | Tools |
|---|---|---|
| Corner posts, rear panels, left skins, brow, channel caps, plinth | 1–3 hidden zip-tie loops each (6.5 × 3 mm tunnel). Tie around the nearest cart tube or basket rim. Hot glue optional. | zip ties |
| Upper ↔ lower half | 10 mm interrupted tongue on the lower parts, 0.3 mm play, drops straight down. | none |
| Doors (front) and vent cassettes (right) | 2 hooks at the top into hook blocks **printed into the corner posts**; 2 magnets (10 × 3 mm) at the bottom. Pull bottom, tilt, lift off. | none |
| Green shoulder (4 pieces) | Splice plate with pins at the centre seam, 2 hanging zip-tie loops per piece to the top basket. | zip ties |
| Fenders (Ø120 mecanum) | 2 tabs through slots in the plinth, zip tie through each tab inside. | zip ties |
| Tray | Same tray as v1, 4 × M4 from inside the tray into the tray mount; the mount is zip-tied to the top basket rim. | hex key (inside tray only) |
| Green light bars | Push in from inside; dot of hot glue on the flange. | glue gun |

## Checks

- 36 part files, 41 pieces. **All fit 245 mm** for the P1S (largest 240 mm). Each part is one solid.
- Collision check against the cart and wheels (reference bodies) and between all parts: **0 collisions**.
- No visible screws. No supports on cosmetic faces. The posts print upright with 45° gussets under every hook, magnet and loop block. Tree supports only inside the fender hoods.
- Colour (visible area): white 45.0 %, charcoal 29.5 %, green 11.4 %, grey 13.3 %.
- Filament ≈ 4.5 kg PETG, ≈ 248 printer-hours (estimate ±30 %). Single colour per part, no AMS needed.

## Hardware

- Zip ties 4.8 × 200 mm: 52 (buy 100)
- Disc magnets 10 × 3 mm: 16 (check polarity: door and post pairs must attract)
- M4 heat-set inserts: 4 + M4 × 16 button head × 4 (tray only)
- Hot glue

## Assembly order

1. Print `coupon/tolerance_coupon.stl` first; adjust `CLR` in `cad/v4.py` if the 0.30 row is too tight or loose.
2. Mount wheels/motors and electronics on the cart.
3. Slide the 4 plinth pieces down over the axles (open-bottom slots); zip-tie them through their loops.
4. Push the fender tabs through the plinth slots and zip-tie them inside.
5. Lower corner posts, lower rear panel, lower left skin: place on the plinth tongue, zip-tie to the cart.
6. Upper posts, upper rear, upper left skin: drop onto the 10 mm tongue, zip-tie.
7. Brow (push the green light bars in first), channel caps, zip-tie.
8. Glue the 16 magnets (8 in posts, 8 in doors/vents). Check polarity first.
9. Green shoulder: splice plates with pins, then zip-tie each piece to the top basket.
10. Tray mount: zip-tie to the top basket rim; bolt the tray through the front green skirt (4 × M4).
11. Hang the doors and vent cassettes on their hooks and swing them shut (magnets hold them).

## Part table

| File | Qty | Colour | X × Y × Z print (mm) | Orientation | g each (est.) | h each (est.) |
|---|---|---|---|---|---|---|
| door_lo | 1 | warm white | 175.0 × 202.0 × 13.0 | outer face down on textured PEI | 143 | 7.9 |
| door_up | 1 | warm white | 175.0 × 167.0 × 13.0 | outer face down on textured PEI | 118 | 6.6 |
| vent_lo | 1 | charcoal | 202.0 × 176.0 × 13.0 | outer face down | 107 | 5.9 |
| vent_up | 1 | charcoal | 202.0 × 176.0 × 13.0 | outer face down | 107 | 5.9 |
| post_FL_lo | 1 | warm white | 92.0 × 127.5 × 215.0 | print upright as assembled; gussets under blocks, no supports | 164 | 9.1 |
| post_FL_up | 1 | warm white | 92.0 × 127.5 × 213.0 | print upright as assembled; gussets under blocks, no supports | 171 | 9.5 |
| post_BL_lo | 1 | warm white | 68.0 × 127.5 × 215.0 | print upright as assembled; gussets under blocks, no supports | 142 | 7.9 |
| post_BL_up | 1 | warm white | 68.0 × 127.5 × 213.0 | print upright as assembled; gussets under blocks, no supports | 148 | 8.2 |
| post_FR_lo | 1 | warm white | 92.0 × 151.5 × 215.0 | print upright as assembled; gussets under blocks, no supports | 189 | 10.5 |
| post_FR_up | 1 | warm white | 92.0 × 151.5 × 213.0 | print upright as assembled; gussets under blocks, no supports | 196 | 10.9 |
| post_BR_lo | 1 | warm white | 68.0 × 151.5 × 215.0 | print upright as assembled; gussets under blocks, no supports | 167 | 9.3 |
| post_BR_up | 1 | warm white | 68.0 × 151.5 × 213.0 | print upright as assembled; gussets under blocks, no supports | 174 | 9.6 |
| rear_lo | 1 | warm white | 175.0 × 215.0 × 13.0 | outer face down | 158 | 8.8 |
| rear_up | 1 | warm white | 175.0 × 213.0 × 13.0 | outer face down | 164 | 9.1 |
| side_L_lo | 1 | charcoal | 215.0 × 176.0 × 13.0 | outer face down | 141 | 7.8 |
| lightbar_side | 4 | green | 90.0 × 16.0 × 5.0 | push in from inside, dot of hot glue on flange | 6 | 0.3 |
| side_L_up | 1 | charcoal | 213.0 × 176.0 × 13.0 | outer face down | 142 | 7.9 |
| channel_cap_L | 1 | charcoal | 28.0 × 130.0 × 13.0 | outer face down | 15 | 0.8 |
| channel_cap_R | 1 | charcoal | 28.0 × 130.0 × 13.0 | outer face down | 15 | 0.8 |
| brow | 1 | smoked black | 175.0 × 43.0 × 13.0 | front face down; smoked/black PETG | 29 | 1.6 |
| lightbar_brow | 2 | green | 38.0 × 10.0 × 5.0 | push in from inside, dot of hot glue | 1 | 0.1 |
| shoulder_FL | 1 | green | 156.5 × 151.5 × 55.0 | top face down, skirts up | 153 | 8.5 |
| shoulder_BL | 1 | green | 156.5 × 151.5 × 55.0 | top face down, skirts up | 153 | 8.5 |
| shoulder_FR | 1 | green | 156.5 × 151.5 × 55.0 | top face down, skirts up | 153 | 8.5 |
| shoulder_BR | 1 | green | 156.5 × 151.5 × 55.0 | top face down, skirts up | 153 | 8.5 |
| splice_shoulder | 2 | charcoal | 30.0 × 105.0 × 6.0 | pins up; dot of glue in each pin hole | 13 | 0.7 |
| plinth_FL | 1 | charcoal | 156.5 × 216.5 × 118.0 | print upright, chamfered edge on bed | 175 | 9.7 |
| plinth_BL | 1 | charcoal | 156.5 × 216.5 × 118.0 | print upright, chamfered edge on bed | 177 | 9.8 |
| plinth_FR | 1 | charcoal | 156.5 × 216.5 × 118.0 | print upright, chamfered edge on bed | 175 | 9.7 |
| plinth_BR | 1 | charcoal | 156.5 × 216.5 × 118.0 | print upright, chamfered edge on bed | 177 | 9.8 |
| fender_FL | 1 | medium grey | 81.0 × 160.0 × 100.0 | print as assembled (open edge down), tree supports inside hood only | 102 | 5.7 |
| fender_BL | 1 | medium grey | 81.0 × 160.0 × 100.0 | print as assembled (open edge down), tree supports inside hood only | 102 | 5.7 |
| fender_FR | 1 | medium grey | 81.0 × 160.0 × 100.0 | print as assembled (open edge down), tree supports inside hood only | 102 | 5.7 |
| fender_BR | 1 | medium grey | 81.0 × 160.0 × 100.0 | print as assembled (open edge down), tree supports inside hood only | 102 | 5.7 |
| tray_mount | 1 | charcoal | 177.0 × 42.5 × 19.2 | plate face down | 105 | 5.8 |
| tray | 1 | medium grey | 146.0 × 240.0 × 33.0 | original v1 tray geometry, moved +2.5 mm X / +45 mm Z | 102 | 5.6 |

## To check before printing everything
- Cart bottom height above floor, and wheel positions/width (3 assumed values above).
- Where the wheel motors sit: the plinth has 30 mm open slots at the axles; widen `box(...WHEEL_Y ± 15...)` if your motor bracket is bigger.

## Folder
`assembled/` assembly + exploded STEP · `step/` · `stl/` (print-oriented) · `3mf/` per colour · `renders/` views, sections, exploded · `coupon/` · `docs/` · `cad/` (v4.py = master)
