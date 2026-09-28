# Verbal Reasoning · Topic 50 · Writing task — part B: the language rubric and academic language.
# Source: the teacher's Hebrew lessons seg06 (language rubric overview), seg07 (fitting academic writing + qualified
# writing), seg08 (qualified writing - the same material as the end of seg07, kept once) and seg09 (semantic precision).
# Hebrew-specific examples are replaced by English ones that make the same point; the teacher's running examples
# (face-recognition cameras, electric bicycles, road enforcement, the student sentences in seg09) are translated.
# Official facts from nite_verbal_guide.txt: 35 minutes, the six language criteria, raters read a first draft.
from dsl import *
from xml.sax.saxutils import escape as _e
import re as _re

T50 = 50

# ------------------------------------------------------------------ before / after boxes
# box('bad'|'good'|'plain', text, y) -> a framed sentence. Words inside [[...]] are bold and coloured
# (red in a 'bad' box, green in a 'good' box, blue in a 'plain' box).
_COL = dict(bad=('#FDECEC', '#E5484D'), good=('#E7F6EE', '#0F9D58'), plain=('#F6F8FC', '#2F6BFF'))
_INK = '#0B1220'


def _tokens(text):
    """-> list of words; each word = list of (segment, bold). [[ and ]] may sit inside a word (e.g. '[[night]],')."""
    out, bold = [], False
    for raw in text.split():
        segs = []
        for j, part in enumerate(_re.split(r'(\[\[|\]\])', raw)):
            if part == '[[': bold = True
            elif part == ']]': bold = False
            elif part: segs.append((part, bold))
        if segs: out.append(segs)
    return out


def box(kind, text, y, fs=32, w=1140, x=410, note=None, top=22):
    fill, stroke = _COL[kind]
    icon = kind != 'plain'
    left = 92 if icon else 30
    maxw = w - left - 30
    cw = fs * 0.46                     # Georgia average character width (a little generous)
    lines, cur, curw = [], [], 0
    for word in _tokens(text):
        ww = sum(len(t) * cw * (1.12 if b else 1) for t, b in word) + cw
        if cur and curw + ww > maxw:
            lines.append(cur); cur, curw = [], 0
        cur.append(word); curw += ww
    if cur: lines.append(cur)
    lh = fs * 1.38
    body = []
    yy = top + fs
    for ln in lines:
        spans = []
        for j, word in enumerate(ln):
            for k, (t, b) in enumerate(word):
                sp = (' ' if j and not k else '') + _e(t)
                spans.append('<tspan font-weight="700" fill="%s">%s</tspan>' % (stroke, sp) if b else '<tspan>%s</tspan>' % sp)
        body.append('<text x="%g" y="%g" font-family="Georgia, \'Times New Roman\', serif" font-size="%g" fill="%s" '
                    'xml:space="preserve">%s</text>' % (left, yy, fs, _INK, ''.join(spans)))
        yy += lh
    if note:
        yy += 4
        body.append('<text x="%g" y="%g" font-family="Arial, Helvetica, sans-serif" font-size="%g" font-style="italic" '
                    'fill="#475569">%s</text>' % (left, yy, fs * 0.8, _e(note)))
        yy += lh * 0.8
    H = int(yy - fs + top + 14)
    g = ['<rect x="2" y="2" width="%d" height="%d" rx="14" fill="%s" stroke="%s" stroke-width="3"/>' % (w - 4, H - 4, fill, stroke)]
    if icon:
        cx, cy = 46, top + fs * 0.62
        g.append('<circle cx="%g" cy="%g" r="22" fill="%s"/>' % (cx, cy, stroke))
        if kind == 'bad':
            g.append('<path d="M %g %g l 18 18 M %g %g l -18 18" stroke="#fff" stroke-width="5" stroke-linecap="round"/>'
                     % (cx - 9, cy - 9, cx + 9, cy - 9))
        else:
            g.append('<path d="M %g %g l 7 8 l 14 -17" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" '
                     'stroke-linejoin="round"/>' % (cx - 11, cy + 1))
    label = {'bad': 'Before', 'good': 'After', 'plain': 'Example'}[kind]
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="%s"><title>%s</title>%s%s</svg>'
           % (w, H, label, label, ''.join(g), ''.join(body)))
    return dict(k='vis', v={'type': 'geometry', 'svg': svg}, x=x, y=y, w=w, h=H)


def below(item, gap=22):
    return item['y'] + item['h'] + gap


# ======================================================================================= lesson 1: the language rubric
SB_RUB = ['Technical lessons', 'Tired? Skip ahead', 'The language rubric', 'Clarity', 'Academic style',
          'Semantic precision', 'Grammar', 'Sentence structures', 'Organizational tools']

# ======================================================================================= lesson 2: academic writing
SB_ACAD = ['What is it?', 'Literary vs academic', 'No personal tone', 'The neutral narrator', 'Creativity',
           'Head, not heart', 'Who may speak', 'No flowery language', 'Rhetorical devices', 'Everyday English',
           'Absolute claims', 'Before and after', 'Five rules']

# ======================================================================================= lesson 3: qualified writing
SB_HEDGE = ['No word lists', 'A guess as a fact', 'Add one word', 'Two absolutes', 'Most or many?',
            'Every driver?', 'Hedge the start', 'Plain, calm words', 'The full fix', 'Hedging words',
            'Hedge, but take a side']

# ======================================================================================= lesson 4: semantic precision
SB_PREC = ['What it means', 'Does it cost points?', 'Why students slip', 'The wheelie', 'A broken idiom',
           'The wrong word', 'Invented phrases', 'Idiom, wrong place', 'Look-alike words',
           'Words change the claim', 'One term throughout', 'The main lesson']

# --- boxes used below (positions computed so that nothing overlaps)
# lesson 2
B_PERS_BAD = box('bad', '[[When I was in high school,]] the cameras in [[my]] neighbourhood made [[me]] feel much safer, so [[I am sure]] they work.', 250)
B_PERS_GOOD = box('good', 'Cameras in public places [[may]] give residents a greater sense of safety, which [[in turn]] may encourage them to use parks and streets in the evening.', below(B_PERS_BAD))
B_EMO_BAD = box('bad', 'It is [[heartbreaking]] to think of [[innocent]] people being [[watched like criminals]] every single day.', 240)
B_EMO_GOOD = box('good', 'Constant identification of people who are not suspected of any crime [[may limit]] their privacy and their freedom of movement.', below(B_EMO_BAD))
B_WHO_BAD = box('bad', '[[We]] must understand that [[you]] cannot stop crime without cameras, so [[we]] need them.', 400)
B_WHO_GOOD = box('good', '[[I believe that]] cameras [[can]] help the police prevent certain crimes. [[In my opinion,]] they are therefore necessary.', below(B_WHO_BAD))
B_FLOW_BAD = box('bad', 'Like [[a silent guardian of the night]], the camera watches [[over the sleeping city]], [[a shining beacon]] of security.', 250)
B_FLOW_GOOD = box('good', 'Cameras operate at night, when fewer police officers are on patrol.', below(B_FLOW_BAD))
B_RQ_BAD = box('bad', '[[Is it acceptable]] that workers work and do not get paid for their work?', 225, fs=28, top=16)
B_RQ_GOOD = box('good', 'Workers who are not paid on time may find it difficult to cover their basic expenses.', below(B_RQ_BAD, 12), fs=28, top=16)
Y_PROV = below(B_RQ_GOOD, 26)
B_PROV_BAD = box('bad', 'The city should keep its current system, because [[a bird in the hand is worth two in the bush]].', Y_PROV + 62, fs=28, top=16)
B_PROV_GOOD = box('good', 'The city should keep its current system, since its results are known, while the results of the new system are uncertain.', below(B_PROV_BAD, 12), fs=28, top=16)
B_BA_BAD = box('bad', "[[Let's be honest:]] who actually wants cameras watching them [[all day]]? [[I know I don't.]] "
               "Face-recognition cameras are [[a total nightmare]] for privacy, and [[everyone knows]] they'll be misused. "
               "[[You'd have to be crazy]] to support this!", 110, fs=28)
