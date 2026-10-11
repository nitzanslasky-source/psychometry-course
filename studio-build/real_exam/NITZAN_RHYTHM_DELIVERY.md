# Nitzan's Rhythm and Delivery, measured: rules for AI script punctuation and pauses

## How this was measured

**Transcription.** All 189 English takes were re-transcribed with word-level timestamps (about 800 minutes; faster-whisper small.en, `word_timestamps`). The output is in `scratchpad/tstyle/wt/*.json`.

**Pauses.** Pauses come from the audio itself, not from whisper. Parselmouth (Praat) intensity was computed every 10 ms. A pause is any stretch of 0.15 s or more that is more than about 28 dB below the take's loud level. Each pause was assigned to the word boundary it falls on.

**Section types.** Each sentence was tagged as one of the following:
- **stem reading**: the opening sentences of a solution that match the question's words
- **calculation**: 40% or more of the sentence's tokens are numbers or operators
- **recap**: starts with "so again / we said / remember / summary", or falls in the last 12% of a lesson
- **closing**: "see you in the next…"
- **explanation**: everything else

**Pitch.** Pitch and loudness of each word were measured with parselmouth on 22 takes, about 2,400 sentences:
- 8 lessons: numbers, absolute-value, fraction-basics, primes, inequalities, r26-t05-shortcuts, r26-t12-signs, systems
- 14 solutions: q-099, 125, 138, 184, 292, 295, 323, 363, 364, 370, r26-t02-05, t03-01, t08-01, t09-04

Pitch is given in semitones (st) relative to her median in that take. Loudness is in dB relative to her median.

**Pipeline it applies to.** The current AI narration settings (ai_narrate.py, segmented mode) join lines with these gaps:

| Where | Gap |
|---|---|
| After a line | 0.42 s |
| After a line ending in "?" | 0.5 s |
| Before a new slide | 0.75 s |
| `[short pause]` | 0.6 s |
| `[pause]` | 0.9 s |
| `[long pause]` | 1.4 s |

The rules below are written for those settings.

---

## 1. The measurements

### 1.1 Pace

| | Words per minute (incl. pauses inside sentences) | Syllables/sec (speech only) |
|---|---|---|
| Whole take, incl. all silences | **167** (lessons 167, solutions 168); per take p10-p90: 155-183 | |
| **Explanation** | **201** | **5.9** |
| **Calculation** | **154** | **4.6** (22% slower) |
| **Stem reading** | **169** | **4.9** (18% slower) |
| **Recap** | 196 | 5.9 (as fast as explanation) |
| Closing ("I'll see you in the next…") | 315 | fastest |
| Self-question ("How do I get rid of the root?") | | 6.1 (slightly faster than statements, 6.0) |

- **Silence.** 27% of each take is silence. Most of it is board-writing time that the AI won't have, so the AI version will be shorter at the same speaking rate.
- **She sped up over the recording period.** Takes from the first half (30 Sep onward) average 5.4 syllables/sec; the second half (to 8 Oct) averages 5.6.
- **Fixed phrases rush.** "to the power of" runs at about 375 wpm, "let's look at" about 375, "what do I do" about 480, "I'll see you in the next" about 600. "is equal to" is slower, about 245, because a value follows it.

### 1.2 Sentence length (whisper punctuation)

| | p10 | p25 | median | p75 | p90 |
|---|---|---|---|---|---|
| Words per sentence | 4 | 6 | **9** | 14 | 20 |

- 29% of her sentences are 6 words or fewer, mostly questions and "right?"-type tags. 6% are 25 words or more: run-on calculations joined with "and then… and…".
- Lessons and solutions are the same.
- By section, the median is: stem 10, explanation 9, calculation 9, recap 10.

**Rhythm.** Short question (4-7 words), then an answer sentence (9-14 words), with an occasional long chain.

### 1.3 Where she pauses, and for how long

| Boundary | n | p25 | **median** | p75 | p90 | No pause at all |
|---|---|---|---|---|---|---|
| End of a sentence (.) | 8,420 | 0.18 | **0.41 s** | 0.61 | 0.92 | 23% |
| After a real question (?) | 1,881 | 0.00 | **0.37 s** | 0.57 | 0.81 | 26% |
| Self-question → her answer | 1,295 | 0.00 | **0.36 s** | 0.54 | 0.79 | 27% |
| After "right?" | 1,451 | 0.00 | **0.32 s** | 0.50 | 0.74 | 33% |
| After a comma | 8,154 | 0.00 | **0.19 s** | 0.40 | 0.60 | 46% |
| **Before "Now…"** (new step) | 942 | 0.38 | **0.55 s** | 0.88 | 1.22 | 10% |
| **Before a method label** ("Our second method…") | 71 | 0.32 | **0.58 s** | 1.15 | 1.59 | 18% |
| Before the verdict sentence ("…is our answer", "circle…") | 109 | | **0.39 s** | | | |
| End of the stem reading | 45 | | **0.50 s** | | | |
| After a calculation sentence | 2,470 | 0.19 | 0.42 | 0.68 | 1.00 | 22% |
| Mid-clause (no punctuation) | 113,705 | | | | | **91% none**; only 3% are 0.5 s or more |

