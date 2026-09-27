# Audit: Topic 35 (Three-dimensional geometry). Were the additions justified by the real exam?

Sources: `math_patches/t35_CHANGES.md`, `math_patches/t35.py`, `real_exam/quant_real.md` (regenerated full-text version), and the pre-patch course `course18.json`.
Real-exam groups read in full: 3d_geometry (32). I also searched all 760 questions for: water, pour, liter/litre, tank, aquarium, ml, rotate/turn, painted, sphere, unfold/shortest/ant, brick/pack, plane/cross-section.

Rules applied (brief + coordinator):
- An added topic, rule or question type stays only if the real exam has it.
- An added method that ORIGINAL course questions need stays (rule 2).
- An added question whose type exists only in the original course, and not on the real exam, is removed.

Main findings from the real exam (32 solid-geometry questions):
- **Water, pouring, liquid rising, liters/ml/m³ units: 0 real questions.** No water or liquid question appears in the 3d group, and none of the "water" hits elsewhere are about solids.
- **Same volume, new shape → new height: 2 real questions.** 2024_spring_q2_19 (equal-volume cylinders, h/H = R²/r²) and 2021_autumn_q1_18 (dough cylinder remade with the same length, find the new radius). This is the computation that the "Height = volume ÷ base" and "Pouring" slides teach.
- **Cone slant height: 2 real questions.** 2019_winter_q1_06 (slant 9, r = 3 → h = 6√2, V = 18√2π) and 2023_winter_q2_11 (slant = 2π, r = 1 → AO = √(4π² − 1)).
- **Solids of revolution (turning a rectangle or triangle): 0 real questions.** The original course needs it for geo35-core-p01.
- **Cube and box diagonals: 3 real questions.** 2022_autumn_q1_20 (vertex to center, a√3/2), 2020_autumn_q1_07 (triangle in a 3×4×6 box), 2024_autumn_q2_15 (longest segment in a cylinder).
- **Angles in a cube: 2 real questions.** 2025_autumn_q2_14 (∡ABG = 90°) and 2022_winter_q2_20 (∡EDG = 60°).
- **Counting faces, edges and vertices: 2 real questions.** 2020_spring_q1_19 (prism vertices : edges = 2 : 3) and 2020_winter_q1_13 (edge sum of a box).
- **Painted cube, three face areas → volume, shortest path on the surface, bricks in a box: 0 real questions each.** The original course has painted-cube (p24) and face-area (p12, p23) questions, but no surface-path or brick questions. The original geo35-g131 packs cubes, not bricks.
- **Prism lying on its side: 2 real questions.** 2021_autumn_q2_10 (dark prism inside a cube) and 2024_spring_q1_20 (triangular prism, base = the triangle).

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| Cube-angle rule corrected ("edge + diagonal of the face it stands on, same corner → 90°"; 60° = two face diagonals from one corner) | solve-geo35-g129 slide 5 board + speech; solve-geo35-g130 slide 2; mem-cube-facts "Angles in a cube" | FIX | KEEP | correction (the rule itself: 2025_autumn_q2_14, 2022_winter_q2_20) |
| Water Level lesson: "Height = volume ÷ base" and "Pouring" (volume stays, ÷ new base) | r26-t35-water slides "Height = volume ÷ base", "Pouring"; recap lines "Height", "Pouring" | METHOD | KEEP | 2024_spring_q2_19, 2021_autumn_q1_18 (same volume, new base → new height) |
| Water Level lesson: "Dropping in a solid" (rise = object volume ÷ base) | r26-t35-water slide "Dropping in a solid" (+ figure); recap board "Rise" and its spoken sentence | CONTENT | REMOVE | 0 real questions; not needed by any original question |
| Water Level lesson: "Liters and cm³" (1 ml = 1 cm³, 1 L = 1000 cm³, 1 m³ = 10⁶ cm³) | r26-t35-water slide "Liters and cm³"; recap board "Units" and "check the units first" | CONTENT | REMOVE | 0 real unit-conversion questions in solids |
| Water Level lesson title line "A classic on the exam" | r26-t35-water title slide | FIX needed | — | this claim is false (0 water questions). Reword it when the lesson is trimmed |
| Guided: box 10×8, water 9 cm high, poured into a 12-cm cube → 5 | q-r26-t35-01 + video solve-q-r26-t35-01 | same volume, new base | KEEP | 2024_spring_q2_19, 2021_autumn_q1_18 |
| Cones lesson: slant height r² + h² = ℓ² | r26-t35-cones slide "Slant height"; recap board "Slant"; mem-solids "Cones" row "Slant height" | METHOD | KEEP | 2019_winter_q1_06, 2023_winter_q2_11 |
| Cones lesson: turning a rectangle → cylinder, a right triangle → cone | r26-t35-cones slides "Turn a rectangle", "Turn a right triangle"; recap boards "Rectangle", "Triangle", "Axis"; mem-solids "Cones" rows 2–3 | METHOD needed by original items | KEEP (rule 2) | 0 real questions; needed for original geo35-core-p01 |
| Guided: cone r = 6, slant 10 → 96π | q-r26-t35-02 + video solve-q-r26-t35-02 | slant height | KEEP | 2019_winter_q1_06, 2023_winter_q2_11 |
| Cube and Box Facts: diagonals a√2, a√3, √(a² + b² + c²) | r26-t35-cubefacts slide "Diagonals"; mem-cube-facts "Box body diagonal" row | METHOD | KEEP | 2022_autumn_q1_20, 2020_autumn_q1_07, 2024_autumn_q2_15 |
| Cube and Box Facts: three cube angles | r26-t35-cubefacts slide "Angles in a cube" | METHOD | KEEP | 2025_autumn_q2_14, 2022_winter_q2_20 |
| Cube and Box Facts: faces/edges/vertices of prisms and pyramids | r26-t35-cubefacts slide "Faces, edges, vertices"; mem-cube-facts table "Counting" | CONTENT | KEEP | 2020_spring_q1_19, 2020_winter_q1_13 (original p07 too) |
| Cube and Box Facts: painted cube (8, 12(n − 2), 6(n − 2)², (n − 2)³) | r26-t35-cubefacts slide "Painted cube" (+ figure); mem-cube-facts table "Painted cube" | METHOD needed by original items | KEEP (rule 2) | 0 real questions; needed for original geo35-core-p24 |
| Cube and Box Facts: three face areas → V = √(product) | r26-t35-cubefacts slide "Three faces → volume"; mem-cube-facts tip "Three face areas …" | METHOD needed by original items | KEEP (rule 2) | 0 real questions; needed for original geo35-core-p23 and p12 |
| Cube and Box Facts: shortest path on the surface (unfold, a√5) | r26-t35-cubefacts slide "Walk on the surface" (+ figure); mem-cube-facts tip "Shortest path on the surface …" | CONTENT | REMOVE | 0 real questions; no original question uses it |
| Quick checks: height < slant edge, part < whole | r26-t35-cubefacts slide "Quick checks", board "Size checks" + its sentence | METHOD | KEEP | 2023_winter_q2_11 (AO < AB), 2019_winter_q1_06; also original g128's check |
| Quick checks: bricks, "try each position" | r26-t35-cubefacts slide "Quick checks", board "Solids in a box: count each direction — try each position" + sentence "Solids in a box aren't water … the count can change."; mem-cube-facts tip "Bricks in a box …" | METHOD for a type not on the exam | REMOVE | 0 real packing questions. The original g131 (cubes) needs only "count each direction", which its own solution already teaches |
| Quick checks: "Same units first: 1 liter = 1000 cm³" | r26-t35-cubefacts slide "Quick checks", board "Units" + "And compare only in the same units." | CONTENT | REMOVE | 0 real questions |
| Guided: painted 5×5×5, exactly one face → 54 | q-r26-t35-03 + video solve-q-r26-t35-03 | painted cube (original-only type) | REMOVE | 0 real questions (original p24 stays) |
| "Lying down" slide (bases = the two identical faces, height = distance between them) | geo-119 new slide 4 "Lying down"; mem-solids tip "Bases = the two identical faces …"; Q4 spoken lines | METHOD | KEEP | 2021_autumn_q2_10, 2024_spring_q1_20 |
| "1 ml = 1 cm³" spoken line | geo-119 slide 11 (Volume), the added line "And one milliliter is exactly one cubic centimeter…" | CONTENT | REMOVE | 0 real questions |
| "On the formula page" slide + recap line + card tip | geo-119 new slide 15 "On the formula page"; recap line "Box, cylinder, cone, pyramid: on the formula page"; mem-solids tip "On the formula page: …" | METHOD (exam orientation) | KEEP | the printed formulas solve 2019_winter_q1_06, 2021_spring_q2_12, 2025_winter_q1_19, 2022_autumn_q2_11 |
| "Solids in Questions" what's-ahead list | geo-120 slide 2 (rewritten) | FIX | KEEP, but edit | Remove "units" from "Water level · units · the cone's slant height", and "liters and cubic centimeters" from the spoken line |
| Q8 silver-triangle reminder; Q10 slide 3 rationalizing; Q10 slide 4 one-step box diagonal 26, "5-12-13 / 3-4-5" on the board; Q4 "lies on its side" | solve-geo35-g128 slide 3; solve-geo35-g130 slides 3–4; solve-geo35-g124 | FIX/METHOD | KEEP | box diagonal: 2020_autumn_q1_07, 2022_autumn_q1_20 |
| Written solutions rewritten; ":" removed; p08 cases; p10 giveaway removed; spelling | Q1–Q12, many practice items | FIX | KEEP | wording |
| Figures (Q2, Q6, Q8, Q4, p25, p13, lesson slides 2–3, Q10 slide 4, Q12 slide 3) | figures + slide copies | FIX | KEEP | figures |
| Practice: liters in a 50×40×30 tank → 60 | q-r26-t35-04 | units | REMOVE | 0 real |
| Practice: cylinder r = 3, poured into r = 6 → 2 cm | q-r26-t35-05 | same volume, new base | KEEP | 2024_spring_q2_19, 2021_autumn_q1_18 |
| Practice: cube dropped in a tank, rise 0.72 | q-r26-t35-06 | displacement | REMOVE | 0 real |
| Practice: stone volume from the rise (50π) | q-r26-t35-07 | displacement | REMOVE | 0 real |
| Practice: cone cup poured into a cylinder with the same base → 10/3 | q-r26-t35-08 | same volume, new shape (cone = ⅓ cylinder) | KEEP | 2024_spring_q2_19; 2025_winter_q1_19 (cone vs cylinder volume ratio) |
| Practice: cone r = 5, slant 13 → 100π | q-r26-t35-09 | slant height | KEEP | 2019_winter_q1_06, 2023_winter_q2_11 |
| Practice: bricks 2×3×5 in a 7×10×9 box → 18 | q-r26-t35-10 | packing | REMOVE | 0 real |
| Practice: ant on a cube, 4√5 | q-r26-t35-11 | surface path | REMOVE | 0 real |
| Practice: order cube / cylinder / cone by volume | q-r26-t35-12 | volume comparison | KEEP | 2020_autumn_q2_08, 2023_autumn_q1_09, 2025_spring_q2_14 |
| Practice: aquarium, 2 liters per minute → 27 min | q-r26-t35-13 | water + units | REMOVE | 0 real |
| Practice: painted 6×6×6, no paint → 64 | q-r26-t35-14 | painted cube (original-only type) | REMOVE | 0 real (original p24 stays) |
| Practice: prism with 18 edges → 8 faces | q-r26-t35-15 | counting | KEEP | 2020_spring_q1_19 |
| Practice: triangle turned about each leg, ratio 5 : 2 | q-r26-t35-16 | solids of revolution (original-only type) | REMOVE | 0 real (original p01 stays) |
| Card mem-solids table "Water and units": rows "Water height", "Pouring into another container" | mem-solids | METHOD | KEEP | 2024_spring_q2_19, 2021_autumn_q1_18 |
| Card mem-solids table "Water and units": rows "Object sinks in water", "Units" | mem-solids | CONTENT | REMOVE | 0 real |

