# Real-exam coverage audit: Charts & Tables (topic 52)

21 Oct 2026. This audit is read-only: no course file was changed.
Real items: `quant_real.md` subtopic `charts_tables`. That is 163 questions in 38 chart sets, from 19 English sections (2019–2026).
Course: `t52.txt`, which has 30 videos:
- 14 lessons;
- 15 solution videos `solve-ch-q01..q15`, covering 3 sets (planets scatter, car-race tables, wedding bars + pies).

The written self-practice is 20 sets with 87 questions: `chp01..chp20` in `modulesV52c-f.py`. These are [practice] items with written explanations only. In the study plan (planData ORDER), the chart lessons and units 1–5 come on day 24, units 6–10 on day 30, units 11–15 on day 37 and units 16–20 on day 44.

Limits of this audit:
- The real items have no chart images. Each item is classified by what it asks, and each set's format is inferred from its wording.
- `video_status.py --list record` lists **every** topic-52 video, including `ch52-*` and `solve-ch-*`. So none of them is recorded yet, and every fix below is cheap.

Practice rating rule: **practised** = at least 2 course questions, and at least one of them has a video. **thin** = 1 question, or written questions only. **none** = no question.

---

## 1. Chart formats (what the page looks like)

The intro lesson (`ch52-intro`) says: *"In about ninety-five percent of the sets, the chart is one of the types we learn here."* The real sets do not support that.

