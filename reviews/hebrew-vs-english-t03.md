# Topic 3 (Fractions): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 1438-2270 (source 4; all of it read). Line numbers
  below are file lines.
- English: topics 1-12 have no reading scripts yet, so the English side is `scratchpad/ext/course/t03.txt` (every video's
  spoken text) and `q03.txt` (28 questions), checked against the base translation `base-v18.html`.
- **Recording status.** Topic 3 is not in `video_status.py` (it covers only the Reading Studio topics). Her older English
  takes exist for `compare-fractions` and all nine of her questions `solve-q-091` … `solve-q-099` (in
  `real_exam/added_by_nitzan.json`). `solve-q-fraction-compare`, `solve-q-r26-t03-01/-02/-03` and the summary have none.
  Topics 1-12 are redone LAST in the plan, so every restore goes into the redo scripts. Nothing needs re-recording now.

**Her structure** (note at 1440-1441): one lesson (comparing fractions), a short intro to the question part, then
"video, question, video, question": nine questions, each with a solution video, then 10 practice questions. The English
ids follow her order with no gaps: her Q1-Q9 = `solve-q-091` … `solve-q-099`. New numbers alone are not a change.

SAME = same idea and every one of her methods. CHANGED = same idea, different method / example / order. PARTIAL = part of
her content missing. MISSING = no English equivalent.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| L1 | השוואת שברים – פתיחה · Intro | 1443-1448 | Now psychometric questions; from the basics up to exam questions | `compare-fractions` slide 1 | SAME |
| L2 | הערכת סדר גודל – חצי · Benchmark ½ | 1449-1480 | 5/11 vs 9/17: half of 11 is 5.5, 5 is less → below ½; half of 17 is 8.5, 9 is more → above ½; two ways to see it (via the numerator ×2, or the cakes: 5 cakes for 11 kids < 5 for 10); **her tip: work from the denominator to the numerator** | `compare-fractions` slide 2 (5/13 vs 8/15) | SAME |
| L3 | השוואת מונים ומכנים · Same top / same bottom | 1481-1491 | Same denominator → bigger top wins (more cakes); same numerator → smaller bottom wins ("fewer kids fighting over the cake") | `compare-fractions` slide 3 | SAME (her "fewer kids fighting over the cake" kept) |
| L4 | הרחבה למונה משותף · Make them match | 1492-1501 | 5/11 vs 15/34: expand 5/11 ×3 to 15/33; same cakes, 33 vs 34 kids | `compare-fractions` slide 4 (the same numbers) | SAME |
| L5 | כפל באלכסון · Cross-multiplication | 1502-1536 | 3/8 vs 4/11: no common denominator of 88; 8·4 = 32, 11·3 = 33; **write each product ABOVE its numerator, or the answer comes out backwards**; "the best and most important technique… it always works; easier to remember one method than 1, 2, 3"; **don't fear bigger numbers: 11·9 = 99, 17·5 = 10·5 + 7·5 = 85** | `compare-fractions` slide 5 (5/8 vs 7/11 = 55 vs 56) | PARTIAL: her third example (bigger-looking products done by splitting, "don't be afraid") is missing. English adds why it works (a hidden common denominator) and the positive-bottom condition |
| L6 | המרה לעשרוני · To decimals | 1537-1554 | 2/5 vs 3/8: know 1/5 = 0.2 (100 ÷ 5 = 20) and 1/8 = 0.125 → 0.4 vs 0.375; but cross-multiplying is simpler (15 vs 16) | `compare-fractions` slide 7 (the same numbers) | SAME |
| L7 | השלמה ל-1 · Distance from 1 | 1555-1567 | 16/17 vs 12/13 (on the exam simpler, like 6/7, 7/8): missing 1/17 vs 1/13; one cake for more people is smaller; missing less → bigger | `compare-fractions` slide 8 (8/9 vs 11/12) | SAME (English adds the above-one version) |
| L8 | העלאה בריבוע · Square it (roots) | 1568-1605 | 3/√10 vs 2/√5 → 9/10 vs 4/5; three ways for students who don't know roots yet (prefer cross-multiplying later; mark the video; "a root and a square cancel"); then compare by distance from 1 or cross-multiply (40 vs 45); **squaring changes the values but keeps the order**; **warning: square the numerator AND the denominator** (some students square only the root) | `compare-fractions` slide 10 (the same numbers) | SAME (English adds "for positive numbers only") |
| L9 | הצבת מספרים · Plug in numbers | 1606-1631 | Letters: x a fraction, y > 1 → x = ½, y = 2; 2/1.5 and 1.5/2.5 → expand ×2 → 4/3 and 3/5; cross-multiply 20 vs 9; **then think instead of calculating: above 1 vs below 1** | `compare-fractions` slide 12 (the same) | SAME |
| L10 | סיכום · Recap | 1632-1639 | Cross-multiplying is the recommended method, "a mantra", always works, even with letters later | `compare-fractions` slide 14 | SAME |
| I | שברים – פתיחה לשאלות · Intro to the question part | 1642-1648 | After the basics, harder psychometric questions | end of `compare-fractions` slide 14 ("Next: real exam-style questions") | SAME |
| Q1 | (1 − 1/3)(1 − 1/4)(1 − 1/5) | 1649-1685 | The prep-course way (common denominator) vs **shortcut 1: complete to the whole instantly**; **shortcut 2: cancel before multiplying** → 2/5 | `solve-q-091` ((1 − 1/4)(1 − 1/5)(1 − 1/6) = 1/2) | SAME (English adds the name "telescoping product") |
| Q2 | 2.5 · 0.2 ÷ 25 | 1686-1744 | **Way A, ordinary fractions**: 2.5 = 5/2, 0.2 = 2/10 = 1/5, cancel the 5s, ÷25 = ×1/25 → 1/50, choices are decimals → expand to /100 → 0.02. **Way B, decimals only**: 25·2 = 50, two places → 0.50; 50 hundredths ÷ 25 = 2 hundredths | `solve-q-092` (5.5 · 0.2 ÷ 22 = 0.05), Methods 1-2 | SAME (English adds left-to-right and the traps 0.5 / 0.11) |
| Q3 | D/A · B/D + C/A | 1745-1796 | **Math**: cancel D, same denominator → (B + C)/A, "the recommended way, one of the first questions". **Plug in**: all = 1, but **first check that the choices come out different** (2, 1, 3, 3/2), then one plug-in is enough | `solve-q-093` (2z/y · x/z + w/y), Methods 1-2 | SAME |
| Q4 | Which is not necessarily equal to A/B | 1797-1861 | **Math**: each choice checked as an expansion (×5 both; A²/B² = top ×A, bottom ×B → not kept, only if A = B; AB/B² and the ×A one cancel back); "if you see it, mark it and move on, else eliminate". **Plug in** A = 1, B = 2 → A²/B² = 1/4 ≠ ½ | `solve-q-094` (m/n; ×4, mn/n², m²/n², ×m), Methods 1-2 | SAME |
| Q5 | a = (b − ½)/(b − 1), b > 1 | 1862-1916 | **Understanding numerator/denominator**: both positive → a positive; same b, top loses less → top > bottom → a > 1. **Plug in** b = 2 → 1.5, eliminate three | `solve-q-095` (b > 2, (b − 1.5)/(b − 2)), Methods 1-2 | SAME |
| Q6 | 0 < a/b < 1: what must be true (hard) | 1917-1999 | "Looks simple, it's a late hard question, there's a trap"; **plug in first**: 1 and 2 → two choices survive; "with plugging in you must eliminate three, never mark at once"; other positive pairs don't help, **test a different kind: both negative** (−1, −2) → answer 4; **understanding**: same signs, the denominator is bigger in absolute value, number line for both cases, b/a > 1 always | `solve-q-096` (m/n, plug in 1, 3 then −1, −3), Methods 1-2 | SAME |
| Q7 | Largest of four root fractions | 2000-2073 | **Semi-finals and final** (pairs with the same bottom, then same tops → smaller bottom); **square them** (9/3, 25/3, 9/5, 25/5 — "more than 8 is enough"); **understanding**: biggest top and smallest bottom → answer 2; "pick the one you like" | `solve-q-097` (4/√2, 9/√2, 4/√6, 9/√6), Methods 1-3 | SAME |
| Q8 | y > 1, 0 < x < 1: largest expression (hard) | 2074-2167 | **Tournament**: semi-finals by same bottom (checking signs), final with different tops and bottoms → "open your eyes": (x + y)/(y + x) = 1, and y/(y − x) > 1. **Plug in, smart choice**: x = ½ and **y = 1.5 (not 2) so that y ± ½ is whole** | `solve-q-098` (0 < a < 1 < b; a = ½, b = 2.5), Methods 1-2 | SAME (her smart plug-in still works with 2.5 ± ½) |
| Q9 | Order 2/11, 3/17, 4/23 (hard) | 2168-2263 | Common denominator ruled out (big primes, no calculator); **Way 1: equal numerators** (12) → smallest bottom is biggest; **Way 2: cross-multiply just two, then use the choices** (2 comparisons instead of 3); **Way 3, "for creative students": flip them** (5.5, 5⅔, 5¾) and reverse the order | `solve-q-099` (6/19, 5/16, 4/13), Methods 1-3 | SAME (all three methods still work with the new numbers: tops → 60; 64 vs 65 and 95 vs 96; flips 3⅙, 3⅕, 3¼). English adds Method 4 (pieces of ⅓) |

