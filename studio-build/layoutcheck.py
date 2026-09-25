"""Render every hybrid slide (all APPEARs shown) in headless Chrome and report layout problems."""
import subprocess, sys, re, html, os
SP = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1]; only = sys.argv[2] if len(sys.argv) > 2 else ''
s = open(src, encoding='utf-8').read(); k = s.rfind('</body></html>')
js = r'''<script>(function wait(){const d=window.COURSE_DIAGNOSTICS;if(!d)return setTimeout(wait,100);
const out=[];let slides=0,items=0;const host=document.createElement('div');host.style.cssText='position:absolute;left:0;top:0;width:1600px;height:900px';document.body.innerHTML='';document.body.append(host);
for(const [id,v] of Object.entries(window.COURSE.videos)){if(!v.hybrid||!id.includes('ONLY'))continue;v.beats.forEach((b,i)=>{const n=1+b.lines.filter(l=>l.appear!=null).length;host.innerHTML=d.boardSvg(v,i,n-1);const svg=host.querySelector('svg');
 const R=g=>{const r=g.getBoundingClientRect();return {x:r.left,y:r.top,r:r.right,b:r.bottom}};const tag=id+' #'+(i+1)+' '+b.title;slides++;
 svg.querySelectorAll(':scope > text').forEach(t=>{const r=R(t);if(r.r<340&&r.r>316)out.push(tag+' | sidebar label overflows: '+t.textContent)});
 const gs=[...svg.querySelectorAll(':scope > g[data-i]')].flatMap(g=>{const subs=[...g.querySelectorAll(':scope > g[data-sub]')];return (subs.length?subs:[g]).map((x,j)=>({i:g.dataset.i+(subs.length?'.'+j:''),grp:g.dataset.i,...R(x)}))}).filter(g=>g.r>g.x);items+=gs.length;
 gs.forEach(g=>{if(g.r>1602||g.b>902)out.push(tag+' | item '+g.i+' runs off the slide ('+Math.round(g.r)+','+Math.round(g.b)+')');if(g.x<332)out.push(tag+' | item '+g.i+' enters the sidebar')});
 for(let a=0;a<gs.length;a++)for(let c=a+1;c<gs.length;c++){const A=gs[a],B=gs[c];if(A.grp===B.grp)continue;const w=Math.min(A.r,B.r)-Math.max(A.x,B.x),h=Math.min(A.b,B.b)-Math.max(A.y,B.y);if(w>6&&h>6)out.push(tag+' | items '+A.i+' and '+B.i+' overlap')}
})}
document.body.innerHTML='<pre id="res">'+out.join('\n').replace(/</g,'&lt;')+'</pre>';document.title='slides='+slides+' items='+items+' problems='+out.length})();</script></body></html>'''.replace('ONLY', only)
open(SP + '/layout-harness.html', 'w', encoding='utf-8').write(s[:k] + js)
r = subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--headless=new', '--disable-gpu', '--window-size=1700,1000',
                    '--virtual-time-budget=60000', '--dump-dom', 'file://' + SP + '/layout-harness.html'], capture_output=True, text=True, timeout=400)
m = re.search(r'<pre id="res">(.*?)</pre>', r.stdout, re.S); t = re.search(r'<title>([^<]*)</title>', r.stdout)
print('LAYOUT CHECKS:', t.group(1) if t else 'no result')
if m and m.group(1).strip(): print(html.unescape(m.group(1)))
os.remove(SP + '/layout-harness.html')
