# Topic 4 — Expressions: Fundamentals — changes (course review 2026-09)

Patch: `math_patches/t04.py`. Check: `python3 math_check.py 4` gives 0 problems, 0 warnings and 0 layout problems.
I solved every new or changed question again and checked each key against its solution video.

## Summary
- Questions rewritten: 25 (Q1, Q2 and 23 practice items)
- Questions added: 19 (6 guided with solution videos, 13 practice)
- Questions removed: 4 (near-duplicates)
- Videos added: 8 (2 lessons and 6 solution videos)
- Slides: 1 lesson video split into 2. 8 existing slides changed (6 in the first lesson, 2 of the moved formula slides). 16 new lesson slides. 2 slides changed in the Q1 video.
- Memory cards: 1 updated, 1 new ("Factoring trinomials")
- New methods: factoring trinomials with the sum-product method; finding a value without finding x
  (a+b and ab give a²+b²; a+b and a−b give a²−b²; x+1/x gives x²+1/x²); difference of squares with numbers;
  "power first" for 3(x+3)² and −x² vs (−x)²; the perfect-square check; a whole bracket as a common factor;
  a·a³ = a⁴; how to choose numbers when you plug in.

## Priority 1 — wrong rules
The review found no false math statements in this topic. It did find a board/voice mismatch on slides 2 and 4.
The board items are there: they are "row" items, which the review export (student_view.py) does not show.
The slide renders show them. I made the slide 4 draw note clear:
"Under 2a + 3a write = 5a; under 2a · 3a write = 6a²".

## Priority 2 — methods added
### Lesson "Expressions — Fundamentals" (expression-basics). It is now 10 slides; the formulas moved to a new video.
- Slide 1: "so let's review…" is now two sentences. It says that the formulas come in the next video.
- Slide 3 (like terms): new board item 3√5 − √5 = 2√5. "Roots work the same way" (needed for q-101). Spelling "color".
- Slide 4 (multiplying terms): new item a · a³ = a⁴, "count the a's" (needed for q-103, q-104).
- Slide 7 (two brackets): a second example with a minus: (x − 5)(x + 2) = x² − 3x − 10.
- Slide 8 (common factor): the "equal terms CANCEL, fractions are REDUCED" remark moved here from the Q1 video.
- NEW slide 9 "Bracket as a factor": x(a+b) + 3(a+b) = (a+b)(x+3), and a(x−2) − 5(x−2) = (x−2)(a−5).
- Slide 10 (recap): rewritten for the first half of the lesson.

### NEW lesson "Multiplication Formulas" (r26-t04-formulas, 11 slides)
- Old slides 9–12 ((a+b)², (a−b)², sum × difference, formulas backward) moved here. Only the first line changed, plus the spelling "recognize … backward".
- NEW "Power first": 3(x+3)² = 3x² + 18x + 27, not (3x+9)². Also −x² vs (−x)² with x = 3 (−9 vs 9).
- NEW "Number shortcuts": 98 · 102 = 100² − 2² = 9996, and 31² − 29² = 2 · 60 = 120.
- NEW "Perfect-square check": the 3-step checklist from the review, shown on 9x² − 12x + 4 = (3x − 2)². Also a failing example (x² + 10x + 16), which points to the sum-product method.
- NEW "Value without x" (2 slides): a+b = 7 and ab = 10 give a²+b² = 29; a+b = 5 and a−b = 3 give a²−b² = 15; (x + 1/x)² = x² + 2 + 1/x².
- NEW recap slide.

### NEW lesson "Factoring Trinomials" (r26-t04-trinomials, 8 slides). The course had no lesson on this, but practice used it.
- From brackets to trinomial: (x+2)(x+3) = x²+5x+6. Sum 5, product 6. General rule (x+p)(x+q) = x²+(p+q)x+pq.
- Sum and product: x²+7x+10. Start from the pairs of the product. Check by opening.
- Signs: x²−7x+12 = (x−3)(x−4); x²+x−12 = (x+4)(x−3).
- Sign rules (4 lines) + x²+5x−6 = (x+6)(x−1).
- Common factor first: 2x²+10x+12 = 2(x+2)(x+3). Factor to reduce: (x²+5x+6)/(x+2) = x+3 (x ≠ −2).
- Check with a number: x = 0 does not catch the mistake (x+1)(x+6); x = 2 catches it (20 vs 24).
- Recap. New memory card "Factoring trinomials" follows the video.

### Guided questions (the topic had only 2; it now has 8)
| # | id | Question | Key | Methods in the video |
|---|---|---|---|---|
| 3 | q-r26-t04-01 | x+y = 6, xy = 5 → x²+y² | 3 (26) | square the sum; spot the numbers 1 and 5 |
| 4 | q-r26-t04-02 | 51² − 49² | 4 (200) | difference of squares; the long way |
| 5 | q-r26-t04-03 | which equals (a−b)² for all a, b | 2 ((b−a)²) | opposite brackets; plug in a = 5, b = 2 |
| 6 | q-r26-t04-04 | x + 1/x = 3 → x² + 1/x² | 1 (7) | square both sides; why not find x |
| 7 | q-r26-t04-05 | x² + x − 12 = ? | 2 ((x+4)(x−3)) | sum-product; plug in (why x = 0 fails: all choices give −12) |
| 8 | q-r26-t04-06 | (x²−9)/(x²+x−6) | 3 ((x−3)/(x−2)) | factor, then reduce; plug in x = 4 |

