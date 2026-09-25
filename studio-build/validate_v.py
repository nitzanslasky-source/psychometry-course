"""Script checks for verbal modules: answers, pop-ins, sidebars, title slides, pre-loaded questions."""
import glob, importlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vbank
BQ, POOLS, BP, RC = vbank.questions()
import json
C = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'course18.json')))
QS = dict(C['questions']); QS.update(BQ)
WORDS = {w: n for n, w in enumerate('zero one two three four'.split())}
probs, n = [], 0
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modulesV*.py'))):
    name = os.path.basename(f)[:-3]
    for m in importlib.import_module(name).MODULES:
        n += 1; tag = '%s %s' % (name, m['id'])
        sb = m['sidebar']
        if len(sb) > 13: probs.append(tag + ' | sidebar has %d items' % len(sb))
        for x in sb:
            if len(x) > 22: probs.append(tag + ' | sidebar label too long: ' + x)
        if m['slides'][0]['mode'] != 'title': probs.append(tag + ' | first slide is not a title slide')
        for sl in m['slides']:
            if sl['mode'] == 'title' and (sl.get('pre') or any(not isinstance(x, str) for x in sl['script'])):
                probs.append(tag + ' | title slide must be clean (no items / pop-ins / draws)')
            if sl['mode'] == 'question' and not sl.get('pre'): probs.append(tag + ' | question slide without pre-loaded question')
            for x in sl['script']:
                if isinstance(x, tuple) and x[0] == 'A' and not isinstance(x[2], dict): probs.append(tag + ' | APPEAR without item')
        if m.get('guided'):
            q = QS.get(m['qid'])
            if not q: probs.append(tag + ' | unknown question ' + m['qid']); continue
            ans = q['correct'][0] + 1
            for sl in m['slides']:
                for x in sl['script']:
                    t = x if isinstance(x, str) else x[1]
                    for mm in re.finditer(r'Circle choice (\d)', t):
                        if int(mm.group(1)) != ans: probs.append(tag + ' | "%s" but the answer is %d' % (mm.group(0), ans))
                    for mm in re.finditer(r'\b[Cc]hoice (\d|one|two|three|four)\.', t if isinstance(x, str) else ''):
                        v = int(mm.group(1)) if mm.group(1).isdigit() else WORDS[mm.group(1)]
                        if v != ans and re.search(r'(answer|correct|mark|circle|so it\'s|that\'s)', t, re.I) and len(t) < 60:
                            probs.append(tag + ' | spoken "%s" but the answer is %d' % (mm.group(0), ans))
            if not any('Circle choice' in (x[1] if isinstance(x, tuple) else '') for sl in m['slides'] for x in sl['script']):
                probs.append(tag + ' | no "Circle choice N" draw step')
print('SCRIPT CHECKS: %d modules, %d problems' % (n, len(probs)))
for p in probs: print(p)
