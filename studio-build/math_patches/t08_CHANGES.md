# Topic 8 (Exponent Laws — Fundamentals): changes

Patch: `math_patches/t08.py`. Check: `python3 math_check.py 8` gives 0 problems, 0 warnings and 0 layout problems.

## 1. Wrong or overclaimed rules
- **Slide "2⁴ = 4²"** (now slide 12) is rewritten. Old: "the one special case… any other pair, one side is always bigger". New: "Among positive whole numbers, 2 and 4 is the only pair of different numbers that works. With negative numbers or fractions there are other pairs." The slide also shows 2³ = 8 and 3² = 9 as the usual case.
- **Memory card, tip 1:** same fix ("Among positive whole numbers…").
- **Slide "When aᵇ = 1":** "b must be even" now says "b an even whole number", on the board and in the script.

## 2. Order: nothing used before it is taught
- **Slide 3 (exponent 0):** the old proof, 5³/5³ = 5⁰, used the division law from slide 7. It is replaced by a "staircase": 125, 25, 5, then ÷ 5 again gives 5⁰ = 1. No law is needed.
- **Negative exponents** now come before "Bases 1 and 0" (they were slides 5 and 4). The staircase continues to 5⁻¹ = 1/5 and 5⁻² = 1/25. Then "Bases 1 and 0" explains why zero to a negative power is undefined (it means one over zero). New order: title, what a power is, exponent 1 and 0, negative exponents, bases 1 and 0, then the laws.
- **Moved to T9** (practice section "Extra independent root practice", at the end), because they use fractional exponents or roots: q-227 (7³)^(2/3), alg-extra-exponent-extra-2 (27^(2/3)) and alg-extra-exponent-extra-7 (√50 + √8). Their text was fixed too. Their topic field is now 9.
- The solution for alg-extra-exponent-extra-3 (3ˣ⁺¹ = 3⁴) uses "same base, therefore equal exponents". This is now taught on the new "Compare powers" slide.

## 3. Missing methods (added)
- **Main video, new slide 14, "Adding equal powers":** 2ⁿ + 2ⁿ = 2ⁿ⁺¹ and 3ⁿ + 3ⁿ + 3ⁿ = 3ⁿ⁺¹. It also shows the trap 2ⁿ + 2ⁿ ≠ 2²ⁿ, checked with n = 3.
- **New lesson video `r26-t08-traps`, "Exponent Traps"** (6 slides, about 3.8 minutes). It is in the core section, after the core questions:
  - Between 0 and 1: 0.5², powers of ½, decimal places (0.2³ = 0.008, 0.3² = 0.09), and x³ < x² < x.
  - Compare powers: make the bases the same (2¹⁰ vs 4⁴) or make the exponents the same (2³⁰ vs 3²⁰ as 8¹⁰ vs 9¹⁰). Also "same base, therefore equal exponents", and a note that rewriting to the smallest prime base comes later in the course.
  - Counting zeros: 2⁴·5⁴ = 10⁴, and the uneven case 2⁵·5³ = 4·10³. The number of zeros equals the smaller exponent.
  - Signs with letters: an odd power keeps the sign, an even power is never negative, and (−x)² vs −x².
  - Check with a number: when to plug in, and what to do when two choices give the same value.
- **5 new guided questions, each with a solution video** (Questions 4–8):
  - q-r26-t08-01: copies
  - q-r26-t08-02: 0 < x < 1
  - q-r26-t08-03: compare powers
  - q-r26-t08-04: zeros
  - q-r26-t08-05: signs
- **New solution videos for existing questions:**
  - q-224 (Question 1): the law, then a check with x = 1. This was the review's plug-in request.
  - q-226 (Question 2): negative minus negative.
  - q-231 (Question 3): tests each choice. I moved q-231 from the practice section into the core section, after q-226, so that it works as a guided question.

