"""Arrow chains reveal one part per click (applied by build_verbal.py).

Teacher request (2026-10-06): a board line like  $m=2:\\ 32=16n \\;\\to\\; n=2$  appeared all at once — the result was
on the screen before the math was said. Now such a line appears in PARTS, on the same line: the first click shows the
part before the first arrow, every following click adds "→ next part", until the whole line is there.

What counts as an arrow (scan of all videos, 2026-10-06): → (751×), \\to (409×), \\rightarrow (231×), \\Rightarrow (136×),
"->" in plain text (50×, topic 50), ⇒ (3×), \\xrightarrow (2×); also \\implies, \\Longrightarrow, \\longrightarrow, ⟹ (unused
today). NOT split: ⇔ \\iff \\Leftrightarrow (equivalence, not a step), arrows inside braces / \\text{..} / \\left..\\right, and
an arrow with nothing visible before it (e.g. a line that starts with "⇒", or a lone "$\\rightarrow$").
Only 't' (text) items that APPEAR on a click are split; items already on the slide when it loads are not.

How (smallest change to the step model):
- Data (build time, apply_data): for every affected item an extra cue line {'appear': i, 'part': j, 'of': n, 'label': ..}
  is inserted into the beat's `lines` after the item's own [APPEAR] — so every part is simply one more click of the
  same item. stepCount (1 + number of appear lines), svgcheck/layoutcheck, the prompter chunks, the step x/y counter
  all count it with no change. The part cues are spread over the spoken lines right after the [APPEAR] (up to the first
  [DRAW] / next [APPEAR]; S of them): part j+1 goes after spoken line min(j, S) — so one spoken line per part, the
  rest after the last one (S = 0 -> right after the APPEAR). This is only where the prompter suggests the click. Spoken lines are never
  split or renumbered, so ai_scripts / ai_check / ai_narrate (spoken-line counts) are unaffected. Beats that got parts
  carry b.arw = 1.
- Renderer (runtime): hybridSvg works out from the cues which items are shown and how many parts of each; the item is
  laid out exactly as before (full line, same size, same wrapping, same positions), and richSvg just leaves out the
  tokens of the hidden parts. A $..$ formula that straddles a cut is drawn whole and clipped at the cut (the cut x is
  the width of the formula's part before the arrow), so nothing moves when a part appears. With the faded preview on
  (window.__ghost, teacher only) the hidden parts are drawn at opacity 0.2, like not-yet-shown items.
- Prompter: a part cue shows as "▶ PRESS NEXT → ADD  → n = 2  (part 2/2)"; the item's own APPEAR label says which part
  it shows first. In the script editor a part cue is the line [NEXT PART: ..]; a script edited and saved BEFORE this
  feature (with only the [APPEAR: ..] lines) still loads — the part cues are put back in automatically.

RECORDED VIDEOS DO NOT CHANGE: a video that has ANY take in ~/Documents/Course.recordings (studio_done.takes) with a
time stamp before CUTOFF is FROZEN — it keeps the old behaviour (whole line at once), so its existing takes, "Continue
a take" and the Cut panel keep the same step sequence. All other videos get arrow parts. The frozen list is fixed by
CUTOFF, so a video recorded later with arrow parts is not frozen by its own new take. The list is embedded in the
studio as window.ARROW_FROZEN (+ window.ARROW_CUTOFF); the runtime ignores part cues of a frozen video as a safety net.
NOTE: takes recorded with an OLDER studio file after CUTOFF are not frozen — the build prints them; if any exist,
move CUTOFF to after them and rebuild.
"""
import os, re
import studio_done

CUTOFF = '2026-10-06T08:40:00.000Z'   # takes recorded before this moment freeze their video (old whole-line reveal)

# ---------- arrow parser (mirrored exactly by arwCuts in the JS below) ----------
TEX_ARROWS = {'to', 'rightarrow', 'Rightarrow', 'implies', 'Longrightarrow', 'longrightarrow', 'xrightarrow'}
UNI_ARROWS = ('→', '⇒', '⟹', '⟶')
_INVIS = re.compile(r'\\(?:quad|qquad)(?![A-Za-z])|\\[ ,;:!]|[\s$\u0001\u0002{}~]')


