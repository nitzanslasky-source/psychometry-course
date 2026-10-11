# Deep pass: general methods across inequalities_absolute (35) + equations (33) + algebraic_expressions (32)

The 100 questions split into 4 families. Each family can be taught as ONE short routine.
"Course" says where the course teaches it and how: as a named method (N), only inside one solution (S), or not at all (NO).
The mini-examples are my own, not exam text.

---------------------------------------------------------------------------
## 1. POWER COUNT (degree check), plus the leading coefficient  — NEW, strongest candidate
Cue: letters in the choices, and the question's expression is "balanced": every term has the same number of
letter-factors (a/b counts 0, ab counts 2, 1/x counts -1). Or the question is a word problem with units.
Move: count the power of the question's expression. Cross out every choice with a different count, or with a
mixed count (like 1 + z, or a + a^2). Two or more survive? Compare the coefficient of one leading term
(set the other letter to 0) instead of plugging in again.
Mini-example: (x^2 - y^2)/(x + y) + y = ?   choices x · x^2 · x + 1 · 1/x
  The power is 1 (2 - 1). x^2 (power 2), x+1 (mixed) and 1/x (power -1) are out. Answer x, in about 5 seconds.
Second job: it BREAKS TIES after a plug-in, with no re-plug. Ties with 1s are common.
Works (kills at least 1 choice):
  2021_autumn_q1_15  (question power -1; choice 4 has power -2, so it is the answer: SOLVED alone, and the all-1s plug ties here)
  2025_winter_q1_08  (power 0: kills 3 and 4; b=0 then finishes)
  2020_autumn_q2_16  (power 0: kills 3 and 4; it also breaks the 2-vs-3 tie at a=2, b=1)
  2023_spring_q1_13  (power 2: kills 3 and 4; then the a^2 coefficient 1/4 picks (a/2+b)^2: SOLVED, no plug)
  2020_winter_q2_13  (power 2: kills choice 1; it also breaks the tie at x=y=1)
  2020_winter_q1_15  (power 2: kills t-q)
  2023_winter_q1_02  (power 2: kills the constants 1 and 4; it also breaks the tie at y=1)
  2025_spring_q1_07  (all choices have power 2, so the count kills nothing; the leading coefficient finishes it:
                      x^2 coefficient 8*16=128, only 8(16x^2-y^2): SOLVED)
  2020_autumn_q1_02  (units: rooms = floors x rooms per floor; (x-y)^F and /F make no sense: SOLVED)
  2024_autumn_q1_06  (big-number version: a^3 is about b^3, so a grows like b; kills b^2+1, b^3, b^3-1. For strong students only)
  2019_winter_q1_15  (z behaves like 1/x, so "x - z" and "1 - 3z" are mixed; kills 2. Too advanced to teach)
Fails (every choice has the same power, or the expression is not balanced): 2024_autumn_q2_11, 2019_winter_q2_14,
  2023_winter_q2_06 (has +-1 constants), 2019_winter_q1_02, 2023_winter_q2_15, 2021_autumn_q2_03, 2020_spring_q1_08.
Course: NO. "degree" appears only as "second-degree inequality" (t12) and in geometry. The old written solutions
  never use it. Plugging in is taught well (t5, t51), but the only tie advice is "A tie? Keep only the tied choices
  and plug in new numbers" (t5 card / video).
Verdict: WORTH IT. In this group alone it helps on about 10 letter-choice questions, solves 4 outright, and
  breaks 4 of the 5 plug-in ties I hit. It probably also pays off in defined operations and letter word problems
  (units). Fit: t5 "Advanced expressions", a ~3 min video "Count the powers before you plug in". Add one t5 card
  tip: "Tie? First check the powers."

---------------------------------------------------------------------------
## 2. MIRROR TEST (symmetry)  — NEW as a tool; only hinted at in t51
Cue: the givens do not change when you swap two letters (x<->y), or flip every sign (x,y -> -x,-y), or swap two
roles in a story (milk <-> cheese).
Move: the mirror of any legal example is also legal. So a choice that changes under the mirror cannot be
"necessarily true", and cannot be the formula for a quantity the mirror leaves unchanged. Cross those choices out
without numbers.
Mini-example: Given x^2 + y^2 = 10. Necessarily true?  x>0 · x<y · x+y>0 · x^2<=10
  Flipping all signs keeps the given but breaks x>0 and x+y>0. Swapping x,y breaks x<y. Answer x^2<=10.
