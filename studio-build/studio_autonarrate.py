"""AI auto-narrate + POINT cues (applied by build_verbal.py last).

1. POINT cues (data): a script line {'point': <target>, 'label': 'what she points at', 'at': 0..1, 'style': 'hl'|'dot'|'both',
   'dur': seconds}. Written in a patch with dsl.PT(target, label, at=, style=, dur=). The cue belongs to the NEXT spoken line:
   auto-narrate fires it when that line starts (or at fraction `at` of the line). In the teacher's script it shows as
   "▶ POINT …" and fires when she clicks it (the highlight / pointer is drawn into the recording, like the laser).
   Targets:
     'item N'            a whole board item (b['items'][N], 0-based)
     'item N: name'      a marked PART of item N's TeX:  $\\hl{name}{5\\alpha+5\\beta}=360°$  renders exactly like {…};
     'name'              the same part, searched in every item on the board
     'choice N' / 'stem' an answer choice / the question text of the question on the board
     'fig: α'            every label "α" in the figure (geometry SVG labels)
     'fig: AB'           side AB (from the vertices next to the labels A and B);  'fig: ABC' / 'fig: ∠ABC' = angle at B
     'fig: shaded'       the shaded (filled) region(s) of the figure
   \\hl{name}{…} is expanded in the studio's mathSvg (renderer_patch.py) into empty MathML marker tokens around the part, so the part keeps its
   normal look and spacing, and its box is measured from the rendered slide (works inside fractions, roots, …).
2. AUTO-NARRATE (teacher only; videos with ai_scripts/<id>.json): 🤖 Auto-narrate plays the slides with the AI audio
   (Course.recordings/_ai_audio/<id>/), firing every cue in order like the teacher: lines -> mp3, APPEAR / NEXT PART -> reveal,
   DRAW marks (circle / cross out / tick / underline a choice, or a draw line with 'mark' + 'target') -> animated pen marks,
   POINT -> highlight / pointer. Any other DRAW (hand-writing) is listed before starting and nothing is recorded.
   CONTINUOUS mode (manifest "mode": "continuous", from ai_narrate.py --continuous; pilot v2 2026-10-09): ONE audio
   file for the whole video, played without a break; every cue is fired on the audio clock at the time the alignment
   gives it (slide change in the pause before the slide's first line, APPEAR just before its line or at its `at`
   phrase, POINT / marks at their phrase) — the audio never waits for an animation, marks and highlights animate while
   the voice goes on. Per-line mode (one mp3 per line, fixed gaps) still works for older manifests.
   Both modes rasterise every slide state BEFORE recording (anPrerender) and measure every POINT / mark target in
   advance, so a slide change / APPEAR during the take only swaps a ready canvas into the recorder. (Pilot v1: each
   APPEAR decoded + painted a new SVG image mid-take -> a ~75 ms frozen frame; fixed gaps stacked up at slide changes
   -> a 2.4 s silence.)
   It records with the normal recorder (CutRecorder; AI audio instead of the mic, no camera, faded preview off) and the
   take is kept / saved like a normal take (same folder, name, chapters -> green "recorded" mark).
"""

