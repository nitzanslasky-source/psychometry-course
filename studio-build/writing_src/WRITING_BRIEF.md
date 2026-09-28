# Writing Task (Verbal topic 50): build English lesson videos from the teacher's Hebrew course

The teacher asked for English writing-task lessons that are **clear and good**. On these slides it is fine to be much
wordier than elsewhere (templates, full example paragraphs, checklists on screen). Work in
`/Users/nitzanslasky/psychometry-course/studio-build`. You write ONE file: `modulesV50<letter>.py` (letter given in your
task). Do not edit any other file (tell the lead if a shared file needs a change).

## Sources (read the ones for your part fully before writing)
1. `writing_src/segNN.txt` - the teacher's Hebrew lesson subtitles (auto-transcribed, so some words are garbled). Your
   segments are given in your task; `writing_src/INDEX.txt` lists all 51 so you know what comes before/after you.
   **This is the backbone: every idea, method, template, example and tip in your segments goes in** (teacher's rule:
   everything from the Hebrew course stays). Keep the teacher's order, voice (direct, warm, practical, "you") and
   running examples.
2. `nite_verbal_guide.txt` (official NITE English guide; writing task = the part about the writing task and the two
   scoring tables). **The official English facts override the Hebrew where they differ**:
   - 35 minutes (the Hebrew course may say 30); the essay is 25% of the Verbal Reasoning score.
   - At least 25 lines, no more than 50 (the lines of the answer sheet); good essays are usually about 30-40 lines.
   - 10-23 lines: rated but flagged as too short; 0-9 lines, off-topic, or illegible: the lowest score.
   - Two raters; each gives content 1-6 and language 1-6; the essay score is the sum (range 4-24 - check the guide's
     exact wording before stating how it is combined, and state only what the guide says).
   - Raters know it is a first draft written under time pressure.
   - Content criteria: relevance to the task and main idea, development of ideas, focus and coherence, critical thinking
     (precise definition of the issue, distinguishing opinion from fact, several perspectives, dealing with opposing views).
   - Language criteria: clarity and academic style, precise vocabulary, correct grammar, varied sentence structures,
     organizational tools (connectors, transitions, paragraphing).
   - Avoid: personal/emotional/narrative style, rhetorical questions, flowery or needlessly difficult language,
     incorrect or made-up information.
   - Check the guide for anything else about the English/combined test (e.g. which languages the essay may be written in)
     and use its exact facts.
3. `writing_src/findings.md` - what the official strong / adequate / weak English sample essays show (ChatGPT study).
   Use its lessons where they fit your part. **Never name, quote or retell a real exam task or real sample essay**
   (NITE material may not be copied) - turn each lesson into an original example.

## Adapting the Hebrew to English
- The Hebrew "language" lessons (Hebrew Academy rules, Hebrew syntax, Hebrew punctuation, Hebrew connectors, Hebrew
  register) become their **English equivalents**: formal academic English (no contractions, no slang, no "you" in the
  essay, no rhetorical questions), hedging/qualified claims (may, tends to, in many cases), precise word choice (and
  the same term throughout for the same thing), grammar that changes meaning (subject-verb agreement, tense,
  articles, pronoun reference, run-ons and fragments, missing negatives), sentence variety and punctuation (commas
  after introductory phrases, semicolons, no comma splices), English connectors grouped by relationship (cause,
  result, contrast, concession, condition, example, addition, conclusion), paragraphing, richness without flowery
  language. Keep the teacher's structure and teaching points; swap the Hebrew-specific examples for English ones
  that make the same point. Common Hebrew-speaker errors in English are very welcome (e.g. "the people think",
  "discuss about", "In my opinion I think", missing articles, "according to me").
