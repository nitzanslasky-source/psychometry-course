# External-course fixes, part R (topics 24, 25, 26), 21 Oct 2026

Files edited: `studio-build/math_patches/_ai_vis_t24.py`, `_ai_vis_t25.py`, `_ai_vis_t26.py` (before-copies in
`reviews/before-2026-10-21-external-fixes/`). Scripts regenerated in `studio-build/ai_scripts/`. No git, no shared builds.

**Recording status:** `video_status.py --list record` lists r26-t24-three-groups, wp-081 (+ -2, -3) and wp-099 as
"Record", and `~/Documents/Course.recordings/_reading/` has no folder for any topic-24/25/26 video, so there are no takes.
Every changed paragraph is unrecorded. There are no proposals for recorded videos.

Slide numbers below are studio slides (the title slide is 1). Paragraph = the script line.

## 1. Topic 24: exactly one, by counting appearances (r26-t24-three-groups)

**Where:** a new slide 5, "Count the appearances", after "Pairs given" (all the triple-overlap teaching: who is missing,
can it be zero, the smallest group/pair). Prerequisites: VENN2 regions (wp-067) and the two-group "exactly one = A + B −
2·both" (wp-069 "Exactly one"). The slide gives a one-sentence reminder of wp-069 and does not re-teach it.
Study plan: topic 24 comes after 22/23. Nothing here needs a later topic.

**Changed paragraph 4.6** (the end of "Pairs given"):
- BEFORE: "So here it's from zero to nine. Now let's see a guided question. Try it first, and I'll see you in the next video."
- AFTER: "So here it's from zero to nine." (the closing moved to the end of the new slide)

**New slide 5 (all new text, exact):**
- `r26-t24-three-groups` 5.1: Now a question with exact numbers. A school play had three performances, with nine actors in each performance.
- `r26-t24-three-groups` 5.2: Three actors were in all three performances, and six actors were in exactly two. How many actors were in exactly one performance?
- `r26-t24-three-groups` 5.3: Let's draw the three performances as three circles. Each circle holds the nine actors of one performance.
- `r26-t24-three-groups` 5.4: The circles make three kinds of regions. In the middle are the actors in all three performances.
- `r26-t24-three-groups` 5.5: Where just two circles overlap, outside the middle, are the actors in exactly two.
- `r26-t24-three-groups` 5.6: And the outer part of each circle is for the actors in exactly one performance. That's what we're looking for.
- `r26-t24-three-groups` 5.7: We don't know how the six actors in exactly two are split among the three pairs. And we don't need it. So instead of people, we count appearances. Every time an actor plays in one performance, that's one appearance.
- `r26-t24-three-groups` 5.8: There are three performances, with nine actors in each. So three times nine is twenty-seven appearances.
- `r26-t24-three-groups` 5.9: Now, how many appearances does each actor make? An actor in exactly one performance appears once. An actor in exactly two appears twice. And an actor in all three appears three times.
- `r26-t24-three-groups` 5.10: Remember, with two groups, we took both away twice, because the people in both are counted in each group. Here it's the same idea, with three groups.
- `r26-t24-three-groups` 5.11: The three actors in all three performances make three times three, nine appearances.
- `r26-t24-three-groups` 5.12: The six actors in exactly two make six times two, twelve appearances.
- `r26-t24-three-groups` 5.13: Together that's nine plus twelve, twenty-one appearances. Twenty-seven minus twenty-one leaves six appearances.
- `r26-t24-three-groups` 5.14: Who made those six appearances? Only the actors in exactly one performance are left, and each of them appears once. So six actors were in exactly one performance.
- `r26-t24-three-groups` 5.15: So when we add up the groups, we count appearances, not people. How many different actors were there? Three plus six plus six is fifteen. So there were fifteen actors, not twenty-seven.
- `r26-t24-three-groups` 5.16: Counting appearances works when we know the size of every group, and the question asks about all the people in exactly one group, or all the people in exactly two, together. Counting appearances doesn't tell us which pair each actor was in, and we don't need that.
- `r26-t24-three-groups` 5.17: Now let's see a guided question. Try it first, and I'll see you in the next video.

**Numbers (recomputed):** 3 × 9 = 27 appearances; 3 × 3 = 9; 6 × 2 = 12; 9 + 12 = 21; 27 − 21 = 6, so 6 actors are in
exactly one. Actors: 3 + 6 + 6 = 15. Check that such a play exists: if each pair has 2, every circle has 3 + 2 + 2 + 2 = 9. ✓
These are new numbers. The other course's example (3 shows × 7 dancers, 2 in all three, 5 in exactly two) is not used.
The pair regions are never filled one by one, so nobody learns "spread the pair regions any way you like" (the review's
CHECK).