JS = r"""
/* ---- POINT cues + AI auto-narrate (studio_autonarrate.py) ---- */
var AN={fx:[],dotPos:null,raf:0,measSvg:null};
function anPointText(l){return '[POINT: '+[l.point,l.label||'',l.at!=null?'at '+l.at:'',l.style||'',l.dur?'dur '+l.dur:''].filter(Boolean).join(' | ')+']'}
function anParsePoint(s){const p=String(s).split(/\s+\|\s+/),o={point:p[0].trim()};for(const x of p.slice(1)){let m;
 if(m=x.match(/^at\s*([\d.]+)$/i))o.at=+m[1];else if(m=x.match(/^dur\s*([\d.]+)$/i))o.dur=+m[1];else if(/^(hl|dot|both)$/i.test(x.trim()))o.style=x.trim().toLowerCase();else if(x.trim())o.label=x.trim()}return o}
function anPointCue(l){return `<div class="hy-cue hy-point" data-pt="${esc(JSON.stringify(l))}" title="Click to point at it (shows in the recording)" style="cursor:pointer;background:#fff3c4;color:#6b3f00;border-radius:8px;padding:3px 10px;margin:3px 0;display:inline-block"><b>▶ POINT</b> ${esc(l.label||l.point)} <span style="opacity:.7;font-size:.85em">· click</span></div>`}
document.addEventListener('click',e=>{const el=e.target.closest?.('.hy-point[data-pt]');if(!el||!STUDIO||!video())return;try{anFire(JSON.parse(el.dataset.pt),video(),state.beat)}catch(err){console.warn(err)}});

/* ---- geometry of the rendered slide (board units 1600×900), measured on a hidden copy of the slide ---- */
function anRoot(svg){svg=svg??currentSvg;let h=document.getElementById('an-measure');
 if(!h){h=document.createElement('div');h.id='an-measure';h.setAttribute('aria-hidden','true');h.style.cssText='position:fixed;left:-30000px;top:0;width:1600px;height:900px;visibility:hidden;pointer-events:none;overflow:hidden;contain:strict';document.body.append(h)}
 if(AN.measSvg!==svg){h.innerHTML=svg;AN.measSvg=svg}return h.querySelector('svg')}
function anM(el,root){return root.getScreenCTM().inverse().multiply(el.getScreenCTM())}
function anPt(x,y,m){const p=new DOMPoint(x,y).matrixTransform(m);return {x:p.x,y:p.y}}
function anBox(el,root){try{const b=el.getBBox();if(!(b.width>0||b.height>0))return null;const m=anM(el,root);
 const P=[[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]].map(([x,y])=>anPt(x,y,m)),xs=P.map(p=>p.x),ys=P.map(p=>p.y);
 return {x:Math.min(...xs),y:Math.min(...ys),w:Math.max(...xs)-Math.min(...xs),h:Math.max(...ys)-Math.min(...ys)}}catch{return null}}
function anUnion(bs){bs=bs.filter(Boolean);if(!bs.length)return null;const x0=Math.min(...bs.map(b=>b.x)),y0=Math.min(...bs.map(b=>b.y)),x1=Math.max(...bs.map(b=>b.x+b.w)),y1=Math.max(...bs.map(b=>b.y+b.h));return {x:x0,y:y0,w:x1-x0,h:y1-y0}}
function anNorm(s){return String(s).normalize('NFKC').replace(/\s+/g,'').replace(/^∠/,'')}
function anFigs(g){return g?[...g.querySelectorAll('svg')].filter(s=>!s.hasAttribute('focusable')&&s.querySelector('text,line,path,polygon,circle')):[]}
function anVerts(fig,root){const V=[];for(const el of fig.querySelectorAll('line,polygon,polyline,path')){let pts=[];const t=el.tagName.toLowerCase();
  if(t==='line')pts=[[+el.getAttribute('x1'),+el.getAttribute('y1')],[+el.getAttribute('x2'),+el.getAttribute('y2')]];
  else if(t==='path'){const d=el.getAttribute('d')||'';for(const m of d.matchAll(/[ML]\s*(-?[\d.]+)[\s,]+(-?[\d.]+)/g))pts.push([+m[1],+m[2]])}
  else{const n=(el.getAttribute('points')||'').trim().split(/[\s,]+/).map(Number);for(let i=0;i+1<n.length;i+=2)pts.push([n[i],n[i+1]])}
  let m;try{m=anM(el,root)}catch{continue}for(const [x,y] of pts)if(Number.isFinite(x)&&Number.isFinite(y))V.push(anPt(x,y,m))}
 const out=[];for(const p of V)if(!out.some(q=>Math.hypot(q.x-p.x,q.y-p.y)<3))out.push(p);return out}
function anOutline(el,root){try{const L=el.getTotalLength(),n=Math.max(24,Math.min(160,Math.round(L/6))),m=anM(el,root),pts=[];for(let i=0;i<=n;i++){const p=el.getPointAtLength(L*i/n);pts.push(anPt(p.x,p.y,m))}return pts}catch{return null}}
function anFill(el){const f=(el.getAttribute('fill')||getComputedStyle(el).fill||'').toLowerCase().replace(/\s/g,'');return f&&!/^(none|transparent|#fff|#ffffff|white|rgb\(255,255,255\)|rgba\(0,0,0,0\))$/.test(f)}
/* spec -> {shapes:[...], box, dot} or {err} */
function anResolve(spec,v,bi,svg){const root=anRoot(svg);if(!root)return {err:'the slide is not ready'};const b=v.beats[bi];let s=String(spec||'').trim(),m;
 const item=i=>root.querySelector(':scope > g[data-i="'+i+'"]'),subs=g=>g?[...g.children].filter(c=>c.matches('g[data-sub]')):[];
 const boxOf=el=>anBox(el,root),res=(shapes,kind)=>{shapes=shapes.filter(Boolean);if(!shapes.length)return {err:'nothing found for "'+spec+'"'};
  const box=anUnion(shapes.map(x=>x.k==='box'?x:x.pts?anUnion(x.pts.map(p=>({x:p.x,y:p.y,w:0,h:0}))):null));
  const sh=shapes[0],dot=sh.k==='box'?(kind==='label'?{x:sh.x+sh.w+10,y:sh.y+sh.h+6}:{x:sh.x+sh.w/2,y:sh.y+sh.h+(sh.pad??9)+20}):sh.dot||{x:box.x+box.w/2,y:box.y+box.h/2};
  return {shapes,box,dot,kind}};
 const qi=b.items.findIndex(it=>it.k==='q'&&!it.nochoices);
 if(m=s.match(/^(?:choice|answer|option)\s*(\d)$/i)){const g=item(qi),c=subs(g)[+m[1]];if(!c||!c.querySelector('rect'))return {err:'no choice '+m[1]+' on the board'};
  return res([anUnion([...c.children].filter(x=>x.tagName.toLowerCase()!=='rect').map(boxOf))].map(x=>x&&{k:'box',...x}),'choice')}
 if(/^(stem|question)$/i.test(s)){const c=subs(item(qi))[0];return c?res([{k:'box',...boxOf(c)}],'item'):{err:'no question on the board'}}
 let scope=null;if(m=s.match(/^item\s*(\d+)\s*(?::\s*(.*))?$/i)){scope=item(+m[1]);if(!scope)return {err:'item '+m[1]+' is not on the board at this moment'};if(!m[2])return res([{k:'box',...boxOf(scope)}],'item');s=m[2].trim()}
 const groups=scope?[scope]:[...root.querySelectorAll(':scope > g[data-i]')];
 if(m=s.match(/^fig(?:ure)?\s*:\s*(.+)$/i)){const want=m[1].trim(),figs=groups.flatMap(anFigs);if(!figs.length)return {err:'no figure on the board'};
  const sh=[];for(const fig of figs){
   if(/^(shaded|shading|filled)$/i.test(want)){for(const el of fig.querySelectorAll('path,polygon,circle,rect,ellipse')){const bx=boxOf(el);if(!bx||bx.w<14||bx.h<14||!anFill(el))continue;const pts=anOutline(el,root);if(pts)sh.push({k:'poly',pts,closed:true})}continue}
   const texts=[...fig.querySelectorAll('text')],lab=x=>texts.filter(t=>anNorm(t.textContent)===anNorm(x));
   const hit=lab(want);if(hit.length){hit.forEach(t=>{const bx=boxOf(t);if(bx)sh.push({k:'box',...bx,r:Math.max(bx.w,bx.h)/2+6,pad:7})});continue}
   const L=want.replace(/^∠/,'').replace(/\s+/g,'');if(/^[A-Z]{2,3}$/.test(L)){const V=anVerts(fig,root),vx=ch=>{const t=lab(ch)[0],bx=t&&boxOf(t);if(!bx)return null;const c={x:bx.x+bx.w/2,y:bx.y+bx.h/2};let best=null,bd=1e9;for(const p of V){const d=Math.hypot(p.x-c.x,p.y-c.y);if(d<bd){bd=d;best=p}}return bd<70?best:null};
    const P=[...L].map(vx);if(P.some(p=>!p))continue;
    if(P.length===2)sh.push({k:'poly',pts:P,closed:false,lw:10,dot:{x:(P[0].x+P[1].x)/2,y:(P[0].y+P[1].y)/2}});
    else{const [A,B,C]=P,a1=Math.atan2(A.y-B.y,A.x-B.x),a2=Math.atan2(C.y-B.y,C.x-B.x);let d=a2-a1;while(d>Math.PI)d-=2*Math.PI;while(d<-Math.PI)d+=2*Math.PI;const r=Math.min(46,.45*Math.min(Math.hypot(A.x-B.x,A.y-B.y),Math.hypot(C.x-B.x,C.y-B.y))),pts=[B];
     for(let i=0;i<=24;i++){const a=a1+d*i/24;pts.push({x:B.x+r*Math.cos(a),y:B.y+r*Math.sin(a)})}const am=a1+d/2;sh.push({k:'poly',pts,closed:true,lw:5,dot:{x:B.x+r*1.25*Math.cos(am),y:B.y+r*1.25*Math.sin(am)}})}}}
  return res(sh,/^(shaded|shading|filled)$/i.test(want)?'region':'label')}
 const name=s.replace(/[^A-Za-z0-9_-]/g,'');const sh=[];
 for(const g of groups)for(const a of g.querySelectorAll('.hla-'+CSS.escape(name))){const e=a.parentElement?.querySelector(':scope > .hlb-'+CSS.escape(name));const parts=[];let n=a.nextElementSibling;
  while(n&&n!==e){parts.push(boxOf(n));n=n.nextElementSibling}const bx=anUnion(parts);if(bx)sh.push({k:'box',...bx})}
 return sh.length?res(sh,'part'):{err:'no part "'+name+'" on the board'+(scope?' in that item':'')+' (mark it in the TeX with \\hl{'+name+'}{…})'}}

/* ---- the highlight / pointer layer: painted into the recording (draw loop) and onto the screen (overlay canvas) ---- */
function anRR(g,x,y,w,h,r){r=Math.min(r,w/2,h/2);g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath()}
function anFire(l,v,bi,svg,pre){const r=pre||anResolve(l.point,v,bi,svg);if(r.err){toast('POINT: '+r.err);return 0}
 const style=(l.style||'hl').toLowerCase(),dur=+l.dur||(r.shapes.length>2?1.9:1.5),dot=style==='hl'?null:r.dot;
 const f={t0:performance.now(),dur,shapes:style==='dot'?[]:r.shapes,dot,lead:dot?.45:0};
 if(dot){f.from=AN.dotPos||{x:Math.min(1560,dot.x+120),y:Math.min(880,dot.y+90)};AN.dotPos=dot}
 AN.fx.push(f);anLoop();return f.lead+dur}
function anPaint(g,k){if(!AN.fx.length)return;const now=performance.now();AN.fx=AN.fx.filter(f=>now-f.t0<(f.lead+f.dur+.35)*1000);if(!AN.fx.length)return;
 g.save();g.scale(k,k);g.lineJoin='round';g.lineCap='round';
 for(const f of AN.fx){const t=(now-f.t0)/1000,th=t-f.lead*.6,a=Math.max(0,Math.min(1,th/.2,(f.lead+f.dur-t)/.4)),grow=1-Math.min(1,Math.max(0,th)/.25);
  if(a>0)for(const s of f.shapes){
   if(s.k==='box'){const p=(s.pad??9)+5*grow,r=s.r??12;g.save();g.globalCompositeOperation='multiply';g.fillStyle='rgba(255,214,10,'+(.6*a)+')';anRR(g,s.x-p,s.y-p,s.w+2*p,s.h+2*p,r);g.fill();g.restore();
    g.save();g.strokeStyle='rgba(230,140,0,'+(.95*a)+')';g.lineWidth=3;anRR(g,s.x-p,s.y-p,s.w+2*p,s.h+2*p,r);g.stroke();g.restore()}
   else if(s.k==='poly'&&s.pts.length>1){g.save();g.beginPath();s.pts.forEach((p,i)=>i?g.lineTo(p.x,p.y):g.moveTo(p.x,p.y));if(s.closed){g.closePath();g.globalCompositeOperation='multiply';g.fillStyle='rgba(255,214,10,'+(.55*a)+')';g.fill();g.globalCompositeOperation='source-over'}
    g.strokeStyle='rgba(230,140,0,'+(.95*a)+')';g.lineWidth=(s.lw||6)+3*grow;g.stroke();g.restore()}}
  if(f.dot){const e=Math.min(1,t/f.lead),q=e<.5?2*e*e:1-Math.pow(-2*e+2,2)/2,x=f.from.x+(f.dot.x-f.from.x)*q,y=f.from.y+(f.dot.y-f.from.y)*q,da=Math.max(0,Math.min(1,(f.lead+f.dur+.3-t)/.3));
   g.save();g.globalAlpha=da;g.beginPath();g.arc(x,y,22,0,7);g.fillStyle='rgba(238,61,89,.28)';g.fill();g.beginPath();g.arc(x,y,9,0,7);g.fillStyle='#ee3d59';g.fill();g.lineWidth=2;g.strokeStyle='#fff';g.stroke();g.restore()}}
 g.restore()}
window.anPaint=anPaint;
function anOverlay(){const bd=document.getElementById('board');if(!bd)return null;let c=document.getElementById('an-ov');
 if(!c||c.parentElement!==bd){c?.remove();c=document.createElement('canvas');c.id='an-ov';c.setAttribute('aria-hidden','true');c.style.cssText='position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:6;mix-blend-mode:multiply';bd.append(c)}
 const r=bd.getBoundingClientRect(),dpr=window.devicePixelRatio||1,W=Math.round(r.width*dpr),H=Math.round(r.height*dpr);if(c.width!==W||c.height!==H){c.width=W;c.height=H}
 const k=Math.min(r.width/1600,r.height/900);c._L={k:k*dpr,ox:(r.width-1600*k)/2*dpr,oy:(r.height-900*k)/2*dpr};return c}
function anLoop(){if(AN.raf)return;const step=()=>{AN.raf=0;const c=anOverlay();if(c){const g=c.getContext('2d');g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,c.width,c.height);g.translate(c._L.ox,c._L.oy);anPaint(g,c._L.k)}
  if(AN.fx.length)AN.raf=requestAnimationFrame(step)};AN.raf=requestAnimationFrame(step)}

/* ---- marks drawn with the pen (same ink as the teacher's): circle / cross out / tick / underline ---- */
function anMarkOf(l){if(l.mark&&l.target)return {kind:String(l.mark).toLowerCase(),targets:[].concat(l.target)};
 const t=String(l.draw||'').trim().replace(/[.\s]+$/,'');const m=t.match(/^(circle|cross out|cross off|cross|strike out|strike through|tick|check|underline)\s+(?:the\s+)?(?:choices?|answers?|options?)\s+((?:\d)(?:\s*(?:,|and|&)\s*\d)*)$/i);
 if(!m)return null;const w=m[1].toLowerCase(),kind=w.startsWith('circle')?'circle':/^(cross|strike)/.test(w)?'cross':/^(tick|check)/.test(w)?'tick':'underline';
 return {kind,targets:m[2].match(/\d/g).map(n=>'choice '+n)}}
function anMarkPts(kind,B){const P=[],cx=B.x+B.w/2,cy=B.y+B.h/2;
 if(kind==='circle'){const rx=B.w/2+22,ry=Math.max(30,B.h/2+14),a0=-2.3,n=72;for(let i=0;i<=n;i++){const u=i/n,a=a0+u*(2*Math.PI+.45),s=1+.035*Math.sin(3*a+1)+.05*u;P.push([cx+rx*s*Math.cos(a),cy+ry*s*Math.sin(a)])}}
 else if(kind==='cross'){const n=24;for(let i=0;i<=n;i++){const u=i/n;P.push([B.x-12+(B.w+24)*u,B.y+B.h*.8-(B.h*.6)*u+2*Math.sin(u*6)])}}
 else if(kind==='tick'){const x=B.x+B.w+16,a=[[x,cy-2],[x+13,cy+16],[x+44,cy-28]];for(let s=0;s<2;s++)for(let i=0;i<=10;i++){const u=i/10;P.push([a[s][0]+(a[s+1][0]-a[s][0])*u,a[s][1]+(a[s+1][1]-a[s][1])*u])}}
 else{const n=20,y=B.y+B.h+7;for(let i=0;i<=n;i++){const u=i/n;P.push([B.x-4+(B.w+8)*u,y+1.5*Math.sin(u*9)])}}
 return P.map(p=>[Math.max(0,Math.min(1600,p[0])),Math.max(0,Math.min(900,p[1]))])}
const anSleep=ms=>new Promise(r=>setTimeout(r,ms));
async function anInk(pts,sec){const k=cutInkKey(),list=state.ink[k]||(state.ink[k]=[]),s={color:'#d62d48',width:5,points:[pts[0]]};list.push(s);const t0=performance.now();
 for(;;){const f=Math.min(1,(performance.now()-t0)/(sec*1000));s.points=pts.slice(0,Math.max(1,Math.round(f*pts.length)));pen.sync();if(f>=1)break;await anSleep(16)}}
async function anMarkDo(mk,v,bi,boxes){for(let i=0;i<mk.targets.length;i++){const box=boxes?.[i]||(()=>{const r=anResolve(mk.targets[i],v,bi);if(r.err)throw Error(r.err);return r.box})();await anInk(anMarkPts(mk.kind,box),mk.kind==='circle'?.6:.35);await anSleep(150)}}

/* ---- the plan: check everything before recording anything ---- */
function anPlan(v,man){const errs=[],W=[];let say=0;
 v.beats.forEach((b,bi)=>{if(b.layout!=='hybrid'){errs.push('slide '+(bi+1)+' is not a hybrid slide');return}let step=0;const ls=hyLines(v,bi);
  ls.forEach((l,li)=>{const where='slide '+(bi+1)+' «'+b.title+'», line '+(li+1);
   if(l.say!=null)say++;else if(l.appear!=null)step++;
   else if(l.draw!=null){const mk=anMarkOf(l);if(!mk){errs.push(where+': [DRAW: '+l.draw+'] — hand-writing. Make it a click item (APPEAR) or give it a mark + target.');return}
    for(const tg of mk.targets){const r=anResolve(tg,v,bi,boardSvg(v,bi,step));if(r.err)errs.push(where+': [DRAW: '+l.draw+'] — '+r.err)}}
   else if(l.point!=null){const r=anResolve(l.point,v,bi,boardSvg(v,bi,step));if(r.err)errs.push(where+': '+anPointText(l)+' — '+r.err)}})});
 if(man){const n=(man.lines||[]).length;if(n!==say)errs.push('The AI audio has '+n+' lines but the video has '+say+' spoken lines — update ai_scripts/'+v.id+'.json and run ai_narrate.py again.')}
 return {errs,say}}

/* ---- AI audio: Course.recordings/_ai_audio/<id>/ (recordings folder), or a folder picked now; window.__AN_SRC for tests ---- */
async function anLoadAudio(id){const T=window.__AN_SRC?.[id];
 if(T)return {manifest:T.manifest,get:async f=>{const s=atob(T.files[f]),u=new Uint8Array(s.length);for(let i=0;i<s.length;i++)u[i]=s.charCodeAt(i);return u.buffer}};
 let dir=null;if(RF.handle){try{let p=await RF.handle.queryPermission({mode:'readwrite'});if(p!=='granted')p=await RF.handle.requestPermission({mode:'readwrite'});
   if(p==='granted')dir=await (await RF.handle.getDirectoryHandle('_ai_audio')).getDirectoryHandle(id)}catch(e){dir=null}}
 if(!dir&&window.showDirectoryPicker){toast('Choose the folder _ai_audio/'+id+' (in your recordings folder)');try{dir=await window.showDirectoryPicker({id:'studio-ai-audio'});if(dir.name!==id)dir=await (dir.name==='_ai_audio'?dir:await dir.getDirectoryHandle('_ai_audio')).getDirectoryHandle(id)}catch(e){dir=null}}
 if(!dir)throw Error('No AI audio found for '+id+'. Generate it with: python3 ai_narrate.py '+id);
 const rd=async f=>await (await (await dir.getFileHandle(f)).getFile()).arrayBuffer();
 return {manifest:JSON.parse(new TextDecoder().decode(await rd('manifest.json'))),get:rd}}

/* ---- run ---- */
function anStatus(t){let p=document.getElementById('an-status');if(!t){p?.remove();return}
 if(!p){p=document.createElement('div');p.id='an-status';p.style.cssText='position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10002;background:#2e1065;color:#fff;border-radius:14px;padding:10px 16px;font:600 15px system-ui;display:flex;gap:14px;align-items:center;box-shadow:0 10px 30px #0005';
  p.innerHTML='<span id="an-st-t"></span><button type="button" id="an-stop" style="padding:7px 14px;border-radius:9px;border:0;background:#ef4444;color:#fff;font-weight:800;cursor:pointer">■ Stop</button>';document.body.append(p);p.querySelector('#an-stop').onclick=()=>anAbort('stopped')}
 p.querySelector('#an-st-t').textContent=t}
function anAbort(why){const R=window.AN_RUN;if(!R)return;R.abort=why||'stopped';try{R.src?.stop()}catch{}}
function anPlay(R,buf){return new Promise(res=>{const s=R.ac.createBufferSource();s.buffer=buf;s.connect(R.dest);s.connect(R.ac.destination);R.src=s;s.onended=()=>{R.src=null;res()};s.start()})}
async function anWait(R,ms){const t=performance.now();while(performance.now()-t<ms&&!R.abort)await anSleep(Math.min(40,ms))}
async function anSettle(){await prepareSlideImage();AN.measSvg=null}
function anGap(s){s=String(s).trim();return /\?$/.test(s)?650:/(\.\.\.|…)$/.test(s)?550:/[.!]$/.test(s)?420:320}
/* every slide state (slide, step) rasterised once BEFORE recording: a slide change / APPEAR during the take only swaps
   a ready 1920×1080 canvas into the recorder (no SVG decode + first-paint stall in the middle of a take) */
async function anPrerender(v){const pre=new Map();pre.svg={};
 for(let bi=0;bi<v.beats.length;bi++)for(let st=0;st<stepCount(v.beats[bi]);st++){const svg=pre.svg[bi+':'+st]=boardSvg(v,bi,st);if(pre.has(svg))continue;
  const url=URL.createObjectURL(new Blob([svg],{type:'image/svg+xml'})),img=new Image();img.src=url;
  try{await img.decode()}catch(e){URL.revokeObjectURL(url);throw Error('slide '+(bi+1)+' step '+(st+1)+' could not be drawn')}URL.revokeObjectURL(url);
  const c=document.createElement('canvas');c.width=1920;c.height=1080;const g=c.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,1920,1080);g.drawImage(img,0,0,1920,1080);pre.set(svg,c)}
 return pre}
/* continuous AI audio: every cue gets a time on the audio clock (seconds from the start of audio.mp3), from the word
   alignment in the manifest. A cue belongs to the NEXT spoken line; the AI line's `at` phrase times it, else:
   APPEAR just before the line starts, a mark at its start, POINT at fraction `at` of the line. Slide changes sit in the
   pause before the slide's first line. All geometry is measured now, not during the take. */
function anTimeline(v,man){const L=man.lines,ev=[];let li=0;
 v.beats.forEach((b,bi)=>{const ls=hyLines(v,bi),slideT=bi?(()=>{const pe=L[li-1]?.end??0,ns=L[li]?.slide===bi?L[li].start:pe+.5;return Math.max(pe+.05,Math.min(ns-.3,(pe+ns)/2))})():0;
  if(bi)ev.push({t:slideT,k:'slide',bi});const mine=[];let pend=[],lastEnd=slideT,lastAp=slideT;
  const place=(m)=>{pend.forEach((c,k)=>{let t=m?(m.at?.[k]??null):null;
    if(t==null)t=!m?lastEnd+.15+.35*k:c.l.appear!=null?m.start-.12:c.l.point!=null?m.start+Math.max(0,Math.min(.95,+c.l.at||0))*(m.end-m.start):m.start+.05;
    c.t=Math.max(slideT+.05,t);if(c.k==='appear'){c.t=Math.max(c.t,lastAp+.05);lastAp=c.t}mine.push(c)});pend=[]};
  for(const l of ls){if(l.say!=null){const m=L[li++];if(!m)break;place(m);mine.push({t:m.start,k:'say',n:li,l});lastEnd=m.end}
   else if(l.appear!=null)pend.push({k:'appear',l});else if(l.draw!=null)pend.push({k:'mark',l});else if(l.point!=null)pend.push({k:'point',l})}
  place(null);
  /* in time order: the board step at each moment, then measure what the cue points at / marks on that board */
  mine.sort((x,y)=>x.t-y.t);let step=0;
  for(const c of mine){c.bi=bi;if(c.k==='appear'){c.step=++step}else if(c.k==='point'){c.pre=anResolve(c.l.point,v,bi,boardSvg(v,bi,step));if(c.pre.err)throw Error('slide '+(bi+1)+': POINT '+c.l.point+' — '+c.pre.err)}
   else if(c.k==='mark'){c.mk=anMarkOf(c.l);c.boxes=c.mk.targets.map(tg=>{const r=anResolve(tg,v,bi,boardSvg(v,bi,step));if(r.err)throw Error('slide '+(bi+1)+': '+c.l.draw+' — '+r.err);return r.box})}}
  ev.push(...mine)});
 ev.sort((x,y)=>x.t-y.t);return ev}
/* during a continuous take the screen shows the same ready canvas over the board (a cheap copy) instead of re-building
   the board / script DOM (updateSlide), whose main-thread work held recorded frames for ~0.1 s; updateSlide runs once at
   the end */
function anScreen(c){const bd=document.getElementById('board');if(!bd)return;let s=document.getElementById('an-screen');
 if(!s||s.parentElement!==bd){s?.remove();s=document.createElement('canvas');s.id='an-screen';s.setAttribute('aria-hidden','true');s.style.cssText='position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:5';bd.append(s)}
 const r=bd.getBoundingClientRect(),dpr=window.devicePixelRatio||1,W=Math.round(r.width*dpr),H=Math.round(r.height*dpr);if(s.width!==W||s.height!==H){s.width=W;s.height=H}
 const k=Math.min(r.width/1600,r.height/900)*dpr,g=s.getContext('2d');g.fillStyle=getComputedStyle(bd).backgroundColor||'#fff';g.fillRect(0,0,W,H);
 g.drawImage(c,(W-1600*k)/2,(H-900*k)/2,1600*k,900*k)}
function anShow(R,bi,step){state.beat=bi;state.step=step;
 const v=R.v,svg=R.pre?.svg?.[bi+':'+step]??boardSvg(v,bi,step),c=R.pre?.get(svg);   /* board SVG text made before the take too (its TeX layout is not free) */
 if(c){currentSvg=svg;++slideToken;slideImage=c;anScreen(c);pen.sync()}else{updateSlide();pen.sync()}}
async function anRunContinuous(R,v,man,buf,lg){
 const ev=R.ev,lead=.9,s=R.ac.createBufferSource();s.buffer=buf;s.connect(R.dest);s.connect(R.ac.destination);R.src=s;
 let ended=false;s.onended=()=>{ended=true};const t0=R.ac.currentTime+lead;s.start(t0);lg('audio start (lead '+lead+' s)');
 const marks=[];let i=0;const last=Math.max(buf.duration,...ev.map(e=>e.t+(e.k==='mark'?1.2:0)));
 while(!R.abort){const now=R.ac.currentTime-t0;
  while(i<ev.length&&ev[i].t<=now){const e=ev[i++];
   if(e.k==='say'){anStatus('🤖 Auto-narrating · slide '+(e.bi+1)+'/'+v.beats.length+' · line '+e.n+'/'+man.lines.length);lg('say '+e.n)}
   else if(e.k==='slide'){anShow(R,e.bi,0);lg('slide '+(e.bi+1))}
   else if(e.k==='appear'){anShow(R,e.bi,e.step);lg('appear '+e.l.appear+(e.l.part!=null?' part '+e.l.part:''))}
   else if(e.k==='point'){anFire(e.l,v,e.bi,null,e.pre);lg('point '+e.l.point)}
   else if(e.k==='mark'){lg('mark '+e.l.draw);marks.push(anMarkDo(e.mk,v,e.bi,e.boxes))}}
  if(now>=last&&(ended||now>buf.duration+.5))break;await anSleep(8)}
 await Promise.all(marks);lg('audio end');if(!R.abort)await anWait(R,1100)}
async function anStart(){const v=video();if(!STUDIO||!v||record||window.AN_RUN)return;
 const ac=new (window.AudioContext||window.webkitAudioContext)({sampleRate:48000});ac.resume?.();
 let audio,bufs=[];try{audio=await anLoadAudio(v.id)}catch(e){ac.close();return dialog('🤖 Auto-narrate',`<p>${esc(e.message||e)}</p>`)}
 const cont=audio.manifest.mode==='continuous';
 const plan=anPlan(v,audio.manifest);
 if(plan.errs.length){ac.close();return dialog('🤖 Auto-narrate cannot record this video yet',`<p>Nothing was recorded. Fix these first (the AI cannot hand-write):</p><ul>${plan.errs.map(x=>'<li style="margin:6px 0">'+esc(x)+'</li>').join('')}</ul>`)}
 anStatus('🤖 Loading the AI voice…');
 let ev=null,pre=null;
 try{if(cont)bufs=[await ac.decodeAudioData(await audio.get(audio.manifest.file))];else for(const x of audio.manifest.lines)bufs.push(await ac.decodeAudioData(await audio.get(x.file)))}catch(e){anStatus();ac.close();return dialog('🤖 Auto-narrate',`<p>Could not read the AI audio: ${esc(e.message||e)}</p>`)}
 try{anStatus('🤖 Preparing the slides…');pre=await anPrerender(v);if(cont)ev=anTimeline(v,audio.manifest)}catch(e){anStatus();ac.close();return dialog('🤖 Auto-narrate',`<p>${esc(e.message||e)}</p>`)}
 const dest=ac.createMediaStreamDestination();dest.channelCount=1;
 /* keep the audio graph running between lines: the take's sound must be continuous (silence too), or the recorder closes the gaps */
 const hum=ac.createConstantSource();hum.offset.value=0;hum.connect(dest);hum.start();
 const R=window.AN_RUN={ac,dest,stream:dest.stream,abort:null,src:null,v,pre,ev};
 const pre0='hy-'+v.id+':',inkBak={};for(const k of Object.keys(state.ink||{}))if(k.startsWith(pre0)){inkBak[k]=state.ink[k];delete state.ink[k]}
 if(camStream)camOff();AN.fx=[];AN.dotPos=null;state.beat=0;state.step=0;updateSlide();pen.sync();await anSettle();
 window.__aiRecOk=true;try{await startRecording()}finally{window.__aiRecOk=false}
 if(!record){window.AN_RUN=null;anStatus();Object.assign(state.ink,inkBak);ac.close();return toast('Auto-narrate: the recording did not start.')}
 let li=0,err=null;const total=cont?audio.manifest.lines.length:bufs.length,LOG=window.AN_LAST_LOG=[],lg=ev=>LOG.push([+recClock().toFixed(2),ev]);
 try{if(cont){lg('slide 1');await anRunContinuous(R,v,audio.manifest,bufs[0],lg)}
  else{for(let bi=0;bi<v.beats.length&&!R.abort;bi++){
   if(bi){state.beat=bi;state.step=0;updateSlide();pen.sync();await anSettle()}lg('slide '+(bi+1));await anWait(R,bi?450:900);
   let step=0,pend=[];const ls=hyLines(v,bi);
   const firePend=async()=>{let w=0;for(const p of pend){lg('point '+p.point);w=Math.max(w,anFire(p,v,bi))}pend=[];if(w)await anWait(R,w*1000)};
   for(let i=0;i<ls.length&&!R.abort;i++){const l=ls[i];
    if(l.say!=null){const buf=bufs[li++];anStatus('🤖 Auto-narrating · slide '+(bi+1)+'/'+v.beats.length+' · line '+li+'/'+total);
     for(const p of pend){const at=Math.max(0,Math.min(.95,+p.at||0))*buf.duration*1000;setTimeout(()=>{if(!R.abort){lg('point '+p.point);anFire(p,v,bi)}},at)}pend=[];
     lg('say '+li);await anPlay(R,buf);await anWait(R,anGap(l.say))}
    else if(l.appear!=null){await firePend();state.step=++step;lg('appear '+l.appear+(l.part!=null?' part '+l.part:''));updateSlide();await anSettle();await anWait(R,420)}
    else if(l.draw!=null){await firePend();await anWait(R,150);lg('mark '+l.draw);await anMarkDo(anMarkOf(l),v,bi);await anWait(R,350)}
    else if(l.point!=null){pend.push(l);if(!ls.slice(i+1).some(x=>x.say!=null))await firePend()}}
   await firePend();await anWait(R,650)}
  if(!R.abort)await anWait(R,1000)}}
 catch(e){err=e;console.error('auto-narrate',e)}
 const why=R.abort;anStatus();try{R.src?.stop()}catch{}stopRecording();document.getElementById('an-screen')?.remove();if(cont){updateSlide();pen.sync()}
 setTimeout(()=>{for(const k of Object.keys(state.ink))if(k.startsWith(pre0))delete state.ink[k];Object.assign(state.ink,inkBak);save();pen.sync();AN.fx=[];window.AN_RUN=null;ac.close().catch(()=>{})},300);
 if(err)toast('Auto-narrate stopped: '+(err.message||err)+' — the take so far is offered to keep or discard.');else if(why)toast('Auto-narrate '+why+'. Keep or discard the take.');
 else toast('🤖 Done. Watch the take, then Keep to save it like a normal recording.')}
window.anStart=anStart;window.AN_DIAG={hlTex,anResolve:(spec,bi,step)=>{const v=video();return anResolve(spec,v,bi,boardSvg(v,bi,step))},anPlan:id=>anPlan(D.videos[id],null),anMarkOf};
/* the 🤖 button on the slide bar (teacher only, AI videos only) */
setInterval(()=>{const q=document.getElementById('qrec');if(!q)return;const v=STUDIO?video():null,on=!!(v&&AI_VIDEOS.has(v.id)&&v.beats.every(b=>b.layout==='hybrid'));let b=document.getElementById('an-btn');
 if(!b){b=document.createElement('button');b.id='an-btn';b.type='button';b.textContent='🤖 Auto-narrate';b.title='Record this video automatically with your AI voice: slides, items, marks and pointer in sync with the AI audio';
  b.style.cssText='background:#ede9fe;color:#3b0764;border-color:#c4b5fd;font-weight:800';b.onclick=()=>anStart();}
 if(!b.isConnected)q.before(b);
 b.hidden=!on||!!record;b.disabled=!!window.AN_RUN},600);
window.addEventListener('keydown',e=>{if(!window.AN_RUN)return;const k=e.key;if(k==='Escape'){e.preventDefault();e.stopPropagation();anAbort('stopped');return}
 if(['p','P','x','X',' ','ArrowRight','ArrowLeft','PageDown','PageUp'].includes(k)&&!['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)){e.preventDefault();e.stopPropagation();toast('Auto-narrate is running — Esc or ■ Stop to stop it.')}},true);
"""

