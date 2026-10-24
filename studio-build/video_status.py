"""Video status tracker: which recorded videos still need the teacher, which go to Codex, which are done.

    python3 video_status.py                         # -> ~/Downloads/Video-Status.html (and prints the counts)
    python3 video_status.py --list send             # plain list of the "Send to Codex" ids (also: record, reread, done, check)
    python3 video_status.py --rendered <id> <path>  # Codex: call after each finished render (stores the fingerprint now)
    python3 video_status.py --rendered-from-index "<.../Video index.json>"   # bulk: register Codex's index (checked)
    python3 video_status.py --reseed                # forget the guessed (seeded) ledger entries and guess again

Every video of the Reading Studio list (same topics, same order, summaries left out) gets ONE status:
  Record                 not recorded yet
  Re-read needed (you)   recorded, but paragraphs are flagged (reading_studio.scan_recorded: changed + video corrections)
  Send to Codex          recorded, nothing to re-read, and never rendered, or its content changed since the last render
  Done                   rendered, and nothing changed since
  Check                  unknown (a render exists but we cannot tell what it was made from) - never guessed as Done

CONTENT FINGERPRINT of a video = sha256 of three parts:
  spoken  - the paragraphs she reads (reading_studio.paragraphs(ai_scripts/<id>.json))
  visual  - the video's entry in the built studio data (window.COURSE.videos[id] of the hybrid build: beats + title)
  takes   - name + mtime of her newest full take and of the patch takes made after it
The ledger render_ledger.json keeps per video: {state, fingerprint, parts, render_path, rendered_at, source, note}.
  source "codex" = registered with --rendered (trusted); "seed" = guessed from Codex's existing renders (below).

SEEDING (existing renders, found in Codex's outputs: "All course videos - organized/Video index.json", the batch
folders outputs/<batch>/videos/*.mp4 and work/<batch>/finished.json; the inputs of a batch from work/<batch>/inputs.json):
  made-from time = the batch's started_at (else the render file's time). A video is guessed Done only if ALL hold:
    - no take newer than that (and not listed among the batch inputs),
    - the script (ai_scripts/<id>.json slides) is the same as the version Codex used (its sha256 in inputs.json, else
      the git version at that time),
    - the video's own block video('<id>', ...) in math_patches/_ai_vis_t<topic>.py did not change after that (git),
    - the render is in Codex's "01 - Ready to use" (or listed in a finished.json).
  Something changed -> Send to Codex (with the reason). Older export / waiting for corrections / not indexed / no git
  history -> Check. A newer render found later in the outputs is seeded again automatically.
  Not seen by the seeding: changes in shared helper code (outside the video's own block, e.g. _ai_visual.py).
Low RAM: the 30 MB hybrid is read once and its videos decoded one at a time.
"""
import argparse, datetime as dt, glob, hashlib, html, importlib.util, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DOWNLOADS = os.path.expanduser('~/Downloads')
HYBRID = os.path.join(DOWNLOADS, 'Psychometric-Teacher-Studio-v19-hybrid.html')
READING_PAGE = os.path.join(DOWNLOADS, 'Reading-Studio.html')
OUT = os.path.join(DOWNLOADS, 'Video-Status.html')
LEDGER = os.path.join(HERE, 'render_ledger.json')
CODEX = os.path.expanduser('~/Documents/Codex/2026-10-11/https-github-com-nitzanslasky-source-psychometry')
OUTPUTS = os.path.join(CODEX, 'outputs')
WORK = os.path.join(CODEX, 'work')
ORG_INDEX = os.path.join(OUTPUTS, 'All course videos - organized', 'Video index.json')
DEFAULT_TOPICS = (13, 14, 15, 16, 17, 18, 19, 20, 30, 31, 32, 33, 51)   # if Reading-Studio.html cannot be read
SKIP_OUTPUT_DIRS = {'All course videos - organized', 'Course-video-library'}   # covered by the organized index
PREVIEW_DIRS = re.compile(r'reread-previews|pilot', re.I)                       # tests / previews, not final renders

STATUSES = [('record', 'Record'), ('reread', 'Re-read needed (you)'), ('send', 'Send to Codex'),
            ('done', 'Done'), ('check', 'Check')]
LABEL = dict(STATUSES)

# 2026-10-22 (Nitzan's workflow: Claude prepares -> Codex reviews and fixes -> READY TO RECORD -> she records -> Codex
# produces). An unrecorded lesson ('record') is either READY (reviewed, frozen) or HELD (in review / waiting, with why).
# The gate lives in review_gate.json: {id: {"state": "ready"|"held", "why": ..., "by": ..., "since": ...}}. A lesson with
# no entry counts as HELD ("not reviewed yet"). Set it with --ready ID [ID ...] / --hold ID [ID ...] --why "..." --by NAME.
GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review_gate.json')

def load_gate():
    try: return json.load(open(GATE))
    except Exception: return {}

def save_gate(G):
    json.dump(dict(sorted(G.items())), open(GATE, 'w'), ensure_ascii=False, indent=1)

# 2026-10-24 (Nitzan: "cut off videos that can be pushed off" — scripts still written and reviewed, recorded after launch).
# deferred.json: {id: {"why": ..., "by": ..., "since": ...}}. Independent of the Ready/Held review gate.
DEFER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deferred.json')

