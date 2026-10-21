# External-course fixes, part P (topic 51 plugging in numbers + the t13 / t51 summary pages), 21 Oct 2026

Files changed: `studio-build/math_patches/_ai_vis_t51.py` (only the `pt51-plug-numbers` lesson spec + its CAMERA_SPLITS + the
V4 right-column list), `studio-build/summary_pages/t51.json`, `studio-build/summary_pages/t13.json`. Before-copies are in
`reviews/before-2026-10-21-external-fixes/`. Nothing committed, git untouched.

## Recording status (checked first)
`python3 video_status.py --list record` lists pt51-plug-numbers, -2 and -3 (and every other pt51 video) as **Record**, and
`~/Documents/Course.recordings/_reading/` has no folder for any pt51 id, so no takes exist. All changes went into unrecorded
paragraphs; nothing recorded was touched. No question video was changed.

## Structure change: the lesson is now 4 camera parts (was 3)
With the new material, old part 3 would have been 7.3 min (R37: camera parts ~3-4 min). The split points moved, at idea
boundaries, and one part was added:

| Part | Slides | Minutes (before -> after) |
|---|---|---|
| pt51-plug-numbers | Why it matters, When, Why it works, Letters in the choices (unchanged) | 4.1 -> 4.1 |
| pt51-plug-numbers-2 | Keep the conditions, **Choose, check, try again** (new), Choices that tie (rewritten) | 3.6 -> 3.9 |
| pt51-plug-numbers-3 | **Two letters** (rewritten from "Different letters"), No letters: a ratio, Case 4, Nothing-changes value | 4.5 -> 4.3 |
| **pt51-plug-numbers-4** (new id) | Always or not always (moved), **Cannot be determined** (new), **Change the kind of number** (new), So when do I use it? (rewritten) | new, 4.4 |

New CAMERA_SPLITS: `(1, None), (5, "Let's continue with plugging in numbers, and how to choose the number."),
(8, "Let's continue with two letters, and two more cases."), (12, "Let's continue with what is always true, and a special kind of choice.")`.
The build creates pt51-plug-numbers-4 automatically (`_camera_parts.add_to_course`); "Case 4" and "Nothing-changes value"
stay in part 3, so `added_content.py` is still right. The old "A tie-breaker number" slide is gone: its x(x + 1) example
now carries the new rule.

## Change 1: the decision rule (pt51-plug-numbers-2)

Her rule, as taught now: check every restriction, choose an easy allowed number (zero is often the fastest and is out only where
a restriction forbids it), see what it rules out, try another easy allowed number only if more than one choice is left, and
check only the choices still left. There is no "skip 0 and 1", no "start with two or three", and no "different letters,
different numbers". The counterexample teaching ("one success doesn't prove always") is kept (part 4, slide 2).

**pt51-plug-numbers-2 2.1** (Keep the conditions)
- BEFORE: "The number must obey every condition in the question. If it says x is at least four, x can't be two."
- AFTER: "How do we choose the number? First, we check every restriction in the question. The number must obey all of them. If it says x is at least four, x can't be two."
- Board: unchanged (f3k1 at "If it says x is at least four"). 2.2-2.4 unchanged.

