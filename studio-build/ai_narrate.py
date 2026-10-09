"""AI narration in the teacher's cloned voice (ElevenLabs).

    python3 studio-build/ai_narrate.py vr50-a-score                 # per-line mode: one mp3 per line
    python3 studio-build/ai_narrate.py vr50-a-score --preview       # ... and write one listening file to ~/Downloads
    python3 studio-build/ai_narrate.py solve-geo33-g091 --continuous          # the WHOLE video in ONE request
    python3 studio-build/ai_narrate.py solve-geo33-g091 --continuous --remap  # re-time from the saved alignment (no credits)
    python3 studio-build/ai_narrate.py solve-q-544 --segmented               # line by line, per-line voice preset, joined
    python3 studio-build/ai_narrate.py solve-q-544 --remap                   # (a segmented video re-times as segmented)

ai_scripts/<videoId>.json = {"slides": [[line, line, ...], ...]} — one entry per spoken line of the video, in order
(the studio's auto-narrate plays line i where the video has spoken line i). A line is a string, or
{"say": "...", "at": ["phrase", null, ...]}: `at` times the video's cues (APPEAR / POINT / DRAW mark) that come right
BEFORE this spoken line, in their order — each fires when the voice reaches that phrase of the line (null = default:
appear / mark at the start of the line, POINT at its `at` fraction). "<phrase" = that phrase of the PREVIOUS spoken line
(e.g. an arrow part cue that studio_arrows puts after a line, but should show while that line is said).

Audio goes to ~/Documents/Course.recordings/_ai_audio/<videoId>/ + manifest.json.
  per-line:    line-001.mp3 ... ; a line is re-generated only when its text or the voice changes.
  continuous:  audio.mp3 (the whole video, one request -> continuous prosody, the last sentence sounds final) +
               alignment.json (character times from /with-timestamps) + manifest {"mode": "continuous",
               "lines": [{text, slide, start, end, at: [seconds|null]}]}. Slides are separated by a short
               <break time="0.6s"/> (eleven_multilingual_v2 supports break tags; v3/v4 get a [pause] tag instead). A line
               may carry "pause": seconds (a short pause after it, e.g. after reading the question). SAY_AS respells words for the TTS only (v4: "pi" -> "pie"). For multilingual_v2 a [pause] / [short pause] tag in a
               line becomes a <break>, other tags are dropped. Audio tags in a
               line ([excited], ...) are sent only to eleven_v3 / eleven_v4 and dropped for older models. Re-generated only
               when the text or the voice changes; --remap recomputes the timing from alignment.json for free.
  segmented:   (teacher 2026-10-09, "mix 3") one request per line / per part of a line between [pause] tags, each in
               its line's voice preset ({"voice": "calm"}; presets in _voice.json), previous/next text as context; silence
               trimmed, loudness evened, joined with set gaps into the same audio.mp3 + alignment.json + manifest as
               continuous mode (+ "gen": "segmented"). Unchanged parts are reused from seg/ (no credits).
Needs ELEVENLABS_API_KEY in ~/psychometry-course/.env.local; segmented mode needs ffmpeg + numpy.
"""
import base64, difflib, hashlib, json, os, re, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.environ.get('AI_AUDIO_OUT') or os.path.expanduser('~/Documents/Course.recordings/_ai_audio')   # env: offline tests
SLIDE_BREAK = 0.6


def key():
    for line in open(os.path.join(ROOT, '.env.local'), encoding='utf-8'):
        m = re.match(r'\s*ELEVENLABS_API_KEY\s*=\s*(\S+)', line)
        if m: return m.group(1).strip('"\'')
    sys.exit('ELEVENLABS_API_KEY missing in .env.local')


def _body(voice, text):
    vs = {'stability': voice['stability'], 'similarity_boost': voice['similarity_boost']}
    if voice.get('speed') is not None: vs['speed'] = voice['speed']      # 1.0 = default pace
    for k in ('style', 'use_speaker_boost'):                               # optional: style exaggeration, speaker boost
        if voice.get(k) is not None: vs[k] = voice[k]
    return {'text': text, 'model_id': voice['model_id'], 'voice_settings': vs}


