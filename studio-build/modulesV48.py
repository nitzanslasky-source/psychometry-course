# Verbal Reasoning · Topic 48 · Rules and arrangements.
# Hebrew (hebverbal.txt 4002-4597) decides the concepts, structure, order, methods and verdicts.
# Every question is an English bank item (vcands48.txt, [real exam]); no Hebrew example is translated.
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
guided(0, 'vb-inf_v2_0239', G1, SBG1,
 ["A sample question — a hard one.", "A rules question: we get a rule, and we check which answer keeps it — or breaks it."],
 [('Read the rule', [
   "Moshe invented a game. The players compose sentences — and every word must satisfy at least one of two conditions.",
   "A: the word has four letters or more. B: at least one letter appears in the word twice.",
   D("Underline 'at least one of two conditions'"),
   "At least one. A word that meets A is fine. A word that meets B is fine. A word that meets both — fine too.",
   "The question: which sentence does NOT keep to the rules of the game?",
   "Rules questions have two main approaches.",
   A("Way 1: answer → rules appears", P('Way 1 · answer → rules: take one answer, check it against every rule', y=120)),
   A("Way 2: rule → answers appears", P('Way 2 · rule → answers: take one rule, run it through all the answers', y=200)),
   "First we'll solve it the first way — then the second way.",
  ]),
  ('Way 1 · Answer by answer', [
   "Choice one: Noam loves eating chocolate cake.",
   D("Tick each word in choice 1: Noam, loves, eating, chocolate, cake"),
   "Noam — four letters. Loves, eating, chocolate, cake — four or more. Every word keeps condition A.",
   "This sentence keeps the rules — we can rule it out.",
   D("Cross out choice 1"),
   "Choice two: Efrat sailed toward Cyprus yesterday. Every word has five letters or more. Out.",
   D("Cross out choice 2"),
   "Choice three: Yossi is my best friend.",
   D("Circle 'is' and 'my' in choice 3"),
   "'Is' — two letters. Condition A fails. Does a letter appear twice? I, S — no. Condition B fails too.",
   A("One word that fails both = the sentence breaks the rule appears", P('One word that fails both conditions → the whole sentence breaks the rule', y=120)),
   "One word is enough. This sentence does not keep to the rules.",
   "On the exam — mark it and move on. In the lesson, let's check the last one too.",
   "Choice four: Shoshana gave Hila some sweets. Shoshana, gave, Hila, some, sweets — all four letters or more. It keeps the rules.",
  ]),
  ('Way 2 · Rule by rule', [
   "Now the same question the second way — through the rules.",
   "Take condition A and run it through all four answers. Only a short word can cause trouble.",
   D("Underline every word shorter than four letters in the four choices"),
   "Choice one — no short words. Choice two — none. Choice four — none. Choice three — 'is' and 'my'.",
   A("Condition A leaves one suspect → check B only there appears", P('Condition A alone leaves one suspect → check B only on it', y=120)),
   "So condition B needs checking in choice three only. 'Is', 'my' — no repeated letter. It fails.",
   "Here the first rule already did almost all the work.",
   "Sometimes the rules depend on each other — then you can't check one rule on its own. Those are usually the harder, edge questions.",
   "Use whichever way feels natural to you.",
   D("Circle choice 3"),
   "Choice three.",
  ])], TOPIC),

