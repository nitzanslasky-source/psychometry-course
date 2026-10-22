# Topic 6 (Equations — Fundamentals): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 3666-3893 (the first part of source 6: the single
  equation and systems of equations, up to her note "then 20 questions of תרגול משוואות יסודות מסכם"; all of it read).
  Line numbers below are file lines.
- **Boundary.** Her next block, "משוואות תאוריה" (7 questions with a video after each, lines 3895-4139), is **not** topic 6:
  its questions are `q-191` … `q-197`, which the English course puts in topic 7 (`equation-strategy` + `solve-q-191` …
  `-197`, both in the base translation and in the current flow). It is covered in the topic-7 report.
- English: topics 1-12 have no reading scripts yet, so the English side is `scratchpad/ext/course/t06.txt` and `q06.txt`
  (43 questions), the base translation `base-v18.html`, and the current flow in
  `~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html` (linear-equations → q-171 → r26-t06-02 → r26-t06-01 → summary
  → systems → q-164 → q-165 → r26-t06-03 → r26-t06-04 → summary 2).
- **Recording status.** Topic 6 is not in `video_status.py` (it covers only the Reading Studio topics). Her older English
  takes exist for `linear-equations`, `systems`, `solve-q-171`, `solve-q-164` and `solve-q-165` (in
  `real_exam/added_by_nitzan.json`). The four r26 solution videos and the two summaries have none. Topics 1-12 are redone
  LAST in the plan, so any restore goes into the redo scripts.

**Her structure** (notes at 3668-3669, 3810-3811, 3891-3893): "video, question, video": the single-equation lesson, one
question, 5 practice questions; then the systems lesson, two questions, 5 practice questions; then 20 summary questions.
English ids: her single-equation question = `solve-q-171`; her two systems questions = `solve-q-164`, `solve-q-165`.

SAME = same idea and every one of her methods (new numbers only). CHANGED = same idea, different method / example /
place. PARTIAL = part of her content missing. MISSING = no English equivalent.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| E1 | משוואה בודדת – פתיחה · Why equations | 3672-3679 | A basic technique for algebra, word problems and geometry; solving = finding the unknown's value by isolating it | `linear-equations` slide 1 | SAME |
| E2 | בידוד הנעלם · Isolating x | 3680-3717 | Two sides and the equals sign; **whatever you do to one side you must do to the other**; 2x − 5 = 3: add 5 to both sides (−5 + 5 cancel), 2x = 8, divide both by 2, x = 4; check in the original | `linear-equations` slide 2 (4x + 7 = 31) | SAME (English adds "move it across and flip the sign is shorthand for the same thing") |
| E3 | הנעלם לא חייב להיות משמאל · x on either side | 3718-3723 | You don't have to isolate on the left; put the unknown where it comes out positive | `linear-equations` slide 2, last line | SAME |
| E4 | אין סוף פתרונות · Infinitely many solutions | 3725-3746 | Simplifying makes both sides identical, independent of x: 2x² + 6 = 2(x² + 3); cancel 2x² from both → 6 = 6, always true, x can be any number | `linear-equations` slide 4 (5(x + 2) = 5x + 10) | SAME |
| E5 | אין פתרון · No solution | 3748-3769 | A contradiction: 4x − 5 = 2x + 2(x − 3) → 4x − 5 = 4x − 6 → −5 = −6, false, so no x works | `linear-equations` slide 3 (5(x + 2) = 5x + 7) | SAME (English shows no-solution first) |
| E6 | משוואה עם שברים · Equations with fractions | 3770-3774 | Common denominator on both sides, then get rid of the denominator | `linear-equations` slide 5 | SAME (English adds a worked example and the restriction there) |
| EQ | 2/(x − 2) = 1/(x − 1) (her question) | 3776-3808 | **Restriction first: x ≠ 1, 2** (a zero denominator is undefined); common denominator (x − 2)(x − 1); in an equation you may cancel the same denominator on both sides = multiplying both sides by it; **"I could have come here directly by cross-multiplying — allowed when two fractions are equal"**; 2x − 2 = x − 2 → x = 0 | `solve-q-171` (4/(x − 2) = 3/(x − 3) → 6), Method 1 | SAME (English adds the cross-multiplying trap −1 and Method 2, test the choices) |
| S1 | מערכת משוואות – פתיחה · Systems intro | 3813-3828 | More than one equation (2, sometimes 3-4); mostly in algebra questions, rare in word problems or geometry; the difficulty is technical; first technique: isolate and substitute | `systems` slide 1 | SAME |
| SQ1 | 6x + 3y = 27, x + y = 5 (find x) | 3830-3862 | As many equations as unknowns → solvable; **isolate and substitute; they want x, so isolate y — it disappears and you are left with the letter you want**; y = 5 − x into the first → 3x = 12, x = 4. Then she introduces technique 2, adding/subtracting equations, "usually more convenient and faster, though not always" | `solve-q-164` (8x + 4y = 44, x + y = 9), Method 1 + `systems` slides 2-4 | SAME (English adds Method 2, divide the first equation by 4 first, and the trap 11) |
| SQ2 | 3x + y = 25, 2x + 3y = 33 (find x) | 3864-3889 | **Match coefficients**: you could match the x's (×2 and ×3 → 6x), but they want x, so match the y's: first equation ×3 → 9x + 3y = 75, "the same equation, just expanded, both sides"; subtract → 7x = 42 → x = 6 | `solve-q-165` (4x + y = 22, 3x + 2y = 24), Method 1 + `systems` slide 6 | SAME (her "could match the x's instead" kept; English adds Method 2, substitution, and the trap 20) |

