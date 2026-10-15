# Batch A — independent pre-recording review

Reviewed by Codex, 15 October 2026. Scope: **30 initially unrecorded** lessons in topics 15–20. At the final check, #147 had just been recorded; it is therefore skipped below. **29 lessons remain in the actionable review.** Numbers below are Reading Studio lesson numbers, not the hybrid's separate video numbers. All recorded lessons were excluded from actionable findings. No scripts, visual plans, studio HTML, recordings or render registrations were edited.

## How to use this review

- Fix **must** findings before recording the affected paragraphs. **Should** findings improve followability; visual-only findings do not themselves require changing otherwise good speech. Do not turn these notes into blanket rewrites or add extra methods.
- Each reference is global paragraph number, then `(slide.paragraph)`, both 1-based. Quotations are the current spoken script unless explicitly marked **prompter** or **board**.
- Keep every existing method, the original fonts/design, easy allowed test numbers and immediate elimination. Do not add a second or third test after the answer is settled. Do not turn examples into a claimed proof of “always.”
- Apply shared fixes only to still-unrecorded lessons. Recheck recording status before editing: Nitzan may record meanwhile. Rebuild the Reading Studio from canonical sources, including display overrides, not by editing exported HTML alone.

Evidence: current `ai_scripts`, its effective `reading_studio.prompter_display`, effective questions/choices from the current hybrid build, study-plan `ORDER`, teaching guide and prior-topic concept maps. Relevant current prerequisite scripts were also checked (consecutive integers/products/sums and topic-51 plugging in).

Rendered and visually inspected **all 487 static step frames**, including intermediate reveals, for all 30 lessons. There were no rendering exceptions. This checks layout and reveal structure; it is **not** an audio-timed video check. Actual word timing, handwriting speed, camera footage and highlight persistence must be checked after recording. The frame renderer reserves the studio's camera space but does not paste in a face.

Frozen evidence, full scripts/display text, effective video data, per-lesson frame counts, SVGs and contact sheets:
`/Users/nitzanslasky/Documents/Codex/2026-10-11/https-github-com-nitzanslasky-source-psychometry/work/batch-A-review-2026-10-15/`.

## Shared fixes — preserve content, fix delivery

1. **Do not confuse “divides” with “is divisible by.”** “N is divisible by d” is exact; “d divides N” means the same thing. Nitzan's “N divides by d” is familiar to her, so this review is not asking to replace every occurrence. Avoid bare phrases that could reverse the relationship, and keep mathematical captions unambiguous.
2. **V4 remains incomplete in the camera introductions.** A single board item often contains two examples, both results or an entire chain. A single appearance/anchor cannot reveal each clause separately. Split/chunk the existing mathematics at its actual spoken clauses, keeping completed work. Examples and locations are given below. Do not solve this by adding another visual lead; the existing lead is 250 ms once.
3. **Formatting must not change maths.** In particular, fix #83 and the remainder display in #48 below in the canonical display override. Verify the displayed paragraph after rebuilding, not just the narration JSON. Do not use an equals sign for a false assertion or an unfinished calculation. #147 was recorded during review and is excluded from this change request.
4. **Recording style cleanup, not a content rewrite:** remove “Okay.” before goodbye; use “choice number N is our answer”; prefer “to the power of three” to “cubed.” Keep this lower priority than the concrete misunderstandings below. Do not flag already-recorded speech for these cosmetic changes.

## #46 divisibility — findings

NEW: divisibility tests for 4/8 and their place-value reason; REMINDERS: even/odd, divisibility, 2/3/5/9/10 tests (some introduced in earlier topics).

- [should] ¶2 (2.1), “538 divided by two is 269” → this starts a *quick-test* lesson with unexplained three-digit division. Keep the example but say the easy split, `500÷2=250`, `38÷2=19`, `250+19=269`, or use a genuinely small definition example. No expectation of doing 538÷2 mentally without help.
- [should] ¶6/8 (3.1/3.3), “Nine plus four is thirteen…” / “Eight plus four is twelve…” → the board only supplies `9+4+2=15` and `8+4+6=18`. Show the spoken intermediate sums at those clauses and then the divisibility conclusion; reveal the second 942 example only when it returns in ¶8.
- [should] ¶12 (4.4), “For eight, we do the same thing…” → only one actual test case is worked. Add a short contrasting case using the same number changed by one, e.g. 7,241: 240 divides by 8, the next number does not. Write `240=30×8` in the existing visual, without an extra lecture on division.
- [should] ¶3–5 (2.2–2.4), board examples “538 ✓ 741 ✗” etc. → each positive/negative example currently arrives as one item. Separate each example and steadily mark the **last digit** being discussed, rather than the entire example row. Existing font and layout can stay.

