# Realism check: Group B (topics 44, 45, 46)

Scope: all 17 course video questions in `video_questions_sources.json` with topic 44 (Understanding paragraphs), 45 (Parables and comparisons) and 46 (Strengthening and weakening). Full text comes from `content/verbal_bank_all.json` (set `inf_v2`).

**How each original was found**
- **Official English translation** (`exams_new_mix.pdf`): Spring 2019 §1 Q6 and Summer 2020 §2 Q12.
- **Hebrew-mix OCR** (`work/verbal/ocr_hebmix`):
  - Autumn 2025 §1 Q16: p037
  - Winter 2024 §2 Q13: p074
  - Autumn 2022 §2 Q12: p165
  - Autumn 2022 §1 Q10: p158
  - Spring 2026 §1 Q14: p004
  - Spring 2024 §1 Q13: p099
  - Spring 2026 §2 Q7: p009
  - Winter 2024 §1 Q8: p065
- **Hebrew OCR** (`work/verbal/ocr`): September 2016 §2 Q10 (p15) and July 2016 §2 Q7 (p13).
- **Rendered from the Hebrew PDFs** in `work/new_exams_2013_2016` and read visually:
  - April 2015 §1 Q10 and Q15 (pdf pages 7 and 9)
  - February 2015 §2 Q7 (page 14)
  - February 2014 §1 Q8 (page 6)
  - September 2015 §1 Q11 (page 7)

**All 17 originals were found. Every source label is correct.** The OCR sometimes drops the leading "1" of a question number, for example ".3" for 13. The page and section positions confirm Q13, Q14 and Q16.

**The comparison yardstick** is 36 of NITE's own English inference items from 2019–2026 (`vr_inference_newmix.json`). Across these, stems run about 50–140 words (median about 85) and each option runs 1–40 words.

Word counts in the tables are the course item's (stem / options).

---

## Topic 44: Understanding paragraphs

| qid | source | words (stem / options) | fidelity to original | rating | verdict |
|---|---|---|---|---|---|
| vb-inf_v2_0077 | Spring 2019 §1 Q6 | 68 / 7–8 | Near-verbatim paraphrase of NITE's official English (NITE: 75 / 6–8). Same key (3). | **5** | KEEP. Policy flag: see note A. |
| vb-inf_v2_0017 | Autumn 2025 §1 Q16 | 107 / 14–18 | Rambam became "Arben" and the *Guide* became "his principal work". **The meaning drifted: the key is no longer clear-cut** (see below). | **2** | TWEAK, or REPLACE with inf_v2_0086 |
| vb-inf_v2_0085 | Summer 2020 §2 Q12 | 88 / 15–20 | Near-verbatim paraphrase of NITE's official English (NITE: 87 / 16–22). There is no official key, but the answer (2) is unambiguous. | **5** | KEEP. Policy flag: see note A. |
| vb-inf_v2_0031 | Winter 2024 §2 Q13 | 96 / 18–22 | The stem was reworded and **all four options were rewritten**. The original's key idea ("people not directly involved share the blame") became a stronger claim ("most of the blame does not fall on the driver"). | **3** | TWEAK |
| vb-inf_v2_0059 | Autumn 2022 §2 Q12 | 80 / 20–30 | Faithful. Jewish references were made generic (Zionist movement, Lag BaOmer, Haggadah, Hanukkah), but option 4 still says "New Year of the Trees". | **4** | KEEP. Optional: make option 4 generic too ("a tree festival"), for consistency. |

**Detail for 0017.**
- The Hebrew separates two ideas: the *purpose* (תכלית), which both schools agree on, and man's *vocation* (ייעוד), which they dispute.
- School 1 says Rambam *could not really have believed* that the intellectual purpose was man's vocation, because it is unattainable. School 2 says he did: man's vocation is to strive toward it anyway.
- The course version merges both ideas into "purpose" and drops School 1's "he couldn't really have meant it". As a result:
  - The two views as written are compatible (school 1 never denies the duty to strive), so "are divided" has no content.
  - Option 2 ("disagree about what the purpose is") now echoes the first sentence ("divided over his conception of the purpose of human life") and becomes defensible. The original option 2 carried a false reason clause ("since he never says what the purpose is"), and the course dropped it.

