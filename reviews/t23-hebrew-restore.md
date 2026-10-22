# Topic 23: four approved Hebrew restores (22 Oct 2026)

Source of the items: `reviews/hebrew-vs-english-t23.md` section 3, items 1-2, plus the reminder and the summary box.
Her Hebrew read: `~/Downloads/02-Word-Problems-Original-Subtitles.txt` lines 3892-4007 (Q62) and 4148-4228 (Q64).
Files changed: `studio-build/math_patches/_ai_vis_t23.py` (g062, g064 scripts and boards), `math_patches/t23.py` (wp23-g062
question data only), `summary_pages/t23.json`, `added_notes.json` (one note for g062 updated to the new numbers).
Regenerated: `ai_scripts/solve-wp23-g062.json`, `ai_scripts/solve-wp23-g064.json`, `~/Downloads/Topic-23-Summary-Page.html`.
Before-copies: `scratchpad/heb23/before/`. No git, no recorded paragraph touched.

## 0. Recording status (checked first)

`python3 video_status.py --list record` + `~/Documents/Course.recordings/_reading/<id>/`:

| Video | Status | Take? | Result |
|---|---|---|---|
| solve-wp23-g062 | Record | none | edited |
| solve-wp23-g064 | Record | none | edited |
| **wp-053** | **Send (recorded)** | `wp-053-2026-10-21T15-15-25-048Z.wav` (full take, 880 s) | **not edited**: item 3 is written below under "Proposals for recorded videos" |

Item 3 was described as "wp-053 (part 1, unrecorded)", but part 1 of lesson 2 *is* `wp-053`, and she recorded it on 21 Oct.
The unrecorded parts are wp-053-2/-3/-4 (multipliers, working backwards, the flip rule), and none of them is the start of the
lesson. So the reminder can only go in as a patch recording (see the proposal).

## 1. solve-wp23-g064: her "drop a zero to see the ratio" shortcut restored

**Her Hebrew (lines 4196-4213):** after the triangle value she says there's no clear ratio across or down, "but there is":
70 → 14 is hard to see, 7 → 14 is easy. "I dropped a zero, divided by ten", so 15 → 1.5, ×2 = 3. Then "another way", the
middle step through 10%. Her closing line: with "some manipulation or an extra step, dividing by 10 or by 7", the ratio is
easier to see.

**English numbers (checked on the real question data, `t23.py` G11):** the market gets 70%, the factory the rest (30%), the
difference is 40% = 48 kg, and the factory gets 36 kg (choice 2). Drop a zero: 40 → 4, 30 → 3. Across the row 4 → 48 is ×12
(4 · 12 = 48 ✓), so 3 · 12 = 36 ✓. (Before dropping, 40 → 48 is ×1.2 ✓.) Ratio 3:4 = 30:40 ✓.

**Placement:** Method 2 is now "two shortcuts". Shortcut (a), drop a zero, comes first, as in her video, and then the
existing 10% middle step, with its wording unchanged except for the lead-in. Method 1 (the triangle value) is unchanged. Method 2
still starts from the givens (R30). The 10% step now has its own slide, with a "So far" box (`factory 30%, 40% = 48 kg`),
because six hand-written rows plus two more ran into the choices in the handwriting layout (math_check layout).

**Condition (W22 shortcuts):** said aloud: both percents are divided by *the same number, ten*, so the ratio 3:4 = 30:40 stays,
and the kilograms column is not touched. When it helps: "Drop a zero when it makes the step across easy to see."

**Prerequisites:** the ratio table, "across the row" and the triangle value come from topic 22 and are already used in Method 1
of this video. Dividing by ten is basic. Nothing new is assumed.

### BEFORE → AFTER (slide.paragraph; 1-based)

- **1.2** BEFORE: "… We'll solve it in two different ways, with the ratio table, and then with ten percent."
  AFTER: "… We'll solve it in two different ways, with the ratio table, and then with two shortcuts."
