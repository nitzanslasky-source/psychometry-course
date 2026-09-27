# Audit T13 — Absolute Value (report only)

Sources: `math_patches/t13_CHANGES.md`, `math_patches/t13.py`, fixed `real_exam/quant_real.md` (full stems of
2021_autumn_q2_15 "|x+y| < |x−y|", 2023_autumn_q1_01 "0<a, c<b<0" re-checked); original course from `base-v18.html` /
git `8965af3`.

Exam facts used (absolute value): 2020_autumn_q2_13 (|x|=13, |y|=4: values of |x−y|), 2021_autumn_q2_15 (|x+y|<|x−y| ⇒ xy<0),
2024_autumn_q1_02 (|x−y|−|y−x|), 2025_autumn_q2_01 (a+|a| for a<0), 2019_spring_q2_14, 2020_spring_q1_02 (|x|−x=6, i.e.
|x| = x+6), 2023_spring_q1_08 (xy<|xy|<y), 2024_spring_q2_18 (|x+y|=|x|−|y|), 2025_spring_q1_19 (|a+b|<a), 2026_spring_q2_10,
2019_winter_q2_17, 2023_winter_q2_10 (|x|(x−2)≤0), 2024_winter_q1_05 (|x|/x), 2025_winter_q2_05, 2022_winter_q2_10,
2023_autumn_q1_15 (number line |x|≤5, 4≤|x|≤6). **0** real questions of the types "|expr| < negative number / ≤ 0",
"write a range as bars (midpoint)", or "sum of two distances |x−a|+|x−b| = c".

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| Sign clue |x| = −x ⇒ x ≤ 0 (zero trap) on slide, Q1 video, card | `absolute-value` slide "Sign clues"; solve-q-358 slide 3; card `mem-absolute-value` | FIX | KEEP | 2025_autumn_q2_01; original alg-extra-unit-t13-3-6 (key x ≤ 0) |
| "The minus just drops off" limited to plain numbers | `absolute-value` slide "Plus or minus inside" | FIX | KEEP | — |
| Q12(now Q15) "bait" line; Q9(now Q11) broken board line; extra-t13-3-1 solution; slide 9 explanation | solve-q-369, solve-q-366, alg-extra-unit-t13-3-1, `absolute-value` slide "Inequalities" | FIX | KEEP | — |
| Rule 2 extended: |a/b| = |a|/|b| | `absolute-value` slide "The rules"; card | METHOD | KEEP | 2024_winter_q1_05; original q-358 (|a/b|) |
| New slide "Signs of a product" (ab>0 same signs, ab<0 opposite, x/|x| = ±1) | `absolute-value` slide 8 | CONTENT | KEEP | 2023_autumn_q1_01, 2023_spring_q1_08, 2024_winter_q1_05, 2021_autumn_q2_15; original q-358, q-362, q-381 |
| New slide "Negative right side" (|x+1|<−3 none; >−3 all; ≤0 one value) | `absolute-value` slide 11 | CONTENT | KEEP (rule 2) | Exam: 0. Kept because it teaches the original card tip "Right side negative? No solution. Right side zero? One case only." |
| "Plug in" slide: avoid 0, 1, −1 and choice numbers; plug in again | `absolute-value` slide "Plug in" | METHOD | KEEP | 2024_winter_q1_05, 2025_autumn_q2_01, 2024_spring_q2_18 |
| Recap + "Seven questions next"; American spelling; "Question five" | `absolute-value` "Recap"; videos | FIX | KEEP | — |
| Tools video title slide | `r26-t13-tools` slide 1 | — | KEEP | — |
| "Squares and bars" (|x|²=x², √x²=|x|, |a−b|=|b−a|) | `r26-t13-tools` "Squares and bars" | METHOD | KEEP | 2024_autumn_q1_02, 2021_autumn_q2_15; original q-379 |
| "Square both sides" (|x−1| = |x+3|) | `r26-t13-tools` "Square both sides" | METHOD | KEEP | 2021_autumn_q2_15, 2024_spring_q2_18; original q-368 (Method 2), q-371, q-372, q-374 |
| "Letter on the right" (|x−6| = 2x, check) | `r26-t13-tools` "Letter on the right" | METHOD | KEEP | 2020_spring_q1_02 (|x| = x+6); original q-380 |
| "Distance" (|x−a| as distance, number-line figure) | `r26-t13-tools` "Distance" (+ figure) | METHOD | KEEP | 2020_autumn_q2_13, 2023_autumn_q1_15, 2025_spring_q1_19; original q-364, alg-extra-unit-t13-3-5 |
| "From a range to bars" (midpoint trick) | `r26-t13-tools` "From a range to bars" | CONTENT | REMOVE | 0 real questions; no original question needs it |
| Tools recap | `r26-t13-tools` "Recap" | — | KEEP (edit) | drop its midpoint line |
| New card "Question wordings" (necessarily/could/cannot/not necessarily/possible but not necessarily) | `mem-r26-t13-wordings` | METHOD | KEEP | 2021_spring_q1_15, 2020_autumn_q2_19, 2024_winter_q2_05, 2022_winter_q1_20; original q-366 |
| Card `mem-absolute-value` rewritten: Rules, Sign clues (incl. ab signs, x/|x|), Solving rows for bars both sides / letter on right; Distance rows |x−a|, |x−a|<r | `mem-absolute-value` | METHOD/FIX | KEEP | as slides |
| Card row "|x+1|<−3 · |x+1|>−3 · |x+1|≤0" and tip "Right side negative or zero?" | `mem-absolute-value` "Solving" | CONTENT | KEEP (rule 2) | original card tip |
| Card row "a<x<b ⇒ |x−(a+b)/2| < (b−a)/2" | `mem-absolute-value` "Distance tools" | CONTENT | REMOVE | 0 |
| Existing videos use the tools: distance picture (Q3, Q4), x/|x| link (Q5), check line (Q13), squaring named (Q14), wordings pointer (Q11) | solve-q-360, -361, -362, -367, -368, -366 | METHOD | KEEP | as above |
| Guided Q6 |2x−1| = 7, all values + video | q-r26-t13-01, solve-q-r26-t13-01 | original content | KEEP | 2020_spring_q1_02, 2025_winter_q2_05; original q-359 |
| Guided Q7 "which has no solution" (|x+2| < −1) + video | q-r26-t13-02, solve-q-r26-t13-02 | CONTENT (type) | REMOVE | 0 real questions of this type |
| Guided Q12 |x+4| = 3x + video | q-r26-t13-03, solve-q-r26-t13-03 | METHOD | KEEP | 2020_spring_q1_02; original q-380 |
| Guided Q16 "which inequality is exactly −3<x<7" + video | q-r26-t13-04, solve-q-r26-t13-04 | CONTENT (type) | REMOVE | 0 |
| Text: TeX, stacked conditions, NITE wording, q-382 choice 4 | T13 questions | FIX | KEEP | — |
| Practice "true for every x" (negative right side) | q-r26-t13-05 | CONTENT (type) | REMOVE | 0 |
| Practice range −8<x<2 → bars | q-r26-t13-06 | CONTENT (type) | REMOVE | 0 |
| Practice |x|/x + 2y/|y| | q-r26-t13-07 | METHOD | KEEP | 2024_winter_q1_05 |
| Practice |2−x| + |x| for x>2 | q-r26-t13-08 | METHOD | KEEP | 2025_autumn_q2_01, 2024_autumn_q1_02 |
| Practice |x−2| = 2x+1 | q-r26-t13-09 | METHOD | KEEP | 2020_spring_q1_02 |
| Practice integers with |x−1|+|x−7| = 6 | q-r26-t13-10 | CONTENT (type) | REMOVE | 0 on the exam (original extra 3-5 has a similar sum-of-distances item) |
| Practice |3x−6| ≤ 0 | q-r26-t13-11 | CONTENT (type) | REMOVE | 0 |
| Practice |x| = −x and |y| = y | q-r26-t13-12 | METHOD | KEEP | 2025_autumn_q2_01, 2019_spring_q2_14 |

