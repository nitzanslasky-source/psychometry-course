"""Mark AI-narrated videos in the studio (applied by build_verbal.py last).

Every video that has a script in ai_scripts/<videoId>.json (the writing task, the added summaries) will be narrated by
the teacher's cloned voice, so the teacher should NOT record it. The studio shows a clear banner on those videos and
the Record button asks before recording one.
"""
import glob, json, os

HERE = os.path.dirname(os.path.abspath(__file__))


def ai_ids():
    return sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(HERE, 'ai_scripts', '*.json'))
                  if not os.path.basename(p).startswith('_'))


JS = r"""
/* ---- AI-narrated videos: banner + guard on Record ---- */
const AI_VIDEOS=new Set(__AI_IDS__);
function aiBanner(){const v=typeof video==='function'?video():null,on=!!(STUDIO&&v&&AI_VIDEOS.has(v.id));let b=document.getElementById('ai-banner');
 if(!on){b?.remove();return}
 if(!b){b=document.createElement('div');b.id='ai-banner';b.style.cssText='position:fixed;left:50%;top:8px;transform:translateX(-50%);z-index:9000;background:#ede9fe;color:#3b0764;border:2px solid #7c3aed;border-radius:12px;padding:8px 16px;font:700 14px system-ui;box-shadow:0 6px 20px #0002;pointer-events:none';document.body.append(b)}
 b.textContent='🤖 AI voice video — no need to record this one'}
setInterval(aiBanner,700);
"""

REPL = [
    # asking before recording an AI video (the teacher may still want to, e.g. to compare)
    ("async function startRecording(){if(record)return;",
     "async function startRecording(){if(record)return;if(!(typeof CUT!=='undefined'&&CUT.cont)&&AI_VIDEOS.has(video()?.id)&&!window.__aiRecOk){"
     "toast('This video will be narrated by your AI voice — no need to record it. Press Record again within 5 seconds if you really want to.');"
     "window.__aiRecOk=true;setTimeout(()=>{window.__aiRecOk=false},5000);return}"),
]


def apply(s):
    for old, new in REPL:
        assert s.count(old) == 1, ('studio_ai anchor', s.count(old), old[:60])
        s = s.replace(old, new)
    k = s.find('async function startRecording(){')
    assert k > 0
    return s[:k] + JS.replace('__AI_IDS__', json.dumps(ai_ids())).lstrip() + s[k:]