**Fix for 0017:**
1. Restore the purpose/vocation split: "One school holds that although Arben states that man's end is X, he cannot have regarded it as man's vocation, since…; the other holds that man's vocation is nonetheless to strive…".
2. Restore the false "since…" clause in option 2.
3. Otherwise, replace it with **inf_v2_0086** (Summer 2020 §2 Q14, the Hazaz "two approaches dispute which question"). It has the same mechanism and is checked against the official English.

**Detail for 0031.**
- The stem says the claim is right "but only in part". The original says it is right *if "the human factor" is correctly interpreted*. That is a different move: Zeidel widens the concept, he does not partly reject it.
- The course distractors are weaker than NITE's:
  - (4) "the driver alone bears responsibility" is the opposite of the passage and so transparently wrong.
  - (3) "a few reckless drivers" is off-topic.
  - NITE's distractors were closer traps: some accidents are caused by non-human factors; drivers, being human, can't be expected to be error-free; drivers often *prevent* accidents by absorbing others' errors.

**Fix for 0031:**
- Restore "right — provided 'the human factor' is understood correctly".
- Soften the key to "…part of the blame lies with people not directly involved in the accident".
- Rebuild options 3 and 4 on the original trap types (human fallibility excuse; driver as preventer).

---

## Topic 45: Parables and comparisons

| qid | source | words (stem / options) | fidelity to original | rating | verdict |
|---|---|---|---|---|---|
| vb-inf_v2_0288 | Spring 2026 §1 Q14 | 95 / 8–11 | The topic changed from "AI vs. natural intelligence / the horseless carriage" to "machine translation vs. the human interpreter / the flameless lamp". The mechanism is preserved and options 1–3 map well. **Option 4 is off.** | **4** | TWEAK option 4 |
| vb-inf_v2_0316 | April 2015 §1 Q10 | 84 / 22–41 | The stem is faithful. **Options 2 and 4 are mistranslated or reworked, and the key's logic weakened** (see below). | **2** | TWEAK |
| vb-inf_v2_0303 | Autumn 2022 §1 Q10 | 63 / 10–13 | Faithful and complete, with the same four options. | **5** | KEEP. Optional: restore the irony, "Your reasoning is about as sound as the claim that…" (Hebrew: דבריך הגיוניים ממש כמו). |
| vb-inf_v2_0297 | Spring 2024 §1 Q13 | 70 / 12–19 | Faithful except **option 3, which is garbled**: "thanking a burglar who, having broken into your house, saved the worker who had forgotten to lock the door". | **3** | TWEAK option 3 |
| vb-inf_v2_0322 | February 2015 §2 Q7 | 42 / 12–19 | Faithful; the options match one for one. | **5** | KEEP |
| vb-inf_v2_0331 | February 2014 §1 Q8 | 65 / 5–12 | Faithful. The trailing "likened —" matches NITE's English style ("compares … to -"). | **5** | KEEP |

**0288, option 4.**
- The course has: calling a digital camera "a camera without a screen". Digital cameras *have* screens, so the option reads as nonsense rather than as a tempting near-miss.
- The original's option 4 names the *older* device after a feature it lacks that the *newer* one has (still camera = "camera without video"). That reverses the direction of the correct example and makes a well-built trap.
- Fix: "Calling a film camera 'a camera without video'" follows the original too closely. Better to use a fresh pair with the same reversed direction, such as "Calling a paper map 'a map without navigation'".

**0316, options 2 and 4.**
- **Option 4 (the key).** The original is a courtesy made into a sellable service: travelers arriving at the port with an expired passport were allowed to renew it on the spot. A high fee was introduced to curb this, and more such travelers came.
  - The course has a tax office that "used to let people wait in line", then charged a fee to file, and more people came to file.
  - Waiting in line is not a favor. Filing is compulsory, so a fee to file cannot make filing "worth buying". The analogy to the kindergarten late fee (paying to extend service hours) is lost.
