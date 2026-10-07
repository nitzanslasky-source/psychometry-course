"""Added content is marked in the studio (applied by build_verbal.py LAST, after studio_arrows).

Teacher request (2026-10-07): "What are the lessons, slides and techniques you added? Mark them for me in the studio so I
know to look at the script more carefully."  The manifest comes from added_content.py (built course vs base-v18).

Display (studio UI only - never the board / canvas that is recorded; the recording draws the slide SVG on a canvas):
- Course navigation: an added video gets an orange "NEW" tag; a video of yours that only got added slides gets a small
  "+ new slides" tag (or "+ new lines" when an older slide only got new-method lines). The tag's tooltip names the
  source / method. Each topic header shows "N new" when it has added material. Works next to the green recorded marks of
  studio_done.py (a recorded video keeps its green bar and ✓ and also shows the tag).
- Video heading: an orange chip "NEW · <label>" / "+ new slides".
- Script panel: on an added slide, an orange banner above the script: "⚠ Added slide — New exam method · Power count.
  Not from your Hebrew course: read the script carefully (see the teacher guide)". Older slides with new-method lines
  get a lighter banner. The on-board script strip (left column, top strip, draw mode) shows a one-line orange banner in
  its head, so it stays in view while reading.
- Slide menu: added slides are marked "★" in the slide drop-down.
Slides are found by index + title; if the script editor has moved slides, the title is used.

WHAT was added (teacher request 2026-10-07: "point out WHAT you added, so I know not only THAT you added, but WHAT"):
the notes come from added_notes.json (attach_notes in added_content.py).
- Added video: on its FIRST slide a box at the top of the script panel (and the on-board script strip):
  "Added lesson — what it adds: <note>" (+ the teacher-guide section for a new exam method); the title chip's tooltip
  carries the same note.
- Added slide: the banner reads "⚠ Added slide — <label>: <note>".
- New lines on the teacher's own slides: those script lines get an orange left border and a small "new line" / "new on board" tag (in the
  script panel and the on-board strip; PRESS NEXT cue boxes keep their colours), and the slide gets a dashed banner
  "New lines on this slide: <note>". Lines are matched by their text, so a line the teacher re-wrote in the script
  editor is no longer marked.  The slide menu marks such slides with "+".
"""
import json