Works:
  2021_autumn_q2_15  (sign flip: y, x+y, x-y change sign; only xy survives: SOLVED with no numbers)
  2024_spring_q2_18  (sign flip kills x+y<0, x<y, y<x: SOLVED)
  2024_spring_q2_04  (sign flip turns M into -M, so "M>0" is out)
  2023_winter_q2_15  (milk<->cheese swaps m and n, bread stays; k+n-m and m-(k+n) are not symmetric, so out; 2 kills)
  2024_autumn_q2_11  (symmetric in a,b; 4a^2/b^2 and the 2a/b version are not, so out; 2 kills)
  2019_winter_q2_14  (swapping b,d swaps x,y and keeps z; y-x is out)
  2023_winter_q2_06  (x -> -x leaves the expression unchanged; (2x+1)/(x^2-1) does not, so out)
  2019_winter_q2_17  (b<->c: |b|-|c| is out)
  2020_autumn_q2_13  (counting: flipping both signs gives the same |x-y|, so only 2 cases to check)
Fails or misleads: 2021_autumn_q1_15 (a "which is NOT equal" question where the correct, equal choices LOOK
  unsymmetric. Teach "mirror-check simplified forms only"). No help when every choice is symmetric:
  2020_winter_q2_13, 2025_winter_q2_05, 2020_autumn_q2_19, 2022_autumn_q1_14.
Course: hinted only. t51 checklist: "Is part of it negligible, shared, or symmetric?" (dice example). t6: "When
  the numbers look symmetric like this, try adding and subtracting first." The t13 card states the RESULTS for
  |x+y|<|x-y| and |x+y|=|x|-|y| as facts to memorize, not the move that finds them. The old written solutions use
  "swap" on 2021_autumn_q2_15 and 2024_spring_q2_18 only.
Verdict: WORTH IT (borderline-strong). It helps on 9 questions here, 2 solved outright. Fit: t13 advanced or t20,
  a ~2-3 min video "The mirror test". Then the three memorized t13 rows become examples of one move.

---------------------------------------------------------------------------
## 3. RANGE QUESTIONS: ENDPOINT + DIRECTION  — the pieces are taught, not as one routine (a "V"-style framework)
Cue: "exact range / which values can x take", and the choices are intervals.
Move (2 steps):
  (1) ENDPOINT: turn the given into an equation (or put in the extreme legal values / corners). The right choice
      must have that endpoint. Usually 1-2 choices survive.
  (2) DIRECTION: test one easy legal number (0, 1, a big number). Or test an ILLEGAL number: a choice that
      contains it is out.
  It never multiplies by a negative, never flips a reciprocal, and never builds a sign table, which are the 3
  places students slip.
Mini-example: 5 - 2x > x - 4.  Endpoint: 5 - 2x = x - 4, so x = 3. Direction: x = 0 gives 5 > -4, legal, so x < 3.
  Reciprocal version: 1/x < 1/3, x != 0. Endpoint 3. x = 1 gives 1 < 1/3? No, so 1 is out. x = -1 gives -1 < 1/3?
  Yes, so the negatives are in. Answer: x < 0 or x > 3.
Works: 2022_autumn_q2_12, 2019_spring_q1_06, 2025_spring_q2_06, 2025_autumn_q1_16, 2023_winter_q2_10 (endpoints 0
  and 2; test -5), 2026_spring_q1_17 (endpoint 2; the illegal x=1 kills 3 choices), 2019_winter_q2_07,
  2020_spring_q1_18, 2023_autumn_q1_07, 2020_winter_q2_14, 2024_spring_q1_03, 2022_winter_q1_15, 2020_spring_q2_14
  (endpoints b/2 and 2b/3, once b>0 is known).  13 questions.