**Board / visual requirement:**
- `t_e0`, `t_e1`: typed givens, left column, at 5.1 / 5.2.
- `t_ev`: a NEW builder `VENN3` (in `_ai_vis_t24.py`, after VENN2): three equal circles named first / second / third.
  Each region kind is an exact shape, built in layers at the spoken words: middle tint + "all three" (5.4), the 3 pair
  regions + "exactly two" (5.5), the 3 outer parts + "exactly one" (5.6), then the teal tags ×1 / ×2 / ×3 at "appears
  once" / "appears twice" / "three times" (5.9). All three circles and every label stay on screen to the end of the slide.
- Right column, hand-written at their clauses: `3×9=27 appearances` (5.8), `all three: 3×3=9` (5.11),
  `exactly two: 6×2=12` (5.12), `9+12=21` and `27−21=6` (5.13), `exactly one: 6 actors` (5.14), then the typed key
  "Add the groups: appearances, not people" and `actors: 3+6+6=15` (5.15), then the typed condition "The totals only,
  not who is in which pair" (5.16).
- I looked at the frames (handwriting build). No overlaps. The figure ends before the right column (x ≈ 940 < 1010).

**Condition:** said in 5.16. Counting appearances works when the size of every group is known and the question asks
about everyone in exactly one group (or in exactly two) together. It does not say which pair each person is in.
**Read-aloud:** done with the frames. I named the referents: "So instead of people, we count appearances", "Counting
appearances works / doesn't tell us" (not "it"). Ready.
**Length:** the lesson is now 5.4 min (it was 3.3). That is inside R37's 5–6 min, so I did not split it. Split it at
"Count the appearances" if she wants shorter parts.

## 2. Topic 25: the newcomer average, "share the extra" (wp-081, the lesson where "a number joins" is taught)

**Where:** two new slides right after "A number joins" (the balance, which is kept unchanged): slide 5, "Share the extra",
and slide 6, "Find the newcomer". Prerequisites, all taught earlier: "each value counts as the average" (wp-081 slide 3),
the towers (wp-080 camera lesson), and the balance (wp-081 slide 4). It is an explanation, not a formula. Nothing is
boxed, and no "new = old + d ÷ n" is written anywhere.

**New slide 5, "Share the extra" (exact):**
- `wp-081` 5.1: Often we know how many numbers there are, and the question asks for the new average. Here's a way to see it. Four numbers have an average of six. A fifth number, eleven, joins. What's the new average?
- `wp-081` 5.2: Each of the four numbers counts as six, like we saw before. So let's draw four towers of six blocks, and a tower of eleven for the new number.
- `wp-081` 5.3: The old average is six. The new number is eleven, so it's five above the old average. That's five extra blocks.
- `wp-081` 5.4: Those five extra blocks are shared equally by everyone in the new group. That's all five numbers, the new one too. Five divided by five is one block each.
- `wp-081` 5.5: So every tower is one block above six. The new average is six plus one, seven.
- `wp-081` 5.6: Let's check with sums. Four times six is twenty-four. Twenty-four plus eleven is thirty-five. And thirty-five divided by five is seven.
- `wp-081` 5.7: Careful, we share the extra among five numbers, not four, because the new number gets its share too.

**New slide 6, "Find the newcomer" (2024_spring_q1_07 type, new story and numbers; exact):**
- `wp-081` 6.1: Now the way the exam asks it. Three suitcases have an average weight of twenty kilos. A fourth suitcase is added, and now the average of the four is eighteen kilos. How heavy is the fourth suitcase?
- `wp-081` 6.2: This time the average went down, from twenty to eighteen. That's two kilos less for each of the four suitcases.
- `wp-081` 6.3: So the fourth suitcase is below the old average, and that missing weight is shared by all four. Two kilos for each of the four is four times two, eight kilos.
- `wp-081` 6.4: So the fourth suitcase is eight kilos below twenty. Twenty minus eight is twelve kilos.
- `wp-081` 6.5: Let's check with sums. Three times twenty is sixty kilos before. Four times eighteen is seventy-two kilos after. Seventy-two minus sixty is twelve, the same weight.
- `wp-081` 6.6: There's a trap here. If we multiply the two kilos by three, we get six below, and fourteen kilos. But the fourth suitcase shares the drop too, so we multiply by four.
- `wp-081` 6.7: So when they ask how many numbers there were, we use the balance, like before. When we know how many, and they ask for the newcomer or the new average, we share its distance from the old average among the new group. [pause] Okay. I'll see you in the next part.

