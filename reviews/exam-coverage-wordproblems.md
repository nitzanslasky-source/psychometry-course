# Real-exam coverage audit: Word problems (topics 21–29, plus 51)

21 Oct 2026. This audit is read-only: no course file was changed.

**Real items.** I read every question in eight `quant_real.md` subtopics: percentages 42, work_rate 34, combinatorics 24,
probability 24, averages 23, motion_speed 12, factorials 12 and overlapping_sets 6. That is **177 questions**.
The exam's subtopic labels are loose, so I sorted each item by the method it really needs:
- the "percentages" label also holds 9 ratio items;
- the "work_rate" label also holds ages, step-by-step processes and unit-conversion items;
- 4 "probability" items are really counting, and 3 are really averages;
- 2024_spring_q1_08, labelled combinatorics, is an overlap range.

**Course.** I used `course/t21–t29.txt` and `t51.txt` (every lesson was read in full, and the solution videos were checked
where they carry the method) and `q21–q29.txt` (all 360 stems).

**Plan order** (planData ORDER): 51 → 21 → 22 → 23 → 24 → 25 → (52 charts) → 26 → 27 → 28 → 29. Topics 28 and 29 come around
days 38–43.

**Recording status** (`video_status.py --list record`):
- **Not yet recorded, so cheap to change:** all of t23–t26 except the summaries and wp-052-2/3/4 and wp-053 part 1. All of the
  t51 lessons, wp-001 and wp-027.
- **Already recorded or in production:** all of t21, t22 (except wp-001 and wp-027), t27, t28, t29 and every summary.

