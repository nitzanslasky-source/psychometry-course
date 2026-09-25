# Verbal · Topic 44 · Understanding paragraphs.
# Hebrew hebverbal.txt 2274-2772 decides the concepts, structure, order, methods, tips and verdicts.
# Every question is an English bank item, quoted word for word (never a translated Hebrew example).
from dsl import *

T44 = 44
SBL = ['Where they appear', 'Two kinds', 'Kind 1: it says so', 'Kind 2: understand it']
GQ = 'Paragraph Questions'
SBQ = ['Kind 1 · NOT', 'Kind 1 · hard text', 'Kind 2 · NOT implied', 'Concept in passage', 'Apply the idea']

MODULES = [
# ------------------------------------------------------------------ lesson (Hebrew 2274-2290)
lesson('vr44-paragraphs', 'Understanding Paragraphs', SBL, [
 dict(mode='title', title='Understanding Paragraphs', script=[
  "Understanding paragraphs.",
  "The most common question type in the whole understanding-and-inference part of the verbal section.",
  "Let's see what they are — and how to split them.",
 ]),
 dict(mode='concept', active=0, title='Where they appear', script=[
  A("Paragraph questions: in the understanding-and-inference part", T('Paragraph questions — inside the understanding-and-inference part of Verbal Reasoning', size=40, x=410, y=110, w=1140)),
  "These questions sit inside the understanding-and-inference part of the verbal section.",
  A("The most common type there", T('The most common question type in that part', size=40, x=410, y=260, w=1140)),
  "And they're the most common type there. So we'd better get them right.",
 ]),
 dict(mode='concept', active=1, title='Two kinds', script=[
  "Broadly, we split them into two kinds.",
  A("Kind 1: it says so in the passage", T('Kind 1 — What does the passage say? (true / not true according to it)', size=40, x=410, y=110, w=1140)),
  "Kind one: you get a paragraph, and they ask what's true — or not true — according to what's written.",
  A("Kind 2: what's behind the words", T('Kind 2 — What lies behind the words? (implied, meant, the idea)', size=40, x=410, y=260, w=1140)),
  "Kind two: a paragraph where you have to understand what stands behind what's written. What's implied, what's meant.",
 ]),
 dict(mode='concept', active=2, title='Kind 1: it says so', script=[
  A("Kind 1: read and check — don't over-think", T('Kind 1: read, then check each choice against the text. No need to over-think.', size=40, x=410, y=110, w=1140)),
  "Kind one: I don't need to think too much. Just read and check — which choice appears in the paragraph, and which doesn't.",
  A("Usually the easier ones", T('Usually the easier questions of this topic', size=40, x=410, y=260, w=1140)),
  "These are usually the easier questions in this topic.",
 ]),
 dict(mode='concept', active=3, title='Kind 2: understand it', script=[
  A("Kind 2: understand what's implied / meant", T('Kind 2: understand what is implied — what the writer means', size=40, x=410, y=110, w=1140)),
  "Kind two: I have to understand what's implied, what the words are getting at.",
  A("These can be hard", T('These can be far from easy', size=40, x=410, y=260, w=1140)),
  "And these can be not easy at all.",
  "Let's start with a sample question.",
 ]),
], T44),

# ------------------------------------------------------------------ Q · Kind 1, "NOT" (Hebrew 2291-2347, easy-plus)
guided(0, 'vb-inf_v2_0077', GQ, SBQ, ["A sample question — easy-plus."], [
 ('Kind 1: find it in the text', [
  "Auroras. Let's read.",
  "\"According to the passage, which of the following statements about the Earth is NOT correct?\"",
  D("Underline 'According to the passage' and circle 'NOT'"),
  "Notice what they ask: according to the passage — what is NOT correct.",
  A("According to the passage → the answer is in the text appears", P("According to the passage → the answer is in the text", y=120)),
  "That means the answer is in the text. I just go through the choices and check each one against what's written.",
  "No inference needed here. This is kind one.",
 ]),
 ('Check each choice', [
  "Choice one: \"Its auroras are weak in comparison with Jupiter's.\"",
  D("Underline 'Unlike the auroras that appear above the Earth, Jupiter's auroras are very strong'"),
  "Where's that? \"Unlike the auroras that appear above the Earth, Jupiter's auroras are very strong.\" So the Earth's are weaker. That's correct — and they asked for NOT correct. Cross it out.",
  D("Cross out choice 1"),
  "Choice two: \"High-energy particles are able to penetrate its atmosphere.\"",
  "Auroras form when particles penetrate a planet's atmosphere — and the Earth has auroras. Correct. Out.",
  D("Cross out choice 2"),
  "Choice three: \"Its magnetic field is stronger than Jupiter's.\"",
  D("Underline 'Jupiter's powerful magnetic field'"),
  "The passage calls Jupiter's field the powerful one — that's why its auroras never disappear. So this is NOT correct.",
  A("NOT correct → that's our answer appears", P("NOT correct → that's our answer", y=120)),
  D("Circle choice 3"),
  "Choice 3.",
  "In the exam — mark it and move on. Here in the lesson, let's check the last one too.",
  "Choice four: \"Its auroras do not appear without interruption.\" Jupiter's never disappear — unlike the Earth's. Correct. Out.",
  D("Cross out choice 4"),
 ]),
], T44),

# ------------------------------------------------------------------ Q · Kind 1, hard text (Hebrew 2348-2464, hard)
guided(1, 'vb-inf_v2_0017', GQ, SBQ, ["A sample question — a hard one."], [
 ('Hard text — answer in the text', [
  "\"Which of the following claims is correct according to the passage?\"",
  D("Underline 'correct according to the passage'"),
  "What are they asking? What's correct according to the passage. So again — the answer appears in the passage.",
  A("Hard passage — but the answer is IN the text appears", P("Hard passage — but the answer is IN the text", y=120)),
  "No big inference. But the passage is hard. We need to read — slowly — and understand it.",
 ]),
 ('Say it in your own words', [
  "Let's put some order into this long, complex text.",
  D("Bracket 'One school holds…' and write 'School 1'"),
  "School one: Arben says the purpose of man is the perfection of the intellect — but man can never fully attain it.",
  D("Bracket 'According to the other school…' and write 'School 2'"),
  "School two: the purpose can't be attained — but man is obliged to strive toward it anyway.",
  A("the former · the latter · the other one → go back: who is it? appears", P("the former · the latter · the other one → go back: who is it?", y=120)),
  "When a text points back — the former, the latter, the other school — stop and pin down exactly who it means.",
  A("Both: can't be attained · They differ: what follows from that appears", P("Both: can't be attained · They differ: what follows from that", y=200)),
  "So: both schools agree it can't be attained. They differ on what follows — strive or not.",
 ]),
 ('Check the choices', [
  "Choice one: \"Scholars of both schools agree that, according to Arben, man cannot fully attain the purpose of his life.\"",
  "School one — can never fully attain. School two — cannot be attained. Both. That's exactly what's written.",
  D("Circle choice 1"),
  "Choice 1.",
  "In the exam we mark and move on. In the lesson, the others:",
  "Choice two says they disagree about what the purpose is. No — both sides describe the same purpose. Out.",
  D("Cross out choice 2"),
  "Choice three — what full attainment would consist in. Not what they argue about. Out.",
  D("Cross out choice 3"),
  "Choice four — whether the intellect can get man there. Both say it can't. No disagreement. Out.",
  D("Cross out choice 4"),
  "A kind-one question — and not an easy one at all.",
 ]),
], T44),

# ------------------------------------------------------------------ Q · Kind 2, NOT implied (Hebrew 2465-2553, medium)
guided(2, 'vb-inf_v2_0085', GQ, SBQ, ["A sample question — medium level."], [
 ('Kind 2: what is NOT implied', [
  "\"Which of the following is NOT implied by the passage?\"",
  D("Underline 'NOT implied'"),
  "This is no longer 'what appears in the passage'. We need to understand what's implied — or not implied.",
  "That takes us to kind two.",
 ]),
 ('Kind 2 — many wordings', [
  "The wordings of kind two are very varied. Here's a partial list:",
  A("Main idea · central claim · best summary · best title appears", P("Main idea · central claim · best summary · best title", y=210)),
  "What's the main idea, the central claim, what best summarizes the passage, what title fits it.",
  A("Implied / NOT implied · purpose · author's position appears", P("Implied / NOT implied · purpose · author's position", y=300)),
  "What's implied — or not implied. The purpose of the passage. The author's position.",
  A("Completion · rephrasing · a concept in the passage appears", P("Completion · rephrasing · a concept in the passage", y=390)),
  "Completion — a missing part, and what could fit. Rephrasing — which idea is most similar. And a question about one concept from the passage.",
  "Ours is 'NOT implied'. Let's go through the choices.",
 ], dict(pre=[T('Kind 2 — the wording varies a lot', size=48, x=410, y=100, w=1140)])),
 ('Check each choice', [
  "Choice one: \"Objects from ancient graves can help archaeologists to learn about the social structure of ancient societies.\"",
  D("Underline 'the unusual objects found in the grave show that … had established a social hierarchy'"),
  "The archaeologists learned about a social hierarchy from objects in a grave. Implied. Out.",
  D("Cross out choice 1"),
  "Choice two: \"According to Grosman and Munro's findings, farming societies already existed in the Lower Galilee twelve thousand years ago.\"",
  D("Underline 'farming societies — which appeared in the region two thousand years later'"),
  "Wait. Farming societies appeared two thousand years LATER. The finding is that hunter-gatherers had a hierarchy like farmers — not that farmers were there. Not implied.",
  D("Circle choice 2"),
  "Choice 2.",
  "In the exam — move on. In the lesson, the rest:",
  "Choice three: the discovery 'aroused great interest', and the hierarchy is usually associated only with later societies — so they didn't expect it. Implied. Out.",
  D("Cross out choice 3"),
  "Choice four: the grave belonged to the hunter-gatherer society that lived in the region. Implied. Out.",
  D("Cross out choice 4"),
 ]),
], T44),

# ------------------------------------------------------------------ Q · concept in the passage (Hebrew 2554-2667, medium-plus)
guided(3, 'vb-inf_v2_0031', GQ, SBQ, ["A sample question — medium-plus."], [
 ('Read slowly — once', [
  "A question about a concept from the passage: \"Why is Dr. Zeidel called 'the driver's advocate'?\"",
  D("Circle 'the driver's advocate'"),
  "To answer it, we have to understand the passage. Which brings me to a very important point.",
  A("Don't skim → run to the choices → run back to the text appears", P("Don't skim → run to the choices → run back to the text", y=120)),
  "These questions have a lot of text. Many students skim, run to the choices — and for every choice run back to the text, and back, and back. Wrong approach. A waste of time.",
  A("Read slowly the first time — understand, then go to the choices appears", P("Read slowly the first time — understand, then go to the choices", y=200)),
  "Read slowly, the first time, and understand as much as you can. Then, when you reach the right answer — you'll know it right away.",
  "Torn between two? Then go back to the text to decide. Not for every choice.",
 ]),
 ('What does he actually claim?', [
  "So instead of going through the choices — let's understand the passage.",
  D("Underline 'right — but only in part'"),
  "People say the human factor causes most accidents. He says: right — but only in part.",
  D("Bracket 'The city planner, the engineer…, the driving instructor, the official'"),
  "Why? The planner, the engineer, the instructor, the official — they're human too. Almost every accident starts with a failure of one of them.",
  A("Human factor ≠ just the driver → he defends the driver appears", P("Human factor ≠ just the driver → he defends the driver", y=120)),
  "The driver just copes with all their failures at once. So he widens 'the human factor' — and takes the blame off the driver. That's why he's the driver's advocate.",
 ]),
 ('Now the choices', [
  "Choice one: \"Because he argues that although most accidents stem from the human factor, most of the blame does not fall on the driver.\"",
  "Exactly what we understood.",
  D("Circle choice 1"),
  "Choice 1.",
  "In the exam — mark and move on. In the lesson:",
  "Choice two blames the engineers only — and speaks of statistics. He names many people, not just engineers. Out.",
  D("Cross out choice 2"),
  "Choice three — a few reckless drivers. Not in the passage at all. Out.",
  D("Cross out choice 3"),
  "Choice four — the driver alone is responsible. The opposite of his claim. Out.",
  D("Cross out choice 4"),
  "Not a simple question — but we got through it.",
 ]),
], T44),

# ------------------------------------------------------------------ Q · apply the idea (Hebrew 2668-2770, medium-plus, even hard)
guided(4, 'vb-inf_v2_0059', GQ, SBQ, ["A sample question — medium-plus, even hard.",
                                       "Before we read — remember what we learned: read slowly, and understand."], [
 ('Read, understand', [
  "Let's apply it.",
  D("Underline 'undergo a process of evolution and specification'"),
  "Folk customs undergo \"a process of evolution and specification\". Not sure I understand yet. Keep reading.",
  D("Underline 'each custom becomes more defined, takes on more shades and variants, and acquires a unique character in each community'"),
  "Each custom becomes more defined, gets more variants, and a unique character in each community. Now it's getting clearer.",
  A("Custom → more defined, more variants, unique to each community appears", P("Custom → more defined, more variants, unique to each community", y=120)),
  "In the end the custom marks identity — it distinguishes one community from another.",
 ]),
 ('Apply — one step further', [
  "\"Which of the following processes is most suited to exemplify Dr. Lavon's claim?\"",
  A("Application: read → understand → apply to a new case appears", P("Application: read → understand → apply to a new case", y=120)),
  "This is an application question. Another kind of understanding — one step further. You read, you understood — now can you apply it?",
  "Choice one: leaders instilled the celebration of a minor festival. That's adoption of a custom — not a custom splitting into community variants. Out.",
  D("Cross out choice 1"),
  "Choice two: several versions became one uniform version. That's the reverse — convergence. Out.",
  D("Cross out choice 2"),
  "Choice three: \"In our day every community insists on customs of its own for lighting the festival lamps, although at first there were no precise instructions in the matter.\"",
  "Every community — its own custom. It got more defined over time. That's specification.",
  D("Circle choice 3"),
  "Choice 3.",
  "In the exam, move on. In the lesson — choice four: a custom that is little practiced today. That's decline, not specification. Out.",
  D("Cross out choice 4"),
  "And we're done with this one.",
 ]),
], T44),
]

MEMORY = [
 dict(id='mem-paragraph-types', after='solve-vb-inf_v2_0059', title='Paragraph questions — know the kind',
  intro='First decide which kind of question it is — that tells you how to work.',
  tables=[dict(head=['Kind', 'Typical wording', 'How to work'], rows=[
   ['1 · It says so', 'According to the passage… · Which is (NOT) correct… · NOT given in the passage', 'The answer is in the text: check each choice against what is written'],
   ['2 · Understand it', 'Main idea / central claim · best summary / title · implied / NOT implied', 'Understand the paragraph first, then choose'],
   ['2 · Understand it', "Purpose · author's position · completion · rephrasing · a concept in the passage", 'Understand the paragraph first, then choose'],
   ['2 · Apply it', 'Which example / case best illustrates…', 'Understand the idea, then apply it to the new case'],
  ])],
  tips=['Read slowly the first time and understand — do not bounce between the choices and the text.',
        'Back to the text only when you are torn between two choices.',
        'Pointer words (the former, the latter, the other one): stop and pin down exactly who is meant.',
        'In the exam: mark the answer and move on.']),
]
