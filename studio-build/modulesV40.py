# Verbal Reasoning · Topic 40 · Analogies.
# Hebrew (hebverbal.txt 14–649) decides the concepts, lesson order, methods, tips and verdicts.
# Every example is one of the course's own English analogies (tv40.txt) — word pairs and choices unchanged.
from dsl import *

T40 = 40
Q = dict(size=64, csize=38)          # analogies: short pair on top, large; answers large


def W(t, y, size=40):                # full-width lesson pop-in
    return T(t, size=size, x=410, y=y, w=1140)


# ------------------------------------------------------------------ lesson 1 · what is an analogy (Hebrew 1–63)
SB1 = ['Where and how fast', 'What they test', 'The instructions', 'Meaning, not form',
       'The most similar', 'Order matters', 'How to solve']
L1 = lesson('vr40-intro', 'What Is an Analogy?', SB1, [
    dict(mode='title', title='What Is an Analogy?', script=[
        "Analogies.",
        "In this lesson: what an analogy is — and how you solve one.",
    ]),
    dict(mode='concept', active=0, title='Where and how fast', script=[
        "The verbal reasoning section opens with the analogies.",
        A("Questions 1–6 of the section · rising difficulty appears", W('Analogies open the section: questions $1$–$6$, in rising difficulty', 140)),
        "About six of them — right at the start of the section, and they get harder as you go.",
        A("20–30 seconds per analogy appears", W('Recommended time: $20$–$30$ seconds per analogy', 240)),
        "The recommended time per analogy: twenty to thirty seconds. Fast.",
    ]),
    dict(mode='concept', active=1, title='What they test', script=[
        "What do these questions check?",
        A("Can you define the relation between two words? appears", W('1 · Can you define the relation between two words?', 140)),
        "First — your ability to define the relation between two words.",
        A("Can you find another pair with the same relation? appears", W('2 · Can you find another pair with a similar relation?', 220)),
        "And then find another pair with a similar relation.",
        A("Vocabulary appears", W('3 · Your vocabulary', 300)),
        "One more thing they test: how rich your vocabulary is.",
    ]),
    dict(mode='concept', active=2, title='The instructions', script=[
        "Let's read the instructions as they appear in the exam.",
        A("Each question has a pair of words in bold appears", W('Each question has a pair of words in bold, for example:', 140)),
        A("crest : wave appears", T('crest : wave', size=70, x=410, y=230, w=1140)),
        "Crest and wave.",
        A("Find the relation between the meanings of these two words appears", W('Find the relation between the meanings of these two words.', 350)),
        "Find the relation between the meanings of the two words.",
        "What's the relation between crest and wave? The crest is the top part of a wave.",
        D("Write under the pair: crest = the top part of a wave"),
    ]),
    dict(mode='concept', active=3, title='Meaning, not form', script=[
        "The first point to notice in the instructions: the relation between the MEANINGS.",
        A("Meaning only — not spelling, sound or length appears", W('Meaning only — not spelling, sound or length', 140)),
        "What does that mean? The form of the words doesn't interest us.",
        "Same first letter, same length, they rhyme — it doesn't matter.",
    ]),
    dict(mode='concept', active=4, title='The most similar', script=[
        "Let's keep reading.",
        A("Choose the pair whose relation is the MOST similar appears", W('Choose the pair whose relation is the MOST similar to the relation you found.', 140)),
        "Choose, from the answers, the pair whose relation is the most similar to the one you found.",
        "So we need the MOST similar relation.",
        "There may be more than one pair with a similar relation — we need the closest one.",
    ]),
    dict(mode='concept', active=5, title='Order matters', script=[
        "Keep reading the instructions: note — the order of the words in the pair matters.",
        A("The order of the words in the pair matters appears", W('The order of the words in the pair matters.', 140)),
        "What does that mean?",
        A("crest → the top part of → wave appears", T('crest $\\rightarrow$ the top part of $\\rightarrow$ wave', size=46, x=410, y=240, w=1140)),
        "The crest is the top part of the wave. The first word is the top part of the second word — not the other way round.",
        "That's the third point from the instructions: order matters.",
    ]),
    dict(mode='concept', active=6, title='How to solve', script=[
        "So we've read the instructions. Now — how do you solve an analogy?",
        A("1 · Ignore the answers. Build a connecting sentence. appears", W('1 · Ignore the answers — build a connecting sentence for the pair', 140)),
        "First we find the relation: we build a connecting sentence. We ignore the answers, look only at the pair, and build a sentence.",
        A("2 · Put your sentence on every answer appears", W('2 · Put the same sentence on every answer', 230)),
        "Then we put the sentence we built on each of the answers, and check: does it fit or not?",
        A("3 · Check ALL four — eliminate three appears", W('3 · Check all four — the method is to eliminate three', 320)),
        "And we check all the answers. Always. The method in analogies isn't marking the right answer — it's eliminating three.",
        "Let's see it on our first question.",
    ]),
], T40)

