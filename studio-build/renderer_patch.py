"""JS additions to the studio renderer (applied to the base HTML by build_verbal.py).

\\hl{name}{tex} – a named PART of a TeX formula (looks exactly like {tex}); POINT cues highlight it by name (studio_autonarrate.py).
tq  – text-heavy question layout (verbal): stem on top, answers as full-width wrapped rows anchored at the bottom.
psg – reading passage with numbered paragraphs, auto-fitted to the available height.
"""
HOOK_OLD = "function hyItem(it,x,y,w){const INK=PAL.ink;\n"
HOOK_NEW = ("function hyItem(it,x,y,w){const INK=PAL.ink;\n"
            " if(it.k==='q'&&it.tq)return hyTextQ(it,x,y,w);\n"
            " if(it.k==='psg')return hyPassage(it,x,y,w);\n")

FUNCS = r"""
/* \hl{name}{tex} -> the tex between two empty marker tokens (same look; the part can be measured by name) */
function hlTex(t){t=String(t);if(t.indexOf('\\hl{')<0)return t;let out='',i=0;
 for(;;){const k=t.indexOf('\\hl{',i);if(k<0){out+=t.slice(i);break}out+=t.slice(i,k);const j=t.indexOf('}',k+4);if(j<0){out+=t.slice(k);break}
  const name=t.slice(k+4,j).replace(/[^A-Za-z0-9_-]/g,'');let p=j+1;while(t[p]===' ')p++;
  if(t[p]!=='{'){out+=t.slice(k,p);i=p;continue}let d=0,q=p;for(;q<t.length;q++){if(t[q]==='\\'){q++;continue}if(t[q]==='{')d++;else if(t[q]==='}'){d--;if(!d)break}}
  out+='{\\mmlToken{mi}[class="hla-'+name+'"]{}'+hlTex(t.slice(p+1,q))+'\\mmlToken{mi}[class="hlb-'+name+'"]{}}';i=q+1}
 return out}
function hyTextQ(it,x,y,w){const Q=D.questions[it.qid]||{},stem=String(it.stem||Q.stemRich||'').trim(),ch=it.choices||Q.choicesRich||[];
 const bottom=876,gap=8,cw=w-78,avail=bottom-y-(it.band??70);let cz=it.csize||28,z=it.size||32,rows,tot,r;
 const lay=()=>{rows=ch.map(c=>richSvg(String(c),0,0,cw,cz));tot=rows.reduce((a,q)=>a+Math.max(52,q.height+12),0)+gap*(ch.length-1);r=richSvg(stem,x,y,w,z);return r.height+tot};
 while(lay()>avail){if(z>26)z--;else if(cz>23)cz--;else if(z>23)z--;else if(cz>21)cz--;else break}
 if(lay()>avail&&it.hideok){z=it.size||32;r=richSvg(stem,x,y,w,z);while(r.height>520&&z>22)r=richSvg(stem,x,y,w,--z);return {svg:`<g data-sub="">${r.svg}</g>`,h:r.height,ctop:900}}
 const top=bottom-tot;let s=`<g data-sub="">${r.svg}</g>`,cy=top;
 ch.forEach((c,i)=>{const rh=Math.max(52,rows[i].height+12);
  s+=`<g data-sub=""><rect x="${x}" y="${cy}" width="${w}" height="${rh}" rx="12" fill="#f6f8fc" stroke="#dde5f1"/><circle cx="${x+30}" cy="${cy+rh/2}" r="17" fill="#e1e9fb"/>`
   +svgText(i+1,x+30,cy+rh/2+7,20,PAL.accent,800,'middle')+richSvg(String(c),x+60,cy+(rh-rows[i].height)/2+2,cw,cz).svg+'</g>';cy+=rh+gap});
 return {svg:s,h:r.height,ctop:top}}
function hyPassage(it,x,y,w){const P=(D.passages||{})[it.pid]||{paragraphs:[]},ids=it.paras||P.paragraphs.map((_,i)=>i+1),maxH=it.h||(876-y);
 let z=it.size||30,parts,hh;const lay=()=>{let yy=y;parts=ids.map(n=>{const r=blockText(P.paragraphs[n-1]||'',x+58,yy+z,w-58,z);const o={n,y:yy,r};yy+=r.height+z*.55;return o});return yy-y};
 hh=lay();while(hh>maxH&&z>15){z--;hh=lay()}
 let s='';parts.forEach(p=>{s+=`<g data-sub=""><rect x="${x}" y="${p.y+z*.1}" width="40" height="${z*1.25}" rx="8" fill="#eaf0ff"/>`+svgText(String(p.n),x+20,p.y+z*.98,z*.8,PAL.accent,800,'middle')+p.r.svg+'</g>'});
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

# Forced line breaks ("\n") in rich text: e.g. a stacked system of equations on its own line, then the question.
BR_TOK_OLD = "else for(const w of p.split(/(\\s+)/)){if(w)tokens.push({text:w,w:textWidth(w,size),h:size*1.1})}}"
BR_TOK_NEW = "else for(const w of p.split(/(\\s+)/)){if(!w)continue;if(w.includes('\\n')){tokens.push({br:1});continue}tokens.push({text:w,w:textWidth(w,size),h:size*1.1})}}"
BR_ROW_OLD = "for(let t of tokens){if(t.w>width&&t.tex)"
BR_ROW_NEW = "for(let t of tokens){if(t.br){rows.push({tokens:row,h:rh});row=[];rw=0;rh=size*1.25;continue}if(t.w>width&&t.tex)"

SB_OLD = ("const row=Math.min(58,(880-y)/h.sidebar.length);\n h.sidebar.forEach((name,i)=>{const on=i===b.active,yy=y+i*row,bh=row-10;\n  "
          "if(on)s+=`<rect x=\"18\" y=\"${yy}\" width=\"${HY.sb-36}\" height=\"${bh}\" rx=\"10\" fill=\"#ffffff\" fill-opacity=\"0.13\"/>"
          "<rect x=\"18\" y=\"${yy}\" width=\"6\" height=\"${bh}\" rx=\"3\" fill=\"#f0b64a\"/>`;\n  "
          "s+=`<g opacity=\"${on?1:0.5}\">`+svgText(name,42,yy+bh/2+(on?8:7),on?23:21,on?'#ffffff':'#a9b8d3',on?800:500)+'</g>'});")
SB_NEW = ("const row=Math.min(58,(880-y)/h.sidebar.length);\n"
          " const SL=h.sidebar.map((name,i)=>{const on=i===b.active,z=on?23:21,w=on?800:500;let t=wrapText(name,HY.sb-88,z,w),zz=z;"
          "if(t.length>1){zz=z-3;t=wrapText(name,HY.sb-88,zz,w).slice(0,3)}return {name,on,t,zz,lh:Math.round(zz*1.2)}});\n"
          " const fit=y+row*SL.length+SL.reduce((a,l)=>a+(l.t.length-1)*l.lh,0)<=880;let yy=y;\n"
          " SL.forEach(l=>{const on=l.on,multi=fit&&l.t.length>1,add=multi?(l.t.length-1)*l.lh:0,bh=row-10+add;\n  "
          "if(on)s+=`<rect x=\"18\" y=\"${yy}\" width=\"${HY.sb-36}\" height=\"${bh}\" rx=\"10\" fill=\"#ffffff\" fill-opacity=\"0.13\"/>"
          "<rect x=\"18\" y=\"${yy}\" width=\"6\" height=\"${bh}\" rx=\"3\" fill=\"#f0b64a\"/>`;\n  "
          "s+=`<g opacity=\"${on?1:0.5}\">`+(multi?l.t:[l.name]).map((tx,j)=>svgText(tx,42,yy+(row-10)/2+(on?8:7)+j*l.lh,multi?l.zz:(on?23:21),on?'#ffffff':'#a9b8d3',on?800:500)).join('')+'</g>';\n"
          "  yy+=row+add});")

MJ_OLD = "function mathSvg(tex){if(svgCache.has(tex))"
MJ_NEW = "function mathSvg(tex){tex=hlTex(tex);if(svgCache.has(tex))"

DICE_LBL_OLD = "v.diagonal?'Matching faces':"
DICE_LBL_NEW = "v.diagonal?(v.label||'Matching faces'):"


def apply(html):
    # \hl{name}{…}: expanded before MathJax (marker tokens around the part)
    assert html.count(MJ_OLD) == 1, 'mathSvg not found'
    html = html.replace(MJ_OLD, MJ_NEW)
    assert html.count(LABEL_OLD) == 1, 'sidebar label not found'
    # dice/spinner grid: an item may carry its own label (e.g. spinners: 'Matching sections')
    assert html.count(DICE_LBL_OLD) == 1, 'dice grid label not found'
    html = html.replace(DICE_LBL_OLD, DICE_LBL_NEW)
    html = html.replace(LABEL_OLD, LABEL_NEW)
    assert html.count(PLACE_OLD) == 1, 'placement code not found'
    html = html.replace(PLACE_OLD, PLACE_NEW).replace("const placed=[];b.items.forEach(", "const placed=[];let ctop=900;b.items.forEach(")
    assert html.count(HOOK_OLD) == 1, 'hyItem hook not found'
    html = html.replace(HOOK_OLD, HOOK_NEW)
    assert html.count(BR_TOK_OLD) == 1 and html.count(BR_ROW_OLD) == 1, 'richSvg tokenizer not found'
    html = html.replace(BR_TOK_OLD, BR_TOK_NEW).replace(BR_ROW_OLD, BR_ROW_NEW)
    # sidebar: a long name wraps onto a second line (smaller) instead of running onto the slide, when there is room
    assert html.count(SB_OLD) == 1, 'sidebar renderer not found'
    html = html.replace(SB_OLD, SB_NEW)
    # slides are drawn into the recording as standalone SVG images (strict XML): a value-less attribute breaks them
    html = html.replace('<g data-sub>', '<g data-sub="">')
    k = html.find('function hyPie(')
    assert k > 0
    html = html[:k] + FUNCS.lstrip() + html[k:]
    # 2026-10-10 hand-written board items (k 'hw', studio_handwrite.py); no effect on other items
    import studio_handwrite
    return studio_handwrite.apply(html)
