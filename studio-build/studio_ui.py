"""Studio behaviour tweaks applied to the built studio HTML (text replacement, like slide_style.py).

- After Stop, the studio asks whether to keep the take (with a preview) before saving it. Discarded takes are never
  written, so the recordings folder only holds takes the teacher chose to keep.
"""

SAVE_OLD = ("if(!blob.size){toast('The recording was empty. No take was saved.');return}"
            "const where=await saveTakeFile(v,name,blob);")
SAVE_NEW = ("if(!blob.size){toast('The recording was empty. No take was saved.');return}"
            "$('#record-message').textContent='Recording stopped. Keep this take?';"
            "if(!(await askKeepTake(blob))){$('#record-message').textContent='Take discarded (not saved).';toast('Take discarded');return}"
            "$('#record-message').textContent='Saving this take…';"
            "const where=await saveTakeFile(v,name,blob);")

ASK_FN = r"""
/* ---- keep or discard a take: a bar docked at the bottom of the screen, with the take's player (asked after Stop,
   before anything is saved) ---- */
function askKeepTake(blob){return new Promise(res=>{const url=URL.createObjectURL(blob),box=document.createElement('div');
 box.id='keep-take';box.setAttribute('role','dialog');box.setAttribute('aria-label','Keep this take?');
 box.style.cssText='position:fixed;left:0;right:0;bottom:0;z-index:9999;background:#fff;border-top:3px solid #0f766e;box-shadow:0 -10px 40px #0003;padding:14px 20px;display:flex;gap:20px;align-items:center;font-family:inherit';
 box.innerHTML='<video src="'+url+'" controls style="width:min(760px,58vw);max-height:46vh;border-radius:10px;background:#000;flex:none"></video>'
  +'<div style="flex:1;min-width:200px"><div style="font-size:20px;font-weight:700;margin-bottom:6px">Keep this take?</div>'
  +'<div style="color:#5b6b7a;font-size:14px;margin-bottom:14px">Watch it here first. Only kept takes are saved to your recordings folder.<br>Enter = keep · Esc = discard</div>'
  +'<div style="display:flex;gap:10px">'
  +'<button id="take-keep" style="padding:11px 26px;border-radius:10px;border:0;background:#0f766e;color:#fff;font-weight:700;font-size:15px;cursor:pointer">Keep</button>'
  +'<button id="take-discard" style="padding:11px 20px;border-radius:10px;border:1px solid #d8e6e3;background:#fff;color:#b91c1c;font-weight:700;font-size:15px;cursor:pointer">Discard</button></div></div>';
 document.body.append(box);const pad=document.body.style.paddingBottom;document.body.style.paddingBottom=(box.offsetHeight+10)+'px';
 box.scrollIntoView?.({block:'end'});
 const done=keep=>{document.removeEventListener('keydown',key,true);box.remove();document.body.style.paddingBottom=pad;URL.revokeObjectURL(url);res(keep)};
 const key=e=>{if(e.target&&e.target.tagName==='VIDEO')return;if(e.key==='Enter'){e.preventDefault();e.stopPropagation();done(true)}else if(e.key==='Escape'){e.preventDefault();e.stopPropagation();done(false)}};
 document.addEventListener('keydown',key,true);
 box.querySelector('#take-keep').onclick=()=>done(true);box.querySelector('#take-discard').onclick=()=>done(false)})}
"""


# ---- script position: left (as before) or top (a teleprompter strip right under the Mac's camera) ----
SB_CSS = """<style>
/* script at the top: its own strip ABOVE the slide (the slide starts under it), full text, scrolls if long */
.board-shell > .sb-prompter.sb-top{display:block;position:relative;left:auto;top:auto;bottom:auto;transform:none;width:auto;height:auto;
 max-height:32vh;margin:0 auto 8px;border-radius:12px;box-shadow:none;background:#0b1f1d;color:#eef3fb;padding:4px 22px 10px;overflow:auto;text-align:center}
.board-shell > .sb-prompter.sb-top .sb-head{position:static;background:none;border:0;justify-content:center;gap:10px;padding:2px 0 4px;margin:0;opacity:.8}
.board-shell > .sb-prompter.sb-top .hy-step.past,.board-shell > .sb-prompter.sb-top .hy-step.ahead:not(.next-up){display:none}
.board-shell > .sb-prompter.sb-top .hy-step{border-left:0;padding:2px 0;margin:0}
.board-shell > .sb-prompter.sb-top .hy-step.live{font-size:1.4em;line-height:1.35;color:#fff;background:none}
.board-shell > .sb-prompter.sb-top .hy-step.next-up{font-size:.95em;opacity:.55;margin-top:6px}
.board-shell > .sb-prompter.sb-top .hy-n{display:none}
.board-shell > .sb-prompter.sb-top .hy-say{justify-content:center}
/* full screen (draw mode): strip in the first row, the slide shrinks so strip + slide fit the screen */
body.draw-mode .board-shell.sbtop{grid-template-rows:auto auto minmax(0,1fr) auto}
body.draw-mode .board-shell.sbtop > .sb-prompter.sb-top{grid-column:1/-1;grid-row:1;max-height:30vh;width:min(100vw,1400px);margin:6px auto;border-radius:12px}
body.draw-mode .board-shell.sbtop > .board-wrap{grid-row:2;width:min(100vw,calc((100vh - 120px - var(--sbh,0px)) * 16 / 9))}
@supports (height:100dvh){body.draw-mode .board-shell.sbtop > .board-wrap{width:min(100vw,calc((100dvh - 120px - var(--sbh,0px)) * 16 / 9))}}
body.draw-mode.hy-active .board-shell.sbtop{grid-template-rows:auto auto 0 auto}
</style>"""