SBQ1 = ['Q1']
Q1 = guided(0, 'vr40-g001', 'Analogy Basics', SBQ1,
    ["Our first analogy — let's solve it with the method."],
    [('Build the sentence', [
        "Crest and wave. We ignore the answers and build a connecting sentence.",
        A("crest = the top part of a wave appears", P('crest = the top part of a wave', size=44, y=230)),
        D("Draw an arrow from crest to wave and write: top part of"),
        "The crest is the top part of the wave.",
     ]),
     ('Check every answer', [
        "Now we put the sentence on each answer.",
        "Is rain the top part of a cloud? No. Rain falls from a cloud.",
        D("Cross out choice 1"),
        "Is a summit the top part of a mountain? Yes! So can I mark it?",
        D("Put a question mark next to choice 2"),
        "Not yet. In analogies we must check all the answers.",
        "Why? They asked for the MOST similar relation. There may be another pair further down with a similar relation.",
        "Is an oar the top part of a boat? No — an oar is what you row the boat with.",
        D("Cross out choice 3"),
        "Is a harbor the top part of a ship? No — a harbor is where a ship docks.",
        D("Cross out choice 4"),
        "Three eliminated. Now I can mark it.",
        D("Circle choice 2"),
        "Choice 2.",
     ]),
     ('The key to analogies', [
        "So we've seen the instructions, an example, and how to solve.",
        A("The more precise the sentence → the easier to eliminate appears", P('The more precise the sentence, the easier it is to eliminate three', size=38, y=230)),
        "The most important thing in analogies: build the connecting sentence as precisely as you can.",
        "A precise sentence lets you eliminate three answers easily.",
        "How do you build a precise sentence? That's the next lesson — solving techniques.",
     ])], T40, q=Q)

# ------------------------------------------------------------------ lesson 2 · techniques (Hebrew 64–247)
SB2 = ['The goal', '"What is it?"', 'Opposite of…', 'Meaning over form',
       'Someone = something', 'Start from word two', 'Two words, one look', 'Sharpen the sentence']
