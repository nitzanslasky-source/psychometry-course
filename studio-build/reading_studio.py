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
neighbouring paragraphs greyed as context. Change detection (generator and page, same rule): a current paragraph whose
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
    t = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'\1/\2', t)
    t = re.sub(r'\\ne(?![a-z])', '≠', t)
    t = re.sub(r'\s*\\cdot\s*', '·', t)
    for a, b in [('\\\\', '; '), (r'\cdot', '·'), (r'\left', ''), (r'\right', ''), (r'\leq', '≤'), (r'\geq', '≥'), (r'\le', '≤'), (r'\ge', '≥'),
                 (r'\neq', '≠'), (r'\sqrt', '√'), (r'\frac', ''), (r'\cdot', '·'), ('\\', '')]:
        t = t.replace(a, b)
    return re.sub(r'\s+', ' ', t).strip()


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
    return [i for i, t in enumerate(current) if norm(t) not in known]


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
    for g in groups:
        for v in g['videos']:
            sp = os.path.join(SCRIPTS, v['id'] + '.json')
            if not os.path.exists(sp):
                sys.exit('missing script: ' + sp)
            v['paras'] = paragraphs(v['id'])
            words = sum(len(p.split()) for sl in v['paras'] for p in sl)
            v['words'] = words
            if not v.get('minutes'):
                v['minutes'] = round(words / WPM, 1)
            if v['title'] == v['id']:   # no title known: the first sentence
                v['title'] = re.split(r'(?<=[.?!])\s', v['paras'][0][0])[0][:110]
            v['group'] = g['topic']
            allv.append(v)
    data = dict(groups=[dict(topic=g['topic'], title=g['title'], ids=[v['id'] for v in g['videos']]) for g in groups],
                videos=allv, recorded=scan_recorded(allv))
    js = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    label = ', '.join(('Topic %d' % g['topic']) + (' · ' + g['title'] if g['title'] else '') if g['topic'] else 'Videos'
                      for g in groups)
    page = PAGE.replace('__DATA__', js).replace('__LABEL__', html.escape(label))
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
@media (max-width:820px){.main{flex-direction:column}aside{width:auto;max-height:30vh;border-right:0;border-bottom:1px solid var(--line)}:root{--prompt:22px}.keys{display:none}}
</style>
</head>
<body>
<div class="top">
  <div class="brand">Reading Studio<small>__LABEL__</small></div>
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
    </div>
    <div class="head"><h1 id="vtitle"></h1>
      <div class="opts">
        <span class="mode" title="Full read = the whole script. Re-read = only the paragraphs you select (a patch take)."><button id="mFull" class="on">Full read</button><button id="mPatch">Re-read paragraphs</button></span>
        <label><input type="checkbox" id="auto" checked> Auto-scroll</label>
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
  return flat(BYID[id]).map((t,i)=>known.has(norm(t))?-1:i).filter(i=>i>=0)}
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
        '<span class="id">'+esc(id)+'</span><span class="st">'+(st?'<span class="pill yes">recorded ✓'+(st.seconds?' · '+fmt(st.seconds):'')+(st.takes>1?' · '+st.takes+' takes':'')+(st.patches?' · '+st.patches+' patch'+(st.patches>1?'es':''):'')+'</span>'+(st.changed&&st.changed.length?' <span class="pill chg">needs re-read: '+st.changed.length+' paragraph'+(st.changed.length>1?'s':'')+'</span>':''):'<span class="pill no">not recorded</span>')+'</span></div>'}}
  L.innerHTML=h;
  L.querySelectorAll('.vid').forEach(el=>el.onclick=()=>selectVideo(+el.dataset.i));
}
function selectVideo(i){
  if(S.rec){toast('Stop the recording first.');return}
  S.cur=Math.max(0,Math.min(V.length-1,i));S.para=0;LS.set('cur',V[S.cur].id);S.sel=new Set(changedList());
  renderList();renderParas();paintFolder();loadLatestTake();
  const el=$('#list .vid.cur');if(el)el.scrollIntoView({block:'nearest'});
}

