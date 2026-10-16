# Teaching check (W20), batches A and B: unrecorded lessons of topics 15–20 and 30–31 (Claude, 16 Oct 2026)

**The teacher's request:** "let's add another test that Claude will do, to make sure I am actually teaching something when we get to some important concept, and not just answering the question. But only when it really adds."

The rule is now **W20** in `studio-build/real_exam/TEACHING_STYLE_GUIDE.md`. A note was added to `reviews/README-for-Codex.md`: Claude runs the check after fixing each Codex batch.

## Result

- **71 videos checked.** That is every video on `video_status.py --list record` in topics 15–20 (21) and 30–31 (50) at the start. All scripts were read in full.
- **About 130 concept moments looked at.**
- **6 teaching additions, plus 1 short reminder,** in 7 videos.
  - The other 64 videos were judged "already taught" or "not needed".
  - Typical reasons: the idea is taught well in the video or in the camera lesson; the fact is trivial; the idea is a reminder of an earlier topic, where a short reminder is the right length (R29).
- **0 skipped.** All 7 changed videos were still unrecorded when the job started, before each edit, and before publishing.
  - solve-q-579 was recorded by her during the job. It was not touched; its verdict was "not needed".

### The changes

| Video | Concept | What was added | Why |
|---|---|---|---|
| divisibility-3 (camera, part 3) | Why the digit sum works for 3 and 9 | New ¶5.4: "Why does the digit sum work? Take forty-seven, which is four tens and seven. Every ten is nine plus one. So forty-seven is four nines, plus four, plus seven. The nines divide by nine, and by three too, so only four plus seven decides what's left. A hundred is ninety-nine plus one, so bigger numbers work the same way." Board: 47 = 4·10 + 7, 10 = 9 + 1, 47 = 4·9 + 4 + 7, "The nines drop out → only the digit sum decides", 100 = 99 + 1. | 4 and 8 had their why, but 3 and 9 (the most used signs, 36 real divisibility questions) had none. One why explains both the sign and the remainder trick, and why it fails for 4 or 7. |
| number-line-3 (camera, part 3) | Strong on strong: why it works | New ¶3.3: "Why does it work? We change one factor at a time. Four times six is bigger than three times six, because four beats three. And three times six is bigger than three times five, because six beats five. So four times six beats three times five, one step at a time." Board: 4·6 > 3·6 > 3·5. | Her own slogan was given as a rule with no reason. The one-swap-at-a-time reason also shows why "one win each" decides nothing. |
| geo-001-4 (camera, part 4) | The Z and the U: why | The Z ¶2.2 gained "Why are they equal? Both corners of the Z are sharp, so both are small angles. And we just saw that all the small angles are equal. The Z just helps us find the matching pair fast." The U ¶3.2 gained "Why? Inside a U, one angle is a small angle and the other is a large one, and small plus large is a hundred eighty." Board key lines: "Z: both corners are small angles → equal" and "U: one small + one large = 180°". | The Z and U were new shapes to memorise. Now they come straight from the two rules taught one slide earlier. They are the signature tool for every parallel-lines question. |
| solve-q-r26-t30-02 | The overlap rule as a reusable idea | New slide 3, "The overlap rule, in general": "When two pieces cover a whole and overlap, the two pieces together are the whole, plus the overlap once more. Why? The overlap belongs to both pieces, so it's counted twice. For example, strips of six and seven cover a line of ten… the overlap is … three. So when you see two pieces that overlap, think: the whole, plus the overlap." Board: a key line, a clean picture (strips of 6 and 7 over a line of 10, with the overlap tinted), and 6 + 7 = 13, 13 − 10 = 3. | It was used once, for these segments only. The same rule returns in g006 (angles), shaded areas, and overlapping groups (topic 24). |
| solve-geo30-g006 (reminder) | The overlap rule, with angles | ¶5.2 now opens with "It's the overlap rule from the segments question again. The pieces together are the whole turn, plus the overlap once more." | It links the insight to the rule just taught (R29: a short reminder). |
| solve-geo31-g025 | How to spot a Pythagorean triple | New slide 4, "Spotting a triple": "Look for one number that divides both sides you know. Take it out, and see what's left. If the legs leave three and four, or a leg and the hypotenuse leave five and thirteen, it's a triple. For example, legs of twenty-four and thirty-two… three and four. So the hypotenuse is five times eight, which is forty." Board: the key line, 24 = 8·3, 32 = 8·4, and hypotenuse = 8·5 = 40. | The script said "these numbers jump out" but never said how. The move (take out the common factor) is the reusable exam skill for every triple question. |
| solve-geo31-g018 | Lengths × k → area × k² | New slide 4, "Lengths and area": "This idea works for every shape… When every length is multiplied by some number, the area is multiplied by that number squared. Why? Area is a length times a length, so the number comes in twice. For example, a square with side three has an area of nine. Double the side to six, and the area is thirty-six, four times as much. So when you see the same shape in two sizes, think: the side ratio, squared." Board: "Lengths × k → area × k²", grids of a 3×3 and a 6×6 square, and "Side ×2, area 9 → 36, ×4". | It was used only as "half the side, a quarter of the area" for this triangle. It is on the real exam (2024 winter q1-03, "9 times the area"; 2023 winter q2-12; "16 times as much"), with circles and similar shapes. |

