"""AI narration in the teacher's cloned voice (ElevenLabs).

    python3 studio-build/ai_narrate.py vr50-a-score                 # per-line mode: one mp3 per line
    python3 studio-build/ai_narrate.py vr50-a-score --preview       # ... and write one listening file to ~/Downloads
    python3 studio-build/ai_narrate.py solve-geo33-g091 --continuous          # the WHOLE video in ONE request
    python3 studio-build/ai_narrate.py solve-geo33-g091 --continuous --remap  # re-time from the saved alignment (no credits)

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
               <break time="0.6s"/> (eleven_multilingual_v2 supports break tags; v3/v4 do not). Re-generated only
               when the text or the voice changes; --remap recomputes the timing from alignment.json for free.
Needs ELEVENLABS_API_KEY in ~/psychometry-course/.env.local.
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
    return {'text': text, 'model_id': voice['model_id'], 'voice_settings': vs}


def tts(k, voice, text, prev, nxt):
    body = _body(voice, text)
    if prev: body['previous_text'] = prev
    if nxt: body['next_text'] = nxt
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/%s?output_format=mp3_44100_128' % voice['voice_id'],
                                 data=json.dumps(body).encode(), headers={'xi-api-key': k, 'Content-Type': 'application/json', 'accept': 'audio/mpeg'})
    return urllib.request.urlopen(req, timeout=180).read()


def tts_timestamps(k, voice, text):
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/%s/with-timestamps?output_format=mp3_44100_128' % voice['voice_id'],
                                 data=json.dumps(_body(voice, text)).encode(), headers={'xi-api-key': k, 'Content-Type': 'application/json'})
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
    voice = {k: voice[k] for k in ('voice_id', 'model_id', 'stability', 'similarity_boost', 'speed') if k in voice}
    return spec, voice


# ---------------------------------------------------------------- continuous mode
def full_text(spec):
    """the text sent in one request + for every line (slide, char start, char end) in that text."""
    text, spans = '', []
    for si, sl in enumerate(spec['slides']):
        for li, l in enumerate(sl):
            if text: text += (' <break time="%.1fs"/> ' % SLIDE_BREAK) if li == 0 else ' '
            t = line_text(l).strip()
            spans.append((si, len(text), len(text) + len(t)))
            text += t
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


def remap(vid, spec, d, voice, h):
    text, spans = full_text(spec)
    al = json.load(open(os.path.join(d, 'alignment.json')))
    ct = char_times(text, al)
    lines, flat = [], [l for sl in spec['slides'] for l in sl]
    for (si, a, b), l in zip(spans, flat):
        t = line_text(l).strip()
        s0, e0 = _at(ct, a, b, 'start'), _at(ct, a, b, 'end')
        if s0 is None or e0 is None: sys.exit('alignment: no times for line %r' % t[:60])
        ats = []
        for ph in (l.get('at') or []) if isinstance(l, dict) else []:
            if ph is None: ats.append(None); continue
            sa, st_ = a, t                      # "<phrase" = a phrase near the end of the PREVIOUS spoken line
            if ph.startswith('<'):
                if not lines: sys.exit('%s: %r - no previous line' % (vid, ph))
                ph = ph[1:]; pi = len(lines) - 1; sa = spans[pi][1]; st_ = lines[pi]['text']
            k = st_.lower().find(ph.lower())
            if k < 0: sys.exit('%s: phrase %r not in line %r' % (vid, ph, st_[:70]))
            ats.append(round(_at(ct, sa + k, sa + k + len(ph), 'start'), 3))
        lines.append({'text': t, 'slide': si, 'start': round(s0, 3), 'end': round(e0, 3), 'at': ats})
    secs = duration(os.path.join(d, 'audio.mp3')) or (lines[-1]['end'] + 0.3)
    man = {'videoId': vid, 'mode': 'continuous', 'voice': voice, 'hash': h, 'file': 'audio.mp3', 'seconds': round(secs, 2), 'lines': lines}
    json.dump(man, open(os.path.join(d, 'manifest.json'), 'w'), indent=1, ensure_ascii=False)
    gaps = [round(y['start'] - x['end'], 2) for x, y in zip(lines, lines[1:])]
    print('%s: %d lines, %.1f s of audio (continuous); gaps between lines: %s' % (vid, len(lines), secs, gaps))
    return man


def continuous(vid, spec, voice):
    d = os.path.join(OUT, vid); os.makedirs(d, exist_ok=True)
    text, _ = full_text(spec)
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


# ---------------------------------------------------------------- per-line mode
def per_line(vid, spec, voice):
    lines = [line_text(l) for s in spec['slides'] for l in s]
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


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args: sys.exit(__doc__)
    vid = args[0]
    spec, voice = load(vid)
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