Fails: nothing here, but 2023_winter_q2_10 has a "touch" endpoint (x=0) that is not a switch, so test both sides.
Course: pieces only. t12 Q1 video: "A ten-second check: plug in x equals zero ... only choice three does" (used in
  one solution). Traps card: "Range of a-b: biggest a minus smallest b"; "Range of ab: check the four corners".
  Card tip: "Answer choices to test? Plug them in — often the fastest route." Solving the inequality is taught
  first; "endpoint first" is not named.
Verdict: WORTH IT as an organizing slide plus one card row (~2 min in t12 Summary). It does not save much time on
  easy linear ones. Its value is preventing flip/sign errors on the fraction, reciprocal and negative-coefficient
  ones (2025_autumn_q1_16, 2026_spring_q1_17, 2019_spring_q1_06, 2020_spring_q1_18).

---------------------------------------------------------------------------
## 4. "MUST / COULD / CANNOT" with conditions: REGION -> ONE LEGAL EXAMPLE -> ITS MIRROR
Cue: sign/order conditions (a<0, |x|>..., a<b) plus "necessarily / could / cannot".
Move: (1) Read the conditions as a picture on the number line (signs, which is farther from 0). (2) Build ONE
  legal example: choose the free letter first, then solve the other from the given, near a boundary if possible.
  (3) Check all 4 choices. (4) If more than one survives, use the mirror (section 2) or an extreme example.
Mini-example: |a + b| < b. Choose b = 1, so a + b is between -1 and 1, so a is between -2 and 0; take a = -1.
  Example (a,b) = (-1, 1). Every choice false for it is gone.
Works: 2023_spring_q1_08 (one example kills 3), 2025_spring_q1_19 (a=1, b=-1 on the boundary kills 3),
  2024_spring_q2_18, 2021_autumn_q2_15, 2026_spring_q2_10, 2021_autumn_q1_16, 2020_autumn_q2_19,
  2020_autumn_q1_13, 2019_spring_q2_14, 2025_winter_q1_01, 2024_spring_q1_03, 2022_winter_q2_16, 2020_spring_q2_08,
  2024_winter_q1_05, 2022_autumn_q1_06.  About 15.
Fails: 2021_spring_q1_15 (wording: the English "not necessarily true" is keyed as "cannot be true"; the method
  works once the wording is read correctly).
Course: N (taught well). t12 video "Must, could, cannot ... Find one number where it fails — and it's out"; the t13
  "Question wordings" card; t12 "Numbers to try: 0, 1, -1, 1/2 and a big number". Missing: HOW to build a legal
  example fast (free letter first, then solve the other; aim at the boundary). The course lists numbers to try
  but not how to make them obey a condition like |a+b|<a.
Verdict: the course covers this. Add one line: "Build the example: choose one letter, solve the other from the
  given; choose near the edge to kill more."

---------------------------------------------------------------------------
## 5. TARGET-FIRST (asked for an expression, not the letters)  — taught well
Cue: they ask for x+y, 2x-y, y(x+1), a sum of ages, s^2-r^2, a price; or there are more letters than equations.
Move: write the target, then build it from the givens (scale, add or subtract equations, a block, an identity).
  Can't see it? Pick ONE LEGAL SOLUTION (see 6).
Works: 2020_autumn_q1_01, 2021_spring_q2_06, 2023_spring_q1_04, 2024_spring_q1_18, 2020_spring_q1_16, 2022_autumn_q1_14,
  2020_spring_q2_01, 2024_winter_q2_05, 2021_autumn_q2_09, 2025_winter_q2_05, 2021_spring_q1_07, 2023_winter_q2_15,
  2020_winter_q1_15, 2024_autumn_q1_14, 2021_spring_q1_03, 2019_winter_q2_17, 2025_autumn_q2_17 (cancel xy).  17.
Course: N. t5 "Exam Shortcuts": "Look for the block inside the question ... The trap is trying to find x and y."
  t6 card: "They ask for x+y, x−y, 2x+y … add or subtract first; you may not need x and y". t4 card: "find values
  without finding the letters". t7 card: "A letter missing from the answers — Make that letter cancel".
Verdict: already covered. Nothing to add.