- **3 (title)** BEFORE: "Method 2 · The math way: through ten percent" → AFTER: "Method 2 · The math way: two shortcuts" (slides 3 and 4)
- **3.1** BEFORE: "[pause] Now a shorter way. We start again from the givens. The factory gets the rest, thirty percent. The difference is seventy minus thirty, forty percent, and that's forty-eight kilograms."
  AFTER: "[pause] Now two shortcuts. We start again from the givens. The factory gets the rest, thirty percent. The difference is seventy minus thirty, forty percent, and that's forty-eight kilograms."
- **3.2 NEW**: "The first shortcut is to drop a zero. In the ratio table, forty percent goes with forty-eight kilograms. From forty to forty-eight, across the row, is times one point two. That step isn't easy to see."
- **3.3 NEW**: "So let's drop the zero from both percents. Forty becomes four, and thirty becomes three."
- **3.4 NEW**: "We divided both percents by the same number, ten. Three to four is the same ratio as thirty to forty. So the kilograms column stays as it is, forty-eight and the question mark."
- **3.5 NEW**: "Now the step across is easy to see. From four to forty-eight is times twelve."
- **3.6 NEW**: "The factory's row has the same step across. Three times twelve is thirty-six kilograms."
- **3.7 NEW**: "Drop a zero when it makes the step across easy to see. Choice number two is our answer."
- **4.1** (was 3.2) BEFORE: "From forty percent to thirty percent isn't one easy step. So let's take a middle step, ten percent. Forty percent divided by four is ten percent. So we divide the kilograms by four too. Forty-eight divided by four is twelve."
  AFTER: "Now the second shortcut. From forty percent to thirty percent isn't one easy step. So let's take a middle step, ten percent. …" (rest unchanged)
- **4.2, 4.3** (were 3.3, 3.4): unchanged.

### Board (hand-written rows, each at its clause)

| Slide | Item | Text | Shown at | Column |
|---|---|---|---|---|
| 3 | b_7 (kept) | `40% = 48` | "forty-eight kilograms" | left |
| 3 | b_z1 | `40 → 48: ×1.2` | "From forty to forty-eight" | left |
| 3 | b_z2 | `drop a zero: 40 → 4` | "Forty becomes four" | left |
| 3 | b_z2b | `30 → 3` | "thirty becomes three" | left |
| 3 | b_z3 | `both ÷10: 3:4 = 30:40` | "We divided both percents" | left |
| 3 | b_z4 | `4 → 48: ×12` | "From four to forty-eight" | right |
| 3 | b_z5 | `3·12 = 36 kg` | "Three times twelve is" | right |
| 3 | tick | choice 2 | "Choice number two is our answer" | — |
| 4 | So-far box | `factory 30%, 40% = 48 kg` | the slide's first words | right/top |
| 4 | b_8, b_9 (kept) | `10% = 48÷4 = 12`, `30% = 3·12 = 36` | as before | — |

Visual requirement: `40% = 48` is on the board before "drop a zero"; nothing shows 36 before "Three times twelve" (no early
result). The new slide-3 lines add about 35 seconds (spec estimate 3.0 min; it was about 2.6).

## 2. solve-wp23-g062: her fraction-table step restored (new question numbers)

**Her Hebrew (lines 3892-4007):** 25% of 50% of x = 6; what is 37.5% of x? (1) Calculation: ¼ · ½ · x = 6 → x = 48;
"37.5/100 is 3/8, a fraction you should know. Review the tables of fractions and percents you must know by heart"; 3/8 of 48 = 18.
(2) Insight: 73% of 84 = 84% of 73 (one multiplication), so 25% of 50% = 50% of 25% = 12.5%; 37.5 is 3 times 12.5, so 3 · 6 = 18.

**Why the numbers had to change:** the English target 13.5% is not a table fraction, so step (1) had become 10% + 3% + ½%.

