# Her Hebrew touches restored in word problems (topics 24, 25, 26) — 22 Oct 2026

What this restores: the RESTORE items in `hebrew-vs-english-t24.md` (1), `-t25.md` (1, 2) and `-t26.md` (1), checked against
her own lines in `~/Downloads/02-Word-Problems-Original-Subtitles.txt`. W23: when the numbers change, each of her methods
still has to work. Where the September numbers broke a method, the numbers changed. No method was dropped.

**Recording status (checked first):** `video_status.py --list record` lists all four videos (solve-wp24-g076,
solve-wp25-g082, solve-wp25-g089, solve-wp26-g105b), and none has a folder in `~/Documents/Course.recordings/_reading/`.
So none of them has a take, and nothing here needs a re-recording. There are no "Proposals for recorded videos".

**Files edited:** `studio-build/math_patches/_ai_vis_t24.py`, `_ai_vis_t25.py`, `_ai_vis_t26.py` (the AI scripts and the
board), and `t24.py`, `t25.py`, `t26.py` (question data: stem, choices, correct answer, written solution; also the older
studio-script lines and solution lines, so that they match the new numbers). The `ai_scripts/*.json` files were regenerated
by running the specs. Before-copies: `scratchpad/hr-wp/before/`.

---

## 1. t24 · solve-wp24-g076 (nurses): "round 1/3 to 33% when the sum is far from 100"

**Her lines (wp 4994-5001):** "שימו לב אגב שכתבתי 33% ולא 33 ושליש כי ה1/3 הוא כזה זניח … אם הייתי מגיע פה ל100 וקצת או 99 וקצת,
סבבה, אבל ב33 ועוד 75 אני עובר את ה100 כל כך". (Roughly: "note that I wrote 33%, not 33 and a third, because the third is
so small … if I landed at 100-and-a-bit or 99-and-a-bit, fine, but 33 plus 75 goes so far past 100.") Our September
numbers (night shifts 3/10) had no third in them, so the line "For one third, thirty-three percent is only an estimate…"
was about a fraction the student never sees.

**Question data change (t24.py `_rn_q`):** night shifts **3/10 → 1/3**. Stem: "Of a hospital's nurses, $\frac13$ work night
shifts, $\frac34$ drive to work, $\frac14$ are new, and $\frac12$ work part time. Which statement is not necessarily true?"
The choice texts are unchanged, and the answer is still choice 3. Recomputed:

| choice | fractions | percent | |
|---|---|---|---|
| 1 not new + not nights | 3/4 + 2/3 = 9/12 + 8/12 = 17/12 > 1 | 75 + 67 = 142 | forced |
| 2 nights + drive | 1/3 + 3/4 = 4/12 + 9/12 = 13/12 > 1 | 33 + 75 = 108 (108⅓ exactly) | forced |
| 3 new + drive | 1/4 + 3/4 = 1 | 25 + 75 = 100 | **not forced (answer)** |
| 4 part time + not nights | 1/2 + 2/3 = 3/6 + 4/6 = 7/6 > 1 | 50 + 67 = 117 | forced |

The worked example changes from 20 nurses to **12 nurses** (3 new by bus, 9 drive). With 1/3 in the question, 20 is not a
whole number of nurses, and 12 works for every fraction (4 nights, 6 part time). Written solution: the fractions and the
example are updated, and one line is added: "In percent: $\frac13\approx33\%$ (the missing third of a percent changes a sum
by less than $1$, so it matters only when a sum is right next to $100$). Choice 1: $75+67=142$, choice 2: $33+75=108$,
choice 4: $50+67=117$, all far above $100$ — forced. Choice 3: $25+75=100$ exactly — not forced."

**W23, all of her methods:** (1) adding fractions with the whole = 1 (more than 1 → forced; exactly 1 → not forced, shown with
numbers; less than 1 → min 0, never negative) still works. (2) Percent, including her 33-not-33⅓ tip, now works on a
real third. Both complements are still there.

### Script, BEFORE → AFTER (exact)

- **1.1** BEFORE: "Of a hospital's nurses, three tenths work night shifts, three quarters drive to work, one quarter are new, and one half work part time. Which statement is not necessarily true?"
  AFTER: "Of a hospital's nurses, one third work night shifts, three quarters drive to work, one quarter are new, and one half work part time. Which statement is not necessarily true?"
