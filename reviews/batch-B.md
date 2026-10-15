# Batch B — independent pre-recording review

Codex, 15 October 2026. Topics 30–31, Reading Studio **#161–210: 50 lessons**. Findings for Claude, not source edits or a claim that these fixes are already applied.

## Scope and evidence

Read each effective question/figure from the current hybrid build, the full effective spoken script, and actual prompter display. Rendered and visually inspected **all 903 static step frames, across 136 contact sheets**, with zero final rendering failures. Evidence is in the Codex workspace `work/batch-B-review-2026-10-15/`: evidence.json, frame-report.json and frames/<id>/contact-*.png. Paragraph numbers below are global, with 1-based slide.paragraph coordinates. Visual locations refer to the accompanying paragraph; native frame steps are 0-based.

Read-only status evaluation (`evaluate(save=False)`) was repeated before publication at 22:53: all 50 still unrecorded; speech and effective figures unchanged. During final verification Claude's active prompter-formatting work changed displays in 46 lessons. Compared those changes: mostly italic-variable markers/equality formatting, but two newly malformed equality chains are now included below (#170/#187). Earlier “two halves”, triple-grouping and “1x” findings still reproduce after that update. Recheck takes and the final rebuilt display again before applying changes. Preserve every existing method; no additional method is requested here.

Course order matters: topic 30 precedes algebra topic 4; topic 31 precedes powers/roots topics 8–9. Teach the small prerequisite needed at first use, rather than assuming that a later topic has already taught it. This is not a request to import an entire school-maths chapter.

**must:** false/generalised mathematics, misleading diagram, or an essential new tool used without teaching it. **should:** a material clarity/visual improvement. READY means no lesson-specific finding in this review; shared production checks still apply.

These are static board/script checks. They do **not** certify audio cuts, speech-to-pen timing, handwriting speed, persistent animated highlights or a final camera composite. Those require the take and final export. Use the studio's existing 250 ms lead once, not twice.

## Shared visual and wording follow-through

- Original figure → focus → enlargement: many solution lessons jump directly to a redrawn panel without first indicating which part of the original is being discussed. Apply V3 with a stable, precise highlight, then an actual enlarged copy with the same labels/orientation. This is a shared **should**, not 30 separate blockers. Specific wrongly registered overlays are listed below as must/should according to their effect.
- Preserve a small labelled working figure or “So far” box across board clears when the next method/calculation needs an earlier result. A later method can explicitly reuse an earlier result; it need not repeat every calculation.
- Write squared lengths as squared lengths, not as bare numbers apparently replacing side lengths. Several Pythagoras diagrams place 25/49/100 next to lengths 5/7/10; keep the original lengths and put AB² = 25, etc. in the calculation column.
- Keep easy number tests and immediate elimination. An allowed example can eliminate wrong multiple-choice expressions; it does not establish a general rule on its own. Do not choose numbers because a non-scale drawing “looks” a particular size.
- Prompter conversion must preserve **counts of pieces**: “two halves” is not the fraction 2/2. Confirmed occurrences below. Also group an entire Pythagorean triple before multiplying it.
- Claude's new italic-variable work is still in progress: do not italicise the English article “a” in “a plus”, etc. #201 (2.1) currently does this. Keep that work in Claude's claim; this review does not change his formatter.
- On the final build, check camera top-right clearance and animated crosses/highlights, not just static board items. Keep givens black/white, derived marks teal/orange, helper lines dashed. Retain her fonts and conversational easy English.

## #161 geo-001 — findings

NEW: lines, segments, gaps, angles around a point. REMINDER: multiplication/counting.

- [must] ¶8–9 (4.1–4.2): “a kind of circle of angles” introduces angles and immediately measures them in degrees without explaining what an angle measures. → First point to the opening between two rays meeting at a point; name the meeting point, explain that degrees measure the opening and a full turn is 360°. Use the existing four angles as the example, not an unrelated new topic.
- [should] ¶7 (3.3), board slide 3: the seven-point/six-gap example retains the earlier five-point picture. → Actually show seven points with six marked gaps when saying it.
- [should] ¶10 (4.3), board: the three-line example still has the two-line drawing. → Add the third line and show its six angles before saying their total remains 360°.

