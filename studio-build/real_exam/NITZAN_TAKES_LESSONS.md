# Lessons from Nitzan's English takes: where she struggled, and what flowed best

**Source.** All 189 takes were read in full against the script she was reading (v19-hybrid). That is 34 lessons, 154 solutions and 1 lesson that has since left the studio. Every stumble was logged with its second in the take and its cause. The per-video lists are in `scratchpad/tstyle/added_by_nitzan.json` (fields `struggles` and `flow_model`).

**Why it matters.** All her non-first videos will be re-voiced by the AI. The AI scripts must:
- carry over her good improvisations;
- write a better script line wherever she struggled.

The AI has no ear for "that came out wrong". It reads whatever the script says.

---

## 1. The numbers

| | Count |
|---|---|
| Struggle spots logged | **378**, in 163 of 189 takes (26 takes are clean) |
| Unclear explanation (sentence tangles, meaning unclear) | 159 |
| Real math slip said aloud | 75 |
| Self-correction ("sorry", "no, the opposite") | 73 |
| Restart of a sentence | 33 |
| Lost her place (board, or a beat run together) | 32 |
| Long hesitation / "wait" | 6 |

**Where they cluster.** Causes are tagged by keyword, and one spot can carry several tags.

| Cause | Mentions | What happens |
|---|---|---|
| **Negatives, signs, "bigger/smaller"** | 138 | "the negative 6 is bigger than 4", "always positive" for "never negative", 2·(−2) = 4, "3x is positive" for "zero or positive" |
| **Reading a formula or bracketed expression aloud** | 71 | (√21+√6)², 3(m−n)−(m−n), \|x\|+\|y\| vs \|x+y\|, "A minus B plus, times A plus B" |
| **Roots ↔ powers conversion** | 61 | her "the power is dominant / the root is on top" mnemonic flips the rule |
| **Improvising past the script** (own example, own method) | 38 | 6×7 = 56; 36/√4; "can't multiply by x"; an old method instead of the script's |
| **Board out of sync with the script** (older version) | 34 | q-095, q-096, q-097, q-099 and parts of roots: her numbers don't match the board |
| **Logic words** (necessarily / or / must / at most) | 27 | "at most 3… so less than 3"; "it doesn't mean that that's enough for it to just be −1. But it doesn't mean for sure…" |

**Lessons struggle far more than solutions.** All 10 of the most-struggled takes are long lessons (7-26 min):
- linear-equations, roots, compare-fractions, r26-t04-formulas, exponents
- fraction-multiply, expression-basics, primes, decimals, fraction-add

In solutions, the struggles sit at one dense step each.

---

## 2. The top 5 struggle spots (these need the best new script lines)

### 1. Roots ↔ powers conversion: `roots` [1100-1162] and the recap [1462-1474]; also `solve-q-294` [52, 155], `r26-t09-01` [22], `r26-t11-13` [34]
- **What she said:** "when I'm converting it to roots, the root is on top … a root of 5 over 2". Later: "the root is dominant … 5 to the power of 6 over 3, which is actually 2".
- **What went wrong:** her private "dominant" mnemonic turns the rule upside down. She repeats it in the recap, so a student would learn it as the rule.
- **Script fix:** one exact rule, said the same way every time: "The power goes on top, the root goes on the bottom. So the fourth root of x cubed is x to the power of three quarters." Then give one worked example each way. Never use "dominant".

### 2. Absolute-value inequality, case 2: `solve-q-370` [62-106]
- **What she said:** for |x| < 12 − x, she negated the wrong side: "x will be smaller than minus 12 plus x… is minus 12 bigger than zero? No… just got me nowhere".
- **What went wrong:** she dropped the case with wrong reasoning. Her final answer (x < 6) is right only by luck.
- **Script fix:** split into two explicit cases with numbers:
  - "If x is 0 or more, x < 12 − x, so x < 6."
  - "If x is negative, −x < 12 − x, so 0 < 12. That's always true, so every negative works."
  - Then "Put them together: x < 6."

### 3. Equations with x in the denominator and "don't divide by x": `linear-equations` [597-682], [917-1062], recap [1294]
What went wrong:
- She "cross-multiplied" identical denominators, then divided by (x − 2): a long, risky route.
- She recorded the whole divide-by-x beat twice.
- In the recap she said "I can't **multiply** by x unless I was told x ≠ 0". The rule is about dividing.

Script fix:
- Say the restriction first, as its own line: "x can't be 2, because the bottom would be 0."
- Then: "Same bottom on both sides, so the tops must be equal."
- In the recap, write the exact sentence: "You can't **divide** by x unless you know x isn't 0."

### 4. Expanding a square of a sum of roots aloud: `solve-q-295` [80-96]; the same problem in `r26-t04-formulas` [218-359] and `solve-q-130` [159-243]
- **What she said:** "21 plus six plus 21 plus six plus 21. Times two times six, right? Because I have two times square, sorry, times the root of 21 times the root of…"
- **What went wrong:** formulas with brackets, coefficients or several bars cannot be followed aloud.
- **Script fix:** spell every term on its own short line, in order, with a name:
  - "First squared: root 21 squared is 21."
  - "Second squared: root 6 squared is 6."
  - "Twice the product: 2 times root 21 times root 6, that's 2 root 126."
  - For brackets, say "3 times, in brackets, m minus n". Never leave a bracket unspoken.

