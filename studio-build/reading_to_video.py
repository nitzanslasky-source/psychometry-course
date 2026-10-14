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
  5. CAMERA LESSONS (2026-10-13; reading_studio.py camera mode): when her latest full take has a camera video, the same
     cuts / silence caps / patch splices are applied to it (WAV -> camera time measured by matching the camera file's own
     audio to the WAV) -> camera.mp4 (round bubble | alpha, clean timeline) + camera.json; report.json['camera'] has the
     sync check. Then, after the board video is rendered:
        reading_to_video.py --composite <videoId> [board.mp4] [out.mp4] [--corner tr|br|bl|tl]
     overlays her face bubble like the studio's (top right unless the board uses that corner) -> '<board> - camera.mp4'.
     READING_CAMERA=0 skips step 5; READING_IN / READING_OUT redirect the _reading / _voice_real folders (tests).
"""
import difflib, json, os, re, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_argv = sys.argv[:]; sys.argv = ['x']
import ai_narrate as A
from reading_studio import covered as rs_covered, sentences as rs_sentences
sys.argv = _argv
# her-voice videos are hand-written (the write cues and their chunk timing need _ai_visual's handwriting mode)
os.environ.setdefault('AI_HANDWRITE', 'all')
REC = os.path.expanduser('~/Documents/Course.recordings')
IN, OUTROOT = os.path.join(REC, '_reading'), os.path.join(REC, '_voice_real')
IN, OUTROOT = os.environ.get('READING_IN') or IN, os.environ.get('READING_OUT') or OUTROOT     # tests: a scratch folder
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


def a_hundred(toks):
    """2026-10-14 (q-r26-t18-02): "a hundred" (the script) = "100" -> "one hundred" (whisper): the same number. The
    'a' / 'one' mismatch made "is 198. 198 plus" a "repeat" and "100" a "restart", and cut 12 s of her take."""
    return ['one' if t == 'a' and k + 1 < len(toks) and toks[k + 1] == 'hundred' else t for k, t in enumerate(toks)]


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


def transcribe_chunks(wav, p, step=24.0, over=4.0):
    """Independent verification with context on BOTH sides of every core window.
    Keep words by midpoint in the core; never cut a word at the ASR window edge.
    """
    from faster_whisper import WhisperModel
    m = WhisperModel(os.environ.get('READING_VERIFY_MODEL', 'small.en'), device='cpu', compute_type='int8', local_files_only=True)
    y = read_wav(wav); T = len(y) / SR; words, t = [], 0.0
    while t < T:
        core_end = min(T, t + step)
        start = max(0.0, t - over)
        seg = y[int(start * SR):int(min(T, core_end + over) * SR)]
        seg = seg[:len(seg) // 3 * 3].reshape(-1, 3).mean(axis=1).astype('float32')     # 48 kHz -> the 16 kHz whisper expects
        ss, _ = m.transcribe(seg, beam_size=5, word_timestamps=True, condition_on_previous_text=False, vad_filter=False, language='en')
        for s_ in ss:
            for w in s_.words:
                a_, b_ = w.start + start, w.end + start
                if not t <= (a_ + b_) / 2 < core_end: continue
                words.append({'w': w.word.strip(), 's': round(a_, 3), 'e': round(b_, 3), 'p': round(w.probability, 3)})
        print('Independent speech check: %.0f / %.0f seconds' % (core_end, T), flush=True)
        t = core_end
    with open(p, 'w') as cache_file:
        json.dump(words, cache_file, ensure_ascii=False)
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


def mark_cuts(W, Wt, marks, words, floor=None, onset=None, heads=None):
    """each mistake mark at t: she re-reads a sentence right after it. The repeat starts at her first word after t; the
    failed attempt is the latest earlier place (within 25 s) where she said the same first words -> cut [failed, repeat).
    heads = {t: the first script tokens of the mark's paragraph}: a re-read that starts with them is a restart of the
    WHOLE paragraph (2026-10-14, q-r26-t18-02: two minutes of other attempts, worded differently, before her restart
    "Now let's check the answer choices") -> the cut reaches back to the paragraph's start (its Space press, `floor`),
    when that adds 20 s or more to the cut."""
    out = []
    for t in marks:
        lo = (floor or {}).get(t, t - 25)          # never reach back before the start of the paragraph she was reading
        # her re-read can start before the mark (she pressed M a moment late) - from her voice onset after the pause
        o = onset(t) if onset is not None else None
        t_r = min(t, o) if o is not None and o > t - 2.5 else t
        r = next((j for j in range(len(W)) if Wt[j][0] >= t_r - .15 or Wt[j][1] > t + .3), None)
        if r is None or r + 2 >= len(W): continue
        # whisper smears a re-read's first words back over the pause before it (r26-01: "Now" 179.5-179.5, "the"
        # 179.5-180.8, mark at 180.05): words glued to it, starting less than 1 s before the mark, belong to the re-read
        while r > 0 and t - Wt[r - 1][0] < 1.0 and Wt[r - 1][1] >= Wt[r][0] - .05:
            r -= 1
        X = W[r:r + 6]; best = None; best_hit = 0
        for p in range(r - 1, -1, -1):
            if Wt[r][0] - Wt[p][0] > 60 or Wt[p][0] < lo - 1.0: break
            if not (same(W[p], X[0]) or (len(X) > 1 and same(W[p], X[1]))): continue
            Y = W[p:min(r, p + len(X) + 2)]       # her words there, a little longer (she may add a word: "how exactly do")
            hit = sum(bl.size for bl in difflib.SequenceMatcher(None, X, Y, autojunk=False).get_matching_blocks())
            # the BEST matching earlier attempt (r26-01: "negative 3 | two times negative three..." re-read as a whole
            # block - the nearest "negative 3" was the wrong one); a tie keeps the later one
            if hit >= max(3, int(.66 * len(X))) and hit > best_hit:
                best, best_hit = p, hit
        if best is not None:
            while best > 0 and same(W[best - 1], X[0]) and not same(W[best], X[0]): best -= 1   # "negative | 16 is there"
        if best is None:                          # no same first words: the failed attempt is the sentence she was in
            for p in range(r - 1, -1, -1):
                if Wt[p][0] < lo - .5 or Wt[r][0] - Wt[p][0] > 20: break
                prev_w = words[Wt[p - 1][2]]['w'] if p > 0 else '.'
                if prev_w.rstrip().endswith(('.', '?', '!')) and Wt[p][2] != Wt[p - 1][2]: best = p; break
        hd = (heads or {}).get(t)
        if hd and floor and t in floor:
            hit = sum(bl.size for bl in difflib.SequenceMatcher(None, X, hd, autojunk=False).get_matching_blocks())
            p0 = next((p for p in range(r) if Wt[p][0] >= floor[t] - .05), None)
            # only a LONG abandoned attempt (20 s+ of the paragraph before the cut the rules above found): shorter
            # differences are left to the sentence rule, so earlier recorded videos keep their cuts
            if hit >= max(3, int(.66 * len(X))) and p0 is not None and (best is None or Wt[best][0] - Wt[p0][0] >= 20): best = p0
        # the re-read can start before whisper's first word after the mark (q-362: "Which choice gives" re-read at
        # 98.1 s, whisper's next word "six" at 98.9 - the cut ate the re-read): end the cut at her voice onset
        end = Wt[r][0]
        if onset is not None:
            o = onset(t)
            if o is not None and t <= o < end: end = max(o - .1, t)
        if best is not None: out.append((Wt[best][0], end, t))
    return out


def write_chunks(text, hw):
    """a hand-written line -> [(char start, char end, first stroke, end stroke, spoken tokens)]: a new chunk at a top-level
    = < > ≤ ≥ ≠, and after a comma / colon or a wide gap (2+ spaces)"""
    ix = hw.get('ix') or []; ns = len(hw.get('s') or [])
    if not ix: return []
    depth, cuts = 0, [0]
    for i, c in enumerate(text):
        if c in '{': depth += 1
        elif c in '}': depth -= 1
        elif depth == 0 and i > 0:
            if c in '=<>≤≥≠' and text[i - 1] not in '=<>≤≥≠': cuts.append(i)
            elif c != ' ' and (text[i - 1] in ',:' or text[max(0, i - 2):i] == '  '): cuts.append(i)
    cuts = sorted(set(cuts)) + [len(text)]
    stroke_at = lambda ci: next((b for a, b in ix if a >= ci), ns)
    out = []
    for a, b in zip(cuts, cuts[1:]):
        seg = text[a:b]
        sp = re.sub(r'\\hl\{[^}]*\}', '', seg).replace('{', ' ').replace('}', ' ').replace('/', ' over ').replace('|', ' absolute ')
        sp = sp.replace('−', '-').replace('·', ' times ').replace('≤', ' at most ').replace('≥', ' at least ').replace('≠', ' not ')
        toks = [t for t in norm_tokens(sp) if t not in ('the', 'of', 'value', 'equals', 'is', 'than', 'less', 'more')]
        s0, s1 = stroke_at(a), stroke_at(b)
        if s1 > s0: out.append((a, b, s0, s1, toks))
    return out


# ------------------------------------------------------------------------------------------------ auto lines
# 2026-10-11 (teacher approved: "just make sure it's flowing"): a calculation she SAYS in her own added words ("minus
# seven plus nine is two", "fourteen squared is one hundred ninety-six") is hand-written as she says it - left side
# while she says it, "= result" with the result. Checked first: a wrong one is not written but flagged (a slip of
# hers). Placed in a small scratch column on the right (_ai_visual.auto_items), at most 3 a slide, never a single
# number, never a line that is already on the board; highlighted after it is written.
from fractions import Fraction as _F
_WN = {w: i for i, w in enumerate(ONES)}; _WN.update({w: 10 * i for i, w in enumerate(TENS) if w != 'x'})
_OPS = {'plus': '+', '+': '+', 'minus': '-', '−': '-', 'times': '*', 'x': '*', '×': '*', 'over': '/', 'divided': '/'}
_RES = {'is', 'equals', 'gives', 'makes', 'equal', '='}
MAX_AUTO = 3


def _calc_tokens(ws):
    """her words -> [(kind, value, word index)]: N number, O operator, U unary minus, P power, R result, X other"""
    out = []
    for k, w in enumerate(ws):
        t = w['w'].lower().strip(" ,.?!;:…'\"")
        for part in re.findall(r"-?\d+(?:\.\d+)?|[a-z']+|[+=−×-]", t.replace('−', '-')):
            if re.fullmatch(r'-\d+(\.\d+)?', part): out += [('U', None, k), ('N', _F(part[1:]), k)]
            elif re.fullmatch(r'\d+(\.\d+)?', part): out.append(('N', _F(part), k))
            elif part in _WN: out.append(('N', _F(_WN[part]), k))
            elif part == 'hundred' and out and out[-1][0] == 'N': out[-1] = ('N', out[-1][1] * 100, out[-1][2])
            elif part == 'negative': out.append(('U', None, k))
            elif part in ('minus', '-'): out.append(('M', None, k))         # unary or binary, decided below
            elif part in _OPS: out.append(('O', _OPS[part], k))
            elif part in ('by', 'divided') and part == 'by' and out and out[-1][0] == 'O': continue
            elif part == 'squared': out.append(('P', 2, k))
            elif part == 'cubed': out.append(('P', 3, k))
            elif part in _RES: out.append(('R', None, k))
            elif part == 'be' and k > 0 and ws[k - 1]['w'].lower().strip(" ,.") == 'will': out.append(('R', None, k))
            elif part == 'will': continue                                  # "will be" = the result word
            elif part in ('and', 'so', 'then'): out.append(('S', None, k))
            else: out.append(('X', part, k))
    # numbers said with "and": "one hundred and ninety-six" is not handled - such a calc is simply not written
    return out


def _parse_calcs(ws):
    T = _calc_tokens(ws); found = []; i = 0
    def operand(j):
        neg = False
        if j < len(T) and T[j][0] in ('U', 'M'): neg = True; j += 1
        if j < len(T) and T[j][0] == 'N': return (-T[j][1] if neg else T[j][1], neg, j + 1)
        return None
    while i < len(T):
        o = operand(i)
        if not o: i += 1; continue
        terms = [(o[0], o[1])]; ops = []; j = o[2]; pw = None; start = i
        while j < len(T):
            if T[j][0] == 'P': pw = T[j][1]; j += 1; break
            if T[j][0] in ('O', 'M'):
                op = T[j][1] if T[j][0] == 'O' else '-'; o2 = operand(j + 1)
                if not o2: break
                ops.append(op); terms.append((o2[0], o2[1])); j = o2[2]; continue
            break
        if (ops or pw) and j < len(T) and T[j][0] == 'R':
            r = operand(j + 1)
            if r:
                expr = ' '.join(['(%r)' % terms[0][0]] + ['%s (%r)' % (op, v) for op, (v, _) in zip(ops, terms[1:])])
                try: val = eval(expr, {'Fraction': _F}) if not pw else terms[0][0] ** pw
                except ZeroDivisionError: val = None
                if pw and ops: val = None                               # "two plus three squared": too ambiguous
                fmt = lambda v, neg, inner: ('(−%s)' % _num(-v) if inner else '−' + _num(-v)) if v < 0 else _num(v)
                left = fmt(terms[0][0], terms[0][1], False)
                for op, (v, ng) in zip(ops, terms[1:]):
                    left += ' %s %s' % ({'+': '+', '-': '−', '*': '·', '/': '÷'}[op], fmt(v, ng, True))
                if pw: left += '^%d' % pw
                text = '%s = %s' % (left, fmt(r[0], r[1], False))
                found.append({'text': text, 'ok': val is not None and val == r[0], 'value': None if val is None else str(val),
                              'w0': T[start][2], 'wr': T[j][2], 'w1': T[r[2] - 1][2]})
                i = r[2]; continue
        i = start + 1
    return found


def _num(v):
    v = _F(v)
    return str(v.numerator) if v.denominator == 1 else '%s/%s' % (v.numerator, v.denominator)


def _calc_key(t):
    return re.sub(r'[\s()]', '', str(t)).replace('−', '-').replace('–', '-').replace('\\cdot', '·').replace('$', '')


def auto_lines(vid, out, man, mp, words, extra_spans, cut, merged, newt, cue_lines, flat, rep):
    import studio_handwrite as HWR
    p = os.path.join(out, 'auto_lines.json'); rep['auto_lines'] = []; rep['auto_flagged'] = []
    if os.environ.get('AI_AUTOLINES', '1') == '0':
        os.path.exists(p) and os.remove(p); return
    L = man['lines']; per_slide = {}; autos = []
    # what is already on each slide (typed and hand-written text of its items), to skip duplicates
    have = {}
    for n, cs in cue_lines.items():
        si = flat[n - 1][0]
        for c in cs:
            if isinstance(c, tuple):
                it = c[1]; have.setdefault(si, set()).add(_calc_key(it.get('t') or ''))
                for part in re.split(r',|\s{2,}', it.get('t') or ''):
                    if '=' in part: have[si].add(_calc_key(part))
    for w0, w1, a_, b_ in extra_spans:
        ws = words[w0:w1 + 1]
        for c in _parse_calcs(ws):
            kept = lambda w: not any(a <= w['s'] < b for a, b in merged)
            W_ = ws[c['w0']:c['w1'] + 1]
            if not all(kept(w) for w in W_): rep.setdefault('auto_skipped', []).append([c['text'], 'partly cut']); continue
            t0 = newt(W_[0]['s']); tr = newt(ws[c['wr']]['s']); t1 = newt(W_[-1]['e'])
            if not c['ok']:
                rep['auto_flagged'].append({'t': round(t0, 2), 'said': ' '.join(w['w'] for w in W_), 'as': c['text'], 'true value': c['value']}); continue
            # its line: the spoken line it is said in (the next line if it falls in the pause before that line)
            li = next((k for k in range(len(L)) if L[k]['start'] - .05 <= t0 <= L[k]['end'] + .3), None)
            if li is None:
                li = next((k for k in range(len(L)) if L[k]['start'] > t0), None)
                if li is None or (li > 0 and flat[li][0] != flat[li - 1][0]):
                    rep.setdefault('auto_skipped', []).append([c['text'], 'said at a slide change']); continue
            si = flat[li][0]
            key = _calc_key(c['text'])
            if any(key in h_ or (h_ and h_ in key) for h_ in have.get(si, set())): key = next(h_ for h_ in have[si] if key in h_ or (h_ and h_ in key))
            if key in have.get(si, set()) or per_slide.get(si, 0) >= MAX_AUTO:
                rep.setdefault('auto_skipped', []).append([c['text'], 'already on the board' if key in have.get(si, set()) else '3 on this slide already']); continue
            hw = HWR.write(c['text']); ch = write_chunks(c['text'], hw)
            if len(ch) != 2: rep.setdefault('auto_skipped', []).append([c['text'], 'chunks']); continue
            chunks = [[round(t0, 3), round(max(tr, t0 + .3), 3), ch[0][2], ch[0][3]], [round(max(tr, t0 + .3), 3), round(max(t1, tr + .3), 3), ch[1][2], ch[1][3]]]
            have.setdefault(si, set()).add(key); per_slide[si] = per_slide.get(si, 0) + 1
            autos.append({'id': 'auto%d' % (len(autos) + 1), 'line': li + 1, 'slide': si, 'text': c['text'], 't0': round(t0, 3),
                          't1': chunks[-1][1], 'chunks': chunks, 'said': ' '.join(w['w'] for w in W_)})
    # room on the board: the scratch column (shared rule, _ai_visual.auto_place) - no room = not written
    import importlib.util as _u
    AV = sys.modules['_ai_visual']; AV.auto_place(vid, cue_lines, autos)
    rep.setdefault('auto_skipped', []).extend([a['text'], 'no room on the board'] for a in autos if a.get('skip'))
    autos = [a for a in autos if not a.get('skip')]
    # cue position in its line (by time among the line's planned cues) + the manifest entries (appear+write, then a
    # highlight on it right after it is written)
    for au in sorted(autos, key=lambda x: x['t0']):
        ln_ = L[au['line'] - 1]; ats = ln_.get('at') or []
        k = sum(1 for x in ats if x is not None and x != -1 and x <= au['t0'])
        # never between a cue and the ones before it in the line that are skipped/None: after the last earlier one
        au['k'] = k
        for key_ in ('at', 'atEnd'):
            arr = ln_.setdefault(key_, [None] * len(ats))
            arr[k:k] = [au['t0'] if key_ == 'at' else au['t1'], au['t1'] + .15 if key_ == 'at' else au['t1'] + .5]
        wr = ln_.get('writes') or {}
        ln_['writes'] = {str(int(x) + 2 if int(x) >= k else int(x)): v for x, v in wr.items()}
        ln_['writes'][str(k)] = au['chunks']
    man['auto'] = len(autos)
    json.dump(man, open(mp, 'w'), indent=1, ensure_ascii=False)
    json.dump(autos, open(p, 'w'), indent=1, ensure_ascii=False)
    rep['auto_lines'] = [{'line': a['line'], 'text': a['text'], 'said': a['said']} for a in autos]


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
    srcmap = side.get('_srcmap') or [[0.0, len(y) / SR, base + '.wav', 0.0, '']]     # camera: [y0, y1, wav, src0, kind]
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
        # 2026-10-11 teacher (q-359 "is our answer" clipped at the splice): the join sits in her pause, measured on the
        # audio - after the end of her voice (+0.15 s), before its onset (-0.1 s) - not at whisper's word times
        dbf = frames_db(y); soft = dbf > np.percentile(dbf[dbf > -80], 90) - 32
        def _end(t):
            k = int(t * 100)
            while k < len(soft) - 6 and k < int(t * 100) + 60 and soft[k:k + 6].any(): k += 1
            return k / 100.0
        def _on(t):
            k = int(t * 100)
            while k > 6 and k > int(t * 100) - 40 and soft[k - 6:k].any(): k -= 1
            return k / 100.0
        a = (_end(before[-1]['e']) + .15) if before else 0.0; b = (_on(after[0]['s']) - .1) if after else len(y) / SR
        py = read_wav(os.path.join(d, f))
        # a patch take that covers SEVERAL paragraphs: only this paragraph's part of it (from her Space press for it to
        # the next one) - the whole take spliced in per paragraph doubled q-359's re-read (2026-10-11)
        pst = sorted(q['t'] for q in ps_.get('paragraphStarts', []) if q['para'] == i)
        pa = pst[-1] if pst else 0.0
        nx_ = [q['t'] for q in ps_.get('paragraphStarts', []) if q['t'] > pa + .05 and q['para'] != i]
        pb = min(nx_) if nx_ else len(py) / SR
        if pa > 0 or pb < len(py) / SR:
            pa = max(0.0, pa - .15); py = py[int(pa * SR):int(pb * SR)]
            pw = [dict(w, s=round(w['s'] - pa, 3), e=round(w['e'] - pa, 3)) for w in pw if pa - .05 <= w['s'] < pb]
            ps_ = dict(ps_, mistakes=[dict(m, t=m['t'] - pa) for m in ps_.get('mistakes', []) if pa <= m['t'] < pb + .5])
        L = len(py) / SR
        pa_src = pa                                  # where py starts in the patch WAV (0 when the whole take is used)
        pf = os.path.join(d, f)
        srcmap = _clip_map(srcmap, 0, a) + [[a, a + .25, pf, pa_src - .25, 'gap'], [a + .25, a + .25 + L, pf, pa_src, ''],
                                             [a + .25 + L, a + .5 + L, pf, pa_src + L, 'gap']] \
            + [[s0 + (a + .5 + L - b), s1 + (a + .5 + L - b), f_, src, k_] for s0, s1, f_, src, k_ in _clip_map(srcmap, b, 1e9)]
        y = np.concatenate([y[:int(a * SR)], np.zeros(int(.25 * SR), 'float32'), py, np.zeros(int(.25 * SR), 'float32'), y[int(b * SR):]])
        off = a + .25; delta = (off + L + .25) - b
        sh = lambda w, o: dict(w, s=round(w['s'] + o, 3), e=round(w['e'] + o, 3))
        words = [w for w in words if w['e'] <= a] + [sh(w, off) for w in pw] + [sh(w, delta) for w in words if w['s'] >= b]
        mk = [m for m in side.get('mistakes', []) if m['t'] <= a] + [dict(m, t=m['t'] + off, para=i) for m in ps_.get('mistakes', [])] \
            + [dict(m, t=m['t'] + delta) for m in side.get('mistakes', []) if m['t'] >= b]
        st2 = [q for q in starts if q['t'] <= a] + [{'para': i, 't': off, 'how': 'patch'}] + [dict(q, t=q['t'] + delta) for q in starts if q['t'] >= b]
        side = dict(side, mistakes=mk, paragraphStarts=st2, _srcmap=srcmap); starts = st2
        patched[i] = f
    return y, words, side, patched


def _clip_map(m, lo, hi):
    """the part [lo, hi) of a source map [[y0, y1, wav, src0, kind], ...]"""
    out = []
    for s0, s1, f, src, k in m:
        a, b = max(s0, lo), min(s1, hi)
        if b > a: out.append([a, b, f, src + (a - s0), k])
    return out


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
    W, S = a_hundred(W), a_hundred(S)
    rep = {'cuts': [], 'kept_extra': [], 'missing': [], 'marks_unused': []}
    extra_spans = []                             # her own words kept: (first word, last word, first token, end token)
    cut = []                                     # (t0, t1, why) in the original WAV
    # 1) her mistake marks FIRST: each one cuts the failed attempt before it (she knows best which take failed); those
    #    words are taken out before aligning, so the aligner cannot pick a failed attempt that happens to match better
    marks = [mk['t'] for mk in side.get('mistakes', [])]; used = set()
    pstart = {}
    for mk_ in side.get('mistakes', []):
        st_ = [q['t'] for q in side.get('paragraphStarts', []) if q['para'] == mk_['para'] and q['t'] <= mk_['t']]
        pstart[mk_['t']] = max(st_) if st_ else mk_['t'] - 25
    _sv = db > np.percentile(db[db > -80], 90) - 32
    def _onset_after(t):
        k = int(t * 100)
        while k < len(_sv) - 10:
            if _sv[k:k + 10].all(): return k / 100.0
            k += 1
        return None
    heads = {}
    for mk_ in side.get('mistakes', []):
        real = any(q['para'] == mk_.get('para') and q['t'] <= mk_['t'] for q in side.get('paragraphStarts', []))
        if real and 0 <= mk_.get('para', -1) < len(lines):                 # only a logged paragraph start (no guess)
            heads[mk_['t']] = [t for w_ in lines[mk_['para']].split()[:8] for t in norm_tokens(w_)][:7]
    for t0, t1, x in mark_cuts(W, Wt, marks, words, pstart, _onset_after, heads):
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
    # 2026-10-11 (verdict paragraphs removed after she read them, q-367/368/369: she reworded them, so the words did not
    # match the removed text): when the removed sentences came BEFORE the kept ones of a line (verdict, then "Okay. I'll
    # see you"), everything extra she said between the previous line and the kept part of that line goes
    removed_regions = []
    for li_ in sorted({r_[0] - 1 for r_ in removed}):
        a_s = rs_sentences(asread[li_]); keep_s = set(rs_sentences(lines[li_]))
        ks = [k for k, x in enumerate(a_s) if x in keep_s]; rs_ = [k for k, x in enumerate(a_s) if x not in keep_s]
        if not ks or not rs_ or min(rs_) > min(ks): continue
        # only a removed paragraph before the CLOSING ("Okay. I'll see you..."): a removed method announcement at the
        # start of a line must not take her whole re-read of that line with it (topic 14, q-388: 48 s)
        if not all(re.match(r"^(\[[^\]]*\]\s*)*(okay|i'll see you|that's it|now go)", a_s[k], re.I) for k in ks): continue
        pe_ = [Wt[jj][1] for jj, ii in matched.items() if Sl[ii][0] < li_]
        # the kept part starts where 3+ of her words in a row match the line (a lone "the" inside her verdict can match)
        mj = sorted(jj for jj, ii in matched.items() if Sl[ii][0] == li_)
        qs_ = [Wt[jj][0] for k_, jj in enumerate(mj) if k_ + 2 < len(mj) and mj[k_ + 2] - jj == 2] or [Wt[jj][0] for jj in mj[-2:]]
        if pe_ and qs_ and max(pe_) < min(qs_): removed_regions.append((max(pe_), min(qs_)))
    rep['removed_regions'] = [[round(a, 2), round(b, 2)] for a, b in removed_regions]
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
        if not restart and not filler and any(r0 - .05 <= t0 and t1 <= r1 + .05 for r0, r1 in removed_regions): gone = True
        if not gone and not restart and not filler and removed and len(toks) >= 3:
            rtoks = [t for _, _, tt in removed for t in tt]
            sm = difflib.SequenceMatcher(None, toks, rtoks, autojunk=False)
            gone = sum(bl.size for bl in sm.get_matching_blocks() if bl.size >= 2) >= .6 * len(toks)
            if not gone:                       # her own wording of a removed sentence: same first words, about as long
                for _, _, rt in removed:
                    if len(rt) >= 3 and len(toks) <= len(rt) + 3 and all(same(toks[q], rt[q]) for q in range(min(3, len(toks), len(rt)))):
                        gone = True; break
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
            extra_spans.append((Wt[a][2], Wt[b - 1][2], a, b))
    for x in marks:
        if x not in used: rep['marks_unused'].append(round(x, 2))
    # 2026-10-11 teacher ("but... but which one", "so we have two rays going outward" twice): a word or phrase said
    # twice in a row (in what is kept) - the FIRST copy goes, the second stays. Not when the script itself repeats it.
    stoks = ' '.join(S)
    def kept_time(t):                              # her time with the cuts so far taken out (how close it sounds)
        return t - sum(max(0.0, min(b, t) - a) for a, b, _w in cut)
    for _ in range(6):
        kk = [k for k in range(len(W)) if not any(a <= Wt[k][0] < b for a, b, _w in cut)]
        hit = None
        for x in range(len(kk)):
            for n in range(8, 0, -1):              # (a) said twice in a row: "but... but", a phrase and the phrase again
                if x + 2 * n > len(kk): continue
                A_, B_ = kk[x:x + n], kk[x + n:x + 2 * n]
                if not all(same(W[A_[q]], W[B_[q]]) for q in range(n)): continue
                if n == 1 and (W[A_[0]] in ('ten', 'one') or len(W[A_[0]]) < 2): continue
                if kept_time(Wt[B_[0]][0]) - kept_time(Wt[A_[-1]][1]) > 2.0: continue
                # whisper can miss words: her voice between the two copies (outside cuts) = not a repeat
                g0, g1 = int(Wt[A_[-1]][1] * 100) + 5, int(Wt[B_[0]][0] * 100) - 5
                if g1 > g0 and sum(1 for k in range(g0, g1) if _sv[k] and not any(a <= k / 100 < b for a, b, _w in cut)) >= 25: continue
                if ' '.join(W[q] for q in A_ + B_) in stoks: continue      # the script says it twice too
                hit = (A_[0], B_[0], ' '.join(W[q] for q in A_)); break
            if hit: break
            # (b) a 5-word stretch said again within 16 words / 10 s ("so we have two rays going outward and we have
            # a gap in the | we have two rays going outward and a gap in the middle"): the first try goes
            if x + 5 <= len(kk):
                G = [W[q] for q in kk[x:x + 5]]
                if stoks.count(' '.join(G)) < 2:
                    for yy in range(x + 5, min(len(kk) - 4, x + 5 + 40)):
                        if kept_time(Wt[kk[yy]][0]) - kept_time(Wt[kk[x]][0]) > 20: break
                        if all(same(G[q], W[kk[yy + q]]) for q in range(5)):
                            # a real re-read: 7+ words the same in a row, and most of the first try said again after it
                            # (r26-13: "if they're the same signs, so they add up..." vs a later "what if they're the
                            # same signs but..." was cut by the 5-word rule - 11 s of real explanation lost)
                            run_ = 5
                            while yy + run_ < len(kk) and x + run_ < yy and same(W[kk[x + run_]], W[kk[yy + run_]]): run_ += 1
                            first = [W[q] for q in kk[x:yy]]; again = [W[q] for q in kk[yy:yy + int(len(first) * 1.5) + 2]]
                            sm_ = difflib.SequenceMatcher(None, first, again, autojunk=False)
                            cov = sum(bl.size for bl in sm_.get_matching_blocks()) / max(1, len(first))
                            if run_ >= 7 and cov >= .6:
                                hit = (kk[x], kk[yy], ' '.join(W[q] for q in kk[x:yy])); break
            if hit: break
        if not hit: break
        a_, b_, txt = hit; t0, t1 = Wt[a_][0], Wt[b_][0]
        cut.append((t0, t1, 'repeat'))
        rep['cuts'].append({'t': round(t0, 2), 'len': round(t1 - t0, 2), 'why': 'repeat (first copy cut)', 'words': txt})
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
    def drop_islands():
        # a kept scrap shorter than 0.6 s between two cuts is a leftover of a failed attempt ("But" | ... | "but which")
        k = 0
        while k + 1 < len(merged):
            if merged[k + 1][0] - merged[k][1] < .6: merged[k][1] = max(merged[k][1], merged[k + 1][1]); del merged[k + 1]
            else: k += 1
    drop_islands()
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
        # ...but never past the start of her voice: whisper can miss the first words of a re-read (q-362 "Which choice
        # gives" before "six") - the next kept WORD is then late, her voice is not
        if ns is not None and b < len(y) / SR and ns - .15 > cr[0]:
            o_ = _onset_after(b - .05)
            cr[1] = max(b, min(ns - .15, o_ - .1 if o_ is not None else ns - .15))
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
    # 2026-10-11 teacher (q-359 "is our answer" cut mid-word, q-361 "x." lost): a cut never starts inside her last kept
    # word or ends inside her next one - measured on the audio (a soft threshold, word tails are quiet), +0.15 s pad
    soft = db > np.percentile(db[db > -80], 90) - 32
    def voice_end(t):
        k = int(t * 100)
        while k < len(soft) - 6 and k < int(t * 100) + 60 and soft[k:k + 6].any(): k += 1
        return k / 100.0
    def voice_onset(t):
        k = int(t * 100)
        while k > 6 and k > int(t * 100) - 40 and soft[k - 6:k].any(): k -= 1
        return k / 100.0
    kept_ws = [w_ for w_ in words if kept_word(w_)]
    def first_dip(t):
        """the first clear dip in her voice after t (a word boundary inside a whisper word): 12 dB under the peak so far"""
        k0 = int(t * 100) + 8; mx = -200.0
        for k in range(k0, min(len(db) - 4, k0 + 50)):
            mx = max(mx, db[k])
            if db[k] < mx - 12 and db[k] <= db[k - 3:k + 4].min() + .01: return k / 100.0 + .005
        return low_point(db, t, .12, .5)
    for cr in merged:
        a, b = cr
        pe = max([w_ for w_ in kept_ws if w_['e'] <= a + .3 and w_['s'] < a], key=lambda w_: w_['e'], default=None)
        if pe is not None and a > 0 and a - pe['e'] < .8:
            if soft[min(len(soft) - 1, int(a * 100))]:
                ve = voice_end(pe['e'])
                # her voice runs on past a short word tail: the cut is inside one whisper "word" ("X2." = "x." + a false
                # start "2,") - cut at the quietest point just after the kept part instead of keeping it all
                cr[0] = max(a, min(ve + .15, b - .05)) if ve - pe['e'] <= .3 else max(a, first_dip(max(a, pe['e'])))
        ns = min([w_ for w_ in kept_ws if w_['s'] >= b - .3 and w_['e'] > b], key=lambda w_: w_['s'], default=None)
        if ns is not None and b < len(y) / SR and ns['s'] - b < .8:
            on = voice_onset(ns['s'])
            if soft[min(len(soft) - 1, int(b * 100))] or on < b: cr[1] = max(cr[0] + .05, min(b, on - .1))
    drop_islands()
    keep, t = [], 0.0
    for a, b in merged:
        a2 = low_point(db, a, -.06, .06) if a > 0 else 0; b2 = low_point(db, b, -.06, .06) if b < len(y) / SR else len(y) / SR
        if a2 > t: keep.append([t, a2])
        t = max(t, b2)
    if t < len(y) / SR: keep.append([t, len(y) / SR])
    # ---- silences: cap long ones, measured over the JOINED audio (2026-10-11 teacher, q-362: 3.5 s before "I'll see
    # you" - quiet stretches with clicks in them, and quiet on both sides of a cut, were not capped). Quiet = not inside
    # a run of 0.1 s or more of voice-level frames, so a click or a breath blip doesn't break a silence.
    speech_db = np.percentile(db[db > -80], 90)
    vo = db > speech_db - 30; quiet = np.ones(len(db), bool); k = 0
    while k < len(vo):
        if vo[k]:
            k0 = k
            while k < len(vo) and vo[k]: k += 1
            if k - k0 >= 10: quiet[max(0, k0 - 3):k + 3] = False
        else: k += 1
    line_t = {}
    for i, j in pairs:
        if i is not None and j is not None and eq[i, j]:
            li = Sl[i][0]; line_t.setdefault(li, Wt[j][0])
    slide_starts = [line_t.get(li) for li in range(1, len(lines)) if flat[li][0] != flat[li - 1][0] and line_t.get(li) is not None]
    idx = np.concatenate([np.arange(int(round(a * 100)), int(round(b * 100))) for a, b in keep if b - a > .005]); idx = idx[idx < len(quiet)]
    q_ = quiet[idx]; drop = np.zeros(len(idx), bool); k = 0
    while k < len(idx):
        if q_[k]:
            k0 = k
            while k < len(idx) and q_[k]: k += 1
            if k0 > 0 and k < len(idx):
                cap = CAP_SLIDE if any(abs(s_ - idx[k] / 100.0) < 1.0 for s_ in slide_starts) else CAP
                n_keep = int(cap * 100)
                if k - k0 > n_keep:
                    drop[k0 + n_keep // 2:k - (n_keep - n_keep // 2)] = True
                    rep.setdefault('silences_capped', 0); rep['silences_capped'] += 1
        else: k += 1
    kept_idx = idx[~drop]; keep2 = []
    for f_ in kept_idx:
        if keep2 and f_ == keep2[-1][1]: keep2[-1][1] = f_ + 1
        else: keep2.append([f_, f_ + 1])
    keep2 = [[a / 100.0, b / 100.0] for a, b in keep2]
    if keep2: keep2[0][0] = max(keep2[0][0], keep[0][0]); keep2[-1][1] = keep[-1][1]
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
    # ---- camera lessons: her face video, cut exactly like the audio (camera.mp4 + camera.json; composite() adds it)
    if os.environ.get('READING_CAMERA', '1') != '0':
        try:
            rep['camera'] = camera_track(vid, out, base, side, tmap, len(clean) / SR)
        except Exception as e:                      # the audio is ready either way; the report says why there is no face
            import traceback; traceback.print_exc()
            rep['camera'] = {'error': '%s: %s' % (type(e).__name__, e)}
        if rep['camera']: print('%s camera: %s' % (vid, json.dumps({k: v for k, v in rep['camera'].items() if k in ('file', 'sync_check', 'hidden', 'error')})))
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
    # 2026-10-11 teacher ("a whole line of calculations is written way before I'm saying it"): a hand-written line is
    # written in CHUNKS, each while she says it - the line split at = < > and at wide gaps / commas, each chunk found in
    # her words of that line (numbers as words), written from the start to the end of those words (never finished
    # before she has said it). -> manifest line 'writes': {cue index: [[t0, t1, first stroke, end stroke], ...]}
    rep['write_chunks'] = []
    for n in sorted(cue_lines):
        li = n - 1; ln_ = man['lines'][li]
        for k, c in enumerate(cue_lines[n]):
            if not (isinstance(c, tuple) and len(c) > 3 and c[3] is True): continue
            at_ = ln_['at'][k] if k < len(ln_['at']) else None
            if at_ is None or at_ == -1: continue
            it = c[1]; text = it.get('t') or ''; hw = it.get('hw') or {}
            ch = write_chunks(text, hw)
            if len(ch) < 2: continue
            ph = ((flat[li][1].get('at') or [])[k] or '').lstrip('<').lower(); c0 = max(0, lines[li].lower().find(ph))
            L = [ti for ti, (L_, a0, b0) in enumerate(Sl) if L_ == li and a0 >= c0]
            cur, got = 0, []
            for (ca, cb, s0, s1, toks) in ch:
                best = None
                for p0 in range(cur, min(len(L), cur + 25)):
                    j, hit = p0, []
                    for tk in toks:
                        q = next((x for x in range(j, min(len(L), j + 4)) if same(S[L[x]], tk)), None)
                        if q is not None: hit.append(q); j = q + 1
                    if toks and len(hit) * 2 >= len(toks) and (best is None or len(hit) > len(best)): best = hit
                    if best and len(best) == len(toks): break
                if best: got.append([tt[L[best[0]]][0], tt[L[best[-1]]][1], s0, s1, len(toks)]); cur = best[-1] + 1
                else: got.append([None, None, s0, s1, len(toks)])
            # unmatched chunks: between their neighbours; the pen never faster than 10 glyphs a second
            out_, prev = [], at_
            for i_, g in enumerate(got):
                t0_, t1_ = g[0], g[1]
                if t0_ is None:
                    nxt = next((h[0] for h in got[i_ + 1:] if h[0] is not None), None)
                    t0_ = prev; t1_ = nxt if nxt is not None and nxt > prev else prev + .25 * max(1, g[4])
                t0_ = max(t0_, prev); t1_ = max(t1_, t0_ + max(.3, (g[3] - g[2]) / 10.0 * .8))
                dmax = max(.6, (g[3] - g[2]) / 2.5)                 # a long spoken stretch: write at the END of it
                if t1_ - t0_ > dmax: t0_ = t1_ - dmax
                out_.append([round(t0_, 3), round(t1_, 3), g[2], g[3]]); prev = t1_
            ln_.setdefault('writes', {})[str(k)] = out_
            rep['write_chunks'].append({'line': n, 'text': text, 'chunks': [[x[0], x[1], text[ch[i][0]:ch[i][1]].strip()] for i, x in enumerate(out_)]})
    json.dump(man, open(mp, 'w'), indent=1, ensure_ascii=False)
    auto_lines(vid, out, man, mp, words, extra_spans, cut, merged, newt, cue_lines, flat, rep)
    rep['patched_paragraphs'] = {str(i + 1): f for i, f in patched.items()}
    rep['changed_not_reread'] = changed
    rep.update(vid=vid, raw_s=round(len(y) / SR, 1), clean_s=round(len(clean) / SR, 1), n_cuts=len(rep['cuts']), unplaced_cues=unplaced,
               words_matched='%d of %d script words' % (len(said), len(S)))
    json.dump(rep, open(os.path.join(out, 'report.json'), 'w'), indent=1, ensure_ascii=False)
    print('%s: %.1f s -> %.1f s, %d cuts, %d silences capped, %s, %d extra stretches kept, %d missing, %d marks unused, %d cues unplaced, %d doubled'
          % (vid, rep['raw_s'], rep['clean_s'], rep['n_cuts'], rep.get('silences_capped', 0), rep['words_matched'], len(rep['kept_extra']),
             len(rep['missing']), len(rep['marks_unused']), len(unplaced), len(rep['doubled'])))
    # Verification is now part of the normal preparation path, not an optional
    # flag that can leave short off-script fragments unchecked before export.
    verify(vid)
    from speech_review import require_ready
    require_ready(out)
    return json.load(open(os.path.join(out, 'report.json')))


# ------------------------------------------------------------------------------------------------ camera lessons
# 2026-10-13: camera lessons (the first lesson of a topic, topic 51) are read with her camera on. A take then has
# <name>.mp4|webm next to <name>.wav, and the sidecar "camera": {file, startOffset, fps, w, h, ...} (reading_studio.py).
# The camera file also holds the same mic (compressed): its audio is matched to the WAV in windows along the take, so
# the WAV -> camera time map is exact (to the sample) and follows every pause (P pauses both; their joins can differ by
# a few ms) and any clock drift. The browser's startOffset is only the starting guess.
#   camera_track(): every frame of the clean timeline -> the same moment of her face: clean time -> (tmap) spliced time
#     -> (source map: full take / patch take, splice_patches) -> WAV time -> camera time. A patch take without a camera
#     (or a lost camera): the bubble fades out (0.3 s) for that stretch and back in - a frozen face looks broken.
#     -> camera.mp4: 30 fps, 1200x600 = the round bubble (mirrored, white ring) on the left, its alpha mask on the right
#        ("stacked alpha"; H.264 has no alpha; the mask is stored in video range 16-235: expand it to 0-255 before use),
#        with the clean audio; camera.json: the map, sync, hidden stretches.
#     Sync check: the camera file's own audio is cut with the same map and matched to clean.wav in windows (report).
#   composite(): overlays the bubble on the rendered board video (studio auto-narrate render / Codex render), lined up
#     by matching the board video's audio to clean.wav; corner and size as the studio's camera bubble.
# Bubble = the studio's (slide_style.py / camRect, drawCam): round, mirrored, centre-square crop, diameter 250 of the
# 1600x900 board (300 px at 1920x1080), 6 board-px from the edges, top right; 6 px white ring (at 1080p), no shadow.
CAM_FPS, CAM_PX = 30, 600                     # camera.mp4 frame rate; bubble size in camera.mp4 (scaled down later)
BUBBLE_D, BUBBLE_M = 250 / 900, 6 / 1600       # bubble diameter / height, margin / width (studio camRect, size 'm')
RING = 6 / 300                                 # ring width / bubble diameter (drawCam: lineWidth 6 at d = 300)
FADE_S = .3


def _ff():
    return A.FFMPEG


def _audio16(path, t0=None, dur=None):
    """any file's audio -> 16 kHz mono float32, its time 0 = the file's time 0 (a late first audio packet is padded)"""
    cmd = [_ff(), '-hide_banner', '-loglevel', 'error']
    if t0: cmd += ['-ss', '%.3f' % t0]
    cmd += ['-i', path]
    if dur: cmd += ['-t', '%.3f' % dur]
    cmd += ['-vn', '-ac', '1', '-af', 'aresample=16000:async=1:first_pts=0', '-f', 'f32le', '-']
    r = subprocess.run(cmd, capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype='<f4').copy()


def _media_info(path):
    """(w, h, fps, duration) from ffmpeg's header print"""
    err = subprocess.run([_ff(), '-hide_banner', '-i', path], capture_output=True, text=True).stderr
    m = re.search(r'Video:.*?(\d{2,5})x(\d{2,5})', err); f = re.search(r'([\d.]+) fps', err) or re.search(r'([\d.]+) tbr', err)
    d = re.search(r'Duration: (\d+):(\d+):([\d.]+)', err)
    dur = int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3)) if d else None
    return (int(m.group(1)), int(m.group(2))) if m else (None, None), float(f.group(1)) if f else None, dur


