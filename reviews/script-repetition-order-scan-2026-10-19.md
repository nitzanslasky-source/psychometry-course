# Script repetition / actual study-plan order — 19 October 2026

Requested by Nitzan: scan for teaching an already-learned idea from scratch. **Findings only; no script, prompter, visual, recording or video changes.** Recorded lessons are protected. No new rereads requested by this report.

## Scope and evidence

- Screened all **482 readable lesson/summary JSON scripts** in current `studio-build/ai_scripts`; `_voice.json` is configuration, not a lesson. Among them, 383 are in the current Reading Studio. At scan time, 137 of those had no saved WAV take; recording status is changing during the day.
- Screening used rule/formula/definition/prerequisite phrases and repeated passages, followed by targeted reading of candidate lessons and their actual earlier teaching. This is a **repetition-focused scan**, not a claim that every sentence received another full mathematical/visual acceptance review.
- Checked `src/lib/planData.ts` ORDER, current hybrid `window.COURSE.flow` and built spoken beats; used current canonical AI scripts for findings. Did not infer learning order from Reading Studio lesson numbers or topic numbers.
- Evidence/snapshot: Codex workspace `work/repetition-order-scan-2026-10-19/inventory.json` (script hashes, paragraphs, topic, displayed number and recorded status); reproducible read-only screening helper `scan.py`.
- No video rendering or recording changes are authorized by this diagnostic request. Recheck latest recordings before any later approved source edits.

## Important correction to my previous review

**I made a prerequisite-mapping error in batch C.** `reviews/batch-C.md` incorrectly said the multiplication identities belong to topic 10, after topic 32, and requested full inline teaching in `solve-geo32-g062` and `solve-q-r26-t32-07`.

The current real sequence starts **1 → 30 → 2 → 4 → 31 → 6 → 8 → 32 → 9 → 10 → 33 → 51**. Topic **4**, not topic 10, contains mandatory `r26-t04-formulas` in flow section `expression-foundation`:

- Beat 2 fully teaches `(a+b)²=a²+2ab+b²`, including the missing-middle-term numerical trap.
- Beat 3 teaches the minus version.
- Beats 5–7 teach `(a−b)(a+b)=a²−b²`, numerical examples and reverse recognition.
- Beats 9–10 show obtaining values without finding the individual unknowns.

Thus both geometry identities are **REMINDERS**, not new tools. This scan supersedes the prerequisite/extra-teaching recommendations in batch-C.md under old #234 / current #294 and old #247 / current #307. Other mathematical, layout and clause-timing findings in that review are unaffected. Preserve the historical report; do not apply its mistaken prerequisite findings to future scripts.

## Strong recommendations — already recorded (do NOT rewrite)

### #294 `solve-geo32-g062` — difference of squares

- **should, ¶10–14 (2.4, 3.1–3.4):** “Why does that work? Multiply out…” followed by two separate numerical checks re-teaches topic 4. The kite question needs recognition/application, not the expansion proof again.
- On a future approved revision, retain: “Using the difference-of-squares formula, `17²−15²=(17−15)(17+15)`.” Then keep the actual `2×32=64`, `AO=8`, whole-kite lengths/area, and all original methods. A short square-of-a-difference trap is enough; do not replace the triple shortcut with compulsory calculation.
- ¶4–6 also revisit the kite definition and several properties. In a later revision, use the relevant main-diagonal properties directly; preserve which diagonal bisects which and the warning that `AO` need not equal `OC`. Do not remove the reason the small triangle is right-angled.
- **Recorded today. Leave existing script/take unchanged.** This is not a mathematical error and does not justify asking Nitzan to rerecord. Any eventual cut would need separate approval and matched visual timing.

### #307 `solve-q-r26-t32-07` — square of a sum

- **should, ¶5–10 (2.1–2.6):** full four-product derivation, two checks and the missing-middle-term trap repeat `r26-t04-formulas`.
- Future revision: “Using the formula we learned, `(a+b)²=a²+2ab+b²`. We know the sum and the diagonal, so we can use it to find `ab`.” Then retain the specific substitution `17²=169+2ab`, arithmetic, `ab=60`, the `2ab` versus area trap, and the separate 5–12–13 method.
- **Recorded today. Do not change speech or require a new take for repetition alone.** Keep all useful methods and the application explanation.

## Strong recommendations — unrecorded at scan time

### #252 `geo-023` — optional proof of Pythagoras

- **should, ¶10 (5.3):** four-product expansion repeats topic 4. Replace only the algebra aside with a short reference to the known identity and its result. The actual rearrangement/area proof is new and is the explicit purpose of this OPTIONAL lesson; keep it.
- **must, same paragraph:** “You can come back to it after the lesson on algebraic identities” misstates the actual schedule. That lesson has already occurred. Suggested direction: “If you need a reminder of the expansion, revisit the multiplication formulas in the expressions fundamentals topic.”

### #329 `solve-geo33-g090` — recognise a right triangle from three sides

- **must, ¶9 (2.4):** “This is new. Until now…” is false in the current curriculum. Earlier `solve-q-r26-t31-03` ¶2–5 explicitly teaches comparing the longest side squared with the other two squares and says equality means a right triangle.
- **should, ¶9–10 (2.4–2.5):** remove the first-time introduction and unrelated 5–12–13 practice example. Keep a brief reference to the known test and the actual 12–35–37 check in ¶6–8. For example: “The sides satisfy the Pythagorean test, so the triangle is right-angled.”
- Keep the specific new circle application: existence/uniqueness of the circumcircle where needed, why the hypotenuse is its diameter, circumference calculation and radius/diameter traps. Do not shorten those merely because Pythagoras is known.