## #162 geo-001-2 — findings

NEW: right/acute/obtuse/straight, linear pairs, vertical angles. REMINDER: full turn.

- [must] ¶4 (2.3): “an angle is ninety degrees only if it's marked ... or it's given” excludes angles that we calculate/prove. → “Don't trust how it looks. We need a given, a right-angle mark, or a calculation that proves 90°.” Match the recap caption.
- [must] ¶6 (3.2): “An obtuse angle is bigger than ninety degrees” is incomplete and includes straight/reflex angles. → “Bigger than 90° and smaller than 180°.” Keep 130° and 160°.
- [should] ¶8 (4.1): “Adjacent angles ... on one straight line” makes all adjacent angles sound supplementary. → Explain that adjacent angles share a corner and a side; **these** other sides form a straight line, so **this pair** totals 180°. Keep the warning later in the script.

## #163 geo-001-3 — findings

NEW: bisector, three-letter angle names, parallel-line distance/transversals. REMINDER: equal halves/180°.

- [must] ¶8 (4.2): “The distance between two lines is always measured perpendicular to both” is stated for arbitrary lines. → Say “the distance between **these parallel lines**”; show the perpendicular joining them. Intersecting lines do not have the constant separation being described.
- [should] ¶16 (6.3), second numerical case: new 55°/125° text is shown beside the earlier 60°/120° diagram. → Change the diagram values too, or clearly clear/label it as a separate example.

## #164 geo-001-4 — findings

NEW: Z/U angle patterns and proving parallel lines. REMINDER: transversal/90°/180°.

- [must] ¶7 (3.2): “They're not equal. One is small and one is large.” U-angles can both be 90°. → State the invariant first: their sum is 180°. Usually one is smaller/larger; a perpendicular transversal gives 90° + 90°. Update the rule graphic too.
- [must] ¶12/14 (4.4/5.2): repeats “ninety only if it's marked or given”. → Include a calculation/proof, as in #162; do not repeat the false exclusion in the recap.

## #165 solve-geo30-g002 — findings

REMINDER: parallel angles/perpendicular lines; no new mathematical tool.

- [must] ¶3–7 (1.3–1.7), board slide 1: added lines/angle marks are shifted relative to the underlying original figure, creating a ghost second figure through the first. → Register the annotations to the actual vertices/lines, or put one clean enlarged copy in its own panel. The highlighted angle must be the angle named in the speech, not a neighbouring displaced copy.

## #166 solve-q-r26-t30-01 — findings

REMINDER: two lines perpendicular to one line are parallel; supplementary angles.

- [should] ¶3–6 (1.3–1.6), board slide 1: the added vertical c and enlarged working lines do not visibly sit on the original c/parallel lines. → First highlight the actual given right-angle marks; then either annotate in place or separate the clean enlargement. Avoid making the student decide which of two overlapping verticals is c.

## #167 solve-q-r26-t30-02 — findings

NEW: overlap is counted twice when adding overlapping segments. REMINDER: segment subtraction.

- [must] ¶3–8 (1.3–1.5/2.1–2.3), both methods: dimension-bar ends/highlighted BC do not align with the named original points. In slide 1 steps 2–5, BD/AC bars and the BC shaded patch are offset from B/C/D. → Anchor all marks to the original figure's point coordinates, with extension lines if dimensions are offset vertically. In method 2 shade the **same BC** twice, once for each addend; do not shade around C as if it were the overlap.

## #168 geo-004 — READY

NEW: no rule; introduction to question difficulty/approach. REMINDER: basic angle tools. No lesson-specific correction.

## #169 solve-geo30-g005 — findings

NEW: units-digit shortcut for the final subtraction, explained using the choices. REMINDER: Z-angles/straight angle.

- [should] ¶8–9 (3.1–3.2), method 2 board clear: only the arithmetic shortcut remains; the transferred 77°/56° at x are lost. → Carry “So far: x + 77° + 56° = 180°” and the small labelled figure into this method. Explicitly say we keep the angles already found, then shorten the subtraction.
- [should] ¶7 (2.2), slide 2 final state: solution text crowds the figure's bottom disclaimer. → Move the calculation above that line or give it a separate column.

## #170 solve-geo30-g006 — findings

