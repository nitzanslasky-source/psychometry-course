# Topic 17 (The Number Line): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 17363-18202 (source 12; all of it read).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t17.py`), practice list from the course dump.
- Recording status (`video_status.py`): **done** = number-line, number-line-2, number-line-3, solve-q-493 … 498, solve-q-500,
  r26-t17-reading-the-line, solve-q-r26-t17-01 … 05. **Recorded, waiting to be sent** = powers-on-number-line. **In the "check"
  list** (recorded) = solve-q-499, solve-q-501. r26-t17-summary = summary page. The whole topic is recorded.

**Match scale.** New numbers alone are not a change. SAME = same idea and all her methods. CHANGED = same idea, method / example
type / order differs. PARTIAL = some of her content or one of her methods is missing. MISSING = no English equivalent.

**Structure and numbering.** Her section: lesson 1 "ranges on the number line" (with one worked example), lesson 2 "the
number-line method" for powers (with two worked examples), 7 advanced questions, 10 practice questions. English splits lesson 1
into three camera parts (number-line, -2, -3) and records lesson 2 as powers-on-number-line. Her lesson-1 example became
q-493, her first lesson-2 example q-494; **her second lesson-2 example (finding the range from x < x³ < x²) stayed inside the
lesson** (powers-on-number-line slide 8, as x < x⁵ < x⁴), which is why the 3 + 7 Hebrew items give only 9 solution videos.
Her 7 advanced questions are q-495 … q-501.

