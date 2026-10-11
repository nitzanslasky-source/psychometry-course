# Nitzan's Phrase Bank: how she actually talks in English

**Source.** Every one of her 189 English takes was read in full: 34 lessons, 154 solutions and 1 lesson that is no longer in the studio. That is about 803 minutes and 133,700 spoken words, in about 10,800 sentences, from `transcripts/*.json` (whisper small.en). Each take was also lined up with the script she was reading.

**How to read the counts.** "n / v" means n times, in v of 189 takes. A quote is given as `video [second]`.

**Purpose.** These are the words for the AI narration (her cloned voice). Use them so the AI sounds like her. Section 18 lists what not to copy.

Companion files:
- `NITZAN_RHYTHM_DELIVERY.md`: pace, pauses, pitch, and punctuation rules.
- `NITZAN_TAKES_LESSONS.md`: where she struggled, and what flowed best.
- `scratchpad/tstyle/added_by_nitzan.json`: what she added in each video.

**Transcription note.** Whisper writes her "I have here" as "I have your" (78 / 47). Whisper also drops "um" and "uh" entirely (0 found). Fillers were therefore measured from the audio instead: see section 17 and the rhythm file.

---

## 0. The ten markers of her voice, by frequency

| Marker | Count | Per minute | Use in AI scripts |
|---|---|---|---|
| Sentence starts with **"So"** | 2,462 / 182 | 3.1 | Yes. This is her default joint; about 1 sentence in 4 starts with it |
| **"right?"** as a tag | 1,349 / 176 | 1.7 | Yes, about once per 3-4 sentences, after a fact |
| Real question, answered in the next sentence | 1,128 | 1.4 | Yes. This is the backbone of her explanations |
| Sentence starts with **"Now"** | 812 / 157 | 1.0 | Yes, to start a new step |
| **"because"** | 594 / 164 | 0.7 | Yes |
| **"I have here" / "we have here"** | 584 / 134 | 0.7 | Yes, about once per beat (she narrates the board) |
| **"is equal to"** | 627 / 131 | 0.8 | Yes. Prefer it to "equals" |
| **"to the power of"** | 674 / 47 | (in power videos, every power) | Yes. Never "to the fifth" |
| **"over here"** | 342 / 112 | 0.4 | Yes, but only when a [draw] cue points at something |
| **"and therefore"** | 218 / 108 | 0.3 | Yes, before a conclusion |

29% of her sentences end in a question mark. 12% are "right?". The other 17% are real questions, and she answers almost all of them herself.

---

## 1. Openers

### 1a. Lesson openers

| Phrase | n / v | Quotes |
|---|---|---|
| **"Welcome back, and (this time / now) X."** | 13 / 13 | `exponents [0]` "Welcome back, and this time, exponents." · `r26-t12-signs [0]` "Welcome back, and here's one rule before the advanced questions." · `inequalities [0]` "Welcome back, and now inequalities." |
| "Welcome to X." | 4 / 4 | `advanced-powers [0]` "Welcome to Advanced Exponents and Roots. Most rules here you already know…" · `linear-equations [0]` "Welcome to equations, one of the most basic techniques in all algebra." |
| Why it matters on the exam, in the first 20 seconds | 25 / 35 lessons | `numbers [3]` "So algebra is about a quarter of the quantitative section… but honestly, it's way bigger than that" · `decimals [0]` "Honestly, pure decimal fraction questions are rare on the exam, but…" · `inequalities [3]` "one of the topics that people really don't like in the psychometry, but honestly, for no good reason." |
| "Now we're taking this level up / Now things get properly psychometric." | 4 / 4 | `expression-strategy [0]` "Welcome back to Expressions. And now we're taking this level up to the exam style." |

### 1b. Question openers

There are three shapes. Use one per video.

