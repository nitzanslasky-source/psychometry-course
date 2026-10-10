"""Mark AI-narrated videos in the studio (applied by build_verbal.py last).

Every video that has a script in ai_scripts/<videoId>.json (the writing task, the added summaries) will be narrated by
the teacher's cloned voice, so the teacher should NOT record it. The studio shows a clear banner on those videos and
the Record button asks before recording one. 2026-10-11: also the AI redo videos (math_patches/_ai_redo.py, recorded
math videos redone with the AI voice; studio_done tags them "AI redo") and the PLANNED AI videos: every unrecorded
math video (topics 1-38, 52) that is not the first lesson of its topic (studio_done tags them "AI (planned)"). Topic 51
is recorded by the teacher (all of it, also pt51-summary). Verbal topics 39-49 are not changed (decision pending).
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


TEACHER_TOPICS = {51}   # 2026-10-11 teacher: she records ALL of topic 51 herself (also pt51-summary, which has an AI script)
MATH_TOPICS = set(range(1, 39)) | {52}   # math topics whose non-first videos are AI (topic 51 is the teacher's)


def first_lessons(D):
    """topic -> its first teaching lesson (first non-solution video in course flow order)."""
    out = {}
    for f in D['flow']:
        if f['type'] == 'video' and f['topic'] not in out and D['videos'][f['ref']].get('kind') != 'solution':
            out[f['topic']] = f['ref']
    return out


def planned_ids(D, recorded=()):
    """2026-10-11 teacher decision: every math video except the first lesson of its topic is narrated by the AI voice.
    Planned = not recorded yet, not already an AI-script video, not the first lesson; topic 51 excluded (teacher)."""
    import math_api
    first, rec, have = first_lessons(D), set(recorded), set(ai_ids()) | set(math_api.load_ai_redo().AI_REDO)   # AI redo: own tag
    return sorted({f['ref'] for f in D['flow'] if f['type'] == 'video' and f['topic'] in MATH_TOPICS
                   and f['ref'] != first.get(f['topic']) and f['ref'] not in rec and f['ref'] not in have})


def teacher_ids(D):
    return {f['ref'] for f in D['flow'] if f['type'] == 'video' and f['topic'] in TEACHER_TOPICS}


def apply(s, D=None):
    for old, new in REPL:
        assert s.count(old) == 1, ('studio_ai anchor', s.count(old), old[:60])
        s = s.replace(old, new)
    k = s.find('async function startRecording(){')
    assert k > 0
    # 2026-10-11 AI redo (math_patches/_ai_redo.py): recorded math videos redone with the AI voice are AI videos too
    # (banner, Record asks first, not counted as "to record"); the on-camera first lessons (CAMERA) are not
    import math_api
    AR = math_api.load_ai_redo()
    ids = set(ai_ids()) | {v for v in AR.AI_REDO if AR.ai_redo(v)}
    planned = []
    if D is not None:
        import studio_done
        planned = planned_ids(D, studio_done.recorded_ids())
        ids = (ids | set(planned)) - teacher_ids(D)   # topic 51: the teacher records it all
    print('studio_ai: %d AI videos (%d planned: unrecorded non-first math videos; topic 51 is the teacher\'s)' % (len(ids), len(planned)))
    js = JS.replace('__AI_IDS__', json.dumps(sorted(ids))) + 'window.AI_PLANNED=new Set(%s);\n' % json.dumps(planned)
    return s[:k] + js.lstrip() + s[k:]
