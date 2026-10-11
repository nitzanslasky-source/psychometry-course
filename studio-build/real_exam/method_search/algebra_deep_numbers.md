# Deep pass — general methods across divisibility / number properties / exponents / defined ops / number line (108 real Qs)
(No exam text copied; mini-examples are my own.)

## A. "TAG IT" — the guaranteed-factor method for the whole "necessarily divisible / greatest certain divisor / necessarily integer" family  -> WORTH IT (one named method)
Cue: "x is divisible by d", "x is even", "K is a multiple of…", then "necessarily / certainly / greatest number it must divide / necessarily an integer".
Move: translate each condition into a tag: x = d·k (k = unknown whole number, guarantees NOTHING). Then do the asked operation and pull the numbers out front:
  - multiply -> tags multiply;  - add -> only the SHARED factor comes out (factor it);  - divide -> every prime of the bottom must be in the top's tags;
  - "divisible by a and by b" -> the tag is the LCM, not a·b.  The number outside the bracket is the answer; to be sure nothing bigger is guaranteed, one small example.
Mini-example: p is a multiple of 4, q is even. pq = 4k·2m = 8km -> 8. And p+q = 4k+2m = 2(2k+m) -> only 2 (p=4,q=2 gives 6: 6 is NOT guaranteed).
Works on (10): 2021_autumn_q2_14, 2022_autumn_q2_05, 2025_autumn_q2_18, 2025_spring_q2_20, 2019_spring_q1_12, 2021_autumn_q1_17, 2024_winter_q2_18, 2021_spring_q2_19 (+numbers-in-a-row), 2019_spring_q2_17, 2024_autumn_q2_12. Prime-bag version of the same idea: 2025_winter_q2_10, 2024_winter_q1_04, 2026_spring_q2_14, 2023_autumn_q2_16, 2024_autumn_q2_13.
Fails / not needed: remainder questions with small numbers (plug the smallest, e.g. 2022_winter_q2_13), consecutive-product questions (need "numbers in a row" on top), digit puzzles.
Course: PARTIAL, scattered. t14 has the prime-bag idea as "the heart of the topic" ("Break apart / Build / Check: which prime is missing?"). The k-form appears only inside solutions (t15 Q48 "Write n=4k", Q51 "Write y=6k", Q14 video "Write the given as an expression: x equals six k plus three"; t16 "x is even, so x=2k"). The t15 summary's general method for this family is plug-in ("Plug in to knock out — not to prove. Avoid 0") + the smallest-case warning. Nowhere is "add -> only the shared factor survives" stated, and the two real sum questions both offer 6 as a trap.
Fit: one slide/card row in t15 advanced ("Tag it: d·k") + 1 question video on x+y; ~2–3 min.

## B. "GIVEN -> TARGET POWER" for exponents  -> WORTH IT
Cue: an exponent/root equation is given, and the question asks for a DIFFERENT power of the same base (x², a^x, a^(3/2)…), not the letter itself.
Move: target exponent ÷ given exponent = r; raise BOTH sides of the given to r. Never solve for the base.
Mini-example: given ∛b = 5, find b^(2/3): (1/3 -> 2/3) r = 2 -> 25. Given c^(4y) = 81, find c^y: r = 1/4 -> 3.
Works on (6): 2022_autumn_q2_07 (r=2), 2023_winter_q1_05 (r=1/2), 2019_winter_q1_13 (r=3), 2021_autumn_q2_07 (r=4), 2025_winter_q2_09 (r=4, both sides incl. coefficient: 2^4=16), 2020_spring_q1_15 (after dividing, r=4). Related "treat the asked combination as one block": 2021_spring_q2_15 (b−a).
Fails: when the unknown is in the exponent and must be solved (2023_autumn_q2_04 -> equal exponents / try choices).
Course: only the special case target = x: t11 card "x with a fractional power | raise both sides to the reciprocal power | x^(-1/2)=4 => x=4^(-2)" (q-301). No course question asks for a different power of the base (checked all stems in t8–t11). t4 has the general idea for algebra ("Can I find the value without finding x?") but not for powers.
Fit: one row in t10/t11 card + one question video (~1.5 min).

