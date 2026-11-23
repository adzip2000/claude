import base64,re,sys,os
S,tpl,out,imgdir=sys.argv[1:5]
h=open(tpl).read()
def rep(m):
    k=m.group(1)
    for ext,mt in (('.png','image/png'),('.jpg','image/jpeg')):
        p=os.path.join(imgdir,k+ext)
        if os.path.exists(p): return 'data:%s;base64,%s'%(mt,base64.b64encode(open(p,'rb').read()).decode())
    raise SystemExit('missing '+k)
h=re.sub(r'\{\{(\w+)\}\}',rep,h)
open(out,'w').write(h); print(len(h)//1024,'KB')
