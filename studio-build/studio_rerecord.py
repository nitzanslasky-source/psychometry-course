"""Videos to RE-RECORD are marked in the studio (applied by build_verbal.py LAST, after studio_order).

The list is math_patches/_rerecord.py: RERECORD[video id] = dict(topic, option 1|2|3, reason, added, minutes, since).
`since` (UTC) is when the change went into the course; without it the file's modification time is used.
A take recorded AFTER `since` counts as done (the video turns green again as usual).

Build time: the list + the latest take time of each listed video (studio_done.takes) are embedded.
Live: the folder scan of studio_done (no prompt) and every saved take (Keep / edited / continued) update the latest take
time; times seen live are remembered in localStorage until the next build reads them from the folder.

Display (studio UI only - never the board / canvas that is recorded):
- Course navigation: a listed video whose latest take is OLDER than its entry loses the green bar / ✓ and gets a red
  "⟳ re-record" tag (option 2: "⟳ continue at end"); the topic count reads "5/7 recorded · 2 to redo".
  Option 3 (a NEW video after a recorded one) leaves the recorded video green.
- Video heading: a red chip instead of "✓ Recorded" and a red banner "⟳ Re-record: <what changed>" (option 2:
  "Continue this take at the end: <what was added> — use ⤴ Continue a take"); the same banner sits above the script
  panel and in the head of the on-board script strip.
"""
import json, os, re, sys, datetime

import studio_done

HERE = os.path.dirname(os.path.abspath(__file__))
LIST = os.path.join(HERE, 'math_patches', '_rerecord.py')


def _ts(since):
    """'2026-10-08T07:50Z' / '...:00Z' / '...:00.000Z' -> take-file format 'YYYY-MM-DDTHH-MM-SS-mmmZ'."""
    m = re.match(r'^(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d{1,3}))?)?Z$', since.strip())
    if not m:
        raise SystemExit('studio_rerecord: bad since %r (want e.g. 2026-10-08T07:50Z, UTC)' % since)
    return '%sT%s-%s-%s-%sZ' % (m.group(1), m.group(2), m.group(3), m.group(4) or '00', (m.group(5) or '000').ljust(3, '0'))


def load_list(path=LIST):
    ns = {}
    exec(compile(open(path, encoding='utf-8').read(), path, 'exec'), ns)
    R = ns['RERECORD']
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path), datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    return R, mtime


def data(D, root=studio_done.ROOT):
    R, mtime = load_list()
    latest = {}
    for vid, ts in studio_done.takes(root):
        if vid in R and ts > latest.get(vid, ''): latest[vid] = ts
    out, warn = {}, []
    for vid, e in R.items():
        if vid not in D['videos']:
            warn.append('%s (in _rerecord.py) is not a video in the studio' % vid); continue
        if not e.get('since'): warn.append('%s has no since - using the file time %s' % (vid, mtime))
        out[vid] = {'o': int(e.get('option', 1)), 't': e.get('topic'), 'r': e.get('reason') or '', 'w': e.get('added') or '',
                    'm': e.get('minutes'), 's': _ts(e.get('since') or mtime)}
    return out, latest, warn