/* ---------------- teleprompter ---------------- */
function renderParas(){
  const v=V[S.cur];let k=0;
  $('#vtitle').innerHTML=esc(v.title)+'<small>'+esc(v.id)+' · about '+v.minutes.toFixed(1)+' min · '+v.words+' words</small>';
  const ch=new Set(changedList());
  $('#paras').innerHTML=v.paras.map(sl=>'<div class="slide">'+sl.map(p=>{const kk=k++;return '<p class="p" data-k="'+kk+'">'+esc(p)+(ch.has(kk)?'<span class="chg">changed</span>':'')+'</p>'}).join('')+'</div>').join('');
  $('#paras').querySelectorAll('.p').forEach(el=>el.onclick=e=>{e.stopPropagation();const kk=+el.dataset.k;if(S.rec&&!S.rec.paused)nextPara();else if(S.mode==='patch'&&!S.rec){S.sel.has(kk)?S.sel.delete(kk):S.sel.add(kk);if(S.sel.has(kk))S.para=kk;else if(!S.sel.has(S.para))S.para=order()[0]??0;paintParas()}else setPara(kk,'jump')});
  $('#prompter').scrollTop=0;paintParas();
}
function changedList(){const st=S.status[V[S.cur].id];return st&&st.changed?st.changed.slice():[]}
function order(){const n=flat(V[S.cur]).length;return S.mode==='patch'?[...S.sel].sort((a,b)=>a-b):[...Array(n).keys()]}
function paintParas(){
  const patch=S.mode==='patch',patching=patch&&!!S.rec,sel=S.sel,ch=changedList();
  document.body.classList.toggle('patch',patch);$('#paras').classList.toggle('patching',patching);
  document.querySelectorAll('#paras .p').forEach(el=>{const k=+el.dataset.k;el.classList.toggle('cur',k===S.para&&(!patch||sel.has(k)));el.classList.toggle('done',!patch&&k<S.para);
    el.classList.toggle('sel',patch&&sel.has(k));el.classList.toggle('ctx',patching&&!sel.has(k)&&(sel.has(k-1)||sel.has(k+1)))});
  document.querySelectorAll('#paras .slide').forEach(sd=>sd.classList.toggle('empty',patching&&!sd.querySelector('.p.sel,.p.ctx')));
  if(patch){const nc=[...sel].filter(k=>ch.includes(k)).length;const o=order(),pos=o.indexOf(S.para)+1;$('#pNext').hidden=!patching||pos>=o.length;
  $('#pinfo').innerHTML=patching?(pos<o.length?'<b>Paragraph '+pos+' of '+o.length+'</b> — press <kbd>Space</kbd> (or Next ▸) for the next paragraph':'<b>Paragraph '+pos+' of '+o.length+'</b> — the last one. Press Stop &amp; save when you finish')+' <span style="color:var(--muted)">· greyed lines are context, do not read them</span>':
    'Re-read mode: click paragraphs to select them. <b>'+sel.size+' selected</b>'+(ch.length?' · '+ch.length+' changed since your last take'+(nc?' ('+nc+' selected)':''):' · no changed paragraphs');$('#pChanged').hidden=patching||!ch.length;$('#pClear').hidden=patching}
  if($('#auto').checked){const el=document.querySelector('#paras .p.cur');if(el){const pr=$('#prompter');const top=el.offsetTop-pr.offsetTop-pr.clientHeight*.3;pr.scrollTo({top:Math.max(0,top),behavior:'smooth'})}}
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
$('#auto').checked=LS.get('auto',true);$('#auto').onchange=()=>{LS.set('auto',$('#auto').checked);paintParas()};

/* ---------------- microphone: processing OFF, mono, 48 kHz ---------------- */
const MIC={stream:null,ctx:null,src:null,an:null,node:null,engine:null,settings:null,label:'',peakHold:0,peakT:0};
const WORKLET=`class Tap extends AudioWorkletProcessor{constructor(){super();this.on=false;this.buf=new Float32Array(4096);this.n=0;
 this.port.onmessage=e=>{const m=e.data;if(m==='start'){this.on=true}else if(m==='pause'){this.on=false;this.flush()}else if(m==='flush'){this.on=false;this.flush();this.port.postMessage('flushed')}}}
 flush(){if(this.n){this.port.postMessage(this.buf.slice(0,this.n));this.n=0}}
 process(inputs){const ch=inputs[0]&&inputs[0][0];if(this.on&&ch){let i=0;while(i<ch.length){const k=Math.min(ch.length-i,this.buf.length-this.n);this.buf.set(ch.subarray(i,i+k),this.n);this.n+=k;i+=k;if(this.n===this.buf.length){this.port.postMessage(this.buf.slice(0));this.n=0}}}return true}}
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
  try{let ok=false;for(const url of [URL.createObjectURL(new Blob([WORKLET],{type:'application/javascript'})),'data:application/javascript;base64,'+btoa(WORKLET)]){try{await MIC.ctx.audioWorklet.addModule(url);ok=true;break}catch(e){console.info('worklet module via '+url.slice(0,5)+' failed: '+e)}}if(!ok)throw new Error('no AudioWorklet module');
    MIC.node=new AudioWorkletNode(MIC.ctx,'rs-tap',{numberOfInputs:1,numberOfOutputs:1,outputChannelCount:[1]});MIC.engine='AudioWorklet';
    MIC.node.port.onmessage=e=>{if(e.data==='flushed'){MIC._flushed&&MIC._flushed()}else if(S.rec)S.rec.push(e.data)};
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
  if(patch)S.para=order()[0];   // a patch take always starts at the first selected paragraph
  S.rec={video:v.id,patch,sel:patch?order():null,started:new Date(),chunks:[],samples:0,paused:false,clipped:false,events:[],pauses:[],
    push(c){this.chunks.push(c);this.samples+=c.length}};
  S.rec.events.push({type:'start',para:S.para,t:0});
  MIC.ctl('start');setUI();paintParas();tick();toast((patch?'Recording a re-read of '+S.sel.size+' paragraph'+(S.sel.size>1?'s':'')+'. ':'Recording. ')+'Space = next paragraph, M = mistake.');
}
function togglePause(){const r=S.rec;if(!r)return;
  if(!r.paused){MIC.ctl('pause');r.paused=true;r.pauses.push({at:+recTime().toFixed(3)})}
  else{MIC.ctl('start');r.paused=false}
  setUI()}
function mistake(){const r=S.rec;if(!r||r.paused)return;const t=recTime();r.events.push({type:'mistake',para:S.para,t});
  const el=document.querySelector('#paras .p.cur');if(el){el.classList.remove('flash');void el.offsetWidth;el.classList.add('flash');let mk=el.querySelector('.mk');if(!mk){mk=document.createElement('span');mk.className='mk';el.appendChild(mk)}mk.dataset.n=(+(mk.dataset.n||0))+1;mk.textContent='✕ '+mk.dataset.n}
  toast('Mistake marked at '+fmt(t,true)+'. Repeat the sentence.',2200)}
async function stopRec(){
  const r=S.rec;if(!r||r.stopping)return;r.stopping=true;
  await new Promise(ok=>{MIC._flushed=ok;MIC.ctl('flush');setTimeout(ok,800)});MIC._flushed=null;
  S.rec=null;setUI();paintParas();
  if(!r.samples){toast('The recording was empty. Nothing saved.');return}
  const sr=MIC.ctx.sampleRate,dur=r.samples/sr,v=BYID[r.video];
  const name=r.video+(r.patch?'-patch-':'-')+r.started.toISOString().replace(/[:.]/g,'-')+'.wav';
  const wav=encodeWav(r.chunks,r.samples,sr);
  const ps=flat(v);const starts=[];for(const e of r.events)if(e.type!=='mistake')starts.push({para:e.para,t:+e.t.toFixed(3),how:e.type});
  const reached=new Set(starts.map(e=>e.para)),read=(r.patch?r.sel:ps.map((_,i)=>i)).filter(i=>reached.has(i)),unread=r.patch?r.sel.filter(i=>!reached.has(i)):[];
  const side={file:name,videoId:r.video,kind:r.patch?'patch':'full',recordedAt:r.started.toISOString(),duration:+dur.toFixed(3),sampleRate:sr,channels:1,bitsPerSample:16,format:'WAV PCM 16-bit mono',
    mic:{label:MIC.label,deviceId:(MIC.settings||{}).deviceId||'',settings:MIC.settings,engine:MIC.engine},
    constraints:{echoCancellation:false,noiseSuppression:false,autoGainControl:false},clipped:!!r.clipped,
    paragraphStarts:starts,mistakes:r.events.filter(e=>e.type==='mistake').map(e=>({t:+e.t.toFixed(3),para:e.para,text:ps[e.para]})),
    pauses:r.pauses,paragraphs:(r.patch?r.sel:ps.map((_,i)=>i)).map(i=>({i,text:ps[i]})),read,scriptParagraphs:ps.length,
    note:(r.patch?'PATCH take: only the paragraphs listed in "paragraphs" (i = index in the current script) were re-read; they replace those paragraphs of the full take. ':'')+'Times are seconds in this WAV (pauses removed). read: the paragraph indexes she reached (only these count as re-read). paragraphStarts: when each paragraph was reached (Space/click; back/jump also listed). mistakes: "I stumbled; I repeat this sentence" - cut the take of that sentence before the mark.',
    tool:'reading_studio.py v1'};
  const json=new Blob([JSON.stringify(side,null,1)],{type:'application/json'});
  setLastTake(wav,name);
  const where=await saveFiles(r.video,[[name,wav],[name.replace(/\.wav$/,'.json'),json]]);
  const st=S.status[r.video]||{takes:0,patches:0,changed:null};
  if(r.patch){const done=new Set(read.map(i=>norm(ps[i])));S.status[r.video]={...st,patches:(st.patches||0)+1,changed:st.changed?st.changed.filter(i=>!done.has(norm(ps[i]))):st.changed}}
  else S.status[r.video]={takes:(st.takes||0)+1,latest:name,seconds:dur,patches:0,changed:[]};
  if(where)await scanVideo(r.video);renderList();
  if(V[S.cur].id===r.video){const keep=S.para;S.sel=new Set([...S.sel].filter(i=>changedList().includes(i)));renderParas();S.para=keep;paintParas()}
  $('#state').textContent=where?'Saved '+fmt(dur)+' → '+where:'Downloaded '+name+' (and its .json). Move both to Course.recordings/_reading/'+r.video+'/';
  toast(where?'Saved ('+fmt(dur)+').':'Downloaded to your Downloads folder.',4000);
  if(unread.length){const msg=unread.map(i=>'Paragraph '+(i+1)+' (“'+ps[i].split(' ').slice(0,5).join(' ')+'…”)').join(', ')+(unread.length>1?' weren\'t':' wasn\'t')+' read yet. '+(unread.length>1?'They stay':'It stays')+' marked “needs re-read”.';
    $('#state').textContent+=' · '+msg;toast(msg,9000)}
  if(r.clipped)toast('Some peaks were too loud (clipping). Move back a little or lower the mic gain.',6000);
}
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
  $('#bRec').disabled=!!r;$('#bPause').disabled=!r;$('#bStop').disabled=!r;$('#bMist').disabled=!r||r.paused;$('#bNext').disabled=!!r;$('#micSel').disabled=!!r;
  $('#bPause').textContent=r&&r.paused?'Resume':'Pause';
  t.classList.toggle('on',!!r&&!r.paused);t.classList.toggle('paused',!!r&&r.paused);
  const s=$('#state');s.classList.toggle('rec',!!r);s.textContent=!r?'Ready.':r.paused?'Paused (not recording).':'● Recording';
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
