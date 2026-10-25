# Teaching Style Guide: how she TEACHES (for the ~800 AI-narrated math scripts)

`TEACHER_VOICE_GUIDE.md` covers **how she sounds**: wording, "right?", "is equal to", "number three is our answer". This guide covers **how she teaches**:
- when she adds an example, and what kind
- how she simplifies
- in what order she explains
- how she checks understanding and heads off mistakes
- what she repeats
- how she runs a question video

It ends with a **script-writing checklist** (R1-R29). Every new AI script should pass it.

Hebrew quotes give the line number in `~/Downloads/0N-*-Original-Subtitles.txt` (alg = 01-Algebra, wp = 02-Word-Problems, geo = 03-Geometry, charts = `charts subtitles.rtf`). English quotes give the video id and the second in her take (`transcripts/*.json`).

---

## 0. What was studied

### Hebrew original subtitles: every math line, read in full

| File | Lines | Lesson units | Question units | Course topics found |
|---|---|---|---|---|
| 01-Algebra (12 sources) | 20,234 | 52 | 157 | 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 (+51 techniques throughout) |
| 02-Word-Problems | 11,057 | 43 | 71 | 21, 22, 23, 24, 25, 26, 27, 28, 29 (+51) |
| 03-Geometry | 10,237 | 38 | 101 | 30, 31, 32, 33, 34, 35, 36, 37, 38 (+51) |
| charts subtitles.rtf | 1,403 | 10 | 5 | 52 |
| **Total** | **42,931** | **≈143** | **≈334** | |

**Coverage gaps in the Hebrew:**
- **Topic 9 (Roots, fundamentals):** no subtitles. alg.txt 5357 is only a production note ("roots fundamentals video, table, then 15 questions").
- **Topic 51 (Psychometric Thinking):** no standalone unit. Its techniques (plugging in numbers, plugging in the answers, estimation, units digit, working from the choices) run through about 60% of all question videos.
- **Missing parts, owner notes only, no subtitles:**
  - the order-of-operations set (topic 1)
  - Equations "advanced B" (topic 7, alg 4459 "in a separate message")
  - every "self-practice / summary" set (all of them appear as placeholders)
- **No Hebrew lesson for:** circular arrangements, "at least one" and conditional probability.
- **Duplicates in the sources:** a video pasted twice (alg 2685/2759; alg 10876/10976), and chart Q4 twice.
- **Verbal (04-Verbal) and the writing task** were out of scope.

**Teacher decision (2026-10-11):** the Hebrew course's teaching moves are THE method to copy. In this English course the teacher is **Nitzan** — never mention any other name for the teacher. For her spoken style, the English takes are the source.

### English takes

All **189** of her recorded math takes (topics 1-14) are transcribed: 64 before this study, 125 new (faster-whisper small.en, same format, `transcripts/*.json`). All 189 takes were lined up with the script she was reading (v19-hybrid studio) in 7 batches, and every substantive departure was logged:
- an added example
- a simplification
- a reason ("why")
- a question to the student
- a trap
- a recap
- a link to an earlier idea
- a method choice
- a cut
- a stumble

The per-batch logs are `scratchpad/tstyle/eng_E*.md`. Counts in this guide marked **(EN)** come from that comparison. Counts marked **(HE)** come from the Hebrew.

---

## 1. The ten findings that matter most

1. **Every rule gets numbers right after it.**
   - (HE) about 90% of rules get at least one concrete number case: A4 50/55, G3 40/45. She says this herself:
     - «סיסמאות ונוסחאות לא ממש עוזרות לי בלי דוגמאות» ("slogans and formulas don't help me without examples", alg 16059)
     - «הרבה מלל לא אומר לי כלום, אני צריך לראות את זה בעיניים» ("lots of words mean nothing to me, I need to see it with my eyes", geo 8889)
   - (EN) when a script line states a rule without numbers, she makes up her own example: 169 additions across 88 of 189 takes. That is about 2.6 per lesson and 0.5 per solution. Some of these improvised examples are weak (36/√4, 18/√9).
2. **The usual is two examples per rule. Counter-intuitive rules get three or more, plus a story.**
   - (HE) the second example changes one thing: a negative, a zero, a fraction, another position, or a non-example.
   - Every "sounds strange" fact gets an everyday story (6 of 6 in Algebra 1-7): 0 is even, you can't divide by 0, a bigger denominator gives a smaller fraction, the remainder of 4÷7 is 4.
3. **She names the mistake before the student makes it, at the step where it happens, together with the gut feeling behind it.**
   - (HE) about 100 explicit "many students get this wrong" moments, around 20 per 50 units.
   - (EN) about 76 of her recorded scripts put a "the trap is choice N…" line **after** the answer. She said it as written in **2**, moved it **before** or **into** the step in 8 ("the first mistake I want to take off from here…"), and dropped it in about 66.
4. **The why comes right after the first example, one step back to something already known.** She skips formal proofs out loud: «אנחנו לא בבגרות» ("we're not in the matriculation exam"), «סמכו עליי» ("trust me").
5. **Question videos solve the problem 2-4 ways.** (HE) 187 of 298 question units (63%) show 2 or more methods:
   - the standard/algebra way first, in almost every case
   - then the "psychometric" way (plugging in numbers or answers, estimation, the choices, a shortcut)
   - then a **verdict**: which way to use, and for whom. (Our course does NOT copy this: no "which way is better" paragraph, see R16.)
   - Our unrecorded solution scripts have 2 or more method beats in 190 of 472 (40%).
6. **She opens a question with a first reaction, not a method.** She reads the stem, restates what is really being asked, and says what makes it hard or what the choices hint at. (EN) a stem/method/first-reaction addition in about 140 of 154 solution takes. (HE) the difficulty is stated in nearly every question unit.
7. **She thinks out loud in questions she answers herself.**
   - (HE) «זאת אומרת» ("that is to say") about 950 times, roughly once every 30 lines; «מה זה / למה / מה זאת אומרת?» several hundred times, each answered immediately.
   - (EN) 364 statements turned into questions, in about 156 of 189 takes. She almost never asks the student to pause and try: (HE) 0 in algebra and word problems, (EN) 5 times in 189 takes.
8. **She simplifies by cutting, not by adding.** Each move gets an honest note on how often it matters on the exam:
   - drops names ("a pretentious name")
   - drops school formality
   - replaces a list of rules with one idea ("it's symmetric", "it's exactly like an equation", "if you don't remember the rule, just plug in")
9. **Questions teach new tools**, «אני רוצה לנצל את השאלה הזאת» ("I want to use this question to…"). About 40 Hebrew question units introduce an idea that appears nowhere else. Lessons end with a recap of the rules (about 85% of lessons). Questions end with a takeaway or verdict (about 60%); ours end with the answer, plus a takeaway only if it is new (R16).
10. **Our scripts are compressed lists. She unpacks them, and that is where she makes mistakes.**
    - (EN) her takes run a median 2.9x the script's words in solutions and 2.5x in lessons, at 167 words per minute.
    - Where she improvises past a dense line, real math slips appear: t06-02 says "2 times minus 2 is 4"; exam-words says "at most 3 … so less than 3"; t08-traps says "with a negative fraction it's the opposite"; the negative case in q-370.
    - Scripts that already contain her additions (the example, the why, the mental math, the method choice) leave nothing to improvise.

---

## 2. Extra examples: when, what kind, how many

### 2.1 How many examples per rule (HE, lesson rules)

| Chunk | Rules | 0 ex | 1 ex | 2 ex | 3+ ex |
|---|---|---|---|---|---|
| Algebra 1-7 | ≈80 | 6 | 28 | 26 | 20 |
| Exponents/roots 8-11 | 29 | 4 | 13 | 8 | 3 |
| Inequalities/abs 12-13 | ≈30 | 4 | 15 | 6 | 6 |
| Primes→Understanding 14-20 | ≈55 | 4 | 14 | 17 | 20 |
| Word problems 21-23 | ≈70 | 8 | 32 | 18 | 12 |
| Word problems 23-27 | ≈45 | 7 | 17 | 11 | 10 |
| Word problems 27-29 | ≈31 | 2 | 10 | 5 | 14 |
| Geometry 30-32 | ≈50 | 12 | 20 | 10 | 5 |
| Geometry 33-35 | ≈45 | 8 | 20 | 7 | 10 |
| Geometry 35-38 | ≈45 | 6 | 25 | 8 | 9 |
| Charts 52 | 31 | 5 | 13 | 8 | 5 |
| **All** | **≈510** | **66 (13%)** | **207 (41%)** | **124 (24%)** | **114 (22%)** |

**In plain words:** almost every rule gets at least one example. Nearly half get two or more.

**Who gets 0:**
- names and definitions she will use right away
- exam-rare facts
- formulas she hands over ("just remember it")

**Who gets 3 or more:**
- anything counter-intuitive
- anything students confuse
- mechanical conversions (% ↔ fraction)

### 2.2 What triggers an extra example

| Trigger (what came just before) | HE count (≈) | Typical case |
|---|---|---|
| A rule just stated in letters or in words | ≈95 | «כמובן שאותיות ונעלמים לא ממש אומרים לנו הרבה, אז בואו נראה את זה במספרים» ("letters and unknowns don't tell us much, so let's see it in numbers", alg 9555) |
| A likely confusion or misconception | ≈60 | remainder of 4÷7 (alg 14935); "his rate is NOT 4" (wp 5972); an arc is "something short" (geo 3492) |
| An edge case: zero, negative, fraction | ≈40 | «ו-0 הוא מספר שלם, זה נשמע קצת מוזר» ("and 0 is an integer, sounds a bit strange", alg 47) |
| A step in a solution that felt too fast | ≈30 | «מי שקשה לו קצת להבין את זה... בואו ניקח את 3... מספר אחר, 7» ("if that's a bit hard to follow… let's take 3… another number, 7", alg 14181) |
| Showing the rule is general ("is it luck?") | ≈25 | «זה במקרה? לא, זה תמיד יהיה ככה» ("is that by chance? No, it will always be so", wp 5817) |
| A counter-intuitive fact | ≈20 | the gambler's fallacy with a roulette wheel (wp 10115) |
| A trap inside the question | ≈15 | «עכשיו קיבלתי 1, אבל ה-1 הזה הוא מול 60» ("now I got 1, but that 1 is opposite the 60", geo 1098) |

**(EN) her takes show the same order of triggers.** Of the 60 examples she added, the triggers were:
- **≈26:** a bare rule with no numbers
  - advanced-powers: script "Break the bases into primes" → *"If I have, let's say, 27 to the power of four… 27 is three to the power of three… three to the power of 12"* [22]
- **≈13:** a "why"
  - t10-power-traps: *"2 to the power of 2 times 5 to the power of 2… it's the same as 2 times 2 times 5 times 5"* [36]
- **≈11:** a new term or pattern
  - t06-03: *"This is what I call a mirror… 2x plus 4y… that's a mirror of 4x plus 2y"* [25]
- **≈8:** a "can't know / not necessarily" claim
  - q-364: *"this might be negative one and this negative two, and this could be 1,000 and 7,000, right? We don't know"* [80]

### 2.3 What kind of example

| Kind | HE (≈) | EN (≈) | Example |
|---|---|---|---|
| Letters → numbers (the same rule as an instance) | 95 | 30% | «נניח ש-a הוא 2 ו-b הוא 3» ("say a is 2 and b is 3", alg 15833); EN q-389 GCD redone with 172 and 112 (about 190 s) |
| Everyday story / image | 100 | 8% | cakes shared among kids (alg 407, 878, 1488), the grocery and the 7-shekel bottle (alg 14940), pizza (alg 855, wp 4361), a bank account (charts 999), a soda can (geo 7906) |
| Same idea, other numbers (2nd/3rd round) | 60 | 40% | «בואו נראה עוד דוגמה, לא עם 2, אלא עם מספר אחר» ("another example, not with 2 but another number", geo 7142); EN roots *"Let's try this again now with 8… 64"* [476] |
| Non-example / counter-example | 55 | 12% | «לא 1/2, לא שבר, לא 0.7, לא 1.3» ("not ½, not a fraction, not 0.7, not 1.3", alg 45); «4.5 לא זוגי, אבל הוא לא אי-זוגי» ("4.5 isn't even, but it isn't odd either", alg 113); EN q-250 *"1 to the power of n is equal to 1 to the power of 5. Does that mean n is 5? No"* [184] |
| Edge / extreme (0, 1, a million) | 50 | 10% | «3 כפול 0, מינוס 4 כפול 0, מיליון כפול 0, תמיד 0» ("3×0, −4×0, a million×0, always 0", alg 401); EN q-363 *"I can divide a positive number by a million and I'm still not getting to a negative"* [110] |
| Simpler numbers first, then the exam numbers | 40 | 25% | the chain ½−⅓ → ⅓−¼ → "and this is already our question" (wp 3851-3879); "twice as fast, half the time; 3 times, a third; 1.5 times, so divide by 1.5" (wp 8010) |
| Same question, one detail changed | 15 | rare | «בואו נראה את אותה שאלה עם נתונים קצת אחרים כדי לראות אם הבנו» ("the same question with slightly different numbers, to see if we understood", wp 5741) |

### 2.4 Rules of thumb drawn from the counts

- **One example is the minimum, two is normal.** The second changes exactly one thing: sign, size, position, or "this one doesn't work".
- **Story for the strange, numbers for the rest.** About 100 everyday images in 143 Hebrew lessons, but almost all are spent on counter-intuitive or abstract rules. She does not use a story for a mechanical step. In her English takes she used almost no stories: her extra examples there are short number cases (2-4 sentences, 10-25 s).
- **The simple case comes before the exam numbers.** «בכוונה בחרתי דוגמא פשוטה, כדי שנלמד את הטכניקה... ולא נסתבך» ("I deliberately chose a simple example, so we learn the technique without getting tangled", wp 1296).
- **Non-examples come right after definitions.** In the intro lesson, 11 of 13 definitions get one.
- **She stops at "always".** After 2-3 instances she generalizes in words: «זה עובד לא משנה איזה מספרים» ("it works whatever numbers we pick", alg 2895). In English: *"Always, no matter what you'll plug into a and b, you'll get two opposites"* (t13-tools 67).
- **She avoids degenerate examples.** «הכי קל לקחת את 1... אבל לפעמים זה קצת מבלבל, בואו ניקח את 3» ("easiest is to take 1… but sometimes that's a bit confusing, let's take 3", alg 16172). Her weak improvised English cases (√4, √9 used to "simplify" a root) show why the script should choose the number.

---

## 3. How she simplifies

| Move | HE (≈) | Examples |
|---|---|---|
| Drop the name, keep the idea | 45 | «מספרים מכוונים זה שם פלצני לפלוס ומינוס» ("'signed numbers' is a pretentious name for plus and minus", alg 178); «לא ממש מעניין אותנו שמות של בית ספר» ("school names don't really interest us", geo 118); «פחות משנה העניין של השמות, אנחנו לא בבגרות» ("the names matter less, we're not in the matriculation exam", alg 4840); EN she cut "LCM", "lower power", "most precise means" and used plain counting instead: *"they both contain two Qs"* (q-389 71) |
| One big idea instead of a list | 30 | «פשוט זוכרים שמשולש שווה שוקיים הוא סימטרי» ("just remember an isosceles triangle is symmetric", geo 584); «אי שוויון זה בעצם כמו משוואה» ("an inequality is basically like an equation", alg 8735); «שטח פנים זה המעטפת ועוד שני הבסיסים בכל הצורות» ("surface area is the wrap plus the two bases, in every shape", geo 6144) |
| "You don't need the rule, just plug in" | 25 | «אני לא צריך לזכור את כל הכללים אני פשוט מציב» ("I don't need to remember all the rules, I just plug in", alg 16358) |
| Smaller / rounder numbers first | 45 | «למה שעה? הכי פשוט, למה לא? למה להסתבך?» ("why an hour? simplest, why not? why complicate things?", wp 7402); «נצמצם את כל ה-20, ל-2» ("we'll shrink all the 20s down to 2", alg 18100) |
| Break the step down, then say you'd skip it in practice | 50 | «כל השלב הזה... רק בשביל ההסבר, בפועל... תגיעו מפה ישר לכאן» ("this whole step is only for the explanation; in practice you go straight from here to here", alg 2367); «למי שקשה נחלק פעמיים» ("if it's hard, divide by 2 twice", geo 4004) |
| Mental math said out loud in easy pieces | 40 | «53 ועוד 86, נחבר עשרות - 50 ועוד 80 זה 130» ("53 plus 86: add the tens, 50 plus 80 is 130", geo 193); EN *"30 times 44, how did I do that? Well, what's 10 times 44? 440…"* (q-386 117); mental-math breakdowns appear in most solution takes, and in all 10 lessons of one batch |
| An image or analogy | 100 | cakes, pizza, a neighbour digit "lending a ten" (alg 293), the grocery, folding paper (geo 577), squashing a rectangle into a parallelogram (geo 1772), "Avivatya" merging two workers into one (wp 6670), the trees as "workers drinking" (wp 6946); EN *"99 copies of 41"* (t05 117), *"three apples plus two apples"* (roots 656), *"turn them into the same language"* (roots 605), *"the family of roots… same umbrella"* (t09 162) |
| Draw or see it | 60 | «בואו נצייר אותם רגע בתור מלבן» ("let's draw them as a rectangle for a moment", wp 2220); grid paper to count (geo 7144); «נעלים רגע את הקו» ("let's hide the line for a moment", charts 1103) |
| Map the new onto the known | 35 | «תחשבו שזו בעיית הספק שהעבודה שלי היא פשוט להתקדם» ("think of it as a work problem where my job is just to move forward", wp 6988); «בעצם אותו תרשים... רק מחברים את הנקודות בקו» ("really the same chart… we just join the points with a line", charts 393) |
| Reassure at the scary point | 60 | «מפחידים אותנו עם אותיות, אז מה? הכל פשוט» ("they scare us with letters, so what? It's all simple", alg 2686); «וואו, קצת אוויר, בואו נעבוד שלב שלב» ("wow, take a breath, let's go step by step", wp 1114); «זה נראה הרבה יותר מפחיד ממה שזה באמת» ("it looks much scarier than it really is", geo 6003) |
| Honest about how often it matters | 70 | «סביר להניח גם שלא ניתקל בזה, סתם לידע» ("we probably won't meet it, just so you know", alg 4918); «שני הכללים האלה אתם יכולים לשכוח» ("you can forget these two rules", wp 7029); «את 8, 15, 17 באמת שלא צריך לזכור» ("you really don't need to memorize 8, 15, 17", geo 1014) |

