# Verbal Reasoning · Topic 50 · Writing Task · Part E: planning - analysing the task and finding arguments.
# Backbone: the teacher's Hebrew lessons, writing_src/seg20-seg28 (task analysis, gathering information from the
# prompt, considerations for choosing a position, introduction to finding arguments, rights, zoom out, zoom in,
# the reduced-tax example, evaluating arguments). Official English facts from nite_verbal_guide.txt; findings.md
# points 1-2 (the exact decision, population and every part of the question) are added where the task is analysed.
# The teacher's running examples (face-recognition cameras, reduced tax for large companies) are translated and kept;
# every other example is original.
import math
from dsl import *
from writing_assets import prompt_box, EXAMPLE_PROMPT, EXAMPLE_QUESTION, vis, _text

T50 = 50


class Col:
    """Stacks text items down the board so nothing overlaps (estimates the wrapped height of each item)."""
    def __init__(self, y=60, x=410, w=1140, gap=22):
        self.y, self.x, self.w, self.gap = y, x, w, gap

    def __call__(self, text, size=34, gap=None, x=None, w=None):
        x = self.x if x is None else x
        w = self.w if w is None else w
        item = T(text, size=size, x=x, y=self.y, w=w)
        rows = max(1, math.ceil(len(text) * 0.52 * size / w))
        self.y += int(rows * (size * 1.25 + 5)) + (self.gap if gap is None else gap)
        return item

    def skip(self, h):
        self.y += h


def box(lines, question, y=60, w=1140):
    """The boxed task (prompt_box) placed on the board; returns (item, bottom y)."""
    it = dict(prompt_box(lines, question, w=w), x=410, y=y)
    return it, y + it['h']


# ---- the teacher's running example: face-recognition cameras (translated) ----
CAM_BACKGROUND = [
    'In recent years, officials in the security services have been promoting',
    'a bill to set up a national network of face-recognition cameras in public',
    'spaces. Since today\'s technology can identify people and objects in real',
    'time with a high degree of certainty, it would be possible to identify any',
    'person, vehicle or other object caught on camera, provided that their image',
    'already exists in the database. This information would help to fight',
    'criminal and security offences that harm the population, since suspicious',
    'activity could be identified before an offence is committed, illegal',
    'activity could be stopped while it is taking place, and offenders could be',
    'caught after the event.',
]
CAM_CLAIMS = [
    'Supporters of this step claim that such a system would reduce, and even',
    'completely eliminate, criminal and security incidents in monitored areas.',
    'Opponents believe that such a step would seriously harm privacy, and that it',
    'is unthinkable for the security services to be able to follow our every step.',
]
CAM_PROMPT = CAM_BACKGROUND + CAM_CLAIMS
CAM_Q = ('In your opinion, should the security services be allowed to install '
         'face-recognition cameras in public spaces? Give reasons.')


def marked_box(parts, question, w=1140, x=410, y=60):
    """The camera task with its parts coloured: parts = [(lines, colour, bold?), ...]."""
    W = 820; yy = 40; b = []
    for lines, colour, bold in parts:
        for s in lines:
            b.append(_text(30, yy, s, 17, 700 if bold else 400, colour)); yy += 27
    yy += 8
    words, cur, qs = question.split(), '', []
    for wd in words:
        if len(cur) + len(wd) + 1 > 80 and cur: qs.append(cur); cur = wd
        else: cur = (cur + ' ' + wd).strip()
    qs.append(cur)
    for q in qs:
        b.append(_text(30, yy, q, 17, 700)); yy += 26
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="Writing task, marked">'
           '<title>Writing task, marked</title><rect x="1" y="1" width="%d" height="%d" fill="#fff" stroke="#1f2937" '
           'stroke-width="2"/>%s</svg>') % (W, yy, W - 2, yy - 2, ''.join(b))
    it = vis(svg, w=w, h=int(w * yy / W))
    return dict(it, x=x, y=y), y + it['h']


BLUE, GREEN, INK = '#2F6BFF', '#0F9D58', '#1f2937'

# ---- the teacher's second example: reduced tax for large companies (background lines are original) ----
TAX_PROMPT = [
    'Many countries compete to attract large companies, which bring factories,',
    'jobs and investment. Some governments therefore offer large companies a',
    'reduced rate of tax. Supporters say that this creates jobs and strengthens',
    'the economy. Opponents argue that it is unfair for the richest firms to pay',
    'less tax than small businesses and ordinary citizens.',
]
TAX_Q = 'In your opinion, should the state charge large companies a reduced rate of tax? Give reasons.'

# ---- an original two-part question (every part of the question needs an answer) ----
BUS_PROMPT = [
    'Several cities have made buses and trams free for everyone. They say that',
    'free public transport reduces traffic and helps families on low incomes.',
    'Critics point to the cost to the city budget and to crowded vehicles.',
]
BUS_Q = ('In your opinion, what are the advantages and disadvantages of free public transport, '
         'for city residents and for the city itself? Give reasons.')
# one shared version of every task (writing_tasks.py, shaped like the real English tasks)
from writing_tasks import T as _T, split_task_slides
CAM_PROMPT, CAM_Q = _T['camera']['paras'], _T['camera']['q']
from writing_assets import _wrap
CAM_BACKGROUND = _wrap(' '.join(CAM_PROMPT[:2]), 80)   # the marked version: background (facts) ...
CAM_CLAIMS = _wrap(CAM_PROMPT[2], 80)                    # ... and the two sides' claims
TAX_PROMPT, TAX_Q = _T['tax']['paras'], _T['tax']['q']
BUS_PROMPT, BUS_Q = _T['bus2']['paras'], _T['bus2']['q']


# =====================================================================================================================
def _analyse():
    s = []
    c = Col(y=60)
    it, bottom = box(CAM_PROMPT, CAM_Q, y=40, w=1000)
    s.append(dict(mode='concept', active=0, title='First: analyse', script=[
        "When we sit down to write an essay, the first thing we do is not write.",
        "The first thing we do is analyse the task.",
        A('The camera task appears', it),
        "Here's the example task we already know: face-recognition cameras in public spaces.",
        "Stop the video for a moment if you need to, and read it again.",
        A('Analyse before you write appears', T('Analyse the task before you write a single line', size=38, x=410, y=bottom + 30, w=1140)),
        "So how do we analyse it? With a few fixed questions. Let's go through them one by one.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=1, title='Same or different aim?', script=[
        "The first question: is the interest the same, or different?",
        A('Why are you arguing? appears', c('Ask the two sides: "Why are you arguing? What do you want?"', 40)),
        "It's as if we walk up to the two sides and ask them: why are you arguing? What's the goal?",
        A('Same aim, different ways appears', c('Same aim → they want the same thing, each in a different way', 34)),
        "Maybe they want the same thing, and each wants to reach it in a different way. A common goal. A similar interest.",
        A('Different aims appears', c('Different aims → each side looks after its own interest', 34)),
        "Or maybe each side has a different interest, and each one is looking after itself.",
        A('Cameras: different appears', c('Cameras: the state wants security; people want privacy → different interests', 34, gap=40)),
        "Our cameras. Why are you arguing? The state wants to look after security. People want to protect their privacy.",
        "So here the interests are different.",
        A('Minister task appears', c('"Should a minister be an expert in the field, or an elected public representative?"', 34)),
        "Now another task. Should a minister be an expert in the ministry's field, or an elected public representative?",
        "One says: an expert! The other says: no way, an elected representative! Wait, wait. What do you both want?",
        A('Minister: same aim appears', c('Both want an effective minister → same aim, different ways', 34)),
        "You both want the minister to be effective, to do the job as well as possible. You're not enemies. You're friends with a common goal.",
        "Each of you just thinks there's a different way to get there.",
        "This will help us later, both when we look for arguments and when we weaken the other side's arguments.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=2, title='The big picture', script=[
        "The second thing: we want to see the big picture. To understand what's really going on here. A kind of zoom out.",
        A('A particular case of... appears', c('The situation in the task is a particular case of a wider debate', 40)),
        "The situation they describe is one particular case of something bigger, and it's the bigger thing we're meant to discuss.",
        "You could build the same debate from many different situations. This is just the one that leads us into it.",
        A('Cameras = security vs privacy appears', c('Cameras → a debate between security and privacy', 40, gap=40)),
        "So what's the big picture with the cameras? It's a debate about security against privacy.",
        A('Other situations appears', c('Many other situations bring security and privacy into conflict; this is one of them', 34)),
        "You could take many other situations that bring security and privacy together. This is one particular case of that clash.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=3, title='State involved?', script=[
        "Another point worth noticing.",
        A('State involved → rights appears', c('When the state is one of the sides → often a clash of rights', 42)),
        "When the state is one of the sides in the dispute, very often it's a clash of rights.",
        A('Not always appears', c('Not always: disputes come in many kinds', 34)),
        "Not every dispute is a clash of rights. There are all kinds of disputes.",
        A('Why appears', c('Why? The state is not a private person doing as it pleases. It is there to protect its citizens, that is, to protect their rights.', 34, gap=40)),
        "But if the state is involved, it will usually be about rights. Why? Because what is the state?",
        "It isn't just a private person doing whatever it likes. It's there to protect the citizens, the residents. To protect our rights.",
        "So if it's involved, it's probably looking after some right of the citizens.",
        A('Cameras: right to security vs right to privacy appears', c('Cameras: the state is involved → the right to security vs the right to privacy', 34)),
        "And in our task? The state is involved, and it fits perfectly: a clash between the right to security and the right to privacy.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=4, title='The choice axis', script=[
        "The next thing I check is probably the most important part of analysing a task. We call it the choice axis.",
        A('Every side has pros and cons appears', c('Every side has advantages and disadvantages', 40)),
        "Obviously, in any situation or dispute, each side has advantages and disadvantages.",
        A('Exam tasks are balanced appears', c('Exam tasks are fairly balanced: if one side had almost only advantages, there would be nothing to discuss', 34)),
        "In exam tasks, things are roughly balanced. There won't be one side with almost only advantages. That task wouldn't appear, because there's no debate.",
        A('The axis appears', c('AGAINST  ◀━━━━━━━━━━━━▶  FOR', 44, gap=30)),
        "So what do we do? We draw an axis, our choice axis, between against and for.",
        A('Place yourself appears', c('Place yourself on the axis: "There are more advantages for FOR, so I am closer to FOR, but not at the very end, because I see its disadvantages too."', 34)),
        "And we place ourselves on it. I say: I think there are more advantages on the side of for. So I place myself somewhere here.",
        "I'm not completely for, because I understand that this position has disadvantages too. So I'm not all the way at the end. But I'm closer to for.",
        "Now let's see the kinds of tasks, because where you can stand on the axis depends on the kind of task.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=5, title='Yes/no tasks', script=[
        A('Yes/no tasks appears', c('Yes/no tasks → choose the side you are closer to', 42)),
        "Some tasks are yes or no. There we choose the side we're closer to.",
        A('Presidency example appears', c('"Should the office of president be abolished?"', 38)),
        "For example: should the office of president be abolished, or not?",
        A('No half president appears', c('I see advantages and disadvantages. It is not black and white. But I cannot have half a president or a quarter of a president.', 34)),
        "Even if I understand there are advantages and disadvantages to keeping it or abolishing it, even if it isn't black and white, in the end I have to decide.",
        "There can't be half a president, or a quarter of a president.",
        A('Choose the end appears', c('→ I choose the end I am closer to: for keeping the office', 38)),
        "So I choose the side I'm closer to. I think keeping it has more advantages, so I choose for the office of president. I choose the end.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=6, title='Degree tasks', script=[
        "Some tasks we call degree tasks, and there it's not exactly about the ends.",
        A('Degree task example appears', c('"To what extent should we rely on public transport?"', 40)),
        "For example: to what extent should we rely on public transport?",
        "They don't ask me whether to rely on public transport, yes or no. They ask: to what extent?",
        A('Anywhere on the axis appears', c('A little  ◀━━━━━━━━━━━━▶  A lot', 40, gap=8)),
        A('Stand anywhere appears', c('→ you can stand anywhere on the axis', 36)),
        "If I think only to a small extent, I say: rely on it a little. Or I say: yes, a lot, we should rely on it heavily.",
        "I can place myself anywhere along the whole axis.",
        A('Obvious degree task appears', c('"To what extent...?" = an obvious degree task: the wording says so', 34)),
        "We call this an obvious degree task, because it's clear. They're asking me: to what extent.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=7, title='Hidden degree tasks', script=[
        "But sometimes we get hidden degree tasks. And these are very common.",
        A('Bonus example appears', c('"Should a bonus be included in an employee\'s pay?"', 40)),
        "For example: should a bonus be included in an employee's pay? It's worded like a yes or no question, right?",
        "But it isn't exactly. Here too there's a degree hidden inside.",
        A('Absolute end appears', c('The absolute end: NO. No bonus at all. Nowhere to move.', 34)),
        "We have an absolute end and a flexible end. No is the absolute end. No bonus, we don't give the employee a bonus. That's it. There's no movement here.",
        A('Flexible end appears', c('The flexible end: YES, but how much? A small part? A large part? Only on sales above a certain level?', 34)),
        "But if I do want to give a bonus, I have a flexible end. Wait: how much bonus? Just a little? A significant part of the pay? A small part? Only on sales above a certain amount?",
        "I can move along the whole axis. Only a small bonus on small things, or mostly bonus because that motivates the most.",
        A('Watch for these appears', c('Worded like yes/no, but really a degree task. Notice them: they matter when you choose your position.', 34)),
        "So it's also a degree task. It's just worded as yes or no. It's very important to notice these hidden degree tasks.",
        "We'll come back to this when we talk about the considerations for choosing a position.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=8, title='"Why" tasks', script=[
        "There are also tasks that aren't for-and-against in the classic form.",
        A('Why task example appears', c('"Why is it worth learning to play an instrument at a young age?"', 40)),
        "For example: why is it worth learning to play an instrument at a young age?",
        "It sounds like, wow, what's this? A different task! It isn't an argument essay, it isn't for and against.",
        A('It is still for/against appears', c('It is still an ordinary argument essay: the side has simply been chosen for you', 36)),
        "But really it is. It's an ordinary for-and-against task. They just chose the position for you in advance.",
        A('Same task as yes/no appears', c('= "Should children learn an instrument at a young age?" with the answer "yes" given', 34)),
        "I could have asked the same task as: should children learn an instrument at a young age? Yes or no. But I turned it into: why is it worth it.",
        A('Any task can become a why task appears', c('"Why is it worth installing face-recognition cameras in public spaces?"', 34)),
        "And by the way, I can turn almost any task into a why task. Why is it worth installing face-recognition cameras in public spaces?",
        "What did I do? I chose your side for you, and now I want you to explain it.",
        "Bottom line: no need to get excited about a why task. They saved you the hesitation. Carry on from there.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=9, title='Three-opinion tasks', script=[
        "In most cases we're used to two opinions, one for and one against. Sometimes there are three.",
        A('Two ends and a middle, or three different appears', c('Three opinions: two ends and a middle, or three different options?', 40)),
        "Then we need to check: is it two ends and a middle, or three different options?",
        A('Pay example appears', c('Pay: only a base salary / only a bonus (a percentage of sales) / both → two ends and a middle', 34)),
        "For example: should an employee's pay be only a base salary, only a bonus, meaning only a percentage of sales, or both?",
        "That's two ends and a middle. One end: only base. The other end: only bonus. And the middle: both.",
        A('Toll road example appears', c('Toll roads: pay per trip / a monthly or yearly pass / state funding → three different options', 34)),
        "Now, toll roads. Who should pay, and how? You can pay per trip. That sounds fair: whoever uses it more pays more.",
        "You can pay for a monthly or yearly pass. Then heavy users pay less per trip, and light users end up paying more per trip.",
        "Or the state can fund it. Then all citizens pay for the trips of the people who use the road.",
        "Here there's no middle. Each opinion is completely different.",
        A('Still an ordinary essay appears', c('Rarer, but no need to panic: it is still an ordinary argument essay', 34)),
        "These are rarer. And we'll see in the recommended structures that it's still just an ordinary argument essay.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=10, title='The exact question', script=[
        "Now one more step, and it's a big one. Answer exactly the question they asked.",
        A('Three things to find appears', c('Before you look for reasons, find:', 38, gap=12)),
        "Before you start looking for reasons, find three things in the question.",
        A('The decision appears', c('1 · The decision: what exactly is being decided?', 36, gap=10)),
        A('The people appears', c('2 · The people: who exactly is affected?', 36, gap=10)),
        A('The conditions appears', c('3 · The conditions: what must stay true in the task?', 36, gap=34)),
        "One: the decision. What exactly is being decided? Two: the people. Who exactly is affected? Three: the conditions that must stay true.",
        A('Cameras: decision appears', c('Cameras: allow the security services to install face-recognition cameras in PUBLIC spaces, not in homes, and not "cameras in general"', 32)),
        "In our task: the decision is whether to allow the security services to install face-recognition cameras in public spaces. Not in private homes. Not cameras in general.",
        A('Change it = wrong issue appears', c('An essay can sound thoughtful and still discuss the wrong issue: change the decision, the population or the setting, and you have answered a different question.', 32)),
        "An essay can sound very thoughtful and still discuss the wrong issue. That isn't a small wording problem. It's a reasoning problem.",
        "If you quietly change the decision, the people, or the setting, you've answered a different question. And weak essays do exactly this.",
    ]))
    it, bottom = box(EXAMPLE_PROMPT, EXAMPLE_QUESTION, y=40, w=1000)
    c = Col(y=bottom + 24, gap=12)
    s.append(dict(mode='concept', active=11, title='Decision & people', script=[
        "Let's practise on a new task.",
        A('The four-day week task appears', it),
        "Read it. What's the decision? Moving schools to a four-day week. Not a shorter school year. Not less homework.",
        A('Decision & people appears', c('Decision: a four-day school WEEK · People: students, including young children, and their working parents', 30)),
        "Who's affected? Students, including young children, and their parents, especially working parents. The prompt names them.",
        A('Drift example appears', c('Drift: "Long weekends help adults at work recover" → wrong population', 30)),
        "Now, if I write a paragraph about how long weekends help adults at work recover, I've changed the population. It isn't about schools any more.",
        "So before every paragraph, check: same decision? Same people? Same conditions?",
    ]))
    it, bottom = box(BUS_PROMPT, BUS_Q, y=40, w=1000)
    c = Col(y=bottom + 22, gap=10)
    s.append(dict(mode='concept', active=12, title='Every part', script=[
        "And one more rule: every part of the question needs an answer.",
        A('The bus task appears', it),
        "Look at this question. Advantages and disadvantages. For residents, and for the city itself.",
        A('The grid appears', c('Advantages × disadvantages  ×  residents × the city = four boxes to cover', 32)),
        "That's really four boxes: advantages for residents, disadvantages for residents, advantages for the city, disadvantages for the city.",
        "A brilliant essay about residents alone leaves half the task unfinished.",
        A('Plan from the question appears', c('Build the plan from what the question asks, not from a memorised essay shape', 32)),
        "So the plan of your essay comes from what the question asks, not from a shape you memorised.",
        "The official guide says it too: a good essay directly addresses all elements of the task.",
    ]))
    return s


