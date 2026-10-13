"""Non-destructive speech QA. Findings are review requests, never automatic cuts."""
import difflib
import hashlib
import json
import re
import wave
from pathlib import Path

VERSION = 1
DISCOURSE = {'and', 'so', 'now', 'okay', 'ok', 'right', 'yes', 'actually', 'just', "let's", "here's", 'this'}
MATH = set('abcdefghijklmnopqrstuvwxyz') | {'zero', 'one', 'two', 'three', 'four', 'five',
    'six', 'seven', 'eight', 'nine', 'ten', 'plus', 'minus', 'times', 'over', 'is', 'equals'}


def tokens(text):
    return re.findall(r"[a-z]+(?:'[a-z]+)?|\d+", text.lower().replace('’', "'"))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def findings(words, manifest, normalize=tokens, report=None, raw_words=None):
    """Use independent final-audio words, actual paragraph windows, and source joins.

    Short ASR ghosts, explanatory number repetitions and different-method repeats
    are deliberately not treated as certain editing mistakes.
    """
    lines = manifest['lines']; result = []
    expected = [normalize(l['text']) for l in lines]
    def owner(w):
        mid = (w['s'] + w['e']) / 2
        return next((i for i,l in enumerate(lines) if l['start']-.12 <= mid <= l['end']+.12), None)
    def add(kind, start, end, text, reason, **extra):
        item = dict(kind=kind, audio_start=round(start,3), audio_end=round(end,3),
                    text=text, reason=reason, confidence='candidate—not a proven error', **extra)
        item['id'] = hashlib.sha256(json.dumps([kind,item['audio_start'],item['audio_end'],text]).encode()).hexdigest()[:16]
        if not any(x['id']==item['id'] for x in result):result.append(item)
    # A stray 'by' after the answer in q-396 was only ONE word, and fell outside
    # both complete paragraph readings. The old >=3-word extra-run check missed it.
    fragments=[]
    for k,w in enumerate(words):
        ts=normalize(w['w'])
        if not ts or w.get('p',1)<.35 or w['e']-w['s']<.06:continue
        own=owner(w)
        if own is not None:continue
        closest=min(range(len(lines)),key=lambda i:min(abs(w['s']-lines[i]['end']),abs(w['e']-lines[i]['start'])))
        local=set(expected[closest])
        # Common bridges and words belonging to the neighbouring sentence can be
        # early/late timestamp estimates. Do not flag those on timing alone.
        neighbours=[i for i,l in enumerate(lines) if abs(l['start']-w['e'])<1.2 or abs(l['end']-w['s'])<1.2]
        allowed=set().union(*(set(expected[i]) for i in neighbours)) if neighbours else local
        if all(t in DISCOURSE or t in allowed for t in ts):continue
        fragments.append((w,closest))
    groups=[]
    for w,closest in fragments:
        if groups and w['s']-groups[-1][-1][0]['e']<.45:groups[-1].append((w,closest))
        else:groups.append([(w,closest)])
    for group in groups:
        add('transition_fragment',group[0][0]['s'],group[-1][0]['e'],' '.join(w['w']for w,i in group),
            'Speech outside the recorded paragraph windows; inspect the complete adjacent sentences before choosing boundaries.',
            paragraph=group[0][1]+1)
    # Immediate repeats: stay LOCAL to one paragraph and require independent,
    # substantial word intervals. A letter or number repeated in a calculation
    # is not a stutter. A 0.02 s duplicate token can be an ASR overlap artifact.
    flattened=[]
    for k,w in enumerate(words):
        for t in normalize(w['w']):flattened.append((t,k))
    hits=[]
    for i in range(len(flattened)):
        for n in range(6,0,-1):
            if i+2*n>len(flattened):continue
            aa=flattened[i:i+n];bb=flattened[i+n:i+2*n]
            if [t for t,k in aa]!=[t for t,k in bb]:continue
            inds=sorted(set(k for t,k in aa+bb));first=words[aa[0][1]];second=words[bb[0][1]];last=words[bb[-1][1]]
            if aa[-1][1]>=bb[0][1]:continue
            if second['s']-words[aa[-1][1]]['e']>1.2:continue
            if any(words[k].get('p',1)<.55 or words[k]['e']-words[k]['s']<.06 for k in inds):continue
            own=owner(first)
            if own is None or any(owner(words[k])!=own for k in inds):continue
            phrase=[t for t,k in aa]
            if n==1 and (phrase[0] in MATH or phrase[0].isdigit()):continue
            doubled=phrase+phrase
            if any(expected[own][j:j+2*n]==doubled for j in range(len(expected[own])-2*n+1)):continue
            if any(a<=i<b for a,b in hits):continue
            hits.append((i,i+2*n))
            add('local_repeat',first['s'],last['e'],' '.join(t for t,k in aa+bb),
                'Immediate repetition within one paragraph, not written twice in that paragraph. Review emphasis versus a failed start.',paragraph=own+1)
            break
    # Script mismatch is informational here: the teacher may paraphrase. Existing
    # verify.missing_sentences remains available separately; do not cut paraphrases.
    for prev,nxt in zip(words,words[1:]):
        gap=nxt['s']-prev['e']
        if gap>1.5:
            add('speech_gap',prev['e'],nxt['s'],prev['w']+' … '+nxt['w'],
                'Long interval without recognized words. Check waveform/source: it may contain speech missed by ASR, not silence.')
    if report:
        for missing in report.get('verify',{}).get('missing_sentences',[]):
            if len(normalize(missing['sentence']))<3:continue
            li=missing['line']-1
            if not 0<=li<len(lines):continue
            add('possible_missing_sentence',lines[li]['start'],lines[li]['end'],missing['sentence'],
                'Independent ASR did not match this script sentence. Check for a valid paraphrase or ASR omission before asking for a rerecord.',paragraph=li+1)
        for filler in report.get('verify',{}).get('fillers',[]):
            add('possible_filler',filler['t'],filler['t'],filler['word'],
                'Possible hesitation from independent ASR. Confirm in context; do not cut a hallucinated token.')
    if report and raw_words:
        joins=[(a,b)for a,b in report.get('cut_ranges',[]) if b-a>=.2]
        # Use original source times for the diagnostic; never confuse them with
        # clean/video times, particularly after a second round of edits.
        for a,b in joins:
            for w in raw_words:
                if w.get('p',1)<.7 or not .12<w['e']-w['s']<1.5:continue
                for edge,side in [(a,'start'),(b,'end')]:
                    if w['s']+.08<edge<w['e']-.08:
                        add('possible_word_clip',edge,edge,w['w'],
                            'Source cut falls inside an ASR word interval. Check source waveform and padding; ASR timestamps can be wrong.',
                            clock='original_source_audio',boundary=side,source_word_start=w['s'],source_word_end=w['e'])
    return sorted(result,key=lambda f:(f.get('clock','clean_audio'),f['audio_start'],f['kind']))


