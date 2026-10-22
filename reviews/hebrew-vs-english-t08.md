# Topic 8 (Exponent Laws, Fundamentals): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 4795-5356 (all of it read). Her structure note
  (4796): "סרטון - טבלת לימוד בעפ ואז 10 שאלות תרגול בלי סרטונים באמצע" = one video, a table to learn by heart, then 10 practice
  questions with no videos between them.
- English: the per-topic dump `scratchpad/ext/course/t08.txt` / `q08.txt` (topic 8 has no reading scripts yet, only
  `ai_scripts/r26-t08-summary.json`), and the base translation `studio-build/base-v18.html` (video `exponents`, memory card `powers`).
- Recording status: `video_status.py` does not track topics 1-12 (it lists only the Reading Studio topics), so `--list record`
  shows nothing for them. **Every topic-8 video has an older camera take** (6 Oct 2026, `~/Documents/Course.recordings/1 Algebra/
  Topic 08 …`: exponents, r26-t08-traps and all 8 solution videos). By the production plan, topics 1-12 are redone LAST: the
  first lesson (`exponents`) on camera again, everything else with AI narration. So any restore below goes into that redo
  script; nothing has to be re-recorded now.

**Match scale** (same as the t23 model). New numbers alone are not a change. SAME = same idea and every one of her methods.
CHANGED = same idea, different method/example type/order. PARTIAL = something of hers is missing. MISSING = no English equivalent.

**Her single video "כללי חזקות" is a list of rules**, so it is split below into her rules (rows 1a-1r), each with its line range.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her part (Hebrew · English gloss) | Lines | What she teaches / how | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | פתיחה · Intro | 4798-4824 | Exponents first, then roots, then exam questions; the laws must be fluent; they appear in algebra and inside geometry | `exponents` slide 1 | SAME |
| 1b | מה זו חזקה · What a power is | 4825-4845 | Short way to write repeated multiplication (3·3·3·3·3 = 3⁵); base and exponent; "the names matter less, this isn't the bagrut" | slide 2 (4³ = 64) | SAME (English adds "it is NOT 4 × 3"; drops the throwaway "names matter less") |
| 1c | חזקת 1 · Power of 1 | 4846-4869 | a¹ = a: "write a once"; 3¹ vs 3² ; (−5)¹ = −5 | slide 3 | SAME |
| 1d | חזקת 0 · Power of 0 | 4870-4884 | Any number⁰ = 1; "a strange rule, we'll explain it later, for now remember"; 2⁰ = 1 | slide 3 (the "staircase": 125, 25, 5, 1) + slide 7 (5ⁿ/5ⁿ) | CHANGED (better): English explains it twice instead of "just remember", and says "nonzero" where she says "always". Her promised explanation never comes in her own video, so nothing of hers is lost |
| 1e | בסיס 1 · Base 1 | 4885-4899 | 1ⁿ = 1: 1·1·1… 7 times, a million times | slide 5 | SAME (the base had her "a million times"; the current line says "as many times as you like") |
| 1f | בסיס 0 · Base 0 | 4900-4923 | 0^(positive) = 0 (0⁷, 0²); 0⁰ undefined, "you probably won't meet it, just for knowledge" | slide 5 | SAME (English adds 0^(negative) is undefined) |
| 1g | חזקה שלילית · Negative exponent | 4924-4952 | (x/y)⁻ⁿ = (y/x)ⁿ: "flip the number and the minus disappears"; (3/7)⁻² = (7/3)² | slide 4 | SAME (English adds the staircase down to 5⁻¹, 5⁻², the whole-number case 2⁻³ = 1/8, and "minus in the exponent = flip, minus in the base = sign") |
| 1h | כפל בסיסים זהים · Multiplying, same base | 4953-5007 | Add the exponents; 2²·2³ = 2⁵, shown by writing out the 2s | slide 6 "Multiplying powers" (3²·3⁴) | SAME (English adds the plus-sign trap 3² + 3⁴ = 90) |
| 1i | חילוק בסיסים זהים · Dividing, same base | 5008-5058 | Subtract; 3⁵/3² = 3³, shown by cancelling the 3s | slide 7 (5⁷/5³) | SAME (English adds "more on the bottom stays downstairs") |
| 1j | חזקה על חזקה · Power of a power | 5059-5127 | Multiply the exponents; warning: students confuse it with multiplying same bases; (4²)³ = 4⁶ explained TWO ways: (a) write out 4·4 three times; (b) as 4²·4²·4² and the add rule: 2+2+2 = 6 | slide 8 ((2³)⁴ = 2¹²; 2³·2⁴ = 2⁷ as the contrast) | SAME (the warning is kept with an example. Only explanation (a) is said; her second view (b), "it is the add rule repeated", is not said. It is an explanation, not a method) |
| 1k | מעריכים זהים, כפל · Same exponent, multiplying | 5128-5172 | 3⁴·2⁴ = (3·2)⁴, by reordering the factors; "a very important rule, we'll use it a lot" | slide 9 (4²·5² = 20² = 400) | SAME |
| 1l | מעריכים זהים, חילוק · Same exponent, dividing | 5173-5199 | 2²/3² = (2/3)² | slide 9 (one line) | SAME (English adds "NOT over a plus or a minus") |
| 1m | בסיס שלילי, חזקה זוגית · Negative base, even power | 5200-5214 | Always positive, minus × minus = plus; (−3)⁴ = 81 | slide 10 (positive 64) | SAME |
| 1n | בסיס שלילי, חזקה אי-זוגית · Negative base, odd power | 5215-5226 | One minus left over; (−5)³ = −125 | slide 10 (−1000) | SAME |
| 1o | סדר פעולות · Order: power before the sign | 5227-5259 | −3² : the power first (9), then the minus. Her reason: power before × ÷, which come before + −, and this minus acts like a subtraction | slide 10 (−7² = −49) | SAME (the rule is there, plus "brackets decide the base; put a negative you plug in inside brackets". Her order-of-operations reason is shortened to "the power comes first") |
| 1p | aᵇ = 1 · When aᵇ = 1 | 5260-5301 | Three options: a = 1 (b anything); a = −1 and b even; b = 0 (a anything) | slide 12 | SAME (English adds "nonzero" in case 3) |
| 1q | 2⁴ = 4² · The 2 and 4 exception | 5302-5349 | aᵇ = bᵃ happens "only" for 2 and 4 (16 = 16); "a nuance that appears a lot on the exam"; not a rule but a specific pair; any other numbers, one side is bigger | slide 11 | SAME (English is more exact: "among positive whole numbers", and notes negatives/fractions have other pairs. Her "in every other case it doesn't happen" is too absolute; English corrects it, which is right) |
| 1r | סיום · Close | 5350-5353 | Next: the lesson on the root rules | — (English slide 1 says "roots come right after"; the lesson ends with the rules table and "core questions next") | SAME (trivial) |
| 2 | טבלת לימוד בעל פה · Table to learn by heart | 4796 (note) | (no transcript) | slide 15 "The rules table" + memory card `powers` (laws + powers table + three tips) | SAME |
| 3 | 10 שאלות תרגול בלי סרטונים · 10 practice questions, no videos | 4796 (note) | (no transcript) | 28 questions: q-218…q-232 and extras as practice, **plus 8 solution videos** (q-131, q-132, q-224, q-226, q-231, r26-t08-01/-02/-05) | CHANGED (structure): she has no solution videos in this topic; English adds 8. Her 10 questions themselves cannot be checked (no transcript) |