**New question (all different from hers except the target 37.5%, as the teacher proposed):**
"25% of 30% of y equals 9. What is 37.5% of y?" Choices **(1) 15 · (2) 36 · (3) 45 · (4) 120**, correct **(3) 45**.
- Check: ¼ · 3/10 = 3/40; 3/40 · y = 9 → 1/40 · y = 3 → y = 120 ✓. 37.5% = 3/8; 120 ÷ 8 = 15 (halve three times: 60, 30, 15);
  3 · 15 = 45 ✓. Swap: ¼ of 30% = 7.5%; 7.5% of 120 = 9 ✓; 37.5 = 5 · 7.5 ✓ → 5 · 9 = 45 ✓.
- Traps: (4) 120 = y itself (stopping early, said aloud in the video); (1) 15 = only an eighth (forgot the "three"); (2) 36 = 30% of y
  (the wrong percent). None is a whole number 1-4 or a unit fraction, so `_choice_order.py` doesn't move them (build: 0 warnings for t23).
- Data changed in `math_patches/t23.py` (G8 block): stem, choices, correct = 3, the written explanation (3 lines: the equation,
  the 3/8 table step, the swap), and the old `_rn_video` studio lines (the base script, replaced by the AI spec, updated so no
  stale numbers stay in the source). `_ai_vis_t23.py`: STEMS23 and the So-far boxes. `added_notes.json`: the note
  "9/200 of y = 9 → y = 200" → "3/40 of y = 9 → y = 120". The video title follows the stem automatically.

**Methods kept, all of hers:** the straight multiplication; **37.5% = 3/8 from the fraction table** ("This is why we memorize the
table"); the swap trick (with both of the English examples, 32% of 50 and 4% of 75). Prerequisite: the fraction table (12.5% = ⅛,
37.5% = ⅜) is taught in wp-052 part 2, so it gets a short reminder only (R29): "Remember why. Twelve point five percent is an eighth…"

### BEFORE → AFTER (slide.paragraph; Method 1 is now two slides because of the extra rows)

- **1.1** BEFORE: "Twenty-five percent of eighteen percent of y is equal to nine. What is thirteen point five percent of y?"
  AFTER: "Twenty-five percent of thirty percent of y is equal to nine. What is thirty-seven point five percent of y?"
- **1.2** unchanged.
- **1.3** BEFORE: "Let's start with the math way. Twenty-five percent is a quarter. Eighteen percent is eighteen over a hundred, which reduces to nine over fifty."
  AFTER: "Let's start with the math way. Twenty-five percent is a quarter. Thirty percent is thirty over a hundred, which reduces to three tenths."
- **1.4** BEFORE: "So a quarter, times nine over fifty, times y, is equal to nine." → AFTER: "So a quarter, times three tenths, times y, is equal to nine."
- **1.5** BEFORE: "A quarter times nine over fifty is nine over two hundred. So nine two hundredths of y is nine."
  AFTER: "A quarter times three tenths: one times three is three, and four times ten is forty. So three fortieths of y is nine."
- **1.6** BEFORE: "Nine two hundredths of y is nine, so one two hundredth of y is one. So y is two hundred."
  AFTER: "Three fortieths of y is nine. So one fortieth of y is nine divided by three, three."
- **1.7 NEW**: "The whole y is forty fortieths, so y is forty times three, a hundred twenty."
- **1.8 NEW**: "Careful, a hundred twenty is y, not what they ask. That's choice number four, a trap."
- **2.1** BEFORE (old 1.7): "Now what they ask, thirteen point five percent of two hundred. Ten percent of two hundred is twenty. Three percent is six. And half a percent is one."
  AFTER: "Now what they ask, thirty-seven point five percent of a hundred twenty. Thirty-seven point five percent is in our fraction table. It's three eighths."
- **2.2 NEW**: "Remember why. Twelve point five percent is an eighth. And thirty-seven point five is three times twelve point five, so it's three eighths. This is why we memorize the table."
- **2.3 NEW**: "So first an eighth of a hundred twenty. We halve three times. Half of a hundred twenty is sixty, half again is thirty, and half again is fifteen."
- **2.4** BEFORE (old 1.8): "Twenty plus six plus one is twenty-seven. Choice number two is our answer."
  AFTER: "So three eighths of a hundred twenty is three times fifteen, forty-five. Choice number three is our answer."
