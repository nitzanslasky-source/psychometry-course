"""Summary pages: one printable page per topic, in place of the r26-tNN-summary video (teacher, 2026-10-13: recording
the summary videos takes too long; students review faster from a page, and it should print).

    python3 summary_pages.py 13                 -> ~/Downloads/Topic-13-Summary-Page.html
    python3 summary_pages.py 13 --out X.html
    python3 summary_pages.py 13 --png X.png --pdf X.pdf     (also screenshot it / print it, headless Chrome)

Data per topic: summary_pages/tNN.json (see t13.json). Text markup: $...$ = math, **bold**, <br> = new line.
  sections[]  {title, span: "full" (both columns) | omitted (one column), class, blocks[]}
  blocks      p {text} · h {text} · ex {label, lines[]} (a worked example) · fig {ref, caption}
              rules / table {head[], rows[][], class} · traps {items[]} · checklist {items[]} · cols {cols: [[blocks]...]}
  figures     {name: {builder, args, kwargs, layers}} - the STUDIO's own figure builders, so the page shows the same
              pictures as the videos: "t13.DIST" = DIST in math_patches/_ai_vis_t13.py, "snl.fig" / "snl.two" =
              math_patches/_shaded_nl.py, "mv.SEESAW" etc. = math_patches/_method_visuals.py. A layered figure (DIST,
              the method visuals) is drawn with all the listed layers stacked, i.e. the finished picture.
  checks      python expressions that must all be true (the math of every example); the build stops if one fails.
              Names: abs, sqrt, GRID (-20 .. 20 in quarter steps), solve(f) = the GRID values where f is true.

Math: the studio and the student site both use MathJax 3 (SVG output). The page uses the studio's own MathJax bundle
(inlined in base-v18.html) at BUILD time, in headless Chrome, and embeds the finished SVGs - so the page needs no
script and works offline (the fonts fall back to the system ones offline). Rendered TeX is cached in
summary_pages/.cache/math.json.
"""
import argparse, html, importlib.util, json, math, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SPECS = os.path.join(HERE, 'summary_pages')
CACHE = os.path.join(SPECS, '.cache')
PATCHES = os.path.join(HERE, 'math_patches')
BASE = os.path.join(HERE, 'base-v18.html')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

# the student site's identity (tailwind.config.ts): ink navy, warm paper, gold, one quiet colour per subject
SUBJECTS = [('Psychometric Thinking', [51], '#3d5a99'), ('Algebra', range(1, 21), '#3d5a99'),
            ('Word Problems', range(21, 30), '#2f7d74'), ('Geometry', range(30, 39), '#b0662b'),
            ('Charts & Tables', [52], '#2f7d74'), ('Verbal Reasoning', range(39, 51), '#8a4a6b')]


# --------------------------------------------------------------------------------------------------------- checks
def run_checks(checks):
    grid = [i / 4 for i in range(-80, 81)]
    env = dict(abs=abs, sqrt=math.sqrt, GRID=grid, all=all, any=any, sorted=sorted,
               solve=lambda f: sorted(x for x in grid if f(x)))
    bad = []
    for c in checks:
        parts = [p.strip() for p in c.split(';')]
        g = dict(env, __builtins__={})
        try:
            for p in parts[:-1]: exec(p, g)
            ok = eval(parts[-1], g)
        except Exception as e:
            ok = False; c += '  (%s)' % e
        if not ok: bad.append(c)
    if bad: sys.exit('MATH CHECK FAILED:\n  ' + '\n  '.join(bad))
    return len(checks)


# -------------------------------------------------------------------------------------------------------- figures
def _module(key):
    path = {'snl': '_shaded_nl.py', 'mv': '_method_visuals.py'}.get(key) or '_ai_vis_%s.py' % key
    spec = importlib.util.spec_from_file_location('_sp_' + key, os.path.join(PATCHES, path))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _merge(svgs):
    """layers of the same size -> one svg (the first one's root and title, then every layer's body)"""
    first = svgs[0]
    head = first[:first.index('</title>') + len('</title>')]
    body = ''.join(re.sub(r'^.*?</title>|</svg>\s*$', '', s, flags=re.S) for s in svgs)
    return head + body + '</svg>'


_COURSE = []