**Numbers (recomputed):** towers 4 × 6 + 11 = 35, 35 ÷ 5 = 7; extra 11 − 6 = 5, 5 ÷ 5 = 1, 6 + 1 = 7 ✓. Suitcases
20 − 18 = 2, 4 × 2 = 8, 20 − 8 = 12; check 3 × 20 = 60, 4 × 18 = 72, 72 − 60 = 12 ✓. Trap: 3 × 2 = 6 gives 20 − 6 = 14.

**Board / visual requirement:**
- Slide 5: typed question `b_n0`. The TOWERS figure `b_nt` (6, 6, 6, 6, 11) is built in layers: the towers at "let's draw
  four towers"; the teal dashed "old average 6" at "The old average is six"; the 5 orange blocks above 6 at "That's five
  extra blocks"; the share at "shared equally by everyone" (4 blocks move onto the four towers, and 1 stays on the
  newcomer's tower, still orange: its own share); "new average 7" at "The new average is". Hand-written lines in the
  right column at their clauses: `11−6=5 extra`, `5÷5=1 each`, `6+1=7`, `4×6+11=35`, `35÷5=7`. Then the typed caution
  "Share by the new count: 5, not 4".
- Slide 6: typed question `b_g0`. Hand-written lines on the left: `20−18=2 less, each`, `4×2=8 below 20`, `20−8=12 kg`.
  On the right: `3×20=60, 4×18=72`, `72−60=12`, `3×2=6: 14 kg, the trap`. Then the typed key "How many? The balance.
  The newcomer or the new average? Share it."
- I looked at the frames. No overlaps.

**Condition:** said in 5.7 and 6.6 (share by the NEW count, because the newcomer gets a share too). 6.7 says when to use
which method: the count is asked → the balance; the count is known and the newcomer or the new average is asked → share.

**Wording changed so the two methods don't contradict each other** (the balance compares a joiner to the NEW average;
the sharing compares it to the OLD one):
- wp-081-2 2.1, BEFORE: "It works the same when a number leaves. The average of a group is fifty. …" → AFTER: "The
  balance works the same when a number leaves. The average of a group is fifty. …" (the rest is unchanged)
- wp-081-2 2.6, BEFORE: "So compare the number to the average of the group it is in. Joins, the new average. Leaves, the
  old average." → AFTER: "So in the balance, we compare the number to the average of the group it is in. Joins, the new
  average. Leaves, the old average." Board `b_l7`: "Compare the number to the average of the group it is in" → "The
  balance: compare the number to the average of the group it is in".
- wp-081-3 summary, BEFORE: "When a number joins or leaves, compare it to the average of the group it is in." → AFTER:
  "When a number joins or leaves, and they ask how many, compare it to the average of the group it is in." plus one new
  line: "When they ask for the newcomer or the new average, share its distance from the old average among the new
  group." Board `b_z2`: "Joins or leaves, how many? Compare it to the average of the group it is in". New `b_z5`: "The
  newcomer or the new average? Share its distance from the old average".
- Part split (SPLITS): part 1 now ends with "Find the newcomer", and "A number leaves" opens part 2. The part-2 opening
  line, BEFORE: "Let's continue, and find the biggest and the smallest possible values." → AFTER: "Let's continue. First
  a number that leaves, and then the biggest and the smallest possible values." The part-3 split moved from slide 8 to 10
  (the same slide, "Letters"). New lengths: part 1 4.7 min (was 3.3), part 2 3.7, part 3 2.8.

**Read-aloud:** done with the frames. "It works the same" became "The balance works the same", and "like we just saw"
became "like we saw before" (the reminder points to slide 3). Ready.

## 3 + 4. Topic 26: staggered arrival and work–rest cycles (wp-099, now in two parts)

**Where:** wp-099 (Worker-Hours, the last lesson of topic 26). It already teaches "someone joins in the middle" (the whole
job − done = left), after the rate/time basics (wp-092) and adding rates (wp-094). The two new slides come right after
"Someone joins in the middle", and the lesson is split into 2 parts (SPLITS, not on camera; CP.add_to_course creates the
new video **wp-099-2** right after wp-099 in the same section). Part 1 = slides 2–5 (2.5 min). Part 2 = "One after another",
"Clock time and working time", Recap (4.2 min).
- Part 1 now ends (5.8) with "So the whole job, minus what's done, is what's left. Then we divide what's left by the new
  rate. [pause] Okay. I'll see you in the next part." (the closing is added by the split)
