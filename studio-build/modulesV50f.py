# Verbal Reasoning · Topic 50 · Writing task · Part F: the argument paragraph.
# Sources: writing_src/seg29-seg35 (teacher's Hebrew lessons: intro to the argument paragraph, the key sentence,
# developing the argument, supporting it, support by example, support by comparison, citing studies), the teacher's
# chain method (WRITING_BRIEF.md), the official NITE guide (nite_verbal_guide.txt) and writing_src/findings.md.
# Running examples: the teacher's face-recognition cameras and criminal-record examples; the course's four-day
# school week task (writing_assets.EXAMPLE_PROMPT); new neutral examples (free city buses, phones in lessons,
# street trees, calorie counts on menus, plastic bags). No real exam task or sample essay is used.
from dsl import *
from writing_assets import vis, _wrap
from xml.sax.saxutils import escape as _e

T50 = 50

# ---------------------------------------------------------------- figure: a chain drawn as boxes and arrows
_FONT = "Inter, 'Segoe UI', Arial, sans-serif"
_INK = '#17233c'; _ACC = '#2F6BFF'; _OK = '#15803d'; _WEAK = '#b45309'; _BAD = '#dc2626'; _BOX = '#eef3ff'


def _tx(x, y, s, size, color=_INK, weight=500):
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" font-weight="%d" fill="%s">%s</text>'
            % (x, y, _FONT, size, weight, color, _e(s)))


def chain_fig(steps, notes=None, size=23, box_w=None, W=1140, y0=110):
    """steps: short step texts (top to bottom). notes: one per arrow, (kind, text) with kind 'ok' | 'weak' | 'bad', or None.
    Without notes the boxes are wide; with notes the arrow tests are written to the right of each arrow."""
    size = size * 1.22
    bw = box_w or (540 if notes else 860)
    cpl = int(bw / (size * 0.53))
    ncpl = int((W - bw - 60) / (size * 0.86 * 0.53))
    lh = size * 1.25
    b, y = [], 4
    for i, s in enumerate(steps):
        ls = _wrap(s, cpl)
        h = len(ls) * lh + 18
        b.append('<rect x="2" y="%g" width="%g" height="%g" rx="12" fill="%s" stroke="%s" stroke-width="2"/>'
                 % (y, bw, h, _BOX, _ACC))
        for j, l in enumerate(ls):
            b.append(_tx(18, y + 9 + size + j * lh - 3, l, size, _INK, 600))
        y += h
        if i < len(steps) - 1:
            note = notes[i] if notes else None
            nls = _wrap(note[1], ncpl) if note else []
            gap = max(46, len(nls) * size * 0.86 * 1.2 + 14)
            cx = bw / 2
            b.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="4"/>' % (cx, y + 4, cx, y + gap - 12, _ACC))
            b.append('<path d="M %g %g l -10 -14 l 20 0 Z" fill="%s"/>' % (cx, y + gap - 2, _ACC))
            if note:
                col = {'ok': _OK, 'weak': _WEAK, 'bad': _BAD}[note[0]]
                ny = y + gap / 2 - (len(nls) - 1) * size * 0.86 * 0.6 + size * 0.3
                b.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="2" stroke-dasharray="5 5"/>'
                         % (cx + 16, y + gap / 2, bw + 30, y + gap / 2, col))
                for j, l in enumerate(nls):
                    b.append(_tx(bw + 40, ny + j * size * 0.86 * 1.2, l, size * 0.86, col, 700 if j == 0 else 500))
            y += gap
    H = int(y + 6)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="Argument chain"><title>Argument chain</title>%s</svg>'
           % (W, H, ''.join(b)))
    d = vis(svg, w=W, h=H); d['x'] = 410; d['y'] = y0
    return d


def t(txt, y, size=32, x=410, w=1140):
    return T(txt, size=size, x=x, y=y, w=w)


# ---------------------------------------------------------------- shared texts
CAM_KEY = ("In my opinion, face-recognition cameras should be installed in public spaces, "
           "since they would deter offenders and reduce crime in these areas.")

