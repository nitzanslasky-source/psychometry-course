"""Take editor (applied by build_verbal.py after studio_cut).

Edit a finished take: cut pieces out of the middle, or speed parts up (1.1× … 1.5×, voice pitch kept natural).
  - right after Stop: "✎ Edit" in the Keep / Discard bar (the bar then shows the edited take; Keep saves it)
  - any time later: "✎ Edit a take" in the studio toolbar → pick a take file; the edited copy is saved next to it as
    a NEW take (newer time stamp, so the upload script uses it; the original file is left untouched).

Timeline with the sound waveform and a line + title at every slide change; drag to select a part, I / O = start / end
at the playhead, Delete = cut out, Space = play (preview plays the take WITH the edits), ⌘Z = undo.
Saving re-encodes the take with Mediabunny (MPL-2.0, vendor/mediabunny.min.cjs, inlined unmodified); speed-ups keep
the voice pitch with a WSOLA time-stretch; slide chapters are moved to match the edited timeline.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

JS = r"""
/* ---- take editor: cut pieces out / speed parts up after recording ---- */
function teFmt(s){s=Math.max(0,s);const m=Math.floor(s/60),x=s-60*m;return m+':'+(x<9.95?'0':'')+x.toFixed(1)}
function teDur(d){return d<60?d.toFixed(1)+' s':teFmt(d)}
function teNorm(E){return E.filter(e=>e.b-e.a>0.02).sort((x,y)=>x.a-y.a)}
function teAdd(E,ed){const out=[];for(const e of E){if(e.b<=ed.a||e.a>=ed.b){out.push(e);continue}if(e.a<ed.a)out.push({...e,b:ed.a});if(e.b>ed.b)out.push({...e,a:ed.b})}if(ed.type!=='normal')out.push(ed);return teNorm(out)}
function teSegments(E,D){const segs=[];let t=0;for(const e of teNorm(E)){if(e.a>t)segs.push({a:t,b:e.a,s:1});if(e.type==='speed')segs.push({a:Math.max(t,e.a),b:e.b,s:e.s});t=Math.max(t,e.b)}if(t<D)segs.push({a:t,b:D,s:1});return segs.filter(s=>s.b-s.a>1e-3)}
function teMap(segs,t){let o=0;for(const s of segs){if(t<s.a)return o;if(t<s.b)return o+(t-s.a)/s.s;o+=(s.b-s.a)/s.s}return o}
function teLen(segs){return segs.reduce((o,s)=>o+(s.b-s.a)/s.s,0)}
function teChapters(ch,segs){const out=[];for(const c of ch||[]){const t=Math.round(teMap(segs,c.start)*10)/10;if(out.length&&out[out.length-1].start>=t)out.pop();if(!out.length||out[out.length-1].title!==c.title)out.push({start:t,title:c.title})}return out}
/* WSOLA time-stretch (rate > 1 = faster), same positions for every channel, keeps the pitch */
function teStretch(ch,rate,sr){const x=ch[0],len=x.length,N=Math.round(sr*.03)&~1,H=N>>1,tol=Math.round(sr*.008),Ha=H*rate,outLen=Math.round(len/rate);
 const w=new Float32Array(N);for(let i=0;i<N;i++)w[i]=.5-.5*Math.cos(2*Math.PI*i/N);
 const out=ch.map(()=>new Float32Array(outLen+N)),norm=new Float32Array(outLen+N);let prev=0;
 for(let k=0;k*H<outLen;k++){let pos=Math.round(k*Ha);
  if(k>0){const nat=prev+H,lo=Math.max(0,pos-tol),hi=Math.min(len-N,pos+tol);if(hi>=lo){let best=Math.min(Math.max(pos,lo),hi),bv=-Infinity;
   for(let p=lo;p<=hi;p+=2){let c=0;for(let i=0;i<N;i+=8){const q=nat+i;if(q<len)c+=x[q]*x[p+i]}if(c>bv){bv=c;best=p}}pos=best}}
  if(pos>len-1)pos=Math.max(0,len-N);const o=k*H;
  for(let c=0;c<ch.length;c++){const src=ch[c],dst=out[c];for(let i=0;i<N&&pos+i<len;i++)dst[o+i]+=src[pos+i]*w[i]}
  for(let i=0;i<N;i++)norm[o+i]+=w[i];prev=pos}
 for(let c=0;c<out.length;c++){const d=out[c];for(let i=0;i<outLen;i++)if(norm[i]>1e-3)d[i]/=norm[i]}
 return out.map(d=>d.subarray(0,outLen))}