def _xcorr(x, y):
    """normalised cross-correlation of the short x against every position of the longer y -> array len(y)-len(x)+1"""
    n = len(x); x = x - x.mean(); L = 1 << int(np.ceil(np.log2(len(y) + n)))
    c = np.fft.irfft(np.fft.rfft(y, L) * np.conj(np.fft.rfft(x, L)), L)[:len(y) - n + 1]
    cs = np.concatenate([[0.0], np.cumsum(y.astype('float64'))]); cs2 = np.concatenate([[0.0], np.cumsum(y.astype('float64') ** 2)])
    sy = cs[n:] - cs[:-n]; sy2 = cs2[n:] - cs2[:-n]
    den = np.sqrt(np.maximum(sy2 - sy * sy / n, 1e-12) * max(float((x * x).sum()), 1e-12))
    return c / den


def _peak(r):
    k = int(np.argmax(r)); off = 0.0
    if 0 < k < len(r) - 1:
        a, b, c = r[k - 1], r[k], r[k + 1]; d = a - 2 * b + c
        if d < 0: off = .5 * (a - c) / d
    return k + off, float(r[k])


def match_lag(ref, sig, sr, t_ref, win, guess, span):
    """where ref[t_ref : t_ref+win] (s) is in sig, searched at lag guess +- span (lag = sig time - ref time)
    -> (lag s, score) or None"""
    a, n = int(t_ref * sr), int(win * sr)
    x = ref[a:a + n]
    if len(x) < n or np.sqrt(np.mean(x ** 2)) < 1e-3: return None              # silence: nothing to match
    lo = max(0, int((t_ref + guess - span) * sr)); hi = min(len(sig), int((t_ref + guess + span + win) * sr))
    if hi - lo < n + 2: return None
    k, q = _peak(_xcorr(x, sig[lo:hi]))
    return (lo + k) / sr - t_ref, q


