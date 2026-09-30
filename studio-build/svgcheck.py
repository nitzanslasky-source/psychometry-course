"""svgcheck.py [studio.html] : check that EVERY slide (every step) of every video can be drawn into a recording.

The recorder turns each slide into a standalone SVG image, which must be strict XML. One bad slide = the recording
freezes on the previous slide ("A slide could not be rendered into the recording"). Run after every build.
Uses headless Chrome over --remote-debugging-pipe. Prints the bad slides (video, topic, slide, step, title, error).
"""
import os, sys, json, subprocess, time, tempfile
CH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html')
DRV = "<script>(async function wait(){const d=window.COURSE_DIAGNOSTICS;if(!d)return setTimeout(wait,200);\nconst C=window.COURSE,bad=[];let n=0;const P=new DOMParser();\nconst order=C.flow.filter(r=>r.type==='video').map(r=>r.ref);\nfor(const id of order){const v=C.videos[id];if(!v)continue;v.beats.forEach((b,i)=>{const steps=1+((b.lines||[]).filter(l=>l.appear!=null).length)+((b.reveal||[]).length)+10;\n for(let st=0;st<steps;st++){let svg;try{svg=d.boardSvg(v,i,st)}catch(e){bad.push([id,i,st,'EXC '+e.message]);break}n++;const doc=P.parseFromString(svg,'image/svg+xml');const er=doc.querySelector('parsererror');if(er){bad.push([id,v.topic,i,st,b.title,er.textContent.slice(0,160)]);break}}})}\nconst o=document.createElement('textarea');o.id='res';o.value=JSON.stringify({n,bad});document.body.append(o);\nconst p=document.createElement('pre');p.id='out';p.textContent='done';document.body.append(p)})();</script></body></html>"
tmp = tempfile.mkdtemp(prefix='svgcheck-', dir=os.path.dirname(os.path.abspath(__file__)))
s = open(SRC, encoding='utf-8').read(); k = s.rfind('</body></html>')
page = os.path.join(tmp, 'check.html'); open(page, 'w', encoding='utf-8').write(s[:k] + DRV)
r1, w1 = os.pipe(); r2, w2 = os.pipe()
def pre(): os.dup2(r1, 3); os.dup2(w2, 4)
p = subprocess.Popen([CH, '--headless=new', '--remote-debugging-pipe', '--user-data-dir=' + os.path.join(tmp, 'prof'), 'file://' + page],
                     pass_fds=(r1, w2, 3, 4), preexec_fn=pre, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
os.close(r1); os.close(w2)
out = os.fdopen(w1, 'wb', 0); inp = os.fdopen(r2, 'rb', 0); buf = b''; mid = 0
def send(method, params=None, sid=None):
    global mid; mid += 1; m = {'id': mid, 'method': method, 'params': params or {}}
    if sid: m['sessionId'] = sid
    out.write(json.dumps(m).encode() + b'\0'); return mid
def recv(want):
    global buf
    while True:
        while b'\0' in buf:
            msg, buf = buf.split(b'\0', 1); d = json.loads(msg)
            if d.get('id') == want: return d
        buf += inp.read(65536)
res = None
try:
    time.sleep(2)
    t = recv(send('Target.getTargets'))['result']['targetInfos']; tid = [x for x in t if x['type'] == 'page'][0]['targetId']
    sid = recv(send('Target.attachToTarget', {'targetId': tid, 'flatten': True}))['result']['sessionId']
    for i in range(300):
        time.sleep(1)
        r = recv(send('Runtime.evaluate', {'expression': "document.getElementById('out')?(document.getElementById('res')?.value||''):''"}, sid))
        v = r.get('result', {}).get('result', {}).get('value', '')
        if v: res = json.loads(v); break
finally:
    p.kill(); subprocess.run(['rm', '-rf', tmp])
if not res: sys.exit('no result (timeout)')
print('checked %d slide steps, %d broken' % (res['n'], len(res['bad'])))
for b in res['bad']: print(' ', b)
sys.exit(1 if res['bad'] else 0)