**Her names.** "חזק על חזק – חלש על חלש" → kept as **"strong on strong, weak on weak"** ("our own slogan", number-line-3 slide 2);
חזקות חריגות → "exceptional powers"; היררכיה → "the hierarchy"; פעולה זהה → "the same operation"; שיטת ציר המספרים / החצים → "the
arrows"; פתרון הברקתי → "a shortcut: check only the order of the powers". "כפל בשבר מקרב ל-0" → "multiplying by a fraction brings
it closer to zero".

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | תחומים על ציר המספרים · Four ranges | 17365-17384 | Positive / negative, then four ranges (< −1, negative fractions, positive fractions, > 1); every number in a range reacts the same way (½ and ¼ both grow ×2) | number-line slides 0-1 | SAME (English adds the borders −1, 0, 1 and "first ask which ranges the givens allow") |
| 1b | סימטריה · The mirror | 17385-17400 | The negative side mirrors the positive side; ×½: 10 → 5 and −10 → −5 (it grew), both toward 0; **tip: instead of plugging in negatives and risking mistakes, look at the positives and mirror** | number-line slide 2 (15, 8 × ¾) | SAME (her tip kept almost word for word) |
| 1c | כפל וחילוק · Multiplying and dividing | 17401-17417 | × (>1) grows, ÷ (>1) shrinks, × fraction shrinks, ÷ fraction grows (= × reciprocal); negatives in the mirror | number-line-2 slide 1 | SAME |
| 1d | היררכיה · The hierarchy | 17418-17433 | A number in a higher range stays bigger whatever power or root (⁵√(7/6) vs √(7/8)) "except the exceptional powers" | number-line-2 slide 2 (⁵√(11/10) vs √(7/9); (5/4)³ vs √(3/5)) | SAME (English adds "for negatives, odd powers only") |
| 1e | חזקות חריגות · Exceptional powers | 17434-17452 | Even power of a negative jumps to the positive side; a negative exponent flips the base (5⁻³ = (1/5)³); handle them first: 4/7 with a root vs (3/5)⁻³ → (5/3)³ > 1 | number-line-2 slide 3 | SAME (English adds the −5² vs (−5)² bracket warning) |
| 1f | פעולה זהה · The same operation | 17453-17467 | Same operation on both → ignore it; first fix exceptional powers: 7⁻³ vs 6⁻³ → (1/7)³ vs (1/6)³ → 1/6 bigger | number-line-3 slide 1 (5⁻⁴ vs 4⁻⁴) | SAME (English adds "positive numbers only: −3 vs −2 squared flips") |
| 1g | חזק על חזק – חלש על חלש (+ example) | 17468-17537 | Compare the strong terms with each other and the weak with each other; example w>z>y>x>1, which is NOT true: xy vs zw; yw vs xz (pair w with z, y with x); y vs zx ("z drank a Red Bull", ×x > 1 makes it even stronger); xw vs z | number-line-3 slide 2 (4·6 vs 3·5; one win each → no decision; ×3 vs ×½) + solve-q-493 (1<p<q<r<s) | SAME (the slogan, the matching, "one win each decides nothing" and "×(>1) makes the bigger one bigger still" are all there; English adds a plug-in method. Her Red Bull image is not used) |
| 1h | סיכום שיעור 1 · Close | 17538-17547 | Ranges and exceptional powers; next: a method for the line | number-line-3 slide 3 | SAME |
| 2a | שיטת ציר המספרים – החצים · The arrows | 17549-17597 | Draw the line with four ranges and an arrow in each: > 1 right, positive fractions left, negative fractions right; bigger power → further along the arrow (½ → ¼ → 1/16; 2/5 vs (2/5)²) | powers-on-number-line slides 0-6 | SAME (English adds the < −1 range and roots as powers 1/2) |
| 2b | שלושה שלבים · Three steps | 17598-17611 | (1) exceptions (negative to an even power); (2) roots → powers; (3) draw the line and read the arrows | powers-on-number-line slide 7 | SAME |
| 2c | −1<x<0, הקטן ביותר (example) | 17614-17659 | The even power jumps positive → out; ⁵√x = x^(1/5); arrow right → smallest power wins → x⁻¹; "the method already handles negative exponents, no need to flip" | solve-q-494 (−1<m<0, m⁻³) | SAME (her "keep the negative power as it is" kept) |
| 2d | מציאת תחום: x < x³ < x² (example) | 17660-17703 | Work backwards: x < x³ fits the right-pointing ranges (> 1, negative fractions); x³ < x² rules out > 1 → negative fraction; why (x² jumps positive); "you can also plug in numbers from the ranges" | powers-on-number-line slide 8 (x < x⁵ < x⁴) | SAME (taught on a lesson slide instead of a separate solution video; "questions like this come up less often" and "you can also plug in" kept) |
| 2e | סיכום שיעור 2 · Close | 17704-17720 | The reverse questions are rarer; plugging in often takes a long time, understanding solves it in seconds | powers-on-number-line slides 0, 8 | SAME |
| 3 | z>y>x>1, הקטן ביותר (Q, easy+) | 17725-17763 | Every choice is a product of three; smallest = all three smallest, x·x·x isn't offered → the nearest, x·x·y; plug in 2, 3, 4 | solve-q-495 (1<a<b<c) | SAME |
| 4 | z>y>1>x>w>0, אינה בהכרח נכונה (Q, medium+) | 17766-17865 | × positive fraction → toward 0 (also by dividing by positive z); y − x vs z − w as distances, or rearranged and strong-on-strong (two wins); ÷ fraction → away from 0; y + x vs z + w: one win each → no decision → counterexample with z close to y and x far from w | solve-q-496 (0<a<b<1<c<d) | SAME (every step: the two rules, the distances, the algebra by dividing by a positive, the "one helps each side" reasoning and the counterexample) |
| 5 | y,z שברים חיוביים, x שבר שלילי, הגדול ביותר (Q, hard) | 17868-17922 | Signs: all negative, no help; × fraction → toward 0, and on the negative side closer to 0 = bigger, so the product of all three fractions is biggest; plug in −½, ¼, ½ and draw −1/16, −1/8, −1/4, −1/2 on the line; "× fraction always brings you toward 0" | solve-q-497 (−1<k<0<m<n<1) | SAME |
| 6 | x³ > x⁴, באיזה תחום (Q, easy+) | 17925-17964 | Arrows: a negative x makes x⁴ positive → out; > 1 the power grows → out; positive fraction ✓; or plug in the answers (2, ½) | solve-q-498 (x⁸ < x⁷) | SAME |
| 7 | −1<x<0: סדר של x³, x, ∛x, x⁻³ (Q, hard) | 17967-18050 | Three ways: (1) arrows (all odd → bigger power, bigger); (2) smart plug-in: **not −½ (no cube root by hand) but −1/8**; (3) "the brilliant way": with no even power of a negative, a correct order must have powers that only rise or only fall | solve-q-499 (y⁷, y, ∛y, y⁻⁷) | SAME (all three ways, incl. "choose −1/8 for an easy cube root") |
| 8 | x שבר חיובי: x²⁰, ²⁰√x, 20x, 20/x (Q, medium) | 18053-18117 | Math: x²⁰ in (0, x), the root in (x, 1), 20x < 20, 20/x > 20; plug-in is hard with 20s → **smart plug-in "by insight": the 20 doesn't matter, only the pattern, so shrink every 20 to 2** and use x = ¼ (½ / ½ / 8) | solve-q-500 (0<t<1: 6t, 6/t, t⁶, ⁶√t) | PARTIAL: the full reasoning is there. The plug-in now picks t = 1/64 (whose sixth root is easy), so **her "replace the big number by 2" shortcut is missing** |
| 9 | x² < x < yz < y < z, אפשרית אך לא בהכרח (Q, hard) | 18120-18199 | Decode the chain: x² < x → positive fraction; yz < y → z < 1; all positive fractions; read "possible but not necessarily"; sum vs product of fractions; x²y < xz by cancelling x or strong-on-strong; sum of two fractions < 1 sometimes (0.2 + 0.4 vs 0.2 + 0.9); a product of fractions never exceeds 1 | solve-q-501 (p² < p < rq < q < r) | SAME (incl. both ways for the product comparison) |
| 10 | 10 שאלות תרגול עצמי · 10 practice questions | 18202 | — | q-502 … q-511 (10) + alg-extra ×3 + q-r26-t17-06/08/09/12 | SAME (all 10 kept) |