| Shape | n / v | Quotes |
|---|---|---|
| **Read the stem**: "Given … And we're asked …" / "It's given that …" | given 21, it's given 10, we're asked 33 / 30. She reads or paraphrases the stem first in at least 101 of 154 solutions | `solve-q-184 [0]` "given 33 minus 2 thirds of x equals a quarter x. And we're asked, what is x?" · `solve-q-r26-t04-01 [0]` "So it's given that x plus y equals 6 and x times y equals 5. We're asked for the value of…" |
| **"Here's a / Here we have a + label"** | here's 48 / 42; here we have 42 / 39 | `solve-q-294 [0]` "Here's a scary one." · `solve-q-096 [0]` "Here's a genuinely hard one. Although it looks easy, it really isn't." · `solve-q-128 [1]` "We have here this beautiful expression" |
| **Difficulty and place in the section** | about 8 | `solve-q-093 [0]` "Here's a relatively easy question… it would be somewhere in the beginning of the section." · `solve-q-094 [0]` "This one is a medium plus question. It would be somewhere in the middle of the section." · `solve-q-189 [0]` "Here's a nice question. It would be one of the last questions in the section" |

Her adjectives: beautiful (9 / 8), scary (9 / 8), hard / tough (8 / 7), classic (7 / 6), tricky (3), nice (2), "pretty ugly" (`solve-q-134 [1]`), "a headache" (`solve-q-188 [20]`).

**Rule.** Open with the stem, or with "Here's a [one adjective] one." followed by the stem. Never use a meta line such as "In this video we will…".

---

## 2. Reading the question

- She says the givens in plain spoken maths, then restates the target as a question: "What are they asking me?" (4), "So what are we looking for?".
  - `solve-q-190 [~60]` "Okay, now that we have that settled. What are they asking me? They're asking me for what a plus 2B is"
  - `solve-q-366 [8]` "And look at the wording. Okay, what are they asking? Let's read it carefully. They're asking possible but not necessarily…"
- She comments on a given right after reading it: "X and Y are integers that are not prime. Okay, they're both not prime." (`solve-q-386 [0]`) · "given the x is between 0 and 1. What does that mean? It means it's a positive fraction." (`solve-q-r26-t08-02 [0]`)
- She points out a hint in the givens: "Because I was told that x is not equal to 0 and this was a big hint that I'm gonna be dividing by some x" (`solve-q-185 [50]`) · "letters also in the question and also in the answers… they're hinting to us that you can plug in numbers" (`solve-q-r26-t05-04 [0]`).

**Rule.** Stem, then "So what are they asking?", then one line on what a given really means ("What does that mean? It means…").

---

## 3. First reaction (before any method)

| Phrase | n / v | Quotes |
|---|---|---|
| "So at a first glance…" / "Kinda scary at first, but let's see." | 7 / 6 | `solve-q-191 [8]` "Okay, so at a first glance, it looks pretty simple, right?" · `expression-strategy [430]` "Kinda scary at first, but let's see." |
| "What needs to jump into mind / What does this remind me of?" | 9 / 8 | `solve-q-180 [6]` "What needs to jump into mind when I see…?" · `solve-q-r26-t09-06 [10]` "What does this remind me of? This kind of reminds me of the formula, right?" |
| "Let's look at the answers" (choices as a hint) | 14 / 12 | `multiply-divide` "Well, let's look at the answers. 382 does not end with a 6, and I could already cross it out" · `solve-q-r26-t10-01 [4]` "a root is never negative and therefore without even calculating anything I know that x can't be negative… I can cancel out option 1 and option 4" |
| "The hard part here is…" | about 5 | `solve-q-187 [10]` "Well, the hard part in this question is just the words. If we turn them into algebra, it'll be much easier." · `solve-q-181 [0]` "Here's a tough one and the trick is to look at what they're actually asking, right?" |
| Big picture before diving in | 6 / 5 | `solve-q-137 [8]` "take a step back and look at it from the outside" · `solve-q-091 [60]` "if I would take a moment before to look at the larger picture I could have cancelled things out earlier" |

---

## 4. Announcing a method