- **1.4** BEFORE: "… Not nights is one minus three tenths, seven tenths."
  AFTER: "Choice number one says, at least one nurse who is not new does not work night shifts. Not new is one minus a quarter, three quarters. Not nights is one minus a third, two thirds."
- **1.5** BEFORE: "Three quarters is fifteen twentieths, and seven tenths is fourteen twentieths. Together, that's twenty-nine twentieths. That's more than one, so an overlap must exist."
  AFTER: "Three quarters is nine twelfths, and two thirds is eight twelfths. Together, that's seventeen twelfths. That's more than one, so an overlap must exist."
- **2.1** BEFORE: "… Three tenths plus three quarters. Six twentieths plus fifteen twentieths is twenty-one twentieths. More than one, so it's true, and choice number two is out."
  AFTER: "Choice number two says, at least one night-shift nurse drives to work. A third plus three quarters. Four twelfths plus nine twelfths is thirteen twelfths. More than one, so it's true, and choice number two is out."
- **2.3** BEFORE: "… Say there are twenty nurses. A quarter, five, are new. Three quarters, fifteen, drive."
  AFTER: "Exactly one doesn't force an overlap. The two groups can sit side by side. Let's see it in numbers. Say there are twelve nurses, because twelve splits into thirds and quarters. A quarter, three, are new. Three quarters, nine, drive."
- **2.4** BEFORE: "The five new nurses come by bus, and the other fifteen drive. …"
  AFTER: "The three new nurses come by bus, and the other nine drive. Every fraction still works, and no new nurse drives. So choice number three is not necessarily true."
- **3.1** BEFORE: "… A half plus seven tenths is five tenths plus seven tenths, twelve tenths. More than one, so it's true."
  AFTER: "… Choice number four says, at least one part-time nurse does not work night shifts. A half plus two thirds is three sixths plus four sixths, seven sixths. More than one, so it's true."
- **4.2** BEFORE: "Three tenths is thirty percent. Three quarters is seventy-five percent. A quarter is twenty-five percent, and a half is fifty percent."
  AFTER: "A third is thirty-three and a third percent. Let's write just thirty-three, and in a moment we'll see why that's fine. Three quarters is seventy-five percent. A quarter is twenty-five percent, and a half is fifty percent."
- **4.3** BEFORE: "Not new is a hundred minus twenty-five, seventy-five. Not nights is a hundred minus thirty, seventy."
  AFTER: "Not new is a hundred minus twenty-five, seventy-five. Not nights is a hundred minus thirty-three, sixty-seven."
- **4.4 (removed)** BEFORE: "For one third, thirty-three percent is only an estimate. Don't round if the sum is close to a hundred. That could change whether an overlap is forced." The tip now comes at choice 2 (5.2), where she gives it.
- **5.1** BEFORE: "… Seventy-five plus seventy is a hundred forty-five. … Thirty plus seventy-five is a hundred five. Again, the overlap is forced."
  AFTER: "Choice number one says at least one nurse who is not new does not work night shifts. Seventy-five plus sixty-seven is a hundred forty-two. That's more than a hundred, so the overlap is forced. Choice number two says at least one night-shift nurse drives to work. Thirty-three plus seventy-five is a hundred eight. Again, the overlap is forced."
- **5.2 (new)** "Now, why could we drop the third of a percent? With it, choice number two would be a hundred eight and a third. Dropping the third changes a sum by less than one. So it matters only when the sum lands right next to a hundred, like ninety-nine and a bit. A hundred eight is far above a hundred, so the overlap is forced with or without the third." (The first draft said "either way". ai_check flags "either" as a word with two pronunciations, so it was reworded.)
- **6.1** BEFORE: "… Fifty plus seventy is a hundred twenty, more than a hundred. That overlap is forced."
  AFTER: "… Fifty plus sixty-seven is a hundred seventeen, more than a hundred. That overlap is forced."

### Board (all hand-written, each row at its clause)

