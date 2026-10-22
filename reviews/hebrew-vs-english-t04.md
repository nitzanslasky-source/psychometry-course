# Topic 4 (Expressions — Fundamentals): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 2273-2547 (the first part of source 5, up to her
  note "then 20 questions of תרגול עצמי"; all of it read). Line numbers below are file lines.
- English: topics 1-12 have no reading scripts yet, so the English side is `scratchpad/ext/course/t04.txt` and `q04.txt`
  (31 questions), the base translation `base-v18.html`, and the current flow order in
  `~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html` (expression-basics → r26-t04-formulas → q-120 → q-121 → four
  r26 questions → summary → practice).
- **Recording status.** Topic 4 is not in `video_status.py` (it covers only the Reading Studio topics). Her older English
  takes exist for `expression-basics`, `solve-q-120` and `solve-q-121` (in `real_exam/added_by_nitzan.json`; recorded when
  the formulas were still inside expression-basics). `r26-t04-formulas`, the four r26 solution videos and the summary have
  none. Topics 1-12 are redone LAST in the plan, so any restore goes into the redo scripts.

**Her structure** (note at 2275): "video, question, video, question": one lesson (algebraic terms, brackets, common factor,
the three formulas), then two exam questions with solution videos, then 20 practice questions. English ids follow her
order: her Q1 = `solve-q-120`, Q2 = `solve-q-121`. New numbers alone are not a change.