def _question_svg(qid):
    """2026-10-14 (Claude, minimal): builder "q.<question id>" = the question's own figure as the BUILT course shows it
    (~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html, or env SP_COURSE), so the page gets the black-and-white
    question figures."""
    if not _COURSE:
        src = os.environ.get('SP_COURSE', os.path.expanduser('~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html'))
        s = open(src, encoding='utf-8').read(); k = s.find('window.COURSE=') + len('window.COURSE=')
        _COURSE.append(json.JSONDecoder().raw_decode(s[k:])[0])
    v = _COURSE[0]['questions'][qid].get('questionVisual') or {}
    return v['svg']


def build_figure(f, mods):
    if f['builder'].startswith('q.'): return _question_svg(f['builder'][2:])
    mod, fn = f['builder'].split('.')
    if mod not in mods: mods[mod] = _module(mod)
    out = getattr(mods[mod], fn)(*([f['name']] if mod.startswith('t') else []) + list(f.get('args', [])),
                                 **f.get('kwargs', {}))
    if isinstance(out, str): return out
    if isinstance(out, dict):                    # DIST-style: {layer: board item}
        return _merge([out[k]['v']['svg'] for k in f.get('layers') or list(out)])
    layers = dict(out)                           # method visuals: [(key, svg), ...]
    return _merge([layers[k] for k in f.get('layers') or [k for k, _ in out]])


# ----------------------------------------------------------------------------------------------------------- math
def _mathjax_bundle():
    s = open(BASE, encoding='utf-8').read()
    for m in re.finditer(r'<script[^>]*>', s):
        j = s.find('</script>', m.end())
        if j - m.end() > 500000 and 'MathJax' in s[m.end():m.end() + 400000]: return s[m.end():j]
    raise SystemExit('MathJax bundle not found in ' + BASE)


def render_math(texs):
    os.makedirs(CACHE, exist_ok=True)
    cp = os.path.join(CACHE, 'math.json')
    cache = json.load(open(cp)) if os.path.exists(cp) else {}
    todo = sorted(set(t for t in texs if t not in cache))
    if todo:
        harness = ('<!doctype html><html><body><script>window.MathJax={startup:{typeset:false},options:{enableMenu:false},'
                   'svg:{fontCache:"none"}};</script><script>' + _mathjax_bundle() + '</script><script>'
                   '(async function(){await MathJax.startup.promise;const T=' + json.dumps(todo).replace('</', '<\\/') + ';'
                   'const out={};for(const t of T){try{const n=MathJax.tex2svg(t,{display:false});const s=n.querySelector("svg");'
                   'out[t]=(n.querySelector("[data-mjx-error],merror")?"ERR ":"")+s.outerHTML}catch(e){out[t]="ERR "+e}}'
                   'document.body.innerHTML="<textarea id=res></textarea>";document.getElementById("res").textContent=JSON.stringify(out)})()'
                   '</script></body></html>')
        hp = os.path.join(CACHE, 'mathjax-harness.html')
        open(hp, 'w', encoding='utf-8').write(harness)
        r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=60000', '--dump-dom', 'file://' + hp],
                           capture_output=True, text=True, timeout=300)
        os.remove(hp)
        m = re.search(r'<textarea id="res">(.*?)</textarea>', r.stdout, re.S)
        if not m: raise SystemExit('MathJax render failed:\n' + r.stderr[-2000:])
        got = json.loads(html.unescape(m.group(1)))
        errs = {t: v[:200] for t, v in got.items() if v.startswith('ERR')}
        if errs: raise SystemExit('TeX errors: %s' % errs)
        cache.update(got)
        json.dump(cache, open(cp, 'w'), ensure_ascii=False)
    return cache


# ----------------------------------------------------------------------------------------------------------- text
MATH = re.compile(r'\$([^$]+)\$')


def bars(t):
    """plain | bars (no nesting) -> \\lvert / \\rvert in turn, so |-4| gets a unary minus (no | − 4| gap)"""
    t = t.replace('\\left|', '\0L').replace('\\right|', '\0R')
    out, k = [], 0
    for ch in t:
        if ch == '|': out.append('\\lvert ' if k % 2 == 0 else '\\rvert '); k += 1
        else: out.append(ch)
    return ''.join(out).replace('\0L', '\\left|').replace('\0R', '\\right|')


def tex_in(spec):
    out = []
    def walk(o):
        if isinstance(o, str): out.extend(bars(x) for x in MATH.findall(o))
        elif isinstance(o, list): [walk(x) for x in o]
        elif isinstance(o, dict): [walk(v) for k, v in o.items() if k not in ('figures', 'checks', '_about')]
    walk(spec)
    return out


