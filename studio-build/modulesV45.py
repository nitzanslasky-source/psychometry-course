# Verbal · Topic 45 · Parables and comparisons.
# Hebrew hebverbal.txt 2773-3144 decides the concepts, structure, order, methods, tips and verdicts.
# Every guided question is an ORIGINAL course question (content/verbal_originals_B.json), quoted word for word;
# each mirrors the type, trap and difficulty of one real NITE question (field "mirrors").
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
  A("Parable: a conversation – one side uses a short parable to pass a message", T('Parable questions: a conversation between two or more people – one of them uses a short parable to get a message across', size=40, x=410, y=110, w=1140)),
  "Parable questions: there's a conversation between two or more people, and one of them uses a short parable to get a message across to the other side.",
 ]),
 dict(mode='concept', active=2, title='Comparisons', script=[
  A("Comparison: compare ideas and situations", T('Comparison questions test how well you compare different ideas and situations', size=40, x=410, y=110, w=1140)),
  "Comparison questions test our ability to compare different ideas and situations.",
  "Let's start with an example.",
 ]),
], T45),

# ------------------------------------------------------------------ Q · comparison: explain it the same way (Hebrew 2781-2833, medium)
guided(0, 'vo-45-001', GQ, SBQ, ["A sample question – medium level."], [
 ('Take the logic – apply it', [
  "\"Which of the following examples could best replace the example at the end of the paragraph?\"",
  "This is a comparison question. There's a claim, with an example that shows its logic.",
  pop("Understand the logic → project it onto the choices", 120),
  "We take that claim, understand it, and project it onto the choices. We're looking for a choice that works the same way.",
  D("Underline 'whose novelty was expressed in the name they were given'"),
  "In many fields, a new invention got its name from the thing it replaced.",
  D("Underline 'the radio, for example, was at first known as \"the wireless telegraph.\"'"),
  pop("New device = the old device it replaced − its defining element", 200),
  "The radio: the telegraph it replaced, minus the wire, the thing that defined the telegraph.",
 ]),
 ('Keep two – then compare exactly', [
  "Choice one: \"Calling the electric refrigerator 'an icebox without ice'.\"",
  "Sounds reasonable. Keep it and come back.",
  "Choice two: \"Calling a mechanical calculator 'a clerk without a pencil'.\"",
  "Also sounds good. But a clerk is a person, and the paragraph says that's the other kind: measuring against a living model. Leave it aside for now.",
  "Choice three: \"Calling a submarine 'an iron fish'.\" A fish is a living creature, not an earlier device the submarine replaced. That's the living-model side again. Out.",
  D("Cross out choice 3"),
  "Choice four: \"Calling a wind-up watch 'a watch without a battery'.\" That's backwards: it names the old watch after what the new one has. Out.",
  D("Cross out choice 4"),
  "Two left. Which one works exactly like the radio?",
  "The refrigerator replaced the icebox, an earlier device, minus the ice that defined it. Exactly the wireless telegraph.",
  "The clerk is a person. That's the human model the paragraph contrasts with.",
  D("Cross out choice 2"),
  D("Circle choice 1"),
  "Choice 1.",
 ]),
], T45),

# ------------------------------------------------------------------ Q · comparison: a similar situation (Hebrew 2834-2902, easy-plus)
guided(1, 'vo-45-002', GQ, SBQ, ["A sample question – easy-plus."], [
 ('Break the case into parts', [
  "\"Which of the following cases is most similar to the case described?\"",
  "Again a comparison question: comparing situations.",
  D("Bracket 'guests would be charged a fee for every hour they stayed beyond noon'"),
  "The hotel: a fee meant to stop guests from checking out late.",
  D("Bracket 'the number of guests who checked out late rose sharply'"),
  "And the result, to the manager's surprise, is the opposite: more late check-outs. The fee became a price worth paying.",
  pop("A charge meant to deter → becomes a price → more of it", 120),
  "So the pattern: a charge that's meant to deter turns into a price, and you get more of the behavior.",
 ]),
 ('Match part by part', [
  "Now match each choice part by part.",
  "Choice one: the baker raised his price and sold just as many loaves. There was no charge meant to stop anything. Doesn't match. Out.",
  D("Cross out choice 1"),
  "Choice two: readers moved to a new travel magazine. No deterrent at all. Out.",
  D("Cross out choice 2"),
  "Choice three: \"to reduce such visits, the city began charging these visitors a high surcharge; to its surprise, the number of visitors arriving without a booking rose.\"",
  "A charge meant to cut visits without a booking, and more of them came. Part by part, the same case.",
  D("Circle choice 3"),
  "Choice 3.",
  "In the exam, move on. In the lesson, choice four: an extra day off, and output grew. A reward, not a deterrent. Out.",
  D("Cross out choice 4"),
 ]),
], T45),