- 1.4 `not new: 1−1/4=3/4` | `not nights: 1−1/3=2/3` ("Not nights is one minus a third").
- 1.5 `9/12+8/12=17/12>1` · 2.1 `4/12+9/12=13/12>1` · 3.1 `3/6+4/6=7/6>1`.
- 2.3 `12 nurses: 3 new` ("A quarter, three, are new") | `9 drive` ("Three quarters, nine, drive").
- 4.2 `nights: 33%` appears at "Let's write just thirty-three". The 33⅓ is said but not written, because she writes only 33. Then `drive: 75%`, `new: 25%`, `part time: 50%`, each at its clause.
- 4.3 `not new: 100−25=75%`, `not nights: 100−33=67%`.
- 5.1 `(1) 75+67=142`, `(2) 33+75=108` · **5.2 new** `with the third: 108⅓, far above 100` at "With it, choice number two would be" · 6.1 `(3) 25+75=100`, `(4) 50+67=117`.

**Placement / prerequisites:** this is the same video and the same spot. It uses the percent method from the lesson
(wp-068 part 2) and the smallest-overlap rule (wp-068). The rounding condition is stated: it is safe only when the sum is not
within 1 of 100. Choice 3's sum is exactly 100, but it has no third in it, so it is exact.

**Read-aloud (against the frames, `scratchpad/hr-wp/fr/solve-wp24-g076/`):** I read each changed paragraph while following
its frame. "A third" always means the night-shift third, named in the sentence before it. In 5.2, "With it" means "the third
of a percent", which is named in the sentence before. "With or without the third" says plainly what doesn't matter. The
board shows each number as she says it. In 4.2, "33%" goes on the board when she says "write just thirty-three". Ready.

---

## 2. t25 · solve-wp25-g089 (two groups, 8 × 58 and 12 × 78): her no-calculation solve

**Her lines (wp 5845-5850):** "נשאר לי 80 ונשאר לי 'אי אפשר לדעת מהנתונים' … לגבי תשובה 4, כבר למדנו מה אנחנו עושים איתה, מה גם
שכאן, אם היה לי מחשבון הייתי יכול לדעת מה הממוצע. זו סתם תשובה שמפחידה אותנו קצת, אנחנו יכולים לפסול אותה … פתרנו את השאלה
הזו בלי לחשב כלום". (Roughly: "I'm left with 80 and with 'cannot be determined from the data' … about answer 4, we already
learned what to do with it, and besides, here, if I had a calculator I could find the average. It's just an answer that
scares us a little, so we can rule it out … we solved this question without calculating anything.") With the September
choices 70 / 68 / 72 / 66, her estimate left two choices, and the seesaw had to finish the question.

**Question data change (t25.py `_rn_q`):** the wrong choice **72 → "It cannot be determined from the information given."**
(the course's usual wording, 37 other questions use it). It goes in place 4, as on the real exam (`_choice_order` puts
"cannot be determined" in (4)). Choices are now: (1) 70 (2) 68 (3) 66 (4) It cannot be determined from the information
given. The answer is still choice 1, 70. Recomputed: (2·58+3·78)/5 = 350/5 = 70, the middle is 68, and 70 > 68. Written
solution, one line added: "Without calculating: above $68$ rules out $68$ and $66$. Both group sizes and both averages are
given, therefore the average has one exact value, and "It cannot be determined" is out too. Only $70$ is left." The studio
script (slide 3) follows: "Cross out choices 2 and 3", plus the "Cannot be determined?" line.

**W23, all of her methods:** (1) the formula, reducing the weights by their common factor ("is it chance? no"); (2) the
estimate, closer to the bigger group, now decides on its own once "cannot be determined" is ruled out; (3) the ratios / seesaw
2 : 3 → 3 : 2, five units of 4 → 70. All three work.

### Script, BEFORE → AFTER (exact), slide 2 "Method 2 · Estimation: the bigger group"

- **2.3** BEFORE: "So sixty-eight, choice number two, and sixty-six, choice number four, are out."
  AFTER: "So sixty-eight, choice number two, and sixty-six, choice number three, are out."
- **2.4** BEFORE: "Sometimes that alone gives the answer. Here two choices are left, seventy and seventy-two. So we need one more step, the seesaw."
  AFTER (three paragraphs):
  - "Choice number four says the average cannot be determined from the information given. Remember, an answer cannot be determined only when the givens allow different answers."
  - "But here every number we need is given, the size of each group and its average. With a calculator, we'd find the average right away. So it has one exact value. Choice number four is just there to scare us, so it's out."
  - "Only seventy, choice number one, is left. We found it without calculating anything, only from the idea that the average is closer to the bigger group."

### Board

