# Realism check — Group A (topics 41 Sentence completion, 42 Formal logic, 43 Understanding sentences)

Scope: all 19 course video questions with topic 41/42/43 in `video_questions_sources.json`.
Method: each item was traced to its real source question and compared with it:
- **Official NITE English exists (2 items):** Summer 2020 §1 Q14 and Summer 2022 §2 Q9, both in `exams_new_mix.pdf`.
- **Hebrew only (17 items):**
  - hebmix OCR: Winter 2025, Winter 2023, Autumn 2024, Spring 2024, Autumn 2025.
  - `work/verbal/ocr/*`: April/July/Sept 2016 and Autumn 2021.
  - Text layer of the single-sitting PDFs in ~/Downloads: 2018_winter, 2020_spring, 2021_spring.
  - Page images rendered from `new_exams_2013_2016`: Dec 2014, April 2014.

I found every source. For the Hebrew-only items I also compared register with real English items of the same type. The comparison set was:
- **Sentence completion:** Summer 2022 §1 Q7 (the fruit-compote item).
- **Formal logic:** Summer 2020 §1 Q14 and Summer 2022 §2 Q9.
- **Wording checks:** English prompts such as "Which is the remaining claim?" and "Which of the following is not possible?"

Word counts are for the course item. For reference, NITE's English completions have a median stem of 31 words and a median option of 16 words. Its English inference items have a median stem of 88 words and a median option of 19 words.

---

## Topic 41 — Sentence completion

| qid | source | stem / option words | fidelity to original | rating | verdict |
|---|---|---|---|---|---|
| vb-sc_tr_0130 | Autumn 2021 §2 Q12 | 39 / 7–10 | Faithful. Same option order and key (1). | 4 | **TWEAK (minor)**: change "neighbourhood" to "neighborhood". The Hebrew idiom סמכו ידיהם is flattened to "endorsed", which is acceptable. |
| vb-sc_tr_0103 | Spring 2020 §1 Q9 | 30 / 15–21 | Faithful. Same order and key (3). | 4 | **TWEAK (minor)**: "lends the writing the characteristics of" is a word-for-word rendering of משווה לכתוב מאפיינים. Change it to "gives the writing the character of". Change "vowel points" to "vowel marks (nikud)". |
| vb-sc_tr_0073 | Winter 2018 §1 Q10 | 63 / 18–24 | Faithful. It is a 4-blank argument/concession item with the same order and key (4). Its length is typical of a NITE item late in the block. | 4 | **KEEP**. Optional: the distractor wording "actually thinks" is weak; "in fact believes" is closer to NITE. |
| vb-sc_tr_0123 | Spring 2021 §1 Q11 | 27 / 8–10 | Faithful (לולא/רק אילו × שקר/מהימנה × זכאי/חייב). Same order and key (3). | 4 | **TWEAK (minor)**: "neighbour's" should be "neighbor's". Options 2 and 4 read "Only if the judge had … , the accused would not have been found …", which is ungrammatical because "only if" requires inversion ("would the accused not have been…"). You can fix the stem or accept it, since the options are wrong anyway. Still, NITE's English is grammatical in every option. |
| vb-sc_tr_0015 | Autumn 2025 §1 Q12 | 17 / 13–18 | Faithful (אילו/לולא counterfactual). Same order and key (2). | 5 | **KEEP** |

## Topic 42 — Formal logic (claims and logic)