ANALYSE = lesson('vr50-e-analyse', 'Analysing the Task',
                 ['First: analyse', 'Same or different aim?', 'The big picture', 'State involved?',
                  'The choice axis', 'Yes/no tasks', 'Degree tasks', 'Hidden degree tasks', '"Why" tasks',
                  'Three-opinion tasks', 'The exact question', 'Decision & people', 'Every part'],
                 [dict(mode='title', title='Analysing the Task', script=[
                     "Planning the essay, step one: analysing the task.",
                     "Before we find a single argument, we need to understand exactly what we're being asked, and what kind of task it is.",
                 ])] + _analyse(), T50)


# =====================================================================================================================
def _gather():
    s = []
    it, bottom = box(CAM_PROMPT, CAM_Q, y=40, w=1000)
    s.append(dict(mode='concept', active=0, title="Don't rush", script=[
        "The next thing we do is gather information from the task itself.",
        "In other words: we spend time on the analysis. We don't run straight into writing the essay.",
        A('The camera task appears', it),
        A('Read slowly appears', T('2-3 minutes: read slowly, mark as you go', size=38, x=410, y=bottom + 30, w=1140)),
        "Many students skim this part and rush to write. But it's very, very important. It takes two or three minutes. You don't need more.",
        "Let's read it together.",
    ]))
    it, bottom = marked_box([(CAM_BACKGROUND, BLUE, False), (CAM_CLAIMS, INK, False)], CAM_Q, w=1000, y=40)
    s.append(dict(mode='concept', active=1, title='The background', script=[
        A('Background marked appears', it),
        "In recent years, officials in the security services have been promoting a bill... and so on, up to: offenders could be caught after the event.",
        "What is all this? All of this part is the background to the dispute. And it's fact.",
        A('Background = facts appears', T('Blue = the background to the dispute = FACTS', size=36, x=410, y=bottom + 24, w=1140)),
        "Everything marked here in blue is fact. They've given us the whole background, and all of it is fact.",
        A('Goes to opening appears', T('→ later it goes into the opening paragraph', size=32, x=410, y=bottom + 80, w=1140)),
        "And by the way, we'll take this background into the opening paragraph later.",
    ]))
    it, bottom = marked_box([(CAM_BACKGROUND, INK, False), (CAM_CLAIMS, GREEN, True)], CAM_Q, w=1000, y=40)
    s.append(dict(mode='concept', active=2, title='Material for arguments', script=[
        A('Claims marked appears', it),
        "Now we continue. Supporters claim that such a system would reduce, and even eliminate, the incidents. Opponents believe that it would seriously harm privacy.",
        "First of all, what is this? It's opinion. Supporters claim that. Opponents believe that. It's their opinion.",
        A('Claims = material appears', T('Green = the two sides\' claims = OPINIONS = material for arguments', size=34, x=410, y=bottom + 24, w=1140)),
        "But what's nice about these opinions is that they're material for our arguments.",
        "We can take these claims and build a whole paragraph out of each one, with development, support and so on.",
        "Right now we're collecting. We're gathering information from the task.",
    ]))
    c = Col(y=60, gap=16)
    s.append(dict(mode='concept', active=3, title='Mark key words', script=[
        "Another thing we do while reading the task: we mark the important words.",
        A('Key word 1 appears', c('"Today\'s technology can identify people... with a high degree of certainty"', 34)),
        "For example: today's technology can identify people with a high degree of certainty. Fine.",
        A('Key word 2 appears', c('"...provided that their image already exists in the database"', 38, gap=6)),
        A('A condition appears', c('→ a condition! No image in the database, maybe no identification. Possible argument or weakening.', 32, gap=30)),
        "Provided that their image already exists in the database. Wait. There's a condition here.",
        "If their image isn't in the database, maybe they can't be identified. I might use that as an argument, or as a weakening.",
        A('Key word 3 appears', c('"before an offence... while it is taking place... after the event"', 34, gap=6)),
        A('Three moments appears', c('→ three different moments: prevent, stop, catch', 32, gap=30)),
        "Suspicious activity identified before the offence, stopped while it's happening, or offenders caught afterwards. Three different moments.",
        A('Key word 4 appears', c('"reduce, and even completely eliminate"', 34, gap=6)),
        A('Strong claim appears', c('→ a very strong claim: the supporters say crime would drop, even disappear', 32)),
        "And: reduce, and even completely eliminate. So the supporters' opinion is that the system would cause a drop in all these incidents. Even make them disappear.",
        "These are words I need to understand the task better, and to choose the most suitable arguments.",
    ]))
    c = Col(y=60, gap=26)
    s.append(dict(mode='concept', active=4, title='Where each part goes', script=[
        "So in this analysis, what did we collect, and where does it go?",
        A('Background row appears', c('The background (facts) → the opening paragraph', 40)),
        "The background to the dispute: we take it to the opening paragraph.",
        A('Material row appears', c('Material for arguments → the body: argument paragraphs, counter-arguments, weakenings', 40)),
        "The material for arguments helps us with the body of the essay: the argument paragraphs, the counter-arguments, the weakenings.",
        A('Key words row appears', c('Key words → keep you focused on the exact question = relevance to the task', 40)),
        "And the important words keep me focused. They make sure I don't miss the question for discussion, and that my essay stays relevant to the task.",
        A('That is the analysis appears', c('Read slowly · mark the relevant parts · find the material · mark the key words', 34)),
        "That's it for analysing the task. Read slowly, mark the relevant parts, find the material for arguments, mark the important words.",
    ]))
    return s


GATHER = lesson('vr50-e-gather', 'Gathering Information', ["Don't rush", 'The background', 'Material for arguments',
                                                            'Mark key words', 'Where each part goes'],
                [dict(mode='title', title='Gathering Information', script=[
                    "Gathering information from the task.",
                    "The task itself hands you facts, arguments and key words. Let's learn to collect them.",
                ])] + _gather(), T50)


