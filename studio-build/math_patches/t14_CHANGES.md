# Topic 14 — Prime Numbers: changes

Patch: `math_patches/t14.py`. Check: `python3 math_check.py 14` shows 0 problems, 0 warnings and 0 layout problems (70 slides checked).

## Summary
- Questions: 41 rewritten, 15 added (4 guided with solution videos and 11 practice), 3 removed.
  The topic had 44 questions (17 guided and 27 practice). It now has 56 (21 guided and 35 practice).
- Order: the GCD question (old Q4) and the "greatest guaranteed divisor" question (old Q5) now come right after the "Factor Tools" lesson and its card. Before, they came before these ideas were taught.
- The guided questions are renumbered automatically in course order: 4 in theory A, 7 in theory B, and 10 in the advanced section.
- Lesson "Prime Numbers": 5 slides changed, 1 slide added ("Is it prime?").
- Lesson "Factor Tools": 7 slides changed, 1 slide added ("GCD vs LCM", a table).
- New lesson video: "More Factor Tools" (6 slides, about 3.3 minutes). It is the first item of the advanced section.
- New solution videos: 4. Changed solution videos: 6 (old Q4, Q5, Q6, Q11, Q12 and Q15).
- Memory cards: 2 updated, 1 new ("More factor tools").
- Figures: none in this topic.

## 1. Wrong or misleading teaching (fixed)
- **"Prime Numbers", slide 2:** deleted "The primes are the small numbers you never meet as an answer inside the times table." This was false.
- **GCD and LCM rule:** the vague words "offset it", "count it once" and "shared ones once" are gone everywhere. That includes lesson slide 3, the recap, the card, and the old Q5 video. The rule now reads:
  - **GCD:** each shared prime, at its LOWER power.
  - **LCM:** every prime, at its HIGHER power.
  - The official names (greatest common divisor, least common multiple) are said and written. The course also says that the "greatest guaranteed divisor" is the LCM.
- **Recap mismatch:** the teacher used to underline "counted once", but the board said something else. The recap is rewritten, and the teacher now underlines "LOWER" and "HIGHER".
- **Old Q4 video:** it used "least common multiple" before the course taught it. It now comes after the lesson, and it says "lower power" and "the trap is the higher power: that's the LCM".
- **Solution texts fixed:**
  - q-420: removed "it is always integers". The question itself was removed as a duplicate.
  - q-422: the confusing "product … divided by nothing" sentence is gone.
  - extra-t14-4-2: now "take each prime at its higher power: $2^2\cdot3^2=36$".
  - extra-t14-4-1: now shows the GCD with the primes.
  - extra-t14-4-4: now uses a taught idea. The divisors of a prime $p$ are only $1$ and $p$, and $p$ leaves remainder $1$ in $2p+1$. The "divides the difference" idea is no longer needed.

## 2. Methods added
**Lesson "Prime Numbers"**
- **Slide 3 "0, 1 and 2":**
  - $0$, $1$ and negative numbers are not prime.
  - New board line: "Odd sum or difference of two primes → one is 2". It also explains odd + odd = even. This parity idea is used in old Q11, q-412 and q-415, and T16 comes later.
- **New slide 5 "Is it prime?":**
  - The √n test, with 91 as the example.
  - The digit-sum test for 3 (T15 comes later).
  - A list of fake primes: 51, 57, 87, 91, 119.
- **Recap:** it now has the parity line and the √n line, and it says "Four questions next".
- **Card:**
  - The primes table now goes up to 60.
  - New facts: 0/1/negatives, parity, √n.
  - New table of fake primes (51, 57, 87, 91, 119, 133).
  - New tip: the digit-sum test for 3.

**Lesson "Factor Tools"**
- **Slide 2 (GCD):** the lower-power rule, shown step by step for 72 and 90.
- **Slide 3 (LCM):** the higher-power rule, shown step by step for 72 and 90.
- **New slide 4 "GCD vs LCM":**
  - A table of 72 and 90, one prime per row, with the lower-power and higher-power columns.
  - GCD × LCM = a × b, checked: 18 · 360 = 72 · 90 = 6480.
  - The trap: multiplying the two numbers.
