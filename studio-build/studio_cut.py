"""Cut back while recording (applied by build_verbal.py after studio_ui).

Made a mistake 12 minutes into a take? Pause (P), press ✂ Cut back (or X), pick how much of the end to remove
(3 s … 1 min, or drag to any point, with a picture of that moment and "listen" buttons), press Cut. The studio drops
that part of the take on the spot, goes back to the slide / step / pen ink you had at that moment, and you Continue.
You can cut as many times as you like; the finished take has no trace of the removed parts.

How: in desktop Chrome/Edge the take is recorded with WebCodecs (H.264 + AAC in an .mp4, or VP9 + Opus in a .webm)
and kept as encoded pieces until Stop, so a cut is instant and exact (no re-encoding). The file is assembled at Stop
with mp4-muxer / webm-muxer (MIT, inlined from vendor/). Browsers without WebCodecs fall back to the old
MediaRecorder (pause works, cut is not offered).
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))


def _lib(name):
    s = open(os.path.join(HERE, 'vendor', name), encoding='utf-8').read()
    return re.sub(r'//# sourceMappingURL=\S+', '', s).replace('"use strict";', '', 1) + '\n'


JS = r"""
/* ---- cut-able recorder: WebCodecs; the take is kept as encoded pieces so "Cut back" (while paused) removes the end
   instantly and exactly; the file is assembled at Stop (MP4 H.264+AAC, else WebM VP9+Opus) ---- */
const CUT={ok:!!(window.VideoEncoder&&window.AudioEncoder&&window.VideoFrame&&window.AudioData&&window.MediaStreamTrackProcessor)};
function recClock(){const r=record;if(!r)return 0;const now=Date.now();return Math.max(0,(now-r.started-r.pausedMs-(r.pausedAt?now-r.pausedAt:0))/1000)}
async function cutVideoCodec(){const base={width:1920,height:1080,bitrate:8000000,framerate:30};
 for(const [codec,mux,extra] of [['avc1.640028','mp4',{avc:{format:'avc'}}],['avc1.4d0028','mp4',{avc:{format:'avc'}}],['vp09.00.40.08','webm',{}]]){
  const cfg={...base,codec,...extra};try{if((await VideoEncoder.isConfigSupported(cfg)).supported)return {cfg,mux}}catch{}}return null}
async function cutAudioCodec(mux,sampleRate,numberOfChannels){
 for(const [codec,name] of (mux==='mp4'?[['mp4a.40.2','aac'],['opus','opus']]:[['opus','opus']])){const cfg={codec,sampleRate,numberOfChannels,bitrate:160000};
  try{if((await AudioEncoder.isConfigSupported(cfg)).supported)return {cfg,name}}catch{}}return null}
