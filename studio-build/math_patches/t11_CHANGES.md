# Topic 11 (Laws of Exponents & Roots — Advanced): changes

Patch: `math_patches/t11.py`. Check: `python3 math_check.py 11` gives 0 problems, 0 warnings and 0 layout problems. It is also clean when run together with T8–T10.

Topics 8–10 now teach sums of powers, comparing powers, bases between 0 and 1, conjugates (T9), (√a + √b)² (T9) and roots of different orders (T9). T11 does not teach these again. It points back to them in the lessons and on the new card. It uses them only in harder mixed practice.

## Counts
- **Questions rewritten:** 38. That is every T11 question that is still in the topic.
- **Questions added:** 12. Two are guided questions with solution videos. Ten are practice questions.
- **Questions removed:** 4 (extras 1, 3, 5 and 6).
- **Guided questions:** 14 before, 16 after.
- **Practice:** 27 before, 33 after.
- **Videos:** 1 new lesson (7 slides) and 2 new solution videos. 9 existing videos were changed.
- **New memory card:** `mem-r26-t11-advanced`. The topic had no card before.
- **Figures:** none. The topic has no figures.

## 1. Wrong rules (fixed)
- **Q4 video, slide 3 ("the 2 and 4 pattern"):** the old line was "for two different numbers bigger than one, only 2 and 4". It now says "two different positive whole numbers". It also explains why the pattern can be used here: the choices are whole numbers, so x = y² is a whole number too. Then it warns that fractions have other pairs, for example 9/4 and 27/8. The written solution and the q-306 solution say the same.
- **q-312 solution:** "a = −1 is the only base whose power can be −1". The exponent may also be a fraction, for example (−1)^(1/3) = −1.
- **Domains added:**
  - q-297: x > 0.
  - q-298: a > 0, b > 0 and a ≠ b.
  - q-302: a > 0 and b > 0.
- **Ambiguous conditions:** "1 < x, y" (Q4) and "0 < x, y" (q-318) are now stacked conditions: x > 1, y > 1 and x > 0, y > 0.

## 2. Methods added
**Section A lesson (`advanced-powers`)**
- Slide 1: "No new rules here" is now "Most rules here you already know — from topics 8, 9 and 10".
- Slide 3 is now "Patterns to spot". It has three patterns:
  - (x + y)²
  - aᵇ = bᵃ gives only 2 and 4, for positive whole numbers (T8)
  - copies of equal powers (T8/T10)
- The recap now says "Five questions next".

**New lesson `r26-t11-tools`, "Advanced Tools — Roots & Powers"** (about 3.5 minutes). It opens Section B, before Q6 (old Q7). Each tool matches a question that used it before it was taught:
1. **Root of a root:** multiply the indices. Bring a factor in front of the root inside first: √(x√x) = ⁴√(x³). Used in old Q10.
2. **Undo a power:** raise both sides to the reciprocal power. x^(−1/2) = 4 gives x = 1/16, with a check. Also x^(2/3) = 9 gives x = 27. Used in old Q14.
3. **Conjugates both ways:** (a − b)/(√a − √b) = √a + √b, and 1/(√5 − 2) = √5 + 2. The slide says that T9 introduced this. Used in old Q11.
4. **Product = 0:** each factor is 0. Never divide by √x. Used in old Q12.
5. **"Or" claims:**
   - when a power is 1 (from T8)
   - "A or B" is necessarily true if every allowed case makes A or B true
   - to kill such a claim, find one allowed case where both parts are false
   Used in old Q3.
6. Recap.

**Old Q3 (q-290, "or" logic) is moved** from Section A to the end of Section B, after the tools lesson. The review found it too hard at position 3. Its video now says which two tools it uses.

**New guided questions** (numbers are after renumbering):

| # | id | Question | Answer | Video methods |
|---|---|---|---|---|
| Q11 | q-r26-t11-01 | 1/(√5 − 2) − 1/(√5 + 2) | 4 (the trap is 2√5) | conjugates; estimate |
| Q15 | q-r26-t11-02 | x > 0, ∛(x√x) = 2 | x = 4 (the trap is 8) | exponents; try the choices |

**Guided order now:**
- Section A: Q1–Q5 = old Q1, 2, 4, 5, 6.
- Section B: tools lesson, then Q6–Q10 = old Q7–Q11, Q11 (new), Q12–Q14 = old Q12–Q14, Q15 (new), Q16 = old Q3, then the memory card.
- Every solution video uses a single sidebar, Question 1–16. `renumber_guided` sets the titles and the spoken numbers.

