# NITE Quantitative Reasoning — Official English Terminology Reference

**Sources (verified verbatim against official bilingual PDFs):**
- `psychometric_summer_2025_EN_acc.pdf` — Quant Section 1: PDF pages 53–72 (EN on odd PDF pages 53,55,57…; HE on even 54,56,58…). Quant Section 2: PDF pages 73–92. Answer key: PDF page 119.
- `psychometric_summer_2024_EN_acc.pdf` — Quant Section 1: PDF pages 50–67. Quant Section 2: pages 68–85. Answer key: PDF page 111.

Both exams use **identical** boilerplate, so everything below is stable reusable text — **reuse verbatim, never re-translate.**

Extraction commands that worked:
```bash
pdftotext -f <first> -l <last> -layout <exam>.pdf out.txt      # layout-preserving
python3 -c "import fitz; d=fitz.open('x.pdf'); print(d[52].get_text())"   # PyMuPDF
```

---

## 1. Reusable boilerplate

### 1.1 Section header (running header on every page)

```
Quantitative Reasoning – First Section
Quantitative Reasoning – Second Section
```

- **En dash** `–` (U+2013), spaces on both sides. NOT a hyphen.
- Title Case. Hebrew equivalent: `חשיבה כמותית - פרק ראשון` / `חשיבה כמותית - פרק שני`.

### 1.2 Section intro block (verbatim)

Title line:
```
Quantitative Reasoning
```

Right-hand box:
```
This section contains 20 questions.
The time allotted is 20 minutes.
```

Instructions paragraph:
```
This section consists of questions and problems involving quantitative reasoning.  Each question is followed by four possible responses.  Choose the correct answer and mark its number in the appropriate place on the answer sheet.
```

Gray-background note (immediately after):
```
Note:  The words appearing against a gray background are translated into several languages at the bottom of each page.
```

Hebrew source for reference:
```
בפרק זה מופיעות שאלות ובעיות של חשיבה כמותית. לכל שאלה מוצעות ארבע תשובות.
```

### 1.3 General Comments (verbatim — exactly 6 bullets, rendered with `*`)

```
General Comments about the Quantitative Reasoning Section

* The figures accompanying some of the problems are provided to help solve the problems, but are not necessarily drawn to scale.  Therefore, do not rely on the figures alone to deduce line length, angle size, and so forth.
* If a line in a figure appears to be straight, you may assume that it is in fact a straight line.
* When a geometric term (side, radius, area, volume, etc.) appears in a problem, it refers to a term whose value is greater than 0, unless stated otherwise.
* When \(\sqrt{a}\) (a > 0) appears in a problem, it refers to the positive root of a.
* "0" is neither a positive nor a negative number.
* "0" is an even number.
* "1" is not a prime number.
```

Note: NITE labels these as "6 bullets" colloquially but the printed list has **7 bullet lines** (the two "0" statements are separate bullets). Reproduce all 7 lines as above.

### 1.4 Formulas sheet (verbatim, MathJax-ready)

Header: `Formulas`

