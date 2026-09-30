# Quantitative terminology audit: course vs NITE's official English guide

This is a report only. No course file was changed.

**Official reference:** NITE English Quantitative Reasoning guide (`quantitive-eng-acc.pdf`, text in `.../3f894141/tmp/nite_quant_guide.txt`). Line numbers below (L###) point into that text. The report also checks `memory/nite-translation-style.md` and `~/nite-psychometry/reference/nite_terminology.md`, which were verified against bilingual exams.

**What was scanned:** the studio `window.COURSE` in `Psychometric-Teacher-Studio-v19-hybrid.html`, covering topics t1–t38, t51 and t52. That is 403 in-scope videos with beats/items/`say` lines, 1,500+ questions (stem, choices, explanation, set intros) and all memory cards linked from those topics. The student-site export (`content/full-course/topics/t*.json`) was cross-checked and shows the same patterns.

**Categories used in counts:**
- **spoken:** `say` lines.
- **screen:** slide text and titles.
- **card:** memory cards.
- **question:** stem, choices or explanation.
- **Stems:** the question ids whose stem or choices contain the term. These matter most, because they mirror exam text.
- Production notes (`draw`/`label`/`loads`/`nextCue`/`canvas`) are left out of the counts.

---

## 1. Real mismatches

| # | Concept | NITE's official wording (where) | Course wording found | Count | Example locations | Suggested fix |
|---|---|---|---|---|---|---|
| 1 | Divisibility | "evenly divisible", "**divisible by**"; "A factor … divides it evenly" (L303–313, L388–398). The exam glossary also has "divisible by". | "**X divides by Y**" used intransitively. This is a Hebrew calque of מתחלק ב־ and is not idiomatic English. | 240 in total: spoken 118, screen 26, card 22, question explanations 57 | t14 `primes` screen "A number divides by every combination of its prime factors"; t15 `divisibility` "the digit sum divides by 3"; t16 `consecutive-products` "n(n+1) always divides by 2"; cards `mem-primes`, `mem-divisibility`, `mem-products` (column head "Always divides by"), `mem-r26-t16-sums`; q-390, q-422, q-423, q-429, q-432, q-438 explanations. Heaviest in t14–t16 and t22. | Written text: "is divisible by" (or "Y divides X"). Spoken lines: same fix recommended, since this is a grammar calque and not a synonym. |
| 2 | Units digit | "**units digit**" (exam glossary §2.4, ספרת האחדות). The course itself uses it in q-428 and q-433. | "**ones digit(s)**" | 69 in total. **8 stems:** q-520, q-530, q-532, q-538, q-r26-t18-07, q-r26-t18-08, alg-extra-unit-t18-3-3, alg-extra-unit-t18-3-6 | t18 `digit-puzzles` screen "Check the ones digit"; card `mem-letters`; t28 | Change to "units digit" everywhere, stems first. "Last digit" (67 hits, t1/t15) is fine as a spoken aside. |
| 3 | Vertical angles | "**Vertical Angles** … each pair of non-adjacent angles are called **vertical angles**" (L968–975). The guide never says "vertically opposite". | "**vertically opposite**" | 9 in total. **1 stem:** geo31-g010 ("…is vertically opposite the interior angle at A") | t31 `solve-geo31-g010` (screen and spoken); explanations geo31-g031, geo31-foundation-p18, geo31-advanced-p12 | Use "vertical angles" (for example "…and the interior angle at A are vertical angles"). The main lesson (t30 `geo-001`, card `mem-lines-angles`) already says "vertical angles" (21 hits). |
| 4 | Angles at parallel lines | "**Corresponding Angles**" and "**Alternate Angles**", both named and defined with a **transversal** (L976–994). "**Adjacent supplementary angles**" (L961–966). | The t30 lesson and card never name corresponding or alternate angles. They teach "**Z shape**", "**U shape**" and "small angles / large angles". Explanations say "**Z-angles**". | Z/U/Z-angles: 20. Small/large angles: 67. "Corresponding/alternate" in t30: **0** (they appear only in t32–t37 explanations, 14 hits). | Card `mem-lines-angles` rows "Z shape", "U shape", "Bent line (Z-type bends)"; t30 `geo-001` slides "The U shape" and "Small and large angles"; card `mem-similar-triangles` "Z angles + vertical angles"; geo32-advanced-p05, geo32-advanced-p12, geo32-foundation-p04 "(Z-angles)" | Keep Z/U as memory aids, but add the official names on the t30 slide and card: "Z shape = **alternate angles** (equal)", "F shape / same position = **corresponding angles** (equal)", "adjacent angles on a straight line = **adjacent supplementary angles**". Replace "(Z-angles)" with "(alternate angles)" in the 3 explanations and the t36 card. |
| 5 | Kite / deltoid | Guide heading: "**Kite (Deltoid)**" (L1288). Real exam stems use "**deltoid**" (glossary §2.6: דלתון → deltoid, e.g. "(GH = GJ , HI = JI)"). | "kite" only. "deltoid" appears **0** times. | kite 105; deltoid 0 | Card `mem-quad-family` "Kite"; t32 and t33 lessons (`geo-077` "Two tangents: a kite") | Add "kite (**deltoid**)" on the quadrilaterals card and lesson slide, so a student who meets "deltoid" on the exam recognises it. |
| 6 | Contracted multiplication formulas | Formula page item 3: "**Contracted Multiplication Formulas**" (L64); guide section "CONTRACTED MULTIPLICATION FORMULAS" (L606) | "**short multiplication formulas**" (Hebrew calque of כפל מקוצר), "multiplication formulas", "special products". "Contracted" appears **0** times. | 33 (spoken 26, screen 2, card 2) | t4 `expression-basics` "the three short multiplication formulas"; card `mem-formulas` title "Multiplication formulas"; card `mem-products` and t1 `r26-t01-summary-fast` "Special products" | Title the card and slide "Contracted multiplication formulas" (the name on the formula page). Change "short multiplication" in speech too, since it is a calque. |
| 7 | Chart-question cluster names and intro | "**Graph Comprehension**" / "**Table Comprehension**"; "Study the **graph** below, then answer the four questions that follow." (guide L10–15, L2302–2303, L2510–2511; glossary §1.5) | Neither official name is ever used (**0**). t52 calls them "chart set", "chart questions" and "drawing conclusions from a chart". **10 practice sets** open with "Study the **chart(s)** below". | 0 official; "Study the chart(s)" in 10 sets (88 question records); "chart set" 8 | Sets chp01, 02, 03, 05, 11, 14, 19 ("Study the chart below") and chp13, 17, 20 ("Study the charts below"); t52 `ch52-intro` slide "The chart set" | Set intros: "Study the graph below, then answer the N questions that follow." In `ch52-intro`, name the two exam headings, "Graph Comprehension" and "Table Comprehension". |
| 8 | Chart key | "**key**" and never "legend" (glossary §2.1: מקרא → key, "(see key)") | "**legend**", "(see legend)" | 106 in total: question 78 across **8 sets**, spoken 13, screen 8, card 1 | Stems of chp01, 03, 05, 11, 14, 15, 19, 20 ("(see legend)", "Legend:" in figures); t52 `ch52-scatter` slide "The legend", `ch52-bar`, `ch52-line`; card `mem-ch52-chart-types` | Use "key" and "(see key)" in stems and figure labels. Spoken lines can say "the key (legend)" once, then "key". chp09 already says "(see the key)". |
| 9 | Dice verb | "**toss** a die/coin" (guide L621–628, L749–759, L818); exams: "toss a dice" (glossary §2.7) | "dice … **rolled**" | **13 stems:** pt-q05, wp28-p18, wp29-g152, g154, g156, g160, p03, p05, p08, p11, p13, p16, p21 | wp29-p03 "Two fair eight-sided dice … are rolled" | Change to "tossed" (for example "Two fair dice … are tossed"). Coins are already "tossed". |
| 10 | Speed unit | "**kph**" (guide L889; glossary §2.5 "NOT km/h, NOT km per hour") | "km per hour", "km/h" | 25 in t27: screen 10, question 5 | t27 `wp-106` slides "20 km per hour" and "A cyclist rides … 15 km per hour"; `wp-113`; `solve-wp27-g121`, `solve-wp27-g114`; wp27-p09 table header "Speed (km per hour)"; wp27-g109 rows "72 km per hour"; q-r26-t27-03 | Use "kph" on screen and in questions, as the other 113 question hits already do. Spoken "kilometers per hour" is fine. |
| 11 | Inscribed angle and its arc | "Inscribed angles **intercepting** the same arc"; "both of which **intercept** arc AB" (L1363–1376) | "**rests on** the arc" and "stands on the arc" (calque of נשענת על), "inscribed angle **on** arc AF" | rests/stands on: 16 (screen 2, card 1). "Angle on (the same) arc": 32 | t33 `geo-074` slide "Rests on an arc" and "The angle rests on the arc you can see from its vertex"; card `mem-circle-rules` "when both rest on the same arc", "inscribed angles on the same arc"; geo33-advanced-p05, geo33-g098 explanations | Use "intercepts / intercepting the same arc" on screen, on cards and in explanations. The spoken line in geo-074 already says "In English: it intercepts the arc", so make that word the main one. |
| 12 | Circle vs "disk" | The guide uses "circle" for the region too ("area of a circle", L1359). Glossary: עיגול → "circle (disc)". | "**disk(s)**" in stems. The t33 lesson teaches a circle-vs-disk distinction that NITE does not make. | 94 in total. **16 stems:** geo33-g099, geo33-advanced-p04, p27, geo33-foundation-p02, p25, geo34-core-p10, p19, p20, geo36-core-p07, p10, p13, geo36-g138, g147, geo38-core-p11, p12, p27 | geo33-g099 "area of the union of the two disks"; t33 `geo-074` slide "Circle and disk" | In stems write "circle(s)" (for example "the area common to both circles"). Keep at most one spoken aside about disks. |
| 13 | Formula-page wording for triangle height | "altitude to the base" (formula page 8a, L79–81); "Altitude of a Triangle" (L1017); trapezoid and parallelogram also use "altitude" (L1240, L1271) | "**height to that side**" on the main area slide and card | 28 "height to" (screen 4, card 2, question 2) | t31 `geo-016` slide "Area = side × height to that side / 2"; card `mem-triangle-area` "height to it"; t34 `geo-105` "Triangle: side × height / 2" | On the formula slide and card, write "altitude to that side (height)". Spoken "height" is fine (see §3). |
| 14 | Lateral surface area | "**lateral surface area**" (formula page 14a, L136; L1477, L1530) | "**lateral area**" | 25 (spoken 14, screen 5, card 2) | t35 `geo-119` slide "Lateral area = perimeter of the base × height"; card `mem-solids` column head "Lateral area" | Screen and card: "lateral surface area". Stems already use the official form (geo35-g124, geo35-core-p22). |
| 15 | Isosceles right triangle | "**isosceles right triangle**" (L1161) | "**right isosceles** triangle", "right and isosceles" | 27 in total. **7 stems:** geo31-advanced-p02, p22, geo31-foundation-p27, geo34-core-p25, geo38-core-p06, p16, q-r26-t34-10 | t31 `geo-027-after` slide "Right and isosceles"; t32 `solve-geo32-g053` title | Stems and titles: "isosceles right triangle". |
| 16 | Box | "**Box (Rectangular Prism)**"; "A box is…" (formula page 13, L129; L1458) | "**rectangular box**" | **12 stems** in t35: geo35-g121, g123, g126, g131, geo35-core-p03, p06, p08, p12, p18, p21, p23, p27 | geo35-g131 "placed in a rectangular box with internal dimensions…" | Stems: "box". Low priority, because the meaning is clear. |

---

## 2. Spoken only, optional

In each case the official term is also taught, so the informal word in speech is acceptable.

| Informal (spoken) | Official | Count | Where it is also written | Note |
|---|---|---|---|---|
| "golden triangle" (30-60-90) / "silver triangle" (45-45-90) | "right triangle whose angles measure 30°, 60°, 90°" (formula page 8c); "isosceles right triangle" (L1161) | 101 (spoken 76, screen 9, card 3, 1 explanation) | Card `mem-special-right` labels "(golden)" and "(silver)"; solve-video titles "A golden triangle" and "Golden triangle · partial calculation" (t33); card `mem-polygon-area` "4 silver triangles"; geo35-g128 explanation | This is an Israeli prep nickname NITE never uses. The main slide titles are correct ("The 30°-60°-90° Triangle"). Suggestion: change the solve-video titles, the `mem-polygon-area` row and the geo35-g128 explanation to the degree names, and keep the nickname in speech. |
| "Pythagoras" | "Pythagorean theorem" (formula page 8b) | 95 (spoken 56, screen 16, card 6, question 3) | Slides "Distance, then Pythagoras" and "Pythagoras, then area"; cards `mem-quad-area` and `mem-coordinates` | Fine in speech. Change screen titles and card text to "the Pythagorean theorem". |
| "height" for triangles, trapezoids and parallelograms | "altitude" | many; "height to" 28 | see #13 | Fine in speech. |
| "adjacent angles (on a straight line)" | "adjacent supplementary angles" (L961) | 32 | card `mem-lines-angles` | Add the official label once (see #4). |
| "numbers in a row" (for consecutive) | "consecutive numbers" (L297–302) | 54 (7 in explanations) | t16 slides "Two in a row", "Three in a row → divides by 6"; card `mem-r26-t15-tools` | "Consecutive" is taught (185 hits), so this is fine as a spoken aid. The t16 slide titles could say "Two consecutive integers". |
| "formula sheet" | "Formula Page" (L24) | 5 (t34 `geo-104`, t51 `solve-pt-q04`, card `mem-polygons`) | slide title "The formula sheet" | "Formula page" is already used 11 times. Make it consistent. |
| "last digit" | "units digit" | 67 | t1 slide "Last digit"; t15 "Divisible by 2: the last digit is even" | Fine as plain English. Use "units digit" wherever it is a named concept. |
| "natural number" | not in the guide or the exam files; exams say "positive integer" | 14 | card `mem-definitions` row "Natural number / positive integer"; **q-037 choice** "It is a natural number" | Put "positive integer" first on the card, and reword the q-037 choice to "It is a positive integer". |

---

## 3. Already consistent

These terms match NITE's wording and need no change.

- **Integer** and "positive integer" (course definition matches L285–294). The "0 / 1" general comments are quoted verbatim in card `mem-definitions` and t1 `numbers`.
- **Even / odd** (defined on integers only), **prime number**, "0 is even", "1 is not prime", "neither positive nor negative".
- **Opposite numbers** and **reciprocals** (the guide's exact pair of terms, L315–338). **Absolute value** (120 hits, "distance from zero"). The **number line** is always "number line", never "number axis".
- **Factor / divisor**, which the course explicitly equates ("Divisor = factor", as in guide L387 "FACTORS (DIVISORS)"). **Multiple**, **prime factor**, **common factor**, **remainder**, **consecutive**.
- **Numerator / denominator**, **common denominator**, **reduce**, **mixed number** and **percent**.
- **Average**: "average" is the main term, and "arithmetic mean" is explained once (t25 `wp-080`), exactly as guide L485–488 says. **Weighted average** matches L499. "Median" is used only in the triangle sense in t30–t38, and statistically only in chp20, where the stem defines it.
- **Power / exponent / base / root / square root / cube root**, and the positive root of √a.
- **Factorial**, **arrangements**, **without replacement**, **at random**, **probability**, **fair coin / fair dice**, **independent**.
- **Trapezoid** is used 240 times and "trapezium" never. **Rectangle, square, parallelogram, rhombus, diagonal, perimeter, isosceles, equilateral, legs, hypotenuse, median, angle bisector** ("perpendicular bisector" appears only once, correctly, in a geo38 explanation), **exterior angle, interior angles, straight angle, right / acute / obtuse angle, transversal, congruent, similar**.
- **Circle terms:** radius, diameter, chord, arc, minor arc, **sector**, **circumference** (never "perimeter of a circle"), **central angle**, **inscribed angle**, **tangent**, **point of tangency**, inscribed in / circumscribed about.
- **Polygon terms:** regular polygon, n-sided polygon, sum of the interior angles.
- **Solids:** cube, cylinder, cone, prism, pyramid, **edge**, **face**, **vertex**, **apex** (L1541), **surface area**, **volume**, "cm³".
- **Coordinate terms:** coordinate system / coordinate plane (both appear in the guide, L1567 and L1573), x-axis / y-axis, **origin**, **quadrants**, coordinates.
- **Stem boilerplate:**
  - "In the accompanying figure" (114 hits).
  - "It cannot be determined from the information given." (49 hits).
  - "Which of the following is necessarily true?" (170 hits).
  - Lowercase "cannot".
  - "Given:".
  - "Note: In answering each question, disregard the information appearing in the other questions." (all t52 sets).
  - "kph" in 113 of 116 question uses.
  - "not necessarily drawn to scale".

---

## 4. Ambiguous or for your judgement

1. **"whole number"**, 118 hits including **4 stems** (alg-extra-root-practice-7, wp21-p23, wp23-p03, geo34-core-p18).
   - The guide explicitly allows it: "An integer, also called a whole number" (L291).
   - Real exam stems, however, always say "integer". Suggest "integer / positive integer" in those 4 stems. Explanations and speech can stay.
2. **"die" vs "dice" (singular).** The guide says "a die" (L621), but real exams print "a dice" (glossary §2.7). The course uses "dice" in stems (matching exams) and "die" in speech. No change is needed.
3. **Chart-type names in t52.**
   - The guide names only "bar chart, line graph or scatter plot" (L16).
   - The course uses "Points on axes" for the scatter plot and "circle chart" (15 hits) for the pie chart. Neither can be verified against a NITE text.
   - Suggestion: mention "scatter plot" once on the card. Leave "circle chart" unless it can be checked against a bilingual exam graph.
4. **Slope.** Not in the guide at all, but the course teaches it (t37 `geo-159`, 66 hits). It is a solving tool rather than exam wording, so it is fine. Just note that exam stems will not use the word.
5. **"Based on the information in the accompanying figure, …"** (6 t30 stems: geo30-foundation-p01, p02, p03, p12, geo30-advanced-p04, p08). The official template is "Based on the information in the figure," (glossary §2.1). This is a minor polish.
6. **"where x is …"** (2 stems: q-376, q-r26-t38-05). The glossary prefers "with x being …". This is minor.
7. **"rhombi"** (17) vs the guide's "rhombuses" (L1229). Both are correct English. Optional.
8. **"percent change" / "change in percent"** (10, slide titles in t23 and t36) vs the guide's "percentage of change" (L2520). Optional.
9. **Congruence criteria.** The guide names SAS / ASA / SSS / SSA (L1079–1100), and the course never names them (0 hits). This is a coverage point, not a wording mismatch. Worth a look only if congruence questions matter.
10. **"GCD / LCM", "inverse proportion", "complement".** These are standard English and not in the guide. They do not conflict with it, so no action is needed.