def tts(k, voice, text, prev, nxt):
    body = _body(voice, text)
    if prev: body['previous_text'] = prev
    if nxt: body['next_text'] = nxt
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/%s?output_format=mp3_44100_128' % voice['voice_id'],
                                 data=json.dumps(body).encode(), headers={'xi-api-key': k, 'Content-Type': 'application/json', 'accept': 'audio/mpeg'})
    return urllib.request.urlopen(req, timeout=180).read()


def tts_timestamps(k, voice, text, prev='', nxt='', seed=None):
    body = _body(voice, text)
    if seed is not None: body['seed'] = seed
    if prev: body['previous_text'] = prev
    if nxt: body['next_text'] = nxt
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/%s/with-timestamps?output_format=mp3_44100_128' % voice['voice_id'],
                                 data=json.dumps(body).encode(), headers={'xi-api-key': k, 'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req, timeout=300).read())


def duration(path):
    out = subprocess.run(['afinfo', path], capture_output=True, text=True).stdout
    m = re.search(r'estimated duration: ([\d.]+)', out)
    return float(m.group(1)) if m else 0.0


def line_text(l):
    return l['say'] if isinstance(l, dict) else l


def load(vid):
    spec = json.load(open(os.path.join(HERE, 'ai_scripts', vid + '.json'), encoding='utf-8'))
    # one shared voice for all videos (ai_scripts/_voice.json); a script file may override it with its own 'voice'
    voice = spec.get('voice') or json.load(open(os.path.join(HERE, 'ai_scripts', '_voice.json'), encoding='utf-8'))
    voice = {k: voice[k] for k in ('voice_id', 'model_id', 'stability', 'similarity_boost', 'speed', 'style', 'use_speaker_boost') if k in voice}
    return spec, voice


VKEYS = ('voice_id', 'model_id', 'stability', 'similarity_boost', 'speed', 'style', 'use_speaker_boost')


def presets():
    """named voice presets from ai_scripts/_voice.json {"presets": {"base": {...}, "calm": {...}}, "default": "base"}:
    each preset = the top-level voice with its own settings on top. -> ({name: voice}, default name)"""
    v = json.load(open(os.path.join(HERE, 'ai_scripts', '_voice.json'), encoding='utf-8'))
    top = {k: v[k] for k in VKEYS if k in v}
    ps = {n: dict(top, **{k: p[k] for k in VKEYS if k in p}) for n, p in (v.get('presets') or {'base': {}}).items()}
    return ps, v.get('default') or next(iter(ps))


# ---------------------------------------------------------------- continuous mode
def expressive(model):
    """eleven_v3 / eleven_v4 read audio tags ([excited], [short pause]) but no SSML <break>; older models the reverse."""
    return bool(re.match(r'eleven_v[34]', model or ''))


TAG = r'\[[a-z][a-z -]*\]'                 # an audio tag: [calmly], [matter-of-fact], [short pause], ...
PAUSE_TAG = {'short pause': 0.4, 'pause': 0.8, 'long pause': 1.5}


def spoken(t, model):
    """the line as written in the manifest / transcript: audio tags are kept for v3/v4 and dropped for older models
    (which would read them out)."""
    t = t.strip()
    if not expressive(model): t = re.sub(r'\s+', ' ', re.sub(r'\s*' + TAG + r'\s*', ' ', t)).strip()
    return t


def tts_form(t, model):
    """the line as SENT to the model: v3/v4 get the tags as they are; older models (multilingual_v2) get a pause tag as
    an SSML <break> and every other tag dropped (nothing in brackets is ever read aloud); then SAY_AS respellings."""
    t = t.strip()
    if not expressive(model):
        t = re.sub(TAG, lambda m: (' <break time="%.1fs"/> ' % PAUSE_TAG[m.group(0)[1:-1]]) if m.group(0)[1:-1] in PAUSE_TAG else ' ', t)
        t = re.sub(r'\s+', ' ', t).strip()
    return say_as(t, model)


# TTS text only (the manifest / transcript keep the written word), per model family
SAY_AS = {'v34': [(r'\bpi\b', 'pie')],     # eleven_v4: "pi" -> "pie", never "P I"
          'v2': []}                         # multilingual_v2 says "pi" right as written (checked 2026-10-09)


def say_as(t, model=None):
    for a, b in SAY_AS['v34' if expressive(model) else 'v2']: t = re.sub(a, b, t)
    return t


def pause(sec, model):
    """a pause in the text: SSML break (multilingual_v2) or an audio tag (v3/v4)."""
    if expressive(model): return ' [short pause] ' if sec < 0.8 else ' [pause] '
    return ' <break time="%.1fs"/> ' % sec


def full_text(spec, model=None):
    """the text sent in one request + for every line (slide, char start, char end) in that text.
    A line {"say": ..., "pause": 0.5} is followed by a short pause (e.g. after reading the question aloud)."""
    text, spans, gap = '', [], ''
    for si, sl in enumerate(spec['slides']):
        for li, l in enumerate(sl):
            if text: text += pause(SLIDE_BREAK, model) if li == 0 else (gap or ' ')
            t = tts_form(line_text(l), model)
            spans.append((si, len(text), len(text) + len(t)))
            text += t
            gap = pause(l['pause'], model) if isinstance(l, dict) and l.get('pause') else ''
    return text, spans


def char_times(text, al):
    """per character of `text`: (start, end) seconds from the alignment (mapped with difflib, so a few characters the
    service drops or adds — e.g. the break tag — don't shift anything)."""
    A = ''.join(al['characters']); st, en = al['character_start_times_seconds'], al['character_end_times_seconds']
    m = [None] * len(text)
    for a, b, n in difflib.SequenceMatcher(None, text, A, autojunk=False).get_matching_blocks():
        for i in range(n): m[a + i] = b + i
    out = [None] * len(text)
    for i, j in enumerate(m):
        if j is not None: out[i] = (st[j], en[j])
    return out


def _at(ct, a, b, pick='start'):
    """first (pick=start) / last (pick=end) known time in text[a:b]."""
    rng = range(a, b) if pick == 'start' else range(b - 1, a - 1, -1)
    for i in rng:
        if ct[i]: return ct[i][0] if pick == 'start' else ct[i][1]
    return None


def remap(vid, spec, d, voice, h, seg=None):
    """seg (segmented mode) = (text, spans, per-line text as placed in `text`, extra manifest fields)"""
    text, spans = (seg[0], seg[1]) if seg else full_text(spec, voice.get('model_id'))
    al = json.load(open(os.path.join(d, 'alignment.json')))
    ct = char_times(text, al)
    lines, flat, tts_l = [], [l for sl in spec['slides'] for l in sl], []
    for (si, a, b), l in zip(spans, flat):
        t = spoken(line_text(l), voice.get('model_id')); tt = seg[2][len(lines)] if seg else tts_form(line_text(l), voice.get('model_id')); tts_l.append(tt)   # tt = as sent
        s0, e0 = _at(ct, a, b, 'start'), _at(ct, a, b, 'end')
        if s0 is None or e0 is None: sys.exit('alignment: no times for line %r' % t[:60])
        ats = []
        for ph in (l.get('at') or []) if isinstance(l, dict) else []:
            if ph is None: ats.append(None); continue
            sa, st_ = a, tt                     # "<phrase" = a phrase near the end of the PREVIOUS spoken line
            if ph.startswith('<'):
                if not lines: sys.exit('%s: %r - no previous line' % (vid, ph))
                ph = ph[1:]; pi = len(lines) - 1; sa = spans[pi][1]; st_ = tts_l[pi]
            ph = say_as(ph, voice.get('model_id')); k = st_.lower().find(ph.lower())
            if k < 0: sys.exit('%s: phrase %r not in line %r' % (vid, ph, st_[:70]))
            ats.append(round(_at(ct, sa + k, sa + k + len(ph), 'start'), 3))
        lines.append({'text': t, 'slide': si, 'start': round(s0, 3), 'end': round(e0, 3), 'at': ats})
    secs = duration(os.path.join(d, 'audio.mp3')) or (lines[-1]['end'] + 0.3)
    man = {'videoId': vid, 'mode': 'continuous', 'voice': voice, 'hash': h, 'file': 'audio.mp3', 'seconds': round(secs, 2), 'lines': lines}
    if seg: man.update(seg[3])
    json.dump(man, open(os.path.join(d, 'manifest.json'), 'w'), indent=1, ensure_ascii=False)
    gaps = [round(y['start'] - x['end'], 2) for x, y in zip(lines, lines[1:])]
    print('%s: %d lines, %.1f s of audio (%s); gaps between lines: %s' % (vid, len(lines), secs, 'segmented' if seg else 'continuous', gaps))
    return man


def continuous(vid, spec, voice):
    d = os.path.join(OUT, vid); os.makedirs(d, exist_ok=True)
    text, _ = full_text(spec, voice.get('model_id'))
    h = hashlib.sha1(json.dumps([text, voice, 'continuous'], sort_keys=True).encode()).hexdigest()[:16]
    mpath = os.path.join(d, 'manifest.json')
    old = json.load(open(mpath)) if os.path.exists(mpath) else {}
    have = old.get('mode') == 'continuous' and old.get('hash') == h and os.path.exists(os.path.join(d, 'audio.mp3')) \
        and os.path.exists(os.path.join(d, 'alignment.json'))
    if '--remap' in sys.argv:
        if not os.path.exists(os.path.join(d, 'alignment.json')): sys.exit('no alignment.json yet - generate first')
        a_hash = json.load(open(os.path.join(d, 'alignment.json'))).get('_hash')
        if a_hash != h: sys.exit('the spoken text changed since the audio was made - generate again (without --remap)')
        return remap(vid, spec, d, voice, h)
    if not have:
        print('  generating the whole video in one request (%d characters)...' % len(text))
        r = tts_timestamps(key(), voice, text)
        open(os.path.join(d, 'audio.mp3'), 'wb').write(base64.b64decode(r['audio_base64']))
        json.dump({'_hash': h, 'text': text, 'characters': r['alignment']['characters'],
                   'character_start_times_seconds': r['alignment']['character_start_times_seconds'],
                   'character_end_times_seconds': r['alignment']['character_end_times_seconds']},
                  open(os.path.join(d, 'alignment.json'), 'w'), ensure_ascii=False)
        for f in os.listdir(d):              # the old per-line files would only confuse
            if re.match(r'line-\d{3}\.mp3$', f): os.remove(os.path.join(d, f))
    else:
        print('  audio unchanged (no credits used)')
    return remap(vid, spec, d, voice, h)


# ---------------------------------------------------------------- segmented mode
# Teacher 2026-10-09 ("mix 3"): every line (and every part of a line between [pause] / [short pause] tags) is its own
# request in its own voice preset - a line {"say": ..., "voice": "calm"} uses preset "calm" (the question reading, plain
# calculation lines), else the default preset; "voice": ["calm", "base"] = one preset per part of the line. Each part: silence trimmed, loudness evened out, then joined with set gaps
# into ONE audio.mp3 + ONE alignment.json (times shifted) -> manifest exactly like continuous mode, so the studio's
# auto-narrate and the `at` cues work unchanged.
GAP_LINE, GAP_QUESTION, GAP_SLIDE = 0.42, 0.5, 0.75          # after a line / a line ending in "?" / before a new slide
GAP_TAG = {'short pause': 0.6, 'pause': 0.9, 'long pause': 1.4}
SPLIT = re.compile(r'\s*\[(short pause|pause|long pause)\]\s*')
FFMPEG = os.environ.get('FFMPEG') or next((p for p in (subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True).stdout.strip(),
         os.path.expanduser('~/Library/Application Support/Cisdem VideoPaw/ffmpeg')) if p and os.path.exists(p)), None)