def measure_sync(wav, cam, side):
    """the WAV -> camera time map of one take, from her voice in both files: windows of 6 s every 3 s, per stretch
    between pauses a robust line lag(t) = camera time - WAV time. -> {'segments': [[t0, t1, lag at t0, slope]], ...}"""
    sr = 16000
    a = _audio16(wav); c = _audio16(cam)
    T = len(a) / sr
    cuts = [0.0] + sorted(float(p['at']) for p in side.get('pauses', []) if 'at' in p) + [T]
    guess = -float((side.get('camera') or {}).get('startOffset') or 0.0)
    segs, wins = [], []
    for s0, s1 in zip(cuts, cuts[1:]):
        if s1 - s0 < .05: continue
        pts = []
        for t in np.arange(s0, max(s0, s1 - 6.0) + 1e-6, 3.0):
            w = min(6.0, s1 - t)
            if w < 2.0: continue
            r = match_lag(a, c, sr, t, w, guess, 2.0 if not segs else 1.0)
            if r and r[1] >= .6: pts.append((t + w / 2, r[0], r[1]))
        wins += [[round(t, 2), round(l, 4), round(q, 3)] for t, l, q in pts]
        if pts:
            ls = np.array([p[1] for p in pts]); med = float(np.median(ls))
            inl = [p for p in pts if abs(p[1] - med) < .008]
            if len(inl) >= 4 and inl[-1][0] - inl[0][0] > 30:
                tt = np.array([p[0] for p in inl]); ll = np.array([p[1] for p in inl])
                slope, icpt = np.polyfit(tt, ll, 1); lag0 = float(icpt + slope * s0)
            else:
                slope, lag0 = 0.0, float(np.median([p[1] for p in inl] or [med]))
            guess = lag0 + slope * (s1 - s0)
            segs.append([round(s0, 4), round(s1, 4), round(lag0, 5), float(slope), len(inl), 'measured'])
        else:
            segs.append([round(s0, 4), round(s1, 4), round(guess, 5), 0.0, 0, 'no voice to match: lag of the stretch before'])
    return {'segments': segs, 'windows': wins, 'browser_guess': round(-float((side.get('camera') or {}).get('startOffset') or 0), 4)}