JS = r"""
/* ---- added content (not from the teacher's Hebrew course) is marked in the studio UI only (never recorded) ---- */
var ADDED=__ADDED__;
var ADDED_GUIDE='real_exam/method_search/TEACHER_GUIDE.md';
(()=>{const st=document.createElement('style');st.textContent=`
.add-tag{margin-left:auto;flex:none;align-self:center;font-size:.625rem;font-weight:800;line-height:1;padding:3px 6px;border-radius:999px;letter-spacing:.02em;white-space:nowrap}
.add-tag.new{background:#ea580c;color:#fff}.add-tag.part{background:#ffedd5;color:#9a3412;border:1px solid #fdba74}
.add-tag+.rec-tag{margin-left:5px}
.add-count{margin-left:auto;flex:none;font-size:.6875rem;font-weight:700;color:#9a3412;padding:2px 7px;border-radius:999px;background:#ffedd5;white-space:nowrap;align-self:center}
.add-count+.rec-count{margin-left:6px}
.topic-group>summary:has(.add-count){flex-wrap:wrap;row-gap:5px}.topic-group>summary:has(.add-count)>span:nth-child(2){flex:1 1 200px;min-width:0}   /* the chips go on their own row, under the title */
.topic-group>summary>.add-count{margin-left:36px}
.add-chip{display:inline-block;vertical-align:middle;margin-left:12px;font-size:.8125rem;font-weight:800;color:#9a3412;background:#ffedd5;border:1px solid #fdba74;border-radius:999px;padding:3px 10px;letter-spacing:0}
.add-chip.new{color:#fff;background:#ea580c;border-color:#ea580c}
.add-banner{margin:12px 20px 4px;padding:10px 14px;border-radius:10px;background:#fff7ed;border:2px solid #fb923c;color:#7c2d12;font-size:15px;line-height:1.4;font-weight:600}
.add-banner b{color:#c2410c}.add-banner .add-why{display:block;font-weight:500;color:#9a3412;margin-top:3px;font-size:14px}
.add-banner.lines{border-style:dashed;background:#fffbeb}
.sb-head:has(.add-sb){flex-wrap:wrap;opacity:1}
.sb-head .add-sb{flex:1 0 100%;order:5;margin:4px 0 0;padding:5px 10px;border-radius:7px;background:#ea580c;color:#fff;font-size:15px;font-weight:700;letter-spacing:0;line-height:1.3;text-align:left}
.sb-head .add-sb.lines{background:#fff7ed;color:#9a3412}
.add-banner .add-note{font-weight:600;color:#7c2d12}.add-banner .add-guide{display:block;font-weight:500;color:#9a3412;margin-top:3px;font-size:13px}
.add-what{margin:12px 20px 4px;padding:11px 15px;border-radius:10px;background:#ea580c;color:#fff;font-size:15px;line-height:1.45;font-weight:500}
.add-what b{font-weight:800}.add-what .add-guide{display:block;margin-top:4px;font-size:13px;color:#ffedd5}
.sb-head .add-sb .add-note{font-weight:500}
.add-ln{border-left:4px solid #ea580c!important;padding-left:8px}
.hy-say.add-ln{margin-left:-12px}
.add-ln-tag{flex:none;align-self:flex-start;margin-left:auto;font-size:11px;font-weight:800;line-height:1;padding:3px 6px;border-radius:999px;background:#ffedd5;color:#9a3412;border:1px solid #fdba74;letter-spacing:.02em;text-transform:uppercase}
.hy-cue .add-ln-tag{float:right;margin:1px 0 0 8px}
.sb-prompter .add-ln{border-left-color:#fb923c!important}
.sb-prompter .add-ln-tag{background:#7c2d12;color:#ffedd5;border-color:#c2410c}`;document.head.append(st)})();
function addVid(id){return ADDED&&ADDED[id]||null}
function addSlide(v,k){const m=v&&addVid(v.id);if(!m)return null;const b=v.beats[k];if(!b)return null;
 const s=m.s[k];if(s&&s[0]===b.title)return s;
 for(const x of Object.values(m.s))if(x[0]===b.title)return x;   // slides moved in the script editor: match by title
 return null}
function addLines(v,k){const m=v&&addVid(v.id);if(!m||!m.L)return null;const b=v.beats[k];if(!b)return null;
 const x=m.L[k];if(x&&x.t===b.title)return x;
 for(const y of Object.values(m.L))if(y.t===b.title)return y;
 return null}
function addKindWord(m){return m.k==='solution'?'question video':m.k==='summary'?'summary':'lesson'}
function addWhatHtml(v,k,strip){const m=v&&addVid(v.id);if(!m||!m.a||k!==0||!m.n)return '';
 if(strip)return `<div class="add-sb" title="${esc(m.n)}">Added ${addKindWord(m)} — what it adds: <span class="add-note">${esc(m.n)}</span></div>`;
 return `<div class="add-what" data-added="1"><b>Added ${addKindWord(m)} — what it adds:</b> ${esc(m.n)}`
  +`<span class="add-guide">${esc(m.l)}${m.g?' · '+esc(m.g):''} · not from your Hebrew course: read the script carefully.</span></div>`}
function addBannerHtml(v,k){const w=addWhatHtml(v,k,false);if(w)return w;
 const s=addSlide(v,k),x=addLines(v,k);if(!s&&!x)return '';const lines=!s||s[2]==='lines',meth=s&&/^New exam method/.test(s[1]);
 const note=lines?(x&&x.n):s[3],g=s&&s[4];
 if(lines)return `<div class="add-banner lines" data-added="1">⚠ <b>New lines on this slide</b>${note?': <span class="add-note">'+esc(note)+'</span>':''}${s?' ('+esc(s[1])+')':''}`
  +`<span class="add-why">Your slide, with ${x&&x.c?x.c+' added line'+(x.c>1?'s':''):'new lines'} (orange border, "new line" tag): read them carefully${g?'':'.'}</span>${g?'<span class="add-guide">'+esc(g)+'</span>':''}</div>`;
 return `<div class="add-banner" data-added="1">⚠ <b>Added slide</b> — ${esc(s[1])}${note?': <span class="add-note">'+esc(note)+'</span>':'.'}`
  +`<span class="add-why">Not from your Hebrew course: read the script carefully${meth&&!g?' (see the teacher guide)':''}.</span>${g?'<span class="add-guide">'+esc(g)+'</span>':''}</div>`}
function addSbBanner(v,k){const w=addWhatHtml(v,k,true);if(w)return w;
 const s=addSlide(v,k),x=addLines(v,k);if(!s&&!x)return '';const lines=!s||s[2]==='lines';const note=lines?(x&&x.n):s[3];
 return `<div class="add-sb${lines?' lines':''}" title="${lines?'Your slide, with new lines':'Not from your Hebrew course'} — read the script carefully">⚠ ${lines?'New lines on this slide':'Added slide — '+esc(s[1])}${note?': <span class="add-note">'+esc(note)+'</span>':''}</div>`}
/* one script line of the prompter (hyPrompter): an added line gets an orange border + "added" tag */
function addLn(v,bi,l,h){if(typeof STUDIO==='undefined'||!STUDIO)return h;const x=addLines(v,bi);if(!x)return h;
 const hit=l.say!=null?x.s.includes(l.say):l.draw!=null?x.d.includes(l.draw):l.appear!=null&&x.i.includes(l.appear);if(!hit)return h;
 h=h.replace('<div class="','<div class="add-ln ');const tag=`<span class="add-ln-tag" title="Added to your slide — not from your Hebrew course">${l.appear!=null?'new on board':'new line'}</span>`;
 return l.say!=null?h.replace(/<\/div>$/,tag+'</div>'):h.replace(/(<b>[^<]*<\/b>)/,tag+'$1')}
function addPaintSlide(){if(typeof STUDIO==='undefined'||!STUDIO)return;const v=video();const cp=$('#script-copy');if(!cp)return;
 cp.parentElement.querySelectorAll(':scope > .add-banner, :scope > .add-what').forEach(x=>x.remove());if(!v)return;const h=addBannerHtml(v,state.beat);if(h)cp.insertAdjacentHTML('beforebegin',h)}   // above the scrolling script, so it stays in view
function addPaint(){if(!ADDED||typeof STUDIO==='undefined'||!STUDIO)return;const nav=$('#course-nav');if(!nav)return;
 nav.querySelectorAll('[data-go]').forEach(b=>{const r=D.flow[+b.dataset.go];const m=r&&r.type==='video'?addVid(r.ref):null;let t=b.querySelector('.add-tag');
  if(!m){t?.remove();return}
  if(!t){t=document.createElement('span');const rt=b.querySelector('.rec-tag');rt?b.insertBefore(t,rt):b.append(t)}
  t.className='add-tag '+(m.a?'new':'part');t.textContent=m.a?'NEW':(m.p?'+ new slides':'+ new lines');t.title=(m.a?'Added video — ':'Added inside this video — ')+m.l+(m.a&&m.n?'\nWhat it adds: '+m.n:'')+' · read the script carefully'});
 const groups=nav.querySelectorAll('.topic-group');D.topics.forEach((tp,k)=>{const g=groups[k];if(!g)return;const sum=g.querySelector('summary');
  const ids=[...new Set(D.flow.filter(r=>r.type==='video'&&r.topic===tp.id&&addVid(r.ref)).map(r=>r.ref))];let c=sum.querySelector('.add-count');
  if(!ids.length){c?.remove();return}if(!c){c=document.createElement('span');const rc=sum.querySelector('.rec-count');rc?sum.insertBefore(c,rc):sum.append(c)}
  const nv=ids.filter(id=>ADDED[id].a).length;c.className='add-count';c.textContent=ids.length+' new';c.title=nv+' added videos, '+(ids.length-nv)+' of your videos with added slides or lines'});
 }
function addChip(r){const m=typeof STUDIO!=='undefined'&&STUDIO&&r&&r.type==='video'?addVid(r.ref):null;if(!m)return '';
 return `<span class="add-chip${m.a?' new':''}" title="${m.a&&m.n?'What it adds: '+esc(m.n)+' — ':''}${esc(m.l)}${m.g?' · '+esc(m.g):''} · read the script carefully">${m.a?'NEW · '+esc(m.l):(m.p?'+ new slides':'+ new lines')}</span>`}
function addStar(v,k){if(typeof STUDIO==='undefined'||!STUDIO)return '';const s=addSlide(v,k);return s&&s[2]==='new'?'★ ':(s||addLines(v,k))?'+ ':''}
window.ADDED_CONTENT=ADDED;
setTimeout(()=>{addPaint();addPaintSlide()},900);
"""