**Ratings.**
- Explained:
  - **clear** = meets W22/R37: what it is, why it works, worked examples, the trap.
  - **old style** = taught, but only in the older terse slide scripts. The lesson is usually a stub ("let's see it in two
    questions"), and the method lives in a few slogan lines inside a question video. That is below the W22/R37 standard.
  - **mentioned** = named or used, but not taught.
  - **missing** = not in the course.
- Practice:
  - **practised** = at least 2 course questions, and at least one of them has a video;
  - **thin** = 1 question, or written questions only;
  - **none** = no question.

---

## 1. Percentages (42 items, of which 9 are ratio items)

| Type | Exam count + ids | Explained where (rating) | Practised where (rating) | Flag |
|---|---|---|---|---|
| P1 Percent translation and chains ("a is 20% of b, so b is ?% of a", letters inside the percent, x% of (y·z)) | 10: 2019_winter_q1_04, 2024_spring_q1_16, 2020_spring_q2_10 (+2020_autumn_q2_05, 2021_autumn_q1_02, 2023_autumn_q2_14, 2024_autumn_q2_08, 2019_spring_q2_12, 2024_winter_q1_15, 2024_spring_q2_13) | wp-052-3 (the percent equation, a letter inside the percent), wp-053-3 (arrow map: along the arrow multiply, against it divide). The swap x% of y = y% of x is taught in g062 (**clear**) | g061 V, g062 V, g063 V, q-r26-t23-05 V, q-r26-t23-09, p09, p14, p26 (**practised**) | r37-t23.md says "no real question needs" the swap. In fact 2020_spring_q2_10 and 2024_winter_q1_15 are fastest with it. It can stay in g062. |
| P2 The same part of two wholes (the flip rule) | 2: 2020_autumn_q1_06, 2019_winter_q2_18 (the fraction version) | wp-053-4: flip versus keep, with the "only when the amounts are equal" condition (**clear**) | q-r26-t23-16 V, wp22-p24 (**practised**) | — |
| P3 Successive changes and multipliers (repeated growth or decay, sums of decaying terms, "first day above …") | 6: 2024_autumn_q1_03, 2022_winter_q2_17, 2023_spring_q1_16 (+2021_spring_q1_13, 2026_spring_q2_07, 2024_winter_q1_01) | wp-053, wp-053-2 (multipliers, up p then down p), wp-053-3 (working back from what is left) (**clear**) | g060 V, g065 V, q-r26-t23-01 V, p03, p07, p10, p24 (**practised**) | 2023_spring_q1_16 answers with weekday names: "the first day" = **Sunday**. The course never says that the Israeli week starts on Sunday (see gap 7). |
| P4 Reverse comparison ("x is 20% more than y, so y is 83⅓% of x"); a percent relative to an average | 2: 2023_spring_q2_12, 2020_winter_q1_17 | wp-053-3, last paragraphs (the exact 20% → 83⅓% trap) (**clear**) | p26, q-r26-t23-09, g061 V (**practised**) | 2020_winter_q1_17 also needs the averages balance, which is taught later (t25). |
| P5 Prices, discounts, wages after tax, fees | 6: 2019_winter_q2_01, 2020_winter_q2_16, 2025_winter_q1_20 (+2023_autumn_q1_08, 2023_winter_q1_16, 2020_spring_q1_20) | Discounts, multipliers and building the equation (wp-053-3, wp-037) (**clear**). A fee per unit added on top of a price is only a summary line, "a fixed fee is paid once" (mentioned). | g058 V, p17, p19, p20, p24 (**practised**) | 2025_winter_q1_20 (commission of 0.25 per shekel): no course question puts a fee on top of a per-unit price (see gap 10). |
| P6 Weighted mix (30% at 40, 70% at 20) | 1: 2025_spring_q2_18 | wp-086-3: "percent shares are weights" (**clear**) | g090 V, wp25-p27 (**practised**) | — |
| P7 Composition after adding (what stays the same) | 1: 2025_autumn_q2_03 | q-r26-t23-04 V; the lesson has only the summary line "add water? the salt stays" (**clear**, in the question video) | q-r26-t23-04 V, q-r26-t23-11, q-r26-t23-12, wp22-p35 (**practised**) | Under R37 this is close to core (4 course uses). |
| P8 Percent minimum and maximum with subgroups | 3: 2021_autumn_q2_11, 2023_winter_q1_13, 2025_winter_q1_15 | wp-068-2 (ranges in percent), wp-068-3 (another region) (**clear**) | wp24-p01, wp24-p03, g074 V, wp23-p06 (**practised**) | The weighted version (minimum number of *people* in AC cars, where cars hold 3 or 1) has no practice. |
| **P9 When is p% of N a whole number?** | **2: 2026_spring_q1_15, 2020_winter_q2_19** | **missing.** The nearest item, wp23-p03 (factors of 2 in a 50% rise), is a different idea. | **none** | See gap 5. |
| P10 Dividing by a ratio (units of x), counting ratios | 5: 2023_autumn_q2_06, 2022_autumn_q2_04, 2019_winter_q1_08 (+2022_autumn_q1_01, 2019_spring_q1_03) | wp-034 (3x + 7x = 50, matching arcs, the reversed "costs the same as") (**clear**) | g035 V, g036 V, wp22-p02, wp22-p04 (**practised**) | — |
| P11 Chained ratios (a shared member) | 2: 2020_spring_q2_06, 2025_autumn_q1_15 | q-r26-t22-01 V (common multiple of the shared member, the 2:3:5 trap); the lesson has only a summary line (**clear**, in the question) | q-r26-t22-01 V, q-r26-t22-06, wp22-p12 (**practised**) | — |
| P12 Ratio invariance (adding vs multiplying) and comparing proportions | 2: 2022_winter_q2_09, 2021_autumn_q2_16 | wp-034 says a ratio can be expanded or reduced. It never says that adding the same amount **changes** it (external-course-B #5) (**mentioned**) | **none** in t21–t29 | Plugging in numbers (t51) solves both, so the risk is low. |

## 2. Work and rate (34 items)

| Type | Exam count + ids | Explained where (rating) | Practised where (rating) | Flag |
|---|---|---|---|---|
| W1 Unit rate and comparing or combining rates (different units, factors with letters) | 8: 2020_autumn_q1_10, 2021_autumn_q1_06, 2024_spring_q2_02 (+2021_spring_q1_02, 2023_spring_q1_03, 2020_winter_q2_15, 2023_autumn_q1_11, 2025_winter_q2_01) | wp-092 (the triangle, units), wp-092-2 (direct and inverse), wp-092-3 (two changes), r26-t26-factors (**clear**) | g093 V, g103 V, p01, p02, p12, p16, p24 (**practised**) | — |
| W2 Working together with the job = 1 (a drain gets a minus, staged starts) | 6: 2022_autumn_q1_05, 2024_winter_q2_04, 2019_winter_q2_06 (+2025_autumn_q1_04, 2019_spring_q1_08, 2023_winter_q2_09) | wp-094, wp-094-2 (stretch to a common time, choose the job size, the product over the sum), wp-099 (done + left) (**clear**) | g095 V, g096 V, q-r26-t26-02 V, q-r26-t26-03 V, p11, p20, q-r26-t26-07, q-r26-t26-08 (**practised**) | — |
| W3 Identical machines and worker-hours | 3: 2024_autumn_q1_05, 2025_spring_q2_13, 2026_spring_q1_07 | wp-097, wp-097-2 (team-work-time table, the V), wp-099 (**clear**) | g098 V, g100 V, g105 V, g105b V, p05, p08 (**practised**) | — |
| W4 Consumption, unit cost and unit conversion (fuel per km, grams per kg, "A coats cost B", pencil life) | 5: 2020_spring_q1_05, 2021_spring_q2_18, 2020_winter_q1_16 (+2025_spring_q2_15, 2026_spring_q1_18 map scale → t36) | wp-028 and wp-031 are stubs, but the method is taught in g029, g030, g032 and g042 (ratio table, "label every number") (**clear**, in the questions). The letters case "A for B, so B/A each" is never stated as a rule (ext-B #1). | g029 V, g032 V, g042 V, q-r26-t22-04 V, wp22-p14 (**practised**) | 2020_winter_q1_16 also needs "at most", which means rounding down. |
| W5 Step-by-step processes (overflow day, bees, passing money on, snow decay, an elevator route, a 30-day month) | 7: 2020_autumn_q2_07, 2023_spring_q2_07, 2026_spring_q1_14 (+2025_winter_q2_13, 2019_spring_q2_07, 2025_winter_q1_04, 2023_winter_q2_04) | t21 wp-008 (write the steps one by one), wp-022, and the t21 summary "check the edges" (**clear**) | g009 V, g023 V, wp21-p05, wp21-p21, wp22-p30 (**practised**) | The exam files these under *work*, but t26 never points back to the t21 tools. The "first day = Sunday" gap applies to 2025_winter_q2_13. Work–rest cycles are absent (ext-B #7). |
| W6 Story equations: ages, fraction of a pool, "necessarily" with inequalities | 3: 2026_spring_q1_03, 2025_winter_q2_07, 2025_winter_q2_11 | wp-039 (give it to the little guy), the then-and-now table in the t22 summary, the fraction bar, and must/could/cannot in wp-001-2 (**clear**) | g039 V, wp22-p34, wp22-p07, wp22-p13, q-r26-t21-02 V (**practised**) | — |
| W7 Net gain per period (catching up a deficit; +10 or −1 stairs a minute) | 2: 2022_winter_q2_15, 2023_winter_q1_17 | The chase idea "close the gap at the difference of the rates" exists only in t27 wp-113, which comes after t26, and is never used for work. The stairs item is a number-theory insight (A ≡ ±1 mod 11) (**mentioned / missing**) | **none** | See gap 8. |

## 3. Combinatorics (24 items + 4 counting items labelled probability = 28)

| Type | Exam count + ids | Explained where (rating) | Practised where (rating) | Flag |
|---|---|---|---|---|
| C1 Product rule (outfits, passwords, kinds of house), with case splits and "not the same colour" | 6: 2021_spring_q2_16, 2022_winter_q2_18, 2026_spring_q2_20 (+2023_spring_q1_05, 2020_spring_q2_16, 2019_winter_q1_07) | wp-124-after "Multiply the Choices" has no example at all ("let's see how it works in two questions"). The method is in g125 V (stages, why multiply) and wp-134 (add or subtract cases) (**old style**) | g125 V, g135 V, g136 V, p03, p08, p11 (**practised**) | The core method of the topic has no real lesson (R37). The reverse item 2023_spring_q1_05 ("7 combinations, 3 sweaters, so at least 3 scarves") has no course question. |
| C2 Choosing a group, handshakes ("who stays out") | 4: 2023_autumn_q2_07, 2025_winter_q1_02, 2022_autumn_q1_16 (+2020_winter_q2_06) | wp-131 (stub), wp-137 (divide by k!, who stays out), r26-t28-cases (test a tiny case) (**old style**) | g132 V, g139 V, g143 V, g144 V, p01, p12 (**practised**) | — |
| C3 Arrangements with a restriction or repeated digits | 2: 2024_spring_q1_05, 2024_autumn_q1_07 | wp-141-after (forced digits); wp-137 checklist ("start with the most restricted position"); r26-t28-arrange is a stub (**old style**) | g142 V, q-r26-t28-08 V, q-r26-t28-21, p24 (**practised**) | — |
| C4 Pigeonhole and extreme sharing (19 delegates in 12 countries, n winners for n−1 countries, a circle) | 3: 2020_spring_q1_01, 2019_winter_q1_14, 2023_winter_q1_19 | t21 wp-016 rule 1. "Worst luck + 1" is taught well, but only in q-r26-t21-01 V and the summary (**clear**) | q-r26-t21-01 V, g007 V, g020 V, wp21-p27 (**practised**) | R37 lists "worst luck + 1" as a core method, yet it is not in any t21 lesson (t21 is recorded). |
| C5 Which totals are possible from given prices or values (incl. the number of different sums) | 5: 2019_winter_q2_05, 2025_spring_q1_03, 2024_winter_q2_16 (+2023_autumn_q1_04, 2021_autumn_q1_03) | wp-001 (list in order), the t21 summary's remainder test (**clear**) | g005 V, g013 V, wp21-p03, wp21-p10, wp21-p18 (**practised**) | — |
| C6 Minimum and maximum counts (majority vote, "more than 1/5 left", overlap of fractions, covering types) | 4: 2023_autumn_q2_01, 2024_spring_q2_17, 2022_winter_q1_17 (+2024_spring_q1_08) | t21 wp-016, t24 wp-068 (**clear**) | g017 V, g019 V, wp23-p06, wp24 g075 V (**practised**) | 2022_winter_q1_17 (the fewest types that cover 8 more prices and 6 more colours) has no similar course question. |
| C7 Inclusion–exclusion count of multiples ("divisible by 2 or 7") | 1: 2020_spring_q1_07 | Only the t29 summary line ("10 + 6 − 2") and the t24 counting rule (**mentioned**) | wp21-p08 (**thin**) | — |
| **C8 Structural counting** (grid colouring, cube vertices, worst-case key tries) | **3: 2020_autumn_q1_16, 2025_spring_q1_08, 2025_autumn_q1_03** | Keys: nothing in the lessons. Grid and cube: "list it" (wp-123) at most (**missing**) | wp28-p13 (7 keys, practice only) (**thin**) | Low priority. These are insight items, but the keys item (3 + 2 + 1 = 6) is teachable. |

## 4. Probability (17 items: the 24 labelled minus 4 counting and 3 averages)

| Type | Exam count + ids | Explained where (rating) | Practised where (rating) | Flag |
|---|---|---|---|---|
| Pr1 A single draw; probabilities add up to 1 (an unfair dice: x, 2x … 6x) | 2: 2026_spring_q1_02, 2020_winter_q1_18 | wp-146, wp-147-after (**old style**) | g147 V, g148 V, g150 V, p06, p18 (**practised**) | Unknown weights that add up to 1 appear only in p18 (practice only). |
| Pr2 Dice-sum tables (2 dice, a 4-sided die, 3 dice) | 3: 2019_spring_q2_13, 2023_spring_q1_17, 2025_spring_q2_16 | wp-159 (the pyramid, symmetry around 7, cards 1..n) (**old style**) | g154 V, g160 V, p05, p16 (**practised**) | No three-dice question ("sum at least 17" = 4/216). |
| Pr3 Independent repeats, "and" = multiply (incl. "the first can be anything", "ends after exactly two rounds") | 5: 2023_winter_q2_02, 2024_spring_q2_20, 2025_autumn_q2_16 (+2023_autumn_q1_14, 2019_winter_q2_19) | wp-151 gives the and/or rule with a single die example. The rest is in the summary (**old style**) | g152 V, g153 V, g162 V, p08, p09, p13, p20 (**practised**) | The main rule (the exam's commonest probability type) has a one-example lesson. |
| Pr4 Without replacement, and symmetry ("which two remain", "the gold ball among the two drawn", a draw that knocks players out) | 4: 2020_spring_q1_14, 2025_winter_q2_14, 2024_winter_q1_16 (+2024_autumn_q2_14) | No lesson. Taught in g157 V (the first pick doesn't matter), g158 V, g165 V and the summary's "door three, symmetry" (**old style**) | g149 V, g157 V, g158 V, g165 V, p22, q-r26-t29-08 (**practised**) | Core methods sit only in questions (R37). g158 (open 2 of 8 boxes) is exactly 2025_winter_q2_14. |
| Pr5 Exactly k of n | 1: 2022_autumn_q2_15 | r26-t29-more-rules (one order × the number of orders) (**old style**) | p11, p23, p25, all practice only (**thin**) | — |
| Pr6 Tree, dependent chain (the basketball shot depends on the last one; random paths) | 2: 2020_autumn_q2_17, 2022_winter_q1_06 | No lesson. q-r26-t29-03 V (tree, don't pour the boxes together), g164 V (**old style**) | q-r26-t29-03 V, g164 V, p10, p15 (**practised**) | The guide notes that a probability tree is "not in the Hebrew": new material, taught only in a question. |

## 5. Averages (23 items + 3 labelled probability = 26)

| Type | Exam count + ids | Explained where (rating) | Practised where (rating) | Flag |
|---|---|---|---|---|
| A1 Sum = n × average; a member joins or leaves; find how many | 8: 2026_spring_q2_15, 2020_winter_q2_20, 2024_spring_q1_07 (+2020_spring_q2_05, 2025_spring_q1_20, 2022_autumn_q2_03, 2024_winter_q2_07, 2019_spring_q1_04) | wp-081 (the balance for joining or leaving: compare to the new or the old average) (**clear**) | q-r26-t25-01 V, q-r26-t25-02 V, q-r26-t25-07, p21, q-r26-t25-11 (**practised**) | — |
| A2 Weighted average, combined groups, percent shares | 4: 2024_autumn_q2_01, 2021_spring_q2_09, 2023_winter_q1_04 (+2022_winter_q2_05) | wp-086, wp-086-2, wp-086-3 (the seesaw, shares as weights) (**clear**) | g089 V, g090 V, p20, p23 (**practised**) | — |
| A3 Deviations from the average (balance) | 2: 2025_autumn_q1_18, 2024_winter_q1_17 | wp-080-2 (differences add up to zero) (**clear**) | g085 V, p18 V, p16 (**practised**) | — |
| A4 "Necessarily" statements, equivalent expressions, ranges | 7: 2026_spring_q1_04, 2022_winter_q1_08, 2023_spring_q1_14 (+2020_autumn_q2_15, 2023_autumn_q1_03, 2025_autumn_q2_15, 2023_spring_q2_15) | wp-081-3 (an inequality balance that is almost identical to 2026_spring_q1_04), wp-080-2 (the average lies between the smallest and the largest) (**clear**) | g084 V, p02, p04, p09, p10, p12 (**practised**) | — |
| A5 Letters (average = difference, sum vs average, average of x and 1/x) | 3: 2024_autumn_q1_08, 2025_winter_q2_16, 2023_autumn_q2_15 | wp-081-3 (average = difference) (**clear**). "x > 1 and xy = 1, so the average is > 1" is **missing**, although plugging in numbers solves it. | p01, p11, p18 V (**practised**) | Minor. |
| A6 The smallest possible maximum given a total | 1: 2025_spring_q1_05 | wp-081-2 (the phone-calls example is almost identical); t21 wp-016 rule 2 (**clear**) | q-r26-t25-03 V, g020 V, p14 (**practised**) | — |
| A7 Average speed with equal times | 1: 2019_spring_q2_19 | t27 wp-108-after ("equal times? the plain average is right") (**old style**) | g109 V, q-r26-t27-21, q-r26-t27-22 (**practised**) | — |

## 6. Motion (12 items)

| Type | Exam count + ids | Explained where (rating) | Practised where (rating) | Flag |
|---|---|---|---|---|
| M1 d = vt, units, letters, a circular route (2πr) | 4: 2021_autumn_q2_01, 2022_autumn_q2_09, 2025_winter_q1_16 (+2021_spring_q2_13) | wp-106 (slide style: the triangle, a table, "forget 3.6") (**old style**) | g107 V, g117 V, q-r26-t27-06 V, p02, p13 (**practised**) | No course motion question uses a circumference (2021_spring_q2_13). |
| M2 Speed ratios and two changes at once | 3: 2023_spring_q2_05, 2025_autumn_q2_20, 2025_spring_q1_16 | wp-110 (what is fixed; the V with distance in the middle) (**old style**) | q-r26-t27-31 V, g111 V, g112 V, p17 (**practised**) | — |
| M3 Head start and chase | 2: 2020_autumn_q2_18, 2026_spring_q2_17 | wp-113 (add or subtract the speeds, the starting gap only) (**old style**) | g115 V, g116 V, p07, p20 (**practised**) | Ext-B #12: from whose start is the time counted? 2026_spring_q2_17 depends on it. |
| M4 Special cases: a train's length, meeting on a circular track | 2: 2024_winter_q1_14, 2024_autumn_q2_10 | r26-t27-special says "we'll learn each one in its question". So only q-r26-t27-01 V and g121 V (**old style**) | q-r26-t27-01 V, q-r26-t27-09, g121 V, q-r26-t27-03 V, p14, p19 (**practised**) | These core cases are deferred to the questions (R37). |
| M5 Estimating a travel time | 1: 2023_autumn_q2_18 | t51 pt51-estimation (**clear**) | solve-pt-q16–q19 V (**practised**) | — |

## 7. Overlapping sets (6 items; overlap items under other labels are counted in P8 and C6)

| Type | Exam count + ids | Explained where (rating) | Practised where (rating) | Flag |
|---|---|---|---|---|
| O1 Two-group range (minimum and maximum overlap; the total is "a day") | 2: 2019_spring_q2_04, 2020_winter_q1_14 | wp-068, wp-068-2 (the machines lit 14 and 16 hours a day are almost identical to the lamps), wp-068-3 (**clear**) | g074 V, g075 V, q-r26-t24-01 V, p01, p07, p16 (**practised**) | — |
| O2 Exact two-group (the squares method) | 1: 2024_winter_q2_02 | wp-067-3, wp-069 (**clear**) | g070 V, g071 V, g078 V, p04, p09, p17 (**practised**) | — |
| O3 Three groups at least and at most (pair limit, count who misses) | 2: 2023_autumn_q2_20, 2024_autumn_q1_19 | r26-t24-three-groups (**clear**) | q-r26-t24-03 V, q-r26-t24-09, q-r26-t24-12, p13 (**practised**) | — |
| O4 Overlap inside a split population (adults and children, where one child can take both classes) | 1: 2020_autumn_q1_11 | Two-way tables, and "neither is the overlap of the not-groups" (**mentioned**) | **none** | See gap 9. |

## 8. Factorials (12 items)

| Type | Exam count + ids | Explained where (rating) | Practised where (rating) | Flag |
|---|---|---|---|---|
| F1 Recognising a factorial (720, 120) | 2: 2020_autumn_q1_04, 2025_spring_q1_14 | wp-140-after "know them by sight" (**old style**) | g140 V, p06, q-r26-t28-31 (**practised**) | — |
| F2 A ratio of factorials = a run of neighbours (x!/y! = x, b! = 42·a!, n!/(n−2)!, (n+1)!/((n−2)!·n), 121!/120!) | 6: 2021_autumn_q2_05, 2022_autumn_q1_17, 2026_spring_q2_18 (+2021_spring_q1_05, 2022_winter_q2_07, 2025_winter_q1_07) | wp-140-after ("stop early", "a run of neighbours", worked backwards 56 = 7·8) (**old style**) | g140 V, q-r26-t28-29 (**practised**) | Sanity check: 2022_autumn_q1_17 (42 = 6·7, so a = 5) and 2026_spring_q2_18 ((n+1)(n−1) = 35) both solve directly with this method. The content is right; the delivery is a 2-minute "quick extension". |
| F3 Sums and differences: take out the smaller factorial | 2: 2020_winter_q1_19, 2024_winter_q2_17 | wp-140-after, last line only ("next, a question with a minus sign"), then q-r26-t28-28 V (**old style**) | q-r26-t28-28 V, q-r26-t28-31 (**practised**) | — |
| F4 Counting prime factors in a factorial | 1: 2019_winter_q2_16 | wp-140-after ("count the twos: four hides two of them") (**old style**) | wp28-p02 (practice only) (**thin**) | — |
| F5 Identity: k!·2^k = 2·4·…·2k | 1: 2025_autumn_q1_17 | Only plugging in numbers (t51) (**mentioned**) | **none** | Minor. |

---

## Totals

- **Types: 54** (percentages 12, work 7, combinatorics 8, probability 6, averages 7, motion 5, overlap 4, factorials 5).
- **Explained:** 29 clear; 18 old style (taught, but below W22/R37); 5 mentioned; 2 missing.
  - The **old-style** types are all of probability (6), motion M1–M4 (4), combinatorics C1–C3 (3), factorials F1–F4 (4) and A7.
  - The **mentioned** types are P12, W7, C7, O4 and F5.
  - The **missing** types are P9 and C8.
- **Practice:** 45 practised, 4 thin (C7, C8, Pr5, F4), 5 none (P9, P12, W7, O4, F5).
- **Where the weakness sits:**
  - **t23–t26 are strong.** Nearly every exam type there has a W22 lesson, and several lesson examples are almost the same
    as real items (phone calls = 2025_spring_q1_05, the inequality balance = 2026_spring_q1_04, machines 14/16 h =
    2020_winter_q1_14, g158 = 2025_winter_q2_14).
  - **Topics 27–29 are the weak spot.** They carry about 69 real items (counting 28, probability 17, motion 12,
    factorials 12) that are taught only in the older terse format.

## Gaps and weak spots, ranked (exam count × weakness)

**1. Factorials: 12 exam items, taught only in a 2-minute slide "extension" (old style).**
- **Where now:** wp-140-after inside t28 (recorded), on about day 38 of the plan. The exam files factorials under algebra and
  asks about them as often as it asks about motion.
- **What to add:** a real lesson (R37) in t28 right after the arrangements lesson (n! needs "n items in a row"). Teach:
  - what n! is, and the values to know by sight up to 7!;
  - "stop early" (9! = 9·8·7!);
  - a run of neighbours, with its condition (whole numbers, a > b) and the backwards case (b!/a! = 56 → 7·8 → a = 6);
  - taking out the smaller factorial in a sum or difference;
  - counting primes ("4 hides two 2s").
- **Examples and practice:** 2–3 worked examples each from an easy one, and 2 more practice items with a video for F4
  (prime counting) and F3.
- **Cost:** it needs a new reading script, because t28 is recorded.

**2. Probability lessons: 17 exam items, old style throughout.**
- **What's wrong now:**
  - wp-146 and wp-147-after are definitions only;
  - wp-151 teaches "and = multiply" (the commonest type, 5 items) with one dice line;
  - without replacement and symmetry (4 items) and the tree (2 items) have **no lesson**. They live in g157, g158, g165 and
    q-r26-t29-03.
- **What to add:** t29 lessons in the W22 format:
  - (a) "and" = multiply, plus "the first can be anything";
  - (b) without replacement: count the bag as it is now; "drawn together = one after the other";
  - (c) symmetry ("nobody is special": the 6th ticket, which two remain);
  - (d) the tree (multiply along a branch, add the branches; don't pour bags together).
- **Examples to use:** new-number versions of 2020_spring_q1_14 and 2020_autumn_q2_17.
- **Cost:** t29 is recorded, so these are new videos.

**3. Counting lessons: 28 exam items. The core lessons are empty stubs.**
- **The stubs:** wp-124-after "Multiply the Choices", wp-127 "With or Without Repetition", wp-131 "Mutual Action" and
  r26-t28-arrange each say only "let's see it in two questions". The product rule, the topic's main method, is never
  taught in a lesson.
- **What to add:** a W22 lesson with stage slots, why we multiply, why adding is wrong, restrictions first, and complements
  ("49 − 18" for 2021_spring_q2_16).
- **Questions to add:**
  - a reverse item: "7 different outfits, 3 sweaters, so at least ⌈7/3⌉ = 3 scarves" (2023_spring_q1_05);
  - a worst-case keys video (2025_autumn_q1_03: 3 + 2 + 1). It now exists only as wp28-p13, practice only.

**4. Motion: 12 exam items, old-style slide lessons, special cases taught only in questions.**
- **Where now:** wp-106, wp-110, wp-113 and r26-t27-special ("we'll learn each one in its question"), all recorded.
- **What to add:**
  - in the lesson, a train passing a post versus a bridge, and meeting on a circular track (once every lap gained), each
    with 2 examples;
  - the ext-B tip "from whose start is the time counted" in wp-113;
  - one practice item with a circumference route (2021_spring_q2_13).

**5. P9: when is p% of N a whole number? 2 items. Missing, no practice.**
- **The items:** 2026_spring_q1_15 (the smallest N whose 3% is whole = 33⅓) and 2020_winter_q2_19 (6% of a is whole, so
  a is divisible by 50, so it is necessarily divisible by 25).
- **Sanity check:**
  - Plugging in the answers does solve the first one: 12½ gives 0.375 and 30 gives 0.9, both out; 33⅓ gives exactly 1.
  - The second one defeats a weak student. a = 100 passes both 20 and 25, so plugging in numbers only works with a = 50,
    which the student has to find.
- **What to add:** a one-off question video in t23, which is unrecorded:
  - write p% as a reduced fraction (6% = 3/50);
  - N must be a multiple of the denominator;
  - the trap is "a multiple of 100";
  - plus 2 practice items.
  - It could also be linked to t15 (divisibility), which comes later in the plan.

**6. Probability and counting minor types: Pr5 exactly k of n (thin), Pr1 weights that add up to 1 (thin), three-dice sums (none).**
- **The items:** 2022_autumn_q2_15, 2020_winter_q1_18 and 2025_spring_q2_16.
- **What to add:** one video question each in t29. The current practice is written only.

**7. "The first day of the week is Sunday": 2 items, never said.**
- **The items:** 2023_spring_q1_16 (cherries; the answers are weekday names) and 2025_winter_q2_13 (snow). An English-speaking
  student will start the week on Monday and choose the wrong day.
- **What to add:** one sentence in the first t23 question that uses consecutive days (unrecorded), or in t21 wp-022, the
  cycles lesson (recorded).
- **Data caveat:** 2025_winter_q2_13 says "decreased by 1/3", but its key (Wednesday) needs "decreased **to** 1/3"
  (100 → 33.3 → 11.1 → 3.7). Check the source before using it.

**8. W7: net gain per period ("catch up the deficit"): 2 items, none.**
- **The items:**
  - 2022_winter_q2_15: the deficit is 10 days × 4 h = 40 h, the machine gains 20 h a day, so x = 2;
  - 2023_winter_q1_17: +10 or −1 stairs a minute;
  - the work–rest cycles of ext-B #7 are the same family.
- **What to add:** a t26 question video (unrecorded) that frames it as the chase idea: the gap closes at the difference of the
  rates. Add a work–rest-cycle practice item.

**9. O4 and P8 weighted: overlap inside a split population, and the minimum when members carry weights. 2 items, none.**
- **The items:**
  - 2020_autumn_q1_11: children can fill both classes, so 100 + 60 places go to children, only 20 adults are forced in, and
    at most 180 adults are in neither;
  - 2021_autumn_q2_11: the minimum overlap is 18 + 12 − 20 = 10, so 10 three-person cars + 8 one-person cars = 38.
- **What to add:** one advanced t24 question video (unrecorded) after r26-t24-two-way. Its lesson point: decide which overlap
  makes the asked region small, then apply sum − total.

**10. P12 and W4: ratio invariance, and price per item with letters. 2–3 items, mentioned only.**
- **The items:** 2022_winter_q2_09 (adding 3,000 to both salaries changes the ratio) and 2020_winter_q1_16 (A coats for B,
  so C shekels buy at most ⌊AC/B⌋).
- **What to add:**
  - the ext-B one-liners, given their sentences and an example per W22: "× or ÷ both keeps a ratio, + or − the same amount
    changes it"; "price per item = total ÷ number of items, also with letters";
  - a fee-on-top practice item for P5 (2025_winter_q1_20: each unit costs 0.5 + 0.125);
  - since t22 is recorded, put them in a new t22 practice question with a video.

**Smaller items, not ranked:**
- C8 grid and cube colouring (2 insight items; leave them);
- the average of x and 1/x (A5, 1 item);
- C7 multiples of 2 or 7 (thin: only wp21-p08);
- the reverse "worst luck + 1" is in no t21 lesson, only q-r26-t21-01 and the summary. It is taught well there, so it is
  low priority while t21 stays recorded.