async function teSegAudio(sink,seg,sr0,nch0){let sr=sr0,nch=nch0;const parts=[];
 for await(const s of sink.samples(seg.a,seg.b)){sr=s.sampleRate;nch=s.numberOfChannels;const f=s.numberOfFrames,chs=[];
  for(let c=0;c<nch;c++){const b=new Float32Array(f);s.copyTo(b,{planeIndex:c,format:'f32-planar'});chs.push(b)}parts.push({t:s.timestamp,chs,f});s.close()}
 const n=Math.max(0,Math.round((seg.b-seg.a)*sr)),ch=Array.from({length:nch},()=>new Float32Array(n));
 for(const p of parts){const off=Math.round((p.t-seg.a)*sr);for(let c=0;c<nch;c++){const i0=Math.max(0,-off),i1=Math.min(p.f,n-off);if(i1>i0)ch[c].set(p.chs[c].subarray(i0,i1),off+i0)}}
 return {sr,ch}}
async function tePeaks(blob,D,onp){const M=Mediabunny,input=new M.Input({source:new M.BlobSource(blob),formats:M.ALL_FORMATS}),at=await input.getPrimaryAudioTrack();if(!at)return null;
 const sink=new M.AudioSampleSink(at),B=.05,pk=new Float32Array(Math.ceil(D/B)+2);let k=0;
 for await(const s of sink.samples()){const f=s.numberOfFrames,buf=new Float32Array(f),sr=s.sampleRate,t0=s.timestamp;s.copyTo(buf,{planeIndex:0,format:'f32-planar'});s.close();
  for(let i=0;i<f;i+=4){const b=Math.floor((t0+i/sr)/B);if(b>=0&&b<pk.length){const a=Math.abs(buf[i]);if(a>pk[b])pk[b]=a}}if(++k%200===0)onp?.(pk)}
 return pk}
async function teExport(blob,E,D,onp){const M=Mediabunny,segs=teSegments(E,D),outD=teLen(segs);
 const input=new M.Input({source:new M.BlobSource(blob),formats:M.ALL_FORMATS}),vt=await input.getPrimaryVideoTrack(),at=await input.getPrimaryAudioTrack();
 const mp4=!/webm/i.test(blob.type||'')&&!/\.webm$/i.test(blob.name||'');
 const output=new M.Output({format:mp4?new M.Mp4OutputFormat({fastStart:'in-memory'}):new M.WebMOutputFormat(),target:new M.BufferTarget()});
 const vsrc=new M.VideoSampleSource({codec:mp4?'avc':'vp9',bitrate:8e6,keyFrameInterval:2});output.addVideoTrack(vsrc,{frameRate:30});
 let asrc=null;if(at){asrc=new M.AudioSampleSource({codec:mp4?'aac':'opus',bitrate:160e3});output.addAudioTrack(asrc)}
 await output.start();const vsink=new M.VideoSampleSink(vt),asink=at?new M.AudioSampleSink(at):null,sr0=at?.sampleRate||48000,nch0=at?.numberOfChannels||1;
 let outBase=0,lastOut=-1,aPos=0;
 for(const seg of segs){let pcm=null;
  if(asink){pcm=await teSegAudio(asink,seg,sr0,nch0);if(seg.s!==1)pcm.ch=teStretch(pcm.ch,seg.s,pcm.sr);
   const F=Math.round(pcm.sr*.004);for(const c of pcm.ch){const n=c.length;for(let i=0;i<F&&i<n;i++){const g=i/F;c[i]*=g;c[n-1-i]*=g}}}
  let aOff=0;const pushAudio=async tOut=>{if(!pcm)return;const want=Math.min(pcm.ch[0].length,Math.round((tOut-outBase)*pcm.sr));
   while(aOff<want){const n=Math.min(4096,want-aOff),data=new Float32Array(n*pcm.ch.length);pcm.ch.forEach((c,i)=>data.set(c.subarray(aOff,aOff+n),i*n));
    await asrc.add(new M.AudioSample({data,format:'f32-planar',numberOfChannels:pcm.ch.length,sampleRate:pcm.sr,timestamp:(aPos+aOff)/pcm.sr}));aOff+=n}};
  for await(const s of vsink.samples(seg.a,seg.b)){const t=Math.max(s.timestamp,seg.a);if(t>=seg.b){s.close();continue}const ot=outBase+(t-seg.a)/seg.s;
   if(ot<lastOut+1/30-.004){s.close();continue}s.setTimestamp(ot);s.setDuration(1/30);await vsrc.add(s);s.close();lastOut=ot;await pushAudio(ot+.5);onp?.(Math.min(1,ot/outD))}
  await pushAudio(Infinity);if(pcm)aPos+=pcm.ch[0].length;outBase+=(seg.b-seg.a)/seg.s}
 vsrc.close();asrc?.close();await output.finalize();
 return {blob:new Blob([output.target.buffer],{type:mp4?'video/mp4':'video/webm'}),segs}}

