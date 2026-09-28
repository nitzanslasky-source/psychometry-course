# Verbal Reasoning · Topic 50 · Writing task - the WORKSHOP: an assignment after each key lesson, so that students
# build the whole essay step by step. The same three tasks (A, B, C) are carried from analysis through arguments,
# chains, paragraphs, rebuttals, openings and closings; D and E are used for skeletons and full essays.
#
# Each assignment = a card placed right after its lesson + a "Your turn" slide at the end of that lesson (or, where
# the lesson's sidebar is already full, a spoken pointer on its last slide). The slides are appended here to the
# lessons defined in modulesV50a-h (this file loads after them), so those files stay as they are.
from dsl import *
from writing_tasks import T as TASKS, WORKSHOP
import modulesV50b, modulesV50c, modulesV50d, modulesV50e, modulesV50f, modulesV50g, modulesV50h

T50 = 50
L = dict(zip('ABCDE', WORKSHOP))           # A social networks · B organ donation · C exams · D grades · E voting


def q(letter):
    return TASKS[L[letter]]['q'].replace(' Give reasons for your answer.', '')


def rows(letters):
    return [['Task %s' % x, q(x)] for x in letters]


ABC = rows('ABC')
CHECK = dict(title='Check yourself', head=['Question', 'Yes?'])

# ------------------------------------------------------------------ the assignments
WS = []   # (lesson id, number, title, slide lines, card)


def assign(after, n, title, intro, tables, tips, slide):
    """slide = short on-screen lines for the 'Your turn' slide."""
    card = dict(id='mem-wr-ws%02d' % n, after=after, title='Workshop %d · %s' % (n, title), intro=intro,
                tables=tables, tips=tips)
    WS.append((after, n, title, slide, card))


assign('vr50-b-hedging', 1, 'Academic English',
       'Rewrite each sentence in formal, hedged academic English. Keep the meaning; change the style.',
       [dict(title='Rewrite', head=['#', 'Sentence'], rows=[
           ['1', "Kids today are totally addicted to their phones and it's ruining everything."],
           ['2', 'Everybody knows that free buses will get rid of traffic jams.'],
           ['3', "You can't just let companies pay less tax, it's crazy."],
           ['4', 'In my opinion I think that the law will always protect children.'],
           ['5', "Isn't it obvious that exams are unfair to some students?"],
           ['6', 'Cameras on every street will stop all crime for sure.'],
       ]), dict(title='Check yourself (one possible answer)', head=['#', 'Academic version'], rows=[
           ['1', 'Many young people spend a great deal of time on their phones, which may affect their studies and relationships.'],
           ['2', 'Free buses are likely to reduce traffic congestion, at least in the city centre.'],
           ['3', 'Allowing large companies to pay a reduced rate of tax may be unfair to small businesses.'],
           ['4', 'In my opinion, the law is likely to protect children in many cases.'],
           ['5', 'Exams may be unfair to students who do not perform well under pressure.'],
           ['6', 'Cameras in public spaces may reduce crime in the monitored areas.'],
       ])],
       ['No contractions, slang, "you" or rhetorical questions.', 'Replace always / everybody / for sure with may, is likely to, many.'],
       ['Rewrite 6 informal sentences in academic English', 'Hedge the absolute claims', 'Then compare with the card'])

assign('vr50-c-grammar', 2, 'Grammar that changes meaning',
       'Each sentence has one mistake. Find it and fix it.',
       [dict(title='Find the mistake', head=['#', 'Sentence'], rows=[
           ['1', 'The cameras in the city centre reduces crime.'],
           ['2', 'If the law will pass, many teenagers will leave the networks.'],
           ['3', 'The people think that voting should be a right.'],
           ['4', 'This essay will discuss about the advantages of free buses.'],
           ['5', 'Students receive money for grades, this may lower their motivation.'],
           ['6', 'Since the fee is charged, patients will come to the emergency room less often.'],
       ]), dict(title='Check yourself', head=['#', 'Correct'], rows=[
           ['1', 'reduce (the subject is "the cameras")'],
           ['2', 'If the law passes (no "will" after "if")'],
           ['3', 'Many people think ... ("the people" = one specific group)'],
           ['4', 'discuss the advantages (no "about")'],
           ['5', '... for grades. This may ... / ..., which may ... (no comma splice)'],
           ['6', 'Once the fee is charged, ... ("since" here reads as a reason, not a time)'],
       ])],
       ['Read your own sentences for the same mistakes.'],
       ['Six sentences, one mistake each', 'Find it, fix it, check with the card'])