- **3.1-3.5** (old slide 2, the swap examples): unchanged.
- **4.1** BEFORE: "Now our question. We start again from the givens. Twenty-five percent of eighteen percent is one multiplication, so we can read it in the easy order. A quarter of eighteen percent is four point five percent."
  AFTER: "Now our question. We start again from the givens. Twenty-five percent of thirty percent is one multiplication, so we can do it in whichever order is easier. Here, a quarter of thirty percent is easy. It's thirty divided by four, seven point five percent."
- **4.2** BEFORE: "So four point five percent of y is nine." → AFTER: "So seven point five percent of y is nine."
- **4.3** BEFORE: "They ask for thirteen point five percent. Thirteen point five is three times four point five. So it's three times nine, twenty-seven."
  AFTER: "They ask for thirty-seven point five percent. Five times seven is thirty-five, and five times a half is two and a half. So thirty-seven point five is five times seven point five."
- **4.4 NEW**: "The same y, with five times the percent, gives five times the amount. So it's five times nine, forty-five."
- **4.5** BEFORE: "We never even found y. Choice number two is our answer, and I'll see you in the next question."
  AFTER: "We never even found y. Choice number three is our answer, and I'll see you in the next question."

### Board (hand-written, each at its clause)

| Slide | Item | Text | Shown at | Col |
|---|---|---|---|---|
| 1 | e_1 | `25% = 1/4` | "Twenty-five percent is a quarter" | L |
| 1 | e_2 | `30% = 30/100 = 3/10` | "Thirty percent is" | L |
| 1 | e_3 | `1/4 · 3/10 · y = 9` | "So a quarter, times three" | L |
| 1 | e_4 | `3/40 y = 9` | "So three fortieths of y" | L |
| 1 | e_5 | `1/40 y = 9÷3 = 3` | "So one fortieth of y" | R |
| 1 | e_5b | `y = 40·3 = 120` | "so y is forty times three" | R |
| 1 | e_5c + cross | `(4) 120 = y, not the answer` | "not what they ask" / "That's choice number four" | R |
| 2 | So-far box | `y = 120` | first words | — |
| 2 | e_6 | `37.5% = 3/8` | "It's three eighths" | R |
| 2 | e_6b | `12.5% = 1/8, 37.5 = 3·12.5` | "Twelve point five percent is an eighth" | R |
| 2 | e_7 | `120÷2 = 60` | "Half of a hundred twenty is sixty" | R |
| 2 | e_7b | `60÷2 = 30` | "half again is thirty" | R |
| 2 | e_7c | `1/8 of 120: 30÷2 = 15` | "and half again is fifteen" | R |
| 2 | e_8 + tick (3) | `3/8 of 120 = 3·15 = 45` | "So three eighths of a hundred twenty" | R |
| 3 | e_9 … e_13 | unchanged swap examples | unchanged | — |
| 4 | So-far box | `x% of y = y% of x` (was on old slide 3) | first words | — |
| 4 | e_14 | `1/4 of 30% = 7.5%` | "Here, a quarter of thirty percent" | R |
| 4 | e_15 | `7.5% of y = 9` | "So seven point five percent of y" | R |
| 4 | e_16 | `37.5 = 5·7.5` | "So thirty-seven point five is five times" | R |
| 4 | e_17 + tick (3) | `5·9 = 45` | "So it's five times nine" | R |

The 1/8-table row appears only when she says it, and 45 only at "three times fifteen" / "five times nine" (no early result).
Spec length: 3.0 min (before: 2.9).

## 3. wp-053 part 1: the one-equation reminder. NOT applied, because wp-053 is recorded

wp-053 has a full take (21 Oct, 880 s), and its status is Send. Per condition 1, no recorded paragraph was changed. The exact
proposal is under "Proposals for recorded videos" below.

## 4. Summary page: "part = percent/100 × whole" is now box 1

