"""Write a blind (no answers) copy of one or more originals files for the cold-solve check. Usage: mkblind.py GROUP [FILE...]"""
import json, sys
SP = '/private/tmp/claude-501/-Users-nitzanslasky/3900a95f-9e6b-4d5d-beea-3c24fc3dcf44/scratchpad/blind/'
G = sys.argv[1]; files = sys.argv[2:] or [G]
out = {'items': [], 'passages': []}
for f in files:
    d = json.load(open('/Users/nitzanslasky/psychometry-course/content/verbal_originals_%s.json' % f))
    out['items'] += [{k: x[k] for k in ('id', 'stem', 'options')} for x in d['items']]
    out['passages'] += [{'id': p['id'], 'paragraphs': p['paragraphs'], 'questions': [{'stem': q['stem'], 'options': q['options']} for q in p['questions']]} for p in d['passages']]
json.dump(out, open(SP + G + '.json', 'w'), indent=1, ensure_ascii=False)
print(G, len(out['items']), 'items', len(out['passages']), 'passages')