JS = r"""
/* ---- videos to re-record (math_patches/_rerecord.py) are marked in the studio UI only (never recorded) ---- */
var RR=__RR__;
var RR_LATEST=__RR_LATEST__;   // latest take per listed video, 'YYYY-MM-DDTHH-MM-SS-mmmZ' (build time + live)
try{const x=JSON.parse(localStorage.getItem('studio-rerecord-latest')||'{}');for(const k in x)if(RR[k]&&x[k]>(RR_LATEST[k]||''))RR_LATEST[k]=x[k]}catch{}
(()=>{const st=document.createElement('style');st.textContent=`
.rec-tag.rr{background:#dc2626;color:#fff;white-space:nowrap}
.nav-item.rr-due{box-shadow:inset 3px 0 0 #dc2626}
.nav-item.rr-due{flex-wrap:wrap;row-gap:5px}.nav-item.rr-due .nav-copy{flex:1 1 calc(100% - 30px);min-width:0}   /* the tags go on their own row, so the title stays readable */.nav-item.rr-due .nav-symbol{color:#dc2626;font-weight:800}
.add-tag+.rec-tag.rr{margin-left:5px}
.rec-count .rr-n{color:#b91c1c;font-weight:800}.rec-count.redo{background:#fee2e2;color:#7f1d1d}
.rec-chip.rr{color:#fff;background:#dc2626;border-color:#dc2626}
.rr-banner{margin:12px 20px 4px;padding:10px 14px;border-radius:10px;background:#fef2f2;border:2px solid #dc2626;color:#7f1d1d;font-size:15px;line-height:1.4;font-weight:600}
.rr-banner b{color:#b91c1c}.rr-banner .rr-why{display:block;font-weight:500;color:#991b1b;margin-top:3px;font-size:13px}
.item-heading .rr-banner{margin:8px 0 2px;flex-basis:100%}
.sb-head:has(.rr-sb){flex-wrap:wrap;opacity:1}
.sb-head .rr-sb{flex:1 0 100%;order:4;margin:4px 0 0;padding:5px 10px;border-radius:7px;background:#dc2626;color:#fff;font-size:15px;font-weight:700;letter-spacing:0;line-height:1.3;text-align:left}`;document.head.append(st)})();
function rrOn(){return typeof STUDIO!=='undefined'&&STUDIO}
/* listed, has a take, and the latest take is older than the entry (option 3 = new video after it: the old one stays done) */
function rrStale(id){const e=RR[id];if(!e||e.o===3)return false;const t=RR_LATEST[id];return !!t&&t<=e.s}
function rrLabel(e){return e.o===2?'⟳ continue at end':'⟳ re-record'}
function rrTip(e){return (e.o===2?'Continue this take at the end (⤴ Continue a take): ':'Re-record: ')+e.w+'\nWhy: '+e.r}
/* nav item: red tag instead of the green ✓ (true = handled) */
function rrTag(b,id){b.classList.toggle('rr-due',rrStale(id));if(!rrStale(id))return false;const e=RR[id];
 let t=b.querySelector('.rec-tag');if(!t){t=document.createElement('span');b.append(t)}t.className='rec-tag rr';t.textContent=rrLabel(e);t.title=rrTip(e);
 b.querySelector('.nav-symbol').textContent='⟳';return true}
function rrChip(id){const e=RR[id];return `<span class="rec-chip rr" title="${esc(rrTip(e))}">${rrLabel(e)}</span>`}
function rrText(e){return e.o===2?['Continue this take at the end:',e.w,'Use ⤴ Continue a take from the old last slide.']
 :['⟳ Re-record:',e.w,'Your take is older than this change — record the whole video again.']}
function rrBanner(id,cls){if(!rrOn()||!rrStale(id))return '';const e=RR[id],[h,w,how]=rrText(e);
 return `<div class="rr-banner ${cls||''}" data-rr="1"><b>${esc(h)}</b> ${esc(w)}<span class="rr-why">Why: ${esc(e.r)} · ${esc(how)}</span></div>`}
function rrLine(r){return r&&r.type==='video'?rrBanner(r.ref,'rr-head'):''}
function rrSbBanner(v){if(!rrOn()||!v||!rrStale(v.id))return '';const e=RR[v.id],[h,w]=rrText(e);
 return `<div class="rr-sb" title="${esc(rrTip(e))}">${esc(h)} ${esc(w)}</div>`}
function rrPaintSlide(){if(!rrOn())return;const cp=$('#script-copy');if(!cp)return;cp.parentElement.querySelectorAll(':scope > .rr-banner').forEach(x=>x.remove());
 const v=video();if(!v)return;const h=rrBanner(v.id);if(!h)return;const first=cp.parentElement.querySelector(':scope > .add-banner, :scope > .add-what');(first||cp).insertAdjacentHTML('beforebegin',h)}
/* a take of id with time ts was seen (folder scan / saved now); true when it is newer than what we knew */
function rrSeen(id,ts){if(!RR[id]||!ts||ts<=(RR_LATEST[id]||''))return false;const was=rrStale(id);RR_LATEST[id]=ts;
 try{const x=JSON.parse(localStorage.getItem('studio-rerecord-latest')||'{}');x[id]=ts;localStorage.setItem('studio-rerecord-latest',JSON.stringify(x))}catch{}
 if(was&&!rrStale(id)){document.querySelectorAll('.rr-head,.rr-sb').forEach(x=>x.remove());rrPaintSlide()}return true}
window.RERECORD=RR;
setTimeout(rrPaintSlide,950);
"""

