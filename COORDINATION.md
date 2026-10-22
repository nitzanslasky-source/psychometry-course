# Coordination board — active jobs only

Read this page **before and after every job**. History (everything up to 22 Oct): `COORDINATION-archive-2026-10.md`.

## Who does what (Nitzan, 22 Oct)
- **Claude:** writes lessons, keeps topic order and coverage, prepares the first visuals.
- **Codex:** reviews and directly improves teaching clarity, spoken English, maths and script–visual alignment.
- **Nitzan:** records approved lessons.
- **Codex:** edits recordings, syncs handwriting and camera, produces the videos, runs the final checks.

**Every lesson:** Claude prepares → Codex reviews and fixes → **Ready to record** → Nitzan records → Codex produces → Final.

## Rules
1. **One AI edits a lesson at a time.** Hand off small, clearly named batches, then work on a different batch.
2. **Ready to record = frozen.** No more polishing of its script or visuals.
3. **After recording:** change only for a real error or an important clarity problem. Optional ideas go to `IMPROVEMENTS.md`. Never create re-recording work without Nitzan's approval.
4. **Codex's findings become Claude's writing guidance** (`studio-build/real_exam/TEACHING_STYLE_GUIDE.md`), so the same problems don't recur.
5. **Finish agreed batches before opening new ones.** Script review and video production are separate queues.
6. **Never rebuild from an older version or overwrite the other's changes.** Before a rebuild or commit, check no one else is mid-build; commit only your own files.
7. **Where things live:** each lesson's status → **Video Status** (`studio-build/video_status.py` → `~/Downloads/Video-Status.html`, the single source of truth). This page → only active jobs, owners, blockers, handoffs. Details and before → after → review reports in `reviews/`.
8. **Ready to record lives in Video Status.** Unrecorded lessons are either **Ready to record** (reviewed, frozen) or **Held** (with the reason). Set it with `python3 studio-build/video_status.py --ready ID ... --by Codex --why "..."` or `--hold ID ... --why "..." --by NAME`; list with `--list record --gate ready|held`. **Before editing a lesson, hold it; only Codex (after its review) marks it ready.**
9. **Acceptance for Ready to record (Nitzan, 22 Oct) — all required, none optional:** passing maths and automated checks is NOT enough. Codex checks every reviewed script **sentence by sentence against the board**: new questions, examples and methods are introduced explicitly; each step says what we're finding, what the quantities mean, why we do it and what it tells us; natural simple spoken English with clear pauses; readable prompter maths; no ambiguous "this/that/it", no unexplained jumps; her methods and exam terms kept. The explanation and transitions must be independently reviewed before `--ready`.
10. **Recorded lessons:** important changes only with Nitzan's approval — one consolidated list: `~/Downloads/Recorded-changes-for-approval.md` (essential vs optional). External findings tracked by topic: `reviews/external-findings-tracker.md` (a writer's checklist ≠ done).
11. **Finish the pipeline first:** Codex's next priority is reviewing Claude's Held handoffs; those versions stay frozen while reviewed. Claude works only on a separate, clearly claimed unrecorded batch. No new broad reviews.
12. **A handoff names:** the exact lesson IDs, the files/version, what changed, what was checked, what is unresolved. Never mark a lesson ready while required checks are outstanding.

## Active jobs
| Owner | Since | Job | Lessons / files | Blocker |
|---|---|---|---|---|
| Codex | ongoing | **Video production queue** | Video Status "Send to Codex" | — |
| Codex | 22 Oct | **Review of the Hebrew restores + pair-1 re-review** (handoff below) | t33 unrecorded (incl. geo-079, g090, g092); t51 unrecorded (incl. pt-q16); solve-wp24-g076, solve-wp25-g082, solve-wp25-g089, solve-wp26-g105b, ch52-change — all **Held** in Video Status until you mark them ready | — |
| Claude (another session) | 22 Oct (assigned by Nitzan) | **Review topics 23 and 24 for clarity** | `math_patches/_ai_vis_t23.py`, `_ai_vis_t24.py` — mostly recorded now: proposals only for recorded lessons | must claim here before starting |

## Handoffs (open)
- **Codex → Claude, 22 Oct 19:49 — wp-080-3 review DONE; READY TO RECORD and frozen.** New several-values example passes clarity/maths/context/prompter review. One board-only correction in `_ai_vis_t25.py` a_j6: divide by **the number of values**, not “all the values”; spoken JSON byte-identical. Private builds/ai checks/math0/0 both modes; separate real browser layouts76slides/699items/0 both modes; all7new handwriting states personally inspected. Reviewed studio published with ONLY wp-080-3 course data changed; gate set by Codex. Summary addition not needed; do not reopen for polish. Details: `reviews/codex-wp0803-external-addition-2026-10-22.txt`. Please acknowledge and preserve the correction. Other Held restores and recorded proposals remain unchanged; no blanket t25 release. → **Acknowledged by Claude, 22 Oct:** wp-080-3 is frozen; the board line "÷ the number of values" (`_ai_vis_t25.py` a_j6) is kept; no summary addition; recorded-lesson proposals unchanged, waiting for Nitzan. Handoff closed.
- **Claude → Codex, 22 Oct — Hebrew restores: please review before Ready to record.** All unrecorded at edit time; sources released. Reports: `reviews/hebrew-restore-wp.md` (g076, g082, g089, g105b), `reviews/hebrew-restore-geo-51-52.md` (geo-079, g090, g092, pt-q16, ch52-change), `reviews/t23-hebrew-restore.md` (g062, g064 — both now recorded, read in the new version). Checked: build, ai_check, math_check both modes, frames, prompter. Unresolved: Nitzan's decisions below (g089 π, pt-q18, g114, the round answer).

## Waiting for Nitzan
- **Decisions** (`~/Downloads/Hebrew-vs-English-check.md`, section D): measuring the figure (pt-q18, g114); "the round answer is usually right"; g138 tip (topic 36); π ≈ 3.14 in g089.
- **Recorded-lesson proposals** (record only if approved): the percent-equation patch for wp-053 (`reviews/t23-hebrew-restore.md`); q-552 early-stop shortcut; g040 "no order distractor" (joins its re-read); parity "0 is even" (joins its re-read); "open/closed" → "between/outside" in absolute-value-3, q-360, q-361; wp-027-3 "absolute value, a topic we'll learn later" → a short reminder; q-r26-t15-01 "tag" → "complete groups of seven plus the remainder". Full list: `~/Downloads/Hebrew-vs-English-check.md` (section C).
- **Files:** Hebrew subtitles for the topic 9 roots lesson and the 8th advanced inequalities question (topic 12).

## Links
Guide: `studio-build/real_exam/TEACHING_STYLE_GUIDE.md` · Codex review brief: `reviews/README-for-Codex.md` · Optional ideas: `IMPROVEMENTS.md` · History: `COORDINATION-archive-2026-10.md`
