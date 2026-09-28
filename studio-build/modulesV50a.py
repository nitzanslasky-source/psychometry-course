# Verbal Reasoning · Topic 50 · Writing Task · Part A (segments seg01-seg05).
# Introduction to the writing task, the exam page and answer sheet, the two rubrics, how the score works,
# what is expected (the teacher's face-recognition-camera model essay), and the opening (baseline) essay.
# Official facts from nite_verbal_guide.txt override the Hebrew course (35 minutes, 25-50 lines, etc.).
from dsl import *
from writing_assets import TASK_PAGE, ANSWER_SHEET, task_page, prompt_box, EXAMPLE_PROMPT, EXAMPLE_QUESTION

T50 = 50

# right-hand column beside a portrait figure
def RC(label, text, y, size=30):
    return A(label, T(text, size=size, x=1070, y=y, w=470))

def L(label, text, y, size=36):
    return A(label, T(text, size=size, x=410, y=y, w=1140))

PAGE = dict(TASK_PAGE, x=380, y=40, w=660, h=684)
SHEET = dict(ANSWER_SHEET, x=400, y=20, w=640, h=832)

CAM_PROMPT = [
    'In recent years, security officials have been promoting bills to set up a national network of',
    'face-recognition cameras in public spaces. Since current technology can identify people and',
    'objects in real time with a high degree of certainty, any person, vehicle or other object caught',
    'on camera could be identified, provided that its image already exists in a database. This',
    'information would help fight criminal and security offences that harm the public: suspicious',
    'activity could be detected before an offence is committed, illegal activity could be stopped',
    'while it is taking place, and offenders could be caught afterwards. Supporters of this step argue',
    'that such a system would reduce, and even eliminate, criminal and security incidents in the',
    'monitored areas. Opponents believe that it would seriously violate privacy, and that it is',
    'unthinkable for security officials to be able to follow our every step.',
]
CAM_QUESTION = ('In your opinion, should security officials be allowed to place face-recognition cameras '
                'in public spaces? Give reasons.')
# one shared version of every task (writing_tasks.py, shaped like the real English tasks)
from writing_tasks import T as _T, split_task_slides
CAM_PROMPT, CAM_QUESTION = _T['camera']['paras'], _T['camera']['q']

P_OPEN = ("Recently, security officials have been working to set up a national network of face-recognition "
          "cameras in public spaces. These cameras, which can identify people and objects in real time with a "
          "high level of accuracy, are intended to help the security forces catch offenders during or after "
          "illegal activity, and thus to reduce, and perhaps even eliminate, crime in the country. However, some "
          "people have come out strongly against this move because of the harm to privacy that it involves. "
          "In my opinion, these cameras should be installed, since their benefits to public safety are likely to "
          "outweigh the harm to privacy.")

P_ARG1 = ("In my opinion, placing face-recognition cameras in public spaces would create deterrence, which "
          "would lead to fewer offences in the monitored areas. It is reasonable to assume that the cameras would "
          "be accompanied by a broad public campaign and by signs in the filmed areas, which would raise awareness "
          "of their presence. This awareness would lead people who plan to commit offences in these areas to "
          "\"think twice\" before doing so, since they would realize that their chances of being caught had risen "
          "considerably. For example, since cameras were installed at traffic lights, the number of vehicles "
          "crossing on a red light has dropped significantly. Since the situation is very similar, it stands to "
          "reason that the same would happen here: knowing that the cameras exist would deter offenders and, as "
          "a result, would probably reduce the number of offences committed in filmed public spaces.")

P_ARG2 = ("In addition, I believe that installing the cameras could make law enforcement considerably more efficient and increase the number "
          "of crimes that are solved, while reducing the resources needed to do so. With the help of the cameras, "
          "the police could work faster, both while an offence is taking place, by sending officers to the area "
          "and stopping it, and afterwards, by identifying and locating suspects more quickly and later proving "
          "their guilt. This step would probably save a great deal of time, manpower and money, since "
          "without the cameras officers would have to question passers-by and invest considerable resources in "
          "searching for other evidence. For instance, suppose that the police arrest a suspect in the act. "
          "Footage of that person committing the offence would make it easier to prove his guilt, and in many "
          "cases he would be sent to prison. That is, the footage would help not merely to prove guilt, but also "
          "to prevent that person from committing future offences, which in turn would consume further resources.")

P_REBUT = ("On the other hand, some argue that operating cameras in public spaces would violate the privacy of the "
           "public. Since the cameras can identify people and vehicles with a high degree of certainty, the "
           "database would hold information about people's locations without their consent, unlike, for example, "
           "tracking by certain apps, which depends on each person's own choice of permission settings on the "
           "device. At first glance, this argument seems very reasonable. However, in the age of smartphones and "
           "social media, the privacy argument largely does not hold in this case. Even if a person "
           "can deny tracking permissions to certain apps, mobile phone companies know the exact location of the "
           "phone at every moment, and this monitoring cannot be switched off. Since many people today keep their "
           "phones with them wherever they go, there is, in practice, a constant ability to track a large part of "
           "the population.")

P_CLOSE = ("In conclusion, in my opinion, placing face-recognition cameras in public spaces would create deterrence "
           "that would reduce the number of offences committed there. Moreover, operating this system would "
           "probably make law enforcement more efficient and save considerable resources, which could then be "
           "used for other important purposes.")

SB_INTRO = ['The exam page', 'Why it matters', 'Why an essay?', 'Where in the test',
            'Academic writing', 'An argument essay', 'Explain, not persuade', 'No right answer',
            'Skills you have', 'A skill for life']

SB_RULES = ['The instructions', 'Time: 35 minutes', 'One given task', 'Length: 25 to 50', 'Too short',
            'Scrap paper', 'One answer sheet', 'Style and language', 'Which language?', 'Pencil and eraser',
            'Only on the lines']

SB_RUBRIC = ['Why a rubric', 'Two rubrics', 'The criteria', 'A toolbox', 'Stay under the radar']

SB_SCORE = ['Two raters', 'One rater: 2 to 12', 'The total: 4 to 24', 'A third rater', 'Disqualified',
            '25% of Verbal', 'Hidden in Verbal']

SB_EXPECT = ['An example task', 'The question', 'Two values clash', 'Opening paragraph', 'What it does',
             'Language in it', 'Argument paragraph 1', 'How it is built', 'One argument each',
             'Quotation marks', 'Argument paragraph 2', 'Hedging = opinion', 'Another perspective']

SB_EXPECT2 = ['Rebuttal paragraph', 'Why a rebuttal', 'Their block', 'Our answer',
              'Closing paragraph', 'Content: polished', 'What we saw']

SB_BASE = ['Where you start', 'Your task', 'The rules', 'No pressure', 'Keep it', 'Before and after']