## C. Plug-in rule for INTEGER-condition letters: "multiples of d -> use d and 2d; two letters -> UNEQUAL multiples"  -> BORDERLINE (one line)
Cue: letters with divisibility/parity conditions + "necessarily / greatest certain".
Move: plug two different allowed pairs (x=y misleads); the answer divides every result (common divisor of the results).
Mini-example: m, n multiples of 5, greatest certain divisor of m+n: 5+5=10 (trap), 5+10=15 -> common 5.
Works on: 2025_autumn_q2_18, 2025_spring_q2_20, 2022_autumn_q2_05 (a=b=c kills nothing), 2021_autumn_q2_14, 2019_spring_q2_17 (5).
Course: t20 "Which numbers to plug in" table lists real-number conditions only; it even says "the letters may be equal | also a=b" (the opposite emphasis). t19 tip "avoid 0, 1 and equal values" exists but in defined operations. t15: "The smallest case gives the biggest POSSIBLE divisor, not the answer". Missing: the integer-condition rows. Fit: 2 rows in the t20 table / t15 card. Redundant if A is added.

## D. Digit WORD equations: "number = k × (digit sum)" etc. -> write 10A+B and collect into a digit RATIO  -> BORDERLINE (add as step 0 to the t18 routine)
Cue: a two-digit number described in words (times its digit sum, minus its digit sum, tens digit twice the units…), no column exercise.
Move: 10A+B = k(A+B) -> (10−k)A = (k−1)B -> read the ratio. Bonus fact: a number minus its digit sum = 9 × tens digit.
Mini-example: AB = 7(A+B) -> 3A = 6B -> A = 2B -> 21, 42, 63, 84.
Works on (5): 2024_autumn_q1_15, 2019_winter_q1_17, 2023_winter_q1_15, 2022_winter_q1_07, 2023_spring_q1_02 (list form); also 2023_spring_q2_09.
Course: COVERED in practice (t18 Q24 "AB=6(A+B) … 4A=5B", Q20, q-520 video "Nine T equals U cubed"), card fact "AB=10A+B". But the named 4-step routine ("write vertically / units digit / leftmost & size / plug in") is built for column puzzles and doesn't name this move. Fit: one line in the t18 routine.

## E. "Number" ≠ "integer"  -> BORDERLINE (cheap tip)
Cue: "how many numbers between…" with no "integer". Move: translate the condition (3x integer -> 3x is a whole number in the range) and count those.
Works on: 2023_winter_q1_20 (1 Q; trap answer 1). Course: t1 word table has "Positive | greater than zero (not necessarily whole)", but no "number = any real" row. Fit: one row.

## Families checked and ALREADY taught as one routine (no change needed)
- Defined operations: t19 card is a full routine ("Read the definition first. Then follow it exactly." + 18 situation rows incl. "Property given: put each rule on trial with a test value (not 0 or 1)", "Undoes itself: c−x, c/x … never x², √x, 2x", "Inverse: undo steps in reverse"). All 16 real Qs fit it.
- Column digit puzzles: t18 4-step routine + facts card (AB±BA, ABC−CBA=99(A−C), AAA=111A, units digits). ~10 real Qs fit.
- Exponent simplification: t10 card "Different bases | write every base as the smallest prime" (+ "Pair the families"). ~8 real Qs fit.
- Roots size/estimation: t9 "put it between two perfect squares", t11 estimation videos.
- Parity/sign: t16 card "Plug in 2 for even and 1 or 3 for odd… For division, plug in three times"; t1 "0 is even".
- Remainders: t15 "N = dk + r", "N − r divisible", change-the-divisor rule, units-digit cycles.
- Cycles / "who gets the last": t21 "divide by the cycle length and look at the remainder… Remainder zero? Then it's the LAST one". Meetings -> LCM (t14).
- Must/could/cannot logic: t20 card table.
- Plug-in / try choices / tie -> plug again: t51, t10 tip, t4 board.