NEW: rearranging an equation with several letters before the algebra topic. REMINDER: straight/full-turn angles; plugging in.

- [must] ¶6 (2.1): “drop them ... cancel ... move minus m ... move across” compresses the first needed algebra into one paragraph. → Teach the required move with a tiny numeric equality and explain “subtract the same amount from both sides”; then reveal one equivalent line at a time for this equation. Keep all three existing methods. Do not assume topic 4 was already studied.
- [should] ¶9 (3.2): “m looks obtuse, about ... 140” uses the drawing as evidence. → Choose 140° as an **allowed easy test** and show that the three neighbouring 40° angles leave x = 60° > 0. All three equal to 140° is a valid test here; no need to force extra tests once three choices are out.
- [should] ¶5 (1.5), slide 1 step 6: the long equation runs off the right of the board. → Wrap it deliberately and carry it to slide 2 as the starting equation.
- [should] ¶14 (5.2): “Strong students ... Most students ... easier” ranks students/methods. → End with the result, without the ability ranking, keeping the insight explanation itself.
- [must] ¶11 (4.1), **new final-check prompter regression**: “3 × 140 = 420 − 180” is a false equality (420 ≠ 240). The snapshot had the correct spoken separation “3 × 140 = 420, minus 180”. → Show “3 × 140 = 420. Then subtract 180” or “3 × 140 − 180 = 420 − 180”, without forcing a calculation the script deliberately avoids. Keep the speech as it is; fix formatting only.

## #171 solve-geo30-g007 — findings

NEW: auxiliary parallel line and zigzag shortcut. REMINDER: Z-angles/angle addition.

- [should] ¶8–9 (2.1–2.2), shortcut board: the tips-left/right sentence reaches beyond the right edge. → Reflow it and show arrows at the actual bends so “tips” refers to a visible vertex, not an unexplained verbal label. Keep the dashed-helper method first.

## #172 solve-q-r26-t30-03 — findings

REMINDER: zigzag rule/parallel helpers; no new tool.

- [should] ¶3 (1.3), board: the method header intersects the original upper line. → Put it above the figure rather than across it.
- [should] ¶7–8 (2.2–2.3), second method: transferred 30°/40°/x marks crowd the same bends. → Keep the two helpers but offset labels/arcs and fade marks no longer needed, without clearing the givens.

## #173 geo-009 — findings

NEW: median, altitude, bisector in a triangle. REMINDER: midpoint, perpendicular, equal angles.

- [must] ¶14 (5.2), **actual prompter**: “The **2/2** are equal” replaces the spoken “two halves”. → Restore “The two halves are equal”; prevent this count from becoming the fraction 2/2. Same converter problem appears in #179/#204.
- [must] ¶4/15 (2.3/5.3): “It doesn't make a right angle ... doesn't split ...” sounds impossible rather than not guaranteed, contradicting the later special-triangle explanation. → “Being a median only tells us the two side pieces are equal. It does **not necessarily** ...” Likewise a general bisector need not be a median/altitude; it can be in special triangles. Keep the depicted unequal pieces as an example.

## #174 geo-009-2 — findings

NEW: triangle angle sum/exterior angle rule. REMINDER: parallel-line angles.

- [should] ¶12 (5.1): “not used very often ... don't really need” undermines the exterior-angle shortcut subsequently used in #177/#201. → Present it as an alternative to completing to 180°, without an exam-frequency verdict.
- [should] ¶6–7 (3.1–3.2), numerical angle-sum examples: the board mainly gives arithmetic rather than tracing the three angles. → Put 50°, 60° and the unknown on a small triangle, reveal the sum and subtraction separately; update the same clear layout for the 90°/35° example.

## #175 geo-009-3 — findings

NEW: side/angle ordering, triangle inequality, counting possible integer lengths. REMINDER: straight path/counting.

- [must] ¶12 (4.3): “Who arrives first? ... because his road is shorter” assumes equal speeds. → Ask “Who walks the shorter distance?” Keep the intended straight-path explanation without making an unsupported time claim.
- [must] ¶16 (5.4): “A quick count is twice the shorter side, minus one” states only that the **third** side is a whole number. → State that this shortcut assumes the two given lengths are whole numbers too, and that we count whole-number third sides. Otherwise count the integers strictly between the two bounds. Keep both existing numeric examples.
- [must] ¶15–16 (5.3–5.4), board slide 5: strict endpoints 5 and 13 are drawn like included endpoints. → Use open circles at the bounds and mark only 6–12 as admissible integer lengths. Do not let a shaded range imply a degenerate triangle is allowed.