- Part 2 opening (new): "Let's continue, with two more questions where we follow the time step by step."

**New slide "One after another"** (the 2023_spring_q2_07 "bees" type: a new story and new numbers; wp-099-2 slide 2, exact):
- `wp-099-2` 2.1: Sometimes workers don't join just once. They join one after another, at fixed times. Then we go step by step, minute by minute, in a table.
- `wp-099-2` 2.2: A box holds thirty flyers. One volunteer starts handing them out. A minute later a second volunteer joins, a minute after that a third, and so on. Each volunteer hands out two flyers a minute, until the box is empty.
- `wp-099-2` 2.3: How many flyers did the first volunteer hand out?
- `wp-099-2` 2.4: Let's make a table. For each minute, we write how many volunteers are working, how many flyers they hand out in that minute, and how many are gone so far.
- `wp-099-2` 2.5: In the first minute, only one volunteer works. One times two is two flyers. So far, two flyers are gone.
- `wp-099-2` 2.6: In the second minute, two volunteers work. Two times two is four flyers. Two plus four is six so far.
- `wp-099-2` 2.7: In the third minute, three volunteers work. Three times two is six. Six plus six is twelve so far.
- `wp-099-2` 2.8: In the fourth minute, four volunteers hand out four times two, eight. Twelve plus eight is twenty so far.
- `wp-099-2` 2.9: In the fifth minute, five volunteers hand out five times two, ten. Twenty plus ten is thirty. That's the whole box, so they stop after five minutes.
- `wp-099-2` 2.10: Now we can answer the question. The first volunteer worked all five minutes, at two flyers a minute. Five times two is ten flyers.
- `wp-099-2` 2.11: Careful, the volunteers didn't all hand out the same. The third volunteer joined in the third minute, so she worked three minutes. Three times two is six flyers.
- `wp-099-2` 2.12: Let's check. From the first volunteer to the fifth, they handed out ten, eight, six, four and two flyers. That adds up to thirty, the whole box.
- `wp-099-2` 2.13: Here the box ran out exactly at the end of a minute. If it runs out in the middle of a minute, the last step is only part of a minute. So we go step by step, and stop when the total reaches the whole job.

**New slide "Clock time and working time"** (wp-099-2 slide 3, exact):
- `wp-099-2` 3.1: One more kind of question. Sometimes a worker takes breaks. Then the time on the clock is not the same as the time she works.
- `wp-099-2` 3.2: A worker packs eight boxes every five minutes of work. After every thirty minutes of work, she rests for ten minutes.
- `wp-099-2` 3.3: How many boxes does she pack in one hour?
- `wp-099-2` 3.4: Let's draw the hour as a timeline, in steps of five minutes. It starts at zero and ends at sixty.
- `wp-099-2` 3.5: She works for the first thirty minutes. So the clock shows thirty when her first break starts.
- `wp-099-2` 3.6: She rests for ten minutes, from thirty to forty.
- `wp-099-2` 3.7: Then she works again, from forty to sixty. That's twenty minutes of work.
- `wp-099-2` 3.8: Why is there no second break in the hour? Her next break comes after thirty more minutes of work. Forty plus thirty is seventy, and the hour ends at sixty.
- `wp-099-2` 3.9: So her working time is thirty plus twenty, fifty minutes.
- `wp-099-2` 3.10: She packs eight boxes in every five minutes of work. So how many five-minute parts are in fifty minutes? Fifty divided by five is ten.
- `wp-099-2` 3.11: Ten parts, eight boxes in each. Ten times eight is eighty boxes.
- `wp-099-2` 3.12: A lot of students divide the whole hour by five. Sixty divided by five is twelve. And twelve times eight is ninety-six. But she doesn't pack while she rests.
- `wp-099-2` 3.13: So draw the timeline, mark when each break starts, and count only the working minutes inside the time they ask about. And read the question carefully. Does the break come after thirty minutes of work, or every thirty minutes on the clock?

**Recap (wp-099-2 slide 4), 2 new paragraphs** (4.4, 4.5): "When workers join one after another, we go step by step in a
table, until the whole job is done." / "And with breaks, we count only the working minutes." The old recap lines are
unchanged (they now close part 2).

