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
.add-chip{display:inline-block;vertical-align:middle;margin-left:12px;font-size:.8125rem;font-weight:800;color:#9a3412;background:#ffedd5;border:1px solid #fdba74;border-radius:999px;padding:3px 10px;letter-spacing:0}
.add-chip.new{color:#fff;background:#ea580c;border-color:#ea580c}
.add-banner{margin:12px 20px 4px;padding:10px 14px;border-radius:10px;background:#fff7ed;border:2px solid #fb923c;color:#7c2d12;font-size:15px;line-height:1.4;font-weight:600}
.add-banner b{color:#c2410c}.add-banner .add-why{display:block;font-weight:500;color:#9a3412;margin-top:3px;font-size:14px}
.add-banner.lines{border-style:dashed;background:#fffbeb}
.sb-head:has(.add-sb){flex-wrap:wrap;opacity:1}
.sb-head .add-sb{flex:1 0 100%;order:5;margin:4px 0 0;padding:5px 10px;border-radius:7px;background:#ea580c;color:#fff;font-size:15px;font-weight:700;letter-spacing:0;line-height:1.3;text-align:left}
.sb-head .add-sb.lines{background:#fff7ed;color:#9a3412}`;document.head.append(st)})();
function addVid(id){return ADDED&&ADDED[id]||null}
function addSlide(v,k){const m=v&&addVid(v.id);if(!m)return null;const b=v.beats[k];if(!b)return null;
 const s=m.s[k];if(s&&s[0]===b.title)return s;
 for(const x of Object.values(m.s))if(x[0]===b.title)return x;   // slides moved in the script editor: match by title
 return null}
function addBannerHtml(v,k){const s=addSlide(v,k);if(!s)return '';const lines=s[2]==='lines',meth=/^New exam method/.test(s[1]);
 return `<div class="add-banner${lines?' lines':''}" data-added="1">⚠ <b>${lines?'New lines on this slide':'Added slide'}</b> — ${esc(s[1])}.`
  +`<span class="add-why">${lines?'Your slide, with new lines for this method: read the new lines carefully':'Not from your Hebrew course: read the script carefully'}${meth?' (see the teacher guide)':''}.</span></div>`}
function addSbBanner(v,k){const s=addSlide(v,k);if(!s)return '';const lines=s[2]==='lines';
 return `<div class="add-sb${lines?' lines':''}" title="${lines?'Your slide, with new lines for this method':'Not from your Hebrew course'} — read the script carefully">⚠ ${lines?'New lines on this slide':'Added slide'} — ${esc(s[1])} · read carefully</div>`}
function addPaintSlide(){if(typeof STUDIO==='undefined'||!STUDIO)return;const v=video();const cp=$('#script-copy');if(!cp)return;
 cp.parentElement.querySelector(':scope > .add-banner')?.remove();if(!v)return;const h=addBannerHtml(v,state.beat);if(h)cp.insertAdjacentHTML('beforebegin',h)}   // above the scrolling script, so it stays in view
function addPaint(){if(!ADDED||typeof STUDIO==='undefined'||!STUDIO)return;const nav=$('#course-nav');if(!nav)return;
 nav.querySelectorAll('[data-go]').forEach(b=>{const r=D.flow[+b.dataset.go];const m=r&&r.type==='video'?addVid(r.ref):null;let t=b.querySelector('.add-tag');
  if(!m){t?.remove();return}
  if(!t){t=document.createElement('span');const rt=b.querySelector('.rec-tag');rt?b.insertBefore(t,rt):b.append(t)}
  t.className='add-tag '+(m.a?'new':'part');t.textContent=m.a?'NEW':(m.p?'+ new slides':'+ new lines');t.title=(m.a?'Added video — ':'Added inside this video — ')+m.l+' · read the script carefully'});
 const groups=nav.querySelectorAll('.topic-group');D.topics.forEach((tp,k)=>{const g=groups[k];if(!g)return;const sum=g.querySelector('summary');
  const ids=[...new Set(D.flow.filter(r=>r.type==='video'&&r.topic===tp.id&&addVid(r.ref)).map(r=>r.ref))];let c=sum.querySelector('.add-count');
  if(!ids.length){c?.remove();return}if(!c){c=document.createElement('span');const rc=sum.querySelector('.rec-count');rc?sum.insertBefore(c,rc):sum.append(c)}
  const nv=ids.filter(id=>ADDED[id].a).length;c.textContent=ids.length+' new';c.title=nv+' added videos, '+(ids.length-nv)+' of your videos with added slides or lines'});
 }
function addChip(r){const m=typeof STUDIO!=='undefined'&&STUDIO&&r&&r.type==='video'?addVid(r.ref):null;if(!m)return '';
 return `<span class="add-chip${m.a?' new':''}" title="${esc(m.l)} · read the script carefully">${m.a?'NEW · '+esc(m.l):(m.p?'+ new slides':'+ new lines')}</span>`}
function addStar(v,k){return typeof STUDIO!=='undefined'&&STUDIO&&addSlide(v,k)?'★ ':''}
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
]


def compact(M):
    out = {}
    for vid, r in M.items():
        s = {str(k): [x['title'], x['label'], x['kind']] for k, x in r['slides'].items()}
        out[vid] = {'a': 1 if r['added'] else 0, 'l': r['label'], 'p': 1 if any(x['kind'] == 'new' for x in r['slides'].values()) else 0, 's': s}
    return out


def apply(s, M):
    for old, new in REPL:
        assert s.count(old) == 1, ('studio_added anchor', s.count(old), old[:60])
        s = s.replace(old, new)
    k = s.find('async function startRecording(){')
    assert k > 0
    data = json.dumps(compact(M), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return s[:k] + JS.replace('__ADDED__', data).lstrip() + s[k:]