### #375 `solve-pt-q17` — estimate √2

- **should, ¶9–10 (2.2–2.3):** the full `1²`, `2²`, `1.5²` bound-building sequence is repeated almost verbatim from **`pt51-estimation` ¶13–14**, only three lesson positions earlier. Use “From the estimate we just learned, `1<√2<1.5`,” then apply those bounds to the choices.
- Keep ¶11–16: explaining the actual fraction/choice bounds is the point of THIS example, not redundant root teaching.
- Do **not** automatically delete the conjugate explanation in ¶3–4. Earlier topic-9 material contains a worked partner example, but its explanation is brief. Naming the conjugate plus showing how the actual denominator becomes 2 is a useful application reminder; the generic “same top and bottom preserves value” sentence is a possible small trim, not a must-fix.

### #380 `solve-pt-q21` — investment percentages

- **should, ¶2 (1.2):** “we haven't learned percents yet, so first, what does a percent mean?” starts over after `solve-pt-q08` taught 50%/10%, `solve-pt-q14` explicitly defined percent/out-of-100, and `solve-pt-q19` used it for concentration. The FORMAL percentages topic is later, but the minimal meaning has already been introduced inline.
- Use a short contextual reminder: “Eight percent is eight for every hundred invested. Here, only half the total money earns that rate.”
- **Keep ¶3–9:** the difference between return on one half and return on the whole investment is a new application. The 100-shekel illustration helps establish it; do not remove it as if it were just another definition of percent. Keep all original approaches and the misconception trap.

## Lower-priority checks, not mandatory deletions

- **#317 `geo-079`, ¶3–9 / ¶15–18:** circumference and π were already introduced in `solve-q-r26-t33-01` ¶2–4, including diameter/radius examples. Frame this as “We used π earlier; now let's see it on the diagram,” rather than pretending π is unknown. The unrolled-circle visual is a genuinely different explanation, so it can be kept as a short reinforcement. **Circle AREA and its slice demonstration are new; retain full teaching.** Do not cut the whole mixed lesson.
- **#369 `solve-pt-q14`, ¶3; #377 `solve-pt-q19`, ¶2; #382 `solve-pt-q23`, ¶3:** avoid repeatedly opening with “First, what is a percent?” / “we haven't learned percents yet.” Use the particular reminder needed (original price, concentration, 10%=one tenth). These are already short and mostly useful; do not remove their task-specific calculations or demand a full rewrite.

## What should stay — examples checked

- `solve-pt-q03` ¶3 and `solve-pt-q10` ¶7 already give brief formula reminders followed by actual application. They do not derive the identity again. Keep.
- `solve-geo33-g101` ¶8 names the known identity and expands the actual `(r+5)²`. This is application, not a fresh example set. Keep enough intermediate work to show where `10r` comes from.
- `solve-q-r26-t33-05` expands the actual `(R+r)²` and `(R−r)²` to derive a NEW common-tangent formula. Do not remove the derivation just because identities are known.
- `solve-geo33-g078` ¶9 introduces the reusable two-tangent/central-angle supplementary relation, not a full repeat of the two tangent rules. Earlier `geo-077` teaches perpendicular radii/equal tangent segments/kite symmetry, not this numeric-angle relation. Keep.
- `solve-wp22-g029` teaches the ratio TABLE as a tool. `solve-wp22-g030` adds the triangle-value method/cross-multiplication. New presentation/tool instruction is not automatically redundant because students can already multiply or divide.
- `wp-034` adds ratio orientation, absolute-amount ambiguity, common units and reversed price ratios beyond the brief phrase translation in `wp-027-3`. Keep substantive new teaching; ordinary fraction arithmetic needs only brief reminders.
- `wp-016` distinguishes maximizing one value, minimizing the largest, and minimizing one value. Earlier `wp-006` only previews minimum/maximum, and `solve-wp21-g007` maximizes the NUMBER of recipients. Those are not identical tasks; do not blanket-shorten the new distinctions.
- `solve-pt-q04` cylinder volume, `solve-pt-q05` probability, and initial percentage introductions occur BEFORE formal topics 35/29/23 respectively. Keep the small inline explanations needed there. Later percentage reminders should shrink, not disappear.
- Dedicated summaries are intentionally repetitive. Do not treat every formula or example in a recap as accidental reteaching.

## Editing policy for Claude / later jobs

1. Mark each reusable idea NEW, REMINDER or NEW APPLICATION using actual earlier mandatory teaching, not topic number or an optional lesson alone.
2. Known rule: name it, show the relevant formula, give one short connection to THIS question, then calculate. Usually one or two sentences; no new general proof or unrelated two-example set.
3. Keep what is new: choosing the rule, matching quantities, new conditions, a new construction or misconception. Do not turn clear applications into bare answers.
4. Preserve exam terminology, all original methods and the teacher's easy-number approach. No hindsight-picked numbers.
5. Do not rewrite recorded speech. The two recorded identity cases above are a pacing issue, not a factual correction; no automatic reread flags.
6. Before approved edits to an unrecorded case, check for new takes, preserve paragraph identity where possible, and update actual writing/cue timing if narration is shortened. This report does not mean the visual changes or edits have been made.