`summary_pages/t23.json`: a new full-width **first** section, "The percent equation":
- "Every percent calculation is one equation: part = percent/100 × whole ("of" = times). The three versions are the same equation,
  with a different unknown."
- Table *Find / Example* (course numbers from wp-052 parts 3-4, none from the Hebrew):
  **the part:** 45% of 80 is what? 45/100 · 80 = 36 · **the percent:** 21 is what percent of 75? 21/75 · 100 = 28%
  (A is what percent of B: A/B × 100) · **the whole:** 30% of what is 63? 30/100 · x = 63, x = 210.
- In "Three ways to calculate", the old worked example of the equation (45% of 80; x% of 75 is 21) was replaced by one line,
  "**The percent equation** (box 1) works every time. Two faster ways:", so the same example isn't shown twice.
- Checks: one added (`21/75*100 == 28`); 34/34 pass. Built with `python3 summary_pages.py 23` → `~/Downloads/Topic-23-Summary-Page.html`
  (screenshot looked at: box 1 at the top, full width, fractions render; the other boxes are numbered 2-…).
- **Fixed on the way (not mine, but it blocked the build):** the percent-tree figure's layers in t23.json were `line, b1, b2`,
  while `PTREE` in `_ai_vis_t23.py` now names them `b10, b11, b20, b21`. The build stopped with `KeyError: 'b1'`; the layers are now
  `line, b10, b11, b20, b21` (the same finished tree as before).

## Proposals for recorded videos

### wp-053 (lesson 2, part 1; recorded 21 Oct): the one-equation reminder (teacher-approved item 3)