## 4. Memory card
- The Laws table has two new rows: copies (aⁿ + aⁿ = 2aⁿ, 2ⁿ + 2ⁿ = 2ⁿ⁺¹) and (−1)ⁿ.
- New table "More powers to know": 2⁹ = 512, 2¹⁰ = 1024, 10ⁿ and 10⁻ⁿ.
- New table "Exam traps": between 0 and 1, compare powers, zeros, signs.
- Tips: the 2 and 4 fix; "smallest prime base, used a lot later"; and a new tip, "check with a number".

## 5. Other slide text
- Slide 9: "two sixteen" is now "two hundred sixteen".
- Slide 15: "Ten core questions next" is now "Core questions next", plus a new line that points to the traps video.
- Main video sidebar: rebuilt for the new order and the new slide.
- Core section title: "…and ten core questions" is now "…and core questions". The API has no call for this, so the patch sets it directly.

## 6. Question text (every T8 question)
- All written solutions are rewritten in TeX with the numbers shown. There is no ":" for division any more (q-221, q-222, q-227, q-229, q-230 used it), and no "so" in the middle of a sentence.
- q-232 is reworded to NITE style. The stem is now "Given: a and b are positive integers, and" followed by the stacked conditions {a < b, aᵇ = bᵃ} and "a + b = ?".
- alg-extra-exponent-extra-6: the choice "It cannot be determined" is removed. The question is now "Which of the following is true?" with the choices 2¹⁰ > 4⁴ (correct), 2¹⁰ = 4⁴, 2¹⁰ < 4⁴ and 2¹⁰ = 2·4⁴.
- alg-extra-exponent-extra-3, 4 and 5: "Evaluate / Solve / simplify" is now the "Given: … / … = ?" style.
- q-226: the solution names the trap choice (−15). q-224: the solution adds the check with a number.

## 7. Practice
- **Removed:** alg-extra-exponent-extra-1 (2⁶/2³). It is a near-duplicate of core q-225.
- **Added 18 practice questions** (q-r26-t08-06 … 23). They cover copies (3), numbers between 0 and 1 or decimals (3), comparing powers and same-base equations (3), zeros and digits (2), signs (3), aᵇ = 1 with letters (1: (x−2)^(x+3) = 1, 3 values) and mixed "which law?" drills (3).
- **Order easy → hard.** The laws come first (q-228 …), then the new items, then the exam-hard ones at the end: digits, copies equation, −1 < x < 0, the ordering of 2⁵⁰, 3³⁰ and 5²⁰, x³y⁵ < 0, q-232 and (x−2)^(x+3) = 1.
- **Totals:** 26 practice items (was 12) and 15 core or guided questions (was 10). About 20 items are now exam-level.