REPL = [
    # nav: after the green recorded marks
    ("$('#course-nav').querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>go(+b.dataset.go));recPaint();}",
     "$('#course-nav').querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>go(+b.dataset.go));recPaint();addPaint();}"),
    # script panel banner (side script)
    ("if(STUDIO){$('#script-title').textContent=b.title;",
     "if(STUDIO){$('#script-title').textContent=b.title;addPaintSlide();"),
    # chip next to the current video's title (after the green "Recorded" chip)
    ("<h1>${esc(name)}${recChip(r)}</h1>", "<h1>${esc(name)}${recChip(r)}${addChip(r)}</h1>"),
    # slide menu: added slides get a star
    ("<option value=\"${i}\" ${i===state.beat?'selected':''}>${i+1} · ${esc(short(x.title,36))}</option>",
     "<option value=\"${i}\" ${i===state.beat?'selected':''}>${addStar(v,i)}${i+1} · ${esc(short(x.title,36))}</option>"),
    # on-board script strip (left column / top strip / draw mode): a one-line banner inside its head, so it stays in view
    ('aria-label="Larger script">A+</button></span></div>`+hyPrompter(v,state.beat,state.step)',
     'aria-label="Larger script">A+</button></span>${addSbBanner(v,state.beat)}</div>`+hyPrompter(v,state.beat,state.step)'),
    # prompter lines (script panel + on-board strip): mark lines added into the teacher's slides
    ("ls.map(l=>l.appear!=null&&l.part!=null?", "ls.map(l=>addLn(v,bi,l,l.appear!=null&&l.part!=null?"),
    ("<span>${esc(l.say)}</span></div>`).join('')+'</div>'}).join('')}",
     "<span>${esc(l.say)}</span></div>`)).join('')+'</div>'}).join('')}"),
]


