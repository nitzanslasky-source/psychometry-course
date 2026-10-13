"""Reading Studio: one HTML page where the teacher records herself (audio only) reading the AI scripts aloud.

    python3 reading_studio.py 13                 # topic 13 -> ~/Downloads/Reading-Studio.html
    python3 reading_studio.py 13 14              # several topics in one page (grouped in the list)
    python3 reading_studio.py --ids a,b,c        # explicit video ids (ai_scripts/<id>.json)
    python3 reading_studio.py 13 -o out.html

The takes serve two uses: clean training audio for her ElevenLabs Professional Voice Clone, and the narration of the
video itself (the auto-narrate pipeline aligns her audio to the words). So the page records LOSSLESS WAV (16-bit PCM,
mono, 48 kHz) through an AudioWorklet (ScriptProcessor fallback), with echoCancellation / noiseSuppression /
autoGainControl all OFF.

Video list of a topic: the overview table of ~/Downloads/Topic-<N>-AI-scripts-review.md (its order, titles and
lengths); without that file, the topic's videos in course18.json that have an ai_scripts/<id>.json.
Script text: every spoken line of ai_scripts/<id>.json is one paragraph, tags ([pause], [short pause], [excited],
<break .../>, ...) stripped - the same text as ~/Downloads/Topic 13 - reading scripts/Topic-13-reading-scripts.html.

Saving (same approach as the teacher studio, studio_patch.py RF / saveTakeFile): File System Access API. The folder is
picked once (Course.recordings) and remembered in IndexedDB 'studio-rec-folder' (store 'h') under the key
'reading-dir'; if not picked yet, the main studio's own folder (key 'dir', same DB) is used read-only as the default.
Takes go to  Course.recordings/_reading/<videoId>/<videoId>-<ISO time>.wav  + a sidecar <same name>.json (paragraph
start times, mistake marks, mic, sample rate). The '_' folder is skipped by studio_done.takes()/recorded_ids(), so
these never count as camera takes. Every take is kept; the newest wins. Without the API (Safari/Firefox) both files
are downloaded instead.

Re-read (patch) mode: when a script paragraph changes after a take, she selects just those paragraphs (the changed ones
are pre-selected) and records a patch take <videoId>-patch-<ISO time>.wav + .json ("kind": "patch", "paragraphs":
[{i, text}] = index in the current script and its text). The teleprompter then shows only those paragraphs, with the
neighbouring paragraphs greyed as context.

Camera mode (2026-10-13): camera lessons (camera_ids(): the first lesson of every math topic + all of topic 51) are read
with her camera on. A per-video "Camera on" toggle (default on for camera lessons, remembered per video), camera choice
and a live round self-preview. With it on, every take (full or patch) also records <same name>.mp4 (H.264, Chrome) or
.webm (VP9/VP8) with MediaRecorder at up to 1920x1080 / 30 fps, started, paused and stopped together with the WAV; the
file also carries the same mic (compressed), used only to sync it to the WAV exactly. The sidecar gets
"camera": {file, startOffset (camera start - WAV start, s), fps, w, h, mime, t0/cameraStartMs/wavStartMs, pauses, ...}.
With the camera off nothing changes. reading_to_video.py cuts the camera video like the audio and composites the bubble.

Change detection (generator and page, same rule): a current paragraph whose
text is not among the paragraphs of her last FULL take's sidecar, nor of a patch take made after it, is "changed"; the
list shows "needs re-read: N paragraphs".
"""
import argparse, glob, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, 'ai_scripts')
DOWNLOADS = os.path.expanduser('~/Downloads')
READING_ROOT = os.path.expanduser('~/Documents/Course.recordings/_reading')
OUT = os.path.join(DOWNLOADS, 'Reading-Studio.html')
WPM = 150          # her reading pace estimate when the review file gives no length
TAKE = re.compile(r'^(.+)-(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z)\.wav$')
PATCH = re.compile(r'^(.+)-patch-(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z)\.wav$')   # re-read of a few paragraphs


def plain(s):
    """spoken text without voice tags: [pause], [short pause], [excited], <break time="1s"/>, ..."""
    s = re.sub(r'<[^>]*>', ' ', s)
    s = re.sub(r'\[[^\]]*\]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s+([,.;:?!])', r'\1', s)
    return s


# =================================================================================================================
# DISPLAY ONLY: numbers and math as figures and symbols on the teleprompter ("one thousand three hundred twenty" ->
# "1320", "x minus two" -> "x − 2", "seven squared" -> "7²"). The script text (ai_scripts, sidecars, change detection,
# alignment) stays in words. A small, conservative rule set:
#   - multi-word numbers and numbers >= 10 always become digits; 0-9 only in math: next to a converted operator, after
#     negative/minus, "number"/"choice number", "equal(s) to", "<letter> is", smaller/bigger/less/greater than,
#     at least/most, before squared/cubed/power, in lists of 3+ numbers, fractions ("three eighths" -> 3/8);
#   - operator words become symbols only BETWEEN two operands (a number or a single letter b-z, after powers/roots):
#     times ×, plus +, minus −, divided by ÷, over /, is equal to / equals =;
#   - powers (squared ², cubed ³, to the power of N), "the square root of" √, "the absolute value of x" |x| (only
#     when no operator follows), "negative N" −N.
# =================================================================================================================
_UNITS = 'zero one two three four five six seven eight nine'.split()
_TEENS = 'ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
_TENS = 'twenty thirty forty fifty sixty seventy eighty ninety'.split()
_NV = {w: i for i, w in enumerate(_UNITS)}
_NV.update({w: 10 + i for i, w in enumerate(_TEENS)})
_NV.update({w: 20 + 10 * i for i, w in enumerate(_TENS)})
_SUP = str.maketrans('0123456789n', '⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ')
_FRAC = {'half': 2, 'halves': 2, 'third': 3, 'thirds': 3, 'quarter': 4, 'quarters': 4, 'fourth': 4, 'fourths': 4,
         'fifths': 5, 'sixths': 6, 'sevenths': 7, 'eighths': 8, 'ninths': 9, 'tenths': 10}
_TOK = re.compile(r"[A-Za-z]+|[^A-Za-z]")



# Spoken shorthand is expanded only for display, never for take text/alignment.
_ORDINAL = dict(zip(
    'half third quarter fourth fifth sixth seventh eighth ninth tenth eleventh twelfth thirteenth fourteenth fifteenth sixteenth seventeenth eighteenth nineteenth'.split(),
    [2, 3, 4] + list(range(4, 20))))
_ORDINAL.update(dict(zip(
    'twentieth thirtieth fortieth fiftieth sixtieth seventieth eightieth ninetieth'.split(),
    range(20, 100, 10))))
for _tens, _value in zip(_TENS, range(20, 100, 10)):
    for _unit, _uv in dict(first=1, second=2, third=3, fourth=4, fifth=5,
                           sixth=6, seventh=7, eighth=8, ninth=9).items():
        _ORDINAL[_tens + '-' + _unit] = _value + _uv
_FRACTION_WORDS = dict(_ORDINAL)
_FRACTION_WORDS.update({k + 's': v for k, v in _ORDINAL.items() if k != 'half'})
_FRACTION_WORDS['halves'] = 2
_CARDINAL_WORD = '(?:' + '|'.join(_NV) + '|hundred|thousand|and|a)'
_FRACTION_RX = re.compile(r'\b((?:' + '|'.join(_NV) + r'|a)(?:[ -]+' + _CARDINAL_WORD + r')*) (' +
                          '|'.join(sorted(_FRACTION_WORDS, key=len, reverse=True)) + r')\b', re.I)
_SHORT_NUMBER_RX = re.compile(r'\b(' + '|'.join(_UNITS[1:]) + r') (' +
    '|'.join(_TEENS + [t + r'(?:-(?:' + '|'.join(_UNITS[1:]) + r'))?' for t in _TENS]) +
    r')\b(?!-[A-Za-z])', re.I)

def _display_number_input(text):
    """Protect fraction denominators before parsing cardinal-number runs."""
    fractions = []
    def fraction(m):
        encoded, parsed = _numbers(m.group(1))
        if len(parsed) != 1 or encoded != '\ue0000\ue001':
            return m.group(0)
        numerator = parsed[0][1]
        name = m.group(2).lower()
        if (numerator == 1) != (not name.endswith('s')):
            return m.group(0)
        fractions.append('%d/%d' % (numerator, _FRACTION_WORDS[name]))
        return '\ue002%d\ue003' % (len(fractions)-1)
    text = _FRACTION_RX.sub(fraction, text)
    text = re.sub(r'\b(' + '|'.join(_UNITS[1:]) + r') oh (' + '|'.join(_UNITS) + r')\b',
        lambda m: m.group(1) + ' hundred ' + m.group(2), text, flags=re.I)
    text = _SHORT_NUMBER_RX.sub(lambda m: m.group(1) + ' hundred ' + m.group(2), text)
    return text, fractions


def _numbers(text):
    """text with every number phrase replaced by \\ue000<k>\\ue001; returns (text, [(raw, value, words)])"""
    toks = _TOK.findall(text); out = []; nums = []; i = 0
    def word(j):
        return toks[j].lower() if j < len(toks) and toks[j].isalpha() else None
    while i < len(toks):
        w = word(i); start = i; j = i; lead_a = False
        if w == 'a' and toks[i + 1:i + 2] == [' '] and word(i + 2) in ('hundred', 'thousand'):
            lead_a = True; j = i + 2; w = word(j)
        if w not in _NV and not (lead_a and w in ('hundred', 'thousand')):
            out.append(toks[i]); i += 1; continue
        total, cur, last, nw, end = 0, (1 if lead_a else 0), ('unit' if lead_a else None), 0, j
        while True:
            w = word(j)
            if w is None:
                break
            # A digit-count adjective starts a new phrase: "sixty three-digit" is
            # 60 three-digit numbers, never a 63-digit number.
            if j > start and toks[j - 1:j] == [' '] and toks[j + 1:j + 2] == ['-'] and word(j + 2) in ('digit', 'digits'):
                break
            # Ordinals are not cardinal runs ("twenty-first" must not become "20-first").
            if toks[j + 1:j + 2] == ['-'] and w + '-' + (word(j + 2) or '') in _ORDINAL:
                break
            v = _NV.get(w); kind = None
            if w == 'zero':
                kind = 'zero' if last is None else None
            elif v is not None and v < 10:
                kind = 'unit' if last in (None, 'tens', 'hundred', 'thousand', 'and') else None
            elif v is not None and v < 20:
                kind = 'teen' if last in (None, 'hundred', 'thousand', 'and') else None
            elif v is not None:
                kind = 'tens' if last in (None, 'hundred', 'thousand', 'and') else None
            elif w == 'hundred':
                kind = 'hundred' if last in ('unit', 'teen') and cur < 100 else None
            elif w == 'thousand':
                kind = 'thousand' if last in ('unit', 'teen', 'tens', 'hundred') and total == 0 else None
            elif w == 'and':
                kind = 'and' if (last in ('hundred', 'thousand') and word(j + 2) in _NV and toks[j + 1:j + 2] == [' ']
                                 and word(j + 4) not in ('hundred', 'thousand')) else None   # "a hundred and two hundred fifty" = 2 numbers
            if kind is None:
                break
            if kind == 'hundred':
                cur *= 100
            elif kind == 'thousand':
                total += cur * 1000; cur = 0
            elif kind != 'and':
                cur += v
            last = kind; nw += kind != 'and'; end = j + 1
            sep = toks[j + 1] if j + 1 < len(toks) else ''
            if sep in (' ', '-') and word(j + 2) is not None:
                j += 2
            else:
                break
        if last in (None, 'and'):
            out.append(toks[i]); i += 1; continue
        raw = ''.join(toks[start:end]); nums.append((raw, total + cur, nw + lead_a))
        out.append('%d' % (len(nums) - 1)); i = end
    return ''.join(out), nums


