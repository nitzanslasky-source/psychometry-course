"""Recorded videos turn green in the studio's course navigation (applied by build_verbal.py last).

- Build time: every take in ~/Documents/Course.recordings (<Subject>/<Topic>/<videoId>-<ISO time>.mp4|webm) gives its
  video id; the ids are embedded as window.RECORDED_IDS, so the colours show even without folder permission.
- Live: on load, if the recordings folder (IndexedDB 'studio-rec-folder') already has permission, the folder is listed
  again WITHOUT asking; every saved take (Keep, an edited take, a continued take) marks its video at once. Ids marked
  live are also remembered in localStorage until the next build picks them up from the folder.
- 2026-10-11 AI redo (math_patches/_ai_redo.py): takes of the recorded math videos that are redone (all but the first
  lessons kept as recorded) no longer count: takes() leaves them out, the nav shows a purple "AI redo" tag (no green, not
  counted, like the AI videos; studio_ai adds them to AI_VIDEOS) and the first lessons to re-record on camera show red
  (studio_rerecord). A take recorded after _ai_redo.CUTOFF counts again. No file is moved or deleted.
- Display (studio UI only, never the board/canvas that is recorded): a recorded video's nav item gets a green bar and a
  ✓; AI-narrated videos (studio_ai AI_VIDEOS) get a purple "AI" tag and are not counted; each topic shows
  "7/11 recorded" and turns green when all its videos are done; the current video's title gets a "✓ Recorded" chip.
"""
import json, os, re

ROOT = os.path.expanduser('~/Documents/Course.recordings')
TAKE = re.compile(r'^(.+)-(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z)\.(mp4|webm)$')


def ai_redo():
    """math_patches/_ai_redo.py (shared module): recorded math videos redone with the AI voice."""
    import math_api
    return math_api.load_ai_redo()


def takes(root=ROOT, all=False):
    """(videoId, time stamp 'YYYY-MM-DDTHH-MM-SS-mmmZ') of every teacher take in the recordings folder.
    2026-10-11: a take of an AI redo video (math_patches/_ai_redo.py) recorded before its CUTOFF is obsolete and left
    out - the video counts as unrecorded (it is redone with the AI voice). all=True lists every file."""
    AR = None if all else ai_redo()
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if not d.startswith(('_', '.'))]   # _ai_audio etc. are not teacher takes
        for f in fn:
            m = TAKE.match(f)
            if m and not (AR and AR.obsolete(m.group(1), m.group(2))):
                yield m.group(1), m.group(2)


def recorded_ids(root=ROOT):
    return sorted({vid for vid, ts in takes(root)})


