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
| Codex | 23 Oct resumed | **Video production queue: current-source audio/visual checks, then checked exports** | First unfinished ready drafts:solve-q-r26-t22-20,wp-039,solve-wp22-g039; workspace ready-all-2026-10-21, then fresh Send queue | No script edits; recheck latest takes/visuals per lesson; low storage, sequential workers |
| Claude | 23 Oct | **Write topic 27 (motion)** — next topic in plan order; new unrecorded batch, all its lessons Held until Codex reviews | `math_patches/_ai_vis_t27.py`, `t27.py` hook, ai_scripts t27, `summary_pages/t27.json` | — |
| Claude (another session) | 22 Oct (assigned by Nitzan) | **Review topics 23 and 24 for clarity** | `math_patches/_ai_vis_t23.py`, `_ai_vis_t24.py` — mostly recorded now: proposals only for recorded lessons | must claim here before starting |

## Handoffs (open)
- **For Claude: topic35 edited/reviewed — DONE,23Oct.** Priorities (Hebrew restores,33/51) finished first. All24 topic35 scripts independently checked sentence-by-sentence against boards, spoken read-through and every prompter paragraph. **21 now Ready/frozen**:geo-119/-2/-3,geo-120/-2/-3,r26-t35-water,solve-q-r26-t35-01/02/03,solve-geo35-g122/g123/g124/g126/g127/g128/g129/g130/g131/g132,r26-t35-cubefacts. **Three unchanged/Held:**solve-geo35-g121(pi),solve-geo35-g125(choices),r26-t35-cones(keep decision). Thirteen narrative clarifications, scope/definition corrections and board alignment; retained all methods, examples, numbers and choices. Summary clarified; existing g123/g126 display entries verified, hook/display registry unchanged for35. Checks:all24ai_check OK both modes;math35 0/0/layout93slides701items0 BOTH;566 rendered step states,0failures;all final boards and key changed intermediate states personally inspected. Final takes rechecked:all24 unrecorded at release. Studios/summary published with backups; same556 ordered ReadingIDs; guarded diff only13 videos,no question changes. Report `reviews/codex-topic35-w25-2026-10-23.txt`. Do not reassemble from an old scratchpad. Writing guidance: state the conditions of a rule (right prism,two bases,no spill); explain why a midpoint/cancellation follows; introduce a,b,c before showing them; root of the SUM of squares, not ambiguous “edges squared.” Earlier topic35 claim and all-Held handoff below are superseded by this completion. Preserve the seven33/51 decision holds listed below.
  → **Acknowledged by Claude, 23 Oct:** the 21 released topic-35 lessons are frozen; Codex's version is the source (no reassembly); the three Held (g121 π, g125 choices, r26-t35-cones) wait for Nitzan; the writing guidance is now in guide W24. Handoff closed.
- **For Claude: priority Hebrew restores and topics33/51 edited/reviewed, 23 Oct.** First13 plus58 further lessons released (71 approvals this job; some may now be recorded). Remaining33: only `solve-geo33-g089` Held for π. Remaining51: `solve-pt-q02-2`, `pt51-plug-answers`, `solve-pt-q07/08/09` Held for round-choice decision; `solve-pt-q18` Held for measurement decision. All other handed-off unrecorded33/51 lessons passed sentence/board/read-through/prompter review and are frozen. Five circle narration clarifications, four51 narration/wording fixes, five51 board-only fixes; `pt-q06` now correctly asks which value COULD fit (−3 and−4 both satisfy, only−4 is in choices). Full methods kept. Nine per-ID prompter fixes, no formatter/pipeline change. Final checks: circle math0/0/layout195slides1712items0 BOTH;51 layouts145slides1026items0 BOTH; ai_check31+34 allOK BOTH; all final boards personally inspected, changed states rechecked. Studios published; same556 ordered Reading IDs; guarded diff only14 videos/one question. Report `reviews/codex-held-w25-2026-10-23.txt`, exact released IDs in workspace `publication-priority.json`. **Codex now owns topic35; do not edit it meanwhile. Three topic35 decisions untouched.** Older “remaining33/51 Held” wording below superseded by this handoff.
  → **Acknowledged by Claude, 23 Oct:** released versions preserved; the seven decision holds (g089, pt-q02-2, pt51-plug-answers, pt-q07/08/09, pt-q18) stay with Nitzan. Handoff closed.

## Waiting for Nitzan
- **Decisions** (`~/Downloads/Hebrew-vs-English-check.md`, section D): measuring the figure (pt-q18, g114); "the round answer is usually right" (holds pt-q02-2, pt51-plug-answers, pt-q07/08/09); g138 tip (topic 36); π ≈ 3.14 in g089 **and g121**.
- **Topic 35 decisions** (`~/Downloads/Topic-35-AI-scripts-review.md`): g125 non-box choices; keep `r26-t35-cones` (no real exam item)?
- **Recorded-lesson proposals** (record only if approved): the percent-equation patch for wp-053 (`reviews/t23-hebrew-restore.md`); q-552 early-stop shortcut; g040 "no order distractor" (joins its re-read); parity "0 is even" (joins its re-read); "open/closed" → "between/outside" in absolute-value-3, q-360, q-361; wp-027-3 "absolute value, a topic we'll learn later" → a short reminder; q-r26-t15-01 "tag" → "complete groups of seven plus the remainder". Full list: `~/Downloads/Hebrew-vs-English-check.md` (section C).
- **Files:** Hebrew subtitles for the topic 9 roots lesson and the 8th advanced inequalities question (topic 12).

## Links
Guide: `studio-build/real_exam/TEACHING_STYLE_GUIDE.md` · Codex review brief: `reviews/README-for-Codex.md` · Optional ideas: `IMPROVEMENTS.md` · History: `COORDINATION-archive-2026-10.md`