class Text:
    def __init__(self, svgs): self.svgs = svgs

    def __call__(self, s):
        parts, k = [], 0
        for m in MATH.finditer(s):
            parts.append(self._plain(s[k:m.start()]))
            svg = re.sub(r'^<svg', '<svg aria-hidden="true"', self.svgs[bars(m.group(1))])
            k = m.end()
            tail = re.match(r'[.,:;!?)]*', s[k:]).group(0)   # keep the punctuation on the math's line
            parts.append('<span class="m" role="img" aria-label="%s">%s</span>%s' % (html.escape(m.group(1), quote=True), svg, tail))
            k += len(tail)
        parts.append(self._plain(s[k:]))
        return ''.join(parts)

    @staticmethod
    def _plain(t):
        t = html.escape(t, quote=False).replace('&lt;br&gt;', '<br>')
        t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
        t = t.replace('✓', '<span class="ok">✓</span>').replace('✗', '<span class="no">✗</span>')
        return t


def block(b, T, figs):
    k = b['type']
    if k == 'p': return '<p>%s</p>' % T(b['text'])
    if k == 'h': return '<h3>%s</h3>' % T(b['text'])
    if k == 'ex':
        lab = '<div class="ex-label">%s</div>' % T(b['label']) if b.get('label') else ''
        return '<div class="ex">%s%s</div>' % (lab, ''.join('<div class="ex-line">%s</div>' % T(x) for x in b['lines']))
    if k == 'fig':
        cap = '<figcaption>%s</figcaption>' % T(b['caption']) if b.get('caption') else ''
        return '<figure class="fig">%s%s</figure>' % (figs[b['ref']], cap)
    if k in ('rules', 'table'):
        cls = 'rules' if k == 'rules' else 'tbl ' + b.get('class', '')
        head = '<thead><tr>%s</tr></thead>' % ''.join('<th>%s</th>' % T(h) for h in b['head']) if b.get('head') else ''
        rows = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % T(c) for c in r)
                       for r in b['rows'])
        rows = rows.replace('<tr><td></td>', '<tr class="cont"><td></td>')
        return '<div class="tablewrap %s"><table>%s<tbody>%s</tbody></table></div>' % (cls, head, rows)
    if k == 'traps': return '<ul class="traps">%s</ul>' % ''.join('<li>%s</li>' % T(x) for x in b['items'])
    if k == 'checklist': return '<ul class="checklist">%s</ul>' % ''.join('<li>%s</li>' % T(x) for x in b['items'])
    if k == 'cols':
        return '<div class="cols cols-%d">%s</div>' % (len(b['cols']), ''.join(
            '<div class="col">%s</div>' % ''.join(block(x, T, figs) for x in c) for c in b['cols']))
    raise ValueError('unknown block type %r' % k)


