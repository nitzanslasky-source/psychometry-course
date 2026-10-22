# Topic 11 (Exponents & Roots, Advanced): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 6610-8727 (all of it read). Her section is **14 worked
  example questions, one video each, with no theory video and no intro** (it starts directly with "שאלה לדוגמה, שאלה ברמת קושי
  גבוהה"), then "20 question of תרגול עצמי" (8725). Her topic-10 closing note (6605) calls this part "חזקות ושורשים לימוד מתקדם".
- English: `scratchpad/ext/course/t11.txt` / `q11.txt`, current choices from `~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html`,
  base translation `base-v18.html`, real exam bank `studio-build/real_exam/quant_real.md`.
- Recording status: `video_status.py` does not track topics 1-12. **Older camera takes exist** (7 Oct 2026, `~/Documents/
  Course.recordings/1 Algebra/Topic 11 …`) for advanced-powers, solve-q-288…297, 299, 300, 301, r26-t11-01, -02, -13.
  **No take: solve-q-298 and r26-t11-tools.** Topics 1-12 are redone last (first lesson on camera, the rest AI), so restores go
  into that redo. Her own additions while reading these English takes are logged in `studio-build/real_exam/added_by_nitzan.json`
  (carry them into the redo too).

**Match scale** as in the t23 model; new numbers alone are not a change.

---

## 1. Hebrew → English (her videos, in her order)

Her 14 questions map one-to-one, in the same order, onto solve-q-288 … solve-q-301.

| # | Her video (Hebrew · English gloss) | Lines | What she teaches / every method | English equivalent | Match |
|---|---|---|---|---|---|
| 1 | (2x)⁴(7x)³/(14x²)³ · 0.5x (high) | 6612-6843 | (1) Laws: each factor in the bracket gets the power; **split 14 into 2·7 first**; (x²)³ = x⁶; cancel → x². (2) Plug in x = 1, "the friendliest number for powers", **after checking the choices differ at x = 1**; split 14 again. Verdict: "for most students plugging in is better, unless you are very strong in algebra" | solve-q-288 ((5x)⁴(2x)³/(10x²)³ · ⅕x) | SAME (every step; "split 10 into 5·2 first"; the distinct-choices check; the verdict, shortened. The written solution adds a power count) |
| 2 | a⁻¹b²/(c³d⁻⁴) (medium) | 6844-6940 | (1) Standard: rewrite negative powers as fractions, multiply, untangle. (2) **"A negative power switches floors"**: a⁻¹ goes down, d⁻⁴ goes up → look for the matching choice; "a few seconds" | solve-q-289 (p³q⁻⁴/(r⁻²s⁵)) | SAME (both methods, "switch floors" kept; English adds Method 3 power count) |
| 3 | x^(y+1) = 1, x ≠ 1, which is necessarily true (medium+) | 6941-7268 | The three cases of bᵃ = 1 (base 1; base −1 with an even power; power 0, base ≠ 0); here y + 1: x = −1 needs y odd, power 0 needs y = −1; x ≠ 1 kills case 1. **The choices are "condition → result" (if y ≠ −1 then x = 0; if x ≠ −1 then y = −1; …): her method, "treat the condition as one more given", cross out the cases it rules out, see what is left.** She then shows why 3 and 4 fail: a condition that rules out no case proves nothing | solve-q-290 (m^(n−3) = 1, m ≠ 1; choices "m = 0 or n ≠ 5", "m = 0", "n = 3 or m = −1", "m = 0 or n ≠ 3") | CHANGED: the three cases and "the extra given kills case 1" are the same. **The choices were rewritten as "or" statements** (already in the base translation), so her if-then method ("the IF is one more given") is not taught in any video. It survives only as text in `ai_scripts/r26-t11-summary.json` (summaries are not videos; topic 11 has no summary page yet). The real exam uses her format: 2025_winter_q1_18 (x²ⁿ = x⁻ⁿ) has choices "If n is even, then necessarily x = 1 …" |
| 4 | xʸ = yˣ, y = √x, x, y > 1 (medium+) | 7269-7428 | (1) Substitute y = √x; **write √x as x^½ ("root → power, as we learned")**; equal bases → equal exponents: √x = ½x; square; 4x = x²; x ≠ 0 since x > 1 → x = 4; "quite long". (2) The 2-and-4 object: for numbers > 1 only 2 and 4; test x = 2 → √2 ≠ 4 → choice 4; "no doubt here, seconds" | solve-q-291 (y = x², x > 1 → x = 2) | CHANGED (by the new numbers): both methods and "quite long" are there; English adds "only for whole numbers" (correct; her "for numbers greater than 1, only 2 and 4" is too wide). With y = x² instead of √x, **her root → power step and the squaring step are gone** (only a power of a power is left). Those skills are practised in q-294, q-297 and r26-t11-02 |
| 5 | 3ˣ·3ʸ = 9, 2xy = 3, x² + y² (medium+) | 7429-7501 | Add the exponents → x + y = 2; the givens build the first contracted formula: (x+y)² = x² + y² + 2xy → 4 = ? + 3 → 1 | solve-q-292 (81, 2xy = 6 → 10) | SAME |
| 6 | 2ˣ = 2ʸ + 2ʸ, x − y (medium+) | 7502-7631 | (1) Same term twice = 2·2ʸ, like y + y = 2y, √5 + √5 = 2√5; 2 = 2¹ → 2^(y+1); three copies → 3·2ʸ. (2) Plug in: an equation, so plug into one letter (y, it appears twice), y = 1 → x = 2 → 1; "the choices are numbers, one substitution is always enough"; plugging in is shorter for most | solve-q-293 (4ˣ = four copies of 4ʸ) | SAME (both methods and all her reasons; English adds the trap "four copies is not plus four") |
| 7 | √(1/3)·√54·⁸√(3⁴)/√6 (medium) | 7632-7749 | Make the roots the same order: ⁸√(3⁴) → 3^(4/8) with **her mnemonic "חזקיהו בשמיים, השורש באדמה"**; shortcut: cancel the power and the root index; multiply same-order roots under one root; some students cancel √(1/3) with √3 early; divide under one root → √9 = 3 | solve-q-294 (√(1/5)·√176·⁶√(5³)/√11 → 4) | SAME (every step; the mnemonic became "the power is the flower, up on top; the root stays in the ground") |
| 8 | Which is largest: √35, 2π, √3 + √26, 4√2 (medium) | 7750-7872 | Estimation, **with decimals, eliminating as you go**: √35 just under 6; 2π ≈ 6.28 (choice 1 out); √3 ≈ 1.7 + √26 ≈ 5+ → 6.7+ (choice 2 out); 4√2 two ways: ×1.4 = 5.6, **or bring 4 inside: √32 < √35** → choice 3 | solve-q-295 (2π, 2√11, √41, √21 + √6) | CHANGED (deliberately, rule *no decimal estimates*): one whole-number benchmark (7) for every choice instead of her decimals and "keep the current best"; the sum of roots is squared and compared with 49 instead of estimating each root. Her "bring the coefficient inside the root" is kept (2√11 = √44); her other way (×1.4) is dropped |
| 9 | 2/(3√3) + √3/9 (high) | 7873-8011 | (1) Simplify the second term first: 9 = 3·√3·√3 → 1/(3√3); **tip: flip it, use the "golden triangle" shortcut (9/√3 → 3√3), flip back**; then add → 1/√3. (2) Multiply the two denominators. "Both are excellent, choose what suits you" | solve-q-296 (5/(2√3) + √3/6 → √3) | SAME (her two methods are Methods 2 and 3, with the flip tip; English adds Method 1, rationalising the first denominator) |
| 10 | ∛(x√x) (high) | 8012-8150 | (1) Bring x into the square root as x²; root of a root → multiply the indices (⁶√x³); **cancel the indices by 3** → √x. (2) Plug in: 1 makes every choice equal; 2 has no root; take 4 ("the first number after 1 with a root"), check the choices differ, ∛8 = 2. "Master both; plugging in was shorter for most" | solve-q-297 (√(x²√x) → ⁴√x⁵) | SAME (both methods with all her plug-in reasoning: 1 useless, 4 not clean here, so 16. The index-cancelling step does not occur with these numbers but is taught in q-294. English adds Method 3 power count) |
| 11 | (a − b)/(√a + √b) (high) | 8151-8301 | (1) The third contracted formula with roots (a − b = (√a+√b)(√a−√b)); "not trivial, certainly not in exam time". (2) Plug in: a ≠ b, numbers with roots: 1 and 4 (2 and 3 have none); **smart choice a = 4, b = 1 to keep things positive**; check the choices differ; "the recommended way for the vast majority" | solve-q-298 (m, n > 0; 9 and 1) | SAME (both methods, the smart order and the distinct check. **No camera take exists for this video**) |
| 12 | Number of solutions of a root equation that becomes √x = x after opening the brackets (easy+; the stem is not read out in the subtitles) | 8302-8365 | Open the brackets, x cancels on both sides → √x = x, **"an object we already learned: √a = a has only two solutions, 0 and 1"** → exactly 2 | solve-q-299 (√x(√x − 6) = 0) | CHANGED (by the new equation): English opens the brackets (x = 6√x → 0 and 36) and adds Method 2 "a product is zero when a factor is zero" plus the warning "never divide by √x". **Her "√x = x → 0 and 1" object is in no video**; it appears only in the summary text |
| 13 | 2x + y = √72, x − y = √18 (high) | 8366-8552 | (1) Add the equations; **never √90**; split into a common root (36·2, 9·2) → 3√2. (2) **Estimation ("הערכת סדר גודל") for those who can't add roots**: √72 ≈ 8.5, √18 ≈ 4+ → x ≈ 4+; √10 ≈ 3+, 3√2 ≈ 4.2 fits, √30 ≈ 5.5, 9√2 far too big. "Master the math; estimation if there is no choice" | solve-q-300 (√180, √45; choices 9√5, √42, 5, 3√5) | CHANGED: Method 1 is the same (plus a faster view, 180 = 4·45, and the √225 trap). **Her estimation method is replaced by "try a choice".** With the English numbers estimation can't work: x = 3√5 ≈ 6.7 and the choice √42 ≈ 6.5 are too close (the base, with √108 and √27, still had "Method 2 · Estimate") |
| 14 | x^(−½) = 9 (medium+) | 8553-8724 | Three methods: (1) flip, power ½ = root, isolate, square → 1/81; (2) **"isolating an unknown in a power": raise to the reciprocal power (−2); always the reciprocal**; (3) plug in the answers, start with the round one (81) → get 1/9 instead of 9 → "only the reciprocal is missing" → 1/81 | solve-q-301 (x^(−⅓) = 2 → 1/8) | SAME (all three, in her order, with "always the reciprocal" and the reciprocal insight in Method 3) |
| 15 | 20 שאלות תרגול עצמי · 20 self-practice questions | 8725 (note) | — | unit `unit-t11-3` "Independent practice" (25) + `unit-t11-2` (8) | SAME |

**Count by row (15 rows):** SAME 10 · CHANGED 5 (3, 4, 8, 12, 13) · PARTIAL 0 · MISSING 0.

### Count by video (her 15 units)

**SAME 10 · CHANGED 5 · PARTIAL 0 · MISSING 0.** Two of the five CHANGED ones lose one of her methods because of the new
numbers or choices (Q3 the if-then method, Q13 the estimation method); Q12 loses her "√x = x" object; Q4 loses a skill
that is practised elsewhere; Q8 is a deliberate rule change.

---

## 2. English → Hebrew (added, no Hebrew equivalent)

| English video / part | Added content | Hebrew source? | Take? |
|---|---|---|---|
| advanced-powers (whole lesson) | Intro: you know the rules from topics 8-10; break big bases into primes; two routes in every question | none (she starts straight with Q1) | yes |
| Method 3 "power count" in q-289, q-297 (and q-288's written solution) | The power of a piece doesn't change when you simplify; match it with the choices | none | yes |
| solve-q-296 Method 1 | Rationalise the first denominator | none | yes |
| solve-q-299 Method 2 + warning | Product = 0; never divide by √x | none | yes |
| solve-q-300 Method 2 | Try the choice 3√5 = √45 | none (replaces her estimation) | yes |
| r26-t11-tools | Section B intro | none | **no** |
| solve-q-r26-t11-01 | 1/(√5−2) − 1/(√5+2): conjugates; estimate | none (real exam 2025_autumn_q1_20) | yes |
| solve-q-r26-t11-02 | ∛(x√x) = 2: exponents; try the choices | close to her Q10 | yes |
| solve-q-r26-t11-13 | Given ⁴√x³ = 8, find √x³: jump from power to power | none | yes |
| r26-t11-summary | Summary (text; becomes a summary page) | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **Q3 if-then choices + "treat the IF as one more given; a condition that rules out no case proves nothing"** | solve-q-290: give the choices her "If …, then necessarily …" form (new numbers, e.g. "If n ≠ 3, then m = −1" true; "If m ≠ −1, then n = 5"…), and teach her method in ~4 sentences. Or keep the "or" choices and add 2 sentences: "an 'or' claim is the same as 'if not this, then that' — treat the if as one more given" | yes (old take, 7 Oct); goes into the AI redo | **Restore.** It is her named method for this question type, the real exam uses exactly this format (2025_winter_q1_18), and right now it is taught only in summary text |
| 2 | **Q13 estimation method** (√180 between 13 and 14, √45 between 6 and 7 → x a bit under 7; compare the choices) | solve-q-300 as Method 3 (~4 sentences, whole-number benchmarks to respect the no-decimal rule). Needs the √42 choice changed to one far from 6.7 (e.g. √20 or 2√5), otherwise estimation can't separate the choices | yes (old take) | **Restore, with the distractor changed.** It is the method she offers students who can't add roots, and the base still had it; it was lost only because the new choices are too close |
| 3 | Q12 "√x = x has only two solutions, 0 and 1" (and x² = x) | one sentence in solve-q-299 Method 1 ("a close relative you should know: √x = x → only 0 and 1"), or a practice question | yes (old take) | Optional. English teaches the more general product-equals-zero route; her object is a quick fact. It is already in the summary text |
| 4 | Q8: 4√2 "the other way", ×1.4 | solve-q-295 | yes | Not needed (the no-decimal rule) |
| 5 | Q4: root → power step (√x = x^½) | solve-q-291 | yes | Not needed (taught in q-294, q-297, r26-t11-02) |

**English vs her, factual:** her "for numbers greater than 1, only 2 and 4 satisfy aᵇ = bᵃ" (7310-7316) is too wide (e.g. 9/4 and
27/8); English correctly limits it to whole numbers. Nothing in English is wrong compared with her.
