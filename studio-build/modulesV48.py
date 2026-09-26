# Verbal Reasoning · Topic 48 · Rules and arrangements.
# Hebrew (hebverbal.txt 4002-4597) decides the concepts, structure, order, methods and verdicts.
# Every guided question is an original written for the course (content/verbal_originals_C.json, vo-48-…); no Hebrew example is translated.
from dsl import *

TOPIC = 48

def L(t, y, size=40): return T(t, size=size, x=410, y=y, w=1140)

SB_TYPES = ['Two question types', 'Rules', 'Arrangements', 'Combined']
SB_ARR = ['Place the items', 'Sketch it', 'Mark the items', 'Find an anchor', 'Chain the clues',
          'Used clues', 'Two-way arc', 'Full or partial']
G1, SBG1 = 'Rules Questions', ['Q1', 'Q2']
G2, SBG2 = 'Arrangement Questions', ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']

MODULES = [
# ------------------------------------------------------------------ lesson: the question types (Hebrew 4002-4020)
lesson('vr48-types', 'Rules and Arrangements', SB_TYPES, [
 dict(mode='title', title='Rules and Arrangements', script=[
  "Rules and arrangements.",
  "Another question type in the verbal reasoning section.",
 ]),
 dict(mode='concept', active=0, title='Two question types', script=[
  "These questions come in two types.",
  "And sometimes the border between the two is a little blurry.",
  A("Rules questions · Arrangement questions · combined ones appears", L('Rules questions · Arrangement questions · and combined ones', 160)),
  "There are also combined questions — rules and arrangements together.",
 ]),
 dict(mode='concept', active=1, title='Rules', script=[
  "So what are rules questions?",
  "We get a rule — or several rules.",
  A("Rules: which answer keeps (or breaks) the rule? appears", L('Rules: which answer keeps — or breaks — the rule?', 160)),
  "And we check which of the answers keeps those rules — or doesn't keep them. It depends on the question.",
 ]),
 dict(mode='concept', active=2, title='Arrangements', script=[
  "And arrangement questions?",
  "Here we place certain items in some order.",
  "People standing in a row. People living in a building — each on a different floor. That kind of thing.",
  A("Arrangements: place items in order, by the clues appears", L('Arrangements: place items in order, according to the clues', 160)),
  "We get a set of clues that hint how the items should be placed.",
 ]),
 dict(mode='concept', active=3, title='Combined', script=[
  "Sometimes some of those clues are themselves a kind of rule.",
  A("Combined: rules + arrangement in one question appears", L('Combined: rules + arrangement in one question', 160)),
  "And that's where the combined questions come in.",
  "Let's start with a sample question.",
 ]),
], TOPIC),

# ------------------------------------------------------------------ Q1 · rules: two approaches (Hebrew example 1, hard)
guided(0, 'vo-48-001', G1, SBG1,
 ["A sample question — a hard one.", "A rules question: we get a rule, and we check which answer keeps it — or breaks it."],
 [('Read the rule', [
   "Dalia invented a word game. Each player says a sentence — and every word must meet at least one of two conditions.",
   "A: the word contains at least two vowels. B: the word begins and ends with the same letter.",
   D("Underline 'at least one of two conditions'"),
   "At least one. A word that meets A is fine. A word that meets B is fine. A word that meets both — fine too.",
   "The question: which sentence does not meet the conditions?",
   "Rules questions have two main approaches.",
   A("Way 1: answer → rules appears", P('Way 1 · answer → rules: take one answer, check it against every rule', y=120)),
   A("Way 2: rule → answers appears", P('Way 2 · rule → answers: take one rule, run it through all the answers', y=200)),
   "First we'll solve it the first way — then the second way.",
  ]),
  ('Way 1 · Answer by answer', [
   "Choice one: Ronit did enjoy reading novels.",
   D("Tick each word in choice 1: Ronit, did, enjoy, reading, novels"),
   "Ronit — o, i: two vowels. Enjoy, reading, novels — two vowels or more. And 'did'? One vowel only — condition A fails.",
   D("Circle 'did' in choice 1"),
   "But 'did' begins with d and ends with d. Condition B saves it. The sentence keeps the rules — rule it out.",
   D("Cross out choice 1"),
   "Choice two: Every student likes jazz music.",
   D("Circle 'jazz' in choice 2"),
   "Every, student, likes, music — two vowels each. 'Jazz' — one vowel. Condition A fails. Begins with j, ends with z. Condition B fails too.",
   A("One word that fails both = the sentence breaks the rule appears", P('One word that fails both conditions → the whole sentence breaks the rule', y=120)),
   "One word is enough. This sentence does not meet the conditions.",
   "On the exam — mark it and move on. In the lesson, let's check the others too.",
   "Choice three: Maria gave twelve roses away. Every word has at least two vowels. It keeps the rules.",
   "Choice four: Aviva ate that tomato quietly. 'That' has one vowel — but begins and ends with t. Saved by B. It keeps the rules.",
  ]),
  ('Way 2 · Rule by rule', [
   "Now the same question the second way — through the rules.",
   "Take condition A and run it through all four answers. Only a word with fewer than two vowels can cause trouble.",
   D("Underline every word with only one vowel in the four choices"),
   "Choice one — 'did'. Choice two — 'jazz'. Choice three — none. Choice four — 'that'.",
   A("Condition A leaves three suspects → check B only on them appears", P('Condition A leaves three suspects → check B only on them', y=120)),
   "Three suspects. Here's the trap: check only condition A, and three sentences look wrong.",
   "Now condition B — only on the suspects. 'Did' — d and d. Passes. 'That' — t and t. Passes. 'Jazz' — j and z. Fails.",
   "Sometimes the rules depend on each other — then you can't check one rule on its own. Those are usually the harder, edge questions.",
   "Use whichever way feels natural to you.",
   D("Circle choice 2"),
   "Choice two.",
  ])], TOPIC),

# ------------------------------------------------------------------ Q2 · the reverse: which rule could not be (Hebrew example 2, easy)
guided(1, 'vo-48-002', G1, SBG1,
 ["A sample question — an easy one.", "This time the question is turned around."],
 [('Turn it around', [
   "Four candidates applied for a job as a guide at a city museum. We're told which languages each one speaks — and who was accepted.",
   "Which of the following could not have been the requirement for being accepted?",
   "Until now we got a rule and asked what keeps it. Here we get a situation — and ask which rule could produce it.",
   A("Given the outcome → which rule is (not) possible? appears", P('Given the outcome → which rule is (not) possible?', y=120)),
   D("Write a mini table: Omer ✓ · Yael ✓ · Tamar ✗ · Ido ✓"),
   "A quick table: Omer — English and French — accepted. Yael — English — accepted. Tamar — Russian — not accepted. Ido — Russian and Spanish — accepted.",
   A("A requirement is possible only if it gives all four results appears", P('A requirement is possible only if it gives all four results', y=200)),
  ]),
  ('Test each requirement', [
   "Choice one: anyone who speaks two languages is accepted, and anyone who speaks English too.",
   "Omer and Ido speak two languages — accepted. Yael speaks English — accepted. Tamar — one language, not English — not accepted. All four match.",
   "This could be the requirement. We're asked what could not be — so we rule it out.",
   D("Cross out choice 1"),
   "Choice two: everyone is accepted except those who speak one language only, and it's not English. That's Tamar — rejected. Everyone else — accepted. It fits.",
   D("Cross out choice 2"),
   "Choice three: accepted only if they speak more than one language, or do not speak English at all.",
   D("Underline 'only if' in choice 3"),
   "Yael — English, and nothing else. Not more than one language, and she does speak English. She couldn't be accepted.",
   "But Yael was accepted. This requirement clashes with the results.",
   A("One candidate who doesn't fit = the requirement is impossible appears", P("One candidate who doesn't fit → the requirement is impossible", y=120)),
   "On the exam — mark it and move on. In the lesson, let's see why the last one fits.",
  ]),
  ('Why the last one fits', [
   "Choice four: a candidate who doesn't speak English is not accepted, unless they speak Spanish.",
   "Tamar — no English, no Spanish — rejected. Ido — no English, but Spanish — can be accepted. Omer and Yael speak English. It fits.",
   D("Cross out choice 4"),
   D("Circle choice 3"),
   "Choice three.",
  ])], TOPIC),

# ------------------------------------------------------------------ lesson: the arrangement method (taught in Hebrew example 3)
lesson('vr48-arrange', 'Arrangement Questions', SB_ARR, [
 dict(mode='title', title='Arrangement Questions', script=[
  "Now we move to arrangement questions.",
  "Take the items — and place them according to the clues.",
 ]),
 dict(mode='concept', active=0, title='Place the items', script=[
  "In an arrangement question we have items — and slots.",
  A("Arrangement: place items in slots by the clues appears", L('Arrangement: place the items in slots, according to the clues', 160)),
  "People in seats, animals on floors, cards in positions. The clues tell us who goes where.",
 ]),
 dict(mode='concept', active=1, title='Sketch it', script=[
  "On the exam you have the test booklet — there's always room to draw.",
  A("Always sketch — never solve in your head appears", L('Always sketch — never solve it in your head', 160)),
  "In arrangement questions I strongly recommend sketching and placing. Don't try to solve it in your head.",
  D("Draw a row of empty slots"),
 ]),
 dict(mode='concept', active=2, title='Mark the items', script=[
  "So what's the first thing I do?",
  A("Step 1 · Circle the items to place appears", L('Step 1 · Circle the items you need to place', 160)),
  "I mark the items — really circle them in the question.",
  "Why? These questions are full of text. I want to spot at a glance who I'm placing.",
  A("Names A, B, C, D? Use first letters appears", L('Names start with different letters? Use the first letters', 260)),
  "And often they make it easy for you: the names start with different letters. Then just use the first letters — it saves time.",
 ]),
 dict(mode='concept', active=3, title='Find an anchor', script=[
  "The second thing: I look for an anchor.",
  A("Step 2 · Anchor = a clue that fixes an exact position appears", L('Step 2 · Anchor = a clue that fixes an exact position', 160)),
  "What's an anchor? Say a clue tells me two items are together. Fine — but where? First slot? Second? Third? I don't know.",
  "That's not where I start. I want a clue that tells me exactly where something goes — so I can place it right away.",
  "That's an anchor. Place it immediately.",
  A("No sure anchor → two sketches in parallel appears", L('No sure anchor → two sketches side by side', 260)),
  "By the way — there isn't always a certain anchor. Sometimes there are two possible places. Then I work with two sketches in parallel.",
 ]),
 dict(mode='concept', active=4, title='Chain the clues', script=[
  "Once the anchor is placed, I start chaining the other clues to it.",
  A("Step 3 · Chain the clues onto the anchor appears", L('Step 3 · Chain the other clues onto the anchor — link after link', 160)),
  "Another link, another link, another link. But I need somewhere to start — that's why the anchor matters.",
  "A clue with no position yet — like two items that must be together — I jot at the side of the sketch.",
  D("Write a loose pair at the side of the sketch"),
  "And I place it when I see where it fits.",
 ]),
 dict(mode='concept', active=5, title='Used clues', script=[
  "Some students cross out each clue as soon as they've used it — so it won't confuse them.",
  A("Used a clue? You may cross it out appears", L('Used a clue? You may cross it out', 160)),
  "It's not a must. Usually there aren't many clues — two or three, you'll manage without it. Your call.",
 ]),
 dict(mode='concept', active=6, title='Two-way arc', script=[
  "Sometimes two items can trade places — you know they sit in these two slots, but not which is which.",
  D("Draw a small two-way arc between two slots"),
  A("Two items can swap → draw a two-way arc appears", L('Two items can swap → draw a two-way arc', 160)),
  "I always draw a small arc with arrows between them — so I remember they can switch.",
 ]),
 dict(mode='concept', active=7, title='Full or partial', script=[
  "Sometimes we place everything — every item has its slot. A full arrangement.",
  A("Full arrangement → just read off the answer appears", L('Full arrangement → just read off the answer', 160)),
  "Then answering the question is easy.",
  A("Partial → ask: could be? must be? appears", L('Partial arrangement → ask: what could be? what must be?', 260)),
  "Sometimes it's only partial — some slots stay open. Then the questions are: what could be there? What must be there? It depends on the question.",
  "Let's see it in action.",
 ]),
], TOPIC),

# ------------------------------------------------------------------ Q3 · anchor and chain (Hebrew example 3, easy)
guided(0, 'vo-48-003', G2, SBG2,
 ["A sample question — an easy one.", "Our first arrangement question. Mark, sketch, anchor, chain."],
 [('Mark and sketch', [
   "Omri, Talia and Neta live in a three-story building, one on each floor. Each keeps one of these pets: a cat, a dog and a rabbit.",
   D("Circle Omri, Talia, Neta — and cat, dog, rabbit"),
   "Step one: mark the items. Three people, three pets.",
   D("Draw three floors stacked: 1 · 2 · 3"),
   "Step two: sketch. Three floors, one above the other.",
   "Clue A: Talia lives on a floor adjacent to the dog owner's floor. Clue B: the rabbit's owner lives on the second floor.",
   "Which clue is the anchor? Talia next to the dog owner — which floor exactly? Don't know. The rabbit on the second floor — an exact position.",
   A("Anchor: rabbit → second floor appears", P('Anchor: rabbit → the second floor', y=120)),
   D("Write 'rabbit' next to floor 2"),
  ]),
  ('Chain the clues', [
   "Now chain Talia to the anchor. Could Talia live on the first or the third floor?",
   "Then the only floor adjacent to hers is the second — and the second floor belongs to the rabbit's owner, not the dog's.",
   A("Talia on floor 1 or 3 → her only neighbor floor has the rabbit ✗ appears", P("Talia on floor 1 or 3 → the only adjacent floor has the rabbit ✗", y=120)),
   "So Talia lives on the second floor — and she owns the rabbit.",
   D("Write T next to floor 2"),
   "Omri and Neta take floors one and three, with the cat and the dog — in either order.",
   D("Draw a two-way arc between floors 1 and 3"),
   "A partial arrangement: the second floor is fixed, the other two can swap.",
   "What is necessarily true?",
  ]),
  ('Check the answers', [
   "Choice one: Neta owns the cat. She might — or she might own the dog. Not necessarily.",
   "Choice two: Omri lives on the third floor. He might — floors one and three swap. Not necessarily.",
   "Choice four: Neta is not the owner of the dog. She might be. Not necessarily.",
   D("Cross out choices 1, 2 and 4"),
   "Choice three: Omri is not the owner of the rabbit. Talia owns it — so this is necessarily true.",
   D("Circle choice 3"),
   "Choice three.",
  ])], TOPIC),

# ------------------------------------------------------------------ Q4 · each answer adds a given (Hebrew example 4, medium)
guided(1, 'vo-48-004', G2, SBG2,
 ["A sample question — medium level.", "Very few givens — and every answer adds one more."],
 [('The base givens', [
   "Two novels and two cookbooks stand on a shelf in places 1 to 4, from left to right. The two cookbooks do not stand next to each other.",
   D("Draw four slots numbered 1, 2, 3, 4"),
   "Where can the cookbooks go? One and three. One and four. Two and four. That's all.",
   A("Cookbook pairs: 1–3 · 1–4 · 2–4 appears", P('Cookbook pairs: 1–3 · 1–4 · 2–4', y=120)),
   "The question: which additional fact lets us determine the type of every book for certain?",
   "Each answer adds a new given. Test each one on its own.",
   A("Each answer = a new given · start fresh every time appears", P('Each answer = a new given · start fresh from the base givens every time', y=200)),
   "And when you move on to the next answer — drop the previous one. It no longer exists. Start again from what the question gave you.",
  ]),
  ('Test each fact', [
   "Choice one: book 3 is a novel. No cookbook at 3 — one–four or two–four are left. Two arrangements. Not certain.",
   D("Cross out choice 1"),
   "Choice two: book 4 is a cookbook. Back to the base givens: one–four or two–four. Two again.",
   D("Cross out choice 2"),
   "Choice three: book 1 is a novel. Then no cookbook at 1 — only two and four are left. One arrangement. Every type is known.",
   D("Cross out the pairs 1–3 and 1–4"),
   "Choice three works. On the exam — mark it and move on. In the lesson, the last one.",
   "Choice four: no book stands next to a book of its own type. Cookbook-novel-cookbook-novel, or novel-cookbook-novel-cookbook. Two arrangements.",
   D("Cross out choice 4"),
   D("Circle choice 3"),
   "Choice three.",
  ])], TOPIC),

# ------------------------------------------------------------------ Q5 · leave one out, is there still a contradiction? (Hebrew example 5, hard)
guided(2, 'vo-48-005', G2, SBG2,
 ["A sample question — a hard one.", "A contradiction question."],
 [('What are they asking?', [
   "The statements made in the following conversation contradict one another.",
   "Without which speaker's statement would the conversation still contain a contradiction?",
   "So we leave one speaker out, and check the remaining three: do they still contradict each other?",
   A("Leave one out · test the other three · still a contradiction? appears", P('Leave one out → test the other three → still a contradiction?', y=120)),
   "If the other three can all be true together — the contradiction is gone. That speaker is not our answer.",
  ]),
  ('Leave one out at a time', [
   "Start by leaving out Amit. Hadas: Amit lends books only to people older than he is. Eli: I'm younger than Amit. Rona: older than Eli, younger than Hadas.",
   "Without Amit's words, nothing says whom Amit lent books to. All three can be true together. No contradiction — not Amit.",
   D("Cross out choice 4"),
   "Put Amit back and leave out Hadas. Now nothing limits whom Amit lends to. No contradiction — not Hadas.",
   D("Cross out choice 1"),
   "Put Hadas back and leave out Eli. Amit lent to Eli — so Eli is older than Amit. Nothing says otherwise. No contradiction.",
   D("Cross out choice 2"),
  ]),
  ('Where the contradiction lives', [
   "The contradiction sits between Hadas, Amit and Eli.",
   A("Hadas + Amit → Eli is older than Amit; Eli: younger ✗ appears", P('Hadas + Amit → Eli is older than Amit · Eli: "I am younger than Amit" ✗', y=120)),
   "Amit lent books to Eli — so by Hadas's words, Eli is older than Amit. But Eli says he's younger.",
   "Rona's words play no part in it. Leave Rona out — and the contradiction is still there.",
   D("Circle choice 3"),
   "Choice three.",
  ])], TOPIC),

# ------------------------------------------------------------------ Q6 · exactly some statements hold (Hebrew example 6, medium)
guided(3, 'vo-48-006', G2, SBG2,
 ["A sample question — medium level.", "A new twist: not every statement holds — only some of them."],
 [('Exactly one fails', [
   "Maya, Nir and Oren had to choose where their team would spend a day out: the zoo, the beach or the science museum. Each expressed a wish.",
   D("Write the wishes as short notes: Maya: beach · Nir: not the zoo · Oren: museum, or Nir pleased"),
   "They went to one of the three places — and exactly one of them did not get their wish.",
   A("Exactly one wish fails → the other two hold appears", P('Exactly one wish fails → exactly two come true', y=120)),
   "So in the real situation, exactly two wishes come true. Which of the following is possible?",
   "The method: place each answer as the situation, and count how many wishes come true. Exactly two? It's possible.",
  ]),
  ('Place each answer', [
   "Choice one: they went to the beach. Maya — pleased. Nir — not the zoo — pleased. Oren — Nir is pleased, so Oren is too. Nobody disappointed.",
   D("Cross out choice 1"),
   "Choice two: Oren is disappointed only if they're not at the museum and Nir is disappointed — and Nir is disappointed only at the zoo. There Maya is disappointed too. Three.",
   D("Cross out choice 2"),
   "Choice three: the science museum. Maya wanted the beach — disappointed. Nir — pleased. Oren — the museum — pleased.",
   A("Museum: Maya ✗ · Nir ✓ · Oren ✓ → exactly one fails ✓ appears", P('Museum: Maya ✗ · Nir ✓ · Oren ✓ → exactly one fails ✓', y=120)),
   "One disappointed, two pleased. Exactly what we need — possible.",
   "On the exam, mark it. In the lesson, the last one.",
   "Choice four: Nir is disappointed only at the zoo — and there Maya and Oren are disappointed too. Three again.",
   D("Cross out choice 4"),
   D("Circle choice 3"),
   "Choice three.",
  ])], TOPIC),

# ------------------------------------------------------------------ Q7 · combined: a rule inside a process (Hebrew example 7, hard)
guided(4, 'vo-48-007', G2, SBG2,
 ["A sample question — a hard one.", "A combined question: a rule and an arrangement together."],
 [('The rule and the process', [
   "Five contestants take part in a television quiz: Noa, Tal, Yuval, Dana and Ariel.",
   "In each round two contestants compete. The loser leaves, and the winner competes next against a contestant who has not yet competed — four rounds in all.",
   D("Draw the ladder: round 1 → round 2 → round 3 → round 4"),
   "And the rule about Noa: if she competes against a contestant who, in the previous round, competed against Tal — she loses. In every other case, she wins.",
   A("Noa loses only if her opponent competed against Tal in the previous round appears", P('Noa loses only if her opponent competed against Tal in the previous round', y=120)),
   "Noa competed in the first round of the quiz. What follows?",
  ]),
  ('Play it out', [
   "Round one: there was no previous round — so her opponent competed against no one. Noa wins.",
   D("Write N ✓ on round 1"),
   "Round two: Noa, the winner, meets a contestant who has not yet competed. That opponent didn't compete in the previous round at all — not against Tal, not against anyone. Noa wins again.",
   D("Write N ✓ on round 2"),
   "Rounds three and four: again a newcomer each time. Noa wins.",
   A("Every opponent of Noa is a newcomer → Noa wins every round appears", P('Every opponent Noa meets is a newcomer → Noa wins every round', y=120)),
   "Don't get lost in Tal. Whoever Tal played, the rule can never catch Noa.",
   D("Cross out choices 1, 3 and 4"),
   D("Circle choice 2"),
   "Choice two.",
   "She won the last round. Not a simple question.",
   "I hope you enjoyed this whole lesson on rules and arrangements. Let's keep going.",
  ])], TOPIC),
]

MEMORY = [
 dict(id='mem-rules-arrangements', after='solve-vo-48-007', title='Rules and arrangements — the method',
  intro='Two question types — rules and arrangements — and combined ones.',
  tables=[
   dict(title='Rules questions', head=['Way', 'How'], rows=[
    ['Answer → rules', 'Take one answer, test it against every rule'],
    ['Rule → answers', 'Take one rule, run it through all the answers, cross out']]),
   dict(title='Arrangement questions', head=['Step', 'What to do'], rows=[
    ['1', 'Circle the items you need to place'],
    ['2', 'Sketch the slots — never solve in your head'],
    ['3', 'Find an anchor: a clue that fixes an exact position'],
    ['4', 'Chain the other clues onto it; loose pairs go at the side'],
    ['5', 'Two items can swap → draw a two-way arc']])],
  tips=['Each answer adds a new given? Test it alone — start again from the base givens.',
        'Contradiction question: leave one statement out and test whether the rest still clash.',
        '"Exactly N are true": place each answer as the situation and count what holds.']),
]