## #176 solve-geo31-g010 — READY

NEW: the small equation 12x = 180 is explained by division. REMINDER: vertical angles/triangle angle sum. The three angles and final 15° are traceable; no lesson-specific correction.

## #177 solve-geo31-g011 — findings

REMINDER: exterior/straight angles; substitution. No new formal rule.

- [should] ¶1/5 (1.1/1.5): “m plus n over two” can be heard as (m+n)/2. → Read it as “m plus **half of n**”, keeping m + n/2 in the prompter/board and the original choice expression. This is clarification, not a change to the requested expression.
- [should] ¶6 (2.1), plug-in introduction: make the multiple-choice premise explicit: the correct expression must work for every allowed triangle, so a wrong value rules a choice out. → Keep k = 60° and immediate checks; do not present one numerical case as a general proof.

## #178 solve-geo31-g012 — findings

REMINDER: strict triangle inequality and choice elimination.

- [should] ¶5 (2.1), interval graphic: use open endpoints for 7 < x < 19 rather than solid endpoint marks with later rejection. → The strict inequality should be visible before testing choices; keep 11 as the accepted length.

## #179 geo-013 — findings

NEW: isosceles symmetry, equilateral properties, median to a right triangle's hypotenuse. REMINDER: median/altitude/bisector.

- [must] ¶11/20 (4.2/7.2), **actual prompter**: “the **2/2** of the base” and “the **2/2** of the hypotenuse”. → Restore “two halves” in each; a count of equal pieces is not the fraction 1.
- [must] ¶9 (3.3): “Only this line does all three ... [another median] isn't perpendicular” forgets the equilateral case, taught immediately afterwards. → Qualify “in this non-equilateral example” or “a median to a leg does not **necessarily** do the other two jobs”.
- [should] ¶4–5 (2.3–2.4), slide 2 numerical example: 44° and both 68° labels arrive together. → Reveal given 44°, then 180−44 = 136, then 136÷2 = 68°, and only then the two base-angle labels. When switching to the 70°/40° case, change the diagram's values rather than leaving 44°/68° underneath it.

## #180 solve-geo31-g014 — READY

REMINDER: equilateral angles and a bisector that is also a median. No new tool. DC = 7 → BC = 14 → AB = 14 is clear.

## #181 solve-geo31-g015 — findings

REMINDER: isosceles base angles and angle subtraction.

- [should] ¶4–6 (1.4–1.6), enlarged BCD: the cutout is stretched into a different-looking tall triangle, and the 76°/28° marks crowd C. → Enlarge the actual BCD without changing its proportions/orientation; distinguish the whole 76° angle from the interior 28° angle with separate arcs. Keep the 48° subtraction.

## #182 geo-016 — findings

NEW: square units and rectangle/right/general triangle area. REMINDER: perpendicular height.

- [should] ¶17 (6.2), second base-height pair: the perpendicular foot from C to AB is almost indistinguishable from vertex A in this near-right drawing. → Name the foot H and make the CH = 8 label/right-angle mark unmistakable (an inset is fine). Do **not** label AC = 8 or put the square at A. The source does calculate the projection rather than intentionally making A a right angle; this is a clarity issue, not a claim that the numerical example is impossible.
- [should] ¶19 (7.1): “In an obtuse triangle ... the altitude falls outside” sounds true for every altitude. → “For **this base** of the obtuse triangle, the height falls outside.” Point to the extension and perpendicular foot; the altitude from the obtuse vertex to the opposite side lies inside.

## #183 solve-geo31-g017 — findings

NEW: same-height area ratio. REMINDER: triangle area/parallel-line distance.

- [should] ¶8–9 (2.1–2.2), second method: DE = 5x and h silently reuse the earlier letters. → Start “Keep CD = x and the same height h”, and carry those labels onto the board. Alternatively write DE = 5·CD. The five-equal-parts picture is useful; retain it.