| Format | Real sets (questions) | Examples | Course lesson | Course practice |
|---|---|---|---|---|
| Table (incl. multi-number cells, ranking tables) | 7 sets (~32) | 2020_autumn_q1, 2022_autumn_q2, 2023_autumn_q1, 2020_winter_q1, 2023_winter_q2, 2025_winter_q1 | ch52-tables, ch52-intro-3, ch52-range (3-number cells) (**clear**) | Set 2 [VIDEO], chp04/06/08/09/10/12/15/18 |
| Bars (side-by-side, inside, stacked, % stacked) | 7 sets (~30) | 2020_autumn_q2, 2020_spring_q1, 2023_spring_q2, 2022_winter_q1, 2024_winter_q2, 2025_winter_q2 | ch52-bar (**clear**) | Set 3 [VIDEO], chp07, chp14 |
| Line / position lines | 4 sets (~17) | 2022_autumn_q1, 2019_spring_q1, 2024_spring_q1, 2021_autumn_q2 | ch52-line (**clear**) | chp05, chp16 |
| Points / bubble grid | 1 set (5) | 2024_autumn_q2 | ch52-scatter (**clear**) | Set 1 [VIDEO], chp01, chp02 |
| Range / regions | 1 set (4) | 2020_winter_q2 | ch52-range, ch52-regions (**clear**) | chp02, chp20 |
| Circle (radial) / pie | 2 sets (8) | 2022_winter_q2 (radial), 2021_spring_q1 (roulette pies) | ch52-circle is radial only. Pie slices appear only inside set 3 (**mentioned**) | Set 3 pies [VIDEO] |
| Cumulative | 1 set (4) | 2019_spring_q2 (divisions arriving) | ch52-cumulative (**clear**) | chp12, chp15-q1, chp16 |
| % change from a fixed base (index chart) | 1 set (4) | 2025_spring_q1 (lemons vs week 0) | ch52-change teaches absolute change only (**mentioned**) | none |
| Histogram with unequal-width groups | 1 set (4) | 2019_winter_q2 (heights) | **missing** | none |
| **Timeline / Gantt / timetable / schedule** | **8 sets (~35)** | 2021_autumn_q1 (absences), 2025_autumn_q2 (print jobs), 2026_spring_q1 (musicians), 2024_winter_q1 (trainings), 2019_winter_q1 (exam dates), 2020_spring_q2 (Tali's job grid), 2024_autumn_q1 (game order), 2023_autumn_q2 (guard rota) | **missing** | chp07 (employment bars), chp11 (stork sightings), chp16 (time journey): written only |
| **Network / path diagram / bracket** | **5 sets (~20)** | 2021_spring_q2 (bus lines), 2024_spring_q2 (flights), 2026_spring_q2 (college paths), 2023_winter_q1 (tournament tree), 2025_winter_q1 (meetings matrix) | **missing** | chp19 (pier-lines matrix, no path questions) |
| Map / area diagram / Venn | 3 sets (13) | 2023_spring_q1 (plots map), 2025_autumn_q1 (circular trail), 2025_spring_q2 (roaming-area Venn) | Venn comes from topic 24. Map: missing (**mentioned**) | chp03 (hike profile) |

About 40% of the real sets (timelines, networks, maps, histograms and index charts: about 75 of 163 questions) use a format the lessons never show.

---

## 2. Question types

| # | Type | Exam count + ids | Explained where (rating) | Practised where (rating) | Flag |
|---|---|---|---|---|---|
| 1 | Read a value / find the largest or smallest (one read, or a difference of two reads) | 20: 2022_autumn_q1_11, 2023_autumn_q1_16, 2019_spring_q1_20 | ch52-intro (check the example), ch52-tables, ch52-bar (stacked part = the gap), ch52-cumulative (**clear**) | solve-ch-q03, q06 [VIDEO]; chp02-q1, chp03-q1/q2, chp05-q3, chp08-q4, chp11-q1, chp12-q1, chp20-q1 (**practised**) | – |
| 2 | Count the periods/items that meet a condition (threshold, "more than the year before", both families) | 11: 2023_spring_q2_16, 2020_autumn_q2_12, 2025_winter_q2_18 | ch52-scatter "counting with a line" (point on the line ≠ more than); solve-ch-q01 (**clear**) | q01 [VIDEO]; chp02-q3, chp03-q5, chp05-q1, chp07-q2, chp09-q1, chp11-q3/4, chp14-q1, chp18-q1, chp20-q2 (**practised**) | – |
| 3 | A defined term in the question ("safe company", "close survey") → which one / how many | 11: 2022_autumn_q1_09, 2020_winter_q1_10, 2025_spring_q2_08 | solve-ch-q02, q07, q11 (circle the condition, "three or more" includes 3) (**clear**, taught in the questions) | q02, q07, q11 [VIDEO]; chp04-q2, chp08-q1, chp14-q2, chp15-q3, chp18-q3, chp20-q3 (**practised**) | – |
| 4 | Ratio / per-unit comparison across categories (a × b or a / b, relative frequency) | 7: 2020_autumn_q1_17, 2023_spring_q1_11, 2024_winter_q2_08 | ch52-scatter (vehicles per dealer, estimate 100/15 < 10); solve-ch-q14 (need both % and total) (**clear**) | q14 [VIDEO]; chp01-q3/q4, chp06-q4, chp14-q3, chp04-q4 (**practised**) | – |
| 5 | Percent: part of the whole, % change, percent gap | 10: 2020_autumn_q1_18, 2022_winter_q1_10, 2025_spring_q1_09–11 | ch52-tables ("the whole comes after *of*"), ch52-continuous (relative increase) (**clear**). The index chart (each bar = % change from week 0) is not taught | q12 [VIDEO]; chp01-q1, chp06-q3, chp07-q4, chp10-q1/q3, chp13-q3, chp18-q2, chp19-q1 (**practised**) | index charts: gap 9 |
| 6 | Reverse: the chart is in %, one real number is given → find the total or identify the item | 5: 2025_winter_q2_17, 2020_spring_q1_11, 2025_spring_q1_12 | Only in topic 23 (ratio row). No chart example (**mentioned**) | chp07-q3, chp13-q3, chp17-q2, written only (**thin**) | gap 7 |
| 7 | Average, total = count × average, median group | 6: 2019_spring_q2_11, 2024_winter_q2_11, 2019_winter_q2_11 | ch52-tables (symmetric average), solve-ch-q08 (balance), q10 (same total, same count), q15 (seesaw) (**clear**). Statistical median: not taught anywhere | q08, q10, q15 [VIDEO]; chp03-q4, chp05-q4, chp06-q1, chp12-q5, chp19-q2 (**practised**) | median: gap 8 |
| 8 | Multi-step rate / unit / time calculation (litres for a distance, pages per hour, walking time, money earned and lost, points) | 12: 2020_autumn_q1_19/20, 2025_autumn_q2_10, 2022_winter_q1_12 | No t52 example of a rate read from a chart. Topic 26 (rates) is studied after the chart lessons (ORDER: [52,"ch52-"], then [26]) (**mentioned**) | solve-ch-q09 [VIDEO] is a sum, not a rate; chp04-q1/q5, chp09-q4, chp10-q4, chp15-q4, chp19-q4, written (**thin**) | gap 6 |
| 9 | Choose the graph that fits (mini-graphs as choices) | 9: 2020_autumn_q2_11, 2021_autumn_q1_10, 2024_winter_q2_09 | solve-ch-q05 (find where they differ, start at the edges) (**clear**) | q05 [VIDEO]; chp15-q1 (**practised**) | – |
| 10 | Bounds: at least / at most / range of possible values from incomplete data | 8: 2021_autumn_q1_12, 2022_autumn_q2_20, 2026_spring_q2_04, 2024_winter_q2_12 | ch52-bar (overlap 30 to 50), ch52-range (max − min, min − max), topic 24 (**clear**) | chp01-q2, chp02-q4, chp13-q2/q4, chp14-q4/q5, chp17-q3, written only (**thin**) | minor |
| 11 | Possible / impossible / necessarily true / can't be known (deduction on the chart or its rules) | **29**: 2023_autumn_q2_09–13, 2020_winter_q2_09–12, 2023_winter_q1_12, 2025_winter_q2_20 | solve-ch-q04 (necessarily = no exception), q13 (whole people), ch52-circle (most ≠ all → can't be known), ch52-range ("what can't it be"); topic 51 (**clear**) | q04, q13 [VIDEO]; chp03-q3, chp04-q3, chp05-q2, chp06-q2, chp09-q2/q3, chp10-q2, chp11-q2/q5, chp12-q3/q4, chp13-q1, chp15-q2, chp17-q1/q5, chp19-q3 (**practised**) | Largest type, but only 2 videos, both on standard charts: gap 4 |
| 12 | Timeline / interval questions (how many are active at time t, durations, gaps, "never at the same time", matching a described day) | 17 (by type; ~35 counting the format): 2025_autumn_q2_09, 2026_spring_q1_10, 2021_autumn_q1_11, 2024_winter_q1_11 | **missing.** ch52-scatter's "the line can also stand up" is the right tool, but no lesson shows interval bars (start, end, length, touching ends) | chp07, chp11, chp16, written only (**thin**) | **gap 1** |
| 13 | Paths and reachability on a network (direct pairs, reach everyone, longest path with no repeat, fewest stops, visit each once) | 9: 2024_spring_q2_09–12, 2021_spring_q2_02–04, 2026_spring_q2_02/03 | **missing** | none (chp19 is a lines matrix with no path questions) (**none**) | **gap 3** |
| 14 | Probability from a chart (pie sectors as probabilities, independent spins, a "chance" from a table) | 6: 2021_spring_q1_17–20, 2023_autumn_q2_11, 2023_winter_q2_16 | t29 (product rule, equal-section spinners) is **clear** but comes on day ~43. Unequal pie sectors as probabilities: not taught (**mentioned** in the chart context) | chp08-q2 (day 30, *before* t29), written only (**thin**) | order + gap 5 |
| 15 | Rankings (place numbers: "rose in the ranking" = the number got smaller; places shifting) | 3 (+ the 2019_spring_q1 relative-position set): 2024_spring_q1_11, 2023_autumn_q1_17 | Set 2 uses places (solve-ch-q06/q07). The direction trap is never said (**mentioned**) | q07 [VIDEO]; chp12-q1/q2 (**practised**) | gap 10 |