# ------------------------------------------------------------------------------------------------------------ page
CSS = r'''
:root{--ink:#101826;--ink-soft:#2b3445;--muted:#6e7481;--line:#e7e3da;--paper:#fbfaf7;--paper-deep:#f4f1ea;
--gold:#a8812e;--gold-soft:#f3ead3;--ok:#1f7a4d;--bad:#b3261e;--teal:#087f83;--accent:%(accent)s}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%%}
body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 Inter,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;
-webkit-font-smoothing:antialiased}
.page{max-width:960px;margin:0 auto;padding:40px 24px 56px}
header.top{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;border-bottom:1px solid var(--line);
padding-bottom:18px;margin-bottom:22px}
.eyebrow{font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.eyebrow b{color:var(--accent);font-weight:600}
h1{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:46px;line-height:1.02;letter-spacing:-.02em;margin:6px 0 0}
.intro{margin:8px 0 0;color:var(--ink-soft);font-size:15px}
.printbtn{flex:none;border:0;border-radius:999px;background:var(--ink);color:#fff;font:500 13px/1 Inter,system-ui,sans-serif;
padding:10px 18px;cursor:pointer}
.printbtn:active{transform:scale(.97)}
.grid{display:flex;flex-direction:column;gap:16px}
.band{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;align-items:start}
.stack{display:flex;flex-direction:column;gap:16px;min-width:0}
section{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px 18px 14px;min-width:0}
h2{display:flex;align-items:center;gap:10px;font-size:16px;font-weight:650;letter-spacing:-.01em;margin:0 0 10px}
h2 .n{display:inline-grid;place-items:center;width:22px;height:22px;border-radius:50%%;border:1.5px solid var(--accent);
color:var(--accent);font-size:12px;font-weight:650;flex:none}
h3{font-size:13px;font-weight:650;margin:14px 0 6px}
p{margin:0 0 8px}
strong{font-weight:650}
.m svg{vertical-align:middle}
.m{white-space:nowrap}
.ex{border-left:3px solid var(--accent);background:var(--paper);border-radius:0 10px 10px 0;padding:7px 12px;margin:0 0 10px}
.ex-label{font-size:12px;font-weight:650;color:var(--accent);margin-bottom:2px}
.ex-line{padding:1px 0}
.fig{margin:4px 0 10px;text-align:center}
.fig>svg{width:100%%;max-width:440px;height:auto;display:block;margin:0 auto}
figcaption{font-size:13px;color:var(--ink-soft);margin-top:2px}
.tablewrap{overflow-x:auto;margin:0 0 6px}
table{border-collapse:collapse;width:100%%;font-size:14px}
th{text-align:left;font-size:10.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);
background:var(--paper);border-bottom:1px solid var(--line);padding:6px 10px}
td{padding:6px 10px;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:0}
tr.cont td{padding-top:0}
.rules{border:1.5px solid var(--ink);border-radius:12px}
.rules td:first-child{white-space:nowrap;font-weight:500}
.rules tr:has(+ tr.cont) td{border-bottom:0}
.tbl{border:1px solid var(--line);border-radius:12px}
.methods td:first-child{width:42%%;font-weight:500}
.clues td:last-child,.clues td:first-child{white-space:nowrap}
.cols{display:grid;gap:14px}
.cols-2{grid-template-columns:1fr 1fr}.cols-3{grid-template-columns:1fr 1fr 1fr}
.cols .fig>svg{max-width:100%%}
ul{margin:0;padding:0;list-style:none}
.traps li{position:relative;padding:3px 0 3px 22px}
.traps li::before{content:"⚠";position:absolute;left:0;top:3px;color:var(--bad)}
section.traps{border-color:#e7c9c5}
.checklist li{position:relative;padding:3px 0 3px 24px}
.checklist li::before{content:"";position:absolute;left:0;top:7px;width:13px;height:13px;border:1.5px solid var(--ink);border-radius:3px}
section.check{background:var(--gold-soft);border-color:#e6d7ae}
.ok{color:var(--ok);font-weight:700}.no{color:var(--bad);font-weight:700}
footer{margin-top:22px;font-size:12px;color:var(--muted);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
@media (max-width:720px){
 .page{padding:22px 16px 40px}
 h1{font-size:36px}
 .grid,.stack{gap:12px}
 .band{grid-template-columns:minmax(0,1fr);gap:12px}
 .clues td:last-child,.clues td:first-child{white-space:normal}
 .stack{display:contents}
 .rules thead{display:none}
 .rules tr{display:block;border-bottom:1px solid var(--line);padding:6px 0}
 .rules tr:last-child{border-bottom:0}
 .rules td{display:block;border:0;padding:2px 12px}
 .rules td:empty{display:none}
 .rules tr:has(+ tr.cont){border-bottom:0}
 .rules tr.cont{padding-top:0}
 .cols-2,.cols-3{grid-template-columns:minmax(0,1fr)}
 header.top{flex-wrap:wrap}
 section{padding:14px 14px 12px}
 .rules td:first-child{white-space:normal}
 .methods td:first-child{width:auto}
}
@page{size:A4;margin:10mm 10mm 11mm}
@media print{
 body{background:#fff;font-size:8.7pt;line-height:1.38;-webkit-print-color-adjust:exact;print-color-adjust:exact}
 .page{max-width:none;padding:0}
 .printbtn{display:none}
 header.top{padding-bottom:6px;margin-bottom:9px}
 h1{font-size:26pt}
 .intro{font-size:9pt;margin-top:3px}
 .grid,.band,.stack{gap:7px}
 section{border-radius:8px;padding:7px 9px 6px;break-inside:avoid;border-color:#bdb8ad}
 h2{font-size:10.5pt;margin-bottom:5px}
 h2 .n{width:15px;height:15px;font-size:7.5pt}
 h3{font-size:9pt;margin:7px 0 3px}
 p{margin-bottom:4px}
 table{font-size:8.5pt}
 th{font-size:6.5pt;padding:3px 6px}
 td{padding:3px 6px;border-bottom-color:#d6d1c6}
 .ex{padding:3px 8px;margin-bottom:5px;border-radius:0 6px 6px 0}
 .ex-label{font-size:8pt;margin-bottom:0}
 .ex-line{padding:0}
 .fig{margin:1px 0 5px}
 .fig>svg{max-width:62mm}
 .cols .fig>svg{max-width:55mm}
 figcaption{font-size:8pt}
 .cols{gap:8px}
 .traps li,.checklist li{padding-top:1.5px;padding-bottom:1.5px}
 .checklist li::before{top:4px;width:9px;height:9px}
 .traps li::before{top:1.5px}
 footer{margin-top:8px;font-size:7.5pt}
}
'''


