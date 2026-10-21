# External course review, group C (geometry): 21 Oct 2026

Scope: 13 files in group-C.txt. All read in full. 4 of them have no speech, only music: the three "האם אתה שולט / שפיץ" quizzes and "שמונה טיפים בגיאומטריה" [EB-7Dl6Wl84]. Their transcripts contain only "[Music] thank you / foreign", so nothing can be reviewed (they are probably on-screen quizzes). That leaves 9 videos with speech.

I checked every claim against our course/t30, t31, t32, t33, t34, t36, t38 and t51 (grep with several phrasings), and judged how much each one matters using studio-build/real_exam/quant_real.md.

Overall: our geometry topics already cover almost all of their content, and often in more depth. Examples: small and big angles between parallel lines (no school names), polygon angle sums, exterior angles, the diagonal count, central angles, the hexagon's two diagonals, the octagon cut, similarity types, k² and k³, and the line of centres of touching circles. The real findings are a few circle facts we never state, one polygon shortcut that is clearer than ours, and two small tips.

---

## 1. 5 Circle Theorems You Tend to Forget [_K4WDFEAVrw]
Teaches five circle facts in two minutes:
- A radius perpendicular to a chord bisects it, and the other way round.
- The line from the tangents' outside point to the centre bisects the angle between the two tangents.
- A trapezoid inscribed in a circle is isosceles.
- In a quadrilateral that has a circle inside it, the sums of opposite sides are equal.
- The line joining the centres of two touching circles passes through the touching point.