_N = r'\d+'
_L = r"(?<![A-Za-z0-9'’])[b-hj-z](?![A-Za-z0-9'’])"   # a one-letter variable (not a / I)
_ATOM = r"(?:−?(?:%s|\d+/\d+|(?<![A-Za-z0-9'’])[b-hj-z](?![A-Za-z0-9'’])|\|[^|\s]+\||√[^\s,.;:?!]+)[⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ^]*)" % _N


def math_display(text):
    display_input, fractions = _display_number_input(text)
    s, nums = _numbers(display_input)
    s = re.sub(r'\ue002(\d+)\ue003', lambda m: fractions[int(m.group(1))], s)
    mark = set(i for i, (raw, v, nw) in enumerate(nums) if nw > 1 or v >= 10)
    def m_all(t):
        mark.update(int(k) for k in re.findall(r'(\d+)', t)); return t
    def num_of(t):
        k = re.fullmatch(r'(\d+)', t)
        return nums[int(k.group(1))][1] if k else None
    # negative N / negative x
    s = re.sub(r'\b[Nn]egative (%s|%s)' % (_N + r'|\d+/\d+', _L), lambda m: '−' + m_all(m.group(1)), s)
    # A negative/fractional base needs brackets; otherwise -2² reads as -(2²).
    def power_base(base):
        base = m_all(base)
        return '(' + base + ')' if base.startswith('−') or '/' in base else base
    # powers
    s = re.sub(r'(%s) squared\b' % _ATOM, lambda m: power_base(m.group(1)) + '²', s)
    s = re.sub(r'(%s) cubed\b' % _ATOM, lambda m: power_base(m.group(1)) + '³', s)
    def pw(m):
        base, e = power_base(m.group(1)), m.group(2); v = num_of(e)
        return base + (str(v).translate(_SUP) if v is not None else (e.translate(_SUP) if e == 'n' else '^' + e))
    s = re.sub(r'(%s) to the power of (%s|[a-z]\b)' % (_ATOM, _N), pw, s)
    # roots, absolute values (a lone operand, no operator after it)
    s = re.sub(r'\b(?:the )?square root of (%s)' % _ATOM, lambda m: '√' + (lambda o: '(%s)' % o if re.search('[⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ^/]', o) else o)(m_all(m.group(1))), s)
    s = re.sub(r'\b[Tt]he absolute value of (%s)(?!,? (?:times|plus|minus|over|divided)\b)' % _ATOM,
               lambda m: '|' + m_all(m.group(1)) + '|', s)
    # binary operators between two operands (repeat for chains)
    ops = [(r'times', ' × '), (r'plus', ' + '), (r'minus', ' − '), (r'divided by', ' ÷ '), (r'over', '/'),
           (r'is equal to', ' = '), (r'equals', ' = ')]
    s = re.sub(r"(?<![A-Za-z0-9'’])a,? (times|plus|minus) (%s)" % _L, lambda m: 'a ' + dict(times='×', plus='+', minus='−')[m.group(1)] + ' ' + m.group(2), s)
    for _ in range(4):
        before = s
        for w, sym in ops:
            s = re.sub(r'(%s),? %s (%s)' % (_ATOM, w, _ATOM), lambda m: m_all(m.group(1)) + sym + m_all(m.group(2)), s)
        if s == before:
            break
    # unary minus before a number
    s = re.sub(r'\b[Mm]inus (%s)' % _N, lambda m: '−' + m_all(m.group(1)), s)
    # contexts that make a small number math
    for rx in [r'\b[Nn]umber (%s)', r'\bequals? to (%s)', r'\bequals (%s)',
               _L.replace('%', '%%') + r" is (%s)", r"[²³⁴⁵⁶⁷⁸⁹ⁿ|] is (%s)",
               r'\b(?:smaller|bigger|less|greater|larger) than (%s)(?! of\b)', r'\bat (?:least|most) (%s)(?! of\b)',
               r'(?:[×+÷=/]|−) ?(%s)']:
        s = re.sub(rx % _N, lambda m: m.group(0)[:m.start(1) - m.start(0)] + m_all(m.group(1)), s)
    # "<converted number> is N": "x + 7 is nine" -> "x + 7 is 9"
    s = re.sub(r'(\d+) is (%s)' % _N,
               lambda m: m.group(0) if int(m.group(1)) not in mark else m.group(0)[:m.start(2) - m.start(0)] + m_all(m.group(2)), s)
    # "four is smaller than 7" -> "4 is smaller than 7" (the other side is already a figure); "four k = m" -> "4k = m"
    s = re.sub(r'(%s) ((?:is )?(?:smaller|bigger|less|greater|larger) than )(\ue000(\d+)\ue001|\d|−)' % _N,
               lambda m: (m_all(m.group(1)) if (m.group(4) is None or int(m.group(4)) in mark) else m.group(1)) + ' ' + m.group(2) + m.group(3), s)
    s = re.sub(r'(%s) (%s)(?= [=×+−÷])' % (_N, _L), lambda m: m_all(m.group(1)) + m.group(2), s)
    # fractions: "three eighths" -> 3/8 (number word + a plural fraction word, or one + half/third/quarter)
    def fr(m):
        v = num_of(m.group(1)); d = _FRAC[m.group(2).lower()]
        if v is None or (v == 1) != (not m.group(2).endswith('s')) and m.group(2) not in ('halves',):
            return m.group(0)
        mark.discard(int(m.group(1)[1:-1])); return '%d/%d' % (v, d)
    s = re.sub(r'(%s) (%s)\b' % (_N, '|'.join(_FRAC)), fr, s)
    # lists of three or more numbers
    item = r'−?%s' % _N
    s = re.sub(r'%s(?:, %s)*,? (?:and|or) %s' % (item, item, item),
               lambda m: m_all(m.group(0)) if len(re.findall(_N, m.group(0))) >= 3 else m.group(0), s)
    def back(m):
        k = int(m.group(1)); raw, v, nw = nums[k]
        return str(v) if k in mark else raw
    return re.sub(r'(\d+)', back, s)


_PROMPTER_FORMATTER = None

def prompter_display(video_id, paras):
    """Presentation only; never change narration or recording paragraph indices."""
    global _PROMPTER_FORMATTER
    path = os.path.join(HERE, 'math_patches', '_codex_reading_display_20261012.py')
    if os.path.exists(path):
        if _PROMPTER_FORMATTER is None:
            import importlib.util
            spec = importlib.util.spec_from_file_location('codex_reading_display', path)
            _PROMPTER_FORMATTER = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(_PROMPTER_FORMATTER)
        return _PROMPTER_FORMATTER.display_for(video_id, paras, READING_ROOT, math_display)
    return [[math_display(p) for p in slide] for slide in paras]


def paragraphs(vid):
    """[[paragraph, ...] per slide] of ai_scripts/<vid>.json"""
    d = json.load(open(os.path.join(SCRIPTS, vid + '.json'), encoding='utf-8'))
    out = []
    for sl in d['slides']:
        ps = [plain(it['say'] if isinstance(it, dict) else it) for it in (sl if isinstance(sl, list) else [sl])]
        ps = [p for p in ps if p]
        if ps:
            out.append(ps)
    return out


def clean_title(t):
    t = t.strip()
    t = re.sub(r'^Question:\s*', '', t)
    # 2026-10-13 (Codex review standard 9, display only): keep the fraction slash in \frac3x, and group a numerator /
    # denominator / root that holds more than one term: (x-y)²/(xy³), √(8x²+y²)
    t = re.sub(r'\\frac(\d)([A-Za-z\d])', r'\1/\2', t)
    _atom = lambda x: bool(re.fullmatch(r'[\\\w◆#]*\((?:[^()]|\([^()]*\))*\)(?:\^\{?\w+\}?)?', x))
    _multi = lambda x: not _atom(x) and bool(re.search(r'[-+−·\s]', x))
    _den = lambda x: _multi(x) or not (_atom(x) or x.isdigit() or re.fullmatch(r'\|[^|]*\|', x)) and len(re.sub(r'\^\{?\w+\}?', '', x)) > 1
    t = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', lambda m: ('(%s)' % m.group(1) if _multi(m.group(1)) else m.group(1)) + '/' +
               ('(%s)' % m.group(2) if _den(m.group(2)) else m.group(2)), t)
    t = re.sub(r'\\sqrt\{([^{}]*)\}', lambda m: '√(%s)' % m.group(1) if _multi(m.group(1)) else '√' + m.group(1), t)
    t = re.sub(r'\\ne(?![a-z])', '≠', t)
    t = re.sub(r'\\(?:begin|end)\{\w+\}', ' ', t).replace('&', ' ')
    t = re.sub(r'\^\{?(\d+|n)\}?', lambda m: m.group(1).translate(_SUP), t)
    t = re.sub(r'\s*\\cdot\s*', '·', t)
    for a, b in [('\\\\', '; '), (r'\cdot', '·'), (r'\left', ''), (r'\right', ''), (r'\leq', '≤'), (r'\geq', '≥'), (r'\le', '≤'), (r'\ge', '≥'),
                 (r'\neq', '≠'), (r'\sqrt', '√'), (r'\frac', ''), (r'\cdot', '·'), ('\\', ''), ('{', ''), ('}', '')]:
        t = t.replace(a, b)
    return re.sub(r'\s+', ' ', t).strip()


# =================================================================================================================
# CAMERA LESSONS (2026-10-13): the FIRST lesson video of every math topic (course order) and every video of topic 51
# (Psychometric Thinking) are recorded with her camera on (face bubble in the final video). Derived from the exported
# course order (~/psychometry-course/content/full-course: outline.json + topics/t<N>.json; the first video step that is
# not a solve-/summary video); the fallback list below is the same derivation as of 2026-10-13. Add/remove single ids
# with CAMERA_EXTRA / CAMERA_SKIP. On the page "Camera on" defaults to on for these and can be switched per video.
# =================================================================================================================
CAMERA_SUBJECTS = ('algebra', 'word-problems', 'geometry', 'charts')     # the math subjects
CAMERA_ALL_TOPICS = (51,)                                                   # every video of these topics
CAMERA_EXTRA, CAMERA_SKIP = set(), set()
CAMERA_FALLBACK = (
    'numbers fraction-basics compare-fractions expression-basics expression-strategy linear-equations equation-strategy '
    'exponents roots powers-techniques advanced-powers inequalities absolute-value primes divisibility whole-numbers '
    'number-line digit-puzzles new-operation algebraic-understanding wp-001 wp-027 wp-052 wp-067 wp-080 wp-092 wp-106 '
    'wp-123 wp-146 geo-001 geo-009 geo-042 geo-074 geo-104 geo-119 geo-134 geo-154 geo-172 ch52-intro').split()
FULL_COURSE = os.path.join(os.path.dirname(HERE), 'content', 'full-course')


def camera_ids():
    """the video ids recorded with the camera on (see CAMERA LESSONS above)"""
    ids = set()
    try:
        outline = json.load(open(os.path.join(FULL_COURSE, 'outline.json'), encoding='utf-8'))
        for s in outline['subjects']:
            for t in s['topics']:
                T = json.load(open(os.path.join(FULL_COURSE, 'topics', 't%d.json' % t['id']), encoding='utf-8'))
                vids = [st['id'] for sec in T['sections'] for st in sec['steps'] if st.get('kind') == 'video']
                if t['id'] in CAMERA_ALL_TOPICS:
                    ids.update(vids)
                elif s.get('key') in CAMERA_SUBJECTS:
                    first = next((v for v in vids if not v.startswith('solve-') and 'summary' not in v), None)
                    if first:
                        ids.add(first)
    except Exception:
        ids = set()
    if not ids:
        ids = set(CAMERA_FALLBACK)
    return (ids | CAMERA_EXTRA) - CAMERA_SKIP