SAME = same idea and every one of her methods. CHANGED = same idea, different method / example / place. PARTIAL = part of
her content missing. MISSING = no English equivalent.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| L1 | איברים אלגבריים – פתיחה · Intro | 2278-2284 | Terms made of numbers and unknowns; collecting, opening brackets, common factor; "students usually remember this, a review" | `expression-basics` slide 1 | SAME |
| L2 | מקדם ונעלם · Coefficient and unknown | 2285-2293 | 3x = 3 times x; the textbook names don't matter | `expression-basics` slide 2 (5x; hidden coefficient 1 and −1) | SAME |
| L3 | כינוס איברים · Collecting like terms | 2294-2324 | Only the same kind; 3x + 4y can't combine; 3x − 2x = x ("someone took 2 of them"); 4y − y = 3y; −2x² + 4x²: the sign joins the number after it, so rewrite as +4 − 2 → 2x²; coloured families | `expression-basics` slide 3 (5x − 2x "someone took two", 6y − 2y, −3x² + 7x²) | SAME (English adds roots as a family: 3√5 − √5) |
| L4 | כפל איברים · Multiplying terms | 2325-2344 | Multiply the coefficients, then the letters: 4a · 3b · 2a = 24a²b; why the order may change (4a is 4 times a; in multiplication order doesn't matter); powers first is the custom, 24ba² is not wrong | `expression-basics` slide 4 (30a²b) | SAME (English adds 2a + 3a vs 2a · 3a and a · a³) |
| L5 | פתיחת סוגריים · Opening brackets | 2345-2378 | Nothing written = times; 3(2x − 5): the minus belongs to the 5, so 6x − 15; the written middle step is only for the explanation, in practice jump straight to the answer; a minus before brackets = ×(−1): −(3y − 2) = −3y + 2, "it just changes every sign" | `expression-basics` slides 5-6 | SAME |
| L6 | פתיחת שני סוגריים · Two brackets | 2379-2399 | First term times each, then the second times each: (x + 4)(3x − 7) = 3x² − 7x + 12x − 28; the long line is "only pedagogical"; collect −7x + 12x = 5x | `expression-basics` slide 7 ((x + 6)(x + 2); (x − 5)(x + 2)) | SAME |
| L7 | הוצאת גורם משותף · Taking out a common factor | 2400-2450 | "Very, very important, the same level as adding fractions"; a factor builds a number by multiplication only (6 = 2·3; 8 = 2·4 = 2·2·2); 2a² − 6a + 8: break into building blocks, a is not in the 8, 2 is in all → 2(a² − 3a + 4), keep the minus; check by opening; **why**: it turns a sum into a product, so later we may cancel in fractions | `expression-basics` slide 8 (6x + 15; 3a² − 12a + 6, the same reasoning and check, and the same "why") | SAME (English adds an easier first example and slide 9, a whole bracket as the factor) |
| L8 | נוסחאות הכפל המקוצר · The three contracted multiplication formulas | 2451-2479 | They appear a lot; you can always open brackets, the formulas save mess; (a + b)² = a² + 2ab + b²; (a − b)²: "with plus, everything is plus; with minus, the minus is only on 2ab"; (a + b)(a − b) = a² − b² | `r26-t04-formulas` slides 1-2, 4 (a separate video right after `expression-basics`) | CHANGED: same content, but moved from her one lesson into its own video (the base translation still had them inside expression-basics). English adds the numeric tests (3 + 2)² = 25 vs 13 and (5 − 3)² |
| Q1 | (x + y)² − (x − y)² (exam question) | 2481-2522 | Expand both formulas; **put the second expansion in brackets because of the minus in front**: "many students fall here; don't try to save steps; the questions are short enough, a few more seconds but correct"; the minus flips; cancel → 4xy; **nuance: "מתבטל" (equal terms cancel to 0 in + / −) vs "מצטמצם" (reduce, only in fractions)** | `solve-q-120` ((m + n)² − (m − n)², Method 1) | SAME (her "don't save steps / a few extra seconds" kept; the cancel-vs-reduce nuance moved to `expression-basics` slide 8; English adds Method 2, plug in 3 and 2, and why not 0 or 1) |
| Q2 | (a − 1)(a + 1) − (b − 1)(b + 1) | 2523-2538 | Recognise the third formula: a² − 1; keep the minus and the brackets: −(b² − 1); open: −1 + 1 cancel → a² − b² | `solve-q-121` ((x − 3)(x + 3) − (y − 3)(y + 3), Method 1) | SAME (English adds Method 2, plug in) |
| R | סיכום · Recap | 2539-2545 | The two important things: the common factor and the formulas | `r26-t04-formulas` slide 11 ("Two big takeaways…"); `expression-basics` slide 10 | SAME |

**Counts (11 items):** SAME 10 · CHANGED 1 (L8, moved into its own video) · PARTIAL 0 · MISSING 0.

---

## 2. English → Hebrew (English topic-4 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Her take? |
|---|---|---|---|
| `expression-basics` slide 9 | A whole bracket as the common factor | none | no (added after her take; the base had no such slide) |
| `r26-t04-formulas` slide 3 | Power first: 3(x + 3)² and −x² vs (−x)² | none | no |
| `r26-t04-formulas` slide 5 | Number shortcuts: 98 · 102, 31² − 29² | none | no |
| `r26-t04-formulas` slides 6-7 | Formulas backward (9x² − 25, x² + 12x + 36); the perfect-square check | none (the base had "Formulas backward") | no |
| `r26-t04-formulas` slides 8-9 | Value without x: a² + b² from a + b and ab; a² − b² from sum and difference; x + 1/x | none | no |
| `solve-q-r26-t04-01, -02, -03, -04` | x² + y² from sum and product; 51² − 49²; (a − b)² = (b − a)²; x² + 1/x² | none | no |
| `r26-t04-summary` | Summary (replaced by the printable summary page) | none | — |

**English inconsistency (not against her, but found here).** `r26-t04-formulas` slide 7 says "For those, there is the
sum-product method. It comes later in this topic", and the topic-4 summary reviews "factoring a trinomial: find two
numbers… sum eleven, product thirty". But no topic-4 video teaches the sum-product method. In topic 5, `solve-q-127` opens
with "You know sum and product from Topic 4", and only `r26-t05-shortcuts` gives a quick reminder. Either teach it in
topic 4 (one slide in `r26-t04-formulas`) or change the wording in all three places. (See also the topic-5 report.)

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | L8 placement: the formulas inside her lesson | — | — | Not needed. The split into `r26-t04-formulas` keeps every word of hers and comes straight after, before her two questions |
| 2 | L3: "rewrite −2 + 4 as +4 − 2" for −2x² + 4x² | `expression-basics` slide 3 (1 sentence) | her old take exists; topic in the 1-12 redo | Optional, minor; English already says "every minus travels with the term after it" |

Nothing of hers is missing and nothing is wrong compared with her. Fix the sum-product wording above (English-only issue).