JS = r"""
/* ---- recorded videos turn green in the course navigation (studio UI only, not recorded) ---- */
window.RECORDED_IDS=__REC_IDS__;
/* 2026-10-11 AI redo (math_patches/_ai_redo.py): takes of these recorded math videos made before CUT are obsolete (the
   video is redone with the AI voice, or - CAMERA - re-recorded on camera with the new content); a newer take counts */
window.AI_REDO=__AI_REDO__;
var AIR_ALL=new Set(window.AI_REDO.all),AIR_AI=new Set(window.AI_REDO.ai);
function recObsolete(name){const m=String(name).match(/^(.+)-(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})/);return !!m&&AIR_ALL.has(m[1])&&m[2]<window.AI_REDO.cut}
var RECD=new Set(window.RECORDED_IDS);   // var: render() may run before this line (then RECD is undefined and painting waits)
try{for(const id of JSON.parse(localStorage.getItem('studio-recorded-ids')||'[]'))if(!AIR_ALL.has(id))RECD.add(id)}catch{}   // AI redo ids: only a new take (folder scan) counts
function recIsAI(id){return typeof AI_VIDEOS!=='undefined'&&AI_VIDEOS.has(id)}
function recIsRedo(id){return AIR_AI.has(id)}
function recIsPlanned(id){return !!window.AI_PLANNED&&window.AI_PLANNED.has(id)}
(()=>{const st=document.createElement('style');st.textContent=`
.nav-item.rec{background:#ecfdf3;box-shadow:inset 3px 0 0 #16a34a}.nav-item.rec.active{background:#d1fae5;color:#065f46}
.nav-item.rec .nav-symbol{color:#16a34a;font-weight:800}
.nav-item.ai-vid{box-shadow:inset 3px 0 0 #c4b5fd}
.rec-tag{margin-left:auto;flex:none;align-self:center;font-size:.6875rem;font-weight:800;line-height:1;padding:3px 6px;border-radius:999px}
.rec-tag.ok{background:#16a34a;color:#fff}.rec-tag.ai{background:#ede9fe;color:#5b21b6}.rec-tag.ai.redo{background:#ddd6fe;color:#4c1d95;white-space:nowrap}
.rec-count{margin-left:auto;flex:none;font-size:.6875rem;font-weight:700;color:#8390a5;padding:2px 7px;border-radius:999px;background:#f1f4f9;white-space:nowrap;align-self:center}
.rec-count.some{color:#166534;background:#dcfce7}.rec-count.all{color:#fff;background:#16a34a}
.topic-group.rec-all>summary{color:#166534}.topic-group.rec-all .topic-number{color:#16a34a}
.rec-chip{display:inline-block;vertical-align:middle;margin-left:12px;font-size:.8125rem;font-weight:800;color:#166534;background:#dcfce7;border:1px solid #86efac;border-radius:999px;padding:3px 10px;letter-spacing:0}
.rec-chip.ai{color:#5b21b6;background:#ede9fe;border-color:#c4b5fd}`;document.head.append(st)})();
function recChip(r){if(!RECD||typeof STUDIO==='undefined'||!STUDIO||!r||r.type!=='video')return '';
 return recIsPlanned(r.ref)?'<span class="rec-chip ai" title="Planned for your AI voice (decision 2026-10-11: only the first lesson of each math topic is on camera). Nothing to record.">🤖 AI (planned)</span>':recIsRedo(r.ref)?'<span class="rec-chip ai" title="You recorded this one; it is redone with your AI voice so all math videos match (decision 2026-10-11). Nothing to record.">🤖 AI redo</span>':recIsAI(r.ref)?'<span class="rec-chip ai">🤖 AI voice</span>':RECD.has(r.ref)?'<span class="rec-chip">✓ Recorded</span>':''}
function recPaint(){if(!RECD||typeof STUDIO==='undefined'||!STUDIO)return;const nav=$('#course-nav');if(!nav)return;
 nav.querySelectorAll('[data-go]').forEach(b=>{const r=D.flow[+b.dataset.go];if(!r||r.type!=='video')return;
  const ai=recIsAI(r.ref),ok=!ai&&RECD.has(r.ref);b.classList.toggle('rec',ok);b.classList.toggle('ai-vid',ai);
  let t=b.querySelector('.rec-tag');if(!ok&&!ai){t?.remove();return}
  if(!t){t=document.createElement('span');b.append(t)}const rd=ai&&recIsRedo(r.ref),pl=ai&&recIsPlanned(r.ref);t.className='rec-tag '+(ai?'ai':'ok')+(rd||pl?' redo':'');t.textContent=rd?'AI redo':pl?'AI (planned)':ai?'AI':'✓';
  t.title=pl?'Planned for your AI voice (2026-10-11: only the first lesson of each math topic is on camera) — nothing to record':rd?'You recorded this one; it is redone with your AI voice (2026-10-11) — nothing to record':ai?'Narrated by your AI voice — no need to record':'Recorded';if(ok)b.querySelector('.nav-symbol').textContent='✓'});
 const groups=nav.querySelectorAll('.topic-group');D.topics.forEach((tp,k)=>{const g=groups[k];if(!g)return;
  const vids=[...new Set(D.flow.filter(r=>r.type==='video'&&r.topic===tp.id&&!recIsAI(r.ref)).map(r=>r.ref))],n=vids.filter(id=>RECD.has(id)).length;
  const sum=g.querySelector('summary');let c=sum.querySelector('.rec-count');g.classList.toggle('rec-all',vids.length>0&&n===vids.length);
  if(!vids.length){c?.remove();return}if(!c){c=document.createElement('span');sum.append(c)}
  c.className='rec-count'+(n===vids.length?' all':n?' some':'');c.textContent=n+'/'+vids.length+(n===vids.length?' ✓':' recorded');
  c.title=n+' of '+vids.length+' videos in this topic recorded'+(n===vids.length?' — all done':'')});
 const h=document.querySelector('#main .item-heading h1');if(h){h.querySelector('.rec-chip')?.remove();const html=recChip(item());if(html&&state.view==='item')h.insertAdjacentHTML('beforeend',html)}}
function recMark(id){if(!id||!RECD||RECD.has(id))return;RECD.add(id);
 try{const a=JSON.parse(localStorage.getItem('studio-recorded-ids')||'[]');if(!a.includes(id)){a.push(id);localStorage.setItem('studio-recorded-ids',JSON.stringify(a))}}catch{}
 recPaint()}
async function recScanFolder(){try{if(!window.showDirectoryPicker)return;const h=RF.handle||await rfGet();if(!h)return;
  if((await h.queryPermission({mode:'readwrite'}))!=='granted'&&(await h.queryPermission({mode:'read'}))!=='granted')return;   // never prompts
  let added=0;const walk=async(d,depth)=>{for await(const [n,x] of d.entries()){if(n.startsWith('_')||n.startsWith('.'))continue;
   if(x.kind==='directory'){if(depth<3)await walk(x,depth+1)}else{if(recObsolete(n))continue;const m=n.match(/^(.+)-\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z\.(mp4|webm)$/);if(m&&!RECD.has(m[1])){RECD.add(m[1]);added++}}}};
  await walk(h,0);if(added)recPaint()}catch(e){console.warn('recorded scan',e)}}
window.recMarkRecorded=recMark;   // (also handy from the console)
setTimeout(()=>{recPaint();recScanFolder()},800);
"""

