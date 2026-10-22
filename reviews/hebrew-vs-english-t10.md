# Topic 10 (Exponents & Roots, Techniques): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 5358-6606 (all of it read). Her structure note (5358):
  "חזקות ושורשים - תאוריה שאלה סרטון 5 פעמים" = theory, question, video, five times. Closing note (6604): 15 practice questions
  "expressions and equations" without videos, then a 20-question mixed practice.
- English: `scratchpad/ext/course/t10.txt` / `q10.txt` (no reading scripts for topic 10 except the summary), the current
  question choices from `~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html`, and the base translation `base-v18.html`.
- Recording status: `video_status.py` does not track topics 1-12. **Every topic-10 video has an older camera take**
  (7 Oct 2026, `~/Documents/Course.recordings/1 Algebra/Topic 10 …`: powers-techniques, r26-t10-power-traps and all 8 solution
  videos). By the production plan topics 1-12 are redone LAST (first lesson on camera, the rest AI), so every restore below
  goes into that redo; nothing must be re-recorded now.

**Match scale** as in the t23 model; new numbers alone are not a change.

**The big structural change.** The base translation followed her order: one long lesson with all five theory parts (dividing
roots, number over a root, smallest prime base, negative exponents, adding roots two ways, power equations, root equations),
then the five questions. **The current English lesson stops after "Number over a root"**; the other theory parts were moved
into the question videos that first use them (memory rule *teach in question videos*). This is actually closer to her own
"theory, question" rhythm. What matters is what got lost on the way; see rows 3a-3b and the distractor tip.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | חלוקה בשורש · Dividing roots | 5360-5428 | √12/√3 two ways: (1) under one root, 12/3 = 4 → 2; (2) split √12 = √4·√3 and cancel √3. "I personally prefer splitting": easier when there are several roots to cancel | `powers-techniques` slide 2 (√150/√6) | SAME |
| 1b | מספר שלם לחלק לשורש · Whole number over a root | 5429-5491 | 6/√2: "you actually can put it under a root: 6 = √36", but easier: 6 = 3·2, 2 = √2·√2 (√2² cancels) → 3√2. 20/√5: 10·2 or 4·5, choose 4·5 because of the 5 below → 4√5 | slide 3 (10/√2; 18/√6, choose 3·6 because of the 6 below) | SAME |
| 1c | קיצור: מתעלמים מהשורש · Shortcut: ignore the root, add it back | 5492-5575 | Used a lot in geometry (silver/gold triangles, hypotenuse → leg); "1.5 seconds, zero mistakes": (1) ignore the root, (2) add the root to the result; shown on 6/√2 and 20/√5 | slide 3 (10/√2, 18/√6) | SAME |
| 1d | פירוק לגורמים - חזקות · Powers: one base, the smallest prime | 5576-5600 | Different bases on top and bottom → make all bases the same, "preferably the smallest possible", i.e. prime factors | solve-q-248 slide 1 (opening) | SAME (moved from the lesson into the question) |
| 2 | שאלה 1: 9⁸·8⁻³ / (3¹²·4⁻³) · Q1, powers | 5601-5777 | 9 = 3², 8 = 2³, 4 = 2²; power of a power; subtract top − bottom: 16 − 12 = 4, (−9) − (−6) = −3 ("minus minus is plus") → 3⁴·2⁻³, choice 4. Warning: the answer may be written as 3⁴/2³, and WHY: 2⁻³ → reciprocal ½, (½)³ = 1/2³, so a negative power "lives in the denominator" | solve-q-248 (4⁵·27⁻² / (2⁷·9⁻²) → 2³·3⁻²) | SAME (every step, plus the "could appear as 2³/3²" warning. Her short re-derivation of WHY the factor moves down is cut to one line, "the negative exponent just moves it to the bottom"; topic 8 slide 4 taught it. English adds Method 2 "pair the families" and the trap choice 4) |
| 3a | חיבור וחיסור שורשים - פירוק לגורמים · Adding roots by splitting | 5778-5996 | √8 + √18: split so one part comes out whole (9·2, not 6·3, or you "stay stuck with roots"); like 2x + 3x = 5x. Then √12 + √48: √48 = √4·√12 gives √3 and √12, "apples and bananas"; she tries 6·8 and 2·24 (nothing whole), then 16·3 → 6√3. "48 = 4·12 or 6·8 is what you see; 16·3 not everyone notices; hard for weaker students" → so a second method | solve-q-249 slide 1 (√72, √98, √32) + the first lines of slide 2 | PARTIAL: the split rule ("why 36: it comes out whole"), "like 7x − 4x" and "apples and bananas" are there. **Missing: her live dead-end demonstration** (a split that leaves √3 and √12, then trying 6·8 and 2·24 before 16·3). English replaces it with one spoken sentence ("many people see 9 times 8, three root eight, and root eight still hides a square") and never shows two roots that won't add. Her second pair (√12 + √48) is not used anywhere |
| 3b | חיבור וחיסור שורשים - גורם משותף · Adding roots by a common factor | 5997-6126 | "Ignore the roots": 8 and 18 share 2 → √2(√4 + √9); **check yourself: √2·√4 = √8, √2·√9 = √18**; = 5√2. √12 + √48: common factor 12 → √12(1 + √4) = 3√12 → then split 12 (easy now) → 6√3. "Simpler, especially for students weaker in algebra" | solve-q-249 slide 2 (√72 + √72 = 2√72; √98 − √32 = √2(√49 − √16) = 3√2) | PARTIAL: the method, "most of us are good at a common factor" and "if algebra isn't your strongest side" are there. **Missing: (a) the self-check step** (multiply back: √2·√49 = √98); **(b) the case where the common factor is one of the roots itself** (√12(1 + √4)), which is the case that makes this method beat splitting. The base translation had both on a lesson slide ("Adding roots: factor"); they were lost when the slide was folded into q-249 |
| 4 | שאלה 2: (√18+√18)/(√50−√8) · Q2, root fraction | 6127-6300 | Why add first: you can't cancel until it's all multiplication. (1) Split: 9·2 (not 6·3), 25·2 (not 5·10), 4·2 → 6√2 / 3√2 = 2. **Tip: "optical distractors": the answer 2 always sits in choice 2; √3 in choice 3; even 1/3 in choice 3 and 1/2 in choice 2.** (2) Common factor: 2√18 / √2(√25 − √4) → (2/3)·√9 = 2. "Whichever is more convenient; you always get the same result" | solve-q-249 (choices 4√2, 2, 16, 4 → 4, choice 4) | PARTIAL: both methods, "can't cancel yet" and "pick whichever is easier" are there. **Her distractor tip is gone.** The base q-249 had it ("the answer three sits in choice three…"); the current script dropped it. It still works with the English numbers (2 is in choice 2, 4 in choice 4). The basic tip is taught once in English, topic 5 (`solve-q-135`, "A side tip about the exam: no visual traps…"), but her extension (similar-looking values: √3 → choice 3, 1/3 → choice 3, 1/2 → choice 2) is taught only here and is now missing |
| 5 | משוואות מעריכיות · Exponential equations (theory) | 6301-6315 | Unknown in the exponent: make the bases equal, then the exponents | solve-q-250 slide 1 (opening) + slide 2 "When it works" (positive base ≠ 1) | SAME (moved into the question; English adds the base ≠ 1 restriction) |
| 6 | שאלה 3: 4^(3x) = (1/8)^(5−3x) · Q3, exponential equation | 6316-6465 | **Quick glance at the distractors: 5 is in choice 1 because 2, 3, 4 occupy their own places.** 4 = 2², 1/8 = 2⁻³ (via the reciprocal (½)³); **tip: ignore the fraction, 8 = 2³, the fraction adds the minus**; multiply exponents (−3·−3x = +9x); same base → equal exponents: 6x = −15 + 9x → x = 5. Recap; **tip: always the SMALLEST base** (16, 1/8, 8, 4 → all 2), "so you don't get stuck with 2, 4, 8 and bigger numbers" | solve-q-250 (9^(2x) = (1/27)^(2−2x) → x = 3) | PARTIAL: equal bases, the "ignore the fraction, add a minus" tip and "always the smallest base" are there; English adds Method 2 (check the answer) and the trap 3/5. **Missing: her distractor glance.** With the English choices (1, 3/5, 3, −3) it would read "1 in choice 1, 3 in choice 3"; it does not single out the answer here, so it is weaker than in her version |
| 7 | משוואות עם שורשים · Root equations (theory) | 6466-6478 | Get rid of the root: square both sides | solve-q-251 slide 1 | SAME (moved into the question) |
| 8 | שאלה 4: √(x−5) = 2 · Q4 | 6479-6518 | Square both sides, the square cancels the root: x − 5 = 4 → x = 9, choice 1 | solve-q-251 (√(x−6) = 5 → 31) | SAME (English adds the check and two traps) |
| 9 | שאלה 5: x√3 = 3√x · Q5 | 6519-6600 | "Many students rush to put the coefficient inside the root": allowed, but squaring is easier; 3x² = 9x → ÷3x → x = 3; for those confused, step by step: ÷3 → x² = 3x, then ÷x | solve-q-252 (x√6 = 6√x → 6) | SAME (English adds: divide by x only because x ≠ 0 is given; otherwise factor and keep 0 and 6) |
| 10 | 15 + 20 שאלות תרגול · 15 practice questions + 20-question mixed practice | 6604 (note) | (no transcript) | units `unit-t10-2` "Expressions and equations" (16) and `unit-t10-3` "Mixed practice" (24) | SAME |