## #47 divisibility-2 — findings

NEW: combining divisibility tests safely; tests for 11. REMINDERS: prime-factor overlap, tests from part 1.

- [must] ¶5–6 (2.4–2.5), “the two parts must share no factor” / “Three and four share nothing” → they share **1**. Say “They must not share a divisor bigger than 1.” Put that condition **before** stating the general product rule. Retain 18 as the counterexample to the unsafe 2-and-6 test; show `6=2×3` so the reused factor 2 is visible.
- [must] ¶10 (3.4), “For longer numbers… That's not zero, eleven or negative eleven” and board “The result is 0, 11 or −11” → this list is not the general test for arbitrarily long numbers. State “The result must be divisible by 11, including 0.” The short list can be labelled as the values relevant to the short examples, not the full rule. Reviewer check: 90,904 has alternating sum `9−0+9−0+4=22` and equals `11×8264`. The repair is the exact general rule; there is no need to add this large check number to the teaching script.
- [should] ¶8–10 (3.2–3.4) → all three techniques are crammed into one slide and their paired success/failure calculations are single items. Keep the methods but distinguish “first two digits minus last” from “alternating digit sum,” reveal one calculation at a time, and show 41−8=33 separately from 42−7=35. Do not leave the ±11 caption next to the first method's valid result 33 without explaining which test it belongs to.

## #48 divisibility-3 — findings

NEW: remainder/quotient interpretation, small dividend trap, remainder cycle, digit-sum remainder rule. REMINDERS: multiplication/division and digit sums.

- [must] ¶7 (3.3), **prompter** “5 ÷ 8 = 0, with a remainder of 5” → display `5 = 8×0 + 5` or “5÷8: quotient 0, remainder 5.” `5÷8=0` alone is false and invites a wrong reading. Preserve the shop explanation; it is a good concrete explanation of the trap.
- [should] ¶11–13 (5.1–5.3), “Fourteen divided by nine leaves five” → the board shows `14÷9:5` and `14÷3:2`, without saying these are **remainders**, and does not explicitly carry the result back to 5432. Write `14=9×1+5 ⇒ remainder 5 for 5432÷9`, then the separate by-3 result. Keep the two results separate in time.
- [should] ¶8–9 (4.1–4.2), board `1→1,2→2,...` → label the two quantities “number” and “remainder” and reveal complete pairs. The current generic arrow splitter reveals dangling pieces such as `1→1,2`, rather than the complete next example. A two-row table is enough; no new style is needed.

## #49 divisibility-4 — findings

NEW: representing a remainder with a letter, changing to a divisor of the old divisor. REMINDERS: quotient/remainder and factors.

- [must] ¶8 (3.4), “eight k isn't made of whole sixes, and it can leave anything” → false: 8k **can** be divisible by 6 (k=3), and `(8k+2)÷6` only leaves 0, 2 or 4, not anything. Say “Knowing the remainder by 8 doesn't tell us one fixed remainder by 6. Our allowed examples gave 2 and 4.” No need to teach the set of all possible remainders here.
- [should] ¶2–4 (2.1–2.3), “We call this a tag” / “Another tag” → this is exactly the unexplained label Nitzan disliked. Use “k tells us how many complete groups of 4 there are.” Start with `7=4×1+3`, then `11=4×2+3`, then `N=4k+3`. Keep k=0 as the small-dividend reminder. The numbers are already present; make their meaning explicit instead of introducing a name.
- [should] ¶8 (3.4), “they drop out” → say “15k leaves no remainder when divided by 5, so only the extra 4 matters.” Keep the written `15k=5×3k` visible with that explanation. Do not replace the metaphor with another metaphor.
- [should] ¶10 (4.2), “For eleven, the first two digits minus the last one…” → specify “for a **three-digit** number.” Otherwise the recap presents a three-digit shortcut as a rule for numbers of any length.

## #67 whole-numbers — findings

NEW: applying known signs to a whole expression. REMINDERS: multiplication/division signs (topic 1), powers (8–10), absolute value (13). Do not reteach these as if the student has never met them.

