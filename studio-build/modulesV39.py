# Verbal Reasoning · Topic 39 · Active reading.
# No Hebrew subtitles and no bank category for this topic: the course's own lesson and guided questions,
# converted to the hybrid whiteboard format (same teaching points, same order, same questions).
from dsl import *

TOPIC = 39
SB = ['Small picture', 'Pause at the full stop', 'Keep control words', 'Give it a voice', 'Tiny visuals',
      'Circle the turn', 'Who owns the view?', 'Predict, then check', 'Margin labels', 'Unfamiliar words',
      'Match the technique', 'Accuracy, then speed']

def C(t, size=40): return T(t, size=size)

MODULES = [
lesson('vr39-active-reading', 'Active Reading', SB, [
 dict(mode='title', title='Active Reading', script=[
  "Active reading.",
  "Before any question type — the one skill that sits under all of verbal reasoning.",
  "Reading so the meaning builds up in your head as you go.",
 ]),
 dict(mode='concept', active=0, title='Small picture', script=[
  "Think about a message from a friend: 'The café is closed, so meet me at the library.'",
  "You don't memorize the words. You instantly picture a changed plan.",
  A("Who or what? · What changed? · How does this sentence connect? appears", C('Who or what? · What changed? · How does this connect?')),
  "That's the habit we want on an unfamiliar exam paragraph. Build a small, accurate picture as the sentences arrive.",
  "Slowly at first. Speed comes from not having to start again.",
  A("About a minute per short question — a training target, not a rule appears", C('About a minute per short question — a training target, not a rule', 34)),
  "A minute per short question is a good training target. Longer passages share their time across several questions.",
 ]),
 dict(mode='concept', active=1, title='Pause at the full stop', script=[
  "At the end of each sentence — a tiny pause. Say its message in your own words.",
  A("The council increased parking fees, but traffic did not fall. appears", C('The council increased parking fees, but traffic did not fall.')),
  D("Underline 'increased' and 'did not fall'"),
  A("My words: parking cost more; traffic stayed about the same. appears", C('My words: parking cost more; traffic stayed about the same.')),
  "That's enough. Not a second essay — just a check that there's a thought in my head.",
  "If your version is the original with two words swapped — ask what you'd tell a younger sibling.",
  "Long sentence with several clauses? Pause at a meaningful comma instead.",
 ]),
 dict(mode='concept', active=2, title='Keep control words', script=[
  "Shorter must still mean the same thing.",
  A("Some ≠ all appears", C('Some ≠ all')),
  "'Some visitors disliked the exhibition' — not 'visitors disliked it'. Don't let 'some' turn into everyone.",
  A("May ≠ must appears", C('May ≠ must')),
  "'The treatment may help' doesn't promise it will.",
  A("Not lower ≠ higher appears", C('Not lower ≠ higher')),
  "A price that did not fall might have stayed the same. It didn't necessarily rise.",
  "These little words are often the whole reason one answer is right and another is wrong.",
  "Cut decoration, never logical limits. Two researchers? Give them two labels.",
 ]),
 dict(mode='concept', active=3, title='Give it a voice', script=[
  A("Although the plan was CHEAPER, it took LONGER. appears", C('Although the plan was CHEAPER, it took LONGER.')),
  "Read it like a bedtime story to a younger sibling. Lean on 'cheaper' and 'longer'.",
  D("Circle 'Although'"),
  "Hear the little disappointment? We expected one advantage to bring another — it didn't.",
  A("Because the plan was cheaper, it was chosen. appears", C('Because the plan was cheaper, it was chosen.')),
  "Now the second part sounds like a result. The words steer your voice: contrast, then reason and result.",
  "It's a way to notice structure — not permission to invent the writer's feelings.",
 ]),
 dict(mode='concept', active=4, title='Tiny visuals', script=[
  A("Taxes ↑ · Shop visits ↓ appears", C('Taxes ↑ · Shop visits ↓')),
  "Taxes increased — a small up arrow. Visits fell — a down arrow. Right beside the thing that changed.",
  A("After ≠ because appears", C('After ≠ because')),
  "Visits fell after taxes rose. I can draw the order in time — but not a proven causal arrow.",
  "'After' gives an order. It doesn't explain why.",
  "This matters later — strengthening, weakening, scientific reasoning. Mark what the writer said, and what the writer didn't establish.",
 ]),
 dict(mode='concept', active=5, title='Circle the turn', script=[
  "Don't underline half the paragraph. Mark the words that show how the parts fit together.",
  A("However → a turn · Because → a reason · For example → an illustration appears", C('However → a turn · Because → a reason · For example → an illustration', 36)),
  "They're clues, not a replacement for meaning. Two sentences can disagree without 'however'.",
  "A small bend beside a contrast. 'Example' beside an illustration.",
  "If your page starts to look like a coloring book — stop. A few marks read faster than a page of ink.",
 ]),
 dict(mode='concept', active=6, title='Who owns the view?', script=[
  A("Critic: the design is impressive. · Engineer: the design is impractical. appears", C('Critic: impressive. · Engineer: impractical. · Writer: reports both.')),
  "Both can be true — appearance and usefulness are different questions.",
  "And the writer may only be reporting them.",
  D("Write C beside the critic and E beside the engineer"),
  "When you meet 'she', 'this view', 'such an approach' — point back to its owner.",
  "Don't give the writer an opinion just because the writer quoted one. Questions love asking whose claim is whose.",
 ]),
 dict(mode='concept', active=7, title='Predict, then check', script=[
  "Once you understand a sentence, ask what kind of sentence might come next.",
  A("Useful but limited → expect a qualified conclusion appears", C('Useful but limited → expect a qualified conclusion')),
  "A method that's useful but limited — I expect an example of its use, or an explanation of its limits.",
  "That keeps me alert. It is not a licence to finish the paragraph in my imagination.",
  "If the text turns somewhere else — I update the picture. The text supplies the evidence.",
 ]),
 dict(mode='concept', active=8, title='Margin labels', script=[
  "After each paragraph — a short label for its job.",
  A("¶1 an old explanation · ¶2 evidence against it · ¶3 a more cautious account appears", C('¶1 an old explanation · ¶2 evidence against it · ¶3 a more cautious account', 34)),
  "Three paragraphs may all be about birds — but one sets a puzzle, one describes a test, one limits the conclusion.",
  "'Birds again' misses the structure.",
  "These labels are your map in reading comprehension: jump straight to the paragraph that does the job.",
 ]),
 dict(mode='concept', active=9, title='Unfamiliar words', script=[
  "A word you don't know? First ask — do I need its exact meaning?",
  A("Keep its role if the exact meaning isn't needed appears", C("Keep its role if the exact meaning isn't needed")),
  "'The device is expensive but reliable' — 'the device' may be all you need.",
  A("Use context cautiously · return if it decides an answer appears", C('Use context cautiously · return if it decides an answer')),
  "But if an analogy hinges on reluctant versus unwilling — vocabulary is the whole question. Be careful.",
  "Context can suggest a meaning. Don't turn a guess into a fact.",
 ]),
 dict(mode='concept', active=10, title='Match the technique', script=[
  "The same habit looks a little different in each topic.",
  A("Analogy → define the relationship appears", C('Analogy → define the relationship')),
  A("Logic → keep condition → result appears", C('Logic → keep condition → result')),
  A("Argument → separate evidence from conclusion appears", C('Argument → separate evidence from conclusion')),
  A("Passage → label roles, return to evidence appears", C('Passage → label roles, return to evidence')),
  "You don't do everything on every sentence. Choose the smallest action that makes the meaning clear.",
 ]),
 dict(mode='concept', active=11, title='Accuracy, then speed', script=[
  A("First: read → paraphrase → check appears", C('First: read → paraphrase → check')),
  "Start untimed. Did you lose an 'only'? Did 'some' become 'all'? Did a possible cause become a proven one?",
  A("Next: read → tiny mental paraphrase appears", C('Next: read → tiny mental paraphrase')),
  "Then shorten the pause until it's almost automatic.",
  A("Finally: time a short set and review the errors appears", C('Finally: time a short set and review the errors')),
  "Review more than the score — ask where the meaning changed in your head. Fix the real source of delay.",
 ]),
], TOPIC),

guided(0, 'vr39-g001', 'Active Reading Questions', ['Question 1', 'Question 2'],
 ["Let's put it to work."],
 [('Three facts, three notes', [
   "A town reduced bus fares. Passenger numbers rose — but the number of cars entering the centre stayed the same.",
   D("Write ↓ beside 'reduced bus fares', ↑ beside 'Passenger numbers rose', = beside 'remained unchanged'"),
   "Fares down. Passengers up. Cars — the same. Much easier to hold than the full wording.",
   D("Underline 'necessarily true'"),
   A("Necessarily true = what the text commits us to appears", P('Necessarily true = what the text commits us to')),
   "We want what the text commits us to — not the most interesting explanation.",
  ]),
  ('"But" is doing work', [
   D("Circle 'but'"),
   "The 'but' tells us the obvious story — cheaper buses, fewer cars — isn't in the figures.",
   D("Cross out choice 1"),
   "Choice one: the extra passengers used to drive. Never stated. Out.",
   D("Cross out choice 2"),
   "Choice two: nobody changed. Too far the other way — some drivers may have switched while others started driving in.",
   D("Cross out choice 4"),
   "Choice four: the fares caused drivers to leave their cars. A cause the text never established.",
   D("Circle choice 3"),
   "Choice 3. More people used buses — the text says so directly.",
  ])]
, TOPIC),

guided(1, 'vr39-g002', 'Active Reading Questions', ['Question 1', 'Question 2'],
 ["Question two — who holds which opinion?"],
 [('Agreement, then the turn', [
   "Mara calls the archive valuable — it preserves ordinary people's letters.",
   "Theo agrees the letters are worth keeping — but says the catalog makes them hard to find.",
   D("Write M: keep the letters · T: yes, but fix access"),
   A("Theo: agrees on the letters · criticizes the catalog appears", P('Theo: agrees on the letters · criticizes the catalog')),
   "Read 'agrees' with a small nod. Let your voice turn at 'but'.",
   "If you shrink Theo to 'he dislikes the archive', you erase the agreement — and walk right into a distractor.",
  ]),
  ('Choose the matching answer', [
   D("Cross out choice 3"),
   "Choice three — he rejects Mara's view about the letters? No, he agrees with it. Out.",
   D("Cross out choices 1 and 4"),
   "One and four invent claims — 'always easy to find', 'the catalog is more valuable'. Nobody said that.",
   D("Circle choice 2"),
   "Choice 2. He values the material but criticizes how it's organized.",
   "Two named thinkers? Write down the exact point where they differ.",
  ])]
, TOPIC),
]

MEMORY = [
 dict(id='mem-active-reading', after='vr39-active-reading', title='Active reading — words that control the claim',
  intro='Shorten the sentence, never its logic.',
  tables=[dict(title='Keep the limits', head=['Text says', 'Does NOT mean'], rows=[
    ['some', 'all'], ['may / might', 'must / will'], ['did not fall', 'rose'], ['after', 'because'],
    ['X reports a view', 'the writer holds it']]),
   dict(title='Signal words', head=['Word', 'Job'], rows=[
    ['however · but · although · yet', 'a turn / contrast'], ['because · since · as', 'a reason'],
    ['so · therefore · thus', 'a result'], ['for example · for instance', 'an illustration']])],
  tips=['Pause at every full stop: say it in your own words.', 'Arrows beside the thing that changed.',
        'Label each paragraph by its job, not its subject.']),
]
