# Topic 5 (Expressions): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 2551-3661 (source 5 from "ביטויים" to her note
  "after that 20 questions of תרגול עצמי"; all of it read). Line numbers below are file lines. Note: her common-factor
  question appears twice in the file (2685-2757 and again 2759-2831, word for word); it is one video.
- English: topics 1-12 have no reading scripts yet, so the English side is `scratchpad/ext/course/t05.txt` and `q05.txt`,
  the base translation `base-v18.html`, and the current course `~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html`
  (flow order and the two videos that moved to topic 8).
- **Recording status.** Topic 5 is not in `video_status.py` (it covers only the Reading Studio topics). Her older English
  takes exist for `expression-strategy` and her questions `solve-q-125` … `solve-q-138` (in
  `real_exam/added_by_nitzan.json`). `r26-t05-shortcuts`, `r26-t05-power-count`, their five solution videos and the
  summary have none. Topics 1-12 are redone LAST in the plan, so any restore goes into the redo scripts.

**Her structure** (notes at 2551 and 2941): a theory video, then "video, question" four times (basic part), then the
advanced part: 10 question videos, then 20 practice questions. English ids: her basic questions are `q-135`, `q-136`,
`q-137`, `q-138`; her advanced ones are `q-125` … `q-134` in her order.

**Two structural changes.**
1. **q-131 and q-132 moved to topic 8** (Exponent Laws). Both of her questions use powers (negative powers; a⁰ and
   (−1)^a), which her course had not taught yet. In the English study plan topic 8 comes before topic 5, so they now sit
   right after the powers lesson. Both scripts keep every method of hers (checked in the current course).
2. **The flow order changed.** Hers: 135, 136, 137, 138 | 125, 126, 127, 128, 129, 130, 131, 132, 133, 134. English:
   136, 135, 137, 138 | 125, 134, 127, 128, 130, 126, 129, 133. The English puts the easy estimation question (134) second
   and 130 before 126; no content depends on her order.