def _lag_at(sync, t):
    for s0, s1, lag0, slope, *_ in sync['segments']:
        if t < s1 + 1e-6: return lag0 + slope * (max(t, s0) - s0)
    s0, s1, lag0, slope = sync['segments'][-1][:4]
    return lag0 + slope * (t - s0)


class _Frames:
    """the camera file as square, mirrored CAM_PX frames at CAM_FPS (frame j = time j / CAM_FPS of the file); read
    forward (re-opened with a seek when asked for an earlier frame)"""
    def __init__(self, path):
        self.path, self.p, self.j, self.last, self.eof = path, None, 0, None, False

    def _open(self, j):
        if self.p: self.p.kill()
        t = j / CAM_FPS
        vf = 'fps=%d:start_time=0,crop=min(iw\\,ih):min(iw\\,ih),scale=%d:%d:flags=lanczos,hflip' % (CAM_FPS, CAM_PX, CAM_PX)
        cmd = [_ff(), '-hide_banner', '-loglevel', 'error'] + (['-ss', '%.4f' % t] if t > 0 else []) + \
              ['-i', self.path, '-an', '-vf', vf, '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-']
        self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL); self.j = j; self.eof = False

    def get(self, j):
        j = max(0, j)
        if self.p is None or j < self.j - 1 or j > self.j + 10 * CAM_FPS: self._open(j)
        if j == self.j - 1 and self.last is not None: return self.last
        n = CAM_PX * CAM_PX * 3
        while self.j <= j and not self.eof:
            b = self.p.stdout.read(n)
            if len(b) < n: self.eof = True; break
            self.last = np.frombuffer(b, np.uint8).reshape(CAM_PX, CAM_PX, 3); self.j += 1
        return self.last

    def close(self):
        if self.p: self.p.kill()