class CutRecorder{
 constructor(canvas,track,vc){Object.assign(this,{canvas,track,vc,mimeType:vc.mux==='mp4'?'video/mp4':'video/webm',state:'inactive',v:[],a:[],vmeta:null,ameta:null,acfg:null,
  lastV:-1,lastKey:-1e9,forceKey:true,aBase:null,aSamples:0,aEnd:0,pcm:[],thumbs:[],err:null,cutCount:0,cutSec:0,marks:[0]});
  this.venc=new VideoEncoder({output:(c,m)=>{if(m?.decoderConfig&&!this.vmeta)this.vmeta=m;this.v.push(c)},error:e=>this.fail(e)});this.venc.configure(vc.cfg)}
 fail(e){console.error('recorder',e);if(this.err)return;this.err=e;this.onerror?.(e)}
 start(){this.state=this.holdStart?'paused':'recording';this.timer=setInterval(()=>this.grab(),1000/30);this.thumbTimer=setInterval(()=>this.thumb(),1000);if(this.track)this.readAudio()}
 grab(){if(this.state!=='recording'||this.venc.state!=='configured')return;const ts=Math.round(recClock()*1e6);if(ts<=this.lastV)return;
  if(this.venc.encodeQueueSize>6&&!this.forceKey)return;let f;try{f=new VideoFrame(this.canvas,{timestamp:ts,duration:33333})}catch{return}
  const key=this.forceKey||ts-this.lastKey>=2e6;if(key){this.lastKey=ts;this.forceKey=false}this.lastV=ts;
  try{this.venc.encode(f,{keyFrame:key})}catch(e){this.fail(e)}f.close()}
 thumb(){if(this.state!=='recording')return;try{const c=this.tc||(this.tc=Object.assign(document.createElement('canvas'),{width:320,height:180}));
  c.getContext('2d').drawImage(this.canvas,0,0,320,180);this.thumbs.push({t:recClock(),url:c.toDataURL('image/jpeg',.6)})}catch{}}
 async readAudio(){const reader=this.reader=new MediaStreamTrackProcessor({track:this.track,maxBufferSize:600}).readable.getReader();   /* ~6 s of 10 ms sound frames queued: a busy main thread no longer makes the processor DROP sound (it kept ~10, so a 0.1-0.4 s stall lost words and pulled the rest of the take early) */
  for(;;){let r;try{r=await reader.read()}catch{break}if(r.done)break;const d=r.value;try{if(this.state==='recording')await this.takeAudio(d)}catch(e){this.fail(e)}finally{d.close()}}}
 async ensureAenc(sr,nch){if(this.aenc)return true;const pick=await cutAudioCodec(this.vc.mux,sr,nch);if(!pick)return false;
  this.acfg={...pick.cfg,name:pick.name};this.aenc=new AudioEncoder({output:(c,m)=>{if(m?.decoderConfig&&!this.ameta)this.ameta=m;this.a.push(c)},error:e=>this.fail(e)});this.aenc.configure(pick.cfg);return true}
 /* encode raw sound (one Float32Array per channel) at timestamp ts (µs), converted to the encoder's channels / rate; returns its length in µs */
 encodePcm(chs,sr,ts){const C=this.acfg.numberOfChannels,R=this.acfg.sampleRate;let x=chs;
  if(x.length!==C){const m=new Float32Array(x[0].length);for(const c of x)for(let i=0;i<m.length;i++)m[i]+=c[i]/x.length;x=Array.from({length:C},()=>m)}
  if(sr!==R){const n=Math.round(x[0].length*R/sr);x=x.map(c=>{const o=new Float32Array(n);for(let i=0;i<n;i++){const p=i*sr/R,j=Math.floor(p),f=p-j;o[i]=(c[j]||0)*(1-f)+(c[Math.min(j+1,c.length-1)]||0)*f}return o})}
  const n=x[0].length;if(!n)return 0;const buf=new Float32Array(n*C);x.forEach((c,i)=>buf.set(c,i*n));
  const ad=new AudioData({format:'f32-planar',sampleRate:R,numberOfFrames:n,numberOfChannels:C,timestamp:ts,data:buf});this.aenc.encode(ad);ad.close();
  const pc=new Int16Array(n);for(let k=0;k<n;k++)pc[k]=Math.max(-1,Math.min(1,x[0][k]))*32767;this.pcm.push({t:ts/1e6,sr:R,d:pc});return Math.round(n/R*1e6)}
 async takeAudio(d){
  if(!this.aenc&&!(await this.ensureAenc(d.sampleRate,d.numberOfChannels))){this.track=null;this.reader?.cancel();toast('This browser cannot encode the microphone; the take will be silent.');return}
  if(this.aBase===null){this.aBase=Math.max(Math.round(recClock()*1e6),this.aEnd);this.aSamples=0;this.aT0=d.timestamp;this.aIn=0}
  /* sound frames that still went missing (their timestamps jump ahead): fill the hole with silence, so everything after it
     stays in sync with the picture instead of sliding earlier */
  const R0=this.acfg.sampleRate,gap=d.timestamp-(this.aT0+this.aIn/d.sampleRate*1e6);
  if(gap>25000&&gap<1e7){let k=Math.round(gap/1e6*d.sampleRate);this.aIn+=k;(window.__recAudioGaps=window.__recAudioGaps||[]).push([+(this.aEnd/1e6).toFixed(2),Math.round(gap/1000)]);console.warn('recorder: sound gap',Math.round(gap/1000),'ms filled with silence');
   while(k>0){const m=Math.min(k,4800),ts=this.aBase+Math.round(this.aSamples/R0*1e6),dur=this.encodePcm([new Float32Array(m)],d.sampleRate,ts);this.aSamples+=Math.round(dur*R0/1e6);this.aEnd=ts+dur;k-=m}}
  this.aIn+=d.numberOfFrames;
  const n=d.numberOfFrames,ch=d.numberOfChannels,chs=[];for(let i=0;i<ch;i++){const b=new Float32Array(n);d.copyTo(b,{planeIndex:i,format:'f32-planar'});chs.push(b)}
  const R=this.acfg.sampleRate,ts=this.aBase+Math.round(this.aSamples/R*1e6),dur=this.encodePcm(chs,d.sampleRate,ts);
  this.aSamples+=Math.round(dur*R/1e6);this.aEnd=ts+dur}
 /* continue a saved take: re-encode its first `cut` seconds (picture + sound) as the start of this take */
 async seed(blob,cut,onp){const M=Mediabunny,input=new M.Input({source:new M.BlobSource(blob),formats:M.ALL_FORMATS}),vt=await input.getPrimaryVideoTrack(),at=await input.getPrimaryAudioTrack();
  if(!vt)throw Error('This file has no video in it.');
  const tc=Object.assign(document.createElement('canvas'),{width:320,height:180}),tg=tc.getContext('2d');let fc=null,fg=null,lastThumb=-9,last=-1,n=0;
  for await(const s of new M.VideoSampleSink(vt).samples(0,cut)){const t=s.timestamp,ts=Math.round(Math.max(0,t)*1e6);if(t>=cut||ts<=last){s.close();continue}
   const src=s.toVideoFrame();let fr;
   if(src.displayWidth===1920&&src.displayHeight===1080)fr=new VideoFrame(src,{timestamp:ts,duration:33333});
   else{if(!fc){fc=new OffscreenCanvas(1920,1080);fg=fc.getContext('2d')}fg.drawImage(src,0,0,1920,1080);fr=new VideoFrame(fc,{timestamp:ts,duration:33333})}
   if(t-lastThumb>=2){tg.drawImage(src,0,0,320,180);this.thumbs.push({t,url:tc.toDataURL('image/jpeg',.6)});lastThumb=t}
   src.close();s.close();
   while(this.venc.encodeQueueSize>6)await new Promise(r=>setTimeout(r,4));
   const key=last<0||ts-this.lastKey>=2e6;if(key)this.lastKey=ts;this.venc.encode(fr,{keyFrame:key});fr.close();last=ts;if(++n%15===0)onp?.(Math.min(.85,t/cut*.85))}
  if(at)for await(const s of new M.AudioSampleSink(at).samples(0,cut)){const t=s.timestamp,f=s.numberOfFrames,sr=s.sampleRate,keep=Math.max(0,Math.min(f,Math.round((cut-t)*sr)));
   const chs=[];if(keep)for(let c=0;c<s.numberOfChannels;c++){const b=new Float32Array(f);s.copyTo(b,{planeIndex:c,format:'f32-planar'});chs.push(b.slice(0,keep))}s.close();
   if(!keep||t<0)continue;if(!this.aenc&&!(await this.ensureAenc(sr,chs.length)))break;
   const ts=Math.max(Math.round(t*1e6),this.aEnd);this.aEnd=ts+this.encodePcm(chs,sr,ts);onp?.(.85+.1*Math.min(1,t/cut))}
  onp?.(.97);await this.venc.flush();if(this.aenc)await this.aenc.flush();
  this.lastV=last;this.forceKey=true;this.aBase=null;this.aEnd=Math.max(this.aEnd,Math.round(cut*1e6));this.marks=[0,cut];this.holdStart=true;onp?.(1)}
 /* a short playable clip of the take so far (from the key frame before 'from' up to 'to') — for the Cut back preview */
 async clip(from,to){try{await this.venc.flush();if(this.aenc)await this.aenc.flush()}catch{}
  const V=this.v,us=x=>Math.round(x*1e6);if(!V.length)return null;let k=0;
  for(let i=0;i<V.length&&V[i].timestamp<=us(from);i++)if(V[i].type==='key')k=i;
  const t0=V[k].timestamp,vs=[];for(let i=k;i<V.length&&V[i].timestamp<=us(to);i++)vs.push(V[i]);
  const A=this.a.length&&this.acfg?this.acfg:null,as=A?this.a.filter(c=>c.timestamp>=t0&&c.timestamp<=us(to)):[],mp4=this.vc.mux==='mp4';
  const m=mp4?new Mp4Muxer.Muxer({target:new Mp4Muxer.ArrayBufferTarget(),video:{codec:'avc',width:1920,height:1080},audio:A&&as.length?{codec:A.name,sampleRate:A.sampleRate,numberOfChannels:A.numberOfChannels}:undefined,fastStart:'in-memory',firstTimestampBehavior:'cross-track-offset'})
   :new WebMMuxer.Muxer({target:new WebMMuxer.ArrayBufferTarget(),video:{codec:'V_VP9',width:1920,height:1080,frameRate:30},audio:A&&as.length?{codec:'A_OPUS',sampleRate:A.sampleRate,numberOfChannels:A.numberOfChannels}:undefined,firstTimestampBehavior:'offset'});
  let i=0,j=0,lv=-Infinity,la=-Infinity,fv=true,fa=true;
  while(i<vs.length||j<as.length){if(j>=as.length||(i<vs.length&&vs[i].timestamp<=as[j].timestamp)){const c=vs[i++];if(c.timestamp>lv){m.addVideoChunk(c,fv?this.vmeta:undefined);fv=false;lv=c.timestamp}}
   else{const c=as[j++];if(c.timestamp>la){m.addAudioChunk(c,fa?this.ameta:undefined);fa=false;la=c.timestamp}}}
  m.finalize();return {blob:new Blob([m.target.buffer],{type:this.mimeType}),start:Math.min(t0,as.length?as[0].timestamp:t0)/1e6}}
 pause(){if(this.state==='recording')this.state='paused'}
 resume(){if(this.state!=='paused')return;const m=recClock();if(Math.abs(m-this.marks[this.marks.length-1])>.3)this.marks.push(m);this.forceKey=true;this.aBase=null;this.state='recording';cutSnapNow(true)}
 async cutTo(sec){if(this.state!=='paused')return;const us=Math.round(sec*1e6);
  try{await this.venc.flush();if(this.aenc)await this.aenc.flush()}catch{}
  let i=this.v.findIndex(c=>c.timestamp>=us);if(i>=0)this.v.length=i;i=this.a.findIndex(c=>c.timestamp>=us);if(i>=0)this.a.length=i;
  this.pcm=this.pcm.filter(p=>p.t<sec);this.marks=this.marks.filter(m=>m<=sec+.01);this.thumbs=this.thumbs.filter(t=>t.t<sec);
  this.lastV=this.v.length?this.v[this.v.length-1].timestamp:-1;const la=this.a[this.a.length-1];this.aEnd=la?la.timestamp+(la.duration||0):0;
  this.lastKey=-1e9;this.forceKey=true;this.aBase=null}
 async stop(){if(this.state==='inactive')return;this.state='inactive';clearInterval(this.timer);clearInterval(this.thumbTimer);
  try{await this.venc.flush();if(this.aenc)await this.aenc.flush()}catch{}try{this.reader?.cancel()}catch{}
  await this.finishSave()}
 /* build the file; if that fails the take is NOT thrown away: it stays in memory with a "Try saving again" bar */
 async finishSave(){let blob;
  try{blob=this.mux()}catch(e){console.error('mux',e);this.saveFailed(e);return}
  document.getElementById('save-retry')?.remove();
  try{this.venc.close();this.aenc?.close()}catch{}this.v=[];this.a=[];this.pcm=[];this.thumbs=[];
  this.ondataavailable?.({data:blob});this.onstop?.()}
 saveFailed(e){const msg='Could not build the video file: '+(e&&(e.message||e.name)||e);
  const m=document.getElementById('record-message');if(m)m.textContent=msg+' — your recording is still kept. Close other tabs or apps, then press "Try saving again".';
  toast('Saving failed — the recording is kept. Use "Try saving again".');
  let bar=document.getElementById('save-retry');if(!bar){bar=document.createElement('div');bar.id='save-retry';
   bar.style.cssText='position:fixed;left:50%;top:16px;transform:translateX(-50%);z-index:10003;background:#fff;border:3px solid #b91c1c;border-radius:14px;padding:12px 18px;box-shadow:0 12px 40px #0004;font:600 15px system-ui;display:flex;gap:12px;align-items:center;max-width:92vw';
   (document.fullscreenElement||document.body).append(bar)}
  bar.innerHTML='<span>⚠ The take was not saved yet ('+String(msg).replace(/</g,'&lt;').slice(0,160)+'). It is still kept here.</span><button type="button" style="padding:8px 14px;border-radius:9px;border:0;background:#b91c1c;color:#fff;font-weight:800;cursor:pointer">Try saving again</button>';
  bar.querySelector('button').onclick=async()=>{bar.querySelector('button').textContent='Saving…';await new Promise(r=>setTimeout(r,50));this.finishSave()}}
 mux(){const A=this.a.length&&this.acfg?this.acfg:null,mp4=this.vc.mux==='mp4';
  // written in 16 MB pieces (no single giant memory block): sequential writes are appended, the few header patches
  // the muxer writes back at earlier positions are applied to the pieces at the end
  const parts=[],patches=[];let end=0;
  const onData=(d,pos)=>{const c=d.slice();if(pos===end){parts.push({pos,d:c});end+=c.length}else patches.push({pos,d:c})};
  const m=mp4
   ?new Mp4Muxer.Muxer({target:new Mp4Muxer.StreamTarget({onData,chunked:true,chunkSize:16*1024*1024}),video:{codec:'avc',width:1920,height:1080},audio:A?{codec:A.name,sampleRate:A.sampleRate,numberOfChannels:A.numberOfChannels}:undefined,fastStart:false,firstTimestampBehavior:'cross-track-offset'})
   :new WebMMuxer.Muxer({target:new WebMMuxer.StreamTarget({onData,chunked:true,chunkSize:16*1024*1024}),video:{codec:'V_VP9',width:1920,height:1080,frameRate:30},audio:A?{codec:'A_OPUS',sampleRate:A.sampleRate,numberOfChannels:A.numberOfChannels}:undefined,firstTimestampBehavior:'offset'});
  let i=0,j=0;const V=this.v,Au=A?this.a:[];
  // a continued take can overlap by a few ms where the old part ends: skip any chunk that would go back in time
  let lv=-Infinity,la=-Infinity,fv=true,fa=true;
  while(i<V.length||j<Au.length){if(j>=Au.length||(i<V.length&&V[i].timestamp<=Au[j].timestamp)){const c=V[i++];if(c.timestamp>lv){m.addVideoChunk(c,fv?this.vmeta:undefined);fv=false;lv=c.timestamp}}else{const c=Au[j++];if(c.timestamp>la){m.addAudioChunk(c,fa?this.ameta:undefined);fa=false;la=c.timestamp}}}
  m.finalize();
  for(const p of patches){let k=0;while(k<p.d.length){const at=p.pos+k,part=parts.find(x=>at>=x.pos&&at<x.pos+x.d.length);
    if(!part){const tail=p.d.subarray(k);if(at===end){parts.push({pos:at,d:tail});end+=tail.length}break}
    const off=at-part.pos,n=Math.min(part.d.length-off,p.d.length-k);part.d.set(p.d.subarray(k,k+n),off);k+=n}}
  return new Blob(parts.map(x=>x.d),{type:this.mimeType})}
}
async function makeRecorder(stream,canvas,mime){
 if(CUT.ok){let vc=null;try{vc=await cutVideoCodec()}catch(e){console.warn('cut recorder unavailable',e)}
  if(vc){const r=new CutRecorder(canvas,stream.getAudioTracks()[0]||null,vc);if(CUT.cont)await r.seed(CUT.cont.blob,CUT.cont.cut,CUT.cont.onp);return r}}
 if(CUT.cont)throw Error('Continuing a take needs a current desktop Chrome or Edge.');
 return new MediaRecorder(stream,mime?{mimeType:mime,videoBitsPerSecond:8000000,audioBitsPerSecond:160000}:undefined)}