**Count by row (22 rows):** SAME 21 · CHANGED 0 · PARTIAL 1 (8) · MISSING 0.

### Count by video (her units)

| Unit | Match |
|---|---|
| Lesson 1 ranges (1a-1h, incl. the strong-on-strong example) | SAME |
| Lesson 2 the arrows (2a-2e, incl. 2 examples) | SAME |
| Q3, Q4, Q5, Q6, Q7, Q9 | SAME |
| Q8 x²⁰ … 20/x | PARTIAL (the "shrink 20 to 2" smart plug-in) |
| 10 practice questions | SAME |

**By video: SAME 9 · CHANGED 0 · PARTIAL 1 · MISSING 0** (10 units: 2 lessons, 7 questions, the practice set).

---

## 2. English → Hebrew (added in English)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| number-line slide 1 (part) | The borders −1, 0, 1 behave on their own; "first ask which ranges the givens allow" | none | yes |
| number-line-2 slide 3 (part) | −5² vs (−5)² | none | yes |
| number-line-3 slide 1 (part) | The same operation keeps the order only for positive numbers | none | yes |
| powers-on-number-line slides 3, 6 | Roots as powers inside the arrows; the range below −1 | none | yes |
| 2nd methods in q-493, q-495; algebra in q-496 | Plug-in / dividing by a positive | her own tools | yes |
| r26-t17-reading-the-line | Multiplying by a negative reverses the order (and the inequality sign) | none | yes |
| solve-q-r26-t17-01 … 05 | Figure (not to scale) questions; −4<x<−2; x<−1<y<0; a point one third of the way from −7 to 5 | none | yes |
| r26-t17-summary | Summary page | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | Q8 smart plug-in: "the 20 doesn't matter, only whether each operation grows or shrinks the number, so shrink every 20 to 2" (with the English numbers: replace 6 by 2, t = ¼ → 1/16, ½, ½, 8) | solve-q-500 slide 1, 2-3 sentences before or instead of the t = 1/64 plug-in | yes (done) | OPTIONAL. It is a real, reusable exam trick of hers, but the English plug-in already works with these numbers and the slide is recorded |
| 2 | "Z drank a Red Bull" image for ×(>1) | solve-q-493 | yes | NOT NEEDED (a brand joke; the idea "it gets even larger" is there) |
| 3 | Her method verdicts ("both are excellent", "the axis method is recommended") | — | — | NOT NEEDED (R35) |

**RESTORE list: none required** (one OPTIONAL item: the "shrink 20 to 2" trick in solve-q-500). Every other method, slogan and
warning she gives in topic 17 is in the English and works with the English numbers. Nothing in the English contradicts her.
