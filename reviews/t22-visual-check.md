# Topic 22: board visual check (all 34 videos)

18 Oct 2026. I checked every contact sheet of every video in the handwriting build (`AI_HANDWRITE=all`, the build Codex renders), in the private builds `scratchpad/t22v/{test,hw}.html`. That came to about 115 sheets of step frames. After the fixes I rendered all 34 videos again and looked again. Source: `math_patches/_ai_vis_t22.py` (backup of the earlier version: `scratchpad/t22v/_ai_vis_t22.py.orig`). No shared files were touched.

Standards used: V1–V4, the Codex review standard, and batch-C (no results before they are said, no bundled calculations, no overlaps, no shrunk rows, no unclear captions, every number she says is on the board).

## Fixes that apply to the whole topic (in the spec file only)

- **Right-column spacing.** The right column was placed as if every row were typed text. Hand-written rows are about 1.3× taller, and fraction rows taller still, so the renderer pushed each row under the one above with a 14 px gap. The result was cramped rows, rows touching each other, and later rows shrunk or squeezed into the choices. Now each hand row (and each fraction row) gets its real height, and the right column starts just below the question's last line (`QBOT`, measured on the frames).
- **Labels made bigger.** Ratio-table ×k arrow labels go from 24 to 28. The down-arrow labels go from 26 to 30 (side margin 100). Ratio-unit labels, brackets and values go up to 27–30. Number-line ticks and labels go up to 28–30. "So far" boxes go from 26 to 30.
- **Broken hand glyphs.** The `✗` glyph rendered as a broken box in the pen font, in 16 rows. These rows now say ", no". `\times` was missing from the pen mapping, so it was added (before, "(×3)" showed as "(imes3)"). Rows I added with single backslashes (they broke the SVG, so `\frac` showed as "=rac") were fixed. All step SVGs now parse: 0 broken.
- **Arrow rows.** An arrow-split line ("Translate → solve → answer", "is → = of → ×", "x whole ⇒ 2x even", "Read → build → solve") was cut on screen and shown in pieces. These were rewritten without arrows, or split into separate rows.
- **Bundled calculations were split into rows, each at its own clause.** Typical examples: `12·7 = 70+14 = 84` became `10·7=70`, `2·7=14`, `12·7=84`. Checks such as `(1) 24: 8·24=192, 7·27=189` became two rows, each written as she says it.
- **Results shown early were moved to their clause.** The equation was moved to "So A is equal to B plus three", not "A is three more than B". The same was done for `B=A−5`, `A=4B` and the half/twice rule. `6p≤105<7p`, the key line I added, appears at "seven tickets cost more". The row for each tested choice now comes with its own calculation, not with "Choice number N".

## Per video

