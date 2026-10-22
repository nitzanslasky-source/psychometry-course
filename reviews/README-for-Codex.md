# Script review by Codex — before Nitzan records (requested by Nitzan, 15 Oct 2026)

**Goal:** every unrecorded lesson is 100% clear to a WEAK student before she records it. You are the independent reviewer
(Claude writes the scripts; a writer misses its own gaps). **Do not edit the sources** — write findings; Claude fixes them.

## Batches (Reading Studio lesson numbers, live page; re-check numbers if the page is rebuilt)
- **Batch A:** unrecorded lessons of topics 15–20 (#46–49, 67–83 unrecorded ones, 92–94, 111–112, 126–150 unrecorded, 151–160)
- **Batch B:** topics 30–31 (#161–210)
- **Batch C:** topics 32–33 (#211–285)
- **Batch D:** topic 51 (#286–323, all camera)
Get the exact unrecorded list with `cd ~/psychometry-course/studio-build && python3 video_status.py --list record`.
Skip anything she records meanwhile (re-check before writing each lesson's findings).

## What to read for each lesson
- The effective question (current build `~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html`, not bare course18.json)
- The full script as she will read it (`ai_scripts/<id>.json` / Reading Studio prompter text)
- The board: render the step frames (your native renderer is fine) — check what appears when.

## Standard (all in `studio-build/real_exam/TEACHING_STYLE_GUIDE.md`)
Your own 11-point "Codex review standard", plus: Clarity style · W1–W16 (how she reads: 6–12-word sentences, her words) ·
R29–R36 (new idea = full teaching with ≥2 examples + why + trap; reminders short; every method stands alone; calculations
aloud; "choice number N"; exam-level mental math only) · **never teach a new tool in one line (~2 min, in the question)** ·
method vocabulary (The math way / Plugging in numbers / Plugging in the answers / Understanding / Estimation / Insight,
named aloud at each method start) · V3/V4 visuals (math written the moment it's said, no early answers, camera bubble clear,
signature method visuals, "So far" boxes) · study-plan order (nothing used before it's taught) · every Hebrew method kept.

Read each script **as a weak B1 student**: Where would I get lost? Which step jumps? Which "why" is missing? Which sentence
is too long or vague? Which example is missing? Is anything shown before it's said?

## Output — one file per batch: `~/psychometry-course/reviews/batch-<A|B|C|D>.md`
For each lesson: `#<lesson> <video id> — READY` or a list of findings:
`- [must|should|nice] ¶<n> (slide.para): <problem> → <suggested fix>`
- **must** = a student would misunderstand / math or logic error / missing teaching of something new
- **should** = clearly better explanation or visual
- **nice** = polish (Claude parks these in IMPROVEMENTS.md, not now)
Keep findings concrete; quote the sentence. Then mark the batch in COORDINATION.md ("For Claude: batch X review ready").

## Order
A first (she records topics 15–20 next), then B, C, D. Big batches are fine.

## ADDED 15 Oct (Nitzan): pace + "no headlines" — check this in every batch (C, D, and the spot-checks)
- **Pace a student can grasp:** one new idea per sentence; after a key idea there is a beat (short pause / a check
  sentence / an example) before the next one; never two new steps in one breath. Board writing must keep up — if a line
  takes longer to write than to say, the speech needs a short connecting sentence, not a rush.
- **Explains, doesn't speak headlines:** flag telegraphic fragments ("Two cases.", "Step one: the signs.", "Same idea.",
  "Done."), label-like openers, and bare results with no reason. Every step = what we do + why + what it gives.
- Mark these as **should** (or **must** if a weak student would lose the thread).

## ADDED 16 Oct (Nitzan): the Teaching check (TC) — Claude runs it, not part of your review
- After Claude fixes each of your batches, Claude runs **W20 "Teaching check"** (`TEACHING_STYLE_GUIDE.md`) on that batch: at each
  important, reusable concept, does the script TEACH it (general statement, brief why, "when you see … think …", one extra case
  if new) or only use it for this answer? Only strong additions; results in `reviews/teaching-check-<batch>.md`.
- Done for A and B (`teaching-check-A-B.md`). C and D get it after their fixes. You don't need to check this yourself, but if
  you notice a key idea that is only used, never taught, a normal **should** finding is welcome.

## ADDED 19 Oct (Nitzan): batches E and F (and from 20 Oct G = topic 23, H = topic 24, and every new topic) — Codex REVIEWS AND EDITS DIRECTLY
Nitzan asked that Codex fix what it finds itself for **batch E (topic 21)** and **batch F (topic 22)**, instead of a
findings file for Claude. The rest of this brief still applies.

**Her two priorities — this is what the edit is for:**
1. **A student can genuinely follow along.** Read every script as a weak student who sees this topic for the first time:
   no step that jumps, every step says what we do + why (the given behind it, W21) + what it gives; nothing used before
   it's taught (study-plan order); each result written on the board at the moment it's said, never before; one new idea
   per sentence, with a beat after key ideas. If a student would ask "wait, why?" or "where did that come from?", fix it.
2. **Simple English (B1).** Short sentences (6–12 words), everyday words, no idioms or metaphors a learner won't know,
   no long noun chains, no vague "it/this/that" when two things could be meant. Say the same thing the same way every
   time. Keep her voice (phrase bank, "choice number N", numbers as words, no symbols, no labels like "Tip:").

**Scope:** fix **must** and **should** items only — no new methods, no long additions, no rewriting what already works
(videos must not grow much; she reads every word). Keep every method and the method titles. "Nice" ideas → a list at the
end of your report (Claude parks them in IMPROVEMENTS.md).

**Rules:**
- **Claim first** in COORDINATION.md "Doing": files `math_patches/_ai_vis_t21.py` (E) / `_ai_vis_t22.py` (F) and the
  ai_scripts they write. Claude will not touch them until you mark the job Done.
- **Unrecorded lessons only.** Before editing a lesson, check `python3 studio-build/video_status.py --list record` and
  `~/Documents/Course.recordings/_reading/<id>/` (no take). If it's already recorded, don't change its speech — list the
  problem for Nitzan instead.
- Edit the spec only (spoken text in `L(...)`, board items, cues). Every cue phrase must stay a substring of its line.
  Regenerate: `python3 studio-build/math_patches/_ai_vis_t21.py` (or t22) → no PROBLEMS.
- Don't edit shared files (`_ai_visual.py`, `_method_visuals.py`, `_camera_parts.py`, `reading_studio.py`, the display
  registry json, other topics, the guide). Prompter display problems → "Needs Claude" in your report as
  "spoken text → wanted display".
- **Checks before Done:** private build only (`OUT=<your work dir>/test.html python3 build_verbal.py`; never write the
  shared Downloads studio), `SRC=<it> python3 ai_check.py <ids>` all OK, `python3 math_check.py 21` (22) 0/0 and layout 0,
  also with `AI_HANDWRITE=all`; look at the step frames of every slide you changed (handwriting build).
- **Report:** `reviews/batch-E-edited.md` / `batch-F-edited.md`: per lesson READY or each change as before → after (just
  the changed sentences / board items), then "Needs Claude" and "Nice". Mark the job Done in COORDINATION.md and post
  "For Claude: batch E/F edited". Claude then rebuilds the Reading Studio, spot-checks, and handles "Needs Claude".

## ADDED 22 Oct (Nitzan): acceptance standard — required before `--ready`
Clarity and read-aloud usability are required acceptance checks, not polish (guide W25). Check every reviewed script sentence by sentence against the board: explicit introductions of new questions/examples/methods; every step = what we find + what the quantities mean + why + what it tells us; simple spoken English with clear pauses; readable prompter maths; no ambiguous "this/that/it"; no unexplained jumps; her methods and exam terms preserved. Maths and automated checks passing does not make a lesson ready. Mark ready only after this independent explanation/transition review: `python3 studio-build/video_status.py --ready <ids> --by Codex --why "…"`.
