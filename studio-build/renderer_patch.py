"""JS additions to the studio renderer (applied to the base HTML by build_verbal.py).

tq  – text-heavy question layout (verbal): stem on top, answers as full-width wrapped rows anchored at the bottom.
psg – reading passage with numbered paragraphs, auto-fitted to the available height.
"""
HOOK_OLD = "function hyItem(it,x,y,w){const INK=PAL.ink;\n"
HOOK_NEW = ("function hyItem(it,x,y,w){const INK=PAL.ink;\n"
            " if(it.k==='q'&&it.tq)return hyTextQ(it,x,y,w);\n"
            " if(it.k==='psg')return hyPassage(it,x,y,w);\n")

FUNCS = r"""
function hyTextQ(it,x,y,w){const Q=D.questions[it.qid]||{},stem=String(it.stem||Q.stemRich||'').trim(),ch=it.choices||Q.choicesRich||[];
 const bottom=876,gap=8,cw=w-78,avail=bottom-y-(it.band??70);let cz=it.csize||28,z=it.size||32,rows,tot,r;
 const lay=()=>{rows=ch.map(c=>richSvg(String(c),0,0,cw,cz));tot=rows.reduce((a,q)=>a+Math.max(52,q.height+12),0)+gap*(ch.length-1);r=richSvg(stem,x,y,w,z);return r.height+tot};
 while(lay()>avail){if(z>26)z--;else if(cz>23)cz--;else if(z>23)z--;else if(cz>21)cz--;else break}
 if(lay()>avail&&it.hideok){z=it.size||32;r=richSvg(stem,x,y,w,z);while(r.height>520&&z>22)r=richSvg(stem,x,y,w,--z);return {svg:`<g data-sub>${r.svg}</g>`,h:r.height,ctop:900}}
 const top=bottom-tot;let s=`<g data-sub>${r.svg}</g>`,cy=top;
 ch.forEach((c,i)=>{const rh=Math.max(52,rows[i].height+12);
  s+=`<g data-sub><rect x="${x}" y="${cy}" width="${w}" height="${rh}" rx="12" fill="#f6f8fc" stroke="#dde5f1"/><circle cx="${x+30}" cy="${cy+rh/2}" r="17" fill="#e1e9fb"/>`
   +svgText(i+1,x+30,cy+rh/2+7,20,PAL.accent,800,'middle')+richSvg(String(c),x+60,cy+(rh-rows[i].height)/2+2,cw,cz).svg+'</g>';cy+=rh+gap});
 return {svg:s,h:r.height,ctop:top}}
function hyPassage(it,x,y,w){const P=(D.passages||{})[it.pid]||{paragraphs:[]},ids=it.paras||P.paragraphs.map((_,i)=>i+1),maxH=it.h||(876-y);
 let z=it.size||30,parts,hh;const lay=()=>{let yy=y;parts=ids.map(n=>{const r=blockText(P.paragraphs[n-1]||'',x+58,yy+z,w-58,z);const o={n,y:yy,r};yy+=r.height+z*.55;return o});return yy-y};
 hh=lay();while(hh>maxH&&z>15){z--;hh=lay()}
 let s='';parts.forEach(p=>{s+=`<g data-sub><rect x="${x}" y="${p.y+z*.1}" width="40" height="${z*1.25}" rx="8" fill="#eaf0ff"/>`+svgText(String(p.n),x+20,p.y+z*.98,z*.8,PAL.accent,800,'middle')+p.r.svg+'</g>'});
 return {svg:s,h:hh}}
"""

PLACE_OLD = "if(it.y!=null&&it.k==='t'){const x1=it.w?x+it.w:x+1;for(const p of placed)if(x<p.x1&&x1>p.x0&&y<p.y1+10&&y+r.h>p.y0){y=p.y1+14;r=hyItem(it,x,y,W)}placed.push({x0:x,x1,y0:y,y1:y+r.h})}if(it.k==='q')placed.push({x0:x,x1:x+W,y0:y,y1:y+r.h+16});"
PLACE_NEW = ("if(it.y!=null&&it.k==='t'){const x1=it.w?x+it.w:x+1;for(const p of placed)if(x<p.x1&&x1>p.x0&&y<p.y1+10&&y+r.h>p.y0){y=p.y1+14;r=hyItem(it,x,y,W)}"
             "let sz=it.size||46;while(y+r.h>ctop-10&&sz>24){sz-=2;r=hyItem(Object.assign({},it,{size:sz}),x,y,W)}placed.push({x0:x,x1,y0:y,y1:y+r.h})}"
             "if(it.k==='q'){placed.push({x0:x,x1:x+W,y0:y,y1:y+r.h+16});if(r.ctop)ctop=r.ctop}")

LABEL_OLD = "s+=svgText((h.subject||'ALGEBRA')+' · MODULE '+h.num,36,64,17,'#f0b64a',800);"
LABEL_NEW = ("{const TS={2:'Fractions — Basics',4:'Expressions — Basics',6:'Equations — Basics',8:'Exponent Laws',10:'Exponents & Roots I',"
             "11:'Exponents & Roots II',19:'New Operations',21:'Trial, Limits, Patterns',22:'Problems & Ratios',35:'3D Geometry',"
             "42:'Formal Logic',43:'Understanding Sentences',44:'Understanding Paragraphs',45:'Parables & Comparisons',46:'Strengthen & Weaken'};"
             "const T=(D.topics||[]).find(t=>+t.id===+v.topic),tt=String(TS[+v.topic]||(T?T.title:'')).toUpperCase(),W=HY.sb-60;"
             "let lbl=(h.subject||'ALGEBRA')+' · '+tt,z=17;while(textWidth(lbl,z,800)>W&&z>13)z--;"
             "if(textWidth(lbl,z,800)>W){lbl=tt;z=17;while(textWidth(lbl,z,800)>W&&z>11)z--}"
             "s+=svgText(lbl,36,64,z,'#f0b64a',800)}")

def apply(html):
    assert html.count(LABEL_OLD) == 1, 'sidebar label not found'
    html = html.replace(LABEL_OLD, LABEL_NEW)
    assert html.count(PLACE_OLD) == 1, 'placement code not found'
    html = html.replace(PLACE_OLD, PLACE_NEW).replace("const placed=[];b.items.forEach(", "const placed=[];let ctop=900;b.items.forEach(")
    assert html.count(HOOK_OLD) == 1, 'hyItem hook not found'
    html = html.replace(HOOK_OLD, HOOK_NEW)
    k = html.find('function hyPie(')
    assert k > 0
    return html[:k] + FUNCS.lstrip() + html[k:]