assign('vr50-c-organize', 3, 'Connectors',
       'Join each pair with a connector that shows the real relationship. Name the relationship first.',
       [dict(title='Join the pair', head=['#', 'Pair'], rows=[
           ['1', 'Free buses cost the city money. / Many cities have introduced them.'],
           ['2', 'Students hand in their phones. / They concentrate better in class.'],
           ['3', 'The fee may shorten waiting times. / Patients may stay at home when they are ill.'],
           ['4', 'Owners may rent to tourists. / It is their own home.'],
           ['5', 'Paying for grades may help. / It may teach students to learn only for a reward.'],
       ]), dict(title='Check yourself', head=['#', 'Relationship · a possible connector'], rows=[
           ['1', 'concession · Although free buses cost the city money, many cities have introduced them.'],
           ['2', 'result · Once students hand in their phones, they concentrate better; as a result, ...'],
           ['3', 'contrast · The fee may shorten waiting times; however, patients may stay at home ...'],
           ['4', 'condition · Owners may rent to tourists only if it is their own home.'],
           ['5', 'contrast · Paying for grades may help; on the other hand, it may teach ...'],
       ])],
       ['First the relationship, then the connector - never the other way round.'],
       ['Five pairs of sentences', 'Name the relationship', 'Then choose the connector'])

assign('vr50-d-development', 4, 'The missing link',
       'Each paragraph names a result but skips a step. Find the missing link and write the sentence that adds it.',
       [dict(title='Find the missing link', head=['#', 'Paragraph'], rows=[
           ['1', 'Raising the minimum age to 16 will protect teenagers. Therefore, their mental health will improve.'],
           ['2', 'Charging a fee in the emergency room is a good idea, because it will save lives.'],
           ['3', 'Compulsory voting is important, since the government will be better.'],
       ]), dict(title='Check yourself (one possible answer)', head=['#', 'The missing step'], rows=[
           ['1', 'Protect them from what? e.g. fewer hours exposed to bullying and to constant comparison with others -> less pressure -> better mental health.'],
           ['2', 'How? Non-urgent patients go to clinics -> shorter queues -> doctors see urgent cases sooner -> lives saved.'],
           ['3', 'Why better? Groups that rarely vote now vote -> politicians must address their needs -> policy reflects the whole population.'],
       ])],
       ['Ask after each sentence: "and how does that lead to the next one?"'],
       ['Three short paragraphs, each skips a step', 'Find the missing link', 'Write the missing sentence'])

assign('vr50-e-gather', 5, 'Analyse three tasks',
       'The workshop starts here. Tasks A, B and C (full texts in the card "Workshop tasks") will follow you through '
       'the next lessons: at the end you will have a whole essay for task A, and most parts of B and C.',
       [dict(title='Tasks', head=['Task', 'Question'], rows=ABC),
        dict(title='For each task, write down', head=['#', 'What'], rows=[
            ['1', 'The exact decision, the people affected, the conditions'],
            ['2', 'The type of task (yes/no, which method, degree, two parts ...)'],
            ['3', 'Background (facts) vs the sides\' claims (opinions): mark each sentence'],
            ['4', 'Key words that limit the question'],
        ])],
       ['About 3 minutes per task, as in the exam.', 'Keep your notes: you will use them in the next assignments.'],
       ['Tasks A, B, C: read and mark them', 'Decision · people · conditions · type', 'Background vs claims · key words'])

