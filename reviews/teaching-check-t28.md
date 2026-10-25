# Teaching check (W20) — topic 28, Counting possibilities and factorials

25 Oct 2026. Run by Claude on its own first-draft scripts (`math_patches/_ai_vis_t28.py`, 39 videos with the parts),
after the W19 pass. For every important, reusable concept: is it TAUGHT (the general statement, why, how to recognise it,
an extra case if new), where, and was anything added. W20 asks for "only when it really adds"; here the teacher's own
request for the topic ("everything explained clearly and well, show small cases before each rule, 2-3 worked examples")
makes the lessons the place where each concept is taught in full, so most rows say "taught in the lesson".

| Concept | Where it is taught (full) | Statement · why · recognise · extra case | Later uses (reminder) | Result |
|---|---|---|---|---|
| What counts as a different result (does the order matter?) | wp-123 part 1 | row / team / code, each with names; "first ask: does the order matter?" | wp-137, checklist | taught |
| Listing in order, smallest first | wp-123 part 1 (24, 27, 47; 8 = 1+7 ... 4+4) | why: nothing missed, nothing twice; when: a short list | g124, g126 M2, g141 M2, g144 M1, g142 M2 | taught |
| Multiply the options of the stages | wp-123 part 2: the tree (3 shirts x 2 hats) BEFORE the rule; 3 examples | why = equal groups (2 + 2 + 2 = 3 x 2); recognise: one choice of each; trap: adding | g125 (slow, "like in the lesson"), every question | taught |
| The order of the stages doesn't matter | wp-123 part 2 (hats first: 3 + 3 = 2 x 3) | why: multiplication is commutative, shown on a second tree | g125 | taught |
| No leading zero | wp-124-after (90, checked by 99 - 10 + 1) | why: 07 is a one-digit number | g141, wp-141-after | taught |
| Start with the restricted stage | wp-124-after (450, checked by half of 900) | why: free stages work with anything | g141, g142 | taught |
| A forced (dependent) stage gets 1 | wp-124-after (digit sum 11, listed; units = 2 x tens, listed) | "imagine you picked, then ask what completes it"; the 8 x 10 mistake | g126, g141, wp-141-after | taught |
| With / without repetition (the pool) | wp-127 (codes from 1, 2, 3 listed both ways; A-F) | the one question after every pick; full vs shrinking | g128, g129 | taught |
| n items in a row = n!; factorial | wp-127 (ABC listed, 3 x 2 x 1; 4 mugs; 3!, 4!, 5!) | why: a row is a choice without repetition | g130, g140, groups, arrange | taught |
| Mutual action: divide by 2 | wp-131 (5 friends: the 20 ordered pairs listed, AB = BA; 11 teams) | why: each pair counted from both sides; cues list; roles: don't halve | g132, g133, g143 | taught |
| One fewer each time (4 + 3 + 2 + 1) | wp-131 (the drawing) | why: a line from the earlier point is already drawn | g132 M2, g133 M3, g143 M3 (rising) | taught |
| Diagonals n(n - 3)/2 | g133 (one-off, 4 ways, with why minus three) | — | — | taught in the question (rare type) |
| Adding non-overlapping cases | wp-134 (lunch 6 + 4; thin base 1 + 9) | why: every result in exactly one case | g135 | taught |
| All minus forbidden | wp-134 (12 - 2; 16 - 4; not the same colour 30 - 10, checked by cases) | cue words "not", "different from", "at least one"; worth it when the forbidden group is small | g135 M2, g136, g142 M3, q04, q07 M2 | taught |
| A group: divide by k! | wp-137 part 1 (2 of 4 listed; 3 of 5: ABC in 6 orders listed = one group; 4 of 6 cancelled) | why: k! orders of the same group | g138, g139 M2, q08 M2 | taught |
| Who stays out; count the smaller side | wp-137 part 2 (4 of 5 listed; 7 of 9 = 36) | why: each one left out gives one group; "more common, and easy" | g139, g144 M2 | taught |
| Roles vs group (210 vs 35) | wp-137 part 2 | "the question tells you which one, by the roles" | g138 M2 (names = labels) | taught |
| Factorials by sight; stop early; a run of neighbours; backwards | wp-140-after part 1 (2 examples each) | condition: whole numbers, b > a; the slip "a is 4, not 5" | g140 (stop early is first taught there), q28 | **added as a real lesson** (was a 2-minute extension) |
| Letters: plug in first, then the math | wp-140-after part 2 (two examples; the product trap) | — | — | taught |
| Take out the smaller factorial | wp-140-after part 2 (6! + 5!, 7! - 6!, each checked) | "don't forget the one", never subtract inside the ! | q28 | **added** (exam F3) |
| Counting primes in a factorial | wp-140-after part 3 (6!, 7!) | the trap: three even numbers but four twos | — (practice p02) | **added** (exam F4) |
| k! x 2^k = 2 x 4 x ... x 2k | wp-140-after part 3 (one example, the why) | said as rare | — | added (exam F5, minor) |
| At least one = all minus none | r26-t28-cases (two coins listed; codes with a 5 listed) | why the direct count double-counts (55) | q04 | **added as a real lesson** |
| Objects into boxes: each object chooses | r26-t28-cases (2 letters, 2 boxes listed; 3 children, 4 flavours) | "who chooses?"; test a tiny case | q05 (M2 = the tiny case) | **added** |
| The worst case (keys) | r26-t28-cases (4 keys: 4 + 3 + 2 + 1) | worst luck, topic-21 reminder | practice p13 | **added** (exam C8) |
| Together: glue; apart: all minus together / gaps | r26-t28-arrange part 1 (ABC listed first; 5 friends; 4 friends both ways) | why each step; "don't forget the order inside" | q06, q07, q09 | **added as a real lesson** |
| Repeats: divide by each repeat's factorial | r26-t28-arrange part 2 (AAAB listed, then A1 A2 A3 rows; AABB listed) | why: swapping identical items changes nothing | q08 (BANANA) | **added** (external findings row 28) |
| A round table: (n - 1)! | r26-t28-arrange part 2 (3 people: ABC, BCA, CAB one seating) | why: turning changes no neighbours; fix one person | q09 | **added** |
| The complementary event is a technique | g144 M2 (her closing line) | "not magic" | — | taught |

**Takeaways after answers (W11/R16):** none forced. The reusable facts sit in the lessons; question videos end with the
answer line, except where her Hebrew closing line is itself the teaching point (g144).

**Result:** every concept the topic's questions use is taught in a lesson before its first question (R37), with a tiny
case shown first and 2-3 examples; one-off ideas (diagonals, stop early at its first use) are taught in their question.
