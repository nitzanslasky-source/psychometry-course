# Audit Topic 1: Algebraic Fundamentals (additions from math_patches/t01.py)

The original course is `course18.json`, from before the patch. The real exam is `real_exam/quant_real.md`, which has 760 questions. **Re-check (2026-09-27):** all REMOVE and UNSURE verdicts were checked again against the regenerated file, which has the full text (the "<" truncation is fixed). The teacher's rule was then applied: original course content stays, and an added lesson that teaches a type the original course tests stays. The ids below are real exam question ids.

Search notes. Counts are of question bodies; the subtopic headers are not counted.
- The must/could/cannot style is very common. The exam says "necessarily true", "necessarily –", "can be", "cannot be" and "could be". About 96 questions use it, most of them in number_properties, inequalities_absolute and divisibility_remainders.
- **"Consecutive even/odd" appears in 0 questions** (confirmed in the full-text file: the regex `consecutive (even|odd)` and `(even|odd) (numbers|integers)` match only 2025_autumn_q1_17, a factorials question about "even numbers from 2 to 2k"). "consecutive" appears in 12 questions, and every one is about plain consecutive numbers, whole numbers or digits: 2025_autumn_q1_01, 2019_spring_q1_02, 2023_spring_q2_08, 2023_spring_q2_09, 2020_winter_q1_02, 2025_winter_q2_08, 2020_winter_q2_01, 2023_spring_q1_17, and 4 charts questions.
- **But the ORIGINAL course teaches and tests consecutive even/odd** (`course18.json`, Topic 16): video `consecutive-integers` ("Consecutive EVEN numbers, or consecutive odd, have a gap of two"), video `consecutive-products`, card `mem-consecutive` (row "consecutive even / odd"), card `mem-products` (row "2 consecutive even"), and the questions q-458, q-468 and alg-extra-unit-t16-3-7 ("Four consecutive even integers have sum 44"), plus q-463 and q-472. Under the teacher's rule, this type stays, so the Topic 1 items that teach it are KEPT. They duplicate the Topic 16 lesson; that is a teaching-order choice for the teacher, not a reason to remove them.
- **The ORIGINAL course also uses the words** "distinct" (46 original questions, e.g. q-087 (T3), q-389 (T14), q-579 (T20)), "quotient" (alg-extra-unit-t15-3-7: "gives quotient 7 and remainder 4"; also q-018 after its fix) and "multiple" (alg-extra-unit-t14-4-2: "least common multiple of 12 and 18"). So the vocabulary rows are justified by original questions.
- The words **"quotient"**, **"multiple (of)"** and **"distinct"** appear in 0 questions. "reciprocal", "opposite" and "nonzero" also appear in 0 questions.
- The exam uses these words instead: "divisible by" (23 questions), "divisor" (3), "different from one another" / "different from 0" (10 or more), "digit(s)" (23), "sum" (42), "difference" (18), "product" (9) and "at least/at most" (39).

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| "Same signs -> plus" only when the signs touch | Add/Sub slides 3, 4, 9 | FIX | KEEP | - |
| "2k / 2k+1, k an integer" | Language of Algebra (`numbers`) slide 9 + card `mem-definitions` Even/odd row | FIX | KEEP | - |
| "Nonzero" taught before the recap uses it | `numbers` slide 5 + new card row "Nonzero" in `mem-definitions` | FIX | KEEP | The exam says "different from 0/zero": 2023_winter_q1_06, 2019_spring_q2_14, 2024_spring_q2_18 |
| The exam prints 3 facts (0 is neither positive nor negative, 0 is even, 1 is not prime) | `numbers` slide 13 lines + `mem-definitions` tip | FIX | KEEP | Checked against the NITE General Comments (nite_terminology.md, lines 66-68) |
| Removed "Remember when we called it times" | Mult/Div (`multiply-divide`) slide 5 | FIX | KEEP | - |
| "Squared means times itself" and "percent means out of 100" | `fast-calculation` slides 10-12 + `mem-fast` tips | FIX (used before it was taught) | KEEP | - |
| ÷ instead of ":" everywhere, plus the colon line | Remainders, Mult/Div slide 3, cards | FIX | KEEP | - |
| "Skip ahead" line for strong students | `add-subtract` slide 1 | FIX (not content) | KEEP | - |
| q-018 changed to ask for the quotient and the remainder | q-018 | FIX (the old form used fractions before they were taught) | KEEP | - |
| q-014, extra-3 and extra-4 moved to fast-practice. q-003, q-004 and q-033 removed | sections | FIX | KEEP | - |
| New example of splitting the top of a fraction bar | `order-of-operations` slide 6 + `order` card tip | FIX (the rule was already on the original card) | KEEP | 2021_spring_q1_03, 2023_winter_q1_06 |
| **x9 and x11** slide | `fast-calculation` new slide "×9 and ×11" + `mem-fast` example 47×9 | FIX (the original card row "Times 9 / 11" and q-014 already used it; no slide taught it) | KEEP | original content |
| **Minus before brackets** flips every sign | new slide "Minus before brackets" in `order-of-operations` + recap line + `order` card tip | METHOD/rule | KEEP | 2020_spring_q2_01 (a – b + c – d), 2025_spring_q2_01, 2021_autumn_q1_13, 2023_winter_q2_15 |
| **Last digit + estimate** to knock out choices | new slide "Last digit" in `multiply-divide` + 2 `mem-times` tips | METHOD | KEEP | 2020_spring_q2_11 (closest to 304×329), 2020_winter_q2_05 (units digit of 7·x), 2019_spring_q2_16 (35A×4B=15CC5) |
| **Exam Words** lesson: title slide, "Four results" (sum/difference/product/quotient) | `r26-t01-exam-words` | CONTENT (vocabulary) | KEEP | sum: 42 questions, difference: 18, product: 9 (e.g. 2019_spring_q1_02, 2023_spring_q1_02). "quotient": 0, see UNSURE |
| Exam Words "Multiples & divisors" | `r26-t01-exam-words` | CONTENT | KEEP | divisible: 23 questions, divisor: 3 (2023_spring_q2_06, 2023_winter_q2_08, 2024_winter_q1_04). "multiple": 0, see UNSURE |
| Exam Words "Digits" (digit ≠ number, sum of digits, cannot start with 0) | `r26-t01-exam-words` | CONTENT | KEEP | 23 questions, e.g. 2024_autumn_q2_06, 2025_autumn_q1_05, 2019_winter_q1_17, 2023_spring_q1_02 |
| Exam Words "Distinct · at least" | `r26-t01-exam-words` | CONTENT | KEEP | at least/at most: 39 questions (2025_autumn_q1_14, 2024_spring_q2_17). "distinct": 0, see UNSURE |
| Exam Words **"Consecutive even / odd"** | `r26-t01-exam-words` slide "Consecutive even / odd" + recap line "Consecutive even / odd: steps of 2" | CONTENT (original course type, Topic 16) | KEEP (was REMOVE) | 0 real questions, but tested by original q-458, q-468, alg-extra-unit-t16-3-7 and taught in original video `consecutive-integers` |
| Exam Words Recap (other lines) | `r26-t01-exam-words` Recap | CONTENT | KEEP | as above |
| Card `mem-r26-t01-exam-words`: rows Sum, Difference, Product, Divisor (factor), Divisible by, Digit, At least / at most, and the 3 tips | card | CONTENT | KEEP | as above |
| Card `mem-r26-t01-exam-words` row "Consecutive even / odd" | card | CONTENT (original type) | KEEP (was REMOVE) | original q-458, q-468, alg-extra-unit-t16-3-7; original card `mem-consecutive` has the same row |
| Card `mem-definitions` Consecutive row: added "(consecutive even / odd: by 2)" | card | CONTENT (original type) | KEEP (was REMOVE) | same as above |
| Card `mem-r26-t01-exam-words` rows Quotient, Multiple of n, Distinct | card | CONTENT (words used by original questions) | KEEP (was UNSURE) | 0 real questions use the words; original questions do: "distinct" in 46 (q-087, q-389, q-579 ...), "quotient" in alg-extra-unit-t15-3-7 and fixed q-018, "multiple" in alg-extra-unit-t14-4-2. The ideas are on the real exam as "divisible by" and "different from one another" |
| **Must / could / cannot + plug-in numbers** lesson (all 7 slides: title, Three questions, One example, Test numbers, Could it?, Exam strategy, Recap) | `r26-t01-must-could` | METHOD | KEEP | about 96 questions, e.g. 2024_spring_q2_08, 2020_winter_q1_02, 2023_spring_q1_08, 2020_autumn_q2_19 ("can be any number") |
| Card `mem-r26-t01-must-could` (both tables + tips) | card | METHOD | KEEP | same |
| q-r26-t01-01 (guided): sum of digits of the smallest 3-digit number with distinct digits + video `solve-q-r26-t01-01` | intro-numbers | CONTENT (digits) | KEEP | 2023_spring_q1_02, 2024_winter_q1_19 ("different from one another"), 2025_autumn_q1_05 |
| q-r26-t01-02: multiple of 6 and divisor of 60 | intro-numbers | CONTENT (divisibility words) | KEEP | 2023_spring_q2_06 (common divisor), 2024_winter_q1_04, 2023_winter_q2_08 |
| q-r26-t01-03: sum divided by difference | intro-numbers | CONTENT (words) | KEEP | 2023_spring_q1_02, 2019_spring_q1_02, 2021_autumn_q2_09 |
| q-r26-t01-04: three consecutive odd numbers, c − a | intro-numbers | CONTENT (original type) | KEEP (was REMOVE) | same type as original alg-extra-unit-t16-3-7 and q-458 |
| q-r26-t01-05 (guided, must) + `solve-q-r26-t01-05` | intro-numbers | METHOD | KEEP | 2024_spring_q2_08, 2020_winter_q2_14, 2021_autumn_q2_15 |
| q-r26-t01-06 (guided, cannot: prime × even) + `solve-q-r26-t01-06` | intro-numbers | METHOD | KEEP | 2024_spring_q2_08 (even factor, so necessarily even), 2026_spring_q1_01, 2020_spring_q1_18 (cannot) |
| q-r26-t01-07 (must be even: n(n+1)) | intro-numbers | METHOD | KEEP | 2021_spring_q2_19 (a(a+1)), 2023_spring_q2_08 |
| q-r26-t01-08 (could: x·x < x) | intro-numbers | METHOD | KEEP | 2021_autumn_q1_07, 2020_autumn_q2_19, 2020_spring_q1_18 |
| q-r26-t01-09 (must, opposites) | intro-numbers | METHOD (tests original vocabulary) | KEEP | 2024_spring_q2_18, 2019_spring_q2_14 (sign reasoning, necessarily) |
| q-r26-t01-10 (cannot, reciprocals) | intro-numbers | METHOD (tests original vocabulary) | KEEP | 2026_spring_q1_17 (1/x), 2020_spring_q1_18 (cannot be) |
| q-r26-t01-11 (guided, minus before brackets) + `solve-q-r26-t01-11` | order | METHOD | KEEP | 2020_spring_q2_01, 2026_spring_q2_05 (numeric, with signs and brackets) |
| q-r26-t01-12, q-r26-t01-22 (minus before brackets) | order, unit-t1-1 | METHOD | KEEP | same |
| q-r26-t01-13, -14, -21 (fraction bar) | order, unit-t1-1 | practice of an original rule | KEEP | 2021_spring_q1_03, 2023_winter_q1_06, 2023_winter_q2_01 |
| q-r26-t01-15 (guided, last digit + estimate) + `solve-q-r26-t01-15` | intro-mult | METHOD | KEEP | 2020_spring_q2_11, 2020_winter_q2_05 |
| q-r26-t01-16 (last digit check) and the new second method in q-012 | intro-mult / unit-t1-1 | METHOD | KEEP | same |
| q-r26-t01-17 (must, consecutive integers) | unit-t1-1 | METHOD | KEEP | 2023_spring_q2_08, 2022_winter_q1_20 |
| q-r26-t01-18 (−1 < x < 0, largest) | unit-t1-1 | METHOD | KEEP | 2021_autumn_q1_07 (1 < x < 2, greatest), 2022_autumn_q1_08 (0 < a < 1, smallest), 2023_spring_q1_08 |
| q-r26-t01-19 (cannot be prime) | unit-t1-1 | METHOD | KEEP | 2022_winter_q2_12, 2020_winter_q1_02, 2026_spring_q1_01 |
| q-r26-t01-20 (distinct factor pairs of 36, cannot be the sum) | unit-t1-1 | CONTENT (factor pairs) | KEEP | 2023_spring_q1_18 (integer sides, area 91), 2022_winter_q2_12 |
| q-r26-t01-23 (86 × 9) | fast-practice | practice of original content (x9 was on the original card) | KEEP | original |
| q-r26-t01-24 (closest to 398×51/99) | fast-practice | METHOD (estimate; an original Estimate slide exists) | KEEP | 2020_spring_q2_11, 2023_autumn_q2_18 |

