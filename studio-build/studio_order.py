"""Two navigation orders in the studio: by topic (as before) or by the students' study plan (applied by build_verbal.py
LAST, after studio_added).

Teacher request (2026-10-07): "Maybe the studio should have two set-ups: one by the order of the topics like now, and
one by the order in which students learn it - so when I record I'll have in mind what they already learned."

The study order is NOT copied here: it is parsed at build time from ORDER in ../src/lib/planData.ts (the student site's
plan), with the "day N" comments. The build fails if that list cannot be parsed. As in getPlanData(): [t] = the whole
topic; [t, "prefix"] = a PART of the topic, from its first item whose id starts with the prefix up to the first item of
the next listed part of the same topic (cards / workshops / questions in between go with it); a part that does not
exist is skipped; topics missing from the list are added at the end (subject order of the student site).

Studio UI only (never the board / canvas that is recorded, never file names or recorded marks):
- Sidebar, under "Jump to a subject": "Order: By topic | By study plan" (remembered in localStorage).
  By topic = the navigation exactly as before. By study plan = the same nav items, grouped by plan entry (writing-task
  and chart parts are separate groups, e.g. 50b / 52c), with day headers from the plan comments and "plan #n" on each
  group; the green recorded counts (studio_done) and "N new" tags (studio_added) count each group's own videos.
- Under the title of the current video: "Study plan #n · Day d · Students learned before this (k): 1, 30, 2 ..." (a
  drop-down lists them with titles) and "Comes next in the plan: <topic>".
- "By study plan" also makes Previous / Next item, the Previous / Next strip and the studio's "Next video" preview
  follow the plan (inside a topic the order is the same; only the jumps between topics change).
"""
import json, os, re

PLAN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'lib', 'planData.ts')
# subject order of the student site (export_student.SUBJECTS): unlisted topics are appended in this order
SUBJECT_ORDER = [[51], list(range(1, 21)), list(range(21, 30)), list(range(30, 39)), [52], list(range(39, 51))]

ENTRY = re.compile(r'\[\s*(\d+)\s*(?:,\s*"([^"]+)"\s*)?\]')


def parse_plan(path=PLAN):
    """[(topic, part or None, day label or None)] from `const ORDER ... = [ ... ];` in planData.ts. Raises on anything odd."""
    src = open(path, encoding='utf-8').read()
    m = re.search(r'const ORDER\s*:[^=]*=\s*\[\s*\n(.*?)\n\];', src, re.S)
    if not m:
        raise SystemExit('studio_order: cannot find "const ORDER ... = [ ... ];" in %s' % path)
    out = []
    for ln in m.group(1).split('\n'):
        code, _, com = ln.partition('//')
        if not code.strip():
            if com.strip(): continue          # comment-only line
            continue
        rest = ENTRY.sub('', code).replace(',', '').strip()
        if rest:
            raise SystemExit('studio_order: cannot parse ORDER line in %s: %r (left over: %r)' % (path, ln, rest))
        d = re.search(r'\b(days?)\s+(\d+(?:\s*[-–]\s*\d+)?)', com, re.I)
        day = ('Days ' if d.group(1).lower() == 'days' else 'Day ') + re.sub(r'\s*[-–]\s*', '–', d.group(2)) if d else None
        pd = re.search(r'\([^)]*:\s*day\s+(\d+)\s*\)', com, re.I)   # "(charts lessons + units 1-5: day 24)" -> the line's parts
        for e in ENTRY.finditer(code):
            t, part = int(e.group(1)), e.group(2)
            out.append((t, part, ('Day ' + pd.group(1)) if (part and pd) else day))
    if len(out) < 10:
        raise SystemExit('studio_order: only %d entries parsed from ORDER in %s' % (len(out), path))
    return out


def plan_spec(D, path=PLAN):
    """The plan as [[topic, part|null, day|null], ...] for the studio, checked against the course; + warnings."""
    tids = [t['id'] for t in D['topics']]
    warn, spec = [], []
    for t, part, day in parse_plan(path):
        if t not in tids:
            warn.append('topic %d (in the plan) is not in the studio' % t); continue
        if part and not any(r['topic'] == t and r['ref'].startswith(part) for r in D['flow']):
            warn.append('part [%d, "%s"] matches no item - skipped (as on the site)' % (t, part)); continue
        spec.append([t, part, day])
    listed = {t for t, _, _ in spec}
    for grp in SUBJECT_ORDER:
        for t in grp:
            if t in tids and t not in listed: spec.append([t, None, None]); listed.add(t)
    for t in tids:
        if t not in listed: spec.append([t, None, None])
    return spec, warn