| # | Video | Problems found → fixed |
|---|---|---|
| 1 | wp-027 | Stage 3 row `x=8 … 8−1=7` showed 7 before she said it, so it was split. The `7x−3x=4x` and `4x−x=3x` steps she says were missing, so they were added. The question text was size 27, now 30. |
| 2 | wp-027-2 | Equations showed in the same row as the phrase, before they were said, so they were split and timed. Sam/Ben check: "12" was said before the subtraction, so there are now 2 rows. The twice/half line was split. The tablet line `300 = ¾·400` and the third-less row were split. Rows were size 28, now 30–32. |
| 3 | wp-027-3 | The arrow line "is → = of → ×" showed in pieces, so it became 2 rows. `⅓ of 30, ⅔ of 30` became 2 rows. `2M=5P` is now its own row at its clause. The summary arrow line was rewritten. The phrase table (size 26, running off the slide) became 2 rows at size 30. |
| 4 | wp-028 | The arrow line was cut, so it became 2 lines, each at its clause. |
| 5 | g029 | The 70+14 and 8+4 / ½·8 bundles were split. The down arrow ×1½ now comes after "one and a half" is said. Table labels are bigger. |
| 6 | g030 | `18<?<36` became 2 rows, at "more than 18" and at "fewer than 36". The across/down rows now show the multipliers she says (×1½, 20/12 = 5/3). The cancelling steps 18÷6 and 12÷6 were added. 60/2 and =30 are split. The second example moved to its own slide (the frames were cramped). Rows were split in method 2. The 12·30=360 check was added. The "So far" box was simplified. |
| 7 | q-r26-t22-02 | The trap row became 3 rows (4·10/6, = 6⅔ days, "fewer workers, fewer days? No"). The rule was split. Rows in the right column no longer touch. `4d=60`. |
| 8 | wp-031 | ok |
| 9 | g032 | ok (the arrow parts of the hand rows are timed to the line) |
| 10 | g033 | The `+½ h → +4` row was split from 36+4=40. The van example became 3 rows; "5 vans" now appears at "So the answer is five vans", where before it showed with "50 people". |
| 11 | wp-034 | Added the 7 = 2⅓·3 she says. Blue/red boxes are bigger. The arcs figure is wider and its ✓/✗ captions bigger. `3x/7x=3/7` is its own row. x=5, red 15 and blue 35 are now 3 rows. The mugs/plates check became 2 rows. |
| 12 | g035 | Row 7 was cut ("x whole ⇒ …" shown as "x whole"), so it was rewritten. `2x=22→x=11: 55 and 77` was split into 3 rows. Added the board line "total = 12x: divisible by 5+7=12" she says. The bar is narrower so it doesn't run into the column. |
| 13 | g036 | ok (bracket labels bigger) |
| 14 | q-r26-t22-01 | Rows had single backslashes, so they broke. The 2:3:5 trap was shown as "✗ (60)" and is now 2 rows (5x=30, 10x=60 / why it's wrong). Expanding the ratios (×4, ×3) and the results are now separate rows. 35x, the ⅘/⅔ steps and 16+24, +30 were split. Right-column rows overlapped, which the spacing fix solved. |
| 15 | q-r26-t22-03 | `×3`/`×2` showed as "imes" (glyph mapping fixed). The `5 units=10 → 1 unit=2`, `10x=60→x=6` and `9x=9·6=54` bundles were split. The 30x−60 row now appears at "five times four x", the last of the three products. |
| 16 | wp-037 | The arrow line was rewritten. |
| 17 | g038 | The plug-in rows (192/189, 168/168) were split. The 140+49 and 140+28 she says were added. Added `21+3=24` (the trap) and "every row: 21 chairs". |
| 18 | q-r26-t22-20 | The Dan/Ella table was small (size 28, rowh 58) and is now in the left column at size 32. Added `6÷2=3` (half the gap). The check row became 3 rows. `2k=32→k=16` was split. Number-line labels are bigger. The "So far" box was shortened. |
| 19 | wp-039 | ok |
| 20 | g039 | The "5 years ago" row was written before Maya's calculation, so `x−5` and `x+9−5=x+4` were added at their clauses. Added the gap check (x+4)−(x−5)=9. The 4-and-8 example now comes before its rule line, which was shortened. Each choice now has 2 rows, one for the ages and one for the gap. The insight now has its own rows (gap 9, Maya = 2·Tom; t / 2t). |
| 21 | g040 | Added `6·17=102, 3 left, 3/6=½`, so 17½ is not bundled. Choice rows were split, with ≤105 / >105 written. W20 addition (see the teaching check). |
| 22 | r26-t22-shortcuts | The "·" separator was spaced oddly, so the line was rewritten. |
| 23 | g042 | The triangle-value row became 3 rows (2·1/1.5, ×2/×2, =4/3). The table shows 1.5. Rows were shrunk, so the adding up moved to its own slide (with a "So far" box: kiwis 2, limes 1, pineapples 4/3). The estimate rows now show 3+1 and 3+2. |
| 24 | g043 | Added 160÷2=80 and 80÷2=40 (she halves twice). The level-2 bar values appeared before "is thirty". Level 2 moved to its own slide with "So far: after level 1: 120", because the rows were shrunk before. The trap row 160−40−40=80 is now shown at her words. `3·3=9, 4·4=16` was added. |
| 25 | g044 | `C/T=5/8 → 5:8` and `5x/13x=5/13` were split. Rows were rebalanced across the columns. |
| 26 | g045 | The first row was typed, with a ✗ and a bundled check. It is now 3 hand rows (supermarket ✓, cafe "No"). The slide was shrunk, so it was split, with a "So far: cafe 5, supermarket 10" box. Rows were split. The estimate became 4 rows. The number line uses plain 1/5, 1/2 and 2/5 (the ⅕ glyphs were tiny). |
| 27 | g046 | The bundled `10=⅚: ⅙=2→6·2=12` rows were split into ⅙ = 10÷5 = 2 / 6·2 = 12 and the chocolate rows. The box values appeared before they were said. The estimate rows now show ⅙·26 and ⅓·48. The rows that were shrunk were rebalanced. |
| 28 | g047 | The 12+6=18 step was added, and `18=2x→x=9` and 5x / 5·9=45 were split. The total moved to its own slide (with "So far: x = 9 (bus B)"), because 5·9=45 ran into the choices. The divisibility rows were split, and they now show 39 = 3·13 and 48 = 3·16, as she says. |
| 29 | g048 | The bundled plug-in rows were split. The hourly-cost calculations she says (4·65, 7·50, 7·45) were added. Choice 2 moved to its own slide ("So far: (3), (4) out"), because the slide was shrunk. Subtract row 3h=135 now appears at "385 minus 250". |
| 30 | g049 | The 1+9 / 4+6 / 5+5 pairs she says were added. The third steps (9+3, 3 = ⅓·9) and 240+80 were split. 12L+8S and = 80·4 = 320 are now separate rows. |
| 31 | g050 | `2n=100→n=50` was split, and 70+30 was added. 50/20 and = 5/2 were split. The columns were rebalanced (a shrunk row). |
| 32 | r26-t22-exam-tools | The double row was split (= 2(2a+3p) / = 2·13 = 26). The 3a+2p row was split, and "cannot be determined" is now at its clause. The first pair's check is its own row. |
| 33 | q-r26-t22-04 | The pens/notebooks calculation became 2 rows. Each choice row now writes the choice's expression and its own steps, at the clause where she works it out. |
| 34 | q-r26-t22-05 | 120−96=24 was added before 24=2m. The "car instead" and "all cars" rows were split. |

Fixed: 30 of 34 videos. ok as they were: wp-031, g032, g036, wp-039.

## Checks (final)

- `python3 math_patches/_ai_vis_t22.py`: no PROBLEMS. The layer order is fine, and the method vocabulary is fine.
- `SRC=test.html python3 ai_check.py <34 ids>`: 34 of 34 OK. The notes only are about wording ("three hundred sixty" and similar), which were there before.
- `python3 math_check.py 22`: 0 problems, 0 warnings, layout 0 (107 slides).
- `AI_HANDWRITE=all python3 math_check.py 22`: 0 problems, 0 warnings, layout 0.
- All step SVGs are valid XML. No hand-written row is shrunk below its normal scale (my check over the last frame of every slide).

## Left / for Nitzan

- Six new continuation slides: g030, g042, g043, g045, g047, g048. Their content and methods are unchanged, and each has a "So far" box where the next step needs an earlier result.
- Spoken text changed only in g040, for the W20 addition. Everything else is board only.
