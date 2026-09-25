"""Build the student site's extra content: the dictionary (content/full-course/dictionary.json).

Sources:
- content/sources/nite_gloss_he_en.json — English words with the Hebrew meaning NITE printed beside them in real exams
  (copied from the elite project's work/verbal folder).
- content/verbal_bank_all.json — English definitions from the reading-passage glossaries.

    python3 studio-build/export_extras.py
"""
import json, os, re
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'content', 'full-course', 'dictionary.json')

def key(w): return re.sub(r'\s+', ' ', w.strip().lower())

def main():
    words = OrderedDict()
    for x in json.load(open(os.path.join(ROOT, 'content', 'sources', 'nite_gloss_he_en.json'), encoding='utf-8')):
        en, he = x['en'].strip(), x['he'].strip()
        if not en or not he: continue
        e = words.setdefault(key(en), dict(en=en, he=[], def_='', years=set()))
        if he not in e['he']: e['he'].append(he)
        e['years'].add(str(x.get('exam', '')))
    bank = json.load(open(os.path.join(ROOT, 'content', 'verbal_bank_all.json'), encoding='utf-8'))
    for r in bank['reading_comprehension']:
        for part in re.split(r';\s*', (r.get('glossary') or '').strip().rstrip('.')):
            m = re.match(r'(.+?)\s+—\s+(.+)', part.strip())
            if not m: continue
            en, d = m.group(1).strip(), m.group(2).strip()
            e = words.setdefault(key(en), dict(en=en, he=[], def_='', years=set()))
            e['def_'] = e['def_'] or d
    out = []
    for e in words.values():
        item = dict(w=e['en'].strip('"“”\' '))
        if e['he']: item['he'] = ' · '.join(e['he'][:3])
        if e['def_']: item['def'] = e['def_']
        if any(y for y in e['years']): item['exam'] = True
        out.append(item)
    out.sort(key=lambda x: re.sub(r'[^a-z]', '', x['w'].lower()))
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('dictionary:', len(out), 'words →', OUT)

if __name__ == '__main__':
    main()