/* slide / step / pen ink over time, so a cut can put the studio back where it was at that moment */
function cutInkKey(){const v=video();return (v?.beats[state.beat]?.layout==='hybrid'?'hy-':'')+v?.id+':'+state.beat}
function cutSnapNow(force){const r=record;if(!r||!r.rec.cutTo||r.rec.state!=='recording')return;const k=cutInkKey(),ink=JSON.stringify(state.ink?.[k]||[]),sig=state.beat+'|'+state.step+'|'+k+'|'+ink;
 if(sig===r.cutSig&&!force)return;r.cutSig=sig;(r.snaps=r.snaps||[]).push({t:recClock(),beat:state.beat,step:state.step,k,ink})}
setInterval(()=>cutSnapNow(false),200);
function cutSnapAt(t){let at=null;for(const s of record?.snaps||[])if(s.t<=t)at=s;return at}
function cutRestore(C){const r=record,S=r.snaps||[],at=cutSnapAt(C);
 for(const k of new Set(S.filter(s=>s.t>C).map(s=>s.k))){let last=null;for(const s of S)if(s.t<=C&&s.k===k)last=s;
  const ink=last?JSON.parse(last.ink):JSON.parse(r.ink0?.[k]||'[]');if(ink.length)state.ink[k]=ink;else delete state.ink[k]}
 r.snaps=S.filter(s=>s.t<=C);r.cutSig=null;if(at){state.beat=at.beat;state.step=at.step}updateSlide();save();
 r.chapters=(r.chapters||[]).filter(c=>c.start<C);r.lastBeat=null}
