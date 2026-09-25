"""Upload recorded lessons to Bunny Stream and connect each one to its lesson on the website.

The Teacher Studio saves every take as  <videoId>-<YYYY-MM-DDTHH-MM-SS-mmmZ>.webm  (inside Subject/Topic folders).
This script finds the newest take of every video, uploads the ones that are new or changed (with the chapter list the
studio saved beside each take, so students can jump to any slide), and records them in
content/full-course/video-manifest.json — the website shows a lesson's video as soon as it's in the manifest.

    python3 studio-build/upload_videos.py "/path/to/Course Recordings"            # upload
    python3 studio-build/upload_videos.py "/path/to/Course Recordings" --dry-run  # just show what would happen
    python3 studio-build/upload_videos.py "/path/to/Course Recordings" --replace  # also delete the old version on Bunny

Needs BUNNY_LIBRARY_ID and BUNNY_API_KEY (in .env.local or the environment).
"""
import glob, json, os, re, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, 'content', 'full-course', 'video-manifest.json')
NAME = re.compile(r'^(?P<id>.+)-(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z)\.(?:webm|mp4|mov)$')

def env():
    p = os.path.join(ROOT, '.env.local')
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            m = re.match(r'\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$', line)
            if m and m.group(1) not in os.environ: os.environ[m.group(1)] = m.group(2).strip('"\'')

def course_video_ids():
    ids = {}
    for f in glob.glob(os.path.join(ROOT, 'content', 'full-course', 'topics', 't*.json')):
        t = json.load(open(f, encoding='utf-8'))
        for s in t['sections']:
            for st in s['steps']:
                if st['kind'] == 'video': ids[st['id']] = '%s · %s' % (t['title'], st['title'])
    return ids

def api(method, path, key, data=None, body_file=None, size=None):
    url = 'https://video.bunnycdn.com' + path
    headers = {'AccessKey': key, 'accept': 'application/json'}
    if data is not None:
        payload = json.dumps(data).encode(); headers['content-type'] = 'application/json'
    elif body_file is not None:
        payload = body_file; headers['content-type'] = 'application/octet-stream'; headers['content-length'] = str(size)
    else:
        payload = None
    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=3600) as r:
        txt = r.read().decode() or '{}'
        return json.loads(txt)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry, replace = '--dry-run' in sys.argv, '--replace' in sys.argv
    if not args: print(__doc__); sys.exit(1)
    folder = os.path.expanduser(args[0])
    env()
    lib, key = os.environ.get('BUNNY_LIBRARY_ID'), os.environ.get('BUNNY_API_KEY')
    if not dry and (not lib or not key): sys.exit('Set BUNNY_LIBRARY_ID and BUNNY_API_KEY in .env.local first (or use --dry-run).')

    known = course_video_ids()
    latest, unknown = {}, []
    for path in glob.glob(os.path.join(folder, '**', '*.*'), recursive=True):
        m = NAME.match(os.path.basename(path))
        if not m: continue
        vid, ts = m.group('id'), m.group('ts')
        if vid not in known: unknown.append(os.path.basename(path)); continue
        if vid not in latest or ts > latest[vid][0]: latest[vid] = (ts, path)

    man = json.load(open(MANIFEST, encoding='utf-8')) if os.path.exists(MANIFEST) else {}
    todo = [(vid, p) for vid, (ts, p) in sorted(latest.items()) if man.get(vid, {}).get('file') != os.path.basename(p)]
    print('Found %d recorded videos (%d already online, %d to upload).' % (len(latest), len(latest) - len(todo), len(todo)))
    if unknown: print('Skipped %d files whose name doesn\'t match a lesson, e.g. %s' % (len(unknown), unknown[:3]))

    for i, (vid, path) in enumerate(todo, 1):
        size = os.path.getsize(path)
        print('[%d/%d] %s  (%.0f MB)  %s' % (i, len(todo), vid, size / 1e6, known[vid]))
        if dry: continue
        try:
            guid = api('POST', '/library/%s/videos' % lib, key, data={'title': '%s — %s' % (vid, known[vid])})['guid']
            with open(path, 'rb') as fh:
                api('PUT', '/library/%s/videos/%s' % (lib, guid), key, body_file=fh, size=size)
        except urllib.error.HTTPError as e:
            print('   failed:', e.code, e.read().decode()[:200]); continue
        chap = re.sub(r'\.(webm|mp4|mov)$', '.chapters.json', path)
        if os.path.exists(chap):
            try:
                cs = json.load(open(chap, encoding='utf-8'))['chapters']
                chapters = [{'title': c['title'][:80], 'start': int(c['start']), 'end': int(cs[k + 1]['start']) if k + 1 < len(cs) else int(c['start']) + 7200}
                            for k, c in enumerate(cs)]
                api('POST', '/library/%s/videos/%s' % (lib, guid), key, data={'chapters': chapters})
                print('   + %d chapters' % len(chapters))
            except Exception as e:  # chapters are a bonus — never fail the upload for them
                print('   (chapters not added: %s)' % e)
        old = man.get(vid, {}).get('videoGuid')
        man[vid] = {'provider': 'bunny', 'libraryId': lib, 'videoGuid': guid, 'file': os.path.basename(path),
                    'uploaded': time.strftime('%Y-%m-%d %H:%M')}
        json.dump(man, open(MANIFEST, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)  # save after every video
        if replace and old:
            try: api('DELETE', '/library/%s/videos/%s' % (lib, old), key)
            except urllib.error.HTTPError: print('   (could not delete the old version %s)' % old)
    if not dry and todo: print('Done. The website shows these videos now (redeploy the site if it is online).')

if __name__ == '__main__':
    main()