- **Break & build:** a named method for letter questions (old Q14). "Letters as primes? Plug in 2, 3, 5, 7, then check every choice."
- **Symmetric divisors:** now uses the general rule. An odd number of divisors means a perfect square (36 has 9 divisors). "Exactly 3 divisors → prime squared" is the common special case.
- **Recap and card:** rewritten to match. The card has 6 rows and 3 tips, including the "multiply them" trap and plugging in small primes. The recap says "Then seven questions".

**New lesson "More Factor Tools"** (advanced section, before the old advanced questions)
1. Perfect squares and cubes by exponents: 18k a square → k = 2; 18k a cube → k = 12.
2. Prime equations by unique factorization: 2ᵃ·3ᵇ = 72; p²q = 50 (with the "which one is squared" trap).
3. Zeros at the end: pairs of 2 and 5. For example, 2⁵·5³·7 = 28,000.
4. A prime that divides a product divides one of the factors. The counterexample for non-primes: 6 divides 4·9 but neither 4 nor 9. Old Q15 needs this.
5. Recap. A new card, "More factor tools", comes right after the lesson. Its tips include "never true is also not necessarily true".

**Old Q15 video:** new closing lines. "Statement four is NEVER true. Never true is also 'not necessarily true'."

**New guided questions**, each with a solution video:

| New # | id | Question | Answer | Method |
|---|---|---|---|---|
| Q4 | q-r26-t14-01 | Which is prime: 91, 119, 113, 133? | 113 | √n test; all 3 fakes divide by 7 |
| Q12 | q-r26-t14-02 | smallest k with 24k a perfect cube | 9 | exponents divide by 3 (traps: 6 gives a square, 72 is not the smallest) |
| Q13 | q-r26-t14-03 | 2ᵃ·3ᵇ = 108, a − b = ? | −1 | break and match (trap: swapping gives 1) |
| Q14 | q-r26-t14-04 | zeros at the end of 20⁴·15³ | 7 | pairs of 2 and 5 (traps: 4, 8) |

**Strong-student tricks, taught explicitly:**
- Plug in the smallest primes: Break & build slide, and the card.
- Try the choices: already in old Q12 and Q14, and used in the new Q4 video.
- GCD × LCM as a shortcut and a check.
- The √n test and fake primes.
- Parity of two primes.

## 3. Text (all 41 existing questions)
- Every stem, choice and solution is now in TeX. No ":" is used for division: q-387, q-396 "280:35", q-408, q-417 "n:d" and q-421 are fixed. The extras' plain-text choices are now TeX.
- Board slide 6 of "Prime Numbers": "20 : 4 = 5" is now "20 ÷ 4 = 5", and the same for 30 ÷ 6. The spacing in the "Counting divisors" draw notes is fixed. The board "9: 1, 3, 9" is now "Divisors of 9: 1, 3, 9".
- **Stacked conditions:**
  - q-389 (x and y), q-393 (a < b and the equation) and q-399 (xy = 36 and A = |x − y|) use `cases`.
  - q-392, q-394, q-395, q-397, q-402, q-409 and q-414 show one given per line.
- **Rewording:**
  - q-396: "The prime factors of a are 2 and 5 only" is now "a has exactly two prime factors: 2 and 5". It now asks for "the smallest possible value of $\frac{a\cdot b}{35}$".
  - q-401: "What is correct to say about y?" is now "Which of the following is necessarily true?"
  - q-400: now says "each number at most once".
  - q-407: adds "x > 44".
  - q-415: the needless "1 < p" is removed.
  - The extras now use NITE-style stems ("What is the GCD of …?").
- The word-only extra solutions now show the numbers.
- The solutions use the taught methods: lower/higher power, √n, pairs of divisors, and parity of two primes.
- Every mid-sentence "so" is now "therefore".
- The solution-video titles and preloaded-question notes match the new stems.

## 4. Figures
None in this topic.

## 5. Practice
**Removed (near-duplicates):**
- q-416 ("t² is prime", the same as guided Q10)
- q-420 (the third "exactly 3 divisors" item)
- q-410 (GCD with letter primes, the same as guided Q5)

**Added:**

