# Verbal · Topic 45 · Parables and comparisons.
# Hebrew hebverbal.txt 2773-3144 decides the concepts, structure, order, methods, tips and verdicts.
# Every question is an English bank item, quoted word for word (never a translated Hebrew example).
from dsl import *

T45 = 45
SBL = ['Two question types', 'Parables', 'Comparisons']
GQ = 'Parable & Comparison Qs'
SBQ = ['Explain it similarly', 'A similar situation', 'What does she mean?', 'Complete the parable', 'The context', 'What is likened?']

def pop(text, y): return A(text + ' appears', P(text, y=y))

MODULES = [
# ------------------------------------------------------------------ lesson (Hebrew 2773-2780)
lesson('vr45-parables', 'Parables and Comparisons', SBL, [
 dict(mode='title', title='Parables and Comparisons', script=[
  "Parables and comparisons.",
  "Another question type in the understanding-and-inference part of the verbal section.",
 ]),
 dict(mode='concept', active=0, title='Two question types', script=[
  A("Two types: parables · comparisons", T('Two types: parables and comparisons', size=48, x=410, y=110, w=1140)),
  "Two types live here: parables, and comparisons.",
 ]),
 dict(mode='concept', active=1, title='Parables', script=[
  A("Parable: a conversation — one side uses a short parable to pass a message", T('Parable questions: a conversation between two or more people — one of them uses a short parable to get a message across', size=40, x=410, y=110, w=1140)),
  "Parable questions: there's a conversation between two or more people, and one of them uses a short parable to get a message across to the other side.",
 ]),
 dict(mode='concept', active=2, title='Comparisons', script=[
  A("Comparison: compare ideas and situations", T('Comparison questions test how well you compare different ideas and situations', size=40, x=410, y=110, w=1140)),
  "Comparison questions test our ability to compare different ideas and situations.",
  "Let's start with an example.",
 ]),
], T45),

# ------------------------------------------------------------------ Q · comparison: explain it the same way (Hebrew 2781-2833, medium)
guided(0, 'vb-inf_v2_0288', GQ, SBQ, ["A sample question — medium level."], [
 ('Take the logic — apply it', [
  "\"Which of the following examples could best replace the example at the end of the passage?\"",
  "This is a comparison question. There's a claim, with an example that shows its logic.",
  pop("Understand the logic → project it onto the choices", 120),
  "We take that claim, understand it — and project it onto the choices. We're looking for a choice that works the same way.",
  D("Underline 'whose novelty was long expressed in the name of the thing they replaced'"),
  "Most inventions were named after the thing they replaced.",
  D("Underline 'the electric light was for years \"the flameless lamp.\"'"),
  pop("New device = the old thing it replaced − its defining feature", 200),
  "The electric light: the lamp it replaced — minus the flame, the thing that defined that lamp.",
 ]),
 ('Keep two — then compare exactly', [
  "Choice one: \"Calling a washing machine 'a laundress without hands'.\"",
  "Sounds good. But a laundress is a person — and the passage says that's the OTHER kind: measuring against a human. It isn't the same logic. Leave it aside for now.",
  "Choice two: \"Calling an electric heater 'a hearth without a fire'.\"",
  "Also sounds reasonable. Keep it and come back.",
  "Choice three: \"Calling a recording of a symphony 'a concert without an orchestra'.\" A concert is an event, not an earlier device. Out.",
  D("Cross out choice 3"),
  "Choice four: \"Calling a digital camera 'a camera without a screen'.\" A digital camera HAS a screen — it removes a feature of the new device, not of the old one. Out.",
  D("Cross out choice 4"),
  "Two left. Which one works exactly like the lamp?",
  "The heater replaced the hearth — an earlier device — minus the fire that defined it. Exactly the flameless lamp.",
  "The laundress is a person — that's the human standard the passage contrasts with.",
  D("Cross out choice 1"),
  D("Circle choice 2"),
  "Choice 2.",
 ]),
], T45),

# ------------------------------------------------------------------ Q · comparison: a similar situation (Hebrew 2834-2902, easy-plus)
guided(1, 'vb-inf_v2_0316', GQ, SBQ, ["A sample question — easy-plus."], [
 ('Break the case into parts', [
  "\"Which of the following cases is most similar to the case described?\"",
  "Again a comparison question — comparing situations.",
  D("Bracket 'for every delay … the parents would pay an extra fee'"),
  "The kindergarten: a fee meant to stop parents coming late.",
  D("Bracket 'the number of latecomers grew markedly'"),
  "And the result — to her surprise — the opposite: more latecomers. The fee became a price worth paying.",
  pop("A charge meant to deter → becomes a price → MORE of it", 120),
  "So the pattern: a charge that's meant to deter turns into a price — and you get more of the behavior.",
 ]),
 ('Match part by part', [
  "Now match each choice part by part.",
  "Choice one: the greengrocer raised prices and sales didn't fall. There was no charge meant to deter anything. Doesn't match. Out.",
  D("Cross out choice 1"),
  "Choice two: subscribers moved to a new monthly. No deterrent at all. Out.",
  D("Cross out choice 2"),
  "Choice three: higher wages, and productivity rose. A reward, not a deterrent. Out.",
  D("Cross out choice 3"),
  "Choice four: \"to shorten the lines it decided to charge a high fee for the service; to its surprise, the number of people coming to file rose.\"",
  "A fee meant to cut the lines — and more people came. Part by part, the same case.",
  D("Circle choice 4"),
  "Choice 4.",
 ]),
], T45),

# ------------------------------------------------------------------ Q · parable: what does she mean — cause and effect (Hebrew 2903-2937, easy)
guided(2, 'vb-inf_v2_0303', GQ, SBQ, ["A sample question — an easy one."], [
 ('What does the parable mean?', [
  "\"What does Dafna mean?\" — a parable question.",
  "We said: in parables there's a conversation, and someone uses a parable to make a point to the other side. Let's understand what she means.",
  D("Underline 'the cock's crowing makes the sun rise'"),
  "The cock's crowing makes the sun rise? Everyone knows it's the other way round — the sun rises, and THEN the cock crows.",
  pop("She says: you've swapped cause and effect", 120),
  "So she's saying to Liora: you've swapped cause and effect.",
 ]),
 ('Chicken and egg', [
  D("Underline 'she leaves him every time he goes back to it'"),
  "Liora says: he drinks → so she leaves.",
  "Dafna says: it's the reverse — she leaves → so he drinks.",
  pop("Chicken and egg: which came first? — a very common nuance", 120),
  "This chicken-and-egg nuance comes up a lot — in parables and in other understanding-and-inference questions. Be aware of it, and look for it.",
  "Choice two: \"Giora slides back into drinking because his partner leaves him.\"",
  D("Circle choice 2"),
  "Choice 2.",
  "Choices three and four add motives nobody mentioned; choice one adds a 'what if'. Out.",
  D("Cross out choices 1, 3 and 4"),
 ]),
], T45),

# ------------------------------------------------------------------ Q · parable: complete it (Hebrew 2938-3006, medium)
guided(3, 'vb-inf_v2_0297', GQ, SBQ, ["A sample question — medium level."], [
 ('Understand the meaning — twice', [
  "\"Which of the following best completes Chaya's words?\"",
  pop("Understand twice: the words — and each parable in the choices", 120),
  "Here we need to understand the meaning twice: what's being said — and what each parable in the choices means — to see which one matches.",
  D("Underline 'rumors almost always have no basis'"),
  "Zohar: a rumor reached me that you skipped the party because of rumors. Rumors almost always have no basis!",
  D("Circle 'a rumor reached me'"),
  "Wait — how does Zohar know? A rumor reached him. He relies on a rumor — to tell her not to rely on rumors.",
  pop("His act undermines his own message", 200),
  "His words undermine themselves.",
 ]),
 ('Which parable means the same?', [
  "Choice one: cheating an opponent because he cheated you first. That's paying back. Not our meaning. Out.",
  D("Cross out choice 1"),
  "Choice two: phoning someone to ask for his phone number. Pointless — but it doesn't undermine a message. Out.",
  D("Cross out choice 2"),
  "Choice three: thanking a burglar. Gratitude in the wrong place. Out.",
  D("Cross out choice 3"),
  "Choice four: \"printing hundreds of copies of an appeal to save paper and handing them to passers-by\".",
  "Wasting paper — to tell people to save paper. The act undermines the message. Exactly Zohar.",
  D("Circle choice 4"),
  "Choice 4.",
 ]),
], T45),

# ------------------------------------------------------------------ Q · parable: the context (Hebrew 3007-3074, easy)
guided(4, 'vb-inf_v2_0322', GQ, SBQ, ["A sample question — an easy one."], [
 ('A parable answers something', [
  "\"Which of the following is most likely to be what Noa said?\"",
  pop("A parable responds to something said, done or planned", 120),
  "When someone uses a parable, it's in response to something — something the other person said, did, or plans to do. Here they ask: what was the background?",
  "To find the background, first understand what the parable means.",
  D("Underline 'enjoyment of a concert depends on the beauty of the grand piano'"),
  "Enjoying a concert because the piano looks nice? The music is what matters — the piano's looks are beside the point.",
  pop("Judging the main thing by something beside the point", 200),
 ]),
 ('Find the parallel', [
  "So Noa judged something by a detail that doesn't matter. Which choice does that?",
  "Choice one: \"Shimon is an excellent dentist — his clinic is large and spacious.\"",
  "An excellent dentist — because of the size of his clinic. The clinic is the piano.",
  D("Circle choice 1"),
  "Choice 1.",
  pop("Often the parable says: that was a bit silly — politely", 120),
  "By the way — a nuance that keeps coming back: very often the parable is a polite way of saying 'what you just said is a bit silly'. Nicely worded — but that's the message.",
  "In the exam we move on. In the lesson — choices two, three and four each judge the thing itself: the necklace she liked, the sculptures' taste, the level of teaching. Out.",
  D("Cross out choices 2, 3 and 4"),
 ]),
], T45),

# ------------------------------------------------------------------ Q · parable: what is likened to what (Hebrew 3075-3143, medium)
guided(5, 'vb-inf_v2_0331', GQ, SBQ, ["A sample question — medium level."], [
 ('Map the parable', [
  "\"In his words Kobalenz likened —\"",
  "Here we get the background and the parable — and they ask what is likened to what. That's the third kind of parable question.",
  D("Underline 'climbing a wall in order to reach a gate that stands wide open'"),
  "Climbing a wall — the hard way — to reach a gate that's wide open: the easy way to the very same place.",
  D("Draw arrows: 'climbing the wall' → journey to New York · 'open gate' → performance in your own city"),
  pop("Hard way (climb the wall) = travel to New York", 120),
  pop("Open gate = the band playing in his own city", 190),
  "The hard way is the trip to New York. The open gate is the band playing next month in his own city.",
 ]),
 ('Check the pairs', [
  "Choice one: the journey to the wall. No — the journey is the climbing, not the wall. Out.",
  D("Cross out choice 1"),
  "Choice two: the band to the gate. The band is what you want to reach — beyond the gate. Out.",
  D("Cross out choice 2"),
  "Choice three: \"the band's performance in Master's city to the open gate\". The easy way in. Yes.",
  D("Circle choice 3"),
  "Choice 3.",
  "In the exam we move on. Choice four: the New York performance to the climbing — the performance is the destination, not the climb. Out.",
  D("Cross out choice 4"),
 ]),
], T45),
]

MEMORY = [
 dict(id='mem-parables', after='solve-vb-inf_v2_0331', title='Parables and comparisons — what they ask',
  intro='Name the question type, then work the way that type needs.',
  tables=[dict(head=['Question type', 'Typical wording', 'How to work'], rows=[
   ['Comparison · explain / example', 'Which example could replace… · explain in a similar way', 'Take the exact logic of the example; keep two, then compare precisely'],
   ['Comparison · situation', 'Which case is most similar…', 'Break the case into parts; match part by part'],
   ['Parable · meaning', 'What does X mean? · What does X think?', 'Understand the parable, then translate it back to the conversation'],
   ['Parable · completion', 'Which best completes X\'s words?', 'Understand twice: the words, and every parable in the choices'],
   ['Parable · context', 'What did X say / what was the context?', 'A parable answers something said, done or planned'],
   ['Parable · mapping', 'X likened ___ to ___', 'Map each element of the parable to the real case'],
  ])],
  tips=['Chicken and egg: check whether someone swapped cause and effect.',
        'A parable is often a polite way of saying "that was a bit silly".',
        'A true or sensible-sounding choice is not enough — it has to work the SAME way.']),
]
