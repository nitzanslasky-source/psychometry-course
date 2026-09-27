# Topic 1: Algebraic Fundamentals. Changes (course review 2026-09)

Patch: `math_patches/t01.py`. Check: `python3 math_check.py 1` gives 0 problems, 0 warnings and 0 layout problems.

## Summary
- Questions: 51 rewritten (all remaining Topic 1 questions), 24 added (4 of them guided, each with a solution video), 3 removed, 3 moved.
- Videos: 2 new lesson videos, 5 new solution videos, 3 new slides in existing lessons, 20 existing slides edited.
- Memory cards: 2 new, 4 updated.
- Figures: Topic 1 has none.

## 1. Wrong or unclear rules in the videos
- **Add/Sub slides 3, 4 and 9:** "same signs → plus" now says it applies only to two signs *touching* (nothing between them). Slide 4 now says that in −8 − 6 the signs do not touch.
- **Language of Algebra slide 9:** "2k" and "2k + 1" now say "where k is an integer".
- **Language of Algebra slide 5:** "Nonzero" is now taught here (board: "Nonnegative: x ≥ 0 · Nonzero: x ≠ 0"), before the recap uses it.
- **Language of Algebra slide 13 (recap):** says that the exam prints three of these facts in the general comments of every quantitative section (0 is neither positive nor negative, 0 is even, 1 is not prime). The closing lines now introduce the two new videos.
- **Mult/Div slide 5:** removed "Remember when we called it 'times'?". That lesson does not exist.
- **Fast Calc slides 10–12:** added one line each: "squared means times itself" (50², 65²) and "percent means out of a hundred". Squares and percentages are not taught before this lesson.
- **Division sign:** every board item and draw note that used ":" for division now uses ÷ (Remainders 10 ÷ 3, 0 ÷ 9, 9 ÷ 0, 576 ÷ 8, 24 ÷ 6 · 2, 44 ÷ 4, 24 ÷ 8, recap "× ÷"). Mult/Div slide 3 has one new line: "Some books write division with a colon. It means the same thing. In this course we write the division sign or a fraction bar."
- Mid-sentence "so" (meaning "therefore") removed from 5 spoken lines. "Five/Seven questions next" changed to "Questions next", because the question counts changed.
- Add/Sub slide 1: one line for strong students: "Already fast and sure? Try the questions after this lesson first. All correct? Jump ahead."

## 2. Methods added
| Method | Where | Guided (with video) | Practice |
|---|---|---|---|
| **Exam words** (sum, difference, product, quotient, multiple, divisor/factor, divisible by, digit, distinct, at least/at most, consecutive even/odd) | New lesson `r26-t01-exam-words` (7 slides) + card `mem-r26-t01-exam-words`, section 1 after the Number words card | q-r26-t01-01 (digits / distinct / sum) | q-r26-t01-02, -03, -04, -20 |
| **Must / could / cannot + plug-in numbers** (test 0, 1, −1, ½, 10; only allowed numbers; exam strategy: break the wrong choices) | New lesson `r26-t01-must-could` (7 slides) + card `mem-r26-t01-must-could`, end of section 1 | q-r26-t01-05 (must), q-r26-t01-06 (cannot) | q-r26-t01-07, -08, -09, -10 (section 1); -17, -18, -19 (mixed practice) |
| **Minus before brackets** flips every sign inside | New slide 5 "Minus before brackets" in Order of Operations + recap line + card tip | q-r26-t01-11 | q-r26-t01-12, -22 |
| **Fraction bar** (split the top, never the bottom), practised for the first time | Order of Operations slide 6 has a new example of splitting the top (draw note) | none | q-r26-t01-13, -14, -21 |
| **Last digit + estimate to knock out choices** | New slide 9 "Last digit" in Multiplication & Division + card tips | q-r26-t01-15 | q-r26-t01-16, q-012 (new second method) |
| **×9 and ×11** (the card listed it, q-014 used it, no slide taught it) | New slide 5 "×9 and ×11" in Fast Calculation | none | q-r26-t01-23, q-014 |
| Estimation (exam-level) | none | none | q-r26-t01-24 |

Sidebars were updated for all three lessons that got new slides.

## 3. Order of teaching (used before taught)
- **q-018** (200 : 6 = 33⅓) needed fractions (Topic 2). It now asks for the quotient and the remainder: "quotient 33, remainder 2". The distractor "32, remainder 8" teaches that a remainder must be smaller than the divisor.
- **q-014** (666 × 11), **extra-3** (25 × 28) and **extra-4** (48 × 15) moved from Mixed practice to Fast-calculation practice. They come after the lesson that teaches their tricks now. *Workaround:* the API has no "move", and `unplace` deletes the question, so the patch keeps a copy and puts it back (`move_q`).
- The Exam Words video comes before q-036, which uses "product".

## 4. Text (all questions)
- Every solution was rewritten with numbers in `$TeX$`. No ":" for division anywhere. Short sentences, no mid-sentence "so".
- Stems with ":" now use ÷ (q-011, 015–017, 019, 020, 022, 023, 025, 026, 028–030, extra-5). The plain-text stems and choices of the extra and fast-practice questions (e.g. "25×28 = ?", "3526") are now TeX with thousands commas.
- Fixed: q-008 (self-contradicting "every column writes 1"), extra-2 (unclear "shared offset"), extra-1…7 and fast-practice 1–7 (word-only solutions now show every number), q-040 and q-018 (colon fractions), q-037 (odd `\text{odd}` font).

## 5. Practice
- Removed near-duplicates: q-003 and q-033 (two-digit borrowing, same as q-031), and q-004 (adding a negative, same as q-032).
- Mixed practice is ordered easy → hard and ends with 6 exam-level items (brackets, fraction bar, must/could/cannot, "distinct", −1 < x < 0).
- Fast-calculation practice is ordered easy → hard and ends with an estimation item.
- Exam-level items in the topic: about 16 new ones (must/could/cannot, vocabulary traps, bracket traps, estimation).
- New questions: the correct answer is in a different position from one question to the next. Every distractor comes from a real mistake, and every solution names the trap.

## Memory cards
- **Number words:** remainder example uses ÷. Even/odd says "k an integer". Consecutive says "even/odd: by 2". New row "Nonzero". New tip: the three facts the exam prints.
- **Signs and the times table:** "Two signs touching" (was "side by side"). New tips on the last-digit check and on estimating.
- **Order of operations:** ÷ instead of ":". New tip on a minus before brackets. The split-numerator tip now has a correct example.
- **Fast-calculation toolkit:** ×10 ÷ 2 etc. instead of ":". The ×9 example is added (now taught). New tips: what "²" and "%" mean.

## For the teacher to decide
- **Skip test for strong students:** the review asks for 8 questions at the start of each lesson. The course has no mechanism for this. I added one spoken line in Add/Sub slide 1 instead.
- **Fast Calculation position:** it is still after the mixed practice (section 6). The review suggests moving it earlier. I left the order and moved the three questions that needed it instead.
- **Colon line:** Mult/Div slide 3 now says that some books use ":" for division. Delete it if you prefer not to mention ":" at all.
- The new videos use "could be true". Topic 20 uses "can be true". You may want the same word in both topics.
