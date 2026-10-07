# Topic 10 — Exponents & Roots (Techniques): changes

Patch: `math_patches/t10.py`. Check: `python3 math_check.py 10` shows 0 problems, 0 warnings and 0 layout problems.

## Summary
- Questions: 44 rewritten, 16 added (5 guided with solution videos and 11 practice), 10 removed.
  The topic had 54 questions (5 guided and 49 practice). It now has 60 (10 guided and 50 practice).
- Main lesson "Exponents & Roots — Techniques": 6 slides changed, 1 slide added ("Try the choices").
- New lesson video: "Exponent Traps — Sums & Comparisons" (8 slides, about 5 minutes).
- New solution videos: Questions 6 to 10.
- Existing solution videos: Q2 (2 slides) and Q5 (1 slide) changed. The sidebar of Q1 to Q5 now lists Questions 1 to 10.
- New memory card: "Exponent and root techniques" (this topic had no card before).
- The learn section is renamed from "Five guided questions" to "Ten guided questions".

## 1. Wrong or misleading teaching (fixed)
- **Q2 video, slide 2:** deleted "the exam often places a number like that in its own position". This is not a real pattern.
- **Lesson slide 9 (root equations):** the old example √(x+7) = x − 1 was never solved, because its roots are not nice numbers. It is now √(x+2) = x, solved in full:
  - x ≥ 0
  - square: x² − x − 2 = 0, so (x − 2)(x + 1) = 0
  - check both answers in the original equation: −1 is a fake solution and is thrown out, so x = 2 only
  - the teacher warns that "2 or −1" is the trap choice

## 2. Methods added
In the main lesson:
- **Slide 5 (negative exponents):** new example 2⁻⁶ ÷ 2⁻⁴ = 2⁻². It shows "minus minus is plus" before Q1 needs it.
- **Slide 8 (power equations):** one line added. You can also put each choice into the exponent.
- **New slide 10 "Try the choices":** the plug-in method for root and power equations. It also throws out fake solutions.
- **Recap:** the root-equation line now reads "square, solve, check — or try the choices". The recap now says "Six questions next."

In the **Q5 video**, the teacher adds a warning: "If x ≠ 0 is NOT given, don't divide by x — factor, and keep both answers." This links to T9 q-247.

The **new lesson video "Exponent Traps — Sums & Comparisons"** comes after Question 6. It covers:
1. Sums of equal powers: 2¹⁰ + 2¹⁰ = 2¹¹, 3ˣ + 3ˣ + 3ˣ = 3ˣ⁺¹, and the trap 2ˣ + 2ˣ ≠ 4ˣ (checked with x = 3).
2. Common factor of powers: 2ˣ⁺² − 2ˣ = 3·2ˣ and 2ˣ⁺³ + 2ˣ = 9·2ˣ (take out the smallest power).
3. Same exponent: aˣ·bˣ = (ab)ˣ, for example 2ˣ·5ˣ = 10ˣ and 6ˣ ÷ 3ˣ = 2ˣ. q-281 uses this.
4. Comparing powers by making the exponents equal: 2³⁰ = 8¹⁰ < 9¹⁰ = 3²⁰.
5. Bases between 0 and 1: the order flips, so (1/2)ˣ > (1/2)ʸ means x < y.
6. aˣ = bˣ with different positive bases means the exponent is 0 (2ˣ = 3ˣ gives x = 0).
7. Recap.

**New guided questions**, each with a solution video:

| # | id | Question | Answer | Solution video |
|---|---|---|---|---|
| Q6 | q-r26-t10-01 | √(2x+3) = x | 3; "−1 or 3" is the trap | 2 methods: square and check, or try the choices |
| Q7 | q-r26-t10-02 | 2¹⁰ + 2¹⁰ + 2¹⁰ + 2¹⁰ | 2¹² | also checks the rule with small numbers |
| Q8 | q-r26-t10-03 | 3ˣ⁺² − 3ˣ = 72 | x = 2 | 2 methods: common factor, or try the choices |
| Q9 | q-r26-t10-04 | order of 2⁴⁵, 3³⁰, 5¹⁵ | c < a < b | makes the exponents equal |
| Q10 | q-r26-t10-05 | (1/3)ˣ > 1/27 | x < 3 | base below 1, with a check using numbers |