---------------------------------------------------------------------------
## 6. ONE LEGAL SOLUTION (zero out a letter)  — used in solutions, never named; t51 seems to forbid it
Cue: an equation (or system) with MORE letters than equations, and a NUMBER is asked (or number choices).
Move: the answer is the same for every solution, so take the easiest one. Set one letter to 0 (or 1) and solve
  the equation for the other.
Mini-example: 4x + 6y = 18. Find 6x + 9y.  y = 0 gives x = 4.5, so 6x = 27.
Works: 2020_autumn_q1_01 (y=0), 2021_spring_q2_06 (y=0), 2022_autumn_q1_14 (one age = 0: 3b+9=69, sum 20),
  2021_autumn_q2_09 (b=0: a^2/2=8), 2021_spring_q1_07 (d=e=1), 2025_winter_q2_05 (x=0, y=-2),
  2024_winter_q2_05 (y=0), 2020_spring_q2_01, 2023_winter_q2_15, 2024_spring_q2_04.  About 10.
Fails: 2020_spring_q1_16 (no easy legal pair: a cubic; aim at the target instead), 2023_spring_q1_04 (fully
  determined: just add).
Course: S. t5 uses it as a check: "Check with numbers that obey the given: x is five, y is zero." and "Don't see the
  block? Plug in — but only numbers that obey the given." BUT t51 "Plugging In Numbers" says: "Equation: something =
  something → do not plug in ... There, x has one specific value; I can't choose it." For one equation with two
  letters that is false. A literal student will skip the fastest route on these ~10 questions.
Verdict: WORTH IT, as a cheap fix. Qualify the t51 slide ("one letter, one equation: don't plug in; more letters
  than equations: choose one letter, solve for the rest") and add one t5/t6 card row. ~1 min, no new video.

---------------------------------------------------------------------------
## 7. KNOWN-SIGN PIECES  — taught as rules; it could be named as a cue
Cue: a piece whose sign you already know: |x|, x^2, a letter given positive, a denominator like 2a+1 with a>0,
  a letter given non-zero. Or a letter both inside and outside bars (x+|x|, |x|-x).
Move: strip it (divide by it, or use >=0 as a bound). Then the question is about the rest. x+|x| is 0 (x<=0) or 2x.
  |x|-x is 0 (x>=0) or -2x.
Mini-example: x^2(3 - x) > 0, so x != 0 and x < 3.  And |x| + x = 8, so x = 4.
Works: 2025_autumn_q1_16, 2023_winter_q2_10, 2020_autumn_q1_13, 2023_spring_q1_08, 2020_spring_q2_14, 2020_winter_q2_08,
  2022_winter_q1_15, 2019_spring_q2_14, 2021_autumn_q2_03, 2023_autumn_q2_03, 2024_winter_q2_06, 2025_autumn_q2_01,
  2020_spring_q1_02.  13.
Course: N/S. t12 card "Multiply by an unknown — only if you know its sign"; t7 card "Divide by p only if p≠0.
  Otherwise factor"; the t13 card has |x|>=0 and the |x|=x / |x|=-x rows; x+|x| and |x|-x appear only inside t13
  Q17 / Q21 solutions.
Verdict: BORDERLINE. Covered in substance. Optional: one t13 card row "x+|x| = 0 or 2x; |x|−x = 0 or −2x" (3 questions).

---------------------------------------------------------------------------
## One-offs (not worth it)
- Largest |±sum|: make every term the same sign, flipping the minority (2021_spring_q2_11).
- Size elimination for equation choices: x/(x+k) < 1 for x > 0 (2022_autumn_q1_13).
- Difference of cubes (2024_autumn_q1_06): a plug or the power count is faster.
- Points given by distances need not lie on one line, so the minimum can be 0 (2022_autumn_q1_19). This one is a trap: add a line to the t31 card.

## A suggested "letters" routine to teach (ties 1-6 together, V-style)
  ASKED?  -> target-first / one legal solution            (sections 5, 6)
  SHAPE?  -> power count, mirror, known signs: cross out without numbers   (sections 1, 2, 7)
  PLUG    -> legal numbers on the survivors only; tie -> SHAPE again before re-plugging
  RANGE?  -> endpoint + direction                          (section 3)