**Counts.**
- Types: **15**.
- Explained: **clearly 9**, **mentioned 4** (types 6, 8, 14, 15), **missing 2** (types 12, 13).
- Practised: **practised 9** (types 1–5, 7, 9, 11, 15), **thin 5** (types 6, 8, 10, 12, 14), **none 1** (type 13).

---

## 3. Sanity checks (solved with the course's own method)

- **2025_autumn_q2_09** ("at which time were the most jobs printing?", a Gantt chart). The course's tool is the scatter-lesson line, "the line can also stand up". It does carry over: put a vertical line at 8:30, 10:35, … and count the bars it crosses.
  But no lesson shows bars that are *time intervals*. So a weak student has to work out alone that:
  - a bar's length is its duration;
  - a bar that ends exactly at 10:35 is a borderline case the question fixes;
  - "in printing processes" means between the bar's left and right ends.

  **The gap is real, but partial:** the tool exists, the reading does not.
- **2026_spring_q1_10** (how many musicians were playing at 3¼ min in all three pieces) is the same vertical-line count, done three times. Nothing in the course practises intersecting time slices like this.
- **2024_spring_q2_11** (the most direct flights in a row without repeating a country). This needs a systematic search on a directed graph: start from a country with no incoming flights and follow the arrows. Nothing in t52, t28 or t51 teaches how to read an arrow diagram or search it. **The gap is real.**
- **2021_spring_q1_19** (1,1,1 and then 2,2,2 = 1/432). The t29 product rule solves it, *once* the student reads each sector's fraction from the pie: an unequal sector gives its share of 360°, or of the circle, as the probability.
  - t29 only uses equal sections.
  - The chart unit that holds a probability question (chp08-q2) comes on day 30, before t29 (day 43).
  - Units 16–20 (day 44, after t29) have no probability question.

  **The gap is real:** it is an order problem plus the unequal-sector step.