L2 = lesson('vr40-techniques', 'Building the Sentence', SB2, [
    dict(mode='title', title='Building the Sentence', script=[
        "Solving techniques for analogies.",
        "Last lesson we learned what analogies are and how to solve them.",
        "We ended with: the most important thing is to build the most precise relation you can.",
    ]),
    dict(mode='concept', active=0, title='The goal', script=[
        A("Precise sentence → eliminate 3 → faster appears", W('A more precise sentence $\\rightarrow$ easier to eliminate three $\\rightarrow$ faster', 140)),
        "The more precise the relation, the easier it is to eliminate three answers — and the faster you solve.",
        "In this lesson: techniques for building the sentence, and nuances you need to watch for while solving.",
    ]),
    dict(mode='concept', active=1, title='"What is it?"', script=[
        "The most common technique we'll use: \"What is it?\"",
        A("\"What is it?\" — define one word using the other appears", W('"What is it?" — define one word using the other word', 140)),
        "What does that mean? We define one word by means of the other word.",
        "Imagine your little nephew comes over and asks: what does that word mean?",
        "And you have to explain it to him — using the other word in the pair.",
        "Let's see it on a question.",
    ]),
    dict(mode='concept', active=2, title='Opposite of…', script=[
        A("\"…the opposite of…\" appears", W('A nuance that comes up again and again:  "…the opposite of…"', 140)),
        "A nuance that repeats itself a lot in the exam: the opposite of.",
        "Often, instead of defining something directly, we define it through its opposite.",
    ]),
    dict(mode='concept', active=3, title='Meaning over form', script=[
        A("Only the meaning matters — not the exact word you used appears", W('Only the meaning matters — not the exact word in your sentence', 140)),
        "When you put your sentence on an answer, you may need to change a word — short, weak, small.",
        "Singular, plural, the exact adjective — it doesn't really matter. Only the meaning matters.",
    ]),
    dict(mode='concept', active=4, title='Someone = something', script=[
        A("someone / something — the same for us appears", W('"someone" or "something" — for us it is the same', 140)),
        "Same idea: if your sentence says someone and the answer needs something — for us that's the same thing.",
        "What matters is the meaning.",
    ]),
    dict(mode='concept', active=5, title='Start from word two', script=[
        A("You may define the SECOND word first appears", W("You don't have to define the first word — start from the second if it's easier", 140)),
        "Another nuance: you don't have to define the first word. You can start from the second word, if that's easier.",
        A("Started from word 2 → check the answers from word 2 appears", W('Started from the second word? Check the answers from the second word too.', 240)),
        "But — if you started the question from the second word, you must check the answers from the second word too.",
    ]),
    dict(mode='concept', active=6, title='Two words, one look', script=[
        A("A word that can be read two ways = a warning light appears", W('A word that can be read two ways = a warning light', 140)),
        "When a word in the pair can be read in two ways — say, as a noun or as a verb — treat it like a warning light.",
        "Make sure you know which meaning they intended. Otherwise the whole analogy can go wrong.",
    ]),
    dict(mode='concept', active=7, title='Sharpen the sentence', script=[
        A("Two answers left? Sharpen the sentence appears", W('Your sentence fits two answers? Sharpen it.', 140)),
        "Sometimes our sentence can't tell two answers apart.",
        "Then we need a different sentence — a more precise one. We call this sharpening the relation.",
        "Let's see all of these on questions.",
    ]),
], T40)

SBQ2 = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
G2 = 'Sentence Techniques'
Q2 = guided(0, 'vr40-g002', G2, SBQ2,
    ["A sample question — position 1, relatively easy."],
    [('"What is it?"', [
        "To inspect and inspection. We need the relation — with a connecting sentence.",
        "The most common technique: \"What is it?\" We define one word using the other.",
        "What is to inspect? Explain it to your nephew — using the word inspection.",
        A("to inspect = to carry out an inspection appears", P('to inspect = to carry out an inspection', size=44, y=230)),
        "To inspect is to carry out an inspection.",
     ]),
     ('Check every answer', [
        "Remember — we're not finding the right answer. Our goal is to eliminate three.",
        "Is to arrive to carry out an invitation? No. You arrive because you were invited.",
        D("Cross out choice 1"),
        "Is to select to carry out a selection? Yes — a selection is exactly what you carry out when you select.",
        D("Put a question mark next to choice 2"),
        "Is to rest to carry out fatigue? No. You rest because of fatigue.",
        D("Cross out choice 3"),
        "Is to sleep to carry out a dream? Similar… but I'm not sure it's the most similar. Let's leave it for now.",
        D("Put a question mark next to choice 4"),
     ]),
     ('The most similar', [
        "Two eliminated, two left. We're looking for the most similar relation.",
        "To select is to carry out a selection — an exact fit.",
        "To sleep — to carry out a dream? Not exactly. A dream is something that happens while you sleep. Sleeping isn't carrying out a dream.",
        D("Cross out choice 4"),
        "Three eliminated. We mark the one that's left.",
        D("Circle choice 2"),
        "Choice 2.",
     ])], T40, q=Q)

Q3 = guided(1, 'vr40-g003', G2, SBQ2,
    ["Another example — again position 1, relatively easy."],
    [('The opposite of', [
        "To straighten and bent. To use our technique, we define one word using the other.",
        "What is to straighten? To make something straight.",
        "But I have to define it using the word bent. So — to straighten is to make something the opposite of bent.",
        A("to straighten = to make something the opposite of bent appears", P('to straighten = to make something the opposite of bent', size=40, y=230)),
        D("Underline: the opposite of"),
        "The opposite of — a nuance that repeats itself a lot in the exam.",
     ]),
     ('Check every answer', [
        "Is to whisper to make something the opposite of quiet? No — a whisper IS quiet. It doesn't make anything the opposite of quiet.",
        D("Cross out choice 1"),
        "Is to dry to make something the opposite of wet? Yes. Drying makes something dry — the opposite of wet.",
        D("Put a question mark next to choice 2"),
        "Is to polish to make something the opposite of shiny? No — polishing makes it shiny.",
        D("Cross out choice 3"),
        "Is to describe to make something the opposite of detailed? No. A description can be detailed.",
        D("Cross out choice 4"),
        "Three eliminated. We mark what's left.",
        D("Circle choice 2"),
        "Choice 2.",
     ])], T40, q=Q)