- [must] ¶17 (7.1), “surely positive, like even powers and absolute values. Then the piece that's left decides the sign” → both may be **zero**, and one remaining piece decides the sign only in an appropriate product/quotient, not an arbitrary sum. Say “For a nonzero x, x² and |x| are positive. In a product or quotient, these positive factors don't change the sign of the other factor.” Keep the zero case visible (`x=0 ⇒ x²=|x|=0`); correct the “Surely positive first” board caption too.
- [should] ¶16 (6.2), “because nine is farther from zero than four” → refer to the actual term **minus nine**. Also cover equal distances briefly: `−4+4=0`. This is a reminder, not another full sign lesson.
- [should] ¶2–3/9/11–13/16 (2.1–2.2, 4.1, 5.1–5.3, 6.2) → rows currently reveal two or three completed examples together. Separate the existing calculations/results at their clauses, especially the three division cases and the positive/negative/zero absolute values.

## #83 solve-q-r26-t16-04 — findings

NEW: why three successive odd numbers include a multiple of 3. REMINDERS: consecutive odds, divisibility of a product, adaptive counterexamples (topic 51/earlier questions). Effective choices: 45, 15, 3, 5; answer 3 / choice 3 is correct.

- [must] ¶7 (1.7), **prompter** “10 × 35 = 350, and **135 less** is 315” → the intended subtraction is **35**, not 135. Use `350−35=315`; spoken “Take away one group of 35.” In ¶5 the display also reads `10×63=630 + 1 more 63`, falsely attaching the extra group to the equality: show `63×11=630+63=693` as separate steps.
- [should] ¶5–7 (1.5–1.7) → calculating 693, then two more products after three choices are already eliminated is avoidable work. Keep 7,9,11 as the easy reasoned second test, but use its units digit (`7×9` ends in 3, then ×11 still ends in 3), or the already-taught prime-factor rule. Keep any warning about groups containing 5 **before** the second test and don't compute both discarded test products after the answer. Preserve both solution methods.
- [should] ¶8–9 (2.1–2.2), “They appear once in every three odd numbers” → show a short row of consecutive odds and highlight 3,9,15 in it. “Odd multiples of 3: 3,9,15,21” alone doesn't show why no three consecutive odds miss them. Retain the two existing groups as the examples; no formal modular proof needed.

## #92 number-line — findings

NEW: four-region classification and using a mirrored picture. REMINDERS: sign/order, fraction size, powers.

- [must] ¶6 (2.5), “If a question only says x is positive, x could be between zero and one, or above one” → missing **x=1**, immediately after naming it as a special border. Say “It could be between 0 and 1, exactly 1, or above 1.” Keep the border visible as a third possibility.
- [should] ¶4 (2.3), “they both move the same way” → make the comparison concrete with the already-mentioned halves/quarters: “Times 2 makes both bigger. Times 1/2 makes both smaller.” Do not imply the operation can be ignored without checking its multiplier or exponent.
- [should] ¶9–10 (3.3–3.4), “it also moves toward zero” → the on-screen axis still shows the old **×2 outward** arrows while the narration has switched to ×1/5 inward. Add the inward movement on that same axis at those words, and mark −3 to the right of −15. The existing equations alone don't illustrate the mirror reasoning being taught.

## #93 number-line-2 — findings

NEW: classifying operation effects and comparisons across different regions. REMINDERS: reciprocals, exponent signs, negative bases versus external minus.

- [must] ¶8 (3.2), “Eleven tenths is not really a fraction… Seven ninths is a real fraction” → 11/10 **is** a fraction. Say “11/10 is bigger than 1 because 11>10. 7/9 is between 0 and 1 because 7<9.” Use “a fraction **between 0 and 1**” wherever the shrink/grow rules need that restriction, including ¶4–5; not every positive fraction is less than 1.
- [should] ¶7–10 (3.1–3.4), “stays bigger after any positive power or root” → connect this to the **different four regions**, not arbitrary bases in the same region. Add the short reason: a positive power/root keeps a positive number on its original side of 1. Bring the odd-only restriction for negatives into the rule before applying it, not as a late exception. Two current positive examples can stay; no long derivation needed.
- [should] ¶2–5/11–14 (2.1–2.4, 4.1–4.4) → each pair of calculations is a single board appearance. Split the multiplication/division cases and the two negative-exponent rewrites. Keep each starting comparison written before its classification/result.

## #94 number-line-3 — findings

NEW: combining factor-size comparisons (“strong on strong”). REMINDERS: same positive power/root order and negative exponents.