**Counts (19 items: L1-L10, I, Q1-Q9):** SAME 18 · CHANGED 0 · PARTIAL 1 (L5) · MISSING 0.

---

## 2. English → Hebrew (English topic-3 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Her take? |
|---|---|---|---|
| `compare-fractions` slide 5 (part) | Why cross-multiplying works (a hidden common denominator); both bottoms must be positive | none | yes |
| `compare-fractions` slide 6 | Negatives: a negative bottom breaks cross-multiplying; move the minus up; two negatives → compare without the minus, then reverse; signs first | none (her Q6 negative case is related) | yes |
| `compare-fractions` slide 8 (part) | Distance from 1 for fractions above one (compare the extras) | none | yes |
| `compare-fractions` slide 9 | Adding the same number to top and bottom moves the fraction toward 1 | none | yes |
| `compare-fractions` slide 11 | x, x², √x, 1/x by range (plug in one number) | none | yes |
| `compare-fractions` slide 13 | "Flip them" taught in the lesson, with the same-sign condition | her Q9 Way 3 (here moved forward into the lesson too) | yes |
| `solve-q-fraction-compare` | Order 7/15, ½, 11/21 by benchmark ½ (+ cross-multiply check) | none (her L2 method) | no |
| `solve-q-099` Method 4 | Pieces of ⅓ (mediant), for strong students | none | yes (take exists; check whether her take includes it) |
| `solve-q-r26-t03-01/-02/-03` | Signs first + plug in; toward 1 + plug in; the x-range table in a question | none | no |
| `r26-t03-summary` | Summary (replaced by the printable summary page) | none | — |
| 18 extra practice questions in q03.txt | — | her 10 practice questions | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | L5: a cross-multiplication example with bigger-looking products, done by splitting ("don't be afraid: 17 · 5 = 10 · 5 + 7 · 5 = 85") | `compare-fractions` slide 5, after 55 vs 56: e.g. 9/13 vs 7/11 → 99 vs 91, "thirteen sevens: seventy plus twenty-one" (2-3 sentences) | her old take exists; topic scheduled for the 1-12 redo | **Optional.** It links cross-multiplying to topic-1 splitting and calms students who see two-digit products; cheap to add in the redo |

**English note (study order, not against her).** `compare-fractions` slide 10 says "We'll learn roots properly later",
which was true in her course order. In the English study plan (`src/lib/planData.ts` ORDER: 1, 30, 2, 4, 31, 6, 8, 32,
9, 10, 33, … 3 …), topics 8, 9 and 10 (powers and roots) come BEFORE topic 3, so the line should become a reminder
("Remember from the roots topic: squaring a root cancels it").

Nothing else of hers is missing, and nothing in topic 3 is wrong compared with her. Every one of her named methods
(benchmark ½ "from the denominator", the cakes, cross-multiplying "above its numerator", distance from 1, squaring both
parts, plugging in with "check the choices are different first", "eliminate three", "a different kind of number", the
tournament, "open your eyes", the smart plug-in y = 1.5, equal numerators, two comparisons + the choices, flipping) is
in the English script, and each still works with the English numbers.