assign('vr50-e-args-intro', 6, 'Choose a position',
       'For each task, choose a first position (a leaning): the one you can argue best - not necessarily the one you feel '
       'strongest about. You may change it after workshop 7, once you have found and tested your arguments.',
       [dict(title='Tasks', head=['Task', 'Question'], rows=ABC),
        dict(title='For each task', head=['#', 'Write'], rows=[
            ['1', 'Your first position in one sentence (simple, or complex if you can keep its limit clear)'],
            ['2', 'The key consideration that decided it'],
            ['3', 'Is your position extreme? If so, soften it'],
        ])],
       ['Every position can score well if it is well argued.', 'This is a first position: confirm or change it after workshop 7.'],
       ['Tasks A, B, C: choose a first position', 'One sentence + the key consideration', 'You may change it after workshop 7'])

assign('vr50-e-test', 7, 'Find and test arguments',
       'For each task, find at least three arguments for your side, in the three ways. Then test them and keep the best two.',
       [dict(title='Tasks', head=['Task', 'Question'], rows=ABC),
        dict(title='Steps', head=['#', 'Do'], rows=[
            ['1', 'From the task: the arguments it gives (in your own words, explained)'],
            ['2', 'Who is involved, and how does it affect them - for better AND for worse?'],
            ['3', 'Points of view: go through all nine'],
            ['4', 'Test each: direct link · one breath · logical links'],
            ['5', 'Keep the best two; write each as one short sentence'],
        ])],
       ['About 5 minutes per task.', 'Different arguments = different reasons, not the same reason in other words.'],
       ['Tasks A, B, C: 3+ arguments each', 'From the task · who is involved · points of view', 'Test them, keep the best two'])

assign('vr50-f-chain-examples', 8, 'Chains',
       'Turn the two arguments you kept for each task into chains: about ten words each, from the thing the task asks about to the final result.',
       [dict(title='Tasks', head=['Task', 'Question'], rows=ABC),
        dict(title='For each chain', head=['#', 'Check'], rows=[
            ['1', 'Starts with the exact policy, ends with the benefit or harm'],
            ['2', 'Every arrow: "why would this lead to that?"'],
            ['3', 'Weak arrow? Add an explanation or a condition'],
            ['4', 'Renaming arrow? Merge the boxes'],
        ])],
       ['Six chains in all. Keep them: the next assignment turns them into paragraphs.'],
       ['Tasks A, B, C: two chains each', 'Test every arrow', 'Fix weak arrows, merge renaming ones'])

assign('vr50-f-template', 9, 'Argument paragraphs',
       'Write one argument paragraph for each task from your chains, using a different template each time.',
       [dict(title='Write', head=['Task', 'Paragraph'], rows=[
           ['A', 'Argument 1 · template A (development only)'],
           ['B', 'Argument 1 · template B (with an example)'],
           ['C', 'Argument 1 · template C (with a comparison)'],
       ]), dict(title='Check yourself', head=['Question', ''], rows=[
           ['Does the key sentence give the position and the reason?', ''],
           ['Is every arrow of the chain a sentence?', ''],
           ['Are the linking phrases varied (not "this will ... this will ...")?', ''],
           ['Does the closing link tie back to the position?', ''],
       ])],
       ['About 6-8 lines per paragraph.', 'Time yourself: about 6 minutes each.'],
       ['Tasks A, B, C: one argument paragraph each', 'Templates A, B and C', 'Check with the card'])

assign('vr50-f-comparison', 10, 'Support',
       'Go back to your paragraphs. Add support where it helps, and write the second argument paragraph for task A.',
       [dict(title='Write', head=['Task', 'Do'], rows=[
           ['A', 'Write argument 2 (with an example)'],
           ['B', 'Improve the example: specific, likely, and ending with a closing link'],
           ['C', 'Check the comparison: similar enough? the shared feature stated?'],
       ])],
       ['No invented studies, statistics or experts.'],
       ['Task A: argument 2', 'Tasks B, C: check the example and the comparison'])

