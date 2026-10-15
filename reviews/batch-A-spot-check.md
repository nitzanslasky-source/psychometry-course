# Batch A fixes — independent spot-check, Codex, 15 October 2026

Result: the sampled fixes pass. This is a targeted spot-check, not a second full certification of all 84 findings or of finished video timing.

Read COORDINATION.md and batch-A-fixed.md first. Used the current canonical scripts, actual prompter output, and current hybrid build. No lesson sources, HTML, recordings, holds or render ledger were edited. Local evidence: Codex workspace `work/batch-A-spot-check-2026-10-15/`.

## Requested checks

1. **#150 solve-q-556 — PASS, including native rendering.** Double brackets are visible in the stem, choices and intermediate evaluations. Both methods remain. Rendered all 12 board steps and inspected both contact sheets. The native review adapter needed support for the canonical renderer's new nested font tspans; that adapter change is local only. The fonts/design of the source were not changed by this review. Future video exports must retain this tspan/font-run support; do not reuse the older flat-text adapter unchanged.
2. **#83 solve-q-r26-t16-04 — PASS.** Three slides, both methods retained; remaining overlay entries are the earlier introductory paragraphs, not the moved latter paragraphs. Actual prompter text no longer contains the corrupt “135 less” or “630 + 1 more 63”. The second test uses last digits rather than calculating 693 and subtracting 350. The current build carries “So far: (1) out, (2)–(4) left” onto the continuation slide. All 21 static steps inspected; no cue target visibly points at the wrong board item in the reviewed sequence. Precise word/pen timing still requires a recorded take.
3. **#148 q-554 — board changes PASS; speech preservation PASS.** Effective spoken paragraphs match the original batch A evidence. Powers now appear progressively rather than announcing 124 early. Status at check: Send. Optional spoken improvements in Claude's handoff remain optional; no rerecord request was added by Codex.
4. **#149 q-555 — board changes PASS; do NOT treat the old Send statement as current.** Cross-multiplication now includes the missing intermediate lines, ending in 1 < 0. At this spot-check it is **Re-read**, not Send, and its spoken script differs from the earlier batch A snapshot. COORDINATION.md explicitly says Claude is now making the separately requested rerecord/choice-reading fix. That is concurrent authorised work, not evidence that the earlier board-only fix silently rewrote a recording. Leave the hold/status alone and use the completed new revision/take later.

## Additional risk-based sample

Read full effective speech and prompter output for these five lessons and inspected representative relevant step sheets:

- **#48 divisibility-3:** quotient/remainder distinguished; the board correctly shows 5 = 8·0 + 5, not 5 ÷ 8 = 0. Number/remainder pairs are revealed together.
- **#49 divisibility-4:** the false “anything” remainder claim is removed; examples correctly demonstrate that the remainder by six is not uniquely determined. The letter k is explained with complete groups.
- **#94 number-line-3:** positive-number/positive-power scope is stated; product comparisons require positive factors. Negative exponent example first converts to positive powers of reciprocals.
- **#127 new-operation-2:** evaluates the operation's input first; distinguishes ◆(3)+◆(4) from ◆(3+4). The nested operation's intermediate result is carried into the outer one.
- **#158 counting:** whole-number and endpoint conditions are explicit; remainder boxes 0–11 and the equal-remainder subtraction example are present.

192 static frames generated across nine sampled lessons, zero rendering failures; selected sheets inspected as described above. This is not a claim that all 192 frames or the remaining batch A fixes were independently reinspected. No new blocker found in this sample. Continue with batch B; Claude's currently claimed W17/W18 and q-555 work remains his.