| Phrase | n / v | Quotes |
|---|---|---|
| **"We're going to solve this in two / three different methods (ways)."** | 28 / 25 | `solve-q-367 [5]` "We're going to try to solve this with three different methods, starting with algebra." · `solve-q-293 [0]` "Two ways: the math route, then plugging in numbers" |
| **"Let's start off with…"** | 49 / 45 | `solve-q-096 [3]` "So let's start off with plugging in numbers." · `solve-q-130 [3]` "So let's start off with the simple one, just opening up the brackets" |
| **"So what I could do is…" / "One thing I could do is…"** | 37 / 28; 7 / 7 | `solve-q-127 [8]` "So one thing I can do is really just open up each one of the answers" · `fraction-multiply` "So what I could do is I multiply the top by the top and the bottom by the bottom." |
| **Method labels**: "our first / second / third method (way)" | 36 / 28 | `solve-q-296` "Our third method would be to multiply the denominators. What does that mean?" · `solve-q-179` "Our third way may be a bit more hidden. Okay, but let's see." |
| "the psychometry way / the math route" | 21 / 14 | `solve-q-293` "Now the psychometry way, and it's an equation, so plug in a number into one letter" |
| Plugging in (any form) | 216 / 69 | `solve-q-r26-t09-04 [0]` "Let's choose an easy number. Let's choose 1 quarter… Why did I choose 1 quarter? Because I know that its root is 1 half." |

**Rule.** Start with "We'll solve this two ways." Before each method, use "Our first method…" or "Now our second method:". Before a plug-in, give the reason: "Why did I choose…? Because…".

---

## 5. Transitions between steps

| Phrase | n / v | Note |
|---|---|---|
| **"Now let's look at…"** / "Let's look at…" | 115 / 71; 163 / 79 | Her main step-turner |
| "Now what about…?" | 17 / 13 | Moves to the next case: `exponents` "Now what about a base of negative 1?" |
| "Let's move on to (number) N" | 40 / 25; "move on to" 51 / 31 | Moves through the choices: `solve-q-096` "Let's move on to number four." |
| "And then…" | 295 / 98 | Joins steps inside a calculation |
| "So now…" / "Okay, so…" | 92 / 67; 128 / 78 | Restarts after a result |
| "Now that I know that, …" | about 10 | `solve-q-292` "Now that I know that, I know that x plus y is equal to 4." |
| "Perfect. Now…" | 53 / 39 ("Perfect") | Closes a step and opens the next: `solve-q-331` "Okay, perfect. Now let's move on." |

---

## 6. Thinking aloud

| Phrase | n / v | Quotes |
|---|---|---|
| **"Let's see…"** | 170 / 97 | `order-of-operations` "because let's see, what is 12 over two?" |
| **"Let's say…"** (before almost every example) | 180 / 77 | `decimals` "If I let's say have 47 divided by 1,000…" |
| "I want to… / I need to… / I have to…" | 88 / 40; 50 / 35; 82 / 44 | `linear-equations` "I want to have the x's on one side, and I'll have the numbers on the other side" |
| "I'm looking for…" | 36 / 23 | `solve-q-179` "I'm looking for only X over W. What does that mean? I want everything else to cancel" |
| **"… will give me / gets me to / brings me (straight) to"** | 198 / 86; 79 / 50 | `solve-q-164` "That brings me straight away to x is equal to 2." |
| "I'm left with…" | 72 / 48 | `fraction-multiply` "this cancels out, and I'm left with 1 over 6" |
| "get rid of…" | 71 / 27 | `solve-q-296` "How do I get rid of the root in the denominator?" |
| "this whole thing" | 96 / 53 | `solve-q-r26-t04-01` "So now what happens if I square this whole thing?" |
| "to the other side" | 119 / 49 | `solve-q-330` "And I move the two X to the other side. So what am I left with?" |
| "It's as if… / It's like…" | 32 / 15 | `exponents [1312]` "it's as if the 2 to the power of n is turning into its own variable. It's like an x" |

---

## 7. Asking and answering herself

This is her strongest habit: 1,128 real questions, each answered in the very next sentence.