**Long silences.** Silences of 1.5 s or more happen about 0.45 times per minute. They fall:
- after a calculation, while she writes (36%);
- before a new step or method (25%);
- elsewhere (35%).

**She never pauses for effect before the answer.** The verdict comes after a normal 0.4 s.

**A self-question is answered almost at once.** The median gap is 0.36 s, shorter than the pipeline's 0.5 s gap after a "?" line.

### 1.4 Where she slows down and speeds up

**Slows down on:**
- **Calculations** (−22%).
- **Reading the stem** (−18%).
- **Numbers.** A number word mid-phrase lasts about **40% longer per syllable** than other words (0.24 vs 0.17 s/syllable). She says the digits deliberately.
- **Before a value.** Function words get stretched when the next thing is a value she is reading off the board. These stretches of 0.6 s or more happen about 2.9 times per minute: "is" (608), "and" (402), "to", "the", "so". This is **her hesitation sound**: she stretches "iiis…" instead of saying "um" (whisper found 0 ums). Mid-clause silences of 1 s or more are rarer, about 0.6 per minute. About 44% of them sit just before a number or symbol, or right after an operator ("x is… 6").

**Speeds up on:**
- Fixed phrases (above).
- Self-questions.
- "right?".
- Sign-offs.
- The last 10% of a take (6.05 vs 5.6 syllables/sec in the middle).

### 1.5 Lingering on the key idea

She does **not** linger by slowing down or pausing.

| | Key-idea sentences (n = 610: important / rule / trap / always / never / it means / therefore) | Other explanation sentences |
|---|---|---|
| Rate (syllables/sec) | 5.8 | 5.9 |
| Pause after | 0.41 s | 0.38 s |
| Repeated (shared 4-word phrase) within 30 s | 16% | 16% |

She lingers through **content and pitch**:
- She gives 1-3 extra sentences per key idea: an example, a "why", a counter-case. This is where most of the 444 keep-worthy additions sit (see added_by_nitzan.json).
- She raises her voice on the logic words (1.6 below).
- She ends with a short capsule line: "False means no x. True means every x."

**For the AI:** linger by writing the extra sentence, not by adding [pause] tags.

### 1.6 Pitch and loudness (22 takes)

- **Her voice.** Median F0 is about **140 Hz** (takes range from 127 to 150). The working range is p10-p90 = 113-193 Hz, about 9 semitones. This is a fairly low, calm female voice, not sing-song.