- **2020_autumn_q1_20** (4 boats sail 3 km → litres). Litres = km ÷ km-per-litre × boats, for example 3 ÷ 15 × 4 = 4/5. That is easy once rates are known, but t26 is studied after the chart lessons, and no t52 example reads a "per" column. **The gap is real but mild.**

---

## 4. Gaps and weak spots, ranked (exam count × weakness)

All the target videos are **not recorded yet** (every `ch52-*` and `solve-ch-*` is on the `--list record` list), so editing them costs nothing.

1. **Timeline / interval charts.** About 35 questions in 8 sets (2021_autumn_q1, 2025_autumn_q2, 2026_spring_q1, 2024_winter_q1, 2019_winter_q1, 2020_spring_q2, 2024_autumn_q1, 2023_autumn_q2). The explanation is missing and the practice is written only.
   - **Where:** a new lesson `ch52-timeline` right after `ch52-bar`, since horizontal bars are its prerequisite.
   - **What to teach:**
     - each bar is a period: left end = start, right end = end, length = duration;
     - a vertical line at time t, then count the bars it crosses;
     - check the endpoints;
     - gaps between bars of the same row;
     - "never at the same time" means no vertical line crosses both rows;
     - a timetable grid (day × hour) is the same idea.
   - **Worked example:** a 6-job print-shop-style chart with new numbers.
   - **Practice:** add one solution-video set (4 questions: active at t, total duration, coordinated pairs, which described day matches). Point the written chp07/chp11/chp16 explanations back to the lesson.
2. **The "95%" claim in `ch52-intro`.**
   - **Problem:** this one sentence is wrong for 2019–2026: about 40% of the sets use other formats. A student who believes it can freeze on a timeline or a network.
   - **Change:** "Most sets use these types. The rest are diagrams whose rules are written in the explanation, and the same method works: read the explanation, check the example, then answer."