**Strong-student tricks, taught explicitly:**
- Try the choices: lesson slide 10, and the solution videos for Q6 and Q8.
- Choose easy values:
  - the q-268 solution uses x = 2
  - the q-270 solution shows what to do when two choices match (a = 2, then a = 3)
  - the memory card has a tip for this
- Check with small numbers: the Q7 video.

**Memory card "Exponent and root techniques":**
- 12 rows (situation, method, example)
- Tips: 2ˣ + 2ˣ ≠ 4ˣ; "pair the families" (the Q1 method 2 shortcut, which now has a name); try the choices; "don't divide by x"; choose easy values.

## 3. Text
- **Draw notes:** every ":" used for division is now "÷". This covers lesson slides 2 and 3 and the Q2 video, slide 3.
- **Written solutions:** all of them are in TeX now, with no ":" for division. They show every number and follow the lesson's method. Where it helps, a faster method is added after it.
- **Conditions:**
  - q-252 and q-286 now show the condition and the equation stacked, using `cases`.
  - q-278 "0 < a, c" is now "a > 0 and c > 0".
  - q-268, q-270 and q-280 now read "x > 0" (or "a > 0").
  - q-276: the needless "0 < x" is removed.
- **Rewording:**
  - q-287: "Which of the following is correct?" Its solution now uses √20 = 2√5, so 3√5 = √45 < 7.
  - q-284: clearer stem. The solution now shows why choices 1 and 3 fail (a = 3, b = 3/2).
  - q-269: the stem now asks "which could be the value of x".
  - q-279: the stem is now just the expression.
- **Extra set t10-2:**
  - "Evaluate …" and "Solve …" stems are now NITE style ("… = ?").
  - The choices are in TeX.
  - The word-only solutions now show the numbers.
  - In t10-2-6, the choices "The first/second power" are now $2^{12}$ and $4^5$.

## 4. Figures
None in this topic.

## 5. Practice
**Removed:**
- alg-extra-unit-t10-3-1 to 3-7, the same 7 templates as set t10-2
- q-263 and q-283, which repeat q-262 (plain "simplify √n")
- q-277 (x = y = 8, trivial)

**Added (exam level):**

| id | Question | Answer |
|---|---|---|
| q-r26-t10-06 | 3ˣ + 3ˣ + 3ˣ | 3ˣ⁺¹ |
| q-r26-t10-07 | 0.2ˣ = 25 | x = −2 |
| q-r26-t10-08 | 4ˣ·25ˣ = 10⁶ | x = 3 |
| q-r26-t10-09 | √(x+12) = x | 4 (−3 is a fake solution) |
| q-r26-t10-10 | x√3 = √(3x) | 0 or 1 ("don't divide by x") |
| q-r26-t10-11 | (5ⁿ⁺¹ − 5ⁿ) ÷ 4 | 5ⁿ |
| q-r26-t10-12 | 2ˣ + 2ˣ = 4ˣ | x = 1 (trap choice: "every x") |
| q-r26-t10-13 | 5ˣ⁻² = 7ˣ⁻² | x = 2 |
| q-r26-t10-14 | (1/2)²ˣ⁻¹ < 1/8 | x > 2 |
| q-r26-t10-15 | greatest of 2⁴⁰, 3³⁰, 4²⁰, 5²⁰ | 3³⁰ |
| q-r26-t10-16 | 3²⁰ + 3²⁰ + 3²⁰ = 9ⁿ | n = 10.5 |

Items 06 to 08 are in "Expressions and equations". Items 09 to 16 are in "Mixed practice".

Both practice sections are now ordered from easy to hard. q-284 and q-287 come last.