def _visible(seg):
    return bool(_INVIS.sub('', seg))


def cuts(s):
    """Char offsets where a new part starts (each at an arrow). [] = not split."""
    out, last, i, n, math_, depth = [], 0, 0, len(s), False, 0

    def cand(k):
        nonlocal last
        if _visible(s[last:k]):
            out.append(k); last = k
    while i < n:
        c = s[i]
        if c == '$':
            math_ = not math_; depth = 0; i += 1; continue
        if not math_:
            if c in UNI_ARROWS: cand(i)
            elif s.startswith('->', i): cand(i); i += 2; continue
            i += 1; continue
        if c == '\\':
            m = re.match(r'[A-Za-z]+', s[i + 1:])
            if not m: i += 2; continue
            name = m.group(0)
            if name in TEX_ARROWS and depth == 0: cand(i)
            if name in ('left', 'begin'): depth += 1
            elif name in ('right', 'end'): depth -= 1
            i += 1 + len(name); continue
        if c == '{': depth += 1
        elif c == '}': depth -= 1
        elif c in UNI_ARROWS and depth == 0: cand(i)
        i += 1
    return out


_PLAIN = [(r'\\hl\{[^{}]*\}', ''), (r'\\(?:Rightarrow|implies|Longrightarrow)(?![A-Za-z])', '⇒'), (r'\\(?:to|rightarrow|longrightarrow)(?![A-Za-z])', '→'),
          (r'\\xrightarrow\{([^{}]*)\}', r'→(\1)'), (r'\\xleftarrow\{([^{}]*)\}', r'←(\1)'),
          (r'\\(?:text|mathrm|textbf|mathbf|operatorname)\{([^{}]*)\}', r'\1'), (r'\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}', r' \1/\2'),
          (r'\\[dt]?frac\s*(\w)\s*(\w)', r' \1/\2'),
          (r'\\sqrt\{([^{}]*)\}', r'√\1'), (r'\\cdot(?![A-Za-z])', '·'), (r'\\times(?![A-Za-z])', '×'), (r'\\div(?![A-Za-z])', '÷'),
          (r'\\pi(?![A-Za-z])', 'π'), (r'\\le(?:q)?(?![A-Za-z])', '≤'), (r'\\ge(?:q)?(?![A-Za-z])', '≥'), (r'\\ne(?:q)?(?![A-Za-z])', '≠'),
          (r'\\(?:quad|qquad)(?![A-Za-z])', ' '), (r'\\[ ,;:!]', ' '), (r'\\%', '%'), (r'\\([A-Za-z]+)', r'\1'), (r'[{}$]', ''), (r'\s+', ' ')]


def plain(t):
    for a, b in _PLAIN: t = re.sub(a, b, t)
    return t.strip()


def parts(t):
    c = cuts(t)
    if not c: return []
    b = [0] + c + [len(t)]
    return [t[b[k]:b[k + 1]] for k in range(len(b) - 1)]


# ---------- frozen videos ----------
def _iso(ts):   # 2026-10-06T07-40-00-000Z -> 2026-10-06T07:40:00.000Z
    d, t = ts.split('T'); h, m, s, ms = t[:-1].split('-'); return '%sT%s:%s:%s.%sZ' % (d, h, m, s, ms)


def frozen_ids(root=studio_done.ROOT, cutoff=CUTOFF):
    fz, late = set(), []
    for vid, ts in studio_done.takes(root):
        if _iso(ts) < cutoff: fz.add(vid)
        else: late.append((vid, _iso(ts)))
    return sorted(fz), late