## 8. For the teacher to decide
- The three questions moved into T9 now sit at the end of T9's practice section. The T9 owner may want to reorder them or drop them as near-duplicates (T9 already has 81^(1/4)).
- The main lesson grew from 6.5 to about 8.3 minutes because of the staircase and the copies slide.
- Do you want the easy practice items hidden for strong students (the review's "let them skip to a hard set")? The order already puts them first, so strong students can start from the middle.

## Tool note
`student_view.py` builds the question list from `../content/full-course/topics/t8.json`. That is the old export, so `tmp_check/view/t8.md` does not show patched questions or new videos. I read a dump made from the patched data instead.

## Pass 2 (teacher-approved remove/restore plan, 2026-09-27)
**Removed**
- `r26-t08-traps`: slide "Counting zeros" and its sidebar label; the title slide says "Four short ideas".
- Guided q-r26-t08-03 (largest of 2⁴⁰, 3³⁰, 5²⁰, 10¹⁰) and q-r26-t08-04 (zeros of 2⁷·5⁴) with their solution videos. The guided questions are renumbered: T8's own are Questions 1–6, and q-131 and q-132 (moved in by the T5 patch) are Questions 7–8. The T8 sidebar is widened automatically to cover them.
- Practice q-r26-t08-13 (ordering 2⁵⁰, 3³⁰, 5²⁰) and q-r26-t08-16 (digits of 4⁵·5⁸). The other ids stay the same.
- Card `powers`, table "Exam traps": row "Zeros at the end".

**Restored**
- alg-extra-exponent-extra-1 (2⁶/2³), back in the practice as its first item (TeX, numeric solution).
- alg-extra-exponent-extra-6: the original "Which is greater: 2¹⁰ or 4⁴?" with the choices "It cannot be determined… / The first power / The second power / They are equal" (key: the first power).
- `exponents` "Bases 1 and 0": the original line "A negative exponent means dividing by zero — undefined. Zero to the zero? Not defined in this course either." is back (the slide now comes after negative exponents).
- `exponents` "Dividing powers": the original proof 5³/5³ = 5⁰ = 1 comes back as a second way, at the end of that slide, so it uses the division law only after teaching it. The ÷5 staircase stays.
- q-131, q-132 and q-expression-extra-09 are moved in by the T5 patch (not by this one).

**Summary video (new)** `r26-t08-summary` "Exponent Laws: Summary", at the end of the core section, right before the practice: Summary · Exponents 1, 0, −n · The three laws · Same exponent · Negative bases · When aᵇ = 1 · Split and count · Compare powers · Before you practice.

## 2026-10-02 new numbers + order
Goal: the English Topic 8 must not look like a copy of the Hebrew course. Every idea, trap, level and method stays.
Code: `new_numbers(M)` and `order_changes(M)` at the end of `apply`. There is a `RECORDED` set, empty for now. A question
or video put in it keeps its old version. The Hebrew Topic 8 has one lesson and 10 study-guide questions with no videos,
so there are no Hebrew levels for them. q-131 and q-132 come from Hebrew Topic 5 videos: q-131 is medium, q-132 is medium+.

**Questions** (key, written solution and, where there is one, the whole solution video were updated together):
| Item | Old (Hebrew) | New | Key |
|---|---|---|---|
| q-218 | 0^√2 + (√2)¹ | (√3)¹ + 0^√3 = √3 | 1 → 4 |
| q-219 | 1^√5 + (√5)⁰ | (√7)⁰ + 1^√7 = 2 | 3 → 2 |
| q-220 | −(−4)³ = 64 | −(−2)⁵ = 32; distractors −32 (forgot the outer minus) and ±10 (base × exponent) | 4 → 3 |
| q-221 | (2/5)⁻³ | (2/3)⁻³ = 27/8 | 2 → 3 |
| q-222 | (−3)⁻⁴ | (−5)⁻² = 1/25 | 4 → 1 |
| q-223 | 11⁻⁷·11¹²·11⁻³ | 7⁻⁵·7⁹·7⁻² = 49; trap 7⁶ (lost minus) | 3 → 1 |
| q-224 (guided) | 5^(x+2) | 4^(x+2) = 16·4ˣ; x = 1 check gives 64, 8, 20, 16 | 3 → 1 |
| q-225 | 13⁹/13⁷ | 12⁸/12⁶ = 144 | 3 → 2 |
| q-226 (guided) | 2·2⁻⁶/2⁻¹⁰ = 32 | 3·3⁻⁵/3⁻⁸ = 81; traps 3⁻¹² (added −8), 1/81, 27 (forgot the lonely 3) | 3 → 4 |
| q-228 | 2⁴·5⁴ | 5⁵·2⁵ = 100,000 | 3 → 1 |
| q-229 | 6⁴/2⁴ | 12³/4³ = 27 | 2 → 4 |
| q-230 | 5³/15³ | 7³/14³ = 1/8 | 1 → 2 |
| q-231 (guided) | aᵇ = 1, not possible: a = 0 | mⁿ = 1, not possible: m = 0 (n = 5, m = −1, n = 0 possible) | 1 → 3 |
| q-232 | a<b, aᵇ = bᵃ, a+b = 6 | m>n, mⁿ = nᵐ, m·n = 8 (the 2-and-4 fact stays; traps 6 = m+n, 16 = mⁿ) | 3 → 1 |
| q-131 (guided) | (x⁻² + 4x²/x⁴)·⅕·5/x⁻² = 5 | (x⁻³ + 2x³/x⁶)·⅓·6/x⁻³ = 6 | 3 → 2 |
| q-132 (guided) | a: (a+3a)−(3a−a) … (a²−9)/(a+3)−a = −3 | n: (n+4n)−(4n−n), (−1)ⁿ+n⁰, (n²−25)/(n+5)−n = −5, ((n+3)+(n+3)²)/(n+4) | 4 → 3 |
| q-expression-extra-09 | (x⁻² + 2/x²)·x² = 3 | x³·(x⁻³ + 4/x³) = 5 | 3 → 1 |

Methods kept in the videos: split the exponent and check with x = 1 (q-224); write the lonely base as a power, then add and
subtract exponents, with the minus-minus trap (q-226); test every choice against the three cases (q-231); simplify step by
step and plug in x = 1 because the choices are only numbers (q-131); simplify each choice, remove three and mark the
fourth, then prove it with the difference of squares, and why plugging in is long here (q-132). The q-132 video now
skips the "heavier" choice 3 and comes back to it. The q-131 and q-132 video titles follow the new stems.

**Lesson "Exponent Laws"** (the Hebrew lesson's own examples): (3/7)⁰ → (4/9)⁰; (2/5)⁻³ (this was q-221) → (5/2)⁻² = 4/25;
"a million times" → "as many times as you like"; (2·3)³ = 216 → (4·5)² = 400; (−3)⁴ = 81, (−3)³, −3² → (−2)⁶ = 64,
(−10)³ = −1,000, −7² = −49. The aᵇ = 1 slide was reworded on screen and in speech ("Option 1: a = 1 — any b" →
"Base 1 / Base −1 / Exponent 0", "cases"). The opening lines of the title slide were reworded. Card tip: (−3)² vs −3² →
(−7)² = 49 vs −7² = −49. 2⁴ = 4² was kept, because that fact is the point of the slide.

**Order changes**
- Lesson: "2⁴ = 4²" now comes before "When aᵇ = 1". Both are independent. aᵇ = 1 still comes after "Negative bases",
  which it needs. The sidebar was updated.
- Core questions now follow the order in which the lesson teaches them: q-219 before q-218 (same level); q-221 (negative
  exponent, slide 4) before q-220 (negative base, slide 10); q-225 (plain division) before q-224 (split exponent,
  slide 13). The guided numbering does not change.
- Answer positions: every key above moved away from its Hebrew position.
- Rejected: swapping "Same exponent" and "Negative bases", because it would break up the group of laws. Swapping q-229
  and q-230, because q-229 (whole-number answer) is easier than q-230. Moving q-131 and q-132, which are already
  medium → medium+. Reordering the summary video and the practice, which are English-made and already easy → hard.

Check: `python3 math_check.py 8 32` and `python3 math_check.py 5 8 32` → 0 problems, 0 warnings, 0 layout problems.

## 2026-10-02 review
- Fixed the q-132 video intro: it still said "doesn't depend on a … until the a disappears". The letter is now n.
- Summary slide "When aᵇ = 1" (it lists aᵇ = 1 and then 2⁴ = 4²): kept. The two facts do not depend on each other, and this summary slide recaps the rule that the guided question uses, so the order does not affect the flow.
- Checked with no changes needed: all the core and guided questions, which were re-computed (keys, traps and the x = 1 checks), plus the lesson examples and 15 practice questions.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). Nothing in topic 8 is recorded.
- **Exponent Traps** (3.2 → 1.8 min). Cut "Signs with letters" → Question 6 (odd keeps the sign, even is never negative; (−x)² and −x² are on the laws lesson's "Negative bases" slide). Cut "Check with a number" → Question 1 method 2, Question 4 (two choices tie → try another n), Question 5 (pick one half).
- "Between 0 and 1": kept the decimals (0.2³ = 0.008, 0.3² = 0.09 — taught nowhere else, used in practice). Cut the ½, ¼, ⅛ powers and the x³ < x² < x rule (Question 5 teaches them); the last line is now "a power makes a number smaller only between zero and one. Above one, it makes it bigger."
- "Compare powers" kept whole (no question video teaches it). Title slide: "Two short ideas here. The other traps come inside the questions." Sidebar: Between 0 and 1 · Compare powers.