**Existing solution videos changed:**
- **Q9 (q-296):** new first method, "Clear the root" (3/(2√2) = 3√2/4). The old "match the denominators" method comes second. The "multiply the denominators" method was dropped.
- **Q10 (q-297):** "The lesson's favourite is four" is removed. That line was never said in this topic.
- **Q12 (q-299):** now opens with "a product is 0 only when a factor is 0". "Don't divide by √x" is kept as the trap. The guessing route is gone.
- **Q13 (q-300):** added the quick check 108 = 4 · 27, so √108 = 2√27.
- **Q14 (q-301):** method 3 now shows the check (1/16)^(−1/2) = 16^(1/2) = 4 ✓. "Last question" is now "Question fourteen", because it is no longer the last one.

**New memory card, "Advanced exponents and roots":**
- a "Tools" table with 9 rows
- a "From topics 8 to 10" table with 6 rows, which points back to those topics
- 4 tips: two routes, check that the choices differ, √a + √b ≠ √(a + b), estimate with perfect squares

## 3. Text
- **All written solutions** are rewritten in TeX with the numbers shown. There is no ":" for division any more. For example, 10125:3375 is gone, and q-288 now uses primes, as the video does.
- **Plug-in checks** were added to q-288, q-293, q-297, q-298, q-304, q-305, q-311, q-314 and q-321.
  - In q-305, x = 1 gives the same value for choices 3 and 4. The solution shows the tie and how x = 2 breaks it.
- **q-303:** the two "solution" lines are merged into one short line: "a = 0 also solves a² = 3a, but it is not a choice".
- **q-317:** the distractor 2/6 is now 3/2.
- **Stacked givens** (`cases`): q-290, q-291, q-292, q-298, q-300, q-306, q-318, q-321, plus the new q-r26-t11-02, 06, 07 and 09.
- **Reworded stems:**
  - q-299: "How many solutions does the equation … have?"
  - q-303: "Which of the following could be the value of a?"
  - q-310: now "When is √a + √b = √(a + b) true?" The choices are "Only when …" and "Always". The key is the same (a = 0 or b = 0).
  - q-311, q-315 and q-312 now use NITE style ("= ?" or "Which of the following is necessarily true?").
  - Plain-letter choices are now TeX: x, b and y.
- **q-313** keeps ":" because it is a real ratio question. Its solution now uses fraction bars.
- **Q7, Q9 and Q11 on-screen fractions:** I rendered them and they display correctly. The strings the review saw were only the plain-text slide notes. q-298 and the new Q11 now use display-size fractions (`\dfrac`) so they are easier to read.

## 4. Practice
**Removed:** extras 1 (5⁹/5⁶), 3 (3ˣ⁺¹ = 3⁷), 5 ((5x)³/25x²) and 6 (2¹⁶ vs 4⁷). They are the same templates as T10's extra set and are T8-level. Extras 2, 4 and 7 stay as a warm-up at the start, with NITE-style stems.

**Added (exam level):**

| id | Question | Answer | Tool |
|---|---|---|---|
| q-r26-t11-03 | (0.2)³·10⁴ / √0.0016 | 2000 | decimals and powers of 10 |
| q-r26-t11-04 | 2/(√7 + √5) | √7 − √5 | conjugate |
| q-r26-t11-05 | 9ˣ·27ˣ = 1/3 | −1/5 (the trap is −1/6) | common base |
| q-r26-t11-06 | a + b = 10, ab = 9: √a + √b | 4 | (√a + √b)² from T9 |
| q-r26-t11-07 | order of 2¹⁰⁰, 10³⁰, 3⁶⁰ | c < b < a (729¹⁰ < 1000¹⁰ < 1024¹⁰) | compare powers, harder than T8/T10 |
| q-r26-t11-08 | 0 < x < 1: largest of ∛x, x^(−1/2), x⁻², x³ | x⁻² | 0 < x < 1 with negative and fractional exponents |
| q-r26-t11-09 | a ≠ 1, aᵇ = 1: necessarily true | "b = 0 or a = −1" | "or" claims |
| q-r26-t11-10 | x√x = 4√x | 0 or 4 | don't divide by √x |
| q-r26-t11-11 | 1/(1+√2) + 1/(√2+√3) + 1/(√3+2) | 1 | a chain of conjugates |
| q-r26-t11-12 | √(2√(2√2)) | 2^(7/8) | root of a root |

**Order:** easy to hard. Warm-up extras come first, then the laws, then roots, and the hardest items (q-310, then new 06–12) come last. There are now about 18 exam-level items.

## 5. For the teacher to decide
- The "or" logic is taught on one T11 slide. PLAN.md suggests teaching must / could / cannot early in the course. If T1–T7 add that, the T11 slide can be shortened.
- Moving old Q3 renumbers every guided question in the topic. Please check `question_numbers.json` when numbers are locked.
- I dropped the "multiply the denominators" method from the Q9 video to keep it short. It can be added back if you want three methods.
- Recording length: the new tools lesson is about 3.5 minutes. The Section A lesson grew by about 0.5 minutes.

## Tool note
`student_view.py` reads the old site export. I checked the patched flow and numbering from the patched data instead, and I rendered every new and changed slide.