def _bubble_masks(px):
    yy, xx = np.mgrid[0:px, 0:px]; r = np.hypot(xx - (px - 1) / 2, yy - (px - 1) / 2); R = px / 2
    disc = np.clip(R - r + .5, 0, 1)                                   # anti-aliased circle
    ring = np.clip(r - (R - RING * px) + .5, 0, 1) * disc               # the white ring at the edge
    return disc.astype('float32'), ring.astype('float32')


def camera_track(vid, out, base, side, tmap, clean_len):
    """camera.mp4 + camera.json for the clean audio of this video (None: the take has no camera)"""
    def cam_of(wav):
        try: sc = json.load(open(wav[:-4] + '.json')).get('camera') or {}
        except Exception: return None
        f = sc.get('file'); p = os.path.join(os.path.dirname(wav), f) if f else None
        return (p, json.load(open(wav[:-4] + '.json'))) if p and os.path.exists(p) else None
    srcmap = side.get('_srcmap') or [[0.0, None, base + '.wav', 0.0, '']]
    if not cam_of(base + '.wav'):
        for f_ in (out + '/camera.mp4', out + '/camera.json'):
            os.path.exists(f_) and os.remove(f_)
        return None
    srcs = {}
    for _, _, wav, _, _ in srcmap:
        if wav in srcs: continue
        ci = cam_of(wav)
        srcs[wav] = None if not ci else dict(path=ci[0], sync=measure_sync(wav, ci[0], ci[1]), reader=_Frames(ci[0]),
                                             dur=_media_info(ci[0])[2] or 1e9)
    # ---- every output frame: (source wav, camera time) or hidden
    tm = sorted(tmap, key=lambda x: x[2]); starts = [x[2] for x in tm]
    import bisect
    N = int(np.ceil(clean_len * CAM_FPS)); plan = []
    def where(c):
        k = max(0, bisect.bisect_right(starts, c) - 1); a, b, n0 = tm[k]
        yt = min(b, a + (c - n0))
        for s0, s1, wav, src, kind in srcmap:
            if s1 is None or yt < s1 + 1e-9: return wav, src + (yt - s0)
        s0, s1, wav, src, kind = srcmap[-1]; return wav, src + (yt - s0)
    for k in range(N):
        wav, st = where(k / CAM_FPS)
        S_ = srcs.get(wav)
        ct = st + _lag_at(S_['sync'], st) if S_ else None
        # no camera at that moment (its recorder started a moment after the WAV, or stopped before it): hold the
        # nearest frame for up to 1 s, else hide the bubble
        plan.append((wav, min(max(0.0, ct), S_['dur'] - .5 / CAM_FPS)) if S_ and -1.0 < ct < S_['dur'] + 1.0 else None)
    vis = np.array([p is not None for p in plan], float)
    # fades: a hidden stretch fades out / in over FADE_S
    nf = int(FADE_S * CAM_FPS); alpha = vis.copy()
    if not vis.all():
        dp, dn = np.full(N, 1e9), np.full(N, 1e9)          # frames since the last / until the next hidden frame
        for i in range(N): dp[i] = 0 if not vis[i] else (dp[i - 1] + 1 if i else 1e9)
        for i in range(N - 1, -1, -1): dn[i] = 0 if not vis[i] else (dn[i + 1] + 1 if i < N - 1 else 1e9)
        alpha = np.clip(np.minimum(dp, dn) / max(1, nf), 0, 1)
    hidden = []
    for i in range(N):
        if vis[i] == 0 and (i == 0 or vis[i - 1] == 1): hidden.append([round(i / CAM_FPS, 3), None])
        if vis[i] == 0 and (i == N - 1 or vis[i + 1] == 1): hidden[-1][1] = round((i + 1) / CAM_FPS, 3)
    # ---- frames -> camera.mp4 (bubble | alpha), with the clean audio
    disc, ring = _bubble_masks(CAM_PX); ring3 = ring[..., None]
    mp = os.path.join(out, 'camera.mp4'); tmp = mp + '.part.mp4'
    enc = subprocess.Popen([_ff(), '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (2 * CAM_PX, CAM_PX),
                            '-r', str(CAM_FPS), '-i', '-', '-i', os.path.join(out, 'clean.wav'), '-map', '0:v', '-map', '1:a',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k',
                            '-movflags', '+faststart', tmp], stdin=subprocess.PIPE)
    last = np.zeros((CAM_PX, CAM_PX, 3), np.uint8); buf = np.zeros((CAM_PX, 2 * CAM_PX, 3), np.uint8)
    for k, p in enumerate(plan):
        if p is not None:
            fr = srcs[p[0]]['reader'].get(int(round(p[1] * CAM_FPS)))
            if fr is not None: last = fr
        col = (last.astype('float32') * (1 - ring3) + 255 * ring3)
        buf[:, :CAM_PX] = col.astype(np.uint8)
        buf[:, CAM_PX:] = (disc * alpha[k] * 255 + .5).astype(np.uint8)[..., None]
        enc.stdin.write(buf.tobytes())
    enc.stdin.close(); enc.wait()
    for S_ in srcs.values():
        if S_: S_['reader'].close()
    assert enc.returncode == 0, 'camera.mp4 encoding failed'
    os.replace(tmp, mp)
    # ---- sync check: the camera files' own audio, cut with the same map, against clean.wav
    check = _sync_check(out, plan, srcs, N)
    info = {'file': 'camera.mp4', 'fps': CAM_FPS, 'layout': 'stacked alpha: left %dx%d = the bubble (mirrored, ring), right = its alpha mask' % (CAM_PX, CAM_PX),
            'duration': round(N / CAM_FPS, 3), 'clean_duration': round(clean_len, 3),
            'sources': {os.path.basename(w): (None if not S_ else {'camera': os.path.basename(S_['path']), 'segments': S_['sync']['segments'],
                         'browser_guess_lag': S_['sync']['browser_guess'], 'windows_matched': len(S_['sync']['windows'])}) for w, S_ in srcs.items()},
            'keep_map': [[round(n0, 5), round(n0 + (b - a), 5), round(a, 5)] for a, b, n0 in tm],
            'source_map': [[round(s0, 5), None if s1 is None else round(s1, 5), os.path.basename(w), round(src, 5), k_] for s0, s1, w, src, k_ in srcmap],
            'hidden': hidden, 'hidden_rule': 'stretches from a take without a camera: the bubble fades out (%.1f s) and back in' % FADE_S,
            'sync_check': check,
            'bubble': {'shape': 'circle, mirrored, centre-square crop of the camera', 'diameter_of_height': round(BUBBLE_D, 5),
                       'margin_of_width': round(BUBBLE_M, 5), 'ring_of_diameter': RING, 'corner': 'top right (composite() picks a free corner)'}}
    json.dump(info, open(os.path.join(out, 'camera.json'), 'w'), indent=1)
    return {k: info[k] for k in ('file', 'duration', 'hidden', 'sync_check', 'sources')}


