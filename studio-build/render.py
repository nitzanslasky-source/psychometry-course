"""render.py OUT.png vid1 vid2 ... : contact sheet of all slides (all APPEARs shown)."""
import subprocess, sys, os, json, re, html
SP = os.path.dirname(os.path.abspath(__file__))
CH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
src = os.environ.get('SRC', '/Users/nitzanslasky/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html')
out, vids = sys.argv[1], sys.argv[2:]
s = open(src, encoding='utf-8').read(); k = s.rfind('</body></html>')
js = '''<script>(function wait(){const d=window.COURSE_DIAGNOSTICS;if(!d)return setTimeout(wait,100);
const vids=%s;const all=[];
for(const id of vids){const v=window.COURSE.videos[id];if(!v){all.push('<svg viewBox="0 0 1600 900"><text x="100" y="400" font-size="60">missing '+id+'</text></svg>');continue}v.beats.forEach((b,i)=>{const n=1+b.lines.filter(l=>l.appear!=null).length;all.push(d.boardSvg(v,i,n-1))})}
document.body.innerHTML='<textarea id="res"></textarea>';document.getElementById('res').textContent=JSON.stringify(all)})();</script></body></html>''' % json.dumps(vids)
open(SP + '/render-harness.html', 'w', encoding='utf-8').write(s[:k] + js)
r = subprocess.run([CH, '--headless=new', '--disable-gpu', '--virtual-time-budget=60000', '--dump-dom', 'file://' + SP + '/render-harness.html'], capture_output=True, text=True, timeout=300)
svgs = json.loads(html.unescape(re.search(r'<textarea id="res">(.*?)</textarea>', r.stdout, re.S).group(1)))
cells = ''.join('<div style="width:960px;height:540px;overflow:hidden;background:#fff">%s</div>' % re.sub(r'<svg', '<svg width="960" height="540"', x, 1) for x in svgs)
open(SP + '/render-static.html', 'w', encoding='utf-8').write('<html><body style="margin:0;background:#777;display:flex;flex-wrap:wrap;gap:6px;width:1926px">' + cells + '</body></html>')
rows = (len(svgs) + 1) // 2
subprocess.run([CH, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=1926,%d' % (rows * 546), '--screenshot=' + os.path.abspath(out), 'file://' + SP + '/render-static.html'], capture_output=True, timeout=180)
print(len(svgs), 'slides ->', out)