MODULES = [
# ------------------------------------------------------------------ 1. first look + introduction (seg01)
lesson('vr50-a-intro', 'The Writing Task', SB_INTRO, [
 dict(mode='title', title='The Writing Task', script=[
  "Welcome to the start of our writing lessons!",
  "This is the biggest single topic in Verbal Reasoning.",
  "Before anything else, let's see what it actually looks like on the day.",
 ]),
 dict(mode='concept', active=0, title='The exam page', script=[
  "This is what you get. A page with the instructions on top, and the task in a frame below.",
  A('The exam page appears', PAGE),
  RC('Instructions on top', 'On top: the instructions. The same every time.', 70),
  "At the top: the instructions. They are the same in every test, so you will know them by heart.",
  RC('The task in a frame', 'In the frame: the task. A short text that presents an issue.', 200),
  "Inside the frame: the task. A short text that presents some issue, with the people for it and against it.",
  RC('The question in bold', 'At the end, in bold: the question you must answer.', 330),
  "And at the very end, in bold, the question itself. That is what you must answer.",
  D("teacher circles the bold question at the bottom of the frame"),
  RC('35 minutes', '35 minutes for the whole essay.', 460),
  "You have 35 minutes to read the task, plan, and write.",
  "This page is a re-created example with a task we wrote for the course. The real one looks just like it.",
 ]),
 dict(mode='concept', active=1, title='Why it matters', script=[
  L('25% of Verbal', 'The essay = 25% of your Verbal Reasoning score', 110, 44),
  "Why should you care? The essay is a quarter of your Verbal Reasoning score.",
  L('About a tenth of the total', 'That is roughly a tenth of your whole test score', 220, 40),
  "And since Verbal is a big part of the general score, the essay alone is roughly a tenth of your whole test score.",
  L('You can improve fast', 'You can improve here fast: follow the lessons and do the practice', 320, 36),
  "Many students neglect it. That's a mistake. This is a topic where you can improve a lot in a short time.",
  "Follow the lessons, do the practice essays, and this one topic can move your score by tens of points.",
  L('Useful beyond the test', 'And it matters beyond the test, too', 440, 36),
  "And by the way, what you learn here matters far beyond the test. We'll come back to that.",
 ]),
 dict(mode='concept', active=2, title='Why an essay?', script=[
  "Why was a writing task added to the test? It wasn't always there.",
  L('Writing is key in academic studies', 'Writing is a key skill in academic studies', 110, 42),
  "In short: someone concluded that writing is a key skill for academic studies.",
  L('Papers, exams, research, articles', 'Papers · exams · research · articles', 210, 38),
  "You need it everywhere at university: papers, exams, research, articles.",
  L('Other tests do it too', 'Other admission tests around the world, such as the GRE, include a writing task too', 300, 32),
  "And it's not only us. Other admission tests around the world include a writing task as well.",
 ]),
 dict(mode='concept', active=3, title='Where in the test', script=[
  L('The essay comes first', 'The test opens with the writing task', 110, 44),
  "The test starts with the essay. It's the very first thing you do.",
  L('35 minutes', '35 minutes · then the essays are collected', 210, 40),
  "You get 35 minutes. Then the essays are collected.",
  L('Then the multiple-choice sections', 'Then: the multiple-choice sections (Verbal, Quantitative, English)', 310, 36),
  "After that, the multiple-choice sections begin: Verbal Reasoning, Quantitative Reasoning and English.",
 ]),
 dict(mode='concept', active=4, title='Academic writing', script=[
  "There are many kinds of essays. For this test, NITE chose academic writing.",
  L('Academic writing', 'Academic writing: the style of papers, exercises and articles at university', 110, 38),
  "Why? Because that's the style used at university, for papers, exercises and articles.",
  L('Presenting and discussing ideas', 'Its job: to present ideas and discuss them', 220, 38),
  "Academic writing is used to present ideas and to discuss them.",
  L('What is tested', 'Tested: forming an idea in writing, supporting it, and expressing it in an organized way, in rich, complex language', 310, 34),
  "The skill being tested: forming an idea in writing, supporting it, and expressing it in an organized way, in rich language.",
  L('Content', 'CONTENT: what you write (the idea and how you support it)', 470, 34),
  "So there are two sides here. Content: what you write. The idea, and how you back it up.",
  L('Language', 'LANGUAGE: how you write (rich, clear, correct)', 550, 34),
  "And language: how you write it. Rich, clear, correct language.",
 ]),
 dict(mode='concept', active=5, title='An argument essay', script=[
  "In practice, you're asked to write an argument essay. For and against.",
  L('An issue is presented', 'The task presents an issue: a new law, cancelling an old law, a proposal, a trend', 110, 34),
  "The task presents an issue. A new law someone wants to pass, an old law someone wants to cancel, a proposal, some trend.",
  L('Example question', 'e.g. "Children get their first phone at a younger and younger age. What is your opinion of this trend? Give reasons."', 230, 34),
  "For example: children get their first phone at a younger and younger age. What do you think of this? Give reasons.",
  L('Every side has pros and cons', 'Every position has advantages and disadvantages', 380, 36),
  "Obviously, every position here has advantages and disadvantages.",
  L('Choose the side whose advantages are bigger', 'Choose the position whose advantages you think are bigger, and give arguments that show why', 460, 36),
  "Your job: choose the position whose advantages, in your view, are bigger. Then give arguments that explain why.",
 ]),
 dict(mode='concept', active=6, title='Explain, not persuade', script=[
  "Many students pick the position they think will be more convincing. And that creates pressure.",
  L('You do not have to persuade', 'You do not have to persuade the other side', 110, 42),
  "Listen: you don't have to persuade the other side.",
  L('You have to explain', 'You have to EXPLAIN why you chose your position', 200, 42),
  "You have to explain why you chose your position.",
  "Why do I insist on this? When we try to persuade someone, we often take a more extreme position, to pull them our way.",
  L('Not extreme, not too sweeping', 'So choose what you really think. No need to be extreme or too sweeping', 300, 36),
  "Here you don't need that. So choose the position you really think is right. No need to be extreme or too sweeping.",
  L('But: strong arguments', 'But your arguments must still be strong and convincing', 400, 36),
  "But careful. This does not mean average arguments. You need strong, convincing arguments, or the reader won't understand why you chose your side.",
 ]),
 dict(mode='concept', active=7, title='No right answer', script=[
  "Another important point: the opinion you choose doesn't really matter.",
  L('Any position is legitimate', 'There is no right or wrong position. Any position is legitimate', 110, 40),
  "Nobody expects position X or position Y. There's no right or wrong here.",
  "If one side were clearly right, the task would not be on the test.",
  L('Both sides have pros and cons', 'Test tasks always allow both positions', 210, 38),
  "The tasks are always ones where it's legitimate to take either side. Each has advantages and disadvantages.",
  L('What counts', 'What counts: how well it is reasoned, supported and worded', 300, 38),
  "What counts is how well your position is reasoned, supported and worded.",
  L('Some are easier to explain', 'Still: some positions are easier to explain. We will see which', 400, 36),
  "Still, we'll see later that some positions are easier to explain, so it can be smart to choose them.",
 ]),
 dict(mode='concept', active=8, title='Skills you have', script=[
  "By the way, writing an essay combines skills you're already learning in Verbal Reasoning.",
  L('Strengthen and weaken', 'Strengthening and weakening arguments: you weaken the other side and strengthen yours', 110, 34),
  "Strengthening and weakening arguments: you face opposing views, you weaken them, and you strengthen your own.",
  L('Analogies and comparisons', 'Analogies and comparisons: explaining one case through a similar one', 220, 34),
  "Analogies and comparisons: sometimes you explain an argument by comparing it to a similar case.",
  L('Main point vs detail', 'Telling the main point from the details', 310, 34),
  "Telling the main point from the details.",
  L('Reading and sentence structure', 'Reading comprehension and understanding how sentences are built', 380, 34),
  "Reading comprehension, and understanding how sentences are built.",
 ]),
 dict(mode='concept', active=9, title='A skill for life', script=[
  "And as I said, this isn't only for university.",
  L('We discuss things every day', 'At home and at work, we explain our positions every day', 110, 40),
  "At home and at work, we explain our positions to people who think differently every single day.",
  L('Skills you will keep', 'Explaining a position clearly is a skill you will keep long after the test', 220, 36),
  "So the skills in these lessons are ones you'll keep long after the test.",
  "Next: the instructions on that page, one by one.",
 ]),
], T50),

# ------------------------------------------------------------------ 2. the instructions (seg01, second half)
lesson('vr50-a-rules', 'The Instructions', SB_RULES, [
 dict(mode='title', title='The Instructions', script=[
  "Let's go through the instructions on the exam page, one by one.",
  "Nothing complicated, but every line matters.",
 ]),
 dict(mode='concept', active=0, title='The instructions', script=[
  A('The exam page appears', PAGE),
  "Here's the page again. Let's zoom in on the instructions at the top.",
  RC('Technical rules', 'Most of the lines are technical rules: time, length, paper, pencil.', 70),
  "Most of the lines are technical: time, length, paper, pencil.",
  RC('Content and language', 'Two lines are about content and language: academic style, organization, clear correct language.', 230),
  "Two lines are about something bigger: how you write. Style, organization and language.",
  RC('Know them by heart', 'Know them before the test, so you do not waste a minute reading them.', 420),
  "Know them before the test, so you don't spend precious minutes reading them.",
 ]),
 dict(mode='concept', active=1, title='Time: 35 minutes', script=[
  L('35 minutes', '"The time allotted is 35 minutes."', 110, 44),
  "First line: the time allotted is 35 minutes.",
  "In the Hebrew test it's 30. In English and the other languages it's 35.",
  L('For everything', 'Reading the task + planning + writing + a quick check', 210, 38),
  "Those 35 minutes are for everything: reading the task, planning, writing, and a quick check at the end.",
  L('Practise with a timer', 'Practise every essay with a 35-minute timer', 300, 38),
  "So every practice essay you write: with a timer, 35 minutes. Exactly like the test.",
 ]),
 dict(mode='concept', active=2, title='One given task', script=[
  L('Read the task in the frame', '"Read the task carefully and write your essay on the lined answer sheet."', 110, 38),
  "Next: read the task carefully, and write your essay on the lined answer sheet.",
  L('One topic, no choice', 'The topic is given. You cannot choose a different one', 220, 40),
  "The task is in the frame. That means the topic is fixed. You can't choose a different topic.",
  L('Answer exactly that', 'Answer exactly the question asked, not a nearby one', 310, 38),
  "And you must answer exactly that question. Not something close to it. We'll spend a whole lesson on this.",
 ]),
 dict(mode='concept', active=3, title='Length: 25 to 50', script=[
  L('At least 25 lines', 'At least 25 lines', 110, 44),
  "The essay must be at least 25 lines long.",
  L('No more than 50', 'No more than the 50 lines on the sheet', 200, 44),
  "And no longer than the lines on the answer sheet. There are 50.",
  L('Good essays: 30-40 lines', 'Good essays: usually about 30-40 lines in average handwriting', 290, 38),
  "NITE's own experience: a good essay in average-size handwriting is usually about 30 to 40 lines.",
  L('Beyond line 50: not read', 'Anything after line 50 is not read', 380, 38),
  "What happens if you go past 50? Everything after line 50 is simply not read.",
 ]),
 dict(mode='concept', active=4, title='Too short', script=[
  "And what if the essay is too short?",
  L('Under 25: points deducted', 'Fewer than 25 lines → points are deducted from your score', 110, 38),
  "Fewer than 25 lines, and points are deducted from your score.",
  L('10-23 lines', '10-23 lines: the essay is rated, but marked as too short', 210, 38),
  "The raters' guide says it clearly: an essay of 10 to 23 lines is rated, but it's marked as too short.",
  L('0-9 lines', '0-9 lines: disqualified → the lowest possible score', 310, 38),
  "Nine lines or fewer: the essay is disqualified. It gets the lowest possible score.",
  L('Aim for 30-40', 'So aim for 30-40 lines, and never fewer than 25', 410, 38),
  "So, the target is simple: 30 to 40 lines, and never fewer than 25.",
 ]),
 dict(mode='concept', active=5, title='Scrap paper', script=[
  L('Scrap paper in the booklet', 'Need scrap paper? Use the pages in the test booklet', 110, 40),
  "Need scrap paper? Use the pages set aside for it in the test booklet.",
  L('The draft is not marked', 'The draft is not marked. Scribble whatever you like', 200, 40),
  "The draft is not marked. You can scribble whatever you want there.",
  L('Plan there', 'Use it to plan: your position, your arguments, the order', 290, 38),
  "Use it for planning: your position, your arguments, the order of the paragraphs. We'll learn exactly how.",
 ]),
 dict(mode='concept', active=6, title='One answer sheet', script=[
  L('No extra sheet', 'You will not get another answer sheet, or a replacement', 110, 40),
  "You will not get an extra answer sheet. And you can't swap the one you have.",
  L('So plan first', 'So plan before you write', 210, 44),
  "That's why planning matters. Otherwise you can end up with a messy sheet, or a full draft, and no room to continue.",
  L('A clean start', 'Start writing on the sheet only when you know where the essay is going', 300, 36),
  "Start writing on the sheet only when you know where the essay is going.",
 ]),
 dict(mode='concept', active=7, title='Style and language', script=[
  "Up to now, technical rules. Now two lines about content and language.",
  L('Academic style', '"Use a style that is consistent with academic writing."', 110, 38),
  "Use a style that is consistent with academic writing.",
  L('Well organized', '"Make sure your essay is well organized..."', 210, 38),
  "Make sure your essay is well organized.",
  L('Clear, correct language', '"...and written in clear, grammatically correct language."', 300, 38),
  "And written in clear, grammatically correct language.",
  L('Content + language', 'These lines are the two rubrics in a nutshell: content and language', 410, 36),
  "These lines are, in a nutshell, what the raters check. We'll see the two rubrics in the next lesson.",
 ]),
 dict(mode='concept', active=8, title='Which language?', script=[
  L('Language of the test', 'In general: write in the language of the test', 110, 40),
  "In general, you write the essay in the language of the test.",
  L('Combined/English test', 'Combined/English test: Hebrew, English, Russian, German, Amharic, Italian, Hungarian, Portuguese or Dutch', 200, 36),
  "In the Combined/English test, NITE allows the essay in one of these languages: Hebrew, English, Russian, German, Amharic, Italian, Hungarian, Portuguese or Dutch.",
  L('We practise in English', 'In this course we practise in English', 340, 40),
  "In this course, we practise in English.",
  L('Other language: score 0', 'Any other language (or an off-topic essay): score 0', 430, 36),
  "An essay in another language, or one that doesn't relate to the topic, gets zero on both content and language.",
 ]),
 dict(mode='concept', active=9, title='Pencil and eraser', script=[
  L('Pencil only', 'Write the essay in pencil. You may use an eraser', 110, 40),
  "Write in pencil. And yes, you may use an eraser. You're allowed to erase and correct.",
  L('Mechanical is fine', 'A mechanical pencil is fine, if it writes dark enough', 200, 38),
  "Many students ask: a mechanical pencil? Yes, no problem.",
  "Just make sure it writes dark enough for the scanner. A very light lead, the kind used for technical drawing, is not good. Regular leads are fine.",
  L('Legible and neat', 'Handwriting: legible and neat', 290, 40),
  "And make sure your handwriting is legible and neat. The raters must be able to read you.",
 ]),
 dict(mode='concept', active=10, title='Only on the lines', script=[
  A('The answer sheet appears', SHEET),
  "Here's the sheet again. At the top you fill in your ID and details. Below: the lines.",
  RC('Scanned', 'The sheets are scanned. Write only on the lines.', 60),
  "The sheets are scanned electronically. So write only on the printed lines. Not in the margins.",
  RC('Outside the lines', 'Anything outside the lines is not read.', 200),
  "Everything outside the lines is not read.",
  D("teacher shades the empty area below line 50"),
  RC('No notes to the rater', 'No stars, no notes: "I didn\'t finish the last paragraph, but..."', 320),
  "So no stars, no notes to the rater like: I didn't manage to finish the last paragraph, but.",
  RC('The rater stops at 50', 'The rater reaches the end of line 50 and stops, even if one word is left.', 480),
  "The rater gets to the end of line 50 and stops. Even if there's one more word.",
  "That's it for the instructions. Not too complicated. Next: how the essay is rated.",
 ]),
], T50),

# ------------------------------------------------------------------ 3. the rubrics (seg02)
lesson('vr50-a-rubric', 'How the Essay Is Rated', SB_RUBRIC, [
 dict(mode='title', title='How the Essay Is Rated', script=[
  "How is an essay rated? That's the problem with essays.",
  "Let's meet the tool the raters use: the rubric.",
 ]),
 dict(mode='concept', active=0, title='Why a rubric', script=[
  L('No multiple choice', 'No multiple choice: no answer that is simply right or wrong', 110, 38),
  "In the rest of the test, an answer is right or wrong. Here there's no such thing.",
  L('A judgement', 'Different raters may give the same essay different scores', 210, 38),
  "The rating is a judgement. Different raters can give the same essay a different score.",
  L('A rubric', 'The fix: a rubric. A list of criteria + what each score looks like', 310, 38),
  "To keep raters as close to each other as possible, they get precise guidelines: a rubric.",
  "A rubric lists the criteria to check, and describes what each score looks like on each criterion.",
 ]),
 dict(mode='concept', active=1, title='Two rubrics', script=[
  L('Two rubrics', 'Two rubrics, rated separately:', 110, 44),
  "On this test there are two rubrics, and the raters rate them separately.",
  L('The content rubric', 'The content rubric: what you say', 200, 40),
  "The content rubric: what you say.",
  L('The language rubric', 'The language rubric: how you say it', 280, 40),
  "And the language rubric: how you say it.",
  L('1 to 6', 'Each is rated from 1 (very poor) to 6 (very good)', 370, 40),
  "Each one gets a score from 1, very poor, to 6, very good.",
 ]),
 dict(mode='concept', active=2, title='The criteria', script=[
  "Let's start with content. I won't go through every box. What matters now are the criteria.",
  L('Heading', 'Content: a clear main idea, relevant to the task', 100, 42),
  "The heading, what the raters look for first: a clear main idea, relevant to the task.",
  L('1', '1 · Development of the thesis: are the ideas explained and supported?', 200, 34),
  "Under it: development of the thesis. Do you explain and support your ideas?",
  L('2', '2 · Focus and coherence: one line of thought, no jumping, no repetition', 290, 34),
  "Focus and coherence. One clear line of thought, no jumping around, no needless repetition.",
  L('3', '3 · Critical thinking: define the issue, opinion vs fact, several perspectives, answer the other side', 380, 34),
  "And critical thinking: defining the issue precisely, telling opinion from fact, several perspectives, and answering the other side.",
  L('Language', 'Language: clarity and academic style · precise words · grammar · varied sentences · organizational tools (connectors, paragraphs)', 500, 34),
  "And the language rubric: clarity and academic style, precise words, correct grammar, varied sentences, and organizational tools, like connectors and paragraphs.",
  L('Best fit', 'Each criterion is rated 1 to 6; raters pick the description that fits best', 640, 34),
  "Each one is rated from 1 to 6, and raters pick the description that fits best. Each rubric gets its own lesson. This is the map.",
 ]),
 dict(mode='concept', active=3, title='A toolbox', script=[
  L('Thinking is tested', 'One thing the essay tests is thinking: critical thinking', 110, 40),
  "One of the main things this essay tests is thinking. Critical thinking.",
  L('A toolbox', 'Like the toolbox in Quantitative Reasoning, you will get a toolbox for thinking critically and expressing yourself well', 210, 36),
  "Just like in Quantitative Reasoning you have a toolbox of methods, here too we'll give you a toolbox.",
  "Tools to think critically, and tools to express yourself better.",
 ]),
 dict(mode='concept', active=4, title='Stay under the radar', script=[
  "One small tip to end this lesson.",
  L('Silence is wisdom', '"If you are not sure, leave it out."', 100, 44),
  "There's an old saying: if you don't know, better stay silent than say something foolish.",
  L('Few mistakes', 'We are not professional writers. The goal: as few mistakes as possible', 190, 36),
  "How is this related to the essay? We're not professional writers. Our goal is to make as few mistakes as possible.",
  L('No risks', 'Fly under the radar: take no risks', 280, 38),
  "To fly under the radar. So the rule is: don't take risks. Don't try to show off.",
  L('Big words', '✗ "The cameras will exacerbate public safety."  (meant: improve)', 370, 34),
  "It happens most in language. Students try to show richness with big words they don't really know, like this.",
  D("teacher crosses out \"exacerbate\""),
  L('Simple and right', '✓ "The cameras will improve public safety."', 450, 34),
  "Exacerbate means make worse. The simple word would have been right. A wrong big word really hurts. We'll come back to this.",
  "Done with the rubrics. Next: the score itself.",
 ]),
], T50),

# ------------------------------------------------------------------ 4. the score (seg03)
lesson('vr50-a-score', 'The Essay Score', SB_SCORE, [
 dict(mode='title', title='The Essay Score', script=[
  "How does the essay score work?",
  "Let's follow the numbers from the raters to your Verbal Reasoning score.",
 ]),
 dict(mode='concept', active=0, title='Two raters', script=[
  L('Two raters', 'Two raters read every essay, independently', 110, 44),
  "To make the score as accurate as possible, your essay is read by two raters, not one.",
  L('Why two', 'More raters = more accurate. NITE found that two give a good estimate', 210, 38),
  "Of course, the more raters, the more accurate. But NITE found that two raters give a pretty good estimate.",
  L('Trained raters', 'Experienced raters, trained to rate objectively and fairly', 310, 38),
  "They're experienced raters, trained to rate objectively and fairly.",
 ]),
 dict(mode='concept', active=1, title='One rater: 2 to 12', script=[
  L('Content 1-6', 'Content: 1-6', 110, 44),
  "Each rater gives two scores. Content, from 1 to 6.",
  L('Language 1-6', 'Language: 1-6', 190, 44),
  "And language, from 1 to 6.",
  L('One rater 2-12', 'One rater: content + language = 2 to 12', 290, 44),
  "Add them up, and one rater gives you between 2 and 12.",
 ]),
 dict(mode='concept', active=2, title='The total: 4 to 24', script=[
  L('Sum of both raters', 'The essay score = the sum of the two raters\' scores for the two components', 110, 38),
  "The essay score is the sum of both raters' scores, for both components.",
  L('4 to 24', 'Rater 1 (2-12) + Rater 2 (2-12) = 4 to 24', 220, 44),
  "So: between 4 and 24.",
  L('Example', 'e.g. Rater 1: 4 + 5 = 9 · Rater 2: 5 + 5 = 10 → 19', 320, 38),
  "For example: one rater gives content 4, language 5. That's 9. The other gives 5 and 5. That's 10. Your essay score: 19.",
 ]),
 dict(mode='concept', active=3, title='A third rater', script=[
  "Sometimes the two raters don't agree. That's natural. As the name says, it's an evaluation, not an exact score.",
  L('Small gaps are normal', 'Small gaps between raters are normal: the scale stays 4-24', 110, 38),
  "As long as the gap isn't too big, we stay with the 4 to 24 scale.",
  L('Major discrepancy', 'A major discrepancy → a third, senior rater decides', 210, 38),
  "But if the gap is too big, a major discrepancy, a third, senior rater is brought in to decide.",
  L('Total vs total', 'The raters\' totals are compared, not each component', 310, 38),
  "And they compare each rater's total, not content against content.",
  L('NITE sets the threshold', 'How big is "major"? NITE sets it and has changed it over time. It is larger than most people think', 400, 34),
  "How big is too big? NITE decides, and it has changed over the years as they gain experience. It's bigger than most people think.",
  "In the end it adds up to a few points in your raw score. Not something to worry about.",
 ]),
 dict(mode='concept', active=4, title='Disqualified', script=[
  L('Off-topic', 'An essay not related to the task\'s topic → disqualified', 110, 38),
  "An essay that isn't on the topic of the task is disqualified. So is one of nine lines or fewer.",
  L('Lowest score', 'The raters mark 1 for content and 1 for language', 200, 38),
  "What score does it get? The guide says: zero. But on a scale of 4 to 24 there is no real zero.",
  "In the raters' instructions, a disqualified essay is marked 1 for content and 1 for language.",
  L('= 4', 'So it gets the bottom of the scale: 4 out of 24', 290, 40),
  "So in practice, it's the bottom of the scale: 4. As if it got 1 on everything.",
  L('Never off-topic', 'Lesson: a brilliant essay on the wrong topic is worth the minimum', 380, 36),
  "The lesson: a brilliant essay on the wrong topic is worth the minimum. Stay on the task.",
 ]),
 dict(mode='concept', active=5, title='25% of Verbal', script=[
  L('4 to 24 → Verbal', 'The essay score (4-24) goes into your Verbal Reasoning score', 110, 38),
  "Now we take that 4-to-24 score and weigh it into your Verbal Reasoning score.",
  L('25%', 'Weight: 25% of Verbal Reasoning', 200, 44),
  "The weight of the essay: 25% of Verbal Reasoning.",
  L('About a tenth', 'That is about a tenth of the general test score', 290, 40),
  "And that comes to about a tenth of your general score.",
  L('200-800', 'General score: 200-800 → a range of 600 points → the essay ≈ 60 of them', 380, 36),
  "Remember, the general score runs from 200 to 800. So the range is 600 points, and a tenth of that is about 60 points.",
  "Sixty points. From one 35-minute task.",
 ]),
 dict(mode='concept', active=6, title='Hidden in Verbal', script=[
  L('Converted', 'The essay score is converted and combined with the Verbal sections', 110, 38),
  "The essay score is converted and combined with your multiple-choice Verbal sections.",
  L('One Verbal score', 'You get one Verbal Reasoning score that already includes the essay', 210, 38),
  "Besides the general score, you get a score in each domain: Verbal, Quantitative, English.",
  "Your Verbal score already includes the essay.",
  L('No separate essay score', 'You cannot see the essay score on its own', 310, 40),
  "But you can't see how much you got on the essay itself. It's hidden inside the Verbal score.",
 ]),
], T50),

# ------------------------------------------------------------------ 5. what is expected of me, part 1 (seg04)
lesson('vr50-a-expect', 'What Is Expected of Me', SB_EXPECT, [
 dict(mode='title', title='What Is Expected of Me', script=[
  "Just before we dive into content, language, paragraphs and arguments,",
  "let's look at an example task, and a fairly high-level essay that answers it.",
 ]),
 dict(mode='concept', active=0, title='An example task', script=[
  "Here's the example task. Read it with me.",
  A('The task appears', dict(prompt_box(CAM_PROMPT, CAM_QUESTION, w=1140), x=410, y=60)),
  "First, the background: security officials want a national network of face-recognition cameras in public spaces.",
  "What for? To identify people in real time, and to stop offences before, during and after they happen.",
  "Supporters say it will reduce, even eliminate, crime in the monitored areas.",
  "Opponents say it will seriously violate privacy.",
 ]),
 dict(mode='concept', active=1, title='The question', script=[
  "Up to here, the background. And now the question. It always comes last, in bold.",
  L('The question', '"In your opinion, should security officials be allowed to place face-recognition cameras in public spaces? Give reasons."', 110, 38),
  D("teacher underlines \"In your opinion\" and \"Give reasons\""),
  L('Two jobs', 'Two jobs: say what you think + explain why', 290, 40),
  "Two jobs: say what you think, and explain why.",
 ]),
 dict(mode='concept', active=2, title='Two values clash', script=[
  "What's the issue really about? It sets two values, two rights, against each other.",
  L('Security', 'The right to life and security', 110, 42),
  "On one side: the right to life and security.",
  L('vs', 'versus', 190, 36),
  L('Privacy', 'The right to privacy', 260, 42),
  "On the other: the right to privacy.",
  L('Our job', 'We say which weighs more here, and explain why', 360, 38),
  "We have to say which one we think should win here, and explain why.",
 ]),
 dict(mode='concept', active=3, title='Opening paragraph', script=[
  "Let's see how the essay looks. We start with an opening paragraph that gives the background to the debate.",
  A('The opening paragraph appears', T(P_OPEN, size=36, x=410, y=80, w=1140)),
  "Recently, security officials have been working to set up a national network of face-recognition cameras in public spaces.",
  "The cameras are meant to help catch offenders, and thus reduce, perhaps even eliminate, crime.",
  "However, some people have come out strongly against this move, because of the harm to privacy.",
  "In my opinion, these cameras should be installed, since their benefits to public safety are likely to outweigh the harm to privacy.",
  D("teacher underlines \"In my opinion, these cameras should be installed\""),
 ]),
 dict(mode='concept', active=4, title='What it does', script=[
  L('Background', 'Background to the debate: taken from the task itself', 110, 38),
  "What does the opening do? It gives the background. Most of it comes from the task itself.",
  L('Content: less tested here', 'So content is tested less here: it is the task\'s own material', 200, 38),
  "So the content is tested less in this paragraph. It's material the task already gave us.",
  L('Position at the end', 'The position is stated at the end of the opening', 290, 38),
  "But one content point is crucial: I state my opinion already at the end of the opening. I'm for the cameras.",
  L('Why', 'So the rater knows exactly where the essay is going', 380, 38),
  "Why? To keep a clear main idea, so the rater knows exactly what I'm going to argue.",
  L('Next', 'The next paragraphs explain WHY', 470, 38),
  "And of course, in the next paragraphs I have to explain why.",
 ]),
 dict(mode='concept', active=5, title='Language in it', script=[
  "Language is checked everywhere, including in the opening. No mistakes, and some richness.",
  L('Rich phrases', '"have come out strongly against" · "are likely to outweigh"', 110, 38),
  "Look at phrases like these: have come out strongly against. Are likely to outweigh. Calm, precise and hedged.",
  L('Do not overdo it', 'But do not overdo it: a phrase or two, not one in every line', 210, 38),
  "But as we'll learn, you must not overdo it.",
  L('One register', 'Keep one register throughout: do not jump from chat to lofty style', 300, 38),
  "And keep one consistent register. A certain level of language, the same all the way. No jumping from everyday chat to lofty words.",
 ]),
 dict(mode='concept', active=6, title='Argument paragraph 1', script=[
  "Now the first argument paragraph. My first reason for the cameras.",
  A('The first argument paragraph appears', T(P_ARG1, size=32, x=410, y=60, w=1140)),
  "In my opinion, the cameras would create deterrence, which would lead to fewer offences in the monitored areas.",
  D("teacher underlines the first sentence"),
  "It's reasonable to assume there'd be a campaign and signs. That raises awareness.",
  "Awareness makes offenders think twice, because their chances of being caught have gone up.",
  "For example: since cameras were installed at traffic lights, fewer cars cross on a red light.",
  "It's a similar situation, so it stands to reason the same would happen here.",
 ]),
 dict(mode='concept', active=7, title='How it is built', script=[
  L('Key sentence', 'Key sentence: position + reason (deterrence → fewer offences)', 90, 36),
  "The paragraph opens with a key sentence: in my opinion, plus my reason. Deterrence, which leads to fewer offences.",
  L('An opinion, not a fact', 'It is an opinion, not a fact, so it must be explained', 180, 36),
  "That's an opinion, not a fact. So I have to explain why I think it's true.",
  L('Development', 'Development: cameras → campaign and signs → awareness → "think twice" → fewer offences', 270, 34),
  "That's the development. Step by step: cameras, a campaign, awareness, offenders think twice, fewer offences.",
  L('Nothing is obvious', 'Nothing is obvious: explain every step, from the cameras to the result', 380, 36),
  "We'll learn that nothing is obvious. You must explain every step, from the cameras to the result.",
  L('Support', 'Support: a comparison to a similar case (traffic-light cameras)', 470, 36),
  "And at the end, support. Up to here I explained with logic. Now I compare to a similar case, traffic-light cameras, to make it stronger.",
 ]),
 dict(mode='concept', active=8, title='One argument each', script=[
  L('One argument', 'This paragraph deals with one argument only: deterrence', 110, 40),
  "Notice: this paragraph talks about one argument only. Deterrence.",
  L('One argument per paragraph', 'Rule: one argument per paragraph (two points from the same field that serve ONE argument may share it)', 190, 36),
  "We'll learn this rule: one argument per paragraph. Two points from the same field may share a paragraph, but only when together they serve one argument.",
  L('Other reasons', 'Another reason? It gets its own paragraph, or pick only the strongest', 320, 36),
  "A different reason doesn't go in here. It gets its own paragraph, or you choose only your strongest ones.",
  L('Connectors', 'Connectors show how each sentence links to the next: "For example", "as a result"', 410, 36),
  "And there's a clear flow. Connectors like for example and as a result show how each sentence links to the next.",
  L('Hedging', 'Hedged: "It is reasonable to assume", "it stands to reason"', 510, 36),
  "And look at the hedging: it is reasonable to assume. It stands to reason. Not: the cameras will certainly.",
  "That's academic writing: qualified claims, not sweeping ones. Two different phrases for the same idea, too. That's richness.",
 ]),
 dict(mode='concept', active=9, title='Quotation marks', script=[
  L('"think twice"', 'Quotation marks: "think twice"', 110, 42),
  "By the way: think twice, in quotation marks. Some people say quotation marks are forbidden in academic writing.",
  L('Not forbidden', 'Not forbidden. Use them rarely, when they really help', 200, 40),
  "That's not true. Better to use them rarely, but you can when it serves the content.",
  L('Once is enough', 'An informal phrase in quotation marks: once in an essay, at most', 290, 38),
  "Here the informal phrase says it simply and clearly. Fine. But once in an essay. No more.",
 ]),
 dict(mode='concept', active=10, title='Argument paragraph 2', script=[
  "The second argument paragraph: my second reason for the cameras.",
  A('The second argument paragraph appears', T(P_ARG2, size=31, x=410, y=50, w=1140)),
  "In addition, I believe the cameras could make law enforcement considerably more efficient, and save resources.",
  "The police could act during the offence, and afterwards: identify, locate, prove guilt.",
  "This would probably save time, manpower and money. Without cameras, officers would question passers-by and search for other evidence.",
  "Then an example: a suspect caught in the act. The footage helps prove guilt, and he can't commit further offences.",
 ]),
 dict(mode='concept', active=11, title='Hedging = opinion', script=[
  L('could', '"could make ... more efficient", not "will make"', 110, 38),
  "Look again at the hedging: could make law enforcement more efficient. Not: will make.",
  L('Two reasons', 'Two reasons to hedge:', 200, 38),
  "Why? For two reasons.",
  L('Academic style', '1 · Academic style (language): qualified, not sweeping', 270, 36),
  "One: academic style. That's language.",
  L('Opinion vs fact', '2 · Opinion vs fact (critical thinking): "could" marks an opinion', 340, 36),
  "Two: critical thinking. Distinguishing opinion from fact.",
  "Could make things more efficient says: this is my view. Will make them more efficient states a fact I can't really know.",
  L('Opinion once', '"In my opinion": once, in the key sentence. In the development: hedging (could, may, is likely to)', 430, 34),
  "So in my opinion, or I believe that, goes once, at the start of the key sentence. Inside the development I don't repeat it. Hedging words like could, may and is likely to do that job.",
  L('Level', 'Richer phrases now and then: "not merely", "which in turn"', 530, 36),
  "Notice some higher phrases: not merely, which in turn. But the essay is not full of dictionary words.",
  "Normal, simple, clear writing. Just not everyday chat, with a higher phrase here and there.",
 ]),
 dict(mode='concept', active=12, title='Another perspective', script=[
  L('Perspective 1', 'Paragraph 1: the security perspective (fewer offences, safer citizens)', 110, 36),
  "One more thing. The first paragraph looked at the issue from a security angle. Fewer offences, safer citizens.",
  L('Perspective 2', 'Paragraph 2: the economic perspective (saving resources)', 200, 36),
  "The second looks from an economic angle. Saving resources.",
  L('Critical thinking', 'Several perspectives = part of critical thinking', 290, 40),
  "That's part of what's rated: critical thinking includes looking at the issue from several perspectives.",
  L('Logic + example', 'Again: logical explanation first, then an example', 380, 38),
  "And the build is the same: first a logical explanation, then an example to support it.",
 ]),
], T50),

# ------------------------------------------------------------------ 6. what is expected of me, part 2 (seg04)
lesson('vr50-a-expect2', 'What Is Expected: The Rest', SB_EXPECT2, [
 dict(mode='title', title='What Is Expected: The Rest', script=[
  "We continue with the same essay: the rebuttal paragraph and the closing paragraph.",
  "Then: what standard is actually expected of you.",
 ]),
 dict(mode='concept', active=0, title='Rebuttal paragraph', script=[
  "Now we're in the rebuttal paragraph: the opposing view, and our answer to it.",
  A('The rebuttal paragraph appears', T(P_REBUT, size=31, x=410, y=60, w=1140)),
  "On the other hand, some argue the cameras would violate privacy. The database would know where people are, without their consent.",
  "Unlike apps, where each person chooses the permissions.",
  "At first glance, this seems very reasonable. However, in the age of smartphones, the privacy argument largely does not hold.",
  "Phone companies know where your phone is at every moment. And many people keep their phones with them everywhere.",
 ]),
 dict(mode='concept', active=1, title='Why a rebuttal', script=[
  L('Show critical thinking', 'The goal: show critical thinking', 110, 42),
  "Why write this paragraph? To show critical thinking.",
  L('Know the other side', 'Show that you know the other side, and see its strengths', 200, 38),
  "We show that we know there is another side. That we understand its advantages, or our own weak spots.",
  L('And deal with it', 'And that you can deal with it', 290, 38),
  "And that we can deal with it.",
  L('Not enough', '✗ "Yes, there is another side, but I still prefer mine."', 380, 36),
  "It's not enough to say: yes, there's another side, but I want mine. That does very little.",
  L('What is needed', '✓ We weighed their arguments, and our advantages still outweigh the disadvantages', 470, 36),
  "We need to show that we took their arguments into account, and still decided that in our position, the advantages outweigh the disadvantages.",
 ]),
 dict(mode='concept', active=2, title='Their block', script=[
  L('Their main argument', 'Their main argument: privacy. Tracking us without our consent', 110, 38),
  "First, I present their main argument: privacy. They could track us all the time, without our consent.",
  L('A block', 'Then a "block": "unlike apps, where each person chooses the permissions"', 210, 38),
  "And look: the writer even gives the other side a block against our answer, before we give it.",
  "The other side says: I know you'll answer that apps track us anyway. But with apps, I choose the permissions.",
  L('Fair to them', 'We present the other side at its strongest, not as a straw man', 330, 38),
  "That's a nice touch. The other side isn't naive either. It blocks us before we even start.",
  "And that's where our creativity and critical thinking come in.",
 ]),
 dict(mode='concept', active=3, title='Our answer', script=[
  L('Concede', '"At first glance, this argument seems very reasonable."', 100, 38),
  "First we admit: at first glance, it makes sense. With apps I choose, with cameras I don't.",
  L('However', '"However, ... the privacy argument largely does not hold in this case."', 190, 38),
  "However, in the age of smartphones and social media, the privacy argument largely does not hold.",
  L('Break the block', 'Answer the block: phone companies know where the phone is, and that cannot be switched off', 290, 36),
  "And now we answer their block directly. Even if you deny permissions to apps, the phone company knows where your phone is.",
  "Location services on or off, it doesn't matter. And if they know where my phone is, they practically know where I am.",
  L('"in practice"', '"in practice" = not just in theory', 420, 38),
  "In practice, there is already constant tracking of a large part of the population. That's a weakening, an answer that weakens their argument. This kind is called: the argument does not hold. Saying 'not true' is risky, but here we show why, with a fact. Weakenings get their own lessons later.",
 ]),
 dict(mode='concept', active=4, title='Closing paragraph', script=[
  "And we finish with the closing paragraph.",
  A('The closing paragraph appears', T(P_CLOSE, size=38, x=410, y=80, w=1140)),
  "In conclusion, the cameras would create deterrence and reduce offences.",
  "Moreover, the system would probably make law enforcement more efficient and save resources.",
  L('What it sums up', 'It sums up: my position + my main arguments', 420, 38),
  "What did I sum up? My position, and my main arguments for it. That's all.",
  L('Nothing new', 'No new arguments in the closing', 500, 38),
  "No new claims here. The conclusion follows from what the essay already explained.",
 ]),
 dict(mode='concept', active=5, title='Content: polished', script=[
  L('Content: fairly polished', 'Raters read a first draft: small language slips are forgiven. Content, though, should be fairly polished', 110, 36),
  "Raters know this is a first draft written in 35 minutes, so a small language slip is forgiven. More on that in the proofreading lesson. In content, though, NITE expects something fairly polished.",
  L('Good direction', 'A good direction: clear position, developed explanations', 240, 38),
  "A good direction: a clear position, the development, the explanations.",
  L('Small gaps OK', 'A small gap is fine: an explanation missing a little, no extra example', 330, 36),
  "A small gap is okay. The explanation was fine but missed a little, or you didn't add an example or comparison. Not terrible.",
  L('Big misses are not', 'Missing the task is not a small gap', 440, 40),
  "But missing the task is a different story. We'll see what that looks like in the Relevance lesson.",
 ]),
 dict(mode='concept', active=6, title='What we saw', script=[
  L('Structure', 'Opening paragraph → argument paragraph → argument paragraph → rebuttal paragraph → closing paragraph', 100, 34),
  "So here's what we saw: an opening, two argument paragraphs, a rebuttal paragraph, and a closing.",
  L('Content', 'Content: clear position, developed arguments, several perspectives, dealing with the other side', 220, 34),
  "In content: a clear position, developed arguments, several perspectives, and dealing with the other side.",
  L('Language', 'Language: academic, hedged, precise, a few richer phrases, connectors', 330, 34),
  "In language: academic, hedged, precise, with a few richer phrases and clear connectors.",
  L('Standard', 'Standard: a strong first draft, not a perfect text', 430, 36),
  "And the standard: a strong first draft, not a perfect text.",
  "Now let's start learning how to do all this. See you in the next videos.",
 ]),
], T50),

# ------------------------------------------------------------------ 7. the opening essay (seg05)
lesson('vr50-a-baseline', 'Your Opening Essay', SB_BASE, [
 dict(mode='title', title='Your Opening Essay', script=[
  "Before we learn anything, we want to know where you're starting from.",
  "So now, you'll write your first essay.",
 ]),
 dict(mode='concept', active=0, title='Where you start', script=[
  L('Your starting level', 'Goal: find your starting level in the essay', 110, 42),
  "We want to know your starting point in the essay.",
  L('To see progress', 'So you can see how much you improve during the course', 200, 40),
  "That way you'll be able to see how much you've improved by the end.",
 ]),
 dict(mode='concept', active=1, title='Your task', script=[
  "Here's your task.",
  A('The example task appears', dict(prompt_box(EXAMPLE_PROMPT, EXAMPLE_QUESTION, w=1140), x=410, y=60)),
  "Some cities have let schools move to a four-day school week.",
  "Supporters: a longer weekend for rest and other interests, and savings on transport and heating.",
  "Opponents: longer school days tire young children, and working parents will struggle on the fifth day.",
  "Your question: should schools move to a four-day week? Give reasons.",
 ]),
 dict(mode='concept', active=2, title='The rules', script=[
  L('35 minutes', '35 minutes, with a timer, exactly as in the test', 110, 40),
  "Thirty-five minutes. Set a timer, exactly as in the test.",
  L('By hand, 50 lines', 'By hand, on a 50-line sheet (NITE\'s sample sheet can be printed from its website)', 200, 36),
  "Write by hand, on a 50-line sheet. NITE's website has a sample essay sheet you can print.",
  L('Or typed', 'Typing instead? Keep the same 35 minutes', 310, 36),
  "If you prefer to type it, that's okay. Just keep the same 35 minutes.",
  L('25-50 lines', 'At least 25 lines, at most 50. Count them', 390, 36),
  "At least 25 lines, at most 50. Count your lines at the end.",
 ]),
 dict(mode='concept', active=3, title='No pressure', script=[
  L('No pressure', 'No pressure: you have not learned the method yet', 110, 42),
  "No pressure. Obviously you don't really know how to do this well yet.",
  L('Just write', 'Just write the best essay you can today', 200, 42),
  "That's the point. Just write the best essay you can today.",
  L('Do not study first', 'Do not read ahead first. We want your real starting point', 290, 38),
  "And don't go study first. We want your real starting point.",
 ]),
 dict(mode='concept', active=4, title='Keep it', script=[
  L('Save it', 'Save it, with the date', 110, 42),
  "When you finish, save it, with the date. Don't throw it away.",
  L('Lines count', 'Note how many lines you wrote and how long it took', 200, 38),
  "Write down how many lines you wrote, and whether you finished in time.",
 ]),
 dict(mode='concept', active=5, title='Before and after', script=[
  L('Same task at the end', 'Near the end of the course: the same task again', 110, 42),
  "Toward the end of the course, you'll write an essay on the same task again.",
  L('Compare', 'Compare the two essays side by side', 200, 42),
  "Then put the two essays side by side and see how much you've improved.",
  L('Next', 'Next: we start learning, one skill at a time', 290, 40),
  "That's it for the introduction to the writing task. From the next lesson, we go deeper: what's expected, and how to do it.",
  "As always, I'm waiting for you in the next lesson.",
 ]),
], T50),
]