JS = r"""
/* ---- navigation order: by topic | by the students' study plan (studio UI only, never recorded) ---- */
var ORD_SPEC=__ORD_SPEC__;
var ORD=null;
function ordBuild(){if(ORD)return ORD;const groups=[],range={};
 D.flow.forEach((r,i)=>{const x=range[r.topic];if(!x)range[r.topic]=[i,i+1];else x[1]=i+1});
 const parts={};ORD_SPEC.forEach(([t,p])=>{if(p)(parts[t]=parts[t]||[]).push(p)});
 const at=(t,p)=>{const x=range[t];if(!x)return -1;for(let i=x[0];i<x[1];i++)if(D.flow[i].ref.startsWith(p))return i;return -1};
 ORD_SPEC.forEach(([t,p,day])=>{const x=range[t];if(!x)return;let a=x[0],b=x[1],k='';
  if(p){a=at(t,p);if(a<0)return;const ps=parts[t],later=ps.slice(ps.indexOf(p)+1).map(q=>at(t,q)).filter(j=>j>a);if(later.length)b=Math.min(...later);
   k=String.fromCharCode(97+ps.indexOf(p))}
  const tp=D.topics.find(z=>z.id===t);let name=tp.title;
  if(p){const vs=[],sets=[];for(let i=a;i<b;i++){const r=D.flow[i];if(r.type==='video'&&!D.videos[r.ref].questionId&&D.videos[r.ref].kind!=='solution')vs.push(D.videos[r.ref].title);
    const m=r.type==='question'&&sectionMap.get(r.section)?.kind==='practice'&&r.ref.match(/(\d+)-q\d+$/);if(m)sets.push(+m[1])}
   const bits=[];if(vs.length)bits.push(vs[0]+(vs.length>1?' … '+vs[vs.length-1]:''));if(sets.length)bits.push('practice sets '+Math.min(...sets)+'–'+Math.max(...sets));
   name=tp.title+' · '+(bits.join(' + ')||'part '+k.toUpperCase())}
  groups.push({t,p,k,day,a,b,num:t+k,name,n:groups.length+1})});
 const seq=[],pos=new Map(),grp=new Map();groups.forEach((g,gi)=>{for(let i=g.a;i<g.b;i++){if(pos.has(i))continue;pos.set(i,seq.length);seq.push(i);grp.set(i,gi)}});
 return ORD={groups,seq,pos,grp}}
function ordMode(){try{return localStorage.getItem('studio-nav-order')==='plan'?'plan':'topic'}catch{return 'topic'}}
function ordPlan(){return typeof STUDIO!=='undefined'&&STUDIO&&ordMode()==='plan'}
/* the flow index d steps away (d = -1 / 1) in the chosen order; by topic = state.index + d, exactly as before */
function ordIdx(d){const i=state.index+d;if(!ordPlan())return i;const O=ordBuild(),p=O.pos.get(state.index);if(p==null)return i;const j=O.seq[p+d];return j==null?(d<0?-1:D.flow.length):j}
(()=>{const st=document.createElement('style');st.textContent=`
.ord-toggle{display:flex;align-items:center;gap:0;margin:10px 0 2px;font-size:12px}
.ord-toggle .ord-lab{color:var(--muted);font-weight:700;margin-right:8px}
.nav-top .ord-toggle button{width:auto;flex:1;text-align:center;border:1px solid var(--line);background:#fff;color:var(--ink);padding:6px 6px;font:inherit;font-size:12px;font-weight:700;cursor:pointer;border-radius:0}
.nav-top .ord-toggle button:first-of-type{border-radius:8px 0 0 8px}.nav-top .ord-toggle button:last-of-type{border-radius:0 8px 8px 0;border-left:0}
.nav-top .ord-toggle button.on{background:#0f766e;border-color:#0f766e;color:#fff}
body:not(.studio-body) .ord-toggle{display:none}
.ord-dayhead{margin:14px 6px 2px;padding:3px 9px;font-size:.6875rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#0f766e;background:#ecfdf5;border-radius:6px}
.ord-pos{display:block;font-size:.6875rem;font-weight:700;color:#8390a5;margin-top:1px}.ord-pos>span{white-space:nowrap}
.topic-group.ord-part .topic-number{color:#0f766e}
.ord-line{flex-basis:100%;margin:2px 0 0;font-size:.8125rem;line-height:1.45;color:#475569;display:flex;flex-wrap:wrap;gap:4px 16px;align-items:baseline}
.ord-line .ord-where{font-weight:800;color:#0f766e;white-space:nowrap}
.ord-line details{flex:1 1 380px;min-width:0}.ord-line summary{cursor:pointer;list-style:none}.ord-line summary::-webkit-details-marker{display:none}
.ord-line summary b{color:#334155}.ord-line .ord-nums{color:#64748b}.ord-line .ord-more{color:#0f766e;font-weight:700;white-space:nowrap}
.ord-line details[open] .ord-more{display:none}
.ord-line ol{margin:6px 0 4px;padding:8px 12px;list-style:none;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:2px 24px;font-size:.78rem;max-height:300px;overflow:auto}
.ord-line li .p{display:inline-block;min-width:26px;color:#94a3b8;font-weight:700}
.ord-line li{break-inside:avoid}.ord-line li .n{font-weight:800;color:#334155;margin-right:5px}.ord-line li .d{color:#94a3b8;margin-left:4px}
.ord-line .ord-next{white-space:nowrap}.ord-line .ord-next b{color:#334155}`;document.head.append(st)})();
function ordBtn(rid){__ORD_BTN__}
function ordNavHtml(){const O=ordBuild(),cur=O.grp.get(state.index);let day=null,h='';
 O.groups.forEach((g,gi)=>{if(g.day&&g.day!==day){day=g.day;h+=`<div class="ord-dayhead">${esc(day)}</div>`}
  const tp=D.topics.find(z=>z.id===g.t);
  h+=`<details class="topic-group${g.p?' ord-part':''}" data-og="${gi}" ${gi===cur?'open':''}><summary><span class="topic-number">${g.k?g.num:String(g.t).padStart(2,'0')}</span><span>${esc(g.p?g.name:tp.title)}<span class="ord-pos" title="Position in the study plan"><span>#${g.n}</span>${g.day?' · <span>'+esc(g.day)+'</span>':''}</span></span></summary>`
   +tp.sections.map(id=>{const s=sectionMap.get(id);const its=s.items.filter(rid=>{const i=flowMap.get(rid);return i>=g.a&&i<g.b&&O.grp.get(i)===gi});
    return its.length?`<div class="section-label">${esc(s.title)}</div>`+its.map(ordBtn).join(''):''}).join('')+'</details>'});
 return h}
/* the nav groups with their topic and "is this flow row in the group" (recPaint / addPaint counts) */
function ordGroups(nav){const gs=[...nav.querySelectorAll('.topic-group')];
 if(!gs.length||gs[0].dataset.og==null)return gs.map((g,k)=>[g,D.topics[k],()=>true]).filter(x=>x[1]);   // by topic: exactly as before
 const O=ordBuild();return gs.map(g=>{const G=O.groups[+g.dataset.og];return [g,D.topics.find(z=>z.id===G.t),r=>{const i=flowMap.get(r.id);return i>=G.a&&i<G.b&&O.grp.get(i)===+g.dataset.og}]})}
function ordPaintToggle(){const m=ordMode();document.querySelectorAll('.ord-toggle [data-ord]').forEach(b=>{b.classList.toggle('on',b.dataset.ord===m);b.setAttribute('aria-pressed',b.dataset.ord===m)})}
function ordSet(m){try{localStorage.setItem('studio-nav-order',m)}catch{}
 if(record)renderNav();else render();
 setTimeout(()=>$('#course-nav .nav-item.active')?.scrollIntoView({block:'center'}),30)}
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('.ord-toggle [data-ord]');if(b)ordSet(b.dataset.ord)});
/* teacher-only line under the current video's title: what the students learned before it, what comes next */
function ordLine(r){if(typeof STUDIO==='undefined'||!STUDIO||!r||r.type!=='video')return '';const O=ordBuild(),gi=O.grp.get(state.index);if(gi==null)return '';
 const g=O.groups[gi],prev=O.groups.slice(0,gi),next=O.groups[gi+1];
 const lab=x=>x.k?x.num:String(x.t),full=x=>(x.k?x.num:String(x.t).padStart(2,'0'))+' · '+x.name+(x.day?' ('+x.day+')':'');
 const where=`<span class="ord-where" title="Position of this ${g.p?'part':'topic'} in the students' study plan (src/lib/planData.ts)">Study plan #${g.n}${g.day?' · '+esc(g.day):''}</span>`;
 const before=prev.length?`<details class="ord-before"><summary title="${esc(prev.map(full).join('\n'))}"><b>Students learned before this (${prev.length}):</b> <span class="ord-nums">${esc(prev.map(lab).join(', '))}</span> <span class="ord-more">▾ names</span></summary><ol>${prev.map(x=>`<li><span class="p">${x.n}.</span><span class="n">${esc(x.k?x.num:String(x.t).padStart(2,'0'))}</span>${esc(x.name)}${x.day?'<span class="d">'+esc(x.day)+'</span>':''}</li>`).join('')}</ol></details>`
  :'<span><b>First in the study plan</b> — students have learned nothing before this.</span>';
 const nx=next?`<span class="ord-next" title="${esc(full(next))}">Comes next in the plan: <b>${esc(next.k?next.num:String(next.t).padStart(2,'0'))} · ${esc(short(next.name,60))}</b></span>`:'<span class="ord-next">Last in the study plan.</span>';
 return `<div class="ord-line">${where}${before}${nx}</div>`}
window.studioNavOrder=()=>ordBuild();   // (handy from the console)
"""

