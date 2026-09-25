# Verbal Reasoning · Topic 49 · Reading Comprehension.
# Hebrew (hebverbal.txt 4598-5292) decides the concepts, structure, method, tips and verdicts.
# Every question and passage is a real English bank item (vcands49.txt); wording is never changed.
# Worked passage: vbp-01 (Winter 2025 §1 Passage A), solved in passage order with the Hebrew method.
from dsl import *

T49 = 49
PID = 'vbp-01'

SB_METHOD = ['The passage section', 'Base it on the text', 'Questions in order', 'Two question types',
             'Three specific types', 'No reference', 'Solve in order', 'Line questions', 'Paragraph questions',
             'General questions', 'Names in questions', 'The working method', 'Tips']

SB_PASSAGE = ['Three approaches', 'Choices first?', 'Paragraph 1', 'Paragraph 2', 'Paragraph 3', 'Paragraph 4',
              'Paragraph 5', 'The solving order']

SB_Q = ['Q1 · Sentence', 'Q2 · Paragraph 2', 'Q3 · Peer hypothesis', 'Q4 · NOT correct', 'Q5 · The study',
        'Q6 · Main conclusion']
GQ = 'Reading Comprehension Passage'

def PS(n): return dict(pre=[PSG(PID, [n])])

MODULES = [
# ------------------------------------------------------------------ lesson: the method
lesson('vr49-method', 'Reading Comprehension', SB_METHOD, [
 dict(mode='title', title='Reading Comprehension', script=[
  "Reading comprehension.",
  "The last part of the verbal section — and the one where a smart working method saves you the most time.",
 ]),
 dict(mode='concept', active=0, title='The passage section', script=[
  "At the end of the verbal section there's a reading passage.",
  A("Passage + 5–6 questions appears", T('One passage, then 5–6 questions (rarely 7)', size=42, x=410, y=110, w=1140)),
  "After it — five or six questions. It's not fixed. In rare cases even seven. But usually five or six.",
  A("Sometimes: two short passages × 3 questions appears", T('Sometimes: two shorter passages, 3 questions each', size=36, x=410, y=190, w=1140)),
  "And sometimes you get two shorter passages instead, with three questions each.",
  A("Recommended time: 6–7 minutes — including reading appears", T('Recommended time: 6–7 minutes — reading included', size=42, x=410, y=270, w=1140)),
  "The recommended time: six to seven minutes. And that includes reading the passage.",
  "Read the whole passage, read all the questions, answer everything — in six minutes? Almost impossible.",
  A("So: read only the parts the questions need appears", T('So we read only the parts the questions send us to', size=42, x=410, y=370, w=1140)),
  "So we'll learn a technique where we DON'T read the whole passage — only the parts we need to answer the questions.",
  A("What's tested appears", T('Tested: understanding the ideas, the details, the links between parts, conclusions, structure', size=34, x=410, y=470, w=1140)),
  "What's being tested? Your ability to understand the passage and the connections between its ideas and claims.",
  "Some questions are simple reading — just understand a sentence. Others go deeper: the ideas, the conclusions, the structure.",
 ]),
 dict(mode='concept', active=1, title='Base it on the text', script=[
  "The instructions are simple: read the passage carefully and answer the questions that follow.",
  "A few notes.",
  A("Answers must be based on the passage appears", T('Answer only from the passage — not from what you know', size=44, x=410, y=120, w=1140)),
  "First: the answers must be based on the passage.",
  "Got a passage on something you happen to know about? Don't answer from general knowledge.",
  "What you know may not match what's written — and only what's written counts.",
 ]),
 dict(mode='concept', active=2, title='Questions in order', script=[
  A("Questions follow the order of the passage appears", T('The questions follow the order of the passage', size=44, x=410, y=120, w=1140)),
  "Second: the questions appear in the order of the passage — not from easy to hard like we're used to.",
  A("Q2 → paragraph 2  ⇒  Q3 → after it appears", T('Question 2 answered in paragraph 2  ⇒  question 3 is answered later, not earlier', size=34, x=410, y=210, w=1140)),
  "So if the answer to question two was in paragraph two, the answer to question three will be after it — not before.",
  A("General questions: anywhere appears", T('General questions can appear anywhere — first, middle or last', size=38, x=410, y=300, w=1140)),
  "General questions are the exception. They can show up anywhere — at the start, in the middle, at the end.",
  "What's a general question? One that doesn't send you to a specific place: what is the passage about, which title fits best, and so on.",
  "We'll see that we simply skip them — for now.",
 ]),
 dict(mode='concept', active=3, title='Two question types', script=[
  "Question types. Broadly — two.",
  A("1 · Specific questions appears", T('1 · Specific — send you to a certain place in the passage', size=42, x=410, y=120, w=1140)),
  "One: specific questions. They send you to a certain place in the passage.",
  A("2 · General questions appears", T('2 · General — need the whole passage', size=42, x=410, y=200, w=1140)),
  "Two: general questions. To answer them you need to understand the whole passage.",
 ]),
 dict(mode='concept', active=4, title='Three specific types', script=[
  "There are three kinds of specific questions.",
  A("Line questions appears", T('Line questions — "(lines 6–7)"', size=42, x=410, y=120, w=1140)),
  "The first: line questions. They send you to a line number — or a few lines, like six to seven.",
  A("Paragraph questions appears", T('Paragraph questions — "According to the third paragraph…"', size=42, x=410, y=200, w=1140)),
  "The second: paragraph questions. Same idea — they send you to a certain paragraph.",
  "With these two, it's crystal clear where to go.",
  A("No-reference questions appears", T('No-reference questions — the answer is in one place, but you\'re not told where', size=38, x=410, y=280, w=1140)),
  "The third — and the trickier one: questions with no reference.",
  "The answer IS in one specific place. You don't need the whole passage like a general question. You just don't know where.",
  "Don't confuse them with general questions — which also have no reference. We'll see how to tell them apart.",
 ]),
 dict(mode='concept', active=5, title='No reference', script=[
  "So what do you do with a no-reference question?",
  A("Bound it by the question before and after appears", T('Bound it: between the question before and the question after', size=42, x=410, y=120, w=1140)),
  "You bound it — using the question before it and the question after it.",
  A("Before → paragraph 1 · after → paragraph 3  ⇒  it's in between appears", T('Before → paragraph 1 · after → paragraph 3  ⇒  the answer is in between', size=36, x=410, y=210, w=1140)),
  "If the question before sent you to the first paragraph, and the question after sent you to the third — the answer is somewhere in between.",
  "Usually that brings you to one paragraph. Read it — just like a paragraph question.",
 ]),
 dict(mode='concept', active=6, title='Solve in order', script=[
  "A couple of small notes.",
  A("Not every passage has general questions appears", T('Not every passage has general questions', size=40, x=410, y=120, w=1140)),
  "Not every passage has general questions. Sometimes they're all specific.",
  A("Questions can build on earlier ones → solve in order appears", T('Questions can build on earlier ones  →  solve in order', size=40, x=410, y=200, w=1140)),
  "Some questions build on earlier questions. So it's important — and recommended — to solve in order.",
  "True, you COULD jump straight to question three because it sends you to the end of the passage.",
  "You could. Better not. Even a line question at the end may rely on what you understood in the questions before it.",
 ]),
 dict(mode='concept', active=7, title='Line questions', script=[
  A("Start reading one sentence before appears", T('Start reading one sentence before the line', size=42, x=410, y=120, w=1140)),
  "Line questions. They send you to a line — or a few lines.",
  "Start reading a little before: from the previous sentence. That's usually a line or two earlier.",
  "In most cases the line they sent you to isn't enough on its own.",
  A("Mostly: understanding the sentence in its context appears", T('Mostly: understanding that sentence in its context', size=40, x=410, y=210, w=1140)),
  "What these questions need is mostly syntax — understanding that specific sentence in its context.",
  "Not always — sometimes a bit more understanding. But you don't need the whole passage.",
  A("Several lines given → just read those appears", T('Sent to several lines (e.g. 26–29)?  Usually just read those', size=36, x=410, y=300, w=1140)),
  "And when they send you to several lines — four lines, say — you usually don't need to start earlier. Read what they gave you.",
 ]),
 dict(mode='concept', active=8, title='Paragraph questions', script=[
  A("Paragraph questions: the idea of the paragraph appears", T('Paragraph questions: understand the idea of the paragraph', size=42, x=410, y=120, w=1140)),
  "Paragraph questions. Unlike line questions — here you need the idea expressed in the paragraph.",
  "Read the paragraph, understand it a bit more deeply. But you still don't need the whole passage.",
  A("No-reference questions work the same way appears", T('No-reference questions work the same way — once you\'ve bounded them', size=36, x=410, y=210, w=1140)),
  "No-reference questions are really like paragraph questions: bound them, and you usually land on one paragraph to read.",
 ]),
 dict(mode='concept', active=9, title='General questions', script=[
  "General questions — these need an understanding of the whole passage.",
  "Careful: that does NOT mean you need to read the whole passage.",
  A("What you gathered from the specific questions is usually enough appears", T('What you gathered on the specific questions is usually enough', size=38, x=410, y=110, w=1140)),
  "In most cases, what you gathered while solving the specific questions is enough. Sometimes you skim a few more lines. That's it.",
  A("See one? Skip it, mark it, solve it last appears", T('See a general question?  Skip it · mark it · solve it last', size=42, x=410, y=190, w=1140)),
  "That's exactly why we leave them for the end. Wherever one shows up — start, middle, end — you skip it.",
  "And mark it! So you don't reach the end of the test and discover you forgot a general question or two.",
  A("How to spot one: \"according to the passage\" appears", T('How to spot one: it always says "according to the passage" / "from the passage"', size=36, x=410, y=280, w=1140)),
  "How do you recognize a general question? It will always say \"according to the passage\" — always.",
  A("Exception: the last question appears", T('Exception: the last question may leave it out', size=38, x=410, y=360, w=1140)),
  "Except one case: if the general question is the last question, it doesn't have to say it. Sometimes it does, sometimes it doesn't.",
  "A specific no-reference question won't say \"according to the passage\". That's how you tell them apart.",
 ]),
 dict(mode='concept', active=10, title='Names in questions', script=[
  "An important point — many students lose time on this.",
  A("Names that aren't in the passage appears", T('A name in the question may not appear in the passage at all', size=40, x=410, y=120, w=1140)),
  "Some questions contain names. And not every name is from the passage — sometimes it's just a name made up for the question.",
  "Sometimes the wording tells you the person is in the passage. Sometimes you can't tell.",
  A("Read only the part it sends you to appears", T('Read only the part it points to — not there (or in parts you read)?  It\'s not in the passage', size=34, x=410, y=210, w=1140)),
  "Can't tell? Read only the part the question sends you to.",
  "If the name isn't there — or in the parts you already read on earlier questions — it's not a name from the passage.",
  "Don't panic. Don't start hunting — \"wait, where is this name?\" It's an example made up for the question. Don't waste time.",
 ]),
 dict(mode='concept', active=11, title='The working method', script=[
  "The working method.",
  A("1 · Read the question — without the choices appears", T('1 · Read the question — without the choices', size=40, x=410, y=110, w=1140)),
  "One: read the question. Without the answer choices.",
  A("2 · Read the part of the passage it points to appears", T('2 · Read the part of the passage it points to', size=40, x=410, y=180, w=1140)),
  "Two: read the part of the passage the question points to — this is for specific questions.",
  A("3 · Read the question with the choices, and answer appears", T('3 · Read the question with the choices — and answer', size=40, x=410, y=250, w=1140)),
  "Three: read the question with the choices, and answer.",
  A("4 · Repeat 1–3 for every specific question appears", T('4 · Repeat 1–3 for every specific question', size=40, x=410, y=320, w=1140)),
  "Four: repeat one to three until you've finished all the specific questions.",
  A("5 · General questions last appears", T('5 · Finally — the general questions', size=40, x=410, y=390, w=1140)),
  "And at the end — the general questions. Don't forget them.",
 ]),
 dict(mode='concept', active=12, title='Tips', script=[
  "A few tips.",
  A("Connectors between paragraphs appears", T('Watch the connectors between paragraphs — they show each paragraph\'s role', size=36, x=410, y=110, w=1140)),
  "First, pay attention to connecting words between paragraphs. They show you the structure — the role of each paragraph.",
  A("Key sentence: usually the first appears", T('The key sentence is usually the first sentence of the paragraph', size=38, x=410, y=190, w=1140)),
  "Key sentences usually come first in each paragraph.",
  A("Short on time: first sentences (or first + last) appears", T('Short on time?  Read the first sentences — more time: first + last', size=38, x=410, y=270, w=1140)),
  "Pressed for time? Read just the first sentence of every paragraph — and you get a general idea of the passage and its structure.",
  "A bit more time? Read the first and last line of each paragraph.",
  A("Skipped a paragraph on the way? Skim it appears", T('Jumped over a paragraph on the way?  Skim it — don\'t skip it completely', size=36, x=410, y=350, w=1140)),
  "And if a question sent you to a line and you jumped over a whole paragraph on the way — don't skip it completely. Skim it, or read its first and last sentence, so you know its role.",
  "So — no special tricks here. Mainly a correct working technique. Let's practise it on a real passage.",
 ]),
], T49),

# ------------------------------------------------------------------ lesson: the practice passage
lesson('vr49-passage', 'Practice Passage', SB_PASSAGE, [
 dict(mode='title', title='Practice Passage', script=[
  "Let's practise a reading passage — and see how we apply everything we learned.",
 ]),
 dict(mode='concept', active=0, title='Three approaches', script=[
  "There are a few approaches.",
  A("1 · Question → passage appears", T('1 · Question → passage: read a question, go to its spot, answer, next', size=36, x=410, y=110, w=1140)),
  "The first — probably the most common: question, then passage. Read the question, go to the area it points to, read until you find the answer, move on.",
  "The questions follow the passage order, so bit by bit you read chunks of the passage — not all of it — and still get a pretty good picture. General questions: last.",
  A("2 · Read the whole passage, then the questions appears", T('2 · Read the whole passage first, then the questions', size=36, x=410, y=200, w=1140)),
  "The second: read the whole passage, then go to the questions. Many answers you'll know straight away; sometimes you'll go back.",
  A("slower — but more confident appears", T('a little slower · much more confident', size=32, x=410, y=260, w=1140)),
  "For many students it's a bit slower — though not by much. The advantage: you're much more confident in your answers. A small trade-off.",
  A("3 · First paragraph + first sentences, then question → passage appears", T('3 · First paragraph + first sentence of the others, then question → passage', size=36, x=410, y=330, w=1140)),
  "The third: read the first paragraph, then the first sentence of each other paragraph — a general picture — and then work question → passage.",
  "Try them out and check what works best for you. We'll solve this passage with the first approach.",
 ]),
 dict(mode='concept', active=1, title='Choices first?', script=[
  "One more decision: when you read the question — do you read the answer choices too, before going to the passage?",
  A("Long choices → question only, then the passage appears", T('Long choices → read only the question, then go to the passage', size=38, x=410, y=110, w=1140)),
  "There's no strict rule. It depends mainly on how long the choices are.",
  "Long choices — like in this passage — I don't read them first. I read the question, find the answer in the passage, then go back to the choices.",
  A("Very short choices → run through them, then the passage appears", T('Very short choices → run through them, then the passage', size=38, x=410, y=190, w=1140)),
  "Very short choices? I can run through them quickly and then jump to the passage.",
 ]),
 dict(mode='question', active=2, title='Paragraph 1', pre=[PSG(PID, [1])], script=[
  "Here's the passage — whoever wants can stop and read all of it. Working question → passage, we read it in pieces. Let's see what's in each paragraph.",
  D("Underline: \"the connection turned out to be a weak one\""),
  "Paragraph one: people believe exercise improves your emotional state — and the studies found a connection, but a weak one.",
  D("Bracket the Denmark sentence and write \"example\""),
  "Then an example — Denmark — and similar results in Canada and Japan.",
 ]),
 dict(mode='question', active=3, title='Paragraph 2', pre=[PSG(PID, [2])], script=[
  D("Circle the first sentence: \"Why does exercise exert so limited…\""),
  "Paragraph two opens with the key question: why is the effect so weak? That's the first sentence — the key sentence.",
  D("Underline \"Reference-point theory\" and \"peer hypothesis\""),
  "Answer number one: reference-point theory — we compare ourselves with those around us. And inside it, the peer hypothesis.",
 ]),
 dict(mode='question', active=4, title='Paragraph 3', pre=[PSG(PID, [3])], script=[
  D("Circle \"An alternative explanation\""),
  "Paragraph three — watch the connector: \"An alternative explanation\". That tells you its role: a second explanation.",
  D("Underline \"not mutually exclusive\""),
  "Habituation. And at the end: the two explanations are not mutually exclusive.",
 ]),
 dict(mode='question', active=5, title='Paragraph 4', pre=[PSG(PID, [4])], script=[
  D("Underline \"attempted to distinguish between the two explanations\""),
  "Paragraph four: a study that tried to decide between the two explanations.",
  D("Underline \"habituation accounts for most of the phenomenon\""),
  "Its conclusion: habituation explains most of it, comparison the rest.",
 ]),
 dict(mode='question', active=6, title='Paragraph 5', pre=[PSG(PID, [5])], script=[
  D("Circle \"Whatever the mechanism\""),
  "Paragraph five: \"Whatever the mechanism\" — a connector that says: here comes the bottom line.",
  D("Underline \"not for its emotional ones\""),
  "Exercise — recommend it for the body, not for the mood.",
 ]),
 dict(mode='concept', active=7, title='The solving order', script=[
  "Now the questions. Before solving — sort them. Where does each one send us?",
  A("Sentence \"In Denmark … temporary\" (paragraph 1) → specific appears", T('"In Denmark, for example … proved to be temporary" (paragraph 1) → specific', size=32, x=410, y=100, w=1140)),
  "The sentence question — paragraph one. Specific: on the exam it's a line question.",
  A("\"According to the second paragraph…\" → specific appears", T('"According to the second paragraph, why…" → specific (paragraph)', size=32, x=410, y=160, w=1140)),
  "\"According to the second paragraph\" — a paragraph question.",
  A("Dana, Michal and Noa … \"peer hypothesis\" → no reference appears", T('Dana, Michal and Noa … "peer hypothesis" → no reference · names not in the passage', size=32, x=410, y=220, w=1140)),
  "Dana, Michal and Noa — names! Are they in the passage? We haven't met them. Don't hunt: they're made up for the question. And it doesn't say \"according to the passage\" — so it's specific with no reference. The peer hypothesis sits in paragraph two.",
  A("\"According to the third paragraph…\" / \"…fourth paragraph…\" → specific appears", T('"According to the third paragraph…" · "According to the fourth paragraph…" → specific', size=32, x=410, y=280, w=1140)),
  "Third paragraph, fourth paragraph — paragraph questions.",
  A("\"What is the main conclusion…\" → general · last appears", T('"What is the main conclusion that arises from the passage?" → general · last', size=32, x=410, y=340, w=1140)),
  "And the main conclusion of the passage — a general question. It comes last, so we solve it last anyway.",
  "So we solve in the order of the passage: paragraph one, two, the no-reference question on paragraph two, three, four — and the general question at the end.",
 ]),
], T49),

# ------------------------------------------------------------------ guided questions on the passage
guided(0, 'vb-rc01-1', GQ, SB_Q, [
  "First question — a line question.",
  "It points to one sentence in the first paragraph.",
 ], [
  ('Read the sentence', [
   "Which of the following is closest in meaning to the sentence \"In Denmark, for example … proved to be temporary\"?",
   "The choices are long — so first, to the passage.",
  ], PS(1)),
  ('Start one sentence before', [
   "Start one sentence before: studies found a connection — but a weak one. Then the Denmark sentence is the example.",
   A("membership doubled · well-being did not rise · where it rose — temporary appears", P('Doubled → did NOT rise (mostly) → where it rose: temporary', size=32, y=230)),
   "Three parts: membership doubled; well-being did not rise in most cases; where it rose, it didn't last.",
   D("Cross out choice 1 — \"declined\" and \"slight\" aren't said"),
   "Choice one: well-being \"declined\", and the rise was \"slight\". Neither is said. Out.",
   D("Cross out choice 2 — \"rose accordingly\" is the opposite"),
   "Choice two: well-being rose \"accordingly\" — exactly what the sentence denies. Out.",
   D("Cross out choice 4 — \"did not report\" ≠ \"did not rise\""),
   "Choice four: Danes \"did not report\" on their well-being. The sentence says they reported — and it didn't rise. Out.",
   D("Circle choice 3"),
   "Doubled, did not rise, and where it rose it did not last. Choice 3.",
  ]),
 ], T49),
guided(1, 'vb-rc01-4', GQ, SB_Q, [
  "Question two — a paragraph question. Medium difficulty.",
 ], [
  ('Go to paragraph 2', [
   "According to the second paragraph, why does an improvement in fitness barely affect well-being?",
   "Long choices again. Read only the question — and go to the paragraph.",
   D("Underline \"His fitness has improved, but his position relative to his new reference group has … deteriorated\""),
   "Here it is, at the end of the paragraph: after joining a club, the group you compare yourself with changes — to experienced members who are fitter.",
   "Your fitness improved. Your position relative to the new group didn't.",
  ], PS(2)),
  ('Now the choices', [
   A("Fitness ↑ · relative position ↓ (new reference group) appears", P('Fitness improves — but the reference group changes, so the relative position doesn\'t', size=30, y=190)),
   D("Cross out choice 1 — the passage says he does NOT compare himself with athletes"),
   "Choice one: he compares himself with athletes he can't equal. The paragraph says the opposite — he's unlikely to measure himself against a professional athlete. Out.",
   D("Cross out choice 3 — reversed: it's the newcomer who compares"),
   "Choice three talks about how the experienced members see HIM. The paragraph is about whom HE compares himself with. Reversed. Out.",
   D("Cross out choice 4 — his fitness improved"),
   "Choice four: his fitness deteriorates. No — his fitness improved; his relative position didn't. Out.",
   D("Circle choice 2"),
   "His reference group changes, and his relative position is no better than before. Choice 2.",
  ]),
 ], T49),
guided(2, 'vb-rc01-3', GQ, SB_Q, [
  "Question three — an application question. Medium difficulty.",
  "Not \"pull a fact out of the passage\" — we need to understand an idea and apply it to a new case.",
 ], [
  ('Names and no reference', [
   "Dana, Michal and Noa train together at the same club. Dana and Noa attain similar results, and yet Noa envies Dana alone, not Michal. According to the peer hypothesis, what could be the reason?",
   A("Names not in the passage → don't hunt appears", P('Dana, Michal, Noa — not in the passage. Don\'t hunt for them.', size=30, y=250)),
   "Names we never met in the passage. Don't look for them — they're invented for the question.",
   A("No reference → bounded: paragraph 2 (the peer hypothesis) appears", P('No reference → the peer hypothesis: paragraph 2', size=30, y=310)),
   "No reference — but it mentions the peer hypothesis, which we met in paragraph two, between the questions we just solved.",
  ]),
  ('The hypothesis', [
   "Paragraph two: the more people regard others as their equals, the more they compare themselves with them.",
   D("Underline \"the more people regard others as their equals, the more they compare themselves with them\""),
   "So comparison — and envy — goes to the people you see as your equals.",
  ], PS(2)),
  ('Apply it', [
   A("Envy ← comparison ← \"my equal\" appears", P('Envy goes to whoever I see as my equal', size=32, y=250)),
   D("Cross out choice 2 — reverses the hypothesis"),
   "Choice two: Dana is NOT her equal, so she doesn't compare herself with her. But Noa DOES envy Dana. Reversed. Out.",
   D("Cross out choices 1 and 3 — not about whom Noa sees as her equal"),
   "Choices one and three — effort, what Michal has in common — they don't say whom Noa regards as her equal. Out.",
   D("Circle choice 4"),
   "In Noa's eyes, Dana is more her equal than Michal is. Choice 4.",
  ]),
 ], T49),
guided(3, 'vb-rc01-5', GQ, SB_Q, [
  "Question four — a NOT question. The hardest kind in this passage.",
  "Here's the method: check each choice against the paragraph. Every one that IS true — cross out.",
 ], [
  ('Mark what\'s true', [
   "According to the third paragraph, which of the following is NOT correct regarding the explanation from habituation?",
   D("Underline \"expectations advance in step with his achievements\""),
   D("Underline \"the distance between the two — which is what determines his satisfaction\""),
   D("Underline the runner sentence"),
   D("Underline \"The two explanations are not mutually exclusive\""),
   "Mark the relevant parts: expectations rise with achievements; satisfaction is the distance between them; the runner; and — not mutually exclusive.",
  ], PS(3)),
  ('Eliminate the true ones', [
   A("We want the one that is NOT correct appears", P('Looking for what is NOT correct: true statements are crossed out', size=30, y=190)),
   D("Cross out choice 1 — stated"),
   "Choice one: expectations rise together with achievements — stated. It's correct, so it's out.",
   D("Cross out choice 2 — stated"),
   "Choice two: satisfaction depends on the distance — stated. Out.",
   D("Cross out choice 4 — the runner"),
   "Choice four: the runner who's no longer satisfied with five kilometers — that's exactly the example. Out.",
   D("Circle choice 3"),
   "Choice three says habituation contradicts reference-point theory. The paragraph says the two are not mutually exclusive — they may even operate together. Not correct — choice 3.",
  ]),
 ], T49),
guided(4, 'vb-rc01-2', GQ, SB_Q, [
  "Question five — a paragraph question about an experiment. A hard one.",
  "The trap in these: choices that sound like the study, but go further than it.",
 ], [
  ('What did the study test?', [
   "According to the fourth paragraph, what did the researchers in the Netherlands conclude from the fact that the participants who trained alone showed no lasting improvement in well-being?",
   D("Underline \"If comparison were the whole explanation… should have reported a lasting improvement\""),
   "The logic: those who trained alone had no one to compare with. If comparison were the whole story, their improvement should have lasted.",
   D("Underline \"habituation accounts for most of the phenomenon, and comparison for the remainder\""),
   "It didn't last. So — habituation explains most of it.",
  ], PS(4)),
  ('The choices', [
   D("Cross out choice 1 — the hypothesis the result told against"),
   "Choice one: comparison is the whole explanation. That's exactly what the result weakened. Out.",
   D("Cross out choice 3 — not what the study measured"),
   "Choice three: training alone is less beneficial. Nobody said that — the study was about how long the improvement lasts. Out.",
   D("Cross out choice 4 — the researchers conceded it's uncertain"),
   "Choice four: those who trained alone compared themselves with no one. The researchers admit the opposite may happen — they may compare with friends outside the club. Out.",
   D("Circle choice 2"),
   "Habituation accounts for most of the phenomenon. Choice 2.",
  ]),
 ], T49),
guided(5, 'vb-rc01-6', GQ, SB_Q, [
  "Last question — the general one. A hard question.",
  "It's the last question, so it doesn't have to say \"according to the passage\". We left it for the end anyway.",
 ], [
  ('Use what you gathered', [
   "What is the main conclusion that arises from the passage?",
   "Do we need to read the whole passage now? No. We've read almost all of it on the way.",
   A("P1: a weak link · P5: recommend exercise for the body, not the mood appears", P('Paragraph 1: the link is weak · paragraph 5: exercise — for the body, not the mood', size=30, y=160)),
   "Paragraph one: the connection is weak. Paragraph five, the bottom line: recommend exercise for the body, not for the emotions.",
   D("Cross out choices 1, 2, 3 — each claims a strong link"),
   "Choices one, two and three each claim a strong relation — impossible to be both, only the fit can be content, contentment is a condition. Too strong. Out.",
   D("Circle choice 4"),
   "Fitness does not necessarily add to contentment. Choice 4.",
   "That's the method: specific questions in order, general questions at the end. That wraps up reading comprehension — and the verbal section as a whole.",
  ]),
 ], T49),
]

MEMORY = [
 dict(id='mem-rc-method', after='vr49-method', title='Reading comprehension — the working method',
  intro='6–7 minutes per passage, reading included: read only what the questions need.',
  tables=[dict(title='Question types', head=['Type', 'How to spot it', 'What to read'], rows=[
    ['Line', '"(lines 6–7)"', 'From one sentence before; several lines → just those'],
    ['Paragraph', '"According to the third paragraph…"', 'The paragraph — its idea'],
    ['No reference', 'No place given, no "according to the passage"', 'Between the question before and after'],
    ['General', '"according to the passage" (the last question may omit it)', 'Skip, mark, solve last — use what you gathered'],
   ]),
   dict(title='Steps', head=['#', 'Do this'], rows=[
    ['1', 'Read the question — without the choices'],
    ['2', 'Read the part of the passage it points to'],
    ['3', 'Read the question with the choices, and answer'],
    ['4', 'Repeat for every specific question, in order'],
    ['5', 'General questions last'],
   ])],
  tips=['Answer only from the passage, never from general knowledge.',
        'Questions follow the passage order — general questions can appear anywhere.',
        'A name you never met in the passage is probably invented for the question — don\'t hunt for it.',
        'Short on time: read the first sentence of each paragraph (or first + last).']),
]
