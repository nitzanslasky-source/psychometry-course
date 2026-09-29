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
.board-shell > .sb-prompter.sb-top .hy-n{display:none}
.board-shell > .sb-prompter.sb-top .hy-say{justify-content:center}
/* full screen (draw mode): strip in the first row, the slide shrinks so strip + slide fit the screen */
body.draw-mode .board-shell.sbtop{grid-template-rows:auto auto minmax(0,1fr) auto}
body.draw-mode .board-shell.sbtop > .sb-prompter.sb-top{grid-column:1/-1;grid-row:1;max-height:36vh;width:min(100vw,1400px);margin:6px auto;border-radius:12px}
body.draw-mode .board-shell.sbtop > .board-wrap{grid-row:2;width:min(100vw,calc((100vh - 150px - var(--sbh,0px)) * 16 / 9))}
@supports (height:100dvh){body.draw-mode .board-shell.sbtop > .board-wrap{width:min(100vw,calc((100dvh - 150px - var(--sbh,0px)) * 16 / 9))}}
body.draw-mode.hy-active .board-shell.sbtop{grid-template-rows:auto auto 0 auto}
/* resizable strip: drag the bottom edge (height remembered), double-click the edge = automatic size */
.board-shell.sbsized > .sb-prompter.sb-top{height:var(--sbmax)!important;max-height:var(--sbmax)!important}
.board-shell > .sb-prompter.sb-top{position:relative;padding-bottom:18px;display:flex!important;flex-direction:column}
.board-shell > .sb-prompter.sb-top::after{content:'⇕ drag this edge to resize';position:sticky;display:block;bottom:-18px;margin:auto -22px -18px;flex:none;height:16px;line-height:16px;font-size:11px;letter-spacing:.04em;color:#9fb7b2;background:#123331;cursor:ns-resize;border-radius:0 0 12px 12px}
/* readability: nothing faded, bigger brighter text, more line spacing (top strip and side panel) */
.sb-prompter{line-height:1.55;color:#f4f8fb}
.sb-prompter .hy-step.ahead,.sb-prompter .hy-step.next-up{opacity:1!important}
.sb-prompter .hy-say{color:#f4f8fb}
.sb-prompter .hy-step.live .hy-say{color:#ffffff;font-weight:600}
.sb-prompter .hy-step.next-up{border-top:1px solid #ffffff33;padding-top:6px}
.sb-prompter .hy-n{color:#b8c7dc}
.board-shell > .sb-prompter.sb-top .hy-step.live{font-size:1.5em;line-height:1.45}
.board-shell > .sb-prompter.sb-top .hy-step.next-up{font-size:1.2em;line-height:1.45;opacity:1;color:#e8f0f7;margin-top:8px}
.board-shell > .sb-prompter.sb-top .hy-cue{font-size:.9em}
.dm-prompter{font-size:21px;line-height:1.6}
.dm-prompter .hy-step.ahead,.dm-prompter .hy-step.next-up{opacity:1!important}
/* the next part (after PRESS NEXT) is shown at full strength everywhere; only lines already said stay dimmed */
.hy-step.ahead{opacity:1!important}
.hy-step.next-up .hy-say,.hy-step.next-up .hy-draw,.hy-step.ahead .hy-say,.hy-step.ahead .hy-draw{opacity:1!important}
.board-shell > .sb-prompter.sb-top .hy-step.next-up .hy-say{color:#e8f0f7}
</style>"""

SYNC_OLD = "$('#board')?.classList.toggle('sb-on',STUDIO&&hy&&sbOn);"
SYNC_NEW = ("$('#board')?.classList.toggle('sb-on',STUDIO&&hy&&sbOn);"
            # move the script out of the slide (above it) when it is at the top, back onto the slide when on the left
            "{const sbp=$('#sb-prompter'),bw=$('#board'),shell=bw?.parentElement;if(sbp&&bw&&shell){const top=sbTop&&STUDIO&&hy&&sbOn;"
            "sbp.classList.toggle('sb-top',top);shell.classList.toggle('sbtop',top);"
            "if(top&&sbp.parentElement!==shell)shell.insertBefore(sbp,bw);if(!top&&sbp.parentElement!==bw)bw.insertBefore(sbp,bw.querySelector('.cam-bubble'));"
            "if(!top)sbp.style.display='';else sbp.style.display='block';"
            "{const hs=(()=>{try{return +localStorage.getItem('hy-sb-h')||0}catch{return 0}})();shell.classList.toggle('sbsized',top&&hs>0);if(hs>0)shell.style.setProperty('--sbmax',hs+'px')}"
            "if(top&&!sbp.dataset.grip){sbp.dataset.grip='1';"
            "sbp.addEventListener('pointerdown',e=>{if(!sbp.classList.contains('sb-top'))return;const r=sbp.getBoundingClientRect();if(e.clientY<r.bottom-20)return;e.preventDefault();"
            "const sh=sbp.parentElement,y0=e.clientY,h0=r.height;sbp.setPointerCapture?.(e.pointerId);"
            "const mv=ev=>{const h=Math.round(Math.max(70,Math.min(window.innerHeight*.75,h0+ev.clientY-y0)));sh.classList.add('sbsized');sh.style.setProperty('--sbmax',h+'px');sh.style.setProperty('--sbh',(h+12)+'px');try{localStorage.setItem('hy-sb-h',h)}catch{}};"
            "const up=()=>{sbp.removeEventListener('pointermove',mv);sbp.removeEventListener('pointerup',up)};sbp.addEventListener('pointermove',mv);sbp.addEventListener('pointerup',up)});"
            "sbp.addEventListener('dblclick',e=>{const r=sbp.getBoundingClientRect();if(e.clientY<r.bottom-20)return;const sh=sbp.parentElement;sh.classList.remove('sbsized');try{localStorage.removeItem('hy-sb-h')}catch{};requestAnimationFrame(()=>sh.style.setProperty('--sbh',(sbp.offsetHeight+12)+'px'))})}"
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
    s = rep(s, "sb.style.fontSize=Math.round(state.font*.9)+'px';", "sb.style.fontSize=Math.round(state.font*1.15)+'px';")   # bigger script text
    s = rep(s, SYNC_OLD, SYNC_NEW)
    s = s.replace("</head>", SB_CSS + "</head>", 1)   # the first </head> is the page head (a later one is inside a string)
    return s