Other edits:
- In t30-02 and g025, the goodbye moved to the new last slide. The trap paragraph of t30-02 and the "triples saved all of that" paragraph of g025 are otherwise unchanged.
- g018: the goodbye moved from ¶3.2 to the new slide.
- Display registry: the number-line-3 key 3.4 moved to 3.5. No other key moved.

## Per video

R = a reminder, enough as it is. T = taught well already. N = not needed (trivial, rare or off-exam). ADD = changed.

### Topic 15
- **divisibility (part 1):** signs for 2, 5, 10, 3, 9, 4, 8: T, with the why for 4 and 8. The why for 3 and 9: ADD, in part 3 where it does double duty.
- **divisibility-2:** build a divisor from parts with no common factor: T (the trap 2·6 with 18). The 11 rule: N (rare, rule only, why off-exam). "Why the signs" (a quarter of a group): T.
- **divisibility-3:** remainder < divisor: T. The 5 ÷ 8 trap (shop story): T. Biggest remainder = divisor − 1: T. Digit sum → remainder: T as a rule; ADD the why.
- **divisibility-4:** 4k + 3 with its why: T. Changing the divisor, with why and counter-example: T.

### Topic 16
- **whole-numbers:** sign rules: T. Count the minuses, with its why: T. An even power is never negative: N (taught in topic 8). Mixed-sign sums: T. Surely-positive pieces: T.
- **solve-q-r26-t16-04:** three odd numbers in a row contain a multiple of 3: T (Method 2 states it generally, with the why and a second case). The first case is only a candidate: T.

### Topic 17
- **number-line:** four ranges and why: T. Borders: T. Mirror image: T.
- **number-line-2:** × / ÷ by more or less than 1: T. ÷ a fraction = × its reciprocal: R (topic 2). Hierarchy: T. Exceptional powers: T.
- **number-line-3:** same operation keeps the order (with the negative non-example): T. Strong on strong: T as a rule; ADD the why.

### Topic 18
- **digit-puzzles:** AB = 10A + B: T. Same and different letters, leading digit: T.
- **digit-puzzles-2:** the four steps: T. The ones column first ("nothing carries in"): T in q-512 right after. A puzzle in words: T.

### Topic 19
- **new-operation:** a definition, then follow it exactly (the heart trap): T. The same template, input in every slot: T.
- **new-operation-2:** brackets on every input (the −2² trap): T. Inside first, can't join two diamonds (the squares analogy): T. Inside out: T.
- **new-operation-3:** no definition → test the choices: T. Order matters; one counter-example vs letters; no equal numbers: T.
- **operation-patterns:** undo in reverse order (shoes and socks, with the trap): T.
- **solve-q-549:** one counter-example proves "not always": T. (5x)² = 25x²: R (topic 8). Opposites have the same square: T.

