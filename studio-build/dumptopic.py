import json,re,sys
D=json.load(open('course18.json'))
flow={f['id']:f for f in D['flow']}
tid=int(sys.argv[1]); t=[x for x in D['topics'] if x['id']==tid][0]
out=['# Topic %d %s'%(tid,t['title'])]
for sid in t['sections']:
  sec=[x for x in D['sections'] if x['id']==sid][0]
  out.append('\n######## SECTION %s — %s (%s)'%(sid,sec['title'],sec['kind']))
  for it in sec['items']:
    f=flow[it]
    if f['type']=='question':
      q=D['questions'][f['ref']]
      out.append('--- Q %s: %s'%(f['ref'],re.sub(r'\s+',' ',q.get('stemRich') or q['stem']).strip()))
      out.append('  CHOICES: %s correct=%s'%(q.get('choicesRich') or q['choices'],','.join(str(k+1) for k in q['correct'])))
    elif f['type']=='video':
      v=D['videos'][f['ref']]
      out.append("=== VIDEO %s: kind=%s title=%r"%(f['ref'],v['kind'],v['title']))
      for i,b in enumerate(v['beats']):
        out.append('[%d] %s'%(i+1,b['title'])); out.append('  BOARD: %s'%b.get('board')); out.append('  SCRIPT: %s'%b.get('script'))
    else: out.append('?? %s %s'%(f['type'],f.get('ref')))
open('tv%d.txt'%tid,'w').write('\n'.join(out))
nv=sum(l.startswith('=== VIDEO') for l in out); nq=sum(l.startswith('--- Q') for l in out)
print(tid,t['title'],'videos',nv,'questions',nq, [ (x['id'],x['kind'],len(x['items'])) for x in D['sections'] if x['topic']==tid])