def build(topic, out):
    spec = json.load(open(os.path.join(SPECS, 't%d.json' % topic), encoding='utf-8'))
    n = run_checks(spec.get('checks', []))
    tdoc = json.load(open(os.path.join(ROOT, 'content', 'full-course', 'topics', 't%d.json' % topic), encoding='utf-8'))
    subj, accent = next((s, a) for s, r, a in SUBJECTS if topic in r)
    mods, figs = {}, {}
    for name, f in spec.get('figures', {}).items():
        figs[name] = build_figure(dict(f, name=name), mods)
    T = Text(render_math(tex_in(spec)))
    # half-width sections between two full-width ones form a band of two stacks (left / right, "col": "L" | "R";
    # default: alternate), so a short section does not leave a hole next to a tall one
    secs, band, i = [], [], 0
    def flush():
        if not band: return
        L = [h for c, h in band if c == 'L']; R = [h for c, h in band if c == 'R']
        secs.append('<div class="band"><div class="stack">%s</div><div class="stack">%s</div></div>' % (''.join(L), ''.join(R)))
        band.clear()
    for s in spec['sections']:
        title = s['title']
        numbered = not (title.startswith('⚠') or s.get('class') == 'check')
        if numbered: i += 1
        num = '<span class="n">%d</span>' % i if numbered else ''
        full = s.get('span') == 'full'
        h = '<section%s class="%s"><h2>%s%s</h2>%s</section>' % ('' if full else ' style="order:%d"' % len(band), s.get('class', ''), num, T(title),
                                                               ''.join(block(b, T, figs) for b in s['blocks']))
        if full:
            flush(); secs.append(h)
        else:
            band.append((s.get('col') or 'LR'[len(band) % 2], h))
    flush()
    title = tdoc['title']
    page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s · Summary</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Instrument+Serif&display=swap" rel="stylesheet">
<style>%(css)s</style></head>
<body><main class="page">
<header class="top"><div><div class="eyebrow"><b>%(subj)s</b> · Topic %(topic)d · Summary</div><h1>%(title)s</h1>
<p class="intro">%(intro)s</p></div><button class="printbtn" onclick="window.print()">Print</button></header>
<div class="grid">%(secs)s</div>
<footer><span>Psychometry · The complete course</span><span>Topic %(topic)d summary · keep it next to you while you practice</span></footer>
</main></body></html>
''' % dict(title=html.escape(title), css=CSS % dict(accent=accent), subj=html.escape(subj), topic=topic,
           intro=T(spec.get('intro', '')), secs='\n'.join(secs))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(page)
    return n


def shoot(src, png=None, pdf=None, width=1100, height=3000):
    url = 'file://' + os.path.abspath(src)
    if png:
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=%d,%d' % (width, height),
                        '--screenshot=' + os.path.abspath(png), url], capture_output=True, timeout=120)
    if pdf:
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--print-to-pdf=' + os.path.abspath(pdf), url],
                       capture_output=True, timeout=120)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('topic', type=int)
    ap.add_argument('--out')
    ap.add_argument('--png'); ap.add_argument('--pdf')
    ap.add_argument('--width', type=int, default=1100); ap.add_argument('--height', type=int, default=3000)
    a = ap.parse_args()
    out = a.out or os.path.expanduser('~/Downloads/Topic-%d-Summary-Page.html' % a.topic)
    n = build(a.topic, out)
    print('math checks passed: %d' % n)
    print('written:', out)
    if a.png or a.pdf:
        shoot(out, a.png, a.pdf, a.width, a.height)
        if a.pdf:
            pages = None
            try:
                import fitz; pages = fitz.open(a.pdf).page_count
            except ImportError:
                pages = len(re.findall(rb'/Type\s*/Page[^s]', open(a.pdf, 'rb').read()))
            print('pdf:', a.pdf, '(%s A4 pages)' % pages)
        if a.png: print('png:', a.png)


if __name__ == '__main__':
    main()