def evaluate(directory, words, normalize=tokens, report=None, raw_words=None):
    """Write a hash-bound report. Only explicit keep/resolved decisions unlock QA."""
    directory=Path(directory);man=json.loads((directory/'manifest.json').read_text())
    hashes={'audio_sha256':digest(directory/'clean.wav'),'manifest_sha256':digest(directory/'manifest.json')}
    issues=findings(words,man,normalize,report,raw_words)
    path=directory/'speech-review-decisions.json'
    decisions=json.loads(path.read_text()) if path.exists() else {}
    fresh=all(decisions.get(k)==v for k,v in hashes.items())
    approvals={x['id']:x for x in decisions.get('decisions',[]) if x.get('reason','').strip() and x.get('reviewer','').strip()} if fresh else {}
    for issue in issues:
        approval=approvals.get(issue['id'],{})
        issue['disposition']=approval.get('disposition','needs_review')
        if approval:issue['review_note']=approval['reason']
    pending=[x for x in issues if x['disposition'] not in ('keep','resolved')]
    result=dict(version=VERSION,**hashes,decisions_sha256=digest(path)if path.exists()else None,
                ready=not pending,pending_count=len(pending),findings=issues,
                policy='No automatic cuts. Review uncertain speech; preserve mathematical meaning and intentional separate methods.',
                timestamps='Audio times unless clock=original_source_audio. Add the renderer lead (pilot: 0.55 s) for MP4 time.')
    (directory/'speech-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    return result


def require_ready(directory):
    directory=Path(directory);p=directory/'speech-review.json'
    if not p.exists():raise RuntimeError('Speech review not run. Run reading_to_video.py VIDEO_ID --verify-only before export.')
    review=json.loads(p.read_text())
    decisions=directory/'speech-review-decisions.json'
    if review.get('version')!=VERSION or review.get('decisions_sha256')!=(digest(decisions)if decisions.exists()else None):
        raise RuntimeError('Speech review is stale: reviewer decisions or checker version changed. Re-run verification.')
    if review.get('audio_sha256')!=digest(directory/'clean.wav') or review.get('manifest_sha256')!=digest(directory/'manifest.json'):
        raise RuntimeError('Speech review is stale: audio or timing changed. Re-run verification.')
    if not review.get('ready'):raise RuntimeError('Speech review needs attention: inspect speech-review.json; no audio has been automatically cut.')
    return review


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('directory');parser.add_argument('--require-ready',action='store_true');args=parser.parse_args()
    if args.require_ready:require_ready(args.directory)
    else:
        p=Path(args.directory)
        result=evaluate(p,json.loads((p/'clean_transcript.json').read_text()),report=json.loads((p/'report.json').read_text()),
                        raw_words=json.loads((p/'transcript.json').read_text()) if (p/'transcript.json').exists() else None)
        print('Speech review:',result['pending_count'],'findings to review')