- [must] ¶2 (2.1), “exactly the same operation… whichever number was bigger… is bigger with it” → too broad: reciprocals or multiplication by a negative reverse order, exponent 0 makes ties. Name the intended tool: “The same **positive power or root**, on two positive numbers, keeps their order.” Retain the instruction to rewrite negative powers first and the existing 5⁻⁴/4⁻⁴ example.
- [must] ¶6–7/9 (3.1–3.2/3.4), “strong on strong” / “If one number is already bigger… above one… gets even bigger” → put **positive factors** into the first spoken rule, not only the later letter case. The latter rule also needs a positive starting number: `−2>−3` but `−2×2=−4<−3`. Keep the positive examples; qualify their rule rather than adding a negative-number method.
- [should] ¶7–9 (3.2–3.4) → split the product comparison into its two paired comparisons and then the conclusion. Current slide 3 item 0 reveals `4×6 vs 3×5: 4>3,6>5:24>15` at once. Mark the corresponding factors steadily so the slogan refers to visible pairs.

## #111 digit-puzzles — findings

NEW: digit concatenation, leading-digit constraint and place-value representation. REMINDERS: place values and substitution.

- [should] ¶3 (2.2), “In that language, two is drawn as A” → A was 4 in the preceding example and becomes 2 without an explicit reset. Begin “Let's choose different digits now: A=2 and B=3.” This keeps the second example without suggesting the same letter changes inside one puzzle.
- [should] ¶8–9 (4.1–4.2) → `27=10×2+7` and `538=100×5+10×3+8` appear together, as do both general formulas. Reveal one place-value example at a time, align its digits with the tens/hundreds being named, then reveal the matching formula. This is the first real letter-puzzle explanation, not a caption-only reminder.
- [should] ¶7 (3.3), “Nobody writes oh eight” → say the mathematical reason directly: “08 has the value 8. It isn't a two-digit number.” The phone-area-code aside is unnecessary for B1 comprehension.

## #112 digit-puzzles-2 — findings

NEW: column technique applied to letters, translating a word puzzle to its equation. REMINDERS: column carries (topic 1), place-value form (part 1), distributive rule and equations.

- [should] ¶6 (3.3), “A plus four is seven, and A is three” → say “7−4=3, so A=3.” Show `A+3+1=7`, then `A+4=7`, then `A=3` beside the **existing correct column/carry figure**. Currently the figure goes straight from the boxed tens column to the answer labels.
- [should] ¶9–11 (4.2–4.3, 5.1) → split `6A=3B; B=2A` into separate reveals. For the second puzzle show `10A+B=7(A+B)` before expanding; the current single item already contains `3A=6B,A=2B`. Say the division by 3 explicitly. Keep all current candidate numbers; don't add another technique.
- [should] ¶11 (5.1), “B is one gives twenty-one, and then forty-two, sixty-three and eighty-four” → say briefly that B=2,3,4 gives those numbers and B=5 would need A=10, not a digit. This explains why the list ends, paralleling ¶10 rather than leaving the student to infer it.

## #126 new-operation — findings

NEW: reading an arbitrary definition and putting the input in every matching position. REMINDERS: arithmetic, squares/cubes and substitution.

- [should] ¶4 (2.3), “a small three means three times” → say “multiply three copies of the number,” to distinguish 2³ from 2×3. The written `2×2×2=8` is right; make the speech equally clear.
- [should] ¶7–8/12–13 (3.3–3.4, 4.3–4.4) → the SLOT pictures correctly link inputs to all positions; keep them. Split their calculation tails, e.g. `5²=25`, `3×5=15`, then `25−15=10`. The current SLOT result layer shows the complete `25−15=10` without those first two calculations, and the second example is a single finished chain. No need to invent more examples.

## #127 new-operation-2 — findings

NEW: an entire expression as input and nested operations. REMINDERS: negative-base brackets, expansion and operation order.

- [must] ¶7 (3.1), “The new operation comes first, before multiplying, dividing and powers. Only brackets come before it” → not a safe general precedence rule. In `◆(3²)`, the power **inside the input** comes first. Say “First work out the entire input inside the operation's brackets. Apply its definition. Then continue with the operations outside.” This preserves the intended distinction in ¶8–10 and avoids teaching a misleading extra BODMAS rule. Correct the matching board/recap captions too.
- [should] ¶6 (2.5), “Together, that's x squared plus seven x plus ten” → explicitly say `4x+3x=7x` and `4+6=10`; show those two collections rather than one already-completed expansion line. This is a short algebra reminder, not a new binomial lesson.
- [should] ¶14 (4.4) → retain the good CHAIN treatment of `◆(◆(2))` and give the two-input star example the same visible handoff: `(1★2)★3 → 7★3`. Currently it writes `1★2=7` then `7★3=30` on separate lines without showing the inner expression replaced in the original outer call.