**Where:** a new short slide, "One equation", between the title slide (paragraphs 0-1: "Welcome back. … the whole often isn't even
given.") and "The change in percent" (which opens "But first, one rule we'll use all the time."). Lesson title slides can't hold
board items, so it needs its own slide. Recorded paragraphs stay as they are. It is one new paragraph block, so she records it as a
**patch take** (about 40 seconds), and Codex re-renders wp-053 with the new paragraph spliced in after paragraph 1 (the paragraph
numbers after it move by the number of new paragraphs).

**Exact new text (R29 reminder; the numbers are the course's own, from wp-052 parts 3-4; about 125 words ≈ 40-45 s):**
1. "A quick reminder from the last lesson. Every percent calculation is one equation. The part is equal to the percent over a
   hundred, times the whole."
2. "There are three versions, and they're all this same equation. Only the unknown changes."
3. "To find the part: forty-five percent of eighty is forty-five over a hundred, times eighty. That's thirty-six."
4. "To find the percent: twenty-one is what percent of seventy-five? Twenty-one over seventy-five, times a hundred. That's
   twenty-eight percent."
5. "To find the whole: thirty percent of what is sixty-three? Thirty over a hundred, times x, is sixty-three. Ten percent is a
   third of that, twenty-one, so x is two hundred ten."
6. "So, what percent is A of B? A divided by B, times a hundred."

**Board (hand-written, each at its clause):** `part = percent/100 × whole` at "The part is equal to"; `45/100 · 80 = 36` at
"forty-five over a hundred, times eighty"; `21/75 · 100 = 28%` at "Twenty-one over seventy-five"; `30/100 · x = 63` at "Thirty
over a hundred, times x", then `10% = 21, x = 210` at "Ten percent is a third"; `A/B × 100` at "A divided by B". Each example row
is labelled at its clause ("part ?", "percent ?", "whole ?") so the three unknowns are visible side by side.
Numbers checked: 45·80/100 = 36; 21/75 = 0.28; 63 ÷ 3 = 21, 21·10 = 210 and 30% of 210 = 63.
W18 note: "A" and "B" are capital letters next to "a" ("a percent", "a third"); on the prompter they show in italics. If she prefers,
say "the letter A".

---

## Checks

- **Status first:** see section 0.
- **Spec:** `python3 math_patches/_ai_vis_t23.py` (all topic-23 videos): no PROBLEMS; method-name vocabulary and carry-over checks pass.
- **Private builds only:** `OUT=scratchpad/heb23/test.html` and `AI_HANDWRITE=all OUT=scratchpad/heb23/test_hw.html`, both built from
  the final spec. (One earlier try failed inside `t33` while Codex was editing `_ai_vis_t33.py`; the retry passed. Nothing of mine.)
  No new topic-23 build warnings (the existing ones are t52 choice order, one t31 spoken label, and added_notes notes).
- **ai_check:** `SRC=<test> python3 ai_check.py solve-wp23-g062 solve-wp23-g064` → OK, OK (and OK on the handwriting build).
- **math_check 23:** typed: PROBLEMS 0 / WARNINGS 0 / layout 0 (99 slides, 767 items). `AI_HANDWRITE=all`: 0 / 0 / layout 0.
  The first handwriting run found 2 overlaps (g062 slide 1, g064 Method 2: six hand-written rows in the left column ran into
  the choices). I fixed them by moving rows to the right column and giving the 10% step its own slide, then re-checked.
- **Frames (handwriting build, looked at, every step):** `scratchpad/heb23/fr/<vid>/sheet_*.png`.
  g062 slide 1: e_1 to e_4 on the left, then 1/40 y, y = 120 and "(4) 120 = y, not the answer" on the right, each at its line, nothing
  over the choices. Slide 2: "So far: y = 120", then 37.5% = 3/8, the 1/8 row, 120÷2 = 60, 60÷2 = 30, 1/8 of 120: 30÷2 = 15, and
  3/8 of 120 = 3·15 = 45 last. Slide 4: the So-far box with the swap rule, then 1/4 of 30% = 7.5%, 7.5% of y = 9, 37.5 = 5·7.5, 5·9 = 45.
  g064 slide 3: 40% = 48, 40→48: ×1.2, drop a zero: 40→4, 30→3, both ÷10: 3:4 = 30:40 on the left; 4→48: ×12 and 3·12 = 36 kg on the
  right, in speaking order. Slide 4: the So-far box (factory 30%, 40% = 48 kg), then 10% = 48÷4 = 12 and 30% = 3·12 = 36. No early
  results, and no pen ✗ (the trap row says "not the answer").
  Minor, as before: the pen draws the dot in `1/4 · 3/10 · y` thin between the two fractions (same glyph as the old `1/4 · 9/50`).
- **Read-aloud (each changed paragraph, against the frames):** fixed while reading: "So the kilograms don't change" → "the kilograms
  column stays as it is, forty-eight and the question mark" (which kilograms?); "the step" → "across the row" (which step?); "the
  factory's three" → "The factory's row has the same step across"; "read it in the easy order" → "whichever order is easier. Here, a
  quarter of thirty percent is easy" (which order?); "y is forty fortieths" → "The whole y is forty fortieths". The halving row was
  split into three clause rows (V4: it showed 30 and 15 before she said them). After that, every "it/this/that" names its thing.
  Ready.
- **Prompter dump** (`reading_studio.prompter_display`): reads correctly after two wording fixes. "Three eighths is three times
  fifteen" displayed as `3/8 = 3 × 15`, which is false, so it now says "So three eighths of a hundred twenty is three times fifteen"
  (`3/8 of 120 is 3 × 15, 45`). "Five times the percent … is five times the amount" displayed with "=", so now: "The same y, with five
  times the percent, gives five times the amount." "five halves" (shown as 5/2) → "five times a half".

## Needs Claude (prompter display, not wrong maths; the converter's general behaviour)

- g064 3.3/3.5: small numbers stay words next to digits: "40 becomes four, and 30 becomes three", "From four to 48 is times 12".
  Consistent digits would read better ("4", "3"). It is the converter's general rule (single digits outside a calculation), so it's
  not patched here.
- g062 1.4: "So a quarter, times 3/10 × y = 9": "a quarter" in words next to 3/10 (the same pattern as the old "a quarter, times 9/50").
- g062 3.5 (unchanged line): "Four percent of 75" (the word "Four").