```
1. Percentages:  a% of x is equal to \(\frac{a}{100} \cdot x\)

2. Exponents:  For every a that does not equal 0, and for any two integers n and m –
   a.  \(a^{-n} = \frac{1}{a^n}\)
   b.  \(a^{m+n} = a^m \cdot a^n\)
   c.  \(a^{\frac{m}{n}} = \sqrt[n]{a^m}\)   (0 < a, 0 < m)
   d.  \(a^{n \cdot m} = (a^n)^m\)

3. Contracted Multiplication Formulas:
   \((a \pm b)^2 = a^2 \pm 2ab + b^2\)
   \((a + b)(a - b) = a^2 - b^2\)

4. Distance Problems:  \(\frac{\text{distance}}{\text{time}} = \text{speed (rate)}\)

5. Work Problems:  \(\frac{\text{amount of work}}{\text{time}} = \text{output (rate)}\)

6. Factorials:  \(n! = n(n-1)(n-2) \cdot \ldots \cdot 2 \cdot 1\)

7. Proportions:  If AD || BE || CF
   then \(\frac{AB}{DE} = \frac{BC}{EF}\) and \(\frac{AB}{AC} = \frac{DE}{DF}\)

8. Triangles:
   a.  The area of a triangle with base of length a and altitude to the base of length h is \(\frac{a \cdot h}{2}\)
   b.  Pythagorean Theorem: In any right triangle ABC, as in the figure, the following always holds true:  \(AC^2 = AB^2 + BC^2\)
   c.  In any right triangle whose angles measure 30°, 60°, 90°, the length of the leg opposite the 30° angle is equal to half the length of the hypotenuse.

9. The area of a rectangle of length a and width b is \(a \cdot b\)

10. The area of a trapezoid with one base length a, the other base length b, and altitude h is \(\frac{(a+b) \cdot h}{2}\)

11. The sum of the internal angles of an n-sided polygon is (180n – 360) degrees.  In a regular n-sided polygon, each internal angle measures \(\left(\frac{180n - 360}{n}\right) = \left(180 - \frac{360}{n}\right)\) degrees.

12. Circle:
    a.  The area of a circle with radius r is \(\pi r^2\)  (\(\pi = 3.14\ldots\))
    b.  The circumference of a circle is \(2\pi r\)
    c.  The area of a sector of a circle with a central angle of x° is \(\pi r^2 \cdot \frac{x}{360}\)

13. Box (Rectangular Prism), Cube:
    a.  The volume of a box of length a, width b and height c is \(a \cdot b \cdot c\)
    b.  The surface area of the box is \(2ab + 2bc + 2ac\)
    c.  In a cube, a = b = c

14. Cylinder:
    a.  The lateral surface area of a cylinder with base radius r and height h is \(2\pi r \cdot h\)
    b.  The surface area of the cylinder is \(2\pi r^2 + 2\pi r \cdot h = 2\pi r (r + h)\)
    c.  The volume of the cylinder is \(\pi r^2 \cdot h\)

15. The volume of a cone with base radius r and height h is \(\frac{\pi r^2 \cdot h}{3}\)

16. The volume of a pyramid with base area S and height h is \(\frac{S \cdot h}{3}\)
```

### 1.5 Subsection headers

**Pure math clusters:**
```
Questions and Problems (Questions 1-8)
Questions and Problems (Questions 13-20)
```
Hebrew: `שאלות ובעיות (שאלות 8-1)`. Note the range uses a plain **hyphen** with no spaces: `1-8`, `13-20`.

**Chart clusters — the term is "Graph Comprehension", NOT "Data Interpretation":**
```
Graph Comprehension (Questions 9-12)
Study the graph below, then answer the four questions that follow.
```
Hebrew: `הסקה מתרשים (שאלות 12-9)` / `עיינו היטב בתרשים שלפניכם, וענו על ארבע השאלות שאחריו.`

After the intro paragraphs and the graph, before the questions:
```
Note: In answering each question, disregard the information appearing in the other questions.
```
Hebrew: `הערה: בכל שאלה התעלמו מהמידע המופיע בשאלות האחרות.`

(2024 exam printed a lowercase variant `Note: in answering each question, …`; use the 2025 capitalized form.)

**Table-based clusters — a THIRD cluster type, confirmed in Summer 2024 (PDF p.76/77):**
```
Table Comprehension (Questions 8-11)
Study the table below, then answer the four questions that follow.
```
Hebrew: `הסקה מטבלה (שאלות 11-8)` / `עיינו היטב בטבלה שלפניכם, וענו על ארבע השאלות שאחריו.`

Note the distinction:
| Hebrew | English | Data shown as |
|---|---|---|
| הסקה מתרשים | **Graph Comprehension** | chart / graph |
| הסקה מטבלה | **Table Comprehension** | table of numbers |