## #128 new-operation-3 — findings

NEW: underdetermined definitions, swap-order counterexamples, solving an unknown input. REMINDERS: definition/substitution and ordinary equations.

- [should] ¶6/8/10–11 (3.1/3.3/4.1–4.2) → after changing slides, write the currently relevant definition again: `a★b=3a+b²` for the star examples, `a♡b=5(a+b)` when returning to the heart. These definitions were on earlier parts/slides and disappear; the student should not solve from memory. Reveal the corresponding substituted equation before its result.
- [should] ¶10–11 (4.1–4.2), “three x is nine, so x is three” / “k plus two is seven, and k is five” → name the missing operation and calculation: divide 9 by 3; divide 35 by 5; subtract 2 from 7. Show those existing steps one at a time, not `3x=9,x=3` together.
- [should] ¶8 (3.3), “Write the rule with letters instead” → retain this as one way to explain why a rule always works, but don't imply a formal algebraic proof is always required on the exam. One short reminder can distinguish general reasoning from eliminating the other choices. The not-always counterexample and unequal-input warning are good and should stay.

## #134 operation-patterns — findings

NEW: reversing an operation in reverse order; REMINDERS: substitution and basic equations. The two different rules and wrong-order contrast supply a useful full introduction.

- [should] ¶4–6 (2.3–2.5), “Two times four is eight…” / “Three times five is fifteen…” → show the forward calculation too, not merely “4 in,11 out.” Reveal `4→8→11`, then `11→8→4`, labelling ×2,+3 and −3,÷2. For the second rule, show ×3,−4 then +4,÷3. Preserve the existing rules and examples; this makes “backwards” visible rather than adding content.
- [should] ¶3/6 (2.2/2.5), “the whole bracket… over…” → keep the correctly grouped displays `(y−3)/2` and `(y+4)/3`, but simplify the spoken wording to “Subtract 3, then divide the result by 2.” The current repeated bracket instructions make this harder to read than the actual idea.

## #141 solve-q-549 — findings

NEW: handling an operation in all choices; REMINDERS: squared product, square/root, opposite squares and one counterexample. Choice 3 is correctly the not-always identity.

- [must] ¶5 (1.5), **board** `(5x)²=25x²≠5x²` → false at the allowed value x=0. Match the correct speech: add “for x>0,” with `x=0: 0=0` as a separate optional check, or show only the specific failure `x=1:25≠5`. Do not let the board turn “not always” into “never.”
- [should] ¶2 (1.2), “when… the operation [is] in every choice, skip it” → frame as a time-management option for a calculation-heavy question, not a universal command triggered just by symbols. This very question has a quick x=1 counterexample. Keep the intended exam-prioritisation tip without teaching students to skip easy questions automatically.
- [should] ¶7 (2.1), “Zero… can't show the failure” → avoid selecting x=1 by referring back to **choice 3, already found by method 1**. Start “Let's use 1 because it's easy and nonzero. Zero would make many products vanish.” Then discover the failing choice by the existing checks. This keeps the second method independent.

## #147 solve-q-553 — SKIPPED: recorded during review

It was unrecorded in the starting inventory but acquired a full take before final publication. Per the brief, its pre-recording findings are excluded. Do not edit this recorded script as part of batch A. The frozen evidence remains available for a separately authorised recorded-lesson review; this review makes no judgement about the new take's speech.

## #148 solve-q-554 — findings

NEW: assigning digits to different powers within this operation; REMINDERS: place values and exponent sizes. Choice 4, ◆(124)=25, is correct.

- [should] ¶3 (1.3) → the board names “Method 1 · The math way,” but speech starts directly “The hundreds digit…”. Add the brief natural transition “Let's start with the math way,” not another roadmap. Keep the efficient early stop on 4⁴.
- [should] ¶7–8 (2.1–2.2), “the biggest power… should go to the one” → retain the intuitive method but connect it to the **actual comparisons**. Show why moving 1 to the fourth-power position reduces this sum, not merely that 1 costs nothing; for the remaining pair explicitly compare the change `4³−4²=48` against `2³−2²=4`. Keep each small step visible. Do not present “smallest digit gets largest exponent” as an unqualified general optimisation theorem.
- [should] ¶7–8 (2.1–2.2) → understanding slide currently shows only the slogans “Power 4…smallest digit,1” and “Power 3…2,not4:124,” while the script speaks concrete powers. Write those powers as they are said. The student needs the numerical reason, not a text substitute.

