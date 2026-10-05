"""Continue a saved take (applied by build_verbal.py after studio_edit).

Toolbar "⤴ Continue a take": pick a take file -> choose where to continue from (the end, or an earlier moment:
everything after it is dropped) -> the studio opens that lesson on the slide of that moment, loads the take into the
recorder (its picture and sound are re-encoded as the start of the new take) and waits PAUSED. Check the slide and the
pen ink (paused time is never recorded), press P, and keep recording. Stop -> Keep saves ONE continuous take as a new
file (newer time stamp, so the upload uses it); the original file is left untouched. Cut back (X / R) works as usual.
"""

JS = r"""
/* ---- continue a saved take ---- */
function pickContinuePoint(blob,chapters,label){return new Promise(async done=>{
 const url=URL.createObjectURL(blob),box=document.createElement('div');box.id='take-continue';
 box.innerHTML=`<style>
#take-continue{position:fixed;inset:0;z-index:10001;background:#0b1f1d;color:#eef3fb;display:flex;flex-direction:column;gap:10px;padding:12px 18px;font-family:inherit;font-size:14px}
#take-continue button{padding:8px 14px;border-radius:9px;border:1px solid #2c5a55;background:#123331;color:#eef3fb;font-weight:600;cursor:pointer;font-size:14px}
#take-continue .row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}#take-continue .sp{flex:1}
#take-continue video{flex:1;min-height:0;max-width:100%;background:#000;border-radius:8px;align-self:center}
#tc-range{width:100%;accent-color:#2dd4bf}</style>
<div class="row"><b style="font-size:18px">⤴ Continue a take</b><span style="color:#9fb7b2">${esc(label||'')}</span><span class="sp"></span>
<button id="tc-cancel">Cancel</button><button id="tc-go" style="background:#0f766e;border-color:#0f766e;color:#fff;font-weight:800">⤴ Continue from here</button></div>
<video id="tc-video" controls playsinline></video>
<input id="tc-range" type="range" min="0" step="0.1">
<div class="row"><span id="tc-info" style="font-size:16px"></span><span class="sp"></span><button id="tc-here">Use the video's position</button><button id="tc-end">The end</button></div>
<div style="color:#9fb7b2;font-size:12px">Play the take and stop where you want to go on from (or drag the bar). Everything after that point is left out of the new take; the original file is kept as it is. ← → = 1 s · Enter = continue · Esc = cancel</div>`;
 document.body.append(box);
 const $c=id=>box.querySelector('#'+id),vid=$c('tc-video'),rg=$c('tc-range');vid.src=url;
 let D=0;try{D=await new Mediabunny.Input({source:new Mediabunny.BlobSource(blob),formats:Mediabunny.ALL_FORMATS}).computeDuration()}catch(e){console.warn(e)}
 if(!(D>0)){await new Promise(r=>{if(vid.readyState>=1)r();else vid.onloadedmetadata=r});D=isFinite(vid.duration)?vid.duration:0}
 if(!(D>0)){box.remove();URL.revokeObjectURL(url);toast('Could not read this take.');return done(null)}
 rg.max=D.toFixed(1);
 const slideAt=t=>{let c=null;for(const x of chapters||[])if(x.start<=t+.05)c=x;return c?.title||''};
 const show=()=>{const p=+rg.value,end=p>=D-.15;$c('tc-info').innerHTML='Continue from <b>'+teFmt(p)+'</b>'+(end?' — the end of the take':' — leaves out the last <b style="color:#fca5a5">'+teDur(D-p)+'</b>')
  +(slideAt(p)?' · slide: <b>'+esc(slideAt(p))+'</b>':'')};
 const set=t=>{rg.value=Math.max(0,Math.min(D,t)).toFixed(1);show()};
 rg.oninput=()=>{show();vid.currentTime=Math.min(+rg.value,D-.05)};
 $c('tc-here').onclick=()=>set(vid.currentTime);$c('tc-end').onclick=()=>set(D);set(D);
 const close=v=>{document.removeEventListener('keydown',key,true);vid.pause();vid.removeAttribute('src');vid.load();URL.revokeObjectURL(url);box.remove();done(v)};
 $c('tc-cancel').onclick=()=>close(null);$c('tc-go').onclick=()=>close(Math.min(+rg.value,D));
 const key=e=>{e.stopPropagation();if(e.key==='Escape'){e.preventDefault();close(null)}else if(e.key==='Enter'){e.preventDefault();close(Math.min(+rg.value,D))}
  else if((e.key==='ArrowLeft'||e.key==='ArrowRight')&&e.target!==vid){e.preventDefault();set(+rg.value+(e.key==='ArrowLeft'?-1:1));vid.currentTime=Math.min(+rg.value,D-.05)}};
 document.addEventListener('keydown',key,true)})}
async function continueTake(){if(record)return toast('Stop the recording first.');
 if(!CUT.ok||!window.Mediabunny||!window.showOpenFilePicker)return toast('Continuing a take needs a current desktop Chrome or Edge.');
 if(!RF.handle)RF.handle=await rfGet();let fh;
 try{[fh]=await window.showOpenFilePicker({id:'studio-edit-take',...(RF.handle?{startIn:RF.handle}:{}),types:[{description:'Recorded takes',accept:{'video/mp4':['.mp4'],'video/webm':['.webm']}}]})}catch{return}
 const file=await fh.getFile(),m=file.name.match(/^(.+)-\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z\.(mp4|webm)$/),v=m&&D.videos[m[1]];
 if(!v)return toast('This file name does not match a lesson in the course, so the studio cannot tell which video to continue.');
 const fi=D.flow.findIndex(r=>r.type==='video'&&r.ref===v.id);if(fi<0)return toast('This video is no longer in the course.');
 let chapters=[];try{const d=await rfTopicDir(v,false),cf=await d.getFileHandle(file.name.replace(/\.(mp4|webm)$/,'.chapters.json'));chapters=JSON.parse(await (await cf.getFile()).text()).chapters||[]}catch{}
 const cut=await pickContinuePoint(file,chapters,file.name);if(cut==null)return;
 return continueFrom(file,v,chapters,cut)}
async function continueFrom(file,v,chapters,cut){const fi=D.flow.findIndex(r=>r.type==='video'&&r.ref===v.id);
 go(fi);await new Promise(r=>setTimeout(r,300));
 // the slide of that moment: follow the chapter titles through the slides in order
 const kept=chapters.filter(c=>c.start<=cut+.05).map(c=>({start:c.start,title:c.title}));let bi=0,from=0;
 for(const c of kept){const k=v.beats.findIndex((b,i)=>i>=from&&(b.bigTitle||b.title)===c.title);if(k>=0){bi=k;from=k}}
 state.beat=bi;state.step=0;updateSlide();
 const ov=document.createElement('div');ov.style.cssText='position:fixed;inset:0;z-index:10002;background:#0b1f1dd9;color:#fff;display:grid;place-items:center;font:700 18px system-ui';
 ov.innerHTML='<div style="text-align:center"><div id="tc-p">Loading the take…</div><div style="width:min(520px,80vw);height:10px;border-radius:5px;background:#123331;margin-top:12px;overflow:hidden"><i id="tc-bar" style="display:block;height:100%;width:0;background:#2dd4bf"></i></div></div>';
 document.body.append(ov);const t0=Date.now();
 CUT.cont={blob:file,cut,onp:p=>{ov.querySelector('#tc-bar').style.width=(p*100).toFixed(1)+'%';const el=(Date.now()-t0)/1000,left=p>.03?el/p-el:0;
  ov.querySelector('#tc-p').textContent='Loading the take… '+Math.round(p*100)+'%'+(left>3?' · about '+(left<60?Math.round(left)+' s':Math.round(left/60)+' min')+' left':'')}};
 try{await startRecording()}finally{CUT.cont=null;ov.remove()}
 if(!record||!record.rec.seed)return;
 const now=Date.now();record.started=now-cut*1000;record.pausedAt=now;record.pausedMs=0;record.chapters=kept;record.lastBeat=null;
 const pb=$('#pause-record');if(pb)pb.textContent='Resume';const ck=$('#rec-clock');if(ck)ck.textContent=timeText(cut);syncRec();
 toast('Ready at '+teFmt(cut)+'. Check the slide, the step and the pen ink (paused time is not recorded), then press P to go on.')}
document.addEventListener('click',e=>{if(e.target.closest?.('#qcont'))continueTake()});
"""