SR = 44100


def seg_plan(spec, ps, default):
    """-> segments [{text, line, voice, gap}], the joined plain text, line spans in it, per-line text"""
    flat = [(si, l) for si, sl in enumerate(spec['slides']) for l in sl]
    segs, forms = [], []
    for i, (si, l) in enumerate(flat):
        pv = (l.get('voice') if isinstance(l, dict) else None) or default      # a preset, or a list: one per part
        parts = SPLIT.split(line_text(l).strip())          # text, tag, text, tag, ...
        if not parts[0].strip() and len(parts) > 1:        # a line that STARTS with [pause]: a longer gap before it
            if segs: segs[-1]['gap'] = max(segs[-1]['gap'], GAP_TAG[parts[1]])
            parts = parts[2:]
        pvs = pv if isinstance(pv, list) else [pv] * len(parts[0::2])
        if len(pvs) != len(parts[0::2]): sys.exit('line %d: %d voices for %d parts (parts are split at [pause] tags)' % (i + 1, len(pvs), len(parts[0::2])))
        for x in pvs:
            if x not in ps: sys.exit('line %d: unknown voice preset %r (have %s)' % (i + 1, x, list(ps)))
        texts = [say_as(spoken(x, ps[q]['model_id']), ps[q]['model_id']) for x, q in zip(parts[0::2], pvs)]
        tags = parts[1::2] + [None]
        keep = [(t, g, q) for t, g, q in zip(texts, tags, pvs) if t]
        for j, (t, g, pv) in enumerate(keep):
            last = j == len(keep) - 1
            if not last: gap = GAP_TAG[g or 'short pause']
            elif i == len(flat) - 1: gap = 0
            elif flat[i + 1][0] != si: gap = GAP_SLIDE
            elif isinstance(l, dict) and l.get('pause'): gap = max(GAP_SLIDE, l['pause'] + 0.3)
            else: gap = GAP_QUESTION if t.endswith('?') else GAP_LINE
            if last and g: gap = max(gap, GAP_TAG[g])       # a line ending in [pause]
            segs.append({'text': t, 'line': i, 'voice': pv, 'gap': gap})
        forms.append(' '.join(t for t, _, _ in keep))
    text, spans, pos = '', [], 0
    for (si, l), f in zip(flat, forms):
        if text: text += ' '
        spans.append((si, len(text), len(text) + len(f))); text += f
    return segs, text, spans, forms