# ---------- data pass ----------
def apply_data(D, frozen):
    frozen = set(frozen); st = dict(items=0, cues=0, videos=set(), beats=0, frozen_skipped=set(), by_arrow={})
    for vid, v in D['videos'].items():
        for b in v.get('beats') or []:
            if b.get('layout') != 'hybrid' or b.get('arw'): continue
            lines, items, out, touched = b['lines'], b['items'], [], False
            k = 0
            while k < len(lines):
                l = lines[k]; out.append(l); k += 1
                if l.get('appear') is None: continue
                it = items[l['appear']]
                ps = parts(it['t']) if it.get('k') == 't' and isinstance(it.get('t'), str) else []
                if not ps: continue
                if vid in frozen: st['frozen_skipped'].add(vid); continue
                n = len(ps); l = dict(l); out[-1] = l
                e = k
                while e < len(lines) and lines[e].get('appear') is None: e += 1
                seg = lines[k:e]; S = 0
                for x in seg:                       # spoken lines right after the APPEAR, up to the first DRAW
                    if x.get('draw') is not None: break
                    if x.get('say') is not None: S += 1
                pos = {j: min(j, S) for j in range(1, n)}
                cue = lambda j: {'appear': l['appear'], 'part': j, 'of': n, 'label': '%s  (part %d/%d)' % (plain(ps[j]), j + 1, n)}
                l['label'] = '%s — part 1/%d first: %s' % (l['label'], n, plain(ps[0]))
                out += [cue(j) for j in range(1, n) if pos[j] == 0]; said = 0
                for x in seg:
                    out.append(x)
                    if x.get('say') is not None:
                        said += 1; out += [cue(j) for j in range(1, n) if pos[j] == said]
                k = e; touched = True
                st['items'] += 1; st['cues'] += n - 1; st['videos'].add(vid)
                for p in ps[1:]:
                    a = re.match(r'\$?\s*(\\[A-Za-z]+|->|.)', p).group(1); st['by_arrow'][a] = st['by_arrow'].get(a, 0) + 1
            if touched:
                assert [x['appear'] for x in out if x.get('appear') is not None and x.get('part') is None] == \
                       [x['appear'] for x in lines if x.get('appear') is not None and x.get('part') is None]
                b['lines'] = out; b['arw'] = 1; st['beats'] += 1
    return st


# ---------- JS ----------
RICH_HEAD_OLD = "function richSvg(text,x,y,width,size=34){let _b=0;"
RICH_HEAD_NEW = ("function richSvg(text,x,y,width,size=34){if(window.__arw){const _A=arwCuts(String(text));"
                 "if(_A.length&&window.__arw.k<=_A.length)return richSvgArw(String(text),x,y,width,size,_A[window.__arw.k-1])}let _b=0;")
SHOWN_OLD = "const shown=(b.pre||0)+Math.max(0,step|0);\n const _lay=sc=>"
SHOWN_NEW = "const [shown,AP]=arwShown(v,b,step);\n const _lay=sc=>"
LOOP_OLD = "b.items.forEach((it0,i)=>{let it=sc===1"
LOOP_NEW = "b.items.forEach((it0,i)=>{window.__arw=(AP&&i<shown&&AP[i]!=null)?{k:AP[i]}:null;let it=sc===1"
END_OLD = "});return {o,bot}};"
END_NEW = "});window.__arw=null;return {o,bot}};"
PARSE_OLD = "function parseHybrid(text,b){"
PARSE_NEW = "function parseHybrid0(text,b){"
PUSH_OLD = "out.push({appear:cues[ai].appear,label:"
PUSH_NEW = "out.push({...cues[ai],label:"
LT_OLD = "const hyLineText=l=>l.say!=null?l.say:l.draw!=null?'[DRAW: '+l.draw+']':'[APPEAR: '+l.label+']';"
LT_NEW = "const hyLineText=l=>l.say!=null?l.say:l.draw!=null?'[DRAW: '+l.draw+']':l.part!=null?'[NEXT PART: '+l.label+']':'[APPEAR: '+l.label+']';"
PR_OLD = "ls.map(l=>l.appear!=null?`<div class=\"hy-cue hy-appear\"><b>${k<=step?'✓ APPEARED':k===step+1?'▶ PRESS NEXT → APPEAR':'APPEAR'}</b> ${esc(l.label)}</div>`"
PR_NEW = ("ls.map(l=>l.appear!=null&&l.part!=null?`<div class=\"hy-cue hy-appear hy-part\"><b>${k<=step?'✓ ADDED':k===step+1?'▶ PRESS NEXT → ADD':'THEN ADD'}</b> ${esc(l.label)}</div>`"
          ":l.appear!=null?`<div class=\"hy-cue hy-appear\"><b>${k<=step?'✓ APPEARED':k===step+1?'▶ PRESS NEXT → APPEAR':'APPEAR'}</b> ${esc(l.label)}</div>`")