Do NOT translate `מטבלה` as "Graph Comprehension" — several exams (Autumn 2020 §1,
Autumn 2024 §1, Winter 2020 §1, Spring 2020 §2, Autumn 2022 §2, Autumn 2023 §1,
Autumn 2025 §2, Winter 2023 §2, Winter 2024 §2) use the table variant. It takes the
same trailing "disregard the information appearing in the other questions" note and
the same `Questions` heading.

When translations sit on a different page:
```
Note: Translations of the words appearing against a gray background appear on pages 62-63.
```

The questions themselves are then introduced by a bare heading:
```
Questions
```
Hebrew: `השאלות`

### 1.6 Observed section layout patterns

| Exam / section | Cluster structure |
|---|---|
| 2025 §1 | Questions and Problems 1-8 → Graph Comprehension 9-12 → Questions and Problems 13-20 |
| 2025 §2 | Questions and Problems 1-16 → Graph Comprehension 17-20 |
| 2024 §1 | Questions and Problems 1-8 → Graph Comprehension 9-12 → Questions and Problems 13-20 |
| 2024 §2 | Questions and Problems 1-7 → Graph Comprehension 8-11 → Questions and Problems 12-20 |

Graph Comprehension is always a **contiguous block of exactly 4 questions**. Do not assume its position — read it off the actual exam.

### 1.7 Copyright footer (English pages)

```

```

---

## 2. Terminology glossary (all entries confirmed against real bilingual exam text)

### 2.1 Figure / diagram vocabulary — critical