| Pattern | n / v | Quotes |
|---|---|---|
| **"How do I …?"** | 205 / 90 | `solve-q-r26-t11-13` "Now, how do I get from this to this? … I multiply it by two, right?" |
| **"What do I do? / What can I do?"** | 116 / 71 | `solve-q-322` "So what do I do? I start off as treating it as if it's an equation." |
| **"What does that mean? It means…"** | 65 / 48 | `linear-equations [499]` "So what does that mean? It means that x plus 1 cannot be 0, which means x cannot be negative 1." |
| **"What's 24 divided by 8? Three."** (arithmetic Q&A) | 127 / 77 | `linear-equations` "So I have here x plus, what's 2 plus 6? 8." |
| **"Why …? Because …"** | why-questions 65 / 48; "Why? Because" 14 / 11 | `solve-q-181 [90]` "Why am I moving the y squared to the other side? Because I'm looking for the y squared to be in the same side as the x squared." · `solve-q-249` "Why? Because we can't cancel just yet." |
| **"Is that true? No / Can I …? No, because…"** | 40 / 29; 20 / 19 | `primes` "Is 91 divisible by 2? No. Is it divisible by 3? No. … Is it divisible by 7? It actually is, right?" · `solve-q-231` "Can m be 0? No, because 0 to the power of anything will give us 0" |
| "What happens if…?" | 74 / 40 | `systems` "What happens if I add these up? I'll have here 4x, right?" |
| "Can I already circle it and move on? I can't…" | about 8 | `solve-q-r26-t08-01 [102]` "Can I already circle it and move on? I can't because I may have another one" |

It is always **"I"** ("How do I…"), sometimes "we", never "you".

---

## 8. Reactions

| Phrase | n / v | Quotes / note |
|---|---|---|
| **"Perfect."** | 53 / 39 | Her standard approval of a step: `inequalities [353]`, `solve-q-192 [60]`. Use about once a video |
| "Exactly (what we said)" | 93 / 58 | `solve-q-364` "we have here P is greater than Q, which is exactly what we said." |
| "See? / you see how…" | 166 / 89 | `r26-t09-traps [200]` "you see how we got from two completely different numbers that we have no idea what's bigger, now we found out which one's bigger" |
| "Oh, …" (discovery) | rare, about 4 | `solve-q-196 [61]` "Oh, now I got to a point where I have 2xy, right? Okay, now we're getting close" · `solve-q-178 [291]` "Oh, that's a bit easier." |
| "beautiful / cool trick" | 9 / 8; 4 / 4 | `solve-q-125 [236]` "It's a beautiful trick." · `solve-q-296 [144]` "That's another cool trick." · `solve-q-289 [255]` "This is the beauty of the power count." |
| "Great." / "Nice." | 13 / 12; 6 / 5 | Rare. Don't overuse |
| "Mmm, … I don't think so." | about 2 | `solve-q-r26-t06-01 [194]` "Mmm, also, I don't think so" |

She **never** says "Good." (the old AI scripts used it 26 times). She never says "wow" or "awesome" as a reaction.

---

## 9. Emphasis

| Phrase | n / v | Quotes |
|---|---|---|
| "just" (minimiser: "it's just 4") | 865 / 168 | Very frequent. Keep it, but less than she does |
| "actually" (surprise or correction) | 228 / 101 | `solve-q-363` "although this looks negative, it's actually positive." |
| **"(super / really) important"** | 87 / 43 | `fraction-multiply [442]` "Super, super important." · `solve-q-328 [364]` "This is important, confusing but important" |
| "always / never / definitely" | 107 / 47; 25 / 16; 49 / 35 | `roots` "The number that's inside a square root can never be negative." |
| "straight away" | 29 / 20 | `expression-strategy` "you could switch this whole thing straight away without plugging in any numbers." |
| "very, very" | 3 / 3 | `solve-q-363 [103]` "It becomes very, very small and very close to zero, but it does not become negative." |
| "the exam loves…" | 6 / 6 | `exponents` "A rule the exam loves is: when is a to the power of b equal to 1?" |
| Repeating the key line | many | `solve-q-r26-t02-05 [59]` "90 is not what I have left. 90 is what I used." · `solve-q-323 [108]` "False means no x. True means every x." |

The pitch measurements are in `NITZAN_RHYTHM_DELIVERY.md`. She stresses the logic words: not, only, always, both, also, same, opposite. These come out about 1.6 semitones higher and about 2.5 dB louder than her other words. She stresses with her voice and with repetition, not with special words.

---

## 10. Warning about a trap