## Not done / for the teacher to decide
- **Conjugates** (1/(√2 − 1) = √2 + 1) and **(√a + √b)²** are not added here. The T9 review lists both as T9 content, so the T9 patch should teach them. q-287 no longer needs (√a + √b)².
- **T9 q-247 and T9 practice-5** use "square both sides", which is only taught here. The T9 review suggests moving them to T10. This patch does not move them, because they belong to the T9 patch. The T9 patch can either teach the step or move them. If they move, T10's slide 9 and slide 10 teach the method.
- **Factoring x² − x − 2** in slide 9 and Q6 uses "two numbers that multiply to … and add to …". PLAN.md says trinomial factoring is not taught anywhere in the course. The "Try the choices" method (slide 10) avoids it. Check this once the T4/T5 patches add quadratics.
- **Fractional exponents:** alg-extra-unit-t10-2-2 (64^(2/3)) and q-285 (⁴√(5⁶)) need ⁿ√(aᵐ) = a^(m/n). The T9 patch is expected to teach this.
- **Negative bases:** (−2)⁴ vs −2⁴ are not revisited here, because the T8 card covers them.
- **Recording length:** the main lesson is now about 8.6 minutes (it was 6.9). The new lesson is about 4.9 minutes.

## Pass 2 (2026-09-27, teacher-approved remove/restore plan + summary lesson)

**Removed (0 real and 0 original questions of these types)**
- Video `r26-t10-power-traps`: slides "Compare powers", "Bases between 0 and 1" and "When is aˣ = bˣ?", their
  sidebar labels and their three Recap lines. The title slide no longer mentions comparing powers or bases smaller
  than one, and the video is renamed "Exponent Traps — Sums of Powers". The Recap now says "Two questions next."
- Guided q-r26-t10-04 (order of $2^{45}, 3^{30}, 5^{15}$) and q-r26-t10-05 ($\left(\frac13\right)^x>\frac1{27}$) with
  their solution videos. The section is now "Eight guided questions"; the question sidebars run Q1–Q8.
- Practice q-r26-t10-13, -14, -15.
- Card `mem-r26-t10-techniques`: rows "Comparing powers", "Base between 0 and 1" and "aˣ = bˣ, a ≠ b (positive)".

**Restored (original course)**
- q-263 ($\sqrt{63}$), q-283 ($\sqrt{98}$), q-277 ($x=y=8$), and alg-extra-unit-t10-3-1 … -3-7 (7 questions). They are back
  in their practice sections, placed by difficulty. Text is in TeX and the solutions show the numbers (keys unchanged).
- alg-extra-unit-t10-2-6: the original choices "They are equal / It cannot be determined from the information given. /
  The first power / The second power" (key: the first power).
- Lesson "Exponents & Roots — Techniques", slide 9 "Root equations": the original slide with $\sqrt{x+7}=x-1$ and the
  board line "x − 1 ≥ 0 → x ≥ 1" is back. The fully solved $\sqrt{x+2}=x$ follows it as a new slide,
  "Root equations: an example", before "Try the choices".

**New: summary lesson** `r26-t10-summary` "Exponents & Roots — Summary" (about 2.6 min), right after the memory card and
before the practice sections (both practice sections follow one after the other, so there is one summary). Slides:
Summary · Dividing roots · Same prime base · Adding roots · Power equations · Root equations · Don't divide by x ·
Sums of powers · Common factor · Before you practice.


## 2026-10-04 question = lesson example fixed
- q-262 was √18, worked on the board in "powers-techniques" slide 6 -> √28 = 2√7 (choice 2).
- q-r26-t10-06 was 3^x + 3^x + 3^x of "r26-t10-power-traps" slide 2 -> five copies of 5^x = 5^(x+1) (choice 3).
- q-r26-t10-09 was √(x + 12) = x of "r26-t09-summary" slide 10 -> √(x + 30) = x, x = 6 (choice 2); −5 is the fake solution.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). Nothing in topic 10 is recorded.
- **Exponents & Roots — Techniques** (9.0 → 2.5 min, Hebrew lesson ≈ 4.6). Kept the Hebrew lesson's two slides: dividing roots, a number over a root (+ "Now the questions. Each one teaches one more technique."). Cut: same prime base and negative exponents → Q1 (q-248); adding roots by splitting and by a common factor → Q2 (q-249); power equations → Q3 (q-250), trying the choices for them → Q8; root equations, the √(x + 2) = x example and "try the choices" → Q4 and Q6 (near-twin √(2x + 3) = x); recap.
  - Q3 title line "You know the method — equal bases" → "The method: equal bases — then equal exponents."
  - Moved into Q3 (new short slide "When it works"): "Equal bases → equal exponents: for a positive base that is not 1" + one line. 1.3 → 1.5 min.