Q4 = guided(2, 'vr40-g004', G2, SBQ2,
    ["Another example — position 3, medium level."],
    [('"What is it?"', [
        "Trickle and flow. Again — \"What is it?\" We define one word using the other.",
        "What is a trickle? A trickle is a flow — a weak one. A very weak one.",
        A("trickle = a very weak flow appears", P('trickle = a very weak flow', size=44, y=230)),
     ]),
     ('Check every answer', [
        "Is a page a very weak chapter? No. A page is part of a chapter.",
        D("Cross out choice 1"),
        "Is a glimmer a very weak light? Let's change the word — very faint light. Yes.",
        D("Put a question mark next to choice 2"),
        "See what I did? I changed the word — weak, faint.",
        A("weak / faint / small — only the meaning matters appears", P('weak · faint · small — only the meaning matters', size=36, y=330)),
        "What matters is that the meaning is similar. Not the exact word.",
        "Is a syllable a very weak word? Let's say a very short word… Similar. I'm not sure yet if it's the most similar. Leave it.",
        D("Put a question mark next to choice 3"),
        "Is a drop a very weak bottle? No. A drop could be IN a bottle.",
        D("Cross out choice 4"),
     ]),
     ('The most similar', [
        "Two left. Which is more similar?",
        "A syllable isn't really a short word. Several syllables together BUILD a word. It's a part of a word — not a weak form of one.",
        D("Cross out choice 3"),
        "A glimmer is a very faint light — exactly like a trickle is a very weak flow.",
        D("Circle choice 2"),
        "Choice 2.",
     ])], T40, q=Q)

Q5 = guided(3, 'vr40-g005', G2, SBQ2,
    ["Another example — position 6. Relatively hard."],
    [('Build the sentence', [
        "To immerse and liquid. Our technique: \"What is it?\"",
        "What is to immerse? Let's define it using the word liquid.",
        A("to immerse = to put something into a liquid appears", P('to immerse = to put something into a liquid', size=42, y=230)),
        "To immerse is to put something into a liquid.",
     ]),
     ('Check every answer', [
        "Is to sweep to put something into a floor? No. Cross it out.",
        D("Cross out choice 1"),
        "Is to bury to put something into earth? Someone, something — for us it's the same. Yes, it fits.",
        D("Put a question mark next to choice 2"),
        "Is to bake to put something into an oven? Hmm — you do put it in the oven… but baking is cooking it, not putting it in.",
        D("Cross out choice 3"),
        "Is to read to put something into a library? No.",
        D("Cross out choice 4"),
        "Three eliminated. We mark the one left.",
        D("Circle choice 2"),
        "Choice 2.",
     ]),
     ('Why is it a 6?', [
        "We built a sentence and eliminated three — without much trouble. So why is this question number 6? Why is it considered hard?",
        "Some students don't build a connecting sentence. And here's what happens.",
        A("\"An action + a place\" → the trap appears", P('"An action and a place" — too vague → the trap', size=38, y=230)),
        "They say: to immerse is an action. To sweep, to bury, to bake, to read — all actions.",
        "Then: liquid is… a medium. An oven is a place in the kitchen — cooking. It feels close. They mark choice 3 — and they're wrong.",
        "Why is it wrong? To bake is to cook something in the oven. To immerse isn't to cook something in a liquid.",
        "When you build a connecting sentence, it's much easier to see what doesn't fit.",
     ])], T40, q=Q)

