# Audit: were the math additions justified by the real exam? (REPORT ONLY - edit nothing)

Teacher's rule: everything that came from the original Hebrew course stays, no discussion. Only what the 2026-09 fixers
ADDED is in question: an added topic / rule / question type must appear on the real NITE exam, or it is removed
(no "shrinking" - keep or remove). A solving method / trick / shortcut stays if it helps solve question types that
really appear on the exam.

Inputs
- What was added: `math_patches/tNN_CHANGES.md` (and `math_patches/tNN.py` for details) for your topics.
- The real exam: `real_exam/quant_real.md` - all 760 questions of 19 official English NITE quantitative sections
  (2019-2026), grouped by subtopic, with answers. Search it (grep/python) by keywords and by reading the relevant
  subtopic groups fully.

For each of your topics, list EVERY addition (new lesson video, new slide teaching something new, new guided question,
new practice question type, new rule on a card) and classify it:
- FIX - a correction or clarification of something already in the course (wrong rule, wording, notation, figure,
  order). Always kept; list briefly.
- METHOD - a solving technique/shortcut (plug in numbers, work back from answers, estimate, a formula shortcut).
  KEEP if you can point to real questions it helps solve (give 1-3 real ids). Otherwise REMOVE.
- CONTENT - new material/question type the original course did not teach (e.g. geometric probability, map scale,
  line equations). KEEP only if real questions of that type exist (give ids and a count). Otherwise REMOVE.
- UNSURE - you can't decide; say why.
Practice/guided questions added by the fixers: judge by their TYPE (a question testing removed content is removed too).

Write `real_exam/audit_tNN.md` per topic: a table | Addition | Where (video id / slide / question ids) | Class |
Verdict | Evidence (real question ids / count) |, then a short list "TO REMOVE" with the exact ids (videos, slides by
video+title, questions, card rows) so the removal can be done mechanically. Be strict and honest: a vague resemblance is
not evidence. Final message: per topic, counts of KEEP / REMOVE / UNSURE and the REMOVE items in one line each.
