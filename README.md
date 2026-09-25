# Psychometry Course — the complete course for first-time takers

> **This is a separate project.** It is *not* the elite platform (`~/nite-psychometry`, repo
> `nitzanslasky-source/psychometry`), which is for students retaking the exam (decks, elite questions,
> exam simulations, drills). The two have separate code, separate content and will be separate websites.
> Don't copy code or content between them without deciding to.

The full English course for the NITE psychometric entrance test — Quantitative Reasoning (Algebra, Word Problems,
Geometry) and Verbal Reasoning — from the first lesson to exam level: ~640 recorded video lessons, guided questions
with worked-solution videos, rules-to-know cards and practice.

## Two parts

| Folder | What it is | Who sees it |
|---|---|---|
| `studio-build/` | Builds the **Teacher Studio** (the recording app: slides, scripts, prompter, pen, camera). Output: `~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html` | Only the teacher |
| `src/`, `content/` | The **student website** (Next.js): the course with videos, questions, cards, practice | Paying students |

Nothing from the studio's scripts, slides or teacher notes reaches the student website.

## Workflow

```bash
# 1. Build the studio (after changing verbal modules or studio code)
cd studio-build && python3 build_verbal.py && python3 validate_v.py
python3 layoutcheck.py ~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html

# 2. Export the student course from the studio
python3 studio-build/export_student.py        # → content/full-course/

# 3. Run the student website
export PATH=$HOME/.local/node/bin:$PATH
npm install && npm run dev                    # http://localhost:3001
```

## Key facts

- `studio-build/base-v18.html` is the finished Algebra + Word Problems + Geometry studio (their original module
  sources were lost; changes to those subjects are made on this file). Verbal Reasoning is built from `modulesV*.py`.
- `studio-build/question_numbers.json` **locks** every guided question number. Recorded videos show these numbers,
  so they must never change; new questions get the next free number in their topic.
- Recordings are saved by the studio as `<Subject>/Topic NN - <title>/<videoId>-<timestamp>.webm`. The video id
  connects each recording to its lesson. `content/full-course/video-manifest.json` maps video id → hosted video;
  a video missing from the manifest shows "coming soon" on the website.
- Verbal questions come word-for-word from `content/verbal_bank_all.json` (see `studio-build/vbank.py`).