| Phrase | n / v | Quotes |
|---|---|---|
| "Here's a (classic) trap…" / "This is where the trap is" | 22 / 15 | `linear-equations [917]` "Here's a trap that costs people a lot of points, okay? It's tempting to divide both sides by x." · `fraction-multiply [177]` "Now, here's a classic trap in the exam." · `solve-q-328 [68]` "What does that mean? This is where the trap is" |
| **"a lot of students / most people (will think)…"** | 8 / 8 (+ "a lot of times we think" about 6) | `solve-q-181 [54]` "this is where most people will get wrong" · `absolute-value [196]` "What a lot of students get mixed up with is…" · `r26-t01-must-could` "most people may say no, because a prime is odd and odd plus one is even." |
| "Don't get that confused / don't mix this up" | 10 / 10 | `exponents` "it's not 4 times 3. Don't get that confused." · `fraction-basics [124]` "Don't confuse this. This isn't seven eighths" |
| "watch out / be careful" | 18 / 16; 5 / 5 | `equation-strategy` "What I have to watch out for is when I'm allowed to divide by X. Only if X is not equal to zero." |
| "make sure…" | 49 / 31 | `fraction-add` "I have to make sure I multiply also the top and also the bottom." |
| "It's tempting to… But…" / "intuitively we might think…" | 8 / 6 | `absolute-value` "So intuitively, we might think, oh, it's equal to x… But that may…" |
| "And where does the exam want you to fall?" | 1 | `solve-q-129 [207]` |

**Placement.** The script put about 76 trap lines after the answer. She said about 66 of them nowhere. When she gave a warning, it came before or at the step. In the AI scripts, keep the trap, but move it to the step, in her words.

---

## 11. Giving the verdict

She names the answer by its **value** much more often than by the choice number.

| Phrase | n / v | Quotes |
|---|---|---|
| "And therefore …" before the result | 218 / 108 | `solve-q-231` "and therefore 3 is our answer." |
| "… is our / my answer" / "that's our answer" | 16 / 15; 15 / 13 | `solve-q-133 [450]` "This is the only one that matches it, so this is our answer." · `solve-q-r26-t10-03` "Therefore, two would be my answer." |
| **"I got to my answer" / "And that's it."** | 24 / 24; 16 / 14 | `solve-q-135` "And that's it, got to my answer." · `solve-q-289` "And that's it. I got to it." |
| **"number N"** (not "choice N") | number N 155 / 73, option N 16 / 10, choice N 16 / 10 | `solve-q-332 [227]` "So I'll cross out number one and I'll circle number three." · `solve-q-187` "Therefore, we're left with only number two." |
| "the only one that…" / "left with only…" | 15 / 13; 37 / 32 | `solve-q-224` "number 1 is the only one that matches our answer." |
| **"circle it and move on"** (exam habit) | 19 / 16 | `solve-q-r26-t01-05 [114]` "So in the exam, I would circle number three and move on." · `solve-q-094 [184]` "We could circle two and we can move on without even checking number four." |
| "… and that's enough for me to circle…" | about 5 | `solve-q-337 [30]` "Must be bigger than A and that's enough for me to circle number one" |

**Gap.** In 85 of 154 solution takes she never names a choice number at all; she ends on the value. The AI script must always end with the value and the number: "So x is 6, number three."

---

## 12. Encouragement and reassurance

| Phrase | n / v | Quotes |
|---|---|---|
| "looks scary, but…" | 7 / 6 | `expression-basics [1134]` "will look scary at first, but then you'll see that just things cancel out and it becomes much simpler." · `fraction-multiply` "So this one looks scary, but it actually isn't." |
| "If you don't understand this, don't stress / just leave it" | 4 / 3 | `solve-q-099 [266]` "this one is for truly strong students… So if you don't understand this don't stress about it" · `solve-q-138 [302]` "If this was a bit confusing for you, please leave it. Because this is really for very, very strong algebra students." |
| "If you remember it, great. If not, …" | about 4 | `systems [485]` "a small shortcut that if you remember, it's great. If not, it's not a big deal." · `solve-q-226 [72]` "if I can memorize that three to the power four is 81, that's great. If not, I'll have to calculate it" |
| "It's hard and it's tiring, but it's worth it." | 1 | `r26-t03-summary [428]` |
| "We want to feel comfortable with both of them." | about 4 | `r26-t02-01 [76]`, `powers-techniques [74]` |
| Practise / memorise nudges | memorize 26 / 13; practise 13 / 10 | `decimals [267]` "These are important. So take your time with memorizing them." · `exponents [404]` "Please pause this and practice it with yourself if you don't feel confident with this yet." |
| "that's how we train our brain" | about 4 | `solve-q-125 [409]`, `solve-q-091 [143]` |