def _sync_check(out, plan, srcs, N):
    """cut the camera files' audio exactly as the frames were picked (each frame's 1/30 s of audio from the same camera
    time) and match it to clean.wav in 4 s windows: the lag left after all cuts / splices (0 = in sync). The frames
    themselves are the nearest frame to that time (at most half a frame, 17 ms, off)."""
    sr = 16000; aud = {w: _audio16(S_['path']) for w, S_ in srcs.items() if S_}
    outa = np.zeros(int(np.ceil(N * sr / CAM_FPS)) + 1, 'float32')
    for k, p in enumerate(plan):
        if p is None: continue
        o0, o1 = int(round(k * sr / CAM_FPS)), int(round((k + 1) * sr / CAM_FPS))
        a = aud[p[0]]; i = int(round(p[1] * sr))
        seg = a[i:i + o1 - o0]; outa[o0:o0 + len(seg)] = seg
    clean = _audio16(os.path.join(out, 'clean.wav'))
    lags = []
    for t in np.arange(0, len(clean) / sr - 4, 2.0):
        r = match_lag(clean, outa, sr, t, 4.0, 0.0, .25)
        if r and r[1] >= .5: lags.append((round(float(t), 1), round(r[0] * 1000, 1)))
    if not lags: return {'windows': 0}
    ab = [abs(l) for _, l in lags]
    return {'windows': len(lags), 'median_ms': float(np.median([l for _, l in lags])), 'max_abs_ms': max(ab),
            'over_20ms': [x for x in lags if abs(x[1]) > 20][:20], 'frame_rounding_ms': round(500 / CAM_FPS, 1)}


