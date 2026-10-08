"""Recorded videos that are CHANGED ON PURPOSE (teacher 2026-10-08: "In the ones I recorded it's OK to record again,
because it is crucial to learn it properly ... most important is that they learn it all properly and don't miss anything").

The 2026-10-08 "Hebrew points restored" pass bypasses the recording guard (_hebrew_back.recorded) for exactly these ids.
Every other recorded video stays untouched.

RERECORD[video id] = dict(topic=N, option=1|2|3, reason='...', added='...', minutes=..., since='YYYY-MM-DDTHH:MMZ')
    since = when the change went into the course (UTC); a take recorded AFTER it counts as done (studio_rerecord.py).
            Without it, the file's modification time is used - always add it to new entries.
    option 1 = lines/slides restored inside the recorded video -> re-record the whole video
    option 2 = new slide(s) appended at the END -> "Continue a take" from the old last slide
    option 3 = a short NEW video placed right after the recorded one (the recorded one itself is unchanged;
               listed here only so the teacher sees it next to the video it belongs to)
"""
RERECORD = {
    # ---- topics 7-12 (2026-10-08 Hebrew points restored)
    'solve-q-195': dict(topic=7, option=2, reason='lost Hebrew point: how to know whether to add or subtract (not common, practice, aim for the same coefficient)',
                        added='new last slide "Add or subtract?"', minutes=0.4, since='2026-10-08T07:50Z'),
    'solve-q-196': dict(topic=7, option=1, reason='lost Hebrew points: a rare type but worth knowing; write the 2xy LAST so x² + y² stay side by side',
                        added='one line on the title slide + one line on "Hidden formula"', minutes=1.4, since='2026-10-08T07:50Z'),
    'solve-q-249': dict(topic=10, option=1, reason='lost Hebrew points: only the same root can be added (apples and bananas); why a second method (the right split needs trial and error)',
                        added='one line on "Method 1 · Split into factors" + three lines at the start of "Method 2 · Common factor"', minutes=2.1, since='2026-10-08T07:50Z'),
    'solve-q-326': dict(topic=12, option=2, reason='lost Hebrew point: trial-and-error questions are very common in inequalities, often early in the section, hard by algebra but simple by plugging in',
                        added='new last slide "Trial and error"', minutes=0.3, since='2026-10-08T07:50Z'),
    'solve-q-328': dict(topic=12, option=2, reason='lost Hebrew points: second-degree inequalities are rare but important; the hardest part - check it with numbers (symmetry)',
                        added='new last slide "Rare - but know it"', minutes=0.5, since='2026-10-08T07:50Z'),
    # ---- topic 13 (2026-10-08 topic 13 restored + clearer; t13.py restore_and_clarify) ----
    'absolute-value': dict(topic=13, option=1, reason='the 2026-10-05 cut removed the Hebrew lesson theory: sign clues, equations (two cases, why the minus), inequalities (symmetric; big side open / small side closed and WHY; like x squared), the wrap-up (expression / equation / inequality, trial and error, harder and rarer, rewind)',
                           added='6 new slides after "When is it equal?": Sign clues, Equations, Two cases, Inequalities · big side, Inequalities · small side, Wrap-up; 4 shaded number lines (|x| = 5, |x − 2| = 6, |x| > 4, |x| < 4). Re-record the whole lesson (3.2 → 6.7 min, about +3.5 min)', minutes=6.7, since='2026-10-08T07:58Z'),
    'solve-q-358': dict(topic=13, option=1, reason='slide "The sign clues" repeated the four clues the lesson now teaches',
                        added='slide 3 removed; one line on "Decode the signs" names the sign clue from the lesson (1.8 → 1.4 min, about −24 s). Re-record the whole video', minutes=1.4, since='2026-10-08T07:58Z'),
    'solve-q-359': dict(topic=13, option=1, reason='clearer: a number line shows |x + 7| = 9 as 9 steps from −7 - two points, 2 and −16',
                        added='one number-line figure + one spoken line on "Two cases" (0.9 → 1.1 min, about +11 s). Re-record the whole video', minutes=1.1, since='2026-10-08T07:58Z'),
}
