# External fixes — Codex final report, topic 25 (22 Oct 2026)

Source: Codex `work/external-expanded-2026-10-22/Complete-review-and-recommendations.txt`, section 2, item 2:
"increase several selected values by a fixed amount" (extends the existing sum-sharing method; not a new formula).

File changed: `studio-build/math_patches/_ai_vis_t25.py` only (+ the scripts it writes: `ai_scripts/wp-080-3.json`;
the other five t25 lesson scripts were re-written byte-identical / unchanged in content). Before-copy:
`scratchpad/xf-t25/_ai_vis_t25.before.py`. Nothing committed, no shared studio / Reading Studio rebuild, nothing
marked ready.

## Status check (condition 1)
`video_status.py --list record --gate held`: wp-080, wp-080-2, wp-080-3, wp-081, wp-081-2, wp-081-3 all **Held** (for
this job). `~/Documents/Course.recordings/_reading/<id>/` does not exist for any of the six: no takes. Only wp-080-3
was edited.

## The change — wp-080-3 (Averages, Part 3 of 3), new slide 4 "Several values change"

**Where and why there:** the lesson builds one → several → every: slide 3 "One value changes" (the sum changes by
ten, "we share the ten among them", ÷ 5) and then slide 5 "Every value changes" (+3, ×2). The new slide sits between
them, so it is a direct extension of "share the change in the sum" that the student has just seen, before the
special case where every value changes. "Share the extra" (newcomer, wp-081) is a different situation (the count
changes), so the new slide does not go there. Topic 25 comes after topics 1-12, 21-24 in planData ORDER; it only
needs multiplication and division (topic 1).

**BEFORE:** (nothing) — slide 3 "One value changes" was followed directly by slide 4 "Every value changes".

**AFTER (new slide, 5 paragraphs, ~115 words, about 40 s):**

> P1. And what if several values change by the same amount? Six students took a test, and their average score is
> eighty. Four of them each get three more points.
>
> P2. First, the sum. Four scores go up by three points each, so the sum goes up by four times three, that's twelve
> points.
>
> P3. Now we share those twelve points among all six scores, not only the four that changed. Twelve divided by six
> is two, so the average goes up by two.
>
> P4. So the new average is eighty plus two, eighty-two.
>
> P5. This works whenever the number of values stays the same. Find the total change in the sum, then share it among
> all the values.

Numbers are new (Codex's example: 10 scores, 70, five +6 → 73; ours: 6 scores, 80, four +3 → 82). Recomputed:
4 × 3 = 12; 12 ÷ 6 = 2; 80 + 2 = 82. Check with real scores: e.g. 80 ×6 = 480 → 480 + 12 = 492 → 492 ÷ 6 = 82. ✓

## Board items (V3/V4: each written at its clause; hand-written rows are pen-safe)

| item | text on the board | appears at (cue, substring of its line) |
|---|---|---|
| a_j1 (typed) | 6 scores, average 80 | P1 "Six students took a test" |
| a_j2 (typed) | 4 of them: +3 each | P1 "Four of them each get" |
| a_j3 (hand) | the sum goes up: 4×3=12 | P2 "four times three" |
| a_j4 (hand) | 12÷6=2: the average +2 | P3 "Twelve divided by six" |
| a_j5 (hand) | 80+2=82 | P4 "eighty plus two" |
| a_j6 (typed key line) | Same number of values: the change in the sum ÷ all the values | P5 "whenever the number of values stays the same" |

Visual requirement: the two givens are on the board before any calculation; 12 is written only when "four times
three" is said; the ÷6 row only at "Twelve divided by six"; 82 only at "eighty plus two"; the key line with its
condition at P5. One column, rows under each other, no early results, no figure needed (the change is a sum, shown
as one multiplication).

## Conditions / prerequisites (W22, condition 4)
- Condition stated aloud and on the board: the number of values stays the same (otherwise it is a join/leave case,
  taught in wp-081 "share the extra").
- The trap is named: share among all six, not only the four that changed.
- W22 order: names the quantity (the sum) → the calculation (4 × 3) → what it tells us (the sum goes up by 12); then
  the sharing (÷ 6) → what it tells us (the average goes up by two) → the new average.
- W23: an addition only; no Hebrew method in wp-080 / wp-081 changed or removed (Hebrew wp 5175-5326 has "one value
  changes" via the sum; this extends it).

## Part lengths
wp-080-3: 604 → 718 words, 3.7 → 4.4 min (165 wpm). Under ~5 min, so no re-split. wp-080 3.4, wp-080-2 4.0, wp-081
4.8, wp-081-2 3.8, wp-081-3 3.0 (unchanged).

## Checks
- Spec run (`python3 math_patches/_ai_vis_t25.py wp-080 … wp-081-3`): no PROBLEMS. wp-080 and wp-080-2 scripts are
  byte-identical to the before-copies.
- Private builds only: `OUT=scratchpad/xf-t25/test.html` and `AI_HANDWRITE=all OUT=scratchpad/xf-t25/hw.html
  python3 build_verbal.py` both EXIT 0 (only the usual added_notes warnings, e.g. "no note for added video wp-080-3").
- `SRC=<test> python3 ai_check.py wp-080 wp-080-2 wp-080-3 wp-081 wp-081-2 wp-081-3`: all OK; wp-080-3 also OK on the
  handwriting build.
- `python3 math_check.py 25`: PROBLEMS 0, WARNINGS 0, layout 0 (86 slides, 728 items); same with AI_HANDWRITE=all.
- Frames: all 51 step frames of wp-080-3 made from the handwriting build; the new slide (s4, 7 steps) LOOKED at: the
  givens appear first, then each hand-written row at its clause, no early results, no overlap, readable sizes; the key
  line wraps to two lines inside the camera-safe width (fine). Fixes made after the first look: the sum row now
  reads "the sum goes up: 4×3=12" (was "the sum: 4×3=12", which read as if the sum were 12), and the key line now
  shows the condition ("Same number of values: the change in the sum ÷ all the values"), shown at "whenever the
  number of values stays the same". Neighbouring slides unchanged. Headless Chrome closed (none left).
- Prompter dump (`reading_studio.prompter_display`), new paragraphs:
  1. "And what if several values change by the same amount? Six students took a test, and their average score is 80. / Four of them each get three more points."
  2. "First, the sum. Four scores go up by three points each, so the sum goes up by 4 × 3, that's 12 points."
  3. "Now we share those 12 points among all six scores, not only the four that changed. / 12 ÷ 6 = 2, so the average goes up by two."
  4. "So the new average is 80 + 2, 82."
  5. "This works whenever the number of values stays the same. Find the total change in the sum, then share it among all the values."
  All maths display correctly (no bare "over"/"times").

## Read-aloud (condition 5)
Read each paragraph aloud against the frames. "Four of them" → the board says "4 of them: +3 each" under "6
scores", so "them" = the students' scores; P2 names "the sum" before calculating; P3 "those twelve points" refers to
the 12 just written; "the four that changed" is named; P5 "it" = "the total change in the sum" in the same sentence.
No unclear this/that/it. The flow from "One value changes" (P: "The change in the sum is shared among all the
values") into "And what if several values change…" is natural. Result: OK, ready for Codex review (not marked
ready; the six lessons stay Held).

## Proposals for recorded videos
None (no recorded lesson touched).

## Needs Claude
None. Optional for Codex: the Summary slide of wp-080-3 was left as it was (its "adding the same amount" line covers
every value changing). If Codex wants the summary to mention this case too, one line could go there; I left it out
to keep the part short (now 4.4 min).