- `GAP` **A trapezoid inscribed in a circle is always isosceles (and only an isosceles trapezoid can be inscribed).** We have no such sentence anywhere in t32 or t33. The only "trapezoid" lines in t33 are a right trapezoid and an unsolved stem. It belongs in t33 geo-075 "Angles in a Circle", right after the inscribed-quadrilateral rule (opposite angles add up to 180). Say why: a trapezoid's two angles on a leg add up to 180, and the inscribed rule says opposite angles add up to 180. So the two base angles are equal, and the trapezoid is isosceles. Real exam: **2024_autumn_q1_13** asks exactly this: "It is not possible that one of the diagonals of the ___ inscribed in the circle is a diameter" (answer: isosceles trapezoid). Our rectangle-diagonal fact (geo-075 line 447) is half of that question. Recommendation: **ADD** (2–3 sentences in geo-075, plus a solution video for a question in the style of 2024_autumn_q1_13).
- `GAP` **Circle inside a quadrilateral: the sums of opposite sides are equal (a + c = b + d).** Not found ("opposite sides … add", "sum of opposite sides", "circumscribed" all come up empty). We even have an unsolved stem (t33 stems: "ABCD is a trapezoid … circumscribed about a circle …") where this fact is the natural tool. It follows directly from our own geo-077 rule that two tangent segments from one point are equal: each corner sends two equal tangent pieces, and each pair of opposite sides uses one piece from every corner. Real exam: no tagged quadrilateral-around-a-circle question in the 19 sections (2016–2026 has hexagon-around-a-circle, 7785). Recommendation: **ADD AS ONE-LINE TIP** at the end of geo-077, derived from the equal-tangents rule (W21 "say why"), not as a new rule to memorise.
- Radius ⟂ chord bisects it: covered (t33 geo-07x line 457, used in 587 and 655). Bisecting the angle between tangents: covered (geo-077 line 505, through the kite's line of symmetry, which is a better reason than theirs). Line of centres through the touching point: covered (g088 line 286, line 351, q-r26-t33-05).
- `CHECK` They say that if a radius bisects a chord it is also perpendicular to it. That is false when the chord is itself a diameter: two diameters bisect each other at any angle. Harmless on the exam, but if we ever state the converse, say "a chord that is not a diameter".
- `CHECK` They call the inscribed-trapezoid fact "not an official theorem". It is a standard theorem (it follows from the inscribed-quadrilateral rule). Don't copy that remark.

## 2. Introduction to Geometry for the Psychometric Entrance Test 1 [pNnYMFOxiIA]
Basic vocabulary (side, edge, face, area, volume, perimeter, radius). Don't solve by eye, but use the figure as a last resort. Memorise the rules and the tricks. Previews the equilateral area a²√3/4 and the hexagon diagonal a√3.
- Nothing new. We cover: "don't trust how it looks" (t30 lines 116, 162, 205), "figures are not necessarily to scale, but most are accurate; with regular shapes rely on the figure" (t51 lines 493–495), the equilateral area (t31 geo-017-after), and both hexagon diagonals (t34 geo-109).
- `CHECK` They say "the diagonal of a regular hexagon is √3 times the side" without saying which diagonal. Only the short one is; the long one is 2a. We already teach both. Don't copy the loose wording.

## 3. Introduction to Geometry for the Psychometric Test 2 [9wq5Ybbetb4]
Angle types (right, acute, obtuse, straight, full 360, reflex 270/300). Adjacent angles on a line, vertical angles, parallel lines. Parallel lines cut by a line: "forget the school names, all small angles are equal, all big are equal, small + big = 180". Perpendicular lines, square diagonals, a line perpendicular to two parallels gives eight right angles.
- Nothing new. We already use the same "small and big angles, no school names" approach (t30 lines 20, 186, 209), plus Z/U. Trapezoid co-interior angles: t32 line 494, t34 line 170.

## 4. מבוא לגיאומטריה לפסיכומטרי 3 [hctVd2adG3k]
Eight line-and-angle questions: an auxiliary parallel line through the bend of a zigzag (α = 30 + 40), "which drawing has parallel lines" (check small + big = 180), angles around a point = 360, mental division (360/5 as 350 + 10), "a ∥ b ∥ c", and an acute/obtuse "which is certainly not true" solved by plugging in values with a second plug-in for the answers still standing, then by reasoning.
- Nothing new. We cover: the parallel line through each bend and the zig-zag rule (t30 g007 line 72, q-r26-t30-03 line 99), "parallel only if given or proved" (t30 line 205), plugging in numbers and keeping the choices still standing (t51), and the angles-around-a-point stems (t30).
- (Their mental division "360 ÷ 5 = 350 ÷ 5 + 10 ÷ 5" is the same splitting we use in t34 "ninety divided by three … eighteen divided by three".)

## 5. Polygons for the Psychometric Exam 1 [bvR-4rsIfsE]
(n−2)·180, one angle of a regular polygon, every regular polygon fits in a circle with the same centre, central angle 360/n, an inscribed angle in a regular polygon found as half a central angle over the same sides. Inscribed regular polygons with more sides have more area and perimeter but a shorter side. Diagonals n(n−3)/2.
- `BETTER` **The "count the sides" rule for angles inside a regular polygon.**
  - Theirs: every angle whose vertex is a corner of a regular n-gon (so it sits on the circle around it) equals (number of sides between its arms) × (half of the central angle). That is, each side "under" the angle is worth 180/n.
  - Ours (t34 geo-104-4 lines 363–365, summary line 312): "the diagonals from one vertex split its angle into equal parts", then each case is divided out (108 ÷ 3 = 36, 120 ÷ 4 = 30). We never say the general value 180/n, and never "multiply by the number of sides the angle spans". Our version only covers angles at one corner between diagonals from that corner.
  - Why theirs is better for a weak student: it is one counting step for any angle with its vertex on the polygon, and it uses only the inscribed-angle rule they already know. Real exam: **2026_spring_q2_19** (9-gon with diagonals, α = 20 = 180/9) and **2023_spring_q2_03** (pentagon with two diagonals, α = 108 = 3 × 36) are both one-liners with it. Polygons are 11 tagged questions, and these two are among them.
  - Change: in geo-104-4, after "the three angles are equal", add a few sentences. Each small angle stands on one side, so it is half the central angle, 180 over n. So any angle with its corner on the polygon is 180 over n times the number of sides between its arms. Then give 2 extra examples (R37: core method in the lesson): the hexagon angle over 3 sides = 90, and the 9-gon over 1 side = 20. Also add it to r26-t34-summary.
- `GAP` (small) **In a regular hexagon, the short diagonal is perpendicular to the side next to it** (the angle over 3 sides = 3 × 30 = 90; it is an angle on a diameter). We use the 30-60-90 inside the corner triangle (geo-109), but never state this right angle, which is the quick way to spot 30-60-90 triangles in hexagon figures (their video 6 solves AO this way). Real exam: hexagon appears 11 times (e.g. 2023_autumn_q2_02, 2025_spring_q1_18). Recommendation: **ADD AS ONE-LINE TIP**, as the first example of the counting rule above.
- More sides means more area and perimeter: covered for the perimeter (t34 g111 lines 190–193: the hexagon as the balance point, the polygon always shorter than the circle). Area not stated, but it is obvious and not on the exam: SKIP.
- Diagonal count: covered (q-r26-t34-02, with the "counted twice" trap). Ours is better: it derives n(n−3)/2 instead of giving it as a bare formula.

## 6. Polygons for the Psychometric Exam 2 [fkdZS5h21hM]
The pentagon (108, central angle 72, inscribed angle on one side 36). The octagon (135, 45, 22.5). The octagon cut: the middle square, rectangles, and four corner 45-45-90 triangles that make one square. The hexagon (120, central angle 60, inscribed angle 30): the long diagonal is 2a, the short one a√3, the area is 6 · a²√3/4 = 3a²√3/2.
- Nothing new. We cover all of it: the octagon cut (t34 g108, g114, g115, line 99), the hexagon diagonals (geo-109), six equilateral triangles and the area (g107, g112-area), and "find the central angle and complete it to 180" (t34 line 308). Our hexagon "star partition" (geo-112-after) goes further than theirs.

## 7. מצולעים לפסיכומטרי 3 [HrOVgKuMLz8]
Seven polygon questions: pentagon α + β with inscribed angles counted in sides, hexagon (α + β)/γ, the sum of all hexagon diagonals with side 5 (3 × 10 + 6 × 5√3), the sum of the outside reflex angles of a 9-gon, AO in a hexagon through 30-60-90, sectors of two circles centred at hexagon vertices (120° = one third of the circle), the hexagon area to the area of three squares on its sides, and the octagon area with side 1 = 2 + 2√2.
- `BETTER` Same counting rule as in video 5, used three times here ("on two sides, double it; on three sides, triple it"). Covered by the video 5 recommendation.
- `GAP` (minor) **The sum of the reflex angles "outside" the corners of an n-gon**: each one is 360 − interior, so the sum is 360n − 180(n−2) = 180(n+2) (for 9 sides, 1980). We teach only the usual exterior angles (sum 360; t34 lines 262–265, 309). No real exam question of this type in the 11 polygon questions. Recommendation: **SKIP**, or at most a practice stem, since a student who knows "interior + reflex = 360" and the angle sum can derive it.
- Sector angle at a hexagon vertex (120 = one third of the circle) and the octagon area: covered (t33 sector lessons, t34 g108).
- Their way of dividing an integer by a root ("4/√2: do 4 ÷ 2, then attach the root") is the same trick we teach in t31 lines 73 and 395–398. Nothing new.

## 8. Geometric Similarity for the Psychometric Exam 3 [V_hXNR3FXz4]
Eight similarity questions:
- Which pair is surely similar (two equal angles are enough).
- A cone scaled ×5 gives volume ×125.
- DE ∥ BC with areas 4:9, so the side ratio is 2:3.
- "Which can't happen": a median in a scalene triangle can't create two similar triangles.
- Two equilateral triangles with sides 2 and 6: grey to white = 1:8.
- Circle areas from ratios of their parts, then the circumference ratio = √(area ratio).
- A trapezoid = the big triangle minus the small one (don't use the trapezoid formula).
- **Two chords crossing in a circle: the triangles are similar (equal inscribed angles plus vertical angles), so a·d = b·e.**
- `GAP` / `PARTIAL` **Crossing chords give similar triangles, and from that, the products of the chord parts are equal.** We have a practice stem for it (t36 stems line 805: "Chords AC and BD meet at E. AE:DE = 2:3 …"), but no lesson sentence and no solution video. grep for "chords … meet/cross", "intersecting chords" and "times … equals … times" finds nothing taught. t36 geo-139 lists the three triangle-similarity pictures (parallel to the base, the altitude to the hypotenuse, the hourglass) but not this fourth one. Real exam: no tagged chord question (similarity has 4 tagged questions; 2022_winter_q1_01 and 2024_winter_q1_03 are the "spot the similar triangles" type). Recommendation: **ADD** as a fourth picture in geo-139: two angles on the same arc are equal, and the vertical angles are equal, so the two triangles are similar. Attach a solution video to the existing stem 805. The product rule a·d = b·e is a one-line consequence, so present it as such (W21), not as a separate theorem.
- `GAP` (minor) "A median in a scalene triangle never gives two similar triangles" (the exterior angle equals the sum of the two remote angles, so the angle at the median's foot has no partner). Niche "which can't happen" item, not seen on the real exam. **SKIP**.
- Everything else is covered: two angles are enough (t36 line 444), k³ (lines 98, 572, geo-141/143), the trapezoid as big minus small (g140, g148 line 56), all equilateral triangles are similar (line 347), the area ratio of circles from their regions (g138, g147).
- Their remark that similarity often comes as the last or second-to-last question in the section fits our placement of it as a "hard" topic. No action.

## 9. חיזוק בדמיון משולשים לפסיכומטרי [rzwEPTAqyHE]
Harder similarity practice:
- A square inscribed in a right triangle (via similar corner triangles and Pythagoras).
- A quadrilateral built from two similar right triangles, where 24² − 16² is done as (24 + 16)(24 − 16).
- Two circles with a common tangent that crosses between them: the radii are ⟂ to the tangent, so there is an hourglass, x/3 = (16 − x)/5, x = 6, and AB = 8√3.
- Three equal squares where congruent hourglass triangles let you move a piece, so the grey area is one square.
- A square inside a rectangle, with an auxiliary line making similar triangles.
- Advice: always mark the equal angles to know which sides to divide.
- `PARTIAL` **A difference of squares inside Pythagoras** (24² − 16² = 40 · 8). We teach it, but only later: t32 lines 233–237, t33 line 327. It is missing from t31 where Pythagoras itself is taught, and t31 g022 (line 332: "a hundred minus forty-nine") and g025 (line 367: "thirty-nine squared minus fifteen squared") are the natural places. Real exam: Pythagoras with two-digit numbers is common across triangles, quadrilaterals and circles. Recommendation: **ADD AS ONE-LINE TIP** in t31 g025, where 39² − 15² comes up: "(39 − 15)(39 + 15) = 24 · 54", with the reason as in t32. Check planData order first: if t32 comes before t31 for the student, just refer back to it.
- `GAP` (minor) **The common tangent that crosses between two circles** (hourglass from two radii perpendicular to it). We have only the outside common tangent (q-r26-t33-05) and the touching cases. No real exam occurrence, and the author himself says these are above exam level. **SKIP** (optional practice question in t36 hourglass if a hard hourglass item is wanted).
- "Mark the equal angles, then match the sides across from them": covered (t36 line 466).
- Square inscribed in a right triangle: covered (t36 g145). Moving a congruent piece to find an area: we do it with the parallelogram (t32 line 369) and the octagon (g115), so the idea is there.
- `CHECK` In question 2 they finish with "52√80", left unsimplified (√80 = 4√5). If we ever write a similar question, simplify the root, as real NITE answers are given in simplest form.

## 10–13. האם אתה שולט בגיאומטריה [katqq4X2lU4], האם אתה שולט במשולשים [W0laWJFTiDE], האם אתה שפיץ בגיאומטריה [kp-qUaWt-3c], שמונה טיפים בגיאומטריה [EB-7Dl6Wl84]
No speech in the transcript (music only). Nothing to review. If the teacher wants these, they would need to be watched (the content is on screen).

---

## Top recommendations (most valuable first)

1. **Add the "count the sides" rule for angles in regular polygons** (t34 geo-104-4 and the summary). Any angle with its vertex on the polygon equals 180/n times the number of sides between its arms. This is a BETTER, one-step version of our "diagonals split the angle equally", with 2 extra examples. It solves real exam questions 2026_spring_q2_19 and 2023_spring_q2_03 in one line.
2. **Add "a trapezoid in a circle is isosceles"** (t33 geo-075, after the opposite-angles rule), with the reason from co-interior angles plus opposite angles. Add a solution video in the style of **2024_autumn_q1_13** (which shape inscribed in a circle can't have a diagonal that is a diameter).
3. **Add crossing chords as a fourth similar-triangles picture** (t36 geo-139). Equal inscribed angles plus vertical angles make the triangles similar, so the chord parts multiply equally. Attach a solution to the existing unsolved stem (t36 stem 805).
4. **One-line tip: in a regular hexagon the short diagonal is perpendicular to the neighbouring side** (90 = 3 × 30), so 30-60-90 triangles appear at once. Put it in t34 geo-109, as the first example of rec. 1. Hexagon is in 11 real questions.
5. **One-line tip: a circle inside a quadrilateral means the sums of opposite sides are equal**, derived from the equal tangent segments (t33 geo-077). It unlocks the unsolved trapezoid-around-a-circle stem in t33.
6. **One-line tip: a difference of squares in Pythagoras** in t31 g025 (39² − 15² = 24 · 54), or a back-reference if t32 is learned first.
7. If we ever state the converse "a radius that bisects a chord is perpendicular to it", add "for a chord that is not a diameter" (CHECK from video 1).
8. Optional practice (not lesson material): the common tangent crossing between two circles (hourglass), and the sum of the reflex angles outside a polygon, 180(n+2). Neither is on the real exam, so put them in practice only if there's room.
9. SKIP: a median in a scalene triangle can't make similar triangles; "more sides means more area" for inscribed polygons; their basic-vocabulary lessons. All are either already covered or not worth exam time.
10. Note for the teacher: 4 of the 13 videos in this group (the 3 geometry/triangles quizzes and "8 geometry tips") have no transcribed speech. If they matter, they need watching, not reading.

Counts: 13 files, 9 reviewed with speech (4 music-only). Findings: GAP 8 (including 2 PARTIAL; 4 to add or tip, 4 skip or optional), BETTER 2 (the same counting rule, seen in 2 videos), CHECK 4.
