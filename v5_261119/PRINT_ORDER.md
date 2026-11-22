# Print order, bottom to top (start with 00)

Same number = same order you assemble. Files are already rotated to print orientation. A part with Qty > 1 is one file: print it that many times.
Tip: parts of the same colour can share one plate (see `3mf/plates_<colour>.3mf`).

| No. | File | Qty | Colour | g each | h each | Note |
|---|---|---|---|---|---|---|
| 00 | 00_tolerance_coupon.stl | 1 | any | - | ~1 | PRINT FIRST: check fit rows 0.20/0.30/0.40 |
| | **A  Bottom: plinth (print upright)** | | | | | |
| 01 | 01_plinth_FL.stl | 1 | charcoal | 176 | 9.8 | print upright, chamfered edge on bed |
| 02 | 02_plinth_FR.stl | 1 | charcoal | 176 | 9.8 | print upright, chamfered edge on bed |
| 03 | 03_plinth_BL.stl | 1 | charcoal | 178 | 9.9 | print upright, chamfered edge on bed |
| 04 | 04_plinth_BR.stl | 1 | charcoal | 178 | 9.9 | print upright, chamfered edge on bed |
| | **B  Bottom: fenders (cap down, no supports)** | | | | | |
| 05 | 05_fender_FL.stl | 1 | medium grey | 131 | 7.3 | PRINT cap-down (axis vertical); flare 40 deg from vertical, no supports |
| 06 | 06_fender_FR.stl | 1 | medium grey | 131 | 7.3 | PRINT cap-down (axis vertical); flare 40 deg from vertical, no supports |
| 07 | 07_fender_BL.stl | 1 | medium grey | 131 | 7.3 | PRINT cap-down (axis vertical); flare 40 deg from vertical, no supports |
| 08 | 08_fender_BR.stl | 1 | medium grey | 131 | 7.3 | PRINT cap-down (axis vertical); flare 40 deg from vertical, no supports |
| | **C  Lower body (z 150-355)** | | | | | |
| 09 | 09_post_FL_lo.stl | 1 | warm white | 166 | 9.2 | print upright as assembled; gussets under blocks, no supports |
| 10 | 10_post_FR_lo.stl | 1 | warm white | 191 | 10.6 | print upright as assembled; gussets under blocks, no supports |
| 11 | 11_post_BL_lo.stl | 1 | warm white | 144 | 8.0 | print upright as assembled; gussets under blocks, no supports |
| 12 | 12_post_BR_lo.stl | 1 | warm white | 169 | 9.4 | print upright as assembled; gussets under blocks, no supports |
| 13 | 13_door_lo.stl | 1 | warm white | 143 | 7.9 | outer face down on textured PEI |
| 14 | 14_vent_lo.stl | 1 | charcoal | 107 | 5.9 | outer face down |
| 15 | 15_rear_lo.stl | 1 | warm white | 159 | 8.8 | outer face down |
| 16 | 16_side_L_lo.stl | 1 | warm white | 142 | 7.9 | outer face down |
| 17 | 17_lightbar_side_x4.stl | 4 | green | 6 | 0.3 | push in from inside, dot of hot glue on flange |
| | **D  Upper body (z 355-560)** | | | | | |
| 18 | 18_post_FL_up.stl | 1 | warm white | 173 | 9.6 | print upright as assembled; gussets under blocks, no supports |
| 19 | 19_post_FR_up.stl | 1 | warm white | 198 | 11.0 | print upright as assembled; gussets under blocks, no supports |
| 20 | 20_post_BL_up.stl | 1 | warm white | 150 | 8.4 | print upright as assembled; gussets under blocks, no supports |
| 21 | 21_post_BR_up.stl | 1 | warm white | 176 | 9.8 | print upright as assembled; gussets under blocks, no supports |
| 22 | 22_door_up.stl | 1 | warm white | 115 | 6.4 | outer face down on textured PEI |
| 23 | 23_vent_up.stl | 1 | charcoal | 107 | 5.9 | outer face down |
| 24 | 24_rear_up.stl | 1 | warm white | 165 | 9.2 | outer face down |
| 25 | 25_side_L_up.stl | 1 | warm white | 143 | 8.0 | outer face down |
| | **E  Top of body: brow + channel** | | | | | |
| 26 | 26_brow.stl | 1 | smoked black | 28 | 1.6 | front face down; smoked/black PETG |
| 27 | 27_lightbar_brow_x2.stl | 2 | green | 1 | 0.1 | push in from inside, dot of hot glue |
| 28 | 28_channel_cap_L.stl | 1 | charcoal | 27 | 1.5 | outer face down |
| 29 | 29_channel_cap_R.stl | 1 | charcoal | 27 | 1.5 | outer face down |
| | **F  Green shoulder (top)** | | | | | |
| 30 | 30_shoulder_FL.stl | 1 | green | 146 | 8.1 | top face down, skirts up |
| 31 | 31_shoulder_FR.stl | 1 | green | 146 | 8.1 | top face down, skirts up |
| 32 | 32_shoulder_BL.stl | 1 | green | 146 | 8.1 | top face down, skirts up |
| 33 | 33_shoulder_BR.stl | 1 | green | 146 | 8.1 | top face down, skirts up |
| 34 | 34_splice_shoulder_x2.stl | 2 | charcoal | 13 | 0.7 | pins up; dot of glue in each pin hole |
| | **G  Tray (last)** | | | | | |
| 35 | 35_tray_mount.stl | 1 | charcoal | 105 | 5.9 | plate face down |
| 36 | 36_tray.stl | 1 | medium grey | 102 | 5.6 | original v1 tray geometry, moved +2.5 mm X / +45 mm Z |

Total: about 4.6 kg, 256 printer-hours (estimate +-30 %).
