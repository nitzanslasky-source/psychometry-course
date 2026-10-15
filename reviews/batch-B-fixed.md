# Batch B: fixes applied (Claude, 16 Oct 2026, 00:55)

Source review: `reviews/batch-B.md` (Codex, 85 findings: 31 must, 54 should). Topics 30–31, Reading Studio #161–210.

## Result

- **84 fixed**, including all 31 must findings. Seven of them were display findings that the earlier prompter job had already fixed ("two halves", triple grouping, the #170/#187 chains, "1x"). I checked each one in the rebuilt prompter and marked it "verified".
- **0 skipped.** All 50 lessons were still unrecorded when I started, before each edit, and before publishing (checked against `_reading` takes and `video_status.py --list`).
- **1 parked:** #195 geo-026, splitting the lesson into parts. See the reason at #195.

Canonical sources edited:
- `math_patches/_ai_vis_t30.py` and `_ai_vis_t31.py`. I started from the current specs, which already had the W17/W18 changes, and found each finding by meaning.
- `math_patches/_codex_reading_display_20261012.json`: scope replacements for the new or moved paragraphs (geo-023 5.3/5.4, g025 1.3/1.4/3.1–3.3, t31-01 2.4, geo-009-3 5.5). Stale entries were removed where the text changed: g006 2.1, geo-019 4.2, g034 2.1, g039 3.3.
- `real_exam/TEACHING_STYLE_GUIDE.md`: the new rule **W19 "pace + explain, no headlines"** (teacher, via the coordinator).
- New tool `studio-build/w19_check.py`: flags fragments, label openers and dense sentences (the W19 aid).

Not edited: `_method_visuals.py`, `_camera_parts.py`, `_math_vars_display.py`, `reading_studio.py`, the renderer.

New spec helpers:
- `ANCH()` (t30) and the existing `f2_pin()` (t31) tie a figure's layers to their own base, so a text line can be written between two layers without moving them.
- `NOFIG30`/`NOFIG31` make a slide show our enlarged copy instead of the question figure.
- `odot` (open endpoint), `wipe` (hide an old label) and `white`/`grey` (fade a cancelled edge) are new figure elements.

Everything kept: every method, her voice and wording style, the fonts and design, the method vocabulary, W1–W18, V3/V4, R29–R36, and the dark-blue pen for geometry.

Slide counts changed in four lessons only:
- t30-01: 1 → 2.
- t31-01: 1 → 2.
- g015: 1 → 2.
- g025: 2 → 3, with a new slide "A square inside a root".

In t30-01, t31-01 and g015, a question slide (the original figure, focused) now comes first, and the next slide shows our enlarged copy instead of the question figure. g037's Method 2 slide also shows our figures instead of the question figure.

Some lessons gained paragraphs, all unrecorded: g006, g005, geo-009-3, geo-019, g021, g025, g034, geo-023.

## Per lesson

### #161 geo-001 (camera, part 1)
- [must] ¶8–9 what an angle is: **fixed**. The board now shows "an angle is the opening between two lines that start at the same point" and names the vertex (a tinted opening plus a "vertex" label). Then "We measure how wide an angle opens in degrees. One whole turn around a point is 360 degrees." The existing four angles are the example.
- [should] ¶7 seven points: **fixed**. A new figure with 7 points and "gap 1…6" appears at the words.
- [should] ¶10 three lines: **fixed**. A small three-line figure shows 60, 50, 70, 60, 50, 70 with the sum 360, said and written before "360 again".

### #162 geo-001-2
- [must] ¶4 "90 only if marked or given": **fixed**. It now says "don't trust how an angle looks… marked like this, given, or we calculate it and get ninety". The caption and the recap now say "marked, given or calculated".
- [must] ¶6 obtuse: **fixed**. It now says "bigger than ninety degrees and smaller than a hundred eighty".
- [should] ¶8 adjacent: **fixed**. It now says "They share a vertex and one side. Here their other two sides make one straight line, so this pair… adds up to a hundred eighty." The later warning is kept.

### #163 geo-001-3
- [must] ¶8 distance: **fixed**. It now says "The distance between these two parallel lines…".
- [should] ¶16 55/125: **fixed**. The board is labelled "Other lines (not drawn)", and the speech says "with other parallel lines, not the ones in the drawing".

### #164 geo-001-4
- [must] ¶7 the U: **fixed**. It now says "Their sum is always a hundred eighty. Usually one is small and one is large… Only when the transversal is perpendicular are they both ninety."
- [must] ¶12/14: **fixed**. The trap line, the caption and the recap all say "marked, given or calculated".

### #165 solve-geo30-g002
- [must] the overlay registration: **fixed**. The marks are no longer laid over the question figure. The question figure sits on the left (x and 64° are focused there first), and one clean copy with the same labels and orientation is in its own panel. The equations are inside that panel, so nothing depends on where the question figure is drawn.

### #166 solve-q-r26-t30-01
- [should] c and its right angles: **fixed**. Slide 1 is the question, with x, 50° and c focused on the original figure. Slide 2 (no question figure) has one enlarged copy:
  - c is traced and its two right-angle squares are marked, then "a ⊥ c, b ⊥ c → a ∥ b";
  - c is faded for the focus;
  - 50 is moved down, then x, then the equations at their clauses.

### #167 solve-q-r26-t30-02
- [must] the bars: **fixed**. An enlarged copy of the line is in its own panel, and every bar ends exactly at its points, with dashed extension lines. In Method 2, the same BC is tinted once on the AC bar and once on the BD bar, with "BC is covered twice".

### #168 geo-004: READY (no finding)

### #169 solve-geo30-g005
- [should] ¶8–9 Method 2: **fixed**. It now says "We keep the two angles we already found…". The labelled figure is carried in, with "So far: x + 77° + 56° = 180°".
- [should] ¶7 crowding: **fixed**. The figure is smaller and the three lines moved up, so they are clear of the disclaimer.

### #170 solve-geo30-g006
- [must] ¶6 the first algebra: **fixed**. Five short paragraphs, one equivalent line each:
  - drop the brackets;
  - the balance tool: 5 + 2 = 7, so 5 = 7 − 2;
  - subtract 180 from both sides;
  - add m, n and k to both sides, giving 360 + x = m + n + k;
  - subtract 360.
  All three methods are kept.
- [should] ¶9 "m looks obtuse": **fixed**. 140 is now *chosen* as an allowed easy value, then checked: "x is 60, more than zero, so our numbers really fit a possible figure."
- [should] ¶5 the long equation: **fixed**. It is wrapped on two lines and carried to slide 2 as the starting equation.
- [should] ¶14 the ranking: **fixed**. "Strong students… Most students…" was removed.
- [must] ¶11 prompter "3 × 140 = 420 − 180": **verified**. It shows "3 × 140 = 420, minus 180".

### #171 solve-geo30-g007
- [should] the tips sentence: **fixed**. It is now on two lines. Arrows at the actual bends show which way each tip points ("tips left", "tip right"). The helper-line method stays first.

### #172 solve-q-r26-t30-03
- [should] ¶3 header: **fixed**. Both method headers are gone from the board (SM slides), and the sidebar names the method.
- [should] ¶7–8 crowding: **fixed**. At the upper bend, the lower-bend work is faded (the givens stay visible). The 30°/40° labels are spread out, and the final line moved up.

### #173 geo-009
- [must] ¶14 "2/2": **verified**. It shows "The two halves are equal".
- [must] ¶4/15 "doesn't…": **fixed**. It now says "does not necessarily make a right angle… does not necessarily split the angle… In this triangle it does neither." The same goes for the bisector, and the captions say "not necessarily 90° / equal angles".

### #174 geo-009-2
- [should] ¶12 "not used very often": **fixed**. It now reads "So there are two ways… The long way… The shortcut…", with no exam-frequency verdict.
- [should] ¶6–7 examples: **fixed**. Each example has its own small triangle (60°, 50°, x and 90°, 35°, x). The sum and the subtraction are written at their own clauses, and then the value is written on the figure.

### #175 geo-009-3
- [must] ¶12 "who arrives first": **fixed**. It now says "Who walks the shorter distance?"
- [must] ¶16 the quick count: **fixed**. It now says "When the two given sides are whole numbers too, there's a quick count… If the given sides are not whole numbers, just count the whole numbers between the two ends." Both examples are kept.
- [must] the endpoints: **fixed**. 5 and 13 are drawn as open circles, the speech adds "Five and thirteen themselves are not allowed… the triangle would lie flat", and only 6–12 are marked.

### #176 solve-geo31-g010: READY (no finding)
- Only a W19 pace split ("45 + 60 = 105. 105 + 75 = 180").

### #177 solve-geo31-g011
- [should] ¶1/5 "m plus n over two": **fixed**. The stem now reads "m plus half of n".
- [should] ¶6 the plug-in premise: **fixed**. It now says "The question promises one answer for every triangle that fits… so the correct choice must also be right for one triangle that we choose, and a choice that doesn't give our result is out." k = 60 is kept.

### #178 solve-geo31-g012
- [should] open endpoints: **fixed**. 7 and 19 are open circles on the band before the choices are tested.

### #179 geo-013
- [must] ¶11/20 "2/2": **verified**. It shows "the two halves of the base / of the hypotenuse".
- [must] ¶9: **fixed**. It now says "In this triangle, which is not equilateral, only this line does all three… does not necessarily do the other two jobs."
- [should] ¶4–5: **fixed**. The board reveals 44°, then 180° − 44° = 136°, then 136° ÷ 2 = 68°, and only then the two 68° labels. For the 70°/40° case, the old labels are wiped and the figure shows 70°, 70° and then 40°.

### #180 solve-geo31-g014: READY (no finding)

### #181 solve-geo31-g015
- [should] the enlarged BCD and crowding at C: **fixed**.
  - Slide 1 is the question (28° focused on the original).
  - Slide 2 has no question figure. It shows one big copy (620 wide instead of 500), and beside it a separate BCD cut-out (×1.9, same proportions and orientation).
  - The whole 76° at C, the 28° and x are separate arcs at different radii.

### #182 geo-016
- [should] ¶17 the foot: **fixed**. The foot is named H (dot, label, larger right-angle mark), and the speech says "It meets AB at the point H, very close to A, but not at A. CH is eight." The numbers were checked: BH = 8.94 of AB = 9, and CH = 8.
- [should] ¶19 the obtuse altitude: **fixed**. It now says "for some sides… The altitude to this side, from A, falls outside… The altitude from the obtuse corner, C, … would fall inside". The foot is marked "outside".

### #183 solve-geo31-g017
- [should] Method 2 letters: **fixed**. It now says "We keep the same letters: CD is x, and both triangles have the same height, h." x and both h's are on the Method 2 copy.

### #184 solve-q-r26-t31-01
- [must] the overlay: **fixed**. Slide 1 is the question (D focused). Slide 2 has no question figure and shows one clean enlarged copy. CD is traced and called h ("from C straight down to it, at a right angle. That's CD, our h") before the second area is written. The equations are at their clauses.

### #185 solve-q-r26-t31-02
- [should] ¶7 "anything up to 24": **fixed**. It now says "any positive number up to twenty-four, and it is exactly twenty-four only when these two sides are perpendicular."
- [should] ¶3–5 trial triangles: **fixed**. Only the current triangle is clear, and older positions are faded. Each changing height is a red dashed h, kept apart from the fixed side of 6.

### #186 geo-018-after
- [should] "congruent": **fixed**. It now says "They don't have the same shape, and they don't have the same side lengths."

### #187 geo-019
- [should] ¶6–7: **fixed**. The board shows "c² = 36 + 64 = 100", then "10 × 10 = 100", then "c = √100 = 10". The square root is taught at this first use (what it is, the sign, positive for lengths). The same is done for "leg² = 169 − 25 = 144" and "leg = √144 = 12".
- [must] ¶9 the chain: **fixed**. The speech now has three separate steps, and the prompter shows "13 × 10 = 130. 13 × 3 = 39. 130 + 39 = 169."

### #188 solve-geo31-g020
- [should] ¶4: **fixed**. It now says "From the longest-side rule alone, we know that AC is more than twenty-one. We haven't found its exact value yet."
- [should] ¶6: **fixed**. The calculation column shows "AB² = 400, BC² = 441" and "AC² = 400 + 441 = 841". The sides keep 20 and 21.

### #189 solve-geo31-g021
- [must] the first non-perfect root: **fixed**. It now says "AC is the positive length whose square is seventy-four", then 8² = 64 and 9² = 81 put it between 8 and 9, before the answer. Then "√74 is the exact name of this length, just as √100 = 10. It's not 74 ÷ 2, and nothing is missing."
- [should] ¶3: **fixed**. "AB² = 25, BC² = 49" goes in the calculation column, and 5 and 7 stay on the sides.

### #190 solve-geo31-g022
- [must] the recap: **fixed**. The board shows "Hypotenuse: c² = a² + b² → c = √(a² + b²)" and "Leg: b² = c² − a² → b = √(c² − a²)". The speech adds "at the end we take the square root".
- [should] ¶4: **fixed**. "AC² = 100, AB² = 49" goes in the column. The √51 reminder: "51 isn't a perfect square, because 7² = 49 and 8² = 64".

### #191 solve-q-r26-t31-03
- [should] ¶5: **fixed**. It now says "Smaller means the largest angle is acute, and the other two angles are smaller still, so every angle is acute." The three inequalities stay under the three angle pictures.

### #192 geo-023
- [should] ¶10: **fixed**. The four products are spoken and written ((a + b)(a + b) = a·a + a·b + b·a + b·b), with the signpost "come back to it after the lesson on algebraic identities". The board shows 2ab, a² + 2ab + b².
- [should] ¶5–6: **fixed**.
  - The legs a and b are labelled on the big square in both pictures.
  - The middle square has its four sides c and a right-angle mark.
  - The speech says why it's a square (four sides c, and the two sharp angles at each corner make ninety) and "The pieces haven't changed".

### #193 geo-024
- [must] ¶7 prompter: **verified**. It shows "(5, 12, 13) × 3 = (15, 36, 39)".
- [should] ¶6 ratio: **fixed**. It now says "three units, four of the same units, and five of the same units… If one unit is seven…", and the figure label reads "unit = 7".

### #194 solve-geo31-g025
- [must] the root of a product: **fixed**. It is taught at first use, on its own slide:
  - √(4·3) = 2√3, checked by squaring: (2√3)² = 2²·(√3)² = 4·3;
  - the rule;
  - a second case, √(9·5) = 3√5;
  - the trap √(9 + 16) = √25 = 5, not √9 + √16 = 7;
  - then CD² = 2·60², so CD = 60√2.
  The theorem method is kept, and the 45-45-90 shortcut is not used.
- [should] ¶4 the ACE labels: **fixed**. The ABC cut-out is wiped before ACE is focused, so only ACE's own vertices, right angle and AC = 36 / AE = 48 show.
- Prompter: the triples are now grouped ("the triple (5, 12, 13), with each number multiplied by 3", and the same for (3, 4, 5) × 12).

### #195 geo-026
- [should] ¶18/20: **fixed**. It now says "first divide nine by three, and then multiply that result by root three". The same for 6/√3. The why stays right after it.
- [should] the length (1,046 words): **parked**. Splitting into parts creates new course videos (geo-026-2, -3) and shifts the Reading Studio numbering after #195. The parts mechanism is built for camera lessons, and geo-026 is an audio-only Reading Studio lesson. → **teacher decision**.

### #196 solve-geo31-g027: READY (no finding)

### #197 geo-017-after
- [should] ¶5–6: **fixed**. A small half triangle (a, a/2, h, right angle) stays beside the Pythagoras check. The mnemonic is unchanged.

### #198 solve-geo31-g018
- [should] Method 2: **fixed**.
  - "So far: DBE side 5, S_ABC = 100√3/4";
  - "Side × ½ → area × (½)² = ¼";
  - the big triangle with the removed quarter tinted (1/4) and the remaining three quarters (3/4), at the words.

### #199 geo-027-after
- [should] ¶8: **fixed**. It now says "16 ÷ 2 = 8, and then 8 times √2 is 8√2."
- [should] ¶10: **fixed**. The square comes back with its diagonal highlighted, labelled a (side) and a√2 (diagonal).

### #200 solve-geo31-g028
- [should] ¶7: **fixed**. Method 2 now finishes the perimeter: "P = 9√2 + 9√2 + 18 = 18 + 18√2", said and written.
- [should] ¶4: **fixed**. The divide-then-multiply wording is used.

### #201 solve-geo31-g031
- [must] ¶12 "x is obtuse in the figure": **fixed**. It now says "The figure isn't drawn to scale, so we don't decide by how x looks. We simply choose an easy value, x = 110", then "50 is a real, positive angle, so our choice fits the givens."
- [should] ¶11 "1x": **verified**, and the speech now says "one allowed value of x".
- [should] ¶7–8: **fixed**. A small ABE (60°, y, 180° − x) stays above the equation.

### #202 solve-geo31-g032: READY (no finding)

### #203 solve-geo31-g033
- [must] "the full maximum": **fixed**. It now says "Let's check it with an upper bound, one that's enough to rule out the big choices", and the sidebar reads "An upper bound". The claim "every number between 20 and 30 is possible" is not made. (Checked: the supremum is 10 + 10√2 ≈ 24.1, and 7/7/10 is obtuse with perimeter 24.)

### #204 solve-geo31-g034
- [must] ¶8: **fixed**. The real condition is read: "Being a median, it cuts that side into two equal halves. And it's given as perpendicular, so it's also an altitude."
- [must] ¶6/8 symmetry: **fixed**. Two fold pictures, one for each choice:
  - equal top angles (choice 4), or equal halves (choice 2), plus the right angles;
  - the halves tinted and the outer sides ticked.
  The speech explains why the corners meet and the outer sides are equal. No congruence vocabulary is used.
- [must] ¶7 prompter: **verified**. It shows "cuts the side into two halves".

### #205 solve-geo31-g035
- [must] ¶3 prompter: **verified**. It shows "(3, 4, 5) × 4".

### #206 solve-geo31-g036
- [should] ¶7: **fixed**. It now says "ten divided by two is five, and then five times root two". The BD warning is kept.

### #207 solve-geo31-g037
- [must] the 4√3/3√3 labels: **fixed**.
  - "AD = 3√3" and "DE = 4√3" now sit beside the vertical AE, with leader lines.
  - "AE = AD + DE = 7√3" is explicit.
  - The figure is wider (360).
- [should] Method 2: **fixed**.
  - A genuinely enlarged ADC in the **same orientation** (no rotation), with AD marked "base" and EC as the red outside "height" with its right angle.
  - "Turn your head" was removed.
  - The overview picture is bigger.

### #208 solve-geo31-g038
- [should] ¶6: **fixed**. 42 and 14 appear on the triangles at "which is forty-two" / "which is fourteen".
- [should] ¶10–11: **fixed**. The washing strip is gone. "1 part / 3 parts" moved under the base, so the four 14s are written on a clean figure. The cuts are unchanged.

### #209 solve-geo31-g039
- [should] ¶10: **fixed**. It now says "We keep AE from before: two diagonals of the small squares, 10√2. And AG is two sides of a square, 10."
- [should] ¶8–10 cancellation: **fixed**.
  - "(AF + EF + AE) − (AF + FG + AG)" is written.
  - AF is faded at "it cancels", and EF/FG are faded at "they cancel too", with "AF − AF = 0, EF − FG = 0".
  - AE and AG are highlighted.
- [should] ¶11–14: **fixed**. A small AGE (right angle at G, AE highlighted) appears at "AE is the longest side". Only the negative choices are crossed, and the honest "two choices are left" is kept.

### #210 solve-geo31-g040
- [must] the b − a label: **fixed**. Both bold bottom pieces are orange and the label now reads "bold bottom = b − a", centred under the whole base, not under one piece.
- [should] ¶6–7: **fixed**. It now says "a is the smaller side, so a/b is less than one. And if b is ten… a is three. So a/b = 3/10." The full algebra line is kept, without "not during the exam".

### Shared section
- **V3 focus → enlarge:** done where flagged.
  - g002, t30-01, t30-02, t31-01, g015: the original is focused first, then a clean copy.
  - g025: ACE is focused cleanly.
  - g037: an enlarged ADC.
- **"So far" boxes:** g005, g018 and t30-01 (kept on one slide). g037 and g039 already had them. g031 keeps a small labelled ABE.
- **Squared lengths:** they go in the calculation column as AB² = …, and the figures keep the lengths (g020, g021, g022). geo-019 writes c² = 100 before c.
- **Allowed easy tests:** g006, g031 and g011 now choose the value and check it. Nothing is read off a not-to-scale drawing.
- **Prompter:** "two halves", triples, the #170/#187 chains, "1x" and "a plus" were verified in the rebuilt page. New math I wrote is protected by registry entries: √(4·3) and √(9 + 16) would otherwise display ambiguously.
- **Pen and colours:** the geometry pen stays dark blue. Givens are ink, derived values teal/orange, helper lines dashed.
- **Camera lessons** (geo-001, geo-009 parts): the right-column items are below the bubble zone (V4.8 rule). Checked in the frames.

## W19 (teacher's addition): pace + explain, no headlines

- Added to `TEACHING_STYLE_GUIDE.md` as **W19**, with the aid `python3 studio-build/w19_check.py <ids>`.
- It ran on all 50 batch-B scripts: 257 flags. I judged them by hand. Most were fine: short transitions that lead into a full sentence, "Out." after the calculation, "Given:" in the stem, and enumerations.
- Fixed by hand:
  - g005: the 77 + 56 sum is now four sentences.
  - geo-009-3: the bounds 5 and 13 are now two sentences.
  - g010, g012 and g034: sums and bounds split.
  - t31-01 ("twice that, three hundred"), geo-019 (the 13 × 13 steps), geo-024 (3-4-5 and 5-12-13 checks), g039 (AF²) and g040 (the check): each step is now its own sentence.
  - geo-017-after: "Side eight." / "Side six." became "Let's try it with a side of eight." / "Now a side of six."
  - geo-026: "Leg, leg, base." became "…: leg, leg and base."
- Every new paragraph I wrote follows W19 too: one new step per sentence, each written at its own clause.
- After: 245 flags remain, and all of them were judged acceptable.

## Checks (final build, 00:55)
- **Spec regeneration** (13–20, 30–33, 51) equals `ai_scripts`, with no PROBLEMS. 43 scripts changed, all of them batch-B lessons. g002 and g007 changed visually only.
- **`ai_check`:** no new fails. The only fail is the old solve-q-r26-t22-02 one.
- **`math_check 30 31 32`:** 0 problems, 0 warnings, layout 0. This holds normally and with `AI_HANDWRITE=all`.
- **`svgcheck`:** 54,790 slide steps, 0 broken.
- **Numbers:** every changed number was checked by script (`verify_numbers.py` in the scratchpad): 55/55 OK. Among them:
  - the g006 algebra steps (sympy);
  - CH = 8 and BH = 8.94 < 9 in geo-016;
  - the g033 supremum 10 + 10√2;
  - every root identity in g025.
- **Timing simulation** (studio's anTimeline, estimated manifests at her pace, guard on/off, 45 videos): 0 new drops and 0 delays compared with before. The geo-027-after drop is the old one, now with a new item number.
- **Early-answer check:** 0 new flags in t30. One in t31 (g018 "½ → ¼") is a parser artifact: \frac12 is read as 12.
- **Step frames:** 968 static step frames of all 50 lessons were rendered and inspected. g015, g037, geo-009, geo-019, geo-023 and g025 were reworked and rendered again from the final build.
  - Nothing is under the camera bubble in the camera parts (geo-001, geo-009).
  - Nothing runs off the board, and no labels are clipped after the fixes.
- **Builds:** the real build, `export_student` (1,019 videos, 2,357 questions, 135 cards), and the Reading Studio rebuilt with all 13 topics (323 videos, 3,760 paragraphs).
- **`video_status.py`:** Record 184 · Re-read 39 · Send 74 · Done 21 · Check 5.
  - All 50 batch-B lessons are still Record (unrecorded), and the Re-read count is unchanged (39).
  - Other changes since the start of the job come from outside this job: solve-q-578 was recorded by her (Record → Send). solve-q-360 is now Done. solve-q-362, t13-01, t13-02 and q-364 are now Check, because of seeded renders "not yet in Codex's index". None of these was touched here.

## READY TO RECORD (Reading Studio numbers, page of 00:55)
All 50: **#161–#210**. In order:
- #161–164 geo-001 parts 1–4
- #165 g002 · #166 t30-01 · #167 t30-02 · #168 geo-004 · #169 g005 · #170 g006 · #171 g007 · #172 t30-03
- #173–175 geo-009 parts 1–3
- #176 g010 · #177 g011 · #178 g012 · #179 geo-013 · #180 g014 · #181 g015 · #182 geo-016 · #183 g017 · #184 t31-01 · #185 t31-02
- #186 geo-018-after · #187 geo-019 · #188 g020 · #189 g021 · #190 g022 · #191 t31-03 · #192 geo-023 · #193 geo-024 · #194 g025 · #195 geo-026* · #196 g027
- #197 geo-017-after · #198 g018 · #199 geo-027-after · #200 g028 · #201 g031 · #202 g032 · #203 g033 · #204 g034 · #205 g035 · #206 g036 · #207 g037 · #208 g038 · #209 g039 · #210 g040

\*#195 geo-026 is ready as one lesson. Decide on the split (below) before recording it.

**She must reload the Reading Studio (version "Last updated 00:55") before recording these.**

## For the teacher
- **#195 geo-026:** split it into 2–3 parts (it has 1,046 words)? That creates new course videos and renumbers the Reading Studio after #195. Recommendation: keep it as one audio lesson unless you want to record it on camera.
- Structural changes to look at once: t30-01, t31-01 and g015 now open with a question slide, and then show our enlarged copy *instead of* the question figure. g025 has a new slide that teaches the square root of a product (√(4·3) = 2√3) at first use. geo-019 now teaches the square root sign at first use.