**Numbers (recomputed):** flyers: minute k has k volunteers → 2, 4, 6, 8, 10; running totals 2, 6, 12, 20, 30 (= the
box). The first worked 5 min → 10. The third worked 3 min → 6. Check 10 + 8 + 6 + 4 + 2 = 30 ✓. Boxes: work 0–30, rest
30–40, work 40–60. The next break would start at 40 + 30 = 70 > 60. 30 + 20 = 50 working minutes; 50 ÷ 5 = 10 parts;
10 × 8 = 80 ✓. Trap: 60 ÷ 5 = 12, 12 × 8 = 96. I used my own numbers, not Codex's/the other course's barber numbers
(12 braids, 120).

**Board / visual requirement:**
- Flyers: typed givens `t9e0`, `t9e1`. Table `t9et` (minute | volunteers | this minute | so far), with one row written
  at each "In the … minute". Each cell carries its expression (`3×2=6`, `6+6=12`), so nothing is said without being
  written. The teal frame on `20+10=30` comes at "That's the whole box". Right column, hand-written: `the first: 5×2=10
  flyers`, `the third: 3×2=6`, `10+8+6+4+2=30`, then the typed key "Step by step, until the whole job is done".
- Work–rest: typed givens `t9f0`, `t9f1`. The timeline `t9ft` (UNITS, 12 five-minute boxes; a NEW mark kind 'tick' =
  a clock time over a box edge, added to t26's own UNITS copy) is built in layers: 0 and 60 at "It starts at zero";
  work 0–30 (teal, bracket "work 30", tick 30); rest 30–40 (grey, bracket "rest 10", tick 40); work 40–60 (bracket
  "work 20"). Right column, hand-written: `next break: 40+30=70, after the hour`, `30+20=50 minutes of work`, `50÷5=10`,
  `10×8=80 boxes`, `60÷5=12, 12×8=96: the trap`. Typed key on the left: "Breaks: draw the timeline, count only the
  working minutes".
- I looked at the frames (handwriting build). The first version overlapped the right column. I narrowed both figures to
  w=560, and the final frames have no overlaps.

**Conditions:** flyers: 2.13, the box ran out exactly at a minute's end; if not, the last step is part of a minute, so
stop when the total reaches the job. Breaks: 3.8 (why only one break: the next break comes after 30 more WORKING
minutes, at 70) and 3.13 (read whether the break comes after 30 minutes of work or every 30 minutes on the clock; count
only the working minutes inside the asked window).
**Read-aloud:** done with the frames. Every number names its quantity ("flyers", "minutes of work", "five-minute parts").
"So far, two" became "So far, two flyers are gone", and "Now the question" became "Now we can answer the question". Ready.

## Checks
- Spec runs (`python3 math_patches/_ai_vis_t24.py`, `t25`, `t26`, all videos): no PROBLEMS.
- Private builds: `scratchpad/xf-R/test.html` and `hw.html` (AI_HANDWRITE=all), both OK.
- `SRC=xf-R/test.html python3 ai_check.py r26-t24-three-groups wp-081 wp-081-2 wp-081-3 wp-099 wp-099-2`: all OK.
- `python3 math_check.py 24 25 26`: PROBLEMS 0, WARNINGS 0, LAYOUT 0 (286 slides). The same with AI_HANDWRITE=all.
- `w19_check.py`: I fixed the flags on the new lines (dense sums split, short fragments made full sentences). The flags
  left are on older lines.
- Frames: `scratchpad/xf-R/fr*/…` (sheets plus full-size renders `last2.png`, `last3.png`, `v3f1.png`, `w81_12.png`).
  I looked at all of them.
- Prompter dump: `scratchpad/xf-R/prompter_new.txt`. The math displays correctly (×, ÷, −, digits).

## Proposals for recorded videos
None. No topic-24/25/26 video has a take.

## Needs Claude
- `summary_pages/t25.json` (the topic-25 summary page) still has only the old "compare it to the average of the group it
  is in" for joins/leaves. Add the "share its distance from the old average among the new group" line there, so it
  matches the new lesson summary. I did not touch it (outside my files). Topic 26's summary page does not mention breaks
  or one-after-another. Add one line each if wanted.
- wp-099-2 is a new video id (a lesson part). It appears in the course through CP.add_to_course, as wp-094-2 and wp-097-2
  do. planData.ts lists no lesson ids, so nothing else needs it.
- Prompter: mixed digits and words in a few new lines ("4 × 2, eight", "10 parts, eight boxes in each"). This is the
  same style as the existing lines, not wrong maths.