def _board_corners(board, W, H, D, m):
    """how much of each candidate bubble corner is covered by board content (text, figures, sidebar items) over the
    video: sampled every 2 s at 1/4 size; a pixel is content when it differs from that corner's own background"""
    sw, sh = W // 4, H // 4
    r = subprocess.run([_ff(), '-hide_banner', '-loglevel', 'error', '-i', board, '-an', '-vf', 'fps=1/2,scale=%d:%d,format=gray' % (sw, sh),
                        '-f', 'rawvideo', '-'], capture_output=True, check=True)
    fr = np.frombuffer(r.stdout, np.uint8).reshape(-1, sh, sw)
    d, mm = D // 4 + 2, m // 4
    boxes = {'tr': (mm, sw - mm - d), 'br': (sh - mm - d, sw - mm - d), 'bl': (sh - mm - d, mm), 'tl': (mm, mm)}
    yy, xx = np.mgrid[0:d, 0:d]; circ = np.hypot(xx - d / 2, yy - d / 2) <= d / 2 + 3        # the bubble + a margin
    out = {}
    for name, (y0, x0) in boxes.items():
        reg = fr[:, y0:y0 + d, x0:x0 + d][:, circ].astype(int)
        bg = np.median(reg, axis=1, keepdims=True)
        cov = (np.abs(reg - bg) > 40).mean(axis=1)
        out[name] = {'max': round(float(cov.max()), 4), 'mean': round(float(cov.mean()), 4), 'frames_hit': int((cov > .003).sum()), 'frames': len(cov)}
    return out