function openTakeEditor(blob,chapters,label){return new Promise(async done=>{
 if(!window.Mediabunny||!window.VideoEncoder){toast('The take editor needs a current desktop Chrome or Edge.');return done(null)}
 chapters=(chapters||[]).filter((c,i,a)=>i===0||c.title!==a[i-1].title);
 const box=document.createElement('div');box.id='take-editor';
 box.innerHTML=`<style>
#take-editor{position:fixed;inset:0;z-index:10001;background:#0b1f1d;color:#eef3fb;display:flex;flex-direction:column;gap:8px;padding:10px 16px;font-family:inherit;font-size:14px}
#take-editor button{padding:6px 11px;border-radius:9px;border:1px solid #2c5a55;background:#123331;color:#eef3fb;font-weight:600;cursor:pointer;font-size:13px}
#take-editor button:hover{background:#1b4541}#take-editor button:disabled{opacity:.45;cursor:default}
#take-editor .te-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}#take-editor .te-sp{flex:1}
#take-editor .te-cut{border-color:#b91c1c;color:#fecaca}#take-editor .te-spd{border-color:#3b82f6;color:#dbeafe}
#take-editor .te-main{flex:1;min-height:0;display:flex;justify-content:center}#take-editor video{max-width:100%;max-height:100%;background:#000;border-radius:8px}
#te-canvas{width:100%;height:130px;display:block;border-radius:8px;cursor:crosshair;touch-action:none}
#te-edits{display:flex;gap:6px;flex-wrap:wrap;max-height:64px;overflow:auto}#te-edits span{padding:3px 8px;border-radius:7px;background:#123331;cursor:pointer;font-size:12px}
#te-edits b{margin-left:6px;color:#fca5a5;cursor:pointer}#te-help{color:#9fb7b2;font-size:12px}
#te-progress{position:absolute;inset:0;background:#0b1f1dd9;display:grid;place-items:center;font-size:18px;font-weight:700}
#te-progress div.bar{width:min(520px,80vw);height:10px;border-radius:5px;background:#123331;margin-top:12px;overflow:hidden}#te-progress i{display:block;height:100%;width:0;background:#2dd4bf}
</style>
<div class="te-row"><b style="font-size:18px">✎ Edit take</b><span style="color:#9fb7b2">${esc(label||'')}</span><span class="te-sp"></span><span id="te-len"></span>
<button id="te-cancel">Cancel</button><button id="te-save" style="background:#0f766e;border-color:#0f766e;color:#fff;font-weight:800;padding:8px 18px">Save edited take</button></div>
<div class="te-main"><video id="te-video" playsinline></video></div>
<div class="te-row"><button id="te-play">▶ Play</button><span id="te-time" style="font-variant-numeric:tabular-nums;min-width:250px"></span>
<label style="display:flex;gap:5px;align-items:center"><input type="checkbox" id="te-pv" checked> play with my edits</label><span class="te-sp"></span>
<span style="color:#9fb7b2">Zoom</span><button id="te-zout">−</button><button id="te-zin">+</button><button id="te-zall">All</button></div>
<canvas id="te-canvas"></canvas>
<div class="te-row"><span id="te-sel" style="min-width:230px;color:#fde68a"></span><button id="te-in" title="I">[ Start here</button><button id="te-out" title="O">] End here</button><button id="te-psel">▶ Play selection</button>
<span style="width:10px"></span><button class="te-cut" id="te-docut" title="Delete">✂ Cut out</button><span style="color:#9fb7b2;margin-left:6px">Speed up:</span>
${[1.1,1.2,1.3,1.5].map(s=>`<button class="te-spd" data-spd="${s}">${s}×</button>`).join('')}<button id="te-normal" title="Remove edits in the selection">Normal</button>
<span class="te-sp"></span><span style="color:#9fb7b2">Whole take:</span>${[1.1,1.2].map(s=>`<button class="te-spd" data-all="${s}">${s}×</button>`).join('')}<button id="te-undo" title="⌘Z">↶ Undo</button></div>
<div id="te-edits"></div>
<div id="te-help">Drag on the timeline to select a part (drag its yellow edges to adjust) · click = jump there · I / O = start / end of the selection at the playhead · Delete = cut out · Space = play · ← → = 1 s (⇧ 5 s, ⌥ 0.1 s) · scroll on the timeline = zoom, sideways = move · lines on the timeline = slide changes</div>
<div id="te-progress" hidden><div style="text-align:center"><div id="te-ptext">Saving…</div><div class="bar"><i></i></div></div></div>`;
 (document.fullscreenElement||document.body).append(box);
 const $e=id=>box.querySelector('#'+id),vid=$e('te-video'),cv=$e('te-canvas'),url=URL.createObjectURL(blob);vid.src=url;vid.preservesPitch=true;
 let D=0;try{const inp=new Mediabunny.Input({source:new Mediabunny.BlobSource(blob),formats:Mediabunny.ALL_FORMATS});D=await inp.computeDuration()}catch(e){console.warn(e)}
 if(!(D>0)){await new Promise(r=>{if(vid.readyState>=1)r();else vid.onloadedmetadata=r});D=isFinite(vid.duration)?vid.duration:0}
 if(!(D>0)){box.remove();URL.revokeObjectURL(url);toast('Could not read this take.');return done(null)}
 let E=[],undo=[],sel=null,v0=0,v1=D,peaks=null,drag=null,playSel=null,raf=0,armCancel=false,busy=false;const B=.05;
 tePeaks(blob,D,p=>{peaks=p}).then(p=>{peaks=p}).catch(e=>console.warn('waveform',e));
 const W=()=>cv.clientWidth,X=t=>(t-v0)/(v1-v0)*W(),T=x=>Math.max(0,Math.min(D,v0+x/W()*(v1-v0)));
 const change=f=>{undo.push(E);if(undo.length>100)undo.shift();E=f(E);armCancel=false;$e('te-cancel').textContent='Cancel';list()};
 function list(){const segs=teSegments(E,D),L=teLen(segs);$e('te-len').innerHTML='Length <b>'+teFmt(D)+'</b>'+(E.length?' → <b style="color:#5eead4">'+teFmt(L)+'</b> (−'+teDur(D-L)+')':'');
  $e('te-edits').innerHTML=E.map((e,i)=>`<span data-i="${i}">${e.type==='cut'?'✂ cut':'⏩ '+e.s+'×'} ${teFmt(e.a)} – ${teFmt(e.b)} (${e.type==='cut'?teDur(e.b-e.a):'saves '+teDur((e.b-e.a)*(1-1/e.s))})<b data-x="${i}" title="Remove this edit">×</b></span>`).join('')||'<span style="background:none;color:#9fb7b2;cursor:default">No edits yet.</span>';
  $e('te-edits').querySelectorAll('[data-x]').forEach(b=>b.onclick=ev=>{ev.stopPropagation();const k=+b.dataset.x;change(E=>E.filter((_,j)=>j!==k))});
  $e('te-edits').querySelectorAll('[data-i]').forEach(s=>s.onclick=()=>{const e=E[+s.dataset.i];if(!e)return;sel={a:e.a,b:e.b};seek(Math.max(0,e.a-2))});showSel()}
 function showSel(){$e('te-sel').textContent=sel?'Selected '+teFmt(sel.a)+' – '+teFmt(sel.b)+' ('+teDur(sel.b-sel.a)+')':'Nothing selected'}
 function seek(t){vid.currentTime=Math.max(0,Math.min(D-.01,t));const span=v1-v0;if(t<v0||t>v1){v0=Math.max(0,Math.min(D-span,t-span*.2));v1=v0+span}}
 function need(){if(!sel||sel.b-sel.a<.05){toast('Select a part first: drag on the timeline, or use [ Start here / ] End here.');return false}return true}
 function zoom(f,c){const span=Math.max(2,Math.min(D,(v1-v0)*f));c=c??(v0+v1)/2;let a=c-(c-v0)*span/(v1-v0);a=Math.max(0,Math.min(D-span,a));v0=a;v1=a+span}
 function draw(){const dpr=devicePixelRatio||1,w=cv.clientWidth,h=cv.clientHeight;if(cv.width!==Math.round(w*dpr)||cv.height!==Math.round(h*dpr)){cv.width=Math.round(w*dpr);cv.height=Math.round(h*dpr)}
  const g=cv.getContext('2d');g.setTransform(dpr,0,0,dpr,0,0);g.fillStyle='#10302d';g.fillRect(0,0,w,h);const top=18,wh=h-top-18,mid=top+wh/2;
  if(peaks){g.fillStyle='#5fb3a6';for(let x=0;x<w;x++){const i0=Math.floor(T(x)/B),i1=Math.floor(T(x+1)/B);let m=0;for(let i=i0;i<=i1;i++)if(peaks[i]>m)m=peaks[i];const hh=Math.max(.5,Math.min(1,m*1.8)*wh/2);g.fillRect(x,mid-hh,1,2*hh)}}
  else{g.fillStyle='#9fb7b2';g.font='12px system-ui';g.fillText('reading the sound…',8,mid)}
  g.font='bold 12px system-ui';for(const e of E){const x0=X(e.a),x1=X(e.b);if(x1<0||x0>w)continue;g.fillStyle=e.type==='cut'?'rgba(220,38,38,.6)':'rgba(59,130,246,.45)';g.fillRect(x0,top,x1-x0,wh);
   if(x1-x0>30){g.fillStyle='#fff';g.fillText(e.type==='cut'?'✂ cut':e.s+'×',Math.max(x0,0)+4,top+14)}}
  if(sel){const x0=X(sel.a),x1=X(sel.b);g.fillStyle='rgba(250,204,21,.25)';g.fillRect(x0,top,x1-x0,wh);g.fillStyle='#facc15';g.fillRect(x0-1,top,3,wh);g.fillRect(x1-1,top,3,wh)}
  g.font='11px system-ui';let last=-1e9;for(const c of chapters){const x=X(c.start);if(x<0||x>w)continue;g.fillStyle='#7ea39d';g.fillRect(x,0,1,h-18);if(x-last>110){g.fillStyle='#d6e8e4';g.fillText(String(c.title).slice(0,24),x+3,12);last=x}}
  const span=v1-v0,step=[.5,1,2,5,10,15,30,60,120,300].find(s=>w/(span/s)>=70)||600;g.fillStyle='#9fb7b2';for(let t=Math.ceil(v0/step)*step;t<v1;t+=step){const x=X(t);g.fillRect(x,h-18,1,5);g.fillText(teFmt(t).replace(/\.0$/,''),x+2,h-4)}
  const px=X(vid.currentTime);g.fillStyle='#fff';g.fillRect(px-1,0,2,h)}
 function tick(){if(!vid.paused&&!vid.seeking){const t=vid.currentTime;if(playSel&&t>=playSel.b){vid.pause();playSel=null}
   if($e('te-pv').checked){const e=E.find(e=>t>=e.a&&t<e.b);if(e&&e.type==='cut'&&!playSel)vid.currentTime=Math.min(D,e.b+.001);const r=e&&e.type==='speed'?e.s:1;if(vid.playbackRate!==r)vid.playbackRate=r}else if(vid.playbackRate!==1)vid.playbackRate=1;
   if(t>v1||t<v0){const span=v1-v0;v0=Math.max(0,Math.min(D-span,t-span*.05));v1=v0+span}}
  const t=vid.currentTime;$e('te-time').textContent=teFmt(t)+' / '+teFmt(D)+(E.length?'  ·  edited: '+teFmt(teMap(teSegments(E,D),t)):'');
  $e('te-play').textContent=vid.paused?'▶ Play':'❚❚ Pause';draw();raf=requestAnimationFrame(tick)}
 const play=()=>{if(vid.paused){playSel=null;vid.play()}else vid.pause()};
 cv.onpointerdown=e=>{const r=cv.getBoundingClientRect(),x=e.clientX-r.left,t=T(x);cv.setPointerCapture(e.pointerId);
  if(sel&&Math.abs(X(sel.a)-x)<7)drag={m:'a'};else if(sel&&Math.abs(X(sel.b)-x)<7)drag={m:'b'};else if(e.shiftKey&&sel)drag={m:t<sel.a?'a':'b'};else drag={m:'n',t0:t,x0:x}};
 cv.onpointermove=e=>{const r=cv.getBoundingClientRect(),x=e.clientX-r.left,t=T(x);
  if(!drag){cv.style.cursor=sel&&(Math.abs(X(sel.a)-x)<7||Math.abs(X(sel.b)-x)<7)?'ew-resize':'crosshair';return}
  if(drag.m==='n'){if(Math.abs(x-drag.x0)>3)sel={a:Math.min(drag.t0,t),b:Math.max(drag.t0,t)}}
  else{sel={...sel,[drag.m]:t};if(sel.a>sel.b){sel={a:sel.b,b:sel.a};drag.m=drag.m==='a'?'b':'a'}}showSel()};
 cv.onpointerup=e=>{const r=cv.getBoundingClientRect(),x=e.clientX-r.left;if(drag?.m==='n'&&Math.abs(x-drag.x0)<=3)seek(T(x));drag=null};
 cv.addEventListener('wheel',e=>{e.preventDefault();const r=cv.getBoundingClientRect();if(Math.abs(e.deltaX)>Math.abs(e.deltaY)||e.shiftKey){const d=(e.shiftKey?e.deltaY:e.deltaX)/W()*(v1-v0),span=v1-v0;v0=Math.max(0,Math.min(D-span,v0+d));v1=v0+span}else zoom(Math.exp(e.deltaY*.003),T(e.clientX-r.left))},{passive:false});
 $e('te-play').onclick=play;$e('te-zin').onclick=()=>zoom(.5,vid.currentTime);$e('te-zout').onclick=()=>zoom(2,vid.currentTime);$e('te-zall').onclick=()=>{v0=0;v1=D};
 const setIn=()=>{const t=vid.currentTime;sel=!sel||sel.b<=t?{a:t,b:Math.min(D,t+1)}:{a:t,b:sel.b};showSel()},setOut=()=>{const t=vid.currentTime;sel=!sel||sel.a>=t?{a:Math.max(0,t-1),b:t}:{a:sel.a,b:t};showSel()};
 $e('te-in').onclick=setIn;$e('te-out').onclick=setOut;
 $e('te-psel').onclick=()=>{if(!need())return;vid.currentTime=sel.a;playSel=sel;vid.playbackRate=1;vid.play()};
 const cut=()=>{if(!need())return;const s=sel;change(E=>teAdd(E,{type:'cut',a:s.a,b:s.b}));sel=null;showSel();if(vid.currentTime>s.a&&vid.currentTime<s.b)vid.currentTime=s.b};
 $e('te-docut').onclick=cut;
 box.querySelectorAll('[data-spd]').forEach(b=>b.onclick=()=>{if(!need())return;const s=sel;change(E=>teAdd(E,{type:'speed',a:s.a,b:s.b,s:+b.dataset.spd}))});
 box.querySelectorAll('[data-all]').forEach(b=>b.onclick=()=>change(E=>{const cuts=E.filter(e=>e.type==='cut'),out=[...cuts];let t=0;for(const c of teNorm(cuts)){if(c.a>t)out.push({type:'speed',a:t,b:c.a,s:+b.dataset.all});t=Math.max(t,c.b)}if(t<D)out.push({type:'speed',a:t,b:D,s:+b.dataset.all});return teNorm(out)}));
 $e('te-normal').onclick=()=>{if(!need())return;const s=sel;change(E=>teAdd(E,{type:'normal',a:s.a,b:s.b}))};
 const doUndo=()=>{if(!undo.length)return toast('Nothing to undo.');E=undo.pop();list()};$e('te-undo').onclick=doUndo;
 const close=res=>{cancelAnimationFrame(raf);document.removeEventListener('keydown',key,true);vid.pause();vid.removeAttribute('src');vid.load();URL.revokeObjectURL(url);box.remove();done(res)};
 $e('te-cancel').onclick=()=>{if(busy)return;if(E.length&&!armCancel){armCancel=true;$e('te-cancel').textContent='Discard my edits?';return}close(null)};
 $e('te-save').onclick=async()=>{if(busy)return;if(!E.length){toast('No edits yet — nothing to save.');return}busy=true;vid.pause();const pg=$e('te-progress'),t0=Date.now();pg.hidden=false;
  try{const r=await teExport(blob,E,D,p=>{pg.querySelector('i').style.width=(p*100).toFixed(1)+'%';const el=(Date.now()-t0)/1000,left=p>.03?el/p-el:0;
    $e('te-ptext').textContent='Saving the edited take… '+Math.round(p*100)+'%'+(left>3?' · about '+(left<60?Math.round(left)+' s':Math.round(left/60)+' min')+' left':'')});
   close({blob:r.blob,chapters:teChapters(chapters,r.segs)})}
  catch(e){console.error('take edit',e);pg.hidden=true;busy=false;toast('Could not save the edited take: '+(e.message||e))}};
 const key=e=>{if(busy){e.stopPropagation();return}if(e.target.tagName==='INPUT'&&e.target.type!=='checkbox')return;const k=e.key,mod=e.metaKey||e.ctrlKey;e.stopPropagation();
  if(mod&&(k==='z'||k==='Z')){e.preventDefault();doUndo()}else if(mod)return;
  else if(k===' '){e.preventDefault();play()}else if(k==='i'||k==='I'){e.preventDefault();setIn()}else if(k==='o'||k==='O'){e.preventDefault();setOut()}
  else if(k==='Delete'||k==='Backspace'){e.preventDefault();cut()}else if(k==='Escape'){e.preventDefault();sel=null;showSel()}
  else if(k==='ArrowLeft'||k==='ArrowRight'){e.preventDefault();const d=e.altKey?.1:e.shiftKey?5:1;seek(vid.currentTime+(k==='ArrowLeft'?-d:d))}
  else if(k==='+'||k==='='){zoom(.5,vid.currentTime)}else if(k==='-'){zoom(2,vid.currentTime)}};
 document.addEventListener('keydown',key,true);list();raf=requestAnimationFrame(tick)})}