Q6 = guided(4, 'vr40-g006', G2, SBQ2,
    ["Another example — position 4, medium-plus."],
    [('Start from word two', [
        "Equipment and to equip.",
        "Notice: to equip. The word could be read more than one way — equipment, to equip. That's a warning light. Make sure which meaning they intend.",
        "Let's solve. What is equipment? Things you… equip someone with… I'm starting to get tangled.",
        "Which leads us to another nuance: I don't have to define the first word. I can start from the second word if it's easier.",
        A("to equip = to give equipment appears", P('to equip = to give equipment', size=44, y=230)),
        D("Draw an arrow from to equip back to equipment"),
        "What is to equip? To give equipment.",
     ]),
     ('Check from word two', [
        "Now we check the answers — but since we started from the second word, we must check the answers from the second word too.",
        "To ask — is to ask to give a question? No. You ask a question — you don't hand it to someone.",
        D("Cross out choice 1"),
        "To sing — to give a song? No. Singing produces a song.",
        D("Cross out choice 2"),
        "To arm — to give weapons? Yes. It fits.",
        D("Put a question mark next to choice 3"),
        "To legislate — to give a law? Hmm… yes, you could say that too.",
        D("Put a question mark next to choice 4"),
        "Our sentence can't tell the two apart. We need a different, more precise sentence.",
     ]),
     ('Sharpen the relation', [
        "We call this sharpening the relation.",
        "When I equip someone, I give the equipment TO SOMEONE ELSE. It passes from me to them.",
        A("to equip = to give equipment TO SOMEONE ELSE appears", P('to equip = to give equipment to someone else', size=40, y=230)),
        D("Underline: to someone else"),
        "To arm — to give weapons to someone else? Yes. When you arm someone, you hand them weapons.",
        "To legislate — to give a law to someone else? No. Legislating is creating a law — you don't hand it to anyone.",
        D("Cross out choice 4"),
        D("Circle choice 3"),
        "Choice 3.",
     ])], T40, q=Q)

# ------------------------------------------------------------------ lesson 3 · through the answers (Hebrew 360–424)
SB3 = ["Can't build it", 'Fits no answer', 'Fits two answers', 'The name trick', 'Summary']
L3 = lesson('vr40-through-answers', 'Solving Through the Answers', SB3, [
    dict(mode='title', title='Solving Through the Answers', script=[
        "Analogies — solving through the answers.",
        "Last lesson: techniques for building the most precise relation we can.",
        "But there are rare cases where the sentence we build won't work for us.",
        "In those situations we use a psychometric technique: solving through the answers. That's this lesson.",
    ]),
    dict(mode='concept', active=0, title="Can't build it", script=[
        A("Situation 1: you can't build a sentence appears", W("Situation 1: you know the words — but can't build the sentence", 140)),
        "Sometimes you know the words, and still it's hard to put the exact relation into a sentence.",
        A("The right relation appears TWICE — in the pair and in the answer appears", W('The right relation appears twice: in the pair AND in the right answer', 240)),
        "Remember: the correct relation appears twice — in the question and in the right answer. It may be easier to spot it in the answer.",
        "So we go through the answers: build a sentence for each answer, and put it back on the pair.",
    ]),
    dict(mode='concept', active=1, title='Fits no answer', script=[
        A("Situation 2: your sentence fits no answer appears", W('Situation 2: your sentence eliminates all four answers', 140)),
        "Sometimes we build a sentence — and eliminate all four answers. It happens.",
        A("→ build a new sentence  OR  work through the answers appears", W('Then: build a new sentence — or work through the answers', 240)),
        "Two options: try a new relation that hopefully fits the right answer — or work through the answers.",
    ]),
    dict(mode='concept', active=2, title='Fits two answers', script=[
        A("Situation 3: your sentence fits two answers appears", W('Situation 3: your sentence fits two answers', 140)),
        "Or the opposite: the sentence fits more than one answer.",
        A("Only one right answer → there MUST be a difference appears", W('Only one answer is right — so the two relations must differ', 240)),
        "It can't be that both answers have exactly the same relation. There's only one right answer — there must be a difference.",
        A("Reset → build a sentence for each remaining answer appears", W('Reset — build a fresh sentence for each remaining answer', 330)),
        "Here's the catch: our heads are stuck on the sentence we built. We need a reset — forget it and start fresh from each answer.",
    ]),
    dict(mode='concept', active=3, title='The name trick', script=[
        A("Hard to phrase? Put the words in a story with names appears", W('Hard to phrase? Put the words into a little story with names', 140)),
        "One more trick for pairs that are hard to phrase: put the words into a little story with people's names.",
        "You'll see it on a question.",
    ]),
    dict(mode='concept', active=4, title='Summary', script=[
        A("Can't build · fits none · fits two → through the answers appears", W("Can't build a sentence · it fits no answer · it fits two  →  work through the answers", 140, size=36)),
        "When you can't build a sentence, or the sentence you built fits no answer or several — use the psychometric technique: solve through the answers.",
        "It works great. Let's see it.",
    ]),
], T40)

