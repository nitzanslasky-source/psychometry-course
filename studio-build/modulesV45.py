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
  "\"Which of the following could replace the example of the radio in the paragraph?\"",
  "This is a comparison question. There's a claim, with an example that shows its logic.",
  pop("Understand the logic → project it onto the choices", 120),
  "We take that claim, understand it, and project it onto the choices. We're looking for a choice that works the same way.",
  D("Underline 'called at first by the name of the device that it replaced, together with the element that it lacks'"),
  "A new device is called at first by the name of the device it replaced, together with what it lacks.",
  D("Underline 'the radio, for example, was called at first \"the wireless telegraph.\"'"),
  pop("New device = the old device it replaced − its defining element", 200),
  "The radio: the telegraph it replaced, without the wire, the thing that defined the telegraph.",
 ]),
 ('Keep two – then compare exactly', [
  "Choice one: \"The first cars were called 'carriages without horses'.\"",
  "Sounds reasonable. Keep it and come back.",
  "Choice four: \"The first television sets were called 'radio with pictures'.\"",
  "Also sounds good: named after the radio, an earlier device. Leave it aside for now.",
  "Choice two: \"The first computers were called 'electronic brains'.\" A brain is an organ - that's the other kind of naming in the paragraph. Out.",
  D("Cross out choice 2"),
  "Choice three: \"The first airplanes were called 'flying machines'.\" Not named after any earlier device. Out.",
  D("Cross out choice 3"),
  "Two left. Which one works exactly like the radio?",
  "The car replaced the carriage, an earlier vehicle - without the horses that defined it. Exactly the wireless telegraph.",
  "The television: the radio with something added - pictures. The radio example is about what's missing, not what's added.",
  D("Cross out choice 4"),
  D("Circle choice 1"),
  "Choice 1.",
 ]),
], T45),

# ------------------------------------------------------------------ Q · comparison: a similar situation (Hebrew 2834-2902, easy-plus)
guided(1, 'vo-45-002', GQ, SBQ, ["A sample question – easy-plus."], [
 ('Break the case into parts', [
  "\"Which of the following cases is most similar to the case described?\"",
  "Again a comparison question: comparing situations.",
  D("Bracket 'a bonus … to each worker who had not been late to work even once during that month'"),
  "The factory: a bonus only for a whole month without being late.",
  D("Bracket 'a worker who had been late once at the beginning of a month tended to be late many more times'"),
  "And the result: once a worker is late one time, the bonus is lost for that month - so he stops trying, and is late again and again.",
  pop("All-or-nothing reward → one slip → nothing left to lose → gives up", 120),
  "So the pattern: a reward only for a clean record. After the first slip there's nothing left to lose, and the effort stops.",
 ]),
 ('Match part by part', [
  "Now match each choice part by part.",
  "Choice one: the bakery raised its price and sold as many loaves. No reward, no slip. Doesn't match. Out.",
  D("Cross out choice 1"),
  "Choice two: readers moved to another newspaper. No reward for a clean record at all. Out.",
  D("Cross out choice 2"),
  "Choice three: \"A library promised a free subscription to readers who returned all their books on time during a year. Readers who had once returned a book late no longer bothered to return their books on time.\"",
  "A reward only for a clean year, one late book, and then no more effort. Part by part, the same case.",
  D("Circle choice 3"),
  "Choice 3.",
  "Before marking - a quick look at choice four: an extra day off, and output grew. A reward for everyone, and it worked. Out.",
  D("Cross out choice 4"),
 ]),
], T45),

# ------------------------------------------------------------------ Q · parable: what does she mean – cause and effect (Hebrew 2903-2937, easy)
guided(2, 'vo-45-003', GQ, SBQ, ["A sample question – an easy one."], [
 ('What does the parable mean?', [
  "\"What does Keren mean?\" A parable question.",
  "We said: in parables there's a conversation, and someone uses a parable to make a point to the other side. Let's understand what she means.",
  D("Underline 'the crows bring the rain, since they always gather on his roof before a storm'"),
  "The crows bring the rain? It's the other way round: a storm is coming, and that's why the crows gather.",
  pop("She says: you've swapped cause and effect", 120),
  "So she's saying to Hila: you've swapped cause and effect.",
 ]),
 ('Chicken and egg', [
  D("Underline 'she gives up on him every time his grades go down'"),
  "Hila says: his grades go down → so the teacher stops coming.",
  "Keren says: it's the reverse. The teacher stops coming → so his grades go down.",
  pop("Chicken and egg: which came first? – a very common nuance", 120),
  "This chicken-and-egg nuance comes up a lot, in parables and in other understanding-and-inference questions. Be aware of it, and look for it.",
  "Choice three: \"Nadav's grades go down because his teacher stops coming to him.\"",
  D("Circle choice 3"),
  "Choice 3.",
  "Choice two adds a motive nobody mentioned; choice one adds a 'what if'; choice four adds a moral judgment. Out.",
  D("Cross out choices 1, 2 and 4"),
 ]),
], T45),