## #184 solve-q-r26-t31-01 — findings

NEW: ab = ch as cancellation of the two equal area expressions. REMINDER: right-triangle area.

- [must] ¶2–5 (1.2–1.5), board slide 1: the teacher's full-triangle overlay is shifted from the underlying figure, so C/D and the altitude do not coincide with the named givens. → Align to the true question coordinates or move one clean enlarged triangle into its own panel. Establish exactly which segment is h before writing either area.

## #185 solve-q-r26-t31-02 — findings

NEW: maximum area from two given sides. REMINDER: height ≤ slanted side, triangle area.

- [should] ¶7 (1.7): “anything up to twenty-four” can include zero. → Say “positive and at most 24; it reaches 24 when these sides are perpendicular.” Keep the existing ≤24 board inequality.
- [should] ¶3–5 (1.3–1.5), moving-vertex illustration: several trial triangles/6 labels accumulate. → Show one current triangle, with old positions faint or cleared, and clearly distinguish the fixed side of 6 from the changing perpendicular height. This is the visual reason for the maximum.

## #186 geo-018-after — findings

NEW: a median halves area, not necessarily shape. REMINDER: same base/height area.

- [should] ¶7 (2.6): “not congruent” uses topic 33 vocabulary before teaching it. → Say “same area does not mean the same shape or the same side lengths”, alongside the unequal shapes. No extra congruence lesson is needed here.

## #187 geo-019 — findings

NEW: Pythagoras, squared lengths and recovering a length. REMINDER: right triangle/hypotenuse.

- [should] ¶6–7 (3.2–3.3), first calculation: put **c² = 100** before c = 10, not just a loose “100”. → Explicitly connect 10×10 = 100 to √100 = 10; do the same with 12×12 = 144 in the other example. Roots have not had their dedicated topic yet; the existing examples can teach this small needed inverse step.
- [must] ¶9 (4.2), **new final-check prompter regression**: “13 × 10 = 130 + 13 × 3 = 39, so 169” is a false chain. → Keep the partial products separate: “13 × 10 = 130. 13 × 3 = 39. 130 + 39 = 169.” The source speech already separates them; the converter must not turn the spoken “plus” into an equality chain with unequal terms.

## #188 solve-geo31-g020 — findings

REMINDER: Pythagoras, longest side/triangle inequality.

- [should] ¶4 (1.4): “AC could be twenty-one and a little” sounds like AC varies in this fixed right triangle. → “From the longest-side rule **alone**, we know AC is above 21; we haven't found its exact value yet.” The exact length remains 29.
- [should] ¶6 (2.1), squared-value labels: bare 400/441 sit next to the sides 20/21. → Write AB² = 400 and BC² = 441 in the calculation column, not as apparent replacement lengths on the triangle.

## #189 solve-geo31-g021 — findings

NEW: an exact non-whole-number square root. REMINDER: Pythagoras/perfect squares from #187.

- [must] ¶4–5 (1.4–1.5): “take the root ... leave it exactly like that” uses the first non-perfect root without fully explaining what √74 means. → Say it is the positive length whose square is 74; 8² = 64 and 9² = 81 put it between 8 and 9, and √74 is its exact name, not 74÷2 or a missing calculation. Move that existing sense-check **before** settling the answer. Let #190's √51 provide the second example, with an explicit reminder, rather than importing the entire roots topic.
- [should] ¶3 (1.3), board: keep 5/7 on the sides; write 5² = 25 and 7² = 49 in the calculation area, not bare 25/49 beside the side labels.

## #190 solve-geo31-g022 — findings

REMINDER: finding a leg by Pythagoras; non-perfect root from #189.

- [must] ¶6 (2.1), recap graphic: “hypotenuse a²+b², leg c²−a²” is presented like a side-length recipe but omits the final root. → Either label these explicitly **squared lengths**, c² = a²+b² and b² = c²−a², or give the full length formulas with √. Say “then take the square root”.
- [should] ¶4 (1.4), board: bare 49 and 100 alongside sides 7 and 10 can be read as new lengths. → Keep squares in the calculation column, as in #188/#189.

## #191 solve-q-r26-t31-03 — findings

NEW: comparing the largest square with the sum classifies acute/right/obtuse triangles. REMINDER: longest side/opposite angle.