### 5. The "in-between fraction" (mediant) and the benchmark: `solve-q-099` [338-381]; `r26-t03-summary` [88-122]
- **What she said:** "So it says if I'm like adding a fifth… I'm not actually adding a fifth… So it's not true that I'm saying that I'm adding a fifth". This loops for about 40 seconds. In summary: "for this to be a half, it needed to be just under that. Just over it, 9.5", and "the smaller the **numerator**, the bigger" (she meant denominator).
- **What went wrong:** a compressed one-line idea with no exact sentence. She tries to invent the explanation live, while pointing at fractions that have no names.
- **Script fix:** give it a name and two concrete lines:
  - "Take 1/3 and 1/2. Add tops, add bottoms: 2/5. And 2/5 always lands between them."
  - For the benchmark: "Half of 13 is 6.5. 6 is under it, so 6/13 is less than a half. Half of 19 is 9.5. 10 is over it, so 10/19 is more than a half."

**Close runners-up.** The fix is the same in each case: write the exact sentence.
- `primes` [474-530]: she never says that 20 does **not** divide 150 (150 has only one 2). A student may conclude that it does.
- `solve-q-366` [116-176]: she argued choice 4 the wrong way before using the given, and said "reciprocals" when she meant opposites.
- `fraction-multiply` [345-408]: "6 times 7, which is 56", reaching 4⅔ instead of 7/2. This is an improvised multiply-first route.
- `solve-q-290` [111-130]: the "or" logic of the exponent cases.
- `absolute-value` [53]: "absolute value can always be positive".
- `solve-q-r26-t06-02` [76]: "2 times minus 2, which is 4".

---

## 3. What the struggles teach about writing AI scripts

1. **Dense lines produce improvisation, and improvisation produces slips.** Nearly every real math slip came where the script gave a headline but no exact sentence: a bare rule, a "→", a one-word contrast. She does not misread full sentences.
2. **Write every contrast as two parallel lines, with numbers.** Her clearest moments are parallel pairs ("False means no x. True means every x."). Her worst are contrasts squeezed into one sentence ("A plus B will be either smaller or equal to A plus B, when they're separate, the absolute value").
3. **Spell out brackets, bars and roots in words.** The listener cannot see the board when the AI reads a formula.
4. **Treat sign words as dangerous.** Write "smaller (more negative)", "further from zero", "never negative", "zero or positive". Never write "bigger" for a negative number without saying what you mean.
5. **Don't let a mnemonic replace the rule.** State the rule exactly, then the image.
6. **Recaps must repeat the teaching sentence word for word.** Three of her worst slips are in recaps: linear-equations, roots and exam-words.
7. **Old-version takes need fresh numbers.** In these takes, her improvised examples cannot be pasted as they are:
   - q-095, q-096, q-097, q-099
   - parts of roots, q-133, r26-t02 and fraction-multiply

   Each one is flagged in `added_by_nitzan.json`.

---

## 4. What flowed best: models to imitate

101 passages were marked as models. They share five features:

| Feature | Model passages (video [seconds]) |
|---|---|
| **A self-question chain, each answer one short sentence** | `solve-q-292` [57-79] "Can I just square this whole thing and get our answer? … Why not? What will have extra? I'll have also 2xy, right?" · `solve-q-r26-t09-04` [0-39] "Why did I choose 1 quarter? Because I know that its root is 1 half." · `solve-q-358` [13-55] "When is X times Y negative? Only when they have opposite signs." |
| **Side-by-side numbers that change one thing** | `absolute-value` [273-349] −3 and −6, then −3 and 6 · `solve-q-390` [42-91] 3 and 7 → 21, but 3 and 9 → not 27 · `solve-q-r26-t05-03` [23-55] opposites −2 / 2, 16 / −16, then "why do I care?" |
| **Meaning in plain words ("copies", "pieces", "missing to 1")** | `r26-t05-shortcuts` [117-141] "I have 99 copies of 41… a hundred copies of 41 minus one copy of 41" · `solve-q-125` [242-305] "12 copies of 13… 13 copies of 12" · `solve-q-r26-t03-02` [42-74] "the piece that it's missing, in order for it to get to one, is much smaller" |
| **One image, then the rule** | `roots` [648-760] "3 apples plus 2 apples… 5 apples… It's as if they're different families" · `exponents` [1312-1335] "2 to the power of n is turning into its own variable. It's like an x… 8x minus 1x" · `fraction-basics` [101-157] two pizzas, "this isn't seven eighths" · `solve-q-r26-t06-03` [18-66] "mirror" equations |
| **A short capsule at the end** | `solve-q-323` [68-110] "False means no x. True means every x." · `solve-q-r26-t02-05` [59-72] "90 is not what I have left. 90 is what I used." · `solve-q-r26-t03-01` [182-197] "When a minus looks bigger, it becomes actually smaller… because it's further from zero." · `solve-q-363` [103-126] "I can divide a positive number by a million and I'm still not getting to a negative." |

Also strong:
- **Plug-in rhythm, choice by choice:** `linear-equations` [1067-1190] and `solve-q-r26-t08-01` [76-132] ("2 plus 2, 4 plus 2, 6 plus 2, 8… can I already circle it? I can't… tie-breaker").
- **Honest exam talk:** `solve-q-r26-t10-01` [4-22] "without even calculating anything… I can cancel out option 1 and option 4" · `compare-fractions` [919-952] "we don't have to get to a final mathematical answer like we had to do in high school".
- **Mental maths:** `multiply-divide` [449-493] 23×7 = 20×7 + 3×7 = 140 + 21 = 161, "all that was just in our head".

**Template distilled from the models.** Use it for every hard step:
1. Ask the question the student would ask ("How do I get rid of the root?").
2. Answer it in one sentence.
3. Show it with one small number example, then a second that changes one thing.
4. Say why in one sentence ("Because…").
5. Close the step with a 6-10-word capsule.

When in doubt, say it in plain words ("copies", "pieces", "further from zero") before the term.
