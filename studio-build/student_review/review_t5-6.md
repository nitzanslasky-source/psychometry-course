# Review — Topics 5 and 6

Note on keys: all `correct:` values are read as 0-based (0 = choice 1). I checked every question in both topics. **All keys are correct.** The problems I found are about wording, display, and one tip that the course's own questions break.

---

## Topic 5: Expressions

### Most important points first

1. **The Q1 video tip is contradicted by the course's own questions.** Q1 video, last line: "When an answer equals a choice NUMBER, say the answer is three, it sits in slot three." In the same question, Q1 has 3 in slot 1. Other examples: Q11 has 4 in slot 2, extra-01 has 3 in slot 1, extra-02 has 3 and 4 in slots 1–2, extra-08 has 0/1/2 in slots 1–3, extra-10 has 4 in slot 2, and extra-11 has 1 in slot 4. In Topic 6, q-159, q-161, q-163, q-149 and q-150 list 4, 3, 2, 1 in slots 1–4. Either remove the tip or reorder every set of choices. As it stands, a strong student who trusts the tip will be confused.
2. **Plain-text practice uses ":" for division, and one question is ambiguous.** extra-01 to extra-14 show items like "9:(1:(1:2+1:6))" and "(a+4b):a". Choice (3) of extra-07, "a+4b:a", can be read as (a+4b)/a, which is the correct answer. Render these in LaTeX with real fraction bars. The written solutions throughout also use ":" (e.g. "1:3 + 1:6"). English-speaking students expect "/" or a fraction bar.
3. **Ideas are used before they are taught.**
   - Q11 uses negative exponents (x⁻²). Q12 uses a⁰ and (−1)ᵃ. Exponents are only taught in Topic 8.
   - Q7 says "We don't know how to factor this yet", but the practice then asks "Factor x²+10x+24" (self-3, t5-1-3, extra-05).
   - 99·41, 96·104 and 95·105 (extra-19, self-5, t5-1-5) need the "round number" trick, which is never shown.
4. **Q8 blank order is reversed.** The stem reads "If ___ then … equals ___". The choices read "3 ; 0 < x", which puts the value first and the condition second. A weak student will fill in "If 3 then…". Swap to "0 < x ; 3", or reword the stem.
5. **Q9 video, Method 1, has weak logic.** "(B+A)/B … That's not what she started with ✗" is not a proof. Two expressions can look different and still be equal (Topic 4 is all about this). Say: "Looks different, so test numbers: A=1, B=2 gives 1/3 vs 3/2. Not equal." Keep Method 3 as the main proof.

### Coverage
- Good: nested fractions, opposite brackets, common factor, minus before brackets, plug-in with "eliminate three", units digit, estimation, and "which is constant".
- **Missing: "given the value of one expression, find another".** This is very common on NITE. Example: "If a − b = 3, then (b − a)² + 2a − 2b = ?" The trick is to treat a − b as a block. Add a guided question here, not only in Topic 7.
- **Missing: splitting a fraction as a rule on the board.** (a+b)/c = a/c + b/c, but c/(a+b) ≠ c/a + c/b. This appears only inside Q9 Method 2. It is the most common algebra trap, so give it its own lesson slide next to slide 3 ("No cancelling!").
- **Missing: plug-in traps.** The lesson mentions these, but no practice question forces them: values that make two choices tie (0 and 1), and values that break a condition (a ≠ ±b, "a is a positive integer"). Add 1–2 practice items where plugging in 1 creates a tie.
- Sign/parity questions ("if x < 0 < y, which expression is positive?") are only touched in Q8. If another topic covers them, add a pointer.

### Teaching quality
**Weak student**
- Slide 4 (nested fraction) is good. The "rewrite in one line" advice is helpful.
- Slide 5: "You could prove it… honestly? Trust it." One line of proof, −(a−b) = b−a, costs 5 seconds and helps memory.
- Gets lost at Q12 choice (2): "a+2 appears twice on top" needs to show (a+2) + (a+2)² = (a+2)(1 + a+2) on the board.
- Q13 is hard. The video correctly recommends plug-in, which is good.