## TO REMOVE
None. (Re-check, 2026-09-27.) The 4 earlier REMOVE items (the "Consecutive even / odd" slide and recap line in `r26-t01-exam-words`, the row on card `mem-r26-t01-exam-words`, the addition to the Consecutive row on `mem-definitions`, and question `q-r26-t01-04`) are now KEEP. The real exam has no consecutive even/odd question, even in the full-text file, but the original course teaches and tests this type in Topic 16 (video `consecutive-integers`, card `mem-consecutive`, questions q-458, q-468, alg-extra-unit-t16-3-7), so it stays under the teacher's rule.

## UNSURE
None. The words Quotient, Multiple of n and Distinct are now KEEP, because original course questions use them (see the search notes). Optional wording note for the teacher: the real exam says "divisible by" and "different from one another", so the lesson could mention those phrases next to the course's words.

## ORIGINAL ITEMS REMOVED BY FIXERS
Found by applying `math_patches/t01.py` in memory to `course18.json` and comparing Topic 1 questions, videos, slides and cards.

Questions deleted (`M.unplace`, which also deletes the question data). None of them had a solution video.
| Original id | Original section | Original stem | Choices (correct) | Fixers' reason |
|---|---|---|---|---|
| q-003 | unit-t1-1 (Mixed practice), flow-0027 | 84 − 36 = ? | 52, 44, **48**, 58 | near-duplicate of q-031 (two-digit borrowing) |
| q-004 | unit-t1-1 (Mixed practice), flow-0028 | 95 + (−38) = ? | 133, **57**, 67, −57 | near-duplicate of q-032 (adding a negative) |
| q-033 | intro-add, flow-0010 | 63 − 27 = ? | 26, 24, 34, **36** | near-duplicate of q-031 (two-digit borrowing) |