- 2.3 `above 68: (2), (3) out` (was "(2), (4)").
- **new** 2.5 `everything given: (4) out` at "So it has one exact value", and choice 4 is crossed out at "so it's out".
- Choice 4 is now a long text, so the four choices stand in four rows, and the question block is taller. The seesaw slide (3) then had one overlap
  (math_check: "items 0.1 and 12 overlap"): the right column's last row, `58+3×4=70`, sat on the choices. That row now
  goes in the left column under the seesaw. In the new frames it is clear of the choices (`fr/solve-wp25-g089/sheet_s3_*.png`).

**Prerequisite check:** "cannot be determined" is taught before topic 25 in the plan order: r26-t22-exam-tools ("Different pairs could fit … So the answer cannot be determined") and the r26-t07 / t22 summaries ("'cannot be determined' only when different allowed cases give different answers"). So one sentence of reminder is enough. That sentence also states the condition behind ruling the choice out: every given needed is there, so there is only one value.

**Read-aloud:** "it" in "So it has one exact value" means the average, which is named in the sentence before. "Choice number four" is always called by its number. The cross on choice 4 comes at "so it's out". Ready.

---

## 3. t25 · solve-wp25-g082 (12 volunteers × 7 bags): "one member can't do more than the whole group"

**Her lines (wp 5310-5317):** "ואם כולם יחד פותרים 48, לא יכול להיות שספיר פותרת 49 … הרי הם לא פותרים מינוס 1 … אולי אפילו היא
פותרת 48 וכל האחרים פותרים 0, זה גם אפשרי, אבל 49 היא לא יכולה לפתור". (Roughly: "and if all of them together solve 48, Sapir
can't solve 49 … after all, they don't solve minus 1 … maybe she even solves 48 and all the others solve 0, that's also
possible, but she can't solve 49.") The older studio script had this line, but the AI script had lost it.

**Question data:** the numbers and choices are unchanged (84, 91, 96, 72; answer 84). One line is added to the written solution:
"So one volunteer alone can fill at most $84$ bags (if the other $11$ fill none), never $85$: no one can do more than the
whole group together."

### Script (new paragraph 1.8, after "Maybe one volunteer filled twenty bags … Together they still fill eighty-four bags.")

- **1.8 (new)** "So one volunteer alone can't fill more than the whole group's total. One volunteer could fill all eighty-four bags, if the other eleven filled none. But never eighty-five, because then the others would have to fill minus one bag."

**Board:** `one volunteer: up to 84` at "One volunteer could fill all eighty-four", then `85? No, more than the total` at
"But never eighty-five". (The first try, "one volunteer: up to 84 (the other 11: 0)", was too long. It shrank to a small font
in the frame, so it was shortened.) This prepares for the biggest-possible-value idea in wp-081-2.

**Read-aloud:** each sentence names "one volunteer" and "the others". The board rows appear as she says them. Ready.

---

## 4. t26 · solve-wp26-g105b (hay): her "estimate first" decides again

**Her lines (wp 6860-6904):** "בשאלה הזו אני רוצה לעשות משהו שאני בדרך כלל לא עושה, אני אתחיל לפתור אותה דווקא בצורה הפסיכומטרית של
הערכת סדר גודל … ובאמת אני רואה שכל התשובות הן יותר מ-5 ימים … 110 דונם זה בדיוק חצי … 100 … קצת פחות … אז אני אוכל קצת יותר
מ-10 ימים, ומתוך התשובות, תשובה מספר 2, 11 ימים … למה הלכתי להערכת סדר גודל? … 100 זה כמעט פי 2, אני יכול בקלות לחשב את
החצי". (Roughly: "in this question I want to do something I don't usually do: I'll start with the psychometric way, an
order-of-magnitude estimate … and really, I see all the answers are more than 5 days … 110 dunams is exactly half … 100
is a bit less … so it will last a bit more than 10 days, and from the answers, answer 2, 11 days … why did I go to the
estimate? … it's almost a factor of 2, so I can easily work out the half.") With 150 sheep, the half-benchmark (18) was not
close to the answer, and the English said "the estimate can't decide". That taught the opposite of her point.