**The pattern:**
1. Strip the topic to its core: «תכל'ס, ההבנה בשאלה הזאת היא בסך הכל קחו את 24» ("bottom line, the understanding in this question is just: take 24", alg 14143).
2. Say what you may ignore.
3. Show it on the smallest numbers.
4. Only then give the general sentence.

She never simplifies by being vague. The general sentence is always exact.

---

## 4. Order: how she builds an explanation

| Order | HE share (≈510 rules) | When she uses it |
|---|---|---|
| rule → example | ≈44% | definitions, routine rules |
| rule → example → why | ≈10% | the working rules (exponent laws by expansion; "let's understand why") |
| rule → why → example | ≈10% | when the why is one step back (angles on a line, 100 is divisible by 4) |
| example → rule | ≈14% | rules she wants students to discover: the remainder pattern 1, 2, 3, 4, 0 → "the biggest remainder is one less than the divisor" (alg 15002-15021); stacking cubes → the mean formula; "let's understand what's behind it before we learn it" (wp 5650) |
| puzzle / question first → rule | ≈8% | «מה זה 8 לב 5? כרגע אני לא יכול לפתור... אז בואו, אני אגדיר» ("what is 8 ♥ 5? I can't solve it yet… so let me define it", alg 18827); "why do we even need divisibility signs?" |
| "remember it for now" / skipped why | ≈12% | formal proofs, exam-rare facts, things not yet taught («אנחנו עוד לא למדנו חזקות... אני פשוט לא רוצה לבלבל אתכם», "we haven't learned powers yet… I just don't want to confuse you", alg 1253) |

**When the why comes:** almost always **right after the first example**, as «למה?» ("why?") plus one line that goes back to something known:
- «למה זה? כי פה יש לי כאילו זוגי ועוד 1, ופה זוגי ועוד 1, וה-1 מכאן וה-1 מכאן מתחברים יחד ויוצרים לי 2» ("why? because here I have even plus 1 and here even plus 1, and the two 1s add up to a 2", alg 16017)
- When the picture isn't convincing, she says so and switches tool: «קשה לי להבין למה זה פי 9, אז בואו נראה את זה רגע בנוסחה» ("it's hard for me to see why it's ×9, so let's look at it in the formula", geo 7933)

**When she skips the why on purpose, she says she is skipping it:**
- «אנחנו יכולים להוכיח את זה... אבל סמכו עליי, חבל להסתבך סתם» ("we could prove it… but trust me, no point getting tangled", alg 2673)
- «אני יכול להסביר... אבל אני לא צריך» ("I can explain… but I don't need to", alg 16391)
- «במבחן אתם לא באמת מתחילים להוכיח נוסחאות» ("in the exam you don't really start proving formulas", geo 2286)

**Lessons and questions use different orders:**
- **Lessons** mostly go rule → example.
- **Question units** almost always go example → named technique → "why is this good?" (W1 counted 17 such cases). New tools are born inside a question: «העיקרון הזה מאוד חשוב, אנחנו נשתמש בשאלה הזאת כדי להרחיב אותו» ("this principle is very important, we'll use this question to expand on it", geo 2955).

---

## 5. Checking understanding, and naming mistakes and traps

### 5.1 Questions she asks and answers

- **(HE)** «זאת אומרת» ("that is to say") 137-174 times per chunk. «מה זה...?» ("what is…?"), «מה זאת אומרת?» ("what does that mean?"), «למה?» ("why?"), «מה המסקנה?» ("what follows?") come several hundred times. **She always answers them herself, immediately.** «נכון?» ("right?") is rare in algebra (3) and frequent in word problems (44 in one chunk).
- **(EN)** 116 statements in the scripts became questions:
  - *"When is x times y negative? Only when they have opposite signs."*
  - *"How do I get rid of y?"* (q-367 29)
  - *"Can I already circle it and move on? I can't, because I may have another one"* (t08-01 98)
  - *"Agreed?"* (q-363 34)
- **She does not ask the student to stop and try.**
  - (HE) 0 times in algebra or word problems. Twice in geometry: «מי שרוצה שיעשה פאוז ויספור» ("whoever wants to can pause and count", geo 1897), and "pause and think" (geo 5533).
  - (EN) twice: *"Try to pause for a moment and try to see if you find a way to really match these exponents"* (t08-traps 165).
  - Her real check is the **self-check example**: «אם הייתי לא בטוח... מה יותר גדול, 12 כפול 7 או 11 כפול 7?» ("if I weren't sure… which is bigger, 12 times 7 or 11 times 7?", alg 1521); «אם אנחנו לא בטוחים, אנחנו נעשה תמיד דוגמה מספרית» ("if we're not sure, we always do a number example", alg 3046).

### 5.2 Mistakes and traps

| Move | HE (≈) | Example |
|---|---|---|
| "Many students get this wrong", said **before** the step | 100 | «שימו לב, טעות מאוד נפוצה של תלמידים... מבטלים... ואסור» ("watch out, a very common student mistake… they cancel… and that's not allowed", alg 2572); «המקום שבו תלמידים טועים בדרך כלל» ("the place where students usually go wrong", alg 14933) |
| The student's gut feeling, in their voice | 30 | «יאללה כבר צריך לצאת עץ» ("come on, it must be tails by now", wp, gambler's fallacy); EN *"even though consecutive, we feel like it's the next one"* (exam-words 194), *"a lot of times we think that they'll just cancel out, because I have here a square root and a square"* (roots 154), *"minus x is not negative"* (q-362 108), *"from our high school math we're used to finding x and then y"* (t05 201) |
| A catchy counter-rule | 15 | «אחוז לא יכול לעמוד לבד» ("a percent can't stand on its own", wp 3648); «אחרי המ' בא השלם» ("after the word 'of' comes the whole", wp 3727); «כפול זה תמיד פי 2» ("double is always ×2", wp 1196); «תן למסכן» ("give it to the poor one", wp 2008); «אני מתעלם מהקו» ("I ignore the line", charts, said 7 times) |
| She makes the mistake herself, then catches it | 6 | «הטעות שלי... צמצמתי את שני האגפים ב-x בריבוע... אבל אסור היה» ("my mistake… I divided both sides by x², but I wasn't allowed to", alg 3928); the 12 planes → "wait, it's not in the answers, what am I missing?" (wp 8662) |
| "Wait!" right before the trap | 10 | «רגע, אין בכד כדורים לבנים» ("wait, there are no white balls in the urn", wp 9862) |
| Process traps in questions | 40 | «אסור לי לסמן. למה? כי אני מציב מספרים, לא באמת פתרתי» ("I mustn't mark it. Why? Because I'm plugging in numbers, I haven't really solved it", alg 2870); «שאלות כאלה שנראות פשוטות... יש שם איזה שהיא מלכודת» ("questions like this that look simple… there's some trap in there", alg 1920) |

**Placement.** In Hebrew the trap comes **before** the step or **at** the step, almost never as a list after the answer. Her English takes confirm it:
- 25 solution scripts ended with "The trap: choice X…".
- She said that line in **2**, and both times she moved it to the start: *"the first mistake I want to take off from here is it's just not equal to a to the power of n"* (t08-01 25), *"I could already mark off 3 and 2 because…"* (t04-04 60).
- In our 472 unrecorded solution scripts, 64 still put the trap after the answer.

---

## 6. Repetition: what she repeats, and what she never over-explains

**She repeats:**
- **End-of-lesson recap.** About 85% of Hebrew lessons («זהו, עד כאן... ראינו...», "that's it, so far… we saw…"; "let's sum it up"). The recap is 2-6 lines that restate the rules, often bringing the lesson's image back.
- **"So again, what did we do?"** after a worked example: «שוב, מה עשיתי?» ("again, what did I do?", alg 757); «בואו נעבור שוב על הטכניקה» ("let's go over the technique again", alg 1171); «אז שוב, מה עשינו» ("so again, what did we do", wp, 9 times in one chunk).
- **Mantras, word for word, across lessons:**
  - «כפל באלכסון... זה מנטרה, אני 'אפמפם' לכם כל הזמן» ("cross-multiplying… it's a mantra, I'll keep drumming it into you", alg 1632)
  - «בפסיכומטרי לא בודקים אם אנחנו מחשבוני כיס» ("the psychometric exam doesn't test whether we're pocket calculators", alg 570, geo 3840)
  - «אני פוסל 3 תשובות» ("I rule out 3 answers", three times in four lines, alg 2881)
  - «במבחן מסמנים וממשיכים» ("in the exam, mark it and move on", ≈30 times)
- **Links back** («כמו שלמדנו», "as we learned"): ≈190 in the Hebrew. (EN) 108 added "what did we say about…?" lines.

**She never over-explains:**
- names of terms (said once, then dropped)
- formal proofs (skipped out loud)
- rare facts (labelled rare, a single line)
- mechanical steps the student already has ("that's a technical step from algebra", wp 1146)
- in English: final verification lists, bonus extensions, "if they'd asked for the largest" tails (cut in most takes; 456 cuts in 189 takes)

---

## 7. Question videos: the anatomy

| Step | HE frequency | What she says |
|---|---|---|
| 1. Label | most question units | «שאלה לדוגמה, שאלה ברמת קושי בינונית פלוס» ("a sample question, medium-plus difficulty"). In English, skip the label. Keep the **reading of the stem** (EN: at least 101 of 154 solution takes). |
| 2. Restate the ask | ≈50% | «זאת אומרת, לא שואלים אותי מה זה x, שואלים אותי כמה פתרונות שונים» ("so they're not asking me what x is, they're asking how many different solutions", alg 3948); EN *"So what are they asking?"* |
| 3. First reaction / what makes it hard | ≈40% | «הקושי בשאלה הזאת נובע משני פרמטרים, מהנתונים ומסגנון התשובות» ("the difficulty here comes from two things: the givens and the style of the answers", alg 6950); EN *"I see that all the answers here are with one term, right? So I need to turn this into one term"* (t08-01 7), *"what will trap me the most here is the square root of x"* (t03-03 13). About 140 of 154 EN solution takes add a line like this; most scripts don't. |
| 4. Announce the methods | ≈50% | «נפתור את השאלה בשתי גישות: פתרון מתמטי, פתרון פסיכומטרי» ("we'll solve this in two ways: the math solution and the psychometric solution", alg 6612) |
| 5. Standard way first | ≈90% of multi-method units | Reversed only on purpose: «נתחיל דווקא באופציה השנייה, ההבנה כאן טיפה מורכבת» ("we'll actually start with the second option, the understanding here is a bit complex", alg 1928) |
| 6. Choosing numbers to plug in, with the reason first | ≈60 units | «המספר הנוח ביותר להצבה עם חזקות זה 1, כי 1 בכל חזקה נשאר 1... קודם כל נבחן שהתשובות שונות זו מזו» ("the most convenient number to plug in with powers is 1, because 1 to any power stays 1… but first we check that the answers come out different", alg 6741); «מומלץ להציב 3... מספר מספיק קטן» ("it's best to plug in 3… a small enough number", geo 10211); «נציב 100... תכף גם נבין למה» ("we'll plug in 100… and in a moment we'll see why", wp 3717) |
| 7. Eliminate in order, never mark the first match | «נפסל» ("ruled out") ≈150 times | «אני פוסל 3 תשובות, אני לא מחפש את התשובה הנכונה» ("I rule out 3 answers, I'm not looking for the right one", alg 2881); EN *"Can I already circle it and move on? I can't…"* |
| 8. Exam vs lesson | ≈60 units | «במבחן מסמנים, ממשיכים הלאה. בשיעור אנחנו נבחן גם את התשובה הרביעית» ("in the exam you mark it and move on; in the lesson we'll also check the fourth answer", alg 3162). EN: she checks the choices in order and asks "can I circle it yet? No, eliminate three" in many takes. |
| 9. Verdict: which way, for whom | ≈100 units | «לרוב התלמידים עדיף להציב, אלא אם כן אתם ממש ממש חזקים באלגברה» ("for most students it's better to plug in, unless you're really, really strong in algebra", alg 6828); «שכל אחד יבחר מה שנוח לו» ("everyone should pick what's comfortable for them", alg 2070); «פתרנו בשתי דרכים אבל הדרך המומלצת... הפתרון המתמטי, חשוב לשלוט ביסודות» ("we solved it two ways, but the recommended way… is the math solution, it's important to master the basics", alg 1791) |
| 10. Takeaway / transfer | ≈60% | «ברגע שעצרנו לחשוב... אם היינו רצים ומחשבים... היינו שורפים זמן יקר» ("once we stopped to think… if we'd rushed into calculating… we'd have burned precious time", alg 4404); EN *"False means no x. True means every x."* (q-323 107), *"when they're looking for x plus y… first see if you have any direct way"* (t06-03 293) |
| 11. Use the question to teach a tool | ≈40 units | «אני רוצה לנצל את השאלה הזאת כדי שנכיר יחד שלושה מצבים» ("I want to use this question so we get to know three situations together", geo 6814) |

**What she believes about the answer choices** (geo 7400-7435): the choices help more than they trick. In hard questions the common-mistake value is usually not among them. That is why she uses the choices from the start (≈20 of 34 geometry units). **Plugging in is "a safety net", not magic:** «זה חשוב, אבל לא להתלהב מזה יותר מדי... מה שאתם יודעים לפתור אלגברית תפתרו אלגברית» ("it's important, but don't get too excited about it… whatever you can solve algebraically, solve algebraically", alg 2933).

---

## 8. Lesson videos vs question videos

| | Lesson | Question |
|---|---|---|
| Opens with | why the topic matters and how often it shows up («יש כ-5 שאלות מתוך 20», "there are about 5 questions out of 20"; «נושא שהרבה תלמידים חוששים ממנו... וחבל», "a topic many students are afraid of… and that's a shame") | the stem, read and restated; the difficulty; a first reaction |
| Examples | 2-3 per rule, escalating; stories for strange rules | one problem, 2-4 methods; "let's see the same question with other numbers" |
| Order | rule → example → why | example → technique → why it's good → verdict |
| Mistakes | the misconception behind a rule | process mistakes: marking early, a wrong substitution, the wrong whole |
| Voice | chatty, jokes (about 1-2 per lesson), personal ("as you know me") | tighter, almost a formula: «נתון... שואלים... נפתור בשתי גישות... תשובה X... בואו נראה עוד שאלה» ("given… they ask… we'll solve it two ways… answer X… let's see another question") |
| Ends with | a recap of the rules + "I'll see you in the next video" | a verdict + a takeaway + "let's see another question" (ours: the answer, a takeaway only if new, no verdict, R16) |
| Exam strategy | frequency, importance, what to skip | time, "mark it and move on", the question's place in the section, NITE habits |

**Note for the AI course.** The teacher has said ideas should be taught inside the question video that uses them (memory: teach-in-question-videos). The Hebrew does the same: about 40 question units introduce a tool. So lessons stay short, and question scripts carry the "lesson" moves (example, why, trap) at the point of use.

---

## 9. Our scripts compared with her

### 9.1 The 667 unrecorded math scripts (v19-hybrid; 472 solutions, 195 lessons)

| Feature | Our solution scripts | Her (HE / EN) |
|---|---|---|
| Read the stem first | 4 of 472 | almost always / at least 101 of 154 takes |
| Say "choice N" | 466 of 472 | "number three is our answer" |
| Contain a "why" | 72 of 472 (15%) | after almost every rule |
| Name the student's mistake | 21 of 472 | ≈2 per Hebrew unit with a trap |
| Trap placed after the answer | 64 of 472 | never; she moves it before |
| 2 or more method beats | 190 of 472 (40%) | 63% of Hebrew questions |
| CAPS for stress | 224 of 472 | stress is carried by words |
| Median length | 188 words (solutions), 325 (lessons) | she speaks 2.1x / 2.8x that |

### 9.2 What she adds when she reads them (EN, all 189 takes: 34 lessons, 154 solutions, 1 with no script)

| Departure from the script | Count | Takes with ≥1 |
|---|---|---|
| Cut (traps after the answer, final checks, bonus tails, formal terms, "which route is best" closers, teasers) | 456 | ≈173 |
| Question to the student, asked and answered | 364 | ≈156 |
| Method talk: first reaction, what the choices hint, why this plug-in number, the cue that picks the method | 242 | ≈140 |
| Reason added ("why", "why am I allowed to divide by x?") | 230 | ≈146 |
| Simplification: sub-steps, mental math, image, plain word before the term | 194 | ≈125 |
| Extra example | 169 | 88 (≈2.6 per lesson, 0.5 per solution) |
| Recap or closing takeaway / general rule | 152 | ≈100 |
| Stumble (dense line, or improvising past the script) | 126 | ≈100 |
| Link to an earlier idea ("what did we say about…?") | 108 | ≈85 |
| Trap she named herself (new, or moved before the answer) | 57 | ≈45 |

**Trap lines placed after the answer:** about 76 scripts had one. She said it as written in 2, moved it into or before the step in 8, and dropped about 66.

**Other measures:**
- "right?" about 2 per minute in solutions and 1.3 per minute in lessons.
- She reads the stem first in at least 101 of 154 solution takes (strict word-overlap test, so the true figure is higher).
- She almost never says "choice N" (8 times in 154 solutions). She ends on the value plus a general rule.
- She often swaps in her own method (powers first, "subtract diagonally", "call the bracket k", consecutive squares) and drops a scripted third method.

### 9.3 What the scripts systematically lack

1. A number example for each rule line. Without one she improvises, sometimes badly.
2. The question that leads into each step ("How do I…?", "40% of what?").
3. A first-reaction line based on the stem or the choices.
4. The reason for each plug-in number, said **before** it is used.
5. Mental math spelled out (scripts give bare results such as "Thirty times forty-four: 1,320").
6. Traps as warnings **before** or **at** the step, with the gut feeling behind them.
7. A one-line takeaway, only when it teaches something new (no verdict, R16).
8. Plain language in place of formal terms (LCM, "lower power", "most precise").
9. Contrasts split into separate short lines. Her factual slips cluster in packed contrasts: primes "20 needs TWO twos, 150 has only one"; "at least / at most"; root ↔ power both ways.