**Not high school.** She uses this 13 times in 7 takes:
- `solve-q-r26-t05-03 [12]` "We don't need that. That's high school math."
- `compare-fractions [948]` "a lot of times we don't have to get to a final mathematical answer like we had to do in high school. Over here, it's different."
- `solve-q-369 [429]` "psychometric cheats that aren't cheats. These are the proper ways."

---

## 13. Humour and warmth

She is warm and dry, not jokey. There are no puns and no laughing. The humour is in vivid images and honest asides.
- Everyday pictures: `absolute-value [47]` "If you're now walking to the bus stop, it isn't minus two kilometers away, right?" · `numbers [621]` "I give all 27 of my candies to one person." · `fraction-basics [542]` sharing a pizza with one person vs seven · `expression-basics [77]` "It's like adding apples and pears."
- Personifying numbers and maths: `add-subtract [501]` "0 says don't worry, I've got you" · `expression-strategy [613]` "I'll call them the lazy numbers." · `numbers` 0 is "the exam's favorite troublemaker" · `roots` "the root world", "under one umbrella", "they speak the same language" (12 / 5).
- Honest asides: `roots [931]` "Well, I actually lied because cube roots are different" · `solve-q-389 [121]` "Well, I actually have no idea. So I'll start with dividing it by two." · `solve-q-296 [6]` "roots in the denominator are always gross." · `solve-q-194 [22]` "Denominators are always bad, so let's try to get rid of it." · `solve-q-138 [48]` "Oh, that was dangerous." · `solve-q-188 [106]` "It's just a riddle. It's not much math to it." · `solve-q-097 [242]` "they gave it to us on a silver plate, right?"
- Job-interview aside (`solve-q-134 [19]`): "No one expects you to actually know that."

**Rule.** Use at most one image or aside per video, at the hardest point. The images she already uses are listed above, so reuse them rather than inventing new ones.

---

## 14. Recap

| Phrase | n / v | Quotes |
|---|---|---|
| "So again, (what did we do / how do we do this)?" | 20 / 16; 15 / 14 | `solve-q-335 [159]` "So again, how do we do this?" · `solve-q-r26-t12-03` "So what did we say we could do? We can subtract in diagonal" |
| **"We said (that)…"** (linking back) | 130 / 70 | `linear-equations` "let's go back to our golden rule. What was our golden rule? We said that whatever we do for one side…" |
| "Remember…" | 90 / 45 | `exponents` "Remember, we said we're always downgraded." |
| "Let's do a quick summary / Here's a short summary" | 9 / 9 | `fraction-basics [758]` "Now let's do a quick summary." · `expression-basics` "Here's a short summary of what we saw today." |
| "So let's lock it in." | 4 / 4 | `numbers` "Lock it in. Zero is an integer, zero is even, and zero is not positive and not negative." |
| Capsule rule (6-10 words, parallel) | many | `solve-q-323 [108]` "False means no x. True means every x." · `solve-q-r26-t12-signs` "If it's the same sign, they flip. If there are different signs, then they don't flip." |

---

## 15. Closings

| Phrase | n / v | Note |
|---|---|---|
| **"I'll see you in the next lesson / question / video."** | "see you" 79 / 79: next lesson 39, next question 29, next video / one 25 | About 42% of takes. Many solution takes simply stop after the answer |
| One nudge before it | about 30 | `advanced-powers` "Try each one first, okay? Try both methods, and then watch the solutions. See you in the next video." · `solve-q-389 [286]` "Super important. So please rewatch this if this wasn't clear." · `fraction-multiply [823]` "Well done for today and I'll see you in the next lesson." |
| Method summary as a close | about 15 | `solve-q-296` "So we have here three different methods for the same question." · `solve-q-r26-t09-02` "That's two different ways to get to the same answer." |

She says "lesson" even after a question about 5 times. In AI scripts, use "question" after a solution.

---

## 16. How she says numbers, fractions, powers, roots and operations