SBQ3 = ['Q1', 'Q2', 'Q3']
G3 = 'Through the Answers'
Q7 = guided(0, 'vr40-g012', G3, SBQ3,
    ["A sample question — position 6, relatively hard."],
    [('Hard to phrase', [
        "Famine and a small food parcel.",
        "What is a famine? A severe lack of food. A small food parcel — a little bit of food.",
        "Let's try to build the relation between famine and a small food parcel… It's a bit hard.",
        "Some students will see this analogy and phrase it easily. But sometimes, even when you know the words, it's hard to phrase the exact relation.",
        A("The right relation appears twice — look in the answers appears", P('The relation appears twice — maybe it is easier to spot in the answer', size=36, y=230)),
        "That's another situation for solving through the answers.",
     ]),
     ('Through the answers', [
        "A wound and a full recovery: a full recovery completely ends a wound. Is a small food parcel something that completely ends a famine? No.",
        D("Cross out choice 1"),
        "A journey and its destination: the destination is where a journey ends. Is a food parcel where a famine ends? No.",
        D("Cross out choice 2"),
        "A drought — a severe lack of rain. A brief shower helps only a tiny bit in a drought.",
        A("brief shower = helps very little in a drought appears", P('a brief shower helps very little in a drought', size=38, y=330)),
        "Just like a small food parcel helps only a tiny bit in a famine. It fits.",
        D("Put a question mark next to choice 3"),
        "A question and a complete answer: a complete answer fully resolves a question. A parcel doesn't fully resolve a famine.",
        D("Cross out choice 4"),
        D("Circle choice 3"),
        "Choice 3. We couldn't build the sentence — the answers built it for us.",
     ])], T40, q=Q)

Q8 = guided(1, 'vr40-g013', G3, SBQ3,
    ["Another sample question — position 6, relatively hard."],
    [('A sentence that fits nothing', [
        "Mouth and cave. What is the mouth of a cave?",
        "Let's say — the mouth is the end of the cave.",
        A("mouth = the end of a cave? appears", P('mouth = the end of a cave?', size=44, y=230)),
        "Let's check the answers.",
        "Is a blade the end of a knife? Not really — the blade is the cutting part.",
        D("Cross out choice 1"),
        "Is an eye the end of a needle? No — the eye is a hole in the needle.",
        D("Cross out choice 2"),
        "Is a handle the end of a suitcase? No — it's the part you hold.",
        D("Cross out choice 3"),
        "Is a lining the end of a coat? No — it's the inner layer.",
        D("Cross out choice 4"),
        "We built a sentence and eliminated all four. It happens.",
     ]),
     ('Through the answers', [
        "Two options: build a new relation — or, when our sentence doesn't fit, work through the answers.",
        "A blade is the cutting part of a knife. Is a mouth the cutting part of a cave? No.",
        "An eye is a hole — an opening — in a needle. Is a mouth an opening in a cave? Yes! It fits.",
        A("eye = the opening in a needle appears", P('eye = the opening in a needle  ·  mouth = the opening of a cave', size=36, y=330)),
        "Let's keep checking.",
        "A handle is the part of a suitcase you hold. Is a mouth the part of a cave you hold? No.",
        "A lining is the inner layer of a coat. Is a mouth the inner layer of a cave? No.",
        D("Circle choice 2"),
        "Choice 2.",
     ])], T40, q=Q)

