"""AI narration in the teacher's cloned voice (ElevenLabs).

    python3 studio-build/ai_narrate.py vr50-a-score            # generate audio for ai_scripts/vr50-a-score.json
    python3 studio-build/ai_narrate.py vr50-a-score --preview  # ... and write one listening file to ~/Downloads

ai_scripts/<videoId>.json = {"voice": {...}, "slides": [[line, line, ...], ...]} — one entry per spoken line of the
video, in order (the studio's AI-narrate mode plays line i where the video has spoken line i).
Audio goes to ~/Documents/Course.recordings/_ai_audio/<videoId>/ (one mp3 per line + manifest.json). A line is only
re-generated when its text or the voice settings change, so edits cost credits only for the changed lines.
Needs ELEVENLABS_API_KEY in ~/psychometry-course/.env.local.
"""
import hashlib, json, os, re, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.expanduser('~/Documents/Course.recordings/_ai_audio')


def key():
    for line in open(os.path.join(ROOT, '.env.local'), encoding='utf-8'):
        m = re.match(r'\s*ELEVENLABS_API_KEY\s*=\s*(\S+)', line)
        if m: return m.group(1).strip('"\'')
    sys.exit('ELEVENLABS_API_KEY missing in .env.local')


def tts(k, voice, text, prev, nxt):
    body = {'text': text, 'model_id': voice['model_id'],
            'voice_settings': {'stability': voice['stability'], 'similarity_boost': voice['similarity_boost']}}
    if prev: body['previous_text'] = prev
    if nxt: body['next_text'] = nxt
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/%s?output_format=mp3_44100_128' % voice['voice_id'],
                                 data=json.dumps(body).encode(), headers={'xi-api-key': k, 'Content-Type': 'application/json', 'accept': 'audio/mpeg'})
    return urllib.request.urlopen(req, timeout=180).read()


def duration(path):
    out = subprocess.run(['afinfo', path], capture_output=True, text=True).stdout
    m = re.search(r'estimated duration: ([\d.]+)', out)
    return float(m.group(1)) if m else 0.0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args: sys.exit(__doc__)
    vid = args[0]
    spec = json.load(open(os.path.join(HERE, 'ai_scripts', vid + '.json'), encoding='utf-8'))
    # one shared voice for all videos (ai_scripts/_voice.json); a script file may override it with its own 'voice'
    voice = spec.get('voice') or json.load(open(os.path.join(HERE, 'ai_scripts', '_voice.json'), encoding='utf-8'))
    voice = {k: voice[k] for k in ('voice_id', 'model_id', 'stability', 'similarity_boost')}
    lines = [l for s in spec['slides'] for l in s]
    d = os.path.join(OUT, vid); os.makedirs(d, exist_ok=True)
    mpath = os.path.join(d, 'manifest.json')
    old = json.load(open(mpath)) if os.path.exists(mpath) else {'lines': []}
    oldh = {x['file']: x['hash'] for x in old['lines']}
    k = key(); man = []; chars = 0
    for i, text in enumerate(lines):
        f = 'line-%03d.mp3' % (i + 1)
        h = hashlib.sha1(json.dumps([text, voice], sort_keys=True).encode()).hexdigest()[:16]
        p = os.path.join(d, f)
        if oldh.get(f) != h or not os.path.exists(p):
            open(p, 'wb').write(tts(k, voice, text, lines[i - 1] if i else '', lines[i + 1] if i + 1 < len(lines) else ''))
            chars += len(text); print('  generated', f, '(%d chars)' % len(text))
        man.append({'file': f, 'text': text, 'hash': h, 'seconds': round(duration(p), 2)})
    json.dump({'videoId': vid, 'voice': voice, 'lines': man}, open(mpath, 'w'), indent=1, ensure_ascii=False)
    print('%s: %d lines, %.0f s of audio, %d characters generated now' % (vid, len(man), sum(x['seconds'] for x in man), chars))
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