/* edit a saved take later: pick the file; the edited copy is saved as a NEW take beside it */
async function rfTopicDir(v,create){if(!RF.handle)return null;let p=await RF.handle.queryPermission({mode:'readwrite'});if(p!=='granted')p=await RF.handle.requestPermission({mode:'readwrite'});if(p!=='granted')return null;
 const T=(D.topics||[]).find(t=>+t.id===+v.topic),d1=await RF.handle.getDirectoryHandle(rfSubject(v.topic),{create});return d1.getDirectoryHandle(rfClean('Topic '+String(v.topic).padStart(2,'0')+' - '+(T?T.title:'')),{create})}
async function editSavedTake(){if(record)return toast('Stop the recording first.');if(!window.showOpenFilePicker)return toast('Editing saved takes needs desktop Chrome or Edge.');
 if(!RF.handle)RF.handle=await rfGet();let fh;
 try{[fh]=await window.showOpenFilePicker({id:'studio-edit-take',...(RF.handle?{startIn:RF.handle}:{}),types:[{description:'Recorded takes',accept:{'video/mp4':['.mp4'],'video/webm':['.webm']}}]})}catch{return}
 const file=await fh.getFile(),m=file.name.match(/^(.+)-\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z\.(mp4|webm)$/),v=m&&D.videos[m[1]];let chapters=[];
 if(v){try{const d=await rfTopicDir(v,false),cf=await d.getFileHandle(file.name.replace(/\.(mp4|webm)$/,'.chapters.json'));chapters=JSON.parse(await (await cf.getFile()).text()).chapters||[]}catch{}}
 const res=await openTakeEditor(file,chapters,file.name);if(!res)return;
 const ext=res.blob.type.includes('mp4')?'mp4':'webm';
 if(!v){const nm=file.name.replace(/\.(mp4|webm)$/i,'')+'-edited.'+ext;downloadBlob(nm,res.blob);return toast('Edited take downloaded: '+nm)}
 const name=v.id+'-'+new Date().toISOString().replace(/[:.]/g,'-')+'.'+ext,where=await saveTakeFile(v,name,res.blob);
 if(where&&res.chapters.length)await saveTakeFile(v,name.replace(/\.(webm|mp4)$/,'.chapters.json'),new Blob([JSON.stringify({videoId:v.id,chapters:res.chapters},null,1)],{type:'application/json'}));
 state.media[v.id]={type:'file',name,path:where||'Downloads/'+name};save();toast('Edited take saved as a new take: '+(where||name)+' (the original is kept)')}