| id | Question | Answer |
|---|---|---|
| q-r26-t14-05 | how many primes between 80 and 100 | 3 (83, 89, 97) |
| q-r26-t14-06 | sum of the primes between 50 and 60 | 112 (fakes 51, 57 give 163, 169, 220) |
| q-r26-t14-07 | 1 < n < 120, not divisible by 2, 3, 5, 7 → necessarily | n is prime (exam-hard) |
| q-r26-t14-08 | GCD 6, LCM 180, one number 36 → the other | 30 |
| q-r26-t14-09 | LCM of p³q and p²q⁴ | p³q⁴ |
| q-r26-t14-10 | smallest k with 2³·3⁴·5·k a square | 10 |
| q-r26-t14-11 | smallest m with 2⁴·3²·m a cube | 12 |
| q-r26-t14-12 | p²q = 75, p + q | 8 |
| q-r26-t14-13 | 6ˣ·5ʸ = 1080, x + y | 4 (exam-hard) |
| q-r26-t14-14 | zeros at the end of 1·2·…·20 | 4 (exam-hard) |
| q-r26-t14-15 | 14 divides ab → necessarily | 7 divides a or b (exam-hard) |

**Order:** the practice runs from easy to hard. The easy extras come first. The exam-hard items come last: q-407, 13, 14, 15, q-415, q-417, q-422, 07, q-408 and q-421. That makes 10 exam-level items.

Every new or changed answer was checked by hand and by brute force.

## Not done / for the teacher to decide
- **Parity (T16) and the digit-sum test for 3 (T15)** are taught here in one or two lines each, because this topic needs them first. If T15/T16 move before T14 (PLAN.md suggests T16 before T15), these lines can stay as reminders.
- **Recording length:**
  - "Prime Numbers": about 6.3 minutes (it was 4.7).
  - "Factor Tools": about 5.2 minutes (it was 3.4).
  - The new "More Factor Tools": about 3.3 minutes.
- **The q-389 stem on the slide** is drawn in a smaller font, because the stacked `cases` block makes it tall. It is readable, but check it in the recording.
- **Module numbers:**
  - The moved Q4 and Q5 solution videos now belong to the "Factor Questions" group (module 42).
  - The new lesson shares module 43 with the "Advanced Primes" group, because the API has no way to create a new module number.
- **"Primes near the target" strip (2 to 60):** added to the memory card as a table, not as a separate slide.

## Pass 2 (teacher-approved remove/restore plan, 2026-09-27)

**Removed** (not on the real exam and not in the original course: zeros at the end of a number, perfect cubes, finding a number from its GCD and LCM):
- Video "More Factor Tools": slide "Zeros at the end", its sidebar label and its Recap line. The slide "Squares & cubes" lost its cube lines and is now called "Perfect squares". The title and recap now say "three tools".
- Guided q-r26-t14-02 (24k a perfect cube) and q-r26-t14-04 (zeros of 20⁴·15³), with their solution videos. The advanced guided questions are renumbered (the prime-equation question is now Question 12, q-391 is Question 13).
- Practice q-r26-t14-08 (GCD 6, LCM 180 → the other number), q-r26-t14-11 (cube), q-r26-t14-14 (zeros of 20!).
- Card "More factor tools": rows "Perfect cube" and "Zeros at the end"; intro now "Three tools".

**Kept:** q-r26-t14-10 (smallest k so that 2³·3⁴·5·k is a square).

**Restored** (3 original questions, text clean-up only: TeX, stacked givens, full numeric solutions; same choices and key):
- q-416 (t > 1, t² prime → t is not an integer), q-420 (exactly three divisors → √m is prime), q-410 (GCD of p²q³r and p³qr² = p²qr).
- They are back in the independent practice at matching difficulty (q-410 with the GCD/LCM items, q-416 and q-420 next to q-417).
- The recap lines "Know the primes up to 40 — and 97" and "Divides by every combination of its prime factors", the two `mem-primes` tips and the `mem-factor-tools` tip ("Divides by 2 and 5 → by 10 …") that the plan lists were already present in the pass-1 patch, so nothing more was needed.

**New: summary video** `r26-t14-summary` "Prime Numbers — Summary", at the end of the advanced section, right before the independent practice (about 2.6 minutes).
Slides: Summary · What a prime is · Two primes, odd result · Is it prime? · Break it down · GCD and LCM · Counting divisors · Squares and equations · A prime in a product · Before you practice.
It only repeats what the three lessons teach. The last slide lists the checks (broke it into primes? really prime - tried up to the root and 7? odd sum → one prime is 2? GCD or LCM - lower or higher power?) and the traps (calling 1 a prime, forgetting 2, multiplying instead of taking the LCM).