**Medium student**
- Well served: there are several methods, and each video names the best one ("Here plugging in is faster").
- Gap: there is no single "method choice" checklist after the advanced section. Slide 8 exists, but only before the hard questions.

**Strong student**
- Q5 (four methods) and Q10 (four methods) are long. Mark Methods 1 in Q5 and Q10 as "skip if you know this".
- Wants exam-hard items. The hardest practice item (extra-14) is easier than Q4. There is no item harder than the guided ones.

### Correctness
- All 55 keys are correct.
- Q1 tip contradiction (see point 1).
- extra-07 ambiguous display (see point 2).
- Q8 blank order (see point 4).
- Q9 Method 1 reasoning (see point 5).
- The pre-loaded question text in the videos drops fraction brackets, e.g. Q2 "7 − p − q/q − p" and Q10 "(p − q) − (q − p)/p − q". Check that the screen renders real fractions.

### Methods to add or change
- **Block substitution slide** (after slide 6): "Repeated block → call it K" is already there as a tip. Extend it: "If they give you the block's value, put the number in its place."
- **Round-number multiplication** (new short slide, or inside Q14): 99·41 = 100·41 − 41, and 96·104 = 100² − 4². It links to Topic 4 "sum × difference".
- **Choosing plug-in values:** one rule card. "Different letters get different small values (2, 3, 5). Avoid 0 and 1 when the choices have powers or products. Check the conditions."
- Q14: anchor with 63·500 = 31,500 instead of rounding both numbers. It is faster and safer.

### Practice
- Quantity is enough (about 34 items), but it is **very repetitive**. The repeated-bracket question appears 6 times (Q3, extra-03, self-6, q-124, t5-1-6, plus the lesson). The alg-extra "self" and "unit-t5-1" sets are near-clones of each other. extra-08 is a copy of Q10.
- Difficulty is flat: mostly easy to medium, with nothing at exam-hard level.
- Suggest: cut 8–10 clones and add 5 exam-hard items (block value given; plug-in tie; constant expression with a condition; nested fraction with letters; a split-fraction trap).

### Verdict
- **Weak:** Mostly yes, thanks to plug-in. They will still stumble on the undefined exponents in Q11/Q12 and on ":" notation.
- **Medium:** Yes for standard items. Not yet for "value of one expression given another".
- **Strong:** Partly. The methods are strong, but they never practise at exam-hard level.

**Top 3 changes**
1. Fix or remove the "answer = choice number sits in that slot" tip, and make the choices consistent across both topics.
2. Render all practice items as LaTeX fractions (no ":"). Fix extra-07 and the Q8 blank order.
3. Replace duplicate practice with exam-hard items, including "given the value of a block, find another expression". Add a lesson slide on splitting fractions.

---

## Topic 6: Equations — Fundamentals

### Most important points first
1. **The practice solutions ignore the lesson's own shortcut.** Slide 6 ("Ask what they want") says to get x + y directly. But t6-2-3 (x+y), t6-2-4 (x−y) and t6-2-5 (2x+y) are all solved by finding x and y first. Better solutions:
   - t6-2-3: add the equations → 5x + 5y = 55 → x + y = 11.
   - t6-2-4: subtract the equations → x − y = 26 − 29 = −3.

   Solution text like "The requested expression is 2" is also template language. Rewrite it.
2. **The seven t6-2 systems are one template.** All seven are 2x+3y / 3x+2y, only with different numbers. Keep 2, and replace the rest with varied types.
3. **q-143 is harder than anything taught.** It needs the LCD of 5, 3 and 10, plus a minus in front of a fraction: −(x+3)/3 → −10x − 30. This is the classic sign trap, and no slide shows it. Add it to slide 6 ("Fractions & brackets"), or add a guided question.
4. **"As many equations as unknowns — you can solve it"** (Systems slide 2) is said as a rule. Say "usually". Topic 7 has systems with no solution and parameter systems, and a strong student will notice the overstatement.
5. **q-153 wording: "Given: 0 < x, y."** This is unclear English. Write "Given: x > 0 and y > 0."