- **Exponent Traps — Sums of Powers** (2.7 → 0.9 min). Cut "Sums of equal powers" → Q7, "Common factor" → Q8, recap. Kept "Same exponent" (aᵡbᵡ = (ab)ᵡ; no question video here). Title slide names what the questions teach.

## 2026-10-06 pen or click
Function `pen_or_click` (runs last, after `cut_repeats`). The teacher's approved split: in lessons the content appears by click and the pen only marks; in solution videos the setup and mechanical lines appear by click, and only the key step (plus the marks on the choices) is written by hand. Where a hand-written line comes before click lines, the board leaves an empty row for it. Spoken lines, math, questions and slide count are unchanged. No topic 10 video is recorded. Topic total: 64 pen cues -> 15 by hand, 40 by click, 9 split (24 pen cues left).
- powers-techniques (8 -> 0 by hand, 6 clicks, 2 split). Every written line is a click. Split: cross out √3 top and bottom by hand (both slides). Slide 3 now has 9 lines, so it is smaller and closer; the two shortcut lines no longer repeat the fraction.
- solve-q-248 (8 -> 3 by hand, 5 clicks). By hand: 9⁶ = (3²)⁶ = 3¹² (method 1), (9⁶ / 3⁸) · (8/4)⁻² (method 2), circle. Clicks: 8⁻² and 4⁻² in base 2, the two exponent subtractions, = 3⁴ · 2⁻².
- solve-q-249 (9 -> 3 by hand, 5 clicks, 1 split). By hand: √27 = √9 · √3 = 3√3 (method 1), bottom = √3(√16 − √4) = 2√3 (method 2), circle. Clicks: top, √48 and √12, bottom, top = 2√27, the last division. Split: 6√3 / 2√3 = 3 click + circle by hand.
- solve-q-250 (5 -> 1 by hand, 3 clicks, 1 split). By hand: 4x = −12 + 6x (same base -> equal exponents). Clicks: 4^(2x) = 2^(4x), (1/8)^(4−2x) = 2^(−12+6x) (written in full, not "under"), the check (two lines). Split: 12 = 2x -> x = 6 click + circle.
- solve-q-251 (4 -> 1 by hand, 2 clicks, 1 split). By hand: (√(x − 7))² = 3². Clicks: x − 7 = 9, x = 16. Split: check click + circle.
- solve-q-252 (7 -> 1 by hand, 5 clicks, 1 split). By hand: (x√5)² = x² · 5. Clicks: (5√x)² = 25x; "5x² = 25x -> x² = 5x" (one arrow line, the second part on the next click); check; the "no x ≠ 0?" chain. Split: x = 5 click + circle. Lines are smaller (32) so the question still fits.
- solve-q-r26-t10-01 (9 -> 2 by hand, 4 clicks, 3 split). By hand: x ≥ 0, circle. Clicks: the squaring, the factoring, the two checks. Split (method 2): each try is a click line "(1) x = −1: √1 = 1 ≠ −1" etc.; crossing out / circling the choices by hand.
- solve-q-r26-t10-02 (4 -> 2 by hand, 2 clicks). By hand: = 4 · 2¹⁰, circle. Clicks: 4 = 2² -> 2¹², the small check.
- solve-q-r26-t10-03 (5 -> 2 by hand, 3 clicks). By hand: 3ˣ(9 − 1) = 72 -> 8 · 3ˣ = 72, circle. Clicks: 3ˣ⁺² = 9 · 3ˣ, 3ˣ = 9 -> x = 2, the x = 2 check.
- r26-t10-summary (5 -> 0 by hand, 5 clicks).

