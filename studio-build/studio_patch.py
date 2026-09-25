"""Studio recording upgrades (applied by build_verbal.py).

- Recordings folder: choose a folder once (desktop Chrome/Edge); every take is written straight into
  <folder>/<Subject>/Topic NN - <title>/<videoId>-<timestamp>.webm. The choice is remembered.
  No folder chosen / unsupported browser → the take downloads automatically to Downloads (same file name).
- Takes are no longer kept inside browser storage (avoids doubling ~100 GB of video on disk).
- Better quality: 8 Mbps video, 160 kbps audio, natural microphone (no echo cancellation / auto gain).
"""

REPL = [
    # quality
    ("const rec=new MediaRecorder(stream,mime?{mimeType:mime,videoBitsPerSecond:4500000}:undefined)",
     "const rec=new MediaRecorder(stream,mime?{mimeType:mime,videoBitsPerSecond:8000000,audioBitsPerSecond:160000}:undefined)"),
    ("audio:useMic?{echoCancellation:true,noiseSuppression:true}:false",
     "audio:useMic?{echoCancellation:false,noiseSuppression:true,autoGainControl:false,channelCount:1,sampleRate:48000}:false"),
    # save the take to the recordings folder (or auto-download)
    ("try{await putMedia({key,lesson:v.id,blob,name,date:new Date().toISOString()});state.media[v.id]={type:'stored',key,name};save();$('#record-message').textContent='Take saved in this browser. Download it to keep a separate copy.';toast('Take saved. The student view now plays this recording on this device.');previewTake()}catch{downloadBlob(name,blob);$('#record-message').textContent='Browser storage was unavailable. The recording has been offered as a download.';toast('Download this take now; it could not be stored in the browser.')}",
     "const where=await saveTakeFile(v,name,blob);state.media[v.id]={type:'file',name,path:where||'Downloads/'+name};save();"
     "if(where&&r.chapters?.length){const ch=r.chapters.filter((c,i,a)=>i===0||c.title!==a[i-1].title);await saveTakeFile(v,name.replace(/\\.(webm|mp4)$/,'.chapters.json'),new Blob([JSON.stringify({videoId:v.id,chapters:ch},null,1)],{type:'application/json'}))}"
     "$('#record-message').textContent=where?'Saved: '+where:'Saved to your Downloads folder: '+name+'  (choose a Recordings folder to file takes automatically)';"
     "toast(where?'Take saved to '+where:'Take downloaded: '+name)"),
    # chapters: note the moment of every slide change while recording (pauses excluded)
    ("function draw(){if(!record)return;", "function draw(){if(!record)return;noteChapter();"),
    ("recTimer=setInterval(()=>{if(record){", "recTimer=setInterval(()=>{if(record){noteChapter();"),
    # file-type takes have no in-browser copy
    ("if(m.type==='url')return m.url;", "if(m.type==='url')return m.url;if(m.type==='file')return null;"),
    # UI: folder button next to Rehearse
    ('<button class="quiet" id="rehearse">Rehearse</button>',
     '<span class="row"><button class="quiet" id="rec-folder" title="Choose where recordings are saved">📁 Recordings folder</button>'
     '<span id="rec-folder-name" class="muted" style="font-size:13px"></span><button class="quiet" id="rehearse">Rehearse</button></span>'),
    ("$('#rehearse').onclick=startRehearsal;", "$('#rehearse').onclick=startRehearsal;bindRecFolder();"),
    # folder button in the top bar too, next to ● Record
    ('<button id="qrec" title="Start recording this lesson">● Record</button>',
     '<button id="qfolder" title="Choose where recordings are saved">📁 Folder</button><button id="qrec" title="Start recording this lesson">● Record</button>'),
]

FUNCS = r"""
/* ---- chapters: the moment of every slide change during a recording (pauses excluded) ---- */
function noteChapter(){if(!record||record.lastBeat===state.beat)return;record.lastBeat=state.beat;const now=Date.now(),t=(now-record.started-record.pausedMs-(record.pausedAt?now-record.pausedAt:0))/1000,bt=record.v.beats[state.beat]||{};(record.chapters=record.chapters||[]).push({start:Math.max(0,Math.round(t*10)/10),title:bt.bigTitle||bt.title||('Slide '+(state.beat+1))})}
/* ---- recordings folder (File System Access API, desktop Chrome/Edge) ---- */
const RF={db:null,handle:null};
function rfDB(){return RF.db||(RF.db=new Promise((ok,no)=>{const r=indexedDB.open('studio-rec-folder',1);r.onupgradeneeded=()=>r.result.createObjectStore('h');r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error)}))}
async function rfGet(){try{const db=await rfDB();return await new Promise(ok=>{const q=db.transaction('h').objectStore('h').get('dir');q.onsuccess=()=>ok(q.result||null);q.onerror=()=>ok(null)})}catch{return null}}
async function rfSet(h){const db=await rfDB();return new Promise(ok=>{const t=db.transaction('h','readwrite');t.objectStore('h').put(h,'dir');t.oncomplete=()=>ok()})}
function rfLabel(){const el=$('#rec-folder-name');if(el)el.textContent=RF.handle?'→ '+RF.handle.name:(window.showDirectoryPicker?'→ Downloads (no folder chosen)':'→ Downloads');const q=$('#qfolder');if(q){q.textContent=RF.handle?'📁 '+RF.handle.name:'📁 Choose folder';q.title=RF.handle?'Recordings are saved in "'+RF.handle.name+'" — click to change':'Choose where recordings are saved'}}
async function bindRecFolder(){const b=$('#rec-folder'),q=$('#qfolder');if(!b&&!q)return;if(!window.showDirectoryPicker){if(b)b.hidden=true;if(q)q.hidden=true;rfLabel();return}
 if(!RF.handle)RF.handle=await rfGet();rfLabel();
 const pick=async()=>{try{const h=await window.showDirectoryPicker({id:'studio-recordings',mode:'readwrite'});RF.handle=h;await rfSet(h);rfLabel();toast('Recordings will be saved in "'+h.name+'", sorted by subject and topic.')}catch{}};if(b)b.onclick=pick;if(q)q.onclick=pick}
function rfClean(s){return String(s).replace(/[\\/:*?"<>|]+/g,'-').replace(/\s+/g,' ').trim().slice(0,80)}
function rfSubject(t){t=+t;return t>=39?'4 Verbal':t>=30?'3 Geometry':t>=21?'2 Word Problems':'1 Algebra'}
async function saveTakeFile(v,name,blob){
 if(RF.handle){try{let p=await RF.handle.queryPermission({mode:'readwrite'});if(p!=='granted')p=await RF.handle.requestPermission({mode:'readwrite'});
  if(p==='granted'){const T=(D.topics||[]).find(t=>+t.id===+v.topic);const sub=rfSubject(v.topic),top=rfClean('Topic '+String(v.topic).padStart(2,'0')+' - '+(T?T.title:''));
   const d1=await RF.handle.getDirectoryHandle(sub,{create:true}),d2=await d1.getDirectoryHandle(top,{create:true});
   const fh=await d2.getFileHandle(name,{create:true}),w=await fh.createWritable();await w.write(blob);await w.close();return RF.handle.name+'/'+sub+'/'+top+'/'+name}}
 catch(e){console.warn('recordings folder failed',e)}}
 downloadBlob(name,blob);return null}
"""

def apply(html):
    for old, new in REPL:
        assert html.count(old) == 1, 'studio patch anchor not found: ' + old[:70]
        html = html.replace(old, new)
    k = html.find('async function startRecording(){')
    assert k > 0
    return html[:k] + FUNCS.lstrip() + html[k:]