SAME = same idea and every one of her methods (new numbers only). CHANGED = same idea, different method / example /
place. PARTIAL = part of her content missing. MISSING = no English equivalent.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| T | ביטויים – תאוריה · Expressions theory | 2553-2595 | Exam asks for the value of an expression, often no number, just manipulate (simplify, factor, cancel); **expression = "something = ?", equation = something = something**; **the common mistake: dropping the common denominator in an expression** (a/b + b/a = (a² + b²)/ab, the denominator stays; only in an equation, both sides, may it go); order of operations matters | `expression-strategy` slides 1-3 (x/y + 2y/x) | SAME. English also front-loads ideas she teaches inside her question videos (opposite brackets, the main bar, the repeated bracket, plug-in rules, choosing numbers: slides 5-9), and adds slide 4 (split a sum on top, never the bottom) |
| B1 | 4 / (1 / (½ + ¼)) | 2597-2649 | Work in order: **the main fraction bar is the one level with "= ?"**; deepest layer first: ½ + ¼ = ¾ (½ = two quarters); 1 ÷ ¾ = 4/3; 4 ÷ 4/3 = 4 × ¾; a whole number times a fraction multiplies the numerator → 3. **Nuance: no visual distractors on NITE — when the answer equals a choice number it sits in that slot.** Then a short intro to opposite numbers (differ by the minus, sum 0, = ×(−1)) | `solve-q-135` (6 over 1 over (½ + ⅓) = 5) + `expression-strategy` slides 5-6 | SAME (the visual-distractor tip kept; English adds the three traps; the opposites intro moved to the lesson) |
| B2 | 2 − (a − b)/(b − a) | 2651-2683 | NITE's favourite pattern; plug in 5 and 3 → 2 / −2 = −1; **rule: swapping the order always gives −1, whatever you plug in** ("you could prove it by taking out a minus, but trust me"); 2 − (−1) = 3; visual distractor again | `solve-q-136` (10 − (y − x)/(x − y) = 11) + `expression-strategy` slide 5 (the proof by taking out a minus) | SAME (English adds the condition a ≠ b and the trap 9) |
| B3 | (a + b)(x − 1) + (a + b)(x + 1) | 2685-2757 | **Common factor** a + b out, −1 and +1 cancel → 2x(a + b); then a first taste of **plugging in**: why all 1s are allowed (any numbers are, nothing says they differ, pick the easiest); 4; put the 1s in the choices; **the catch: don't mark the first match, eliminate three** | `solve-q-137` ((m + 2n)(k − 6) + (m + 2n)(k + 6)), Methods 1-2 | SAME |
| B4 | הצבת מספרים · Plugging in: (x + y + z + w)² − (x + y − z − w)² | 2833-2939 | A real exam question; strong students expand it (1-1.5 min); the rest of us plug in: all 1s → 16; choice 2 gives 16 "but you may not mark it"; eliminate three; **if two tie, change one number (W = 2) and test only those**; **a second plug-in (0, 1, 2, 3 → 20) to show it always works**; **when it is allowed: only in an expression, never with two sides**; it is a safety net, **don't overuse it: what you can solve algebraically, solve algebraically** | `solve-q-138` ((p + q + r + s)² − (p − q + r − s)²), Methods 1-2 + `expression-strategy` slides 8-9 | SAME (English adds Method 3, two blocks A and B → 4AB) |
| A1 | 15² − 15 − (14² + 14) | 2943-3035 | Four ways: **just calculate** (know 15² = 225, 14² = 196); **units digit** (ends in 5 − 5 → 0; 6 + 4 → 0; only one choice ends in 0; works only because the choices' units digits all differ); **common factor with plain numbers** (15·14 − 14·15); **understanding without writing** (15 fifteens minus one fifteen = 14 fifteens…) | `solve-q-125` (13² − 13 − (12² + 12)), Methods 1-4 | SAME |
| A2 | Nested brackets with minus signs | 3037-3117 | **When does a minus affect a bracket?** Test 10 − (1) − 1 = 8: a minus AFTER a bracket doesn't touch it, so drop all the brackets; −b + b cancel → a − c − d. **Plug in, smart choice**: not all 1s (the result goes negative; the choices tie); a = 10 (round, bigger), b, c, d = 2, 3, 4 ("b is the second letter"); check the choices are different first; innermost bracket first. **Verdict: here the math way is shorter; plugging in is the default safety net** | `solve-q-126` ({[(w − x) + y] − z + x}; w = 20, x, y, z = 3, 4, 5), Methods 1-2 | SAME (her letter-position memory aid for picking numbers is dropped) |
| A3 | Which equals x² + 9x + 18? | 3119-3190 | "We haven't learned how to factor this; it's not a formula — **the choices help us: open them**"; every choice gives x² and 18, so only the middle term decides; **plug in x = 1**, check the choices differ (38, 30, 28, and 5.5 × 5 "not round — don't calculate it; if the expression comes out not round, that's the answer"); 28 → choice 3; here plugging in is shorter | `solve-q-127` (x² + 15x + 36), Methods 1-2 | SAME (both methods and her "not round, don't calculate" tip kept). **But see the English error below: the script opens with "You know sum and product from Topic 4"** |
| A4 | 3 + \|x\|/x | 3192-3224 | Identical numbers divide to 1, opposites to −1; x positive (5) → 1, x negative (−1) → −1; go through the choices by the sign case; "on the exam this shows up as \|x\| or as (x − y)/(y − x)" | `solve-q-128` (x/\|x\| + 8) | SAME |
| A5 | Two claims: (A + B)/A = 1 + B/A and A/(A + B) = 1 + A/B | 3226-3322 | **Math way 1: work backwards, add the fractions** (1 = A/A → (A + B)/A: true; 1 = B/B → (B + A)/B: not the same → false); **Math way 2: "cancelling" in a sum by splitting the numerator** (only a sum on top splits; with one term on top it can't), with her geometry example **(180 + α)/2 = 90 + α/2**; **plug in** A = 1, B = 2 | `solve-q-129` (Tom: B/(A − B) = B/A − 1, false; Dana: (A − B)/B = A/B − 1, true), Methods 1-3 | SAME (the claims now use minus and the true one is the second; English adds a number check inside Method 1 and uses (180 − α)/2) |
| A6 | (x − y − (y − x))/(x − y) | 3324-3413 | Three math ways: **standard** (the minus hits only the second bracket, collect, factor 2, cancel → 2); **split the top** (1 − (−1) = 2, opposites); **take out a minus** ("two basketballs": x − y plus x − y); **plug in**: not 1 (choices 2x, 2y would tie with 2), x > y to stay positive: 3 and 2; check the choices first | `solve-q-130` ((3(m − n) − (n − m))/(m − n) = 4; m = 5, n = 3), Methods 1-4 | SAME (her basketballs kept) |
| A7 | Negative powers expression = ? | 3416-3459 | Math (negative power flips; cancel; 3); **plug in x = 1: the choices are only numbers, so one plug-in always solves it; 1 is the friendliest for powers**; here plugging in is clearly shorter, recommended | `solve-q-131`, now in **topic 8** | CHANGED (moved to topic 8; both methods and her "only numbers → one plug-in" rule kept) |
| A8 | Which is constant, not depending on a? | 3462-3537 | Simplify each choice until a disappears: (a + a) − (a − a) = 2a; (a + 1) + (a + 1)² over (a + 2): **a "complex" common factor (a + 1)** → a + 1; a⁰ + (−1)^a: 2 or 0 by parity; eliminated three → mark the fourth, "no need to prove" (proof for the lesson: difference of squares → −2); **plugging in would be long (two values per choice), so the math way is recommended** | `solve-q-132`, now in **topic 8** | CHANGED (moved to topic 8; all of her steps kept, including "mark it, no need to prove" and why plugging in is slow) |
| A9 | 1 + (2y² + 2xy)/(x² − y²) (hard) | 3540-3616 | **Math way 1: simplify first** (factor 2y, difference of squares, cancel, then 1 = (x − y)/(x − y)); **Math way 2: combine first** (1 as (x² − y²)/(x² − y²), the top becomes (x + y)²); **plug in** x = 2, y = 1 (x ≠ ±y), check choices differ; **for most students plugging in is the right way, "unless you are algebra prodigies"** | `solve-q-133` (1 + (6b² + 6ab)/(a² − b²)), Methods 1-3 | SAME |
| A10 | 42,944 / 61 | 3618-3659 | No calculator; long division is slow; **they test whether you're rigid — like a job interview "how many gas stations are there in Israel?"; estimate**: the choices are far apart; 42 ÷ 6 = 7 → 42,000 ÷ 60 = 700 → 704; **or test the choices**: 61 × 404 ≈ 24,000; 508 and 608 by leading digits and by the units digit (8 × 1 ends in 8, not 4) | `solve-q-134` (33,046 / 41), Methods 1-2 | SAME |

**Counts (15 items: T, B1-B4, A1-A10):** SAME 13 · CHANGED 2 (A7, A8: moved to topic 8) · PARTIAL 0 · MISSING 0.

---

## 2. English → Hebrew (English topic-5 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Her take? |
|---|---|---|---|
| `expression-strategy` slide 4 | Splitting a fraction: top yes, bottom never (6/(1 + 2)) | her A5 way 2 (moved forward) | no (not in the base) |
| `expression-strategy` slides 5-7, 9-10 | Opposite brackets, main fraction bar, repeated bracket, plug-in rules, pick your method | taught by her inside B1-B4 (pre-taught here, then taught again in the question videos) | yes (the base had slides 5-8) |
| `expression-strategy` slide 9 | Choosing numbers (different small values, lazy 0 and 1, obey conditions, pick numbers that satisfy a given equation) | her A2 / A6 smart choices, generalised | no |
| `solve-q-138` Method 3 | Two blocks: (A + B)² − (A − B)² = 4AB | none | yes |
| `r26-t05-shortcuts` + `solve-q-r26-t05-02/-03/-04` | Sum and product (a quick reminder); round numbers (99 · 41, 96 · 104); a given block (x + y = 5); a plug-in tie with ones | none | no |
| `r26-t05-power-count` + `solve-q-r26-t05-17/-18` | Count the powers (degree check) to eliminate choices and break plug-in ties | none | no |
| `r26-t05-summary` | Summary (replaced by the printable summary page); it also teaches "which does NOT depend on x?" with x² + 6x + 9 − x² − 6x, the idea of her A8, which now lives in topic 8 | — | — |

**Repeats to consider (memory rule *teach-in-question-videos*).** `expression-strategy` teaches the opposite-brackets
rule (slide 5), the main bar (slide 6), the repeated bracket (slide 7) and the plug-in rules (slides 8-9), and then her
question videos q-135, q-136, q-137 and q-138 teach each of them again. In her course the theory video is short and each
idea is taught once, in the question that uses it. For the 1-12 redo: shorten slides 5-9 to one-line previews (or drop
them) and keep the full teaching in the question videos. Estimated saving: about 2 minutes of lesson.

**English errors found (not hers).**
1. `solve-q-127` opens: "You know sum and product from Topic 4. … Sum and product would work." Topic 4 never teaches the
   sum-product method (only a promise: "It comes later in this topic"), and she says in this very question "we haven't
   learned how to bring this expression to one of the answers". Either teach sum-product in topic 4 (then this line is
   right) or rewrite the opening as hers: "We haven't learned to factor this one. But the choices help: open them."
   The topic-5 summary has the same claim ("A trinomial? Sum and product, from Topic 4").
2. `r26-t05-shortcuts` slide 3 says "That's sum times difference, from the last topic." In the study plan topic 5 comes
   long after topic 4 (ORDER: … 4, 31, 6, 8 … 22, 41 … 5), so "from topic 4" or "from the formulas lesson" is safer.

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | A3: her opening ("we haven't learned to factor this; the choices help us") in place of the English "You know sum and product from Topic 4" | `solve-q-127` slide 1, first two lines | her old take exists; topic in the 1-12 redo | **Restore** (it fixes a false claim; 1-2 sentences) unless sum-product is added to topic 4 |
| 2 | A2: her number-choosing aid "b is the second letter, so 2; c is 3" | `solve-q-126` Method 2 (1 sentence) | same | Optional. It makes the smart choice easy to remember, but the English letters (w, x, y, z) don't line up with 1, 2, 3, so it would need w, x, y, z → 20, 2, 3, 4 or similar |
| 3 | B2: the visual-distractor tip repeated | `solve-q-136` | same | Not needed; once (q-135) is enough |

Her four named rules are all kept: "the expression has one side, never drop its denominator", "(a − b)/(b − a) is always
−1", "when plugging in, eliminate three — a tie means new numbers", and "plug in only in an expression, and don't
overuse it". Her A7/A8 are complete in topic 8.
