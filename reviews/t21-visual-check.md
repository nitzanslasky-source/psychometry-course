# Topic 21: board visual check (all 26 videos)

18 Oct 2026. I rendered every step frame of every topic-21 video in the handwriting build (`AI_HANDWRITE=all`, the build Codex renders), in the private builds `scratchpad/t21v/{test,hw}.html`, and looked at every contact sheet (61 sheets, then 64 after the fixes). I fixed the problems, rendered everything again and looked again. Source: `math_patches/_ai_vis_t21.py` (the earlier version is backed up at `scratchpad/t21v/_ai_vis_t21.py.orig`). The ai_scripts were regenerated from it. I did not touch any shared file.

I used the same standards as the topic-22 check (`t22-visual-check.md`): no result before it is said, no bundled calculations, no overlaps, no shrunk rows, no broken pen glyphs, and every number she says is on the board.

## Fixes that apply to the whole topic (in the spec file only)

- **Right-column spacing (the topic-22 layout fix).** Before, each right-column row was placed as if it were typed. Now each hand-written row gets its real height: 1.45× a typed row, or 1.9× when it has a fraction. The right column starts just below the question's last line. That line is stored in `QBOT`, which I measured on the frames. I checked every slide's last frame afterwards: no hand row is shrunk.
- **`\times` added to the pen mapping.** Without it, a `\times` line fell back to typed text.
- **`✗` in the pen.** In the pen font, `✗` looks like a ×, so "14÷3 ✗" read as "times". There were 27 rows like this. After a number, the mark is now written as ", no". After words that already say it ("20 is skipped", "not different", "one even"), it is dropped. A few rows got an explicit reason instead: "14÷3 not whole", "largest 10, not ≤9".
- **Clock times.** `6{:}40` was drawn by the pen as a group, and every time came out as a stacked, underlined mess (g025, 5 rows). The pen now writes plain `6:40`.
- **Arrow lines shown in pieces.** In the lesson videos, typed lines split by arrows appeared part by part, out of step with her speech: wp-001-2, wp-003, wp-006, wp-008, wp-016, g014, g015, q-r26-t21-02 and wp-022. These lines are now separate rows, each shown at its own clause. Where a line has to keep its arrow, it is now hand-written, and the pen writes it in chunks as she speaks.
- **So-far boxes** go from size 26 to 30, and their arrow was removed.

## Per video