**Count by row (20 rows):** SAME 18 · CHANGED 2 (1d, 3) · PARTIAL 0 · MISSING 0.

### Count by video (her 3 units)

| Unit | Match |
|---|---|
| Lesson כללי חזקות (1a-1r) | SAME (every rule and warning is there; only two "why" explanations are shortened: 1j (b) and 1o) |
| Table to learn by heart | SAME |
| 10 practice questions | CHANGED (English adds solution videos and more questions) |

**By video: SAME 2 · CHANGED 1 · PARTIAL 0 · MISSING 0.**

---

## 2. English → Hebrew (added, no Hebrew equivalent)

| English video / part | Added content | Hebrew source? |
|---|---|---|
| `exponents` slides 3-4 (part) | The "staircase" (5³ → 5² → 5¹ → 5⁰ → 5⁻¹ → 5⁻²): why a⁰ = 1 and why a⁻ⁿ = 1/aⁿ | none (she says "remember, we'll explain later") |
| `exponents` slide 7 (part) | Second proof of 5⁰ = 1 (5ⁿ/5ⁿ) | none |
| `exponents` slide 13 "Splitting exponents" | 2ⁿ⁺³ = 8·2ⁿ; 2ⁿ⁺³ − 2ⁿ = 7·2ⁿ by a common factor | none in topic 8 (this kind appears in her topic 10/11 questions) |
| `exponents` slide 14 "Adding equal powers" | 2ⁿ + 2ⁿ = 2ⁿ⁺¹; the trap 2²ⁿ | none in topic 8 (her topic-11 question 4ˣ = 4ʸ+4ʸ+4ʸ+4ʸ) |
| `exponents` slide 6, 9 (parts) | Plus-sign trap (3² + 3⁴ ≠ 3⁶); not over + or − | none |
| solve-q-131, -132, -224, -226, -231 | Solution videos for practice questions (simplify + plug in x = 1; constant expression; split the exponent + check a number; one base; test each choice with the three cases) | none (she has no videos here) |
| r26-t08-traps | Powers between 0 and 1 get smaller; decimal powers (0.2³, 0.3²); compare powers by equal bases or equal exponents; equal bases → equal exponents | none in topic 8 |
| solve-q-r26-t08-01, -02, -05 | Copies of a power; plug in ½ between 0 and 1; odd/even powers and signs | none |
| r26-t08-summary | Spoken summary of all the laws | none |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | Power of a power, her second explanation: (4²)³ = 4²·4²·4², so by the add rule 2+2+2 = 6 | `exponents` slide 8, one sentence after "Twelve twos" | yes (old camera take); goes into the camera redo | Optional. One sentence; it ties the new rule to the one just learned, which helps students who mix the two up (the exact confusion she warns about) |
| 2 | Her order-of-operations reason for −3² (the minus acts like a subtraction, and powers come before it) | `exponents` slide 10 | yes (old take) | Not needed. The rule and the bracket advice are there; the reason adds little |
| 3 | "A nuance that appears a lot on the exam" for 2⁴ = 4² | `exponents` slide 11 | yes (old take) | Not needed; English already flags it ("when the exam wants two and four, it says: positive integers") |

**Nothing of her teaching is missing or wrong in English.** Where English differs from her, it is more exact (0⁰, "nonzero",
the 2-and-4 pair only among positive whole numbers). Her "always" for a⁰ = 1 and "only 2 and 4" are slightly overstated in
the Hebrew; English is right to qualify them. **RESTORE list: empty** (one optional sentence, item 1).