# ------------------------------------------------------------------ Q · parable: what does she mean – cause and effect (Hebrew 2903-2937, easy)
guided(2, 'vo-45-003', GQ, SBQ, ["A sample question – an easy one."], [
 ('What does the parable mean?', [
  "\"What does Tami mean?\" A parable question.",
  "We said: in parables there's a conversation, and someone uses a parable to make a point to the other side. Let's understand what she means.",
  D("Underline 'opening umbrellas is what makes it rain'"),
  "Opening umbrellas makes it rain? Everyone knows it's the other way round: it rains, and then people open their umbrellas.",
  pop("She says: you've swapped cause and effect", 120),
  "So she's saying to Noga: you've swapped cause and effect.",
 ]),
 ('Chicken and egg', [
  D("Underline 'she gives up on him each time his grades drop'"),
  "Noga says: his grades drop → so the tutor stops coming.",
  "Tami says: it's the reverse. The tutor stops coming → so his grades drop.",
  pop("Chicken and egg: which came first? – a very common nuance", 120),
  "This chicken-and-egg nuance comes up a lot, in parables and in other understanding-and-inference questions. Be aware of it, and look for it.",
  "Choice three: \"Eitan's grades fall because his tutor stops coming to see him.\"",
  D("Circle choice 3"),
  "Choice 3.",
  "Choice two adds a motive nobody mentioned; choice one adds a 'what if'; choice four adds a moral judgment. Out.",
  D("Cross out choices 1, 2 and 4"),
 ]),
], T45),

# ------------------------------------------------------------------ Q · parable: complete it (Hebrew 2938-3006, medium)
guided(3, 'vo-45-004', GQ, SBQ, ["A sample question – medium level."], [
 ('Understand the meaning – twice', [
  "\"Which of the following best completes Dana's words?\"",
  pop("Understand twice: the words – and each parable in the choices", 120),
  "Here we need to understand the meaning twice: what's being said, and what each parable in the choices means, to see which one matches.",
  D("Underline 'shouting at people never gets anything done'"),
  "Ofer: I was told you shouted at the intern! Shouting never gets anything done!",
  D("Circle 'raising his voice so loudly that the whole office could hear him'"),
  "Wait. How does Ofer say it? At the top of his voice. He shouts, to tell her not to shout.",
  pop("His act undermines his own message", 200),
  "His words undermine themselves.",
 ]),
 ('Which parable means the same?', [
  "Choice one: refusing to lend your neighbor a ladder because he once refused you. That's paying back. Not our meaning. Out.",
  D("Cross out choice 1"),
  "Choice two: \"writing a long, rambling letter to a newspaper to complain that people no longer express themselves briefly\".",
  "A long, rambling letter, to demand that people be brief. The act undermines the message. Exactly Ofer.",
  D("Circle choice 2"),
  "Choice 2.",
  "In the exam, move on. In the lesson, the others:",
  "Choice three: watering the garden in a rainstorm. Pointless, but it doesn't undermine a message. Out.",
  D("Cross out choice 3"),
  "Choice four: complaining that a pickpocket took advantage of your carelessness. That's shifting the blame. It sounds ironic, but it's not a message that undermines itself. Out.",
  D("Cross out choice 4"),
 ]),
], T45),