REPL = [
    # nav item: a stale listed video is not green; red tag instead
    ("const ai=recIsAI(r.ref),ok=!ai&&RECD.has(r.ref);", "const ai=recIsAI(r.ref),ok=!ai&&RECD.has(r.ref)&&!rrStale(r.ref);"),
    ("let t=b.querySelector('.rec-tag');if(!ok&&!ai){t?.remove();return}",
     "let t=b.querySelector('.rec-tag');if(rrTag(b,r.ref))return;if(!ok&&!ai){t?.remove();return}"),
    # topic count: stale ones are not counted as recorded, "· 2 to redo"
    ("n=vids.filter(id=>RECD.has(id)).length;", "n=vids.filter(id=>RECD.has(id)&&!rrStale(id)).length,nr=vids.filter(rrStale).length;"),
    ("c.className='rec-count'+(n===vids.length?' all':n?' some':'');c.textContent=n+'/'+vids.length+(n===vids.length?' ✓':' recorded');",
     "c.className='rec-count'+(n===vids.length?' all':n?' some':'')+(nr?' redo':'');c.innerHTML=n+'/'+vids.length+(n===vids.length?' ✓':' recorded')+(nr?' <span class=\"rr-n\">· '+nr+' to redo</span>':'');"),
    ("c.title=n+' of '+vids.length+' videos in this topic recorded'+(n===vids.length?' — all done':'')",
     "c.title=n+' of '+vids.length+' videos in this topic recorded'+(n===vids.length?' — all done':'')+(nr?'\\n'+nr+' recorded before a change: re-record / continue (red ⟳)':'')"),
    # heading chip
    ("RECD.has(r.ref)?'<span class=\"rec-chip\">✓ Recorded</span>'", "rrStale(r.ref)?rrChip(r.ref):RECD.has(r.ref)?'<span class=\"rec-chip\">✓ Recorded</span>'"),
    # banner under the heading
    ("${addChip(r)}</h1>${ordLine(r)}", "${addChip(r)}</h1>${rrLine(r)}${ordLine(r)}"),
    # banner above the script panel
    ("$('#script-title').textContent=b.title;addPaintSlide();", "$('#script-title').textContent=b.title;addPaintSlide();rrPaintSlide();"),
    # on-board script strip
    ("${addSbBanner(v,state.beat)}</div>`+hyPrompter(", "${rrSbBanner(v)}${addSbBanner(v,state.beat)}</div>`+hyPrompter("),
    # live: a saved take marks the time (also when the video was already recorded) and repaints
    ("function recMark(id){if(!id||!RECD||RECD.has(id))return;",
     "function recMark(id){if(id)rrSeen(id,new Date().toISOString().replace(/[:.]/g,'-'));if(!id||!RECD)return;if(RECD.has(id)){recPaint();return}"),
    # live: the folder scan reads each take's time
    ("const m=n.match(/^(.+)-\\d{4}-\\d{2}-\\d{2}T\\d{2}-\\d{2}-\\d{2}-\\d{3}Z\\.(mp4|webm)$/);if(m&&!RECD.has(m[1])){RECD.add(m[1]);added++}",
     "const m=n.match(/^(.+)-(\\d{4}-\\d{2}-\\d{2}T\\d{2}-\\d{2}-\\d{2}-\\d{3}Z)\\.(mp4|webm)$/);if(m){if(rrSeen(m[1],m[2]))added++;if(!RECD.has(m[1])){RECD.add(m[1]);added++}}"),
]


def apply(s, D):
    RRD, latest, warn = data(D)
    for w in warn: print('  studio_rerecord WARNING:', w)
    for old, new in REPL:
        assert s.count(old) == 1, ('studio_rerecord anchor', s.count(old), old[:70])
        s = s.replace(old, new)
    k = s.find('async function startRecording(){')
    assert k > 0
    due = [v for v, e in RRD.items() if e['o'] != 3 and latest.get(v) and latest[v] <= e['s']]
    print('studio_rerecord: %d listed, %d to redo (take older than the entry): %s' % (len(RRD), len(due), ', '.join(due)))
    dj = lambda x: json.dumps(x, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return s[:k] + JS.replace('__RR__', dj(RRD)).replace('__RR_LATEST__', dj(latest)).lstrip() + s[k:]
