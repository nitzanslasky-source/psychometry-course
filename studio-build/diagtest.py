import subprocess,re,os,sys
def test(path):
    s=open(path).read(); k=s.rfind('</body></html>')
    js='''<script>(function wait(n){const d=window.COURSE_DIAGNOSTICS;if(!d){if(n>300){document.title='NO DIAG';return}return setTimeout(()=>wait(n+1),100)}document.title='OK'})(0)</script></body></html>'''
    open('dbg.html','w').write(s[:k]+js)
    r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--virtual-time-budget=60000','--dump-dom','file://'+os.path.abspath('dbg.html')],capture_output=True,text=True,timeout=200)
    return re.search(r'<title>(.*?)</title>',r.stdout,re.S).group(1)[:200]
if __name__=='__main__': print(test(sys.argv[1]))