MEMORY = [
 dict(id='mem-wr-glance', after='vr50-a-score', title='The writing task at a glance',
  intro='The first section of the test: one essay, 35 minutes, 25% of the Verbal Reasoning score.',
  tables=[dict(title='The rules', head=['Rule', 'What it means'], rows=[
    ['Time', '35 minutes: read, plan, write, check'],
    ['Task', 'One given task in a frame; the question is in bold at the end'],
    ['Length', 'At least 25 lines, at most 50 (the answer sheet); good essays: usually about 30-40 lines'],
    ['Too short', '10-23 lines: rated but marked as too short (points deducted); 0-9 lines: disqualified'],
    ['Off-topic', 'Disqualified: the lowest possible score'],
    ['Where to write', 'Only on the lines; anything outside the lines, or after line 50, is not read'],
    ['Scrap paper', 'Pages in the test booklet; the draft is not marked; no extra answer sheet'],
    ['Style', 'Academic, well organized, clear and grammatically correct'],
    ['Tools', 'Pencil (dark enough for the scanner) and eraser; legible, neat handwriting'],
   ]),
   dict(title='The scoring', head=['Step', 'Score'], rows=[
    ['Each of two raters', 'Content 1-6 + language 1-6 = 2-12'],
    ['Essay score', 'The sum of both raters: 4-24'],
    ['Major discrepancy', 'A third, senior rater decides'],
    ['Weight', '25% of Verbal Reasoning (about a tenth of the general score)'],
    ['Standard', 'Rated as a first draft written under time pressure'],
   ]),
   dict(title='The two rubrics', head=['Content rubric', 'Language rubric'], rows=[
    ['Relevance to the task + a clear main idea', 'Clarity + consistency with academic writing'],
    ['Development of the thesis', 'Semantic precision (the exact word)'],
    ['Focus and coherence', 'Grammar'],
    ['Critical thinking: precise definition of the issue, opinion vs fact, several perspectives, answering opposing views', 'Varied sentence structures'],
    ['', 'Organizational tools: connectors, transition sentences, paragraphing (+ richness of vocabulary)'],
   ])],
  tips=['You do not have to persuade: explain why you chose your position. Any position is legitimate.',
        'Aim for 30-40 lines and never fewer than 25.',
        'Stay exactly on the task: an off-topic essay gets the minimum.',
        'Fly under the radar: if you are not sure of a word, use a simpler one you know.']),
]

MODULES = split_task_slides(MODULES)