### Topic 20
- **algebraic-understanding:** plug in only allowed numbers; a fraction breaks "a² > a": T. a² − b² = (a + b)(a − b): R (topic 4). An integer below 5 is at most 4: T.
- **solve-q-579** (recorded during the job, not touched): multiplying a triple keeps it: R (geo-024). The longest side and two sides > the third: R (31). → N.
- **r26-t20-counting:** b − a + 1, and the strictly-between and one-end cases: T. Pigeonhole: T. Same remainder → the difference divides: T (the fives cancel).
- **solve-q-r26-t20-03:** steps vs numbers (+1): T at the trap. Half of the numbers are odd: T.
- **solve-q-r26-t20-04:** "to be sure" = the worst luck: T. Only the number of colours matters: T.

### Topic 30
- **geo-001:** one straight line through two points: T. Count the gaps, not the points: T. 360 around a point: T.
- **geo-001-2:** 90 only if marked, given or calculated: T. Adjacent angles add to 180, with the non-example: T. Vertical angles, with the why: T.
- **geo-001-3:** the bisector: T. Naming angles: N. Parallel distance: T. Small = small, large = large, small + large = 180, with the why: T. "Moved down": T.
- **geo-001-4:** Z and U: ADD the whys. Parallel or not (three rules, not to scale): T.
- **solve-geo30-g002:** small angles equal, the right angle split: R.
- **solve-q-r26-t30-01:** two perpendiculars → parallel, with the why: T.
- **solve-q-r26-t30-02:** the overlap rule: ADD the general slide.
- **geo-004:** what makes questions harder: T (a list, taught in the questions).
- **solve-geo30-g005:** one pair of parallels at a time: T. The last-digit shortcut: T (stated generally, from topic 1).
- **solve-geo30-g006:** an anchor (180 or 360): T. Plugging in for letters, with the why: T. Overlapping angles: ADD a short reminder of the overlap rule.
- **solve-geo30-g007:** an auxiliary line through the bend: T. The zig-zag rule, with its why: T.
- **solve-q-r26-t30-03:** the zig-zag rule with two bends: R. Helper lines: R.

### Topic 31
- **geo-009:** median, altitude and bisector, and what each one does not promise: T. Altitude outside: T.
- **geo-009-2:** angle sum, with the proof: T. At most one obtuse angle: T. Exterior angle, with the why and both ways: T.
- **geo-009-3:** the biggest side is opposite the biggest angle, with the why: T. Triangle inequality (two pictures): T. Between the difference and the sum: T. The count shortcut 2·short − 1: N (optional; counting the whole numbers is also given).
- **solve-geo31-g010:** vertical angles, then the angle sum: R.
- **solve-geo31-g011:** write everything with one letter and hope it cancels: T. Exterior angle: R.
- **solve-geo31-g012:** strictly between the difference and the sum: R.
- **geo-013:** equal base angles, why (the fold), and backwards: T. The symmetry line does three jobs: T. Equilateral = 60, with the why: T. The hypotenuse is opposite the square: T. The median to the hypotenuse: T (rare).
- **solve-geo31-g014:** the bisector is also a median (symmetry): R.
- **solve-geo31-g015:** the base angles of two isosceles triangles: R.
- **geo-016:** area as unit squares, a triangle as half a rectangle (why), any side with its own altitude, altitude outside: T.
- **solve-geo31-g017:** equal heights between parallel lines → the ratio of the bases: T (stated generally in ¶1.4 and the trap ¶1.7).
- **solve-q-r26-t31-01:** an altitude → find the area two ways: T ("an altitude always comes with an area", same triangle same area, leg·leg = hyp·altitude).
- **solve-q-r26-t31-02:** two sides with no angle → the biggest area at 90°: T (stated generally).
- **geo-018-after:** a median halves the area; same base and same height: T.
- **geo-019:** the theorem, the square root at first use, and only in a right triangle: T.
- **solve-geo31-g020:** rule out with the longest side and the triangle inequality first: T.
- **solve-geo31-g021:** a root is a fine answer: T.
- **solve-geo31-g022:** for a leg, subtract the squares: T.
- **solve-q-r26-t31-03:** compare c² with a² + b² (why: the angle opens): T.
- **geo-023:** the proof: N (optional by design).
- **geo-024:** triples, multiples with the why (k²), position matching: T.
- **solve-geo31-g025:** spotting a triple: ADD. The square inside a root: T.
- **geo-026:** gold triangle from the equilateral, the ratio, dividing by √3 with the why. The 30-30-120 triangle as two gold halves (her example) is taught fully: "Nothing new to memorize, just cut it in half", with numbers, the area, and where it appears (a rhombus with 120°): T.
- **solve-geo31-g027:** the side ratio and a Pythagoras check: R.
- **geo-017-after:** the equilateral area, derived two ways, with the mnemonic plus the formula: T.
- **solve-geo31-g018:** lengths × k → area × k²: ADD.
- **geo-027-after:** silver triangle (the sandwich), the ratio with the why, a square's diagonal: T.
- **solve-geo31-g028:** "30 → gold, 45 → silver" (recognition): T.
- **solve-geo31-g031:** exterior angle, angle sum, plugging in: R/T.
- **solve-geo31-g032:** the longest side is opposite the biggest angle: R.
- **solve-geo31-g033:** only one choice can be right in a range: T. Bounds: T.
- **solve-geo31-g034:** the fold argument for isosceles: T.
- **solve-geo31-g035:** triples, legs as base and height: R.
- **solve-geo31-g036:** gold → silver: R.
- **solve-geo31-g037:** shaded = what minus what (stated generally): T.
- **solve-geo31-g038:** same height → the area ratio is the base ratio (stated generally, with a picture): T.
- **solve-geo31-g039:** shared sides cancel; the sign estimate: T.
- **solve-geo31-g040:** from 3b = 10a to a/b: T (both ways shown).