| Thing | She says (use this) | Counts / notes |
|---|---|---|
| Powers | **"2 to the power of 10"**, "x to the power of minus 3", "to the power of n plus 3" | 674 / 47. Ordinal forms ("to the tenth") 5 in total. "squared" 750 / 72. "cubed" only 34 / 7; she prefers "to the power of 3" |
| Fractional powers | "to the power of a half", "to the power of 2 thirds", "nine to the power of three over two" | "power of a half" 19 / 4 |
| Roots | "root 44", "root of 25", "the square root of 2", "5 root 2", "a fourth root", "a cubed root" | Avoid "cubed root", which is a slip (write "cube root"). "a silent 2" for the hidden index (`r26-t09-05 [106]`) is FLAVOUR, keep it |
| Fractions, simple | "a half", "a third", "a quarter", "two thirds", "three quarters", "a fifth", "an eighth", "nine quarters" | 311 / 46 |
| Fractions, bigger | **"5 over 13"**, "19 over 6", "60 over 90", "1 over 27" | "N over M" 511 / 70. She never says "nineteen sixths" or "ninetieths" |
| Mixed numbers | "6 and a third", "1 and a half", "4 and 2 thirds" | |
| Equals | **"is equal to"** 627 / 131; "equals" also common; **"equals to"** 116 / 45 (slip) | Write "is equal to" or "equals" |
| Negatives | "minus 5" (1,053) and "negative 5" (435), often both in one sentence | Fine either way. For the sign rule she says **"minus minus… collapses into a plus"** (19 / 9) |
| Operations | "times" (1,180), "divided by" (198), "plus", "minus", "over" | "multiplied by" only 17 |
| Inequalities | **"is smaller than"** (230), "is bigger than" (177), "is greater than" (176); "less than" only 39 | "greater or equal to" (she drops "than"). Ranges: "x is between 2 and 9", "trapped between" |
| Absolute value | "the absolute value of x" (89), "2x minus 1 in absolute value" (12) | Rarely "bars" |
| Brackets | "open up the brackets" (20 / 12), "all that squared", "this whole thing", "in brackets" | She often **doesn't voice the bracket** ("3x plus y plus 1" for 3(x+y)+1). The AI must say "3 times, in brackets, x plus y" or "x plus y, all that times 3" |
| Fraction parts | "on the top / on the bottom" (74 / 32) and "numerator / denominator" (223 / 43) | Says the plain word first, then the term |
| Mental maths | "What's 24 divided by 8? Three." / "2 plus 2, 4 plus 2, 6 plus 2, 8" / "10 times 44 is 440, now 440 times three…" | Always split into easy pieces |
| Decimals | "0.125", "4.5", "move the decimal point one spot to the left" | |
| Choices | **"number three"**, "option number one", "answer number 2"; rarely "choice" | "Answer number" can be confused with a branch ("answer number one is m = 0"). Use "number" |
| Unknown values | "equals question mark" | `solve-q-178 [59]` |

---

## 17. Fillers and hesitations: what they are and where

Whisper removes "um" and "uh", so these come from the audio (word timestamps plus silence detection). Full numbers are in the rhythm file.
- **Her fillers are words, not sounds:**
  - "So, …" restarts a sentence.
  - "Okay," (633 / 145, 339 at the start of a sentence).
  - "right?"
  - "let's see".
  - "basically" (75 / 38), "like" (as a filler: "try to like keep that in your memory").
  - "kind of" (17 / 11), "I mean" (10 / 10).
- **Where her hesitations happen:**
  - Elongated function words before a number or an expression she is reading off the board: "that… are below zero", "so we have… somewhere".
  - Restarting the subject: "So it's, I would say it's the language…".
  - "I could do is I could…" (31 / 26): a doubled "I could" when she is choosing a move.
- **Self-repairs:** "sorry" (17 / 17) and "no, wait / the opposite".
  - These cluster where she reads a formula aloud or compares signs. `solve-q-295` "Because I have two times square, sorry…" · `solve-q-358` "No, sorry the opposite." · `solve-q-325 [51]` "Okay, wait. What happens here?"
- **Doubled starts:** "Also, also the left side and also the right side" (`equation-strategy`) and "we have here we have" (14 / 13).

**Rule.** The AI should **not** script her fillers. Keep at most one "Okay," or "So," per beat as a joint, and never script "sorry" or "I mean". Her natural hesitation shows up as a slight slow-down before the key number. Get that with a comma, not a filler (see the rhythm file).

---

## 18. Non-native or unclear wording: what to copy and what not

