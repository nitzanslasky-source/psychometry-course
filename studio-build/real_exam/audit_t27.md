# Audit T27 - Motion (additions by the 2026-09 fixers)

Source: `math_patches/t27_CHANGES.md`, `math_patches/t27.py`. Real exam: regenerated `real_exam/quant_real.md` (motion_speed group, 12 q., read in full; plus work_rate, averages, charts_tables, percentages keyword hits). All cited ids re-checked against the regenerated file.
Rule 2 (coordinator): an added method/type that ORIGINAL course questions already need is kept ("orig" in the Evidence column names the original question).

Real-exam motion picture: 12 questions - basic d = v·t (2021_autumn_q2_01, 2023_autumn_q2_18, 2025_winter_q1_16), letters (2022_autumn_q2_09, 2025_autumn_q2_20), ratios (2023_spring_q2_05), chase / head start (2020_autumn_q2_18, 2026_spring_q2_17), parts of a trip (2025_spring_q1_16), circular track same direction (2024_autumn_q2_10), circle length (2021_spring_q2_13), train passing a man (2024_winter_q1_14). Average speed appears once, in the averages group (2019_spring_q2_19). No current/wind, no two trains passing, no meeting-twice, no percent-speed, no distance-time graph question.

| Addition | Where | Class | Verdict | Evidence (real ids / count) |
|---|---|---|---|---|
| Average Speed slide 4: "equal distances → closer to slower" now conditional; "equal times → plain average" added | wp-108-after slide 4 "Not the average" | FIX | KEEP | 2019_spring_q2_19 (60/40 average 50 → equal times) |
| "Honestly? Rare on the exam." removed | wp-108-after slide 1 | FIX | KEEP | - |
| Q12 estimate slide corrected | solve-wp27-g120 slide 4 "Method 3 · Estimate" | FIX | KEEP | - |
| Q13 relative speed first, equation as check | solve-wp27-g121 slides 2-3 | FIX (order) | KEEP | 2024_autumn_q2_10 |
| ÷ for division, American spelling, "so", stems (Q2, Q4, Q10, Q12, p15, p19, units, TeX letters) | all T27 videos / questions | FIX | KEEP | - |
| p10 central angle → fraction of the track | wp27-p10 | FIX | KEEP | (original question) |
| Q2/Q8/Q9/Q11 extra explanation lines (reciprocal, ×36, 169−144) | solve-wp27-g108, -g111/-g112 area, -g116, -g117, -g119 | FIX | KEEP | - |
| Pythagoras one-line reminder | wp-106 slide "Draw a sketch" | FIX (original Q2 needs it) | KEEP | orig wp27-g108 |
| Sketch habit (dot, arrow, gap) | wp-106 slide "Draw a sketch"; card tip | METHOD | KEEP | 2024_autumn_q2_10, 2026_spring_q2_17 |
| Minutes as fractions of an hour table | wp-106 slide 4 "Units"; card table "Minutes as parts of an hour" | METHOD | KEEP | 2025_spring_q1_16 (20 min = ⅓ h), 2024_winter_q1_14 (½ min), 2025_winter_q1_16 (72 s) |
| Distance-speed-time table | wp-106 new slide "The table"; card tip | METHOD | KEEP | 2025_spring_q1_16, 2020_autumn_q2_18, 2019_spring_q2_19 |
| "What is fixed?" (4 quick situations) | wp-110 new slide "What is fixed?" + recap; card table title | METHOD | KEEP | 2023_spring_q2_05, 2025_autumn_q2_20 |
| Relative speed sketch on the board | wp-113 slide 5 | FIX | KEEP | - |
| Estimate first (which side of the middle) | wp-108-after recap; card tip; Q3/Q12 | METHOD | KEEP | 2019_spring_q2_19 (50 is the middle of 60 and 40 → equal times) |
| 2ab/(a+b) check for equal distances | wp-108-after recap line; solve-wp27-g109 end line + written solution; mem-motion row "Equal distances" | METHOD | KEEP (rule 2) | 0 real equal-distance questions; orig wp27-g109 (72/48), wp27-p21 are equal-distance average-speed questions |
| Work back from the answers | Q11 video, card tip, p16/p17 solutions | METHOD | KEEP | 2021_autumn_q2_01 (try 8: t = 4, 32 km), 2020_autumn_q2_18 |
| Circular track opposite directions (add speeds) | mem-motion row "Circular track, opposite directions" | CONTENT | KEEP (rule 2) | 0 real (real 2024_autumn_q2_10 is same direction); orig wp27-p10, wp27-p19 need it |
| NEW VIDEO r26-t27-special "Special Motion Cases": slide "Train length" (post = length; tunnel/bridge = tunnel + train) | r26-t27-special slide 2 | CONTENT | KEEP | 2024_winter_q1_14 (1); orig wp27-p25 (tunnel) |
| - slide "Two trains" (sum of lengths at relative speed) | r26-t27-special slide 3 | CONTENT | REMOVE | 0 real; no original needs it (orig wp27-p22 is two trains meeting as points) |
| - slide "Current" (down = boat + current, current = half the difference) | r26-t27-special slide 4 | CONTENT | KEEP (rule 2) | 0 real; orig wp27-p24 (downstream) |
| - slide "Circular track" (same subtract, opposite add) | r26-t27-special slide 5 | CONTENT | KEEP | 2024_autumn_q2_10 (same direction); orig wp27-p10, p14, p19, g121 |
| - slide "Meeting twice" (3 road lengths) | r26-t27-special slide 6 | CONTENT | REMOVE | 0 real, no original |
| - Recap slide | r26-t27-special slide 7 | - | KEEP minus the "two trains" and "meeting twice" lines | - |
| Guided Q14 train 300 m, post 15 s, bridge 500 m | q-r26-t27-01 + solve-q-r26-t27-01 | train length | KEEP | 2024_winter_q1_14; orig wp27-p25 |
| Guided Q15 current from down/up trips | q-r26-t27-02 + solve-q-r26-t27-02 | current | KEEP (rule 2) | 0 real; orig type wp27-p24 |
| Guided Q16 circle 1.2 km, opposite directions | q-r26-t27-03 + solve-q-r26-t27-03 | circular opposite | KEEP (rule 2) | 0 real; orig wp27-p10, p19 |
| Guided Q17 meet 4 km from A, then 2 km from B | q-r26-t27-04 + solve-q-r26-t27-04 | meeting twice | REMOVE | 0 real, no original |
| NEW VIDEO r26-t27-graphs "Percents, Letters and Graphs": slide "Speed % → time %" | r26-t27-graphs slide 2 | METHOD | KEEP | 2023_winter_q1_16 (rate up → time by flipped fraction), 2020_autumn_q2_18 (20× speed), 2023_spring_q2_05; orig wp27-g120 (80% faster), wp27-p06 (1.6×) |
| - slide "Answers in letters" (plug in numbers) | r26-t27-graphs slide 3 | METHOD | KEEP | 2022_autumn_q2_09, 2025_autumn_q2_20; orig wp27-p02, p03, p17 |
| - slide "Distance–time graphs" (with figure) | r26-t27-graphs slide 4 | CONTENT | UNSURE | No clear real question and no original needs it. Only candidate: data-interpretation set 2019_spring_q1_16..20 (Amnon and Boaz on a running course, "distance between them"); its figure is not in the text, so it cannot be confirmed as a distance-time graph. If the teacher confirms that figure is a distance-time graph, KEEP; otherwise REMOVE. |
| - slide "Two travelers" (with figure) | r26-t27-graphs slide 5 | CONTENT | UNSURE | same as above |
| - Recap slide | r26-t27-graphs slide 6 | - | KEEP (drop graph lines if graphs are removed) | - |
| Guided Q18 25% faster saves 12 min | q-r26-t27-05 + solve-q-r26-t27-05 | speed % | KEEP | 2023_winter_q1_16; orig wp27-g120 |
| Guided Q19 d km in t h → minutes for k km | q-r26-t27-06 + solve-q-r26-t27-06 | letters | KEEP | 2022_autumn_q2_09 (almost the same question) |
| Guided Q20 graph: fastest part | q-r26-t27-07 + solve-q-r26-t27-07 | graph | UNSURE | see graph slide |
| Card mem-r26-t27-special rows: post, tunnel/bridge | mem-r26-t27-special table "Special cases" | CONTENT | KEEP | 2024_winter_q1_14; orig p25 |
| - row "Two trains pass each other" | same table | CONTENT | REMOVE | 0 |
| - rows "Boat downstream / upstream", "Both trips given" | same table | CONTENT | KEEP (rule 2) | orig p24 |
| - rows "Circle, same direction", "Circle, opposite directions" | same table | CONTENT | KEEP | 2024_autumn_q2_10; orig p10, p19 |
| - row "Two walkers meet, go on to the ends, meet again" | same table | CONTENT | REMOVE | 0 |
| - table "Speed % → time %" + tip | same card | METHOD | KEEP | as speed % |
| - table "Distance–time graphs" | same card | CONTENT | UNSURE | as graphs |
| - tips (letters, two choices) | same card | METHOD | KEEP | 2022_autumn_q2_09 |
| Practice 08 two trains passing | q-r26-t27-08 | two trains | REMOVE | 0 |
| Practice 09 train length from two passes | q-r26-t27-09 | train length | KEEP | 2024_winter_q1_14; orig p25 |
| Practice 10 plane and wind | q-r26-t27-10 | current/wind | KEEP (rule 2) | 0 real; orig type p24 |
| Practice 11 current as multiple of boat | q-r26-t27-11 | current | KEEP (rule 2) | 0 real; orig type p24 |
| Practice 12 circle, both directions → speed ratio | q-r26-t27-12 | circular | KEEP (rule 2) | 2024_autumn_q2_10 (same-dir part); orig p10, p19 |
| Practice 13 meeting twice, distance | q-r26-t27-13 | meeting twice | REMOVE | 0 |
| Practice 14 meeting twice, time | q-r26-t27-14 | meeting twice | REMOVE | 0 |
| Practice 15 50% faster | q-r26-t27-15 | speed % | KEEP | 2023_winter_q1_16; orig g120 |
| Practice 16 speed −20% → time % | q-r26-t27-16 | speed % | KEEP | 2023_winter_q1_16; orig g120 |
| Practice 17 x m in y s → km in z min (letters) | q-r26-t27-17 | letters | KEEP | 2022_autumn_q2_09 |
| Practice 18 chase with letters | q-r26-t27-18 | letters + chase | KEEP | 2020_autumn_q2_18, 2026_spring_q2_17 |
| Practice 19 graph, two cyclists | q-r26-t27-19 | graph | UNSURE | as graphs |
| Practice 20 graph, trip with a stop | q-r26-t27-20 | graph | UNSURE | as graphs |
| Practice 21 equal times average | q-r26-t27-21 | average speed | KEEP | 2019_spring_q2_19 |
| Practice 22 first third at 30, rest at 60 | q-r26-t27-22 | average speed | KEEP | 2019_spring_q2_19; orig p21, g109 |