## #149 solve-q-555 — findings

NEW: interpreting the reciprocal operation across the choices; REMINDERS: multiplying inequalities by positive values and reciprocal fractions. Choice 2 is correct.

- [should] ¶4/8 (1.4/3.2), “b over a equals a over b only when a and b are equal” → true under the positive givens, but the weak student has to accept the key elimination without seeing it. Add one easy allowed counterexample, e.g. a=1,b=2 gives 2 versus 1/2. One is enough; no exhaustive checking.
- [should] ¶5–6 (2.1–2.2) → keep the carry-over box already present. Add the original comparison `3/a<3/(a+1)` before `3(a+1)<3a`, then `(a+1)<a`, then `1<0`. Currently the new slide begins after the crucial fraction-to-product step, and its next item compresses the rest. The chosen arithmetic and reasoning can stay.
- [should] ¶7 (3.1) → stop the failing test after a=1 establishes equality rather than strict inequality; the extra a=1/2 repeats an already-settled elimination. If retained as a separate teaching contrast, say what it adds rather than requiring all three values for an ordinary must-be-true check.

## #150 solve-q-556 — findings

NEW: the count-of-prime-factor operation, not digit counting; REMINDERS: prime factorization and a counterexample. Choice 4 is correct; x=1 is an appropriate easy test here and really eliminates all three distractors.

- [must] ¶1 (1.1), **native-rendered question and choices** → the special ⟦ ⟧ symbols appear as missing-glyph boxes in the inspected native frames. The underlying text retains the correct characters; this may be a native font-fallback issue, not a broken browser build. Verify the actual studio and provide working vector/math glyphs or correct fallback in the final renderer **without changing the teacher's font design or the operation notation**. Do not publish a video with broken operation symbols.
- [should] ¶4 (1.4) → the board jumps straight to `(1)1≠0 (2)0≠1 (3)1≠0`. Write the intermediate evaluations being read: `⟦1⟧=0`, `⟦5⟧=1`, `⟦1²⟧=0`, `⟦6⟧=0`, then each choice check separately. Otherwise the student must remember which of several “ones” and “zeros” is the input, output or multiplier.
- [should] ¶7 (2.2) → the third counterexample is not needed after the answer and universal reason. Keep only a contrast that teaches a new reusable distinction, if any; don't require checking the discarded claims again. Preserve the definition's good zero-count non-example.

## #151 algebraic-understanding — findings

NEW: choosing among existing tools; REMINDERS: topic-51 plugging in numbers/answers, topic-4 identities, integers/order.

- [should] ¶3 (2.2), “tools that open your head” / “Try numbers first, because they're fast and safe” → use “help us find a way to solve the question,” and don't turn the overview into a numbers-first command for every question. “Choose an easy test when the givens allow it” preserves the strategy; the very next formula example is solved immediately from the givens.
- [should] ¶4–6 (3.1–3.3) → write the **claim** `a²>a?` along with `a>0` before showing the tests; the board currently gives the evaluated inequalities but never the original claim. At the switch to a<0 label this “if the given were different,” so the old positive and new negative conditions aren't seen as simultaneous givens.
- [should] ¶7 (4.1) → the script says the choices are 2,3,4,6, but the board only gives the equation and the first two substitutions. Put the stated choice list on screen before testing. Don't add checks of 4 and 6 once 3 fits; this is a find-x answer-choice question, not an identity/must question.

## #152 solve-q-r26-t20-01 — findings

NEW: applying adaptive tests to this combined inequality; REMINDERS: whole-number versus fractional positive cases, difference of squares. The easy 3,2 trial then 1/2,1/4 trial is exactly the desired strategy. Keep it.

- [should] ¶4/7 (1.4/2.2) → the board groups three successful checks in one item, then two failing checks in one item. Split by choice and keep a simple live status: 4 out after the first pair; 1 and 2 crossed as each fails in the second pair. The “So far: (4) out” carry-over is good; preserve it.
- [should] ¶9–10 (3.1–3.2) → separately reveal `x−y>0`, then `x+y>0`, then their product positive, then `x²>y²`. These are short reminders, not new concepts; the final board currently stops at `x²−y²>0` and relies on the student to translate back to the desired choice.

