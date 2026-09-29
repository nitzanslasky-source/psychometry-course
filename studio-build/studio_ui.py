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
/* ---- keep or discard a take (asked after Stop, before anything is saved) ---- */
function askKeepTake(blob){return new Promise(res=>{const url=URL.createObjectURL(blob),box=document.createElement('div');
 box.id='keep-take';box.setAttribute('role','dialog');box.setAttribute('aria-label','Keep this take?');
 box.style.cssText='position:fixed;inset:0;z-index:9999;background:#0f172acc;display:flex;align-items:center;justify-content:center;font-family:inherit';
 box.innerHTML='<div style="background:#fff;border-radius:16px;padding:22px;width:min(720px,92vw);box-shadow:0 20px 60px #0006">'
  +'<div style="font-size:20px;font-weight:700;margin-bottom:4px">Keep this take?</div>'
  +'<div style="color:#5b6b7a;font-size:14px;margin-bottom:12px">Only kept takes are saved to your recordings folder. Enter = keep · Esc = discard</div>'
  +'<video src="'+url+'" controls style="width:100%;border-radius:10px;background:#000;max-height:50vh"></video>'
  +'<div style="display:flex;gap:10px;justify-content:flex-end;margin-top:14px">'
  +'<button id="take-discard" style="padding:10px 18px;border-radius:10px;border:1px solid #d8e6e3;background:#fff;color:#b91c1c;font-weight:700;cursor:pointer">Discard</button>'
  +'<button id="take-keep" style="padding:10px 22px;border-radius:10px;border:0;background:#0f766e;color:#fff;font-weight:700;cursor:pointer">Keep</button></div></div>';
 document.body.append(box);
 const done=keep=>{document.removeEventListener('keydown',key,true);box.remove();URL.revokeObjectURL(url);res(keep)};
 const key=e=>{if(e.key==='Enter'){e.preventDefault();e.stopPropagation();done(true)}else if(e.key==='Escape'){e.preventDefault();e.stopPropagation();done(false)}};
 document.addEventListener('keydown',key,true);
 box.querySelector('#take-keep').onclick=()=>done(true);box.querySelector('#take-discard').onclick=()=>done(false);
 box.querySelector('#take-keep').focus()})}
"""


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:60])
    return s.replace(old, new)


def apply(s):
    s = rep(s, SAVE_OLD, SAVE_NEW)
    s = rep(s, "function stopRecording(){", ASK_FN + "function stopRecording(){")
    return s