B_BA_GOOD = box('good', 'Face-recognition cameras in public spaces [[may]] seriously limit privacy. These systems record the movements '
                'of people who are not suspected of any crime, and this information [[could]] be misused [[if]] it is not '
                'properly protected. [[For this reason, I believe that]] their use should be limited.', below(B_BA_BAD, 30), fs=28)
# lesson 3
B_EB_BAD = box('bad', 'A ban on electric bicycles [[will reduce]] the number of road accidents.', 130)
B_EB_GOOD = box('good', 'A ban on electric bicycles [[may reduce]] the number of road accidents.', 130)
B_CAM_BAD = box('bad', '[[There is no doubt that most]] of the public will oppose the installation of face-recognition cameras in public places.', 130)
B_CAM_MID = box('plain', '[[Most]] of the public will oppose the installation of face-recognition cameras in public places.', 130)
B_CAM_GOOD = box('good', '[[Many]] members of the public will oppose the installation of face-recognition cameras in public places.', 580)
B_RD_BAD = box('bad', 'Without enforcement on the roads, [[every driver]] will [[do whatever he wants]], and the roads will [[turn into a war zone]].', 130)
B_RD_1 = box('plain', '[[It is likely that,]] without enforcement on the roads, every driver will do whatever he wants, and the roads will turn into a war zone.', 130)
B_RD_2 = box('plain', 'It is likely that, without enforcement on the roads, [[many drivers]] will do whatever they want, and the roads will turn into a war zone.', 130)
B_RD_3 = box('plain', 'It is likely that, without enforcement on the roads, many drivers [[will not obey the law]], and the roads will turn into a war zone.', 130)
B_RD_BAD2 = box('bad', 'Without enforcement on the roads, every driver will do whatever he wants, and the roads will turn into a war zone.', 130)
B_RD_GOOD = box('good', '[[It is likely that,]] without enforcement on the roads, [[many drivers will not obey the law]], and [[driving will become dangerous]].', below(B_RD_BAD2, 26))
B_OVER_BAD = box('bad', 'It [[might perhaps possibly]] be the case that cameras [[could in some ways]] help the police [[to some extent]].', 250)
B_OVER_GOOD = box('good', 'Cameras [[can]] help the police identify suspects [[more quickly]].', below(B_OVER_BAD))
# lesson 4
B_IDIOM_BAD = box('bad', 'Without a strong police force, criminals would have [[free reign]].', 250)
B_IDIOM_GOOD = box('good', 'Without a strong police force, criminals [[could act without fear of punishment]].', below(B_IDIOM_BAD))
B_ELITE_BAD = box('bad', 'The government should also take responsibility for the weaker groups in society and not focus only on the [[elitists]].', 130)
B_ELITE_GOOD = box('good', 'The government should also take responsibility for the weaker groups in society and not focus only on the [[elites]].', below(B_ELITE_BAD))
B_UNI_BAD = box('bad', 'I believe that the presidency encourages [[uniformity]] among the public.', 130)
B_UNI_GOOD = box('good', 'I believe that the presidency encourages [[unity]] among the public.', below(B_UNI_BAD))
B_ADM_BAD = box('bad', 'Only a few young people are interested in what happens in the country [[administrative-wise]].', 80, fs=26, top=16)
B_ADM_GOOD = box('good', 'Only a few young people are interested in [[how the country is governed]].', below(B_ADM_BAD, 10), fs=26, top=16)
B_VETO_BAD = box('bad', 'The state has no [[moral veto]] to harm the right of parents to choose how to educate their children.', below(B_ADM_GOOD, 24), fs=26, top=16)
B_VETO_GOOD = box('good', 'The state has no [[legitimate grounds]] for violating the right of parents to choose how to educate their children.', below(B_VETO_BAD, 10), fs=26, top=16)
B_SPORT_BAD = box('bad', 'Some students object to compulsory sports courses because they are not interested in [[sportive time]].', below(B_VETO_GOOD, 24), fs=26, top=16)
B_SPORT_GOOD = box('good', 'Some students object to compulsory sports courses because they are not interested in [[time set aside for sport]].', below(B_SPORT_BAD, 10), fs=26, top=16)
B_FOOT_BAD = box('bad', 'It is possible that some people will [[shoot themselves in the foot]] and publish private information about citizens without permission.', 130)
B_FOOT_GOOD = box('good', 'It is possible that some people will [[publish]] private information about citizens without permission.', 580)
B_SUS_BAD = box('bad', 'Face-recognition cameras help the police find [[criminals]] in the crowd.', 250)
B_SUS_GOOD = box('good', 'Face-recognition cameras help the police find [[suspects]] in the crowd.', below(B_SUS_BAD))
B_TERM_BAD = box('bad', 'Face-recognition cameras may reduce crime. ... However, [[security cameras]] are expensive. ... Finally, '
                 '[[surveillance]] should be limited.', 250)
B_TERM_GOOD = box('good', 'Face-recognition cameras may reduce crime. ... However, [[face-recognition cameras]] are expensive. ... '
                  'Finally, the use of [[these cameras]] should be limited.', below(B_TERM_BAD))