## TO REMOVE
- Videos: `solve-q-r26-t35-03` (the painted-cube solution video).
- Slides:
  - r26-t35-water:
    - slide "Dropping in a solid"
    - slide "Liters and cm³"
    - their sidebar entries
    - the recap boards "Rise" and "Units", with the words "An object pushes the water up by its own volume." and "And check the units first."
    - the title line "A classic on the exam …" (reword it)
  - r26-t35-cubefacts:
    - slide "Walk on the surface" and its sidebar entry
    - on slide "Quick checks", the board "Solids in a box: count each direction — try each position" and its sentence
    - on slide "Quick checks", the board "Same units first: 1 liter = 1000 cm³" and its sentence
  - geo-119 slide 11 (Volume): the added line "And one milliliter is exactly one cubic centimeter. That can holds 330 cubic centimeters."
  - geo-120 slide 2: drop "units" / "liters and cubic centimeters" from the what's-ahead text.
- Questions: q-r26-t35-03, q-r26-t35-04, q-r26-t35-06, q-r26-t35-07, q-r26-t35-10, q-r26-t35-11, q-r26-t35-13, q-r26-t35-14, q-r26-t35-16. Update the practice order and the guided numbering.
- Card rows:
  - mem-solids, table "Water and units": the rows "Object sinks in water" and "Units".
  - mem-cube-facts: the tips "Shortest path on the surface: …" and "Bricks in a box: try every position — the count can change."

