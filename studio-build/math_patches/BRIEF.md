# Math course fixes — brief for one topic (teacher-approved: nothing is recorded yet, so videos may change freely)

You own ONE topic N. Write `math_patches/tNN.py` (two digits, e.g. t05.py) defining `apply(M)`, plus
`math_patches/tNN_CHANGES.md` (plain-language changelog for the teacher). Edit no other file. If the API
(`math_api.py`, read its docstring) is missing something, work around it inside your patch and mention it in the changelog.

## Inputs
- Review of your topic: `student_review/review_t*.md` (find the file that covers N) and `student_review/PLAN.md`.
- What the student sees now: `student_review/tN.md` (figures in `student_review/fig/*.png`).
- Check tool (run often): `python3 math_check.py N` -> PROBLEMS must be 0, LAYOUT problems must be 0, and every WARNING
  must be fixed or be a genuine exception (real ratio, etc.). It also writes the patched student view to
  `tmp_check/view/tN.md` — read it at the end as a student. Render slides to look at them:
  `SRC=tmp_check/check-N.html python3 render.py tmp_check/tN-<name>.png <videoId> ...` then open the PNG.

## What to do (in this order)
1. **Wrong rules** in videos/boards/cards (review + PLAN priority 1): correct the slide's spoken lines, board items and
   memory cards so every statement is mathematically true, keeping the teacher's voice.
2. **Missing methods** (priority 2): for every method/rule/question type the review says is used but never taught, or
   missing for the exam: add it where it belongs - new slides inside the right lesson video (`M.insert_slides`), or a
   short new lesson video (`M.new_video`, kind='lesson') for a larger block. Each added method gets at least one
   guided question with a solution video (`M.new_q` + `M.place_q` + `M.new_video(kind='solution', qid=...)`) and
   2–4 practice questions. Update the memory card(s). Fix "used before taught" inside the topic by teaching it or
   moving the question. Where the review asks for strong-student tricks (plug in numbers, work back from the answers,
   estimation, elimination, special values), teach them explicitly.
3. **Text** (priority 3) - EVERY question of the topic (guided and practice) and every video:
   - Math in `$TeX$`: fractions `\frac{a}{b}`, division `\div` or a fraction bar. **Never ":" for division** (only a
     real ratio may use ":", and then say "ratio"). Plain-text stems/choices/solutions like "(a+b):a" become proper TeX.
   - **Several given equations/conditions go one on top of the other** (teacher's rule): in a stem use
     `Given:\n$\begin{cases} x+y=7 \\ x-y=3 \end{cases}$\nWhat is ...?` (`\n` = line break, works on slides and site).
     Same in solutions and on the board (`T('$\begin{cases}...\end{cases}$')`), and in teacher "Write ..." notes.
   - Space after every comma; no "so" meaning "therefore" mid-sentence ("So, ..." or "therefore"); no typos; no
     self-corrections left in solutions; hyphens in words, not "−" (three-digit, not three−digit).
   - Teacher draw notes (`D('Write "12 : 2 = 6"')`) use ÷ or fractions, not ":".
   - Reword ambiguous questions the review lists; make every solution show the numbers (no words-only solutions) and
     use the method the lesson taught (mention a faster one after it if useful).
   - Unclear conditions like "0 < x, y" -> "x > 0 and y > 0".
4. **Figures** (priority 4, geometry and any figure): remove giveaways (don't draw what the question asks to find,
   don't label the answer), fix misleading drawings and labels, make figures match what the teacher says.
   Question figure = `M.q(id)['questionVisual']['svg']` (set with `M.set_q(id, figure=new_svg)`); slide figure =
   an item `{'k':'vis','v':{'svg':...}}` in `M.slide(vid, n)['items']`. Keep the existing SVG style (colors, fonts,
   viewBox). Render to check: `qlmanage -t -s 640 -o tmp_check file.svg`.
5. **Practice** (priority 5): remove near-duplicates (`M.unplace(qid)`), order each practice section easy -> hard
   (`M.practice_order`), and add exam-hard questions for strong students so each topic has at least 6–10 exam-level
   items (new ids). Keep the total practice size roughly the same or larger.

## Style
- Match the existing videos: short spoken lines, one idea per line, direct and warm ("Here's the trap."), a board item
  appears (A(...)) right before the teacher talks about it. Concept slides: `mode='concept'`, `active` = sidebar index;
  add sidebar labels with `M.set_sidebar` when you add slides. Keep slide titles short.
- New ids: questions `q-r26-tNN-01`, `q-r26-tNN-02`...; videos `r26-tNN-<short-name>`; guided solution video id
  `solve-q-r26-tNN-01`; cards `mem-r26-tNN-<name>`. Guided question title slide: `'Question %d' % M.next_question_number(N)`
  (call it again for each new one - it counts the ones you already added).
- English for learners: short sentences, American spelling, no idioms.
- Questions must look like NITE multiple choice: 4 choices, one correct, plausible distractors built on real mistakes.

## Correctness (mandatory)
- Solve every new or changed question yourself from scratch; exactly one correct choice; the key and the solution
  video ("Circle choice N", "Choice N") must agree. Double-check every statement you add to a video.
- Run `python3 math_check.py N` until clean; look at rendered PNGs of every new or changed slide.

## Report (final message, short)
Counts (questions rewritten / added / removed, slides changed / added, videos added, figures fixed), the new methods
added, anything you could not do, and anything the teacher should decide. Put the full list in tNN_CHANGES.md.
