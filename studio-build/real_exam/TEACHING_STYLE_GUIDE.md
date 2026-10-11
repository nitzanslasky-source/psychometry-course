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
- R15 is approved.
- Topic 51 is recorded by her.

## SCRIPT-WRITING CHECKLIST (R1-R34)

Check every AI script line by line. The numbers in brackets are evidence from §1-9.

**Every rule or idea**
- **R1. Full spoken sentences.** 6-14 words (her median is 9), joined with so / because / and. No colons, em-dashes, "..." or "X? Y." fragments. A self-question and its answer stay on one line ("How do I get rid of the root? I multiply by root 2."). Pauses follow `NITZAN_RHYTHM_DELIVERY.md` P1-P13.
- **R2. Define a new term with instances.** "Numbers in a row, like 7 and 8." Plain word first, the official term second.
- **R3. State each rule in one exact plain sentence.** Never vague: she simplifies the path, not the rule.
- **R4. Every rule gets a simple-number example right after it** ("Let's see it in numbers."). Letters → numbers. No rule line without numbers (HE ≈87% of rules; EN 46 improvised additions).
- **R5. Two examples is the norm.** The second changes exactly one thing: a negative, zero, a fraction, another position, or a **non-example** ("but 2 times 4 is 8, no 3 there"). Give 3 or more, plus an everyday story, only for counter-intuitive rules ("sounds strange, but…").
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
- **R14. The answer line is the value plus the number, said calmly:** "So x is 6, choice number two is our answer." (R34: always "choice number N".) Never "choice two", and never a build-up pause before it. (She dropped the number in 85 of 154 takes. The AI must not.) Checks go **inside** the step ("let's check with a = 3"), not in a list after the answer.
- **R15. Plugging in, every time:**
  1. Say which number, where it goes (the whole, the start), and **why**, before using it. Use 100 for percents.
  2. Check that the choices come out different. Avoid 0 and 1 when they make choices tie; 3 is a good default when 1 or 2 leaves ties.
  3. Give different letters different numbers.
  4. Rule out 3 choices; don't stop at the first match. If two survive, use a tie-breaker number.
  5. Call it "a safety net".
- **R16. No "which way is better" paragraph.** End after the answer, with a takeaway only if it teaches something new (a sentence that works on the next question, e.g. "whenever you see a percent of a percent, ask: of what?"), not a recap of what was just shown. Then "[pause] Okay. I'll see you in the next question."
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
- **Recorded readings** (teacher, 2026-10-11): once she has read a script in the Reading Studio, change its paragraphs only where it matters for learning (a first-time idea not explained, a wrong or missing reason). Small wording rules (R33, R34) are not worth a re-read. Every changed paragraph is flagged "needs re-read" in the Reading Studio.

### Topic 13: where each idea is first taught (R29 / R32)

Study-plan order before topic 13: 1, 30, 2, 4, 31, 6, 8, 32, 9, 10, 33, 51, 39, 42, 21, 3, 43, 22, 41, 5, 7, 44, 23, 11, 24, 49, 12, 45, 25, 40, 34. Topic-13 order: the camera lesson `absolute-value`, then q-358, q-359, q-360, q-361, q-362, q-r26-t13-01, q-r26-t13-02, r26-t13-tools, q-363, q-364, q-365, q-366, q-r26-t13-13, q-r26-t13-03, q-367, q-368, q-369, q-370, summary.

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
| \|x\| = distance from zero, never negative; \|0\| = 0; letters hide their sign (\|x\| = −x for a negative x) | camera lesson, slides 1-2 | q-362, q-r26-t13-02, summary |
| Inside first, then the bars | camera lesson, slide 3 | summary |
| \|ab\| = \|a\|\|b\|, \|a/b\| = \|a\|/\|b\|; \|a + b\| ≤ \|a\| + \|b\| (equal with the same signs) | camera lesson, slides 4-5 | q-366, q-r26-t13-13 |
| Sign clues: \|x\| > x negative, \|x\| = x zero or positive, \|x\| = −x zero or negative | camera lesson, slide 6 | q-358, q-365 |
| Bars = a number: two cases | camera lesson, slides 7-8 | q-359, q-r26-t13-01, q-r26-t13-03, q-367, q-368 |
| Bars on the big side: open range (two rays); small side: closed range (one band) | camera lesson, slides 9-10 | q-360, q-361, q-369, summary |
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