## Pass 2 (plan `real_exam/PLAN_REMOVE_RESTORE.md`, teacher-approved 2026-09-27)
**Removed (3):**
- Practice q-r26-t11-03 ((0.2)³·10⁴/√0.0016) and q-r26-t11-07 (order of 2¹⁰⁰, 10³⁰, 3⁶⁰). Also removed from the practice order.
- Card `mem-r26-t11-advanced`, table "From topics 8 to 10": the row "compare powers: make the exponents equal". The row "different roots: raise to a common power" stays.

**Restored (9):**
- Practice extras alg-extra-unit-t11-3-1, -3-3, -3-5, -3-6. They are back at the start of the practice (warm-ups, original order 1–7). Only clean-up: TeX, "=?" stems, numeric solutions.
- `advanced-powers` slide 3: the original "Laws + identities" slide and script. "Patterns to spot" stays as an added slide after it (slide 4). Its (x+y)² pattern was the same as the original slide, so it now holds only the other two patterns (2 and 4; counting copies). Sidebar: Translate first, Laws + identities, Patterns to spot, Choose a method, Recap.
- `solve-q-296`: the original slide "Multiply the denominators" is back as Method 3 (after Method 1 · Clear the root and Method 2 · Match the denominators). The title slide now says "Three ways".
- `solve-q-299`: the original slide "Open the brackets" is back as Method 1. "Product equals zero" is now Method 2 (shortened so it doesn't repeat the trap line).
- `solve-q-297` slide 3: the original line "The lesson's favourite is four — but here four gives root eight…" is back.
- q-317: the original distractor 2/6 is back (in place of 3/2).

**Summary video (new):** `r26-t11-summary`, "Advanced Exponents & Roots: Summary". It is at the end of Section B, after the memory card and right before the practice. Slides: Summary · Translate first · Hidden formulas · Root of a root · Undo a power · Conjugates · Product = 0 · Power = 1 and "or" · Two routes · Before you practice. About 3 minutes.

Check: `python3 math_check.py 11` gives 0 problems, 0 warnings and 0 layout problems. The same is true for `11 12` together.


## 2026-10-04 question = lesson example fixed
- Lesson "r26-t11-tools" slide 3: example x^(−1/2) = 4 (same as guided q-301) -> x^(−1/2) = 3, x = 1/9.
- Lesson "r26-t11-tools" slide 5: example √x(√x − 3) = 0 (same as guided q-299) -> √x(√x − 2) = 0, x = 0 or 4. Questions and their videos unchanged.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). The Hebrew topic 11 has no lesson — only questions. Nothing in topic 11 is recorded.
- **Advanced Exponents & Roots** (2.5 → 0.5 min): title + "What's ahead" (big powers → prime bases; two routes: the laws or plug in). Cut: prime bases → Q1; (x + y)² inside an exponent question → Q4; the 2-and-4 pattern → Q3 (incl. the fractions warning); counting copies → Q5; two routes + "check the choices differ first" → Q1 method 2; "a claim about every value → counterexample" → Q16; recap. (The "try boundary values" tip is taught in topic 12 Q20 and topic 1.)
- **Advanced Tools — Roots & Powers** (3.8 → 0.7 min): title + "What's ahead" naming the five tools. Cut: root of a root → Q9 (same example √(x√x)); undo a power → Q14 method 2; conjugates → Q10 and Q11 (same 1/(√5 − 2)); product = 0 → Q12; power = 1 and "or" claims → Q16; recap.
- Rewording: Q16 (q-290) "It uses two tools from the start of this section" → "It needs two ideas: when a power is one, and claims with the word "or"." Q9 (q-297) "The lesson's favourite is four" → "Four is a favorite".

## 2026-10-06 new exam methods
Function `add_methods` (runs last). GIVEN POWER → ASKED POWER (helps on 6 real exam questions). Topic 10 is unchanged: the idea builds on the "reciprocal power" of Question 14 (q-301) here in topic 11, so it lives here only.
- **Guided q-r26-t11-13** (Question 16; old Question 16 q-290 becomes 17), placed after solve-q-r26-t11-02: Given x > 0 and ⁴√(x³) = 8, √(x³) = ? Choices 16 · 32 · 64 · 512 → **3 (64)**. r = (3/2) ÷ (3/4) = 2, so square the given: 8² = 64. Trap 16 = x itself. Solve video: method 1 given power → asked power (cue, why it works), method 2 the long way (x = 16, √4,096 = 64) + the limit (unknown in the exponent).
- Sidebar of every guided solution video now has 17 questions; "Advanced Tools" intro says "Twelve questions next".
- Card "Advanced exponents and roots": new row after "x with a fractional power": given one power of b, asked a different power → r = asked ÷ given exponent, raise the given to r (not when the unknown is in the exponent and must be solved); ∛b = 5 ⇒ b^(2/3) = 25.
