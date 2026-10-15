# Batch A: fixes applied (Claude, 15 Oct 2026, 22:30)

Source review: `reviews/batch-A.md` (Codex, 84 findings: 14 must, 70 should, 0 nice).

## Result

- **82 fixed**, including all 14 must findings. 2 of these are only partly fixed: the board part is done, and the spoken part needs Nitzan (#148 and #149 below).
- **2 skipped**: spoken text in lessons she recorded during this job.
- **0 parked.**

Recording status was checked before editing each lesson and again before publishing.
- **#148 solve-q-554** was recorded at 21:51, before the edits.
- **#149 solve-q-555** was recorded at 22:02 and 22:05, from the old 21:32 Reading Studio page. Its spoken edits were reverted, so its speech is byte-identical to what she read.
- Both lessons got board-only fixes. They now show as "Send to Codex".

Canonical sources edited:
- `math_patches/_ai_vis_t15.py` … `_ai_vis_t20.py`. The camera-part closings are fixed inside the specs after `CP.split`.
- `_codex_script_clarity_20261012.json`: 5 t16-04 entries were moved into the spec (details in #83 below).
- `_codex_reading_display_20261012.json`: scope_replacements for the changed paragraphs.
- `slide_style.py`: a glyph fallback for ⟦ ⟧.

Not edited: `_method_visuals.py`, `_her_reading_20261015.py` and `_camera_parts.py`.

Everything kept: every method, her content, the fonts and design, the method vocabulary (`check_vocab` passes), W1–W16, V3/V4 and R29–R36. Slide and paragraph counts are unchanged except in #83 (2 → 3 slides).

## Per lesson

Status words: **fixed**; **partly fixed** (board done, spoken part needs her); **skipped** (with the reason).

### #46 divisibility (camera, part 1)
- [should] ¶2 538÷2: **fixed**. It is now 500÷2=250, 38÷2=19, 250+19=269, each written at its clause.
- [should] ¶6/8 digit sums: **fixed**. The board shows 9+4=13, then 13+2=15, then the verdict, at her words.
- [should] ¶12 test for 8: **fixed**. Added the contrast 7,241: 240=30·8, so 241=30·8+1.
- [should] ¶3–5 example rows: **fixed**. Each example has its own reveal, with its last digit highlighted.
- Also: "Okay." dropped from the part closings (all 4 parts), and the "By 4 and 8" right column moved below the camera bubble.

### #47 divisibility-2
- [must] ¶5–6 "share no factor": **fixed**. It now says "must not share a divisor bigger than one", before the product rule. 18 stays as the counterexample, with 6=2·3 on the board.
- [must] ¶10 rule for 11: **fixed**. It now says "the result divides by eleven, and zero counts too". The general rule is stated.
- [should] ¶8–10 three ways for 11: **fixed**. They are labelled Way 1, Way 2 and Longer numbers, and every calculation is its own line (41−8=33 apart from 42−7=35).

### #48 divisibility-3
- [must] ¶7 "5 ÷ 8 = 0": **fixed**. It now says "the quotient is zero, and the remainder is five", and the board shows 5=8·0+5. The prompter shows no false equation.
- [should] ¶11–13 remainders 14÷9 / 14÷3: **fixed**. The board shows 14=9·1+5, then 5,432÷9: remainder 5. The by-3 case follows separately.
- [should] ¶8–9 remainder cycle: **fixed**. It is now a two-row number/remainder table, revealed one full pair at a time.

### #49 divisibility-4
- [must] ¶8 "it can leave anything": **fixed**. It now says "doesn't tell us one fixed remainder by six. Our examples gave two and four." The script checked that (8k+2) leaves 0, 2 or 4.
- [should] ¶2–4 "tag": **fixed**. The lesson now goes 7=4·1+3, then 11=4·2+3, then 4k+3, with "k tells us how many complete groups of four there are". The k=0 reminder is kept.
- [should] ¶8 "drop out": **fixed**. It now says "Fifteen k leaves no remainder when divided by five, so only the extra four matters."
- [should] ¶10 rule for 11: **fixed**. It now says "in a three-digit number".

### #67 whole-numbers
- [must] ¶17 "surely positive": **fixed**. The new wording: if x isn't zero, x² and |x| are positive; if x is zero, both are zero; in a product or quotient a positive piece doesn't change the sign. The caption was corrected too.
- [should] ¶16 "nine is farther": **fixed**. It now says "negative nine is farther from zero", plus −4+4=0.
- [should] combined example rows: **fixed**. Every example now appears at its own clause.

### #83 solve-q-r26-t16-04
- [must] ¶7 prompter "135 less" / ¶5 "630 + 1 more 63": **fixed**. The second test now uses only the last digit (7·9=63 ends in 3, and ×11 still ends in 3). 693, 350 and 315 are no longer calculated, so both bad displays are gone.
- [should] ¶5–7 avoidable work: **fixed**. The warning about groups that contain a 5 now comes before the second test, and nothing is calculated after the answer. Both methods are kept.
- [should] ¶8–9 why one in three odds: **fixed**. The board shows the row 1, 3, 5, …, 15 with 3, 9 and 15 highlighted.
- Layout: Method 1 now continues on a second slide (2 → 3 slides), with a "So far: (1) out, (2)–(4) left" box.
- Overlay reconciliation: the clarity-overlay entries for (slide 1, ¶5–7) and (slide 2, ¶1–2) were moved into the spec, because the new board items shift their cue indices. Entries ¶2–4 are untouched.

### #92 number-line (camera, part 1)
- [must] ¶6 x=1 missing: **fixed**. It now says "between zero and one, exactly one, or above one".
- [should] ¶4 "both move the same way": **fixed**. It now says "Times two makes both bigger. Times one half makes both smaller", with one board line for each.
- [should] ¶9–10 mirror: **fixed**. The ×1/5 inward arrows (15→3 and −15→−3) and "−3 > −15" are added on the same axis, at the words.

### #93 number-line-2
- [must] ¶8 "11/10 is not a fraction": **fixed**. It now says "Eleven tenths is bigger than one, because eleven is bigger than ten…". ¶4–5 now say "a fraction between zero and one".
- [should] ¶7–10 hierarchy rule: **fixed**. The rule now covers the four ranges and gives the reason ("keeps a positive number on its side of one"). The odd-only rule for negatives comes before the example.
- [should] paired calculations: **fixed**. Each case is split into its own reveal.

### #94 number-line-3
- [must] ¶2 "the same operation": **fixed**. It now says "The same positive power or root, on two positive numbers, keeps their order."
- [must] ¶6–7/9 strong on strong: **fixed**. It now says "positive factors" and "If one positive number is already bigger".
- [should] ¶7–9 product comparison: **fixed**. The board shows 4·6 vs 3·5, then 4>3, then 6>5, then 24>15.

### #111 digit-puzzles (camera, part 1)
- [should] ¶3 A changes value: **fixed**. It now says "Let's choose different digits now."
- [should] ¶8–9 place-value pairs: **fixed**. 27, 538, AB and ABC each get their own reveal.
- [should] ¶7 "oh eight": **fixed**. It now says "Zero eight has the value eight. It isn't a two-digit number." The area-code aside is gone.

### #112 digit-puzzles-2
- [should] ¶6 A+4=7: **fixed**. It now says "Seven minus four is three". The board shows A+3+1=7, then A+4=7, then 7−4=3: A=3.
- [should] ¶9–11 split equations: **fixed**. 10A+B=7(A+B) is shown before expanding, and "÷3" is said and written.
- [should] ¶11 why the list ends: **fixed**. It now says B=2, 3 and 4 give the other numbers, and B=5 would need A=10.

### #126 new-operation (camera, part 1)
- [should] ¶4 "a small three": **fixed**. It now says "multiply three copies of the number".
- [should] SLOT tails: **fixed**. 5²=25, 3·5=15 and 25−15=10 each appear at their clause, as do 2♥6 → 5·8 → 40 and ◆(2).

### #127 new-operation-2
- [must] ¶7 precedence rule: **fixed**. It now says "First, work out everything inside the operation's own brackets. Then use the definition… Only then do the rest." The caption, the part-3 recap and the slide title ("Inside first, then the definition") were corrected too.
- [should] ¶6 expansion: **fixed**. 4x+3x=7x and 4+6=10 are said and shown.
- [should] ¶14 star handoff: **fixed**. The board shows (1★2)★3=7★3.

### #128 new-operation-3
- [should] definitions rewritten: **fixed**. a★b=3a+b² and a♥b=5(a+b) are shown again on the slides that use them.
- [should] ¶10–11 missing operations: **fixed**. It now says "Divide nine by three…", "Divide thirty-five by five…" and "Subtract two from seven…", each written separately.
- [should] ¶8 proof vs exam: **fixed**. It now says "One way is to write the rule with letters", plus "ruling out the other three choices also works".

### #134 operation-patterns
- [should] ¶4–6 forward and back: **fixed**. The board shows 4 →×2 8 →+3 11, then 11 →−3 8 →÷2 4. The second rule is shown the same way.
- [should] ¶3/6 bracket wording: **fixed**. It now says "first we subtract three from y. Then we divide the result by two." The prompter shows (y − 3)/2 and (y + 4)/3.

### #141 solve-q-549
- [must] ¶5 board (5x)²≠5x²: **fixed**. It now reads "for x>0".
- [should] ¶2 "skip it": **fixed**. It is now framed as a time option.
- [should] ¶7 choosing x=1: **fixed**. It now says "because it's easy and it's not zero". It no longer refers back to Method 1.

### #148 solve-q-554 — RECORDED 21:51 (board-only changes)
- [should] ¶3 "Let's start with the math way": **skipped**, because it is spoken. → teacher
- [should] ¶7–8 connect to the actual comparisons: **partly fixed**. The powers she says are written at her words, and "2, not 4: 124" no longer appears early. The spoken comparison is **skipped**. → teacher
- [should] ¶7–8 write the powers as said: **fixed**.

### #149 solve-q-555 — RECORDED 22:02/22:05 from the old page (spoken edits reverted, board-only)
- [should] ¶4/8 counterexample a=1, b=2: **skipped**, because it is spoken. → teacher
- [should] ¶5–6 fraction-to-product steps: **fixed**. The board shows 3/a<3/(a+1), then 3(a+1)<3a, then a+1<a, then 1<0, at her words.
- [should] ¶7 extra a=½ test: **partly fixed**. a=2 ✓, a=1 ✗ and a=½ ✗ are now each at their own clause. Cutting the spoken a=½ is **skipped**. → teacher

### #150 solve-q-556
- [must] ¶1 ⟦ ⟧ missing glyphs: **fixed** in the canonical renderer (`slide_style.py` `svgText`). Only ⟦ and ⟧ get a tspan with STIX Two Math / STIXGeneral / Apple Symbols. Her font and the notation are unchanged.
  - Checked in the built studio frames: the question, the choices and the board lines draw correctly.
  - **Codex: please confirm in your renderer.**
- [should] ¶4 intermediate evaluations: **fixed**. ⟦1⟧=0, ⟦5⟧=1, ⟦1²⟧=0 and the rest are written, one choice per line.
- [should] ¶7 third counterexample: **fixed**. It was cut, which also removed "cubed".

### #151 algebraic-understanding
- [should] ¶3 "open your head" / numbers first: **fixed**. It now says "help you find a way" and "When the givens allow it, an easy number is often a fast first test."
- [should] ¶4–6 the claim: **fixed**. "Given a>0. Always a²>a?" is written first. The a<0 case is labelled "If the given were different".
- [should] ¶7 choices: **fixed**. "Choices: 2, 3, 4, 6" is on the board. 4 and 6 are not checked.

### #152 solve-q-r26-t20-01
- [should] ¶4/7 per-choice status: **fixed**. Each choice gets its own line with ✓ or ✗, and the crosses come as each choice fails. The "So far" box is kept.
- [should] ¶9–10: **fixed**. The board shows x−y>0, then x+y>0, then the product >0, then x²>y², each at its clause.

### #153 solve-q-r26-t20-02
- [should] ¶2 exam premise: **fixed**. The premise is said once.
- [should] ¶3–4 substitutions: **fixed**. They are written at their clauses, including −x²=−(−½)²=−1/4. The prompter now shows (−½)³ = (−½) × (−½) × (−½).
- [should] ¶7–8 ranges: **fixed**. −1<x³<0, then −1<−x²<0, then 1/x<−1, one at a time.

### #154 solve-q-580
- [should] ¶2 hold the others fixed: **fixed**. It now says "we change only that letter and keep the other two the same."
- [should] ¶5–6 the expression: **fixed**. C^S/M is written, and C, S and M are each focused at the words.
- [should] ¶3–4 method name: **fixed**. It now opens "Let's solve it by understanding". The title is "Understanding: check each letter".

### #155 solve-q-577
- [should] ¶6 a+b → b+c: **fixed**. It now says "replace a with the smaller number c. That takes away a minus c…"
- [should] ¶8 "at most six": **fixed**. Added: b≥8 → a≥9 → a+b≥17. A brute-force check confirms the maximum is 13.
- [should] ¶9 jump to b≥8: **fixed**. It now says "If b were seven or less… at most thirteen", and each clause is written.

### #156 solve-q-578
- [should] ¶5/8 (5³)²=5⁶ before 125: **fixed**. The board shows new y ÷ old y = 125÷1 = 125.
- [should] ¶7 cancellation: **fixed**. The board shows k²b³=25³b³, then ÷b³, with b>0 said.
- [should] ¶9 extra identity: **fixed**. It is now "There's another way to see…", with its steps on the main board, chunk by chunk.

### #157 solve-q-579
- [should] ¶3–5: **fixed**. p/q and q/p are each written over pq separately. "Given: r²=p²+q²" is carried onto the plug-in slide.
- [should] ¶8–10: **fixed**. The same equation is carried onto the insight slide. The triangle is layered: r is marked at "the longest side", and p and q at "two sides together".
- [should] ¶11 retelling: **fixed**. It was cut, and the closing stays short.

### #158 r26-t20-counting
- [must] ¶2–4 formula conditions: **fixed**. It now says "a and b are whole numbers, and a is at most b", and for the strict case "when a is smaller than b". The captions match, and every example calculation is its own line.
- [should] ¶9 why the difference divides by 12: **fixed**. The board shows 17=12+5 and 41=36+5, so the fives cancel and 41−17=24=2·12.
- [should] ¶6–8 boxes: **fixed**. Three boxes with four dots, then twelve boxes labelled 0–11 ("These twelve remainders are our boxes").

### #159 solve-q-r26-t20-03
- [should] ¶4–5 gaps vs numbers: **fixed**. The warning now comes before the +1. The board shows 79−21=58, then 58÷2=29 gaps, then 29+1=30.
- [should] ¶6–7 pairs: **fixed**. The board shows (21,22), (23,24), …, (79,80), with "Eighty is even".

### #160 solve-q-r26-t20-04
- [should] ¶3–5 the sock picture: **fixed**. Three labelled colour boxes (text labels for colour-blind readers), one sock each, then the 4th sock. Method 2 reuses the picture.
- [should] ¶6 the reason: **fixed**. It now says "Only the number of colors matters, and there are three."

### Shared fixes
1. **Divides vs divisible by:** the captions in the changed lessons are unambiguous.
2. **V4 chunking:** done in the camera parts above.
3. **Formatting must not change the maths:** #83 and the #48 remainder are fixed. The changed paragraphs were checked in the rebuilt page, and registry entries were added (digit-puzzles-2 5.1, number-line-2 4.4, operation-patterns 2.2/2.5, divisibility-2 2.4/2.5/3.4, divisibility-4 2.1, t16-04 3.1, t20-02 1.3/2.1, 578 1.5/2.1/2.3/2.4, counting 2.2/3.3, t20-03 2.1).
4. **Style:** "Okay." was dropped before the goodbyes, "choice number N is our answer" is used, and "cubed" became "to the power of three". This was done in unrecorded lessons only, including the camera-part closings of these lessons.

## Checks (final build, 22:28)
- Spec regeneration (13–20, 30–33, 51) equals `ai_scripts`, with no PROBLEMS. Only the 29 batch lessons' scripts changed. 554 and 555 differ only in cue phrases; their spoken text is identical.
- `ai_check`: no new fails. The only fail is the old solve-q-r26-t22-02 one.
- `math_check 15 16 17 18 19 20 32`: 0 problems, 0 warnings, layout 0, both normally and with `AI_HANDWRITE=all`.
- `svgcheck`: 54,682 slide steps, 0 broken.
- Timing simulation (all 29): 0 problems. The early-answer check found no result shown before it is said; the remaining flags are parser artifacts or results said in the same clause while the pen writes.
- Step frames: every step of every changed lesson was rendered and inspected, and the re-fixed slides were rendered again from the final build. Nothing is under the camera bubble in the camera parts, and nothing is off the board or overlapping.
- The real build, `export_student`, and the Reading Studio rebuilt with all 13 topics. The changed paragraphs' prompter text was verified. The re-read count is the same, 76 → 76, and no recorded lesson's count rose.
- `video_status.py`: Record 190 · Re-read 38 · Send 74 · Done 20 · Check 1.

## READY TO RECORD (Reading Studio numbers, page of 22:28)
#46, #47, #48, #49 (divisibility parts 1–4) · #67 · #83 · #92, #93, #94 · #111, #112 · #126, #127, #128 · #134 · #141 · #150 · #151, #152, #153, #154, #155, #156, #157, #158, #159, #160. That is 27 lessons.

**She must reload the Reading Studio (version "Last updated 22:28") before recording these.** Her open page is from 21:32 and still has the old text.

Recorded and not in the list: #147 (553), #148 (554) and #149 (555).

## For Nitzan (optional re-reads)
- **#148 q-554:**
  - ¶3: add "Let's start with the math way."
  - ¶7–8: say the real comparison aloud. Moving the 1 to the fourth power makes the sum smaller. For the last pair, 4³−4² is 48, against 2³−2² is 4.
- **#149 q-555:**
  - ¶4 and ¶8: add one counterexample. "For example, a is one and b is two. Then b over a is two, but a over b is one half."
  - ¶7: drop "And for a fraction like one half, we get six." The a=1 test already rules the choice out.