**Count by row (14 rows):** SAME 10 · CHANGED 0 · PARTIAL 4 (3a, 3b, 4, 6) · MISSING 0. (No row is CHANGED: the moves of
theory into the questions keep her order theory → question.)

### Count by video (her 10 units: 5 theory parts + 5 questions, plus the practice)

| Unit | Match |
|---|---|
| Theory 1: dividing roots, number over a root, shortcut, one base (1a-1d) | SAME |
| Q1 powers fraction (2) | SAME |
| Theory 2: adding roots, two methods (3a-3b) | PARTIAL (dead-end demonstration, self-check and the √12(1+√4) case missing) |
| Q2 root fraction (4) | PARTIAL (distractor tip missing) |
| Theory 3: exponential equations (5) | SAME |
| Q3 (6) | PARTIAL (distractor glance missing) |
| Theory 4: root equations (7) | SAME |
| Q4 (8) | SAME |
| Q5 (9) | SAME |
| Practice (10) | SAME |

**By video: SAME 7 · CHANGED 0 · PARTIAL 3 · MISSING 0.**

---

## 2. English → Hebrew (added, no Hebrew equivalent)

| English video / part | Added content | Hebrew source? |
|---|---|---|
| solve-q-248 slide 2 | Method 2 "pair the families" (4 with 2, 27 with 9); the trap −6 + (−4) | none |
| solve-q-250 slides 2-3 | Base must be positive and ≠ 1; Method 2: check the answer | none |
| solve-q-251 (part) | Check in the original; traps 11 and 25 | none |
| solve-q-252 (part) | Dividing by x only when x ≠ 0 is given; otherwise factor (0 and 6) | none (she divided by 3x without comment) |
| solve-q-r26-t10-01 | √(2x+3) = x: a root is never negative, fake solutions after squaring, check in the original | none in topic 10 (her topic-11 question √x(√x−6)=0 is related) |
| r26-t10-power-traps | Same exponent, different bases: multiply the bases | her topic-8 rule, reminded |
| solve-q-r26-t10-02 | 2¹⁰ + 2¹⁰ + 2¹⁰ + 2¹⁰ = 2¹²: count the copies | none in topic 10 (her topic-11 question 4ˣ = 4ʸ+4ʸ+4ʸ+4ʸ) |
| solve-q-r26-t10-03 | 3^(x+2) − 3^x = 72: take out the smallest power; try the choices | none |
| r26-t10-summary | Replaced by the summary page | none |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **Distractor tip, with her extension**: "the answer 2 always sits in choice 2; and a similar-looking value too: √3 → choice 3, 1/3 → choice 3, 1/2 → choice 2" | solve-q-249 slide 1, after "Choice four" (2 sentences). With the English choices: "four sits in choice four, and two in choice two" | yes (old camera take, 7 Oct); goes into the AI redo | **Restore.** It was in the base, it still works with the new numbers, and the extension is taught nowhere else in English |
| 2 | **Common factor: the self-check** (multiply back: √2·√49 = √98, √2·√16 = √32) | solve-q-249 slide 2, one sentence after "root forty-nine minus root sixteen" | yes (old take) | **Restore.** One sentence; it is her habit of checking a factorisation, and the base had it |
| 3 | **Common factor when it is one of the roots** (√12 + √48 = √12(1 + √4) = 3√12 = 6√3), and why it beats splitting there | solve-q-249 slide 2 as a 2-3-sentence second example (with new numbers, e.g. √20 + √80 = √20(1 + √4) = 3√20 = 6√5), or a practice question | yes (old take) | **Restore (short).** It is the case that shows WHY the second method exists; with only √72 + √72 the common factor looks trivial |
| 4 | The dead-end demonstration (two roots that won't add; trying 6·8, 2·24, then 16·3) | solve-q-249 slide 2, where English now says "many people see 9 times 8" | yes (old take) | Optional. English keeps the point in one sentence; showing it costs ~3 sentences |
| 5 | Q3 distractor glance | solve-q-250 slide 1 | yes (old take) | Not needed if #1 is restored (one place is enough; with the English choices it does not single out the answer) |
| 6 | Q1: her re-derivation of why a negative power moves to the denominator | solve-q-248 slide 1 | yes (old take) | Not needed; taught in topic 8 slide 4 and reminded in one line |

Nothing in English contradicts her. The English additions (x ≠ 0 before dividing, base ≠ 1, check after squaring) are correct
and safer than her versions.