MODULES = [
# ============================================================================ lesson 1 · seg06
lesson('vr50-b-language-rubric', 'The Language Rubric', SB_RUB, [
 dict(mode='title', title='The Language Rubric', script=[
  "Now we're starting a series of lessons on the language side of the essay.",
  "What the raters check in your language — and how to improve it.",
 ]),
 dict(mode='concept', active=0, title='Technical lessons', script=[
  "I'll be honest with you: these lessons are fairly technical.",
  A("Same rules as school English appears", T('Basically the same grammar and style you learned at school', size=40, x=410, y=110, w=1140)),
  "Broadly, it's the same language and grammar you learned at school. The same rules.",
  A("You don't need every term appears", T("You don't need every rule or every term: subject, predicate, clause types, verb forms ...", size=34, x=410, y=240, w=1140)),
  "But for the psychometric exam you don't need to know every rule in detail — and certainly not all the names.",
  "Subject, predicate, types of clauses, verb forms and so on. You can let those go.",
  A("What we will learn appears", T('What we will learn: what is expected · common mistakes · what to avoid · small tips that raise your score', size=34, x=410, y=380, w=1140)),
  "What we will learn is what's expected of you, the common mistakes, what to avoid — and lots of small tips that help you improve.",
 ]),
 dict(mode='concept', active=1, title='Tired? Skip ahead', script=[
  "These lessons can be a bit tiring. There are a lot of technical details.",
  "So if you feel worn out — before you give up on the essay altogether — stop for a second.",
  A("Skip to the content rubric appears", T('Feeling worn out?  Skip ahead to the content rubric', size=42, x=410, y=110, w=1140)),
  "Skip ahead to the content lessons. The material there is newer, maybe a bit more interesting, and less technical.",
  "And you have a lot to learn and improve there too.",
  A("Come back later appears", T('Come back to the language lessons whenever you are ready', size=38, x=410, y=230, w=1140)),
  "You can always come back to these language lessons at the end.",
  "Move on with the content and with how to build the essay, and when you want to improve your language, come back and watch these.",
  A("Not a prerequisite appears", T('They are not a base you must finish first. They are the rules for writing correctly and in an academic style.', size=34, x=410, y=340, w=1140)),
  "It's no problem at all to move on. These lessons are not a base that you can't continue without.",
  "Again: they are simply the rules for writing correctly, in a way that fits academic writing. You can come back to them later.",
 ]),
 dict(mode='concept', active=2, title='The language rubric', script=[
  "As you already know, the raters score your writing according to fixed criteria, set in advance.",
  "Those criteria are listed in the rubric. Now we'll go over the language rubric — the parameters being checked.",
  A("The five rows appear", T('The language rubric — each row is rated from 1 to 6:', size=40, x=410, y=100, w=1140)),
  A("Row 1 appears", T('1 · Clarity and consistency with academic writing', size=36, x=450, y=180, w=1100)),
  A("Row 2 appears", T('2 · Semantic precision', size=36, x=450, y=250, w=1100)),
  A("Row 3 appears", T('3 · Grammar', size=36, x=450, y=320, w=1100)),
  A("Row 4 appears", T('4 · Syntactic structures (sentence structure)', size=36, x=450, y=390, w=1100)),
  A("Row 5 appears", T('5 · Organizational tools', size=36, x=450, y=460, w=1100)),
  "We won't go into every detail now — just what is expected of you in each parameter, in general.",
  A("A lesson for each appears", T('After this overview: a separate lesson on each row — what to do, how to do it, how to improve', size=32, x=410, y=560, w=1140)),
  "Then there is a separate lesson on each one, so you understand exactly what to do, how to do it, and how to improve.",
 ]),
 dict(mode='concept', active=3, title='Clarity', script=[
  "The top part of the rubric is: clarity, and consistency with academic writing.",
  A("Clarity appears", T('Clarity: the rater must understand your ideas easily', size=42, x=410, y=110, w=1140)),
  "Clarity means, first of all, that your essay must be clear. The ideas you are trying to express must be clear to the person reading them.",
  "It's not by chance that NITE put this word first.",
  A("Great ideas, unclear writing appears", T('Great arguments + unclear writing = the rater cannot tell what they are', size=38, x=410, y=240, w=1140)),
  "If you have great ideas for arguments, but they are written unclearly, the raters will find it very hard to understand what they are.",
  D("teacher circles 'cannot tell what they are'"),
 ]),
 dict(mode='concept', active=4, title='Academic style', script=[
  "The second part: consistency with academic writing. That means your writing fits the academic style.",
  A("Academic writing appears", T('Consistency with academic writing = your wording fits the academic style', size=40, x=410, y=110, w=1140)),
  "Academic writing is a type of writing you probably haven't really practised yet. We'll have a whole lesson on it.",
  A("The official instruction appears", T('The exam instructions: "Use a style that is consistent with academic writing."', size=36, x=410, y=240, w=1140)),
  "And the exam instructions say it directly: use a style that is consistent with academic writing.",
  "NITE also details what this is made of — the next rows of the rubric. Let's go over them.",
 ]),
 dict(mode='concept', active=5, title='Semantic precision', script=[
  "The first parameter: semantic precision.",
  A("Semantic precision appears", T('Semantic precision: every word says exactly what you mean', size=40, x=410, y=110, w=1140)),
  "Your language has to express your ideas precisely.",
  "What does that mean? That we use words and expressions in the right context — and in their correct form.",
  A("Demand 1 appears", T('1 · the right word or expression, in the right context', size=36, x=450, y=230, w=1100)),
  A("Demand 2 appears", T('2 · in its correct form — not a broken version of it', size=36, x=450, y=310, w=1100)),
  "Sometimes people distort an expression. So we need to use the expression correctly, and use the word in a place that fits the content.",
 ]),
 dict(mode='concept', active=6, title='Grammar', script=[
  "The next parameter: grammar. Correct language.",
  A("Grammar appears", T('Grammar: correct language — as few errors as possible', size=40, x=410, y=110, w=1140)),
  "Just like it sounds. The language has to be correct — without mistakes.",
  A("Not a perfect essay appears", T('But NITE does not expect a perfect essay in 35 minutes', size=40, x=410, y=220, w=1140)),
  "But NITE doesn't expect a perfect essay written in thirty-five minutes. Raters read it as a first draft. We'll see what that means in the proofreading lesson.",
 ]),
 dict(mode='concept', active=7, title='Sentence structures', script=[
  "The next parameter: syntactic structures.",
  A("Sentence structures appears", T('Sentence structures: how you build your sentences and paragraphs', size=40, x=410, y=110, w=1140)),
  "That's basically the way you build the sentences that make up the essay — the sentences and the paragraphs.",
  A("Serve the ideas appears", T('The structure must serve your ideas: it should help the reader follow what you are saying', size=36, x=410, y=240, w=1140)),
  "And it has to serve your ideas well. Your sentences and paragraphs should support what you are trying to say.",
  A("Variety appears", T('Higher scores: varied and complex sentences, used correctly', size=36, x=410, y=370, w=1140)),
  "In the rubric, the high scores go to varied and complex sentence structures — used appropriately. We'll see how in its own lesson.",
 ]),
 dict(mode='concept', active=8, title='Organizational tools', script=[
  "And the last parameter in the rubric: organizational tools.",
  A("Organizational tools appears", T('Organizational tools:', size=40, x=410, y=100, w=1140)),
  A("Connectors appears", T('· connectors  (because, however, therefore ...)', size=36, x=450, y=170, w=1100)),
  A("Transition sentences appears", T('· transition sentences between ideas and paragraphs', size=36, x=450, y=240, w=1100)),
  A("Paragraphs appears", T('· correct division into paragraphs', size=36, x=450, y=310, w=1100)),
  "Here you're expected to use connectors correctly, write transition sentences, and divide the essay into paragraphs properly.",
  "Again, we'll expand on this later. Each of these parameters gets its own lesson, starting with academic writing.",
 ]),
], T50),

# ============================================================================ lesson 2 · seg07 (first part)
lesson('vr50-b-academic', 'Academic Writing', SB_ACAD, [
 dict(mode='title', title='Academic Writing', script=[
  "Academic writing.",
  "What exactly it is, how it's different from other kinds of writing — and how to make your essay fit it.",
 ]),
 dict(mode='concept', active=0, title='What is it?', script=[
  "Let's start by explaining what academic writing is.",
  A("Definition appears", T('Academic writing: writing whose goal is to present ideas in an organized and clear way', size=40, x=410, y=110, w=1140)),
  "In a flat, simple definition: academic writing is writing whose goal is to present ideas in an organized, clear way.",
  A("Why NITE chose it appears", T('It is the writing used at university: research, papers, articles', size=36, x=410, y=260, w=1140)),
  "As we said in the first lesson, it's the writing you'll use at university: research, papers, articles.",
 ]),
 dict(mode='concept', active=1, title='Literary vs academic', script=[
  "So we don't talk too much in the air, let's compare academic writing with a type you probably do know: literary writing.",
  A("Literary writing appears", T('Literary writing: novels, stories — Agnon, Dostoevsky, J. K. Rowling ...', size=36, x=410, y=110, w=1140)),
  "Literary writing is how prose is created: novels, novellas, the texts you studied in literature classes, or books you've read.",
  "I believe and hope names like Agnon, Dostoevsky, even J. K. Rowling sound familiar. That's literary writing.",
  "So what are the differences? Let's start with the goal.",
  A("Literary goal appears", T('Literary goal: the writer shares his inner world with the reader — a story about others or about himself', size=34, x=410, y=240, w=1140)),
  "In literary writing, the writer wants to share his world with the reader. It might be through a story about others, or about himself — but either way, he's sharing his inner world.",
  A("Academic goal appears", T('Academic goal: explain an idea clearly — with arguments and facts. The writer\'s inner world is not the point.', size=34, x=410, y=380, w=1140)),
  "Academic writing has one goal, and it has nothing to do with the writer's inner world. We need to explain an idea clearly.",
  "And the explanation is usually made of arguments and facts.",
 ]),
 dict(mode='concept', active=2, title='No personal tone', script=[
  "Following from the goal: in literary writing, the writer uses a personal tone a lot, and examples from his own experience.",
  A("Literary: personal = expected appears", T('Literary: personal tone and experience — welcome and expected', size=34, x=410, y=110, w=1140)),
  "That's welcome and expected there.",
  A("Academic: objective appears", T('Academic: objective — a personal tone is really not acceptable', size=34, x=410, y=175, w=1140)),
  "Academic writing is more objective. A personal tone is really, really not acceptable.",
  A("Personal sentence appears", B_PERS_BAD),
  "Look at this one. High school, my neighbourhood, how I felt. That's a personal story, not an argument.",
  A("Academic version appears", B_PERS_GOOD),
  "Here's the same idea in an academic style. Nobody's biography — just the idea and why it would happen.",
 ]),
 dict(mode='concept', active=3, title='The neutral narrator', script=[
  "You could say that good academic writing takes the writer out of the text.",
  "When someone reads an academic text, we, the writers, are not expressed there.",
  A("Opinion column appears", T('An opinion column or a blog: you hear the writer\'s voice in the background', size=36, x=410, y=110, w=1140)),
  "Think for a moment about a blog you read, or an opinion column in a newspaper — a columnist who writes every week.",
  "When you read what he writes, you sort of hear his voice in the background, right? You imagine him talking.",
  A("Academic text appears", T('An academic text: you hear no one — just a neutral, anonymous narrator', size=36, x=410, y=240, w=1140)),
  "In academic writing it's not like that. I read the text and I hear nothing. Just some neutral narrator, or myself.",
  A("Reading passages appears", T('Like the reading comprehension passages in the exam', size=36, x=410, y=370, w=1140)),
  "Think of the reading comprehension passages in the exam. That's academic writing.",
  "When you read them, do you hear someone reading to you? No. Some anonymous narrator reads the text to you.",
  A("That means good writing appears", T('If the reader hears no one — the writer did a good job', size=40, x=410, y=470, w=1140)),
  "And if that's the case, it means whoever wrote that text did a good job.",
  A("Like a classic news report appears", T('The model: a classic news report — not an opinion column or a blog. Formal, respectful, clear, as factual as possible.', size=32, x=410, y=580, w=1140)),
  "So the language should be like classic news reporting. Not opinion columns and blogs — the news reports of the old days.",
  "The narrator's voice is neutral. Formal, respectful, clear, and as factual as possible.",
 ]),
 dict(mode='concept', active=4, title='Creativity', script=[
  "Creativity. In literary writing it's welcome and expected. In academic writing it can hurt you.",
  A("Creativity can hurt appears", T('Literary: creativity is welcome.   Academic: creativity can hurt your score', size=36, x=410, y=110, w=1140)),
  "That doesn't mean creativity is forbidden. But it has the potential to hurt if we don't know how to use it properly.",
  A("Stay inside the topic appears", T('Stay inside the borders of the topic: no invented stories, no back stories, nothing "too creative"', size=34, x=410, y=230, w=1140)),
  "The writing must stay within the borders of the topic you're dealing with. You don't invent things, you don't give back stories.",
  "The writing should be very focused on the topic.",
  A("No invented expressions appears", T('No new expressions of your own — they do not impress the rater; they cost points', size=34, x=410, y=360, w=1140)),
  "And we don't invent new things to get a great score. If you invent a new expression — that can be fine in literary writing.",
  "In a novel or a comedy script, someone invents a phrase and suddenly it enters the language.",
  "In academic writing it's not fine at all. An exotic expression you invent probably won't enter anyone's vocabulary — it'll just hurt your score.",
  A("'in my prevalent opinion' appears", T('A real student invention: "in my prevalent opinion" ...', size=34, x=410, y=500, w=1140)),
  "Though I can tell you that as essay raters we sometimes come across amazing creativity — expressions we actually take with us.",
  "Like one student who wrote: in my prevalent opinion. We still smile about it. But it didn't help his score.",
 ]),
 dict(mode='concept', active=5, title='Head, not heart', script=[
  "Appealing to emotion. In literary writing it's legitimate — welcome and expected.",
  "Some would say a good author is one who plays on the reader's heartstrings and stirs up feelings.",
  A("Head, not heart appears", T('Academic writing appeals to the head, not to the heart', size=40, x=410, y=110, w=1140)),
  "In academic writing that's not acceptable at all. The writer has to explain things rationally — by appealing to the mind, not the heart.",
  "Emotional appeals are very common in speeches, by the way. Those fiery speeches that stir up the crowd.",
  A("Emotional sentence appears", B_EMO_BAD),
  "Heartbreaking, innocent, watched like criminals. That's trying to make the reader feel something.",
  A("Rational version appears", B_EMO_GOOD),
  "The same concern — explained. Stay focused and to the point.",
 ]),
 dict(mode='concept', active=6, title='Who may speak', script=[
  "Taking the writer's personal circumstances out of the text also shows in the grammatical person you use.",
  "In literary writing there's no limit: I, you, he, she, we, they.",
  A("I: only for your position appears", T('"I" — only to state your position:  I believe that ... · In my opinion, ... · In my view, ...', size=34, x=410, y=100, w=1140)),
  "In academic writing, the writer may use 'I' — but only in phrases like 'in my opinion' or 'I believe that'. Beyond that, no 'I'.",
  A("No 'we', no 'you' appears", T('No "we" (We must ...) · No "you" (You can see that ...) — do not address the reader', size=34, x=410, y=190, w=1140)),
  "'We' is not acceptable: 'we must do this and that'. And 'you' — no. We don't address the reader: 'so you should...', 'you can see that...'.",
  A("They: fine appears", T('Third person is fine: people, the public, society, they', size=34, x=410, y=280, w=1140)),
  "Third person is fine. I can talk about 'they': people, the population, society, and so on.",
  A("Wrong version appears", B_WHO_BAD),
  "Here: we, and you. The writer talks to the reader, and speaks for everyone.",
  A("Right version appears", B_WHO_GOOD),
 ]),
 dict(mode='concept', active=7, title='No flowery language', script=[
  "Flowery or poetic language. Decorated language, like in poetry.",
  A("No decoration appears", T('Literary: decorated language is fine.   Academic: precise, not decorated', size=36, x=410, y=110, w=1140)),
  "It's legitimate in literary writing, of course, but not acceptable in academic writing. The language must be precise, not decorated.",
  A("Flowery sentence appears", B_FLOW_BAD),
  "Silent guardian, sleeping city, shining beacon. Beautiful, maybe. But what does it actually claim?",
  A("Plain version appears", B_FLOW_GOOD),
  "This is what it was trying to say. Plain, precise — and it carries a real reason.",
 ]),
 dict(mode='concept', active=8, title='Rhetorical devices', script=[
  "Rhetorical devices and proverbs.",
  "First, rhetorical devices: tools a writer uses to persuade through emotion.",
  A("Rhetorical question appears", T('Rhetorical question: a question whose answer is obvious — it is not really asked', size=34, x=410, y=100, w=1140)),
  "One of the best known is the rhetorical question — a question whose answer is obvious, so there's no real need to ask it.",
  "Picture a speaker on a stage in the city square, talking about workers' conditions. What would we expect from him? Dramatic questions.",
  A("The speaker's question appears", B_RQ_BAD),
  "The answer is obvious — it's not acceptable. His goal is to fire up the listeners. That's an appeal to emotion, and it's not acceptable in academic writing.",
  A("Statement version appears", B_RQ_GOOD),
  "In the essay, turn the question into a statement — and explain it.",
  A("Proverbs appear", T('Proverbs (short sayings of life wisdom): avoid them in the essay', size=32, x=410, y=Y_PROV, w=1140)),
  "Proverbs are short sayings of life wisdom, like: a bird in the hand is worth two in the bush.",
  A("Proverb sentence appears", B_PROV_BAD),
  "In literary writing that's fine, no limit. In academic writing it's less acceptable.",
  A("Explained version appears", B_PROV_GOOD),
  "Say what the proverb means — in your own plain words.",
 ]),
 dict(mode='concept', active=9, title='Everyday English', script=[
  "In English there's one more thing to watch: spoken, everyday English. We speak one way and write the essay another way.",
  A("Contractions appear", T("No contractions:  don't → do not · it's → it is · can't → cannot · won't → will not", size=32, x=410, y=100, w=1140)),
  "No contractions. Write 'do not', 'it is', 'cannot'.",
  A("Slang appears", T('No slang or chatty words:  kids → children · a lot of → many / much · stuff, things → the exact noun · OK → acceptable · totally, really, super → leave out', size=32, x=410, y=190, w=1140)),
  "No slang and no chatty words. Children, not kids. Many, not a lot of. Say what the 'stuff' actually is.",
  A("Phrasal verbs appear", T('Prefer the formal verb:  find out → discover · cut down on → reduce · get better → improve · put up with → tolerate · get → become / receive', size=32, x=410, y=330, w=1140)),
  "And where there's a formal verb, prefer it. Reduce, not cut down on. Improve, not get better.",
  A("Filler appears", T('No spoken fillers or openers:  Well, ... · Basically, ... · Let\'s be honest, ... · like · you know', size=32, x=410, y=470, w=1140)),
  "No spoken fillers: well, basically, let's be honest, like, you know.",
 ]),
 dict(mode='concept', active=10, title='Absolute claims', script=[
  "How strongly you state things is another difference.",
  A("Literary: as absolute as you like appears", T('Literary: be as absolute as you like', size=36, x=410, y=110, w=1140)),
  "In literary writing you can be as absolute as you want. No problem.",
  A("Academic: qualified appears", T('Academic: qualified — avoid absolute terms (always, never, everyone, there is no doubt ...)', size=34, x=410, y=190, w=1140)),
  "In academic writing the writing has to be qualified. We avoid absolute terms and extreme positions.",
  A("Even with a position appears", T('You still take a position — but in qualified language, knowing there are several sides', size=34, x=410, y=320, w=1140)),
  "Even when we choose a position, it's done in qualified language — recognizing that the issue has several sides.",
  "The other side probably has some advantages too, or my side has some disadvantages.",
  A("No one is completely right appears", T('No one is completely right', size=44, x=410, y=450, w=1140)),
  "None of us is completely right, so we need to be qualified. We'll see exactly how in the next lesson.",
 ]),
 dict(mode='concept', active=11, title='Before and after', script=[
  "Let's see everything together. Here's a paragraph written in a spoken, personal, emotional style.",
  A("Informal paragraph appears", B_BA_BAD),
  "Let's be honest, I know I don't, a total nightmare, everyone knows, you'd have to be crazy. A rhetorical question, contractions, 'you', emotion, an absolute claim.",
  "Every one of those is something we just learned to avoid.",
  A("Academic paragraph appears", B_BA_GOOD),
  "And here's the academic version. The same position — against the cameras. But calm, qualified, and explained.",
  D("teacher underlines 'may', 'could', 'if'"),
  "Notice: the position didn't get weaker. It got more convincing.",
 ]),
 dict(mode='concept', active=12, title='Five rules', script=[
  "So let's sum up briefly. To write in a way that fits academic writing:",
  A("Rule 1 appears", T('1 · Appeal to the mind, not to the emotions', size=34, x=410, y=90, w=1140)),
  A("Rule 2 appears", T('2 · Write directly and clearly: no decoration, no proverbs, no rhetorical devices', size=34, x=410, y=150, w=1140)),
  A("Rule 3 appears", T('3 · Do not be "creative": stay inside the topic, do not invent new expressions', size=34, x=410, y=250, w=1140)),
  A("Rule 4 appears", T('4 · No personal tone: no personal stories or life circumstances', size=34, x=410, y=350, w=1140)),
  A("Rule 5 appears", T('5 · Do not be absolute: qualified writing — we will come back to it again and again', size=34, x=410, y=410, w=1140)),
  "Qualified writing is really, really important, and it keeps coming back. We'll return to it many times in the next lessons.",
  A("The tone appears", T('The tone: moderate, respectful, calm — two people debating quietly, each letting the other speak', size=34, x=410, y=530, w=1140)),
  "The tone of the writing should be moderate, respectful, calm.",
  "When two people argue, each one shouts at the other. Don't picture that. Picture two people debating — who speak quietly to each other.",
  "Each respects the other side, lets him speak, listens to him.",
  A("No monopoly on the truth appears", T('There is logic on the other side too — no one has a monopoly on the truth', size=34, x=410, y=660, w=1140)),
  "We need to recognize that there's logic on the other side too. No one has a monopoly on justice, on the truth.",
  "That's the essence of academic writing. That's how we write in a way that fits it.",
 ]),
], T50),

# ============================================================================ lesson 3 · seg07 (second part) = seg08
lesson('vr50-b-hedging', 'Qualified Writing', SB_HEDGE, [
 dict(mode='title', title='Qualified Writing', script=[
  "Now I want to expand a little on qualified writing — or, as it's called in English, hedging.",
  "How to state your claims at the right strength.",
 ]),
 dict(mode='concept', active=0, title='No word lists', script=[
  "In general, I don't recommend memorizing endless lists of words and expressions for the essay.",
  A("Word lists backfire appears", T('Endless memorized word lists → forced words → semantic errors and artificial writing', size=36, x=410, y=110, w=1140)),
  "The result is often students who force in words and expressions they learned. Because what — they learned them, and they won't use them?",
  "That often causes semantic errors, or at least an essay whose writing looks forced and artificial.",
  A("Instead appears", T('Instead: qualify your claims with ordinary words you already know', size=40, x=410, y=260, w=1140)),
  "Instead, I'll show you how to phrase things in a qualified way, at the level that fits academic writing — without any new or unusual vocabulary.",
  "Let's look at a few examples.",
 ]),
 dict(mode='concept', active=1, title='A guess as a fact', script=[
  A("Sentence appears", B_EB_BAD),
  "Here's a sentence presented as a fact.",
  "The writer states, with no qualification at all, that if there's a ban on electric bicycles, the number of road accidents will necessarily go down.",
  A("The problem appears", T('The problem: we cannot know for certain that this is what will happen', size=38, x=410, y=300, w=1140)),
  "And there's a problem. We can't state that this is certainly what will happen.",
  A("For example appears", T('Riders may switch to another vehicle with a higher risk — motorcycles → accidents may not go down', size=34, x=410, y=420, w=1140)),
  "For example, people who stop using electric bicycles might switch to some other vehicle with a higher level of risk. They'll move to motorcycles.",
  "And then the number of road accidents won't necessarily go down.",
  A("A guess presented as a fact appears", T('The writer presents a guess (a hypothesis) as if it were a fact — this does not fit academic writing', size=34, x=410, y=550, w=1140)),
  "In short: the writer presents a hypothesis without qualification, as if it were a fact. That doesn't fit academic writing.",
  "Try to think for a moment: how can we change the sentence to fix this? Take a moment.",
 ]),
 dict(mode='concept', active=2, title='Add one word', script=[
  "Look — all we need is a small qualification.",
  A("Fixed sentence appears", B_EB_GOOD),
  "Instead of 'will reduce', we can write 'may reduce'. Right?",
  D("teacher circles 'may reduce'"),
  A("What changed appears", T('"may" = it does not necessarily reduce accidents, but it might', size=38, x=410, y=300, w=1140)),
  "That doesn't say it will necessarily reduce road accidents — but maybe it will.",
  A("Absolute → qualified appears", T('One word: an absolute sentence became a qualified one', size=40, x=410, y=400, w=1140)),
  "And there you go: we took an absolute sentence and qualified it.",
 ]),
 dict(mode='concept', active=3, title='Two absolutes', script=[
  "Let's see another example.",
  A("Sentence appears", B_CAM_BAD),
  "Here we have two main problems. Take a moment — try both to find them and to see how you'd solve them.",
  "So let's see.",
  A("Problem 1 appears", T('Problem 1: "There is no doubt that" — an absolute expression', size=38, x=410, y=300, w=1140)),
  "The first is 'there is no doubt'. That's an absolute expression. It doesn't fit academic writing.",
  A("Just drop it appears", T('Better to simply drop it', size=38, x=410, y=390, w=1140)),
  "It's better to simply give it up. That's it.",
  A("Without it appears", dict(B_CAM_MID, y=470)),
  "Most of the public will oppose the cameras. But here we come to the second problem.",
 ]),
 dict(mode='concept', active=4, title='Most or many?', script=[
  A("Sentence appears", B_CAM_MID),
  "The second problem: 'most of the public'.",
  D("teacher circles 'Most'"),
  A("Most = more than half appears", T('"Most" = more than 50% of the group', size=40, x=410, y=300, w=1140)),
  "When someone says 'most', he's actually saying that more than fifty percent of a certain group has some characteristic.",
  "Here he's committing to the claim that more than half the public will oppose face-recognition cameras. How does he know that?",
  A("Did you run a survey? appears", T('Did the writer stop, run a national survey, and come back — all within 35 minutes?', size=34, x=410, y=380, w=1140)),
  "He probably didn't stop the essay, jump outside, survey everyone in the country, get the results, and come back to finish writing within thirty-five minutes.",
  "So he's stating something as a fact — but it isn't a fact. It might be true. But we don't know it.",
  A("The trick appears", T('The trick:  most → many', size=44, x=410, y=500, w=1140)),
  "And here I'll teach you a little trick that works really nicely. Instead of 'most', write 'many'.",
  A("Fixed sentence appears", B_CAM_GOOD),
  "How many is 'many'? Two or more. More than one.",
  "The content of the sentence didn't change. Whoever reads it thinks: fair enough, there's a case here, many really will oppose it.",
  "But no one can contradict me. No one can say that this sentence is wrong.",
  A("Rule of thumb appears", T('Not sure it is more than half?  Write "many", not "most".  Almost the same effect — no risk.', size=32, x=410, y=760, w=1140)),
  "So as a rule of thumb: if you don't know for certain that most of a group does or did something, don't use 'most'. Use 'many'.",
  "You get almost the same effect — without taking a risk.",
 ]),
 dict(mode='concept', active=5, title='Every driver?', script=[
  "Let's see one more example.",
  A("Sentence appears", B_RD_BAD),
  "And I ask: really? If there's no enforcement, every driver will do whatever he wants, and the roads will become a war zone?",
  A("Some drivers obey anyway appears", T('Some drivers will obey the law anyway — enforcement or not, they want to stay alive', size=36, x=410, y=300, w=1140)),
  "Can't there be some drivers who will keep obeying the law? And why? Because for them it has nothing to do with enforcement.",
  "They want to protect their lives, so they drive according to the law.",
  A("Not qualified appears", T('Again: a sentence that is not qualified — it does not fit academic writing', size=36, x=410, y=430, w=1140)),
  "So again we see a sentence that isn't qualified, and that doesn't fit academic writing.",
  "Like before — take a moment and try to think how to fix it.",
 ]),
 dict(mode='concept', active=6, title='Hedge the start', script=[
  "Let's see how we can improve this sentence a little, step by step.",
  A("Step 1 appears", B_RD_1),
  "We start by adding 'It is likely that' at the beginning of the sentence. That already qualifies the start.",
  "It's not 'without enforcement every driver will...'. It's 'It is likely that, without enforcement...'.",
  A("Step 2 appears", dict(B_RD_2, y=below(B_RD_1, 40))),
  "Next — 'every driver'. Here's the second absolute expression. Remember the trick from before? Many.",
  "Instead of 'every driver': 'many drivers'.",
 ]),
 dict(mode='concept', active=7, title='Plain, calm words', script=[
  "Now we have 'do whatever they want'. That's a bit of an everyday expression. It fits academic writing less.",
  A("Step 3 appears", B_RD_3),
  "So we replace it: will not obey the law.",
  A("Not fancy words appears", T('Not searching for fancy words — just clear and qualified', size=36, x=410, y=320, w=1140)),
  "And look — I'm not searching for especially high words to show off some unusual richness of language.",
  "No. I'm simply trying to write clearly. Qualified — but clear.",
  A("War zone appears", T('"the roads will turn into a war zone" — this is already real drama', size=36, x=410, y=430, w=1140)),
  "Let's continue. 'The roads will turn into a war zone.' That's already real drama.",
  "So of course that expression doesn't fit academic writing either. The road isn't really going to turn into a war zone.",
  A("Calm version appears", T('→ "driving will become dangerous"', size=40, x=410, y=540, w=1140)),
  "Instead, we can write: driving will become dangerous.",
 ]),
 dict(mode='concept', active=8, title='The full fix', script=[
  "Let's see the whole thing, before and after.",
  A("Before appears", B_RD_BAD2),
  A("After appears", B_RD_GOOD),
  "Four changes: a qualified opening, 'many' instead of 'every', plain words instead of an everyday expression, and a calm claim instead of drama.",
  D("teacher numbers the four changes 1 to 4"),
  "Same idea. Same position. But now nobody can say it's wrong.",
 ]),
 dict(mode='concept', active=9, title='Hedging words', script=[
  "In English, a handful of ordinary words do almost all the qualifying. You already know them.",
  A("Verbs appear", T('may · might · can · could · tends to · is likely to', size=40, x=410, y=100, w=1140)),
  "Verbs that soften: may, might, can, could, tends to, is likely to.",
  A("How often appears", T('often · in many cases · frequently · in some cases', size=40, x=410, y=190, w=1140)),
  "How often: often, in many cases, in some cases.",
  A("How many appears", T('many · some · a large number of · a significant part of', size=40, x=410, y=280, w=1140)),
  "How many: many, some, a large number of.",
  A("Openers appear", T('It is likely that ... · It is possible that ... · There is reason to believe that ...', size=34, x=410, y=370, w=1140)),
  "And openers that qualify the whole sentence.",
  A("Swap table appears", T('always → often · never → rarely · everyone → many people · no one → few people · will → may / is likely to · certainly, undoubtedly → probably · proves → suggests', size=32, x=410, y=470, w=1140)),
  "And here are the swaps for the absolute words. Always becomes often. Everyone becomes many people. Proves becomes suggests.",
  A("See the card appears", T('All of these are in the card "Academic register & hedging" after this lesson', size=30, x=410, y=640, w=1140)),
  "You'll find all of these in the summary card after this lesson.",
 ]),
 dict(mode='concept', active=10, title='Hedge, but take a side', script=[
  "One warning. Qualified doesn't mean foggy.",
  A("Over-hedged appears", B_OVER_BAD),
  "Might, perhaps, possibly, could, in some ways, to some extent. Six hedges on one small claim. Now the reader doesn't know what you're saying.",
  A("One hedge is enough appears", B_OVER_GOOD),
  "One qualifying word per claim is usually enough.",
  A("Your position stays clear appears", T('Qualify the claims, not the position: "I believe that the city should ..." stays clear and firm', size=34, x=410, y=550, w=1140)),
  "And your position itself stays clear. You qualify how sure you are about a consequence — you don't hide which side you're on.",
  A("A hedge does not fix a weak reason appears", T('And "may" does not repair a weak explanation — the reason still has to make sense', size=34, x=410, y=680, w=1140)),
  "Also: 'may' doesn't rescue a weak explanation. If the reason doesn't make sense, a hedge won't save it. The explanation still has to hold.",
  "And no need to memorize lists. Just notice your wording as you write: is this certain? Is it everyone? Is it drama?",
 ]),
], T50),

# ============================================================================ lesson 4 · seg09
lesson('vr50-b-precision', 'Semantic Precision', SB_PREC, [
 dict(mode='title', title='Semantic Precision', script=[
  "Semantic precision.",
  "One of the places where students lose the most points in language — and the easiest one to protect yourself from.",
 ]),
 dict(mode='concept', active=0, title='What it means', script=[
  "Let's start with some definitions.",
  A("Semantics appears", T('Semantics: the branch of linguistics that deals with words and their meanings', size=36, x=410, y=100, w=1140)),
  "Semantics is the branch of linguistics that deals with the link between words and their meanings.",
  A("Semantic precision appears", T('Semantic precision: using words in a way that matches their meaning exactly', size=36, x=410, y=210, w=1140)),
  "When NITE talks about semantic precision, it means using words in a way that matches their meaning precisely.",
  A("Two kinds of imprecision appear", T('Imprecision comes in two kinds:', size=38, x=410, y=330, w=1140)),
  A("Kind 1 appears", T('1 · a correct word or expression — in the wrong place (it means something other than what you wanted)', size=34, x=450, y=400, w=1100)),
  "One: using a word or expression correctly — but in a place where it doesn't fit. It means something different from what we wanted to say.",
  A("Kind 2 appears", T('2 · a distorted word or expression — written in a wrong, broken form', size=34, x=450, y=520, w=1100)),
  "Two: distorting the expression or the word. We take a word or an expression and write it in a different, incorrect form.",
  "Those are the two problems that make up imprecision.",
 ]),
 dict(mode='concept', active=1, title='Does it cost points?', script=[
  A("May lower the score appears", T('An imprecise word, or a word in the wrong context, may lower your score', size=38, x=410, y=110, w=1140)),
  "Imprecise use of a word or expression, or use out of context, may hurt your score.",
  "Why do I say 'may' and not 'lowers the score'? Because it really depends.",
  A("One or two: probably fine appears", T('One or two slips in a first draft: probably no points lost', size=36, x=410, y=240, w=1140)),
  "Again, NITE understands that we write the essay in thirty-five minutes, and it's a draft.",
  "If there's a mistake or two here and there — even a language mistake or an imprecise word — we probably won't lose points for it.",
  A("Several: points lost appears", T('Several times: points are lost', size=36, x=410, y=340, w=1140)),
  "But if it happens several times, they'll take points off.",
  A("One of the most common appears", T('One of the most common reasons students lose language points', size=38, x=410, y=450, w=1140)),
  "And by the way — semantic imprecision is one of the places where students lose the most points. It's one of the most common mistakes.",
 ]),
 dict(mode='concept', active=2, title='Why students slip', script=[
  "And the reason is that students try to impress the rater. Right?",
  "In language, I want to impress the rater. I want him to think my language is richer than it really is.",
  "And look — there's a difference here between content and language.",
  A("Content: reaching up is safe appears", T('Content: reach a little higher — if it fails, your argument is still there', size=36, x=410, y=110, w=1140)),
  "In content, I have my level. I have critical thinking, I build arguments in a certain way.",
  "And I try to pull a bit higher, because I always want a little more than I can do. So I add another piece of support, something like that.",
  "If I succeed — great. If I don't — nothing happened. My support, my sentences, my arguments, the link to the task: it's all still there.",
  A("Language: reaching up is risky appears", T('Language: reach higher with a word you are not sure of — if it fails, you drop below where you were', size=36, x=410, y=260, w=1140)),
  "In language, it's not like that. I'm at a certain level, and I try to impress the rater. I try to pull up.",
  "As long as I succeed, fine — how nice, I raised my language score a little.",
  "But if I don't succeed, I don't stay where I was. My score is hurt. I lose points.",
  D("teacher draws an arrow up for 'success' and a longer arrow down for 'failure'"),
 ]),
 dict(mode='concept', active=3, title='The wheelie', script=[
  "Think about it like this. Forget the rater for a moment — let's go to real life.",
  "Sometimes we want to impress our friends. How do I try to impress them? I do some trick I've mastered and do very well. Right?",
  A("The wheelie appears", T('Impressing your friends:  a magic trick · a wheelie on a bike', size=40, x=410, y=110, w=1140)),
  "I don't know — come see me lift the front wheel. Hop, I do a wheelie. How nice.",
  A("If you can do it appears", T('Can really do it → you impressed them', size=38, x=450, y=220, w=1100)),
  "As long as I really know how to do the trick, or really know how to do a wheelie — great, I impressed them.",
  A("If you can't appears", T('Can\'t really do it → the card falls out of your sleeve, you crash — worse than before', size=38, x=450, y=300, w=1100)),
  "But if I don't know how — I start the trick and suddenly they see me slipping the card in. Or I lift the wheel and crash.",
  "My situation is worse than before. Not only didn't I impress them — now they're laughing at me.",
  A("Same in the essay appears", T('Same in the essay: a word used wrongly = semantic imprecision = lost points', size=38, x=410, y=450, w=1140)),
  "It's the same in the exam, in the essay. When you use a word or expression incorrectly, there's semantic imprecision, and you lose points. You make your situation worse.",
  A("The request appears", T('Not 100% sure of a word?  Let it go.', size=48, x=410, y=590, w=1140)),
  "So I really, really stress this and ask you: don't use words you're not a hundred percent sure of.",
  "The ones where you think 'hop, now I'll use this and the rater will fall off his chair'. If you're not perfectly sure — drop it. Let it go.",
  "Now let's look at sentences from students' essays — students who tried to write 'high' — and see how to fix them, without showing off and without unnecessary risks.",
 ]),
 dict(mode='concept', active=4, title='A broken idiom', script=[
  "First example.",
  A("Sentence appears", T('Example 1', size=34, x=410, y=110, w=1140)),
  A("Broken idiom appears", B_IDIOM_BAD),
  "'Free reign' — that's not the expression. The expression is 'free rein': like the reins of a horse, let loose.",
  D("teacher crosses out 'reign' and writes 'rein'"),
  "So even though the rater reading it probably understands what the student meant, points will probably come off here. It isn't the right expression.",
  "So here we have a distorted expression.",
  A("Simple version appears", B_IDIOM_GOOD),
  "And honestly — the simplest fix is not to need the idiom at all. Say it plainly.",
 ]),
 dict(mode='concept', active=5, title='The wrong word', script=[
  A("Sentence appears", B_ELITE_BAD),
  "The word 'elitists' doesn't fit here.",
  "An elitist is a person who believes a small, superior group should lead. The student meant the powerful groups themselves.",
  A("Fixed appears", B_ELITE_GOOD),
  "Not focus only on the elites — or only on the stronger groups.",
  A("What went wrong appears", T('The student meant "elites" and wrote "elitists": a real word, but not the right one', size=34, x=410, y=500, w=1140)),
  "Here too there's an incorrect word. They meant to write 'elites' and wrote 'elitists'. So it's an incorrect use.",
 ]),
 dict(mode='concept', active=6, title='Invented phrases', script=[
  A("Sentence 1 appears", B_ADM_BAD),
  "'Administrative-wise'? That's someone inventing an expression. I don't really understand what he means — and the rater won't either.",
  "Since there's no such expression — and we said we don't invent expressions — points come off here.",
  A("Fix 1 appears", B_ADM_GOOD),
  "Say what you actually mean.",
  A("Sentence 2 appears", B_VETO_BAD),
  "'Moral veto' — again, an invented expression. There's no such thing as a moral veto.",
  "The state has no right, simply, to harm the right of parents... But now 'right' appears twice in the same sentence.",
  A("Fix 2 appears", B_VETO_GOOD),
  "So we can say the state has no legitimate grounds for violating the parents' right. Again: here there was an invented expression — one that doesn't exist.",
  A("Sentence 3 appears", B_SPORT_BAD),
  "Another invented expression. What is 'sportive time'? What did he mean? Time meant for sport.",
  A("Fix 3 appears", B_SPORT_GOOD),
  "So write: time set aside for sport. Here too — an incorrect expression. There's no such expression.",
 ]),
 dict(mode='concept', active=7, title='Idiom, wrong place', script=[
  A("Sentence appears", B_FOOT_BAD),
  "Now here we have the expression 'shoot themselves in the foot'. It's a real expression, and this time it's written correctly.",
  "But it's used in a place that doesn't fit.",
  A("What it means appears", T('"shoot yourself in the foot" = to harm yourself by your own action, by mistake', size=36, x=410, y=350, w=1140)),
  "What does it mean to shoot yourself in the foot? You do something — and by mistake you end up hurting yourself.",
  A("What the sentence is about appears", T('Here: people who harm others on purpose — the meaning does not fit', size=36, x=410, y=450, w=1140)),
  "Here we're talking about people who publish private information about citizens without permission. They're not hurting themselves by mistake. They're harming others — on purpose, from the start.",
  "So even though the expression is correct, it's not in the right place. Its meaning doesn't fit the sentence.",
  A("Plain version appears", B_FOOT_GOOD),
  "And in this case, look: instead of 'will shoot themselves in the foot and publish', simply: will publish.",
  "How simple. Instead of taking a risk — instead of trying to lift the wheel when I don't really know how to do a wheelie.",
 ]),
 dict(mode='concept', active=8, title='Look-alike words', script=[
  A("Sentence appears", B_UNI_BAD),
  "Here too the word 'uniformity' is an incorrect use. What he wanted to say is 'unity'.",
  A("Fixed appears", B_UNI_GOOD),
  "Notice: we're not talking about a spelling mistake. He really tried to write 'uniformity', because he thought that was the meaning that fits.",
  "But uniformity means everyone is the same. Unity means people are together. The word that fits here is 'unity'. That's also semantic imprecision.",
  A("More look-alikes appear", T('Look-alike pairs to check:  affect / effect · economic / economical · sensible / sensitive · principal / principle · historic / historical · rise / raise · lose / loose', size=32, x=410, y=450, w=1140)),
  "In English there are many pairs like this — words that look or sound alike but mean different things. Here are some that often appear in essays.",
  "If you're not sure which one is which — use a different, simpler word you are sure of.",
 ]),
 dict(mode='concept', active=9, title='Words change the claim', script=[
  "Sometimes one word changes the whole claim. That's precision in content, not just in language.",
  A("Suspect vs criminal appears", T('A suspect is not a criminal: guilt is decided in court, not by a camera', size=36, x=410, y=110, w=1140)),
  "Our cameras example. A camera can identify a suspect. Whether that person is a criminal is decided in court.",
  A("Wrong status appears", B_SUS_BAD),
  A("Right status appears", B_SUS_GOOD),
  "So 'suspects' is the precise word — and it matters for the argument, especially if you're worried about innocent people.",
  A("More pairs appear", T('Other pairs that change the claim:  reduce / eliminate · many / most · a right / a privilege · allow / require · some / all', size=32, x=410, y=600, w=1140)),
  "Reduce crime is not eliminate crime. Allow is not require. A right is not a privilege. Many is not most — remember?",
  "Before you write the key word of a sentence, ask: is this exactly what I'm claiming?",
 ]),
 dict(mode='concept', active=10, title='One term throughout', script=[
  "Students are often told to vary their words so they don't repeat themselves. With the key term of the essay — that's a trap.",
  A("Same thing, same term appears", T('The same thing gets the same name, all through the essay', size=40, x=410, y=110, w=1140)),
  A("Drifting terms appear", B_TERM_BAD),
  "Face-recognition cameras, then security cameras, then surveillance. Ordinary security cameras don't recognize faces. The rater wonders: did you change the topic?",
  A("Consistent terms appear", B_TERM_GOOD),
  "Keep the key term. Vary everything else around it. And 'these cameras' is fine — it clearly points back to the same thing.",
  A("Repetition inside one sentence appears", T('Repeated word inside one sentence (like "right ... right") can be varied — the key term of the essay stays', size=32, x=410, y=690, w=1140)),
  "Remember the 'moral veto' sentence? There we avoided the same word twice in one short sentence. That's style. The key term of the essay stays the same.",
 ]),
 dict(mode='concept', active=11, title='The main lesson', script=[
  "So let's sum up the most important lesson here.",
  A("The rule appears", T('Do not use a word or expression unless you are 100% sure of its meaning and its correct form', size=42, x=410, y=110, w=1140)),
  "Don't use words and expressions if you're not a hundred percent sure of their meaning, or of the correct way to write them. OK?",
  A("Impress vs hurt appears", T('You try to impress — and in practice you hurt your score', size=38, x=410, y=300, w=1140)),
  "It's this thing where you try to impress, but in practice you hurt your score.",
  A("From tens of thousands of essays appears", T('From checking tens of thousands of essays: one of the main reasons students lose language points', size=34, x=410, y=410, w=1140)),
  "And again, from checking tens of thousands of essays: this is one of the most common mistakes, and one of the main reasons students lose points in language.",
  A("Next appears", T('Next: grammar', size=44, x=410, y=560, w=1140)),
  "That's it for semantic precision. We're moving on to the next lesson — grammar. As usual, I'll be waiting for you there.",
 ]),
], T50),
]