- [should] ¶5 (1.5): when the largest angle is less than 90°, explicitly connect why **all** angles are then acute: the other two are smaller still. → Keep the three inequalities next to their three clearly marked angle diagrams, rather than a numerical test alone.

## #192 geo-023 — findings

NEW: optional rearrangement proof. REMINDER: square/triangle areas and Pythagoras.

- [should] ¶10 (5.3): expansion of (a+b)² and cancellation are used very quickly. → Since this is optional, keep that label and unpack the four products on the board, or clearly signpost that the final algebra can be revisited after identities. Do not make formal proof a prerequisite for using the theorem; preserve the existing visual method.
- [should] ¶5–6 (4.1–4.2), rearranged square: mark the four corner triangles' corresponding legs and the central right angle. → Make it visible why the pieces have not changed and why the middle shape really is a square, not merely a coloured quadrilateral.

## #193 geo-024 — findings

NEW: Pythagorean triples/scaling. REMINDER: squares/Pythagoras.

- [must] ¶7 (3.2), **prompter**: “5, 12, 13 × 3 = 15, 36 and 39” writes a multiplication on only the final entry. → “Multiply **each** of 5, 12 and 13 by 3. We get 15, 36 and 39”, or show the grouped triple (5,12,13) × 3 = (15,36,39). Keep commas clearly as list separators, not a malformed equality.
- [should] ¶6 (3.1): ratio notation arrives before the ratios topic. → Explain “3 units, 4 of the **same** unit, 5 of the same unit”; show one unit becoming 7 in the existing 21/28/35 example. The scaling examples already supply the practice; no extra method is required.

## #194 solve-geo31-g025 — findings

NEW: simplifying √(2×60²). REMINDER: triples/Pythagoras/non-perfect roots.

- [must] ¶6 (2.2): “the root ... is the root of two, times sixty” is a new root-product rule stated as if familiar; topic 9 comes later. → Teach the extraction with an easy perfect-square factor first (e.g. √(4×3) = 2√3), explain that squaring the proposed length gives the original number, then apply the same idea to 60²×2. Give a second small case and the trap “multiply, not add” within this first-use explanation. Keep the current theorem method; do not replace it with the still-untaught silver-triangle shortcut.
- [should] ¶4 (1.4), ACE enlargement: labels from the overlapping previous figure obscure which right angle/vertices belong to ACE. → Use a clean actual ACE cutout, carrying AC = 36 and AE = 48.

## #195 geo-026 — findings

NEW: 30°/60°/90° ratio, dividing by √3, 30°/30°/120° triangle. REMINDER: equilateral altitude/Pythagoras/root extraction.

- [should] ¶18/20 (7.2/7.4): “ignore the root ... put the root back” sounds like an arbitrary operation. → Use the precise procedure “divide 9 by 3, then multiply that result by √3”, keeping the existing why immediately afterwards: 9/√3 = 9√3/3. Repeat with 6/√3. This clarifies the same shortcut, not a new method.
- [should] ¶1–27 (whole lesson): 1,046 spoken words span three substantial new tools. → Consider separate camera parts at the existing natural boundaries: basic gold triangle; working back from its long leg/dividing by √3; the 120° triangle. Preserve every example and why; do not shorten it back into slogans. This is pacing advice, not an invented runtime measurement.

## #196 solve-geo31-g027 — READY

REMINDER: gold-triangle ratio and Pythagoras check. Root extraction relies on the first-use teaching requested in #194. Both methods identify their known sides and get 15 + 5√3; no additional lesson-specific correction.

## #197 geo-017-after — findings

NEW: equilateral-triangle area formula. REMINDER: gold height/Pythagoras.

- [should] ¶5–6 (3.1–3.2), alternative height calculation: “the same half triangle” is said after its diagram is cleared. → Keep a small right half-triangle labelled a, a/2 and h beside the algebra. Retain the intentional “a-two-three-four” mnemonic as spoken words; it is not a malformed formula to auto-convert.

## #198 solve-geo31-g018 — findings

NEW: halving the side quarters the area via the formula. REMINDER: equilateral area/subtracting areas.