MODULES = [
# ================================================================== 1 · introduction to the argument paragraph (seg29)
lesson('vr50-f-argument-intro', 'The Argument Paragraph',
       ['Goal for the essay', 'Goal for the rater',
        'The first argument', 'Strongest first', 'Three components', 'Key sentence', 'Development', 'Support'], [
 dict(mode='title', title='The Argument Paragraph', script=[
  "The argument paragraph.",
  "We're starting a series of lessons that are all about one paragraph: the argument paragraph.",
  "It's the heart of your essay. This is where you actually argue for your position.",
  "Before we write a single word, let's understand the goal of this paragraph. Once you know what it's for, you know what to put in it.",
 ]),
 dict(mode='concept', active=0, title='Goal for the essay', script=[
  "I'm going to split the goal into two.",
  A("Two goals appears", t("The argument paragraph has two goals:\n(1) for the essay  ·  (2) for the rater", 110, 40)),
  "First, the goal from the essay's point of view. I'm writing an essay. What's this paragraph for?",
  A("Goal 1 appears", t("For the essay: present the first argument for your position", 260, 40)),
  "To present the first argument for my position. Simple.",
  "If all we had to do was write an essay, that would be the whole story.",
  A("But: we get a score appears", t("But this is an exam essay. Someone gives it a score.", 400, 36)),
  "But we're not just writing an essay. We're writing an exam essay, and we get a score for it.",
  "So there's a second kind of goal: the goal from the rater's point of view.",
 ]),
 dict(mode='concept', active=1, title='Goal for the rater', script=[
  A("Official scoring appears", t("Officially: two raters. Each gives content 1-6 and language 1-6.", 110, 34)),
  "Quick reminder of the official scoring. Two raters read your essay. Each one gives a content score from one to six and a language score from one to six.",
  A("Goal 2 appears", t("For the rater: in the first argument paragraph I want the rater to\n"
                        "(a) form a first CONTENT impression of me, as high as possible\n"
                        "(b) keep, or even raise, the LANGUAGE impression from the opening", 230, 34)),
  "In the first argument paragraph, my goal is for the rater to form a first content impression of me. As high as possible.",
  "And to keep, or even raise, the language impression they already formed in the opening paragraph.",
  "Why impressions? Experienced raters form a picture of the score while they read, paragraph by paragraph. The opening mostly shows your language; we'll see why in the opening paragraph lesson.",
 ]),
 dict(mode='concept', active=2, title='The first argument', script=[
  "Now the rater moves to the first argument paragraph.",
  A("First content impression appears", t("First argument paragraph = the FIRST time the rater sees your content.\nStrong argument or weak? Real development? Solid support?", 110, 34)),
  "This is the first time they meet your content. They read the argument and think: strong argument, or weak? Great development, or thin? Solid support, or not?",
  "Here I set a first, tentative content score in their head. And of course, I want it as high as possible.",
  A("Keep the language up appears", t("Language: keep the level, or pull it up a little: a precise phrase, a varied sentence.", 330, 34)),
  "And on language, I try to keep the level, or pull it up a bit. Another precise phrase, a well-built sentence.",
  "As if to say: in the opening I didn't have room to show you what I can do. Here I do.",
  "Of course, I don't write 'my vocabulary is amazing'. I show it, quietly, in the sentences themselves.",
 ]),
 dict(mode='concept', active=3, title='Strongest first', script=[
  A("Strongest argument first appears", t("So: your STRONGEST argument goes in the first argument paragraph", 110, 42)),
  "And that's exactly why the first argument paragraph gets our strongest argument.",
  A("Strongest = appears", t("Strongest = the one you can develop and support best", 250, 38)),
  "Strongest doesn't mean the most dramatic. It means the one you know how to develop and support best.",
  A("Two first impressions appears", t("Opening paragraph → first impression of your language\nFirst argument paragraph → first impression of your content", 380, 34)),
  "The first impression of your language was created in the opening. Here, you create the first impression of your content.",
 ]),
 dict(mode='concept', active=4, title='Three components', script=[
  "So what is an argument paragraph made of?",
  A("Component 1 appears", t("1 · Key sentence: the argument in short: position + reason", 110, 36)),
  "First, the key sentence. The argument in a nutshell: my position, and the reason for it.",
  A("Component 2 appears", t("2 · Development: explain it logically, step by step", 210, 36)),
  "Second, development. Explaining the argument with logic, step by step.",
  A("Component 3 appears", t("3 · Support: strengthen it, show that it holds in practice", 310, 36)),
  "Third, support. Strengthening it. Showing it's actually true.",
  "Let's take each one in a sentence now. Each gets its own lesson.",
 ]),
 dict(mode='concept', active=5, title='Key sentence', script=[
  A("Key sentence template appears", t("In my opinion, [we should / should not do X], because it will lead to [a benefit / a harm].", 110, 36)),
  "The key sentence has a template. In my opinion, we should, or should not, do something, because it will lead to some benefit, or some harm.",
  A("Camera example appears", t("In my opinion, face-recognition cameras should be installed in public spaces, because they would deter offenders and reduce crime.", 280, 34)),
  "For example, the running example we'll use: face-recognition cameras in public spaces.",
  "In my opinion, they should be installed, because they would deter offenders and reduce crime.",
  A("= my opinion appears", t("This is my opinion. Now I have to explain it and back it up.", 450, 34)),
  "That's my opinion. That's what I think. Now I need to develop it and support it.",
 ]),
 dict(mode='concept', active=6, title='Development', script=[
  A("Development = logic appears", t("Development = explaining with logic: a chain of steps\nA leads to B, B leads to C, C leads to D → the result", 110, 36)),
  "Development means explaining with logic. A chain of steps: A leads to B, which leads to C, which leads to D. And finally I reach my result. The chain gets its own lesson soon.",
  A("Camera development appears", t("If cameras are installed in public spaces → offenders will know the cameras are there → they will be deterred → fewer crimes in these areas", 290, 34)),
  "If cameras are installed, offenders will know they're there. That knowledge deters them. And that reduces crime in these areas.",
  "Something leads to something, which leads to something. Logically.",
 ]),
 dict(mode='concept', active=7, title='Support', script=[
  A("Support = proof appears", t("Support = strengthening: showing the explanation is true, not only logical", 110, 36)),
  "After I've explained my key sentence with logic, I want to support it.",
  "Support means strengthening. As if to say: I explained it, you understood it. Now let me show you it's true.",
  A("Explained → now show appears", t("Development: 'Here is why it makes sense.'\nSupport: 'Here is how it works in practice.'", 260, 36)),
  "The explanation isn't always enough. So: let me show you.",
  "How do we do that? Soon, in the support lessons. First, the key sentence.",
 ]),
], T50),

# ================================================================== 2 · the key sentence (seg30)
lesson('vr50-f-key-sentence', 'The Key Sentence',
       ['The template', 'Part 1: the answer', 'Part 2: the reason', 'First draft', 'What to fix', 'Rewrite 1',
        'Rewrite 2', 'Rewrite 3', 'Summary'], [
 dict(mode='title', title='The Key Sentence', script=[
  "The key sentence.",
  "The first sentence of every argument paragraph. Let's see how to write it, and then how to raise it.",
 ]),
 dict(mode='concept', active=0, title='The template', script=[
  "The key sentence has a very simple template.",
  A("Template appears", t("In my opinion, [X] should / should not [...],\nbecause it will lead to [a benefit / a harm].", 120, 42)),
  "In my opinion, something should, or should not, be done. Because it will lead to some benefit, or some harm.",
  A("Two parts appears", t("Part 1: the answer to the question  ·  Part 2: the reason", 330, 36)),
  "Two parts. Let's look at each one.",
 ]),
 dict(mode='concept', active=1, title='Part 1: the answer', script=[
  A("Part 1 appears", t("Part 1 answers the task's question: should we, or shouldn't we?", 110, 38)),
  "The first part simply answers the question in the task. Should we, or shouldn't we?",
  A("Example part 1 appears", t("In my opinion, face-recognition cameras should be installed in public spaces ...", 260, 34)),
  "In my opinion, face-recognition cameras should be installed in public spaces.",
  "That's it. A clear answer. Yes or no.",
 ]),
 dict(mode='concept', active=2, title='Part 2: the reason', script=[
  A("Part 2 appears", t("Part 2 gives the reason: a benefit (if you are for) or a harm (if you are against)", 110, 38)),
  "The second part gives the reason. A benefit, or a harm.",
  A("Example part 2 appears", t("... because they will deter criminals and help keep residents safe.", 290, 34)),
  "Here it's a benefit: they will deter criminals and help keep residents safe.",
  "Answer, plus reason. That's a key sentence.",
 ]),
 dict(mode='concept', active=3, title='First draft', script=[
  "Now here's a typical first draft. Look at it for a moment.",
  A("Draft appears", t("In my opinion, we should install face-recognition cameras in public spaces because it will deter criminals and helping keep the residents safe.", 110, 36)),
  "It's clear. You understand what the writer means.",
  "But it's not written at a high enough level yet. And it has a few small errors. Mostly errors of style, and one of grammar.",
  "We want to rewrite it and raise it a bit.",
 ]),
 dict(mode='concept', active=4, title='What to fix', script=[
  A("Fix 1 appears", t("'we should install'  →  who is 'we'? Make the policy the subject: 'cameras should be installed'", 110, 32)),
  "One. 'We should install'. Who is 'we'? In an academic essay, the subject is the policy, not us. Cameras should be installed.",
  A("Fix 2 appears", t("'it will deter'  →  'it' = the cameras? They are plural: 'they will deter'", 230, 32)),
  "Two. 'It will deter'. What is 'it'? The cameras? Then it's 'they'. A pronoun must point clearly to one thing.",
  A("Fix 3 appears", t("'will deter ... and helping'  →  keep the same form: 'will deter ... and help'", 350, 32)),
  "Three. 'Will deter and helping'. The two verbs must match. Deter and help. Keep the forms the same.",
  "I told you: consistency. Same form for parallel parts.",
  A("Fix 4 appears", t("'the residents'  →  'residents' (or 'the public'): no 'the' for people in general", 470, 32)),
  "Four. 'The residents'. We mean residents in general, so no 'the'. A classic error for Hebrew speakers.",
  A("Fix 5 appears", t("'because'  →  fine; 'since' or 'as' is a little more formal", 590, 32)),
  "And five, a small one. 'Because' is perfectly fine. 'Since' is a little more formal, if you want to raise it a notch.",
 ]),
 dict(mode='concept', active=5, title='Rewrite 1', script=[
  "Here's a light rewrite. We didn't change much, just fixed the style.",
  A("Rewrite 1 appears", t("In my opinion, face-recognition cameras should be installed in public spaces, since they would deter criminals and help keep residents safe.", 110, 36)),
  A("Rewrite 1 notes appears", t("✓ the policy is the subject   ✓ 'they' matches 'cameras'   ✓ 'deter ... and help'   ✓ 'since'", 330, 30)),
  "The policy is the subject. 'They' matches cameras. Deter and help, same form. And since instead of because.",
  "A small rewrite. Nothing dramatic. Just correct and a little higher.",
 ]),
 dict(mode='concept', active=6, title='Rewrite 2', script=[
  "Now a more significant rewrite.",
  A("Rewrite 2 appears", t("In my opinion, operating face-recognition cameras in public spaces would strengthen deterrence and thus, in practice, reduce harm to people and their property in these areas.", 110, 34)),
  A("Note: hedged verbs appears", t("'strengthen', 'reduce': not 'will cause'. Measured words show critical thinking.", 330, 32)),
  "Look at the verbs: strengthen, reduce. Not 'will cause'.",
  "Will the cameras create deterrence out of nothing? Maybe not. It's not black and white. They strengthen deterrence. They reduce harm.",
  "Measured words like these show critical thinking. Prefer them.",
  A("Note: in practice appears", t("'in practice': a useful, precise phrase", 450, 32)),
  "I also added a phrase: in practice.",
  A("Note: harm to appears", t("Hebrew-speaker trap: 'harm of people' / 'damage for property'  →  'harm to people and their property'", 540, 32)),
  "And watch the preposition. Harm TO people. Not harm of people, not damage for property. Harm to people and their property.",
 ]),
 dict(mode='concept', active=7, title='Rewrite 3', script=[
  "And one more rewrite. Here we really turn the sentence around, but keep the same meaning.",
  A("Rewrite 3 appears", t("In my opinion, operating face-recognition cameras in public spaces would prevent harm to people and their property in these areas, or at the very least reduce it significantly, owing to the deterrent effect of public awareness that the cameras exist.", 110, 32)),
  A("Note: at the very least appears", t("'would prevent ..., or at the very least reduce it': it may not stop all crime, but it will reduce it = critical thinking", 380, 32)),
  "'Would prevent harm, or at the very least reduce it significantly.'",
  "This way of writing shows critical thinking. I'm saying: it may not prevent everything. But even if it doesn't, it will at least reduce it.",
  A("Note: nouns appears", t("'the deterrent effect of public awareness'  →  nouns (deterrence, awareness) suit academic writing", 520, 32)),
  "And notice: the deterrent effect, public awareness. Nouns, not 'so that people know and get scared'. That's the language of academic writing.",
 ]),
 dict(mode='concept', active=8, title='Summary', script=[
  "So let's sum up the key sentence.",
  A("Step 1 appears", t("Step 1: write it simply and logically:\nIn my opinion, [should / should not ...], because it will lead to [benefit / harm].", 110, 36)),
  "First, write it in this simple form. Answer the question. Give the reason. Logical and clear.",
  A("Step 2 appears", t("Step 2: rewrite and raise it:\nthe policy as the subject · consistent forms · clear pronouns · measured verbs (reduce, strengthen, at the very least) · precise prepositions", 330, 34)),
  "Then rewrite and raise it. The policy as the subject. Consistent forms. Clear pronouns. Measured verbs. Precise prepositions.",
  "That's the first part: the key sentence. Next, development: explaining it. See you there.",
 ]),
], T50),

# ================================================================== 3 · developing the argument (seg31)
lesson('vr50-f-development', 'Developing the Argument',
       ['What development is', 'Make it vertical', 'What does it cause?', 'Explain every step', 'Worked: key sentence',
        'Worked: the links', 'Worked: rough draft', 'Polish: fact or guess', 'Polish: enrich', 'The polished version',
        'Explain a sentence', 'Explain an expression', 'Not every sentence'], [
 dict(mode='title', title='Developing the Argument', script=[
  "Developing the argument.",
  "In the last lesson we wrote the key sentence: I'm for or against something, because it will lead to a benefit or a harm.",
  "Now we explain it.",
 ]),
 dict(mode='concept', active=0, title='What development is', script=[
  A("Development appears", t("Development = explaining the argument with logic, step by step:\nhow your position leads to the benefit or harm you predict", 110, 38)),
  "In development, we explain our argument with logic. Step by step.",
  "How does choosing for or against bring us to the benefit or harm we predict?",
  A("This leads to this appears", t("Position  →  this leads to that  →  which leads to that  →  benefit / harm", 330, 36)),
  "I chose a side. That leads to this, which leads to this, which leads to this. And there's my result.",
 ]),
 dict(mode='concept', active=1, title='Make it vertical', script=[
  "Here's the trick. Take the key sentence and turn it vertical.",
  A("Vertical figure appears", chain_fig(["First link: the first part of the key sentence (the policy)",
                                          "... middle links: you add these ...",
                                          "Last link: the second part of the key sentence (the benefit / harm)"], size=26)),
  "The first part of the key sentence goes at the top. It's the first link.",
  "The last part, the benefit or the harm, goes at the bottom. It's the last link.",
  "And your job is to fill in the links in between.",
 ]),
 dict(mode='concept', active=2, title='What does it cause?', script=[
  "How do you fill in the links? With one question, again and again.",
  A("The question appears", t("'And what does that lead to?'", 110, 48)),
  "And what does that lead to? This. And what does that lead to? This. And what does that lead to?",
  "Oh, I've reached my result. The benefit, or the harm.",
  A("Repeat until appears", t("Ask it again and again, until you reach the last link: your benefit or harm.", 250, 36)),
 ]),
 dict(mode='concept', active=3, title='Explain every step', script=[
  "A few notes.",
  A("Note 1 appears", t("Explain EVERY step. Nothing is obvious.", 110, 42)),
  "We have to explain all the steps. Nothing is self-evident.",
  "True, the rater would probably understand what you meant even if you skipped a link. 'This leads to this, and from here I get to my benefit.'",
  A("Note 2 appears", t("The rater is not checking whether they understand you.\nThey check whether the argument is built and explained fully.", 220, 34)),
  "But that's not what they're checking. They don't check whether they understand you. They check whether your argument is built and explained in full.",
  A("Child test appears", t("The test: would a child, who does not draw conclusions on their own, follow you from the first link to the last?", 380, 34)),
  "Imagine a child reads it. A child who doesn't fill in gaps on their own. Would they understand how you got from the first link to the last?",
  A("Note 3 appears", t("Add suitable linking words between the parts. And you can enrich the paragraph (rewriting, explaining).", 540, 32)),
  "Of course, add suitable linking words between the parts. And you can enrich the paragraph. We'll see how soon.",
 ]),
 dict(mode='concept', active=4, title='Worked: key sentence', script=[
  "Let's do it. Here's our key sentence.",
  A("Key sentence appears", t("In my opinion, the security forces should be allowed to install face-recognition cameras in public spaces, since this would reduce crime in the monitored areas.", 110, 34)),
  "Great sentence. Now I want to explain it logically.",
  "I split it in two.",
  A("First link appears", t("First link: the security forces install face-recognition cameras", 330, 34)),
  "The first part, installing the cameras, becomes the first link.",
  A("Last link appears", t("Last link: less crime in the monitored areas", 420, 34)),
  "The second part, less crime, is the benefit. The end. The last link.",
 ]),
 dict(mode='concept', active=5, title='Worked: the links', script=[
  "Now let's add the links in between.",
  A("Chain appears", chain_fig(["The cameras are installed",
                                "Offenders realize that crimes in public spaces are recorded and that the people who commit them can be identified",
                                "Offenders are deterred from committing crimes there",
                                "Less crime in the monitored areas"], size=25)),
  "The cameras are installed. And what does that lead to? Offenders realize that crimes committed in public spaces are recorded, and that they can be identified.",
  "And what does that lead to? They're deterred. They think: wait, they'll catch me there. I'd rather not.",
  "And what does that lead to? Less crime in the monitored areas.",
  "There. I've explained it logically, as a chain. From here, through these links, to my result.",
 ]),
 dict(mode='concept', active=6, title='Worked: rough draft', script=[
  "Actually, we already have a paragraph. I just put the links together, in order.",
  A("Rough paragraph appears", t("In my opinion, the security forces should be allowed to install face-recognition cameras in public spaces, since this would reduce crime in the monitored areas. After the cameras are installed, criminals will understand that they are filmed. This will deter them from committing crimes there. This will reduce crime in the monitored areas.", 110, 32)),
  "Key sentence first. Then the links. Then the last link: the benefit.",
  "It's a full paragraph. But it's not really polished yet. Let's polish it.",
 ]),
 dict(mode='concept', active=7, title='Polish: fact or guess', script=[
  "Let's read. The key sentence: excellent.",
  "Next link. 'After the cameras are installed, criminals will understand that they are filmed.'",
  A("Problem appears", t("'criminals WILL understand'  →  written as a fact. It is a prediction.", 110, 36)),
  "Wait, wait. This is written as a fact. But it's what I think will happen. It's my opinion.",
  "A reasonable opinion. It's likely that after the cameras go up, offenders will realize they're recorded. What else would the cameras be there for? And the authorities would probably announce them, because deterrence is one of the goals.",
  A("Fix appears", t("→ 'offenders are LIKELY TO realize that ...'", 260, 38)),
  "So: offenders are likely to realize.",
  A("Who appears", t("Who installs them? 'Once the security forces install ...' (not a mistake either way, but more precise)", 380, 32)),
  "And who installs the cameras? The security forces. Writing just 'after the cameras are installed' isn't a mistake. But naming who does it is more precise, and it enriches the paragraph.",
 ]),
 dict(mode='concept', active=8, title='Polish: enrich', script=[
  "Sometimes I want to lengthen the paragraph a little, because I'm barely reaching the minimum. And sometimes it simply enriches it: more precise words, a better phrase.",
  A("Real time appears", t("Use the task's key words: '... can be identified IN REAL TIME'", 110, 36)),
  "Not just identified. Identified in real time. If the task stresses a word like that, it matters. Use it.",
  "Why does it matter? If they think the footage is only checked later, an offender might think: fine, I'll wear a hat and sunglasses, no one will know who I was.",
  "But in real time, someone can come and stop them now. That understanding is what deters them.",
  A("These areas appears", t("Avoid repeating 'the monitored areas' → 'these areas'", 260, 36)),
  "Then I avoid repeating 'the monitored areas' again. These areas.",
  A("Real benefit appears", t("Add the real benefit: '... making them safer for the public'", 360, 36)),
  "And one more addition. Fine, it reduces crime. But what's the real benefit? These areas become safer for the public.",
 ]),
 dict(mode='concept', active=9, title='The polished version', script=[
  "And here is the paragraph, polished and a little richer.",
  A("Polished paragraph appears", t("In my opinion, the security forces should be allowed to install face-recognition cameras in public spaces, since this would reduce crime in the monitored areas. Once the security forces install such cameras, offenders are likely to realize that crimes committed in public spaces are recorded and that the people who commit them can be identified in real time. This understanding is likely to deter many of them from committing crimes in the monitored areas. As a result, crime in these areas would decrease, making them safer for the public.", 110, 31)),
  "Same chain. Same logic. But now every link is written as a reasoned prediction, the task's key words are in, and the benefit is spelled out.",
 ]),
 dict(mode='concept', active=10, title='Explain a sentence', script=[
  "Another way to enrich a paragraph: explain one of its sentences.",
  "Here's part of a paragraph on another task: should employers be forbidden to ask job applicants for a criminal record certificate?",
  A("Original appears", t("A ban on asking applicants for a criminal record certificate would mean that hiring decisions are based on professional merit alone, without irrelevant considerations. In this way, former prisoners would be able to find their way back into the workforce.", 110, 31)),
  "I want to expand it. How? I explain the first sentence. What does 'without irrelevant considerations' mean?",
  A("Added explanation appears", t("+ In other words, the law would prevent employers from deciding on the basis of an applicant's past, and would require them to assess the applicant's professional skills objectively, without prejudice.", 380, 31)),
  "In other words, the law would stop employers from judging an applicant by their past, and make them assess professional skills objectively, without prejudice.",
  "Did the rater need this? Probably not. The paragraph was fine without it. But the explanation enriches it.",
  A("Phrases appears", t("In other words, ...  ·  That is, ...  ·  This means that ...", 620, 32)),
  "This technique is wonderful. In other words. That is. This means that.",
 ]),
 dict(mode='concept', active=11, title='Explain an expression', script=[
  "You can also explain an expression, or a word.",
  "You're going to use richer language in the essay anyway. Sometimes it's worth explaining the expression you used. Especially if it's less common, and the rater may not know it.",
  A("Expression appears", t("In my view, the new regulation is likely to become a dead letter", 110, 36)),
  "In my view, the new regulation is likely to become a dead letter. I could stop here.",
  A("Explained appears", t("... a dead letter: a rule that remains valid on paper but is not enforced in practice because of everyday realities.", 250, 34)),
  "But I can enrich it. A dead letter: a rule that is still valid on paper, but in practice is not enforced.",
  "You know the kind of rule I mean. At first it's enforced strictly, fines everywhere. A while later nobody enforces it anymore. It's still written down, but it's dead. A dead letter.",
 ]),
 dict(mode='concept', active=12, title='Not every sentence', script=[
  A("Warning appears", t("Do NOT explain every sentence.\nSaying the same thing again in other words = repetition (padding).", 110, 38)),
  "One warning. Don't do this on every sentence.",
  "Otherwise you're just saying the same thing again in other words. That's repetition. Padding. And the rubric counts it against you.",
  A("Explain what adds appears", t("Explain only where it ADDS something: a precise meaning, a key term, an unusual expression.", 300, 34)),
  "Explain where it adds something. Like 'irrelevant considerations': objectively, professional skills, without prejudice. That's new content, not the same words again.",
  A("Next appears", t("Next: the chain, my method for building the development before you write.", 460, 34)),
  "So that's development. Next, I'll show you my own method for building it: the chain. See you there.",
 ]),
], T50),

# ================================================================== 4 · the chain (teacher's method)
lesson('vr50-f-chain', 'The Chain',
       ['Why draft it', 'About ten words', 'Test every arrow',
        'Weak arrow: fix it', 'No renaming arrows', "Don't sound pasted", 'Linking phrases', 'Chain the other side',
        'Repair a weak chain', 'Summary'], [
 dict(mode='title', title='The Chain', script=[
  "The chain.",
  "This is my own method. It's how I make sure a development never skips a step, and never gets lost.",
 ]),
 dict(mode='concept', active=0, title='Why draft it', script=[
  A("Why appears", t("The chain = the vertical key sentence from the last lesson, as quick notes. Draft it, then 'paste' it into the paragraph.", 110, 38)),
  "A chain is the vertical key sentence from the last lesson, written as quick cause-and-effect notes on your scrap paper: from what the task asks about to your result.",
  "Before you write the paragraph, you draft the chain. Then you paste it into the paragraph, using a template.",
  A("Benefits appears", t("✓ nothing is skipped: every arrow becomes a sentence\n✓ you don't get lost in the middle of the paragraph\n✓ you see at once whether the argument really reaches its result", 270, 34)),
  "Why? Nothing gets skipped, because every arrow turns into a sentence.",
  "You don't get lost in the middle of the paragraph. You always know what the next sentence is.",
  "And you see immediately whether your argument really reaches its result, or has a hole in it.",
 ]),
 dict(mode='concept', active=1, title='About ten words', script=[
  A("Ten words appears", t("About 10 words per argument", 110, 46)),
  "How long is a chain? About ten words per argument.",
  A("Example appears", t("free buses → cheaper than driving → some drivers switch → fewer cars → less traffic", 220, 34)),
  "Like this one. Free buses. Cheaper than driving. Some drivers switch. Fewer cars. Less traffic.",
  A("A guide, not a rule appears", t("A guide, not a limit:\n✗ don't drop a necessary link to keep it short\n✗ don't add links that say nothing new", 350, 34)),
  "Ten words is a guide, not a limit.",
  "Don't drop a link you need, just to keep it short. And don't pad it with links that say nothing new.",
  "Short enough to write in thirty seconds. Complete enough that nothing is missing.",
 ]),
 dict(mode='concept', active=2, title='Test every arrow', script=[
  "Now the four checks. They make the difference between a chain and a good chain.",
  A("Check 1 appears", t("Check 1 · Test every arrow: 'Why would this step lead to the next?'", 110, 40)),
  "Check one. Test every arrow. For every arrow, ask: why would this step lead to the next one?",
  A("Three outcomes appears", t("✓ obvious and sound  →  keep it, explain it in one clause\n~ true only sometimes  →  add a CONDITION\n✗ doesn't follow  →  add the missing step, or drop the argument", 260, 34)),
  "If the answer is obvious and sound, keep it, and explain it in the paragraph.",
  "If it's true only sometimes, add a condition.",
  "And if it doesn't really follow, there's a missing step. Add it. Or, if you can't, this argument isn't strong enough. Choose another one.",
 ]),
 dict(mode='concept', active=3, title='Weak arrow: fix it', script=[
  "Let's test the camera chain.",
  A("Tested chain appears", chain_fig(["Cameras installed",
                                       "Offenders know they are recorded",
                                       "Offenders are deterred",
                                       "Less crime in these areas"],
                                      [('weak', "Only if they know the cameras are there → condition: the public is informed (signs, announcements)"),
                                       ('weak', "Only if being recorded means being caught → explain: identification in real time"),
                                       ('ok', "Holds for these areas → keep the claim to 'these areas'")], size=24)),
  "Cameras installed, so offenders know they're recorded. Always? Only if they know the cameras exist. So I add a condition: the public is informed.",
  "They know, so they're deterred. Why? Only if being recorded means a real chance of being caught. So I explain: identification in real time.",
  "Deterred, so less crime. In these areas, yes. Some may just move elsewhere. So I keep my claim precise: less crime in these areas.",
  "Each weak arrow got an explanation or a condition. Now the chain is solid.",
 ]),
 dict(mode='concept', active=4, title='No renaming arrows', script=[
  A("Check 2 appears", t("Check 2 · No arrows that only rename the same thing", 110, 40)),
  "Check two. No arrows that just rename the same thing.",
  A("Renaming example appears", t("✗ students concentrate → students pay attention → better grades", 220, 36)),
  "Look at this. Students concentrate, so students pay attention. That's not a step. It's the same thing in different words.",
  A("Why bad appears", t("A renaming arrow looks like development, but adds nothing.\nIn the paragraph it becomes repetition, and hides the real missing link.", 330, 34)),
  "An arrow like that looks like development. It adds nothing. In the paragraph it becomes repetition.",
  "Worse, it hides the real gap: how exactly does paying attention lead to better grades?",
  A("Test appears", t("Test: can the second box happen WITHOUT the first? If not, and it says nothing new, merge them.", 510, 34)),
  "A quick test: does the second box say something new, something that could have failed to happen? If not, merge the two boxes.",
 ]),
 dict(mode='concept', active=5, title="Don't sound pasted", script=[
  A("Check 3 appears", t("Check 3 · The paragraph must not sound pasted", 110, 40)),
  "Check three. The paragraph must not sound pasted.",
  A("Pasted appears", t("✗ Cameras are installed. This will make offenders know. This will make them deterred. This will make less crime.", 220, 32)),
  "If you just copy the arrows one after another, it sounds like this. This will, this will, this will. A list, not a paragraph.",
  A("Natural appears", t("✓ Once cameras are installed and the public is informed, offenders are likely to realize that ... This, in turn, is likely to deter many of them ... As a result, crime in these areas would decrease.", 400, 32)),
  "Instead: once cameras are installed. This, in turn. As a result. Vary the connectors. Vary the sentence structure.",
  "And put the explanation of each arrow inside the sentence, with 'because' or 'since'.",
 ]),
 dict(mode='concept', active=6, title='Linking phrases', script=[
  "Here's a set of linking phrases for the arrows. Mix them.",
  A("Linkers appears", t("First step:  Once ..., ...  ·  When ..., ...  ·  If ..., ...\n"
                         "Next step:  This, in turn, ...  ·  As a result, ...  ·  Consequently, ...  ·  This means that ...\n"
                         "Inside a sentence:  ..., which in turn ...  ·  ..., so that ...  ·  ..., leading to ...\n"
                         "Explaining an arrow:  because ...  ·  since ...  ·  as ...\n"
                         "A condition:  as long as ...  ·  provided that ...  ·  if ...", 110, 31)),
  "For the first step: once, when, if.",
  "For the next steps: this, in turn. As a result. Consequently. This means that.",
  "Inside a sentence: which in turn. So that. Leading to.",
  "To explain an arrow: because, since, as. And for a condition: as long as, provided that.",
  A("Warning appears", t("A connector signals a link. It does not create one: 'therefore' does not make a step follow.", 560, 32)),
  "One warning. A connector signals a link. It doesn't create one. Writing 'therefore' doesn't make a step follow. The arrow has to be sound first.",
 ]),
 dict(mode='concept', active=7, title='Chain the other side', script=[
  A("Check 4 appears", t("Check 4 · Chain the other side too", 110, 40)),
  "Check four. Use the chain for the other side too.",
  A("Opponent chain appears", t("Opponent: cameras everywhere → every movement recorded → people feel watched → some avoid lawful gatherings → public life suffers", 210, 34)),
  "Write the opponent's chain, the same way. Cameras everywhere. Every movement recorded. People feel watched. Some avoid lawful gatherings. Public life suffers.",
  A("Weakest arrow appears", t("Find its WEAKEST arrow. That is your weakening, and the heart of your rebuttal paragraph.", 400, 36)),
  "Then find its weakest arrow. That's your weakening. That's the heart of the rebuttal paragraph.",
  A("Later appears", t("We will do this fully in the rebuttal lessons.", 540, 32)),
  "We'll do this properly in the lessons on weakening and the rebuttal paragraph. For now, just remember: chains work on both sides.",
 ]),
 dict(mode='concept', active=8, title='Repair a weak chain', script=[
  "Let's repair a weak chain. The task: should phones be banned during lessons?",
  A("Weak chain appears", t("Weak: ban phones → students concentrate → students pay attention → better grades", 110, 34)),
  "Here's a first draft. Ban phones. Students concentrate. Students pay attention. Better grades.",
  A("Diagnosis appears", t("✗ 'concentrate → pay attention': renaming arrow\n✗ 'ban → concentrate': why? the mechanism is missing\n✗ 'pay attention → better grades': a jump, and stated as certain", 230, 32)),
  "Concentrate, pay attention: a renaming arrow. Ban, so they concentrate: why? The mechanism is missing. And attention straight to better grades: a jump. Stated as a certainty.",
  A("Repaired chain appears", t("Repaired: phones banned in lessons → no notifications, less temptation in class → longer stretches of uninterrupted attention → more of the material understood the first time → learning is likely to improve", 440, 34)),
  "The repair. Phones banned in lessons. So no notifications and less temptation. So longer stretches of uninterrupted attention. So more of the material is understood the first time. So learning is likely to improve.",
  A("What changed appears", t("Mechanism added · renaming removed · the jump filled · the result hedged", 680, 32)),
  "The mechanism is in. The renaming is gone. The jump is filled. And the result is hedged: likely to improve.",
 ]),
 dict(mode='concept', active=9, title='Summary', script=[
  A("Summary appears", t("THE CHAIN\n1 · Draft: from what the task asks about → ... → the final result (about 10 words)\n"
                         "2 · Test every arrow: why would this lead to that? Add an explanation or a condition\n"
                         "3 · No renaming arrows\n4 · Don't sound pasted: vary the connectors\n"
                         "5 · Chain the other side: its weakest arrow = your weakening", 110, 33)),
  "So. Draft the chain, from what the task asks about to the final result. About ten words.",
  "Test every arrow. No renaming arrows. Write it so it doesn't sound pasted. And chain the other side too.",
  "Next, we'll do two more full chains together, from draft to finished paragraph.",
 ]),
], T50),

# ================================================================== 5 · worked chains
lesson('vr50-f-chain-examples', 'Worked Chains',
       ['The routine', '4-day week: draft',
        '4-day week: arrows', '4-day week: paragraph', 'Free buses: draft', 'Free buses: arrows',
        'Free buses: paragraph'], [
 dict(mode='title', title='Worked Chains', script=[
  "Worked chains.",
  "Two topics, two full chains. Each one from the draft, through the arrow tests, to the finished paragraph.",
 ]),
 dict(mode='concept', active=0, title='The routine', script=[
  A("Routine appears", t("Draft the chain  →  test every arrow  →  write the paragraph", 110, 42)),
  "Every time, the same routine. Draft the chain. Test every arrow. Write the paragraph.",
  A("Topics appears", t("1 · A four-day school week (against)\n2 · Free city buses (for)", 260, 36)),
  "The camera chain we already tested in the last lesson. Now: the four-day school week, from our example task, and I'll argue against it. And a new one: should a city make its buses free?",
  "Pause the video whenever you like and try the next step yourself before I show it.",
 ]),
 dict(mode='concept', active=1, title='4-day week: draft', script=[
  "Now our example task: should schools move to a four-day week? I'll argue against.",
  A("Key sentence appears", t("Key sentence: schools should not move to a four-day week, since longer school days are likely to harm young children's learning.", 110, 32)),
  "The key sentence: schools should not move to a four-day week, since longer school days are likely to harm young children's learning.",
  A("Draft chain appears", chain_fig(["Four-day week",
                                      "Longer school days",
                                      "Young children tired in the last lessons",
                                      "Less learned at the end of the day",
                                      "Lower achievement"], size=25, y0=290)),
  "The draft. Four-day week. Longer school days. Young children tired in the last lessons. Less learned at the end of the day. Lower achievement.",
 ]),
 dict(mode='concept', active=2, title='4-day week: arrows', script=[
  "Now test every arrow.",
  A("Tested appears", chain_fig(["Four-day week",
                                 "Longer school days",
                                 "Young children tired in the last lessons",
                                 "Less learned at the end of the day",
                                 "Lower achievement"],
                                [('weak', "Only if the teaching hours stay the same → condition: 'if the hours are kept'"),
                                 ('ok', "Sound, especially for young children: attention drops late in a long day"),
                                 ('ok', "Explain: tired pupils follow and remember less"),
                                 ('weak', "Too strong → hedge: 'over a school year, may lower achievement'")], size=23)),
  "Four days means longer days? Only if the number of teaching hours stays the same. The task itself raises longer days, but I'll state the condition.",
  "Longer days, so tired young children? Sound. Attention drops late in a long day, especially for young children.",
  "Tired, so they learn less? Yes, but I explain it: tired pupils follow and remember less.",
  "Less learned, so lower achievement? Too strong as a certainty. I hedge it: over a school year, it may lower achievement.",
 ]),
 dict(mode='concept', active=3, title='4-day week: paragraph', script=[
  "And the paragraph.",
  A("Paragraph appears", t("In my opinion, schools should not move to a four-day week, since longer school days are likely to harm young children's learning. If the number of teaching hours is kept, fitting them into four days means that each school day becomes considerably longer. Young children in particular find it hard to stay focused for so many hours, so by the last lessons of the day many of them are likely to be tired. Tired pupils follow explanations less closely and remember less of what they are taught, which means that the final hours of each day would be used far less effectively. Over a full school year, this loss may lower children's achievement, the opposite of what a change in the school timetable should do.", 110, 30)),
  "If the number of teaching hours is kept: the condition. Young children in particular: precise. So, which means that: varied links.",
  "And the result is hedged: may lower achievement. Then a short closing link back to the position.",
 ]),
 dict(mode='concept', active=4, title='Free buses: draft', script=[
  "A new task. Should a city make its public buses free of charge? I'll argue for.",
  A("Key sentence appears", t("Key sentence: the city should make its buses free, since this would reduce traffic and air pollution in the city centre.", 110, 32)),
  A("Draft chain appears", chain_fig(["Buses free of charge",
                                      "Bus cheaper than driving",
                                      "Some drivers switch to the bus",
                                      "Fewer cars in the city centre",
                                      "Less traffic and air pollution"], size=25, y0=240)),
  "The draft. Free buses. The bus is cheaper than driving. Some drivers switch. Fewer cars in the centre. Less traffic and pollution.",
 ]),
 dict(mode='concept', active=5, title='Free buses: arrows', script=[
  "Test.",
  A("Tested appears", chain_fig(["Buses free of charge",
                                 "Bus cheaper than driving",
                                 "Some drivers switch to the bus",
                                 "Fewer cars in the city centre",
                                 "Less traffic and air pollution"],
                                [('bad', "Renaming? 'free' already means 'cheaper' → merge into one step"),
                                 ('weak', "Price is not the only reason people drive → condition: frequent, reliable buses"),
                                 ('ok', "Sound: each driver who switches is one car fewer"),
                                 ('ok', "Sound: fewer cars in the same streets → less congestion and exhaust")], size=23)),
  "Free, so cheaper than driving? That's almost a renaming arrow. Free already means cheaper. I merge the two boxes.",
  "Cheaper, so drivers switch? Not automatically. Price isn't the only reason people drive. Condition: the buses must be frequent and reliable.",
  "Switch, so fewer cars? Sound. Fewer cars, so less traffic and pollution? Sound.",
 ]),
 dict(mode='concept', active=6, title='Free buses: paragraph', script=[
  "The paragraph.",
  A("Paragraph appears", t("In my opinion, the city should make its buses free of charge, since this would reduce traffic and air pollution in the city centre. Once travelling by bus costs nothing, it becomes a clearly cheaper option than driving and paying for fuel and parking. Price is not the only reason people choose their car, of course; however, as long as the buses are frequent and reliable, some drivers are likely to leave their cars at home, at least for daily trips into the centre. Each driver who switches means one car fewer on the same crowded streets, which in turn reduces both congestion and exhaust fumes. In this way, free buses would make the city centre easier to move through and healthier to live in.", 110, 30)),
  "The merged step. The condition: as long as the buses are frequent and reliable. And a small concession inside the paragraph: price isn't the only reason.",
  "In this way: the closing link back to the benefit.",
 ]),
], T50),

# ================================================================== 6 · the argument paragraph template
lesson('vr50-f-template', 'Argument Paragraph Template',
       ['Built on the chain', 'The four slots', 'Slot 1: key sentence', 'Slot 2: chain steps', 'Slot 3: support',
        'Slot 4: closing link', 'Template A', 'A filled in', 'Template B', 'B filled in', 'Template C',
        'C filled in', 'Checklist'], [
 dict(mode='title', title='Argument Paragraph Template', script=[
  "The argument paragraph template.",
  "You have a tested chain. Now let's pour it into a paragraph, with a template you can use on any task.",
 ]),
 dict(mode='concept', active=0, title='Built on the chain', script=[
  A("Idea appears", t("Chain on scrap paper  →  template  →  finished paragraph", 110, 42)),
  "The chain is on your scrap paper. The template turns it into a paragraph.",
  A("Mapping appears", t("first box  →  the key sentence (with the last box as the reason)\neach arrow  →  one sentence, with its explanation or condition\nlast box  →  the result, then the closing link", 240, 34)),
  "The first box and the last box make the key sentence. Each arrow becomes a sentence, with its explanation or condition. The last box is the result.",
  "Nothing skipped. Nothing lost.",
 ]),
 dict(mode='concept', active=1, title='The four slots', script=[
  A("Slots appear", t("1 · Key sentence: position + reason\n2 · Chain steps: one sentence per arrow, varied linking phrases\n3 · Support (optional): example or comparison\n4 · Closing link: back to your benefit / harm and your position", 110, 36)),
  "Four slots. The key sentence. The chain steps. Support, which is optional. And the closing link.",
  "Let's see the options for each slot, then three versions of the whole template.",
 ]),
 dict(mode='concept', active=2, title='Slot 1: key sentence', script=[
  A("Options appear", t("In my opinion, [X] should / should not [...], since it would [result].\n"
                        "I believe that [X] should [...], as this is likely to [result].\n"
                        "In my opinion, the main reason to support / oppose [X] is that it would [result].\n"
                        "Second paragraph:  Moreover, in my opinion, ...  ·  In addition, I believe that ...", 110, 34)),
  "Slot one, the key sentence. Some openings to choose from. They all start with in my opinion, or I believe that.",
  "In my opinion, X should, since it would. I believe that X should, as this is likely to. In my opinion, the main reason to support, or oppose, X is that it would lead to this result.",
  "And in the second argument paragraph, add a connector before it: moreover, in my opinion. In addition, I believe that.",
  A("Tip appears", t("Use the SAME wording for X as the task (the exact decision, the exact people).", 450, 32)),
  "Whatever you choose, name X exactly as the task does. The exact decision, the exact people.",
 ]),
 dict(mode='concept', active=3, title='Slot 2: chain steps', script=[
  A("Options appear", t("First step:  Once / When / If [X happens], [first effect].\n"
                        "Explaining it:  ..., because / since / as [reason].\n"
                        "Next step:  This, in turn, [...].  ·  As a result, [...].  ·  Consequently, [...].\n"
                        "Next step:  This means that [...].  ·  ..., which leads to [...].\n"
                        "A condition:  As long as / Provided that [condition], [effect].", 110, 32)),
  "Slot two, the chain steps. One sentence per arrow.",
  "Start with once, when, or if. Explain inside the sentence with because, since, as.",
  "Move on with this, in turn. As a result. Consequently. This means that. Which leads to.",
  "And a condition with as long as, provided that.",
  A("Tip appears", t("Never the same connector twice in a row.", 470, 34)),
 ]),
 dict(mode='concept', active=4, title='Slot 3: support', script=[
  A("Options appear", t("Example:  For example, a [person] who [...] would probably [...].\n"
                        "Example:  For instance, a [typical case] in which [...] is likely to [...].\n"
                        "Comparison:  A similar pattern can be seen in [similar field], where [...].\n"
                        "Comparison:  The same principle applies to [similar field]: [...].", 110, 32)),
  "Slot three, support. It's optional. We'll learn it properly in the next lessons, but here are the openings.",
  "An example: for example, a person who does this would probably do that.",
  "A comparison: a similar pattern can be seen in another field, where this happens.",
  A("Tip appears", t("Never invent studies, statistics or experts. Explain; do not cite.", 420, 34)),
  "And never invent studies or numbers. We'll see why in the last lesson of this series.",
 ]),
 dict(mode='concept', active=5, title='Slot 4: closing link', script=[
  A("Options appear", t("After support:  In the same way, [...].  ·  Similarly, [...].  ·  Just as [...], so [...].\n"
                        "After development only:  In this way, [X] would [result].  ·  Thus, [...].  ·  This is why [...].", 110, 32)),
  "Slot four, the closing link.",
  "After support, it brings the reader back from the example or comparison to your own argument: in the same way, similarly, just as.",
  "Without support, it rounds off the chain: in this way, thus, this is why.",
  A("Tip appears", t("A closing link LINKS: it is not a copy of the key sentence.", 330, 36)),
  "A closing link links. It is not a copy of the key sentence.",
 ]),
 dict(mode='concept', active=6, title='Template A', script=[
  "Template A. Development only. Shorter, and completely enough for a strong paragraph.",
  A("Template A appears", t("[KEY]  In my opinion, [X] should [...], since it would [result].\n"
                            "[STEP 1]  Once [X], [effect 1], because [reason].\n"
                            "[STEP 2]  This, in turn, [effect 2].\n"
                            "[STEP 3]  As a result, [effect 3].\n"
                            "[CLOSE]  In this way, [X] would [result], which is why [position].", 110, 34)),
  "Key. Once. This, in turn. As a result. In this way.",
 ]),
 dict(mode='concept', active=7, title='A filled in', script=[
  "Template A, filled in. A new task: should cities plant many more trees along their streets?",
  A("Chain appears", t("Chain: more street trees → shade on streets and buildings → cooler streets in summer → walking and waiting outdoors less exhausting in the heat", 110, 30)),
  A("Paragraph appears", t("In my opinion, cities should plant many more trees along their streets, since this would make urban summers easier to bear. Once trees line a street, their branches shade both the pavement and the walls of nearby buildings, which would otherwise absorb the sun's heat all day. This, in turn, keeps the street noticeably cooler during the hottest hours. As a result, walking to school or work, or waiting at a bus stop, would become far less exhausting, particularly for older people and young children. In this way, street trees would make the city more pleasant and safer to move around in summer, which is why planting them should be a priority.", 260, 30)),
  "Key sentence. Once trees line a street: step one, with its explanation. This, in turn. As a result, with the people it matters most for. In this way: the closing link.",
 ]),
 dict(mode='concept', active=8, title='Template B', script=[
  "Template B. Development plus support by example.",
  A("Template B appears", t("[KEY]  I believe that [X] should [...], as this is likely to [result].\n"
                            "[STEPS]  When [X], [effect 1]. Consequently, [effect 2], which means that [effect 3].\n"
                            "[EXAMPLE]  For example, a [person] who [...] would probably [...].\n"
                            "[CLOSE]  In the same way, [the example's effect] would apply to [everyone the argument covers].", 110, 33)),
  "Key. When, consequently, which means that. For example. In the same way.",
  "The closing link takes the specific person from the example and widens it back to everyone your argument is about.",
 ]),
 dict(mode='concept', active=9, title='B filled in', script=[
  "Template B, filled in, with our repaired chain: phones banned during lessons.",
  A("Paragraph appears", t("I believe that phones should be banned during lessons, as this is likely to improve students' learning. When phones are put away, students no longer receive notifications during class, and the temptation to check them disappears. Consequently, they can follow the lesson for longer stretches without interruption, which means that more of the material is understood the first time it is taught. For example, a student who would normally glance at a message every few minutes would probably miss parts of a maths explanation each time and struggle with the exercise that follows; without the phone, the same student is far more likely to follow the whole explanation. In the same way, removing this distraction would help most students make better use of lesson time.", 110, 30)),
  "Key. When. Consequently. Which means that. The example: one typical student. Then: in the same way, most students.",
 ]),
 dict(mode='concept', active=10, title='Template C', script=[
  "Template C. Development plus support by comparison.",
  A("Template C appears", t("[KEY]  [X] should [...], because it would [result].\n"
                            "[STEPS]  If [X], [effect 1]. As a result, [effect 2].\n"
                            "[COMPARISON]  A similar pattern can be seen in [similar field], where [...].\n"
                            "[CLOSE]  Just as [...] in [that field], so [X] would [result].", 110, 34)),
  "Key. If, as a result. A similar pattern can be seen in. Just as, so.",
 ]),
 dict(mode='concept', active=11, title='C filled in', script=[
  "Template C, filled in. A new task: should restaurants be required to show the calories of each dish on the menu?",
  A("Paragraph appears", t("Restaurants should be required to show the calories of each dish on their menus, because this would help diners make healthier choices. If the information appears next to each dish, diners who want to eat more healthily no longer have to guess which option is lighter. As a result, they can compare dishes at a glance and choose accordingly. A similar pattern can be seen in supermarkets, where packaged foods carry nutrition labels that allow shoppers to compare products before buying them. Just as these labels support shoppers who care about their diet, so calorie information on menus would support diners who wish to make healthier choices.", 110, 30)),
  "The comparison: nutrition labels on packaged food. A familiar, similar case: information at the moment of choice.",
  "And notice: no numbers, no invented study. Just a comparison anyone can check in the nearest supermarket.",
 ]),
 dict(mode='concept', active=12, title='Checklist', script=[
  A("Checklist appears", t("Before you move on, check your argument paragraph:\n"
                           "☐ The key sentence answers the task's exact question and gives a reason\n"
                           "☐ Every arrow of the chain is a sentence, with its explanation or condition\n"
                           "☐ No renaming steps; no repeated connectors\n"
                           "☐ Predictions are hedged (likely to, would, may), not stated as facts\n"
                           "☐ Support, if any, is plausible and linked back to your argument\n"
                           "☐ No invented studies, statistics or experts", 110, 32)),
  "A checklist for the finished paragraph.",
  "Exact question. Every arrow a sentence. No renaming, no repeated connectors. Hedged predictions. Support linked back. Nothing invented.",
  "Next: support. How to strengthen the argument.",
 ]),
], T50),

# ================================================================== 8 · support by example (seg33)
lesson('vr50-f-example', 'Support by Example',
       ['What support is', 'A specific case', 'Invented but likely', 'Not absurd', 'Key sentence', 'Development',
        'The example', 'The closing link', 'The whole paragraph', 'What it shows'], [
 dict(mode='title', title='Support by Example', script=[
  "Support by example.",
  "First, what support is. Then the first kind: an example.",
 ]),
 dict(mode='concept', active=0, title='What support is', script=[
  A("Definition appears", t("Support = strengthening. 'I explained why it should happen. Now let me show you it does.'", 110, 36)),
  "What is support? A kind of strengthening. Before, we explained why it should happen. Now: let me show you my explanation is right.",
  A("Two options appears", t("Two options:  1 · a specific example (this lesson)   2 · a comparison to a similar field (next lesson)", 250, 34)),
  "There are two options: a specific example, in this lesson, and a comparison to a similar field, in the next one.",
  A("Optional appears", t("Support is OPTIONAL: a key sentence + a full development can already score top marks", 390, 34)),
  "And support is optional. A key sentence and a full, step-by-step development can already score top marks. Support only adds strength.",
 ]),
 dict(mode='concept', active=1, title='A specific case', script=[
  A("Definition appears", t("An example = a specific case that shows what happens, or would happen, if a certain position is chosen", 110, 38)),
  "The example should be a specific case that describes what happens, or will happen, if a certain position is chosen.",
  "Say we decided to install face-recognition cameras. What happens then? I describe some case, and from it I draw a conclusion about my argument: the benefit or harm I claim.",
 ]),
 dict(mode='concept', active=2, title='Invented but likely', script=[
  A("Hypothetical OK appears", t("It does not have to be a real event you know. A hypothetical case is fine:\n'Suppose cameras are installed. A ... who ... would probably ...'", 110, 36)),
  "The example doesn't have to be something real that you know from life. You can describe a hypothetical case.",
  "Suppose this position is chosen. Suppose there are cameras. Then this could happen, and this, and this.",
  A("A story-shaped explanation appears", t("It is really an explanation, told as a story about one typical case.", 300, 36)),
  "It's actually another kind of explanation. Told as a story, as if it happened.",
  A("Label it appears", t("Present it as what WOULD probably happen, never as a real event or a real statistic.", 420, 34)),
  "One important point: present it honestly, as what would probably happen. Not as a real event that you're reporting, and not with made-up numbers.",
 ]),
 dict(mode='concept', active=3, title='Not absurd', script=[
  A("Not absurd appears", t("We invent the case, so it must be LIKELY. No absurd examples.", 110, 40)),
  "Even though we're inventing the example a little, it's important not to invent absurd ones.",
  "I remember a task about whether the state should limit the names parents can give their children.",
  "Many, many students gave as their example some ridiculous name. Something no real parent would ever give their child.",
  A("Why appears", t("An absurd case proves nothing about real people. Choose a case the rater recognizes as realistic.", 280, 36)),
  "That proves nothing. You need realistic examples. A case the rater reads and thinks: yes, that could easily happen.",
 ]),
 dict(mode='concept', active=4, title='Key sentence', script=[
  "Let's see how it's done. Here's the start of a paragraph.",
  A("Key sentence appears", t("In my opinion, making the public aware that cameras are present is likely to create deterrence and reduce harm to people and property in the monitored areas.", 110, 34)),
  "Up to here, my key sentence.",
 ]),
 dict(mode='concept', active=5, title='Development', script=[
  "Now I develop it. Why would it reduce harm to people and property in the monitored areas?",
  A("Development appears", t("A person who knows that the chance of being caught committing an offence is higher in a certain area is likely to commit it elsewhere, if at all. Since the cameras increase the chance of catching offenders, illegal activity in the filmed areas is likely to decrease, and so is the harm to people and their property.", 110, 32)),
  "Someone who knows the chance of being caught is higher in a certain area will probably act somewhere else, if at all.",
  "Since the cameras raise the chance of catching offenders, illegal activity in these areas is likely to fall, and so is the harm to people and property.",
  "Good. I've explained it logically. Now I want to strengthen it: show that it works in practice.",
 ]),
 dict(mode='concept', active=6, title='The example', script=[
  A("Example appears", t("For example, a pickpocket who usually operates in a particular shopping area and notices that cameras have been installed there would probably prefer to move elsewhere, or at least to act far less often, perhaps only at the busiest hours, when the chance of being caught on camera is lower.", 110, 32)),
  "For example, a pickpocket who usually works a certain shopping area, and notices cameras have been installed, would probably prefer to move elsewhere.",
  "Or at least act much less, maybe only at the busiest hours, when the chance of being caught on camera is lower.",
  A("Note appears", t("A specific, realistic case of what may happen if there are cameras.", 400, 32)),
  "We described one specific case that could well happen if there are cameras.",
 ]),
 dict(mode='concept', active=7, title='The closing link', script=[
  "But look. The example is about a pickpocket. My argument is about harm to people too, not only to property.",
  A("Problem appears", t("The example: one pickpocket (property).  The argument: harm to people AND property.", 110, 34)),
  "The example is another case, with its own benefit or harm. So I need to link it back to my argument, to my general benefit. That's the closing link: In the same way, Similarly, Just as ... so ...",
  A("Closing link appears", t("Awareness of the cameras is likely to have a similar effect on those who commit other offences, such as assault or robbery.", 240, 36)),
  "Awareness of the cameras is likely to have a similar effect on people who commit other offences, such as assault or robbery.",
  "With this sentence I show: yes, I talked about one specific case, pickpockets. But I mean every kind of offence. And that brings us back to the benefit of the argument.",
 ]),
 dict(mode='concept', active=8, title='The whole paragraph', script=[
  "And here's the whole paragraph together.",
  A("Paragraph appears", t("In my opinion, making the public aware that cameras are present is likely to create deterrence and reduce harm to people and property in the monitored areas. A person who knows that the chance of being caught committing an offence is higher in a certain area is likely to commit it elsewhere, if at all. Since the cameras increase the chance of catching offenders, illegal activity in the filmed areas is likely to decrease, and so is the harm to people and their property. For example, a pickpocket who usually operates in a particular shopping area and notices that cameras have been installed there would probably prefer to move elsewhere, or at least to act far less often. Awareness of the cameras is likely to have a similar effect on those who commit other offences, such as assault or robbery.", 110, 29)),
  "Key sentence. Development. Example. Closing link.",
 ]),
 dict(mode='concept', active=9, title='What it shows', script=[
  "One last point about examples, and it's about critical thinking.",
  A("Shows how appears", t("An example shows HOW your mechanism works. It does not prove how COMMON it is.", 110, 38)),
  "An example shows how the mechanism works. It doesn't prove how often it happens.",
  A("So appears", t("So: keep the wording measured: 'would probably', 'is likely to'. Never 'all offenders will ...'", 280, 34)),
  "So keep the wording measured. Would probably. Is likely to. Not: all offenders will.",
  A("Explain, don't replace appears", t("The example illustrates the explanation. It never replaces it.", 420, 36)),
  "And the example illustrates the explanation. It never replaces it. The development comes first.",
 ]),
], T50),

# ================================================================== 9 · support by comparison (seg34)
lesson('vr50-f-comparison', 'Support by Comparison',
       ['Another field', 'Similar enough', 'A risky tool', 'The comparison', 'Why it works', 'The closing link',
        'Linking, not repeating'], [
 dict(mode='title', title='Support by Comparison', script=[
  "Support by comparison.",
 ]),
 dict(mode='concept', active=0, title='Another field', script=[
  A("Definition appears", t("A comparison: we compare to another field with characteristics as SIMILAR as possible", 110, 38)),
  "In a comparison, we compare our case to some other field. And we want it to share as many characteristics as possible.",
  "Why? Because it's a kind of analogy. I want to draw a conclusion about our case from the case I'm going to describe.",
 ]),
 dict(mode='concept', active=1, title='Similar enough', script=[
  A("Not identical appears", t("Not identical (it does not have to be cameras and security too) but similar ENOUGH", 110, 36)),
  "It doesn't have to be identical. Not cameras and security again. But it has to be similar enough.",
  A("Objection appears", t("Otherwise: 'That's not comparable. There, many other factors are completely different.'", 250, 36)),
  "Otherwise someone can say: wait, that's not comparable. You're showing me some other field, but you can't compare. There, lots of other factors are different.",
  A("The test appears", t("Ask: is the feature that makes it work THERE also present HERE?", 400, 36)),
  "So ask yourself: is the feature that makes it work there also present here? That's the part of the comparison that has to match.",
 ]),
 dict(mode='concept', active=2, title='A risky tool', script=[
  A("Hard appears", t("A good comparison is NOT easy. It takes high-level critical thinking.", 110, 38)),
  "Finding another field that's truly similar is not easy. It takes very high-level critical thinking.",
  A("Advice appears", t("Not confident? Skip the comparison. Use an example; it is easier and safer.", 250, 38)),
  "So if you don't feel strong at this, don't take the risk. Stay with an example.",
  "An example is easier. You invent a likely story about our own case. In a comparison you also tell a story, but it has to be about a similar field, and sometimes you drift too far.",
 ]),
 dict(mode='concept', active=3, title='The comparison', script=[
  "Here's the same start of the paragraph, the same key sentence and development. Now a comparison.",
  A("Comparison appears", t("For instance, some workplaces make it clear to employees that office computers belong to the company, are intended for work purposes only, and that all activity on them is monitored. This policy creates deterrence: employees tend to limit their personal use of the computers during working hours, since they know that their actions are recorded and that the employer can review their browsing history or messages at any time.", 110, 32)),
  "Here I took a different case. There are workplaces with computers, and the employees know they're not allowed to use them for personal things.",
 ]),
 dict(mode='concept', active=4, title='Why it works', script=[
  A("Without monitoring appears", t("Unmonitored: 'Nobody can see what I do. I'll check my personal messages.'", 110, 36)),
  "If the computers weren't monitored, an employee might think: nobody can catch me, I'll browse and check my personal messages.",
  A("With monitoring appears", t("Monitored and announced: 'They will know. I'd better keep it for work.'", 230, 36)),
  "But once the company tells them: our computers are monitored, activity is recorded, we'll know. Then they think: in that case, I'll probably cut down on personal use at work.",
  A("Shared feature appears", t("The shared feature: people KNOW their actions are recorded → they change their behaviour", 360, 36)),
  "So far this sounds logical, and it's something familiar. And the shared feature is exactly the one our argument needs: people know they're recorded, so they change their behaviour.",
 ]),
 dict(mode='concept', active=5, title='The closing link', script=[
  "But I've been talking about computers and messages. What does that have to do with our cameras?",
  A("Closing link appears", t("In the same way, awareness of the cameras in public spaces is likely to deter offenders from acting in these areas.", 110, 38)),
  "So I link it back with my closing link. In the same way, awareness of the cameras in public spaces is likely to deter offenders from acting in these areas.",
  A("Just as appears", t("Just as employees who know they are monitored limit their personal use,\nso offenders who know they are filmed are likely to limit or avoid their activity.", 300, 34)),
  "Just as employees who know they're monitored cut down, offenders who know certain areas are monitored are likely to cut down, or even stop completely.",
 ]),
 dict(mode='concept', active=6, title='Linking, not repeating', script=[
  "Writing this closing link well is not simple, and I recommend you practise it.",
  A("Bad appears", t("✗ Therefore, I believe that making the public aware of the cameras will create deterrence and reduce harm to people and property.", 110, 34)),
  "There's a danger. Many students write a closing sentence that just repeats. They go back over their whole argument, without actually linking it to the example or the comparison.",
  "That's padding. And that's not the goal.",
  A("Good appears", t("✓ In the same way, ...  /  ✓ Just as the pickpocket ..., so other offenders ...", 310, 34)),
  "The goal is to explain the connection. In the same way. Or, as with the example: just as the pickpocket, so other offenders.",
  A("Test appears", t("Test: does your closing link mention BOTH the support case and your own case?", 450, 34)),
  "A quick test: does your closing link mention both the support case and your own case? If it only repeats your argument, rewrite it.",
 ]),
], T50),

# ================================================================== 10 · studies and general knowledge (seg35)
lesson('vr50-f-studies', 'Studies and General Knowledge',
       ['Why cite a study?', 'The problem', 'The official rule', 'General vs specific', 'They want the why',
        'Chicken and egg', 'Downsides', 'What you may say', 'Honest phrasing',
        'Summary'], [
 dict(mode='title', title='Studies and General Knowledge', script=[
  "Studies and general knowledge.",
  "May I cite studies in the essay? May I invent them? Should I? Let's see.",
 ]),
 dict(mode='concept', active=0, title='Why cite a study?', script=[
  A("Goal appears", t("Why cite a study? To prove the argument: to strengthen the explanation.", 110, 38)),
  "What's the goal when I cite a study in an argument paragraph? I'm trying to prove my argument. To strengthen the explanation.",
  A("Another kind of support appears", t("Support by example  ·  Support by comparison  ·  Support by a study?", 250, 36)),
  "So it's really another kind of support. We learned support by example and by comparison. Maybe also support by a study?",
 ]),
 dict(mode='concept', active=1, title='The problem', script=[
  "What's the problem?",
  A("No studies appears", t("In the exam you have no studies, and no internet.", 110, 38)),
  "In the exam we don't really have studies. We can't stop and search online.",
  A("Two options appears", t("Either you happen to know a real one ... or you are tempted to invent one.", 230, 38)),
  "So either you happen to know a real study. Or you're tempted to invent one.",
  A("Real one? appears", t("A real one?  Maybe there is another study that shows the opposite, and you don't know it.", 370, 34)),
  "And if you know a real one: maybe there's another study showing exactly the opposite, one you don't know about.",
 ]),
 dict(mode='concept', active=2, title='The official rule', script=[
  A("Rule appears", t("The official guide: avoid 'illogical, incorrect or fabricated information'.", 110, 40)),
  "Inventing a study? Here the answer is short, and it comes from the official guide itself.",
  "The guide tells you to avoid illogical, incorrect or fabricated information.",
  A("So appears", t("Invented studies, statistics, percentages, experts, dates, cities = fabricated information. Never.", 260, 36)),
  "An invented study is fabricated information. So is an invented percentage. An invented expert. An invented city where it supposedly worked.",
  "So that question is closed. We don't invent. Ever.",
  "And as you'll see now, even a real study doesn't help you the way you'd think.",
 ]),
 dict(mode='concept', active=3, title='General vs specific', script=[
  "First, a distinction in wording.",
  A("General appears", t("General:  'Studies have shown that ...'", 110, 38)),
  "'Studies have shown that'. That's general. I'm not talking about a specific study.",
  A("Specific appears", t("Specific:  'A recent study conducted in [city] found that ... by [number]%'", 210, 38)),
  "'A recent study conducted in some city found that crime dropped by some percentage.' That's describing a specific study. With a year, a country, a number.",
  A("The trap appears", t("The rater cannot check it, and a precise-sounding study is exactly what the guide calls fabricated information if you made it up.", 360, 34)),
  "The rater isn't going to stop and search for it. And that's exactly the trap: it sounds precise, and if you made it up, it's exactly what the guide means by fabricated information.",
 ]),
 dict(mode='concept', active=4, title='They want the why', script=[
  "But here's the part most students don't realize.",
  A("Cited = must explain appears", t("A cited result is not enough. The rater wants you to explain WHY the result happened.", 110, 38)),
  "Suppose you mention a study: in streets with face-recognition cameras, crime went down. Fine. What the rater wants next is: explain it.",
  "Why did crime go down there? What happened? Now you have to explain the result, with logic.",
  A("= development again appears", t("So you are back to developing: explaining the mechanism with logic.", 280, 36)),
  "In other words, you're back to development. Explaining the mechanism.",
 ]),
 dict(mode='concept', active=5, title='Chicken and egg', script=[
  A("Loop appears", chain_fig(["The study is meant to support my explanation",
                               "But the study itself needs an explanation",
                               "So I explain... the same mechanism I already explained"], size=26)),
  "Wait. The study was supposed to strengthen my explanation. But now I have to explain the study? Chicken and egg.",
  A("Conclusion appears", t("A cited study is just another claim that needs support. It adds nothing to the argument.", 520, 34)),
  "So citing a study doesn't strengthen the argument. It's like making another claim, one that itself needs developing and supporting.",
 ]),
 dict(mode='concept', active=6, title='Downsides', script=[
  A("Minuses appear", t("✗ adds no strength (you must explain it anyway)\n✗ wastes time and may count as padding\n"
                        "✗ signals an escape from explaining\n✗ academic raters dislike 'a study showed' with no source\n"
                        "✗ may be wrong, or invented = fabricated information", 110, 34)),
  "The downsides. It adds no strength, because you must explain it anyway. It wastes time and may count as padding.",
  "It signals an escape from explaining: this writer can't explain, so they cite. Raters come from academia, where 'a study showed' with no source is a no-no.",
  "And the rater may know the field. If it's wrong, or invented, it's fabricated information, which the guide explicitly says to avoid.",
  A("Verdict appears", t("And the upsides? None. From today: no specific studies, no statistics, no invented facts.", 450, 36)),
  "And the upsides? None. So from today, you don't cite specific studies anymore.",
 ]),
 dict(mode='concept', active=7, title='What you may say', script=[
  "So what can you say? Well-established general knowledge.",
  A("OK appears", t("✓ Facts that are true and widely known:\n'Smoking harms health.'  ·  'Regular exercise is good for health.'", 110, 36)),
  "There are things everyone knows were proven. Smoking harms health. Regular exercise is good for health.",
  "That's fine to use. It's a fact today, and you're not inventing anything.",
  A("Not OK appears", t("✗ Your own opinion dressed up as research:\n'Studies have shown that face-recognition cameras cut crime by 50%.'", 290, 36)),
  "But I would never write: studies have shown that face-recognition cameras cut crime by fifty percent. That's my opinion dressed up as research, with a made-up number.",
  A("Rule appears", t("If you are not sure it is true, it does not go in the essay.", 470, 38)),
  "The rule: if you're not sure it's true, it doesn't go in.",
 ]),
 dict(mode='concept', active=8, title='Honest phrasing', script=[
  "And even for real, well-known facts, I prefer a little trick.",
  A("Trick appears", t("Instead of 'Studies have shown that ...'  →  'It is now well known that ...'", 110, 36)),
  "Instead of 'studies have shown', I write: 'it is now well known that'.",
  "What does 'it is now well known' mean? Once it wasn't known. Today it is. How? Because studies were done. I'm saying the same thing, without the word 'studies'.",
  A("Phrases appears", t("For facts you are sure of:  It is now well known that ...  ·  It is generally accepted that ...\n"
                         "For your reasoning:  It is reasonable to expect that ...  ·  This is likely to ..., since ...  ·  In many cases, ...", 260, 32)),
  "For facts you're sure of: it is now well known that. It is generally accepted that.",
  "And for your own reasoning, which is most of the essay: it is reasonable to expect that. This is likely to, since. In many cases.",
  A("Honest appears", t("Honest phrasing: a known fact is stated as a fact; your prediction is stated as a prediction.", 470, 34)),
  "That's honest phrasing. A known fact, stated as a fact. Your prediction, stated as a prediction. The explanation does the work.",
 ]),
 dict(mode='concept', active=9, title='Summary', script=[
  A("Summary appears", t("• Do not cite specific studies: they add nothing and can only hurt\n"
                         "• Never invent studies, statistics, experts or numbers (fabricated information)\n"
                         "• Well-known, true facts are fine: 'It is now well known that ...'\n"
                         "• Your own claims: explain them with logic, and hedge them honestly", 110, 34)),
  "Bottom line. No specific studies. Nothing invented. Well-known true facts, yes, with 'it is now well known'. And your own claims: explain them, and phrase them honestly.",
  "That's the argument paragraph. Next, we deal with the other side: weakening, and the rebuttal paragraph. The part that takes the highest level of critical thinking.",
  "As always, I'm waiting for you there.",
 ]),
], T50),
]