3. **Network / path diagrams.** About 20 questions in 5 sets (2024_spring_q2, 2021_spring_q2, 2026_spring_q2, 2023_winter_q1 bracket, 2025_winter_q1 matrix). The explanation is missing and there is no practice.
   - **Where:** a new lesson `ch52-network` after `ch52-regions`, or at the end before `ch52-summary`.
   - **What to teach:**
     - nodes and lines, and one-way arrows vs two-way lines;
     - a mutual pair (an arrow each way);
     - "reachable, not necessarily direct": follow the arrows, list where you can get to;
     - fewest stops: go outward one step at a time;
     - "visit each once": start at the dead ends;
     - a tournament tree read from the bottom up.
   - **Practice:** a new solution-video set of 4 questions (flight-style arrows with new countries/names), plus one written set.
4. **Possible / impossible / necessarily questions on rule-based charts.** 29 questions, the largest type.
   - The explanation is good, but only q04 and q13 have videos, and both are on standard charts. Many real ones are deductions on a schedule or rota (2023_autumn_q2_09–13, 2020_winter_q2_09–12).
   - **Add:** one more solution video that teaches the method:
     - "necessarily": try to break it with one case;
     - "possible": build one case;
     - "can't be known": find two cases that give different answers.

     Put it on the timeline set from gap 1, so one set fixes both gaps.
5. **Probability in charts.** 6 questions (2021_spring_q1 roulette set, 2023_autumn_q2_11, 2023_winter_q2_16).
   - **Order:** move chp08-q2 to after t29, or swap it for a non-probability question.
   - **Content:** add one pie-roulette question with unequal sectors to the units 16–20 block (day 44, after t29), as a written question, or as a video if a set is added. Its key line: "a sector's share of the circle is its probability; spins are independent, so multiply".
6. **Rates read from a chart.** 12 questions (2020_autumn_q1_19/20, 2025_autumn_q2_10/11, 2024_winter_q2_11).
   - **Where:** `ch52-tables`, which already brings in percent, average and overlap.
   - **What:** a fourth "inside a table" example with a "per" column (km per litre → litres for a trip = distance ÷ km per litre). Say it in one line: "a 'per' column is a rate: amount = rate × how many".
   - **Note:** t26 comes after the chart lessons, so the example must stand on its own.
7. **One real number turns the percent chart into counts.** 5 questions (2025_winter_q2_17, 2020_spring_q1_11, 2019_winter_q2_10).
   - **Where:** `ch52-bar`, at the end of the percent-stacked part, or in `ch52-tables`.
   - **What:** "20% ↔ 1,200 is one row of the ratio table, so 100% ↔ 6,000" (topic 23), with a worked example and a solution video on one written item.
8. **Histograms and the median group.** 5 questions (2019_winter_q2_09–12).
   - **Where:** a short part in `ch52-bar`.
   - **What to teach:**
     - groups on the bottom axis can have different widths, so compare counts, not bar widths;
     - splitting a group spreads its count;
     - "as many taller as shorter" = the middle person: add up the counts from one end until you pass half.
   - **Note:** the statistical median is not taught anywhere in the course (t25 has no median). chp08-q3 and chp20 define it inside the question.
9. **Index charts: % change from a fixed base.** 4–5 questions (2025_spring_q1_09–12, 2020_autumn_q1_18).
   - **Where:** `ch52-change`, after the volunteers example.
   - **What:** a short second case, "each bar is the percent change from week zero, *not* from the bar before". Example: week 0 = 1,500, +20% → 1,800. Comparing two plots in the same week means comparing their percents.
10. **Ranking direction.** 3 questions plus the 2019_spring_q1 set.
    - **Where:** a single line in `solve-ch-q07` or `ch52-line`: "In a ranking, going *up* means the number gets *smaller*: from 5th to 2nd is a rise of three places."

Not gaps:
- Reading values, counting with a line, defined terms, ratio comparisons, choosing the graph, averages and the basic percent questions are taught clearly and practised, with videos.
- Map/Venn sets (2025_spring_q2, 2023_spring_q1) lean on topic 24 Venn and on geometry areas, which are already taught. At most, one sentence in the intro ("some sets are a map or a Venn diagram; the explanation gives its rules").