---

## 10. Her Hebrew moves in English: phrase bank for scripts

| Hebrew (job) | Use in English |
|---|---|
| זאת אומרת (unpacks the line) | "So what does that mean? …" / "In other words, …" / "That just means…" |
| בואו נראה את זה במספרים (rule → numbers) | "Let's see it in numbers." |
| למה? כי… (the why) | "Why? Because…" / "Why does this work?" |
| שימו לב (flags what follows) | "Now careful here." / "Watch out for this one." (not "Notice:") |
| הרבה תלמידים טועים פה (predicts the mistake) | "A lot of students slip here…" / "Most people would say…" |
| זה נשמע קצת מוזר (counter-intuitive) | "This sounds a bit strange, but…" |
| אנחנו לא בבגרות (drops formality) | "We don't need to prove it. This isn't high-school math, it's the psychometric." |
| סתם לידע / נדיר (rarity) | "This is rare on the exam, so just so you know…" |
| לא לפחד / זה לא נורא (reassurance) | "It looks scary, but it's really not." / "If you don't remember it, that's fine, you can plug in." |
| נפתור בשתי גישות (announces methods) | "We'll solve this two ways." |
| איזו גישה עדיפה? (verdict) | Not used: no "which way is better" paragraph (R16). |
| במבחן מסמנים וממשיכים (exam vs lesson) | "In the exam you'd circle it and move on. Here, let's check the rest too." |
| אני רוצה לנצל את השאלה הזאת (teach through the question) | "I want to use this question to show you something." |
| אז שוב, מה עשינו? (recap) | "So again, what did we do?" |
| אני ממתין לכם בסרטון הבא (sign-off) | "I'll see you in the next video." |

**Hebrew mnemonics that need ONE fixed English version before mass production** (see gaps):
- «חמסה בת מצווה בר מצווה» = 5-12-13 ("hamsa, bat mitzvah, bar mitzvah")
- «ריקודי עם... איי שתיים שלוש ארבע» = the area of an equilateral triangle, a²√3/4 (folk-dance count "a, two, three, four")
- «חזקיהו בשמיים, השורש באדמה» = fractional powers (a pun on the name Hezekiah: "the power in the sky, the root in the ground")
- «משולש בורקס» = the 30-60-90 triangle (named for its burekas-pastry shape)
- «תן למסכן» = which side to double ("give it to the poor one")
- «אחרי המ' בא השלם» = after "of" comes the whole
- «האלכסון הוא אסון» = a long diagonal is bad ("the diagonal is a disaster", a rhyme)
- «אביבתיה» = two workers merged into one (the names Aviva + Batya)

---

## 11. Cautions found in the sources

- **Decimal estimates.** The Hebrew uses √2 ≈ 1.4, √3 ≈ 1.7 and "π, even 3.1 is enough" (alg ≈8441, geo 1652, geo 3678), and "√72 ≈ 8.5". These clash with the saved rule "no decimal estimates". Don't copy them; use whole-number benchmarks.
- **Plug-in number advice differs between chunks:**
  - "plug in 0 or 1, the smallest" (alg 15100)
  - "avoid 0 and 1"
  - "plug in 3, not 1 or 2, because 1 and 2 usually leave two answers standing" (geo 10211)
  - "2, when it makes a convenient special case" (geo 8141)
  - The common rule behind all of them is in R15.
