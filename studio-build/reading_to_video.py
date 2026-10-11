"""reading_to_video.py <videoId> [...] : the teacher's own reading (Reading Studio) -> clean audio + auto-narrate cues.

2026-10-11: the teacher reads the AI scripts herself, audio only, in the Reading Studio (reading_studio.py). Each take is
~/Documents/Course.recordings/_reading/<videoId>/<videoId>-<time>Z.wav (48 kHz mono) + a sidecar .json:
  paragraphs      [{i, text}]  = the script lines she read (ai_scripts/<videoId>.json, tags dropped), in order
  paragraphStarts [{para, t, how}]  when each paragraph was reached (how: start / para / back / jump ...)
  mistakes        [{t, para, text}] "M": "I stumbled, I repeat this sentence" - the take of that sentence before t goes
  pauses          [{at}]  the recording was paused there (the WAV has the pause removed: a join point)
Times are seconds in the WAV.

What this does (run it with the Python that has faster-whisper + numpy, e.g. the stt venv):
  1. transcribe (faster-whisper medium.en, word timestamps, VAD, no prompt)  -> <out>/transcript.json (cached)
  2. align her words to the script words (dynamic programming; on a tie the LATER reading wins, so the last attempt of
     a sentence / of a paragraph she went back to is the one kept). An extra stretch of her words that is not in the
     script is CUT when it is a restart (its words are re-read right after it), a filler (um / uh / er), or when a
     mistake mark falls in it / right after it; any other extra words are her own rewording and are KEPT (reported).
     Before the first script word and after the last one: cut.
  3. silences capped at 0.7 s (0.9 s at a slide change = method change); her shorter pauses stay. Cuts at the
     lowest-energy 10 ms point near the boundary, 15 ms crossfades. Gentle 70 Hz high-pass, loudness -16 LUFS (two-pass
     linear loudnorm, no compression, no denoise).
  4. cues: every script word gets her time (a script word she did not say gets the time between its neighbours), and
     ai_narrate.remap() turns ai_scripts/<videoId>.json's `at` phrases into the manifest the studio's auto-narrate plays
     -> ~/Documents/Course.recordings/_voice_real/<videoId>/ audio.mp3, alignment.json, manifest.json, clean.wav,
     report.json (the AI-voice files in _ai_audio/ are not touched). Record with run_an.py and AUD_ROOT pointing there.
"""
import difflib, json, os, re, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_argv = sys.argv[:]; sys.argv = ['x']
import ai_narrate as A
from reading_studio import covered as rs_covered, sentences as rs_sentences
sys.argv = _argv
REC = os.path.expanduser('~/Documents/Course.recordings')
IN, OUTROOT = os.path.join(REC, '_reading'), os.path.join(REC, '_voice_real')
SR = 48000
CAP, CAP_SLIDE, FADE = 0.7, 0.9, 0.015
FILLERS = {'um', 'uh', 'er', 'erm', 'hmm', 'mm', 'ah', 'eh'}
ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = 'x x twenty thirty forty fifty sixty seventy eighty ninety'.split()


