# Topic 9 (Roots, Fundamentals): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

## The Hebrew source does not exist for this topic

- `~/Downloads/01-Algebra-Original-Subtitles.txt` has **no transcript of her roots-fundamentals lesson.** Between the end of the
  exponents lesson (5350: "מפה אנחנו ממשיכים לשיעור הבא של כללים של שורשים", "from here we go to the next lesson, the root
  rules") and topic 10 (5360) there is only her structure note (5357):
  "ואז שורשים יסודות סרטון טבלה לימוד בעפ ואז 15 שאלות בלי סרטונים ביניהם" = one video, a table to learn by heart, then 15
  questions with no videos between them.
- No other file in `~/Downloads` has it (checked the Pasted text files, the .rtf files and `Subtitle-Match-Review.md`, which
  says the same: "Module 26 (roots lesson) … has no Hebrew subtitles, so it was not reviewed against the Hebrew").
- So a line-by-line comparison is impossible. What can be checked: (1) her structure; (2) **what her later videos say she taught
  in the roots lesson** ("כמו שלמדנו בשיעור יסודות", "as we learned in the fundamentals lesson"). Those back-references are
  listed in section 1 with their line numbers.

English sources: `scratchpad/ext/course/t09.txt` / `q09.txt`, base translation `base-v18.html` (video `roots`, card `roots`).
Recording status: `video_status.py` does not track topics 1-12. **Every topic-9 video has an older camera take** (6 Oct 2026,
`~/Documents/Course.recordings/1 Algebra/Topic 09 …`: roots, r26-t09-traps, 6 solution videos). Topics 1-12 are redone last
(first lesson on camera, the rest AI). Memory notes that her recorded `roots` take has a spoken slip ("root is on top",
said backwards); the script itself is right ("the power goes on top, the root index on the bottom"), so the camera redo
fixes it.

---

## 1. Hebrew → English

| # | Her video / what she says she taught | Lines (where she refers back to it) | English equivalent | Match |
|---|---|---|---|---|
| 1 | Roots-fundamentals lesson | 5357 (note only; no transcript) | `roots` (13 slides: what a root is, root of a square = \|x\|, pull out squares, bring a number inside, adding roots, multiply & divide, odd & even roots, roots as powers, powers inside roots, not for sums, root equations, rules table) | cannot be rated (no Hebrew) |
| 1a | Multiply/divide roots under one root (√a·√b = √(ab), √a/√b = √(a/b)) | 5372, 5387 ("לפי החוקים של כללי שורשים"), 7707 | `roots` slide "Multiply & divide" + card `roots` | SAME |
| 1b | "A rule we said is very important to know": a = √a·√a (2 = √2·√2) | 5453, 7900 | `roots` slide "Multiply & divide" ("six is root six times root six") | SAME |
| 1c | Root ↔ power: ⁿ√(aᵐ) = a^(m/n) ("divide the power by the root"), with her mnemonic **"חזקיהו בשמיים, והשורש באדמה"** (Hezekiah, the power, is in the sky; the root is in the ground = the denominator) | 7317, 7659-7676, 7683 | `roots` slides "Roots as powers", "Powers inside roots" + solve-q-r26-t09-01 ("The power is the flower, so it goes up on top. And the root stays in the ground") | SAME (her Hebrew pun "חזקיהו" became the English rhyme "the power is the flower"; the sky/ground image is kept) |
| 1d | Cancel the power and the root index by the same number (⁶√(x³) = √x) | 8072 ("כמו שלמדנו קודם"), 7677 | `roots` slide "Powers inside roots" (⁴√(3⁸): 8/4 = 2), root of a root = multiply the indexes | SAME in substance (English shows it as reducing the fraction exponent; the explicit "cancel the two indices" shortcut is used in topic 11) |
| 1e | √3 ≈ 1.7 (and √2 ≈ 1.4) | 7807 ("למדנו שזה בערך 1.7") | card `roots`, "Useful estimates" (√2 ≈ 1.41, √3 ≈ 1.73, …); r26-t09-traps "Estimate a root" | SAME |
| 1f | Even root: the root sign is only the positive value (√25 alone is 5) | 3981 (her equations-fundamentals video, topic 6: "בפסיכומטרי כשכתוב לי רק שורש 25 זה תמיד יהיה המספר 5") | `roots` slide "What a root is" | SAME |
| 2 | Table to learn by heart | 5357 (note) | `roots` slide "The rules table" + card `roots` (rules, roots table, estimates) | SAME |
| 3 | 15 questions, no videos between | 5357 (note) | 32 questions (units `unit-t9-1`, `root-practice`, plus r26 extras) **and 6 solution videos** (r26-t09-01…06) + r26-t09-traps | CHANGED (structure): she has no solution videos in this topic |

**Count (rateable rows, 8):** SAME 7 · CHANGED 1 (3) · PARTIAL 0 · MISSING 0. Row 1 (the lesson itself) cannot be rated.

---

## 2. English → Hebrew (added; no Hebrew equivalent can be confirmed)

Because her lesson has no transcript, every part of `roots` not listed in section 1 is "not confirmable" rather than "added":
root of a square = |x| (slide 3), pull out the LARGEST square (slide 4), bring a number inside (slide 5), not for sums
(slide 11), root equations with the fake-solution check and "don't divide by x" (slide 12). Clearly added by English (she has no
videos in this topic):

| English video | Content |
|---|---|
| solve-q-r26-t09-01 | Power over index; break into primes |
| solve-q-r26-t09-02 | Bring every number inside (to compare) |
| solve-q-r26-t09-03 | Plug in the answers; why −2 is a trap |
| r26-t09-traps | Estimate a root between perfect squares; square of a sum of roots (middle term); compare √3 + √5 with √15 |
| solve-q-r26-t09-04 | Plug in x = ¼ |
| solve-q-r26-t09-05 | Raise all to the 6th power |
| solve-q-r26-t09-06 | Multiply by the conjugate ("the partner"); work back from the answers |
| r26-t09-summary | Replaced by the summary page |

The base translation's lesson had 10 slides; the current one adds "Bring a number inside", "Powers inside roots" and "Root
equations". Nothing of the base was removed.

---

## 3. Missing from English: restore?

Nothing can be shown to be missing. Everything her later videos say she taught in the roots lesson (1a-1f) is in the English
lesson or the card. **RESTORE list: empty.**

Recommendation: **ask the teacher for the subtitles of her Hebrew roots-fundamentals video** (her course's "שורשים - יסודות"),
so this topic can be checked like the others before the topics 1-12 redo. Until then, the English lesson is the most complete
version available.