def composite(vid, board, dest=None, corner=None):
    """the rendered board video of a camera lesson + her face bubble -> <dest> (default: next to the board video,
    '<name> - camera.mp4'). The board video's audio must be her clean audio (any lead-in is found by matching)."""
    out = os.path.join(OUTROOT, vid); cj = json.load(open(os.path.join(out, 'camera.json')))
    cam = os.path.join(out, cj['file'])
    (W, H), fps, dur = _media_info(board)
    D = int(round(BUBBLE_D * H)); m = int(round(BUBBLE_M * W))
    # board time of clean time 0: match the first 40 s of the clean audio in the board audio (lead-in up to 60 s)
    sr = 16000; ba = _audio16(board, dur=180); ca = _audio16(os.path.join(out, 'clean.wav'), dur=60)
    best = None
    for t in (2.0, 10.0, 20.0):
        r = match_lag(ca, ba, sr, t, 8.0, 30.0, 30.0)
        if r and (best is None or r[1] > best[1]): best = r
    if not best or best[1] < .6: raise SystemExit('composite: the board video audio does not match clean.wav of ' + vid)
    lead = best[0]
    cov = _board_corners(board, W, H, D, m)
    if not corner:
        # the studio's corner (top right) when the board leaves it free; else the freest of the other corners
        order = ['tr', 'br', 'bl', 'tl']
        free = [c for c in order if cov[c]['max'] < .01]
        corner = free[0] if free else min(order, key=lambda c: (cov[c]['frames_hit'], cov[c]['mean']))
    x = W - m - D if corner in ('tr', 'br') else m; y = m if corner in ('tr', 'tl') else H - m - D
    dest = dest or os.path.splitext(board)[0] + ' - camera.mp4'
    fc = ('[1:v]split[a][b];[a]crop=%d:%d:0:0[c];[b]crop=%d:%d:%d:0,format=gray,lut=c0=clip((val-16)*255/219\\,0\\,255)[k];[c][k]alphamerge,scale=%d:%d:flags=lanczos[bub];'
          '[0:v][bub]overlay=%d:%d:eof_action=pass:format=auto,format=yuv420p[v]') % (CAM_PX, CAM_PX, CAM_PX, CAM_PX, CAM_PX, D, D, x, y)
    subprocess.run([_ff(), '-hide_banner', '-loglevel', 'error', '-y', '-i', board, '-itsoffset', '%.4f' % lead, '-i', cam,
                    '-filter_complex', fc, '-map', '[v]', '-map', '0:a?', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                    '-r', '%g' % (fps or 30), '-c:a', 'copy', '-movflags', '+faststart', dest], check=True)
    rep = {'board': board, 'out': dest, 'lead_s': round(lead, 4), 'lead_match': round(best[1], 3), 'corner': corner,
           'bubble_px': [x, y, D], 'corner_cover': cov}
    json.dump(rep, open(os.path.join(out, 'composite.json'), 'w'), indent=1)
    print('%s composite: %s (corner %s, bubble %d px at %d,%d, board lead %.3f s)' % (vid, dest, corner, D, x, y, lead))
    return rep


def newest_board(vid):
    """the newest studio take of this video (auto-narrate render) in Course.recordings, outside the '_' folders"""
    best = None
    for root, dirs, files in os.walk(REC):
        dirs[:] = [d for d in dirs if not d.startswith('_')]
        for f in files:
            if re.match(re.escape(vid) + r'-\d{4}-.*\.(mp4|webm)$', f) and ' - camera' not in f:
                p = os.path.join(root, f)
                if best is None or os.path.getmtime(p) > os.path.getmtime(best): best = p
    return best


def verify(vid):
    """transcribe the CLEAN audio again and check it against the script: every sentence once, in order; no filler or
    leftover restart. -> report.json['verify']"""
    out = os.path.join(OUTROOT, vid)
    man = json.load(open(os.path.join(out, 'manifest.json')))
    lines = [l['text'] for l in man['lines']]
    from speech_review import digest, evaluate
    p = os.path.join(out, 'clean_transcript.json')
    meta_path = os.path.join(out, 'clean_transcript-meta.json')
    cache_key = dict(audio_sha256=digest(os.path.join(out, 'clean.wav')), window_algorithm='two-sided-core-v2', model=os.environ.get('READING_VERIFY_MODEL', 'small.en'))
    if os.path.exists(p) and os.path.exists(meta_path) and json.load(open(meta_path)) == cache_key: words = json.load(open(p))
    else:
        os.path.exists(p) and os.remove(p)
        words = transcribe_chunks(os.path.join(out, 'clean.wav'), p)
        json.dump(cache_key, open(meta_path, 'w'), indent=2)
    W, Wt = [], []
    for k, w in enumerate(words):
        for tok in norm_tokens(w['w']): W.append(tok); Wt.append((w['s'], w['e'], k))
    sents = []
    for li, t in enumerate(lines):
        for sm in re.findall(r'[^.?!]+[.?!]?', t):
            st = norm_tokens(sm)
            if st: sents.append((li + 1, sm.strip(), st))
    S = [tok for _, _, st in sents for tok in st]; owner = [k for k, (_, _, st) in enumerate(sents) for _ in st]
    W, S = a_hundred(W), a_hundred(S)
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
    raw_path = os.path.join(out, 'transcript.json')
    rep['speech_review'] = evaluate(out, words, norm_tokens, rep, json.load(open(raw_path)) if os.path.exists(raw_path) else None)
    json.dump(rep, open(rp, 'w'), indent=1, ensure_ascii=False)
    print('%s verify: %d sentences missing, %d doubled, %d extra runs (3+ words), %d fillers' % (vid, len(missing), len(doubled), len(extra), len(fill)))
    return rep['verify']


if __name__ == '__main__':
    args = sys.argv[1:]                      # (run() resets sys.argv for ai_narrate)
    if args and args[0] == '--composite':    # reading_to_video.py --composite <vid> [board.mp4] [out.mp4] [--corner tr|br|bl|tl]
        c_ = args[args.index('--corner') + 1] if '--corner' in args else None
        pos = [a for a in args[1:] if not a.startswith('--') and a != c_]
        board_ = pos[1] if len(pos) > 1 else newest_board(pos[0])
        assert board_, 'no rendered board video of %s found in %s - pass its path' % (pos[0], REC)
        composite(pos[0], board_, pos[2] if len(pos) > 2 else None, c_)
        sys.exit(0)
    ids = [a for a in args if not a.startswith('--')] or sorted(os.listdir(IN))
    for v in ids:
        if '--verify-only' not in args: run(v)
        if '--verify-only' in args: verify(v)
        from speech_review import require_ready
        require_ready(os.path.join(OUTROOT, v))