function cutPlay(from,to){const rc=record?.rec;if(!rc?.pcm)return;from=Math.max(0,from);const parts=rc.pcm.filter(p=>p.t+p.d.length/p.sr>from&&p.t<to);
 if(!parts.length||to-from<.05)return toast('Nothing to hear there.');const sr=parts[0].sr,n=Math.round((to-from)*sr),out=new Float32Array(n);
 for(const p of parts){const off=Math.round((p.t-from)*sr);for(let k=0;k<p.d.length;k++){const q=off+k;if(q>=0&&q<n)out[q]=p.d[k]/32767}}
 const ac=CUT.ac||(CUT.ac=new AudioContext());ac.resume();try{CUT.src?.stop()}catch{}const b=ac.createBuffer(1,n,sr);b.copyToChannel(out,0);const s=ac.createBufferSource();s.buffer=b;s.connect(ac.destination);s.start();CUT.src=s}

/* ---- the Cut back panel (opens while paused: toolbar ✂ button or X) ---- */
function openCutPanel(){const r=record;if(!r)return;if(!r.rec.cutTo)return toast('Cut back needs a current desktop Chrome or Edge. You can still pause, or stop and discard the take.');
 if(r.rec.state==='recording'){pauseRecording();syncRec()}if(document.getElementById('cut-panel'))return;
 const T=recClock(),fmt=s=>{s=Math.max(0,s);const m=Math.floor(s/60),x=s-60*m;return m+':'+(x<10?'0':'')+x.toFixed(2)},dur=d=>d<60?d.toFixed(2)+' s':fmt(d);
 if(T<.5)return toast('Nothing recorded yet to cut.');
 const box=document.createElement('div');box.id='cut-panel';box.setAttribute('role','dialog');box.setAttribute('aria-label','Cut back');
 box.style.cssText='position:fixed;left:50%;top:70px;transform:translateX(-50%);z-index:10000;width:min(900px,96vw);max-height:94vh;overflow:auto;background:#fff;color:#17233c;border:3px solid #b91c1c;border-radius:16px;box-shadow:0 20px 60px #0005;padding:16px 20px;font-family:inherit';
 const mk=r.rec.marks.filter(m=>m<T-.3).slice(-2).reverse(),rd=mk.map((m,i)=>'<button type="button" data-redo="'+i+'" style="padding:'+(i?'7px 12px':'10px 16px')+';border-radius:10px;border:'+(i?'1px solid #e5c4c4;background:#fff;color:#17233c':'0;background:#17233c;color:#fff')+';font-weight:800;cursor:pointer">↺ Redo from '+fmt(m)+(i?'':' (R)')+' <span style="font-weight:500;opacity:.8">'+(m===0?'· start over':i?'· the time before':'· where you last continued')+' · removes '+dur(T-m)+'</span></button>').join('');
 const q=[3,5,10,20,30,60].filter(x=>x<T+1).map(x=>'<button type="button" data-cut="'+x+'" style="padding:7px 12px;border-radius:9px;border:1px solid #e5c4c4;background:#fff;font-weight:700;cursor:pointer">− '+(x<60?x+' s':'1 min')+'</button>').join('');
 box.innerHTML='<div style="display:flex;justify-content:space-between;align-items:baseline;gap:10px"><div style="font-size:20px;font-weight:800">✂ Cut back</div><div style="color:#5b6b7a;font-size:13px">take length now '+fmt(T)+'</div></div>'
  +'<div style="color:#5b6b7a;font-size:14px;margin:4px 0 10px">Remove the end of the take, then continue recording from that moment. R = redo from where you last continued · ← → move 0.1 s · Shift ← → 1 s · Option ← → 0.02 s · Enter = cut · Esc = cancel</div>'
  +(rd?'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">'+rd+'</div>':'')+'<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px">'+q+'</div>'
  +'<input id="cut-range" type="range" min="0" max="'+T.toFixed(1)+'" step="0.01" style="width:100%;accent-color:#b91c1c">'
  +'<div style="display:flex;gap:16px;align-items:flex-start;margin-top:10px"><div style="flex:none;width:min(440px,50vw)"><video id="cut-vid" controls playsinline style="width:100%;aspect-ratio:16/9;border-radius:8px;background:#0b1f1d"></video><div id="cut-vid-note" style="color:#5b6b7a;font-size:12px;margin-top:2px">Loading the video around this point…</div></div>'
  +'<div style="flex:1;min-width:0"><div id="cut-info" style="font-size:15px;line-height:1.5"></div>'
  +'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px"><button type="button" id="cut-hear-keep" style="padding:7px 12px;border-radius:9px;border:1px solid #cfe0dd;background:#f3faf8;cursor:pointer">▶ Watch the last part kept</button>'
  +'<button type="button" id="cut-hear-drop" style="padding:7px 12px;border-radius:9px;border:1px solid #efd3d3;background:#fdf4f4;cursor:pointer">▶ Watch the part being removed</button></div></div></div>'
  +'<div style="display:flex;gap:10px;justify-content:flex-end;margin-top:14px"><button type="button" id="cut-cancel" style="padding:10px 18px;border-radius:10px;border:1px solid #d8e0e6;background:#fff;font-weight:700;cursor:pointer">Cancel</button>'
  +'<button type="button" id="cut-go" style="padding:10px 22px;border-radius:10px;border:0;background:#b91c1c;color:#fff;font-weight:800;font-size:15px;cursor:pointer">✂ Cut</button></div>';
 (document.fullscreenElement||document.body).append(box);
 const rg=box.querySelector('#cut-range'),v=video();let busy=false;
 const show=()=>{const p=+rg.value,s=cutSnapAt(p),b=s&&v?.beats[s.beat],th=[...r.rec.thumbs].reverse().find(x=>x.t<=p+.5)||r.rec.thumbs[0];
  const vv=box.querySelector('#cut-vid');if(th&&!vv.src)vv.poster=th.url;refreshClip();
  box.querySelector('#cut-info').innerHTML='Keep <b>0:00 – '+fmt(p)+'</b> · remove the last <b style="color:#b91c1c">'+dur(T-p)+'</b>'
   +(b?'<br>You continue from <b>slide '+(s.beat+1)+'</b>'+(s.step?' · step '+(s.step+1):'')+' · '+esc(b.title||''):'')};
 let clip=null,clipUrl=null,clipTimer=0,clipStop=null;
 const vid=()=>box.querySelector('#cut-vid'),note=t=>{const n=box.querySelector('#cut-vid-note');if(n)n.textContent=t};
 // rebuild the short clip (4 s before → 6 s after the point) a moment after the point stops moving
 function refreshClip(){clearTimeout(clipTimer);clipTimer=setTimeout(async()=>{const p=+rg.value;
   if(clip&&p-4>=clip.from-0.01&&Math.min(T,p+6)<=clip.to+0.01){seekTo(p);return}
   if(!r.rec.clip){note('');return}
   try{const c=await r.rec.clip(Math.max(0,p-4),Math.min(T,p+6));if(!c)return;if(clipUrl)URL.revokeObjectURL(clipUrl);
    clip={...c,from:Math.max(0,p-4),to:Math.min(T,p+6)};clipUrl=URL.createObjectURL(c.blob);const v2=vid();v2.src=clipUrl;
    v2.onloadedmetadata=()=>seekTo(+rg.value)}catch(e){console.warn('cut preview',e);note('Preview not available — use the sound buttons.')}},250)}
 function seekTo(p){const v2=vid();if(!clip||!v2.src)return;v2.pause();v2.currentTime=Math.max(0,p-clip.start);
  note('Showing the moment you keep up to ('+fmt(p)+'). Press play to watch around it.')}
 function playRange(a,b){const v2=vid();if(!clip||!v2.src)return false;clearInterval(clipStop);v2.currentTime=Math.max(0,a-clip.start);v2.play();
  clipStop=setInterval(()=>{if(v2.currentTime>=b-clip.start||v2.paused){v2.pause();clearInterval(clipStop)}},40);return true}
 const set=x=>{rg.value=Math.max(0,Math.min(T,x)).toFixed(2);show()};set(T-Math.min(5,T));
 let exact=null;box.querySelectorAll('[data-cut]').forEach(b=>b.onclick=()=>{exact=null;set(T-+b.dataset.cut)});rg.oninput=()=>{exact=null;show()};
 const redo=i=>{if(mk[i]==null)return;set(mk[i]);exact=mk[i];go()};box.querySelectorAll('[data-redo]').forEach(b=>b.onclick=()=>redo(+b.dataset.redo));
 box.querySelector('#cut-hear-keep').onclick=()=>{const p=+rg.value;if(!playRange(Math.max(0,p-3),p))cutPlay(p-4,p)};
 box.querySelector('#cut-hear-drop').onclick=()=>{const p=+rg.value;if(!playRange(p,Math.min(T,p+6)))cutPlay(p,Math.min(T,p+8))};
 const close=()=>{document.removeEventListener('keydown',key,true);try{CUT.src?.stop()}catch{}clearTimeout(clipTimer);clearInterval(clipStop);try{vid().pause()}catch{}if(clipUrl)URL.revokeObjectURL(clipUrl);box.remove()};
 const go=async()=>{if(busy)return;busy=true;const C=exact??+rg.value;if(C>=T-.05)return close();box.querySelector('#cut-go').textContent='Cutting…';
  await r.rec.cutTo(C);r.pausedMs+=(T-C)*1000;r.rec.cutCount++;r.rec.cutSec+=T-C;cutRestore(C);close();syncRec();
  const ck=$('#rec-clock');if(ck)ck.textContent=timeText(C);
  toast('Cut '+dur(T-C)+'. The take is now '+fmt(C)+'. Press Continue (P) when you are ready.')};
 const key=e=>{if(e.key==='Escape'){e.preventDefault();e.stopPropagation();close()}else if(e.key==='Enter'){e.preventDefault();e.stopPropagation();go()}
  else if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();e.stopPropagation();exact=null;const d=e.altKey?.02:e.shiftKey?1:.1;set(+rg.value+(e.key==='ArrowLeft'?-d:d))}else if((e.key==='r'||e.key==='R')&&mk.length){e.preventDefault();e.stopPropagation();redo(0)}else if(e.key==='p'||e.key==='P'||e.key===' ')e.stopPropagation()};
 document.addEventListener('keydown',key,true);box.querySelector('#cut-cancel').onclick=close;box.querySelector('#cut-go').onclick=go}