Q3–Q6 come after Q2. Q7–Q8 come after the trinomial lesson and its card. The sidebar of all 8 solution videos is now "Question 1 … Question 8".
The (a+b)²+(a−b)² twin that the review suggested as a question went into the Q1 video and solution as a "bonus" line.
The x + 1/x question replaces it.

### Q1 video (solve-q-120)
- Removed the "cancel vs reduce" remark (now in lesson slide 8). Added the twin identity (a+b)² + (a−b)² = 2a² + 2b².
- Plug-in slide: added the rule for choosing numbers. Use different numbers, not 0 or 1, and never a = b.

### Memory card "Multiplication formulas"
New rows: a²+b² = (a+b)²−2ab, (x+1/x)², a whole bracket as a common factor, 98 · 102.
New tips: power first, −x² vs (−x)², (b−a)² = (a−b)², the perfect-square checklist, a · a³ = a⁴.

## Priority 3 — text (all questions of the topic)
- Q1 and Q2: the stem "What is the value of the expression: … = ?" is now just the expression "… = ?". The solutions are in TeX and show a numeric check.
- All 23 kept practice items were rewritten in clean TeX. Each has a worked solution with the numbers.
  The one-line solutions of the t4-1-x items are gone (for example, t4-1-2 now shows 3x + 12 − 2x − 2 = x + 10).
- t4-1-1: "1x + 8y", "1x + 2y" became "x + 8y", "x + 2y".
- "(factor)" stems (q-113, q-116, q-119, t4-1-3) became "Which of the following is equal to …?".
  "For x≠3, simplify …" became "Given: x ≠ 3." on its own line.
- q-112, q-114, q-118: choices are in standard order (3x² + 18x + 27, not 3x² + 27 + 18x). The q-112 key moved to choice 3 (same answer).
- q-106 and new p19: the solution shows the plug-in shortcut (x = 2, x = 1).
- The colon warnings in q-111 and q-114 are gone (q-111 was removed; q-114 was rewritten).
- No "so" meaning "therefore" in the middle of a sentence. American spelling.
- Stems with two conditions use the stacked `\begin{cases}` form.
- The titles of the Q1/Q2 solution videos follow the new stems. The course convention is title = plain stem.

## Priority 4 — figures
No figures in this topic.

## Priority 5 — practice (26 → 35 items)
- Removed near-duplicates: q-108, q-109 (minus-bracket drills, like q-107 and q-110), q-111 (like q-112 and q-114), q-117 (like q-118).
- Added 13 exam-level items (q-r26-t04-07 … -19): a−b and ab → a²+b²; x+y and x−y → x²−y²; 1001² − 999²;
  x + 1/x = 4; x²−2x−15; x²−7x+12; (x²+x−6)/(x²−4); (2a+b)² − (2a−b)²; (a+b)² = 49 and (a−b)² = 9 → ab;
  (2021² − 2019²)/2020; x−y = 5 → x²−2xy+y²−2x+2y; x²−y² = 24 and x+y = 6 → x; (x+3)² − (x−3)(x+3) (plug-in friendly).
- The section is ordered easy → hard: terms → brackets → formulas → factoring → fractions → trinomials → "value without x" → hardest combined items.
- t4-1-3 (trinomial) is now taught before it is used.

## For the teacher to decide
- Split video: the formulas are now their own video ("Multiplication Formulas", about 5.5 min). The first lesson is about 7.5 min. If you prefer one long video, the slides can be merged back.
- Topic 5 practice also uses trinomial factoring (e.g. q-expression-extra-05). It can now point back to the topic 4 "Factoring Trinomials" video.
  Quadratic *equations* are still not taught anywhere (PLAN priority 2). That belongs to the equations topic.
- In the guided-question choices, fractions show at small (inline) size. The renderer seems to force inline style in choices. This is readable, but a renderer fix would help every topic.
- API note: `math_api` has no call to rename a video. I set `title`/`navLabel` of the solution videos directly in the patch.

## Pass 2 (2026-09-27, teacher-approved remove/restore plan)

**Removed:** the "twin identity" (a+b)² + (a−b)² = 2a² + 2b²: the draw note and the "Bonus" line on `solve-q-120`
slide 2, and the last line of the q-120 written solution. The trinomial lesson and questions stay (the plan keeps them);
guided numbering unchanged.

**Restored:**
- Practice q-108, q-109, q-111, q-117 back in `unit-t4-1` (original stems, choices, keys; TeX + numeric solutions),
  placed at their difficulty in the easy-to-hard order.
- The original `expression-basics` Recap content on the `r26-t04-formulas` Recap (which closes the old slides 9-12):
  "Circle the three formulas", "Two big takeaways from this lesson: taking out a common factor, and the three formulas",
  "Now try a question — then watch its solution video." The three formulas were already on that board.
- `mem-formulas`: the (a−b)(a+b) example is again 48·52 = 50² − 2² (= 2500 − 4 = 2496); the intro again says
  "Use them forward to expand and backward to factor." (American spelling), plus the kept "find values" sentence.

**Summary video** `r26-t04-summary` "Expressions: Summary" (about 2.2 min), last item of the learn section, right before
the practice. Slides: Summary · Like terms · Brackets · Common factor · The three formulas · Formula traps ·
Number shortcuts · Value without x · Trinomials · Before you practice.