def num_words(n):
    n = int(n)
    if n < 0: return 'negative ' + num_words(-n)
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ('' if n % 10 == 0 else ' ' + ONES[n % 10])
    if n < 1000: return ONES[n // 100] + ' hundred' + ('' if n % 100 == 0 else ' ' + num_words(n % 100))
    return str(n)


def norm_tokens(t):
    """text -> comparable tokens (numbers as words, symbols as words)"""
    t = t.replace('−', '-').replace('–', '-').replace('—', ' ')
    t = re.sub(r'(?<![\w])-(\d)', r' negative \1', t)
    t = t.replace('+', ' plus ').replace('=', ' equals ').replace('<', ' less than ').replace('>', ' more than ')
    t = re.sub(r'(\d+)\s*/\s*(\d+)', r'\1 over \2', t)
    t = re.sub(r'\d+', lambda m: ' ' + num_words(m.group(0)) + ' ', t)
    t = t.lower().replace("’", "'")
    out = []
    for w in re.findall(r"[a-z']+", t):
        w = w.strip("'")
        if w: out.append(w)
    return out


EQUIV = {'equals': 'is', 'equal': 'is', 'minus': 'negative', 'okay': 'ok', 'ok': 'ok', 'aaand': 'and', "it's": 'its',
         'smaller': 'less', 'bigger': 'more', 'greater': 'more'}


def same(a, b):
    if a == b: return True
    a2, b2 = EQUIV.get(a, a), EQUIV.get(b, b)
    if a2 == b2: return True
    return len(a) > 3 and len(b) > 3 and difflib.SequenceMatcher(None, a, b).ratio() >= .8


# ------------------------------------------------------------------------------------------------ 1. transcribe
def transcribe(wav, out, script_text, name='transcript.json'):
    p = os.path.join(out, name)
    if os.path.exists(p): return json.load(open(p))
    from faster_whisper import WhisperModel
    m = WhisperModel(os.environ.get('WHISPER', 'medium.en'), device='cpu', compute_type='int8')
    # no script prompt: with the script as initial_prompt whisper SKIPPED 20+ s stretches it "already knew" (q-360 test);
    # VAD keeps long silences from derailing it
    segs, _ = m.transcribe(wav, beam_size=5, word_timestamps=True, condition_on_previous_text=False, vad_filter=True)
    words = [{'w': w.word.strip(), 's': round(w.start, 3), 'e': round(w.end, 3), 'p': round(w.probability, 3)} for s in segs for w in s.words]
    json.dump(words, open(p, 'w'), ensure_ascii=False)
    return words


def transcribe_chunks(wav, p, step=28.0, over=2.0):
    """for checking only: 30 s windows (2 s overlap), no VAD - whisper's long-form mode silently skipped whole stretches"""
    from faster_whisper import WhisperModel
    m = WhisperModel(os.environ.get('WHISPER', 'medium.en'), device='cpu', compute_type='int8')
    y = read_wav(wav); T = len(y) / SR; words, t = [], 0.0
    while t < T:
        seg = y[int(t * SR):int(min(T, t + step + over) * SR)]
        if len(seg) < SR * .5: break
        seg = seg[:len(seg) // 3 * 3].reshape(-1, 3).mean(axis=1).astype('float32')     # 48 kHz -> the 16 kHz whisper expects
        ss, _ = m.transcribe(seg, beam_size=5, word_timestamps=True, condition_on_previous_text=False, vad_filter=False, language='en')
        for s_ in ss:
            for w in s_.words:
                a_, b_ = w.start + t, w.end + t
                if words and a_ < words[-1]['e'] - .05: continue          # already have it from the previous window
                if t > 0 and w.start < over * .5: continue
                words.append({'w': w.word.strip(), 's': round(a_, 3), 'e': round(b_, 3), 'p': round(w.probability, 3)})
        t += step
    json.dump(words, open(p, 'w'), ensure_ascii=False)
    return words


# ------------------------------------------------------------------------------------------------ 2. align
def align(S, W):
    """S: script tokens, W: her tokens -> list of (i, j) pairs (i script idx or None, j her idx or None) in order.
    Costs: match 0, substitution 1, a script word she did not say .9, an extra word of hers .5. Backtracking from the
    end prefers a match, so with two readings of the same words the LATER one is matched."""
    n, m = len(S), len(W)
    INS, DEL, SUB = .5, .9, 1.0
    D = np.zeros((n + 1, m + 1), dtype=np.float32)
    D[1:, 0] = np.arange(1, n + 1) * DEL; D[0, 1:] = np.arange(1, m + 1) * INS
    eq = np.array([[same(S[i], W[j]) for j in range(m)] for i in range(n)], dtype=bool)
    for i in range(1, n + 1):
        row, prev, e = D[i], D[i - 1], eq[i - 1]
        diag = prev[:-1] + np.where(e, 0, SUB)
        up = prev[1:] + DEL
        best = np.minimum(diag, up)
        # left (insertion) must be done sequentially
        r = row; r[0] = D[i - 1, 0] + DEL
        for j in range(1, m + 1):
            v = best[j - 1]; w = r[j - 1] + INS
            r[j] = v if v <= w else w
    out = []; i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and abs(D[i, j] - (D[i - 1, j - 1] + (0 if eq[i - 1, j - 1] else SUB))) < 1e-4 and eq[i - 1, j - 1]:
            out.append((i - 1, j - 1)); i -= 1; j -= 1
        elif j > 0 and abs(D[i, j] - (D[i, j - 1] + INS)) < 1e-4:
            out.append((None, j - 1)); j -= 1
        elif i > 0 and j > 0 and abs(D[i, j] - (D[i - 1, j - 1] + SUB)) < 1e-4:
            out.append((i - 1, j - 1)); i -= 1; j -= 1
        else:
            out.append((i - 1, None)); i -= 1
    return out[::-1], eq


def back_to_start(W, Wt, a, b, t0, look=20.0):
    """a restart: her words a..b-1 are cut and she re-reads from b. If the re-read starts with words she ALSO said just
    before a (the failed attempt began earlier, and the aligner matched its first words), move the cut start back to
    where the failed attempt began: the latest p < a, within `look` s, where her words p.. match the words from b."""
    X = W[b:b + 4]
    if len(X) < 2: return a
    best = a
    for p in range(a - 1, -1, -1):
        if t0 - Wt[p][0] > look: break
        k = 0
        while k < len(X) and p + k < a and same(W[p + k], X[k]): k += 1
        if k >= min(3, len(X)) and p + k <= a: best = p
    return best


def mark_cuts(W, Wt, marks, words, floor=None):
    """each mistake mark at t: she re-reads a sentence right after it. The repeat starts at her first word after t; the
    failed attempt is the latest earlier place (within 25 s) where she said the same first words -> cut [failed, repeat)."""
    out = []
    for t in marks:
        lo = (floor or {}).get(t, t - 25)          # never reach back before the start of the paragraph she was reading
        r = next((j for j in range(len(W)) if Wt[j][0] >= t - .05), None)
        if r is None or r + 2 >= len(W): continue
        X = W[r:r + 6]; best = None
        for p in range(r - 1, -1, -1):
            if Wt[r][0] - Wt[p][0] > 60 or Wt[p][0] < lo - 1.0: break
            if not (same(W[p], X[0]) or (len(X) > 1 and same(W[p], X[1]))): continue
            Y = W[p:min(r, p + len(X) + 2)]       # her words there, a little longer (she may add a word: "how exactly do")
            hit = sum(bl.size for bl in difflib.SequenceMatcher(None, X, Y, autojunk=False).get_matching_blocks())
            if hit >= max(3, int(.66 * len(X))):
                best = p
                while best > 0 and same(W[best - 1], X[0]) and not same(W[best], X[0]): best -= 1   # "negative | 16 is there"
                break
        if best is None:                          # no same first words: the failed attempt is the sentence she was in
            for p in range(r - 1, -1, -1):
                if Wt[p][0] < lo - .5 or Wt[r][0] - Wt[p][0] > 20: break
                prev_w = words[Wt[p - 1][2]]['w'] if p > 0 else '.'
                if prev_w.rstrip().endswith(('.', '?', '!')) and Wt[p][2] != Wt[p - 1][2]: best = p; break
        if best is not None: out.append((Wt[best][0], Wt[r][0], t))
    return out


# ------------------------------------------------------------------------------------------------ audio helpers
def read_wav(p):
    w = wave.open(p); assert w.getframerate() == SR and w.getnchannels() == 1, p
    return np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype('float32') / 32768


def frames_db(y, fr=480):
    n = len(y) // fr
    e = np.sqrt(np.mean(y[:n * fr].reshape(n, fr) ** 2, axis=1) + 1e-12)
    return 20 * np.log10(e)


def low_point(db, t, lo, hi):
    """the quietest 10 ms frame time within [t+lo, t+hi]"""
    a, b = max(0, int((t + lo) * 100)), min(len(db) - 1, int((t + hi) * 100))
    if b <= a: return t
    k = a + int(np.argmin(db[a:b + 1]))
    return k / 100.0 + .005


# ------------------------------------------------------------------------------------------------ patch takes
def splice_patches(vid, base, side, y, words, lines, out):
    """PATCH takes (<vid>-patch-<time>.wav, sidecar kind 'patch', paragraphs [{i, text}]): she re-read single paragraphs
    of the CURRENT script. For each paragraph the newest patch that really contains it (its words match the paragraph)
    replaces that paragraph of the full take: the full take's audio from the end of her last word before she reached
    the paragraph to just before her first word of the next paragraph is swapped for the patch's audio. Her marks in
    the patch come along (shifted), so the patch is cleaned like the rest. -> y, words, side (marks, paragraph starts
    shifted), {paragraph index: patch file}"""
    d = os.path.dirname(base)
    pts = sorted(f for f in os.listdir(d) if f.endswith('.wav') and '-patch-' in f)
    newest = {}
    for f in pts:                                    # oldest -> newest: later ones win
        ps_ = json.load(open(os.path.join(d, f[:-4] + '.json')))
        pw = transcribe(os.path.join(d, f), out, '', 'patch-' + f[:-4].split('-patch-')[1] + '.json')
        toks = [t for w in pw for t in norm_tokens(w['w'])]
        for p in ps_['paragraphs']:
            st = norm_tokens(lines[p['i']])
            sm = difflib.SequenceMatcher(None, st, toks, autojunk=False)
            got = sum(bl.size for bl in sm.get_matching_blocks())
            if got >= .6 * len(st): newest[p['i']] = (f, ps_, pw)       # she read it (mostly) in this take
    if not newest: return y, words, side, {}
    # paragraph regions of the full take, from her Space presses (the last time she reached each paragraph)
    starts = side.get('paragraphStarts', [])
    def reached(i):
        ts = [q['t'] for q in starts if q['para'] == i]
        return max(ts) if ts else None
    patched = {}
    for i in sorted(newest, reverse=True):        # from the end, so earlier times stay valid
        f, ps_, pw = newest[i]
        t_a = reached(i); nxt = [q['t'] for q in starts if q['t'] > (t_a or 0) and q['para'] != i]
        if t_a is None: continue
        t_b = min(nxt) if nxt else len(y) / SR
        before = [w for w in words if w['e'] <= t_a + .3]; after = [w for w in words if w['s'] >= t_b - .05]
        a = (before[-1]['e'] + .2) if before else 0.0; b = (after[0]['s'] - .1) if after else len(y) / SR
        py = read_wav(os.path.join(d, f)); L = len(py) / SR
        y = np.concatenate([y[:int(a * SR)], np.zeros(int(.25 * SR), 'float32'), py, np.zeros(int(.25 * SR), 'float32'), y[int(b * SR):]])
        off = a + .25; delta = (off + L + .25) - b
        sh = lambda w, o: dict(w, s=round(w['s'] + o, 3), e=round(w['e'] + o, 3))
        words = [w for w in words if w['e'] <= a] + [sh(w, off) for w in pw] + [sh(w, delta) for w in words if w['s'] >= b]
        mk = [m for m in side.get('mistakes', []) if m['t'] <= a] + [dict(m, t=m['t'] + off, para=i) for m in ps_.get('mistakes', [])] \
            + [dict(m, t=m['t'] + delta) for m in side.get('mistakes', []) if m['t'] >= b]
        st2 = [q for q in starts if q['t'] <= a] + [{'para': i, 't': off, 'how': 'patch'}] + [dict(q, t=q['t'] + delta) for q in starts if q['t'] >= b]
        side = dict(side, mistakes=mk, paragraphStarts=st2); starts = st2
        patched[i] = f
    return y, words, side, patched


# ------------------------------------------------------------------------------------------------ main per video
def run(vid):
    # the full take (patch takes - "<vid>-patch-<time>.wav", single paragraphs re-read - are spliced in later, not here)
    takes = sorted(f for f in os.listdir(os.path.join(IN, vid)) if f.endswith('.wav') and '-patch-' not in f)
    assert takes, 'no reading for ' + vid
    base = os.path.join(IN, vid, takes[-1][:-4])              # the latest take
    side = json.load(open(base + '.json'))
    spec, _ = A.load(vid); ps, df = A.presets()
    model = ps[df]['model_id']
    flat = [(si, l) for si, sl in enumerate(spec['slides']) for l in sl]
    lines = [A.spoken(A.line_text(l), model) for si, l in flat]
    asread = [p['text'] for p in side['paragraphs']]
    assert len(lines) == len(asread), vid + ': the script has a different number of lines than her reading'
    out = os.path.join(OUTROOT, vid); os.makedirs(out, exist_ok=True)
    y = read_wav(base + '.wav')
    words = transcribe(base + '.wav', out, ' '.join(lines))
    y, words, side, patched = splice_patches(vid, base, side, y, words, lines, out)
    changed = [i + 1 for i in range(len(lines)) if lines[i] != asread[i] and i not in patched
               and not rs_covered(lines[i], {' '.join(asread[i].split())})]
    # whole sentences taken OUT of the script after she read them (e.g. the "which way is better" verdict, 2026-10-11):
    # her words for them are cut, not kept as her own wording
    removed = []
    for i in range(len(lines)):
        if i in patched or lines[i] == asread[i] or not rs_covered(lines[i], {' '.join(asread[i].split())}):
            continue
        keep_s = set(rs_sentences(lines[i]))
        for sen in rs_sentences(asread[i]):
            if sen not in keep_s:
                removed.append((i + 1, sen, [t for w_ in sen.split() for t in norm_tokens(w_)]))
    db = frames_db(y)
    # her tokens (each sub-token keeps its word's times)
    W, Wt = [], []
    for k, w in enumerate(words):
        for tok in norm_tokens(w['w']): W.append(tok); Wt.append((w['s'], w['e'], k))
    # script tokens -> (line, char span in the line) so cues can be timed
    S, Sl = [], []
    for li, t in enumerate(lines):
        for m in re.finditer(r"\S+", t):
            for tok in norm_tokens(m.group(0)): S.append(tok); Sl.append((li, m.start(), m.end()))
    rep = {'cuts': [], 'kept_extra': [], 'missing': [], 'marks_unused': []}
    cut = []                                     # (t0, t1, why) in the original WAV
    # 1) her mistake marks FIRST: each one cuts the failed attempt before it (she knows best which take failed); those
    #    words are taken out before aligning, so the aligner cannot pick a failed attempt that happens to match better
    marks = [mk['t'] for mk in side.get('mistakes', [])]; used = set()
    pstart = {}
    for mk_ in side.get('mistakes', []):
        st_ = [q['t'] for q in side.get('paragraphStarts', []) if q['para'] == mk_['para'] and q['t'] <= mk_['t']]
        pstart[mk_['t']] = max(st_) if st_ else mk_['t'] - 25
    for t0, t1, x in mark_cuts(W, Wt, marks, words, pstart):
        cut.append((t0, t1, 'mistake mark')); used.add(x)
        rep['cuts'].append({'t': round(t0, 2), 'len': round(t1 - t0, 2), 'why': 'mistake mark (failed attempt before it)',
                            'words': ' '.join(w['w'] for w in words if t0 - .01 <= w['s'] < t1)})
    keepk = [k for k in range(len(W)) if not any(a <= Wt[k][0] < b for a, b, _ in cut)]
    W = [W[k] for k in keepk]; Wt = [Wt[k] for k in keepk]
    # 2) align what is left; extra stretches: a restart (re-read right after) or a filler is cut, her own wording is kept
    pairs, eq = align(S, W)
    matched = {j: i for i, j in pairs if i is not None and j is not None and eq[i, j]}
    js = sorted(matched)
    first_j, last_j = js[0], js[-1]
    t_first = Wt[first_j][0]; t_last = Wt[last_j][1]
    cut.append((0.0, max(0.0, t_first - .25), 'before the first script word'))
    # after the last matched word: keep her tail if it is speech that belongs to the last paragraph (reworded), cut
    # only what follows a long silence or is not near the script at all
    tail_end = t_last
    for k in range(last_j + 1, len(W)):
        if Wt[k][0] - tail_end > 3.0: break
        tail_end = Wt[k][1]
    cut.append((tail_end + .35, len(y) / SR, 'after the last words'))
    j = first_j
    while j <= last_j:
        if j in matched: j += 1; continue
        a = j
        while j <= last_j and j not in matched: j += 1
        b = j                                   # her tokens a..b-1 are extra; b is the next matched token
        toks = W[a:b]; t0 = Wt[a][0]; t1 = Wt[b][0] if b < len(Wt) else Wt[b - 1][1]
        nxt = [S[matched[k]] for k in range(b, min(len(W), b + len(toks) + 4)) if k in matched]
        restart = len(toks) >= 1 and difflib.SequenceMatcher(None, toks, nxt[:len(toks) + 2]).ratio() >= .5 if nxt else False
        if not restart and len(toks) >= 5:
            # a re-read a little later (her own words in between): most of the run is said again within the next 40 s
            later = [S[matched[k]] for k in range(b, len(W)) if k in matched and Wt[k][0] - t1 < 40]
            sm = difflib.SequenceMatcher(None, toks, later, autojunk=False)
            got = sum(bl.size for bl in sm.get_matching_blocks() if bl.size >= 3)
            restart = got >= .6 * len(toks)
        filler = all(t in FILLERS for t in toks)
        gone = False
        if not restart and not filler and removed and len(toks) >= 3:
            rtoks = [t for _, _, tt in removed for t in tt]
            sm = difflib.SequenceMatcher(None, toks, rtoks, autojunk=False)
            gone = sum(bl.size for bl in sm.get_matching_blocks() if bl.size >= 2) >= .6 * len(toks)
        if gone:
            cut.append((t0, t1, 'removed from the script'))
            rep['cuts'].append({'t': round(t0, 2), 'len': round(t1 - t0, 2), 'why': 'removed from the script after she read it',
                                'words': ' '.join(w['w'] for w in words[Wt[a][2]:Wt[b - 1][2] + 1])})
        elif restart or filler:
            why = 'restart' if restart else 'filler'
            if not filler:
                a = back_to_start(W, Wt, a, b, t0); t0 = Wt[a][0]
            cut.append((t0, t1, why))
            rep['cuts'].append({'t': round(t0, 2), 'len': round(t1 - t0, 2), 'why': why, 'words': ' '.join(w['w'] for w in words[Wt[a][2]:Wt[b - 1][2] + 1])})
        else:
            rep['kept_extra'].append({'t': round(t0, 2), 'words': ' '.join(w['w'] for w in words[Wt[a][2]:Wt[b - 1][2] + 1])})
    for x in marks:
        if x not in used: rep['marks_unused'].append(round(x, 2))
    # script words she did not say
    said = set(i for i, j in pairs if i is not None and j is not None and eq[i, j])
    miss_runs, run_ = [], []
    for i in range(len(S)):
        if i not in said: run_.append(i)
        elif run_: miss_runs.append(run_); run_ = []
    if run_: miss_runs.append(run_)
    for r in miss_runs:
        if len(r) >= 3:
            li, a0, _ = Sl[r[0]]; _, _, b0 = Sl[r[-1]]
            rep['missing'].append({'line': li + 1, 'text': lines[li][a0:b0]})
    # ---- kept intervals (original time), cut points at quiet frames
    cut.sort()
    merged = []
    for a, b, why in cut:
        if b <= a: continue
        if merged and a <= merged[-1][1] + .05: merged[-1][1] = max(merged[-1][1], b)
        else: merged.append([a, b])
    # whisper's word starts can be late by 0.1-0.3 s: a cut starting at the failed word's start left its first syllable
    # (q-359 1:03, teacher: "it needs to cut off that second"). So a cut runs from just after her last KEPT word to just
    # before her next kept word (0.15 s of her pause kept on each side), at the quietest point there.
    def kept_word(w_):
        return not any(a_ - .02 <= w_['s'] and w_['e'] <= b_ + .02 for a_, b_ in merged)
    ends = sorted(w_['e'] for w_ in words if kept_word(w_)); starts = sorted(w_['s'] for w_ in words if kept_word(w_))
    for cr in merged:
        a, b = cr
        pe = max([e for e in ends if e <= a + .05], default=None); ns = min([s_ for s_ in starts if s_ >= b - .05], default=None)
        if pe is not None and a > 0 and pe + .15 < b: cr[0] = min(a, pe + .15) if a - pe < 4 else a
        if ns is not None and b < len(y) / SR and ns - .15 > cr[0]: cr[1] = max(b, ns - .15)
    # ... and whisper's times can be early too (a word "starting" in the silence before it): trim to her real voice -
    # from 0.15 s after the last loud frame before the cut to 0.15 s before the first loud frame after it
    loud = db > np.percentile(db[db > -80], 90) - 20       # her voice, not a breath or click (~ -25 dB)
    for cr in merged:
        a, b = cr
        if a > 0:
            k = int(a * 100)
            while k > 0 and not loud[k] and a - k / 100 < 2.0: k -= 1
            if loud[k]: cr[0] = max(cr[0] - 2.0, min(a, k / 100 + .15))
        if b < len(y) / SR:
            k = int(b * 100)
            while k < len(loud) - 1 and not loud[k] and k / 100 - b < 2.0: k += 1
            if loud[k]: cr[1] = max(b, k / 100 - .15)
    keep, t = [], 0.0
    for a, b in merged:
        a2 = low_point(db, a, -.06, .06) if a > 0 else 0; b2 = low_point(db, b, -.06, .06) if b < len(y) / SR else len(y) / SR
        if a2 > t: keep.append([t, a2])
        t = max(t, b2)
    if t < len(y) / SR: keep.append([t, len(y) / SR])
    # ---- silences: cap long ones (inside the kept audio)
    speech_db = np.percentile(db[db > -80], 90)
    quiet = db < max(np.percentile(db, 8) + 10, speech_db - 38)
    slide_end_t = {}                           # her time of each line start, to know where a slide changes
    line_t = {}
    for i, j in pairs:
        if i is not None and j is not None and eq[i, j]:
            li = Sl[i][0]; line_t.setdefault(li, Wt[j][0])
    slide_starts = [line_t.get(li) for li in range(1, len(lines)) if flat[li][0] != flat[li - 1][0] and line_t.get(li) is not None]
    keep2 = []
    for a, b in keep:
        fa, fb = int(a * 100), int(b * 100); k = fa; seg_start = a
        while k < fb:
            if quiet[k]:
                s0 = k
                while k < fb and quiet[k]: k += 1
                L = (k - s0) / 100.0; cap = CAP_SLIDE if any(abs(s - k / 100.0) < 1.0 for s in slide_starts) else CAP
                if L > cap and s0 > fa and k < fb:
                    keep2.append([seg_start, s0 / 100.0 + cap / 2]); seg_start = k / 100.0 - cap / 2
                    rep.setdefault('silences_capped', 0); rep['silences_capped'] += 1
            else: k += 1
        keep2.append([seg_start, b])
    keep = [x for x in keep2 if x[1] - x[0] > .03]
    rep['cut_ranges'] = [[round(a, 2), round(b, 2)] for a, b in merged]; rep['keep_ranges'] = [[round(a, 2), round(b, 2)] for a, b in keep]
    # ---- edited audio with crossfades + the time map
    f = int(FADE * SR); parts, tmap, tnew = [], [], 0.0
    for a, b in keep:
        seg = y[int(a * SR):int(b * SR)].copy()
        if parts and len(seg) > 2 * f and len(parts[-1]) > 2 * f:
            ramp = np.linspace(0, 1, f, dtype='float32')
            prev = parts[-1]; prev[-f:] = prev[-f:] * (1 - ramp) + seg[:f] * ramp; seg = seg[f:]; tnew -= 0
            tmap.append((a + FADE, b, tnew))
        else:
            tmap.append((a, b, tnew))
        parts.append(seg); tnew += len(seg) / SR
    clean = np.concatenate(parts)
    def newt(t):
        for a, b, n0 in tmap:
            if a - .02 <= t <= b + .02: return n0 + max(0.0, min(t, b) - a)
        best = min(tmap, key=lambda x: min(abs(t - x[0]), abs(t - x[1])))
        return best[2] + (0 if t < best[0] else best[1] - best[0])
    raw = os.path.join(out, 'edit.wav')
    with wave.open(raw, 'wb') as ww:
        ww.setnchannels(1); ww.setsampwidth(2); ww.setframerate(SR); ww.writeframes((np.clip(clean, -1, 1) * 32767).astype('<i2').tobytes())
    FF = A.FFMPEG
    m1 = subprocess.run([FF, '-hide_banner', '-i', raw, '-af', 'highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                        capture_output=True, text=True).stderr
    js_ = json.loads(m1[m1.rfind('{'):m1.rfind('}') + 1])
    ln = ('highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true'
          % (js_['input_i'], js_['input_tp'], js_['input_lra'], js_['input_thresh'], js_['target_offset']))
    subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', '-i', raw, '-af', ln, '-ar', str(SR), os.path.join(out, 'clean.wav')], check=True)
    subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', '-i', os.path.join(out, 'clean.wav'), '-c:a', 'libmp3lame', '-b:a', '160k',
                    os.path.join(out, 'audio.mp3')], check=True)
    os.remove(raw)
    # ---- word times for every script token (her time on the clean audio)
    tt = [None] * len(S)
    for i, j in pairs:
        if i is not None and j is not None:
            s0, e0, _ = Wt[j]; tt[i] = (newt(s0), newt(e0))
    known = [k for k, v in enumerate(tt) if v]
    for k in range(len(S)):
        if tt[k] is None:
            lo = max([x for x in known if x < k], default=None); hi = min([x for x in known if x > k], default=None)
            a_ = tt[lo][1] if lo is not None else 0.0; b_ = tt[hi][0] if hi is not None else a_ + .3
            tt[k] = (a_, max(a_, b_))
    # ---- alignment.json in the segmented format (text = the lines joined by spaces, like seg_plan) + manifest via remap
    forms = lines; text = ' '.join(forms)
    spans, pos = [], 0
    for (si, l), f_ in zip(flat, forms):
        spans.append((si, pos, pos + len(f_))); pos += len(f_) + 1
    ch, cs, ce = list(text), [0.0] * len(text), [0.0] * len(text)
    tok_of_char = {}
    for k, (li, a0, b0) in enumerate(Sl):
        g = spans[li][1]
        for c in range(g + a0, g + b0): tok_of_char.setdefault(c, []).append(k)
    last = 0.0
    for c in range(len(text)):
        ks = tok_of_char.get(c)
        if ks:
            s0 = min(tt[k][0] for k in ks); e0 = max(tt[k][1] for k in ks); cs[c], ce[c] = s0, e0; last = e0
        else: cs[c] = ce[c] = last
    h = 'reading-' + takes[-1]
    json.dump({'_hash': h, 'text': text, 'characters': ch, 'character_start_times_seconds': [round(x, 3) for x in cs],
               'character_end_times_seconds': [round(x, 3) for x in ce]}, open(os.path.join(out, 'alignment.json'), 'w'), ensure_ascii=False)
    extra = {'gen': 'reading', 'source': takes[-1], 'voiceName': 'the teacher (her own reading)'}
    sys.argv = ['x']; A.remap(vid, spec, out, {'voice_id': 'teacher', 'model_id': 'reading'}, h, (text, spans, forms, extra))
    # cues whose phrase words she did not say (timed between neighbours)
    unplaced = []
    for n, (si, l) in enumerate(flat):
        for ph in (l.get('at') or []) if isinstance(l, dict) else []:
            li = n - 1 if ph.startswith('<') else n; p_ = ph.lstrip('<')
            k = lines[li].lower().find(p_.lower())
            if k < 0: continue
            toks = [ti for ti, (L_, a0, b0) in enumerate(Sl) if L_ == li and a0 >= k and b0 <= k + len(p_) + 1]
            if toks and not any(ti in said for ti in toks): unplaced.append({'line': n + 1, 'phrase': ph})
    # doubled / missing check: each script sentence's first 4 words, how often she says them in the KEPT audio
    kept_tok = [k for k in range(len(W)) if not any(a <= Wt[k][0] < b for a, b, _ in cut)]
    KW = [W[k] for k in kept_tok]; doubled = []
    for li, t_ in enumerate(lines):
        for sent in re.findall(r'[^.?!]+[.?!]?', t_):
            st = norm_tokens(sent)
            if len(st) < 5: continue
            n_, q = 0, 0
            while q <= len(KW) - len(st):
                if same(KW[q], st[0]) and difflib.SequenceMatcher(None, KW[q:q + len(st)], st).ratio() >= .8:
                    n_ += 1; q += len(st)
                else: q += 1
            if n_ > 1: doubled.append({'line': li + 1, 'sentence': sent.strip(), 'times': n_})
    rep['doubled'] = doubled
    # cues whose words she SKIPPED (2026-10-11 teacher: nothing appears without her words): at = -1 = not fired (the
    # studio's auto-narrate skips it). An APPEAR can only be dropped when no later item of that slide still appears
    # (items show in order); a POINT / mark on a dropped item is dropped too.
    import importlib.util as _u
    if '_ai_visual' not in sys.modules:
        _s = _u.spec_from_file_location('_ai_visual', os.path.join(HERE, 'math_patches', '_ai_visual.py'))
        _m = _u.module_from_spec(_s); sys.modules['_ai_visual'] = _m; _s.loader.exec_module(_m)
    AV = sys.modules['_ai_visual']; cue_lines, _ = AV.cues_of(vid)
    un = {(u['line'], u['phrase']) for u in unplaced}; skip = set(); kept_after = {}
    order = [(n, k, c) for n in sorted(cue_lines) for k, c in enumerate(cue_lines[n])]
    for n, k, c in reversed(order):
        si = flat[n - 1][0]; ph = (flat[n - 1][1].get('at') or [])[k]
        is_app = isinstance(c, tuple)
        if (n, ph) in un and (not is_app or not kept_after.get(si)): skip.add((n, k))
        elif is_app: kept_after[si] = True
    item_no, gone = {}, set()                  # slide -> item count; (slide, item number) of dropped items
    for n, k, c in order:
        si = flat[n - 1][0]
        if isinstance(c, tuple):
            item_no[si] = item_no.get(si, 0) + 1
            if (n, k) in skip: gone.add((si, item_no[si]))
        else:
            tg = c.get('point') or c.get('target') or ''
            mm = re.match(r'item (\d+)', tg)
            if mm and (si, int(mm.group(1))) in gone: skip.add((n, k))
    mp = os.path.join(out, 'manifest.json'); man = json.load(open(mp))
    for (n, k) in skip:
        man['lines'][n - 1]['at'][k] = -1
        if man['lines'][n - 1].get('atEnd'): man['lines'][n - 1]['atEnd'][k] = -1
    json.dump(man, open(mp, 'w'), indent=1, ensure_ascii=False)
    rep['cues_dropped'] = [{'line': n, 'phrase': (flat[n - 1][1].get('at') or [])[k]} for n, k in sorted(skip)]
    rep['cues_kept_unsaid'] = [u for u in unplaced if not any((u['line'], u['phrase']) == (n, (flat[n - 1][1].get('at') or [])[k]) for n, k in skip)]
    # cues in speaking order: a cue whose words she skipped got an in-between time; keep each line's cues in their order
    # (an underline must come after the line it underlines appears), 0.4 s apart where they would bunch up
    mp = os.path.join(out, 'manifest.json'); man = json.load(open(mp)); un = {(u['line'], u['phrase']) for u in unplaced}
    for n, (ln_, (si, l)) in enumerate(zip(man['lines'], flat)):
        ph = (l.get('at') or []) if isinstance(l, dict) else []
        for k in range(1, len(ln_['at'])):
            if ln_['at'][k] is None or ln_['at'][k - 1] is None or ln_['at'][k] == -1 or ln_['at'][k - 1] == -1: continue
            step = .4 if (n + 1, ph[k]) in un or (n + 1, ph[k - 1]) in un else .05
            if ln_['at'][k] < ln_['at'][k - 1] + step:
                d_ = ln_['at'][k - 1] + step - ln_['at'][k]; ln_['at'][k] = round(ln_['at'][k] + d_, 3)
                if ln_.get('atEnd') and ln_['atEnd'][k] is not None: ln_['atEnd'][k] = round(max(ln_['atEnd'][k] + d_, ln_['at'][k] + .3), 3)
    json.dump(man, open(mp, 'w'), indent=1, ensure_ascii=False)
    rep['patched_paragraphs'] = {str(i + 1): f for i, f in patched.items()}
    rep['changed_not_reread'] = changed
    rep.update(vid=vid, raw_s=round(len(y) / SR, 1), clean_s=round(len(clean) / SR, 1), n_cuts=len(rep['cuts']), unplaced_cues=unplaced,
               words_matched='%d of %d script words' % (len(said), len(S)))
    json.dump(rep, open(os.path.join(out, 'report.json'), 'w'), indent=1, ensure_ascii=False)
    print('%s: %.1f s -> %.1f s, %d cuts, %d silences capped, %s, %d extra stretches kept, %d missing, %d marks unused, %d cues unplaced, %d doubled'
          % (vid, rep['raw_s'], rep['clean_s'], rep['n_cuts'], rep.get('silences_capped', 0), rep['words_matched'], len(rep['kept_extra']),
             len(rep['missing']), len(rep['marks_unused']), len(unplaced), len(rep['doubled'])))
    return rep


def verify(vid):
    """transcribe the CLEAN audio again and check it against the script: every sentence once, in order; no filler or
    leftover restart. -> report.json['verify']"""
    out = os.path.join(OUTROOT, vid); spec, _ = A.load(vid); ps, df = A.presets()
    lines = [A.spoken(A.line_text(l), ps[df]['model_id']) for sl in spec['slides'] for l in sl]
    p = os.path.join(out, 'clean_transcript.json')
    if os.path.exists(p) and os.path.getmtime(p) > os.path.getmtime(os.path.join(out, 'clean.wav')): words = json.load(open(p))
    else:
        os.path.exists(p) and os.remove(p)
        words = transcribe_chunks(os.path.join(out, 'clean.wav'), p)
    W, Wt = [], []
    for k, w in enumerate(words):
        for tok in norm_tokens(w['w']): W.append(tok); Wt.append((w['s'], w['e'], k))
    sents = []
    for li, t in enumerate(lines):
        for sm in re.findall(r'[^.?!]+[.?!]?', t):
            st = norm_tokens(sm)
            if st: sents.append((li + 1, sm.strip(), st))
    S = [tok for _, _, st in sents for tok in st]; owner = [k for k, (_, _, st) in enumerate(sents) for _ in st]
    pairs, eq = align(S, W)
    hit = {}
    for i, j in pairs:
        if i is not None and j is not None and eq[i, j]: hit.setdefault(owner[i], []).append(j)
    missing = [{'line': ln, 'sentence': sm} for k, (ln, sm, st) in enumerate(sents) if len(hit.get(k, [])) < max(1, .5 * len(st))]
    doubled = []
    for k, (ln, sm, st) in enumerate(sents):
        if len(st) < 6: continue
        n_, q = 0, 0
        while q <= len(W) - len(st):
            if same(W[q], st[0]) and difflib.SequenceMatcher(None, W[q:q + len(st)], st).ratio() >= .9: n_ += 1; q += len(st)
            else: q += 1
        if n_ > 1: doubled.append({'line': ln, 'sentence': sm, 'times': n_})
    matched = set(j for i, j in pairs if i is not None and j is not None and eq[i, j])
    extra, j = [], 0
    while j < len(W):
        if j in matched: j += 1; continue
        a = j
        while j < len(W) and j not in matched: j += 1
        if j - a >= 3 or any(W[x] in FILLERS for x in range(a, j)):
            extra.append({'t': round(Wt[a][0], 2), 'words': ' '.join(W[a:j])})
    fill = [{'t': round(Wt[x][0], 2), 'word': W[x]} for x in range(len(W)) if W[x] in FILLERS]
    rp = os.path.join(out, 'report.json'); rep = json.load(open(rp))
    rep['verify'] = {'missing_sentences': missing, 'doubled_sentences': doubled, 'extra_runs': extra, 'fillers': fill}
    json.dump(rep, open(rp, 'w'), indent=1, ensure_ascii=False)
    print('%s verify: %d sentences missing, %d doubled, %d extra runs (3+ words), %d fillers' % (vid, len(missing), len(doubled), len(extra), len(fill)))
    return rep['verify']


if __name__ == '__main__':
    args = sys.argv[1:]                      # (run() resets sys.argv for ai_narrate)
    ids = [a for a in args if not a.startswith('--')] or sorted(os.listdir(IN))
    for v in ids:
        if '--verify-only' not in args: run(v)
        if '--verify' in args or '--verify-only' in args: verify(v)