Her four examples are covered as follows:
- The 30-30-120 triangle: taught in geo-026.
- "Same remainder → take it away": taught in r26-t15-remainder-tools (recorded) and r26-t20-counting ¶3.4.
- Equal angles in an isosceles triangle: taught in geo-013, with the fold.
- "Multiplying by a negative flips the inequality": taught in r26-t17-reading-the-line (recorded). number-line-2 points to it.

## Checks (final build)
- **Spec regeneration** (13–20, 30–33, 51) equals `ai_scripts`, with no PROBLEMS. 7 scripts changed, the 7 above.
- **`ai_check`:** no new fails. The only fail is the old solve-q-r26-t22-02 one.
- **`math_check 15 16 17 18 19 20 30 31 32`:** 0 problems, 0 warnings, layout 0. The same with `AI_HANDWRITE=all`.
- **`svgcheck`:** 54,848 steps, 0 broken.
- **Numbers:**
  - 47 = 4·9 + 4 + 7;
  - 4·6 > 3·6 > 3·5 (24 > 18 > 15);
  - 6 + 7 − 10 = 3;
  - 24² + 32² = 40² (576 + 1024 = 1600);
  - 3² = 9 → 6² = 36.
- **Timing simulation** (the studio's anTimeline on estimated manifests at her pace, before and after): with the guard ON (the real behaviour), 0 new drops. number-line-3 even lost an old one.
  - With the guard OFF there are 3 new dropped points on handwritten lines still being written. This is the same kind as the existing g006 and number-line-3 drops, and the guard handles them.
- **Frames:** every step of every slide of the 7 videos was rendered from the real build (198 frames) and looked at.
  - Nothing overlaps.
  - The U layers stay on their figure (ANCH).
  - The new slides show a clean picture under the stem.
- **W19 aid:** one new dense sentence (t30-02) was split.
- **Builds:** the real build; `export_student` (1,019 videos, 2,357 questions, 135 cards); the Reading Studio rebuilt with all 13 topics (323 videos, 3,765 paragraphs, +5).
- **`video_status.py`:** Record 183 · Re-read 39 · Send 75 · Done 25 · Check 1.
  - The only change since the start is solve-q-579, which she recorded (Record → Send).
  - Re-read is unchanged.

## Ready to record
All 7 changed videos are unrecorded and ready: divisibility-3, number-line-3, geo-001-4, solve-q-r26-t30-02, solve-geo30-g006, solve-geo31-g025, solve-geo31-g018. **She must reload the Reading Studio before recording them.**

New slides: t30-02, g025 and g018 each gained one short last slide.