# ------------------------------------------------------------------ Q2 · the reverse: which rule could NOT be (Hebrew example 2, easy)
guided(1, 'vb-inf_v2_0281', G1, SBG1,
 ["A sample question — an easy one.", "This time the question is turned around."],
 [('Turn it around', [
   "Four academics applied to join the board of the botanical garden. We're told what degrees each one holds — and who was accepted.",
   "Which of the following could NOT have been the condition for acceptance to the board?",
   "Until now we got a rule and asked what keeps it. Here we get a situation — and ask which rule could produce it.",
   A("Given the outcome → which rule is (not) possible? appears", P('Given the outcome → which rule is (not) possible?', y=120)),
   D("Write a mini table: Shoshana ✓ · Rakefet ✓ · Lilach ✗ · Erez ✓"),
   "A quick table: Shoshana — accepted. Rakefet — accepted. Lilach — not accepted. Erez — accepted.",
   A("A condition is possible only if it gives all four results appears", P('A condition is possible only if it gives all four results', y=200)),
  ]),
  ('Test each condition', [
   "Choice one: those who hold a second degree are accepted, and so are those who hold a first degree in botany.",
   "Shoshana and Erez have a second degree — accepted. Rakefet — first degree in botany — accepted. Lilach — only history — not accepted. All four match.",
   "This could be the condition. We're asked what could NOT be — so we rule it out.",
   D("Cross out choice 1"),
   "Choice two: accepted only if they hold a second degree, or a first degree in a department other than botany.",
   D("Underline 'other than botany' in choice 2"),
   "Rakefet — a first degree in botany, nothing else. No second degree, and her degree IS in botany. She'd be rejected.",
   "But Rakefet was accepted. This condition clashes with the results.",
   A("One applicant who doesn't fit = the condition is impossible appears", P("One applicant who doesn't fit → the condition is impossible", y=120)),
   "On the exam — mark it and move on. In the lesson, let's see why the others fit.",
  ]),
  ('Why the others fit', [
   "Choice three: everyone is accepted except those who hold only a first degree outside botany. That's Lilach — rejected. Everyone else — accepted. It fits.",
   D("Cross out choice 3"),
   "Choice four: whoever has no degree in botany is not accepted, unless he holds a degree in physics. Lilach — no botany, no physics — rejected. Erez — physics — accepted. It fits.",
   D("Cross out choice 4"),
   D("Circle choice 2"),
   "Choice two.",
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
guided(0, 'vb-inf_v2_0252', G2, SBG2,
 ["A sample question — an easy one.", "Our first arrangement question. Mark, sketch, anchor, chain."],
 [('Mark and sketch', [
   "Three women — Rinat, Keren and Anavel — sit side by side in the waiting room of a veterinary clinic. Each owns one of these animals: a hamster, a guinea pig and a parrot.",
   D("Circle Rinat, Keren, Anavel — and hamster, guinea pig, parrot"),
   "Step one: mark the items. Three women, three animals.",
   D("Draw three seats in a row: left · middle · right"),
   "Step two: sketch. Three seats in a row.",
   "Clue A: Keren sits beside the owner of the hamster. Clue B: the owner of the guinea pig sits in the middle.",
   "Which clue is the anchor? Keren beside the hamster — where exactly? Don't know. The guinea pig in the middle — an exact position.",
   A("Anchor: guinea pig → middle seat appears", P('Anchor: guinea pig → the middle seat', y=120)),
   D("Write 'guinea pig' under the middle seat"),
  ]),
  ('Chain the clues', [
   "Now chain Keren to the anchor. Could Keren sit at an end?",
   "At an end her only neighbor is the middle seat — and the middle seat belongs to the guinea pig owner, not the hamster owner.",
   A("Keren at an end → her only neighbor has the guinea pig ✗ appears", P('Keren at an end → her only neighbor owns the guinea pig ✗', y=120)),
   "So Keren sits in the middle — and she owns the guinea pig.",
   D("Write K above the middle seat"),
   "The hamster and the parrot go to the two ends — in either order.",
   D("Draw a two-way arc between the two end seats"),
   "A partial arrangement: the middle is fixed, the ends can swap.",
   "What is necessarily true?",
  ]),
  ('Check the answers', [
   "Choice one: Anavel is not the owner of the guinea pig. Keren owns it — so this is necessarily true.",
   "Choice two: Rinat is not the owner of the hamster. She might be — the ends swap. Not necessarily.",
   "Choices three and four — same story. The ends can swap, so neither is necessarily true.",
   D("Cross out choices 2, 3 and 4"),
   D("Circle choice 1"),
   "Choice one.",
  ])], TOPIC),

# ------------------------------------------------------------------ Q4 · each answer adds a given (Hebrew example 4, medium)
guided(1, 'vb-inf_v2_0282', G2, SBG2,
 ["A sample question — medium level.", "Very few givens — and every answer adds one more."],
 [('The base givens', [
   "Two green cards and two pink cards lie in a row, in positions 1 to 4 from left to right. The two pink cards are NOT adjacent.",
   D("Draw four slots numbered 1, 2, 3, 4"),
   "Where can the pinks go? One and three. One and four. Two and four. That's all.",
   A("Pink pairs: 1–3 · 1–4 · 2–4 appears", P('Pink pairs: 1–3 · 1–4 · 2–4', y=120)),
   "The question: adding which datum lets us know the color of every card for certain?",
   "Each answer adds a new given. Test each one on its own.",
   A("Each answer = a new given · start fresh every time appears", P('Each answer = a new given · start fresh from the base givens every time', y=200)),
   "And when you move on to the next answer — drop the previous one. It no longer exists. Start again from what the question gave you.",
  ]),
  ('Test each datum', [
   "Choice one: card 4 is green. Then no pink at 4 — only one and three are left. One arrangement. Every color is known.",
   D("Cross out the pairs 1–4 and 2–4"),
   "Choice one works. On the exam — mark it and move on. In the lesson, the rest.",
   "Choice two: card 1 is pink. Back to the base givens: one–three or one–four. Two arrangements. Not certain.",
   D("Cross out choice 2"),
   "Choice three: card 2 is green. Again one–three or one–four. Two arrangements.",
   D("Cross out choice 3"),
   "Choice four: no two adjacent cards of the same color. Pink-green-pink-green, or green-pink-green-pink. Two again.",
   D("Cross out choice 4"),
   D("Circle choice 1"),
   "Choice one.",
  ])], TOPIC),

# ------------------------------------------------------------------ Q5 · leave one out, is there still a contradiction? (Hebrew example 5, hard)
guided(2, 'vb-inf_v2_0272', G2, SBG2,
 ["A sample question — a hard one.", "A contradiction question."],
 [('What are they asking?', [
   "In the conversation below there is a contradiction between the speakers' claims.",
   "Which speaker's words could be omitted from the conversation — and the contradiction would remain?",
   "So we leave one speaker out, and check the remaining three: do they still contradict each other?",
   A("Leave one out · test the other three · still a contradiction? appears", P('Leave one out → test the other three → still a contradiction?', y=120)),
   "If the other three can all be true together — the contradiction is gone. That speaker is not our answer.",
  ]),
  ('Leave one out at a time', [
   "Start by leaving out Tami. Ruti: taller than Smadar, shorter than Shira. Smadar: shorter than Tami. Shira: Tami likes only people taller than she is.",
   "Without Tami's words, nothing says whom Tami likes. All three can be true together. No contradiction — not Tami.",
   D("Cross out choice 4"),
   "Put Tami back and leave out Shira. Now nothing limits whom Tami likes. No contradiction — not Shira.",
   D("Cross out choice 3"),
   "Put Shira back and leave out Smadar. Tami likes Smadar — so Smadar is taller than Tami. Nothing says otherwise. No contradiction.",
   D("Cross out choice 2"),
  ]),
  ('Where the contradiction lives', [
   "The contradiction sits between Shira, Tami and Smadar.",
   A("Shira + Tami → Smadar is taller than Tami; Smadar: shorter ✗ appears", P('Shira + Tami → Smadar is taller than Tami · Smadar: "I am shorter than Tami" ✗', y=120)),
   "Tami likes Smadar — so by Shira's words, Smadar is taller than Tami. But Smadar says she's shorter.",
   "Ruti's words play no part in it. Leave Ruti out — and the contradiction is still there.",
   D("Circle choice 1"),
   "Choice one.",
  ])], TOPIC),

# ------------------------------------------------------------------ Q6 · exactly some statements hold (Hebrew example 6, medium)
guided(3, 'vb-inf_v2_0238', G2, SBG2,
 ["A sample question — medium level.", "A new twist: not every statement holds — only some of them."],
 [('Exactly one fails', [
   "Adi, Ben and Chen wanted to choose a restaurant for dinner. Each one stated a wish.",
   D("Write the wishes as short notes: Adi: Harbor · Ben: not the Garden · Chen: the Market, or Adi content"),
   "They ate at one of the three restaurants — and exactly one of them did not get his wish.",
   A("Exactly one wish fails → the other two hold appears", P('Exactly one wish fails → exactly two come true', y=120)),
   "So in the real situation, exactly two wishes come true. Which of the following is possible?",
   "The method: place each answer as the situation, and count how many wishes come true. Exactly two? It's possible.",
  ]),
  ('Place each answer', [
   "Choice one: they ate at the Market. Adi wanted the Harbor — not content. Ben — anywhere but the Garden — content. Chen — the Market — content.",
   A("Market: Adi ✗ · Ben ✓ · Chen ✓ → exactly one fails ✓ appears", P('Market: Adi ✗ · Ben ✓ · Chen ✓ → exactly one fails ✓', y=120)),
   "One disappointed, two content. Exactly what we need — possible.",
   "On the exam, mark it. In the lesson, the others.",
   "Choice two: the Harbor. Adi content, Ben content — and Chen content, because Adi is. Nobody disappointed.",
   D("Cross out choice 2"),
   "Choice three: Ben is disappointed only at the Garden — and there Adi is disappointed too. Two.",
   D("Cross out choice 3"),
   "Choice four: Chen is disappointed only away from the Market with Adi disappointed — so Adi is disappointed too. Two again.",
   D("Cross out choice 4"),
   D("Circle choice 1"),
   "Choice one.",
  ])], TOPIC),

# ------------------------------------------------------------------ Q7 · combined: a rule inside a process (Hebrew example 7, hard)
guided(4, 'vb-inf_v2_0263', G2, SBG2,
 ["A sample question — a hard one.", "A combined question: a rule and an arrangement together."],
 [('The rule and the process', [
   "In a tournament, four players compete: Itzik, Beni, Gil and David.",
   "At every stage one game is played. The loser leaves, and the winner plays next against a player who has not yet played.",
   D("Draw the ladder: game 1 → game 2 → final"),
   "And the rule about Gil: if he plays against an opponent who played in the previous game, he loses. In every other case, he wins.",
   A("Gil loses ⇔ his opponent played in the previous game appears", P('Gil loses only if his opponent played in the previous game', y=120)),
   "Gil played in the first game of the tournament. What follows?",
  ]),
  ('Play it out', [
   "Game one: there was no previous game — so Gil's opponent didn't play in it. Gil wins.",
   D("Write G ✓ on game 1"),
   "Game two: Gil, the winner, meets a player who has not yet played. That opponent didn't play in the previous game. Gil wins again.",
   D("Write G ✓ on game 2"),
   "The final: again a newcomer. Gil wins.",
   A("Every opponent of Gil is a newcomer → Gil wins every game appears", P('Every opponent Gil meets is a newcomer → Gil wins every game', y=120)),
   D("Cross out choices 1, 2 and 3"),
   D("Circle choice 4"),
   "Choice four.",
   "He won the final. Not a simple question.",
   "I hope you enjoyed this whole lesson on rules and arrangements. Let's keep going.",
  ])], TOPIC),
]

MEMORY = [
 dict(id='mem-rules-arrangements', after='solve-vb-inf_v2_0263', title='Rules and arrangements — the method',
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