**pt51-plug-numbers-2 slide 3 "Choose, check, try again"** (NEW slide; replaces the old "A tie-breaker number" slide's x(x+1) example, now done with 0 first)
- BEFORE (old 5.1-5.4): "Fourth, rule out three choices. Sometimes even a good number leaves two. For example, x times the bracket x plus one. … Let's take x equals two. Two times three is six … Two choices give six, so we can't decide yet. This is why we don't stop at the first choice that fits. We take a tie-breaker number, and we check only the two choices that are left. The ones that are out stay out. / Now x equals three. … The answer is x squared plus x."
- AFTER:
  - 3.1 "Second, we choose an easy number that's allowed. Zero is often the fastest, because every term with zero in it becomes zero. Zero is out only when it breaks a restriction, like the bottom of a fraction."
  - 3.2 "Here's an example. x times the bracket x plus one. The choices are x squared plus x, three x, x squared plus one, and four x."
  - 3.3 "Is there a restriction? No, x can be any number. So zero is allowed, and we take x equals zero. Zero times one is zero. So the right choice must give zero when x is zero."
  - 3.4 "Third, we check what zero rules out. Choice number one says x squared plus x. Zero plus zero is zero, so it stays. Choice number two says three x. Three times zero is zero, so it stays too."
  - 3.5 "Choice number three says x squared plus one. Zero plus one is one, not zero, so it's out. Choice number four says four x. Four times zero is zero, so it stays."
  - 3.6 "Three choices give zero, so zero can't tell them apart. That's why we don't stop at the first choice that fits. Fourth, we try another easy allowed number, and we check only the three choices that are left."
  - 3.7 "Now x equals one. One times two is two, so the right choice must give two. x squared plus x is one plus one, two, so it stays. Three x is three, and four x is four. They aren't two, so they're out."
  - 3.8 "Only x squared plus x is left, so it's the answer. No third try is needed. So that's how we choose. Check the restrictions, choose an easy allowed number, and see what it rules out. Try another number only if more than one choice is left."
- Board (what is on screen when):
  - "Zero is often the fastest, if it is allowed" (typed) appears at "Zero is often the fastest".
  - x(x+1) = ? appears at "Here's an example", and the four choices at "The choices are".
  - Hand-written rows, in order. "No restriction. x=0: 0·1=0" appears at "Zero times one is zero". "x²+x=0" at "Zero plus zero is zero". "3x=0" at "Three times zero is zero". "x²+1=1, no" at "Zero plus one is one". "4x=0" at "Four times zero is zero".
  - Typed "Three left → again, only those three" appears at "Three choices give zero".
  - Right column (y 300-480, below the face bubble). The hand-written rows "x=1: 1·2=2", "x²+x=1+1=2" and "3x=3, no 4x=4, no" appear at their clauses, then the typed line "One left → no third try".
  - At the end, the typed key lines "Restrictions → easy number → what is out?" (at "Check the") and "Another number only if needed" (at "Try another number only if").
- Why a second try was / wasn't needed: zero ruled out one choice and left three that all gave 0, so a second try was needed. After x = 1, one choice was left, so no third try. All of this is said and written.
- Maths: x = 0 gives 0 and the choices give 0, 0, 1, 0. x = 1 gives 2, and x² + x = 2, 3x = 3, 4x = 4. Correct.

**pt51-plug-numbers-2 slide 4 "Choices that tie"** (rewritten around the rule; same example x²·x³/x)
- BEFORE 3.1-3.5: "Second, choose numbers that help tell the choices apart. Here's an example: x squared times x to the power of three, all divided by x. The choices are x to the fourth, … / Say I plug in x equals one. … Nothing is ruled out. / When zero is allowed, it can also make several choices come out the same. But zero is not allowed in this example, because x is at the bottom of the fraction. We'd be dividing by zero. So we need another easy number. / Now x equals two. Two squared is four, and two cubed is eight. … They're all different, and only x to the fourth gives sixteen. / So before you calculate, look at the choices. If they have powers, products or fractions, skip zero and one, and start with two or three. When the choices are numbers, zero and one are fine if the question allows them, because there's nothing to tie."
- AFTER:
  - 4.1 "Here's an example where zero isn't allowed. x squared times x to the power of three, all divided by x. The choices are x to the power of four, x to the power of five, x to the power of six, and x to the power of three."
  - 4.2 "First the restrictions. x is at the bottom of the fraction, and we can't divide by zero. So zero isn't allowed here."
  - 4.3 "The next easy number is one. One to any power is one. So the question gives one, and all four choices give one too. Nothing is ruled out, so we need another try."
  - 4.4 "Now x equals two. Two squared is four, and two to the power of three is eight. Four times eight is thirty-two, and thirty-two over two is sixteen. So the right choice must give sixteen."
  - 4.5 "The choices give sixteen, thirty-two, sixty-four and eight. Only x to the power of four gives sixteen. So this one try rules out the other three."
  - 4.6 "So zero and one are fine to start with. But with powers in the choices, they often make every choice give the same result. Then we just take the next easy allowed number." (followed by the part closing)
- Board. The typed "Restriction: x is at the bottom → x≠0" appears at "First the restrictions" (it was a hand-written "x=0: not allowed" row). The hand-written row "x=1: 1, and the choices 1, 1, 1, 1" appears at "So the question gives one". The ✗ is removed, so the row is pen-safe. The rows x = 2 and = 32/2 = 16 appear at their clauses. Typed "Choices: 16, 32, 64, 8 → only x⁴ is 16" appears at "The choices give sixteen". The typed "Zero or one make the choices tie? → the next easy allowed number" appears at "they often make every choice". The old line was "0 and 1 often make choices tie (letters in the choices)".
- Condition check: zero is ruled out by its restriction (the denominator), which is said and written before any number is chosen.

**pt51-plug-numbers-3 slide 2 "Two letters"** (was "Different letters" in part 2)
- BEFORE 4.1-4.4: "Third, different numbers can help when there are different letters. Look at two choices, a squared b, and a b squared. / If a and b are both two, both choices give eight. … They tie. / With a equals two and b equals three, a squared b is four times three, twelve. And a b squared is two times nine, eighteen. Now they're different. / Different letters may be equal, unless the question says they're not. But equal numbers often hide the difference, so we choose different ones."
- AFTER:
  - 2.1 "Two letters may get the same number, unless the question says they're different. Giving them the same number is often the fastest. For example, the bracket a plus three, times the bracket b plus three. From that product we subtract three a, three b, and a b. The choices are zero, three, six and nine."
  - 2.2 "There's no restriction, so let's take zero for both letters. Zero plus three is three, and three times three is nine. Three a, three b and a b are all zero. So the expression is nine."
  - 2.3 "The choices are numbers, so only one of them can be nine, choice number four. One try is enough."
  - 2.4 "With letters in the choices, the same number can make two choices tie. Look at two choices, a squared b, and a b squared. With a and b both one, both choices give one."
  - 2.5 "So we keep a as one, and we change b to two. Then we check only those two choices. a squared b is one times two, two. And a b squared is one times four, four. Now they're different. So different letters don't need different numbers. We change one only when the same number makes choices tie."
- Board:
  - Typed: "(a+3)(b+3)−3a−3b−ab = ?" and "Choices: 0, 3, 6, 9".
  - Hand-written: "a=b=0: 3·3=9" appears at "three times three is nine", and "3a, 3b, ab are 0 → 9" at "are all zero".
  - Typed: "Number choices → only one is 9: one try", then "Letter choices: a²b and ab²".
  - Hand-written: "a=b=1: 1 and 1, a tie", then "a=1, b=2: a²b=1·2=2" and "ab²=1·4=4", each at its own clause.
  - Typed: "The same number is allowed; change one only for a tie".
- Why one try was enough: the choices are numbers, so only one choice can equal 9. With the letter choices, the same number made a tie, so a second try was needed.
- Maths: (a+3)(b+3) − 3a − 3b − ab = 9 for every a and b. At a = b = 1, a²b = ab² = 1. At a = 1, b = 2, they are 2 and 4. Correct.

**pt51-plug-numbers-4 2.1 / 2.2** (Always or not always, moved from part 3)
- 2.1 BEFORE: "Last, questions about what is always true, …" → AFTER: "Now, questions about what is always true, …" (it's no longer the last idea).
- 2.2 BEFORE: "Let a equal one and b equal two, two small, different numbers." → AFTER: "… two small, easy numbers." (no "different numbers" rule). The counterexample teaching is unchanged.

**pt51-plug-numbers-4 5.2 / 5.3** (So when do I use it?)
- 5.2 BEFORE: "And how? Say which number and why, before you use it. Check that the choices come out different, so when the choices have letters, skip zero and one, because they often make choices tie."
- 5.2 AFTER: "And how? First, check every restriction. Then choose an easy allowed number, often zero, and say why before you use it. See which choices it rules out. If more than one is left, try another easy number, and check only those."
- 5.3 BEFORE: "Give different letters different numbers. Rule out three choices, and if two are left, use a tie-breaker number. And remember, it's your safety net."
- 5.3 AFTER: "A choice like cannot be determined is never ruled out by a number. If one other choice is left with it, try to break that choice with a different kind of number. And remember, it's your safety net."
- Board. Four numbered lines, each at its clause:
  1. "Check every restriction"
  2. "An easy allowed number (often zero); say why"
  3. "Which choices does it rule out?"
  4. "More than one left → another number, only those"
  Then the boxed line '"Cannot be determined": never ruled out → change the kind', and "It's your safety net". The old lines "3. Different letters, different numbers" and "4. Rule out three; two left → a tie-breaker number" are gone.

## Change 2: "Cannot be determined" / "None of the above" (pt51-plug-numbers-4, two new slides)

Placed after the rule (part 2), after "two letters" (part 3), and right after "always is never proved by examples" (part 4,
slide 2), which it builds on. Prerequisites check (study plan: topic 51 is day 6, after topics 1, 2, 4, 6, 8, 9, 10):
the example only needs squares (topic 8), negatives (topic 1), the fractions ½ and ¼ (topic 2), and the symbols ≥ and <,
which this lesson already uses ("x is at least four", x ≥ 4). No inequality algebra (topic 12) is used. The example is our own: the
given x ≠ 0 with x² ≥ x / x² < x / x² = x / "None", answer (4). It's like 2021_autumn_q1_16 in form, but the given and
the expressions are different.

**Slide 3 "Cannot be determined"** (new)
- 3.1 "Some questions have a last choice like, it cannot be determined, or, none of the above is necessarily true. You'll see it often on the exam. No number can rule that choice out."
- 3.2 "Why? That choice says the answer isn't always the same. And we just saw that examples can't prove always. So when we plug in numbers, that choice always stays."
- 3.3 "For example, given: x is not equal to zero. Which of the following is necessarily true? Choice number one, x squared is greater than or equal to x. Choice number two, x squared is smaller than x. Choice number three, x squared is equal to x. And choice number four, none of the above is necessarily true."
- 3.4 "Necessarily true means true for every allowed x. So one x where a choice is false rules it out. Zero isn't allowed, so the easiest number is one. One squared is one."
- 3.5 "Choice number one says x squared is greater than or equal to x. One is equal to one, so it stays. Choice number two says x squared is smaller than x. One isn't smaller than one, so it's out."
- 3.6 "Choice number three says x squared is equal to x. One equals one, so it stays too. And choice number four stays, because no number can rule it out."
- 3.7 "Now we try another easy number, two, and we check only choice numbers one and three. Two squared is four. Four is greater than two, so choice number one stays. Four isn't equal to two, so choice number three is out."
- Board (left):
  - Boxed: '"Cannot be determined", "None of the above": no number rules it out'.
  - Typed: "Given: x≠0. Necessarily true?", then "(1) x²≥x (2) x²<x", then "(3) x²=x" and "(4) None of the above is necessarily true", each at the moment the choice is read.
  - Hand-written: "x=0 not allowed. x=1: 1²=1" appears at "One squared is one".
- Board (right column, y 300-560, below the face bubble). Hand-written rows "(1) 1≥1", "(2) 1<1, no", "(3) 1=1", "x=2: (1) 4≥2" and "(3) 4=2, no", each at its clause.

**Slide 4 "Change the kind of number"** (new)
- 4.1 "Choice number one and choice number four are left. No number can rule out choice number four. So we ask: is choice number one always true? Three or ten would keep choice number one true, just like two."
- 4.2 "To show that the answer can change, we try a different kind of number. Zero, a big number, a negative number, or a fraction, as long as the restriction allows it. Zero isn't allowed here."
- 4.3 "A negative number, minus two. Its square is four, and four is greater than minus two. So choice number one still stays."
- 4.4 "A fraction, one half. One half times one half is one quarter. Is one quarter greater than or equal to one half? No, it's smaller. So choice number one isn't always true, and it's out."
- 4.5 "Only choice number four is left. None of the above is necessarily true, so that's the answer."
- 4.6 "And what if every kind of number gives the same result? Then examples alone aren't enough. Back them with a reason, like with six x plus nine y. It's one and a half times four x plus six y, so it's always twenty-seven."
- Board, in order:
  - Typed carry line "Left: (1) x²≥x and (4) None".
  - Typed "Break (1)? Change the kind: zero, big, negative, fraction".
  - Hand-written "x=−2: 4≥−2, (1) stays".
  - "x=½: ½·½=¼" and "¼≥½, no → (1) is out". These two rows are typed, because the pen has no fraction glyph and the system falls back to typed.
  - Typed "Answer: (4) None of the above" and "The same result every time? → find the reason".
- Condition check: every try respects x ≠ 0, and zero is said to be excluded. The "reason" fallback points back to the 6x + 9y example in part 3 (Case 4), which is in the same lesson.
- Maths: 1 ≥ 1 is true, 1 < 1 is false, 1 = 1 is true. 4 ≥ 2 is true, 4 = 2 is false. 4 ≥ −2 is true. ¼ ≥ ½ is false. Correct.

## Change 3: summary pages (not recorded)
- **t51.json**:
  - Methods table, plugging-in row. "How" now reads: check every restriction; pick an easy allowed number (0 is often the fastest) and say why; work out the question, then every choice; more than one left? another easy number, checking only those. The trap is now: ruling out "cannot be determined" because your examples agreed.
  - Rules table, rewritten: check every restriction first (0 is out only where one forbids it); choose an easy allowed number, say why; more than one left? another easy number; 0 or 1 tie? the next easy number; letters may share a number; percent; not always / always.
  - New rules row: "Cannot be determined" / "None": no number rules it out, so change the KIND of number (x ≠ 0, x² ≥ x fails at x = ½); the same result every time? find the reason.
  - Removed: "Different letters get different numbers" and "The choices must come out different".
  - New trap: ruling out "cannot be determined" / "none" because a few similar numbers agreed.
  - 6 new math checks. All 14 checks pass.
- **t13.json**:
  - New paragraph under the sign-clue table: "**Anything bigger than an absolute value is positive.** If a > |x|, then a > 0. Why? |x| is never negative, and a is bigger than it. E.g. a > |−3|: a is bigger than 3, so positive. In |a+b| < a, the letter a is positive." (real items 2025_spring_q1_19, 2023_spring_q1_08)
  - New grid checks: a > |x| ⇒ a > 0, and |a+b| < a ⇒ a > 0.
  - The "Plug in a number" box also stated the old rule ("Avoid 0, 1, −1 and numbers from the choices…"). It now says: "Check the conditions first, then take an easy allowed number. Here, try a negative too: bars change only negatives. If 0 or 1 make the choices tie, or more than one survives, plug in again and check only those left."
- Both pages were built with `python3 summary_pages.py 13` / `51` and looked at as PNGs. The t51 rules table first overflowed (a nowrap rule column), so the rule cells were shortened and the detail moved to the example column. Both were then built to ~/Downloads/Topic-13-Summary-Page.html and ~/Downloads/Topic-51-Summary-Page.html.

## Checks
- Spec: `python3 math_patches/_ai_vis_t51.py` (all of topic 51): 0 PROBLEMS. The ai_scripts JSONs were rewritten, including the new pt51-plug-numbers-4.json.
- Private builds: `OUT=…/xf-P/test.html` and `AI_HANDWRITE=all OUT=…/xf-P/hw.html python3 build_verbal.py` both exit 0. The first attempt failed inside t33 while another agent was mid-edit; it passed on retry.
- `SRC=<test> python3 ai_check.py pt51-plug-numbers pt51-plug-numbers-2 pt51-plug-numbers-3 pt51-plug-numbers-4`: all OK (and OK on the handwriting build).
- `math_check.py 51` (plain and AI_HANDWRITE=all) gives 0 problems and 0 warnings, but it only covers math topics 1-38, so it touches no t51 videos. So I ran `layoutcheck.py` directly on both builds for the 4 parts: 19 slides, 101 items, **0 layout problems** on each.
- `w19_check.py`: 22 flags. I judged each one. They are the expression readings (needed by W17), short transitions ("Now x equals one.", "First the restrictions.", "A fraction, one half.") and "Why?" with its answer in the same paragraph (W15). No fix needed.
- Frames: I made every step frame of every changed slide from the handwriting build (t24frames.py) and looked at them. Fixes I made after looking:
  - Results were written before they were said, so I split the "3·3−0−0−0=9", "x²+x=0, 3x=0" and "1·2=2, 1·4=4" rows so each result is written at its clause.
  - The cue rows "x=0: 0·1=0" and "1²=1" now appear at the sentence that says them.
  - The CBD check rows were in the top-right corner, so I moved them below the face bubble (y 300-560, like f3t4-f3t7).
  - Lines that wrapped: I split the choices into rows and shortened the summary lines.
  - A typed math "$0$" rendered like "()" in the dump next to a colon or bracket, so those typed lines now say "zero" in words.
  - All the new hand-written rows use ", no", never ✗. The two rows with ½ fall back to typed, because the pen has no fraction glyph.
  - Headless Chrome exits with each frame run (p.kill in the tool), and no stray processes were left.
- Summary pages: t13 and t51 math checks pass, and I looked at both PNGs.

## Read-aloud check
I read every changed paragraph aloud against the frames. Fixes from it:
- "That's often the fastest" became "Giving them the same number is often the fastest" (it was unclear what "that" was).
- "To break the other choice" became "If one other choice is left with it, try to break that choice …" (in the summary, "the other choice" had no referent).
- "This is why" became "That's why".
- The (a+3)(b+3) expression is now said in two sentences, "… times the bracket b plus three. From that product we subtract three a, three b, and a b." The old one-breath reading left unclear what was inside the bracket.

"It" and "that choice" now always refer to a choice named just before them. Every elimination says what we need (W9: "the right choice must give …", "Necessarily true means true for every allowed x"). Every number chosen comes with its reason (W21: "no restriction, so zero"; "zero isn't allowed, so one"; "a different kind"). All paragraphs are **ready**.

## Proposals for recorded videos
None. No topic-51 video has a take, and no recorded paragraph needed a change for this item. A later "cannot be determined" question video would use this lesson, but that is not in scope here.

## Needs Claude
- **Prompter display registry** (`math_patches/_codex_reading_display_20261012.json`, shared, I didn't edit it):
  - Its `scope_replacements` for pt51-plug-numbers-2 are keyed by the old slide.paragraph numbers. They no longer match: old "3.1" is now 4.1, the old "4.1/4.3" (a²b) text is now in part 3 slide 2, and the old "5.1" x(x+1) text is now 3.2. pt51-plug-numbers-3 has a stale `paras/disp` (the formatter re-renders when paras differ, so nothing wrong is shown).
  - pt51-plug-numbers-4 has no entry.
  - Wrong or ugly maths in the current prompter dump:
    - -2 3.2: "x times the bracket x + 1" should read x(x + 1).
    - -3 2.1: "the bracket a + 3, times the bracket b + 3" should read (a + 3)(b + 3), and "a × b" should be ab.
    - -3 2.4 / 2.5: "a² × b", "a × b²" should be a²b, ab².
    - -4 3.3 / 3.5: "x² is greater than or equal to x" could show x² ≥ x.
    - -4 2.2: "the bracket a + b, squared" should be (a + b)².
  - Everything else displays correctly.
- **New course id pt51-plug-numbers-4.** It is created by the build like the other camera parts. Check that the ledger (`video_status.py`) shows it as Record, and that nothing else (student site minutes, plan) needs a manual entry.
- `added_notes` may warn "no note for added video pt51-plug-numbers-4" (the same kind of warning the build already prints for other parts).