MEMORY = [
 dict(id='mem-wr-chain', after='vr50-f-chain-examples', title='The chain',
      intro='Draft a short cause → effect chain for each argument before you write it, test it, then turn every arrow into a sentence.',
      tables=[
       dict(title='How to draft it', head=['Step', 'What to do'], rows=[
        ['1 · Start', 'The thing the task asks about (the exact policy or change)'],
        ['2 · End', 'The final result: the benefit or harm in your key sentence'],
        ['3 · Middle', "Ask again and again: 'And what does that lead to?'"],
        ['4 · Length', 'About 10 words per argument: a guide, not a limit'],
        ['Example', 'cameras installed → offenders know they are recorded → deterred → less crime in these areas'],
       ]),
       dict(title='The four checks', head=['Check', 'How'], rows=[
        ['Test every arrow', "'Why would this step lead to the next?' Weak arrow → add an explanation or a condition; broken arrow → add the missing step or drop the argument"],
        ['No renaming arrows', "'concentrate → pay attention' is the same thing twice: merge the boxes"],
        ["Don't sound pasted", "Vary connectors and sentence shapes; never 'This will ... This will ...'"],
        ['Chain the other side', "Draft the opponent's chain; its weakest arrow is your weakening"],
       ]),
       dict(title='Linking phrases for the arrows', head=['Job', 'Phrases'], rows=[
        ['First step', 'Once ..., ...  ·  When ..., ...  ·  If ..., ...'],
        ['Next step', 'This, in turn, ...  ·  As a result, ...  ·  Consequently, ...  ·  This means that ...'],
        ['Inside a sentence', '..., which in turn ...  ·  ..., so that ...  ·  ..., leading to ...'],
        ['Explaining an arrow', 'because ...  ·  since ...  ·  as ...'],
        ['A condition', 'as long as ...  ·  provided that ...  ·  if ...'],
       ]),
      ],
      tips=["A connector signals a link; it does not create one. Make the arrow sound first.",
            "Hedge the predictions: is likely to, would, may. Not 'will always'."]),
 dict(id='mem-wr-arg-template', after='vr50-f-template', title='Argument paragraph template',
      intro='Key sentence → chain steps → (support) → closing link. Pick one phrase per slot and vary them.',
      tables=[
       dict(title='The slots', head=['Slot', 'Options'], rows=[
        ['1 · Key sentence', 'In my opinion, [X] should / should not [...], since it would [result].  ·  I believe that [X] should [...], as this is likely to [result].  ·  In my opinion, the main reason to support / oppose [X] is that ...  ·  2nd paragraph: Moreover, in my opinion, ... / In addition, I believe that ...'],
        ['2 · Chain steps', 'Once / When / If [X], [effect], because [reason].  ·  This, in turn, ...  ·  As a result, ...  ·  Consequently, ...  ·  This means that ...  ·  As long as [condition], ...'],
        ['3 · Support (optional)', 'For example, a [person] who [...] would probably [...].  ·  A similar pattern can be seen in [similar field], where [...].'],
        ['4 · Closing link', 'After support: In the same way, ...  ·  Similarly, ...  ·  Just as [...], so [...].  After development only: In this way, ...  ·  Thus, ...  ·  This is why ...'],
       ]),
       dict(title='Three versions', head=['Template', 'Shape'], rows=[
        ['A · Development only', 'KEY · Once ... because ... · This, in turn, ... · As a result, ... · In this way, ...'],
        ['B · With an example', 'KEY · When ... · Consequently, ..., which means that ... · For example, a ... who ... · In the same way, ...'],
        ['C · With a comparison', 'KEY · If ... · As a result, ... · A similar pattern can be seen in ..., where ... · Just as ..., so ...'],
       ]),
      ],
      tips=["The closing link mentions BOTH the support case and your own case; it never just repeats the key sentence.",
            "No invented studies, statistics or experts. Well-known true facts: 'It is now well known that ...'.",
            "Support is optional: key sentence + a fully explained chain can be a top-scoring paragraph."]),
]
