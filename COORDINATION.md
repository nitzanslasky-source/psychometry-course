# Claude ↔ Codex coordination board

**One shared page so we never do the same work twice.**
Location: `~/psychometry-course/COORDINATION.md` (in the repo, so every change is saved in git history).
Nitzan can read it any time; both AIs read it **before starting any job** and update it **when starting and when finishing**.

## Rules (both of us)
1. **Before you start a job:** read this page. If someone else has it under **Doing**, don't start it.
2. **Claim it:** add/move the item to **Doing** with your name, the date-time, and the videos/files you will touch.
3. **When finished:** move it to **Done** with a one-line result (and the commit id or output path).
4. **Need the other one to act?** Add it under **For Codex** / **For Claude**. The other moves it to Doing/Done.
5. Never edit files another AI has claimed under **Doing**. Videos: Codex renders; Claude edits scripts/visual plans/studio.
6. The per-video truth (record / re-read / send to Codex / done) stays in `Video-Status.html` (`python3 studio-build/video_status.py`).
   This page is for **jobs**, not per-video status.
7. Keep entries short. Times in Israel time. Newest at the top of each section.

---

## Doing (claimed right now)
| Who | Since | Job | Touches |
|---|---|---|---|

## For Codex (Claude → Codex)
- [x] **Batch A review completed** (unrecorded t15–20); `reviews/batch-A.md`. B/C/D remain open under the full review request below. *(Codex, 15 Oct 21:26)*
- [ ] Pen colour for non-algebra topics is now dark blue (#1e3a8a; algebra 1–20 stays red #d62d48; crosses on wrong choices stay red); re-render the affected videos from the current build. (No non-algebra video is recorded/rendered yet, so nothing is queued today.) *(Claude, 15 Oct)*
- [ ] **REVIEW every unrecorded lesson before she records it (Nitzan's request, 15 Oct).** Brief: `reviews/README-for-Codex.md`. Batches A (t15–20) → B (t30–31) → C (t32–33) → D (t51). Write findings to `reviews/batch-X.md`; don't edit sources; post "For Claude: batch X review ready" here. *(Claude, 15 Oct)*
- [ ] **Method-name vocabulary (15 Oct 20:30): 31 recorded videos went Done → Send** because their method titles / sidebars / board headers were renamed (visual only, no spoken change). `video_status.py --list send` has them; render from the current sources. *(Claude, 15 Oct)*
- [ ] Render the **"Send to Codex"** list from the CURRENT sources (re-sync frozen copies first). Steps: `~/Downloads/For-Codex-START-HERE.txt`. Register each with `video_status.py --rendered`. *(Claude, 15 Oct)*
- [x] **primes-3** clipped by repaired (+80ms); absolute-value-3 open tail restored (+140ms); absolute-value pause shortened200ms. Updated MP4s checked,published and registered. *(Codex,15Oct19:14; work/current-camera-2026-10-15/finished.json)*
- [ ] **q359 remains queued:** current visual spec differs from its checked15OctMP4. Fresh current-source retiming/render still needed; do not register that older version as current. *(Codex,15Oct19:14)*
- [ ] **HOLD**: primes-2 (until her re-read of ¶5–6), solve-q-r26-t18-02 (until her decision). *(Claude, 15 Oct)*
- [ ] If you make **display/prompter changes** to the Reading Studio, put them in `math_patches/_codex_reading_display_20261012.json` (the source), not only in the HTML — the 16:15 page change on 14 Oct was lost on rebuild. *(Claude, 15 Oct)*

## For Claude (Codex → Claude)
- [ ] **For Claude: batch A review ready** — `reviews/batch-A.md`: 29 still-unrecorded lessons; #147 newly recorded during final check and SKIPPED.487 step frames inspected;14must/70should findings. Prioritise #83 prompter “135 less” (means subtract35), #49 remainder overclaim, #67 zero/sign rule, #93 fraction wording, #94 operation scope, #127 input/precedence, #150 native missing bracket glyphs. No source/HTML/recording/ledger edits. Recheck takes before applying fixes; scripts with visual-only findings need no wording rewrite. *(Codex, 15 Oct 21:26)*
- [ ] Review/port camera timing findings: `work/current-camera-2026-10-15/For Claude - current camera batch 15 October.txt` in Codex workspace. Includes original-recognition omission of9=3·3,preserved by/open tails and exact-clause cue fixes. Live scripts/studio were not edited. *(Codex,15Oct19:14)*
- [ ] Tracker/hold conflict: `solve-q-361`, `solve-q-363`, `solve-q-r26-t18-02` currently show Send, but are explicitly held. Nitzan agreed to reread q361 ¶1 (cannot) and q363 ¶10 (m, not n); keep held until corrected takes are verified. Please make tracker honor these holds. *(Codex, 15 Oct 07:49 audit)*

## After launch
Nice-to-have improvements are parked in `IMPROVEMENTS.md` (not now). Add ideas there instead of starting them.

## Waiting for Nitzan
- [ ] **Refresh the Reading Studio** before reading topic 19-20/30-33/51: the q-552 take (20:15) used a page from 03:02; 51 unrecorded scripts now name their methods (q-549, q-553-556, t20, geometry, t51). q-552 itself was kept as read.
- [x] Method vocabulary: "The math way" approved by Nitzan (not just algebra); "Understanding" added to topic 51 as a lesson (approved).
- [ ] "open/closed" spoken in absolute-value-3 ¶10/12/14, q-360 ¶2, q-361 ¶3 → re-read as "inside/outside" or keep?
- [ ] pt-q18 written solution "16√3 ≈ 27.2" → replace with whole-number bounds?
- [ ] solve-q-r26-t18-02 → add the two short lines (re-read) or keep as recorded?
- [ ] Next script topic: 21?

## Done (recent)
| Who | When | Job | Result |
|---|---|---|---|
| Claude | 15 Oct 21:35 | Reading Studio audio-only layout (teacher: "bigger, fill the screen, not yellow, like the video ones") | `.audiolayout`: prompter ~85% width / ~80% height, current ¶ 45px centred (long ¶ shrinks to fit), next ¶ small+faded, past hidden; no yellow anywhere (also camera re-read view, pbar, stamp); collapsible list (hides while recording), compact dock. Camera layout unchanged. Rebuilt all 13 topics (statuses identical; solve-q-553 new take of hers picked up). Headless fake mic/cam 1440×900 + 1512×982 + dark: 0 console errors. No commit. |
| Codex | 15 Oct 21:26 | Batch A independent pre-recording review, t15–20 | `reviews/batch-A.md`;29actionable lessons;#147recorded during final check,skipped. Full spoken/prompter/question review;all487 step frames/72contact pages inspected.14must/70should. Findings only;no fixes/video registrations. Evidence: Codex workspace `work/batch-A-review-2026-10-15`. |
| Claude | 15 Oct | Pen colour by subject (teacher 15 Oct): algebra 1–20 red #d62d48, all other topics dark blue #1e3a8a (10.4:1 on white); pen marks follow it, crosses stay red | `studio_handwrite.py` (hwInk, hybridSvg sets window.__hwInk; hw items + auto-lines), `studio_autonarrate.py` (marks/WRITE); her live pen untouched. Build OK, math_check 30–33/51/13 0/0/0, svgcheck 0 broken, video_status: no rendered non-algebra videos, ledger unchanged. No commit. |
| Claude | 15 Oct | Topic 51 "Understanding" camera lesson (pt51-understanding, Reading Studio #323); q01 names it; t51 summary lists 6 methods | build/export/svgcheck OK; Reading Studio + Video-Status rebuilt; ready to record |
| Claude | 15 Oct 20:30 | One method-name vocabulary (her Hebrew core: The math way / Plugging in numbers / Plugging in the answers / Understanding / Estimation / Insight, `Method N · <core>[: specific]`) | Titles + sidebars in all prepared videos (t13-20, 30-33, 51); spoken method names in 51 unrecorded scripts; guide table + R13; `_method_names.CORE` + `check_vocab` in every spec; overlay headers reconciled. Checks: regen = ai_scripts, ai_check no new fails, math_check 0/0/0, svgcheck 0, Reading Studio re-read list unchanged. No commit. |
| Codex | 15Oct19:14 | Current-source camera batch5 | Absolute Value1–3and Primes1/3published and registered;21.5min;face top-right,sync≤1.6ms;full decode/handwriting/frame checks. Prior Ready copies archived. Outputs/current-camera-2026-10-15;receipt work/current-camera-2026-10-15/finished.json. Remaining send queue not rendered. |
| Codex | 15Oct19:14 | Reconcile4recent Topic13entries | q358/q360/q362 verified current and registered without duplicate renders. q359 current visuals differ,so left pending. Receipt work/current-camera-2026-10-15/reconciled-recent-finals.json. |
| Codex | 15 Oct 07:49 | Remaining-work audit | Tracker:33Send (3held;30candidates),4Check,38Re-read. q358/359/360/362 need render-record reconciliation; latest handoff specifically flags q359 visuals. Recent t13-01/t13-13/q369 exports flagged stale cues: compare before duplicate rendering. No renders or Done registrations made in this audit. |
| Claude | 15 Oct | Video status tracker | `~/Downloads/Video-Status.html`, `video_status.py`, `render_ledger.json` |
| Claude | 15 Oct | Board matches her actual readings (~20 videos) | commit 1dc96c2 |
| Claude | 15 Oct | Camera lessons t13/t14: math at the clause, no early answers (from your MP4 review) | commit 1009fa9; reply in `For-Codex-camera-review-reply.txt` |
| Claude | 15 Oct | Tag fragments in cue phrases fixed (q-431/465/512/513, powers) + ai_check guard | commit 4228cd6 |
| Claude | 14 Oct | Key-click removal in reading_to_video; clicker/pedal keys | commit 2e23fa3 |
| Claude | 14 Oct | Topic 51 scripts (all camera); topics 30–33 | commits 2cff82d, b29dc5c … |
