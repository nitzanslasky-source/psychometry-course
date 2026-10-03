# Verbal Reasoning · Topic 50 · Writing task - summary lesson, right before the practice tasks.
# CUT from the course (teacher, 2026-10-03): MODULES is empty. Its 'Before you write' questions are now a checklist
# on the practice-tasks card (mem-wr-practice, modulesV50h). The lesson is kept below as _CUT only for reference.
# Only what parts A-H teach (the cards of each part are the reference); nothing new.
from dsl import *

T50 = 50


def rows(items, y=60, size=32, gap=30, x=410, w=1140):
    """Stack text items down the board (estimates wrapped height) -> list of A(label, T)."""
    out = []
    for label, text, *z in items:
        s = z[0] if z else size
        out.append(A(label, T(text, size=s, x=x, y=y, w=w)))
        n = max(1, -(-int(len(text) * 0.52 * s) // w))
        y += int(n * s * 1.3) + gap
    return out


def slide(i, title, lines, items, **k):
    """lines: spoken lines, spoken one after each item (extra lines at the end)."""
    its = rows(items, **k)
    script = []
    for j, it in enumerate(its):
        script.append(it)
        if j < len(lines): script.append(lines[j])
    script += lines[len(its):]
    return dict(mode='concept', active=i, title=title, script=script)


SB = ['The task in numbers', 'The two rubrics', 'Analyse the task', 'Find arguments', 'The chain',
      'Argument paragraph', 'Rebuttal paragraph', 'Opening & closing', 'Structure & timing', 'Academic English',
      'Before you write']

_CUT = [
lesson('vr50-i-summary', 'Writing Task: Summary', SB, [
 dict(mode='title', title='Summary', script=[
  "Before you start writing practice tasks, a quick review of everything we learned about the writing task.",
  "One idea per slide. If something doesn't ring a bell, go back to its lesson or its card.",
 ]),
 slide(0, 'The task in numbers', [
  "One task, 35 minutes.",
  "At least 25 lines, at most 50, only on the lines of the answer sheet. Good essays are usually about 30 to 40 lines.",
  "Two raters, each gives content and language a mark from 1 to 6. Together: 4 to 24.",
  "And it's a quarter of your Verbal score. Worth the work.",
 ], [
  ('35 minutes', '35 minutes · one task · your opinion + reasons', 40),
  ('Lines', '25 lines minimum · 50 maximum · good essays: about 30-40 lines', 36),
  ('Raters', '2 raters × (content 1-6 + language 1-6)  =  4-24', 36),
  ('Weight', 'The essay = 25% of the Verbal Reasoning score', 36),
 ]),
 slide(1, 'The two rubrics', [
  "Content: do you answer the exact question, develop your ideas, stay focused, and think critically: fact versus opinion, other perspectives, the opposing view.",
  "Language: clear academic style, precise words, correct grammar, varied sentences, and organizing tools: connectors, transitions, paragraphs.",
  "Raters know it's a first draft. A few slips are fine. Unclear reasoning is not.",
 ], [
  ('Content', 'CONTENT: relevance to the task · development · focus and coherence · critical thinking', 34),
  ('Language', 'LANGUAGE: academic style and clarity · precise words · grammar · sentence variety · connectors, transitions, paragraphs', 34),
  ('First draft', 'It is read as a first draft: small slips are fine, unclear reasoning is not', 34),
 ]),
 slide(2, 'Analyse the task', [
  "First, analyse. What exactly is being decided, who is affected, and under what conditions? Answer every part of the question.",
  "Then gather: the background goes to the opening paragraph, the claims of both sides are raw material for arguments.",
  "Choose a first position. Start from what you really think. But if the other side is much easier to explain, switching is completely legitimate: the raters score how well you argue, not what you believe. Confirm or change it after you find your arguments.",
 ], [
  ('Exact question', 'The exact decision · the people affected · the conditions · every part of the question', 34),
  ('Gather', 'Background → opening paragraph · the sides\' claims → material for arguments', 34),
  ('Position', 'A first position: start from what you think; switch if the other side is much easier to explain. Confirm it after finding arguments', 34),
 ]),
 slide(3, 'Find arguments', [
  "Three ways to find arguments. One: from the task. Use its arguments, but not only them, not word for word, and explain them well.",
  "Two: who is involved, and how does it affect them? For each player, for better and for worse.",
  "Three: points of view. Social-economic, psychological, educational, moral, democracy, rights, safety, environment, science and progress.",
  "Then test every argument: a direct link to the question, simple enough to say in one breath, and logical links all the way.",
 ], [
  ('From the task', '1 · From the task: not only, not word for word, explained', 34),
  ('Who', '2 · Who is involved, and how? For better AND for worse', 34),
  ('Points of view', '3 · Points of view: social-economic · psychological · educational · moral · democracy · rights · safety · environment · progress', 32),
  ('Test', 'Test: direct link · one breath · logical links (the chain)', 36),
 ]),
 slide(4, 'The chain', [
  "For every argument, draft a chain: from the thing the task asks about, step by step, to the final result. About ten words.",
  "Test every arrow: why would this step lead to the next? A weak arrow needs an explanation or a condition.",
  "No arrows that just rename the same step. And do the same for the other side: its weakest arrow is your weakening.",
 ], [
  ('Chain', 'the policy → step → step → the result   (about 10 words per argument)', 36),
  ('Why', 'Every arrow: "Why would this lead to that?"  Weak → explain it or add a condition', 34),
  ('Checks', 'No renaming arrows · don\'t sound pasted · chain the other side too', 34),
 ]),
 slide(5, 'Argument paragraph', [
  "The argument paragraph: key sentence with your position and the reason.",
  "Then the chain, each arrow a sentence, with varied linking phrases: once, this in turn, as a result, which means that.",
  "Support if you have room: a likely example or a fair comparison. Never invented studies or numbers.",
  "And a closing link back to your position.",
 ], [
  ('Key sentence', '1 · Key sentence: In my opinion, [X] should [...], since it would [result].', 32),
  ('Chain', '2 · The chain: Once ..., ... because ... · This, in turn, ... · As a result, ...', 32),
  ('Support', '3 · Support (optional): For example, a ... who ... would probably ... · A similar pattern can be seen in ...', 32),
  ('Closing link', '4 · Closing link: In this way, ... · In the same way, ... · Just as ..., so ...', 32),
 ]),
 slide(6, 'Rebuttal paragraph', [
  "The rebuttal paragraph: state the other side's reason fairly, the way they would sign it.",
  "Develop their chain, find the weakest arrow, and answer exactly there: mine matters more, a solution, what can go wrong, or the reversal.",
  "Weaken, don't refute. Hedge.",
  "And if you like, a bridging recommendation: a small, specific step that eases the same worry, and says how.",
 ], [
  ('Their view', 'On the other hand, some argue that ... since ...   (their REASON, fairly)', 32),
  ('Weakening', 'However, ... → at their weakest arrow: mine matters more · a solution · what can go wrong · the reversal', 32),
  ('Hedge', 'Weaken, don\'t refute: may, is likely to, many', 32),
  ('Bridging', 'Nevertheless, since [their worry] is a legitimate concern, [measure] could be introduced, so that ...', 32),
 ]),
 slide(7, 'Opening & closing', [
  "The opening comes from the task: the background, the dispute, and your position at the end. Short. Copying segments of the task is fine, but not the whole task word for word.",
  "The closing comes from your essay: your position and your reasons. No new argument.",
  "Never skip the closing. No time? One line.",
 ], [
  ('Opening', 'Opening: background → the dispute → your position (at the end). 2-3 minutes', 34),
  ('Closing', 'Closing: In conclusion, [position], since [benefit 1], and also because [benefit 2].', 34),
  ('Never skip', 'No time? In conclusion, [position], since, as shown above, its advantages outweigh its disadvantages.', 32),
 ]),
 slide(8, 'Structure & timing', [
  "The recommended structure: opening, two argument paragraphs, rebuttal, closing. A tool, not a rule: each paragraph has one job.",
  "The plan: ten minutes to plan with a skeleton and chains, then write, and two to three minutes at the end to proofread.",
 ], [
  ('Structure', 'Opening · Argument 1 (your ace) · Argument 2 · Rebuttal · Closing', 36),
  ('Timing', '0-10 plan (skeleton + chains) · 10-13 opening · 13-19 arg. 1 · 19-25 arg. 2 · 25-31 rebuttal · 31-33 closing · 33-35 proofread', 32),
 ]),
 slide(9, 'Academic English', [
  "Language. Formal and calm: no contractions, no slang, no 'you', no rhetorical questions, no emotional appeals.",
  "Hedge your predictions: may, is likely to, many. Not always, everyone, never.",
  "Precise words, and the same term for the same thing.",
  "Choose the connector that matches the relationship: cause, result, contrast, condition. A connector signals a link, it doesn't create one.",
  "And watch the classics: 'In my opinion I think', 'according to me', 'discuss about'.",
 ], [
  ('Register', 'Formal: no contractions · no slang · no "you" · no rhetorical questions · no emotion', 32),
  ('Hedging', 'Hedge: may · is likely to · in many cases   (not: always · everyone · never)', 32),
  ('Precision', 'Precise words · the same term for the same thing · simple and correct beats fancy', 32),
  ('Connectors', 'Connector = the real relationship: because · as a result · however · provided that', 32),
  ('Classics', '✗ In my opinion I think · ✗ according to me · ✗ discuss about', 32),
 ]),
 slide(10, 'Before you write', [
  "Before you practise, the questions to always ask yourself.",
  "Am I answering the exact question, every part of it?",
  "Does every arrow in my chain hold? Why would this lead to that?",
  "Did I give the other side its real reason, and answer its actual worry?",
  "Does every paragraph do one job, and does the closing follow from the body?",
  "Did I leave two to three minutes to proofread, especially for a missing 'not'?",
  "Now take the practice tasks. Set a timer for 35 minutes, draft your chains first, and check yourself with the cards. Good luck.",
 ], [
  ('Q1', '✓ Am I answering the exact question, every part of it?', 34),
  ('Q2', '✓ Does every arrow hold? "Why would this lead to that?"', 34),
  ('Q3', '✓ Did I state the other side\'s real reason and answer its actual worry?', 34),
  ('Q4', '✓ One job per paragraph? Does the closing follow from the body?', 34),
  ('Q5', '✓ 2-3 minutes to proofread: punctuation, agreement, a missing "not"', 34),
 ], y=50, gap=14),
], T50),
]

MODULES = []
MEMORY = []