REPL = [
    # after Stop: "Keep recording" in the Keep / Discard bar = load the take just stopped back in and continue (nothing saved)
    ("✎ Edit</button></div></div>';",
     "✎ Edit</button><button id=\"take-cont\" title=\"Stopped by mistake? Go on recording this take (nothing is saved yet)\" "
     "style=\"padding:11px 20px;border-radius:10px;border:1px solid #d8e6e3;background:#fff;color:#17233c;font-weight:700;font-size:15px;cursor:pointer\">"
     "⤴ Keep recording</button></div></div>';"),
    ("res(keep&&edited?edited:keep)};", "res(keep===true&&edited?edited:keep)};"),
    ("box.querySelector('#take-discard').onclick=()=>done(false);",
     "box.querySelector('#take-discard').onclick=()=>done(false);"
     "box.querySelector('#take-cont').onclick=()=>done({continue:true,blob:edited?edited.blob:null,chapters:edited?edited.chapters:null});"),
    ("Enter = keep · Esc = discard", "Enter = keep · Esc = discard · Stopped by mistake? Keep recording"),
    ("const kk=await askKeepTake(blob,r.chapters);",
     "const kk=await askKeepTake(blob,r.chapters);"
     "if(kk&&kk.continue){if(kk.blob){blob=kk.blob;r.chapters=kk.chapters}"
     "if(!CUT.ok||!window.Mediabunny){toast('Continuing needs a current desktop Chrome or Edge. Keep the take and use Continue a take later.');return}"
     "$('#record-message').textContent='Loading the take back in to continue… (nothing was saved)';"
     "const f=new File([blob],name,{type:blob.type||'video/mp4'});let dur=0;"
     "try{dur=await new Mediabunny.Input({source:new Mediabunny.BlobSource(f),formats:Mediabunny.ALL_FORMATS}).computeDuration()}catch(e){console.warn(e)}"
     "if(!(dur>0)){toast('Could not read the take back. Keep it and use Continue a take.');return}"
     "await continueFrom(f,v,(r.chapters||[]).map(c=>({start:c.start,title:c.title})),dur);return}"),
    ('<button id="qedit" title="Edit a saved take: cut pieces out, speed parts up">✎ Edit a take</button>',
     '<button id="qedit" title="Edit a saved take: cut pieces out, speed parts up">✎ Edit a take</button>'
     '<button id="qcont" title="Continue recording a saved take, from its end or from an earlier moment">⤴ Continue a take</button>'),
]


def apply(s):
    for old, new in REPL:
        assert s.count(old) == 1, ('studio_continue anchor', s.count(old), old[:70])
        s = s.replace(old, new)
    k = s.find('async function startRecording(){')
    assert k > 0
    return s[:k] + JS.lstrip() + s[k:]