TOGGLE = ('<div class="ord-toggle" role="group" aria-label="Navigation order"><span class="ord-lab">Order:</span>'
          '<button type="button" data-ord="topic" title="Topics 1, 2, 3 … as in the course">By topic</button>'
          '<button type="button" data-ord="plan" title="The order in which students learn it (the study plan), with the days">By study plan</button></div>')

REPL = [
    # sidebar header: the toggle under "Jump to a subject"
    ('<option value="39">Verbal reasoning</option></select>', '<option value="39">Verbal reasoning</option></select>' + TOGGLE),
    # nav: plan order (same buttons) or the topics as before
    ("$('#course-nav').innerHTML=D.topics.map(t=>", "ordPaintToggle();$('#course-nav').innerHTML=ordPlan()?ordNavHtml():D.topics.map(t=>"),
    # green recorded counts (studio_done) and "N new" counts (studio_added) per nav group
    ("const groups=nav.querySelectorAll('.topic-group');D.topics.forEach((tp,k)=>{const g=groups[k];if(!g)return;\n  const vids=[...new Set(D.flow.filter(r=>r.type==='video'&&r.topic===tp.id&&!recIsAI(r.ref))",
     "ordGroups(nav).forEach(([g,tp,inG])=>{\n  const vids=[...new Set(D.flow.filter(r=>r.type==='video'&&r.topic===tp.id&&inG(r)&&!recIsAI(r.ref))"),
    ("const groups=nav.querySelectorAll('.topic-group');D.topics.forEach((tp,k)=>{const g=groups[k];if(!g)return;const sum=g.querySelector('summary');\n  const ids=[...new Set(D.flow.filter(r=>r.type==='video'&&r.topic===tp.id&&addVid(r.ref))",
     "ordGroups(nav).forEach(([g,tp,inG])=>{const sum=g.querySelector('summary');\n  const ids=[...new Set(D.flow.filter(r=>r.type==='video'&&r.topic===tp.id&&inG(r)&&addVid(r.ref))"),
    # line under the current video's title
    ("${addChip(r)}</h1>", "${addChip(r)}</h1>${ordLine(r)}"),
    # Previous / Next strip, footer buttons, the studio's "Next video" preview follow the chosen order
    ("const i=state.index+off,r=D.flow[i]", "const i=ordIdx(off),r=D.flow[i]"),
    ("<button id=\"previous-item\" ${state.index===0?'disabled':''}>", "<button id=\"previous-item\" ${ordIdx(-1)<0?'disabled':''}>"),
    ("<button class=\"primary\" id=\"next-item\" ${state.index===D.flow.length-1?'disabled':''}>${D.flow[state.index+1]?.type==='video'&&D.videos[D.flow[state.index+1]?.ref]?.kind==='solution'",
     "<button class=\"primary\" id=\"next-item\" ${ordIdx(1)>=D.flow.length?'disabled':''}>${D.flow[ordIdx(1)]?.type==='video'&&D.videos[D.flow[ordIdx(1)]?.ref]?.kind==='solution'"),
    ("$('#previous-item').onclick=()=>go(state.index-1);", "$('#previous-item').onclick=()=>go(ordIdx(-1));"),
    ("save();go(state.index+1)};$('#mark-done')", "save();go(ordIdx(1))};$('#mark-done')"),
    ("else{const row=D.flow[state.index+1];", "else{const row=D.flow[ordIdx(1)];"),
]