# ------------------------------------------------------------------ Q · parable: complete it (Hebrew 2938-3006, medium)
guided(3, 'vo-45-004', GQ, SBQ, ["A sample question – medium level."], [
 ('Understand the meaning – twice', [
  "\"Which of the following best completes Tzipi's words?\"",
  pop("Understand twice: the words – and each parable in the choices", 120),
  "Here we need to understand the meaning twice: what's being said, and what each parable in the choices means, to see which one matches.",
  D("Underline 'Shouting at people does not help at all'"),
  "Amnon: I was told you shouted at the new clerk! Shouting at people does not help at all!",
  D("Circle 'in a loud voice that was heard throughout the office'"),
  "Wait. How does Amnon say it? In a voice heard throughout the office. He shouts, to tell her not to shout.",
  pop("His act undermines his own message", 200),
  "His words undermine themselves.",
 ]),
 ('Which parable means the same?', [
  "Choice one: refusing to lend a neighbor a ladder because he once refused you. That's paying back. Not our meaning. Out.",
  D("Cross out choice 1"),
  "Choice two: \"a speaker who lectures for two hours on the advantages of short speeches\".",
  "Two hours, in praise of short speeches. The act undermines the message. Exactly Amnon.",
  D("Circle choice 2"),
  "Choice 2.",
  "Before marking - a quick look at the others:",
  "Choice three: watering the garden during the rain. Pointless, but it doesn't undermine a message. Out.",
  D("Cross out choice 3"),
  "Choice four: blaming the thief because you left the car door open. That's shifting the blame. It sounds ironic, but it's not a message that undermines itself. Out.",
  D("Cross out choice 4"),
 ]),
], T45),

# ------------------------------------------------------------------ Q · parable: the context (Hebrew 3007-3074, easy)
guided(4, 'vo-45-005', GQ, SBQ, ["A sample question – an easy one."], [
 ('A parable answers something', [
  "\"Which of the following is most likely to be what Orna said?\"",
  pop("A parable responds to something said, done or planned", 120),
  "When someone uses a parable, it's in response to something: something the other person said, did, or plans to do. Here they ask: what was the background?",
  "To find the background, first understand what the parable means.",
  D("Underline 'decides whether a watermelon is sweet according to the sticker of the shop on it'"),
  "Judging the watermelon by the shop's sticker? The fruit is what matters. The sticker is beside the point.",
  pop("Judging the main thing by something beside the point", 200),
 ]),
 ('Find the parallel', [
  "So Orna judged something by a detail that doesn't matter. Which choice does that?",
  "Choices one, two and three each judge the thing itself: the comfort of the shoes, the acting, the taste of the coffee. Out.",
  D("Cross out choices 1, 2 and 3"),
  "Choice four: \"Attorney Amir is certainly an excellent lawyer - his office is in the most expensive building in the city.\"",
  "An excellent lawyer, because of the building his office is in. The building is the sticker.",
  D("Circle choice 4"),
  "Choice 4.",
  pop("Often the parable says: that was a bit silly – politely", 120),
  "By the way, a nuance that keeps coming back: very often the parable is a polite way of saying 'what you just said is a bit silly'. Nicely worded, but that's the message.",
 ]),
], T45),

# ------------------------------------------------------------------ Q · parable: what is compared to what (Hebrew 3075-3143, medium)
guided(5, 'vo-45-006', GQ, SBQ, ["A sample question – medium level."], [
 ('Map the parable', [
  "\"In his answer, Boaz compares -\"",
  "Here we get the background and the parable, and they ask what is compared to what. That's the third kind of parable question.",
  D("Underline 'You are crossing the river by swimming, when the bridge is a few steps from you'"),
  "Crossing a river by swimming, the hard way, when the bridge is right there: the easy way to the very same bank.",
  D("Draw arrows: 'swimming' → ordering from abroad · 'the bridge' → the copy in the city library"),
  pop("Hard way (swimming across) = ordering the book from abroad", 120),
  pop("The bridge = the copy in the city library", 190),
  "The hard way is ordering from abroad and waiting two months. The bridge is the library copy, standing on the shelf.",
 ]),
 ('Check the pairs', [
  "Choice one: \"the copy in the city library to the bridge\". The easy way across. Yes.",
  D("Circle choice 1"),
  "Choice 1.",
  "Before marking - a quick look at the others:",
  "Choice two: ordering the book to the river. No, ordering is the swimming, not the river. Out.",
  D("Cross out choice 2"),
  "Choice three: the cookbook to the bridge. The book is what you want to reach, on the other side. Out.",
  D("Cross out choice 3"),
  "Choice four: the copy from abroad to the swimming. That copy is the goal, not the effort. Out.",
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