Q9 = guided(2, 'vr40-g014', G3, SBQ3,
    ["Another example — position 4, medium-plus."],
    [('The name trick', [
        "Was lowered and descended. Let's build the relation.",
        "What is was lowered? To descend… because someone else did it to you. A bit hard. Let's try from the second word.",
        "Descended — was lowered by yourself? Still hard to phrase.",
        "When it's hard to phrase, use the name trick.",
        A("Sam was lowered — Dana descended by herself appears", P('Sam was lowered — Dana descended by herself', size=42, y=230)),
        "Sam was lowered, and Dana descended by herself. Much simpler.",
     ]),
     ('Check every answer', [
        "Sam was raised, and Dana ascended by herself. Fits. Keep checking.",
        "Sam was invited, and Dana arrived by herself. Also fits. Keep checking.",
        "Sam was warned, and Dana obeyed by herself? No.",
        D("Cross out choice 3"),
        "Sam was praised, and Dana improved by herself? No.",
        D("Cross out choice 4"),
        "Two left. With the sentence I built, I can't eliminate either of them. So what do we do?",
     ]),
     ('Reset and compare', [
        "Two options: find a new sentence that does eliminate one of them — or work through the answers.",
        "Only one answer is right, so there must be a difference between the two relations.",
        "We're stuck on our sentence — reset. Build a sentence for each remaining answer.",
        A("was raised = someone made him ascend appears", P('was raised = someone made him ascend', size=38, y=230)),
        "Was raised: someone made him ascend.",
        A("was invited = someone asked him to arrive appears", P('was invited = someone asked him to arrive', size=38, y=300)),
        "Was invited: someone asked him to come.",
        "Now put each one back on the pair.",
        "Was lowered: someone made him descend. Fits.",
        "Was lowered: someone asked him to descend? No — he didn't choose to come down. It was done to him.",
        D("Cross out choice 2"),
        D("Circle choice 1"),
        "Choice 1.",
     ])], T40, q=Q)

# ------------------------------------------------------------------ lesson 4 · common relations (Hebrew 425–503)
SB4 = ['Relations that repeat', 'Hard words, easy link', 'Taking out of', 'Wrap-up']
L4 = lesson('vr40-common', 'Common Relations', SB4, [
    dict(mode='title', title='Common Relations', script=[
        "Analogies — common relations.",
        "We've solved quite a few questions by now and defined all kinds of relations.",
    ]),
    dict(mode='concept', active=0, title='Relations that repeat', script=[
        A("Some relations come back again and again appears", W('Some relations come back again and again in the exam', 140)),
        "In the exam, some relations repeat themselves every now and then.",
        "In this lesson we'll meet a few of them. Knowing them in advance helps you recognise them in the exam — and phrase the sentence more easily.",
    ]),
    dict(mode='concept', active=1, title='Hard words, easy link', script=[
        A("High vocabulary → often a simple relation appears", W('Hard vocabulary → the relation is often very simple', 140)),
        "Some analogies have high-level vocabulary. There, the difficulty isn't phrasing the relation — it's knowing the words.",
        A("…usually synonyms or opposites appears", W('…very often synonyms or opposites', 230)),
        "In a good share of those analogies, the relation is very simple — very often synonyms or opposites. Worth knowing.",
    ]),
    dict(mode='concept', active=2, title='Taking out of', script=[
        A("\"to take something out of\" appears", W('A common relation:  "to take something out of…"', 140)),
        "Another common relation: to take something out of something.",
        A("to milk · to tap · to shell · to pit · to weed · to skim appears",
          W('to milk (a cow) · to tap (a tree) · to shell (peas) · to pit (a cherry) · to weed (a garden) · to skim (milk)', 230, size=34)),
        "It comes back in all kinds of words: to milk — take milk out of a cow. To tap — take sap out of a tree.",
        "To shell peas, to pit a cherry, to weed a garden, to skim the cream off milk. Many words — one relation.",
    ]),
    dict(mode='concept', active=3, title='Wrap-up', script=[
        "Let's see these on two questions — and then that's all of analogies.",
    ]),
], T40)