document.addEventListener('click',e=>{if(e.target.closest?.('#qedit'))editSavedTake()});
"""

REPL = [
    # toolbar: ✎ Edit a take, next to the folder button
    ('<button id="qfolder" title="Choose where recordings are saved">📁 Folder</button>',
     '<button id="qfolder" title="Choose where recordings are saved">📁 Folder</button>'
     '<button id="qedit" title="Edit a saved take: cut pieces out, speed parts up">✎ Edit a take</button>'),
    # Keep / Discard bar: ✎ Edit (the bar then shows the edited take; Keep saves the edited one)
    ("function askKeepTake(blob){return new Promise(res=>{const url=URL.createObjectURL(blob),box=",
     "function askKeepTake(blob,ch){return new Promise(res=>{let url=URL.createObjectURL(blob),edited=null;const box="),
    ("Discard</button></div></div>';",
     "Discard</button>"
     "<button id=\"take-edit\" style=\"padding:11px 20px;border-radius:10px;border:1px solid #d8e6e3;background:#fff;color:#0f766e;font-weight:700;font-size:15px;cursor:pointer\">✎ Edit</button></div></div>';"),
    ("const done=keep=>{document.removeEventListener('keydown',key,true);box.remove();document.body.style.paddingBottom=pad;URL.revokeObjectURL(url);res(keep)};",
     "const done=keep=>{document.removeEventListener('keydown',key,true);box.remove();document.body.style.paddingBottom=pad;URL.revokeObjectURL(url);res(keep&&edited?edited:keep)};"),
    ("const key=e=>{if(e.target&&e.target.tagName==='VIDEO')return;",
     "const key=e=>{if(document.getElementById('take-editor'))return;if(e.target&&e.target.tagName==='VIDEO')return;"),
    ("box.querySelector('#take-discard').onclick=()=>done(false)})}",
     "box.querySelector('#take-discard').onclick=()=>done(false);"
     "box.querySelector('#take-edit').onclick=async()=>{const pv=box.querySelector('video');pv.pause();"
     "const r=await openTakeEditor(edited?edited.blob:blob,edited?edited.chapters:(ch||[]),'this take');if(!r)return;"
     "edited=r;URL.revokeObjectURL(url);url=URL.createObjectURL(r.blob);pv.src=url;"
     "box.querySelector('#take-edit').textContent='✎ Edit again';toast('Edited. Watch it here, then Keep to save the edited take.')}})}"),
    # the save flow uses the edited take (and its moved chapters) when there is one
    ("const blob=new Blob(chunks,{type:rec.mimeType||'video/webm'}),ext=", "let blob=new Blob(chunks,{type:rec.mimeType||'video/webm'}),ext="),
    ("if(!(await askKeepTake(blob))){",
     "const kk=await askKeepTake(blob,r.chapters);if(kk&&kk.blob){blob=kk.blob;r.chapters=kk.chapters}if(!kk){"),
]


def apply(s):
    for old, new in REPL:
        assert s.count(old) == 1, ('studio_edit anchor', s.count(old), old[:70])
        s = s.replace(old, new)
    k = s.find('async function startRecording(){')
    assert k > 0
    s = s[:k] + JS.lstrip() + s[k:]
    lib = open(os.path.join(HERE, 'vendor', 'mediabunny.min.cjs'), encoding='utf-8').read()
    lib = lib.replace('if (typeof module === "object" && typeof module.exports === "object") Object.assign(module.exports, Mediabunny)', '')
    assert '</script' not in lib
    m = '<meta charset="utf-8">'
    assert s.count(m) >= 1
    k = s.find(m) + len(m)
    return s[:k] + '<script>' + lib + '</script>' + s[k:]