**FLAVOUR, Israeli English that sounds fine. The AI may keep it (sparingly):**
- "also the top and also the bottom" / "also the left side and also the right side" (62 / 38). Her signature, and clear.
- "I have here…" / "we have here…".
- "this whole thing", "over here".
- "collapses into a plus".
- "they speak the same language", "the root world", "under one umbrella", "different families".
- "throw us to / jump into mind" (recognising a formula). "Throw us to" is borderline; "should make you think of" is cleaner.
- "the troublemakers", "the lazy numbers", "a silent 2", "the survivor", "tie-breaker", "copies of 41".
- "we could promise ourselves" (`solve-q-364 [43]`), "Agreed?" (`solve-q-363 [34]`), "on a silver plate".
- "So I flip it too", "this is how it would look like" (common in speech; the AI can use "this is what it looks like").
- "Honestly, …", "Super important.", "Perfect."
- "the psychometric" as a noun ("in the psychometric, usually that's not needed"). Acceptable, but **"on the exam"** is clearer for an international audience. Prefer "on the exam".

**SLIP. Do not copy:**

| Her words | Say instead | Where |
|---|---|---|
| "equals to 5" | "equals 5" / "is equal to 5" | 116 / 45 |
| "the psychometry" (as the exam's name) | "the exam" / "the psychometric exam" | 21 / 14 |
| "full number(s)" | "whole number(s)" | 5 / 3 (Hebrew *mispar shalem*) |
| "how would it look like" | "what it would look like" | 4 / 3 |
| "verse" | "versus" | `decimals [812]`, `r26-t09-traps [185]` |
| "cubed root" | "cube root" | `solve-q-301`, `r26-t09-01 [87]` |
| "x square" | "x squared" | `r26-t12` |
| "even amount of negatives" | "an even number of negatives" | `fraction-basics [729]` |
| "the minus that belongs to him" | "belongs to it" | `fraction-basics [747]` (Hebrew gender) |
| "plays its own rules" | "plays by its own rules" | `multiply-divide [111]` |
| "take down / took down for too many" | "subtract / took away 4 too many" | `add-subtract [658]`, `[673]` |
| "for you to see it in your eyes" | "to see it for yourself" | `exponents [1429]` |
| "will add you the seconds" | "will save you seconds" | `exponents [1580]` |
| "I could have did" | "I could have done" | `solve-q-129 [131]`, `solve-q-091 [131]` |
| "traits" (for cases / intervals / properties) | "cases", "ranges" | `r26-t13-13`, `t12-02`, `q-096` |
| "differentiates between" | "tells apart" | `compare-fractions`, `solve-q-295` |
| "two even groups" | "two equal groups" | `numbers [387]` |
| "This equation does not exist." | "This equation has no solution." | `r26-t06-02 [157]` |
| "reciprocals" when she means opposites | "opposites" | `solve-q-366 [136]` |
| "cross multiply" for cancelling equal denominators, or for finding a common denominator | "multiply both sides by…" / "find a common denominator" | `r26-t06-02`, `expression-strategy [103]` |
| "LCM is the lowest common denominator" | "LCM is the least common multiple" | `fraction-add [307]` |
| "the root is on top / the power is dominant" (her private power↔root mnemonic) | "the power goes on top, the root goes on the bottom" | `roots [1100]`, `t09-01`, `t11-13`, `q-294` |
| "absolute value is always positive" | "never negative, it can be zero" | `absolute-value [53]`, `r26-t13-02 [48]` |
| Agreement and article slips: "the ingredients of 150 is", "My pieces is", "letters is", "a bars", "two prime" | standard grammar | many |
| Garbled sentences: "We proved it wrong. We proved it right. We proved that it's definitely not necessarily" | rewrite fully | `solve-q-094 [174]` |
| Dropped negation: "just stick to one method" (meant "don't") | — | `expression-strategy [753]` |

**General rule.** Her Hebrew-shaped *structures* sound natural and can stay: "also… and also", "I have here", "so" to open a sentence, a question then the answer. Her *word errors* and *agreement errors* must be corrected. Wherever the meaning flips, the AI script must use the exact correct sentence:
- at most vs less than
- never negative vs always positive
- opposites vs reciprocals
- multiply vs divide by x
