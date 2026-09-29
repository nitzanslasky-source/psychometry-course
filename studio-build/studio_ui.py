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


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:60])
    return s.replace(old, new)


def apply(s):
    s = rep(s, SAVE_OLD, SAVE_NEW)
    s = rep(s, "function stopRecording(){", ASK_FN + "function stopRecording(){")
    return s