# ---- falling statement endings (teacher 2026-10-09: some statement endings rose and sounded like a question).
# For every sentence ending in "." or "!" in a part: the pitch slope over its last 0.4 s of voiced speech (semitones per
# second) and its end level (median pitch of the last 0.15 s minus the sentence's median, semitones). RISING = slope > +5
# and end level > -1 - her real clip (solve-q-r26-t06-02, 0:08-1:04): statement endings median slope -3.5 st/s, end level
# -2.0 st. A part with a rising ending is made again (new seed, up to END_TRIES more takes); the take with the fewest /
# smallest rising endings is kept. Runs with parselmouth (Praat) when installed, else a simple autocorrelation tracker.
END_SLOPE, END_LEVEL, END_TRIES = 5.0, -1.0, 3


def _pitch(y):
    """-> (times, semitones) of voiced 10 ms frames, 90-400 Hz"""
    import numpy as np
    try:
        import parselmouth
        p = parselmouth.Sound(y.astype('float64'), SR).to_pitch_ac(time_step=0.01, pitch_floor=90, pitch_ceiling=400)
        t, f = p.xs(), p.selected_array['frequency']
    except ImportError:
        n, hp, lo, hi = int(.04 * SR), int(.01 * SR), int(SR / 400), int(SR / 90); pk = float(np.abs(y).max() or 1); t, f = [], []
        for i in range(0, max(0, len(y) - n), hp):
            x = y[i:i + n] - y[i:i + n].mean(); t.append(i / SR + .02); f.append(0.0)
            if np.sqrt(np.mean(x * x)) < pk * .03: continue
            F = np.fft.rfft(x, 2 * n); r = np.fft.irfft(F * np.conj(F))[:n]
            if r[0] <= 0: continue
            k = int(np.argmax(r[lo:hi]))
            if r[lo + k] / r[0] >= .45: f[-1] = SR / (lo + k)
        t, f = np.array(t), np.array(f)
    m = f > 0
    return t[m], 12 * np.log2(f[m] / 100)