REPL = [
    # repaint after every nav render
    ("$('#course-nav').querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>go(+b.dataset.go));}",
     "$('#course-nav').querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>go(+b.dataset.go));recPaint();}"),
    # chip next to the current video's title
    ("<h1>${esc(name)}</h1>", "<h1>${esc(name)}${recChip(r)}</h1>"),
    # a saved take (Keep / edited / continued) marks its video recorded as soon as the file is written
    ("async function saveTakeFile(v,name,blob){",
     "async function saveTakeFile(v,name,blob){const res=await saveTakeFile0(v,name,blob);if(/\\.(mp4|webm)$/.test(name))recMark(v.id);return res}\n"
     "async function saveTakeFile0(v,name,blob){"),
]


def apply(s):
    for old, new in REPL:
        assert s.count(old) == 1, ('studio_done anchor', s.count(old), old[:60])
        s = s.replace(old, new)
    k = s.find('async function startRecording(){')
    assert k > 0
    ids = recorded_ids()
    AR = ai_redo()
    raw = sorted({vid for vid, ts in takes(all=True)})
    unk = AR.check(list(takes(all=True)))
    if unk: print('  studio_done WARNING: takes before the AI-redo CUTOFF of videos in neither _ai_redo.KEEP nor AI_REDO: %s' % unk)
    air = {'cut': AR.CUTOFF, 'all': sorted(AR.AI_REDO), 'ai': sorted(v for v in AR.AI_REDO if AR.ai_redo(v))}
    print('studio_done: %d recorded video ids from %s (%d with takes; %d AI redo = %d AI voice + %d re-record on camera, old takes ignored)'
          % (len(ids), ROOT, len(raw), len(AR.AI_REDO), len(air['ai']), len(AR.AI_REDO) - len(air['ai'])))
    return s[:k] + JS.replace('__REC_IDS__', json.dumps(ids)).replace('__AI_REDO__', json.dumps(air)).lstrip() + s[k:]