# =====================================================================================================================
def _position():
    s = []
    c = Col(y=60)
    s.append(dict(mode='concept', active=0, title='Your opinion is free', script=[
        "We've already said that your opinion doesn't matter. You may hold whatever opinion you like.",
        A('No penalty appears', c('No points are taken off for choosing one side rather than the other', 38)),
        "Nobody lowers your score because you chose one opinion and not another.",
        A('But: some are easier appears', c('But some positions are much easier to explain', 40)),
        "But there are considerations for choosing a position. Some positions are better to choose, because they'll be much easier to explain.",
        A('Considerations, not rules appears', c('These are considerations, not rules. Sometimes they point to different sides, and you decide.', 34)),
        "Before we start, it's important for me to make this clear. These are considerations, not instructions. You don't have to choose that position.",
        "Sometimes some considerations will point one way and others the other way, and you'll have to decide.",
        "But they'll help you choose the position that's easier for you to explain.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=1, title='Material in the task', script=[
        A('1 · Material appears', c('1 · Material for arguments in the task', 42)),
        "The first one: material for arguments in the task.",
        A('Choose the detailed side appears', c('Choose the side the task gives more detail for: they have already handed you main arguments', 36)),
        "We saw in the task analysis that we get suggestions for the main arguments of one side, of the other side, and so on.",
        "So let's choose the side that has more detail. They're already giving me main arguments. Let's use them.",
        "Why should I rack my brains looking for arguments of my own?",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=2, title='Your own opinion', script=[
        A('2 · Your opinion appears', c('2 · Your own opinion', 42)),
        "The second: your opinion.",
        A('Why do you think so appears', c('Something convinced you. Use it: explain WHY you think so.', 38)),
        "If you hold a certain position, why? Explain why you think that. Something convinced you.",
        "It's not that you tossed a coin: heads, I support the cameras, tails, privacy. No. Something made you choose a certain position. Use it.",
        A('That is the essay appears', c('Explaining why we think so is exactly what an argument essay does', 34)),
        "Explain why you think so. That's exactly what we need to do in an argument essay.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=3, title='Common vs individual', script=[
        A('3 · Common good appears', c('3 · The common good vs the good of the individual', 42)),
        "The third. In quite a few tasks there's the common good against the good of the individual.",
        A('Usually easier: common good appears', c('Usually easier to explain: the common good', 38)),
        "And usually it will be easier to explain the common good.",
        A('Prison example appears', c('An offender in prison: we limit the freedom of the individual in order to protect the public', 34)),
        "Take the example of an offender in prison. Here the common good outweighs the good of the individual. We harm the freedom and liberty of the individual to protect the public.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=4, title='The moral side', script=[
        A('4 · Moral appears', c('4 · A moral consideration', 42)),
        "The fourth. Sometimes there's a moral consideration hiding somewhere in the task.",
        A('Easier: the more moral appears', c('Usually easier to explain: the more moral position', 38)),
        "Then it will usually be easier to explain the more moral position. Again, not always. But if there is one, it's easier.",
        A('Weaker group appears', c('e.g. a vulnerable group that cannot protect itself, against a side that can look after itself', 34)),
        "For example, if there's a vulnerable group, and I want to choose its side to protect it, because it can't protect itself.",
        "Compared with the other side, which can look after itself.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=5, title='The existing situation', script=[
        A('5 · Status quo appears', c('5 · Changing the existing situation', 42)),
        "The fifth: changing the existing situation.",
        A('Usually: do not change appears', c('Usually easier: NOT to change. If something exists, there is probably logic behind it.', 36)),
        "The preference is usually not to change. If something exists, it will probably be easier to explain.",
        A('New law appears', c('A law that was just passed and some want to cancel → "It was only just passed! There was a reason."', 32)),
        "For example, a new law that people are talking about cancelling. Wow, they only just passed it and you already want to cancel it? If they passed it, there was probably logic to it. And you can explain that logic.",
        A('Old law appears', c('An old law → think: has the situation changed since it was passed?', 32)),
        "But sometimes it's an old law they want to cancel. Then I need to think a bit, not so decisively. Maybe the law is old and the situation has changed, and it needs changing. Or not.",
        A('Law that does not exist yet appears', c('A proposed new law → usually prefer not: there is probably a reason it has not been passed until now', 32)),
        "And sometimes they want to pass a new law. Here too I need to weigh it. Usually we'll prefer not to, because if the law doesn't exist, there's probably a reason it wasn't passed until now.",
        "But again, these are only considerations.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=6, title='Degree: no extremes', script=[
        A('6 · Degree tasks appears', c('6 · Degree tasks: do not choose the extremes', 42)),
        "The sixth: degree tasks. Don't choose the extremes.",
        A('Extremes = no critical thinking appears', c('An extreme answer signals a lack of critical thinking: as if you do not see the other side', 34)),
        "When I choose an extreme in a degree task, it signals a lack of critical thinking. A lack of consideration for the other side. As if I don't see it.",
        A('Hillel appears', c('In Jewish law the ruling follows the moderate House of Hillel, not the strict House of Shammai', 32)),
        "By the way, in Jewish law you may have heard of the House of Shammai and the House of Hillel. Shammai are the strict, uncompromising ones. Hillel are the more moderate ones.",
        "And which way does the law go? According to Hillel. Because the world isn't black and white. There's grey, lots of grey, in different shades.",
        A('Close, but not at the end appears', c('To a great extent → close to YES · to a small extent → close to NO · but not at the ends', 34)),
        "So if I think to a great extent, I'm close to yes. If to a small extent, I'm close to no. But I try not to choose the ends.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=7, title='The flexible end', script=[
        A('Choose the flexible end appears', c('Absolute end or flexible end? Choose the FLEXIBLE end: it lets you present a complex position', 38)),
        "When there's an absolute end and a flexible end, as we saw before, I don't want the absolute end. I want the flexible one.",
        "As the name says, it gives me flexibility. It lets me present a complex position.",
        A('Drug example appears', c('"Should there be a period of exclusivity for a company that develops a new medicine?"', 34)),
        "For example: should there be a period of exclusivity for a company that develops a new medicine?",
        "On one hand, companies develop medicines, they want to profit and to get back what they invested. On the other hand, there are patients here. Human life is at risk.",
        A('No = absolute appears', c('"No exclusivity" → the absolute end', 34, gap=8)),
        A('Yes, but = flexible appears', c('"Yes, but..." → one year? five? ten? and free medicine where a life is in danger', 34)),
        "If I say no, there's no exclusivity, I've chosen the absolute end.",
        "Usually I'd rather choose the flexible end. I can say yes, but only for a month. That's extreme, of course, but I can play with the range. A year, five years, ten years.",
        "I give them exclusivity, but I require them to give the medicine free in life-threatening cases. I have the whole range of the axis to choose from.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=8, title='A complex position', script=[
        "A very important part of what we're assessed on is critical thinking, and our ability to deal with opposing positions.",
        "To understand that the other side has a point. That our side isn't absolutely right.",
        A('Complex position appears', c('A complex position: choose side A, and add reservations and safeguards that solve some of its disadvantages', 36)),
        "And here I want to talk about a complex position. It lets me have my cake and eat it.",
        "I don't choose end A or end B. I choose side A, but I add some reservations. Safeguards that help solve some of the disadvantages I'd have if I went all the way with side A.",
        A('Shows critical thinking appears', c('It already shows critical thinking and consideration of the opposing view', 32)),
        "A complex position already signals critical thinking. Consideration of the opposing view. An understanding that nobody is simply right or wrong.",
        A('Cameras: yes, with safeguards appears', c('Cameras: YES, but a special body to handle the data (fewer people see it) + strong data security (no leaks)', 32)),
        "In our camera task: I don't choose the absolute end, no cameras. I choose the flexible end, because it lets me present a complex position.",
        "Yes, I do want face-recognition cameras in public spaces. But I understand the problem, the danger to privacy. So I want to add safeguards.",
        "For example, a special body that handles the data, to reduce the number of people exposed to it. And information-security measures, so the database doesn't leak.",
        "Choosing a complex position is, in my eyes, one of the best things you can do in an essay. And it's like that in life too. Life isn't black and white.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=9, title='Rights: detailed?', script=[
        A('7 · Rights appears', c('7 · Rights: choose the right the task explains in detail', 42)),
        "The seventh: human rights. Quite a few tasks involve a clash between this right and that right.",
        "And many students find it harder to explain a right when there's no detail.",
        A('Detailed right appears', c('Security: prevent offences, stop them, catch offenders afterwards → lots of detail', 34)),
        "If the task gives detail about the right, why it's a problem, what happens, I have material for arguments.",
        "Back to the cameras. Two rights: privacy and security. For security, there was detail: prevent offences, stop them, catch offenders afterwards. Wonderful. Lots of material.",
        A('Undetailed right appears', c('Privacy: "would seriously harm privacy" → no detail at all', 34)),
        "For privacy, there's no detail. They just say it would seriously harm privacy. That's it.",
        A('Choose the detailed one appears', c('If explaining rights is hard for you → choose the right that comes with detail', 34)),
        "For many students that's harder to explain. So for those students, it may be better not to choose the right without detail, but the one with detail.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=10, title='Three opinions: middle', script=[
        A('8 · Three opinions appears', c('8 · Three-opinion tasks: if possible, choose the middle', 42)),
        "And sometimes, more rarely, there are three-opinion tasks. If possible, it's better to choose the middle.",
        A('Middle = complex position appears', c('The middle is exactly a complex position: not black, not white, grey', 36)),
        "Why? The middle signals critical thinking. I'm choosing a complex position. Not black, not white. Grey.",
        A('80+80 appears', c('One end = 100 / 0      The middle ≈ 80 + 80 = 160', 44)),
        "When I choose one of the ends, it's as if I'm at a hundred and zero.",
        "When I choose a complex position, it's as if I take eighty percent of the advantages of this side and eighty percent of the advantages of that side. Pareto's eighty-twenty again.",
        "Eighty from each side is a hundred and sixty together, compared with a hundred and zero. I don't keep the cake completely whole, but overall I gain more.",
    ]))
    c = Col(y=50, gap=10)
    s.append(dict(mode='concept', active=11, title='Our task: the tally', script=[
        "Let's go through our task and see which considerations we have, and what they recommend.",
        A('Title appears', c('The camera task: what does each consideration recommend?', 36, gap=18)),
        A('Row 1 appears', c('Material in the task → FOR (detailed supporters\' claims)', 32)),
        "Material for arguments: we have a lot, and it's for the cameras. The opponents just say it would harm privacy. No detail.",
        A('Row 2 appears', c('Your own opinion → your choice', 32)),
        "Our opinion: I don't know yours. Each of you with your own.",
        A('Row 3 appears', c('Common vs individual good → none (security and privacy are both everyone\'s)', 32)),
        "Common good against individual good: not here. In both cases it's the common good: we look after everyone's security and everyone's privacy.",
        A('Row 4 appears', c('A moral consideration → none', 32)),
        "Moral consideration: I don't see anything special here.",
        A('Row 5 appears', c('The existing situation → AGAINST (there are no such cameras now)', 32)),
        "Changing the existing situation: this says against the cameras, because right now there's no such law and no such cameras.",
        A('Row 6 appears', c('Degree → FOR (against = the absolute end; for = yes, with safeguards)', 32)),
        "Degree: this is for the cameras. Against is the absolute end. For lets me say yes, with reservations and safeguards.",
        A('Row 7 appears', c('Rights → FOR (security is detailed, privacy is not)', 32)),
        "And rights: for the cameras, again, because the supporters' right, security, comes with detail, and privacy doesn't.",
    ]))
    c = Col(y=60)
    s.append(dict(mode='concept', active=12, title='The key consideration', script=[
        "So that's the lesson on considerations for choosing a position. And a reminder: they're considerations, not instructions.",
        A('The most important appears', c('The most important: in a degree task, do not choose an extreme; choose the flexible end', 42)),
        "If I had to pick the single most important one, it's degree tasks. Don't choose the extremes. Choose the flexible end.",
        A('Why appears', c('→ a complex position → critical thinking + dealing with the opposing view', 36)),
        "It'll be much, much easier for you to present a complex position that shows critical thinking and consideration of the opposing view.",
        "Perfect. Everything they're looking for.",
    ]))
    return s


POSITION = lesson('vr50-e-position', 'Choosing a Position',
                  ['Your opinion is free', 'Material in the task', 'Your own opinion', 'Common vs individual',
                   'The moral side', 'The existing situation', 'Degree: no extremes', 'The flexible end',
                   'A complex position', 'Rights: detailed?', 'Three opinions: middle', 'Our task: the tally',
                   'The key consideration'],
                  [dict(mode='title', title='Choosing a Position', script=[
                      "Considerations for choosing a position.",
                      "Any position can get a top score. But some positions are much easier to explain. Let's see which.",
                  ])] + _position(), T50)


# =====================================================================================================================
def _args_intro():
    s = []
    c = Col(y=60)
    s.append(dict(mode='concept', active=0, title='The most suitable', script=[
        "Maybe one of the most important stages: finding the most suitable arguments for the essay.",
        A('Suitable, not best appears', c('Find the most SUITABLE arguments, not "the best" ones', 42)),
        "Notice I said the most suitable. I didn't say the best.",
        A('No calculator appears', c('There is no calculator that gives an argument a score', 36)),
        "First, because there's no such thing as the best argument. There's no calculator you put an argument into and, hop, it gives you a score.",
        A('Other considerations appears', c('Strength is not the only consideration: a slightly weaker argument that is original may impress the rater', 34)),
        "And second, when choosing arguments there are other considerations besides strength.",
        "For example, I might prefer an argument that's a bit less strong, but still strong enough, because it's very creative. One that will impress the rater, because not many people thought of it.",
    ]))
    c = Col(y=60, gap=26)
    s.append(dict(mode='concept', active=1, title='Three techniques', script=[
        "We'll learn several techniques for finding arguments. It's important to master all of them, because one technique may suit one task better, and another technique another task.",
        A('Rights appears', c('1 · Rights: which rights clash? Is the harm to them too great, or proportionate and reasonable?', 34)),
        "First, human and civil rights. Many tasks have a clash between rights. Then we can argue that the harm to a right is too great. Or, from the other direction, that it's actually proportionate and reasonable.",
        A('Zoom out appears', c('2 · Zoom out: the wider frame of the debate + different perspectives (social, educational, economic...)', 34)),
        "Zoom out. That means looking at the wider frame of the debate. Understanding that the case in the task is a particular case of a wider problem. Something at the macro level.",
        "In zoom out we also examine the dispute from the points of view of different fields. You've probably heard: social, educational, economic and so on.",
        A('Zoom in appears', c('3 · Zoom in: into the issue: who are the players, how are they affected, what do they gain or lose?', 34)),
        "And zoom in. Going into the issue. Who are the relevant parties? Who are the players? Who does it affect, how, what do they gain, what do they lose?",
        "We'll fill in each of these in the coming lessons.",
    ]))
    c = Col(y=60, gap=18)
    s.append(dict(mode='concept', active=2, title='Types of argument', script=[
        "Types of argument. What is an argument? It's something I claim. It's not necessarily my opinion.",
        A('Opinion appears', c('Opinion: "This is what I think." Someone else can simply think otherwise.', 34)),
        "An argument can be my opinion. It can be an opinion.",
        A('Reasonable assumption appears', c('Reasonable assumption: "It is likely that..." Others will agree more easily. Stronger than an opinion.', 34)),
        "But it can also be a reasonable assumption that strengthens my position. And that's of course stronger than an opinion.",
        A('Fact appears', c('Fact: cannot be refuted. Maybe weakened in other ways, but not by saying "that is not true". The strongest.', 34, gap=34)),
        "And it can even be a fact that strengthens my position. The fact argument is the strongest, because it's a fact. You can't refute it.",
        "You may be able to weaken it in other ways, but not by saying it isn't true.",
        A('The ladder appears', c('opinion  →  reasonable assumption  →  fact      (weaker → stronger)', 38)),
        "An opinion is, you know, what you think. And I think otherwise.",
        "So we want our arguments to be as close as possible to this end: fact, or at least reasonable assumption.",
        "Of course we'll sometimes use opinion arguments too. But the more fact and reasonable assumption, the stronger the arguments.",
    ]))
    c = Col(y=60, gap=20)
    s.append(dict(mode='concept', active=3, title='Links in the chain', script=[
        A('Not just the key sentence appears', c('An argument is not only the key sentence', 40)),
        "And by the way, an argument isn't only the key sentence, the main argument of my paragraph.",
        A('Mini-arguments appears', c('The development is built of small arguments: links in a logical chain, each leading to the next', 34)),
        "In the development stage, where I explain and support my argument, I actually do it with small arguments. Links in the logical chain of something that leads to something that leads to something.",
        "And there I can definitely include reasonable assumptions and facts. That strengthens the development and the support.",
        A('Only opinions appears', c('"I think... and I think... and I think..." → very weak', 34, gap=8)),
        A('Likely appears', c('"It is likely that this will cause... which is likely to lead to..." → easier to agree with', 34)),
        "Now imagine that every link in my paragraph is only opinion. I think this, and I think that, and I think this. It's very weak. Someone looks on and says: fine, that's what you think. I think differently.",
        "But if I say: it's likely that this will cause that, and it's likely that that will cause this... Then other people will agree with me more. It's easier to show the logic. The arguments are more convincing.",
    ]))
    c = Col(y=60, gap=16)
    s.append(dict(mode='concept', active=4, title='Wording: opinion', script=[
        "One more thing: the wording of the argument.",
        A('Type affects wording appears', c('The type of argument decides where "in my opinion" goes', 40)),
        "The difference between opinion, reasonable assumption and fact also affects how you word the argument.",
        A('Opinion example appears', c('"In my opinion, face-recognition cameras will deter offenders and reduce crime."', 34)),
        "An opinion argument starts with: in my opinion. In my opinion, face-recognition cameras will deter offenders and reduce crime.",
        A('All opinion appears', c('Both parts are opinion: not certain to deter, not certain to reduce crime → "In my opinion" at the start', 32, gap=30)),
        "Here it's an opinion, right? That's why I wrote in my opinion. It isn't certain the cameras will deter. That's my opinion. And I also think deterrence will reduce crime. Again, my opinion.",
        A('Hebrew-speaker errors appears', c('Avoid: "In my opinion I think..." · "According to me..." → write "In my opinion, ..." or "I believe that ..."', 32)),
        "And a note for English: don't write in my opinion, I think. That's saying the same thing twice. And don't write according to me. Write in my opinion, or I believe that.",
    ]))
    c = Col(y=60, gap=16)
    s.append(dict(mode='concept', active=5, title='Wording: fact first', script=[
        "But sometimes part of my argument is factual. Then in my opinion appears in the middle of the argument, not at the beginning.",
        A('Fact-first example appears', c('"The database will eventually have to be accessible to people, and in my view, even if only a few people have access, there is a risk that it will leak."', 34, gap=30)),
        "Look at this argument. The database will eventually have to be accessible to people, and in my view, even if only a few people have access, there is a risk that it will leak.",
        A('Part 1 = fact appears', c('Part 1 = FACT: a database nobody ever looks at cannot be used', 32, gap=8)),
        "The first part is factual. If the database just sits in some cloud and nobody ever sees the footage, it can't be used. Obviously some people will have to be exposed to it.",
        A('Part 2 = opinion appears', c('Part 2 = OPINION: "in my view" goes here, in the middle', 32, gap=30)),
        "So I add in my view only in the middle, because I started with a fact.",
        A('Wrong placement appears', c('"In my view, the database will eventually have to..." → casts doubt on the whole argument, even on the fact', 32)),
        "If I put in my view at the start of the sentence, I cast doubt on my whole argument. Everything from here on is now opinion, and the reader thinks: I'm not sure I agree with you.",
        "But if I start with the fact and add in my view only to the second part, now we can talk about whether you agree with me, and I'll try to explain why I think so.",
    ]))
    c = Col(y=60, gap=26)
    s.append(dict(mode='concept', active=6, title='Next: the techniques', script=[
        "So the distinction between types of argument affects the wording too.",
        A('Summary 1 appears', c('Look for the most suitable arguments, not "the best"', 36)),
        A('Summary 2 appears', c('Aim for facts and reasonable assumptions, not only opinions', 36)),
        A('Summary 3 appears', c('Word each argument by its type: "in my opinion" only where it is opinion', 36)),
        "Most suitable, not best. As many facts and reasonable assumptions as you can. And word each argument according to its type.",
        A('Next appears', c('Next: rights · zoom out · zoom in', 42)),
        "Now let's dive in and see how we find arguments with the techniques: rights, zoom out and zoom in.",
    ]))
    return s


ARGS_INTRO = lesson('vr50-e-args-intro', 'Finding Arguments',
                    ['The most suitable', 'Three techniques', 'Types of argument', 'Links in the chain',
                     'Wording: opinion', 'Wording: fact first', 'Next: the techniques'],
                    [dict(mode='title', title='Finding Arguments', script=[
                        "An introduction to finding arguments.",
                        "What are we looking for, what kinds of arguments are there, and how does the kind of argument change the way we word it?",
                    ])] + _args_intro(), T50)


# =====================================================================================================================
def _rights():
    s = []
    c = Col(y=60)
    s.append(dict(mode='concept', active=0, title='Which rights?', script=[
        "Our first technique for finding arguments: think about rights.",
        A('Which rights appears', c('Which rights are at play? Which are harmed? Too much? Too little?', 42)),
        "Which rights are at play here? Which are harmed, too much, too little, and so on.",
        "Most of you have heard the words right and rights before. But there's some confusion. Which rights are there? Which categories? Are some rights stronger and some weaker?",
        A('No official list appears', c('There is no single official list. We divide rights into three types:', 36)),
        "Lucky you came, because I'm here to put some order into it.",
        "First of all, there's no fixed list that the whole world works by. There are different ways of dividing rights, and we'll divide them into three types.",
    ]))
    c = Col(y=60, gap=16)
    s.append(dict(mode='concept', active=1, title='Natural rights', script=[
        A('Natural rights appears', c('1 · Natural rights: every person has them simply by being born', 40, gap=24)),
        "The first type: natural rights. That means rights every person has simply by being born. You were born, you have this right.",
        A('Life and security appears', c('• Life and security: nobody may harm you', 34)),
        "The right to life and security. You can't just walk down the street and have someone harm you, kill you, injure you. It's your right not to be harmed.",
        A('Liberty appears', c('• Liberty: to feel, choose and think as you wish', 34)),
        "The right to liberty. To feel, to choose and to think whatever you want.",
        A('Movement and occupation appears', c('• Freedom of movement · freedom of occupation', 34)),
        "Freedom of movement. Freedom of occupation, to work at whatever you want.",
        A('Property and equality appears', c('• Property · equality', 34)),
        "To own property. The right to equality.",
        A('Dignity and privacy appears', c('• Dignity → from it comes the right to privacy (the subject of many exam tasks)', 34)),
        "Dignity. And from dignity comes the right to privacy, which is the subject of quite a few tasks in the exam.",
    ]))
    c = Col(y=60, gap=20)
    s.append(dict(mode='concept', active=2, title='Civil & social rights', script=[
        A('Civil rights appears', c('2 · Civil rights: because I belong to a state', 40, gap=8)),
        A('Civil list appears', c('to vote and to be elected · freedom of association · freedom of the press · freedom of expression', 32, gap=40)),
        "The second type: civil rights. Once I belong to a particular state, I already have rights in my relationship with the state.",
        "The right to vote and to be elected, freedom of association, freedom of the press, freedom of expression.",
        A('Social rights appears', c('3 · Social rights: an adequate standard of living', 40, gap=8)),
        A('Social list appears', c('the state provides: education · health · housing · fair employment conditions', 32)),
        "And the third: social rights. The right to an adequate standard of living. That the state looks after my education, health, housing and employment conditions.",
    ]))
    c = Col(y=60, gap=20)
    s.append(dict(mode='concept', active=3, title='A short history', script=[
        "Let's look at human history for a moment.",
        A('Once: no rights appears', c('Once there were no rights: a slave was property, with no equality, no property, no freedom of movement or occupation', 34)),
        "Once, there simply were no rights. The concept didn't exist. Certainly not equality, life, security, liberty. There were slaves, and a slave was like your property.",
        "He wasn't allowed to own property, he certainly wasn't your equal. No freedom of movement, no freedom of occupation. He did what he was forced to do.",
        A('Natural rights recognised appears', c('Gradually: "all people are born equal" → natural rights for everyone', 34)),
        "Over history there were many situations where certain societies recognised these rights. Sometimes it stayed in those societies, or was forgotten, until at some point people began to understand that natural rights belong to every person.",
        "All people are born equal. And it became accepted all over the world, with declarations of this organisation and that one, the United Nations and so on.",
        A('Then civil rights appears', c('People who feel equal want a voice → civil rights: to vote, to be elected, to speak', 34)),
        "Once there were natural rights, civil rights began to form. People who feel equal say: wait, I also want to vote, and to be elected. I'm entitled to equality, so I want freedom of expression too.",
        A('Then social rights appears', c('Weaker groups enter government → social rights that look after weaker groups', 34)),
        "And then the weaker groups began to enter politics, the institutions of government. Once they were there, they began to look after themselves, and they created social rights. Rights that look after the weaker groups.",
    ]))
    c = Col(y=60, gap=20)
    s.append(dict(mode='concept', active=4, title='Social vs property', script=[
        A('Rich do not need appears', c('If I have money, I do not need the state to provide my standard of living', 36)),
        "If I have money, I don't really need the state to look after my standard of living. I look after myself. Education, health? I go to a private doctor. Housing? I have a villa by the sea.",
        A('State funds them appears', c('What makes social rights special: the STATE funds them, and they are not guaranteed everywhere', 34)),
        "What's special about social rights is that the state is the one that funds them. And by the way, they aren't guaranteed. Some states don't fund health or housing or workers' rights. It depends on the state you live in.",
        A('Funded by taxes appears', c('Funded by the state → from taxes → from the property of other citizens', 36)),
        "And some see social rights as lesser than natural rights or civil rights. Why? Who funds social rights? The state. Where does the state get the money? From taxes. Where do taxes come from? From the property of other citizens.",
        A('Built-in clash appears', c('→ social rights clash, by definition, with the right to property (a natural right)', 36)),
        "So the very definition of social rights already creates a clash with the right to property, a natural right of every person.",
        "If you meet a task about a clash like that, this is a point you might choose to take and develop.",
    ]))
    c = Col(y=60, gap=20)
    s.append(dict(mode='concept', active=5, title="State's passive role", script=[
        A('Passive role appears', c('The passive role: the state must not harm rights WITHOUT JUSTIFICATION', 40)),
        "What about the state? It has a passive role. The state must not harm rights without justification.",
        "Notice: without justification. It's completely clear that the state harms our rights, and will keep harming them. It can't be otherwise.",
        A('Speed example appears', c('I want to drive at 150 km/h: freedom of movement. But it endangers other people\'s right to life and security → the limit is justified.', 34)),
        "Why? Because to protect certain rights, it has to harm other rights. For example, I want to drive at a hundred and fifty kilometres an hour, because that's my right. Freedom of movement.",
        "But of course I'd be harming other citizens' right to life and security if I drove that fast. So the state harms my right and doesn't let me drive at that speed. But there's a justification.",
        A('Who decides appears', c('Justified or not? No calculator: it depends on the circumstances, and decisions can be reopened years later', 34)),
        "Now, who decides whether there's a justification? Again, there's no calculator. We need to look at the circumstances of the specific case and decide.",
        "And sometimes time passes, old decisions come up for discussion again, and the decision changes. Just like an essay: someone argued for a law, someone argued against, a law was passed. Thirty years later it's reopened, and suddenly the arguments against are stronger.",
    ]))
    c = Col(y=60, gap=22)
    s.append(dict(mode='concept', active=6, title="State's active role", script=[
        A('Active role appears', c('The active role: the state must also act to PROTECT rights', 40)),
        "The state's second role is an active one. It isn't only forbidden to harm rights. It also has to act to protect them.",
        A('Unavoidable clash appears', c('Protecting one right often harms another → the clash between rights is unavoidable', 36)),
        "And as we said, sometimes protecting one right harms another. So with rights arguments, you need to understand that the clash between rights is unavoidable.",
        "It's not that two rights can always live side by side and everything is fine. If that were so, it wouldn't be in our task.",
        A('Do not panic appears', c('A clash is fine. Our job: make sure each right is harmed PROPORTIONATELY.', 38)),
        "What's important is not to panic about the clash. It's fine that there's a clash. In a clash, we need to make sure the harm to each right is proportionate.",
    ]))
    c = Col(y=60, gap=22)
    s.append(dict(mode='concept', active=7, title='Proportionate harm', script=[
        A('Proportionate, not minimal appears', c('PROPORTIONATE harm, not minimal harm', 44)),
        "Notice I wrote proportionate harm, not minimal harm. Because it won't always be the minimum. Sometimes I need to harm a right more than the minimum to protect another right.",
        A('Depends on circumstances appears', c('Which right, and how much? It depends on the circumstances of THIS task', 36)),
        "How do we know which right to harm, and what's proportionate? Again, according to the circumstances.",
        A('General claim appears', c('✗ "The right to life always beats privacy: what good is privacy if you are dead?"', 34)),
        "Some will argue that the right to life and security is always bigger than the right to privacy. If you're dead, what good is your privacy? None, right?",
        "But that's not what we need to do. We don't talk in general, theoretical terms. We talk according to the circumstances of the specific task in front of us.",
        A('Specific claim appears', c('✓ "Here the benefit of the cameras is not large, so the harm to privacy is not proportionate" + explain why', 34)),
        "You want face-recognition cameras, and they harm privacy. In this specific case, the cameras shouldn't be installed: they harm privacy, although their benefit isn't that large.",
        "And then we need to explain why we think the benefit isn't large, and so why the harm isn't proportionate. The harm to privacy is too great.",
    ]))
    c = Col(y=60, gap=22)
    s.append(dict(mode='concept', active=8, title='A rights argument', script=[
        "About choosing a rights argument: it's a mixed blessing.",
        A('Plus appears', c('+ It cannot be denied: the right is a given fact that everyone accepts', 36)),
        "On one hand, it can't be denied. When I make another kind of argument, it's my opinion. I think the cameras will deter and reduce crime in the filmed area. Fine, that's your opinion. I can already doubt it.",
        "But when I argue that a certain right is harmed, you can't deny the right. It's an existing fact. Everyone accepts that there is a right, and that it mustn't be harmed, or the harm must be limited.",
        A('Minus appears', c('− But "privacy is harmed, I win" does not work: you must explain WHY the harm is not proportionate here', 36)),
        "But having a right doesn't mean I can say: there's harm to privacy, that's it, I've won the debate. It doesn't work like that.",
        "I need to explain. I need to explain why the harm to the right isn't proportionate, in the specific circumstances of the task.",
        A('Choose what suits you appears', c('Some students find a logical chain easier than a rights argument: choose what you can explain', 32)),
        "So on one hand, the start is more solid: I begin with a fact, there is a right. On the other hand, I have to explain, and that isn't always easy.",
        "Some students find it easier just to explain the logical chain of an argument that has nothing to do with rights, than to argue and explain why a right is harmed disproportionately.",
    ]))
    return s


RIGHTS = lesson('vr50-e-rights', 'Finding Arguments: Rights',
                ['Which rights?', 'Natural rights', 'Civil & social rights', 'A short history',
                 'Social vs property', "State's passive role", "State's active role",
                 'Proportionate harm', 'A rights argument'],
                [dict(mode='title', title='Finding Arguments: Rights', script=[
                    "The first technique for finding arguments: rights.",
                    "Which rights are there, what does the state owe us, and how do we turn a right into an argument?",
                ])] + _rights(), T50)


# =====================================================================================================================
def _zoom_out():
    s = []
    c = Col(y=60, gap=22)
    s.append(dict(mode='concept', active=0, title='A view from above', script=[
        "Zoom out. By zoom out we mean a kind of view from above over everything that's happening here.",
        A('Like task analysis appears', c('It is like analysing the task:', 38, gap=12)),
        "First of all, there's something here that really reminds us of analysing the task.",
        A('Same or different aim appears', c('• Same or different interest? Friends with one aim, or rivals pulling apart?', 34)),
        "In the analysis we checked whether the interest is similar or different. Guys, why are you arguing? Are you two friends who want the same goal in different ways, or two rivals each pulling in a different direction?",
        A('Particular case appears', c('• A particular case of... → the wider frame of the debate', 34)),
        "We said: this is a particular case of... and tried to understand the wider frame of the debate.",
        A('Rights appears', c('• The state is involved → probably a debate about rights', 34)),
        "What's here? A debate about rights? Something else? And if the state is involved, we probably have a debate about rights.",
        A('New: perspectives appears', c('+ NEW: different perspectives', 40)),
        "And what I want to add here: different perspectives.",
    ]))
    c = Col(y=60, gap=18)
    s.append(dict(mode='concept', active=1, title='Four perspectives', script=[
        "Many students call them different fields, angles, aspects: the social aspect, the economic aspect and so on.",
        "There are many points of view on any case, debate or dispute. But I want to focus on four that, in my eyes, can be linked to almost every dispute.",
        A('Economic appears', c('1 · Economic', 42, gap=8)),
        A('Social appears', c('2 · Social', 42, gap=8)),
        A('Educational appears', c('3 · Educational', 42, gap=8)),
        A('Psychological appears', c('4 · Psychological', 42, gap=30)),
        "Economic. Social. Educational. And psychological.",
        A('And more appears', c('and more: moral · environmental · legal · religious', 34)),
        "There are more, of course: moral, environmental, legal, even religious. But these four are the ones I like to look from.",
    ]))
    c = Col(y=60, gap=16)
    s.append(dict(mode='concept', active=2, title='Economic', script=[
        A('Economic question appears', c('Economic: money is almost always a consideration. Who pays? Who gains? Who loses?', 36, gap=26)),
        "The first is economic. What can you do: money will almost always be one of the considerations. In the end someone has to pay. Where does the money come from? Who pays, who loses, who gains?",
        "It's a point you can fit onto almost every task. Let's take some examples. Reduced tax for large companies.",
        A('State earns less appears', c('The state collects less tax', 34)),
        "If there's a reduced tax for large companies, the state earns less tax. Less money comes into the state.",
        A('Workers earn more appears', c('But people who get jobs in these companies earn more', 34)),
        "But on the other hand, the people who start working in these companies will earn more money.",
        A('Small citizen pays appears', c('A third side: the budget must come from somewhere → the ordinary citizen pays more tax', 34)),
        "But there's also a third side. If the state earns less from taxes, someone has to pay. The state budget doesn't come out of nowhere. If these companies don't pay, the money comes from the ordinary citizen.",
        A('Short vs long term appears', c('Short term: less tax revenue · long term: more people working, less unemployment → a stronger economy', 34)),
        "And you can look at the long term. In the short term the state gets less tax revenue. In the long term it may actually strengthen it: more people work, unemployment falls, and that strengthens the economy.",
        A('The companies appears', c('The companies themselves earn more (maybe not an argument you would use, but notice it)', 30)),
        "Another point is the companies themselves. They'll earn more. I'm not sure we'd choose to use that argument, but in some cases maybe. So it's important to be aware of it.",
    ]))
    c = Col(y=60, gap=22)
    s.append(dict(mode='concept', active=3, title='Economic: cameras', script=[
        "Now let's take the face-recognition camera task.",
        A('Costs appears', c('Against: building and running the whole camera network costs a great deal. Who pays?', 36)),
        "I can say: wait, you need to set up this whole network. Building and running it costs a huge amount of money. Someone has to pay. Where will it come from?",
        A('In addition appears', c('And it comes on top of existing bodies: police officers are still needed to search and to catch', 34)),
        "And I can argue that it's in addition to the bodies that exist today. Even if the cameras run, you still need the police officers, someone to go and catch, someone to go and search.",
        A('Saves money appears', c('For: it may SAVE money: faster arrests, fewer resources spent searching, evidence of guilt → no re-arrests', 36)),
        "And from the other side, someone can argue: wait, this network will actually save money. With the cameras we can catch offenders faster, invest fewer resources searching and locating them.",
        "We have evidence of their guilt. Once we've caught them, that's it, they go to prison. No need to release them and chase them again and waste more and more resources.",
        A('Money connects to almost everything appears', c('Money connects to almost everything, but you have to practise finding it', 32)),
        "So to sum up: money is connected to almost everything. You'll find it very easy to bring in. But you need to practise. It won't just jump out at you.",
    ]))
    c = Col(y=60, gap=22)
    s.append(dict(mode='concept', active=4, title='Social', script=[
        A('Social appears', c('Social: we do not live in a vacuum. Almost every decision affects society.', 38)),
        "The next point of view is social. Because we don't live in a vacuum. We live in a society, and there's almost always an effect on society.",
        A('Tax social appears', c('Reduced tax → companies hire → fewer unemployed → a stronger society', 34)),
        "For example, reduced tax for large companies. The companies start employing people, so there are fewer unemployed. That contributes to the strength of society.",
        A('Cameras social appears', c('Cameras → people avoid public spaces (they do not want to be followed) → fewer social interactions → people meet only in private homes', 34)),
        "Or face-recognition cameras. Maybe it will make people go out less, into public spaces. They care about their privacy. They don't want to be followed.",
        "So there are fewer social interactions. The whole way people interact could change. Suddenly people start meeting only in private homes and don't go out.",
        "So it's clear there's a social effect. And from here I can take it in all kinds of directions.",
    ]))
    c = Col(y=60, gap=20)
    s.append(dict(mode='concept', active=5, title='Educational', script=[
        A('Educational appears', c('Educational: not "tasks about schools", but what a decision teaches people', 38)),
        "The next point of view is educational. And I don't mean tasks that are about education: home schooling, rewarding students, how to pay teachers.",
        "I mean the educational effects, on how a child is brought up. Not necessarily learning. Through all kinds of things we do.",
        A('Cameras teach distrust appears', c('Cameras teach children distrust, and fear: "the street is so dangerous that it needs cameras"', 34)),
        "For example, if there are face-recognition cameras in public spaces, what does that say? We're educating our children to distrust. Not to trust each other. Maybe to fear the street: there have to be cameras, because the street is so dangerous.",
        A('Or the opposite appears', c('Or the opposite: "Don\'t be afraid, everything is filmed, you are safe"', 34)),
        "And from the other side someone could argue exactly the opposite: I'm teaching them not to be afraid in the street. Don't worry, everything is filmed, everything's fine. Either way, it has an educational effect.",
        A('Adults too appears', c('Adults too: a law forcing pension savings, or courses in financial planning instead?', 34)),
        "By the way, educational effects aren't only on children. Often the argument is: I want to educate the population to do certain things, not through enforcement or legislation, but through education.",
        "For example, the pension law: we must set money aside for a pension. In the past, whoever wanted to did, and whoever didn't, didn't.",
        "Some said: let's pass a law requiring people to save for when they stop working. Others said: no. If you want people to look after their financial future, educate them. Give them courses on financial planning. But don't force them. It's their money.",
    ]))
    c = Col(y=60, gap=22)
    s.append(dict(mode='concept', active=6, title='Psychological', script=[
        "And I'll finish with the point of view I love most: the psychological one.",
        A('Psychological appears', c('Psychological: almost every decision has psychological effects on people', 38)),
        "Why? One, we can bring it into almost anything, because almost every action or decision has psychological effects on people, or could have.",
        A('Tax psych appears', c('Reduced tax → the unemployed find work → a sense of worth, less stress and depression', 34)),
        "Examples from our tasks. Reduced tax for large companies: unemployed people start working. That has a huge effect on them. Suddenly a sense of worth.",
        "People who've been looking for work for a long time often become depressed, impatient and stressed. It affects their whole life. When you give someone a job and let them earn a living with dignity and support their family, it has an enormous effect.",
        A('Cameras psych appears', c('Cameras → people feel followed → their behaviour becomes paranoid: "Am I being filmed here?"', 34)),
        "Face-recognition cameras: people start to feel they're being followed. Their behaviour becomes paranoid. Wait, am I being filmed here? Am I not?",
    ]))
    c = Col(y=60, gap=22)
    s.append(dict(mode='concept', active=7, title='Why psychological', script=[
        A('Few use it appears', c('Few students use it → an original argument stands out', 40)),
        "Beyond the fact that it fits almost every task, the main reason I love it is that not many students use it.",
        A('Rater reaction appears', c('Economic again? "Everyone writes about money." Psychological? "A nice angle!"', 36)),
        "And if I use arguments that aren't common, the rater says: wow, I've got someone with nice critical thinking here. The economic argument? Yes, yes, everyone writes to me about money. But psychological? Nice angle.",
        A('Credit for originality appears', c('The same strength of support, but extra credit for originality', 36)),
        "And that shows in the score. Let's say using a psychological argument, which isn't so common, affects the rater psychologically. He gives me a bit more credit for the originality of my argument, even if I supported it exactly as well as others support other arguments.",
    ]))
    c = Col(y=60, gap=22)
    s.append(dict(mode='concept', active=8, title='Knowing is not enough', script=[
        "I'll end this lesson with a recommendation.",
        A('Lists do not help appears', c('Memorising a list of fields (acronyms, "the ministers method") does not find arguments for you', 36)),
        "I meet many students who have the list of fields. Sometimes they make acronyms, sometimes the ministers method: the minister of economy, the minister of finance, the minister of education. That's how they try to remember it.",
        "But just knowing the fields doesn't help you find the argument. To find arguments you need to think. It's not enough that I tell you: social. Oh, OK, wait, I don't know how it affects anything.",
        A('Practise appears', c('Practise: one essay a week is the bare minimum. Analyse many published tasks.', 38)),
        "You need to practise. You need to try it. Remember the weekly essay? It isn't enough. It's the absolute minimum: one essay a week. You need to write much more and look at many more tasks.",
        A('Just find arguments appears', c('You do not always have to write the whole essay: sometimes just find the arguments', 34)),
        "There are dozens of NITE tasks that have already been published. Go through them, analyse them, try to find arguments.",
        "And you don't always have to write the whole essay. You can just go through a task and see whether you manage to find arguments. Practise this part.",
    ]))
    c = Col(y=60, gap=26)
    s.append(dict(mode='concept', active=9, title='Right vs perspective', script=[
        "One more thing. Some students mix up rights with perspectives. For example, a social right like the right to education, and the educational perspective.",
        A('Right to education appears', c('The RIGHT to education: something I am entitled to receive, here from the state', 36)),
        "The right to a proper education is my right. It's something I'm entitled to receive, in this case from the state.",
        A('Educational perspective appears', c('The EDUCATIONAL PERSPECTIVE: what effect does this decision have on how children and adults are educated?', 36)),
        "In the educational perspective, I ask myself: what effect does this have on education? What effects does what we do, or choosing this position or that one, have on how children and adults are educated?",
        A('Summary appears', c('Zoom out = the macro view: the wider frame + perspectives', 38)),
        "That's it for finding arguments with zoom out. The macro view. And from here we go on to zoom in.",
    ]))
    return s


ZOOM_OUT = lesson('vr50-e-zoom-out', 'Finding Arguments: Zoom Out',
                  ['A view from above', 'Four perspectives', 'Economic', 'Economic: cameras', 'Social',
                   'Educational', 'Psychological', 'Why psychological', 'Knowing is not enough',
                   'Right vs perspective'],
                  [dict(mode='title', title='Finding Arguments: Zoom Out', script=[
                      "The second technique for finding arguments: zoom out.",
                      "We step back, look at the wider debate, and look at it through different perspectives.",
                  ])] + _zoom_out(), T50)


# =====================================================================================================================
def two_cols(player, y0=60):
    """A player's benefit / harm columns. Returns the list of A(...) items (heading + both columns)."""
    out = [A('Player: %s appears' % player, T('Player: ' + player, size=40, x=410, y=y0, w=1140))]
    L = Col(y=y0 + 80, x=410, w=540, gap=16); R = Col(y=y0 + 80, x=1000, w=550, gap=16)
    out.append(A('Benefit heading appears', L('BENEFIT', 34, gap=10)))
    out.append(A('Harm heading appears', R('HARM', 34, gap=10)))
    return out, L, R


def _zoom_in():
    s = []
    c = Col(y=60, gap=24)
    s.append(dict(mode='concept', active=0, title='An argument = a result', script=[
        "The next technique. Before we see exactly how it works, we need to understand one thing first.",
        A('Argument = result appears', c('An argument is really a RESULT: benefit or harm', 44)),
        "An argument is really a result. To use this technique, I need to understand that what I'm looking for here is benefit and harm.",
        A('Better / worse appears', c('"We should do X, because it will be better" · "We should not do X, because it will be worse"', 34)),
        "When I make an argument, what am I really saying? We should do this, because it will be better. Or: we shouldn't, because it will be worse. Right?",
        A('Different parties appears', c('Benefit and harm belong to different parties → who are they, and what does each gain or lose?', 34)),
        "So we need to start thinking in terms of benefit and harm. And benefit and harm can belong to different parties.",
        "In zoom in, we try to understand who the different parties playing in this game are, and what benefit or harm each one gets.",
    ]))
    c = Col(y=60, gap=20)
    s.append(dict(mode='concept', active=1, title='Who, what, how', script=[
        "The way we do it is with three questions: who, what and how.",
        A('Who appears', c('WHO: who are the players? Who takes part?', 38)),
        "Who are the players? Who takes part here?",
        A('What appears', c('WHAT: what benefit, what harm, for each one? (possible: "may", "could", not "will certainly")', 38)),
        "What is the benefit, what is the harm, for each one? By the way, not a certain benefit or harm. What could happen. What benefit may arise, what harm could be caused.",
        "My argument doesn't say this will certainly happen. It says this may happen. And we're back to hedged, qualified writing, and the difference between opinion and fact.",
        A('How appears', c('HOW: how does it happen? Why?', 38)),
        "And how: how does it happen? I need to explain why it happens.",
    ]))
    c = Col(y=60, gap=22)
    s.append(dict(mode='concept', active=2, title='The key sentence', script=[
        A('Who+what appears', c('WHO + WHAT = the key sentence (the short version of the argument)', 40)),
        "Who and what: that's really my key sentence. The argument itself, my short argument. It says who the players are, and what the benefit or harm is.",
        A('Example key sentence appears', c('"In my opinion, face-recognition cameras should be installed in public spaces, since they are likely to prevent or reduce harm to people."', 34, gap=8)),
        A('Who/what labels appears', c('who = people · what = less harm to them', 32, gap=30)),
        "In my opinion, face-recognition cameras should be installed in public spaces, since they are likely to prevent or reduce harm to people. Who are the players? People. What's the benefit? Less harm to them.",
        A('How = development appears', c('HOW = the development and support of the argument paragraph', 40)),
        "And the how? That's how it happens. I need to explain why it happens. That's our development and support inside the argument paragraph, as we'll see later.",
        "Key sentence first, then develop and support it. Explain why it's true. That whole process is the how.",
    ]))
    c = Col(y=60, gap=20)
    s.append(dict(mode='concept', active=3, title='The table', script=[
        "Let's see how it's done in practice.",
        A('Question appears', c('"Should the security services be allowed to install face-recognition cameras in public spaces?"', 34, gap=30)),
        "Here's our question. And we ask ourselves: who? Who are the players? And what? What's the harm or the benefit?",
        A('Table appears', c('Player            |   BENEFIT            |   HARM', 40, gap=10)),
        A('Table rows appears', c('people · law enforcement · society and the state · offenders', 34, gap=30)),
        "I recommend doing it as a table like this. Benefit, harm. And here you simply write the players, who is affected.",
        A('Perspectives optional appears', c('You may tag each item with a perspective or a right: it makes you more precise (optional)', 32)),
        "I'll be using the same perspectives we used before, in zoom out. You don't have to write them. You can just write the benefit. But it makes me more precise.",
        A('Just for you appears', c('Nobody marks this table: it is a thinking tool for you', 32)),
        "And remember: this isn't a table we hand in to anyone. It's for you, to help you think of arguments.",
    ]))
    items, L, R = two_cols('the people')
    s.append(dict(mode='concept', active=4, title='The people', script=[
        "Who are our first players? I chose the people.",
        items[0], items[1], items[2],
        "What benefit or harm may be caused to them? Let's start.",
        A('Fewer thefts appears', L('Fewer thefts and break-ins (economic)', 30)),
        "Economic: fewer thefts. If the areas are filmed there are fewer break-ins, fewer thefts. A benefit. Great.",
        A('Feel safer appears', L('Feeling safer: "I know there are cameras here" (psychological)', 30)),
        "What else? Psychological: feeling safer. Wow, I know there are cameras here, I feel safe.",
        A('Personal security appears', L('Personal security (the right to life and security)', 30)),
        "And personal security, not as a perspective but as a right. The most basic human right: personal security, the right to life. It protects me. A great benefit.",
        A('Privacy harmed appears', R('Harm to privacy: being followed (the right to dignity and privacy)', 30)),
        "What harm could be caused to people? First, harm to privacy. That's also a right: dignity, privacy. I don't want people to know what I do. I don't want to be followed.",
        A('Leaks appears', R('RISK of further harm: personal details leaking (possible, not certain)', 30)),
        "Beyond that harm, which exists, full stop, there's a risk of further harm to privacy through leaks of personal details. My credit card data, all kinds of other data.",
        "The harm to privacy is certain. Will there also be leaks? That's a risk. It isn't certain, but it could happen.",
    ]))
    items, L, R = two_cols('law enforcement')
    s.append(dict(mode='concept', active=5, title='Law enforcement', script=[
        "Which other players do we have? Law enforcement.",
        items[0], items[1], items[2],
        A('Efficiency appears', L('Efficiency: far fewer resources to catch and stop offenders (economic)', 30)),
        "On the benefit side, economic: efficiency. I need to invest far fewer resources in catching or stopping offenders.",
        A('Running cost appears', R('Very high cost of setting up and running the network (economic)', 30)),
        "From the other side, I can look at the economic side and say: wait, there's a very high running cost for setting up such a network. So that's actually a harm.",
        A('Image appears', R('The police\'s image: "they are following us" (social)', 30)),
        "Another harm, social: some damage to image. Think about it: the police are following us. That's unpleasant and uncomfortable. So there's damage to the image of the police.",
        A('Professionalism appears', R('Professional skills fade: relying only on the cameras, officers forget "old-fashioned" police work', 30)),
        "And there could also be damage to professionalism. The officers start saying: I don't need to question people and witnesses any more. I just look at the camera.",
        "There's a danger here too. If officers get used to relying only on cameras, they'll forget the old-fashioned police work.",
    ]))
    items, L, R = two_cols('society and the state')
    s.append(dict(mode='concept', active=6, title='Society and the state', script=[
        "Another player: society, the state. It doesn't always have to be together. Sometimes the state is separate and society is separate. Here I put them together; sometimes it's hard to separate them.",
        "And society is almost always there. Even when the state itself isn't part of the issue, society is often affected somehow. For example: what do you think of the rise in cosmetic surgery? The state isn't involved, but society is.",
        items[0], items[1], items[2],
        A('Safe country appears', L('Living in a safe country: children can play outside (social)', 30)),
        "So what's the benefit here? First, socially, we feel we live in a safe country. That affects us. We can let our children go out and play without worrying every minute where they are.",
        A('Tourism appears', L('A reputation for safety → more tourism (economic)', 30)),
        "Another perspective, economic: tourism. If the country is seen as safe, there'll be more tourism.",
        "You may know it from the opposite side: a beautiful country with a reputation for carjackings and kidnappings on the road. People don't want to go there as tourists, although it's amazing to visit, because it seems frightening.",
        A('Police state appears', R('A "police state": filmed and followed all the time (social, educational)', 30)),
        "And on the harm side, again social, and maybe even educational: a police state. They film us, follow us all the time. It has effects on education, on our children, and socially it affects our daily life.",
        A('Stay at home appears', R('People avoid the street and meet friends only at home (social)', 30)),
        "Maybe, because I know I'm being filmed, I don't want to go out. I meet friends only at home. Being watched? No thanks.",
        A('Police state tourism appears', R('Seen as a police state → fewer visitors (economic)', 30)),
        "And economic here too. If the country is seen as a police state, think of the Soviet Union and the KGB, I'm less keen to go there. They might catch me and do something to me.",
    ]))
    items, L, R = two_cols('the offenders')
    s.append(dict(mode='concept', active=7, title='The offenders', script=[
        "And we also have the offenders themselves. I often mark them in red, because we understand the issue isn't really about them. But they're players in this game too.",
        items[0], items[1], items[2],
        A('Risk to freedom appears', R('A risk to their freedom: suddenly they are filmed', 30)),
        "They have a harm: a risk to their freedom. Suddenly they're filmed. What a thing! Before, I was stealing a bit here, pickpocketing there, all fine. Suddenly they put up cameras.",
        A('Known enforcement appears', L('Enforcement becomes predictable: police may work less hard', 30)),
        "And the benefit? The enforcement becomes known. Today the police do professional police work. Once there are cameras, as we said, their professionalism may suffer and they may stop working hard.",
        A('Crime moves appears', L('They know where the cameras are → crime moves from public to private spaces', 30)),
        "And as an offender, I know where the cameras are. So I say: OK, there are cameras here, I'll steal somewhere else. I'll break in where there are no cameras, in private places.",
        "In other words, crime doesn't go down. It just moves from public space to private space. Because the offender, what can you do, needs to make a living.",
        A('Alibi appears', L('Sophisticated offenders use the cameras: a look-alike creates an alibi', 30)),
        "Not to mention more sophisticated offenders, who can use the cameras to their advantage. For example, to create an alibi: dress in very distinctive clothes, dress a look-alike in the same clothes in front of the cameras, while they commit the offence somewhere else.",
        "It's a bit like playing poker with someone whose cards you can see. They see the police's cards: I know where their cameras are, fine, I'll mislead them and use it against them.",
    ]))
    c = Col(y=60, gap=26)
    s.append(dict(mode='concept', active=8, title='Why it works', script=[
        "Look how nice this technique is. Who, what, how.",
        A('Players easy appears', c('Finding the players is not hard: society and the state are almost always there', 38)),
        "Finding the players isn't too hard. Usually society is there. Even if specific people are linked to the issue, society and the state are often involved in a more indirect way.",
        A('Use rights and perspectives appears', c('Inside each player, use rights and perspectives to find benefits and harms', 38)),
        "And we can use both rights and different perspectives to think of the benefits and harms that could happen.",
        A('Possible harm appears', c('Possible, not certain: "there is a risk that details will leak" is still a potential harm', 36)),
        "Again, it doesn't have to happen. It could happen. It isn't certain that details will leak, but there's a risk, so there's a potential harm.",
        "Let's see another example of this tool, because in my eyes it's very, very effective. By the way, it's the one I use most.",
    ]))
    return s


ZOOM_IN = lesson('vr50-e-zoom-in', 'Finding Arguments: Zoom In',
                 ['An argument = a result', 'Who, what, how', 'The key sentence', 'The table',
                  'The people', 'Law enforcement', 'Society and the state', 'The offenders', 'Why it works'],
                 [dict(mode='title', title='Finding Arguments: Zoom In', script=[
                     "The third technique for finding arguments: zoom in.",
                     "We go into the issue itself: who are the players, and what could each of them gain or lose?",
                 ])] + _zoom_in(), T50)


# =====================================================================================================================
def _tax():
    s = []
    it, bottom = box(TAX_PROMPT, TAX_Q, y=60, w=1100)
    c = Col(y=bottom + 40, gap=16)
    s.append(dict(mode='concept', active=0, title='The task', script=[
        "Another example of zoom in. Here's the task.",
        A('The tax task appears', it),
        "In your opinion, should the state charge large companies a reduced rate of tax?",
        A('Who what how appears', c('Who? What? How?  →  player by player', 40)),
        "Same method. Who, what, how. Player by player.",
    ]))
    items, L, R = two_cols('the state and society')
    s.append(dict(mode='concept', active=1, title='The state: harm', script=[
        "Let's see. First, again, we have the state and society. What's the benefit or harm?",
        items[0], items[1], items[2],
        A('Less tax appears', R('Less tax, less money coming into the state (economic)', 30)),
        "First the harm. Economic: less tax, less money coming into the state.",
        A('Inequality appears', R('Inequality: "The richest pay less? That is not fair." (moral, social)', 30)),
        "There's also a moral side: inequality. What? Why do they pay less tax? And these are large companies with lots of money. So it's the millionaires and the rich who pay less? That's not fair.",
        "That's also social. It has a social effect.",
    ]))
    items, L, R = two_cols('the state and society')
    s.append(dict(mode='concept', active=2, title='The state: benefit', script=[
        "And on the benefit side, I can take the same perspective, economic, just from the other side.",
        items[0], items[1], items[2],
        A('Less unemployment appears', L('Less unemployment → a stronger state in the long term (economic)', 30)),
        "Economic: wait, there'll be less unemployment. Less unemployment strengthens the state. In the long term, admittedly, but it strengthens it.",
        A('Factories abroad appears', L('Without the reduction, the factories go abroad → with it, more tax overall (economic)', 30)),
        "And I can talk about more economic arguments. If these companies don't get reduced tax, they won't build their factories here. They'll go and do it in another country. If they do it here, in the end I actually collect more tax.",
        A('Supporting the weak appears', L('Supporting the weak: helping people who need work (moral; social rights)', 30)),
        "The moral side: supporting the weak. People who need work. As a state I'm committed, I want to help. We said that the social rights include an adequate standard of living and employment conditions, and that includes providing jobs.",
        A('Development appears', L('Development of the area: shops and services grow around the factories (environmental)', 30)),
        "And there's an environmental side: development. Once these large companies set up factories, the whole area usually becomes more developed. Shops that serve them, and so on. That's also a contribution to the state.",
    ]))
    c = Col(y=60, gap=26)
    s.append(dict(mode='concept', active=3, title='Same field, other side', script=[
        "Notice something I did there.",
        A('Obvious appears', c('The obvious argument: "less tax revenue" (economic, against)', 38)),
        "Less tax is the obvious one. The argument everyone sees immediately. And it's economic.",
        A('Other side same field appears', c('An argument from the OTHER side in the SAME field: "less unemployment, factories stay here" (economic, for)', 38)),
        "But I show you: hop, on the economic side there's actually something that could be better.",
        A('Critical thinking appears', c('→ this usually signals strong critical thinking', 40)),
        "When there are very common or obvious arguments in a certain field, if I manage to bring an argument from the other side in the same field, it usually signals high critical thinking.",
    ]))
    items, L, R = two_cols('the unemployed')
    s.append(dict(mode='concept', active=4, title='The unemployed', script=[
        "Another player: the unemployed. Someone who is unemployed and will now get a job has a very clear benefit.",
        items[0], items[1], items[2],
        A('Jobs appears', L('They get jobs in these companies (economic)', 30)),
        "They'll get jobs in these companies. That's the economic side.",
        A('Sense of worth appears', L('A sense of worth; out of the stress and depression (psychological)', 30)),
        "But there's also a psychological side. I told you I really love this perspective, because it isn't common. Not many students use it.",
        "When an unemployed person starts working, they have a sense of worth. They get out of the stress, out of the depression.",
        A('Economic feeds psychological appears', L('Less financial pressure → calmer', 30)),
        "And the economic side affects the psychological side too, of course. Once you're under less financial pressure, you're calmer.",
    ]))
    items, L, R = two_cols('other citizens')
    s.append(dict(mode='concept', active=5, title='Other citizens', script=[
        "Other citizens. Not the ones who got jobs. The others. What about them?",
        items[0], items[1], items[2],
        A('Pay more appears', R('If the companies pay less, we pay more: the state\'s budget must be filled (economic)', 30)),
        "Wait. If these companies pay less tax, we'll pay more tax. Someone has to pay these taxes in the end. The state has a budget and it has to be filled. From where? From taxes. Who pays them? We do.",
        "If these companies paid more tax, we'd pay less. But no. Right now we're harmed.",
        A('Frustration appears', R('A sense of unfairness: anger and frustration (psychological)', 30)),
        "And psychological: inequality. We talked about inequality as a moral matter, but I think it also has a psychological side.",
        "I remember it from discussions with friends about large factories that pay little tax: what, they don't pay taxes? They're taking our country's resources. It's not fair. It annoys people, it frustrates them.",
        A('Tax evasion appears', R('"They do not pay, so why should I?" → more tax evasion', 30)),
        "And it could make other citizens say: what, they don't pay tax? Then I won't either. Now I'm evading tax.",
        "Quite a few people use exactly that justification: I evade tax, because they're cheating me here, so I'll cheat back.",
    ]))
    items, L, R = two_cols('the companies')
    s.append(dict(mode='concept', active=6, title='The companies', script=[
        "And of course we have the companies. Again, I'd mark them in red, because often we won't take the arguments about them. But they have benefit and harm too.",
        items[0], items[1], items[2],
        A('Pay less appears', L('They pay less tax', 30)),
        "The benefit, of course: they pay less tax.",
        A('Image harm appears', R('Their image: seen as tax dodgers, above everyone else → protests, boycotts', 30)),
        "And the harm, for example: image. They're seen as avoiding tax, as thinking they're above everyone else. There could be protests against them, or even a boycott of their other businesses.",
        "See how, when we dig deeper and look each time at a different player and focus on it, we can go deeper and deeper and find more and more potential benefits and harms.",
    ]))
    c = Col(y=60, gap=26)
    s.append(dict(mode='concept', active=7, title='Focus', script=[
        "What this technique mainly does, I think, is give you focus.",
        A('General is hard appears', c('"I\'m trying to think of arguments... something general" → hard', 36)),
        "Often, when students try to think of arguments, they say in their heads: OK, I'm trying to think of arguments, something general. That's hard.",
        A('Zoom out direction appears', c('Zoom out: a perspective → who does it affect?  (economic → the state? the unemployed? citizens?)', 34)),
        "In zoom out, I take one perspective, say economic, and ask: who does it affect? The state? The unemployed? The citizens?",
        A('Zoom in direction appears', c('Zoom in: a player → which perspectives and rights?  (the state → economic? moral? social?)', 34)),
        "In zoom in we go the other way. I take a certain player, say the state, and ask: in which fields is it affected? Which rights are involved?",
        A('Same technique appears', c('The same technique from the other side. Either way: focus on one thing at a time.', 36)),
        "It's exactly the same technique, from the other side. And either way it creates focus. When you look only at the state, you can find arguments about it, instead of thinking in general about everyone at once.",
    ]))
    return s


TAX = lesson('vr50-e-zoom-in-tax', 'Zoom In: Reduced Tax',
             ['The task', 'The state: harm', 'The state: benefit', 'Same field, other side', 'The unemployed',
              'Other citizens', 'The companies', 'Focus'],
             [dict(mode='title', title='Zoom In: Reduced Tax', script=[
                 "Zoom in, a second example: reduced tax for large companies.",
                 "Player by player, we'll find benefits and harms, and see how deep this technique can go.",
             ])] + _tax(), T50)


# =====================================================================================================================
def _test():
    s = []
    c = Col(y=60, gap=26)
    s.append(dict(mode='concept', active=0, title='What makes it good', script=[
        "So after we've found our arguments, how do we know whether they're good or not? First of all, what is a good argument?",
        A('Direct link appears', c('1 · A DIRECT link to the question under discussion (relevance to the task)', 38)),
        "First: we need a direct link to the question under discussion. Remember relevance to the task?",
        A('Simple appears', c('2 · SIMPLE: you can say it in one breath', 38)),
        "Second: it needs to be simple. And by simple I mean a rule of thumb: you can say it in one breath, without stopping in the middle to take a breath. Otherwise it's probably too complicated, too long, too clumsy.",
        A('Logical links appears', c('3 · LOGICAL links between the steps of the explanation (the how)', 38)),
        "And the part connected to the development, to the how: when we explain it, there must be a logical connection between the links that make up the explanation.",
        "In the table we didn't write the whole development. But we did it in our heads. When I talked to you, I explained how this affects that, and how a benefit or harm is created.",
        "So make sure you have a clear logical chain in your head, leading from choosing for or against all the way to the result, the benefit or the harm.",
    ]))
    c = Col(y=60, gap=20)
    s.append(dict(mode='concept', active=1, title='Direct link: miss 1', script=[
        "Let's see some examples. A direct link to the question.",
        A('Miss 1 appears', c('✗ "In my opinion, face-recognition technology is not yet developed enough, so it cannot be relied on."', 36, gap=30)),
        "In my opinion, face-recognition technology is not yet developed enough, so it cannot be relied on.",
        A('Why it misses appears', c('The task already says the technology identifies people "with a high degree of certainty". That is a given fact.', 34)),
        "We understand this misses the question a bit. Whether the technology is developed enough or not is already a given. It's even given in the task. It isn't in doubt at all.",
        "It's written in the task that the technology is good enough and identifies with a high degree of certainty. That's it, it's good enough.",
        A('Do not argue with facts appears', c('Do not argue with the facts the task gives you', 40)),
        "I can't say now: wait, the facts the test gave me in the task aren't true.",
    ]))
    c = Col(y=60, gap=20)
    s.append(dict(mode='concept', active=2, title='Direct link: miss 2', script=[
        A('Miss 2 appears', c('✗ "In my opinion, face-recognition technology can be useful in many areas."', 36, gap=30)),
        "In my opinion, face-recognition technology can be useful in many areas.",
        "Great, we're glad that's what you think. But how is it connected to the question under discussion?",
        A('The question appears', c('The question: cameras in PUBLIC spaces, installed by the security services', 36)),
        "We asked whether the police or the security services should install face-recognition cameras in public spaces.",
        A('Social media appears', c('"It can recognise my friends in photos on social media" → nice, but not the question', 34)),
        "That it can be useful? Great. You think it can be useful in public spaces too? Talk only about that. Not about all kinds of things, like recognising my friends in photos on social media faster. Cool. How is it connected to the question?",
        A('Stay on the decision appears', c('Same decision, same people, same setting as the task', 36)),
        "It's exactly what we said when we analysed the task: stay with the same decision, the same people, the same setting.",
    ]))
    c = Col(y=60, gap=20)
    s.append(dict(mode='concept', active=3, title='Simple: one breath', script=[
        "Simple.",
        A('Long sentence appears', c('✗ "In my opinion, installing a network of face-recognition cameras in public spaces will make people feel safer, which will spread by word of mouth and create an image of a safe country, which will lead to more tourism, so that both the state and its citizens will earn more."', 30, gap=30)),
        "In my opinion, installing a network of face-recognition cameras in public spaces will make people feel safer, which will spread by word of mouth and create an image of a safe country, which will lead to more tourism, so that both the state and its citizens will earn more...",
        "Sorry, I stopped to take a breath, because I wasn't breathing.",
        A('Short sentence appears', c('✓ "In my opinion, installing a network of face-recognition cameras in public spaces will create an image of a safe country and increase tourism."', 32, gap=30)),
        "I hope it's clear this sentence is too long and clumsy. I can condense it: in my opinion, installing a network of face-recognition cameras in public spaces will create an image of a safe country and increase tourism.",
        A('Rest goes to development appears', c('Why more tourism is good, and how it happens → the development, not the key sentence', 32)),
        "From here, it's clear that more tourism is a good thing. And even if not, I can explain it later, in the development.",
    ]))
    c = Col(y=60, gap=20)
    s.append(dict(mode='concept', active=4, title='Logical links', script=[
        "Logical links. This doesn't appear in the table either, but I need to make sure in my head that everything fits. So we won't see a paragraph now, just a logical chain.",
        A('Wrong chain appears', c('✗ cameras → deterrence → awareness → less crime', 40, gap=10)),
        A('Wrong why appears', c('How can people be deterred before they know the cameras are there?', 32, gap=36)),
        "When there are cameras, the cameras cause deterrence, which causes awareness, which causes less crime.",
        "Clearly there's no logic here. No connection between the steps.",
        A('Right chain appears', c('✓ cameras → awareness that there are cameras → deterrence → less crime', 40, gap=36)),
        "The right steps: there are cameras. Then there's awareness that there are cameras. That causes deterrence. And then crime goes down.",
        A('Check the chain appears', c('Make sure your chain works and is logical, from the decision to the result', 36)),
        "So make sure your chain, your logical sequence, works correctly and makes sense.",
    ]))
    c = Col(y=60, gap=20)
    s.append(dict(mode='concept', active=5, title='The chain', script=[
        "Now let's turn that into a working method. I call it the chain.",
        A('The chain appears', c('THE CHAIN: before you write, draft each argument as short cause → effect steps', 40)),
        "For every argument, before you write, draft a chain of short steps. Cause, then effect, then effect.",
        A('From the task to the result appears', c('from the thing the task asks about  →  ...  →  the final result (benefit or harm)', 36)),
        "It starts from the exact thing the task asks about, and ends at the final result: the benefit or the harm.",
        A('About ten words appears', c('About ten words per argument: short notes, but never drop a necessary link to make it shorter', 34)),
        "About ten words per argument is usually enough. Short notes. But don't drop a link you need just to make the chain shorter.",
        A('Example chain appears', c('cameras in public spaces → offenders know they are filmed → fear of being identified → fewer offences there', 34)),
        "For example: cameras in public spaces, offenders know they're filmed, they fear being identified, fewer offences there.",
        A('Why it helps appears', c('Later you paste the chain into the argument paragraph: nothing is skipped, you do not get lost', 34)),
        "Later, in the argument paragraph lessons, you'll paste this chain into the paragraph with a template. So nothing is skipped, and you don't get lost in the middle.",
        "There we'll also learn to test every arrow, and to use the other side's chain to find its weak spot. For now: draft a chain for every argument you find.",
    ]))
    c = Col(y=60, gap=22)
    s.append(dict(mode='concept', active=6, title='Summary', script=[
        "Let's sum up the techniques for finding arguments.",
        A('Rights appears', c('Rights: which rights are harmed, or at play? Too much, or proportionately?', 34)),
        "Rights: which rights are harmed, or at play, in this issue?",
        A('Zoom out appears', c('Zoom out: the wider frame + perspectives → how each one affects each player', 34)),
        "Zoom out: understand the wider frame of the debate, look through different perspectives, and in each perspective ask how it affects the different players.",
        A('Zoom in appears', c('Zoom in: who, what, how → start from the players, then which rights and perspectives affect each', 34)),
        "Or go from the other side. Zoom in: who, what, how. Who are the players, what do they gain or lose, and how does it happen.",
        A('Test appears', c('Then test each argument: direct link · simple · logical links (the chain)', 34)),
        "Then test each argument: a direct link, simple, and logical links. Draft its chain.",
        "Next, we move on to actually writing the essay. We'll start with paragraphs, and at the end put them all together into a whole essay. Hopefully a perfect one, or almost. But a good one.",
    ]))
    return s


TEST = lesson('vr50-e-test', 'Is It a Good Argument?',
              ['What makes it good', 'Direct link: miss 1', 'Direct link: miss 2', 'Simple: one breath',
               'Logical links', 'The chain', 'Summary'],
              [dict(mode='title', title='Is It a Good Argument?', script=[
                  "We've found arguments. Now: are they any good?",
                  "Three tests for every argument, and a planning tool, the chain, that makes the third test easy.",
              ])] + _test(), T50)


MODULES = [ANALYSE, GATHER, POSITION, ARGS_INTRO, RIGHTS, ZOOM_OUT, ZOOM_IN, TAX, TEST]

MEMORY = [dict(
    id='mem-wr-planning', after='vr50-e-test', title='Planning: analyse the task & find arguments',
    intro='Before writing: analyse the task, gather what it gives you, choose a position you can explain, '
          'find arguments with three techniques, and test each one.',
    tables=[
        dict(title='1 · Analyse the task', head=['Ask', 'What to look for'], rows=[
            ['Same or different aim?', 'Friends with one aim, different ways, or rivals with different interests'],
            ['A particular case of...?', 'The wider debate (cameras = security vs privacy)'],
            ['Is the state a side?', 'Then it is often a clash of rights'],
            ['What kind of task?', 'Yes/no · degree (obvious or hidden: absolute end vs flexible end) · "why" (side chosen for you) · three opinions (ends + middle, or three different)'],
            ['The exact question', 'The decision · the people affected · the conditions. Do not drift to a different question.'],
            ['Every part?', 'Cover every element the question names (e.g. advantages AND disadvantages, for residents AND for the city)'],
        ]),
        dict(title='2 · Gather from the task (2-3 minutes)', head=['Part of the task', 'Where it goes'], rows=[
            ['Background = facts', 'The opening paragraph'],
            ['The sides\' claims = opinions', 'Material for argument paragraphs, counter-arguments, weakenings'],
            ['Key words and conditions', 'Keep you on the exact question; may become an argument or a weakening'],
        ]),
        dict(title='3 · Choosing a position (considerations, not rules)', head=['Consideration', 'Usually easier to explain'], rows=[
            ['Material in the task', 'The side with more detail'],
            ['Your own opinion', 'What convinced you: explain why'],
            ['Common vs individual good', 'The common good'],
            ['A moral consideration', 'The more moral side (e.g. protecting a vulnerable group)'],
            ['The existing situation', 'Not changing it (but think again about an old law)'],
            ['Degree tasks', 'No extremes: the flexible end → a complex position with safeguards'],
            ['Rights', 'The right the task explains in detail'],
            ['Three opinions', 'The middle (≈ 80 + 80 instead of 100 / 0)'],
        ]),
        dict(title='4 · Three techniques for finding arguments', head=['Technique', 'How'], rows=[
            ['Rights', 'Natural (life, liberty, movement, occupation, property, equality, dignity → privacy) · civil (vote, association, press, expression) · social (education, health, housing, work). Argue the harm is too great, or proportionate, in THIS task.'],
            ['Zoom out', 'The wider frame + perspectives: economic · social · educational · psychological (+ moral, environmental, legal...) → how each affects each player'],
            ['Zoom in', 'Who (the players) · what (possible benefit / harm) · how (the development). Who + what = the key sentence.'],
        ]),
        dict(title='5 · The argument test', head=['Test', 'Check'], rows=[
            ['Direct link', 'Answers the exact question; does not dispute facts the task gives'],
            ['Simple', 'The key sentence can be said in one breath'],
            ['Logical links', 'Draft the chain (~10 words): task → ... → result. Ask of every arrow "why would this lead to the next?"; add an explanation or condition; no arrows that just rename a step.'],
            ['Other side', 'Write the opponent\'s chain; its weakest arrow = your weakening / rebuttal'],
        ]),
    ],
    tips=['Aim for facts and reasonable assumptions, not only opinions; "in my opinion" goes only where the opinion starts.',
          'Original angles (e.g. psychological) stand out, but only if they are explained as well as any other argument.',
          'Practise finding arguments on published tasks, without always writing the whole essay.'])]

MODULES = split_task_slides(MODULES)