- **Option 2.** The original newspaper stopped printing its *economics supplement*; a separate economics daily appeared at nearly the newspaper's price, and many readers switched. The course says the newspaper "ceased publication for economic reasons", which is a mistranslation.
- Fix: rewrite option 4 around a deterrent fee that turns a tolerated lapse into a paid option. Restore option 2's "supplement" logic.
- There is no unused same-mechanism alternative in `inf_v2`, so fix rather than replace.

**0297, option 3.**
- The original distractor is "complaining that a burglar exploited the fact that you left the door unlocked". That is blame-shifting: it looks ironic but is not self-undermining.
- Fix: rewrite option 3 along those lines, for example "complaining that a burglar took advantage of your having left the door unlocked".

---

## Topic 46: Strengthening and weakening

| qid | source | words (stem / options) | fidelity to original | rating | verdict |
|---|---|---|---|---|---|
| vb-inf_v2_0378 | September 2016 §2 Q10 | 50 / 15–18 | Faithful ("two weeks" became "a few weeks"). | **5** | KEEP |
| vb-inf_v2_0385 | September 2015 §1 Q11 | 44 / 10–12 | Faithful. Option 1 dropped "as a birthday present" (Hebrew: לרגל יום הולדתו), which makes it purely irrelevant; that is arguably cleaner. | **5** | KEEP. Optional: restore "as a birthday present". |
| vb-inf_v2_0366 | Spring 2026 §2 Q7 | 86 / 20–24 | Faithful; the options were reordered. | **5** | KEEP |
| vb-inf_v2_0382 | July 2016 §2 Q7 | 46 / 11–15 | Faithful. | **5** | KEEP. Optional: "Hypothesis:" for "Supposition:"; "Physicians may prescribe Cyclodin only to…" (Hebrew רשאים). |
| vb-inf_v2_0387 | April 2015 §1 Q15 | 54 / 16–30 | Faithful; the options match one for one. | **5** | KEEP |
| vb-inf_v2_0369 | Winter 2024 §1 Q8 | 81 / 16–25 | **The scenario was rewritten, but the original options were kept, so option 2 is orphaned** (see below). | **2** | TWEAK (restore the original scenario), or REPLACE with inf_v2_0372 |

**Detail for 0369.**
- **The original's twist:**
  - The caretaker was absent last week, and latenesses dropped.
  - The secretary concluded that helping the caretaker does *not* deter lateness, because pupils enjoy his company.
  - A prize announcement at the same time is the confound.
- **The course version:** a new corridor punishment was introduced, latenesses fell, and the secretary concluded that it deters. The key (the prize) still works, but:
  - Option 2 ("When the caretaker returned to work after a long absence…") refers to an absence the stem never mentions.
  - Option 3 (a record three weeks ago) now half-suggests regression to the mean, a possible second weakener.
  - The item lost the original's "why would pupils be late *to* be punished?" inversion, which was the point of difficulty.
- **Fix:** restore the caretaker-absence scenario and the secretary's "they like being with him" conclusion.
- **Or replace** with **inf_v2_0372** (Summer 2022 §1 Q10, the celebrity ads with the reverse-causation confound). It is checked against the official English, and its key is (4).

---

## Summary of ratings

| topic | qid | rating | verdict |
|---|---|---|---|
| 44 | 0077 | 5 | KEEP (note A) |
| 44 | 0017 | 2 | TWEAK / REPLACE → 0086 |
| 44 | 0085 | 5 | KEEP (note A) |
| 44 | 0031 | 3 | TWEAK |
| 44 | 0059 | 4 | KEEP (minor) |
| 45 | 0288 | 4 | TWEAK option 4 |
| 45 | 0316 | 2 | TWEAK options 2 and 4 |
| 45 | 0303 | 5 | KEEP |
| 45 | 0297 | 3 | TWEAK option 3 |
| 45 | 0322 | 5 | KEEP |
| 45 | 0331 | 5 | KEEP |
| 46 | 0378 | 5 | KEEP |
| 46 | 0385 | 5 | KEEP |
| 46 | 0366 | 5 | KEEP |
| 46 | 0382 | 5 | KEEP |
| 46 | 0387 | 5 | KEEP |
| 46 | 0369 | 2 | TWEAK / REPLACE → 0372 |