## #153 solve-q-r26-t20-02 — findings

NEW: using this comparison across expressions; REMINDERS: fractional negative powers/reciprocals and ordering negatives.

- [should] ¶2 (1.2), “one easy number can decide” → state the exam premise once: one listed expression is guaranteed to be smallest throughout the given range. If another choice is smaller at our allowed test, a candidate cannot be that answer. The current reasoning is valid for the intended single-answer question; don't imply a single sample proves arbitrary comparisons generally.
- [should] ¶3–4 (1.3–1.4) → board gives bare results `−1/8,−1/2,−1/4,−2` before the number-line comparison. Show the substitutions at their clauses, especially `−x²=−(−1/2)²=−1/4`, where brackets are the actual trap. Keep the correctly grouped prompter.
- [should] ¶7–8 (2.1–2.2) → on the understanding slide add the symbolic ranges `−1<x³<0`, `−1<−x²<0`, `1/x<−1`, one at a time. The existing band labelled “(1),(2),(3)” is helpful but cannot replace the mathematical statements.

## #154 solve-q-580 — findings

NEW: translating the story into how a formula changes; REMINDERS: positive products, fractions and exponent growth. The early stop on choice 2 is correct; retain the clearly announced teaching-only look at choice 3.

- [should] ¶2 (1.2), “when one letter grows” → explicitly hold the other two fixed. “We change only C and keep S and M the same,” then the analogous checks. This one condition prevents students changing everything at once; no extra solving method needed.
- [should] ¶5–6 (2.1–2.2) → replace the text-only “bigger top → bigger…” board with the actual expression `C^S/M`, focusing C, then S, then M at the words. Keep the fixed-other-quantities condition visible. A brief existing-tool reminder is enough; don't re-teach powers or fractions here.
- [should] ¶3–4 (1.3–1.4) → name the existing method naturally as “Let's solve this by understanding.” The current “Check each letter” title can be a specific under Understanding; no extra method or roadmap is needed.

## #155 solve-q-577 — findings

NEW: finding a maximum by the integer gaps; REMINDERS: strict integer inequalities and testing choices. All three methods reach the correct choice 4 and should be kept.

- [should] ¶6 (1.6), “a plus b… minus a minus c” → the **display** is correctly grouped, but the speech can sound like `(a+b)−a−c`. Say “Start with a+b. To get b+c, replace a with the smaller number c. That reduces the sum by a−c.” Keep `(a+b)−(a−c)` written alongside. This clarifies the same method, not a new one.
- [should] ¶8 (2.2), “b can only be six” → say “b can be **at most** 6” for a=9. Smaller integers are also permitted. To establish the maximum independently, briefly explain that b≥8 would force a≥9 and a+b≥17; one unsuccessful larger-a example alone is not a proof of the maximum. The same simple bound already appears in method 3.
- [should] ¶9 (3.1), “c is smaller than b, so b has to be at least eight” → explain the jump: “If b were 7 or less, c would be 6 or less. Their sum would be at most 13.” Then show b≥8, a≥9, a+b≥17 one clause at a time instead of the current all-in-one item.

## #156 solve-q-578 — findings

NEW: tracking a scaling factor through this equation; REMINDERS: power-of-power/product rules. b=y=1 is allowed and is an appropriately easy test; don't enforce different values where the equation requires equality.

- [should] ¶5/8 (1.5/2.3) → preserve the good spoken explanation that `(5³)²=5⁶`, but write this missing comparison on the board **before** y=125/k=125. Keep old y=1 visible and show `new y/old y=125/1=125` to distinguish the new value from the requested multiplying factor.
- [should] ¶7 (2.2) → show the cancellation `k²b³=25³b³`, then divide by b³>0, rather than jumping directly from `k²y²=25³b³` to `k²=25³`. No new algebra technique; just display the equality being used.
- [should] ¶9 (2.4), “Some students see this in their head” → if the extra identity is retained, introduce it as another way to recognise the square and reveal its small steps on a main board line. The current tiny side caption compresses `25³=25²·5²=(25·5)²=125²`. Don't imply the weak student should already see it instantly.

## #157 solve-q-579 — findings

NEW: recognising this equation as a right triangle; REMINDERS: common denominators (2), Pythagoras/triangle inequalities (31), allowed counterexamples. Correct choice 3; doubling 3,4,5 is a natural second case, not hindsight magic.