def compact(M, D):
    """per video: a = added video, l = label, p = has added slides, n = what it adds, g = teacher-guide section,
    k = lesson / solution / summary, s = {slide: [title, label, kind, note, guide]},
    L = {slide: {t: title, n: note, c: count, s: [said lines], d: [drawn lines], i: [board item indexes]}}."""
    out = {}
    for vid, r in M.items():
        v = D['videos'][vid]
        s = {str(k): [x['title'], x['label'], x['kind'], x.get('note') or '', x.get('guide') or ''] for k, x in r['slides'].items()}
        e = {'a': 1 if r['added'] else 0, 'l': r['label'], 'p': 1 if any(x['kind'] == 'new' for x in r['slides'].values()) else 0, 's': s}
        if r['added']:
            e['n'] = r.get('note') or ''
            e['k'] = 'solution' if (v.get('kind') == 'solution' or v.get('questionId')) else 'summary' if 'summary' in (v.get('title') or '').lower() else 'lesson'
            if r.get('guide'): e['g'] = r['guide']
        L = {}
        for k, x in r['lines'].items():
            b = v['beats'][k]; ls = b.get('lines') or []
            L[str(k)] = {'t': b.get('title'), 'n': x.get('note') or '', 'c': len(x['say']) + len(x['draw']) + len(x['items']),
                         's': [ls[i]['say'] for i in x['say']], 'd': [ls[i]['draw'] for i in x['draw']], 'i': x['items']}
        if L: e['L'] = L
        out[vid] = e
    return out


def apply(s, M, D):
    for old, new in REPL:
        assert s.count(old) == 1, ('studio_added anchor', s.count(old), old[:60])
        s = s.replace(old, new)
    k = s.find('async function startRecording(){')
    assert k > 0
    data = json.dumps(compact(M, D), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return s[:k] + JS.replace('__ADDED__', data).lstrip() + s[k:]