def apply(s, D, path=PLAN):
    spec, warn = plan_spec(D, path)
    for w in warn: print('  studio_order WARNING:', w)
    # the nav item button of renderNav, reused as is for the plan order
    k = s.find("s.items.map(rid=>{"); e = s.find("</button>`}", k)
    assert k > 0 and e > k and s.count("s.items.map(rid=>{") == 1, 'studio_order: nav button anchor'
    body = s[k + len("s.items.map(rid=>{"): e + len("</button>`")]
    assert not re.search(r'(?<![\w.$])[ts]\.', body), ('studio_order: nav button uses the topic/section variable', body[:200])
    for old, new in REPL:
        assert s.count(old) == 1, ('studio_order anchor', s.count(old), old[:70])
        s = s.replace(old, new)
    k = s.find('async function startRecording(){')
    assert k > 0
    print('studio_order: study plan from %s - %d entries (%d parts), first: %s' % (
        os.path.relpath(path, os.path.dirname(os.path.dirname(os.path.dirname(path)))), len(spec), sum(1 for x in spec if x[1]),
        ', '.join(str(t) + ('/' + p if p else '') for t, p, _ in spec[:8])))
    js = JS.replace('__ORD_SPEC__', json.dumps(spec, ensure_ascii=False)).replace('__ORD_BTN__', body)
    return s[:k] + js.lstrip() + s[k:]
