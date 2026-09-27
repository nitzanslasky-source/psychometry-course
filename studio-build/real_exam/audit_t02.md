# Audit: Topic 2 (Fractions: Fundamentals). Additions vs the real NITE exam

Sources: `math_patches/t02_CHANGES.md`, `math_patches/t02.py`, `real_exam/quant_real.md` (760 real questions).
Real exam ids below are `year_season_qS_NN` from quant_real.md.

## Key real-exam evidence (Topic 2 material)
- Pure fraction arithmetic: 2023_autumn_q1_02 (1/10+1/5+1/3+1/2−1), 2023_winter_q2_01 (1/4·3/5 + 7/10 + 1/2 − 7/20, mixed operations), 2026_spring_q2_05 (12·(1/6−3/4) = −7, negative result), 2025_autumn_q1_15 (5/9 + 5/12), 2022_winter_q2_16 (2/3·15/4·a/b = 1).
- "Of" and "of the remaining": 2022_winter_q1_04 (Yossi ate 2/3, Shula ate 3/4 of what he left: same type as the guided water tank), 2020_spring_q1_20 ("1/4 of the remaining time"), 2022_winter_q1_13 (b = 1/4(x − a)), 2021_autumn_q1_04 (1/3 + 1/6, the rest is 1,500, work back to the total), 2025_winter_q2_07 (3/5 → 1/4 after 21 drawn), 2020_autumn_q2_01 (1/3 of boys = 1/4 of class), 2024_winter_q2_15 (1/2 of A and 1/3 of B), 2024_spring_q1_08 (4/5 and 3/5 of 25), 2023_spring_q2_02 (1/x, half of that).
- Stacked fractions / fraction bar as brackets / splitting the top: 2020_winter_q2_13 ((x+y)/(1/x+1/y)), 2019_spring_q1_10 ((x/y)/(z/w)), 2022_winter_q1_08 (choices (a+b)/4 − (−c−d)/4 and ((a+b)/2 + (c+d)/2)/2), 2021_autumn_q1_15 (which is NOT equal to 1/x+1/y+1/z; choices (xy+yz+xz)/xyz, x/x² + (z+y)/zy, stacked fraction, (x+y+z)/xyz).
- Negative fractions: 2022_winter_q1_08 (−(−c−d)/4, a minus in front of a fraction with a negative top), 2026_spring_q2_05, 2026_spring_q1_17 (−1/2 < 1/x < 1/2).
- Dividing by a simple decimal: 2020_autumn_q2_18 (100 ÷ 0.5 m/s), 2026_spring_q2_15 (average rises by 0.5: 16 ÷ 0.5 = 32), 2025_winter_q1_20 (0.25 commission, 0.5 rate: 1000 ÷ 0.625), 2021_spring_q2_18 (0.03·50 ÷ 0.006).
- Estimate / "closest to": 2020_spring_q2_11, 2023_autumn_q2_18 (closest-to questions); 2025_autumn_q1_15 (5/9+5/12 ≈ 0.55+0.42 ≈ 0.97 kills 2/3, 10/17, 25/108 at once, key 35/36).
- Mixed numbers in the calculation: 2019_winter_q1_08 (½ + 1½ + 1; 1 + 1½), 2024_spring_q1_14 (1 + ½ + ¼ + ⅛ = 1⅞, choices are mixed numbers), 2020_autumn_q1_10 (3⅔ hours), 2021_spring_q2_06 (8½).