## TO REMOVE
- Video r26-t27-special: slide "Two trains" (slide 3) and slide "Meeting twice" (slide 6); in its Recap slide the two-trains and meeting-twice lines; its sidebar entries "Two trains", "Meeting twice".
- Guided question q-r26-t27-04 and its solution video solve-q-r26-t27-04 (meeting twice); drop "Question 17" from SPECIAL_SB sidebars (renumbering follows).
- Practice questions q-r26-t27-08, q-r26-t27-13, q-r26-t27-14.
- Card mem-r26-t27-special, table "Special cases": rows "Two trains pass each other" and "Two walkers meet, go on to the ends, meet again"; intro words "meeting twice".

UNSURE (teacher decides; if not confirmed → remove):
- Video r26-t27-graphs slides "Distance–time graphs" (4) and "Two travelers" (5) with their 2 figures, graph lines in its Recap; guided q-r26-t27-07 + solve-q-r26-t27-07; practice q-r26-t27-19, q-r26-t27-20; card mem-r26-t27-special table "Distance–time graphs". (If removed, the video title "Percents, Letters and Graphs" needs renaming.)

## ORIGINAL ITEMS REMOVED BY FIXERS (restore - originals stay)
Questions removed (unplaced):
- wp27-p14 (circular track same direction, ≈ Q13)
- wp27-p21 (round-trip average speed, ≈ Q3)
- wp27-p22 (two trains 420 km apart meet)
- wp27-p23 (3 m/s for 25 minutes, ≈ Q1)