SYNC_OLD = "$('#board')?.classList.toggle('sb-on',STUDIO&&hy&&sbOn);"
SYNC_NEW = ("$('#board')?.classList.toggle('sb-on',STUDIO&&hy&&sbOn);"
            # move the script out of the slide (above it) when it is at the top, back onto the slide when on the left
            "{const sbp=$('#sb-prompter'),bw=$('#board'),shell=bw?.parentElement;if(sbp&&bw&&shell){const top=sbTop&&STUDIO&&hy&&sbOn;"
            "sbp.classList.toggle('sb-top',top);shell.classList.toggle('sbtop',top);"
            "if(top&&sbp.parentElement!==shell)shell.insertBefore(sbp,bw);if(!top&&sbp.parentElement!==bw)bw.insertBefore(sbp,bw.querySelector('.cam-bubble'));"
            "if(!top)sbp.style.display='';else sbp.style.display='block';"
            "requestAnimationFrame(()=>{shell.style.setProperty('--sbh',top?(sbp.offsetHeight+12)+'px':'0px');const lv=sbp.querySelector('.hy-step.live');if(top&&lv)lv.scrollIntoView({block:'nearest'})})}}"
            "{const t=$('#sb-toggle');if(t&&!$('#sb-pos')){const bt=document.createElement('button');bt.id='sb-pos';bt.className=t.className;"
            "bt.title='Where the script sits: on the left of the slide, or above the slide under the camera (so you look at the lens)';"
            "t.after(bt);bt.onclick=()=>{sbTop=!sbTop;try{localStorage.setItem('hy-sb-pos',sbTop?'top':'left')}catch{}hySyncDraw()}}"
            "const bp=$('#sb-pos');if(bp){bp.textContent=sbTop?'⬆ Script: top (camera)':'⬅ Script: left';bp.classList.toggle('active',sbTop)}}")
SBON_OLD = "let sbOn=(()=>{try{return localStorage.getItem('hy-sb')!=='off'}catch{return true}})();"
SBON_NEW = SBON_OLD + "let sbTop=(()=>{try{return localStorage.getItem('hy-sb-pos')!=='left'}catch{return true}})();"


# ---- microphone: asked for ONCE when the studio opens and kept for every take (asking at each take showed the
#      browser's permission pop-up, which throws the page out of full screen) ----
MIC_FN = r"""
let micStream=null;
async function getMic(){if(micStream&&micStream.getAudioTracks().some(t=>t.readyState==='live'))return micStream;
 micStream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:false,noiseSuppression:true,autoGainControl:false,channelCount:1,sampleRate:48000},video:false});return micStream}
setTimeout(()=>{try{if(typeof STUDIO!=='undefined'&&STUDIO&&navigator.mediaDevices?.getUserMedia){
 if(document.getElementById('use-mic')?.checked!==false)getMic().then(()=>{if(document.getElementById('use-camera')?.checked&&!camStream)camOn()}).catch(()=>{});
 else if(document.getElementById('use-camera')?.checked&&!camStream)camOn()}}catch(e){}},1200);
"""
MIC_REPL = [
    ("if(useMic)input=await navigator.mediaDevices.getUserMedia({audio:useMic?{echoCancellation:false,noiseSuppression:true,autoGainControl:false,channelCount:1,sampleRate:48000}:false,video:false});",
     "if(useMic)input=await getMic();"),
    # the recording gets COPIES of the mic tracks, so stopping a take never closes the shared microphone
    ("if(useMic)input.getAudioTracks().forEach(t=>stream.addTrack(t));", "if(useMic)input.getAudioTracks().forEach(t=>stream.addTrack(t.clone()));"),
    ("r.input?.getTracks().forEach(t=>t.stop());", ""),
    ("}catch(e){input?.getTracks().forEach(t=>t.stop());", "}catch(e){"),
    ("async function startRecording(){", MIC_FN + "async function startRecording(){"),
]


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:60])
    return s.replace(old, new)


def apply(s):
    s = rep(s, SAVE_OLD, SAVE_NEW)
    s = rep(s, "function stopRecording(){", ASK_FN + "function stopRecording(){")
    for o, n in MIC_REPL: s = rep(s, o, n)
    s = rep(s, SBON_OLD, SBON_NEW)
    s = rep(s, SYNC_OLD, SYNC_NEW)
    s = s.replace("</head>", SB_CSS + "</head>", 1)   # the first </head> is the page head (a later one is inside a string)
    return s