SBQ4 = ['Q1', 'Q2']
G4 = 'Common Relations'
Q10 = guided(0, 'vr40-g017', G4, SBQ4,
    ["A sample question — position 3, medium level."],
    [('Know the words', [
        "Miser and skinflint. What's a skinflint? A skinflint is a miser — someone who hates spending money.",
        A("skinflint = miser (synonyms) appears", P('skinflint = miser  (same meaning)', size=44, y=230)),
        "Let's check the answers.",
        "Novice and beginner: a novice is a beginner. Same meaning. It fits.",
        D("Put a question mark next to choice 1"),
        "Patron and artist: a patron supports an artist. Not the same meaning.",
        D("Cross out choice 2"),
        "Judge and verdict: a judge gives a verdict. No.",
        D("Cross out choice 3"),
        "Rival and ally: opposites. No.",
        D("Cross out choice 4"),
        D("Circle choice 1"),
        "Choice 1.",
     ]),
     ('High vocabulary', [
        "Here we saw an analogy with high vocabulary.",
        "Until now our difficulty was mainly phrasing the relation. Here the difficulty was knowing the words.",
        A("Hard words → often synonyms or opposites appears", P('Hard words → often synonyms or opposites', size=40, y=230)),
        "In a good share of high-vocabulary analogies, the relation is very simple — often synonyms or opposites. Important to know.",
     ])], T40, q=Q)

Q11 = guided(1, 'vr40-g018', G4, SBQ4,
    ["Another example — position 6, hard."],
    [('Build the sentence', [
        "Sap and to tap. What is to tap? To tap a tree is to draw sap out of it.",
        A("to tap = to take sap out of something appears", P('to tap = to take sap out of something', size=42, y=230)),
        "Notice — a tree is something specific. I keep it general: to take sap out of something.",
     ]),
     ('Check every answer', [
        "Water and to freeze: is to freeze to take water out of something? No — freezing turns water into ice.",
        D("Cross out choice 1"),
        "Milk and to milk: is to milk to take milk out of something? Yes — out of a cow, a goat. It fits. Keep checking.",
        D("Put a question mark next to choice 2"),
        "Flour and to bake: is to bake to take flour out of something? No — baking makes bread from flour.",
        D("Cross out choice 3"),
        "Wood and to carve: is to carve to take wood out of something? No — carving shapes the wood.",
        D("Cross out choice 4"),
        "Three eliminated. We mark what's left.",
        D("Circle choice 2"),
        "Choice 2.",
     ]),
     ('Wrap-up', [
        "What we saw here is the nuance of taking out of: to tap takes out, to milk takes out.",
        "This relation repeats itself quite a lot in the exam, in all kinds of different words.",
        "So, in this lesson we went over common relations. Knowing them in advance will help you spot them faster in the exam.",
        "And with that, we've finished analogies.",
        A("Precise sentence → sharpen → through the answers appears", P('Precise sentence → sharpen it → or work through the answers', size=38, y=330)),
        "The most important thing: build the most precise relation you can. If you can't, try to sharpen it — or work psychometrically through the answers.",
        "That's it for analogies. Go practise!",
     ])], T40, q=Q)

MODULES = [L1, Q1, L2, Q2, Q3, Q4, Q5, Q6, L3, Q7, Q8, Q9, L4, Q10, Q11]

MEMORY = [
    dict(id='mem-analogy-relations', after='solve-vr40-g018', title='Analogy relations to recognise',
         intro='Build one precise sentence, keep the word order, and test it on all four choices.',
         tables=[dict(title='Relations from the lessons', head=['Relation', 'Pair', 'Matching pair'], rows=[
             ['top part of', 'crest : wave', 'summit : mountain'],
             ['carry out the action named by', 'to inspect : inspection', 'to select : selection'],
             ['make something the opposite of', 'to straighten : bent', 'to dry : wet'],
             ['a very weak form of', 'trickle : flow', 'glimmer : light'],
             ['put something into', 'to immerse : liquid', 'to bury : earth'],
             ['give something to someone else', 'equipment : to equip', 'weapons : to arm'],
             ['helps very little against', 'famine : small food parcel', 'drought : brief shower'],
             ['the opening of / in', 'mouth : cave', 'eye : needle'],
             ['was made to do (not by choice)', 'was lowered : descended', 'was raised : ascended'],
             ['same meaning', 'miser : skinflint', 'novice : beginner'],
             ['take something out of', 'sap : to tap', 'milk : to milk'],
         ])],
         tips=['Check all four choices — eliminate three.',
               'Started from the second word? Check the choices from the second word too.',
               'Two choices fit? Sharpen the sentence, or build a fresh sentence for each choice.',
               'Hard vocabulary usually hides a simple relation: synonyms or opposites.']),
]