## Table
| # | Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|---|
| 1 | Expanding wording ("two quarters ... two halves is one whole") | `fraction-basics` slide 7 | FIX | KEEP | wording |
| 2 | Division colon ":" → "÷" on boards, draw notes, labels, both cards; stems q-048, q-073, q-075, extra-4 | `fraction-basics`, `fraction-multiply`, `fraction-add`, `decimals`; cards `mem-fractions`, `mem-decimals` | FIX | KEEP | notation (real exam uses ÷ / fraction bar) |
| 3 | Spelling "practise" → "practice"; two "…, so …" lines rephrased | `fraction-multiply` slide 1 and others | FIX | KEEP | wording |
| 4 | LCM named on slide 5 ("least common multiple = smallest common denominator"); LCM used in written solutions | `fraction-add` slide 5 | FIX | KEEP | names an existing step |
| 5 | All 43 remaining solutions rewritten (real fractions, ÷); q-047, q-048 cancel first; q-065 (0.9)² → 0.9·0.9; extra-1..7 solutions show numbers; extra-2 replaced by 7/10 − 1/4 (same type); answer positions shuffled | questions q-043…q-075, alg-extra-unit-t2-1-1..7 | FIX | KEEP | corrections/clarifications |
| 6 | Removed near-duplicates q-041, q-042, q-045 | practice | FIX (removal of original items) | RESTORE (teacher's rule: original content stays) | see "ORIGINAL ITEMS REMOVED BY FIXERS" |
| 7 | Practice reordered easy → hard; new card `mem-r26-t02-basics` placed after `fraction-basics` | `unit-t2-1` practice order | FIX | KEEP | order |
| 8 | Recap slides extended with lines summarizing the new slides | `fraction-basics` slide 13 (Recap), `fraction-multiply` slide 11 (Recap), `fraction-add` slide 10 (Recap), `decimals` slide 12 (Recap) | FIX | KEEP | each added line follows a slide below, all KEEP |
| 9 | New slide "Splitting the top" ((a+b)/c = a/c + b/c; never split the bottom) | `fraction-basics`, slide "Splitting the top" | CONTENT | KEEP | 2022_winter_q1_08, 2021_autumn_q1_15 (choice 2 splits (z+y)/zy), 2020_winter_q2_13; 3 |
| 10 | New slide "Negative fractions" (−3/4 = (−3)/4 = 3/(−4); two minus cancel; minus in front belongs to whole top) | `fraction-basics`, slide "Negative fractions" | CONTENT | KEEP | 2022_winter_q1_08 (−(−c−d)/4), 2026_spring_q2_05, 2026_spring_q1_17; 3 |
| 11 | Guided Question 1 ((−6+15)/(−3)) + solution video "Split the top"; practice -02 (which is NOT equal to −2/5), -03 ((48+36)/12), exam-level -04 | q-r26-t02-01 (+ its guided video), q-r26-t02-02, -03, -04 | CONTENT (question types of rows 9–10) | KEEP | "which is NOT equal" type: 2021_autumn_q1_15, 2022_winter_q1_08; numeric fraction arithmetic: 2023_autumn_q1_02, 2026_spring_q2_05 |
| 12 | New slide '"Of" means times' incl. "spend 1/3, then 1/4 of the rest" trap | `fraction-multiply`, slide '"Of" means times' | CONTENT | KEEP | 2022_winter_q1_04, 2020_spring_q1_20, 2022_winter_q1_13, 2021_autumn_q1_04, 2024_winter_q2_15; 9+ |
| 13 | Guided Question 2 (water tank, "of the remaining") + solution video "Of the remaining"; practice -06 (3/4 of 48), -07 (2/5 of a number is 24), -09 (workers); exam-level -08 (book, of the remaining, work back), -24 (girls/boys with glasses) | q-r26-t02-05 (+ video), -06, -07, -08, -09, -24 | CONTENT (type of row 12) | KEEP | -05/-08: 2022_winter_q1_04, 2020_spring_q1_20, 2021_autumn_q1_04, 2025_winter_q2_07; -07: 2020_autumn_q2_01; -24: 2024_winter_q2_15, 2024_spring_q1_08 |
| 14 | New slide "Fraction bar = brackets" ((1+½)/(2−¼) = 6/7) | `fraction-add`, slide "Fraction bar = brackets" | CONTENT | KEEP | 2020_winter_q2_13, 2019_spring_q1_10, 2022_winter_q1_08, 2021_autumn_q1_15; 4 |
| 15 | New slide "Mixed operations" (× ÷ before + −: 3/4 − 1/2·2/3) | `fraction-add`, slide "Mixed operations" | CONTENT | KEEP | 2023_winter_q2_01 (exactly this), 2026_spring_q2_05; 2 |
| 16 | Guided Question 3 (stacked fraction with sums) + solution video "Fraction bar = brackets"; practice -14, -11; exam-level -12 (5/6 − 2/3 ÷ 4/5) | q-r26-t02-10 (+ video), -14, -11, -12 | CONTENT (types of rows 14–15) | KEEP | 2020_winter_q2_13, 2023_winter_q2_01 |
| 17 | Exam-level -13: three-level continued fraction 1/(1+1/(1+1/2)) | q-r26-t02-13 (section 5 practice) | CONTENT (type of row 14) | KEEP (was UNSURE; re-checked 2026-09-27) | Re-checked on the regenerated quant_real.md: the deepest real nesting is still 2 levels (e.g. 2020_winter_q2_13, 2019_spring_q1_10, 2021_autumn_q1_15); no real 3-level fraction. BUT the original course already tests exactly this 3-level form: q-122 (8/(1/(1/2+1/4)), Topic 5), q-135 (12/(1/(1/3+1/6)), Topic 5), taught in original video `expression-strategy`. Teacher's rule: original questions must be taught, so the type stays and -13 (same type, applying row 14) is kept. |
| 18 | New lesson video "Fraction Shortcuts": title slide + slide "Estimate first" (benchmarks 0, ½, 1; kill choices) | `r26-t02-shortcuts` (title, "Estimate first") | METHOD | KEEP | 2025_autumn_q1_15, 2020_spring_q2_11, 2023_autumn_q2_18 |
| 19 | Slide "Test a rule" (test with easy numbers, e.g. ½+½) | `r26-t02-shortcuts`, "Test a rule" | METHOD | KEEP | 2021_autumn_q1_15, 2022_winter_q1_08, 2020_winter_q2_13 (plug in numbers to check equality of expressions) |
| 20 | Slide "Cross shortcut" (a/b + c/d = (ad+bc)/bd; 1/a − 1/b = (b−a)/ab) | `r26-t02-shortcuts`, "Cross shortcut" | METHOD | KEEP | 2021_autumn_q1_15 (choice 1 is this form), 2020_winter_q2_13 (1/x+1/y = (x+y)/xy), 2025_autumn_q1_15 |
| 21 | Slide "Mixed numbers fast" (whole parts + fraction parts, no borrowing) | `r26-t02-shortcuts`, "Mixed numbers fast" | METHOD | KEEP | 2019_winter_q1_08, 2024_spring_q1_14 |
| 22 | Shortcuts "Recap" slide | `r26-t02-shortcuts`, "Recap" | METHOD | KEEP | summarizes rows 18–21 |
| 23 | Guided Question 4 ("closest to" 5/11+8/15+4/9) + solution video "Estimate with ½"; practice -20 (7/8+5/9, estimate) | q-r26-t02-19 (+ video), -20 | METHOD | KEEP | "closest to" type: 2020_spring_q2_11, 2023_autumn_q2_18; fraction-sum estimate: 2025_autumn_q1_15 |
| 24 | Practice -21 (1/6 − 1/7), -22 (5¾ − 2⅓), exam-level -23 (which always equals 1/a + 1/b, plug in numbers) | q-r26-t02-21, -22, -23 | METHOD | KEEP | -21: 2023_autumn_q1_02; -22: 2019_winter_q1_08, 2024_spring_q1_14; -23: 2021_autumn_q1_15 (same type), 2020_winter_q2_13 |
| 25 | q-054 solution gets "Method 2: estimate and eliminate" | q-054 | METHOD | KEEP | as row 18 |
| 26 | New slide "÷0.5, ÷0.25, ÷0.2" (= ×2, ×4, ×5; ÷0.125 = ×8) | `decimals`, slide "÷0.5, ÷0.25, ÷0.2" (sidebar "Quick divisors") | METHOD | KEEP | 2020_autumn_q2_18 (÷0.5), 2026_spring_q2_15 (÷0.5), 2025_winter_q1_20 (0.25/0.5/0.125 arithmetic). Note: only ÷0.5 is directly seen; ÷0.25/÷0.2 are the same trick |
| 27 | Guided Question 5 (3.6/0.25) + solution video "Divide by 0.25"; practice -18 (0.125·64), -16 (7 ÷ 0.2); exam-level -17 (4.5 m rope ÷ 0.25 m) | q-r26-t02-15 (+ video), -16, -17, -18 | METHOD (decimals are original content) | KEEP | as row 26; -17 word-problem form like 2020_autumn_q2_18 |
| 28 | New card "Fraction basics" (rows incl. Split the top, Negative fractions; tips) | card `mem-r26-t02-basics` | CONTENT | KEEP | rows 9–10 |
| 29 | New card "Multiplying & dividing" (rows "Of", "Of the rest", divide, stacked, mixed) | card `mem-r26-t02-multiply` | CONTENT | KEEP | row 12 |
| 30 | `mem-fractions` new rows/tips: '"Of" means times', 'Several operations', LCM tip, "Fast add … Estimate first" tip | card `mem-fractions` | CONTENT/METHOD | KEEP | rows 12, 15, 4, 18, 20 |
| 31 | `mem-decimals` new rows 2/3, 1/6, 3/5, 4/5, 1/20, 1/25 and new table "Quick division" (÷0.5, ÷0.25, ÷0.2, ÷0.125) | card `mem-decimals` | METHOD | KEEP | Quick division: row 26; conversions extend the original fraction↔decimal table (2024_spring_q1_08 4/5, 3/5 of 25; 2023_winter_q2_01 via decimals) |

## TO REMOVE
- None.
- (Re-check 2026-09-27: the former UNSURE q-r26-t02-13 is now KEEP, see row 17.)

## ORIGINAL ITEMS REMOVED BY FIXERS
Checked against the pre-patch course `course18.json` (no q-r26 items) and `math_patches/t02.py`. These are original items the patch removed or replaced; under the teacher's rule they should be restored.
- `q-041` (practice in `unit-t2-1`): stem `\frac{5}{6} = \frac{35}{?}`, choices 48 / 36 / 42 / 40, key 42 (choice 3). Removed by `M.unplace('q-041')` as a "near-duplicate". No solution video.
- `q-042` (practice in `unit-t2-1`): stem `\frac{4}{12} = \frac{?}{27}`, choices 9 / 12 / 6 / 8, key 9 (choice 1). Removed by `M.unplace`. No solution video.
- `q-045` (practice in `unit-t2-1`): stem `7\,\frac{1}{6} = ?`, choices 45/6 / 43/6 / 37/6 / 41/6, key 43/6 (choice 2). Removed by `M.unplace`. No solution video.
- `alg-extra-unit-t2-1-2` (practice in `unit-t2-1`): the original question "Evaluate 5/6 − 1/4" (choices 7/12, 1/2, 2/3, 1/3; key 7/12) was REPLACED in place by "Evaluate 7/10 − 1/4" (key 9/20). To restore: put back the original stem, choices and key.
- Not removals (listed for completeness, no action needed): extra-1, -3, -4, -5, -6 keep the same question with answer positions shuffled; q-048, q-073, q-075 stems only change ":" to "÷"; q-065 stem (0.9)² became 0.9·0.9 (same value, notation change); original recap slides of `fraction-basics`, `fraction-multiply`, `fraction-add`, `decimals` were rewritten but every original line is still in them; card `mem-fractions` row "Add / subtract" text gained "(the LCM)" and `mem-decimals` row ":10, :100, :1000" became "÷10, ÷100, ÷1000"; four spoken lines were reworded (fraction-basics slides 6 and 7, decimals slide 8, fraction-multiply slide 1). No original slide, video or card row was deleted.

## Counts
KEEP 31 (8 FIX + 23 METHOD/CONTENT) / REMOVE 0 / UNSURE 0