## TO REMOVE
- Slide: video `r26-t13-tools`, slide "From a range to bars" (plus its sidebar label and the matching line on the "Recap" slide).
- Questions + solution videos: q-r26-t13-02 + solve-q-r26-t13-02; q-r26-t13-04 + solve-q-r26-t13-04. (Guided numbering changes: new Q7 and Q16 go; sidebars SB1/SB2 must follow.)
- Practice questions: q-r26-t13-05, q-r26-t13-06, q-r26-t13-10, q-r26-t13-11.
- Card row: `mem-absolute-value`, table "Distance tools", row "$a<x<b$ → $|x-\frac{a+b}{2}|<\frac{b-a}{2}$ (center, half the length)".

Counts (table rows): KEEP 25 (incl. 5 FIX) · REMOVE 8 · UNSURE 0.

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- No original question was removed.
- Card `mem-absolute-value` — all tables were rebuilt. Original rows that no longer exist in their original wording: Rules "|x|=x if x≥0 · |x|=−x if x<0 | A minus inside drops off"; "|a·b|=|a|·|b| | Bars on a product can go on each factor"; Sign clues "|x|>x | x is negative", "|x|=x | x is zero or positive"; Solving "|x−2|<4 (small side) | −4<x−2<4 → closed range", "|x−2|>4 (big side) | … → open range"; tip "Right side negative? No solution. Right side zero? One case only."
- Video `absolute-value` slides "Plus or minus inside" (3), "The rules" (5), "Sign clues" (7), "Plug in" (10), "Recap" (11) — original scripts rewritten (e.g. "In practice? The minus just drops off."; 3 sign clues instead of 4).
- Video solve-q-358 slide 3 **"The three sign clues"** replaced by "The sign clues" (4 clues).
- Video solve-q-362 — original plug-in with x = −1 replaced by x = −2; "Last question." replaced.
- Video solve-q-369 — original line "Six to seven is the bait — what you get if you forget to subtract the one" replaced.
- **q-382** choice 4 replaced (original "Correct for every a and b"); **q-378** choices reformatted; **alg-extra-unit-t13-3-1** solution replaced.
- Guided numbering: old Q6–Q13 are now Q8, Q9, Q10, Q11, Q13, Q14, Q15, Q17.