- The teacher's running Hebrew examples (e.g. face-recognition cameras in public spaces, reduced tax for large
  companies) are the teacher's own - translate and keep them. Any NEW example you need must be original, neutral,
  everyday-policy style (schools, cities, workplaces, health, transport, technology). Do NOT use working from home as
  an example anywhere (teacher's request).
- Terms to use consistently across all parts (so the lessons match each other):
  opening paragraph · argument paragraph · key sentence (the paragraph's first sentence: position + reason) ·
  development · support (example / comparison / studies-general knowledge) · the chain · weakening (החלשה) ·
  rebuttal paragraph (פסקת עימות: the opposing view + our answer) · bridging recommendation (המלצה מגשרת) ·
  closing paragraph · essay skeleton (שלד) · proofreading · the content rubric / the language rubric ·
  zoom out / zoom in (keep the teacher's names for techniques).
- No Hebrew characters anywhere in the output. Hebrew words the teacher uses become English terms.

## The chain (teacher's own method - lead writes it into part E; others refer to it where natural)
The teacher's method: for every argument, before writing, draft a cause->effect chain of short steps (~10 words per
argument) from the thing the task asks about to the final result; then "paste" the chain into the paragraph with a
template, so nothing is skipped and the writer doesn't get lost. Agreed refinements: (1) test every arrow - "why
would this step lead to the next?"; a weak arrow needs an explanation or a condition; (2) no arrows that just rename
the same thing; (3) the paragraph must not sound pasted - vary the connectors (because, which in turn, as a result,
this means that, and once ..., ...); (4) use it for the other side too: write the opponent's chain, find the weakest
arrow - that is the weakening / rebuttal.

## Slide format (Python, `from dsl import *`)
```python
from dsl import *
from writing_assets import TASK_PAGE, ANSWER_SHEET, task_page, prompt_box, EXAMPLE_PROMPT, EXAMPLE_QUESTION
T50 = 50
MODULES = [
lesson('vr50-<slug>', 'Lesson title', ['Sidebar 1', 'Sidebar 2', ...], [
  dict(mode='title', title='Lesson title', script=["spoken line", ...]),
  dict(mode='concept', active=0, title='Sidebar 1', script=[
     "spoken line",
     A("short label appears", T('On-screen text', size=40, x=410, y=110, w=1140)),
     "spoken line", D("teacher underlines ...")]),
  ...], T50),
]
MEMORY = [dict(id='mem-wr-<slug>', after='vr50-<slug>', title='...', intro='...',
               tables=[dict(title='...', head=['...', '...'], rows=[[..], ..])], tips=['...'])]
```
- Board: 1600x900; the content area is x=410..1550 (w up to 1140), y=30..880. Place items with explicit x/y/w; stack
  them so nothing overlaps. Wordy is OK: size 30-34 for paragraphs/templates, 38-46 for key statements. Long
  example paragraphs: one per slide, size ~28-30, w=1140.
- Sidebar: max 13 labels, each <= 22 characters; concept slide `title` must equal its sidebar label, `active` = index.
- A lesson = one video, about 4-12 concept slides. Split big segments into several lessons if that is clearer.
- Figures: `A('The exam page appears', dict(TASK_PAGE, x=380, y=40, w=660, h=684))` (portrait page, viewBox 600x622; text can go to its
  right at x=1060, w=480); `ANSWER_SHEET` is 600x780: use e.g. x=400, y=20, w=640, h=832; `A('The task appears', dict(prompt_box(lines, question), x=410,
  y=60))` for a boxed task (landscape, w=1000 default). `task_page(lines, question)` makes a page with another
  original prompt (lines ~70 chars each).
- Spoken lines: short sentences, the teacher's voice, English only. Each A(...) is announced/explained by the
  spoken lines around it.
- Memory cards: 1-2 per file, compact reference tables (templates, connectors, checklists). A card with
  `section='vr50-practice'` goes to the practice section instead of after its video.

## Checks (all must pass; run them yourself)
1. `python3 validate_v.py` - 0 problems for your file.
2. Test build into your own file (never the shared output):
   `OUT=$PWD/tmp_check/w50/<letter>.html VMODS=modulesV50<letter> python3 build_verbal.py`
3. `python3 layoutcheck.py tmp_check/w50/<letter>.html vr50-` - 0 problems.
4. `SRC=tmp_check/w50/<letter>.html python3 render.py tmp_check/w50/<letter>-<lesson>.png <video ids>` and LOOK at the
   PNGs: readable, nothing cramped, nothing overlapping, nothing cut off.
5. `python3 -c "import re,sys;s=open(sys.argv[1]).read();print(re.findall('[\u0590-\u05FF]+',s)[:5])" modulesV50<letter>.py` - must print [] (no Hebrew).

Final message (short): lessons made (id, title, number of slides), cards, which segments/ideas went where, anything
from your segments you left out and why (should be nothing), anything you need from the lead.