def from_review(topic):
    """[(id, title, minutes)] from ~/Downloads/Topic-<N>-AI-scripts-review.md (its order), or None"""
    p = os.path.join(DOWNLOADS, 'Topic-%d-AI-scripts-review.md' % topic)
    if not os.path.exists(p):
        return None
    s = open(p, encoding='utf-8').read()
    m = re.search(r'^# Topic \d+ \(([^)]*)\)', s, re.M)
    ttitle = m.group(1) if m else ''
    rows = re.findall(r'^\|\s*\d+\s*\|\s*([\w-]+)\s*\|\s*([\d.]+)\s*\|\s*(\w+)\s*\|', s, re.M)
    out = []
    for vid, mins, kind in rows:
        sec = re.search(r'^## \d+\. ' + re.escape(vid) + r'\s*\n+\*\*(.+?)\*\*', s, re.M)
        out.append(dict(id=vid, title=clean_title(sec.group(1)) if sec else vid, minutes=float(mins), kind=kind))
    return ttitle, out


def from_course(topic):
    D = json.load(open(os.path.join(HERE, 'course18.json'), encoding='utf-8'))
    T = next((t for t in D['topics'] if str(t.get('id')) == str(topic)), {})
    out = []
    for f in D.get('flow', []):
        ref = f.get('ref') if isinstance(f, dict) else None
        v = D['videos'].get(ref) if ref else None
        if v and int(v.get('topic', -1)) == topic and os.path.exists(os.path.join(SCRIPTS, ref + '.json')):
            out.append(dict(id=ref, title=clean_title(v.get('navLabel') or v.get('title') or ref), minutes=None,
                            kind='question' if ref.startswith('solve-') else 'lesson'))
    return T.get('title', ''), out


def norm(t):
    return re.sub(r'\s+', ' ', str(t)).strip()


def take_files(names):
    """(full takes, patch takes) among file names, each sorted oldest -> newest"""
    patches = sorted(f for f in names if PATCH.match(f))
    fulls = sorted(f for f in names if TAKE.match(f) and not PATCH.match(f))
    return fulls, patches


def stamp(f):
    return (PATCH.match(f) or TAKE.match(f)).group(2)


def patch_read_texts(side):
    """texts of the paragraphs a patch take really covers: only those she REACHED (their start was logged), not every
    selected one. 'read' = the indexes reached (since 2026-10-11); older patch sidecars: the paragraphStarts entries."""
    text = {p['i']: p['text'] for p in side.get('paragraphs', []) if isinstance(p, dict) and 'i' in p}
    read = side.get('read')
    if read is None:
        read = [e.get('para') for e in side.get('paragraphStarts', [])]
    return [text[i] for i in read if i in text]


def changed_paragraphs(current, full_side, patch_sides):
    """indexes of the current paragraphs that her takes do not cover: the text is not among the paragraphs of her
    last full take's sidecar, nor of a patch take made after it (new or edited paragraphs). None = no sidecar."""
    if not full_side or not full_side.get('paragraphs'):
        return None
    known = {norm(p['text'] if isinstance(p, dict) else p) for p in full_side['paragraphs']}
    for ps in patch_sides:
        known |= {norm(t) for t in patch_read_texts(ps)}
    return [i for i, t in enumerate(current) if not covered(t, known)]


def sentences(t):
    return [x for x in re.split(r'(?<=[.?!])\s+', norm(t)) if x]


def covered(t, known):
    """read already: the same text, or the text with whole sentences REMOVED (each remaining sentence word for word,
    in order, from one read paragraph - e.g. a verdict paragraph cut, 2026-10-11). Any added or edited sentence = changed."""
    if norm(t) in known:
        return True
    want = sentences(t)
    for k in known:
        it = iter(sentences(k))
        if want and all(any(w == x for x in it) for w in want):
            return True
    return False


def scan_recorded(videos):
    """{id: {takes, latest, seconds, patches, changed}} from ~/Documents/Course.recordings/_reading (build-time
    status; the page re-scans the folder live when it has permission, with the same rules)"""
    rec = {}
    for v in videos:
        vid = v['id']; d = os.path.join(READING_ROOT, vid)
        if not os.path.isdir(d):
            continue
        fulls, patches = take_files(os.listdir(d))
        if not fulls:
            continue
        last = fulls[-1]; secs = None; side = None
        try:
            side = json.load(open(os.path.join(d, last[:-4] + '.json'), encoding='utf-8'))
            secs = side.get('duration')
        except Exception:
            try:
                secs = (os.path.getsize(os.path.join(d, last)) - 44) / (48000 * 2)
            except Exception:
                pass
        later = []
        for f in patches:
            if stamp(f) > stamp(last):
                try:
                    later.append(json.load(open(os.path.join(d, f[:-4] + '.json'), encoding='utf-8')))
                except Exception:
                    pass
        cur = [p for sl in v['paras'] for p in sl]
        rec[vid] = dict(takes=len(fulls), latest=last, seconds=secs, patches=len(later),
                        changed=changed_paragraphs(cur, side, later))
    return rec


def build(topics=(), ids=None, out=OUT):
    groups = []
    if ids:
        groups.append(dict(topic=None, title='Videos', videos=[dict(id=i, title=i, minutes=None, kind='') for i in ids]))
    for t in topics:
        r = from_review(t) or from_course(t)
        title, vids = r
        if not vids:
            sys.exit('topic %d: no videos found (no review file, no ai_scripts in course18.json) - use --ids' % t)
        groups.append(dict(topic=t, title=title, videos=vids))
    allv = []
    cams = camera_ids()
    for g in groups:
        for v in g['videos']:
            sp = os.path.join(SCRIPTS, v['id'] + '.json')
            if not os.path.exists(sp):
                sys.exit('missing script: ' + sp)
            v['paras'] = paragraphs(v['id'])                       # the script text (sidecars, change detection)
            v['disp'] = prompter_display(v['id'], v['paras'])       # display only; take text stays unchanged
            words = sum(len(p.split()) for sl in v['paras'] for p in sl)
            v['words'] = words
            if not v.get('minutes'):
                v['minutes'] = round(words / WPM, 1)
            if v['title'] == v['id']:   # no title known: the first sentence
                v['title'] = re.split(r'(?<=[.?!])\s', v['paras'][0][0])[0][:110]
            v['group'] = g['topic']
            v['camera'] = v['id'] in cams                          # camera lesson: "Camera on" by default
            allv.append(v)
    import datetime as _dt
    now = _dt.datetime.now().astimezone()
    data = dict(groups=[dict(topic=g['topic'], title=g['title'], ids=[v['id'] for v in g['videos']]) for g in groups],
                videos=allv, recorded=scan_recorded(allv), builtAt=now.isoformat(timespec='seconds'))
    js = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    label = ', '.join(('Topic %d' % g['topic']) + (' · ' + g['title'] if g['title'] else '') if g['topic'] else 'Videos'
                      for g in groups)
    page = PAGE.replace('__DATA__', js).replace('__LABEL__', html.escape(label)).replace('__UPDATED__', now.strftime('%a %d %b, %H:%M'))
    with open(out, 'w', encoding='utf-8') as f:
        f.write(page)
    return out, allv


PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Reading Studio</title>
<link rel="icon" href="data:,">
<style>
:root{--bg:#f7f6f3;--panel:#fff;--ink:#1f2328;--muted:#6b7280;--faint:#9ca3af;--line:#e7e5e0;--soft:#f1efea;
--accent:#0f766e;--accent-soft:#e6f4f1;--rec:#c2410c;--rec-soft:#fdf0e9;--ok:#15803d;--ok-soft:#e8f5ec;--warn:#b45309;--warn-soft:#fdf6e7;
--hl:#fff8db;--hl-line:#e0b100;--mist:#b91c1c;--radius:12px;--prompt:30px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#17181a;--panel:#1f2023;--ink:#ececea;--muted:#a1a1aa;--faint:#71717a;--line:#2e2f33;--soft:#26272b;
--accent:#2dd4bf;--accent-soft:#12332f;--rec:#fb923c;--rec-soft:#3a2416;--ok:#4ade80;--ok-soft:#14321f;--warn:#fbbf24;--warn-soft:#3a2e12;--hl:#2f2a12;--hl-line:#d4a72c;--mist:#f87171}}
:root[data-theme="dark"]{--bg:#17181a;--panel:#1f2023;--ink:#ececea;--muted:#a1a1aa;--faint:#71717a;--line:#2e2f33;--soft:#26272b;
--accent:#2dd4bf;--accent-soft:#12332f;--rec:#fb923c;--rec-soft:#3a2416;--ok:#4ade80;--ok-soft:#14321f;--warn:#fbbf24;--warn-soft:#3a2e12;--hl:#2f2a12;--hl-line:#d4a72c;--mist:#f87171}
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{background:var(--bg);color:var(--ink);font:15px/1.45 ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif;display:flex;flex-direction:column}
button,select{font:inherit;color:inherit}
button{cursor:pointer;border:1px solid var(--line);background:var(--panel);border-radius:9px;padding:7px 12px}
button:hover:not(:disabled){border-color:var(--faint)}
button:disabled{opacity:.45;cursor:default}
button:focus-visible,select:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.top{display:flex;align-items:center;gap:14px;padding:10px 18px;border-bottom:1px solid var(--line);background:var(--panel);flex-wrap:wrap}
.updated{font:700 14px system-ui;background:#fef3c7;color:#78350f;border:1.5px solid #f59e0b;border-radius:10px;padding:5px 10px;white-space:nowrap;margin-left:auto;order:3}
.updated.old{background:#fee2e2;color:#7f1d1d;border-color:#ef4444}
.brand{font-weight:700;letter-spacing:.01em}.brand small{font-weight:500;color:var(--muted);margin-left:8px}
.tips{flex:1 1 420px;display:flex;flex-wrap:wrap;gap:6px 16px;color:var(--muted);font-size:13px}
.tips span::before{content:"•";margin-right:6px;color:var(--faint)}
.tips b{color:var(--ink);font-weight:600}
.main{flex:1;display:flex;min-height:0}
aside{width:300px;flex:none;border-right:1px solid var(--line);background:var(--panel);overflow:auto;padding:10px 8px 20px}
.grp{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);padding:10px 10px 6px;display:flex;justify-content:space-between}
.vid{display:grid;grid-template-columns:22px 1fr auto;gap:2px 8px;align-items:start;padding:8px 10px;border-radius:9px;cursor:pointer;border:1px solid transparent}
.vid:hover{background:var(--soft)}
.vid.cur{background:var(--accent-soft);border-color:color-mix(in srgb,var(--accent) 35%,transparent)}
.vid .n{color:var(--faint);font-variant-numeric:tabular-nums;font-size:13px;padding-top:1px}
.vid .t{font-size:13.5px;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.vid .id{grid-column:2;font-size:11.5px;color:var(--faint);font-family:ui-monospace,Menlo,monospace}
.vid .m{font-size:12px;color:var(--muted);white-space:nowrap;font-variant-numeric:tabular-nums;padding-top:1px}
.vid .st{grid-column:2/4;font-size:12px}
.pill{display:inline-block;border-radius:999px;padding:1px 8px;font-size:11.5px;font-weight:600}
.pill.no{background:var(--soft);color:var(--muted)}
.pill.yes{background:var(--ok-soft);color:var(--ok)}
.work{flex:1;display:flex;flex-direction:column;min-width:0}
.bar{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;padding:12px 22px;border-bottom:1px solid var(--line);background:var(--panel)}
.folder{display:flex;gap:10px;align-items:center;font-size:13px;flex:1 1 100%;min-width:0}.folder>span:first-child{white-space:nowrap;color:var(--muted)}
.folder .path{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;background:var(--soft);padding:4px 8px;border-radius:7px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0}
.folder.bad .path{background:var(--warn-soft);color:var(--warn)}
.mic{display:flex;gap:6px 10px;align-items:center;font-size:13px;flex:1 1 100%;flex-wrap:wrap}
.mic select{max-width:240px;padding:6px;border:1px solid var(--line);border-radius:8px;background:var(--panel)}
.meter{position:relative;flex:1;min-width:120px;max-width:420px;height:12px;border-radius:6px;background:var(--soft);overflow:hidden}
.meter i{position:absolute;left:0;top:0;bottom:0;width:0;background:linear-gradient(90deg,var(--ok) 0 70%,var(--warn) 70% 88%,var(--rec) 88%);transition:width .05s linear}
.meter b{position:absolute;top:0;bottom:0;width:2px;background:var(--ink);opacity:.5;left:0}
.meter .z{position:absolute;top:0;bottom:0;left:70%;width:18%;border-left:1px dashed var(--faint);border-right:1px dashed var(--faint)}
.db{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--muted);width:62px;text-align:right}
.db.clip{color:var(--rec);font-weight:700}
.micinfo{font-size:12px;color:var(--muted);flex-basis:100%}
.micinfo .bad{color:var(--rec);font-weight:600}
.cam{display:flex;gap:6px 10px;align-items:center;font-size:13px;flex:1 1 100%;flex-wrap:wrap}
.cam label{display:flex;gap:6px;align-items:center;cursor:pointer;font-weight:600}
.cam select{max-width:240px;padding:6px;border:1px solid var(--line);border-radius:8px;background:var(--panel)}
.cam video{width:84px;height:84px;border-radius:50%;object-fit:cover;transform:scaleX(-1);border:3px solid #fff;box-shadow:0 2px 8px #0004;background:#17233c;flex:none}
.cam .caminfo{color:var(--muted);font-size:12px}
.cam .caminfo .bad{color:var(--rec);font-weight:600}
.cam.on label{color:var(--accent)}
.pill.cam{background:var(--accent-soft);color:var(--accent)}
.recdot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--rec);margin-right:5px;vertical-align:1px}
.head{display:flex;gap:18px;align-items:center;padding:14px 22px 10px}
.head h1{font-size:18px;margin:0;font-weight:650;flex:1;min-width:0}
.head h1 small{display:block;font-size:12.5px;font-weight:500;color:var(--muted);font-family:ui-monospace,Menlo,monospace;margin-top:2px}
.ctrl{display:flex;gap:10px;align-items:center;padding:0 22px 12px;flex-wrap:wrap}
.timer{font:600 40px/1 ui-monospace,Menlo,monospace;font-variant-numeric:tabular-nums;min-width:150px;letter-spacing:.02em}
.timer.on{color:var(--rec)}.timer.paused{color:var(--warn)}
.big{padding:10px 18px;font-weight:650;border-radius:10px}
#bRec{background:var(--rec);border-color:var(--rec);color:#fff}
#bRec .dot{display:inline-block;width:10px;height:10px;border-radius:50%;background:#fff;margin-right:8px;vertical-align:1px}
#bMist{border-color:color-mix(in srgb,var(--mist) 50%,var(--line));color:var(--mist)}
.state{font-size:13px;color:var(--muted)}
.state.rec{color:var(--rec);font-weight:600}
.keys{font-size:12px;color:var(--faint);margin-left:auto}
kbd{font:11.5px ui-monospace,Menlo,monospace;border:1px solid var(--line);border-bottom-width:2px;border-radius:5px;padding:0 5px;background:var(--panel);color:var(--muted)}
.prompter{flex:1;overflow:auto;padding:16px 22px 40vh;scroll-behavior:smooth;outline:none}
.prompter .inner{max-width:880px;margin:0 auto}
.slide{border-top:1px dashed var(--line);margin-top:14px;padding-top:14px}
.slide:first-child{border-top:0;margin-top:0;padding-top:0}
.p{font:400 var(--prompt)/1.55 Georgia,"Iowan Old Style",serif;margin:0 0 .55em;padding:.25em .6em .3em;border-radius:10px;border-left:4px solid transparent;color:var(--muted);transition:background .2s,color .2s;cursor:pointer;position:relative}
.p.done{color:var(--faint)}
.p.cur{background:var(--hl);border-left-color:var(--hl-line);color:var(--ink)}
.p .mk{position:absolute;right:8px;top:6px;font:700 12px ui-sans-serif,sans-serif;color:var(--mist)}
.p.flash{animation:fl .6s}
.mode{display:inline-flex;border:1px solid var(--line);border-radius:9px;overflow:hidden}
.mode button{border:0;border-radius:0;padding:6px 11px;background:var(--panel)}
.mode button.on{background:var(--accent);color:#fff}
.pbar{display:none;margin:0 22px 8px;padding:8px 12px;border-radius:10px;background:var(--warn-soft);font-size:13.5px;align-items:center;gap:10px;flex-wrap:wrap}
.patch .pbar{display:flex}
.pbar button{padding:4px 10px;font-size:13px}
.pbar #pNext{margin-left:auto;padding:8px 18px;font-size:15px;background:var(--accent);border-color:var(--accent);color:#fff}
.patch .p{padding-left:2.1em}
.patch .p::before{content:"";position:absolute;left:.6em;top:.62em;width:.62em;height:.62em;border:2px solid var(--faint);border-radius:4px}
.patch .p.sel{color:var(--ink)}
.patch .p.sel::before{background:var(--accent);border-color:var(--accent)}
.p .chg{font:700 11px ui-sans-serif,sans-serif;color:var(--warn);background:var(--warn-soft);border-radius:999px;padding:1px 7px;margin-left:8px;vertical-align:4px}
.patching .p:not(.sel):not(.ctx){display:none}
.patching .slide.empty{display:none}
.patching .p.ctx{opacity:.45;font-size:.8em;cursor:default}
.patching .p::before{display:none}
.pill.chg{background:var(--warn-soft);color:var(--warn)}
@keyframes fl{0%{background:color-mix(in srgb,var(--mist) 25%,transparent)}100%{}}
.foot{display:flex;gap:12px;align-items:center;padding:10px 22px;border-top:1px solid var(--line);background:var(--panel);flex-wrap:wrap}
.foot audio{height:34px;flex:1;min-width:240px;max-width:520px}
.foot .lbl{font-size:13px;color:var(--muted)}
.opts{display:flex;gap:12px;align-items:center;font-size:13px;color:var(--muted)}
.opts label{display:flex;gap:5px;align-items:center;cursor:pointer}
#toast{position:fixed;left:50%;bottom:70px;transform:translateX(-50%);background:var(--ink);color:var(--bg);padding:9px 16px;border-radius:10px;font-size:14px;opacity:0;pointer-events:none;transition:opacity .25s;max-width:90vw;z-index:9}
#toast.show{opacity:1}

/* 2026-10-14 CAMERA LAYOUT (teacher: "the script at the top in the middle, so I can look at the camera as I speak"):
   with "Camera on" the current paragraph sits in a narrow column at the TOP CENTRE of the screen, right under a MacBook's
   camera; the next paragraph small and faded under it, the past ones hidden. Everything else moves below, compact; the
   self-preview goes to the bottom-right corner. Audio-only keeps the normal layout. */
body.camlayout{--band:44vh;padding-top:var(--band)}
.camlayout .top{display:none}
.camlayout .prompter{position:fixed;top:0;left:50%;transform:translateX(-50%);width:min(46vw,780px);height:var(--band);z-index:5;
  padding:10px 20px 12px;background:var(--panel);border:1px solid var(--line);border-top:0;border-radius:0 0 16px 16px;box-shadow:0 6px 24px #0002;scroll-behavior:auto}
.camlayout .prompter::before{content:"";position:fixed;top:4px;left:50%;width:10px;height:10px;margin-left:-5px;border-radius:50%;background:var(--faint);opacity:.6}
.camlayout .prompter .inner{max-width:none}
.camlayout.mirror .prompter .inner{transform:scaleX(-1)}
.camlayout .slide{border:0;margin:0;padding:0}
.camlayout #paras:not(.selecting) .p{display:none}
.camlayout #paras:not(.selecting) .p.cur{display:block;font-size:calc(var(--prompt)*1.12);line-height:1.42;color:var(--ink);background:none;border-left-color:transparent;padding:.15em .1em;margin:0 0 .5em;text-align:center}
.camlayout #paras:not(.selecting) .p.nextp{display:block;font-size:calc(var(--prompt)*.62);line-height:1.4;color:var(--muted);opacity:.55;padding:.1em;text-align:center;border-left-color:transparent}
.camlayout #paras:not(.selecting) .p.cur::before,.camlayout #paras:not(.selecting) .p.nextp::before{display:none}
.camlayout aside{width:250px;padding:6px 6px 14px}
.camlayout .vid{padding:5px 8px}.camlayout .vid .t{font-size:12.5px}.camlayout .grp{padding:6px 8px 4px}
.camlayout .bar{padding:6px 14px;gap:4px 14px}
.camlayout .folder,.camlayout .mic,.camlayout .cam{flex:1 1 auto;font-size:12px}
.camlayout .micinfo{display:none}
.camlayout .head{padding:6px 14px 4px}.camlayout .head h1{font-size:15px}
.camlayout .ctrl{padding:0 14px 6px}.camlayout .timer{font-size:28px;min-width:110px}.camlayout .big{padding:7px 13px}
.camlayout .pbar{margin:0 14px 6px}
.camlayout .foot{padding:6px 14px}
.camlayout .work{overflow:auto}
.camlayout #camPrev{position:fixed;right:14px;bottom:14px;width:120px;height:120px;z-index:6}
.opts .mirrorbox{display:none}.camlayout .opts .mirrorbox{display:flex}
@media (max-width:820px){.main{flex-direction:column}aside{width:auto;max-height:30vh;border-right:0;border-bottom:1px solid var(--line)}:root{--prompt:22px}.keys{display:none}}
</style>
</head>
<body>
<div class="top">
  <div class="brand">Reading Studio<small>__LABEL__</small></div>
  <div class="updated" id="updated" title="Version saved at this time. Refresh only between takes to load a newer version.">Last updated: __UPDATED__</div>
  <div class="tips">
    <span><b>Quiet room</b>, no fan or AC</span>
    <span><b>Same mic, same distance</b> every time (about a hand-span)</span>
    <span><b>Read like you teach</b>, to one student</span>
    <span>Stumbled? Press <kbd>M</kbd> and <b>repeat the sentence</b></span>
  </div>
</div>
<div class="main">
  <aside id="list"></aside>
  <section class="work">
    <div class="bar">
      <div class="folder" id="folderBox"><span>Saving to</span><span class="path" id="fpath">…</span><button id="bFolder">Choose folder</button></div>
      <div class="mic">
        <button id="bMic">Turn on microphone</button>
        <select id="micSel" title="Microphone" hidden></select>
        <div class="meter" title="Input level. Aim for peaks in the dashed zone (about −12 to −6 dB)."><span class="z"></span><i id="lvl"></i><b id="peak"></b></div>
        <span class="db" id="db">— dB</span>
        <div class="micinfo" id="micinfo">Microphone is off.</div>
      </div>
      <div class="cam" id="camBox" title="Camera lessons (the first lesson of a topic) are recorded with your face too. The WAV stays the narration.">
        <label><input type="checkbox" id="camOn"> Camera on</label>
        <select id="camSel" title="Camera" hidden></select>
        <video id="camPrev" muted playsinline hidden></video>
        <span class="caminfo" id="caminfo">Camera is off for this video (audio only).</span>
      </div>
    </div>
    <div class="head"><h1 id="vtitle"></h1>
      <div class="opts">
        <span class="mode" title="Full read = the whole script. Re-read = only the paragraphs you select (a patch take)."><button id="mFull" class="on">Full read</button><button id="mPatch">Re-read paragraphs</button></span>
        <label><input type="checkbox" id="auto" checked> Auto-scroll</label>
        <label class="mirrorbox" title="Flip the script left-right, for a teleprompter glass in front of the camera"><input type="checkbox" id="mirror"> Mirror</label>
        <button id="aMinus" title="Smaller text">A−</button><button id="aPlus" title="Bigger text">A+</button>
      </div>
    </div>
    <div class="ctrl">
      <div class="timer" id="timer">0:00.0</div>
      <button class="big" id="bRec"><span class="dot"></span>Record</button>
      <button class="big" id="bPause" disabled>Pause</button>
      <button class="big" id="bStop" disabled>Stop &amp; save</button>
      <button class="big" id="bMist" disabled title="I stumbled; I'll repeat this sentence (M)">Mistake</button>
      <span class="state" id="state">Ready.</span>
      <span class="keys"><kbd>Space</kbd> / click next paragraph · <kbd>←</kbd> back · <kbd>M</kbd> mistake · <kbd>P</kbd> pause</span>
    </div>
    <div class="pbar" id="pbar"><span id="pinfo"></span><button id="pChanged">Select changed</button><button id="pClear">Clear</button><button id="pNext" class="big" hidden>Next ▸</button></div>
    <div class="prompter" id="prompter" tabindex="-1"><div class="inner" id="paras"></div></div>
    <div class="foot">
      <span class="lbl" id="playLbl">Last take</span>
      <audio id="player" controls preload="metadata"></audio>
      <button id="bNext">Next video →</button>
    </div>
  </section>
</div>
<div id="toast"></div>
<script>
const DATA=__DATA__;
/* 2026-10-11: how old is this page? (she sometimes reads from a page opened hours earlier) */
function pageAge(){const el=document.getElementById('updated');if(!el||!DATA.builtAt)return;const h=(Date.now()-new Date(DATA.builtAt))/36e5;
 const t=h<1?Math.max(1,Math.round(h*60))+' min ago':h<48?Math.round(h)+' h ago':Math.round(h/24)+' days ago';
 el.textContent='Last updated: '+new Date(DATA.builtAt).toLocaleString([], {day:'2-digit',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit',second:'2-digit'})+' · '+t+(h>=3?' · reload the newest page before reading':'');
 el.classList.toggle('old',h>=3)}
setTimeout(pageAge,0);setInterval(pageAge,60000);
const $=s=>document.querySelector(s);
const V=DATA.videos, BYID=Object.fromEntries(V.map(v=>[v.id,v]));
const SR=48000;
const TAKE_RE=/^(.+)-(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z)\.wav$/,PATCH_RE=/^(.+)-patch-(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z)\.wav$/;
const norm=t=>String(t).replace(/\s+/g,' ').trim();
const LS={get(k,d){try{const v=localStorage.getItem('reading-studio-'+k);return v==null?d:JSON.parse(v)}catch{return d}},set(k,v){try{localStorage.setItem('reading-studio-'+k,JSON.stringify(v))}catch{}}};
function toast(m,ms=3200){const t=$('#toast');t.textContent=m;t.classList.add('show');clearTimeout(t._h);t._h=setTimeout(()=>t.classList.remove('show'),ms)}
function fmt(s,tenths){s=Math.max(0,s);const m=Math.floor(s/60),r=s-m*60;return m+':'+(tenths?r.toFixed(1).padStart(4,'0'):String(Math.floor(r)).padStart(2,'0'))}
function esc(s){return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}

/* ---------------- state ---------------- */
const S={cur:0,para:0,status:{},rec:null,lastUrl:null,mode:'full',sel:new Set()};
for(const [id,r] of Object.entries(DATA.recorded||{}))S.status[id]=r;
const flat=v=>v.paras.flat();

/* ---------------- recordings folder (File System Access API; same IndexedDB as the teacher studio) ---------------- */
const RF={db:null,handle:null,perm:'none',own:false};
function rfDB(){return RF.db||(RF.db=new Promise((ok,no)=>{const r=indexedDB.open('studio-rec-folder',1);r.onupgradeneeded=()=>r.result.createObjectStore('h');r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error)}))}
async function rfGet(key){try{const db=await rfDB();return await new Promise(ok=>{const q=db.transaction('h').objectStore('h').get(key);q.onsuccess=()=>ok(q.result||null);q.onerror=()=>ok(null)})}catch{return null}}
async function rfSet(key,h){try{const db=await rfDB();await new Promise(ok=>{const t=db.transaction('h','readwrite');t.objectStore('h').put(h,key);t.oncomplete=()=>ok();t.onerror=()=>ok()})}catch(e){console.warn('folder not remembered',e)}}
async function rfPerm(ask){if(!RF.handle)return 'none';try{let p=await RF.handle.queryPermission({mode:'readwrite'});if(p!=='granted'&&ask)p=await RF.handle.requestPermission({mode:'readwrite'});return p}catch(e){return 'denied'}}
async function readingDir(create){if(!RF.handle)return null;if(RF.handle.name==='_reading')return RF.handle;return RF.handle.getDirectoryHandle('_reading',{create})}
async function videoDir(id,create){const r=await readingDir(create);return r&&r.getDirectoryHandle(id,{create})}
function rootLabel(){if(!RF.handle)return null;return RF.handle.name==='_reading'?'_reading':RF.handle.name+' / _reading'}
function paintFolder(){
  const box=$('#folderBox'),p=$('#fpath'),b=$('#bFolder'),v=V[S.cur];box.classList.remove('bad');
  if(!window.showDirectoryPicker){p.textContent='Downloads folder (this browser cannot save into a folder; use Chrome)';box.classList.add('bad');b.hidden=true;return}
  if(!RF.handle){p.textContent='No folder chosen yet: choose Documents / Course.recordings';box.classList.add('bad');b.textContent='Choose folder';return}
  p.textContent=rootLabel()+' / '+v.id+' /';p.title='Each take is saved as '+v.id+'-<time>.wav plus a .json with the paragraph times';
  if(RF.perm!=='granted'){box.classList.add('bad');p.textContent=rootLabel()+' / '+v.id+' /  (click Allow to reconnect)';b.textContent='Allow';return}
  if(RF.handle.name!=='Course.recordings'&&RF.handle.name!=='_reading'){box.classList.add('bad');p.title='Expected Documents/Course.recordings. Click "Change" to pick it.'}
  b.textContent='Change';
}
async function initFolder(){
  if(!window.showDirectoryPicker){paintFolder();return}
  RF.handle=await rfGet('reading-dir');RF.own=!!RF.handle;
  if(!RF.handle){RF.handle=await rfGet('dir')}          // the teacher studio's recordings folder, as the default
  RF.perm=await rfPerm(false);paintFolder();if(RF.perm==='granted')await scanAll();
}
$('#bFolder').onclick=async()=>{
  if(RF.handle&&RF.perm!=='granted'){RF.perm=await rfPerm(true);paintFolder();if(RF.perm==='granted'){if(!RF.own){await rfSet('reading-dir',RF.handle);RF.own=true}await scanAll();toast('Folder connected.')}return}
  try{const h=await window.showDirectoryPicker({id:'studio-recordings',mode:'readwrite'});RF.handle=h;RF.own=true;await rfSet('reading-dir',h);RF.perm=await rfPerm(true);paintFolder();
    if(h.name!=='Course.recordings'&&h.name!=='_reading')toast('Saving in "'+h.name+'/_reading". The usual folder is Documents/Course.recordings.',6000);else toast('Takes will be saved in '+rootLabel()+'/<video>/');
    await scanAll()}catch(e){if(e&&e.name!=='AbortError')console.warn(e)}
};
async function readJson(d,n){try{return JSON.parse(await (await (await d.getFileHandle(n)).getFile()).text())}catch{return null}}
function patchReadTexts(side){/* only the paragraphs she REACHED count: 'read', or for older sidecars the paragraphStarts */
  const text={};for(const p of (side.paragraphs||[]))if(p&&p.i!=null)text[p.i]=p.text;
  const read=side.read||(side.paragraphStarts||[]).map(e=>e.para);return read.filter(i=>i in text).map(i=>text[i])}
function changedOf(id,full,patches){/* same rule as the generator: current paragraphs not in the last full take's sidecar nor in a later patch */
  if(!full||!full.paragraphs)return null;const known=new Set(full.paragraphs.map(p=>norm(p.text!=null?p.text:p)));
  for(const ps of patches)for(const t of patchReadTexts(ps))known.add(norm(t));
  return flat(BYID[id]).map((t,i)=>coveredBy(t,known)?-1:i).filter(i=>i>=0)}
const sentencesOf=t=>norm(t).split(/(?<=[.?!])\s+/).filter(Boolean);
function coveredBy(t,known){/* same as covered() in the generator: same text, or only whole sentences removed */
  if(known.has(norm(t)))return true;const want=sentencesOf(t);if(!want.length)return false;
  for(const k of known){const have=sentencesOf(k);let j=0;let ok=true;for(const w of want){while(j<have.length&&have[j]!==w)j++;if(j>=have.length){ok=false;break}j++}if(ok)return true}
  return false}
async function scanVideo(id){
  try{const d=await videoDir(id,false);if(!d)return;const names=[];for await(const [n,h] of d.entries())if(h.kind==='file'&&TAKE_RE.test(n))names.push(n);
    const patches=names.filter(n=>PATCH_RE.test(n)).sort(),fulls=names.filter(n=>!PATCH_RE.test(n)).sort();
    if(!fulls.length){delete S.status[id];return}const last=fulls[fulls.length-1],lastT=last.match(TAKE_RE)[2];let secs=null;
    const side=await readJson(d,last.replace(/\.wav$/,'.json'));if(side)secs=side.duration;else{try{const f=await (await d.getFileHandle(last)).getFile();secs=(f.size-44)/(SR*2)}catch{}}
    const later=[];for(const n of patches)if(n.match(PATCH_RE)[2]>lastT){const j=await readJson(d,n.replace(/\.wav$/,'.json'));if(j)later.push(j)}
    S.status[id]={takes:fulls.length,latest:last,seconds:secs,patches:later.length,changed:changedOf(id,side,later)}}catch(e){/* no folder for this video yet */}
}
async function scanAll(){if(RF.perm!=='granted')return;try{await readingDir(false)}catch{renderList();return}await Promise.all(V.map(v=>scanVideo(v.id)));renderList();loadLatestTake()}

/* ---------------- list ---------------- */
function renderList(){
  const L=$('#list');let h='',n=0;
  for(const g of DATA.groups){const done=g.ids.filter(id=>S.status[id]).length;
    h+='<div class="grp"><span>'+esc(g.topic?('Topic '+g.topic+(g.title?' · '+g.title:'')):g.title)+'</span><span>'+done+'/'+g.ids.length+'</span></div>';
    for(const id of g.ids){const v=BYID[id],i=V.indexOf(v),st=S.status[id];n++;
      h+='<div class="vid'+(i===S.cur?' cur':'')+'" data-i="'+i+'"><span class="n">'+(i+1)+'</span><span class="t" title="'+esc(v.title)+'">'+esc(v.title)+'</span><span class="m">'+v.minutes.toFixed(1)+' min</span>'+
        '<span class="id">'+esc(id)+'</span><span class="st">'+(st?'<span class="pill yes">recorded ✓'+(st.seconds?' · '+fmt(st.seconds):'')+(st.takes>1?' · '+st.takes+' takes':'')+(st.patches?' · '+st.patches+' patch'+(st.patches>1?'es':''):'')+'</span>'+(st.changed&&st.changed.length?' <span class="pill chg">needs re-read: '+st.changed.length+' paragraph'+(st.changed.length>1?'s':'')+'</span>':''):'<span class="pill no">not recorded</span>')+(camWanted(v)?' <span class="pill cam" title="Recorded with the camera on">camera</span>':'')+'</span></div>'}}
  L.innerHTML=h;
  L.querySelectorAll('.vid').forEach(el=>el.onclick=()=>selectVideo(+el.dataset.i));
}
function selectVideo(i){
  if(S.rec){toast('Stop the recording first.');return}
  S.cur=Math.max(0,Math.min(V.length-1,i));S.para=0;LS.set('cur',V[S.cur].id);S.sel=new Set(changedList());
  renderList();renderParas();paintFolder();loadLatestTake();syncCam(false);
  const el=$('#list .vid.cur');if(el)el.scrollIntoView({block:'nearest'});
}

/* ---------------- teleprompter ---------------- */
function renderParas(){
  const v=V[S.cur];let k=0;
  $('#vtitle').innerHTML=esc(v.title)+'<small>'+esc(v.id)+' · about '+v.minutes.toFixed(1)+' min · '+v.words+' words</small>';
  const ch=new Set(changedList());
  $('#paras').innerHTML=(v.disp||v.paras).map(sl=>'<div class="slide">'+sl.map(p=>{const kk=k++;return '<p class="p" data-k="'+kk+'">'+esc(p).replace(/\n/g,'<br>')+(ch.has(kk)?'<span class="chg">changed</span>':'')+'</p>'}).join('')+'</div>').join('');
  $('#paras').querySelectorAll('.p').forEach(el=>el.onclick=e=>{e.stopPropagation();const kk=+el.dataset.k;if(S.rec&&!S.rec.paused)nextPara();else if(S.mode==='patch'&&!S.rec){S.sel.has(kk)?S.sel.delete(kk):S.sel.add(kk);if(S.sel.has(kk))S.para=kk;else if(!S.sel.has(S.para))S.para=order()[0]??0;paintParas()}else setPara(kk,'jump')});
  $('#prompter').scrollTop=0;paintParas();
}
function changedList(){const st=S.status[V[S.cur].id];return st&&st.changed?st.changed.slice():[]}
function order(){const n=flat(V[S.cur]).length;return S.mode==='patch'?[...S.sel].sort((a,b)=>a-b):[...Array(n).keys()]}
function paintParas(){
  const patch=S.mode==='patch',patching=patch&&!!S.rec,sel=S.sel,ch=changedList();
  document.body.classList.toggle('patch',patch);$('#paras').classList.toggle('patching',patching);
  {const o=order(),nk=o[o.indexOf(S.para)+1];$('#paras').classList.toggle('selecting',patch&&!patching);
   document.querySelectorAll('#paras .p').forEach(el=>el.classList.toggle('nextp',nk!=null&&+el.dataset.k===nk))}
  document.querySelectorAll('#paras .p').forEach(el=>{const k=+el.dataset.k;el.classList.toggle('cur',k===S.para&&(!patch||sel.has(k)));el.classList.toggle('done',!patch&&k<S.para);
    el.classList.toggle('sel',patch&&sel.has(k));el.classList.toggle('ctx',patching&&!sel.has(k)&&(sel.has(k-1)||sel.has(k+1)))});
  document.querySelectorAll('#paras .slide').forEach(sd=>sd.classList.toggle('empty',patching&&!sd.querySelector('.p.sel,.p.ctx')));
  if(patch){const nc=[...sel].filter(k=>ch.includes(k)).length;const o=order(),pos=o.indexOf(S.para)+1;$('#pNext').hidden=!patching||pos>=o.length;
  $('#pinfo').innerHTML=patching?(pos<o.length?'<b>Paragraph '+pos+' of '+o.length+'</b> — press <kbd>Space</kbd> (or Next ▸) for the next paragraph':'<b>Paragraph '+pos+' of '+o.length+'</b> — the last one. Press Stop &amp; save when you finish')+' <span style="color:var(--muted)">· greyed lines are context, do not read them</span>':
    'Re-read mode: click paragraphs to select them. <b>'+sel.size+' selected</b>'+(ch.length?' · '+ch.length+' changed since your last take'+(nc?' ('+nc+' selected)':''):' · no changed paragraphs');$('#pChanged').hidden=patching||!ch.length;$('#pClear').hidden=patching}
  if(document.body.classList.contains('camlayout')&&!$('#paras').classList.contains('selecting')){$('#prompter').scrollTop=0}
  else if($('#auto').checked){const el=document.querySelector('#paras .p.cur');if(el){const pr=$('#prompter');const top=el.offsetTop-pr.offsetTop-pr.clientHeight*.3;pr.scrollTo({top:Math.max(0,top),behavior:'smooth'})}}
}
function step(d){const o=order();if(!o.length)return;let i=o.indexOf(S.para);if(i<0)i=d>0?-1:o.length;const j=i+d;if(j<0||j>=o.length){if(d>0&&S.rec)toast('Last paragraph. Press Stop & save when you finish.');return}setPara(o[j],d>0?'next':'back')}
function setPara(k,why){const n=flat(V[S.cur]).length;k=Math.max(0,Math.min(n-1,k));if(k===S.para&&why!=='start')return;S.para=k;
  if(S.rec)S.rec.events.push({type:why==='back'?'back':why==='jump'?'jump':'para',para:k,t:recTime()});paintParas()}
function nextPara(){step(1)}
function setMode(m){if(S.rec){toast('Stop the recording first.');return}S.mode=m;$('#mFull').classList.toggle('on',m==='full');$('#mPatch').classList.toggle('on',m==='patch');
  if(m==='patch'){if(!S.sel.size)S.sel=new Set(changedList());const o=order();if(o.length&&!S.sel.has(S.para))S.para=o[0]}paintParas()}
$('#mFull').onclick=()=>setMode('full');$('#mPatch').onclick=()=>setMode('patch');
$('#pChanged').onclick=()=>{S.sel=new Set(changedList());const o=order();if(o.length)S.para=o[0];paintParas()};
$('#pClear').onclick=()=>{S.sel.clear();paintParas()};
$('#pNext').onclick=e=>{e.currentTarget.blur();if(S.rec&&!S.rec.paused)nextPara()};
$('#prompter').onclick=()=>{if(S.rec&&!S.rec.paused)nextPara()};
function fontSize(d){let f=LS.get('font',30);f=Math.max(18,Math.min(48,f+d));LS.set('font',f);document.documentElement.style.setProperty('--prompt',f+'px')}
$('#aMinus').onclick=()=>fontSize(-2);$('#aPlus').onclick=()=>fontSize(2);
$('#mirror').checked=LS.get('mirror',false);document.body.classList.toggle('mirror',$('#mirror').checked);
$('#mirror').onchange=()=>{LS.set('mirror',$('#mirror').checked);document.body.classList.toggle('mirror',$('#mirror').checked)};
$('#auto').checked=LS.get('auto',true);$('#auto').onchange=()=>{LS.set('auto',$('#auto').checked);paintParas()};

/* ---------------- microphone: processing OFF, mono, 48 kHz ---------------- */
const MIC={stream:null,ctx:null,src:null,an:null,node:null,engine:null,settings:null,label:'',peakHold:0,peakT:0};
const WORKLET=`class Tap extends AudioWorkletProcessor{constructor(){super();this.on=false;this.buf=new Float32Array(4096);this.n=0;
 this.mark=false;this.port.onmessage=e=>{const m=e.data;if(m==='start'){this.on=true;this.mark=true}else if(m==='pause'){this.on=false;this.flush()}else if(m==='flush'){this.on=false;this.flush();this.port.postMessage('flushed')}}}
 flush(){if(this.n){this.port.postMessage(this.buf.slice(0,this.n));this.n=0}}
 process(inputs){const ch=inputs[0]&&inputs[0][0];if(this.on&&ch&&this.mark){this.mark=false;this.port.postMessage({started:currentFrame,time:currentTime})}if(this.on&&ch){let i=0;while(i<ch.length){const k=Math.min(ch.length-i,this.buf.length-this.n);this.buf.set(ch.subarray(i,i+k),this.n);this.n+=k;i+=k;if(this.n===this.buf.length){this.port.postMessage(this.buf.slice(0));this.n=0}}}return true}}
registerProcessor('rs-tap',Tap)`;
async function openMic(deviceId){
  closeMic();
  const c={echoCancellation:false,noiseSuppression:false,autoGainControl:false,channelCount:{ideal:1},sampleRate:{ideal:SR},sampleSize:{ideal:24}};
  if(deviceId)c.deviceId={exact:deviceId};
  let stream;try{stream=await navigator.mediaDevices.getUserMedia({audio:c,video:false})}
  catch(e){if(deviceId&&e.name==='OverconstrainedError'){LS.set('mic','');return openMic('')}$('#micinfo').innerHTML='<span class="bad">Microphone blocked or missing ('+esc(e.name)+').</span> Allow it in the address bar, then click “Turn on microphone”.';throw e}
  MIC.stream=stream;const tr=stream.getAudioTracks()[0];MIC.label=tr.label;MIC.settings=tr.getSettings?tr.getSettings():{};
  MIC.ctx=new AudioContext({sampleRate:SR,latencyHint:'interactive'});if(MIC.ctx.state==='suspended')try{await MIC.ctx.resume()}catch{}
  MIC.src=MIC.ctx.createMediaStreamSource(stream);MIC.an=MIC.ctx.createAnalyser();MIC.an.fftSize=2048;MIC.src.connect(MIC.an);
  const sink=MIC.ctx.createGain();sink.gain.value=0;sink.connect(MIC.ctx.destination);
  try{let ok=false;const wu=[URL.createObjectURL(new Blob([WORKLET],{type:'application/javascript'})),'data:application/javascript;base64,'+btoa(WORKLET)];if(location.protocol==='file:')wu.reverse();/* a file:// page refuses blob: worklets (console error) */
    for(const url of wu){try{await MIC.ctx.audioWorklet.addModule(url);ok=true;break}catch(e){console.info('worklet module via '+url.slice(0,5)+' failed: '+e)}}if(!ok)throw new Error('no AudioWorklet module');
    MIC.node=new AudioWorkletNode(MIC.ctx,'rs-tap',{numberOfInputs:1,numberOfOutputs:1,outputChannelCount:[1]});MIC.engine='AudioWorklet';
    MIC.node.port.onmessage=e=>{if(e.data==='flushed'){MIC._flushed&&MIC._flushed()}else if(e.data&&e.data.started!=null){if(S.rec)S.rec.audioMark(e.data)}else if(S.rec)S.rec.push(e.data)};
    MIC.ctl=m=>MIC.node.port.postMessage(m);
  }catch(e){console.warn('AudioWorklet unavailable, using ScriptProcessor',e);
    MIC.node=MIC.ctx.createScriptProcessor(4096,1,1);MIC.engine='ScriptProcessor';let on=false;
    MIC.node.onaudioprocess=ev=>{if(on&&S.rec)S.rec.push(new Float32Array(ev.inputBuffer.getChannelData(0)))};
    MIC.ctl=m=>{if(m==='start')on=true;else{on=false;if(m==='flush')setTimeout(()=>MIC._flushed&&MIC._flushed(),0)}};
  }
  MIC.src.connect(MIC.node);MIC.node.connect(sink);
  tr.onended=()=>{$('#micinfo').innerHTML='<span class="bad">The microphone was disconnected.</span>';if(S.rec)stopRec()};
  await fillMics(tr.getSettings().deviceId||deviceId);paintMicInfo();$('#bMic').hidden=true;$('#micSel').hidden=false;meterLoop();
}
function closeMic(){if(MIC.stream)MIC.stream.getTracks().forEach(t=>t.stop());if(MIC.ctx)try{MIC.ctx.close()}catch{}MIC.stream=MIC.ctx=MIC.node=null}
function paintMicInfo(){const s=MIC.settings||{},off=k=>s[k]===false?'off':s[k]===true?'<span class="bad">ON</span>':'n/a';
  $('#micinfo').innerHTML=esc(MIC.label||'Microphone')+' · '+(MIC.ctx?MIC.ctx.sampleRate:'?')+' Hz mono WAV · echo cancel '+off('echoCancellation')+' · noise suppr. '+off('noiseSuppression')+' · auto gain '+off('autoGainControl')}
async function fillMics(cur){const sel=$('#micSel');const ds=(await navigator.mediaDevices.enumerateDevices()).filter(d=>d.kind==='audioinput');
  sel.innerHTML=ds.map(d=>'<option value="'+esc(d.deviceId)+'"'+(d.deviceId===cur?' selected':'')+'>'+esc(d.label||'Microphone')+'</option>').join('')}
$('#micSel').onchange=async()=>{if(S.rec){toast('Stop the recording first.');return}const id=$('#micSel').value;LS.set('mic',id);try{await openMic(id);toast('Microphone: '+MIC.label)}catch{}};
$('#bMic').onclick=async()=>{try{await openMic(LS.get('mic',''))}catch{}};
let meterRaf=0;
function meterLoop(){cancelAnimationFrame(meterRaf);const buf=new Float32Array(2048);
  const tick=()=>{if(!MIC.an)return;MIC.an.getFloatTimeDomainData(buf);let pk=0;for(let i=0;i<buf.length;i++){const a=Math.abs(buf[i]);if(a>pk)pk=a}
    const db=pk>0?20*Math.log10(pk):-100,now=performance.now();if(db>MIC.peakHold||now-MIC.peakT>1500){MIC.peakHold=db;MIC.peakT=now}
    const pos=d=>Math.max(0,Math.min(100,(d+60)/60*100));$('#lvl').style.width=pos(db)+'%';$('#peak').style.left=pos(MIC.peakHold)+'%';
    const el=$('#db');el.textContent=(MIC.peakHold<=-99?'—':MIC.peakHold.toFixed(0))+' dB';el.classList.toggle('clip',MIC.peakHold>-1);
    if(S.rec&&MIC.peakHold>-1)S.rec.clipped=true;
    meterRaf=requestAnimationFrame(tick)};tick()}
document.addEventListener('pointerdown',()=>{if(MIC.ctx&&MIC.ctx.state==='suspended')MIC.ctx.resume()},{capture:true});


/* ---------------- camera (camera lessons, 2026-10-13): webcam VIDEO recorded in parallel with the WAV ----------------
   Camera lessons (DATA video .camera = the first lesson of a topic, and topic 51) default to "Camera on"; any video can
   be switched (remembered per video). The WAV stays the narration; the camera file <id>-<time>.mp4|webm also carries
   the same microphone (compressed) only so the video can be synced to the WAV exactly (reading_to_video.py matches the
   two audio tracks). Both recorders start, pause and stop together; the sidecar "camera" block keeps both start times. */
const CAM={stream:null,label:'',settings:null,err:''};
function camWanted(v){const o=LS.get('cam:'+v.id,null);return o==null?!!v.camera:!!o}
const CAM_TYPES=['video/mp4;codecs=avc1.640028,mp4a.40.2','video/mp4;codecs=avc1.4d0028,mp4a.40.2','video/mp4;codecs=avc1,mp4a.40.2','video/mp4;codecs=avc1,opus','video/mp4',
  'video/webm;codecs=vp9,opus','video/webm;codecs=vp8,opus','video/webm'];
function camMime(){if(!window.MediaRecorder)return '';for(const m of CAM_TYPES)try{if(MediaRecorder.isTypeSupported(m))return m}catch{}return ''}
async function openCam(deviceId){
  closeCam();CAM.err='';
  const c={width:{ideal:1920},height:{ideal:1080},frameRate:{ideal:30}};if(deviceId)c.deviceId={exact:deviceId};
  let stream;try{stream=await navigator.mediaDevices.getUserMedia({video:c,audio:false})}
  catch(e){if(deviceId&&(e.name==='OverconstrainedError'||e.name==='NotFoundError')){LS.set('cam','');return openCam('')}CAM.err=e.name||'error';paintCam();throw e}
  CAM.stream=stream;const tr=stream.getVideoTracks()[0];CAM.label=tr.label;CAM.settings=tr.getSettings?tr.getSettings():{};
  tr.onended=()=>{CAM.stream=null;CAM.err='disconnected';paintCam();if(S.rec&&S.rec.cam){S.rec.cam.lost=true;toast('The camera was disconnected. The audio goes on recording.',6000)}};
  const pv=$('#camPrev');pv.srcObject=stream;pv.hidden=false;pv.play().catch(()=>{});
  await fillCams(CAM.settings.deviceId||deviceId);paintCam();
}
function closeCam(){if(CAM.stream)CAM.stream.getTracks().forEach(t=>t.stop());CAM.stream=null;const pv=$('#camPrev');pv.srcObject=null;pv.hidden=true}
async function fillCams(cur){const sel=$('#camSel');const ds=(await navigator.mediaDevices.enumerateDevices()).filter(d=>d.kind==='videoinput');
  sel.innerHTML=ds.map(d=>'<option value="'+esc(d.deviceId)+'"'+(d.deviceId===cur?' selected':'')+'>'+esc(d.label||'Camera')+'</option>').join('');sel.hidden=!ds.length}
function camFmt(){const m=camMime();return m.startsWith('video/mp4')?'MP4 (H.264)':m?'WebM ('+(m.includes('vp9')?'VP9':'VP8')+')':'no video recorder'}
function paintCam(){
  const v=V[S.cur],want=camWanted(v),box=$('#camBox'),info=$('#caminfo');$('#camOn').checked=want;box.classList.toggle('on',want);
  if(document.body.classList.contains('camlayout')!==want){document.body.classList.toggle('camlayout',want);if(typeof paintParas==='function')paintParas()}
  if(!want){info.textContent=(v.camera?'Camera lesson, but camera switched off: ':'')+'audio only for this video.';$('#camSel').hidden=true;$('#camPrev').hidden=true;return}
  if(CAM.stream){const s=CAM.settings||{};info.innerHTML=esc(CAM.label||'Camera')+' · '+(s.width||'?')+'×'+(s.height||'?')+' · '+Math.round(s.frameRate||0)+' fps · '+camFmt()+(s.height&&s.height<720?' · <span class="bad">low resolution</span>':'')+' · recorded with every take of this video';return}
  info.innerHTML=CAM.err?'<span class="bad">Camera '+(CAM.err==='NotAllowedError'?'blocked: allow it in the address bar':CAM.err==='disconnected'?'disconnected':'not available ('+esc(CAM.err)+')')+'.</span> Click “Camera on” again to retry, or untick it to record audio only.':
    (v.camera?'Camera lesson: ':'')+'the camera starts when you press Record (or click “Camera on”).'}
async function syncCam(ask){const v=V[S.cur],want=camWanted(v);
  if(!want){if(CAM.stream&&!S.rec)closeCam();paintCam();return}
  if(!CAM.stream){let ok=ask;if(!ok)try{ok=(await navigator.permissions.query({name:'camera'})).state==='granted'}catch{}
    if(ok)try{await openCam(LS.get('cam',''))}catch{}}
  paintCam()}
$('#camOn').onchange=async e=>{if(S.rec){e.target.checked=!e.target.checked;toast('Stop the recording first.');return}const v=V[S.cur];LS.set('cam:'+v.id,e.target.checked);renderList();await syncCam(true)};
$('#camSel').onchange=async()=>{if(S.rec){toast('Stop the recording first.');return}const id=$('#camSel').value;LS.set('cam',id);try{await openCam(id);toast('Camera: '+CAM.label)}catch{}};
function camRecorder(r){
  const mime=camMime();if(!mime)throw new Error('This browser cannot record video (MediaRecorder).');
  const s=CAM.settings||{},tracks=[...CAM.stream.getVideoTracks(),...(MIC.stream?MIC.stream.getAudioTracks():[])];
  const mr=new MediaRecorder(new MediaStream(tracks),{mimeType:mime,videoBitsPerSecond:(s.height||720)>=1000?8000000:5000000,audioBitsPerSecond:128000});
  const c={mr,mime,ext:mime.startsWith('video/mp4')?'mp4':'webm',chunks:[],startPerf:null,stopPerf:null,pauses:[],lost:false,w:s.width||null,h:s.height||null,fps:s.frameRate||null,label:CAM.label,deviceId:s.deviceId||''};
  mr.ondataavailable=e=>{if(e.data&&e.data.size)c.chunks.push(e.data)};
  mr.addEventListener('start',()=>{c.startPerf=performance.now()});
  mr.onerror=e=>{console.warn('camera recorder error',e.error||e);c.lost=true;toast('The camera recording failed. The audio goes on recording.',6000)};
  return c}
function camStop(c){return new Promise(ok=>{if(!c||c.mr.state==='inactive')return ok();c.mr.onstop=()=>{c.stopPerf=performance.now();ok()};try{c.mr.stop()}catch{ok()}setTimeout(ok,4000)})}

/* ---------------- recording ---------------- */
function recTime(){return S.rec?S.rec.samples/MIC.ctx.sampleRate:0}
async function startRec(){
  if(S.rec)return;
  if(!MIC.stream){try{await openMic(LS.get('mic',''))}catch{return}}
  if(MIC.ctx.state!=='running')try{await MIC.ctx.resume()}catch{}
  if(window.showDirectoryPicker&&RF.handle&&RF.perm!=='granted'){RF.perm=await rfPerm(true);paintFolder();if(RF.perm==='granted')scanAll()}
  if(window.showDirectoryPicker&&!RF.handle)toast('No folder chosen: this take will go to Downloads. Choose Course.recordings to save it in place.',6000);
  const v=V[S.cur],patch=S.mode==='patch';
  if(patch&&!S.sel.size){toast('Select the paragraphs to re-read first (click them).');return}
  const useCam=camWanted(v);
  if(useCam&&!CAM.stream){try{await openCam(LS.get('cam',''))}catch{toast('“Camera on” is ticked, but the camera is not available. Allow it, or untick “Camera on” to record audio only.',7000);return}}
  if(patch)S.para=order()[0];   // a patch take always starts at the first selected paragraph
  S.rec={video:v.id,patch,sel:patch?order():null,started:new Date(),chunks:[],samples:0,paused:false,clipped:false,events:[],pauses:[],
    push(c){this.chunks.push(c);this.samples+=c.length},audioMarks:[],audioMark(m){this.audioMarks.push({frame:m.started,time:m.time,perf:performance.now()})}};
  S.rec.events.push({type:'start',para:S.para,t:0});
  if(useCam){try{S.rec.cam=camRecorder(S.rec)}catch(e){S.rec=null;toast(String(e.message||e),7000);return}}
  /* one shared start (performance.now t0): the camera recorder and the WAV tap are started in the same task, both start
     times kept. The WAV never waits for the camera (its encoder can take a moment to start; no word may be lost) */
  S.rec.t0=performance.now();if(S.rec.cam)S.rec.cam.mr.start(1000);MIC.ctl('start');S.rec.audioCall=performance.now();
  setUI();paintParas();tick();toast((patch?'Recording a re-read of '+S.sel.size+' paragraph'+(S.sel.size>1?'s':'')+'. ':'Recording. ')+'Space = next paragraph, M = mistake.');
}
function togglePause(){const r=S.rec;if(!r)return;
  if(!r.paused){MIC.ctl('pause');if(r.cam&&r.cam.mr.state==='recording'){r.cam.mr.pause();r.cam.pauses.push({pause:performance.now()})}r.paused=true;r.pauses.push({at:+recTime().toFixed(3)})}
  else{if(r.cam&&r.cam.mr.state==='paused'){r.cam.mr.resume();r.cam.pauses.push({resume:performance.now()})}MIC.ctl('start');r.paused=false}
  setUI()}
function mistake(){const r=S.rec;if(!r||r.paused)return;const t=recTime();r.events.push({type:'mistake',para:S.para,t});
  const el=document.querySelector('#paras .p.cur');if(el){el.classList.remove('flash');void el.offsetWidth;el.classList.add('flash');let mk=el.querySelector('.mk');if(!mk){mk=document.createElement('span');mk.className='mk';el.appendChild(mk)}mk.dataset.n=(+(mk.dataset.n||0))+1;mk.textContent='✕ '+mk.dataset.n}
  toast('Mistake marked at '+fmt(t,true)+'. Repeat the sentence.',2200)}
async function stopRec(){
  const r=S.rec;if(!r||r.stopping)return;r.stopping=true;
  const camDone=r.cam?camStop(r.cam):null;
  await new Promise(ok=>{MIC._flushed=ok;MIC.ctl('flush');setTimeout(ok,800)});MIC._flushed=null;
  if(camDone){$('#state').textContent='Saving the camera video…';await camDone}
  S.rec=null;setUI();paintParas();
  if(!r.samples){toast('The recording was empty. Nothing saved.');return}
  const sr=MIC.ctx.sampleRate,dur=r.samples/sr,v=BYID[r.video];
  const name=r.video+(r.patch?'-patch-':'-')+r.started.toISOString().replace(/[:.]/g,'-')+'.wav';
  const wav=encodeWav(r.chunks,r.samples,sr);
  const ps=flat(v);const starts=[];for(const e of r.events)if(e.type!=='mistake')starts.push({para:e.para,t:+e.t.toFixed(3),how:e.type});
  const reached=new Set(starts.map(e=>e.para)),read=(r.patch?r.sel:ps.map((_,i)=>i)).filter(i=>reached.has(i)),unread=r.patch?r.sel.filter(i=>!reached.has(i)):[];
  const side={file:name,pageBuiltAt:DATA.builtAt||null,videoId:r.video,kind:r.patch?'patch':'full',recordedAt:r.started.toISOString(),duration:+dur.toFixed(3),sampleRate:sr,channels:1,bitsPerSample:16,format:'WAV PCM 16-bit mono',
    mic:{label:MIC.label,deviceId:(MIC.settings||{}).deviceId||'',settings:MIC.settings,engine:MIC.engine},
    constraints:{echoCancellation:false,noiseSuppression:false,autoGainControl:false},clipped:!!r.clipped,
    paragraphStarts:starts,mistakes:r.events.filter(e=>e.type==='mistake').map(e=>({t:+e.t.toFixed(3),para:e.para,text:ps[e.para]})),
    pauses:r.pauses,paragraphs:(r.patch?r.sel:ps.map((_,i)=>i)).map(i=>({i,text:ps[i]})),read,scriptParagraphs:ps.length,
    note:(r.patch?'PATCH take: only the paragraphs listed in "paragraphs" (i = index in the current script) were re-read; they replace those paragraphs of the full take. ':'')+'Times are seconds in this WAV (pauses removed). read: the paragraph indexes she reached (only these count as re-read). paragraphStarts: when each paragraph was reached (Space/click; back/jump also listed). mistakes: "I stumbled; I repeat this sentence" - cut the take of that sentence before the mark.',
    tool:'reading_studio.py v1'};
  const files=[[name,wav]];
  if(r.cam&&r.cam.chunks.length){const c=r.cam,camName=name.replace(/\.wav$/,'.'+c.ext),blob=new Blob(c.chunks,{type:c.mime.split(';')[0]});
    side.camera=camSide(r,c,camName,sr,dur,blob.size);side.tool='reading_studio.py v2 (camera)';files.push([camName,blob])}
  else if(r.cam){side.camera={file:null,error:'no video data was recorded'};toast('The camera recorded nothing. The audio is saved.',7000)}
  const json=new Blob([JSON.stringify(side,null,1)],{type:'application/json'});
  setLastTake(wav,name);
  files.push([name.replace(/\.wav$/,'.json'),json]);
  const where=await saveFiles(r.video,files);
  const st=S.status[r.video]||{takes:0,patches:0,changed:null};
  if(r.patch){const done=new Set(read.map(i=>norm(ps[i])));S.status[r.video]={...st,patches:(st.patches||0)+1,changed:st.changed?st.changed.filter(i=>!done.has(norm(ps[i]))):st.changed}}
  else S.status[r.video]={takes:(st.takes||0)+1,latest:name,seconds:dur,patches:0,changed:[]};
  if(where)await scanVideo(r.video);renderList();
  if(V[S.cur].id===r.video){const keep=S.para;S.sel=new Set([...S.sel].filter(i=>changedList().includes(i)));renderParas();S.para=keep;paintParas()}
  $('#state').textContent=where?'Saved '+fmt(dur)+' → '+where:'Downloaded '+name+(files.length>2?' (and its camera video and .json). Move all three':' (and its .json). Move both')+' to Course.recordings/_reading/'+r.video+'/';
  toast(where?'Saved ('+fmt(dur)+').':'Downloaded to your Downloads folder.',4000);
  if(unread.length){const msg=unread.map(i=>'Paragraph '+(i+1)+' (“'+ps[i].split(' ').slice(0,5).join(' ')+'…”)').join(', ')+(unread.length>1?' weren\'t':' wasn\'t')+' read yet. '+(unread.length>1?'They stay':'It stays')+' marked “needs re-read”.';
    $('#state').textContent+=' · '+msg;toast(msg,9000)}
  if(r.clipped)toast('Some peaks were too loud (clipping). Move back a little or lower the mic gain.',6000);
}
function camSide(r,c,file,sr,dur,size){
  /* WAV t=0 = the first recorded audio frame (worklet mark: context time -> performance.now via getOutputTimestamp, minus
     the output + input latency); camera t=0 = MediaRecorder 'start'. startOffset = camera start - WAV start (s):
     a moment at WAV time t is at camera time t - startOffset. */
  let aPerf=r.audioCall,how='start call (ScriptProcessor)';const m=r.audioMarks[0];
  if(m&&MIC.ctx.getOutputTimestamp){try{const ts=MIC.ctx.getOutputTimestamp(),lat=(MIC.ctx.outputLatency||MIC.ctx.baseLatency||0)+((MIC.settings||{}).latency||0);
    if(ts.performanceTime>0){aPerf=ts.performanceTime+(m.time-ts.contextTime)*1000-lat*1000;how='worklet frame '+m.frame+' via getOutputTimestamp, latency '+(lat*1000).toFixed(1)+' ms'}else{aPerf=m.perf;how='worklet message arrival'}}catch{aPerf=m.perf;how='worklet message arrival'}}
  const cPerf=c.startPerf!=null?c.startPerf:r.t0;let paused=0,ps=null;for(const p of c.pauses){if(p.pause!=null)ps=p.pause;else if(ps!=null){paused+=p.resume-ps;ps=null}}
  return {file,startOffset:+((cPerf-aPerf)/1000).toFixed(4),fps:c.fps,w:c.w,h:c.h,mime:c.mime,bytes:size,
    camera:{label:c.label,deviceId:c.deviceId},audioInFile:'the same microphone, compressed - for the sync check only; the WAV is the narration',
    clock:'performance.now() ms, from the shared start t0',t0:+r.t0.toFixed(3),cameraStartMs:+(cPerf-r.t0).toFixed(3),wavStartMs:+(aPerf-r.t0).toFixed(3),wavStartFrom:how,
    approxDuration:c.stopPerf?+((c.stopPerf-cPerf-paused)/1000).toFixed(3):null,wavDuration:+dur.toFixed(3),
    pauses:c.pauses.map(p=>p.pause!=null?{pauseMs:+(p.pause-r.t0).toFixed(1)}:{resumeMs:+(p.resume-r.t0).toFixed(1)}),lost:!!c.lost,
    note:'Paused together with the WAV (pauses are removed from both files). startOffset is the browser estimate; reading_to_video.py measures the exact offset (along the take) by matching this file\'s audio to the WAV.'}}
async function saveFiles(id,files){
  if(RF.handle){try{let p=await rfPerm(true);RF.perm=p;paintFolder();
    if(p==='granted'){const d=await videoDir(id,true);for(const [n,b] of files){const fh=await d.getFileHandle(n,{create:true}),w=await fh.createWritable();await w.write(b);await w.close()}
      return rootLabel()+'/'+id+'/'+files[0][0]}}catch(e){console.warn('saving in the folder failed, downloading instead',e)}}
  for(const [n,b] of files)download(n,b);return null}
function download(n,b){const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=n;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),60000)}
function encodeWav(chunks,n,sr){const buf=new ArrayBuffer(44+n*2),dv=new DataView(buf);const w=(o,s)=>{for(let i=0;i<s.length;i++)dv.setUint8(o+i,s.charCodeAt(i))};
  w(0,'RIFF');dv.setUint32(4,36+n*2,true);w(8,'WAVE');w(12,'fmt ');dv.setUint32(16,16,true);dv.setUint16(20,1,true);dv.setUint16(22,1,true);dv.setUint32(24,sr,true);dv.setUint32(28,sr*2,true);dv.setUint16(32,2,true);dv.setUint16(34,16,true);w(36,'data');dv.setUint32(40,n*2,true);
  const out=new Int16Array(buf,44,n);let o=0;for(const c of chunks)for(let i=0;i<c.length;i++){const s=Math.max(-1,Math.min(1,c[i]));out[o++]=s<0?Math.round(s*32768):Math.round(s*32767)}
  return new Blob([buf],{type:'audio/wav'})}
function setLastTake(blob,name){if(S.lastUrl)URL.revokeObjectURL(S.lastUrl);S.lastUrl=URL.createObjectURL(blob);$('#player').src=S.lastUrl;$('#playLbl').textContent='Last take · '+name.replace(/^.*?-(\d{4}-\d\d-\d\d)T(\d\d)-(\d\d).*$/,'$1 $2:$3')}
async function loadLatestTake(){const v=V[S.cur],st=S.status[v.id];
  if(!st||RF.perm!=='granted'){if(S.lastUrl){URL.revokeObjectURL(S.lastUrl);S.lastUrl=null}$('#player').removeAttribute('src');$('#player').load();$('#playLbl').textContent=st?'Last take (connect the folder to play)':'No take yet';return}
  try{const d=await videoDir(v.id,false),f=await (await d.getFileHandle(st.latest)).getFile();if(V[S.cur].id===v.id)setLastTake(f,st.latest)}catch(e){$('#playLbl').textContent='No take yet'}}
let tickRaf=0;
function tick(){cancelAnimationFrame(tickRaf);const f=()=>{if(!S.rec){return}$('#timer').textContent=fmt(recTime(),true);tickRaf=requestAnimationFrame(f)};f()}
function setUI(){const r=S.rec,t=$('#timer');
  $('#bRec').disabled=!!r;$('#bPause').disabled=!r;$('#bStop').disabled=!r;$('#bMist').disabled=!r||r.paused;$('#bNext').disabled=!!r;$('#micSel').disabled=!!r;$('#camOn').disabled=!!r;$('#camSel').disabled=!!r;
  $('#bPause').textContent=r&&r.paused?'Resume':'Pause';
  t.classList.toggle('on',!!r&&!r.paused);t.classList.toggle('paused',!!r&&r.paused);
  const s=$('#state');s.classList.toggle('rec',!!r);s.textContent=!r?'Ready.':r.paused?'Paused (not recording).':'● Recording'+(r.cam?' (camera + audio)':'');
  if(!r)t.textContent=fmt(0,true)}
$('#bRec').onclick=startRec;$('#bPause').onclick=togglePause;$('#bStop').onclick=stopRec;$('#bMist').onclick=mistake;
$('#bNext').onclick=()=>selectVideo(S.cur+1);
document.addEventListener('keydown',e=>{
  if(e.target.closest&&e.target.closest('select,input,textarea'))return;if(e.metaKey||e.ctrlKey||e.altKey)return;
  const k=e.key;
  if(k===' '||k==='ArrowRight'||k==='ArrowDown'||k==='PageDown'){e.preventDefault();if(document.activeElement&&document.activeElement.blur)document.activeElement.blur();if(!S.rec||!S.rec.paused)nextPara()}
  else if(k==='ArrowLeft'||k==='ArrowUp'||k==='PageUp'){e.preventDefault();step(-1)}
  else if(k==='m'||k==='M'){e.preventDefault();mistake()}
  else if(k==='p'||k==='P'){e.preventDefault();togglePause()}
});
window.addEventListener('beforeunload',e=>{if(S.rec){e.preventDefault();e.returnValue=''}});

/* ---------------- start ---------------- */
(async()=>{
  fontSize(0);
  const last=LS.get('cur',null),i=V.findIndex(v=>v.id===last);S.cur=i<0?0:i;
  renderList();renderParas();paintFolder();setUI();
  await initFolder();loadLatestTake();
  try{const p=await navigator.permissions.query({name:'microphone'});if(p.state==='granted')await openMic(LS.get('mic',''))}catch{}
  await syncCam(false);
})();
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('topics', nargs='*', type=int)
    ap.add_argument('--ids', help='comma-separated video ids instead of / before the topics')
    ap.add_argument('-o', '--out', default=OUT)
    a = ap.parse_args()
    if not a.topics and not a.ids:
        ap.error('give a topic number (e.g. 13) or --ids')
    out, vids = build(a.topics, a.ids.split(',') if a.ids else None, a.out)
    print('%s  (%d videos, %.0f min, %d paragraphs)' % (out, len(vids), sum(v['minutes'] for v in vids),
                                                        sum(len(sl) for v in vids for sl in v['paras'])))


if __name__ == '__main__':
    main()
