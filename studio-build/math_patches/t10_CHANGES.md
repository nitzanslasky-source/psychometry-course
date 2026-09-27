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