| Word class | Mean F0 (st vs median) | High F0 (90th pct, st) | Peak loudness (dB vs median) |
|---|---|---|---|
| **Logic / key words** (not, only, always, both, every, same, opposite, also, can't, must…) | **+2.1** | **+4.0** | **+7.1** |
| Numbers | +0.5 | +2.8 | +6.9 |
| Other content words | +0.6 | +2.7 | +6.2 |
| Function words | +0.55 | +2.1 | +4.6 |
| First word of a sentence | +0.9 | +2.0 | +4.7 |
| Last word of a sentence | −1.0 | +1.7 | +4.3 |
| **Verdict number** ("number **three**") | **−1.7** | +0.1 | +5.5 |
| "right?" | starts at −1.9, ends at **+2.5** | | +3.4 |

The words most often at her top-15% pitch peaks:
- **always** (68% of its uses), **therefore** (54%), **still** (41%), **can't** (41%), **each** (39%), **does** (39%)
- **only**, **every**, **either** (33%), **also**, **or**, **flip**, **not**, **means**, **true** (26-31%)

Words that almost never peak: "power", "remember", "our", "okay", "which", "I'll", "like".

**What the pitch shows:**
- **The stress falls on the logic, not the maths.** She lifts the word that carries the reasoning ("**always**", "**only** when…", "it's **still** negative", "**can't**"). The numbers get length and loudness, but little extra pitch.
- **Sentences decline steadily.** Pitch runs +1.5 → +0.4 → −0.2 st across the first, middle and last third of a sentence. Statements fall at the end.
- **The verdict is said low and flat.** "number three" sits about 1.7 st *below* her median: calm, final, not excited. It is not a celebration.
- **"right?" rises in 98% of cases** (by about 4.5 st), quickly and lightly. It is a real question tag, with no pause before it.

### 1.7 Fillers and hesitations

There are no "um"s. Her hesitation devices are, in order of frequency:
1. Stretched function words before a value (about 2.9 per minute).
2. "So," / "Okay," restarts.
3. Doubled starts ("what I could do is I could…", 31 / 26 takes).
4. "sorry" self-repairs (17 takes), almost all while reading a formula or a sign.

Where they happen: before numbers, while reading the board, and in improvised generalisations. They almost never happen in a self-question or in a line she has fully scripted.

---

## 2. Rules for AI script punctuation and [pause] placement

These rules fit ai_narrate.py's segmented mode. One line becomes one TTS request, and lines are joined by 0.42 s, or 0.5 s after "?".

**P1. One line = one spoken sentence of 6-14 words.** Her median is 9 words, and the gap between lines (0.42 s) equals her median sentence-end pause (0.41 s). So the default line gap is already right. **Don't add [pause] at ordinary sentence ends.**

**P2. Keep a self-question and its answer on the same line.**
- Write: "How do I get rid of the root? I multiply by root 2."
- Her question-to-answer gap is 0.36 s. A line break after "?" gives 0.5 s, which sounds like a quiz.
- Only start a new line for the answer when the answer is itself long (more than 12 words).

**P3. "right?" goes at the end of a statement line,** after a comma: "9 is 3 squared, right?" Never put "right?" on its own line. Use it once per 3-4 lines, after a fact the student should already accept.

**P4. Commas are her breath, not a pause.** Half of her commas have no pause at all. Use commas freely inside lines to group "number, operation, number" ("So 30 over 6, that's 5."). Don't use "…" (she has no mid-sentence pauses: 3% are 0.5 s or more). **Replace every "..." with a comma or a full stop.** The current ai_scripts contain 344 of them.

**P5. Put [short pause] (0.6 s) at the start of these lines:**
- the line that starts a new step with "Now…" (her median there is 0.55 s);
- the line after the stem reading (0.5 s), or use `"pause": 0.5` on the stem line;
- the line before the verdict, only when the verdict follows a list of checks.

**P6. Put [pause] (0.9 s) only:**
- before a method label ("Our second method: plugging in numbers."): her median is 0.58 s, p75 is 1.15 s;
- before the closing nudge.

That is at most 2-3 per solution video.

**P7. No [long pause].** Her long silences are board-writing. The AI has no board time to fill, and a draw cue already has its own animation time.

**P8. Never pause before the answer for drama.** The verdict comes after a normal gap and is said calmly. Write it as a plain, low statement: "So x is 6. Number three." Use no "!", no CAPS and no [excited]. Her verdict pitch is 1.7 st *below* her median.

**P9. Slow down for numbers and stems with wording, not tags.**
- Calculation lines: shorter lines (6-10 words), one operation per line, numbers in digits, and a comma between the steps: "4 times 3, that's 12. 12 times 2, 24."
- Stem lines: read in full sentences, and use the `"voice": "calm"` preset (already defined for "the question reading and the plain calculation lines"). This matches her measured −18% / −22%.

**P10. Let the fixed phrases run.** "to the power of", "let's look at", "what do I do", "I'll see you in the next question" are fast in her speech. Don't break them with commas.

**P11. Stress is carried by the logic word, placed where the voice naturally falls on it.** Put the key word near the start or middle of a short line, not at the end, where her pitch falls:
- "It's **always** negative." "**Only** when they have opposite signs."
- The script's CAPS rule (at most one per video) should go on one of her peak words: always, only, not, can't, still, every, both, also, or.
- Never use CAPS on a number or on the answer.

**P12. Put the capsule last, as its own line.** A key idea ends with a 6-10-word line built as a parallel pair ("Same sign, they flip. Different signs, they don't."). That line is where she lingers. Don't follow it with a [pause]; the line gap is enough.

**P13. Keep the closing short and quick.** "I'll see you in the next question." is fine as its own line after the [pause] of P6.

### Quick check for any AI script

- [ ] Median line 6-14 words; no line over 20 words.
- [ ] No "..."; no [long pause]; no more than 3 [pause] per solution and 1 per slide in lessons.
- [ ] Each self-question has its answer on the same line.
- [ ] "right?" at most once per 3 lines, never on its own line.
- [ ] [short pause] or `"pause"` after the stem and before each "Now…" step; [pause] before each method label.
- [ ] Calculation lines short, one operation each, calm preset.
- [ ] The verdict is a plain, low statement ("So x is 6. Number three."), with no build-up pause.
- [ ] Stress words (always / only / not / can't / still / every / both) sit early in a short line.