Questions whose content was replaced:
- wp27-p10 - original asked the CENTRAL ANGLE of the slower runner's arc (choices 45°, 72°, 90°, 60°); replaced by "what fraction of the track" (⅛, ⅕, ¼, ⅙).
- Reworded only (same math): wp27-g107, g108 ("displacement" → "horizontal distance"), g109, g111, g118, g120, p01, p02, p03, p04, p07, p09, p11, p15, p16, p17, p19, p24, p25, p26, p27.

Slides whose original script was overwritten:
- wp-106 "Distance, Speed and Time": slide 4 "Units", slide "Draw a sketch", slide "Recap".
- wp-108-after "Average Speed": slide 1 "Average Speed" (removed "Honestly? Rare on the exam."), slide 4 "Not the average", slide 5 "Recap".
- wp-110 "Speed Ratios": Recap slide.
- wp-113 "Relative Speed": slide 5.
- solve-wp27-g120 slide 4 "Method 3 · Estimate".
- solve-wp27-g121 slide 2 "Method 1 · Understand, then an equation" → "Method 1 · Relative speed"; slide 3 "Method 2 · Relative speed" → "Method 2 · Check with an equation" (order swapped, content rewritten).
Memory card mem-motion: all tables and tips rewritten (original rows kept in substance; the "Average speed = total distance : total time" tip became a table row; "Always draw a sketch" tip expanded; circular-track row reworded).