## 2026-10-06 renumber pass
Goal: the English topic 10 must not look like the Hebrew course. Every idea, trap, level and method stays the same; only the numbers, letters and names change.
Code: `renumber(M)` runs last in `apply`, after `pen_or_click`, so the click items and the hand cues are rewritten together. There is a `RECORDED` set, which is empty: no topic 10 video is in ~/Documents/Course.recordings.
Counts: 5 guided questions renumbered (and their videos rewritten), 34 Hebrew practice questions renumbered (q-262 already had new numbers from 2026-10-04 and was kept), and 3 Hebrew lesson examples renumbered. 1 English practice item was also changed (q-r26-t10-11). Practice: 57 → 40.

**Guided questions + solution videos** (board, spoken lines, hand cues and circles all use the new numbers; the methods are unchanged)
| Item | Old (Hebrew) | New | Answer | Key |
|---|---|---|---|---|
| q-248 (Q1) | (9⁶·8⁻²)/(3⁸·4⁻²) = 3⁴·2⁻² | (4⁵·27⁻²)/(2⁷·9⁻²) | 2³·3⁻²; trap 2³/3¹⁰ (−6 + (−4)) | 1 → 2 |
| q-249 (Q2) | (√27+√27)/(√48−√12) = 3 | (√50+√50)/(√32−√8) | 5 | 3 → 4 |
| q-250 (Q3) | 4^(2x) = (1/8)^(4−2x), x = 6 | 9^(3x) = (1/27)^(2−3x) | x = 2; trap 2/5 (forgot the minus of the fraction) | 3 → 4 |
| q-251 (Q4) | √(x−7) = 3, x = 16 | √(x−6) = 5 | 31; traps 11, 25, 19 | 4 → 3 |
| q-252 (Q5) | x√5 = 5√x, x ≠ 0 → 5 | x√6 = 6√x, x ≠ 0 | 6; "no x ≠ 0 → 0 or 6" | 2 → 4 |
Methods kept: Q1 smallest prime base + pair the families; Q2 split + common factor; Q3 equal bases + plug back in (9⁶ = 3¹² = 27⁴); Q4 square + check; Q5 square, divide by x only because x ≠ 0, factor otherwise. One new spoken line each in Q1 and Q3 names the trap choice.

**Lesson "Exponents & Roots — Techniques"** (Hebrew examples): √48/√3 = 4 → √98/√2 = 7 (both ways); 6/√3 = 2√3 → 10/√2 = 5√2; 20/√5 = 4√5 → 18/√6 = 3√6 ("nine times two or three times six"). 6/√3 is also the topic 9 lesson's example. Memory card: example 6/√3 → 10/√2; the "pair the families" tip now shows the new Q1; the tip x² = 5x is now x² = 6x.