### Coverage
- Good: isolating x, identity vs. contradiction, x in the denominator with a restriction, not dividing by x, substitution, elimination, and matching coefficients.
- Many exam types (adding three equations, parameters, "how many solutions", hidden identities) are in Topic 7. That is fine, but note these gaps for *this* topic:
  - **Testing the choices** as a general equation method appears only in Q1 Method 2. On NITE it is often the fastest route for single equations. Put it on the recap board.
  - **An extraneous answer among the choices.** Slide 5 says "throw it out", but no practice question has a choice that makes a denominator zero. q-171 has x = 2 as a choice, which is good, but its correct answer is not the trap. Add one item where solving gives the forbidden value, so the answer is "no solution".
  - **Cross-multiplication** is used in q-171, q-154, t6-4-7 and t6-1-5, but it is only mentioned in passing in the Q1 video. Put it on a lesson slide with its condition (fraction = fraction only).
  - **Multiplying or dividing equations** (q-153): (xy)·(x/y) = x² = 36 → x = 6. This is a good NITE shortcut, and it is not shown.
  - t6-1-4 (x+y and xy → x²+y²) is a good exam item, but its solution is one vague line. Show (x+y)² − 2xy = 144 − 70 = 74.

### Teaching quality
**Weak student**
- The lesson pace is good, and the checks ("4·6+7=31 ✓") are good habits.
- Gets lost in elimination when subtracting a negative term. q-162 needs (x+y) − (x−y) = 2y. The rule "keep the whole second equation in brackets" is said once on slide 4 but never drawn. Draw it.
- q-152 (1/x over 3) and q-157 (expand (m+1)(n+1)) jump in difficulty with no guided example.

**Medium student**
- Well served by the two guided system questions, each solved two ways.
- Gap: there is no rule for which method to choose. Add one line: "coefficient 1 → substitution; matching or opposite coefficients → elimination; they ask for a combination → add or subtract first."

**Strong student**
- Bored by t6-4-* and t6-2-* (easy clones).
- Wants: symmetric-system tricks (add, then subtract), testing choices, and "don't solve fully". q-156 (x = 7x → one solution) and t6-1-7 (no solution for k) are the right kind of trap. Add more like these.

### Correctness
- All 53 keys are correct. I checked each one by solving or substituting back.
- t6-4-3 "(x+7)/4 = 12/4" is valid but odd, since the right side is just 3. Write "= 3", or use a real fraction equation.
- The template solutions of t6-2-1 to t6-2-7 do not fit the questions that ask for a combination (see point 1).
- q-153 wording (see point 5).

### Methods to add or change
- **Test the choices** (Recap slide): "Single equation, number choices → substitute from the middle choice. Skip forbidden values."
- **Add and subtract symmetric systems** (after slide 4): x+y = a and x−y = b → x = (a+b)/2 and y = (a−b)/2. q-148, q-162 and t6-1-2 become one-liners.
- **LCD with a minus sign** (slide 6): one worked line, e.g. (6x+4)/5 − (x+3)/3. Put brackets around every numerator before multiplying.
- **Cross-multiplication** (slide 5): show it as the shortcut for "fraction = fraction", with the restriction still written first.

### Practice
- Quantity is fine (about 50 items). Mixed practice (q-139 to q-158) has a good spread and several real exam items (q-156, q-157, q-158).
- Too many easy clones: t6-4-1 to 7, t6-2-1 to 7, and t6-1-1 to 2. q-141 is identical to lesson slide 6.
- Missing hard items: an extraneous-root trap, an LCD with a minus (only q-143), and a "find x+y without solving" question with a solution that uses the shortcut.

### Verdict
- **Weak:** Yes for basic single equations and simple systems. At risk on sign errors in elimination and on q-143-style fractions.
- **Medium:** Yes for this level. Needs a method-choice rule to be fast.
- **Strong:** Will solve everything, but slowly (full solving). The shortcut is taught once and never practised in the solutions.

**Top 3 changes**
1. Rewrite the t6-2 solutions (and add items) so "ask what they want" is actually practised: add or subtract to get x+y or x−y directly.
2. Replace most template clones (t6-2-*, t6-4-*) with varied items: an extraneous root, an LCD with a minus, testing the choices, and multiplying equations.
3. Add lesson content: cross-multiplication (with its condition), a minus before a fraction when clearing denominators, and "usually solvable" instead of the absolute rule.