def endings(y, al):
    """[(word, slope st/s, end level st, rising)] for the sentences of a take that end in '.' or '!'"""
    import numpy as np
    ch, en = al['characters'], al['character_end_times_seconds']; T, S = _pitch(y); out = []; prev = 0.0
    for i, c in enumerate(ch):
        if c not in '.!?' or (i + 1 < len(ch) and ch[i + 1] != ' ') or (i and ch[i - 1] == '.') or (i + 1 < len(ch) and ch[i + 1] == '.'):
            continue
        j = i
        while j > 0 and not ch[j - 1].isalnum(): j -= 1
        k = j
        while k > 0 and (ch[k - 1].isalnum() or ch[k - 1] in "'-"): k -= 1
        t_end = en[j - 1] if j else 0; a = prev; prev = t_end
        if c == '?': continue
        sel = (T >= a) & (T <= t_end + .05); t, s = T[sel], S[sel]
        if len(s) < 10: continue
        ok = np.abs(s - np.median(s)) < 6; t, s = t[ok], s[ok]
        last = t[-1]; kk = t >= last - .4; ee = t >= last - .15
        if kk.sum() < 6: continue
        sl = float(np.polyfit(t[kk], s[kk], 1)[0]); lv = float(np.median(s[ee]) - np.median(s))
        out.append((''.join(ch[k:j]) + c, round(sl, 1), round(lv, 1), sl > END_SLOPE and lv > END_LEVEL))
    return out