| Hebrew | Official English | Notes |
|---|---|---|
| בסרטוט שלפניכם | **In the accompanying figure** | NEVER "diagram", "sketch", "drawing", "the figure before you". |
| בסרטוט שלפניכם ריבוע ABCD | **The accompanying figure shows square ABCD** | When the Hebrew leads with the object, English uses "The accompanying figure shows …". Both forms are official; choose by Hebrew clause order. |
| לפי נתון זה והנתונים שבסרטוט, x=? | **Based on this information and the information in the figure,**<br>**x = ?** | Exact template. Line break before `x = ?`. |
| לפי הנתונים שבסרטוט | **Based on the information in the figure,** | Used when there is no preceding "this information". |
| לפי נתון זה והנתונים שבסרטוט, מה אורך הצלע CD (בס"מ)? | **Based on this information and the information in the figure, what is the length of side CD (in cm)?** | Interrogative variant — the template flexes into a wh-question. |
| תרשים | **graph** | In Graph Comprehension clusters. |
| מקרא | **key** | NOT "legend". e.g. "(see key)", "(see upper part of the key)". |
| הערה | **Note:** | |

### 2.2 Question stems / logical phrasing

| Hebrew | Official English |
|---|---|
| נתון: | **Given:** |
| נגדיר: | **Let us define:** |
| איזו מהטענות הבאות נכונה בהכרח? | **Which of the following statements is necessarily true?** |
| איזו מהטענות הבאות נכונה בהכרח? (claim-form) | **Which claim is necessarily true?** (only if Hebrew uses that shorter form) |
| איזה מהאי-שוויונים הבאים נכון בהכרח? | **Which of the following inequalities is necessarily true?** |
| איזה מהשוויונים הבאים נכון בהכרח? | **Which of the following equations is necessarily true?** |
| מה מהבא נכון בהכרח? | **Which of the following is necessarily true?** |
| שום טענה משלוש הטענות הנ"ל אינה בהכרח נכונה | **None of the above three statements is necessarily true.** |
| אף אחת מהתשובות אינה נכונה בהכרח | **None of the above is necessarily true.** |
| אי אפשר לדעת על פי נתוני התרשים | **It is impossible to know from the data in the graph.** |
| אי אפשר לדעת על פי הנתונים | **It cannot be determined from the information given.** |
| לא ניתן לקבוע איזו מהטענות נכונה | **From the information given, it cannot be determined which of these statements is true.** |
| איזה מהתרשימים הבאים … | **Which of the graphs below could describe …** / **Which of the following graphs describes …** |

### 2.3 Negative stems — plain lowercase "cannot"

Confirmed: `אינה יכולה להיות` → **"cannot be"**, written as plain lowercase mid-sentence. **Never** capitalize, bold, italicize, or underline it, and never rephrase to a positive.

> Which of the following groups of three numbers **cannot** be the lengths of the sides (in cm) of a triangle?

Also confirmed: "A smaller amount of wax **cannot** be recycled."

### 2.4 Number-type terms

| Hebrew | Official English |
|---|---|
| מספר שלם וחיובי | **positive integer** |
| מספרים שלמים וחיוביים | **positive integers** |
| (x שלם וחיובי) | **(x is a positive integer)** — preserve the parenthetical exactly where the Hebrew places it, including the space before `(`. |
| מספרים חיוביים | **positive numbers** |
| מספר ראשוני | **prime number** |
| p ראשוני כלשהו | **p is any prime number.** |
| מספר כלשהו הגדול מ-10 | **x is any number greater than 10.** |
| כל המספרים השלמים בין 1 ל-299 (ועד בכלל) | **All the integers between 1 and 299 (inclusive)** |
| מתחלק ב- | **divisible by** |
| שארית | **remainder** |
| מה השארית המתקבלת מחלוקת x ב-4? | **What will be the remainder if x is divided by 4?** |
| ספרת האחדות | **units digit** |
| טווח מדויק | **exact range** |

### 2.5 Units — exact forms

| Hebrew | Official English | Notes |
|---|---|---|
| סמ"ק | **cm³** | Superscript 3. In MathJax contexts: `cm\(^3\)` or literal `cm³`. |
| ס"מ / בס"מ | **cm** / **(in cm)** | |
| קמ"ש | **kph** | NOT "km/h", NOT "km per hour". Confirmed twice ("a speed of w kph", "moves at a speed of x kph"). |
| ק"מ | **km** | |
| מטרים | **meters** | |
| מ"ר | **cm²** / **m²** as applicable | Superscript form. |
| שניות | **seconds** |
| דקה ו-10 שניות | **1 minute and 10 seconds** |
| שעתיים | **two hours** |
| דולרים | **dollars** |

### 2.6 Geometry vocabulary

| Hebrew | English | Hebrew | English |
|---|---|---|---|
| ישרים מקבילים | parallel straight lines | מרובע | quadrilateral |
| ריבוע | square | מלבן | rectangle |
| משולש | triangle | משולש שווה שוקיים | isosceles triangle |
| מעגל | circle | עיגול | circle (disc) |
| רדיוס | radius | קוטר | diameter |
| קוטר המעגל | the diameter of the circle | היקף | perimeter / circumference |
| היקף הבסיס | base circumference | שטח | area |
| נפח | volume | משיק | tangent |
| קודקוד | vertex | צלע | side |
| צלעות | sides | אורכים | lengths |
| גליל | cylinder | תיבה | box (rectangular prism) |
| קובייה (solid) | cube | דלתון | deltoid |
| חסום ב- | inscribed in | משושה משוכלל | regular hexagon |
| ניצב | leg | יתר | hypotenuse |
| מערכת צירים | coordinate system | טרפז | trapezoid |
| זווית | angle | גובה | height / altitude |

Notes:
- `המעגל משיק לצלע DC ולהמשך הצלע BC` → **"The circle is tangent to side DC and to the continuation of side BC"**.
- `שטח המשולש ABC שווה לשטח המשולש DBC` → **"The area of triangle ABC equals the area of triangle DBC"** (no "the" before triangle names).
- Deltoid givens keep the parenthetical inline: `(GH = GJ , HI = JI)` — **spaces around the comma** inside coordinate/pair lists, matching NITE typography: `(0 , a)`, `(b , 0)`, `$(x , y)`, `A(0,7)` (the latter without spaces when it's a labeled point in a figure).

### 2.7 Probability / combinatorics / statistics

| Hebrew | Official English | Notes |
|---|---|---|
| קובייה (die/dice) | **dice** | Colloquial NITE usage — singular sense, still "dice". Confirmed: "then they toss a **dice**", "the result of tossing the **dice**". Never "die". |
| מטילים | **toss** | |
| מטבע | **coin** | |
| הסתברות | **probability** | |
| מה ההסתברות ש…? | **What is the probability that …?** | |
| ממוצע | **average** | |
| באופן מקרי / באקראי | **at random** | |
| זוגות | **pairs** | |
| בכמה דרכים שונות זו מזו …? | **In how many different ways can …?** | |
| ועד בכלל | **(inclusive)** | |

### 2.8 Absolute value and operator notation

- Absolute value bars are kept **as-is**, spaced exactly as the Hebrew: `| 3 | – | -5 | + | -12 | – a = 16`.
- Custom operators defined in-question are kept literally, including the `$` symbol:
  > For every two numbers a and b, the operation **$** is defined as: $(a , b) = 2 ∙ (a + b)

  → **This is why MathJax must NOT enable `$…$` as an inline delimiter.** Config must be `tex: { inlineMath: [['\\(', '\\)']] }` only.
- Multiplication dot in stems appears as `∙` (U+2219) or `·` (U+00B7); NITE uses both. Prefer `\cdot` inside MathJax, and `∙` in plain text where the original had it.
- `?=x` in RTL Hebrew is `x = ?` in English, on its own line.

### 2.9 Word-problem phrasing — zero simplification

Word problems preserve **full multi-clause structure**, clause order, and every parenthetical aside. Confirmed examples of the density to match:

> One hour before Idan entered the classroom, his watch stopped working (before it stopped working, the watch showed the correct time).
> Ten minutes before he entered the classroom, his watch began to work again.
> At the moment that he entered the classroom, his watch showed the (incorrect) time of 8:30.
>
> What was the correct time at the moment that Idan entered the classroom?

> Sagit is training in long-distance running.  Every time she runs, she runs at a speed of w kph during the first hour and at a speed of (w – 2) kph during the second hour.  At the end of each month of training, her speed w increases according to the following rule:
> w = 10 + x, with x being the number of full months of training that have elapsed since Sagit began training.
>
> After how many full months of training will Sagit manage to run 30 km in two hours?

Patterns to copy:
- `כאשר x הוא …` → **"with x being …"** (not "where x is").
- `לאחר כמה חודשי אימון שלמים …?` → **"After how many full months of training …?"** — "full months" preserved.
- Blank-completion stems keep the trailing period placement: `קומה X היא .` → **"The X floor is           ."** ; `גילו של נדב גדול פי ___ מגילה של מירב` → **"Nadav's age is           times as much as Merav's age."**
- `גדול פי 3 מ-` → **"3 times as much as"**.
- Ordinal floors: `קומה 8` → **"the 8th floor"** / option form **"(1) at the 8th floor"**.
- Hebrew elevator labels `מעלית א` / `מעלית ב` → **Elevator A** / **Elevator B** (Hebrew letters map to Latin A/B/C/D in order).
  **Collision case:** when the figure already uses Latin letters, mapping א→A would
  create two points with the same name. Use **X/Y/Z** for the Hebrew-lettered
  points instead, assigned in the original's RTL order (rightmost א→X), which keeps
  each question's numerator/denominator pointing at the same point it did in Hebrew.
  Precedent: Winter 2022 §1 Q6, where the start node is already a Latin "A".
- Hebrew names are transliterated, not localized: שגית → Sagit, עידן → Idan, נדב → Nadav, מירב → Merav, רונית → Ronit, שי → Shai, מיכל → Michal, אלישבע → Elisheva, בתיה → Batya, גאולה → Ge'ulah, דורית → Dorit, עודד → Oded.
  Use the name's conventional English spelling, not a letter-by-letter rendering
  (עודד is **Oded**, not "Odede"). A final ד/ת/ר takes no trailing vowel.
- **Watch RTL gender/role swaps**: `חוקרת` is a female researcher → "she"; `חברות` = female friends → "girls"; `שליח` → "a delivery person". Getting these backwards is a known failure mode when reading RTL.

### 2.10 Option formatting

```
(1) 110°
(2) 120°
```
- Number in parentheses, single space after. No trailing punctuation.
- Degrees use `°` directly attached to the numeral.
- Answer-key numbering is 1-based (`correct_answer` ∈ {1,2,3,4}).

---

## 3. Answer key

Location: near the end of the PDF, headed **`Answer Key`** (English) / **`מפתח תשובות נכונות`** (Hebrew).
- 2025 bilingual: PDF page **119**.
- 2024 bilingual: PDF page **111**.
- 2021 Hebrew-only: PDF page **59** (Hebrew table, `פרק ראשון- חשיבה כמותית` / `התשובה הנכונה`).

**Always read the key FIRST**, before deriving anything by hand.

Extraction:
```bash
python3 -c "import fitz; d=fitz.open('exam.pdf'); print(d[119].get_text())"
```

Keys already extracted (1-based option numbers, Q1→Q20):

| Exam | Section | Answers |
|---|---|---|
| Summer 2025 | Quant §1 | 2 3 3 4 4 3 3 2 3 2 3 2 1 4 2 2 1 4 1 1 |
| Summer 2025 | Quant §2 | 1 2 1 3 4 1 2 4 4 1 1 1 3 3 2 1 4 2 4 4 |
| Summer 2024 | Quant §1 | 3 4 1 1 1 3 4 1 2 3 2 2 3 2 4 1 4 1 4 1 |
| Summer 2024 | Quant §2 | 1 2 1 3 2 2 3 2 4 3 2 3 3 4 3 1 4 3 3 4 |
| **Autumn 2021** | **Quant §1** | **4 4 4 1 2 1 1 1 1 4 2 4 1 1 4 4 3 1 1 1** |
| **Autumn 2021** | **Quant §2** | **3 2 2 1 1 1 2 4 2 2 1 3 4 3 2 1 4 3 3 1** |

Also note NITE's disqualification wording, in case it appears next to an item:
> "this item was not used in the calculation of scores"

---

## 4. Phase-2 operational checklist (derived from the above)

1. Read the answer key page first; record all 40 answers.
2. Identify cluster boundaries (`שאלות ובעיות` vs `הסקה מתרשים`) — do not assume positions.
3. Translate with the glossary above; reuse §1 boilerplate verbatim.
4. During the *initial* pass, convert every `/` and `^` to MathJax `\(\frac{}{}\)` / `\(x^n\)`; use `\dfrac` for nested fractions. Re-scan for stray `/` before declaring a batch done.
5. Insert `\n\n` between givens/setup and the final question sentence.
6. Never introduce variables absent from the Hebrew; never pre-simplify; keep clause order.
7. Figures: crop originals (Latin-only figures → crop untouched; Hebrew-baked text → crop then PIL-patch only the confusing words, skip trivia like ס"מ→cm).
8. No worked solutions — `stem`, `options`, `correct_answer` only.
9. Full 20-question exams → `pool: "simulation"` only, never `"drill"`.

## 5. 2021 Hebrew exam — page map (for Phase 2)

`psychometric_autumn_2021_acc.pdf`, 63 pages, Hebrew only.
- Quant §1 (`פרק ראשון- חשיבה כמותית`): PDF pages **20–27**
- Quant §2 (`פרק שני- חשיבה כמותית`): PDF pages **28–35**
- Answer key (`מפתח תשובות נכונות`): PDF page **59**
