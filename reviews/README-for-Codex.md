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