- **Her recorded takes contain real math slips**, almost always where she improvised past a dense or bare line. These need a re-record or patch decision (see the decisions list). Full lists with timestamps are in `scratchpad/tstyle/eng_E1-E7.md` §6.
  - **Clear errors in the spoken rule:**
    - r26-t01-exam-words: "at most 3… less than 3"
    - r26-t08-traps: "with a negative fraction it's the opposite"
    - fraction-multiply: "dividing by a fraction makes the number smaller", and "6×7 = 56"
    - exponents: "only if 0 is positive"
    - multiply-divide: 8·47 "went up a bit"
    - linear-equations: "can't multiply by x unless told x≠0"
    - systems: "two equations, that's why we have two unknowns"
    - r26-t07: "no two numbers multiply to a negative"
    - q-289: q⁻⁴ "lives downstairs"
    - q-366: "reciprocals add up to zero"
    - compare-fractions: several slips
  - **Wrong steps with the right final answer:** t06-02 (2·(−2)=4), q-370 (negative case), q-329, q-328 (self-fixed), q-333, r26-t12-02, r26-t12-03 (three slips), q-326 (says answer 4 vs script 3), q-099.
  - **Takes recorded from an older script version** (numbers don't match the board): q-095, q-096, q-098, q-099, and parts of roots, q-097, q-133, r26-t02, fraction-multiply.
  - **Trimming:** q-324 and r26-t12-01 have stray speech at the end; q-297 stops before its 2nd/3rd methods.

---

## 12. Settle these BEFORE mass production

**Decided 2026-10-11:** (1) copy the Hebrew course's moves; the teacher is Nitzan, no other name. (3) mnemonics: find cute English tricks (proposals pending approval). (4) R15 plug-in rule approved. (6) no cap on methods. Topic 51 (psychometric thinking): the teacher records ALL of it herself.


1. **Whose method is the Hebrew course?**
   - The Hebrew narrator is male ("Elad", wp 6298).
   - Confirm that these teaching moves are the ones the AI course should copy: "in the exam / in the lesson", humour level. (Verdicts: decided, not copied, R16.)
   - Confirm that the AI voice should still sound like her English takes.
2. **Content with no Hebrew source:**
   - topic 9 (Roots fundamentals: no subtitles)
   - topic 51 (no standalone unit)
   - topic 7 "advanced B"
   - the order-of-operations set
   - every self-practice/summary set
   - circular arrangements, "at least one" and conditional probability

   Scripts for these have nothing to be checked against. Verify them against real NITE exams first (memory: verify-before-adding-content).
3. **One English version of each Hebrew mnemonic** (list in §10): hamsa/bar-mitzvah 5-12-13, the folk-dance area count, «חזקיהו בשמיים», «בורקס», «תן למסכן», «אחרי המ' בא השלם», «האלכסון הוא אסון», «אביבתיה». Decide: translate, replace, or drop. Then use the same version everywhere.
4. **One plug-in policy.** The Hebrew gives three different defaults ("0 or 1", "avoid 0 and 1", "plug in 3"). R15 proposes one rule; approve it or change it.
5. **Official method verdicts per topic.** DECIDED: no verdict paragraph at all (R16). Her takes soften the script's recommendations ("both are fine") and sometimes reverse them: the ears method, plugging in, multiplying an inequality by a minus, "the math is recommended". The AI should say the same thing every time. Decide per topic family which method is "for most students".
6. **Length and budget.** Following the checklist roughly doubles a script: solutions about 400 words, lessons 600-1,000. That is about 800 videos × about 3 minutes of audio. Check ElevenLabs credits (Starter plan), and decide the cap: at most 2 methods per question? Check all four choices or only "mark it and move on"?
7. **Mechanical clean-up of the 667 unrecorded scripts before narration:**
   - 64 trap-after-answer lines
   - 466 "choice N"
   - 224 CAPS
   - 468 scripts with no stem reading
   - one decimal estimate in the script itself (r26-t11-01: √5 ≈ 2.24)
8. **Recorded takes with math slips or old-version numbers** (§11). Decide for each: re-record, cut and patch with the AI voice, or keep.
9. **Terminology clashes to fix in the glossary.**
   - "cross-multiply" is used both for comparing fractions and for adding fractions.
   - "reciprocals" vs "opposites".
   - The "common factor / common denominator" slip.
10. **Voice settings.** `ai_scripts/_voice.json` says multilingual_v2 (PVC, segmented, mix 3), while the memory notes mention eleven_v4 and other stability values. Confirm the final settings once and update the memory note.
11. **"Pause and try."** Neither she nor the Hebrew does it. Decide whether the AI course should have none (default) or one per lesson.

## 13. Deeper pass on her English takes (2026-10-11)

All 189 takes were re-read in full, against their scripts. They were also re-transcribed with word timestamps and measured for pauses and pitch with parselmouth. Full results are in four places:
- `NITZAN_PHRASE_BANK.md`: her phrases by function, with counts, and slips vs flavour.
- `NITZAN_RHYTHM_DELIVERY.md`: pace, pauses, pitch, and the punctuation / [pause] rules P1-P13.
- `NITZAN_TAKES_LESSONS.md`: where she struggled, and the passages that flowed best.
- `scratchpad/tstyle/added_by_nitzan.json`: what she added in every video, cleaned and math-checked.

What is new compared with §9:
1. **Her additions must travel into the AI re-voice.** There are 849 additions. **444 are rated keep**, in **163 of 189** videos: 187 in lessons and 257 in solutions. The largest groups are explanations (94), reasons (90), examples (54), warnings (43) and alternative methods (39). Each one has a cleaned, math-checked line in her words. 174 slips are flagged, and their clean lines are corrected.
2. **She speaks in questions.** 29% of her sentences end in "?". Of those, 12% are "right?" and 17% are real questions she answers at once: 1,128 of them, a median 0.36 s later. Her joints are "So" (a quarter of all sentences), "Now" (new step), "because" and "and therefore".
3. **She names the answer by its value.** 85 of 154 solution takes never say a choice number. She says the verdict calmly and low (about 1.7 semitones below her median), with no pause for effect.
4. **She stresses logic words, not numbers.** "always", "only", "not", "can't", "still", "every" and "also" carry the pitch peaks: about +1.6 st and +2.5 dB over other words. Numbers get length (about 40% longer per syllable), not pitch. The key idea is held by an extra example or reason, never by slowing down: key-idea sentences run at the same pace and have the same pauses as other sentences.
5. **Pace by section.** Explanation runs at about 201 wpm and recap the same. Calculation is 22% slower and stem reading 18% slower. 27% of every take is silence, mostly board-writing that the AI won't need. Her sentence-end pause (median 0.41 s) equals the pipeline's 0.42 s line gap.
6. **Struggles.** There are 378 struggle spots in 163 takes. The top 10 most-struggled takes are all lessons. They cluster in four places:
   - signs and "bigger/smaller" for negatives
   - formulas and brackets read aloud
   - roots ↔ powers ("the root is on top": her mnemonic flips the rule)
   - improvised examples
   
   75 are real math slips said aloud, nearly all where the script gave a headline instead of an exact sentence.
7. **Models to imitate** (101 marked):
   - a self-question chain with one-sentence answers
   - side-by-side numbers that change one thing
   - plain-word meaning ("99 copies of 41")
   - one image, then the rule
   - a parallel 6-10-word capsule at the end ("False means no x. True means every x.")
8. **No fillers to copy.** Her hesitation is a stretched "iiis / aaand" before a value, about 2.9 per minute, never "um". The AI should not script fillers, "sorry", or "..." (344 in ai_scripts today). Her Hebrew-shaped structures ("also the top and also the bottom", "I have here") stay. Her word slips ("equals to", "full number", "the psychometry", "cubed root", "how would it look like") are corrected.

**Unchanged decisions (2026-10-11):**
- The teacher is Nitzan.
- No cap on methods.
- **Exact decimals are fine** (teacher, 2026-10-12): counterexamples like 1.1, 0.9 and 0.2 are her style. Only decimal ESTIMATES of roots and π (√42 ≈ 6.5, π ≈ 3.1) are banned; use whole-number benchmarks for those.
- **Never drop or merge a Hebrew method** (teacher, 2026-10-11). Every method of her Hebrew solution gets its own method in the English script, even when it overlaps another (change the numbers if needed). Each stands on its own from the givens (R30), is explained clearly and kept tight; where it overlaps another method, one sentence says what is different about it. Extra methods may be added, never fewer.
- R15 is approved.
- Topic 51 is recorded by her.

## Method names (one vocabulary) — teacher, 2026-10-15

Teacher: "What happened to naming the methods the same way, so students get a sense of the general thinking we use?"
Her Hebrew (all three subtitle files + the topic-51 source) names almost every solution with **one small core set**: she
splits every question into **פתרון מתמטי** (the math way, ~296×) and **פתרון פסיכומטרי באמצעות …** (a psychometric way,
~200×) and names the psychometric one with a super-method: **הצבת מספרים** (~189×), **הצבת תשובות** (~60×),
**הערכת סדר גודל** (~71×), plus **הברקה** (an insight, ~86×) and **הבנה** (understanding, ~112×). Topic techniques
(שיטת הציר, שיטת ה-V, שיטת הריבועים, ספרת האחדות, סימטריה, מינימום-מקסימום…) come **after** the core:
"פתרון מתמטי באמצעות שיטת הציר" (algebra 17927). She announces the plan first ("נפתור את השאלה בשתי גישות: פתרון
מתמטי, פתרון פסיכומטרי", ~69×) and opens each method with its name ("נתחיל מהפתרון המתמטי", ~54×; "נעבור לפתרון
פסיכומטרי באמצעות הצבת מספרים", ~49×; "בואו נפתור בדרך נוספת - בדרך של הברקה").

**Labels.** A method label (the slide title "Method N · X"; in geometry the sidebar of `SM(...)`) is
`Method N · <core>` or, only when the technique helps, `Method N · <core>: <specific>` (lower-case specific, short).
`math_patches/_method_names.py` `CORE` holds the list; every `_ai_vis_tNN.py` calls `check_vocab(VIDEOS)`, so a script
with any other name stops on its first run.

| English (label) | Her Hebrew | When to use it | Spoken start (R13, no "Our first method.") |
|---|---|---|---|
| **The math way** | פתרון מתמטי (מלא / סטנדרטי / טכני), הדרך המתמטית / האלגברית / הטריוויאלית / החישובית, בניית משוואה | the school solution: algebra, an equation, a formula, the topic's rules, a full calculation. Usually first (R13). | "Let's start with the math way." / "The math way first." / "Now the math way, with algebra." |
| **Plugging in numbers** | הצבת מספרים (also הצבה, "נציב 100") | letters (or a free amount: 100 for percents, a ratio) replaced by numbers we choose; R15 | "Now let's plug in numbers." / "Let's plug in x is …" |
| **Plugging in the answers** | הצבת תשובות | the choices are numbers and the story gives conditions to check; start with the round / convenient one | "Now let's plug in the answers." |
| **Understanding** | פתרון באמצעות הבנה, שאלת הבנה, פתרון (מתמטי) הבנתי | reasoning about signs, sizes, parity, order, a rule we know, without calculating; most absolute-value / number-line / sign questions | "Now by understanding." / "Let's solve it by understanding." |
| **Estimation** | הערכת סדר גודל ("חישוב בערך") | rule out choices by the size (or sign) of the answer; π ≈ a bit more than 3; whole-number benchmarks only | "Now let's estimate." / "with an estimate" |
| **Insight** | הברקה (פתרון פסיכומטרי הברקתי) | an idea that belongs to this one question ("not a method you learn") | "Now the insight." / "with an insight" |

**Specifics** (after the colon, only when they help): two cases, number line, square both sides, prime factors, common
factor, shortcut formula, tag it, one letter, listing, place values, columns, the arrows, a helper line, the angle sum,
Pythagoras, the side ratio, subtract areas, partial calculation (her "מתמטית עם חישוב חלקי"), the diagonals →
under **The math way**; last digit (ספרת האחדות), the extremes (מינימום-מקסימום), symmetry (סימטריה), a ratio (יחסים),
the zig-zag rule, the overlap rule, even and odd, the median → under **Understanding**; trial and error (ניסוי וטעייה, a
word-problem technique) → under **Plugging in numbers**; the V method (שיטת ה-V) and the squares method (שיטת הריבועים)
→ under **The math way** when word problems are written. Two methods of the same core in one video get a specific each
("Method 1 · The math way: the side ratio", "Method 2 · The math way: Pythagoras").

**Where they are introduced.** Topic 51 (day 6 of the plan) teaches the math way, plugging in the answers, plugging in
numbers, estimation and insights by these names ("super-methods"). "Understanding" is not one of her topic-51 lessons:
she uses it from absolute value on ("רוב שאלות ערך מוחלט בבחינה הן שאלות הבנה") and in Algebraic Understanding (t20).
Topics 30-33 come before topic 51 in the plan, so their first uses say the name with a short why.

## SCRIPT-WRITING CHECKLIST (R1-R37)

Check every AI script line by line. The numbers in brackets are evidence from §1-9.

**Every rule or idea**
- **R1. Full spoken sentences.** 6-14 words (her median is 9), joined with so / because / and. No colons, em-dashes, "..." or "X? Y." fragments. A self-question and its answer stay on one line ("How do I get rid of the root? I multiply by root 2."). Pauses follow `NITZAN_RHYTHM_DELIVERY.md` P1-P13.
- **R2. Define a new term with instances.** "Numbers in a row, like 7 and 8." Plain word first, the official term second.
- **R3. State each rule in one exact plain sentence.** Never vague: she simplifies the path, not the rule.
- **R4. Every rule gets a simple-number example right after it** ("Let's see it in numbers."). Letters → numbers. No rule line without numbers (HE ≈87% of rules; EN 46 improvised additions).
- **R5. Two examples is the norm.** The second changes exactly one thing: a negative, zero, a fraction, another position, or a **non-example** ("but 2 times 4 is 8, no 3 there"). Give 3 or more, plus an everyday story, only for counter-intuitive rules ("sounds strange, but…").
  - **Enough examples** (teacher, 2026-10-11: "make sure they really understand from this and there are enough examples that explain the concepts"): every first-time concept gets at least 2 concrete number examples (the second changing one thing), plus a non-example when it helps. A tool is taught in full inside the question that first uses it; a short lesson only for a tool no question video uses. Reminders stay brief (R29).
- **R6. The why comes right after the first example,** one step back to something already taught: "Why? Because…". If you skip a proof, say so in one line ("We don't need to prove it.").
- **R7. Cut, don't add.** Drop names and school formality. Prefer one idea to a list ("it's symmetric", "it's just like an equation"). Say what can be ignored.
- **R8. At most one everyday image per lesson,** for the hardest idea (shop, cakes, pizza, bank account). Reuse it later instead of inventing new ones. Use no new real names or culture-bound puns without an approved English version.
- **R9. Name the mistake before it happens, at the step where it happens,** with the gut feeling behind it ("A lot of students write 24, because 4 times 6 is 24…"). Never as a list after the answer. At most 2 per video.
- **R10. Stress goes in words, not typography.**
  - Teacher-read scripts: no CAPS, no "!".
  - AI scripts follow the ai_scripts rules: at most one CAPITALISED word and one "!" per video, at the real aha moment.
  - Split contrasts: each side of a contrast gets its own short line with its numbers.
  - The one CAPS word goes on a logic word she naturally stresses (always / only / not / can't / still / every / both), early in a short line. Never on a number or the answer.
- **R11. Say the mental math in easy pieces.** "10 times 44 is 440, times 3 is 1,320." Never a bare result. Every number must be one a student knows by heart or gets in one step: no decimal estimates.
- **R12. Ask and answer.** About one question per step ("How do I get rid of y?", "40% of what?"), answered in the next sentence. No "pause and try" (she never does it in Hebrew), except at most one in a lesson, at a real key step.

**Question videos**
- **R13. Open with:**
  1. the stem, read in plain words
  2. what they really ask ("So they're not asking for x, they're asking…")
  3. a first reaction from the stem or the choices ("All the answers are one term, so…")
  4. "We'll solve this two ways."
  - The standard / algebra way comes first, unless you say why not.
  - No "Our first method / Our second method / And our third method" lines (teacher, 2026-10-11: she skips them, and the on-screen method title already names the method; "just make sure it's flowing"). Announce the methods once, at the start ("We'll solve this two ways, the math way, and then by plugging in numbers."). At each switch, use a natural spoken transition in her style: "Let's start with the math way.", "Now let's plug in the answers.", "Now by understanding.", "And there's a short formula too." Never an abrupt jump into the next method.
  - **Name every method with the ONE vocabulary** (teacher, 2026-10-15; section "Method names (one vocabulary)" above): the title / sidebar is `Method N · <core>[: specific]` and the method's first spoken line says the core word (the math way, plugging in numbers, plugging in the answers, understanding, estimation / an estimate, the insight). Dropping "Our first method." must not drop the name.
- **R14. The answer line is the value plus the number, said calmly:** "So x is 6, choice number two is our answer." (R34: always "choice number N".) Never "choice two", and never a build-up pause before it. (She dropped the number in 85 of 154 takes. The AI must not.) Checks go **inside** the step ("let's check with a = 3"), not in a list after the answer.
- **R15. Plugging in, every time:**
  1. Say which number, where it goes (the whole, the start), and **why**, before using it. Use 100 for percents.
  2. Check that the choices come out different. Avoid 0 and 1 when they make choices tie; 3 is a good default when 1 or 2 leaves ties.
  3. Give different letters different numbers.
  4. Rule out 3 choices; don't stop at the first match. If two survive, use a tie-breaker number.
  5. Call it "a safety net".
- **R16. No verdict; a closing takeaway only when it earns its place.** No "which way is better" paragraph. A takeaway after the answer stays ONLY if it adds a genuine, reusable exam insight the video has not already said (teacher, 2026-10-11: "sometimes the takeaways are relevant, but sometimes they're a bit forced"), e.g. a pattern the exam loves ("the whole question was one fact, two is the only even prime, and the exam loves it") or "the rest of the story is just words to make it look harder". Drop it if it only repeats the steps or the method just shown, or sounds like a forced moral ("once a power passes the limit, stop calculating"). Then "[pause] Okay. I'll see you in the next question." Lessons keep their end recap only when it is the lesson's actual summary content.
- **R17. Teach the idea where it is used.** If a question needs a tool that wasn't taught, teach it there ("I want to use this question to show you…"), with R4-R6. Lesson scripts stay short.
- **R24. Exam vs lesson.** Say once: "In the exam you'd circle it and move on. Here, let's check the others too." Then check the remaining choices briefly, in order.

**Lessons**
- **R18. Open with why it matters,** honestly: how often it appears, where else it shows up, or "this is rare". One or two lines.
- **R19. Link back only to what was taught earlier in the study-plan order** (planData.ts ORDER). Otherwise teach it on the spot.
- **R20. Recap at the end.**
  - Lessons: 2-5 lines restating the rules, in the same words used when teaching them, as a mantra.
  - Questions: "So again, what did we do?" for multi-step solutions.
- **R21. Close** with one nudge (rewatch / try both methods / memorize these) and "I'll see you in the next video / question."

**Tone and calibration**
- **R22. Reassure at the scary point,** not everywhere: "It looks scary, but…", "If you don't remember it, that's fine, you can plug in." Keep the single real aha moment, said in words.
- **R23. Length.** Expect her method to make scripts about 2x the current length: solutions about 350-450 words, lessons about 600-1,000. **Never cap the number of methods** — teacher (2026-10-11): "that's how you learn for this exam — through multiple methods". If a video gets too long, cut bonus tails and repeated final checks first, never a method, the example, the why or the trap.
- **R26. Re-voicing a recorded video:** first paste in her keep=yes additions from `scratchpad/tstyle/added_by_nitzan.json`, using their `clean` lines (in her words, already math-checked). Then fix every `struggles` spot with the exact sentence its `script_fix` asks for. Re-fit the numbers in old-version takes (q-095, q-096, q-097, q-099, parts of roots) to the current board. Keep the trap lines and choice numbers she dropped.
- **R27. Write the exact sentence wherever she improvised.** This applies to contrasts (two parallel lines with numbers), formulas (every term on its own line, with brackets and bars said in words), sign words ("never negative", "zero or positive", "further from zero"), and rules in recaps (word for word as taught). Never let a mnemonic stand in for the rule ("the power goes on top, the root on the bottom").
- **R28. Her words, corrected.** Use her phrase bank: "So…", "Now let's look at…", "What does that mean? It means…", "right?" (once per 3-4 lines), "Perfect.", "this whole thing", "also the top and also the bottom". Correct her slips: "equals" not "equals to", "whole number" not "full number", "the exam" not "the psychometry", "cube root", "what it looks like". Script no fillers, no "sorry", no "Good."
- **R25. Before publishing,** run the math check on every number spoken (her takes show slips exactly where scripts were dense), and confirm no example repeats a Hebrew-course number (memory: questions-differ-from-hebrew).
- **R29. Teach new, remind known** (teacher, 2026-10-11: "have in mind what the students should have learnt up to that stage already. It doesn't mean you don't repeat anything that was ever spoken about, but clearly a bit less than teaching it the first time.")
  - For every idea a script uses, check whether it was taught earlier: in the study-plan order (src/lib/planData.ts ORDER) or in an earlier video of the same topic.
  - Taught before → a SHORT reminder: one or two sentences ("Remember, absolute value is the distance from zero, so it's never negative."), at most one quick example, no new why-derivation, no full example set.
  - Taught here for the first time → the full treatment: the rule, two examples, the why, and the trap (R3-R9).
  - Reminders shrink as a topic goes on: later videos in a topic get shorter reminders than earlier ones.
  - In review files, mark per video which ideas are NEW (taught fully) and which are REMINDERS (brief), so the balance can be checked.
- **R30. Every method stands on its own** (teacher, 2026-10-11, on solve-q-358: Method 2 said "I need numbers that obey both givens, so y is negative and x is positive", but that was the conclusion of Method 1).
  - Never use a result that was found by another method. Start each method from the givens.
  - Let plugging in discover facts by trying numbers, including a failed try when it teaches something ("Let's try a positive y, y is three. Is three smaller than the absolute value of three? No, they're equal. So y can't be positive.").
  - A short "same first step as before" is allowed only when the steps really are identical (e.g. the same algebra up to a point, then a different finish).
  - Comparing at the end is fine ("the same two answers", "six again"); using the earlier answer to pick numbers, cross out choices or skip a check is not.
- **R31. Explain every step: what, why, and what it means for the next step** (teacher, 2026-10-11: "it has to be very explanatory").
  - Every step says WHY, not only what: "Why do I try a positive y first? Because it's the most natural guess, so let's see if it works."
  - Every number chosen gets a reason (easy to compute, keeps the choices apart, fits a given, tests the one thing two choices disagree on).
  - Every elimination says why the choice fails, with the actual numbers ("forty is not smaller than three, so number one is out").
  - After each discovery, say what it means for the next step ("So y is negative. And therefore, for the product to be negative, x must be positive.").
  - A bare step ("Take seven off both sides, and x is two.") gets a short reason when it isn't obvious to a weak student. Keep R1's short spoken sentences and R29's brief reminders: one "because" clause, not a lecture.
- **R32. First time means the full explanation** (teacher, 2026-10-11, after watching q-359: the number-line method was used without being explained).
  - Before calling an idea a REMINDER (R29), check where it was really taught: the CURRENT slides of the topic's camera lesson in the built studio, and every video earlier in the study-plan order. A one-line mention ("the picture: x minus two in bars is the distance from two") does not count as taught.
  - At its first real use, teach it fully: what we are doing, why it works, one or two number examples, and how to read the picture or result. Every later use gets a short reminder.
  - Keep a per-topic list "concept → where it is first taught" (topic 13: below) and use it when writing or reviewing scripts.
- **R33. Say every calculation aloud, in small steps** (teacher, 2026-10-11): "negative nine minus seven is negative sixteen", not only "x is negative sixteen". This applies to every arithmetic step in every method: adding to both sides, dividing, squaring, plugging a number in.
- **R34. "Choice number N"** (teacher, 2026-10-11): when talking about an answer choice, always say "choice number three" ("choice number three is our answer", "choice number two is out", "choice numbers one and four"). Never a bare "number three", which can be heard as the number 3. This replaces the "number N" wording in R14. `ai_check.py` flags a bare "number one / two / three / four" in a solution script.
- **R35. Don't calculate what logic already decides** (teacher, 2026-10-11, on solve-q-387: "don't break it down to 3·3·3·3·3·3"; "first try 3, then 2. And 2, I won't even have to calculate, because it's the only prime smaller than 3").
  - If a value is forced (only one option is left, or the question guarantees an answer exists), say why and skip the calculation: "x is smaller than three, and the only prime smaller than three is two. So x is two." No 2⁶ = 64.
  - A question has one correct answer. Never check whether another option "also works" once the answer is found (teacher, 2026-10-11: "there can't be two answers that completely work"). In q-387: try 3, it's too big, so x is smaller than 3, so x is 2, no calculation. A lesson check of the other choices that teaches something (R24) is still fine.
  - Build powers from the ones the student knows (3³ = 27, times 3 is 3⁴ = 81) instead of writing out long products.
  - Stop as soon as the result is clear: "81 times 3 already passes two digits, so the exact number doesn't matter."
  - After three choices are out, the fourth needs no check of its own (in the lesson, a check is fine only when it teaches something, R24).
- **R36. Exam-level mental math only; anything bigger gets a fast way said aloud, or is avoided** (teacher, 2026-10-13, on solve-q-517: "sometimes you expect students to know big calculations that aren't really expected in the exam, like 26 squared ... So either show how you calculate it fast, or change the numbers so we won't have to calculate something so big, or change the method and show a way to rule out the rest").
  - **Exam-level = what a student may use with no explanation:** times tables to 10 (12 × 12 at most); multiplying by 10, 100 and halving; squares to 15, plus the round ones (20² = 400, 25² = 625, 30² = 900 ...) and 16² = 256 = 2⁸; powers of 2 to 2¹⁰ = 1024, 3⁴ = 81, 5³ = 125; small cubes (to 5³, 6³ = 216 when needed); simple fractions and percents (½, ⅓, ¼, ⅕, 10%, 25%, 50%).
  - **Evidence.** Real NITE exams 2019–2026 (`real_exam/quant_real.md`): the digit puzzles use 11² = 121 (2026 spring, A1 × A1 = 1BB), "aᵃ is a two-digit number" is 3³ = 27 against 4⁴ = 256, and 35A × 4B = 15CC5 (2019 spring) is meant for parity / the last digit, never to be multiplied out. Her Hebrew course: "the numbers here are not too big ... we even need to know 15² and 14² by heart" (01-Algebra subtitles 2948-2954), and in the same question, "if we don't know 15², we all need to know that the result ends in 5" (units digit instead of the square). In the letters lesson's sample question (AB × AB = 2CB, lines 18535-18596) she lists 15², 16², 17² as known, adds at once "and if not, we need to estimate the size: 20² is already 400", and her insight method finds the digit "without having calculated" (18593). Bigger products she splits aloud: 15 × 55 = 10 × 55 + 5 × 55, "and 5 × 55 is exactly half of 10 × 55" (18624-18630). Geometry: "instead of 13² minus 5² and calculating, notice the triple 5, 12, 13" (03-Geometry 1029).
  - **Anything beyond** (two 2-digit numbers multiplied, a non-round square above 16, a 3-digit multiplication or division, a big power, a long sum), in this order of preference:
    - (a) **avoid it with the method**, when the Hebrew does that kind of thing: rule choices out by the last digit, by parity, by a size estimate with round numbers (10 · 10 = 100, 20² = 400, 30² = 900), or by logic (R35);
    - (b) **show a fast way, said aloud with its steps**: split into tens and units (26 · 26 = 26 · 20 + 26 · 6; 55 · 17 = 55 · 10 + 55 · 7); a number ending in 5, squared (25²: 2 · 3 = 6, then 25, so 625); the next square from a known one (26² = 25² + 25 + 26 = 676); times 11 = times 10 plus the number (63 · 11 = 630 + 63); near a round number (29 · 44 = 30 · 44 − 44; 621 − 126 = 621 − 121 − 5);
    - (c) **change the numbers**: same question type and trap with smaller numbers, still different from the Hebrew numbers (memory: questions differ from the Hebrew), the answer-choice order kept (`_choice_order.py`), and the stem, choices, written solution and visuals changed together.
  - A calculation that is already shown with a fast way (e.g. 23 · 37 = 23 · 30 + 23 · 7) is fine. In a video she has already read, a missing fast way is listed for the teacher to decide on a re-read, not changed silently (see Recorded readings).
- **R37. Where a method is taught: core methods in the LESSON, one-off tricks in the question** (teacher, 2026-10-21: "most important is to explain everything well and that every method is taught properly, explained perfectly with extra examples").
  - **Core method** = used in several questions of the topic, or common on the real exam (flip rule, arrow map, multipliers, ratio table, Venn circles, "count each one once", worst luck + 1 …). It is taught in the topic's LESSON: what it is, why it works, 2–3 concrete worked examples starting from an easy one, the trap, and "when you see …, use …". A student who rewatches only the lesson can use it.
  - **Never abstract theory** (2026-10-05 still holds: "all theoretical and in the air" doesn't sink in): every rule is shown on numbers at once, and the lesson's examples are short exam-style cases.
  - **The first question that uses it** applies it slowly and fully: every step, said and written, with a one-sentence link back ("like in the lesson, …"). It does not re-teach the whole why. Later questions: a one-sentence reminder.
  - **One-off trick** (one question only): taught in that question, about 2 minutes (why, examples, the trap; never one line).
  - A lesson that grows past ~5–6 minutes is split at an idea boundary (camera lessons: parts of ~3–4 minutes).
- **Recorded readings** (teacher, 2026-10-11): once she has read a script in the Reading Studio, change its paragraphs only where it matters for learning (a first-time idea not explained, a wrong or missing reason). Small wording rules (R33, R34) are not worth a re-read. Every changed paragraph is flagged "needs re-read" in the Reading Studio.

### Topic 13: where each idea is first taught (R29 / R32)

Study-plan order before topic 13: 1, 30, 2, 4, 31, 6, 8, 32, 9, 10, 33, 51, 39, 42, 21, 3, 43, 22, 41, 5, 7, 44, 23, 11, 24, 49, 12, 45, 25, 40, 34. Topic-13 order: the camera lesson in three parts (`absolute-value`, `absolute-value-2`, `absolute-value-3`), then q-358, q-359, q-360, q-361, q-362, q-r26-t13-01, q-r26-t13-02, r26-t13-tools, q-363, q-364, q-365, q-366, q-r26-t13-13, q-r26-t13-03, q-367, q-368, q-369, q-370, summary.

| Idea | First taught (full) | Later (reminder) |
|---|---|---|
| Sign of a product: same signs positive, different signs negative | topic 1 `multiply-divide` | q-358, q-r26-t13-13 |
| Must / could / cannot / not necessarily; one allowed example | topic 1 `r26-t01-must-could` | q-358, q-361, q-365, q-366 |
| Plugging in numbers for an expression; choices must come out different; 0 and 1 are "lazy" | topic 51 `pt51-plug-numbers`, topic 5 `expression-strategy` | q-362, summary |
| Plugging in the answers | topic 51, topic 31 (`solve-geo31-g040`) | q-359, q-360, q-361, q-367, q-369, q-370 |
| Shortcut formula (a + b)² | topic 4 `r26-t04-formulas` | q-368 |
| Systems: subtract the equations | topic 6 `systems` | q-367 |
| √(x²) = \|x\|; squaring positive numbers keeps the order; check answers in the original equation | topic 9 `roots`, `r26-t09-traps`, `r26-t09-summary` | tools, q-366, q-r26-t13-03 |
| x / \|x\| = 1 or −1 | topic 5 `solve-q-128` | q-362 |
| Inequalities: sign flips with a negative; double inequality, isolate the middle; x² < 9 bands and rays | topic 12 `inequalities`, `solve-q-335`, `solve-q-328` | q-360, q-361, q-369 |
| \|x\| = distance from zero, never negative; \|0\| = 0; letters hide their sign (\|x\| = −x for a negative x) | camera lesson `absolute-value`, part 1 | q-362, q-r26-t13-02, summary |
| Inside first, then the bars | camera lesson, part 1 | summary |
| \|ab\| = \|a\|\|b\|, \|a/b\| = \|a\|/\|b\|; \|a + b\| ≤ \|a\| + \|b\| (equal with the same signs) | camera lesson, part 2 (`absolute-value-2`) | q-366, q-r26-t13-13 |
| Sign clues: \|x\| > x negative, \|x\| = x zero or positive, \|x\| = −x zero or negative | camera lesson, part 2 | q-358, q-365 |
| Bars = a number: two cases | camera lesson, part 3 (`absolute-value-3`) | q-359, q-r26-t13-01, q-r26-t13-03, q-367, q-368 |
| Bars on the big side: open range (two rays); small side: closed range (one band) | camera lesson, part 3 | q-360, q-361, q-369, summary |
| **\|x − a\| = the distance between x and a; why; x + 7 = the distance from −7; reading the picture** | **q-359 Method 2** (the lesson only names it in one line) | q-360, q-361, tools, summary |
| Givens about signs say nothing about sizes; the tie-breaker plug (necessarily = for every pair) | q-358 | q-362, q-364, q-368 |
| "Could be" with two answers and one offered | q-359 | — |
| An expression inside, small side: −7 < inside < 7, then act on all three parts | q-360 | q-369 |
| "Minus x" is positive when x is negative | q-362 | summary |
| A number in front of x: solve the second case all the way | q-r26-t13-01 | — |
| Negative or zero right side: never / always / one solution | q-r26-t13-02 | summary |
| \|x\|² = x² (why); \|a − b\| = \|b − a\| | r26-t13-tools | q-366, q-368, summary |
| m = \|n\| can't be 0 when n ≠ m; dividing a positive number keeps it positive | q-363 | — |
| Same side of zero: you can compare distances; two extreme pictures | q-364 | q-365 |
| Only a negative number changes under the bars | q-365 | — |
| Possible but not necessarily; a common factor comes out of the bars | q-366 | — |
| Flipping one sign made it bigger, so the signs are opposite | q-r26-t13-13 | summary |
| A letter on the right side: the right side must be ≥ 0, check every answer | q-r26-t13-03 | q-367, summary |
| Bars alone on one side, then two options | q-367 | — |
| Equal bars: equal or opposite insides (why: the same distance from zero) | q-368 | summary |
| Double inequality with bars: two bands; the split method | q-369 | — |
| x + \|x\|: split at zero; on the negative side they cancel to zero | q-370 | — |

### Topic 14: where each idea is first taught (R29 / R32)

Topic-14 order: the camera lesson in three parts (`primes`, `primes-2`, `primes-3`), then q-387, q-r26-t14-01, q-388, q-386, prime-tools, q-389, q-390, q-398, q-399, q-400, q-401, q-402, r26-t14-more-tools, q-r26-t14-03, q-391, q-392, q-393, q-396, q-394, q-395, q-397, summary. Topics 15 (divisibility) and 16 (even and odd) come after topic 14.

| Idea | First taught (full) | Later (reminder) |
|---|---|---|
| Prime: exactly two divisors; 0, 1, negatives not prime; 2 the only even prime | topic 1 `numbers` (first taste) and the camera lesson `primes`, part 1 | q-391, summary |
| Odd sum or difference of two primes → one of them is 2 (why: odd ± odd is even) | camera lesson, part 1 | q-391, summary |
| The primes up to 40 by heart, and 97 | camera lesson, part 1 | q-386, q-397, summary |
| Is it prime? Only the primes up to √n (with the why); fake primes 51, 57, 87, 91, 119 | camera lesson, part 2 (`primes-2`) | q-r26-t14-01, q-386, q-391, summary |
| **The digit-sum test for 3** (the lesson says it in one line) | **q-r26-t14-01** (rule, 51 example, 52 non-example) | q-386, q-391, summary |
| 7 has no quick test: divide; counting by sevens; "never forget 7" | q-r26-t14-01 | summary |
| Divisor = factor; prime factors; divisible by every combination of them | camera lesson, part 2 | q-388, q-389, summary |
| Factor trees / prime factorization (150) | camera lesson, part 3 (`primes-3`) | q-389, q-r26-t14-03, every question |
| Is it a divisor? Its primes, enough copies (50 yes, 20 no) | camera lesson, part 3 | q-388, q-394, summary |
| **Unpacking a piece that isn't prime (10² = 2²·5²)** (one line in the lesson) | **q-388** | summary |
| Trial and error | topic 21 | q-387, q-397 |
| Primes on a number line: mark and count; "not including x" | q-386 | — |
| Counting divisors: each exponent plus one, multiply | prime-tools (lesson) | summary |
| GCD = what comes out of both; shared primes at the lower power | q-389 (common factor: topic 4) | summary |
| LCM name and running through multiples | topic 2 `fraction-add` | q-390 |
| Greatest guaranteed divisor = LCM; every prime at the higher power; overlap counted once | q-390 | summary |
| GCD · LCM = a · b | q-390 | summary |
| Building products: only the primes the pieces bring | q-398 | q-400, q-396 |
| Odd times odd is odd | q-398 (topic 16 comes later) | — |
| Factor pairs in order, stop at √n | q-399 | q-393 |
| "Two or more" includes all; build every product in order | q-400 | — |
| √(prime) is never whole; prime / even / odd = whole numbers only | q-401 | — |
| Divisors come in pairs; odd count ⇔ perfect square; exactly 3 ⇔ prime squared | q-402 | q-397, summary |
| Perfect square ⇔ every exponent even; smallest k | more-tools (lesson) | summary |
| **A number breaks into primes in only one way → match exponents** (one line in the lesson) | **q-r26-t14-03** | summary |
| Count how many numbers each prime divides | q-392 | — |
| Take out a common factor → a product of factor pairs; a is the smaller factor | q-393 (common factor: topic 4) | — |
| Build the smallest number from required primes; grow by the cheapest prime | q-396 | — |
| An exponent letter is not a factor; letters as primes → plug in 2, 3, 5, 7 in order | q-394 | summary |
| A prime in a product sits whole in one factor; squaring adds no new prime; never true = not necessarily true | q-395 (must/could: topic 1) | summary |
| Bounding a prime by squares (14² < 200 < 15²) | q-397 | — |

### Topic 15: where each idea is first taught (R29 / R32)

Topic-15 order: the camera lesson in four parts (`divisibility`, `divisibility-2`, `-3`, `-4`), then q-423, q-424, q-425, q-426, q-r26-t15-01, r26-t15-remainder-tools, q-427, q-428, q-429, q-430, q-431, q-r26-t15-15, q-432, q-433, q-434, q-435, q-436, summary. Topic 16 (consecutive numbers, even and odd) comes after topic 15.

| Idea | First taught (full) | Later (reminder) |
|---|---|---|
| Divisibility signs for 2, 5, 10, 3, 9, 4, 8 (with the why for 4 and 8) and 11 | camera lesson `divisibility`, part 1 (11: part 2) | q-423, q-427, q-428, q-429, q-433, q-434, summary |
| A bigger divisor: parts with no common factor (12 = 3·4, the trap 2·6) | camera lesson, part 2 (`divisibility-2`) | q-429, q-430, q-434, summary |
| Remainder: N = divisor × quotient + remainder, remainder < divisor; 5 ÷ 8 leaves 5 (the trap) | camera lesson, part 3 (`divisibility-3`) | q-424, q-425, summary |
| The biggest remainder is the divisor minus one | camera lesson, part 3 | q-425, q-436, summary |
| Dividing by 3 or 9: the same remainder as the digit sum | camera lesson, part 3 | summary |
| A number with remainder 4 by 15 is 15k + 4; changing the divisor (only if it divides the old one), with the why | camera lesson, part 4 (`divisibility-4`) | q-426, q-r26-t15-01, q-435, summary |
| "What could it be" = rule out what it can't be; a fraction of a fraction: build from the inside, multiply the denominators | q-423 | q-427, summary |
| Listing numbers with a remainder by hopping by the divisor | q-424 | — |
| Split off the part that divides; only the last number squared matters | q-426 | — |
| The remainder of a sum / difference / product; a negative remainder → add the divisor | q-r26-t15-01 | q-435, q-436, summary |
| Take away the remainder; divisible by both → the LCM tag | r26-t15-remainder-tools (lesson) | summary |
| A sum of tags keeps only the shared factor; a product of tags multiplies | q-r26-t15-15 | summary |
| Numbers in a row: two → 2, three → 6; a³ − a in disguise | q-432 | summary |
| A percent → a fraction → divisibility | q-427 (percent: topic 23) | — |
| An unknown digit: the possible digit sums | q-428 | — |
| Counting multiples in a range: last − first + 1; one in every 15 vs one in every 17 | q-430 | summary |
| Write every letter with one letter; one failing example is enough | q-431 | q-r26-t15-15, q-435, q-436 |
| Equal values hide the trap: different letters, different values | q-r26-t15-15 | summary |
| Don't plug in values that give 0 | q-432 (plugging in: topic 51) | summary |
| Divisible by 10 → the last digit; the last digit of a product | q-433 (last digits: topic 1) | — |
| Take out the common factor of what's left (900 − 6x = 6(150 − x)) | q-434 | — |

### Topic 16: where each idea is first taught (R29 / R32)

Topic-16 order: the camera lesson `whole-numbers`, then q-457, q-r26-t16-01, consecutive-integers, q-458, q-459, r26-t16-consecutive-sums, q-r26-t16-02, q-r26-t16-03, parity, q-460, q-461, q-462, consecutive-products, q-463, q-464, q-r26-t16-04, q-465 to q-472, summary. Topic 17 (the number line) comes after topic 16.

| Idea | First taught (full) | Later (reminder) |
|---|---|---|
| Sign rules for × and ÷; count the minuses; mixed-sign sums; even powers and \|x\| ≥ 0; −x for a negative x | camera lesson `whole-numbers` | q-457, q-r26-t16-01, q-465, q-466, summary |
| Find the surely positive pieces; the piece that's left decides the sign | q-457 | q-466 |
| Mixed signs: the bigger size wins (−2 + 5, −5 + 2) | q-r26-t16-01 | summary |
| Three ways into numbers in a row: one letter around the middle, the smallest legal numbers (check the choices differ), differences with their signs | consecutive-integers (lesson) | q-458, q-459, q-468, q-469 |
| Counting evens / odds in a range; squares of neighbours b² − a² = a + b | r26-t16-consecutive-sums (lesson) | summary |
| Sum of numbers in a row = count × middle | q-r26-t16-02 | summary |
| Four in a row: the sum is 4a + 6, never divisible by 4; odd count → divisible by the count | q-r26-t16-03 | — |
| Count the odd terms; one even factor; the four division cases; powers keep parity; one plug-in per case, three close ones for ÷ | parity (lesson) | q-460 to q-462, q-470 to q-472, summary |
| Cancel first, then judge parity | q-461 | — |
| An even difference = the same parity | q-462 | — |
| Four in a row → 24; two evens → 4; consecutive evens → 8; count the twos; x² − 1 with x odd → 8 | consecutive-products (lesson) | q-463, q-472, summary |
| The smallest case is only a candidate; a second case that avoids the factor | q-r26-t16-04 | summary |
| Bigger minus smaller is positive, even for negatives | q-465 | summary |
| Start with the choice that pins one case | q-467 | — |
| Don't divide by an unknown that may be 0 | topic 6 (reminder in q-469) | — |
| An odd product: every factor odd; 2k + 1 is odd for every k | parity (lesson) / q-471 | — |

### Topic 17: where each idea is first taught (R29 / R32)

Topic-17 order: the camera lesson in three parts (`number-line`, `number-line-2`, `number-line-3`), then q-493, powers-on-number-line, q-494, r26-t17-reading-the-line, q-495 to q-501, q-r26-t17-01 to 05, summary. Topic 36 comes after topic 17 in the study plan.

| Idea | First taught (full) | Later (reminder) |
|---|---|---|
| The four ranges, borders, the mirror image; × and ÷ by a number above 1 or a fraction; the hierarchy; exceptional powers; same operation; strong on strong | camera lesson `number-line` (part 1: ranges, borders, mirror; part 2: × and ÷, hierarchy, exceptional powers; part 3: same operation, strong on strong) | q-493, q-495 to q-497, q-500, q-501, summary |
| The arrows for powers in each range; a root is a smaller power; what counts as odd; the three steps (keep a negative power); finding the range | powers-on-number-line (lesson) | q-494, q-498 to q-500, q-r26-t17-02, summary |
| Times a negative: the other side of zero, the order flips | r26-t17-reading-the-line (lesson) | summary |
| The smallest product = the smallest factors; one plug-in for "the smallest" | q-495 | — |
| Place the givens on the line; a difference is a distance; one win each = no decision | q-496 | q-501 |
| × a fraction pulls toward 0 on both sides (on the negative side: bigger) | q-496, q-497 | q-501, summary |
| A smart plug-in with a clean root; the powers of a correct chain keep one direction | q-499 | q-500, summary |
| Swap a number that is in every choice (only then) | q-500 | summary |
| Decode a chain; possible but not necessarily | q-501 | — |
| A picture of the line: ranges, trust the order | q-r26-t17-01 | summary |
| The reciprocal flips the order (same sign) | q-r26-t17-03 | summary |
| Push to the edges to break "necessarily" | q-r26-t17-04 | summary |
| Distance, a third of the way, the midpoint | q-r26-t17-05 | summary |

### Topic 18: where each idea is first taught (R29 / R32)

Topic-18 order: the camera lesson in two parts (`digit-puzzles`, `digit-puzzles-2`), then q-512, q-513, q-514, r26-t18-facts, q-515 to q-520, q-r26-t18-01 to 03, summary. Topic 28 (after the charts units 11-15) comes after topic 18 in the study plan.

| Idea | First taught (full) | Later (reminder) |
|---|---|---|
| What the letters mean; the four steps; a puzzle in words → 10A + B and collect | camera lesson `digit-puzzles` (part 1: what the letters mean, 10A + B; part 2: the four steps, a puzzle in words) | q-512, q-515, q-520, summary |
| The ones column (nothing carries in); two numbers, more digits → leading digit 1 | q-512 | q-515, q-516, summary |
| The special digits 0, 1, 5, 6; 5 × even / odd; 6 × even | q-513 | q-517, q-518, summary |
| Plug in when there is nothing to read; the algebraic form; AB ± BA | q-514 | q-520, q-r26-t18-01, q-r26-t18-02, summary |
| One repeated digit; largest / smallest with a digit sum | r26-t18-facts (lesson) | summary |
| Flip a subtraction into an addition (her AA − BB = BB) | q-516 | summary |
| Estimate the size; start from the choices | q-517 | q-r26-t18-03, summary |
| Flip a division into a multiplication | q-518 | summary |
| Take inventory; plug in the choices | q-519 | summary |
| A middle column: 0 or 9 and the carry | q-r26-t18-01 | summary |
| ABC − CBA = 99(A − C) | q-r26-t18-02 | summary |
| The units digit and the size of a product | q-r26-t18-03 | summary |

### Topic 19: where each idea is first taught (R29 / R32)

Topic-19 order: the camera lesson in three parts (`new-operation`, `new-operation-2`, `new-operation-3`), then q-541, q-542, q-543, q-r26-t19-01, q-r26-t19-02, operation-patterns, q-544, q-545, q-r26-t19-03, q-546, q-547, q-548, q-549, q-r26-t19-18, q-550, q-551, q-r26-t19-05, q-552, q-553, q-554, q-555, q-556, summary. Topic 19 comes after topic 37 in the study plan. The signature pictures (the same template, inside out, down and back up) are in "Method visuals library".

| Idea | First taught (full) | Later (reminder) |
|---|---|---|
| A new operation = a definition; the order of the inputs can matter; the exam's symbols | camera lesson `new-operation`, part 1 | q-r26-t19-02, summary |
| Every input goes in brackets; an expression goes in whole | camera lesson, part 2 (`new-operation-2`) | q-r26-t19-01, summary |
| The same template with the input in EVERY slot (the substitution picture) | q-541 | q-544, q-548, q-552, q-554, summary |
| Inside out: the inner value becomes the outer input; don't stop halfway | camera lesson, part 2 (rule); q-542 (the picture, the trap) | q-545, q-550, q-551, summary |
| No definition: put the input into each choice | camera lesson, part 3 (`new-operation-3`) | q-543, summary |
| "Not always" = one counterexample; "always" = algebra; no equal numbers | camera lesson, part 3 | q-r26-t19-02, q-555, summary |
| Zero as a lazy test number → a second number | q-r26-t19-01 | q-549, summary |
| The inverse operation: undo the steps in reverse order | operation-patterns (lesson) | summary |
| An operation on an expression: match the whole input slot | q-544 | summary |
| Conditions: check odd / even at every step | q-545 | q-r26-t19-03, summary |
| Conditions backwards: keep an answer only if it fits its own rule | q-r26-t19-03 | summary |
| A circular rule: down to the start value, back up; the pattern | q-546 | q-547, summary |
| The operation on both sides: isolate it like an unknown (rare) | q-548 | summary |
| The operation in every choice: skip and come back | q-549 | summary |
| Rules that undo themselves (c / x, c − x) | q-r26-t19-18 | summary |
| Read the outer operation first (1, 1, z; a zero in a slot) | q-550 | — |
| Shortcut formulas inside a definition | q-551 (formulas: topic 4) | summary |
| f(k) − f(−k): even powers cancel, odd powers double | q-r26-t19-05 | summary |
| The slot matters; one plug-in when the choices are numbers | q-552 | — |
| Squared brackets: don't open early; (a − b)² = (b − a)² | q-553 | — |
| The biggest power needs the smallest digit | q-554 | — |
| 3/x: reciprocal thinking; a bigger denominator, a smaller fraction | q-555 | — |
| Counting a prime factor: × 5 adds one five | q-556 (factorization: topic 14) | — |

## Clarity style (learned from the 2026-10-12 Codex edits — teacher approved 2026-10-13: "easier for the students to understand, with easier English")

Write every NEW script directly in this style (topics 13–18 got it as an overlay: `_codex_script_clarity_20261012.json`, applied by the topic hooks — never remove it or regenerate without it).

- **Make every reasoning step explicit, in plain English.** No compressed shorthand.
  - Before: "x minus w, x is bigger, so it's positive."
  - After: "x minus w is positive because x is bigger than w."
- **Say what is being compared, and say "because".** Name both sides ("bigger than w", "smaller than z"); give the reason as a full clause.
- **Break algebra into the mini-steps a weak student needs.** E.g. squaring a product: "To square b, square the whole product, two times k. Two squared is four, so b squared is four k squared." Then "Divide the top and bottom by two."
- **State the conditions that make a step legal** ("b is even and not zero, so … k cannot be zero either").
- **Name the plug-in numbers and say why they fit** ("w is negative two, x is negative one… both negative numbers are before zero, just as the given says").
- **Generalise a rule in one sentence before the example** ("A factor pair normally gives two different divisors. If both factors are the same number, that divisor is counted only once.").
- **Adaptive counterexamples.** Start with easy numbers that fit the givens — not a hindsight-chosen "magic" example. Check the choices after each example. Try another easy example only if needed, and say which different feature it tests. Stop when one choice is left. Never conclude "always" from a few samples.
- **Overlapping choices:** don't eliminate a broader description with an example that it also allows; use the general rule.
- **Short sentences, everyday words,** each one easy to read aloud from the teleprompter. Keep the teacher's phrases (phrase bank) and all R1–R35 rules.
- **Keep cue anchors** (`at` phrases) as natural parts of the new sentences.

## Method visuals library (teacher, 2026-10-13: "always check if the visuals change a bit … the V method … the V table and the way it looks, that's what makes it so easy for students to use it. The seesaw method also has special visuals of its own")

**Rule V1. When a method has a signature visual, every video that uses that method must show and build that same visual (same look, built step by step), not a plain list of lines.** Build it in the order she draws it (below), each layer at the spoken words. In the AI-redo plans a figure is a base item plus layers (`over=1`) that must be shown **right after** the base, with no other board item in between (the renderer draws a layer at the y of the last item shown; `_method_visuals.check_layers` enforces it).

**Rule V2. When a slide is cleared mid-solution, the results the next step depends on stay on screen (carry-over box).** A small "So far: x = 2 · choices 2 and 4 left" box is shown with the new slide's first words, in the lighter column (`_method_visuals.carry`, list `CARRY`, or `keep` lists per slide). It is never carried into a new method (each method starts from the givens, R30).

Code: `math_patches/_method_visuals.py` (builders return layers `[('line', base), (key, layer) …]`; `items(_layers, name, out)` turns them into board items; `post(ns, topic)` applies the fixes and the carry-overs at the END of each `_ai_vis_tNN.py`, after Codex's clarity overlay). Every SVG: no width/height on the root, a viewBox, `<title>` + aria-label, strict XML, ink #203344 / teal #087f83 / band #d5f1ed, bold labels, transparent background (layers).

Topic numbers are the course's. Hebrew line refs: alg / wp / geo = `~/Downloads/0N-*-Original-Subtitles.txt`. "Studio" = where the current studio first shows it.

### Algebra

| Method (topic) | What it looks like | Built in this order | First taught (Hebrew → studio) | Builder |
|---|---|---|---|---|
| Column arithmetic on a grid (1, 2) | numbers right-aligned, one digit per square, the carry above the column; decimal points one above the other | the numbers → the line → column by column from the right, carry written above | alg 269-275, 1311 → `add-subtract` s6 | renderer `k:'col'` (static) |
| Fraction shapes (2) | circles cut into equal slices, shaded; two rectangles laid over each other (3/8 + 2/8); mismatched stripes for 3/8 on 2/6 | the whole → cut → shade → (lay over) | alg 642-898, 1091-1203 → `fraction-basics` s2 | `k:'pie'`, `k:'bar'`, `k:'grid'` |
| Butterfly compare (2, 3) | two fractions side by side, the diagonal products written ABOVE the numerators | fractions → one diagonal → its product on top → the other | alg 1443-1640 (a mantra) | none (typed) |
| Colour families of like terms (4) | the like terms in one colour per family | expression → colour each family → collect | alg 2315-2320 | none |
| Solution-set sketch (12) | each inequality's solution as a ray over the axis; the overlap read off | axis → ray 1 → ray 2 → the overlap shaded | alg 9102-9237 → `solve-q-325` | `_shaded_nl.fig` |
| Distance picture of absolute value (13) | \|x − a\| = steps between x and a: the centre marked, arrows r steps each way, a closed band (small side) or two open rays (big side); symmetric "mirror" | line with the centre → right arrow → left arrow → band / rays | alg 11083-11847 → `solve-q-359` | `DIST` (t13-t19) |
| Prime strip (14) | the whole numbers in a row, the primes coloured | the strip → the primes → x and y placed | alg 13738-13742 → `solve-q-386` | `STRIP` (t14-t16) |
| Factor tree (14) | the number at the top, splitting into a circled prime and the rest, down to primes; two trees side by side for "divisible by 9 and 12" | root → each split, prime circled → (cross out the shared prime once) | alg 13812-14068 → camera `primes` s8 (hand-drawn), `solve-q-389` | `TREE` (t14) |
| Divisibility-signs table (15) | the rules for 2, 3, 4, 5, 6, 8, 9, 10, 11 in one table | row by row | alg 14848-14882 → camera `divisibility` | typed |
| Four regions + mirror (17) | ticks at −1, 0, 1 cutting the line into 4 ranges; the negatives as the mirror image | line → −1, 0, 1 → name the ranges | alg 17365-17547 → camera `number-line` | `ZL` (t17-t19) |
| Power arrows (17) | the 4-range line with one arrow per range: right, left, right (odd), left (odd) | the line → the arrow of each range as it is said | alg 17549-17720 → `powers-on-number-line` s3 | `ZL` |
| Letters on the axis (13, 16, 17) | a < b < 0 < c < d placed on an axis, signs over the factors | axis → each letter in order → plug-in values under them | alg 12234-12411, 16520 → `solve-q-496` | `ZL` |
| Stacked letter columns (18) | AB + AD = CDB written vertically, letters by place; the ones column read first, then the leftmost digit | the two numbers + line → the result row → box the ones column → the leftmost digit | alg 18215-18450 → camera `digit-puzzles` | `COLS` (new) |
| The same template (19) | the rule, and under it the SAME template with the input in every slot ("where there was an a, I put the 4") | the rule with its slots → arrows into the copy → the copy with the input → the calculation | alg 18853-18868 | `SLOT` (new) |
| Inside out, coloured (19) | the inner operation coloured, then replaced by its value, which flows into the outer slot | the nested call, inner boxed → the inner row and its value → the value moves into the outer row | alg 18910-18925 ("צבעתי את זה בכתום") | `CHAIN` (new) |
| Down and back up (19, circular rule) | one row per call going down to the start value, then the values climbing back up | each row down (the unknown call boxed) → the start value → each value back up | alg 19048-19114 | `CHAIN(..., up=)` (new) |

### Word problems

| Method (topic) | What it looks like | Built in this order | First taught (Hebrew → studio) | Builder |
|---|---|---|---|---|
| Then-and-now table (22) | rows today / 3 years ago, columns per person (X, X+4 / X−3, X+1) | header → today row → "I stop and continue my table": the then row → the equation | wp 1942-1990 | `RATIO`-style table (typed today) |
| Matching arcs (22) | "boys : girls = 4 : 7", two non-crossing arcs boys→4, girls→7 | words → numbers → the two arcs | wp 1690-1697 | none |
| Fraction bar for stories (22) | the group as a rectangle cut into 8, 7 kept; again for the next stage | rectangle → cut → keep | wp 2213-2267 → `k:'bar'` | `k:'bar'` |
| Ratio table + the triangle (22; reused 23-29, 36) | a column per quantity, row 1 the known pair, row 2 the new value and "?"; ×k across or down, else the diagonal ("triangle value": multiply along the diagonal, divide by what is left) | headers → row 1 → row 2 → the ×k arrow (or the diagonal) | wp 1278-1439 → `solve-wp22-g029` (arrows hand-drawn) | `RATIO` (new) |
| Plug 100, written on the stem (23) | the numbers 100, 60, 40 … written right above the words of the question | pick 100 → write each number on its words | wp 3274-3321 | stem POINTs + typed numbers |
| Percent tree (23) | root = the whole 100%, a split that adds up to 100%, one node splits again (its own 100%); a leaf = the product along its path | root → first split → second split → multiply along the path | wp 3338-3392 (she prefers plugging in 100) | `PCTTREE` (new) |
| Two circles (24) | sail / motor circles; only-A, both, only-B, neither | circles → both first → each "only" → neither | wp 4330-4392 → `wp-067` s2 | `VENN` (new) |
| The squares method (24; also 52) | one rectangle cut into 4 boxes: only A, both, only B, neither; brackets over 1-2 (A) and 2-3 (B) | the 4 boxes → bracket A → bracket B → fill "like a sudoku" | wp 4530-4617 → `wp-069` s3 | `STRIP4` (new) |
| Cube towers (25) | a tower of cubes per value, levelled to the mean | towers → move cubes → level | wp 5175-5253 → `wp-080` s5 | `bars` (legacy) |
| Balance point (25) | the mean on an axis, two values at equal distances | axis → mean → one value → the mirror value | wp 5329-5387 | `ZL` |
| The seesaw (25) | exam form: an axis, the values ABOVE the ends, the weights BELOW, the gap cut into w1 + w2 units, the pivot nearer the heavier side | axis → values → weights → units → pivot (+ the two distances) | wp 5643-5918 → `solve-wp25-g083` (hand-drawn split) | `SEESAW` (new) |
| Formula triangle (26, 27) | work (distance) on top, time × rate (speed) at the bottom; cover the one you want | triangle → the three names | wp 5945-5950, 6999-7014 → `wp-092` s2 | `TRI` (new); legacy `formulaTriangle` |
| Common-time rows (26) | one line per worker, scaled to the same time, then a sum line | worker lines → scale to 6 h → sum → back to 1 job | wp 6165-6206 | typed |
| The V method (26) | team \| work \| time (work ALWAYS in the middle); row 1 given, row 2 asked; a V from row-1 team down to row-2 work and up to row-1 time; multiply the V, divide by the other two; upside-down V when the work is unknown | header → row 1 → row 2 → the V → the rule | wp 6226-6354, 6739-6784 ("when 2 factors change") → `wp-097` s4 (V hand-drawn) | `VTABLE` (new) |
| Merged worker "Avivatya" (26) | two workers bracketed into one named worker | the two → bracket → the new name | wp 6647-6724 | typed (name needs an approved English version) |
| Motion sketch (27) | a road with the cities, the vehicles, the first-stage distance, the gap left, arrows toward each other | road → ends → first stage → gap → arrows | wp 7560-7567, 7096 | legacy `route` |
| Motion table (27) | distance \| time \| speed, a row per leg / body, or one "between them" row | header → rows → the unknown | wp 7175, 7550-7599, 7879 → `wp-106` s5 | `DST` (new) |
| Road in ratio parts (27) | the road cut into 2 + 3 parts, each mover's share | road → the parts → "give them a second" | wp 7244-7419 | none |
| Crash / chase pictures (27) | two vehicles with arrows: toward = add, same way = subtract | vehicles → arrows → the speeds | wp 7442-7498 | none |
| Lap track (27) | an oval track, two karts, a lap counter | track → karts → laps | wp 8061-8283 | legacy `circularMotion` |
| Stage slots (28) | a row of labelled stages with the number of options under each, multiplied | the stages → options under each → × | wp 8289-8627 | typed |
| Handshake graph (28) | countries on a globe / polygon vertices, lines counted twice | points → lines → ÷ 2 (− sides) | wp 8629-8814 | legacy `network` / `polygon` |
| Games table (28) | teams \| games added \| total (1 → 0, 2 → 1, 3 → 3 …), on the exam one row 1 + 2 + … | header → row by row → the short row | wp 9528-9706 → `solve-wp28-g143` | typed table |
| Dice-sum pyramid (29) | sums 2-12, a column of marks for each (1 … 6 … 1); red and blue dice | the sums → the marks → the symmetry | wp 10311-10463 | none (legacy `dice`) |

**Not in the Hebrew** (new material if added): a probability tree, a 3-circle Venn.

### Geometry and charts (one line each; builders are the per-shape figures in t30-t38)
Z for parallel lines (30; geo 109-124) · gold 30-60-90 and silver "borekas" 45-45-90 triangles (31; geo 1053-1194) · the fold line of symmetry (31-32; geo 577) · the squash / stretch shape family (32; geo 1771) · white = grey, and "grey = what minus what" (32-34; geo 2868-3269) · the sector as a pizza slice + the benchmark angle table (33-34; geo 3794-3837) · hexagon splits (34; geo 5660) · the unrolled cylinder (35; geo 6030) · counting cubes in layers (35-36; geo 6942) · grid paper for similarity, then ratio units (36; geo 7144-7253) · the similarity table small \| large + hourglass (36; geo 7440-7703, uses the ratio table's triangle) · slope stairs (37; geo 8896-8928) · opening angle / anchor / push to the extreme (38; geo 9568-9769) · charts: one data set as table, points, line and bars; the 60% boundary line; hide the trend lines; the squares method in a table (52).

### Audit of topics 13-19 against V1 and V2 (2026-10-13)
- Topic 13: the summary's "Distance" slide now draws the distance line (|x + 6| measured from −6). The number-line method videos (q-359, q-360, q-361) already build DIST.
- Topic 14: the 112 ladder in q-389 had a carried item drawn between its root and its layers (it would draw the ladder 14 px off): fixed. The summary's "Break it down" now builds the factor tree of 44.
- Topic 17: the summary's "The arrows" slide now builds the four arrows. q-r26-t17-02 keeps its typed lines (the question itself shows the number line).
- Topic 18: every column layout (q-512, q-513, q-515, q-516 both layouts, q-518, q-519, q-r26-t18-01) is the COLS figure: a fixed grid in the slide's math font (MathJax outlines, `_mathjax_glyphs.json`), ones under ones, the operator in its own cell, the bar above the result; built rows → bar → result at the words, the column being discussed boxed (each layer is a full snapshot, so the box moves), carries small above the column, the digits found so far in teal under the figure; continuation slides show the figure again with what was found. Renderer (studio_handwrite.py): a positioned figure is pushed below the question and fitted above the choices, and a layer with `of` is drawn at its own figure even when other items come in between.
- Topic 19: written with SLOT / CHAIN from the start.
- Carry-over boxes: 25 slides in topics 13-18 (list `CARRY` in `_method_visuals.py`), e.g. q-428 keeps "X = 2, 5, 8" while it checks divisibility by 2.


### Geometry visual toolkit — Rule V3 (teacher, 2026-10-14)

Teacher: "really think about what's the best way to visualize things. Like sometimes we only want to look at a part of the shape, so we can maybe cut out that part. Or if we want to add a radius, or add lines, or explain something general about the shape: all of this needs to be thought about, what's the best way to explain it." And: "when we cut out something … you also need to think about how the student will follow and understand what he's looking at. Like maybe highlight that shape within the original shape and only then pull it out."

**Rule V3. In every geometry explanation, design the visual for each step BEFORE writing the cues: choose what makes it easiest for a weak student to see the idea, and make every transition followable.** The given figure (the question's own figure) stays black and white; everything we add is in the teaching colours. Builder: `GEO(name, layers)` in `_ai_vis_t30.py` (copy it to later geometry topics), a figure built in layers at the spoken words; elements `seg` (a line; dashed for construction lines), `dot`, `txt`, `arc` / `wedge` (an angle; a label = its value), `right` (the right-angle square with its dot), `tick` (equal sides), `par` (parallel arrows), `path` (a Z or U traced over the lines), `tint` (a region), `dim` (fade what is drawn so far, for focus).

The toolkit:
- **Step-by-step reveal.** Never show the finished, crowded diagram at once: the lines first, then each angle, mark or value as she names it.
- **Marking.** Equal sides with tick marks, equal angles with matching arcs, right angles with the square, parallel lines with arrows; a value is written on the figure the moment it is found, so the figure fills up as the solution goes.
- **Highlighting a region or segment.** A tint (or a thick trace, like the Z) on the part being discussed, held steadily until the subject changes.
- **Focus / cut-out.** To look at one part (one triangle, the Z, one crossing): first tint and outline it INSIDE the original while she names it; then dim the rest, or show it again as its own enlarged copy next to the original, with the same labels and the same tint, so the link is obvious; the original stays visible (dimmed) with the part still outlined. When going back, the values found are written on the original figure.
- **Construction lines.** Radii, heights, diagonals and auxiliary lines are drawn IN as she says them, dashed in the teaching colour, distinct from the given figure; point to the endpoints first ("from the bend, parallel to a"), then draw the line.
- **General shapes and properties.** For a general rule (angles on a line, vertical angles, parallel lines), use a clean generic figure, and show the rule again on a second figure (another angle or position, 2-3 variations), not only the question's figure.
- **Moving attention.** Never jump to another part of the figure without a cue: highlight the new part as she names it; the old highlight goes.
- **A new slide or a redrawn figure** keeps the same orientation and labels, and carries the marked values over (V2).
- **Colour coding is consistent within a lesson:** small angles teal, large angles orange (her green / orange), the part under study always the same tint, construction lines dashed teal, a wrong path red.

Checks: render every step of every slide (not only the final state; `t30/frames.py`) and LOOK at the frames before calling a lesson ready. The review file says which technique each step uses, so she can check.

### Written working at the spoken clause — Rule V4 (teacher, 2026-10-14: Codex's camera-lesson review is the standard)

Source: Codex's review of the six recorded camera lessons (absolute-value 1-3, primes 1-3; …/Codex/2026-10-11/…/work/camera-visual-review-2026-10-14/), ported into `_ai_vis_t13.py` / `_ai_vis_t14.py` on 2026-10-14. A student must be able to follow the mathematics on the board without rebuilding expressions from speech.

**Rule V4. Every piece of mathematics she says is written on the board at the clause where she says it, and stays there.**
1. **The starting statement first.** The expression, equation or inequality being discussed is written the moment it is mentioned ("The absolute value of x is bigger than three" -> `|x| > 3` at those words), before any picture, example or answer.
2. **One step per clause.** Each substitution, sign change and intermediate calculation is its own board line (or chunk), shown at its own clause: `x = −3`, then `−x = −(−3) = 3`, then `|x| = 3 = −x`; `−5 + 2 < x − 2 + 2 < 5 + 2` before `−3 < x < 7`.
3. **Completed work stays.** A line is not replaced or cleared while the explanation still leans on it (clearing a slide: V2 carry-over box).
4. **No early answers.** A final answer or result line appears only when she reaches it, even if an earlier sentence mentions the same number.
5. **Pictures support, they don't replace.** A number line, tree or figure never stands in for the starting mathematical statement; both are on the board.
6. **No compressed captions.** A caption that packs several worked steps or several results into one line is split into individually timed lines (e.g. `|ab| = |a||b|` and `|a/b| = |a|/|b|, b ≠ 0` as two cues; `180 = 10·18`, `10 = 2·5`, `18 = 2·3·3` as three).
7. **Ad-libs are written too.** In a recorded take, a calculation she adds in her own words (e.g. "fourteen is fourteen times one", "two squared is four, three squared is nine") gets its written working at those words (anchor on the nearest script words, or `reading_to_video` auto lines for simple `a op b = c` calculations).
8. **Camera lessons: the face bubble never covers math.** The bubble is top right (board x ≥ 1344, y ≤ 256): any item that starts above y = 262 must end left of x ≈ 1330 (use `w` ≤ 850 at x = 410, or move it below the bubble).
9. **Visual cues lead slightly.** Board events (appear, write, highlight, mark) fire about 250 ms before the anchored word (`studio_autonarrate.py` AN_VISUAL_LEAD; audio, slide changes and speed unchanged). A cue that is late by seconds needs a re-anchored phrase, not a bigger lead.
10. **Endpoint wording.** Captions say inside / outside (or show the inequality) for the solution region, never "open / closed" in that sense; strict `<` / `>` means the endpoint circles are open (not included), `≤` / `≥` filled, and the caption says so ("endpoints −3 and 3 not included").

Anchors are always script phrases of the line where she says the words (never time offsets): a recorded take's times change with every re-read and edit.

### Camera lessons in parts (teacher, 2026-10-14)

**Rule.** A topic's camera first lesson is split into parts of about 3-4 minutes (2.5-4.5) at idea boundaries, so she can record each part in one or two takes (on camera, cuts are visible). A lesson under about 4.5 minutes stays one part. Write the lesson as ONE spec and split it with `math_patches/_camera_parts.py` (`CP.split(globals(), id, title, [(1, None), (slide, opening line), ...])` right before the visual passes, and `CP.add_to_course(M, S, topic)` at the start of the tNN.py redo hook). Part 1 keeps the lesson id, part k is `<id>-k`, titles "<Title> (Part k of n)". Each part: its own title slide; a later part opens with one short natural line (no recap of the previous part); every part but the last ends with "Okay. I'll see you in the next part."; a new board (a "So far" box only if the part really needs an earlier result). Content, examples and visuals are not changed by the split. Concept maps name the part ("camera lesson, part 2"). Applies to topics 21+ and topic 51 from the first draft.

## Codex review standard (2026-10-13)

Source: Codex's script review of studio lessons 111-138 (…/Codex/2026-10-11/…/outputs/Claude-script-review-2026-10-13.txt), applied to lessons 112-138 on 2026-10-13. Follow it from the FIRST draft of every new topic, together with R1-R37, the Clarity style and the Method visuals library above.

1. Connect the relevant given to the next action. Explain what the number or letter represents, what we are checking, and why that check answers the question. A student should not have to infer which group, expression, fraction, or input you mean. The students already see and attempt the question before the video, so the explanation does not need a second full retelling of the story.

2. Explain the real reasoning, not an abstract label. Avoid unexplained phrases such as tags, factor inventory, selected factors fit inside, pull it out, or flip its part. Write a concrete mathematical sentence instead: "Both terms are multiples of 3, so their sum is also a multiple of 3." If using a normal mathematical term, explain what it means in this calculation. Do not replace one vague phrase with a longer vague phrase.

3. Add clarity, not padding. Do not put a two-sentence roadmap before a paragraph that immediately gives the same roadmap and calculation. Introduce a method once. Explain a trap at the relevant step, not three times before and after it. Read each changed paragraph WITH its neighbors; a paragraph that sounds clear alone may still repeat the surrounding video.

4. Keep the exam strategy efficient. Start with one easy allowed value or pair. Check the choices immediately. Cross out failed claims immediately. Only choose another simple example if the remaining choices need it. Do not require two or three examples merely because the expression includes division. Do not choose obscure, magically perfect numbers just to eliminate every distractor. Ordinary small values are fine even when they initially eliminate only one or two choices.

5. Use the question's exact logical request.
   - Always / necessarily / must: a failing allowed example rules out a claim. Working examples alone do not establish a universal rule. In a single-answer multiple-choice question, eliminating all other choices can settle the answer.
   - Not always / not necessarily: stop when an allowed counterexample makes the relevant claim fail. No need to test the remaining choices afterward, unless an explicitly separate teaching explanation genuinely adds something.
   - Could be: one fully checked working case is sufficient for a proposed answer; a pattern that is only necessary is not automatically sufficient.
   - Most precise description: if several choices all permit the observed result, another identical type of result may not distinguish them. Use the existing rule to decide which other outcomes are impossible.
   - A choice listing multiple possible solutions must be correct as a whole; one working value does not validate extra values that fail.

6. Keep legitimate shortcuts. Do not calculate a large power if parity, units digits, or an already-established size bound decides the issue. But state the comparison that makes the shortcut valid. A heuristic that merely sounds plausible is not a replacement for the needed calculation.

7. Respect the givens at every step: positive, integer, nonzero, unequal, leading digit, range, and operation domain. Different letters do not automatically mean unequal values. Conversely, if the question requires equality, do not tell students never to choose equal values. Every nested operation's intermediate input must lie in its domain.

8. Use natural spoken English. No title fragments such as "Michal." No "a hard one," "technically," "a sharp insight," "lazy number," or unexplained software metaphors. These labels do not help the student know what to do. Natural transitions like "Now let's check the other condition" are fine. Use complete sentences where the reasoning needs explaining, not compressed notes.

9. Show math as math in the prompter. Preserve the distinction between spoken narration and display text. Use (x+1)², 9−◆(x−2), 3/(a+1), (9n²−1)/4, and √(8x²+y²), with grouping that matches the speech. Check counts versus digit descriptions: "60 three-digit numbers" is not "a 63-digit number." Never silently change spoken values while formatting. Fractions and negative bases need explicit brackets where appropriate.

10. Keep the original fonts and established design. Match graphics to the actual explanation. Use the SLOT picture when replacing inputs and the CHAIN picture when a result becomes the next input; reveal only the step being explained. Make highlights target the particular given or expression being discussed and hold them steadily, rather than flashing the whole question repeatedly. Preserve the current original styling. Do not add a new signature method graphic for a technique the script does not teach.

11. Preserve every useful existing method. Do not invent an extra method just to have two, or convert a shortcut into an unnecessarily formal proof. A second method can be shorter, but it must still make sense when heard after the first. If it reuses a computed value, say that clearly instead of pretending it starts independently.

### Next topics

Apply this standard at first draft, not as a blanket sentence-prefix pass afterward. Start from the question's decision: what do students need to notice to choose the answer quickly? Explain that decision fully, then show the computation or check. Keep earlier-topic reminders short, teach only the reasoning needed here, and use the topic's established signature visual where relevant. If a paragraph does not resolve a genuine ambiguity or teach a useful decision, do not add it.

### Practical notes from applying it (2026-10-13)

- Prompter display (standard 9): the teleprompter formatter does not know the scope of a spoken bracket such as "the bracket x plus one, squared". Read every changed paragraph's display and add a `scope_replacements` entry in math_patches/_codex_reading_display_20261012.json (key "slide.paragraph", 1-based) whenever grouping is wrong: (x + 1)², (a − b)² + a, (y − 3)/2, √(8x² + y²), 3/(a + 1), 8 − (−8).
- Highlights (standard 10): the densify pass adds many POINTs; `_method_visuals.calm()` thins them (no header points, no re-points of the lit target, ≥4 s between changes unless she names a choice / a part of the question / a just-written item). Add a new topic's unrecorded lessons to CALM_IDS.
- Topic-18 lessons are edited through the clarity overlay (original/revised + cue_anchors or reviewed_cues); topic 19+ through the spec itself.

## How Nitzan reads our scripts (Oct 2026 readings)

**Source.** These are her Reading Studio takes from 11-14 Oct 2026 (`~/Documents/Course.recordings/_reading/<id>/`), mostly topics 13-19. There are 121 videos: 21 lessons and 100 question videos.
- The **M marks** were counted in all 121 videos: 1,857 marks over 1,327 paragraphs.
- The **word-level comparison** covers 99 videos, about 413 minutes of final reading. It uses the latest full take of each video plus its patch takes.
- 77 of those 99 reuse existing faster-whisper transcripts (`_voice_real`, Codex `work/*/audio`). The other 22 were queued for small.en and are not in these counts: parity, r26-t14-summary, r26-t15-remainder-tools, r26-t15-01, r26-t15-15, r26-t18-02, and q-395, 397, 423, 425-427, 431, 435, 460-466, 470.
- Attempts she marked with M were taken out before comparing, so these counts describe her **final** reading.
- Whisper writes numbers as digits and sometimes mishears words, so a count of ±10% is noise.
- Scripts are the sidecar `paragraphs`, which is what the prompter showed. The prompter shows math partly as symbols (`math_display`: ³, ², −3, 3/5).
- Analysis files are in `scratchpad/rd/` (`final.json` per paragraph, `agg.json`, `pararows.json`).

### What the numbers say
- **She says about 22% more than the script:** 52,980 words against 43,436. In 357 of 1,051 paragraphs she added a real phrase of 6 or more content words. Most of the rest of the extra words are joints: "so" (934 in the scripts → 1,660 from her), "right?" (3 → 270, about 0.65 a minute), "now" (173 → 369), "also" (36 → 178), "just" (38 → 165), "we have" (16 → 155), "because" (69 → 174), "let's say" (2 → 43).
- **She almost never drops a whole sentence.** Only 91 script sentences (2%) were mostly unsaid, and they fall into a few types (see Simplifications below).
- **Pace while reading:** about 157 words a minute, with pauses capped at 0.6 s. That is the same in lessons and in solutions, and slower than her free teaching (about 200, §13).
- **Stumbles.** She pressed M 3.4 times per 100 script words. The median is 13 marks per video, and 57% of paragraphs got at least one M. After an M she starts the **paragraph** again from its first word.
  - In 970 of about 1,390 failed attempts the words were the script's own, so these were reading slips.
  - In 107 she was rewording or adding something when she stopped.

### 1. Elaborations: what she adds, and what triggers it
These are counted by paragraph, with keyword tagging, so the counts are approximate. The quotes are her words from the final reading.

| What she adds | ≈ paragraphs | Typical trigger in our script | Her words |
|---|---|---|---|
| A **reason** ("because…", "that's why") | 78 | a rule or claim stated bare; a choice ruled out with no why | q-366: "because we're looking for something that is sometimes true and sometimes not, and this one is always" · q-457: "because it can't be negative and it can't be zero" |
| **Her own number example** after a rule | 32 | a divisibility or consecutive-numbers rule with one example or none | q-432: "Let's say I say seven, eight, and nine. So nine divides by three. Let's say I say eight, nine, and ten. Again, nine divides by three, right? Every three numbers, I'll have a number that divides by three" |
| **Link back** ("remember", "we said") | 25 | a tool from the lesson used with no reminder | absolute-value-3: "let's remember that bars on the small side … give us a closed range" · primes: "because we said that two is the only prime that's even" |
| **Factor or mental-math steps** spelled out | 19 (plus many short ones) | "forty-five is nine times five…", "its digit sum is five" | r26-t14-01: "Let's take fifty-one: five plus one is six, and six divides by three … fifty-two: five plus two is seven, so fifty-two does not divide by three" · primes-2: "seventy is ten times seven and seven times three is twenty-one, so seventy plus twenty-one … ninety-one is thirteen times seven" |
| **Meaning in plain words** ("What does that mean? It means…") | 17 | a given in symbols | q-468: "a plus d is not zero. What does that mean? It means they're not opposite numbers" · r26-t18-facts: "What does that mean? It means it's divisible by eleven, right?" |
| A **general rule after the answer** | ≈10 (long ones) | a question that hides a reusable fact | q-402: "any prime number, I square it … it has three divisors always … two to the power of three … one, two, four and eight" · q-514: "when we subtract AB with BA we'll get a multiple of nine, and when we add AB to BA we'll get a multiple of eleven" · consecutive-sums: "seventeen squared minus sixteen squared, that's just seventeen plus sixteen, which is thirty-three" |
| A **warning** at the step | 10 | a result that is not yet the answer; a look-alike rule | q-r26-t16-02: "we got to thirteen but thirteen isn't our final answer" · r26-t16-03: "let's not confuse this with multiplication" |
| **Study / exam advice** | 10 | lesson ends; a rule list; a "funny operation" question | primes: "take the time memorizing this" · q-541: "what I highly recommend in these questions is to always say out loud what's happening here" |
| **The question type, said again at the check** | 8 | an elimination in an "always / could be / necessarily" question | q-358: "a necessarily true type of question has to work for every pair that fits the givens" |
| **An easier warm-up example** before the real one | several | a picture or method used on the real numbers straight away | q-359: "Let's start with an easier example. The absolute value of x minus five is seven … five plus seven is twelve … five minus seven is negative two" |
| **"Two / three different ways"** | 51 (0 in the scripts) | the roadmap line | She says it at the start of the first method: "We'll solve it in three different ways. Our first method, the algebra." |

**The pattern: she elaborates exactly where a line is a *claim without numbers* or a *result without its step*.** Lines that already give the numbers and the step ("Five squared is twenty-five, and four squared is sixteen. Twenty-five minus sixteen is nine.") she reads almost word for word.

### 2. Simplifications: what she shortens or skips
| Kind of sentence | What she does | Count / example |
|---|---|---|
| **Inequality chains in the given** ("one is smaller than p, which is smaller than q, which is smaller than r…") | She reads them from the big end with "bigger than", or squeezes them into "this chain of ranges" | 8 stems, plus 14 "smaller → bigger" swaps. q-493: "Given s is bigger than r, bigger than q, bigger than p, and bigger than one" · q-496: "So we have this given of ranges, and then we're asked…" (also q-497, q-501, r26-t17-04) |
| **Roadmap at the end of the reasoning paragraph** ("We'll solve it three ways.") | She moves it to the start of the method paragraph | q-360, q-361, q-369, q-457 |
| **Bare "Our first method."** | She drops it or merges it ("Our first method is breaking up into primes") | 5 |
| **Verdicts and forced morals** ("Which way is better?", "Pick what feels comfortable for you", "But know the two bands too…") | She drops them or says them half-heartedly | q-358, q-362, q-367, q-368, q-369, q-r26-t13-01: 6 of 6 |
| **Rule lists and checklists in summaries** (5 rules, or 4 questions in a row) | She replaces them with "take another look at the rules. Take a moment to memorize this" | r26-t15-summary p11-12: 9 sentences |
| **An example packed into the opening / roadmap paragraph** | She skips it | q-457 p1: all four "negative two cubed, times four, over two" sentences |
| **Teasers and tiny confirmations** ("It's the tool of the next question.", "That's our hint.", "It works.", "That choice is out.") | She drops them | about 10 |
| **"Okay." before the goodbye** | She joins it to the answer instead: "…choice number two is our answer, and I'll see you in the next question" | "Okay. I'll see you" 89 → 6; "and I'll see you" 1 → 40 |
| **Spoken bracket cues** ("times the whole bracket, n plus one", "in brackets") | She reads the math and leaves the cue out | "the whole bracket" 14 → 0; "in brackets" 7 → 3 |
| **Long trailing clauses** | She stops at the main clause | q-r26-t17-03: "Now calculate with the two ends." (of "…of the range to find the new ends") · q-520: dropped "so no digit works, and choice numbers two and four are out" |

### 3. Rewordings: our phrase → her phrase (counts are script total → her total in the same paragraphs)
| We write | She says | Count |
|---|---|---|
| "negative three" (a number in a calculation) | **"minus three"** | 83 direct swaps; "negative" 574 → 427, "minus" 358 → 543. She keeps "negative" for the sign idea ("x is negative") |
| "x is two" / "equals" (in a calculation or given) | **"is equal to"** | "equal to" 67 → 386 (213 insertions) |
| "cubed" | **"to the power of three"** | 47 → 3, and "power of three" 3 → 52. ("squared" is kept: 212 → 211, plus 34 "to the power of two") |
| "three fifths", "one twenty-seventh" | "three over five" | 6 swaps (the prompter shows 3/5) |
| "over" (as an operation) | "divided by" | 18 swaps; 25 → 57 |
| "larger" | "bigger" | 12 swaps; "bigger" 68 → 118 |
| "smaller than" chains | "bigger than", read backwards | 14 |
| "cannot", "it is", "do not" | "can't", "it's", "don't" | 17 / 17 / 5 |
| "GCD" | "greatest common divisor" | 7 → 0 |
| "divides by" | also "is divisible by" | "divisible" 31 → 80 |
| "is" (as a step) | "and therefore … is", "has to be", "must be" | 11 |
| "Choice number three." (as the last line) | "Choice number three is our answer." | almost always |
| "We'll solve it two ways" | "two different ways" | 0 → 51 |
| "Given: …" (in the middle of a stem) | "and it's given that…" | 1 → 7 |
| "This is…" (pointing at the board) | "So we have here…", "over here" | "we have" 16 → 155, "over here" 0 → 13 |

### 4. Stumbles: where the M marks fall
Marks per sentence, located from the point where the failed attempt broke off (99 videos):

| Sentence | Marks per sentence |
|---|---|
| 1-6 words | 0.09 |
| 6-10 words | 0.21 |
| 10-14 words | 0.31 |
| **14-18 words** | **0.45** |
| **18-22 words** | **0.51** |
| **Method announcement / abstract procedure** ("Third, find the number's range, draw its arrow, and compare the powers.") | **0.51** (7.5 per 100 words, 2.7× the average) |
| Contains "multiple(s)" | 0.70 |
| Contains "bracket" / "root" / "divisible-divisor" | 0.43 / 0.42 / 0.39 |
| No number words at all | 3.6 per 100 words |
| 4 or more number words | 0.85 per 100 words (concrete calculations flow) |
| Contains "absolute value" (a familiar topic) | 0.16 (lowest) |

- **Paragraph types.** Paragraphs that write remainders as tags (seven k plus two, seven m plus five) average **3.0 marks** each. Paragraphs with a "Why?" self-question average 2.3, and the overall average is 1.4.
- **Most-marked videos** (marks per 100 words): q-427 8.4, q-r26-t15-01 7.9, q-430 7.5, q-426 6.5, powers-on-number-line 6.5, q-470 6.4, r26-t15-summary 6.4. These are all abstract remainder or divisibility procedure, or "range, arrow, power" method talk.
- **Typical stumble spots:**
  - a name before a colon: q-430 "Yoav claims:" came out as "You have have have have claims"
  - a look-alike word: q-365 "sign of x" read as "sine of x"
  - an abbreviation with its long name: q-390 "the LCM, the least common multiple, the…"
  - an abstract rule with no number: powers-on-number-line "Keep negative powers as they are when using this method"
  - a choice number she said ahead of the script: q-364 "circle number three" where the script said two

### 5. Order and method changes
- **q-r26-t18-02.** She replaced "three-digit multiples of 99 have 9 in the middle and the outer digits add to 9" with **counting up by 99**: "it's like doing plus a hundred minus one … 198, 297, 396 … 495". She did not do the scripted second method (plugging in reversed numbers).
- **q-436.** She added a no-numbers version: "when one number divides by six, the other two have to add up to divide by six … with a bit less calculations".
- **q-r26-t14-01.** She gives two ways to test 3: "ninety is divisible by three, so ninety-one can't be", then the digit sum.
- **q-359.** She puts an easier example, |x − 5| = 7, before the scripted |x + 7| = 9 on the number line.
- **q-458.** She turns the trap into "that's what you would get if you would use q plus one and q minus one instead". The scripted "each gap is two" lines are gone.
- **q-472, q-388, q-471.** She says "we can circle it and move on, but let's prove it anyway" before the remaining choices. She places the exam/lesson switch (R24) herself.
- **Roadmaps** move from the end of the reasoning paragraph to the start of the first method (q-360, q-361, q-369).

### 6. Her speaking style while reading
- **Openers.**
  - Lessons start with "Welcome back" (9 in the scripts → 13 from her; she adds it where the script opens "Prime numbers. This topic…") and "today we're going to be learning about…".
  - Stems are read flat: "Given, x plus seven in absolute value is equal to nine."
- **Joints.** "So" starts most sentences (4 a minute). "Now" starts a new step. "right?" comes after a fact (0.65 a minute). "and therefore" comes before a conclusion. She narrates the board with "so we have here…".
- **Numbers.**
  - She says "minus 7", "x to the power of 3", "3 over 5", "a half", "a quarter".
  - "AB" is said as one word-pair.
  - "a hundred" vs "one hundred" is not measurable here (whisper writes 100).
- **Closings.**
  - Questions: "Choice number N is our answer, and I'll see you in the next question." She said "next lesson" by mistake 5 times.
  - Lessons: "Take a moment to memorize this … and I'll see you in the next video."

### WRITING RULES for scripts she will read (topic 21 onward): W1-W25
These add to R1-R37 and the Codex review standard. Where they differ from the AI-voice rules, these apply to **teacher-read** scripts.

1. **W1. Keep sentences short.** Aim for 6-12 words and split anything over 14. Her M rate doubles from 0.21 per sentence (6-10 words) to 0.45-0.51 (14-22 words). Put a trailing clause in its own sentence ("Now calculate with the two ends. That gives the new range.").
2. **W2. No abstract method announcements.** Don't write "Third, find the range, draw its arrow, and compare the powers." Start the method with its first concrete action: "Let's start with the place values. ABC is a hundred A, plus ten B, plus C." One short roadmap line goes at the start of the first method paragraph: "We'll solve it in two different ways." Never put it at the end of the paragraph before.
3. **W3. Givens with inequality chains.** Never spell out a chain of three or more "which is smaller than" in words.
   - Write "Given this chain, from smallest to biggest: one, p, q, r, s." and let the board show 1 < p < q < r < s.
   - Or write it the way she reads it: "s is bigger than r, which is bigger than q…".
   - Then add the meaning: "So all four letters are bigger than one."
4. **W4. Write her words.**
   - Use **"minus three"** for a number in a calculation. Keep **"negative"** for the sign ("x is negative").
   - Use **"is equal to"** in givens and calculation lines.
   - Write **"to the power of three"**, never "cubed". "Squared" is fine.
   - Use **"bigger"**, not "larger".
   - Use **"divided by"** for the operation. Use "three over five" for a fraction you calculate with.
   - Use contractions (can't, it's, don't).
   - Write **"greatest common divisor"** (never GCD) and "least common multiple" (spell it out). Say "two **different** ways".
5. **W5. No spoken bracket cues.** Drop "the whole bracket" and "in brackets"; she drops them every time (14 of 14). Put the grouping on the board and in the prompter display (`scope_replacements`), and write the expression plainly ("m squared times n plus one, all divided by eight").
6. **W6. Every rule or claim line gets a number example right after it, and a second run for "every / always" rules.** She adds about 32 own examples and about 78 reasons. Examples:
   - "Every third integer divides by three. Five, six, seven: six. Seven, eight, nine: nine."
   - "Two even numbers in a row: two times four is eight."
7. **W7. Give the step, not just the result.**
   - **Factor trees:** each break in its own clause ("ninety is nine times ten. Nine is three times three, and ten is two times five").
   - **Divisibility tests:** say the test with the numbers ("five plus one is six, and six divides by three, so fifty-one divides by three").
   - **Primality:** first the root bound ("ten squared is a hundred, so we only check two, three, five and seven").
8. **W8. Translate each given in symbols with "What does that mean? It means…".** For example: "a plus d is not zero. What does that mean? It means they're not opposites."
9. **W9. At each elimination, restate the question type in plain words.** For example: "We need something that is sometimes true and sometimes not. This one is always true, so it's out."
10. **W10. Teach by an easier example first** whenever a picture or method appears for the first time in a question. For example: "|x − 5| = 7 means seven steps from five: twelve or minus two." Then do the real numbers.
11. **W11. One reusable fact after the answer, when the question hides one.** This is in line with R16. Examples: "A prime squared always has exactly three divisors." "AB plus BA is always a multiple of eleven." "Seventeen squared minus sixteen squared is seventeen plus sixteen." **Never** "Which way is better?" or "Pick what feels comfortable": she dropped 6 of 6.
12. **W12. Closings.**
    - Questions end with "Choice number N is our answer, and I'll see you in the next question." This replaces "Choice number N. Okay. I'll see you…".
    - Lessons end with one nudge ("Take a moment to memorize this.") plus "I'll see you in the next video".
    - No checklist of four questions or five rules read aloud. Put such lists on the board and say one line about them.
13. **W13. Keep the opening paragraph clean.** The "what they ask + roadmap" paragraph holds no worked example (q-457 lost four sentences). Put the example in the method paragraph.
14. **W14. Avoid these, because she stumbles on them:**
    - "multiple(s)" in a long sentence (0.70 marks per sentence). Say "divides by".
    - Tag algebra without a number first. Write "Nine leaves two, because nine is seven plus two. So a is seven k plus two." Not "a is seven k plus two, full sevens plus two."
    - Names right before a colon ("Yoav claims:"). Use an easy name and "says that".
    - "sign" next to math words (read as "sine"): write "positive or negative".
    - Abbreviation + long name pairs.
    - "respectively" and "multipliers", and formal terms in general (0.57 marks per sentence).
15. **W15. Keep "Why?" with its answer in the same line.** For example: "Why m and not k? Because a and b are different numbers." A lone "Why?" line gets 2.3 marks per paragraph.
16. **W16. Don't script her fillers.** She adds "so", "right?", "now", "just" and "also" by herself (270 "right?" with 3 in the scripts). Write at most one "right?" per paragraph, and no "Okay." before the goodbye.
17. **W17. Before working on a choice, read the whole choice aloud as written (operations/symbols included), then translate.** (Teacher, 2026-10-15, re-recording q-555: "you don't read out the whole choice, so it's confusing reading off the screen without knowing what you are talking about.")
    - First the full choice: "Choice number three says: diamond of a, divided by diamond of b, is equal to a over b."
    - Then the translation of each symbol: "Diamond of a is three over a, and diamond of b is three over b."
    - Only then the work. Never jump straight to "three over a…" or to a test value.
    - On the board: the choice is highlighted at "Choice number N says", then the translation is written, then the steps.
    - In a second method, read the choice again briefly ("Choice number one says: diamond of a is smaller than three."); in a plug-in method, read it first and then say it with the test value ("Choice number two says x minus sixty. One hundred ten minus sixty is fifty.").
    - Exception: a choice that is only a number or a single short expression ("Choice number two, twelve") is already read in full.
18. **W18. Never use the article "a/an" near the variable a; avoid ambiguous letter-words.** "a fraction" → "any fraction" / "one fraction"; "a number" → "any number"; "a bigger denominator makes a smaller fraction" → "the bigger the denominator, the smaller the fraction". Where useful, say "the letter a" or "the number a" the first time. The same goes for other letter-words next to a variable of that name (e.g. "I" when there is a variable I). The prompter shows math variables in italic serif with their own colour (`math_patches/_math_vars_display.py`), but the spoken sentence must be clear without it.
19. **W19. Pace + explain, no headlines.** (Teacher, 2026-10-15: scripts must be understandable at a pace students can follow, and explain rather than "speak headlines".)
    - **Pace:** one new idea per sentence. After a key idea comes a beat: a short pause, a check sentence, or an example. Never two new steps in one breath ("Seventy plus fifty is a hundred twenty. Then the ones: seven plus six is thirteen.", not both in one clause chain). The board writing keeps up with the speech: each step is written at its own clause.
    - **No headline speech:** no telegraphic fragments ("Two cases.", "Step one: the signs.", "Same idea.", "Side eight.") and no bare results. Every step says what we do, why, and what it gives ("Let's try it with a side of eight. Eight squared is sixty-four, ...").
    - Short spoken transitions that lead into a full sentence are fine ("Now the area.", "Why? Because ..."), and so is "Out." right after the calculation that rules a choice out.
    - **Aid:** `python3 studio-build/w19_check.py <video ids>` (2026-10-15) flags: sentences under about 5 words with no verb, label-style openers (word + colon), and sentences with more than 2 numbers and 2 operations. The flags only find spots; judge and fix each one by hand.

20. **W20. Teaching check (TC): teach the reusable idea, not only this answer.** (Teacher, 2026-10-16: "make sure I am actually teaching something when we get to some important concept, and not just answering the question. But only when it really adds.")
    - **Find the moments** where a script uses an IMPORTANT, REUSABLE concept: a rule, pattern, shortcut or principle that comes back across the topic or on the real exam (e.g. the 30-30-120 triangle as two 30-60-90 halves; "same remainder → take it away"; equal angles in an isosceles triangle; "multiplying by a negative flips the inequality"; the overlap rule; lengths × k → area × k²).
    - **At each one, check that the script TEACHES it:** (1) the idea stated generally, in one plain sentence; (2) WHY it's true, briefly; (3) how to recognise it next time ("when you see …, think …"); (4) one quick extra case if the concept is new here (R4/R5).
    - **Only when it really adds.** Skip trivial facts and anything fully taught earlier (a short reminder is enough, R29) or already taught well in this video or the camera lesson. Aim for a few strong additions per topic, not a sweep. Use real-exam frequency (`quant_real.md`) when in doubt.
    - **Form:** about 2-5 short sentences in her voice (W1-W19), never one line. Usually right after the answer, before the goodbye, or as the "Why?" right after the rule. If the board is full, give it its own short slide (a clean generic picture, V3).
    - **Board (V3/V4):** the general statement as a short key line at its clause, and a picture when it helps (the second, generic case). Keep cue anchors valid and the method vocabulary.
    - **Workflow:** Claude runs TC on each batch after fixing Codex's review of it; results per video in `reviews/teaching-check-<batch>.md` (concept → added / already taught / not needed).

21. **W21. Say WHY before each step (the given behind it).** (Teacher, 2026-10-18, on solve-geo31-g040's check "And three times nine is twenty-seven": "you should have explained that you are multiplying by three because the given says it needs to be 3 times bigger; just doing the math won't be clear enough for the student. Especially in the second method, but you do it pretty often.")
    - Before (or in the same sentence as) every operation, say the reason: which given, rule or goal makes us do it. "The given says the bold line is three times the small perimeter, so we multiply the perimeter by three: three times nine is twenty-seven. That's exactly the bold line." Not a bare "And three times nine is twenty-seven."
    - **Checks in plugging in the answers / numbers:** name the condition being tested before the calculation ("Now the given: … has to be …"), then compare the two sides out loud ("…, and the bold line is twenty-seven, so it works").
    - **Picked numbers:** say why these numbers ("three tenths, so let's take a three and b ten"; "it has to be even, so let's take four").
    - **Any non-obvious move** (divide both sides by…, add a to both sides, square both sides, compare with…): one short "because / so that" clause with the goal ("…so that only a over b is left").
    - Second methods need it most: never assume the student remembers the given from the first method; restate it.

22. **W22. The student always knows what we're finding, what each thing is, and why this step** (teacher, 2026-10-21: "review the teaching style and clarity — not just whether the content is present").
    - At every step the student can answer: What are we trying to find? What does this number / expression stand for? Why this step? How does it help answer the question? Don't just announce a rule or a calculation.
    - Name the quantity first, then show the calculation, then say what the result tells us ("Tom's age is x. Maya is twice as old, so Maya's age is two times x.").
    - Translate relationships fully, never as a slogan. Not "multiply the smaller one", but: "Maya is twice Tom's age. Their ages aren't equal, but twice Tom's age equals Maya's age. So we multiply Tom's age by two and set that equal to Maya's."
    - Banned vague phrases unless explained right there: "it comes out", "use the trick", "make them equal", "plug it in" (say WHAT goes WHERE), "it works" (say what matched what).
    - Exam terminology stays (choice, given, integer, inscribed …); an unfamiliar term is explained in plain words the first time.
    - A new idea is never squeezed into a slogan or half a sentence: give it its sentences, a worked example, and the board picture needed to follow it.
    - Don't make scripts longer for its own sake: cut repetition, remind briefly of what was learned, spend the words on the NEW reasoning. One efficient method shown clearly; another method only when it adds something.
    - **Read-aloud check before "ready":** read every changed paragraph aloud while following the planned screen. If a student would have to guess what "this", "that" or "it" refers to, name it.
    - **Shortcuts:** state the conditions every time a shortcut is taught (e.g. "only in a regular polygon", "only when both amounts are multiplied by the same number"), and place it after its prerequisites.

23. **W23. Hebrew preservation check — required before every Codex review** (teacher, 2026-10-22: "how can I trust you and know that maybe other important content was dropped?"). Two of her shortcuts in topic 23 had been lost in the September translation: one condensed away, and one broken when the numbers were changed.
    - For every topic: split her Hebrew section into her actual videos and compare METHOD BY METHOD with the English (SAME / CHANGED / PARTIAL / MISSING), then the reverse (what English added). Model: `reviews/hebrew-vs-english-t23.md`.
    - **When numbers are changed** (English questions must differ from hers), re-check that EVERY one of her methods and named shortcuts still works with the new numbers. If one stops working, choose other new numbers; never drop the method.
    - Missing items in unrecorded videos are restored before she records; items in recorded videos go on a list for her decision.

24. **W24. Lessons from Codex's reviews — write these from the start** (Nitzan, 22 Oct: "Codex's review findings should become guidance for your future writing, so the same problems don't keep recurring"). Collected from Codex's batch reviews A–L, P, Q and its external-course reports:
    - **Start each question explicitly:** "Now a new question. We are given … We need …".
    - **Name what each number measures** before calculating, and keep units / total / each / remaining / per-hour attached to the numbers on the board.
    - **Definitions describe the value, not a way of writing it** ("a fraction writes a division; it can equal a whole number").
    - **State what is held equal** before a comparison ("for the same perimeter …") and the conditions of every shortcut (regular polygon, same multiplier, nonzero, inscribed vertex …). Never "always" when a special case breaks it.
    - **Geometry:** name a helper line and its purpose before drawing it; match similar triangles by angles, not by how they look.
    - **Full method first; an exam shortcut afterwards only when it saves work, and say why stopping early is enough.**
    - **Plugging in:** easy allowed numbers (0 and 1 are fine unless ruled out; letters may share a value); check the choices at once; change a feature only for the survivors. A few agreeing trials never prove "always".
    - **Prompter maths must group correctly:** whole fractions, brackets, percent signs outside a whole fraction; no bare "over"/"times" between numbers.
    - **A result is written when it is said**, never before; split bundled rows; keep needed results in a "So far" box when a slide clears.
    - **Don't promise "we'll learn it later"** for something already taught — give a one-line reminder instead.
    - **(Codex, topic 35 review, 23 Oct)** State a formula's conditions when it is first used (right prism, two equal bases, nothing spills); say WHY a midpoint or a cancellation follows, not only that it does; introduce letters (a, b, c) in words before they appear on the board; say "the square root of the SUM of the squares", never the ambiguous "edges squared".

25. **W25. Acceptance standard — clarity and read-aloud usability are REQUIRED** (Nitzan, 22 Oct): a script is not ready because its maths and automated checks pass. Every sentence is checked against its board: new questions / examples / methods introduced explicitly ("Now a new question. We are given … We need …"); each step = what we're finding + what the quantities mean + why + what it tells us; natural simple spoken English with clear pauses; readable maths on the prompter; no ambiguous references or unexplained jumps; her methods and exam terms kept. Writers self-check this before handing off; Codex independently reviews it before marking Ready.

26. **W26. Plugging in the answers is not always right on the first try** (Nitzan, 25 Oct: "when you plug in the answers you always get it in the first plug in, and that's not the case in reality — stop doing that"). Across a topic, many plugging-in-the-answers solutions must try a choice that FAILS first, the way it happens on the exam. Choose the first choice by a real, stated reason (the most convenient / round one, or the middle one when the choices are ordered) — never pick it because it is the answer. When it fails, say what it shows ("too big, so the answer is smaller") and use that to rule out more choices before the next try. Some solutions may still hit on the first try when the reason picks it — but not most of them. Never change a question's correct answer or choices only to stage a failure; change the starting reason or the order of tries instead.

**Put her most frequent elaborations in the script from the start:**
1. the reason after each claim;
2. a second and third run of number examples for "every / always" rules;
3. the plain meaning of each given;
4. the factor or divisibility step said with its numbers;
5. "remember, we said…" before a tool from the lesson;
6. the question type at each elimination;
7. an easier warm-up example before a first-time picture;
8. the warning "this isn't our final answer yet" when an intermediate value appears in the choices;
9. one reusable fact after the answer;
10. "We'll solve it in two different ways." at the start of the first method.