**Question data change (t26.py `_rn_q`, `_sp_line`, `_po_line`):** **150 sheep → 90 sheep**, choices **15 / 18 / 20 / 27**
(answer choice 3, 20). No value 1 to 4 is a choice, so the order is free, and I kept it ascending. Recomputed: 200 × 9 = 1,800
sheep-days, and 1,800 ÷ 90 = 20. The V: (200·1·9)/(1·90) = 20, and 200/90 = 20/9, so 20/9 · 9 = 20. Compare by factors: the
sheep ×9/20 → the days ×20/9 → 20. The estimate: 100 sheep → 18 days, 90 is a bit fewer → a bit more than 18 → 20. 27 = 18 + 9
would need about 67 sheep. Written solution: "90 sheep: $1{,}800\div90=20$ days." plus a new estimate line ("Estimate: half
the sheep, $100$, would make the hay last twice as long, $9\times2=18$ days. $90$ sheep are a bit fewer than $100$, therefore
the hay lasts a bit more than $18$ days. Only $20$ fits."). Both "Compare by factors" lines now use 90/200 = 9/20 → 20/9.
The older studio script has the same numbers.

**W23, all of her methods:** (1) the estimate, now deciding; (2) plugging in numbers (1 unit a day → 1,800 → ÷90 = 20);
(3) the V, team = sheep, work = the hay; and the English "compare by factors". All of them give 20. Her "all the choices are
more than N days" is true again (all four are above 9), so the 6.75 trap and its line are gone, as in hers.

### Script, BEFORE → AFTER (exact)

- **1.1** "… For how many days would that supply feed a hundred fifty sheep?" → "… feed ninety sheep?"
- **1.5** BEFORE: "So six point seven five, choice number three, is out. That's fewer days."
  AFTER: "And really, all four choices are more than nine days. So the question is how many more."
- **1.6 (new)** "Ninety is close to a hundred, and a hundred is exactly half of two hundred. Half is the easiest to work with, so let's go through it first."
- **1.7** BEFORE: "Now an easy number. Half of two hundred is a hundred. Half the sheep make the hay last twice as long. Nine times two is eighteen days."
  AFTER: "Half of two hundred is a hundred. Half the sheep make the hay last twice as long. Nine times two is eighteen days."
- **1.8** BEFORE: "But we have a hundred fifty sheep, more than a hundred. More sheep finish the hay sooner. So fewer than eighteen days."
  AFTER: "But we have ninety sheep, a bit fewer than a hundred. Fewer sheep make the hay last longer. So a bit more than eighteen days."
- **1.9** BEFORE: "So eighteen, choice number two, is out."
  AFTER: "So eighteen, choice number two, is out. And fifteen, choice number one, is fewer than eighteen, so it's out too."
- **1.10** BEFORE: "Twelve and fifteen are left. Both are between nine and eighteen, so the estimate can't decide. Let's find it exactly."
  AFTER: "Twenty and twenty-seven are left. Ninety sheep are only ten fewer than a hundred, a small change. So the days grow only a little above eighteen. Twenty-seven is nine days more than eighteen, half as much again. That's far too much, so twenty-seven is out."
- **1.11 (new)** "So the estimate alone picks twenty, choice number three. Now let's see two exact ways."
- **2.3** "A hundred fifty sheep eat a hundred fifty units a day." → "Ninety sheep eat ninety units a day."
- **2.4** BEFORE: "One thousand eight hundred divided by a hundred fifty. Fifteen hundred is ten times a hundred fifty, and three hundred is two more hundred fifties. So twelve days."
  AFTER: "One thousand eight hundred divided by ninety. We can drop a zero from both numbers. A hundred eighty divided by nine is twenty. So twenty days."
- **2.5** "Let's check it. A hundred fifty times twelve is one thousand eight hundred. That's all the hay." → "Let's check it. Ninety times twenty is one thousand eight hundred. That's all the hay."
- **2.6** "So twelve days. That's choice number one." → "So twenty days. That's choice number three, just like the estimate."
- **3.3** BEFORE: "… We divide by the other two, one and a hundred fifty."
  AFTER: "The question mark is in the time. So the V joins two hundred, one and nine. We divide by the rest, one and ninety." (I changed "the other two" to "the rest" because the prompter showed "the other 2, 1 and 90".)
- **3.4** "Two hundred over a hundred fifty is four thirds, because we divide both by fifty." → "Two hundred over ninety is twenty ninths, because we divide both by ten."
- **3.5** "Four thirds times nine. Nine divided by three is three. Then three times four is twelve days." → "Twenty ninths times nine. The nine cancels the ninth, and that leaves twenty days."
- **3.7** "Choice number one is our answer, …" → "Choice number three is our answer, and I'll see you in the next question."

### Board

- 1.7 `200÷2=100 sheep` | `9×2=18 days` (each at its clause) · 1.8 `90 sheep: a bit more than 18` (first version "90 is
  a bit fewer than 100: a bit more than 18" shrank to a tiny font on the frame → shortened) · **new** 1.10 `27=18+9: far too much`
  at "Twenty-seven is nine days more" · crosses on choices 2, 1, 4 at their clauses (the 6.75 cross is gone).
- 2: `90 sheep: 90 units a day`, `1800÷90=20 days` (written at "So twenty days"), `90×20=1800`.
- 3: the V table 200·1·9 / 90·1·?, `?=(200·1·9)/(1·90)`, `200/90=20/9`, `20/9·9=20 days` (written at "that leaves twenty days").

**Condition / placement:** the estimate is valid because the hay is fixed and every sheep eats the same amount ("Each sheep
eats the same constant amount per day", in the stem). So days and sheep go opposite ways. It is the same video and the same spot.

**Read-aloud:** "it" in "let's go through it first" means the half, named in the sentence before it. "The rest" in 3.3 means the two table numbers outside the V, which are named right after it ("one and ninety"). The frames show each row as she says it. Ready.

---

## Checks

- **Specs:** `python3 math_patches/_ai_vis_t24.py`, `_t25`, `_t26` write all their scripts with no PROBLEMS or other output.
- **Private builds only:** `scratchpad/hr-wp/test.html` and `testhw.html` (AI_HANDWRITE=all). I did not write the Downloads studio file.
  (One earlier build attempt failed in `solve-pt-q16`, topic 51. Another session was editing `_ai_vis_t51.py` at the same
  moment. The rebuild a minute later passed.)
- **`SRC=<build> python3 ai_check.py solve-wp24-g076 solve-wp25-g082 solve-wp25-g089 solve-wp26-g105b`:** all 4 OK on both builds. The one note, "either", is in g076 3.2 ("then no overlap is forced either"). That sentence is older than these changes and I left it as it is.
- **`python3 math_check.py 24 25 26`:** PROBLEMS 0 / WARNINGS 0 / layout 0 problems (288 slides), in both modes. The first
  run found one layout problem, `solve-wp25-g089 #3 items 0.1 and 12 overlap`, caused by the taller 4-row choice list. It was
  fixed as described in §2.
- **Frames:** every slide of the four videos, rendered from the handwriting build and looked at
  (`scratchpad/hr-wp/fr2/<vid>/sheet_*.png`; the first round is in `fr/`). Two rows that had shrunk to a tiny font were
  shortened (g105b `90 sheep: a bit more than 18`, g082 `one volunteer: up to 84`). In the final frames there is no overlap,
  every row is readable, and no row appears before its clause. The new `58+3×4=70` row now sits under the seesaw, clear of the choices.
- **Numbers recomputed:** g076 (17/12, 13/12, 1, 7/6; 142, 108, 100, 117; 12 nurses → 4 / 9 / 3 / 6, all whole);
  g089 (350/5 = 70, middle 68); g082 (12·7 = 84); g105b (1,800/90 = 20; 200/90 = 20/9; 9·20/9 = 20; 18 → 20).
- **Prompter dump:** `scratchpad/hr-wp/prompter.txt` (all paragraphs of the four videos).

## Proposals for recorded videos

None. None of the four videos has a take.

## Needs Claude (prompter display)

These are display issues only. The spoken text is right. They are older patterns that show up inside changed paragraphs:
- g076 ¶4, 7, 8, 16, 18: "at least 1 nurse" shows the word "one" as the digit 1, although it is not a number here ("at least one nurse").
- g076 ¶9: "A quarter, three, are new. 3/4, nine, drive." mixes words and digits ("three quarters" becomes 3/4, but the counts stay words).
- g105b ¶1, 13: "nine days" stays a word next to "200" / "1800" (digits). ¶20: "So the V joins 200, 1 and 9. We divide by the rest, one and 90." mixes "1" and "one". (Before my change, "the other two" was also shown as "the other 2". Rewording it to "the rest" fixed that.)
- g089 ¶5, 16 (unchanged paragraphs): "Eight to 12 is 2 to three", "eight to 12, so two to three".