MEMORY = [
 dict(id='mem-wr-b-register', after='vr50-b-hedging', title='Academic register & hedging',
  intro='Write like a calm, neutral narrator: formal, impersonal, qualified. Simple words are perfect.',
  tables=[
   dict(title='Informal → academic', head=['Avoid', 'Write instead'], rows=[
    ["don't · it's · can't · won't", 'do not · it is · cannot · will not'],
    ['kids · a lot of · stuff', 'children · many / much · the exact noun'],
    ['get better · cut down on · find out', 'improve · reduce · discover'],
    ['You can see that ... · We must ...', 'This shows that ... · The city should ...'],
    ['In my opinion, I think ... · according to me', 'In my opinion, ... · I believe that ... · in my view'],
    ['Is it fair that ...? (rhetorical question)', 'A statement + the reason'],
    ['heartbreaking · a nightmare · a war zone', 'harmful · a serious risk · dangerous'],
    ['a proverb or a flowery image', 'what it means, in plain words'],
    ['When I was ... (personal story)', 'a general, explained example'],
   ]),
   dict(title='Hedging words', head=['Instead of (absolute)', 'Write (qualified)'], rows=[
    ['will', 'may · might · can · could · is likely to'],
    ['always', 'often · in many cases · tends to'],
    ['never', 'rarely · in few cases'],
    ['everyone · all · every', 'many people · many'],
    ['most (unless you know it)', 'many'],
    ['no one', 'few people'],
    ['There is no doubt that · certainly', 'It is likely that · probably'],
    ['proves', 'suggests · indicates'],
   ]),
  ],
  tips=['Qualify the claims, not your position: the side you support stays clear.',
        'One hedge per claim is enough: "might perhaps possibly" is foggy, not academic.',
        '"May" does not repair a weak explanation; the reason still has to make sense.',
        'Formal does not mean fancy: use only words you are 100% sure of.']),
 dict(id='mem-wr-b-precision', after='vr50-b-precision', title='Precise word choice',
  intro='Not 100% sure of a word or an expression? Let it go and say it plainly.',
  tables=[
   dict(title='The four precision errors', head=['Error', 'Example → fix'], rows=[
    ['Broken idiom', 'free reign → free rein (or: could act without fear of punishment)'],
    ['Wrong word', 'the elitists → the elites · uniformity → unity'],
    ['Invented phrase', 'sportive time → time set aside for sport · moral veto → legitimate grounds'],
    ['Idiom, wrong place', 'shoot themselves in the foot and publish → publish'],
   ]),
  ],
  tips=['The same thing gets the same name all through the essay (face-recognition cameras ≠ security cameras).',
        'Check the words that change the claim: suspect / criminal · reduce / eliminate · many / most · allow / require.',
        'Look-alikes: affect / effect · economic / economical · sensible / sensitive · principal / principle.']),
]