The totals are 11 KEEP, 6 TWEAK (2 of them with a replacement option) and 0 outright REPLACE.

**Note A.** 0077 and 0085 are close paraphrases of NITE's *official English* text: the same sentence order and near-identical options. That is good for realism. However, the project rule says real-exam text is never copied into course files, and these sit close to that line. The owner should decide whether that is acceptable for these two items.

---

## Overall: how the course items differ from the real ones

**1. Where the item is a faithful translation, it reads like NITE.**
- 11 of the 17 are essentially one-for-one renderings of the original: stem, all four options and the key mechanism.
- Their lengths fall inside NITE's English range: stems 42–107 words against NITE's 50–140, and options 5–41 words against 1–42.
- Their difficulty and distractor quality match the source.
- **Every realism problem comes from rewording or "localising"**: 0017, 0031, 0316, 0297, 0369 and option 4 of 0288.
- The typical failures are:
  - **Meaning drift:** merging two concepts (0017); turning "if correctly understood" into "only in part" (0031).
  - **Orphaned options:** a distractor that refers to a scenario element the new stem no longer has (0369).
  - **Garbled distractors:** 0297 option 3; 0316 option 2.
  - **Implausible replacement examples:** 0316 option 4; 0288 option 4.

**2. Distractor strength drops when options are newly written.**
- NITE's distractors are near-misses. They restate part of the passage, reverse one relation, or add a plausible motive.
- The rewritten sets tend to include one or two transparently wrong options, such as the opposite claim or an off-topic claim (0031 options 3 and 4). That makes the items easier than the real ones.

**3. Register is a little more literary and British than NITE's English.**
- NITE's official English is plain, slightly stiff translationese:
  - It says "According to the paragraph…", "Which of the following statements does not weaken X's assumption?", "can be inferred from the text" and "In his reply, A compares X to -".
  - It uses spaced en-dashes ( – ).
  - "not" appears in lowercase, bold in print.
- The course items lean literary:
  - They use "passage", "whoever…", generic "man", "One hardly needs the apparatus of…", and heavy em-dashes (—).
  - They print "NOT" in capitals and use "data" as a plural question noun ("Which of the following data…").
  - They use Briticisms such as "rubbish" and "licorice".
- None of this is wrong, but it is detectably "not NITE".

**4. Stem wording and difficulty otherwise match** where the translation is faithful, and so do the answers' clear-cut quality and the answer-choice form (parallel, similar length).

### Recommendations
1. **Re-anchor the six flagged items to their Hebrew originals**, and keep every option's logical role: which one is the key, and what trap each distractor sets. When an example or scenario is localised, re-check every option against the new stem. The 0369 orphan and the 0316 key both come from skipping this.
2. **Never merge two terms the source keeps apart** (purpose/vocation, "only in part"/"if correctly interpreted"). After translating, confirm that each distractor is still *false* and the key still *uniquely* true.
3. **Match NITE's English house style in question prompts:**
   - "According to the paragraph / text"
   - "Which of the following statements weakens / does not weaken …?"
   - "In his reply, X compares … to -"
   - "Hypothesis:" rather than "Supposition:"
   - spaced en-dashes ( – ) and bold lowercase "not" rather than "NOT"
4. **Keep distractors at NITE's strength.** When an option has to be rewritten, build it on the original's trap type (partial restatement, reversed relation, plausible added motive), not on a flat contradiction.
5. **Use the two ready replacements if a fix is not wanted:** inf_v2_0086 for 0017 and inf_v2_0372 for 0369. Both are checked against the official English. Separately, decide on the verbatim-closeness question for 0077 and 0085 (note A).
