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