| # | Video | Problems found and fixed |
|---|---|---|
| 1 | wp-001 | The row "A total in parts · a ratio · a short list of cases" was shown all at once, so it became 3 rows, each at its clause. The ✗ glyphs became "not whole". |
| 2 | wp-001-2 | The could/must/cannot line (size 26, cut by arrows) became 3 rows at size 30, each at its words. "Try first → watch and compare" became 2 rows. The ✗ glyphs became ", no". |
| 3 | wp-003 | The arrow line became 2 rows. |
| 4 | g004 | The ✗ in Pop 3 (small) became ", no". Everything else ok. |
| 5 | g005 | The ✗ glyphs were fixed. The board row now says "is divisible by 6", the way she says it after the terminology pass. |
| 6 | wp-006 | The arrow line became 2 rows. |
| 7 | g007 | The formula k(k+1)/2 is now hand-written. The check with ten (10·11/2 = 110/2 = 55, then 5 pairs of 11) became 3 rows at her clauses, where before it was 1 bundled row. The question part ("Now back to our question") moved to its own continuation slide, with a "So far" box that keeps the formula, because the slide was full. 36≤42 and 45>42 are now their own rows, each at its words. |
| 8 | wp-008 | The 2 arrow lines became 4 rows. |
| 9 | g009 | ok. "Undo it: +1, then ×2" is now hand-written. |
| 10 | g010 | "Day 1: 5, Day 2: 10, Day 3: 20" was written with wide gaps and shrank, so it was rewritten as "Days 1, 2, 3: 5, 10, 20". The right column now has proper spacing. The ✗ glyphs became ", no". |
| 11 | wp-012 | ok |
| 12 | g013 | The ✗ glyphs were fixed. Everything else ok. |
| 13 | g014 | The typed arrow lines (s4d, t4a, t4b, t4d) were shown in pieces and are now hand-written. s4d was too wide for the right column and shrank, so it was shortened to "bigger: fewer tenors, 30 out". "Divides by 3" became "divisible by 3". |
| 14 | g015 | The arrow in the So-far box was removed, and the box is bigger. |
| 15 | wp-016 | The 3 rule lines (shown as arrow pieces) are now 2 rows each, each at its clause. The example rows showed the result before it was said ("1+2+23=26"), so they now follow her steps: 1+2=3, 26−3=23 / 1+2+3=6, 20−6=14 / 10+10=20, 26−20=6 / 10+10+10=30, 31−30=1. Each is shown at the clause where she starts it. |
| 16 | g017 | Added 10÷5 to the one-fifth row (she says it). Added the row 14·25=350 that she says in Method 2. The 14·25 rows moved to the right column. |
| 17 | g018 | ok (only the ✗ glyphs) |
| 18 | q-r26-t21-01 | The pair rows were cramped and showed early, so they were simplified ("red, blue, green: no pair yet" / "3 can fail, 4 always work"). Added the 3-red trap 8+6+3=17, which she says but was not on the board. "6 → no 3 of a color" became "2 of each: 2+2+2=6". The ✗ became words. |
| 19 | g019 | 23·8 = 160+24 was bundled, so `20·8=160, 3·8=24` was added at her words and 184 now comes at "A hundred sixty plus". The rows moved to the right column, because the left column had grown into the choices. |
| 20 | g020 | Added 36÷3=12, which she says. "12, 12, 12 ✗" became "equal". The 13, 12, 11 row now shows the sum 13+12+11=36, which she says. These rows are in the right column. |
| 21 | g021 | The long row "at most 12 go up → at least 26−12=14" showed 14 before it was said, so it became 2 rows. Added "13<14: 13 is impossible" at her words. The edge rows now show 26·3 and 25·3. |
| 22 | q-r26-t21-02 | The typed arrow line was shown in pieces and is now hand-written. Rows were rebalanced into the right column, because the left column ran into the choices. The ✗ glyphs were fixed. |
| 23 | wp-022 | The 3^20 line was shown in pieces (3 parts) and is now hand-written. |
| 24 | g023 | The typed trap line was shown at once and its 110 came early, so it became 2 hand rows in the right column: "before the removal: 140" and "140−30=110: after, the trap" at "A hundred ten would be". The left column no longer touches the choices. |
| 25 | g024 | The check row "43=40+3 ✓ 41, 42, 44: 1, 2, 4 ✗" was bundled, so it became 2 rows, each at its clause. |
| 26 | g025 | The clock times were broken (see above). The rows were at size 28 and are now 30. "4 times, 3 gaps: 6:40→…→10:40" showed all the times before she said them, so it became 2 rows ("4 times, 3 gaps" / "8:00 2nd, 9:20 3rd, 10:40 4th" at "So eight o'clock"). The bundled "6:40+80 min = 8:00, 9:20, 10:40" became 3 rows (80 min = 1 h 20 min / 6:40+1:20=8:00 / then 9:20, then 10:40). |

Fixed: 23 of 26 videos. Three were ok as they were: wp-012, g009 (only a typed row made hand-written) and g018 (only the glyphs).

## Spoken text

There are **no spoken-text changes**. Every line she says is word for word as before. I checked the regenerated ai_scripts against the spoken lines in the build from before my edits. The only differences are "divides by" and "is divisible by", and those come from the terminology pass (`terminology.py`), which is applied at build time as before.

One structural note: in g007, the line "Now back to our question…" now opens a new continuation slide (slide 3). It used to be the 6th line of slide 2. The words are the same.

## Checks (final)

- `python3 math_patches/_ai_vis_t21.py`: no PROBLEMS.
- `SRC=test.html python3 ai_check.py <26 ids>`: 26 of 26 OK. The only notes are about wording ("either", "schedules", "three hundred sixty"), and those were there before.
- `python3 math_check.py 21`: 0 problems, 0 warnings, layout 0 (72 slides).
- `AI_HANDWRITE=all python3 math_check.py 21`: 0 problems, 0 warnings, layout 0.
- All 326 step SVGs are valid XML. No hand-written row is shrunk below its normal scale (I checked the last frame of every slide).

## Left / for Nitzan

- There is one new continuation slide, in g007, with a "So far" box that keeps the formula.
- Some method-header lines ("Method 1: Understanding: push to the extremes") wrap onto 2 small lines on slides that use the right column (g014, g019, g020, q-r26-t21-02). They are readable and do not overlap anything, so I left them.
