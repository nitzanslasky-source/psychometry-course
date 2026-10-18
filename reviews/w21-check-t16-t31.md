# W21 check (say WHY before each step): topics 16, 19, 20, 30, 31

Only unrecorded videos. Source edits are in math_patches/_ai_vis_t16/t19/t20/t30/t31.py, and the ai_scripts/*.json files were regenerated from them.

## t16
**solve-q-r26-t16-04**
- 1.1 "We only need the last digit of the product." -> "To check five, we only need the last digit of the product, because a number divides by five only when it ends in zero or five."
- 1.2 "So it doesn't divide by fifteen either." -> "So it doesn't divide by fifteen either, because fifteen is five times three."
- Not changed: 0.2 "with the smallest group, one, three and five". The line already says "smallest group", and its text comes from the clarity overlay (_codex_script_clarity_20261012.json), which is outside my files.

## t19
**new-operation**: ok, no change
**new-operation-2**: ok, no change
**new-operation-3**
- 3.0 "Subtract sixteen from both sides, and three x is nine. Divide nine by three, and x is three." -> "We want x alone, so subtract sixteen from both sides, and three x is nine. Then divide nine by three, and x is three."
- 3.1 "Let's check it. Three times three is nine, and nine plus sixteen is twenty-five. It works." -> "Let's check it. Three star four has to give twenty-five. Three times three is nine, and nine plus sixteen is twenty-five. That's exactly the given, so it works."
- 3.1 "By the definition, that's five times the bracket k plus two. Divide thirty-five by five, and k plus two is seven." -> "By the definition, that's five times the bracket k plus two. Five times the bracket is thirty-five. So divide thirty-five by five, and k plus two is seven."

**operation-patterns**: ok, no change (each check already compares with the starting number)

**solve-q-549** (method 2, plugging in)
- 1.0 "Choice number one. Diamond of six is thirty-six, and thirty-six times diamond of one is thirty-six times one, thirty-six. Equal." -> "Choice number one. With x as one, six x is six, so the left side is diamond of six, which is thirty-six. The right side is thirty-six times diamond of one. That's thirty-six times one, thirty-six. Both sides are thirty-six, so they're equal."
- 1.0 "Choice number two. Diamond of one is one, and one times one is one. Diamond of one is one too. Equal." -> "Choice number two. Root one is one, so the left side is diamond of one, times diamond of one. That's one times one, which is one. The right side is diamond of one, which is one too. Equal."
- 1.1 "Choice number three. Diamond of five is twenty-five, but five times diamond of one is five times one, which is five." -> "Choice number three. With x as one, five x is five, so the left side is diamond of five. Diamond of five is twenty-five. But the right side is five times diamond of one. That's five times one, which is five."

## t20
**algebraic-understanding**
- 2.0 "Try a is three." -> "a has to be positive, so let's start with something easy and positive. Try a is three."
- 4.0 "That's ten times four, which is forty." -> "Both brackets are given, a plus b is ten and a minus b is four. That's ten times four, which is forty."

## t30
**geo-001**
- 2.2 "then from the first point to the last one is four times three, twelve centimeters, not five times three, fifteen." -> "then from the first point to the last one there are four gaps. So it's four times three, twelve centimeters, not five times three, fifteen."
- 3.2 "a hundred five plus seventy-five is a hundred eighty, and twice that is three hundred sixty." -> "a hundred five plus seventy-five is a hundred eighty. That pair comes twice around the point, and twice that is three hundred sixty."

**geo-001-2**: ok, no change
**geo-001-3**: ok, no change
**geo-001-4**: ok, no change

## t31
**geo-009**
- 4.1 "each half is thirty-five." -> "each half is seventy divided by two, thirty-five."

**geo-009-2**
- 2.0 "Sixty plus fifty is a hundred ten, so the third angle is a hundred eighty minus a hundred ten, which is seventy." -> "Sixty plus fifty is a hundred ten. All three angles make a hundred eighty, so the third angle is a hundred eighty minus a hundred ten, which is seventy."
- 4.2 "The third angle is a hundred eighty minus forty-seven minus sixty-eight, which is sixty-five. And the exterior angle completes sixty-five to a hundred eighty, so it's a hundred fifteen again." -> "The angles of the triangle add up to a hundred eighty. The third angle is a hundred eighty minus forty-seven minus sixty-eight, which is sixty-five. The exterior angle sits next to it on a straight line, so it completes sixty-five to a hundred eighty. It's a hundred fifteen again."

**geo-009-3**
- 4.0 "so together they're longer than a. Move b to the other side, and c is more than a minus b." -> "so together they're longer than a. So c plus b is more than a. To leave c alone, move b to the other side, and c is more than a minus b."
- 4.4 "there's a quick count: twice the shorter side, and then subtract one. Twice four is eight..." -> "there's a quick count: twice the shorter side, and then subtract one. Why? Because the two ends are twice the shorter side apart, and the ends themselves don't count. Twice four is eight..."

**geo-023**: ok, no change

## Checks
- The _ai_vis_tNN.py runs for all five files: no PROBLEMS lines.
- w19_check: the new sentences raise no flags. Dense sentences I added were split. The flags that remain were there before.
- ai_check: everything OK except solve-q-r26-t16-04, which FAILs. Line 6 has 12 "at" phrases but only 9 cues before it, and line 7 has 8 but only 7. The automatic cue passes (_follow / _fill) added anchors for the longer lines 1.1 and 1.2, and the built studio (~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html) still has the old cue count. It should clear once the studio is rebuilt (t16.py ai_redo_t16), which is outside the files I was allowed to edit.

15 videos checked, 8 changed, 15 lines changed.