**Counts (10 items):** SAME 10 · CHANGED 0 · PARTIAL 0 · MISSING 0.

---

## 2. English → Hebrew (English topic-6 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Her take? |
|---|---|---|---|
| `linear-equations` slide 5 (part) | A worked x-in-the-denominator example with the restriction | her EQ (pre-taught) | yes |
| `linear-equations` slide 6 | Cross-multiply, with its condition (one fraction on each side) | her EQ line "I could have cross-multiplied" (pre-taught) | no (not in the base) |
| `linear-equations` slide 7 | A forbidden answer → no solution | none | no |
| `linear-equations` slides 8-9 | Fractions & brackets; a minus before a fraction (put the numerator in brackets) | none | slide 8 yes, slide 9 no |
| `linear-equations` slide 10 | Don't divide by x: a product equals zero | her topic-7 theory Q1 (3898-3945), pre-taught here | yes |
| `linear-equations` slide 11 | Test the choices | none in topic 6 | no |
| `systems` slides 5, 7-9 | x + y and x − y (half the sum, half the difference); ask what they want; get x + y directly; multiply / divide the equations | none (her topic-7 questions use some of these) | slide 7 yes; 5, 8, 9 no |
| `solve-q-r26-t06-01` | A minus before a fraction (common denominator 6) + test the choices | none | no |
| `solve-q-r26-t06-02` | The forbidden answer → no solution | none | no |
| `solve-q-r26-t06-03` | Add the equations to get x + y directly | none | no |
| `solve-q-r26-t06-04` | Multiply a product and a quotient | none | no |
| `r26-t06-summary`, `r26-t06-summary-2` | Summaries (replaced by the printable summary page) | none | — |

**Repeats to consider (memory rule *teach-in-question-videos*).** As in topic 5, the English lessons pre-teach what she
teaches inside her questions, and then the question videos teach it again:
- "isolate the letter they don't ask for, so it disappears" is in `systems` slide 3 AND in `solve-q-164`;
- "match the letter they don't ask for" is in `systems` slide 6 AND in `solve-q-165`;
- cross-multiplying is in `linear-equations` slide 6 AND in `solve-q-171`.
In her course each of these is taught once, in the question. For the 1-12 redo, the lessons could keep only the general
method and leave the tip to the question video (about 30-45 seconds saved). Not urgent: the repeats are short.

---

## 3. Missing from English: restore?

Nothing of hers is missing, and nothing is wrong compared with her. Every method and tip she gives (both sides,
check in the original, put x where it is positive, infinite vs no solution, restriction first, cancel a common
denominator only in an equation, cross-multiplying for fraction = fraction, isolate / match the letter they don't
ask for, as many equations as unknowns) is in the English and still works with the English numbers.

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| — | none | — | — | No restore needed |