| qid | source | stem / option words | fidelity to original | rating | verdict |
|---|---|---|---|---|---|
| vb-inf_v2_0409 | Summer 2020 §1 Q14 (**official English exists**) | 31 / 14–16 | Same logic. The options were re-ordered (NITE's (4) is now (3)). The wording drifts from NITE's: "football" instead of NITE's "soccer", "certainty" instead of "absolute certainty", "Are there students" instead of "Are there any students", and "was born in the summer" instead of "has a birthday in the summer". | 4 | **TWEAK**: bring it back to NITE's register (soccer, "with absolute certainty", "Are there any students…"). Note: this sitting was published in English, so students who later sit that paper as a simulation will have seen the item. |
| vb-inf_v2_0403 | Winter 2025 §1 Q13 | 14 / 12–14 | Faithful. The options were re-ordered and the key moved from 4 to 1. The prompt matches NITE's English formula ("Which is the remaining claim?"). | 5 | **KEEP** |
| vb-inf_v2_0406 | Winter 2023 §2 Q15 | 31 / 14–19 | Faithful. The options were re-ordered (NITE's profs pair is now (4) and the Liron pair is now (2)). | 4 | **KEEP**. Optional: put A and B on separate lines as NITE does. "Complementary pair" is the literal rendering of זוג משלים; "complete" is acceptable. |
| vb-inf_v2_0412 | July 2016 §2 Q12 | 26 / 9–14 | Faithful. Option 4 adds "nocturnal", which the original does not have; this does not change the key. | 4 | **TWEAK**: "on the basis of the datum" is stilted. Use "on the basis of this information". Optionally drop the added "nocturnal" in (4). |
| vb-inf_v2_0411 | April 2016 §2 Q10 | 34 / 12–17 | Faithful, with the same order and key (2). NITE starts every option with "Last winter…"; the course's "A winter in which…" is fine. | 5 | **KEEP** |
| vb-inf_v2_0408 | Summer 2022 §2 Q9 (**official English exists**) | 24 / 3–7 | Same item. Options 3 and 4 are swapped, and "contradicts neither statement" replaces NITE's "does not contradict either statement". NITE puts Statement A and Statement B on separate lines. | 4 | **TWEAK (minor)**: use NITE's line layout and its phrase "does not contradict either statement". The same note as for 0409 applies: this item comes from an English-published sitting. |
| vb-inf_v2_0404 | Autumn 2024 §2 Q17 | 58 / 6–9 | Logic is faithful, but the options were re-ordered (key 4 moved to 1). There are three surface problems: (a) option 1 says "lives in Shikmim" while options 2 and 4 say "lives in the village of…", so the options are not parallel; (b) the stem adds "and others did not", which the source does not have; (c) "it is NOT possible" is written in capitals. | 3 | **TWEAK**: make all four options say "lives in the village of …". Use "If so, it is not possible that one of the children -" in lower case. Put the two rules on separate bulleted lines. |
| vb-inf_v2_0416 | April 2014 §2 Q10 | 48 / 6 | Faithful, with the same order and key (4). | 4 | **TWEAK**: "Therefore it is NOT possible that there is in the zoo an animal that —" keeps Hebrew word order. Use "If so, it is not possible that the zoo has an animal that -", in lower case as NITE writes it. |
| vb-inf_v2_0405 | Spring 2024 §2 Q13 | 26 / 6–9 | Faithful. The options were re-ordered (key 4 moved to 2). | 4 | **TWEAK (minor)**: change "does NOT have" to lower case. "Which of the following data" becomes "Which of the following pieces of information", because each option is a single fact. |

## Topic 43 — Understanding sentences

| qid | source | stem / option words | fidelity to original | rating | verdict |
|---|---|---|---|---|---|
| vb-inf_v2_0359 | December 2014 §1 Q16 | 53 / 21–24 | Faithful, with the same order and key (1). The options are long and parallel, and the distractors are close (a certainty flip, and a shift from the future to the present), just as in NITE's version. | 5 | **KEEP** |
| vb-inf_v2_0353 | September 2016 §1 Q12 | 58 / 8–10 | **The distractors are much weaker than the original's.** Two course options substitute "and so" for "and so" or leave the claim unchanged, so they can be eliminated at a glance. Option 4 introduces "hard", a word the stem never uses. The original's traps were subtler: (a) swapping in a synonym connective ("and therefore"); (b) substituting a paraphrase of the premise ("only a few students fail" for "most pass"); (c) an option joined with "and in addition" instead of "or", where the item works only if both changes are made; (d) an option that starts from an already-logical sentence. | 2 | **TWEAK (substantial)**: rebuild options 2 and 4 on the original's traps: a synonym-connective swap, a premise-paraphrase swap, and "and also" in place of "or". If it is not rebuilt, **REPLACE** it with **vb-inf_v2_0361** (April 2014 §1 Q13, Dr. Tofi: "I support … but not his reasons"). I have not traced 0361 to its source. |
| vb-inf_v2_0356 | September 2016 §2 Q16 | 54 / 19–23 | Faithful, with the same order and key (4). | 5 | **KEEP**. Optional: NITE's English is American, so "positions vacant notice" becomes "job advertisement". |
| vb-inf_v2_0362 | April 2014 §2 Q13 | 82 / 16–23 | **Two translation errors.** (1) The stem says the researchers examined caffeine's effect "on the ability to concentrate". The original says they examined its effect on **being persuaded by arguments**. The course wording gives away the causal link the question asks about. (2) Option 2 says "those who **need** it". The original's צורך means "consume", so it should read "causes those who **consume** it to support vegetarianism more…". The key (3) is unaffected. Note that this is really an underlying-assumption item (scientific thinking), not sentence understanding. | 3 | **TWEAK (required)**: fix both errors. Optionally move it to a scientific-thinking video and use vb-inf_v2_0360 (Dec 2014 §2 Q9, Wilson's speeches) for topic 43. I have not traced 0360 to its source. |
| vb-inf_v2_0355 | September 2016 §2 Q14 | 55 / 13 | **Meaning error.** The original has Osnat saying "I do not believe **I am able** to translate the article from German into French, let alone into Spanish." The course has "I do not believe **anyone** could translate…". With "anyone", Osnat says nothing about her own languages, so Shlomo's inference ("you command French better than Spanish") no longer follows from her words, and the question falls apart. The options are faithful, with the same order and key (1). | 2 | **TWEAK (required)**: change it to "I do not believe I could translate the article…". After that fix the item is a 5. |

---

## Overall: how the course items differ from the real ones

1. **Content fidelity is high, and the logic is always the real item's.** All 19 items are translations of real NITE questions, and in all 19 the course key matches the original key after allowing for re-ordered options. Seven items had their options re-ordered, which is fine. Length and difficulty therefore match the originals almost exactly:
   - Sentence-completion stems run 17–63 words against NITE's English median of 31.
   - Logic stems run 14–58 words, and the two items with official English versions match them within a few words.
   - Understanding stems run 53–82 words, the same as their Hebrew sources.
2. **The real problems are translation slips, and they break items.** Two items are broken: 0355 ("anyone" instead of "I") and 0362 ("ability to concentrate" instead of persuasion, and "need" instead of "consume"). Item 0353 lost the original's clever distractors in the English adaptation, and its two eliminable options are the least NITE-like thing in this group. NITE's distractors are never eliminable at a glance.
3. **Wording tics that do not match NITE's official English:**
   - **Capitalized NOT** (0404, 0416, 0405; 0356 uses the lower-case "not"). NITE's English verbal sections never capitalize it: the corpus has 0 occurrences of " NOT " against 52 lower-case "not possible / not necessarily" forms.
   - **British spelling and vocabulary**: neighbour/neighbourhood, football, positions vacant. NITE's English is American (neighbor, soccer, color).
   - **Em-dash lead-ins ("—")**. NITE uses a spaced hyphen ("… one of the children -") and puts each rule and each Statement A/B on its own line.
   - **Hebrew word order or literalisms**: "there is in the zoo an animal", "on the basis of the datum", "lends the writing the characteristics of", "Which of the following data" for a single fact.
   - **Two English-published items reworded away from NITE's own English** (0409, 0408): football for soccer, "certainty" instead of "absolute certainty", "contradicts neither" instead of "does not contradict either".
4. **Register.** Apart from the tics above, the prose reads formal and dense, like NITE. It does not read like generic AI prose: there is no padding, no hedging, and the options are parallel.

### Recommendations
1. **Fix the three broken or weakened items first:**
   - **0355:** change "anyone could" to "I could".
   - **0362:** change the study's topic to persuasion and change "need" to "consume".
   - **0353:** rebuild the distractors on the original's synonym-swap and "and also" traps, or replace the item with vb-inf_v2_0361.
2. **Global find-and-replace in the Verbal video items:**
   - Change " NOT " to " not ".
   - Change British spellings to American (neighbour → neighbor, neighbourhood → neighborhood).
   - Change "football" to "soccer".
   - Change "If so/Therefore … —" to "If so, … -".
3. **Keep options parallel:** 0404 needs "the village of" in all four options. Keep NITE's line layout for rule lists and for Statement A/B.
4. **For the two items from English-published sittings (0409, 0408):** either use NITE's exact phrasing and register, or swap in a Hebrew-only equivalent from the inf_v2 "Claims and Logic" set. Students who later sit Summer 2020 or Summer 2022 as a simulation will have seen them, which the project's own sourcing rule warns against.
5. **Re-home 0362 to scientific thinking.** It is an underlying-assumption item, not sentence understanding.