REPL = [
    # the highlight / pointer layer goes into every recorded frame (after the laser dot)
    ("ctx.fillStyle='#ee3d59';ctx.fill()}record.frame=requestAnimationFrame(draw)}draw();",
     "ctx.fillStyle='#ee3d59';ctx.fill()}if(window.anPaint)anPaint(ctx,1.2);record.lastPaint=performance.now();if(!record.inPaint)record.frame=requestAnimationFrame(draw)}"
     # 2026-10-09: a headless take froze on its first slide for 2 minutes - requestAnimationFrame stopped firing (the page
     # counted as hidden), so the recording canvas was never redrawn while the cues and sound went on. The recorder's
     # 30 fps frame grab now repaints the canvas itself when the draw loop has not run for 100 ms (CutRecorder.grab).
     "record.paint=()=>{if(!record)return;record.inPaint=1;try{draw()}finally{if(record)record.inPaint=0}};draw();"),
    # auto-narrate: AI audio instead of the microphone, no camera
    ("const useMic=$('#use-mic').checked,useCamera=$('#use-camera').checked;",
     "const useMic=window.AN_RUN?true:$('#use-mic').checked,useCamera=window.AN_RUN?false:$('#use-camera').checked;"),
    ("if(useMic)input=await getMic();", "if(window.AN_RUN)input=window.AN_RUN.stream;else if(useMic)input=await getMic();"),
    # faded preview off while auto-narrating (screen = recording)
    ("function ghostOn(){try{", "function ghostOn(){if(window.AN_RUN)return false;try{"),
    # auto-narrate: a slide state rasterised before the take is swapped in at once (no decode / first-paint stall)
    ("async function prepareSlideImage(){return new Promise(resolve=>{",
     "async function prepareSlideImage(){const anPre=window.AN_RUN?.pre?.get(currentSvg);if(anPre){++slideToken;slideImage=anPre;return anPre}return new Promise(resolve=>{"),
    # POINT lines in the script views and the script editor
    ("const hyLineText=l=>l.say!=null?l.say:", "const hyLineText=l=>l.say!=null?l.say:l.point!=null?anPointText(l):"),
    (":l.draw!=null?`<div class=\"hy-cue hy-draw\">", ":l.point!=null?anPointCue(l):l.draw!=null?`<div class=\"hy-cue hy-draw\">"),
    ("m=s.match(/^\\[DRAW:\\s*(.*)\\]$/i);if(m){out.push({draw:m[1].trim()});continue}",
     "m=s.match(/^\\[POINT:\\s*(.*)\\]$/i);if(m){out.push(anParsePoint(m[1]));continue}m=s.match(/^\\[DRAW:\\s*(.*)\\]$/i);if(m){out.push({draw:m[1].trim()});continue}"),
]


def apply(s):
    for old, new in REPL:
        assert s.count(old) == 1, ('studio_autonarrate anchor', s.count(old), old[:70])
        s = s.replace(old, new)
    k = s.find('async function startRecording(){')
    assert k > 0
    return s[:k] + JS.lstrip() + s[k:]