assign('vr50-g-practising-weakenings', 11, 'The other side\'s chain',
       'For each task, write the strongest argument of the OTHER side as a chain. Find its weakest arrow and choose a weakening.',
       [dict(title='Tasks', head=['Task', 'Question'], rows=ABC),
        dict(title='For each task', head=['#', 'Write'], rows=[
            ['1', 'Their strongest argument, stated fairly'],
            ['2', 'Their chain (about ten words)'],
            ['3', 'The weakest arrow, circled'],
            ['4', 'The weakening type: mine matters more · a solution · what can go wrong · the reversal'],
        ])],
       ['Avoid weak weakenings: the short blanket, extremism, the slippery slope.'],
       ['Tasks A, B, C: their chain', 'Circle the weakest arrow', 'Choose the weakening type'])

assign('vr50-g-rebuttal-examples', 12, 'Rebuttal paragraphs',
       'Write the rebuttal paragraph for tasks A and B with the four-slot template.',
       [dict(title='Write', head=['Task', 'Paragraph'], rows=[['A', 'Rebuttal paragraph'], ['B', 'Rebuttal paragraph']]),
        dict(title='Check yourself', head=['Question', ''], rows=[
            ['Is their REASON stated, not just their side?', ''],
            ['Would they sign your description of their view?', ''],
            ['Does your answer hit their weakest arrow - their actual worry?', ''],
            ['Did you weaken rather than refute, with hedging?', ''],
        ])],
       ['About 6-8 lines each.'],
       ['Tasks A, B: a rebuttal paragraph each', 'Four slots', 'Check with the card'])

assign('vr50-g-bridging', 13, 'Bridging recommendations',
       'For each task, write a bridging recommendation of one or two sentences, and check it.',
       [dict(title='Tasks', head=['Task', 'Question'], rows=ABC),
        dict(title='Check yourself', head=['Question', ''], rows=[
            ['Does it answer the SAME worry?', ''], ['Does it say HOW it works?', ''],
            ['Is it genuine, not a bone thrown to the other side?', ''], ['Is the boundary coherent?', ''],
        ])],
       ['Optional in the exam - but practise it here.'],
       ['Tasks A, B, C: one bridging recommendation each', 'Same worry · how it works · coherent'])

assign('vr50-h-opening-tpl', 14, 'Opening paragraphs',
       'Write three opening paragraphs: one per task.',
       [dict(title='Write', head=['Task', 'Template'], rows=[
           ['A', 'Minimal template'], ['B', 'Rewrite template'], ['C', 'Your choice']]),
        dict(title='Check yourself', head=['Question', ''], rows=[
            ['Background · dispute · your position at the end?', ''],
            ['Segments of the task only - not the whole task word for word?', ''],
            ['No empty phrases?', ''], ['About 3-6 lines, 2-3 minutes?', ''],
        ])],
       ['Time each one: no more than 3 minutes.'],
       ['Tasks A, B, C: one opening each', 'Minimal · rewrite · your choice', '3 minutes each'])

assign('vr50-h-closing-tpl', 15, 'Closing paragraphs',
       'Write the closing paragraph for each task from the parts you already have.',
       [dict(title='Write', head=['Task', 'Template'], rows=[
           ['A', 'Benefits summary'], ['B', 'Essay summary'], ['C', 'Benefits summary']]),
        dict(title='Check yourself', head=['Question', ''], rows=[
            ['Same position as the opening?', ''], ['Benefits taken from your key sentences?', ''],
            ['No new argument?', ''],
        ])],
       ['Task A is now complete: opening, two arguments, rebuttal, closing.'],
       ['Tasks A, B, C: a closing each', 'Task A is now a whole essay'])

assign('vr50-h-skeleton', 16, 'Skeletons',
       'Two new tasks. For each, build the full skeleton in 10 minutes: analysis, position, two arguments with chains, the other side\'s chain and your weakening.',
       [dict(title='Tasks', head=['Task', 'Question'], rows=rows('DE'))],
       ['Set a timer: 10 minutes per skeleton.', 'Full texts in the card "Workshop tasks".'],
       ['Tasks D, E: a full skeleton each', '10 minutes per skeleton, with chains'])