- [should] ¶9–10 (3.1–3.2), method 2: explicitly retain “DBE is equilateral” and the big area found earlier. → Carry a “So far” note; show (1/2)² = 1/4 on the same big/small triangle. Shade the removed quarter and remaining three quarters instead of leaving the ratio solely in prose. This does not require teaching the later midpoint theorem.

## #199 geo-027-after — findings

NEW: 45°/45°/90° ratio/square diagonal. REMINDER: Pythagoras/root-division shortcut.

- [should] ¶8 (4.2): “ignore the root ... put the root two back” → use the explicit operation wording from #195: 16÷2 = 8, then 8×√2. Keep the reminder short because the why was already taught.
- [should] ¶10 (4.4), square diagonal: the final connection is text-only. → Return to the square, highlight its diagonal, and label the leg a/diagonal a√2 as said.

## #200 solve-geo31-g028 — findings

REMINDER: silver ratio and Pythagoras; no new tool.

- [should] ¶7 (2.2): method 2 ends after “t is nine root two ... choice number one”, without completing the requested **perimeter**. → Finish “two legs of 9√2, plus 18: 18 + 18√2” on screen and aloud. This makes the second method complete without repeating the first.
- [should] ¶4 (1.4): use the precise divide-then-multiply wording from #195/#199 rather than “ignore ... put back”.

## #201 solve-geo31-g031 — findings

REMINDER: triangle sum, exterior angle, allowed-number elimination.

- [must] ¶12 (4.2): “In the figure x is an obtuse angle” is inferred from appearance, not the givens. E inside BC permits acute x too (60° < x < 120°). → Say we **choose** an allowed easy value, not that x must be obtuse. For example x = 90° gives y = 30°; 110° also works if explicitly chosen as a test, not deduced from the drawing.
- [should] ¶11 (4.1), **prompter**: “true for **1x** that we choose” turns “one x” into a coefficient. → “true for an allowed value of x that we choose”.
- [should] ¶7–8 (2.1–2.2), equation-only slide: retain the small ABE with 60°, y, 180°−x so the equation still has a visible source.

## #202 solve-geo31-g032 — READY

REMINDER: angle sum, larger angle/opposite longer side. The comparison α > 65° > 50° is explained, and β need not be compared with 50°. No lesson-specific correction.

## #203 solve-geo31-g033 — findings

NEW: ordered-range/single-correct-choice insight. REMINDER: triangle inequality/obtuse opposite side.

- [must] ¶7–8 (3.1–3.2): “the **full maximum**” calls 30 the actual upper endpoint. The reasoning proves only an easy upper bound, P < 30, not the complete attainable range. → Say “Let's find an upper bound that's enough to rule out these choices.” Do not claim every number between 20 and 30 is possible. Keep the short exam solution; no need to add the tighter bound to the student's lesson. Reviewer check: the true supremum is 10+10√2, and a 7/7/10 obtuse triangle shows 24 really is attainable.

## #204 solve-geo31-g034 — findings

NEW: converses linking a median/altitude/bisector to an isosceles triangle. REMINDER: forward isosceles properties.

- [must] ¶8 (2.4): “the median makes two equal angles, alpha and alpha” does not follow from being a median. Here perpendicularity is explicitly **given**. → Read the actual condition: “This median is perpendicular, so it is also an altitude.” Do not introduce angle-bisecting as a property of every median.
- [must] ¶6/8 (2.2/2.4): “That's a line of symmetry, so ...” asserts the converse without teaching why. → Show the two halves folding/mirroring with the equal given angles or equal half-bases and the common height. Explain the equal outer sides in simple language, without requiring the not-yet-taught congruence chapter. Then the later choice can use that established fact as a reminder.
- [must] ¶7 (2.3), **prompter**: “cuts the side into **2/2**” → “cuts the side into two equal halves”. Fix the converter, not just the visible HTML.

## #205 solve-geo31-g035 — findings

REMINDER: two triples, right-triangle areas, area addition.

- [must] ¶3 (1.3), **prompter**: “That's **3, 4, 5 × 4**” gives the same ungrouped multiplication problem as #193. → “Each number in 3, 4, 5 is multiplied by 4” or a clearly grouped triple. Keep 12/16/20 and the 20/48/52 continuation unchanged.

## #206 solve-geo31-g036 — findings