- [should] ¶3–4/5 (1.3–1.4, 2.1) → show `p/q=p²/(pq)` and `q/p=q²/(pq)` separately before their sum. Carry **r²=p²+q²** into the first frame of the plug-in slide. Currently that slide clears the simplification and starts with a method title, then only the triple's numeric check.
- [should] ¶8–10 (3.1–3.3) → carry the same equation into the insight slide, then show the triangle. Keep p,q on the legs and r on the hypotenuse as currently drawn. Mark each relevant side steadily at the corresponding comparison; don't ask the student to remember why a triangle appeared after the board cleared.
- [should] ¶11 (3.4) → the 5-versus-10 comparison adds no new result after ¶6–7. Keep the concise closing on the already-established counterexample rather than retelling the whole test. Do not remove the triangle method, which explains the other claims.

## #158 r26-t20-counting — findings

NEW: pigeonhole reasoning and its remainder application. REMINDERS: inclusive integer counts/gaps (the current consecutive-sums lesson already teaches this), remainders (15).

- [must] ¶2–4 (2.1–2.3), “From a to b… b minus a plus one” → state **a and b are integers with a≤b** for the inclusive formula, and **a<b** for the strictly-between formula. The same captions lack these conditions. Otherwise a student can apply them to fractional endpoints or get −1 for identical excluded endpoints. Keep the reminder brief; do not introduce floor/ceiling notation.
- [should] ¶9 (3.4), “two numbers with the same remainder have a difference that divides by twelve” → give the missing reason with the current example: `17=12+5`, `41=36+5`; subtracting removes the same extra 5, leaving `36−12=24`. This teaches the useful new connection rather than asserting it from one example. Show each step.
- [should] ¶6–8 (3.1–3.3) → text-only “13 people,12 months” is much less visible than the idea. Use three simple boxes and four dots for the first example, with the fourth dot sharing a box; for remainder use labelled boxes 0…11. This is a supporting illustration of the method already taught, not extra curriculum. Keep the second example and explain why the boxes are remainder values.

## #159 solve-q-r26-t20-03 — findings

NEW: no new mathematical tool; REMINDERS: counting step-2 lists and pairing odds/evens, both taught earlier. Script reasoning is clear and the answer 30 / choice 2 is correct.

- [should] ¶4–5 (1.4–1.5) → put the warning about counting **gaps versus numbers** at the moment before adding 1, not after announcing the answer. Reveal `79−21=58`, `58÷2=29 gaps`, then `29+1=30 numbers`; the current item reveals the combined calculation/result in one step.
- [should] ¶6–7 (2.1–2.2) → show the first two pairs `(21,22),(23,24),…,(79,80)` when explaining why exactly half are odd. Keep the existing 21-to-80 trick and explain that the included 80 is even, so it adds no odd number to the original question.

## #160 solve-q-r26-t20-04 — findings

NEW: applying the guarantee/worst-case idea to a draw; REMINDERS: pigeonhole from #158. The three-distinct first draws establish the lower bound, and the fourth draw establishes sufficiency. Answer 4 / choice 4 is correct.

- [should] ¶3–5 (1.3–1.4, 2.1) → the board only says “red,blue,green” then “4th sock → a pair.” Show three individually labelled/color-distinguished sock marks, then a fourth matching one of them; retain the labels for color-blind readability. Reuse that picture as the three boxes in method 2. This makes the same argument visible without changing its speech or adding a method.
- [should] ¶6 (2.2), “because every color has more than one sock” → the relevant reason is that **only three colors are possible**, and three distinct first socks are available. “The exact amounts don't matter here. There are three possible colors.” Do not suggest each color needs at least two socks for the pigeonhole guarantee itself.

## Handoff / acceptance

Batch A review is complete for the **29 still-unrecorded lessons**, with #147 skipped because it was recorded during review. This is **not** a declaration that all lessons are ready to record. Claude should address the must findings, make the specific clarity/visual improvements that help, rebuild, and mark each reviewed lesson with its resolved status. Don't add new rules or examples merely to increase length; earlier-topic reminders must stay short. Scripts with only visual findings may be recorded unchanged, but their final videos still need the visual fixes.

The existing source methods were retained throughout this review. This was not a fresh line-by-line audit of all original Hebrew subtitles, nor a final recorded-audio review. No recorded lesson was rewritten and no video was marked rendered by this job.