window.addEventListener('keydown',e=>{if(!record||e.metaKey||e.ctrlKey||e.altKey)return;if(['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)||e.target.isContentEditable)return;
 if(e.key==='x'||e.key==='X'){e.preventDefault();openCutPanel()}});
"""

REPL = [
    # the recorder: cut-able WebCodecs recorder when the browser has it, otherwise MediaRecorder as before
    ("const rec=new MediaRecorder(stream,mime?{mimeType:mime,videoBitsPerSecond:8000000,audioBitsPerSecond:160000}:undefined);",
     "const rec=await makeRecorder(stream,canvas,mime);"),
    # remember the pen ink at the start of the take (a cut back to before a drawing removes that drawing again)
    ("record={rec,input,stream,v,started,pausedAt:0,pausedMs:0,frame:0,ctx,canvas,useCamera};",
     "record={rec,input,stream,v,started,pausedAt:0,pausedMs:0,frame:0,ctx,canvas,useCamera,"
     "ink0:Object.fromEntries(Object.entries(state.ink||{}).map(([k,x])=>[k,JSON.stringify(x)]))};"),
    # toolbar: ✂ Cut back button next to Continue while paused
    ("p.style.cssText=paused?'background:#0f766e;color:#fff;border-color:#0f766e;font-weight:700':''}}",
     "p.style.cssText=paused?'background:#0f766e;color:#fff;border-color:#0f766e;font-weight:700':'';"
     "let x=$('#qcut');if(!x){x=document.createElement('button');x.id='qcut';x.type='button';x.textContent='✂ Cut back';"
     "x.title='Remove the end of the take and continue from there (X)';x.style.cssText='background:#fff;color:#b91c1c;border-color:#e5c4c4;font-weight:700';"
     "x.onclick=openCutPanel;p.after(x)}x.hidden=!(paused&&record.rec.cutTo)}}"),
]


def apply(s):
    for old, new in REPL:
        assert s.count(old) == 1, 'studio_cut anchor not found: ' + old[:70]
        s = s.replace(old, new)
    k = s.find('async function startRecording(){')
    assert k > 0
    return s[:k] + _lib('mp4-muxer.min.js') + _lib('webm-muxer.min.js') + JS.lstrip() + s[k:]