def _end_score(e):
    r = [x for x in e if x[3]]
    return (len(r), sum(x[1] for x in r))


def _pcm(path):
    import numpy as np
    raw = subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype='<i2').astype('float32') / 32768


def segmented(vid, spec):
    import numpy as np
    if not FFMPEG: sys.exit('segmented mode needs ffmpeg (set FFMPEG=/path/to/ffmpeg)')
    ps, default = presets()
    segs, text, spans, forms = seg_plan(spec, ps, default)
    d = os.path.join(OUT, vid); os.makedirs(d, exist_ok=True)
    h = hashlib.sha1(json.dumps([[(x['text'], ps[x['voice']], x['gap']) for x in segs], 'segmented-1'], sort_keys=True).encode()).hexdigest()[:16]
    extra = {'gen': 'segmented', 'presets': ps, 'lineVoices': [], 'segments': []}
    for x in segs:
        while len(extra['lineVoices']) <= x['line']: extra['lineVoices'].append([])
        extra['lineVoices'][x['line']].append(x['voice'])
    if '--remap' in sys.argv:
        a_hash = json.load(open(os.path.join(d, 'alignment.json'))).get('_hash')
        if a_hash != h: sys.exit('the spoken text / voices changed since the audio was made - generate again (without --remap)')
        extra['segments'] = json.load(open(os.path.join(d, 'manifest.json'))).get('segments', [])
        return remap(vid, spec, d, ps[default], h, (text, spans, forms, extra))
    sd = os.path.join(d, 'seg'); os.makedirs(sd, exist_ok=True)
    plain = [x['text'] for x in segs]; k = None; chars = 0
    out, chs, cst, cen, t = [], [], [], [], 0.0
    for n, x in enumerate(segs):
        v = ps[x['voice']]
        sh = hashlib.sha1(json.dumps([x['text'], v], sort_keys=True).encode()).hexdigest()[:12]
        mp, ap = os.path.join(sd, '%s.mp3' % sh), os.path.join(sd, '%s.json' % sh)
        ctx = (' '.join(plain[:n])[-500:], ' '.join(plain[n + 1:])[:300])
        if not (os.path.exists(mp) and os.path.exists(ap)):
            k = k or key()
            r = tts_timestamps(k, v, x['text'], *ctx)
            open(mp, 'wb').write(base64.b64decode(r['audio_base64'])); json.dump(r['alignment'], open(ap, 'w'), ensure_ascii=False)
            chars += len(x['text']); print('  generated part %d/%d [%s] (%d chars)' % (n + 1, len(segs), x['voice'], len(x['text'])))
        # falling statement endings: measure once per part (seg/<hash>.end.json); a rising one -> new takes, keep the best
        cp = os.path.join(sd, '%s.end.json' % sh)
        chk = json.load(open(cp)) if os.path.exists(cp) else None
        if chk is None and '--no-endcheck' not in sys.argv:
            e0 = endings(_pcm(mp), json.load(open(ap))); tries = [{'seed': None, 'endings': e0}]; best = (_end_score(e0), None)
            for tn in range(END_TRIES if best[0][0] else 0):
                seed = 1009 * (tn + 1)
                tm, ta = os.path.join(sd, '%s.s%d.mp3' % (sh, seed)), os.path.join(sd, '%s.s%d.json' % (sh, seed))
                if not os.path.exists(tm):
                    k = k or key()
                    r = tts_timestamps(k, v, x['text'], *ctx, seed=seed)
                    open(tm, 'wb').write(base64.b64decode(r['audio_base64'])); json.dump(r['alignment'], open(ta, 'w'), ensure_ascii=False)
                    chars += len(x['text'])
                e = endings(_pcm(tm), json.load(open(ta))); tries.append({'seed': seed, 'endings': e})
                if _end_score(e) < best[0]: best = (_end_score(e), seed)
                print('  part %d/%d: rising ending, take %d (seed %d): %s' % (n + 1, len(segs), tn + 2, seed, [w for w in e if w[3]] or 'falling'))
                if not best[0][0]: break
            if best[1] is not None:                     # the better take becomes the part's audio (the first take is kept)
                os.replace(mp, os.path.join(sd, '%s.s0.mp3' % sh)); os.replace(ap, os.path.join(sd, '%s.s0.json' % sh))
                import shutil
                shutil.copy(os.path.join(sd, '%s.s%d.mp3' % (sh, best[1])), mp); shutil.copy(os.path.join(sd, '%s.s%d.json' % (sh, best[1])), ap)
            chk = {'chosen': best[1], 'tries': tries, 'endings': next(t['endings'] for t in tries if t['seed'] == best[1])}
            json.dump(chk, open(cp, 'w'), ensure_ascii=False)
        al = json.load(open(ap)); y = _pcm(mp)
        # trim silence: 10 ms frames above -45 dBFS, keep 40 ms before / 80 ms after
        fr = 441; e = np.sqrt(np.add.reduceat(y * y, np.arange(0, len(y), fr)) / fr) if len(y) else np.zeros(1)
        on = np.where(e > 10 ** (-45 / 20))[0]
        a0 = max(0, on[0] * fr - int(.04 * SR)) if len(on) else 0
        a1 = min(len(y), (on[-1] + 1) * fr + int(.08 * SR)) if len(on) else len(y)
        y = y[a0:a1]
        # loudness: RMS of the voiced frames -> -20 dBFS, peaks kept under -1 dBFS
        v_on = e[e > 10 ** (-45 / 20)]; rms = float(np.sqrt(np.mean(v_on ** 2))) if len(v_on) else 0.1
        g = min(10 ** (-20 / 20) / max(rms, 1e-4), 0.89 / max(float(np.abs(y).max()) if len(y) else 1, 1e-4))
        y = y * g; off = t - a0 / SR; t1 = t + len(y) / SR
        if chs: chs.append(' '); cst.append(cen[-1]); cen.append(t)          # the join = one space in the text
        for c, s0, s1 in zip(al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']):
            # times inside the trimmed part (the last character's end time often reaches into the trimmed tail)
            chs.append(c); cst.append(round(min(t1, max(t, s0 + off)), 3)); cen.append(round(min(t1, max(t, s1 + off)), 3))
        extra['segments'].append({'line': x['line'] + 1, 'voice': x['voice'], 'start': round(t, 3), 'end': round(t + len(y) / SR, 3),
                                  'gain_db': round(20 * np.log10(g), 1), 'text': x['text'],
                                  'endings': (chk or {}).get('endings'), 'take': (chk or {}).get('chosen'), 'tries': len((chk or {}).get('tries') or [0])})
        out.append(y); t += len(y) / SR
        if x['gap']: out.append(np.zeros(int(x['gap'] * SR), dtype='float32')); t += x['gap']
    pcm = (np.clip(np.concatenate(out), -1, 1) * 32767).astype('<i2').tobytes()
    subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', '-',
                    '-c:a', 'libmp3lame', '-b:a', '128k', os.path.join(d, 'audio.mp3')], input=pcm, check=True)
    json.dump({'_hash': h, 'text': text, 'characters': chs, 'character_start_times_seconds': cst, 'character_end_times_seconds': cen},
              open(os.path.join(d, 'alignment.json'), 'w'), ensure_ascii=False)
    for f in os.listdir(d):
        if re.match(r'line-\d{3}\.mp3$', f): os.remove(os.path.join(d, f))
    print('  %d parts, %d characters generated now' % (len(segs), chars))
    still = [(x['line'], w) for x in extra['segments'] for w in (x['endings'] or []) if w[3]]
    if still: print('  STILL RISING after %d takes: %s' % (END_TRIES + 1, still))
    return remap(vid, spec, d, ps[default], h, (text, spans, forms, extra))


