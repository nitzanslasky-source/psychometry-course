"""w19_check.py vid... : W19 aid (pace + explain, no headlines). Flags, per sentence of the script she reads:
  SHORT  fewer than 5 words and no verb (a telegraphic fragment / bare result)
  LABEL  a label-style opener: one or two words and a colon ("Step one: ...")
  DENSE  more than 2 numbers or operations in one sentence (two new steps in one breath)
Heuristic only: judge each flag by hand."""
import sys, re, json, os
SB = '/Users/nitzanslasky/psychometry-course/studio-build'
NUM = r"(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|half|halves|third|quarter|\d+)"
OPS = r"\b(?:plus|minus|times|divided|over|squared|cubed|root|equals?|is)\b"
VERB = re.compile(r"\b(is|are|was|were|be|been|has|have|had|do|does|did|can|could|will|would|should|must|may|might|gives?|makes?|means?|take|takes|get|gets|go|goes|look|looks|see|find|found|cut|cuts|add|adds|subtract|divide|multiply|put|move|keep|say|says|works?|stays?|comes?|leaves?|lands?|meet|meets|need|needs|know|let's|let|check|choose|try|draw|drop|use|start|remember|think|is|isn't|aren't|don't|doesn't|can't|it's|that's|there's|here's|we're|they're|you're|what's|we'll|i'll)\b", re.I)
TAG = re.compile(r'\[[^\]]*\]')
def sentences(t):
    t = TAG.sub(' ', t); t = re.sub(r'\s+', ' ', t).strip()
    return [s.strip() for s in re.findall(r'[^.?!]+[.?!]?', t) if s.strip()]
def flags(vid):
    d = json.load(open(os.path.join(SB, 'ai_scripts', vid + '.json')))
    out = []; n = 0
    for si, sl in enumerate(d['slides']):
        for pi, l in enumerate(sl):
            n += 1; say = l if isinstance(l, str) else l['say']
            for s in sentences(say):
                w = re.findall(r"[A-Za-z']+|\d+", s); f = []
                if len(w) < 5 and not VERB.search(s): f.append('SHORT')
                if re.match(r"^\s*\w+(?: \w+)?:", s): f.append('LABEL')
                nn = len(re.findall(r'\b' + NUM + r'\b', s, re.I)); ops = len(re.findall(r"\b(?:plus|minus|times|divided by|squared|cubed)\b", s, re.I))
                if nn > 2 and ops >= 2: f.append('DENSE(%d nums, %d ops)' % (nn, ops))
                if f: out.append('%s P%d (%d.%d) %s: %s' % (vid, n, si + 1, pi + 1, '/'.join(f), s))
    return out
if __name__ == '__main__':
    tot = 0
    for v in sys.argv[1:]:
        for x in flags(v): print(x); tot += 1
    print('flags:', tot)