def load_defer():
    try: return json.load(open(DEFER))
    except Exception: return {}

def save_defer(F):
    json.dump(dict(sorted(F.items())), open(DEFER, 'w'), ensure_ascii=False, indent=1)

_s = importlib.util.spec_from_file_location('reading_studio', os.path.join(HERE, 'reading_studio.py'))
RS = importlib.util.module_from_spec(_s); _s.loader.exec_module(RS)


# ----------------------------------------------------------------------------------------------------------- utils
def sha(x):
    if not isinstance(x, (bytes, str)):
        x = json.dumps(x, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(x.encode('utf-8') if isinstance(x, str) else x).hexdigest()


def day(ts):
    """'14 Oct' (local time) from a unix time"""
    d = dt.datetime.fromtimestamp(ts)
    return '%d %s' % (d.day, d.strftime('%b'))


def when(ts):
    d = dt.datetime.fromtimestamp(ts)
    return '%d %s %s' % (d.day, d.strftime('%b'), d.strftime('%H:%M'))


def iso(ts):
    return dt.datetime.fromtimestamp(ts).astimezone().isoformat(timespec='seconds')


def from_iso(s):
    try:
        d = dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
        if d.tzinfo is None:
            d = d.astimezone()
        return d.timestamp()
    except Exception:
        return None


def load_json(p, default=None):
    try:
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default


# ------------------------------------------------------------------------------------------------- the video list
def reading_topics():
    """the topics of the Reading Studio page (its groups), else DEFAULT_TOPICS"""
    try:
        with open(READING_PAGE, encoding='utf-8') as f:
            head = f.read(200000)
        m = re.search(r'"groups":\s*(\[.*?\]),\s*"videos"', head, re.S)
        ts = [g['topic'] for g in json.loads(m.group(1)) if g.get('topic') is not None]
        if ts:
            return ts
    except Exception:
        pass
    return list(DEFAULT_TOPICS)


def video_list():
    """[{id, title, topic, topicTitle}] in Reading Studio order (same rules as reading_studio.build)"""
    out = []
    for t in reading_topics():
        r = RS.from_review(t) or RS.from_course(t)
        ttitle, vids = r
        for v in vids:
            if re.fullmatch(r'r26-t\d+-summary(-\d+)?', v['id']):
                continue
            if not os.path.exists(os.path.join(RS.SCRIPTS, v['id'] + '.json')):
                continue
            out.append(dict(id=v['id'], title=v['title'], topic=t, topicTitle=ttitle))
    return out


def hybrid_videos(ids, path=HYBRID):
    """{id: {visual, num, title, topic}} from window.COURSE.videos of the hybrid build, one video decoded at a time"""
    res = {}
    if not os.path.exists(path):
        return res
    with open(path, 'rb') as f:
        b = f.read()
    i = b.find(b'window.COURSE=')
    m = re.compile(rb'"videos":\s*\{\s*"').search(b, i if i >= 0 else 0)
    if not m:
        return res
    s = b[b.index(b'{', m.start()) + 1:].decode('utf-8', 'replace')
    del b
    dec = json.JSONDecoder(); p = 0; n = len(s)
    while p < n:
        while p < n and s[p] in ' \n\r\t,':
            p += 1
        if p >= n or s[p] == '}':
            break
        k, p = dec.raw_decode(s, p)
        while s[p] in ' \n\r\t:':
            p += 1
        v, p = dec.raw_decode(s, p)
        if k in ids and isinstance(v, dict):
            hy = v.get('hybrid') or {}
            res[k] = dict(visual=sha(dict(title=v.get('title'), beats=v.get('beats'))), num=hy.get('num'),
                          title=v.get('title'), topic=v.get('topic'))
        del v
    return res


# ------------------------------------------------------------------------------------------------------- her takes
def takes_info(vid):
    """(newest full take name, [(name, mtime)] of it + the patches after it, newest take mtime) or None"""
    d = os.path.join(RS.READING_ROOT, vid)
    if not os.path.isdir(d):
        return None
    fulls, patches = RS.take_files(os.listdir(d))
    if not fulls:
        return None
    last = fulls[-1]
    used = [last] + [f for f in patches if RS.stamp(f) > RS.stamp(last)]
    items = []
    for f in used:
        try:
            items.append((f, int(os.path.getmtime(os.path.join(d, f)))))
        except OSError:
            pass
    return dict(full=last, items=items, newest=max((t for _, t in items), default=0), dir=d)


# ------------------------------------------------------------------------------------------------- fingerprint
def fingerprint_parts(vid, hyb, tk):
    try:
        spoken = sha(RS.paragraphs(vid))
    except Exception:
        spoken = None
    return dict(spoken=spoken, visual=(hyb.get(vid) or {}).get('visual'), takes=sha(tk['items']) if tk else None)


def fingerprint(parts):
    return sha([parts.get('spoken'), parts.get('visual'), parts.get('takes')])


# ------------------------------------------------------------------------------------------------------------ git
_GIT = {}


def git(*a):
    key = a
    if key not in _GIT:
        try:
            _GIT[key] = subprocess.run(('git', '-C', REPO) + a, capture_output=True, timeout=60).stdout
        except Exception:
            _GIT[key] = None
    return _GIT[key]


def revisions(rel):
    """[(commit, unix time)] of a repo file, oldest first"""
    out = git('log', '--format=%H %ct', '--', rel)
    if out is None:
        return None
    revs = [(h, int(t)) for h, t in (l.split() for l in out.decode().splitlines() if l.strip())]
    return revs[::-1]


def at_rev(rev, rel):
    return git('show', '%s:%s' % (rev, rel))


def change_after(rel, made_from, extract, codex_sha=None):
    """(changed?, unix time of the change, note). extract(bytes) -> comparable value of the part we care about.
    The base = the version Codex used: the git version whose sha256 = codex_sha, else the last commit before made_from."""
    path = os.path.join(REPO, rel)
    try:
        with open(path, 'rb') as f:
            cur_bytes = f.read()
    except OSError:
        return None, None, 'file missing'
    if codex_sha and sha(cur_bytes) == codex_sha:
        return False, None, ''
    revs = revisions(rel)
    if revs is None:
        return None, None, 'no git'
    base = None
    if codex_sha:
        for i, (h, t) in enumerate(revs):
            c = at_rev(h, rel)
            if c is not None and sha(c) == codex_sha:
                base = i
    if base is None:
        before = [i for i, (h, t) in enumerate(revs) if t <= made_from]
        if not before:
            return None, None, 'no saved version from before the render'
        base = before[-1]
    try:
        base_val = extract(at_rev(revs[base][0], rel))
        cur_val = extract(cur_bytes)
    except Exception:
        return None, None, 'could not read it'
    if base_val == cur_val:
        return False, None, ''
    for h, t in revs[base + 1:]:
        try:
            if extract(at_rev(h, rel)) != base_val:
                return True, t, ''
        except Exception:
            continue
    return True, os.path.getmtime(path), ''        # not committed yet: the file's own time


def script_slides(b):
    return json.dumps(json.loads(b.decode('utf-8'))['slides'], sort_keys=True, ensure_ascii=False)


def spoken_only(b):
    d = json.loads(b.decode('utf-8'))
    return [RS.plain(it['say'] if isinstance(it, dict) else it) for sl in d['slides']
            for it in (sl if isinstance(sl, list) else [sl])]


def spec_block(vid):
    """extract(bytes) -> the normalized text of video('<vid>', ...) in a spec file (None if absent)"""
    start = re.compile(r"^video\(\s*['\"]%s['\"]" % re.escape(vid))
    end = re.compile(r'^(video\(|def |class |if |for |[A-Za-z_][\w.]*\s*=)')

    def ex(b):
        lines = b.decode('utf-8', 'replace').splitlines()
        on = False; out = []
        for l in lines:
            if on and end.match(l):
                break
            if start.match(l):
                on = True
            if on and l.strip():
                out.append(l.strip())
        return '\n'.join(out) or None
    return ex


def spec_for(vid, topic):
    """(repo-relative spec file, video id whose block holds this video) or (None, None)"""
    rel = 'studio-build/math_patches/_ai_vis_t%s.py' % topic
    p = os.path.join(REPO, rel)
    if not os.path.exists(p):
        return None, None
    with open(p, encoding='utf-8', errors='replace') as f:
        s = f.read()
    for cand in (vid, re.sub(r'-\d+$', '', vid)):       # camera parts 'x-2' are cut from the lesson 'x'
        if re.search(r"^video\(\s*['\"]%s['\"]" % re.escape(cand), s, re.M):
            return rel, cand
    return None, None


# ------------------------------------------------------------------------------------------------ Codex's renders
def batch_inputs():
    """{batch name: {made_from, hashes, ids}} from work/<batch>/inputs.json"""
    res = {}
    for p in glob.glob(os.path.join(WORK, '*', 'inputs.json')):
        d = load_json(p, {}) or {}
        name = os.path.basename(os.path.dirname(p))
        t = from_iso(d['started_at']) if d.get('started_at') else os.path.getmtime(p)
        ids = set(d.get('new_ids') or []) | set(d.get('visual_only_ids') or [])
        res[name] = dict(made_from=t, hashes=d.get('original_hashes') or {}, ids=ids,
                         finished=os.path.isdir(os.path.join(OUTPUTS, name)))
    return res


def finished_files():
    out = {}
    for p in glob.glob(os.path.join(WORK, '*', 'finished.json')):
        for v in (load_json(p, {}) or {}).get('videos', []):
            if v.get('file') and v.get('id'):
                out[os.path.realpath(v['file'])] = v['id']
    return out


def id_from_name(fn, ids):
    base = os.path.splitext(fn)[0]
    cands = []
    m = re.match(r'^\d+\s+(.+?)(?:\s+-\s+.*)?$', base)
    if m:
        cands.append(m.group(1).strip())
    cands += [re.sub(r'-codex$', '', base), base.split(' - ')[0].strip()]
    for c in cands:
        for x in (c, 'solve-' + c):
            if x in ids:
                return x
    return None


def find_renders(ids):
    """{id: [render]} render = {path, time, kind, batch}; kind ready / waiting / earlier / archive / finished / batch / preview"""
    batches = batch_inputs()
    fin = finished_files()
    seen = set(); res = {}

    def batch_of(path):
        rel = os.path.relpath(path, OUTPUTS)
        b = rel.split(os.sep)[0]
        return b if b in batches else None

    def add(vid, path, kind, batch):
        try:
            t = os.path.getmtime(path)
        except OSError:
            return
        res.setdefault(vid, []).append(dict(path=path, time=t, kind=kind, batch=batch))

    idx = load_json(ORG_INDEX, {}) or {}
    kinds = {'01': 'ready', '02': 'waiting', '03': 'earlier', '04': 'archive'}
    for e in idx.get('files', []):
        vid = e.get('id')
        srcs = [p for p in e.get('source_paths') or [] if os.path.exists(p)]
        for p in srcs + [e.get('file') or '']:
            seen.add(os.path.realpath(p))
        if vid not in ids:
            continue
        kind = kinds.get((e.get('status') or '')[:2], 'archive')
        if kind != 'archive' and any(PREVIEW_DIRS.search(p) for p in srcs):
            kind = 'archive'
        batch = next((batch_of(p) for p in srcs if batch_of(p)), None)
        path = min(srcs, key=os.path.getmtime) if srcs else e.get('file')     # the original render file
        add(vid, path, kind, batch)
    for d in sorted(os.listdir(OUTPUTS)) if os.path.isdir(OUTPUTS) else []:
        if d in SKIP_OUTPUT_DIRS or not os.path.isdir(os.path.join(OUTPUTS, d)):
            continue
        for p in glob.glob(os.path.join(OUTPUTS, d, '*.mp4')) + glob.glob(os.path.join(OUTPUTS, d, 'videos', '*.mp4')):
            rp = os.path.realpath(p)
            if rp in seen:
                continue
            vid = fin.get(rp) or id_from_name(os.path.basename(p), ids)
            if vid not in ids:
                continue
            size = os.path.getsize(p)          # the same file already indexed under another path (a copy)
            if any(os.path.exists(x['path']) and os.path.getsize(x['path']) == size for x in res.get(vid, [])):
                continue
            kind = 'preview' if PREVIEW_DIRS.search(d) else ('finished' if rp in fin else 'batch')
            add(vid, p, kind, d if d in batches else None)
    return res, batches, idx


FINAL_KINDS = ('ready', 'finished', 'waiting', 'earlier', 'batch')


def seed(v, renders, batches, tk):
    """guess the ledger entry of a video from Codex's existing renders: (state, render, made_from, notes)"""
    rs = [r for r in renders if r['kind'] in FINAL_KINDS]
    if not rs:
        return None
    r = max(rs, key=lambda r: r['time'])
    b = batches.get(r['batch']) if r['batch'] else None
    made_from = b['made_from'] if b else r['time']
    hashes = b['hashes'] if b else {}
    reasons, unknown = [], []
    # her audio
    if tk:
        used = {os.path.basename(p) for p in hashes if '/_reading/%s/' % v['id'] in p}
        newer = [(f, t) for f, t in tk['items'] if t > made_from and f not in used]
        if newer:
            f, t = max(newer, key=lambda x: x[1])
            reasons.append('new %s take %s (after the render)' % ('patch' if '-patch-' in f else 'full', day(t)))
    # the script
    rel = 'studio-build/ai_scripts/%s.json' % v['id']
    csha = next((h for p, h in hashes.items() if p.endswith('/ai_scripts/%s.json' % v['id'])), None)
    ch, t, note = change_after(rel, made_from, script_slides, csha)
    if ch is None:
        unknown.append('script: ' + note)
    elif ch:
        ch2, t2, _ = change_after(rel, made_from, spoken_only, csha)
        reasons.append(('script changed %s after render' if ch2 else 'visual cues in the script changed %s after render')
                       % day(t2 if ch2 and t2 else t))
    # the visual plan (the video's own block in the topic spec)
    srel, block = spec_for(v['id'], v['topic'])
    if srel:
        ch, t, note = change_after(srel, made_from, spec_block(block))
        if ch is None:
            unknown.append('visual plan: ' + note)
        elif ch:
            reasons.append('visual plan changed %s after render' % day(t))
    if reasons:
        return 'send', r, made_from, reasons
    if unknown:
        return 'check', r, made_from, ['rendered %s, but cannot tell what from (%s)' % (day(r['time']), '; '.join(unknown))]
    if r['kind'] in ('ready', 'finished'):
        return 'done', r, made_from, ['rendered %s, nothing changed since' % day(r['time'])]
    why = {'waiting': "Codex filed this render under 'Waiting for corrections'",
           'earlier': "only an older export that Codex has not checked",
           'batch': 'a render not yet in Codex\'s index (Codex should run --rendered)'}[r['kind']]
    return 'check', r, made_from, ['rendered %s - %s' % (day(r['time']), why)]


# -------------------------------------------------------------------------------------------------------- ledger
def load_ledger():
    return load_json(LEDGER, {}) or {}


def save_ledger(L):
    tmp = LEDGER + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(dict(sorted(L.items())), f, indent=1, ensure_ascii=False)
    os.replace(tmp, LEDGER)


def entry(state, parts, path, rendered_at, source, note, made_from=None):
    e = dict(state=state, fingerprint=fingerprint(parts) if state == 'done' else None, parts=parts if state == 'done' else None,
             render_path=path, rendered_at=iso(rendered_at), source=source, note=note)
    if made_from:
        e['made_from'] = iso(made_from)
    return e


# ------------------------------------------------------------------------------------------------------ evaluate
def evaluate(reseed=False, save=True):
    global GATEMAP
    GATEMAP = load_gate()
    DEFMAP = load_defer()
    vids = video_list()
    ids = {v['id'] for v in vids}
    hyb = hybrid_videos(ids)
    for v in vids:
        v['paras'] = RS.paragraphs(v['id'])
    rec = RS.scan_recorded(vids)
    renders, batches, idx = find_renders(ids)
    holds = idx.get('held_for_reread_or_visuals') or {}
    L = load_ledger()
    if reseed:
        L = {k: e for k, e in L.items() if e.get('source') != 'seed'}
    changed_ledger = False
    rows = []
    for n, v in enumerate(vids, 1):
        vid = v['id']
        tk = takes_info(vid)
        parts = fingerprint_parts(vid, hyb, tk)
        h = hyb.get(vid) or {}
        rlist = renders.get(vid, [])
        finals = [r for r in rlist if r['kind'] in FINAL_KINDS]
        newest = max(finals, key=lambda r: r['time']) if finals else None
        e = L.get(vid)
        # seed (or re-seed when a newer render than the ledger's shows up in Codex's outputs)
        if newest and tk and (e is None or (from_iso(e.get('rendered_at') or '') or 0) < newest['time'] - 60):
            s = seed(v, rlist, batches, tk)
            if s:
                state, r, made_from, notes = s
                e = L[vid] = entry(state, parts, r['path'], r['time'], 'seed', '; '.join(notes), made_from)
                changed_ledger = True
        row = dict(n=n, num=h.get('num'), id=vid, title=v['title'], topic=v['topic'], topicTitle=v['topicTitle'])
        notes = []
        r = rec.get(vid)
        if not tk or not r:
            st = 'record'
            why = 'not recorded yet'
            if newest:
                why += ' (an older render exists, %s)' % day(newest['time'])
        elif r.get('changed'):
            st = 'reread'
            ps = [i + 1 for i in r['changed']]
            why = 'paragraph%s %s to re-read' % ('s' if len(ps) > 1 else '', ', '.join(map(str, ps)))
            row['paras'] = ps
        elif not e:
            st = 'send'
            arch = [x for x in rlist if x['kind'] not in FINAL_KINDS]
            why = 'recorded %s, never rendered' % day(tk['newest'])
            if arch:
                why += ' (only test / preview renders exist)'
        elif e['state'] == 'done':
            old = e.get('parts') or {}
            reasons = []
            if parts['takes'] != old.get('takes'):
                f, t = max(tk['items'], key=lambda x: x[1])
                reasons.append('new %s take %s' % ('patch' if '-patch-' in f else 'full', day(t)))
            if parts['spoken'] != old.get('spoken'):
                reasons.append('script changed %s after render' % day(os.path.getmtime(os.path.join(RS.SCRIPTS, vid + '.json'))))
            if parts['visual'] != old.get('visual'):
                reasons.append('visual plan changed %s after render' % day(os.path.getmtime(HYBRID)) if parts['visual']
                               else 'not in the studio build any more')
            if reasons:
                st, why = 'send', '; '.join(reasons)
            else:
                st, why = 'done', 'rendered %s, nothing changed since' % day(from_iso(e['rendered_at']) or 0)
        else:
            st, why = e['state'], e.get('note') or ''
        if e and e.get('render_path'):
            row['render'] = e['render_path']
        if not h:
            notes.append('not in the studio build (hybrid)')
        hold = holds.get(vid)
        if hold and st not in ('done', 'record') and 'needing reread' not in (hold.get('reason') or ''):
            notes.append('Codex note (14 Oct): ' + hold.get('reason', ''))
        for bname, b in batches.items():
            if vid in b['ids'] and not b['finished'] and b['made_from'] > (newest['time'] if newest else 0):
                notes.append('Codex started a new render on %s (%s), not finished yet' % (when(b['made_from']), bname))
        if st == 'record':
            g = GATEMAP.get(vid) or {'state': 'held', 'why': 'not reviewed yet'}
            row['gate'] = g['state']
            if g['state'] == 'ready':
                why = 'READY TO RECORD — reviewed and frozen' + (' (%s)' % g['why'] if g.get('why') else '')
            else:
                why = 'HELD — ' + (g.get('why') or 'in review')
            if vid in DEFMAP:
                row['deferred'] = True
                why = 'AFTER LAUNCH (deferred) — ' + (DEFMAP[vid].get('why') or '') + ' · review: ' + why
        row.update(status=st, label=(LABEL[st] if st != 'record' else ('After launch (deferred)' if row.get('deferred') else 'Ready to record' if row.get('gate') == 'ready' else 'Held (not ready)')), why=why, notes=notes)
        rows.append(row)
    if save and (changed_ledger or reseed):
        save_ledger(L)
    return rows


# ------------------------------------------------------------------------------------------------------- commands
def cmd_rendered(vid, path, rendered_at=None, quiet=False):
    vids = {v['id']: v for v in video_list()}
    if vid not in vids:
        sys.exit('unknown video id (not in the Reading Studio list): ' + vid)
    tk = takes_info(vid)
    if not tk:
        sys.exit('%s: no recording found in %s' % (vid, RS.READING_ROOT))
    path = os.path.abspath(os.path.expanduser(path))
    if not os.path.exists(path):
        sys.exit('render not found: ' + path)
    hyb = hybrid_videos({vid})
    parts = fingerprint_parts(vid, hyb, tk)
    t = rendered_at or os.path.getmtime(path)
    L = load_ledger()
    L[vid] = entry('done', parts, path, t, 'codex', 'registered by Codex %s' % when(dt.datetime.now().timestamp()))
    save_ledger(L)
    if not quiet:
        print('%s: Done (fingerprint %s)' % (vid, L[vid]['fingerprint'][:12]))
        if tk['newest'] > t + 60:
            print('  warning: her newest take (%s) is newer than this render file' % when(tk['newest']))


def cmd_from_index(path):
    """registers the "01 - Ready to use" renders of a Codex index that are newer than the ledger, after the same
    checks as the seeding (a render older than a change is NOT registered as Done)."""
    global ORG_INDEX
    ORG_INDEX = os.path.abspath(os.path.expanduser(path))
    if not os.path.exists(ORG_INDEX):
        sys.exit('not found: ' + ORG_INDEX)
    rows = evaluate()          # seeds every video whose newest render is newer than its ledger entry
    L = load_ledger()
    n = sum(1 for r in rows if (L.get(r['id']) or {}).get('source') == 'seed')
    print('index read: %s' % ORG_INDEX)
    print('ledger: %d entries (%d guessed from renders, %d registered by Codex)' %
          (len(L), n, sum(1 for e in L.values() if e.get('source') == 'codex')))
    return rows


# ---------------------------------------------------------------------------------------------------------- page
PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Video Status</title>
<link rel="icon" href="data:,">
<style>
:root{--bg:#f7f6f3;--panel:#fff;--ink:#1f2328;--muted:#6b7280;--faint:#9ca3af;--line:#e7e5e0;--soft:#f1efea;
--accent:#0f766e;--accent-soft:#e6f4f1;
--record:#6b7280;--record-soft:#eef0f2;--reread:#c2410c;--reread-soft:#fdf0e9;--send:#1d4ed8;--send-soft:#e8eefc;
--done:#15803d;--done-soft:#e8f5ec;--check:#a16207;--check-soft:#fdf6e7}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#17181a;--panel:#1f2023;--ink:#ececea;--muted:#a1a1aa;--faint:#71717a;--line:#2e2f33;--soft:#26272b;
--accent:#2dd4bf;--accent-soft:#12332f;--record:#a1a1aa;--record-soft:#2a2b2f;--reread:#fb923c;--reread-soft:#3a2416;--send:#93b4ff;--send-soft:#1c2740;
--done:#4ade80;--done-soft:#14321f;--check:#fbbf24;--check-soft:#3a2e12}}
:root[data-theme="dark"]{--bg:#17181a;--panel:#1f2023;--ink:#ececea;--muted:#a1a1aa;--faint:#71717a;--line:#2e2f33;--soft:#26272b;
--accent:#2dd4bf;--accent-soft:#12332f;--record:#a1a1aa;--record-soft:#2a2b2f;--reread:#fb923c;--reread-soft:#3a2416;--send:#93b4ff;--send-soft:#1c2740;
--done:#4ade80;--done-soft:#14321f;--check:#fbbf24;--check-soft:#3a2e12}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif}
button{font:inherit;color:inherit;cursor:pointer;border:1px solid var(--line);background:var(--panel);border-radius:9px;padding:7px 12px}
button:hover{border-color:var(--faint)}
button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.wrap{max-width:1180px;margin:0 auto;padding:18px 16px 60px}
header{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 16px;margin-bottom:6px}
h1{font-size:22px;margin:0}
.built{font:700 13px system-ui;background:#fef3c7;color:#78350f;border:1.5px solid #f59e0b;border-radius:10px;padding:4px 10px;margin-left:auto}
.lead{color:var(--muted);margin:4px 0 16px;max-width:820px}
.counts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:14px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px 14px;text-align:left;cursor:pointer}
.card b{display:block;font-size:26px;font-variant-numeric:tabular-nums;line-height:1.1}
.card span{font-size:13px;color:var(--muted)}
.card small{display:block;font-size:12px;color:var(--faint);margin-top:2px}
.card.on{outline:2px solid var(--accent);outline-offset:1px}
.card.record b{color:var(--record)}.card.reread b{color:var(--reread)}.card.send b{color:var(--send)}.card.done b{color:var(--done)}.card.check b{color:var(--check)}
.tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 12px}
.tools .f.on{background:var(--accent-soft);border-color:var(--accent);color:var(--accent);font-weight:600}
.tools .sp{flex:1}
#q{padding:7px 10px;border:1px solid var(--line);border-radius:9px;background:var(--panel);color:var(--ink);font:inherit;min-width:180px}
.copybox{display:none;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin-bottom:12px}
.copybox.show{display:block}
.copybox textarea{width:100%;min-height:90px;font:13px ui-monospace,Menlo,monospace;background:var(--soft);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px}
.topic{margin:18px 0 6px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.list{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}
.row{display:grid;grid-template-columns:52px minmax(0,1fr) 190px;gap:4px 14px;padding:10px 14px;border-top:1px solid var(--line);align-items:start}
.row:first-child{border-top:0}
.num{color:var(--faint);font-variant-numeric:tabular-nums;font-size:13px;padding-top:2px}
.t{font-size:14.5px}
.id{font:12px ui-monospace,Menlo,monospace;color:var(--faint)}
.why{grid-column:2/4;font-size:13.5px;color:var(--ink)}
.note{grid-column:2/4;font-size:12.5px;color:var(--muted)}
.pill{justify-self:end;border-radius:999px;padding:2px 10px;font-size:12.5px;font-weight:600;white-space:nowrap}
.pill.record{background:var(--record-soft);color:var(--record)}.pill.reread{background:var(--reread-soft);color:var(--reread)}
.pill.send{background:var(--send-soft);color:var(--send)}.pill.done{background:var(--done-soft);color:var(--done)}.pill.check{background:var(--check-soft);color:var(--check)}
.empty{padding:20px;color:var(--muted)}
.help{margin-top:26px;color:var(--muted);font-size:13.5px;max-width:860px}
.help b{color:var(--ink)}
.toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);background:var(--ink);color:var(--bg);padding:8px 14px;border-radius:9px;font-size:14px;opacity:0;transition:opacity .2s;pointer-events:none}
.toast.show{opacity:1}
@media (max-width:640px){.row{grid-template-columns:40px minmax(0,1fr)}.pill{grid-column:2;justify-self:start}.why,.note{grid-column:2}.built{margin-left:0}}
</style>
</head>
<body>
<div class="wrap">
<header><h1>Video Status</h1><span class="built">Built at __BUILT__</span></header>
<p class="lead">Every video of the Reading Studio list, in the same order. Each one has one status: who acts next, and why.
Rebuild this page with <code>python3 video_status.py</code> after recording or after a Codex render.</p>
<div class="counts" id="counts"></div>
<div class="tools" id="tools"></div>
<div class="copybox" id="copybox"><div style="margin-bottom:6px">Paste this to Codex:</div><textarea id="copytext" readonly></textarea></div>
<div id="out"></div>
<div class="help">
<p><b>Record</b>: not recorded yet. <b>Re-read needed (you)</b>: open the Reading Studio, the flagged paragraphs are pre-selected.
<b>Send to Codex</b>: ready for Codex to render (or render again); use the copy button. <b>Done</b>: Codex's render matches the current recording, script and visuals.
<b>Check</b>: a render exists, but we cannot tell what it was made from; ask Claude to look before sending it.</p>
<p>A video counts as changed after a render when her takes, its spoken script or its visual plan in the studio build differ from the moment Codex registered the render.</p>
</div>
</div>
<div class="toast" id="toast"></div>
<script>
const DATA=__DATA__;
const ST=[["all","All"],["record","Record"],["reread","Re-read needed (you)"],["send","Send to Codex"],["done","Done"],["check","Check"]];
const WHO={record:"you record",reread:"you re-read",send:"Codex renders",done:"nothing to do",check:"look first"};
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let filter="all",q="";
try{filter=localStorage.getItem("video-status-filter")||"all"}catch(e){}
const count=k=>DATA.rows.filter(r=>k==="all"||r.status===k).length;
function toast(t){const el=document.getElementById("toast");el.textContent=t;el.classList.add("show");setTimeout(()=>el.classList.remove("show"),1800)}
function setFilter(k){filter=k;try{localStorage.setItem("video-status-filter",k)}catch(e){}draw()}
function sendList(){return DATA.rows.filter(r=>r.status==="send").map(r=>r.id).join("\n")}
async function copySend(){
  const txt=sendList(),box=document.getElementById("copybox"),ta=document.getElementById("copytext");
  ta.value=txt;box.classList.add("show");
  if(!txt){toast("Nothing to send to Codex");return}
  try{await navigator.clipboard.writeText(txt);toast("Copied "+count("send")+" ids")}
  catch(e){ta.select();try{document.execCommand("copy");toast("Copied "+count("send")+" ids")}catch(e2){toast("Select the list below and copy it")}}
}
function draw(){
  document.getElementById("counts").innerHTML=ST.slice(1).map(([k,l])=>`<button class="card ${k}${filter===k?" on":""}" data-k="${k}"><b>${count(k)}</b><span>${l}</span><small>${WHO[k]}</small></button>`).join("");
  document.getElementById("tools").innerHTML=ST.map(([k,l])=>`<button class="f${filter===k?" on":""}" data-k="${k}">${l} (${count(k)})</button>`).join("")+
    `<span class="sp"></span><input id="q" type="search" placeholder="Search id or title" value="${esc(q)}"><button id="copy">Copy "Send to Codex" list</button>`;
  document.querySelectorAll("[data-k]").forEach(b=>b.onclick=()=>setFilter(b.dataset.k));
  document.getElementById("copy").onclick=copySend;
  const qi=document.getElementById("q");qi.oninput=()=>{q=qi.value;drawList()};
  drawList();
}
function drawList(){
  const ql=q.trim().toLowerCase();
  const rows=DATA.rows.filter(r=>(filter==="all"||r.status===filter)&&(!ql||(r.id+" "+r.title).toLowerCase().includes(ql)));
  let html="",cur=null,open=false;
  for(const r of rows){
    if(r.topic!==cur){if(open)html+="</div>";cur=r.topic;html+=`<div class="topic">Topic ${esc(r.topic)} · ${esc(r.topicTitle)}</div><div class="list">`;open=true}
    html+=`<div class="row"><div class="num">${esc(r.n)}</div><div><div class="t">${esc(r.title)}</div><div class="id">${esc(r.id)}</div></div><span class="pill ${r.status}">${esc(r.label)}</span>`+
      `<div class="why">${esc(r.why)}</div>`+(r.notes||[]).map(n=>`<div class="note">${esc(n)}</div>`).join("")+`</div>`;
  }
  if(open)html+="</div>";
  document.getElementById("out").innerHTML=html||'<div class="list"><div class="empty">No videos with this status.</div></div>';
}
draw();
</script>
</body>
</html>
"""


def write_page(rows, out=OUT):
    now = dt.datetime.now()
    data = dict(rows=rows, builtAt=now.astimezone().isoformat(timespec='seconds'))
    js = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    page = PAGE.replace('__DATA__', js).replace('__BUILT__', html.escape('%s %d %s, %s' % (
        now.strftime('%a'), now.day, now.strftime('%b'), now.strftime('%H:%M'))))
    tmp = out + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(page)
    os.replace(tmp, out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--list', choices=[k for k, _ in STATUSES], help='print the ids with this status, one per line')
    ap.add_argument('--rendered', nargs=2, metavar=('ID', 'PATH'), help='Codex: register a finished render')
    ap.add_argument('--rendered-from-index', metavar='VIDEO_INDEX_JSON', help='register the renders of a Codex index')
    ap.add_argument('--reseed', action='store_true', help='forget guessed ledger entries and guess them again')
    ap.add_argument('--ready', nargs='+', metavar='ID', help='mark unrecorded lessons READY TO RECORD (reviewed, frozen)')
    ap.add_argument('--hold', nargs='+', metavar='ID', help='mark unrecorded lessons HELD (use --why)')
    ap.add_argument('--why', default='', help='reason for --hold / note for --ready')
    ap.add_argument('--by', default='', help='who sets the gate (Claude / Codex)')
    ap.add_argument('--gate', choices=['ready', 'held', 'deferred'], help='with --list record: only ready / held (both without deferred) or only deferred lessons')
    ap.add_argument('--defer', nargs='+', metavar='ID', help='mark lessons AFTER LAUNCH (deferred; use --why)')
    ap.add_argument('--undefer', nargs='+', metavar='ID', help='bring deferred lessons back into the launch')
    ap.add_argument('-o', '--out', default=OUT)
    a = ap.parse_args()
    if a.ready or a.hold:
        G = load_gate(); now = dt.datetime.now().astimezone().isoformat(timespec='minutes')
        for vid in (a.ready or []): G[vid] = {'state': 'ready', 'why': a.why, 'by': a.by, 'since': now}
        for vid in (a.hold or []): G[vid] = {'state': 'held', 'why': a.why or 'in review', 'by': a.by, 'since': now}
        save_gate(G)
    if a.defer or a.undefer:
        F = load_defer(); now = dt.datetime.now().astimezone().isoformat(timespec='minutes')
        for vid in (a.defer or []): F[vid] = {'why': a.why, 'by': a.by, 'since': now}
        for vid in (a.undefer or []): F.pop(vid, None)
        save_defer(F)
    if a.rendered:
        cmd_rendered(*a.rendered)
        rows = evaluate()
    elif a.rendered_from_index:
        rows = cmd_from_index(a.rendered_from_index)
    else:
        rows = evaluate(reseed=a.reseed)
    if a.list:
        sel = lambda r: (not a.gate) or (r.get('deferred') if a.gate == 'deferred' else (not r.get('deferred') and r.get('gate') == a.gate))
        print('\n'.join(r['id'] for r in rows if r['status'] == a.list and sel(r)))
        return
    out = write_page(rows, a.out)
    c = {k: sum(1 for r in rows if r['status'] == k) for k, _ in STATUSES}
    print('%s  (%d videos)' % (out, len(rows)))
    print('  ' + ' · '.join('%s: %d' % (LABEL[k], c[k]) for k, _ in STATUSES))
    rec = [r for r in rows if r['status'] == 'record']
    print('  of Record: Ready to record %d · Held %d · After launch (deferred) %d' % (sum(1 for r in rec if r.get('gate') == 'ready' and not r.get('deferred')), sum(1 for r in rec if r.get('gate') != 'ready' and not r.get('deferred')), sum(1 for r in rec if r.get('deferred'))))


if __name__ == '__main__':
    main()