# ---------------------------------------------------------------- per-line mode
def per_line(vid, spec, voice):
    lines = [tts_form(line_text(l), voice['model_id']) for s in spec['slides'] for l in s]
    d = os.path.join(OUT, vid); os.makedirs(d, exist_ok=True)
    mpath = os.path.join(d, 'manifest.json')
    old = json.load(open(mpath)) if os.path.exists(mpath) else {'lines': []}
    oldh = {x['file']: x['hash'] for x in old['lines'] if 'file' in x and 'hash' in x}
    k = None; man = []; chars = 0
    for i, text in enumerate(lines):
        f = 'line-%03d.mp3' % (i + 1)
        h = hashlib.sha1(json.dumps([text, voice], sort_keys=True).encode()).hexdigest()[:16]
        p = os.path.join(d, f)
        if oldh.get(f) != h or not os.path.exists(p):
            k = k or key()
            open(p, 'wb').write(tts(k, voice, text, lines[i - 1] if i else '', lines[i + 1] if i + 1 < len(lines) else ''))
            chars += len(text); print('  generated', f, '(%d chars)' % len(text))
        man.append({'file': f, 'text': text, 'hash': h, 'seconds': round(duration(p), 2)})
    json.dump({'videoId': vid, 'voice': voice, 'lines': man}, open(mpath, 'w'), indent=1, ensure_ascii=False)
    print('%s: %d lines, %.0f s of audio, %d characters generated now' % (vid, len(man), sum(x['seconds'] for x in man), chars))
    return d, man