**Practice (Hebrew study guide)**
| Item | Old | New | Answer | Key |
|---|---|---|---|---|
| q-253 | 3⁵/15² | 2⁷/6² | 32/9 (trap 32/3) | 3 → 4 |
| q-254 | 3²·9³ | 2³·4⁴ | 2¹¹ (trap 2⁷) | 1 → 3 |
| q-255 | (16³·8²)/(4⁴·2⁶) | (9⁴·27²)/(81·3⁶) | 3⁴ | 1 → 1 |
| q-256 | 7² = 7^(x+6) | 5³ = 5^(x+8) | −5 | 1 → 1 |
| q-257 | 2⁸ = 4^(x−1) | 3¹⁰ = 9^(x−2) | 7 (traps 12, 6, 5) | 4 → 2 |
| q-258 | 8⁵ = 4⁴·2ˣ | 27⁴ = 9³·3ˣ | 6 | 4 → 3 |
| q-259 | (1/5)³ = 5^(x−7) | (1/3)⁴ = 3^(x−6) | 2 (trap 10) | 1 → 4 |
| q-260 | 10/√5 | 21/√3 | 7√3 | 1 → 2 |
| q-261 | 5√3/√15 | 7√2/√14 | √7 | 2 → 4 |
| q-262 | √18 | √28 (kept from 2026-10-04) | 2√7 | 2 |
| q-263 | √63 (the reverse of the T9 lesson's 3√7 = √63) | √45 | 3√5 (trap 9√5) | 4 → 4 |
| q-264 | √3 + √27 | √2 + √32 | 5√2 | 2 → 3 |
| q-265 | √80 − √20 (the T9 summary has √80 + √20) | √75 − √12 | 3√3 (trap √63) | 3 → 4 |
| q-266 | √(2x+9) = 5 | √(3x+1) = 4 | 5 (trap 1) | 1 → 3 |
| q-267 | √(4x+6) = √70 | √(5x−4) = √66 | 14 | 3 → 1 |
| q-268 | x>0, x^(x+3)·x^(−x−2) | y>0, y^(y+4)·y^(−y−5) | 1/y (check y = 2) | 2 → 2 |
| q-269 | √(x²) = 5 | √(x²) = 7 | −7 | 3 → 4 |
| q-270 | a^(a+2)/a² (a = 2 ties) | b^(b+3)/b³; choices bᵇ, (b+3)ᵇ, 2b, b^(b+6) (b = 2 ties bᵇ and 2b → try b = 3) | bᵇ | 3 → 1 |
| q-271 | 16ˣ·4ˣ·2ˣ | 27ˣ·9ˣ·3ˣ | 3^(6x) | 3 → 2 |
| q-272 | (9³·3⁴)/81 | (8³·2⁵)/32 | 2⁹ | 3 → 4 |
| q-273 | 36⁴ (216², (6²)⁸, 72²) | 25⁴ (125², (5²)⁸, 50²) | 5⁸ | 4 → 3 |
| q-274 | 2^(n+1) = 64 | 3^(n+2) = 243 | 3 (trap 5) | 4 → 3 |
| q-275 | (5^(−√3))^(−√3) | (2^(−√5))^(−√5) | 32 | 4 → 3 |
| q-276 | 7ˣ·7⁻ˣ | 6ˣ·6⁻ˣ | 1 | 4 → 1 |
| q-277 | x = y = 8 | m = n = 6, m^(n−m)·n^(m−n) | 1 | 4 → 2 |
| q-278 | 5a⁸c⁶/(a²c³) | 3x⁹y⁴/(x³y²) | 3x⁶y² (trap 3x³y² = divided exponents) | 2 → 1 |
| q-279 | (3⁴)³·3⁻¹⁴ | (2³)⁴·2⁻¹⁵ | 1/8 (traps 1/256, −1/8, −8) | 1 → 3 |
| q-280 | x^(3/4)·x^(4/3) | x^(2/5)·x^(5/2) | x^(29/10) (traps x, flipped) | 4 → 1 |
| q-281 | 3ˣ·4ˣ·5ˣ = ∛60 | 2ˣ·3ˣ·7ˣ = √42 | 1/2 | 2 → 4 |
| q-282 | x+y+z = 5, 3ˣ3ʸ3ᶻ | a+b+c = 4, 2ᵃ2ᵇ2ᶜ | 16 (traps 8, 64) | 4 → 2 |
| q-283 | √98 | √112 | 4√7 | 1 → 4 |
| q-284 | letters a, b | letters m, n; choices reordered | m·n = m+n | 2 → 3 |
| q-285 | ⁴√(5⁶) | ⁴√(7⁶) | 7√7 | 2 → 2 |
| q-286 | x>0, √(48x) = √3·x | x>0, √(50x) = √2·x | 25 | 4 → 1 |
| q-287 | Dana 7 > √5+√20 (right), Yoav 4√3 > 5√2 (wrong) | Noa 8 > √7+√28 (63 < 64, right), Ethan 3√5 > 4√3 (45 < 48, wrong) | Only Noa | 1 → 3 |
| q-r26-t10-11 (English) | (5ⁿ⁺¹−5ⁿ)/4, nearly the summary example 5ˣ⁺¹−5ˣ = 4·5ˣ | (7ⁿ⁺¹−7ⁿ)/6 | 7ⁿ | 2 |

**Practice clean-up (57 → 40)**
- Removed the copies (14 extra-bank items alg-extra-unit-t10-2-1…7 and -3-1…7, which repeat each other and the topic 8/9 extras). Also removed q-r26-t10-09, which is the same type as guided Q6. No extra-bank warm-ups are left.
- Removed 2 September items whose type the Hebrew practice already covers: q-r26-t10-07 0.2ˣ = 25 (q-259) and q-r26-t10-08 4ˣ·25ˣ = 10⁶ (q-281).
- Kept the September items for types the Hebrew practice lacks: 06 (count the copies), 10 (don't divide by x), 11 (common factor), 12 (2ˣ+2ˣ = 4ˣ trap), 16 (sum of powers = 9ⁿ).
- Order in "Expressions and equations": simplify one root (q-262, q-263) → add roots → a number over a root → root equations → power equations → fractions of powers. "Mixed practice" keeps its easy → hard order. The answer keys are now spread over all four positions.
- Guided order kept: Q4 is the easiest, but it starts the root equations right before Q5 and Q6, and moving it would break that run.

Check: every answer and trap was recomputed in Python (sympy). No question equals a lesson example from topics 1–10, and no question stem duplicates another question in the course. `python3 math_check.py 10 32` → 0 problems, 0 warnings, 0 layout problems. Rendered powers-techniques and solve-q-248…252 and checked them by eye (tmp_check/ren10.png).

## 2026-10-06 review
- Lesson "Exponents & Roots — Techniques" slide 2: √98/√2 = 7 was the same as topic 9 guided q-240 (√98/√2) and split
  √98 = √49·√2, the Hebrew q-283. Changed to √150/√6 = √25 = 5, both ways (board, click labels, draw cue "Cross out √6",
  speech). √150 is not used anywhere else.
- q-263: √45 was the same question as the topic 9 warm-up alg-extra-root-practice-2 (√45, nearly the same choices).
  Changed to √117 = 3√13 (still a factor 9): choices 13√3, 4√3, 9√13 (trap: forgot the root of 9), 3√13 · key 4.
- Everything else checked (keys, traps, all 5 videos step by step, no old numbers left): no other problems.

## 2026-10-06 Hebrew back-check
Checked every guided + practice question, the lesson, the summary and the memory card against the teacher's Hebrew
VIDEO subtitles (01-Algebra-Original-Subtitles.txt, lines 5359–6607 = the Hebrew "expressions and equations with powers
and roots" lesson and its sample questions; 6610–8727 glanced at). Nothing in topic 10 is recorded.
Function `hebrew_backcheck(M)` in t10.py runs last.

Hebrew examples: √12/√3 = 2 · 6/√2 = 3√2, 20/√5 = 4√5 · 9⁸·8⁻³/(3¹²·4⁻³) = 3⁴·2⁻³ · √8+√18 = 5√2, √12+√48 = 6√3 ·
sample (√18+√18)/(√50−√8) = 2 · 4^(3x) = (1/8)^(5−3x), x = 5 · √(x−5) = 2, x = 9 · x√3 = 3√x, x = 3.

| where | was (landed on the Hebrew) | now | answer |
|---|---|---|---|
| q-249 + solve-q-249 (both methods) | (√50+√50)/(√32−√8) = 5 — Hebrew (√18+√18)/(√50−√8): √8 in the same place, √50 too | (√72+√72)/(√98−√32): 12√2 / 3√2; common factor √2(√49−√16) = 3√2, (2/3)√36 | 4 (choice 4); distractors 4√2, 16, 2 |
| q-250 + solve-q-250 | 9^(3x) = (1/27)^(2−3x) — Hebrew exponents 3x and 5−3x | 9^(2x) = (1/27)^(2−2x): 4x = −6 + 6x | 3 (choice 4); trap 3/5 (forgot the minus of the fraction); check 9⁶ = 27⁴ = 3¹² |
| memory card, "Negative exponent" | 3⁴·2⁻³ = 3⁴/2³ (the Hebrew lesson's answer) | 7²·2⁻⁵ = 7²/2⁵ | — |
| memory card, "Adding roots" | √8+√18 = 5√2 (the Hebrew lesson's example) | √44+√99 = 5√11 (as in the summary lesson) | — |

Left on purpose: q-251 √(x−6)=5 and q-252 x√6=6√x (same type as the Hebrew, different numbers); q-248 (different bases);
lesson 150/√6, 10/√2, 18/√6 (different numbers); practice q-r26-t10-10 x√3 = √(3x) (an English-made question: the left
side looks like the Hebrew x√3 = 3√x, but the equation and answer differ). Keys brute-forced (one correct choice each);
duplicate scan over all topics: no question or lesson uses these expressions. `python3 math_check.py 8 9 10 32` → 0/0/0;
solve-q-249 and solve-q-250 rendered and checked.

## 2026-10-07 no trinomial factoring
Teacher: factoring x² + bx + c ("two numbers that multiply to … and add to …") is not exam material and is slow — out.
Function `no_trinomial(M)` in t10.py runs last. Scanned all of topic 10 in the built view (lesson, summary, guided,
practice, memory card): the only place left was Question 6 (q-r26-t10-01, not recorded) — video + written explanation.
(The old lesson slide √(x+2)=x with (x−2)(x+1) is no longer in the build; factoring a common factor, x(x−7)=0, stays.)
Recorded and untouched: powers-techniques, solve-q-248…252.

| where | was | now |
|---|---|---|
| solve-q-r26-t10-01 slide 2 | Method 1 · Square and check: x² − 2x − 3 = 0 → (x − 3)(x + 1) = 0 ("two numbers that multiply…") | Method 1 · A root is never negative: x ≥ 0 by hand → cross out choices 1 and 4; try 1 (√5 ≠ 1, cross out) and 3 (√9 = 3 ✓, circle); trap: "−1 or 3" = squared and forgot to check |
| solve-q-r26-t10-01 slide 3 | Method 2 · Try the choices | Method 2 · Square, then check: 2x + 3 = x² by hand, don't solve; x = 3 ✓; x = −1 satisfies the squared equation (2·(−1)+3 = 1 = (−1)²) but √1 = 1 ≠ −1 ✗ (fake, created by squaring); circle 3; rule "After squaring: check in the original" |
| q-r26-t10-01 explanation | square, factor (x−3)(x+1), check | same two methods in writing, no factoring; trap explained |

Same answer (choice 3), same trap (choice 4). `python3 math_check.py 10 32` → 0/0/0; video rendered and checked.


## 2026-10-07 methods spread
Function `spread_methods` (runs last; append only). 1 practice question:
- Method 2 · Power count: q-278 (3x⁹y⁴/(x³y²): power 13 − 5 = 8; choices 8, 5, 18, 13 → choice 1).
Checked, not added: given power → asked power (taught in topic 11) has no question here; exponent-in-letter items (q-268, q-270) are not power-count questions. No slides: every solution video in this topic is recorded (unchanged).
All new lines verified numerically (python: power by scaling, fitting values, choice values, mirror values). `math_check.py 1 2 3 4 5 6 7 8 9 10 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0.


## 2026-10-07 study-plan order
Function `plan_order_fix` (runs LAST). Students follow the study plan (`src/lib/planData.ts` ORDER), not topic numbers; named methods were checked against the plan rank of their teaching topic.
- q-278: "Method 2 · Power count" → self-contained "Shortcut · Power count" (topic 10, days 1–5, comes before topic 5, day 13).
`python3 math_check.py 5 7 10 21 22 25 26 28 30 31 33 37 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0.


## 2026-10-07 no decimal estimates
Function `no_decimal_estimates` (runs last). Teacher: a student cannot estimate roots or π to one decimal place; estimates use whole-number benchmarks only (perfect squares, squaring, a factor into the root, 3 < π < 3.5). Videos with a recording are skipped by a build-time guard.
- q-284 (written): 3^1.5 ≈ 5.2 -> 3^1.5 = √27 > √25 = 5, so not 4.5.
Check: `python3 math_check.py 10 32` -> 0 / 0 / 0.