TOAST_OLD = "' [APPEAR: …] lines"
TOAST_NEW = "' [APPEAR: …] / [NEXT PART: …] lines"

JS = r"""
/* ---- arrow chains: one part per click (studio_arrows.py) ---- */
window.ARROW_CUTOFF=__CUTOFF__;window.ARROW_FROZEN=__FROZEN__;var ARW_FROZEN=new Set(window.ARROW_FROZEN),ARWN=0;   // var: a render may run before this line
var ARW_TEX=new Set(['to','rightarrow','Rightarrow','implies','Longrightarrow','longrightarrow','xrightarrow']),ARW_UNI='→⇒⟹⟶';
function arwVisible(seg){return seg.replace(/\\(?:quad|qquad)(?![A-Za-z])|\\[ ,;:!]|[\s$\u0001\u0002{}~]/g,'')!==''}
function arwCuts(s){const out=[];let last=0,i=0,m=false,d=0;const n=s.length,cand=k=>{if(arwVisible(s.slice(last,k))){out.push(k);last=k}};
 while(i<n){const c=s[i];if(c==='$'){m=!m;d=0;i++;continue}
  if(!m){if(ARW_UNI.includes(c))cand(i);else if(s.startsWith('->',i)){cand(i);i+=2;continue}i++;continue}
  if(c==='\\'){const mm=s.slice(i+1).match(/^[A-Za-z]+/);if(!mm){i+=2;continue}const nm=mm[0];if(ARW_TEX.has(nm)&&d===0)cand(i);
   if(nm==='left'||nm==='begin')d++;else if(nm==='right'||nm==='end')d--;i+=1+nm.length;continue}
  if(c==='{')d++;else if(c==='}')d--;else if(ARW_UNI.includes(c)&&d===0)cand(i);i++}
 return out}
/* which items are shown at this step, and how many parts of each item that has part cues (null = no parts here) */
function arwShown(v,b,step){const s=Math.max(0,step|0);if(!b.arw||ARW_FROZEN.has(v.id))return [(b.pre||0)+s,null];
 const cues=b.lines.filter(l=>l.appear!=null),P={},AP={};let shown=b.pre||0;cues.forEach(c=>{if(c.part!=null)P[c.appear]=c.of});
 for(const c of cues.slice(0,s)){if(c.part!=null)AP[c.appear]=c.part+1;else{shown++;if(P[c.appear])AP[c.appear]=1}}
 for(const k in AP)if(AP[k]>=P[k])delete AP[k];return [shown,AP]}
/* richSvg with everything from char offset V on hidden (faded with the preview on); layout = the full text, unchanged */
function richSvgArw(text,x,y,width,size,V){let _b=0,pos=0;const parts=text.split(/(\$[^$]+\$)/g);let tokens=[];
 for(const p of parts){const p0=pos;pos+=p.length;if(p.startsWith('$')&&p.endsWith('$')){const tex=p.slice(1,-1),m=mathSvg(tex);tokens.push({tex,o:p0,e:pos,w:m.width*size*.5,h:m.height*size*.5})}
  else{let q=p0;for(const w of p.split(/(\s+)/)){const o=q;q+=w.length;if(!w)continue;if(w.includes('\n')){tokens.push({br:1});continue}{let ww=w;if(ww[0]==='\u0001'){_b=1;ww=ww.slice(1)}const end=ww.endsWith('\u0002');if(end)ww=ww.slice(0,-1);const bb=_b&&ww.trim();if(end)_b=0;tokens.push({text:ww,raw:w,o,e:q,b:bb,w:textWidth(ww,size,bb?700:400),h:size*1.1})}}}}
 let rows=[],row=[],rw=0,rh=size*1.25;for(let t of tokens){if(t.br){rows.push({tokens:row,h:rh});row=[];rw=0;rh=size*1.25;continue}if(t.w>width&&t.tex){const factor=width/t.w;t={...t,w:width,h:t.h*factor,size:size*factor}}if(rw+t.w>width&&row.length){rows.push({tokens:row,h:rh});row=[];rw=0;rh=size*1.25;if(t.text?.trim()==='')continue}row.push(t);rw+=t.w;rh=Math.max(rh,t.h+12)}if(row.length)rows.push({tokens:row,h:rh});
 const G=!!window.__ghost,clip=(svg,x0,w0,y0,h0,fade)=>{const id='arwc'+(++ARWN);return `<clipPath id="${id}"><rect x="${x0}" y="${y0}" width="${Math.max(0,w0)}" height="${h0}"/></clipPath><g clip-path="url(#${id})"${fade?' opacity="0.2"':''}>${svg}</g>`};
 let out='',cy=y;for(const r of rows){let cx=x;for(const t of r.tokens){const svg=t.tex?mathAt(t.tex,cx,cy+(r.h-t.h)/2,t.size||size).svg:(t.b?svgText(t.text,cx,cy+r.h/2+size*.34,size,PAL.accent,700):svgText(t.text,cx,cy+r.h/2+size*.34,size,PAL.ink));
  if(t.e<=V)out+=svg;
  else{let cut=0;if(t.o<V){if(t.tex){const pre=t.tex.slice(0,V-t.o-1);if(arwVisible(pre))cut=mathSvg(pre).width*(t.size||size)*.5+(t.size||size)*.08}else{const pre=t.raw.slice(0,V-t.o).replace(/[\u0001\u0002]/g,'');if(pre.trim())cut=textWidth(pre,size,t.b?700:400)}}
   if(cut>0)out+=clip(svg,cx-30,cut+30,cy-40,r.h+80,false);
   if(G)out+=cut>0?clip(svg,cx+cut,t.w-cut+40,cy-40,r.h+80,true):`<g opacity="0.2">${svg}</g>`}
  cx+=t.w}cy+=r.h+5}return {svg:out,height:cy-y}}
/* script editor: part cues are [NEXT PART: ..] lines; a script saved before the parts existed gets them put back */
function parseHybrid(text,b){if(!b.arw)return parseHybrid0(text,b);const t=String(text).replace(/^\s*\[NEXT PART:\s*(.*)\]\s*$/gim,'[APPEAR: $1]');
 let p=parseHybrid0(t,b);if(p)return p;p=parseHybrid0(t,{...b,lines:b.lines.filter(l=>l.part==null)});if(!p)return null;
 const res=[];for(let i=0;i<p.length;i++){const l=p[i];res.push(l);if(l.appear==null)continue;const ps=b.lines.filter(c=>c.part!=null&&c.appear===l.appear);if(!ps.length)continue;
  let e=i+1;while(e<p.length&&p[e].appear==null)e++;const seg=p.slice(i+1,e);let S=0;for(const x of seg){if(x.draw!=null)break;if(x.say!=null)S++}const at=j=>Math.min(j,S);
  ps.forEach((c,j)=>{if(at(j+1)===0)res.push(c)});let said=0;for(const x of seg){res.push(x);if(x.say!=null){said++;ps.forEach((c,j)=>{if(at(j+1)===said)res.push(c)})}}i=e-1}
 return res}
window.ARW_DIAG={arwCuts,arwShown};   // for checks (svgcheck-style harnesses)
setTimeout(()=>{try{const bad=Object.values(D.videos).filter(v=>ARW_FROZEN.has(v.id)&&v.beats.some(b=>b.arw)).map(v=>v.id);if(bad.length)console.warn('arrow parts on frozen videos (ignored):',bad)}catch{}},1500);
"""


def apply(html, frozen):
    import json
    for old, new in ((RICH_HEAD_OLD, RICH_HEAD_NEW), (SHOWN_OLD, SHOWN_NEW), (LOOP_OLD, LOOP_NEW), (END_OLD, END_NEW),
                     (PARSE_OLD, PARSE_NEW), (PUSH_OLD, PUSH_NEW), (LT_OLD, LT_NEW), (PR_OLD, PR_NEW), (TOAST_OLD, TOAST_NEW)):
        assert html.count(old) == 1, ('studio_arrows anchor', html.count(old), old[:60])
        html = html.replace(old, new)
    k = html.find('function richSvg(')
    assert k > 0
    js = JS.replace('__CUTOFF__', json.dumps(CUTOFF)).replace('__FROZEN__', json.dumps(sorted(frozen)))
    return html[:k] + js.lstrip() + html[k:]