def _gen(vid):
    p = os.path.join(OUT, vid, 'manifest.json')
    return json.load(open(p)).get('gen') if os.path.exists(p) else None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args: sys.exit(__doc__)
    vid = args[0]
    spec, voice = load(vid)
    if '--segmented' in sys.argv or ('--remap' in sys.argv and _gen(vid) == 'segmented'):
        segmented(vid, spec)
        if '--preview' in sys.argv:
            dst = os.path.expanduser('~/Downloads/%s-ai-preview.mp3' % vid)
            subprocess.run(['cp', os.path.join(OUT, vid, 'audio.mp3'), dst], check=True); print('preview:', dst)
        return
    if '--continuous' in sys.argv or '--remap' in sys.argv:
        continuous(vid, spec, voice)
        if '--preview' in sys.argv:
            dst = os.path.expanduser('~/Downloads/%s-ai-preview.mp3' % vid)
            subprocess.run(['cp', os.path.join(OUT, vid, 'audio.mp3'), dst], check=True); print('preview:', dst)
        return
    d, man = per_line(vid, spec, voice)
    if '--preview' in sys.argv:
        import tempfile, wave
        tmp = tempfile.mkdtemp(dir=d); pcm = b''; rate = 44100
        for i, x in enumerate(man):
            w = os.path.join(tmp, '%03d.wav' % i)
            subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16@44100', '-c', '1', os.path.join(d, x['file']), w], check=True)
            b = open(w, 'rb').read(); j = b.find(b'data'); pcm += b[j + 8:] + b'\0\0' * int(rate * 0.35)
        wp = os.path.join(tmp, 'all.wav')
        with wave.open(wp, 'wb') as ww:
            ww.setnchannels(1); ww.setsampwidth(2); ww.setframerate(rate); ww.writeframes(pcm)
        dst = os.path.expanduser('~/Downloads/%s-ai-preview.m4a' % vid)
        subprocess.run(['afconvert', '-f', 'm4af', '-d', 'aac', '-b', '128000', wp, dst], check=True)
        subprocess.run(['rm', '-rf', tmp]); print('preview:', dst)


if __name__ == '__main__':
    main()
