# Topic 13 (Absolute Value): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 11081-13678 (source 11; all of it read).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t13.py`), practice list from the course dump.
- Recording status (`video_status.py`): **done** = absolute-value, -2, -3, solve-q-358/359/360/362/364-370, r26-t13-tools,
  solve-q-r26-t13-01/02/03/13. **Re-read pending** = solve-q-361, solve-q-363. r26-t13-summary = a summary page, not read aloud.
  So almost the whole topic is already recorded.

**Match scale.** New numbers alone are not a change. SAME = same idea and all her methods. CHANGED = same idea, method / example
type / order differs. PARTIAL = some of her content or one of her methods is missing. MISSING = no English equivalent.

**Structure.** Her topic is one theory lesson (11083-12057) with five worked examples *inside* it, then the advanced part
(8 questions, 12061-13674), then 15 self-practice questions. English splits her lesson into three camera parts
(absolute-value, -2, -3) and turns each of her five in-lesson examples into its own solution video (q-358 … q-362), keeping her
numbering: Hebrew advanced questions 1-8 = q-363 … q-370. No numbering gaps.

**Her names.** ערך מוחלט = "absolute value"; "שאלות הבנה" = "understanding questions"; "ניסוי וטעייה / הצבת מספרים" = "plugging in
numbers"; "אזור הקטן / הגדול של אי השוויון" = "the small side / the big side"; תחום סגור / פתוח = "a closed range / an open range";
"ערך מוחלט ≈ חזקה זוגית" = "bars and an even power behave the same way". All carried over.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | ערך מוחלט – הגדרה · Definition | 11083-11179 | Distance from 0; 5 and −7; always ≥0 ("my friend's home isn't −3 km"); the bars notation; positive stays, negative loses the minus (8, −3, −2/7, 0: "0 is right there") | absolute-value slides 1-2 | SAME (English adds "a letter hides its sign: \|x\| = −x when x<0") |
| 1b | ביטוי בתוך ערך מוחלט · An expression inside the bars | 11182-11233 | \|4+(−7)\| = 3: compute the inside first; the wrong way (turn −7 into 7 and add) | absolute-value slide 3 (\|3+(−10)\|, \|5−11\|) | SAME |
| 1c | כללים של ערך מוחלט · The rules | 11236-11428 | (1) \|a\| ≥ 0, "the most important rule"; (2) \|ab\| = \|a\|·\|b\| (3·5); (3) \|a+b\| ≤ \|a\|+\|b\|, "fine if you don't remember it, you'll solve by plugging in or understanding"; same signs equal (−2,−5), opposite signs smaller (−2,5) and why (a minus "eats" part) | absolute-value-2 slides 1-2 | SAME (English adds the fraction version of rule 2; keeps her "fine if you don't remember") |
| 1d | שאלות הבנה – xy<0, x<\|x\| · Understanding question | 11431-11561 | Opposite signs from the product; x<\|x\| → x negative, so y positive; "\|y\|<\|x\|? can't know (−2 and 7)"; \|y\| = y is right | solve-q-358 slide 0 (xy<0, y<\|y\|) | SAME (understanding method kept, the "signs say nothing about sizes" point kept). English adds a 2nd method, plugging in, with a tie-breaker pair |
| 1e | רמזים: מספר מול הערך המוחלט שלו · Clues: a number vs its absolute value | 11564-11612 | \|x\|>x → negative; \|x\|=x → ≥0 (don't forget 0); x>\|x\| → contradiction; "repeats a lot on the exam, tells me the sign at once" | absolute-value-2 slide 3 | SAME (English adds \|x\| = −x → ≤0) |
| 1f | ערך מוחלט במשוואות · Equations: \|x+4\|=9 | 11615-11691 | Two cases (= right side / = minus right side); x=5 or −13; −5 is in the choices "but that's not correct"; "could be" wording, only −13 offered | absolute-value-3 slide 1 (theory, \|x+3\|=8) + solve-q-359 slide 0 (\|x+7\|=9) | SAME (her −5 trap = English −2 trap; "could be" kept). English adds the number-line distance method (q-359 slides 1-2, absolute-value-3 slide 2) and plugging in the answers |
| 1g | ערך מוחלט באי-שוויון – תיאוריה · Inequalities: theory | 11694-11844 | Two situations, bars on the small or big side; range always symmetric; \|x\|>5 → open (6,7,8 / −6,−7,−8); \|x\|<5 → closed; "exactly like second-degree inequalities" | absolute-value-3 slides 3-4 (\|x\|>3, \|x\|<3, \|x−2\|<5) | SAME (the link to x² inequalities kept) |
| 1h | דוגמה: \|x+4\|<7 · Example, small side | 11847-11899 | Closed range: 7 on one side, −7 on the other; subtract 4 → −11<x<3; pick the choice in range | solve-q-360 slide 0 | SAME (+ number line and plug-in methods added) |
| 1i | דוגמה: \|x+2\|>5 · Example, big side | 11902-11951 | Open range, two cases: x>3 or x<−7; the one choice that doesn't fit (3) | solve-q-361 slides 0, 2 | SAME ("cannot" wording made explicit; + number line method) |
| 1j | ניסוי וטעייה: x<0, 2+2x/\|x\| · Trial and error | 11954-12036 | An expression → plug a number; x=−3 "just because, any number"; got 0, the other choices weren't 0, so one plug-in was enough | solve-q-362 slide 0 (10+4x/\|x\|, x=−2) | SAME (English makes the "one plug-in is enough because the choices come out different" explicit, and shows why −6 would be a bad pick). English adds the algebra method (\|x\| = −x, x/\|x\| = −1) |
| 1k | סיכום השיעור · Lesson close | 12039-12057 | Bars in expressions, equations, inequalities; "inequalities are the harder part, **and rarer on the exam**; rewind and review" | absolute-value-3 slide 5 | PARTIAL (the recap is there; her "rarer on the exam" remark is not) |
| 2 | פתיח לימוד מתקדם · Advanced intro | 12061-12067 | "After the basics, on to psychometric practice" | none | MISSING (trivial, no content) |
| 3 | \|b\|=a, b≠a, 2c=a (Q, easy+) | 12071-12227 | "Most absolute-value exam questions are understanding questions"; (1) understanding: a positive (not 0, else b=0=a), b = −a, c = a/2 → b<c<a, on a number line; (2) plug in: a=1,b=1 fails the 2nd given → change to b=−1; c=½; her verdict "I prefer understanding, plugging in is excellent too" | solve-q-363 (\|n\|=m, n≠m, 4k=m) | SAME (both methods, the failed first pick and the fix; English adds "when a pick breaks a given, change it"). Her which-way verdict dropped (R35) |
| 4 | a<b<0<c<d (Q, medium) | 12234-12408 | Number line; same side → can compare, positive vs negative → can't (−2,−1 vs 100,200); disprove choices 1-3 with numbers; mark 4, then confirm it in the lesson | solve-q-364 (p<q<0<r<s) | SAME (English adds a 2nd method: two "extreme pictures" of numbers) |
| 5 | a>b>c, \|b\|>\|a\| – not necessarily true (Q, hard) | 12415-12658 | Bars flip the order → b negative ("only a negative number changes under bars"); c negative; a could be either (−1/1 with b=−2); answer \|a\|≠a; she still checks 2-4 | solve-q-365 (z<y<x, \|x\|<\|y\|) | SAME (English also allows x=0; adds a plug-in method) |
| 6 | \|x+y\|>1 – possible but not necessarily (Q, hard) | 12665-12941 | Reading the wording (impossible out, always-true out); (1) square it technically, then "much simpler: bars ≈ even power"; (2) \|xy\|<\|x\|\|y\| never; (3) factor 2 out of \|2x+2y\|, split, cancel → 1<2 always; (4) the sum rule: equal with same signs (3,1), smaller with opposite (3,−1) | solve-q-366 (3<\|x+y\|; 5x+5y) | SAME (every step; English adds "it could only fail if x+y were 0" and a full plug-in method) |
| 7 | 4\|x\|+8\|y\|=20, x+2\|y\|=1 (Q, medium) | 12948-13173 | Three ways: (a) full math: ÷4, subtract equations, \|x\| = 4+x, two cases (0=4 false; x=−2); (b) same algebra, then plug the answers into \|x\|=4+x ("much more right at this stage"); (c) plug the answers in from the start (find \|y\| from one equation, check the other); her pick: (b) or (c) | solve-q-367 (4\|x\|+12\|y\|=44, x+3\|y\|=1) | SAME (all three ways; English adds a check of x in the original). Her "these are the ones I'd choose" verdict dropped (R35) |
| 8 | \|x+2y\|=\|2x+y\| (Q, medium+) | 13180-13357 | Three ways: (1) two cases → x=y or x=−y → \|x\|=\|y\|; (2) square both sides, expand, y²=x² → bars ≈ even power (or root ±); (3) plug in: equal numbers, then the hint in the choices → opposite numbers as tie-breaker; "the third is the shortest but hard to see" | solve-q-368 (\|x+4y\|=\|4x+y\|) | SAME (her "not obvious, but the shortest" line kept; English adds "swap x and y" to drop choices 1 and 4) |
| 9 | 13<\|2x+1\|<15 (Q, hard) | 13364-13496 | Double inequality, "a more elegant way": positive band 13..15 → 6<x<7, peek at the choices, none → the symmetric negative band → −8<x<−7; plug in the answers with a convenient middle number (7.5, −7.5); "no doubt plugging in is much shorter" | solve-q-369 (7<\|2x−1\|<9) | SAME (both of her methods incl. "check the choices before doing the negative band"; English adds a 3rd method, splitting into two inequalities, and the bait choices from subtracting instead of adding). Her verdict dropped |
| 10 | x+\|x\|<10 – most precise domain (Q, hard) | 13503-13668 | (1) Two cases: x≥0 → x<5; x<0 → x+\|x\| = 0 <10, every negative works → answer x<5; (2) plug in: choice "every positive" → 1 works but 10 fails; choice "only negatives" → 1 already works; 2 vs 4 share x<5 → "no need to check the top, the difference is the bottom" → smart plug-in x=−10 | solve-q-370 (x+\|x\|<12) | CHANGED (method 1 SAME. Method 2: the choices were rebuilt, so English starts with x=0, which kills two choices at once, instead of her 1-then-10 test; her "same top, test the bottom" tie-breaker is kept, with −8) |
| 11 | 15 שאלות תרגול עצמי · 15 self-practice questions | 13678 | — | q-371 … q-385 (15) + alg-extra ×3, q-r26-t13-10/-11 | SAME (all 15 kept) |

**Count by row (21 rows):** SAME 18 · CHANGED 1 (10) · PARTIAL 1 (1k) · MISSING 1 (2).

### Count by video (her units)

| Unit | Match |
|---|---|
| Lesson (1a-1k, incl. her 5 in-lesson examples) | SAME (only the one-line "rarer on the exam" remark is missing) |
| Advanced intro | MISSING (trivial) |
| Q3 … Q9 (seven questions) | SAME |
| Q10 x+\|x\|<10 | CHANGED |
| 15 practice questions | SAME |

**By video: SAME 9 · CHANGED 1 · PARTIAL 0 · MISSING 1** (11 units: the lesson, the intro, 8 questions, the practice set).

---

## 2. English → Hebrew (added in English)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| absolute-value slide 2 (part) | A letter hides its sign: \|x\| = −x when x<0 | none | yes |
| absolute-value-2 slide 3 (part) | \|x\| = −x → x ≤ 0 | none | yes |
| absolute-value-3 slide 2, q-359 slides 1-2, q-360 slide 1, q-361 slide 1 | The number-line **distance** reading of \|x−a\| (and \|x+a\| = distance from −a) | none | yes (q-361 re-read pending) |
| 2nd methods in q-358, q-364, q-365, q-366 | Plugging in numbers (incl. tie-breaker pairs, two "extreme pictures") | she uses numbers only to disprove choices | yes |
| solve-q-362 slide 1 | Algebra: \|x\| = −x, x/\|x\| = ±1 | none | yes |
| solve-q-369 slide 1 + bait | Splitting a double inequality into two; the "subtract instead of add" bait | none | yes |
| r26-t13-tools | \|x\|² = x², √(x²) = \|x\|, \|a−b\| = \|b−a\|, distance reading | the even-power idea is hers (Q6, Q8) | yes |
| solve-q-r26-t13-01 | \|2x−1\|=7: solve the 2nd case fully, not "flip the sign" | none | yes |
| solve-q-r26-t13-02 | Bars vs a negative right side: no solution / always true | none (her rule 1 is the seed) | yes |
| solve-q-r26-t13-03 | A letter on the right side (\|x+4\|=3x): check for fake answers; right side ≥ 0 shortcut | none | yes |
| solve-q-r26-t13-13 | \|a\|=7, \|b\|=3, \|a+b\|<\|a−b\| → opposite signs | builds on her sum rule | yes |
| r26-t13-summary | Summary page (not read aloud) | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | "Absolute value in inequalities is the harder part, and it is rarer on the exam" (lesson close) | absolute-value-3 slide 5, one sentence | yes (done) | NOT NEEDED. Exam-frequency comment only; would mean re-recording a finished camera part |
| 2 | Advanced-section intro | start of solve-q-363 | yes (re-read pending) | NOT NEEDED (no content) |
| 3 | Q10: her plug-in path (test 1, then 10, to kill "every positive") | solve-q-370 slide 1 | yes | NOT NEEDED. The English choices were rebuilt, and the zero test does the same job faster; her "same top, test the bottom" idea is kept |
| 4 | Her "which way I prefer" verdicts (Q3, Q7, Q9, Q8) | — | — | NOT NEEDED (dropped on purpose by rule R35; Q8's "shortest but not obvious" is kept) |

**RESTORE list: none.** Every method and named trick she gives in topic 13 is in the English, and each still works with the
English numbers. Nothing in the English is wrong compared with her.