Questions replaced (same id, different question):
| Original id | Original | Now |
|---|---|---|
| q-018 | "200 : 6 = ?" with choices 33 1/6, **33 1/3**, 33 2/3, 33 5/6 | "What are the quotient and the remainder when 200 is divided by 6?" (quotient 33, remainder 2). Reason: fractions are only taught in Topic 2. To restore, put back the original stem and choices (and the original explanation from `course18.json`). |

Questions moved, not removed: q-014, alg-extra-unit-t1-1-3 and alg-extra-unit-t1-1-4 went from unit-t1-1 to fast-practice. All other 50 original Topic 1 questions keep their stem, choices and answer; only the notation changed (":" became ÷, TeX, thousands commas). Every original explanation was rewritten (the originals are in `course18.json` if the teacher wants any back).

Slides: no original slide or video was deleted (multiply-divide 9 → 10, order-of-operations 6 → 7, fast-calculation 14 → 15 slides; all original titles are still there). 20 original slides had their script edited. The only original line deleted outright is "Remember when we called it times" (multiply-divide slide 5). The ":" notation was replaced by ÷ everywhere.

Card rows and tips: no original row was deleted. Edited rows are `mem-definitions` Consecutive ("integers that differ by exactly 1"), Remainder ("10:3 → remainder 1") and Even / odd ("integers only: 2k / 2k+1"); `mem-times` "Two signs side by side"; and `mem-fast` "Times 5 / 25 / 125" (":" to ÷) and "Times 9 / 11" (example 47×9 added). The `order` card's two original tips were replaced by three: the same two in ÷ notation plus a new minus-before-brackets tip.