assign('vr50-h-essay', 17, 'Whole essays',
       'Put it all together.',
       [dict(title='Write', head=['Task', 'Do'], rows=[
           ['A', 'Copy your parts into one essay on a 50-line sheet; improve the links between the paragraphs'],
           ['D', 'Write the whole essay from your skeleton: 25 minutes'],
           ['E', 'Whole essay, exam conditions: 35 minutes from reading the task'],
       ])],
       ['Count your lines: at least 25, about 30-40 is good.'],
       ['Task A: assemble the essay', 'Task D: 25 minutes from the skeleton', 'Task E: 35 minutes, exam conditions'])

assign('vr50-h-proofread', 18, 'Proofread',
       'Proofread essays A, D and E with the checklist. Mark every correction clearly, as you would in the exam.',
       [dict(title='Look for', head=['#', 'What'], rows=[
           ['1', 'Punctuation and comma splices'], ['2', 'Agreement and articles'], ['3', 'A missing "not"'],
           ['4', 'Repetition'], ['5', 'Missing connectors'],
       ])],
       ['2-3 minutes per essay.'],
       ['Essays A, D, E', 'Proofread with the checklist'])

assign('vr50-h-review', 19, 'Back to your first essay',
       'Write the four-day school week task again, in 35 minutes, and compare it with the essay you wrote before the lessons.',
       [dict(title='Compare', head=['Then', 'Now'], rows=[
           ['Position clear?', ''], ['Arguments explained step by step?', ''], ['The other side answered?', ''],
           ['Academic language?', ''], ['Length?', ''],
       ])],
       ['Then move on to the practice tasks.'],
       ['The four-day week task, again', '35 minutes', 'Compare with your first essay'])

TASK_CARD = dict(id='mem-wr-ws-tasks', after='vr50-e-gather', title='Workshop tasks',
                 intro='The five tasks used in the workshop assignments. A, B and C follow you through the lessons; D and E are for skeletons and whole essays.',
                 tables=[dict(title='Task %s · %s' % (x, TASKS[L[x]]['title']), head=['', ''],
                              rows=[[p, ''] for p in TASKS[L[x]]['paras']] + [[TASKS[L[x]]['q'], '']]) for x in 'ABCDE'],
                 tips=['Real tasks look like these: 2-3 paragraphs - the situation, the change, both sides - then the question.'])

# ------------------------------------------------------------------ "Your turn" slides on the lessons
LESSONS = {m['id']: m for mod in (modulesV50b, modulesV50c, modulesV50d, modulesV50e, modulesV50f, modulesV50g,
                                  modulesV50h) for m in mod.MODULES}
for after, n, title, lines, card in WS:
    m = LESSONS[after]
    say = ["Your turn: workshop %d, %s. It's in the card right after this lesson." % (n, title.lower())]
    if len(m['sidebar']) < 13 and not any(s.get('title') == 'Workshop %d' % n for s in m['slides']):
        label = 'Workshop %d' % n
        m['sidebar'] = m['sidebar'] + [label]
        script = [say[0],
                  A('Workshop title', T('Workshop %d · %s' % (n, title), size=46, x=410, y=110, w=1140))]
        y = 220
        for i, l in enumerate(lines):
            script.append(A('Step %d' % (i + 1), T('%d · %s' % (i + 1, l), size=36, x=440, y=y, w=1100)))
            y += 90
        script.append(A('Why', T('Do it before the next lesson: each assignment builds on the one before', size=30,
                                 x=410, y=y + 30, w=1140)))
        script += ["Do it before you move on. Each assignment builds on the one before, and by the end of the lessons you'll have written whole essays."]
        m['slides'].append(dict(mode='concept', active=len(m['sidebar']) - 1, title=label, script=script))
    else:
        m['slides'][-1]['script'] = m['slides'][-1]['script'] + say

MODULES = []
MEMORY = [c for *_, c in WS[:4]] + [WS[4][4], TASK_CARD] + [c for *_, c in WS[5:]]   # the task texts right after workshop 5, which introduces them