## ORIGINAL ITEMS REMOVED BY FIXERS (restore candidates)
- Questions:
  - geo35-core-p09 (angle AEG = 90°) was unplaced.
  - geo35-core-p27 (each dimension −25% → 27/64) was moved to the Topic 36 practice (`M.move`). It was not deleted; move it back if wanted.
- Slides and lines replaced:
  - geo-119 slide 2: the 3×3 "Rubik" cube figure was replaced by a plain box.
  - geo-119 slide 3: the lying prism figure was replaced by an upright prism. The lying one moved to the new slide.
  - geo-120 slide 2: the whole script was rewritten.
  - solve-geo35-g130 slide 4: the whole script was rewritten, with a new box figure instead of the edge-2 cube.
  - solve-geo35-g129 slide 5: the board lines "Edge and a diagonal of another face → 90°" and "Two diagonals of different faces → 60°" were replaced. The first one was wrong.
  - solve-geo35-g130 slide 2: the line "an edge and a diagonal of another face" was replaced.
- Solutions and stems:
  - geo35-g121: the solution bound "65.1 < 21π < 66" was replaced.
  - geo35-core-p10: the stem sentence "three faces exposed, three touching" was removed.
  - All the other written solutions were reworded.
- Figures changed:
  - geo35-g122: the cone on the cylinder is now drawn side by side.
  - geo35-g126: the label "a" was removed.
  - geo35-g128: the "5" was moved.
  - geo35-g124: the "13" was moved.
  - geo35-core-p25: the body diagonal is no longer drawn.
  - geo35-core-p13: the 6×6 layer was replaced.
