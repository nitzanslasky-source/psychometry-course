"""Build the student dictionary (content/full-course/dictionary.json). English only — no translations.

Sources:
- content/sources/vocab_pdf.json — the approved "Psychometric Vocabulary" dictionary (430 words and expressions,
  parsed word-for-word from the teacher's PDF: definition, example, note, where it was seen in exams).
- studio-build/vocab_new_*.json — added words in the same style: vocabulary from the course's analogy questions,
  words glossed in real exams, and reading-passage terms.

    python3 studio-build/export_extras.py
"""
import glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'content', 'full-course', 'dictionary.json')

def key(w): return re.sub(r'[^a-z]', '', w.lower())

def main():
    out, seen = [], set()
    for x in json.load(open(os.path.join(ROOT, 'content', 'sources', 'vocab_pdf.json'), encoding='utf-8')):
        out.append(dict(w=x['w'], label=x['label'], def_=x['def_'], ex=x['ex'], note=x['note'], core=True))
        seen.add(key(x['w']))
    added = 0
    for f in sorted(glob.glob(os.path.join(ROOT, 'studio-build', 'vocab_new_*.json'))):
        for x in json.load(open(f, encoding='utf-8')):
            k = key(x['w'])
            if not k or k in seen: continue
            seen.add(k); added += 1
            out.append(dict(w=x['w'], label=x['label'], def_=x['def'], ex=x['ex'], note=x.get('note', '')))
    out.sort(key=lambda x: key(x['w']))
    res = []
    for x in out:
        e = dict(w=x['w'], label=x['label'], def_=x['def_'], ex=x['ex'])
        if x['note']: e['note'] = x['note']
        if x.get('core'): e['core'] = True
        res.append({('def' if k == 'def_' else k): v for k, v in e.items()})
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('dictionary:', len(res), 'entries (%d from the PDF, %d added) →' % (len(res) - added, added), OUT)

if __name__ == '__main__':
    main()