# ------------------------------------------------------------------ Q · parable: the context (Hebrew 3007-3074, easy)
guided(4, 'vo-45-005', GQ, SBQ, ["A sample question – an easy one."], [
 ('A parable answers something', [
  "\"Which of the following is most likely to be what Maya said?\"",
  pop("A parable responds to something said, done or planned", 120),
  "When someone uses a parable, it's in response to something: something the other person said, did, or plans to do. Here they ask: what was the background?",
  "To find the background, first understand what the parable means.",
  D("Underline 'decides how good a restaurant's food is by looking at the shape of its plates'"),
  "Judging the food by the shape of the plates? The food is what matters. The plates are beside the point.",
  pop("Judging the main thing by something beside the point", 200),
 ]),
 ('Find the parallel', [
  "So Maya judged something by a detail that doesn't matter. Which choice does that?",
  "Choices one, two and three each judge the thing itself: the comfort of the shoes, the acting, the taste of the coffee. Out.",
  D("Cross out choices 1, 2 and 3"),
  "Choice four: \"Attorney Amir must be an outstanding lawyer – his office is in the most luxurious tower in the city.\"",
  "An outstanding lawyer, because of the building his office is in. The tower is the plates.",
  D("Circle choice 4"),
  "Choice 4.",
  pop("Often the parable says: that was a bit silly – politely", 120),
  "By the way, a nuance that keeps coming back: very often the parable is a polite way of saying 'what you just said is a bit silly'. Nicely worded, but that's the message.",
 ]),
], T45),

# ------------------------------------------------------------------ Q · parable: what is compared to what (Hebrew 3075-3143, medium)
guided(5, 'vo-45-006', GQ, SBQ, ["A sample question – medium level."], [
 ('Map the parable', [
  "\"In his reply, Boaz compares -\"",
  "Here we get the background and the parable, and they ask what is compared to what. That's the third kind of parable question.",
  D("Underline 'swimming across a river while there is a bridge just a few steps away'"),
  "Swimming across a river, the hard way, when there's a bridge right there: the easy way to the very same bank.",
  D("Draw arrows: 'swimming across' → ordering from overseas · 'the bridge' → the copy in the city library"),
  pop("Hard way (swimming across) = ordering the book from overseas", 120),
  pop("The bridge = the copy in the city library", 190),
  "The hard way is ordering from overseas and waiting two months. The bridge is the library copy, sitting on the shelf.",
 ]),
 ('Check the pairs', [
  "Choice one: \"the copy in the city library to the bridge\". The easy way across. Yes.",
  D("Circle choice 1"),
  "Choice 1.",
  "In the exam we move on. In the lesson, the others:",
  "Choice two: ordering the book to the river. No, ordering is the swimming, not the river. Out.",
  D("Cross out choice 2"),
  "Choice three: the cookbook to the bridge. The book is what you want to reach, on the other side. Out.",
  D("Cross out choice 3"),
  "Choice four: the copy from overseas to the swimming. That copy is the goal, not the effort. Out.",
  D("Cross out choice 4"),
 ]),
], T45),
]

MEMORY = [
 dict(id='mem-parables', after='solve-vo-45-006', title='Parables and comparisons: what they ask',
  intro='Name the question type, then work the way that type needs.',
  tables=[dict(head=['Question type', 'Typical wording', 'How to work'], rows=[
   ['Comparison · explain / example', 'Which example could replace… · explain in a similar way', 'Take the exact logic of the example; keep two, then compare precisely'],
   ['Comparison · situation', 'Which case is most similar…', 'Break the case into parts; match part by part'],
   ['Parable · meaning', 'What does X mean? · What does X think?', 'Understand the parable, then translate it back to the conversation'],
   ['Parable · completion', 'Which best completes X\'s words?', 'Understand twice: the words, and every parable in the choices'],
   ['Parable · context', 'What did X say / what was the context?', 'A parable answers something said, done or planned'],
   ['Parable · mapping', 'In their reply, X compares ___ to -', 'Map each element of the parable to the real case'],
  ])],
  tips=['Chicken and egg: check whether someone swapped cause and effect.',
        'A parable is often a polite way of saying "that was a bit silly".',
        'A true or sensible-sounding choice is not enough: it has to work the same way.']),
]