REMINDER: gold then silver ratio; a shared segment changes role from leg to hypotenuse.

- [should] ¶7 (2.2): “ignore the root ... stick the root two back on” → “10÷2 = 5, then multiply by √2”, as already taught in #195/#199. Keep the excellent explicit warning that BD is the hypotenuse of the second triangle, not a leg.

## #207 solve-geo31-g037 — findings

REMINDER: shaded-area subtraction, gold triangle, outside altitude. No new area formula.

- [must] ¶5–6 (1.5–1.6), board slide 1 steps 6–7: the 4√3 and 3√3 labels lie by the sloping AB outline instead of the intended vertical DE and AD. → Anchor them beside their actual height segments, with a brace/leader if needed, and keep AE = AD+DE explicit. A student must not infer those are lengths of AB's pieces.
- [should] ¶11–13 (3.1–3.3), method 2: the supposedly enlarged working figure is too small to follow, and its reorientation is abrupt. → Use a genuinely enlarged ADC, preserve orientation first, then visibly indicate any rotation with the same A/D/C/E labels. Mark AD as the chosen base and EC as the perpendicular external height, rather than relying on “turn your head”.

## #208 solve-geo31-g038 — findings

REMINDER: triangle area/common height; the equal-parts interpretation extends #183.

- [should] ¶6 (2.2), board slide 2: area numbers 42 and 14 are already inside the focused triangles before the calculation chain establishes them. → Reveal each number at its actual result clause, keeping xh = 28 available first.
- [should] ¶10–11 (3.3–3.4), four-part picture: the white translucent strip used to fade “1 part / 3 parts” also washes out the base region, and old/new text remains cluttered. → Remove/replace those two text labels cleanly before writing the four 14s; retain the correctly spaced cuts and base-equality marks. The source cut coordinates themselves are correct—no repartition of the geometry is requested.

## #209 solve-geo31-g039 — findings

NEW: perimeter-difference cancellation/sign-only estimation. REMINDER: silver ratio/Pythagoras.

- [should] ¶10 (3.3), insight method: AE = 10√2 appears without a fresh derivation or explicit reuse. → “Keep AE = 10√2 from the two square diagonals, and AG = 10.” This method may reuse that result but should say so; it must not require calculating AF.
- [should] ¶8–10 (3.1–3.3), cancellation visual: the shared AF is coloured but its cancellation is not explicit. → Cross out the identical AF terms and mark EF = FG; fade those cancelled edges, leaving AE−AG. This is the signature visual that makes the insight understandable.
- [should] ¶11–14 (4.1–4.4), sign estimate: keep a small AGE with its right angle while saying AE is its hypotenuse. → Cross out only the negative choices as spoken. Preserve the honest conclusion that two choices remain; do not turn a partial elimination into a proof of choice 4.

## #210 solve-geo31-g040 — findings

NEW: ratio from a perimeter relation/testing proposed ratios. REMINDER: equilateral perimeter/equations.

- [must] ¶4 (1.4), board slide 1 step 4: “b−a” is printed under only the **left** outer base piece, although it is the sum of **both** remaining pieces. → Bracket both bold bottom pieces together as b−a, or show whole base b minus central gap a. Do not assign b−a to one piece.
- [should] ¶6–7 (1.6–1.7): “three to ten, or ten to three ... not during the exam” encourages skipping which way the requested ratio goes. → Use a quick clear check: 3b = 10a, and a is the smaller length, so a/b < 1; choosing b = 10 gives a = 3 and a/b = 3/10. Keep the optional division-by-10b line without calling understanding it unsuitable for the exam.

## Handoff / acceptance

Fix must items before recording the affected scripts; apply should items where they improve following the same existing content. A visual-only finding does not justify rewriting the spoken script. The most urgent clusters are #162/#164 rule scope, #165/#167/#184 overlay registration, #173/#179/#204 “two halves”, #170/#189/#194 first-use teaching, #190 missing-root recap, #201 non-scale inference, #203 bound wording and #210 combined-base label.

Rebuild from canonical sources, check the actual prompter again, then re-render changed steps. Recheck statuses before any spoken change. This report does not authorise changing a lesson she has recorded meanwhile. Batch C/D are not included in this completed batch B review.
