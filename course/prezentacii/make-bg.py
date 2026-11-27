import numpy as np, math, random
from PIL import Image, ImageDraw, ImageFilter
random.seed(7); np.random.seed(7)
W,H=3200,1800
base=Image.new('RGB',(W,H),(150,205,245))
# deep blue blurred star spikes (like the certificate)
def spikes(cx,cy,R,r,n,rot,color,blur,op):
    L=Image.new('L',(W,H),0); d=ImageDraw.Draw(L)
    pts=[]
    for i in range(n*2):
        a=rot+math.pi*i/n; rad=R if i%2==0 else r
        pts.append((cx+rad*math.cos(a),cy+rad*math.sin(a)))
    d.polygon(pts,fill=int(255*op))
    L=L.filter(ImageFilter.GaussianBlur(blur))
    col=Image.new('RGB',(W,H),color); return L,col
for (cx,cy,R,r,n,rot,blur,op) in [(-150,1500,1500,330,8,-0.3,34,.95),(3250,1350,1400,300,8,0.2,38,.9),(1750,-250,900,260,8,0.5,40,.55),(2900,150,800,240,8,0.1,36,.55)]:
    L,col=spikes(cx,cy,R,r,n,rot,(24,118,214),blur,op); base.paste(col,(0,0),L)
# airbrushed light-blue wash
wash=Image.new('L',(W,H),0); d=ImageDraw.Draw(wash)
for _ in range(14):
    x=random.randint(0,W); y=random.randint(0,H); rr=random.randint(250,600); d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=random.randint(40,110))
wash=wash.filter(ImageFilter.GaussianBlur(160)); base.paste(Image.new('RGB',(W,H),(95,175,240)),(0,0),wash)
# white glow in the middle
glow=Image.new('L',(W,H),0); d=ImageDraw.Draw(glow); d.ellipse((600,200,2600,1500),fill=235)
glow=glow.filter(ImageFilter.GaussianBlur(260)); base.paste(Image.new('RGB',(W,H),(238,248,255)),(0,0),glow)
# soft drips from the glow
dr=Image.new('L',(W,H),0); d=ImageDraw.Draw(dr)
for x in range(900,2400,95):
    h=random.randint(200,520); w=random.randint(14,30); d.rounded_rectangle((x,1050,x+w,1050+h),radius=w//2,fill=random.randint(70,150))
dr=dr.filter(ImageFilter.GaussianBlur(14)); base.paste(Image.new('RGB',(W,H),(236,247,255)),(0,0),dr)
base=base.filter(ImageFilter.GaussianBlur(5))
# halftone bottom-left + grain + scratches
a=np.asarray(base).astype(float)
yy,xx=np.mgrid[0:H,0:W]
step=26; cxg=(xx%step)-step/2; cyg=(yy%step)-step/2
dist=np.hypot(xx/(0.5*W),(H-yy)/(0.6*H)); fade=np.clip(1-dist/0.95,0,1)
dots=(np.hypot(cxg,cyg)<(1+5.5*fade)).astype(float)*fade
a=a*(1-0.35*dots[...,None])+np.array([20,110,210])*0.35*dots[...,None]
a+=np.random.normal(0,5,(H,W,1))
im=Image.fromarray(np.clip(a,0,255).astype('uint8')); d=ImageDraw.Draw(im,'RGBA')
for _ in range(70):
    x=random.randint(0,W); y=random.randint(0,H); L=random.randint(120,520); ang=random.uniform(-0.4,0.4)
    d.line((x,y,x+L*math.cos(ang),y+L*math.sin(ang)),fill=(255,255,255,random.randint(35,90)),width=random.choice([1,1,2]))
im.save('/home/user/claude/course/prezentacii/img/bg-blur.jpg',quality=86,optimize=True)
im.resize((1280,720)).save('/tmp/claude-0/-home-user-claude/2cb2a3db-983a-593d-b763-79a7c2ceab03/scratchpad/bg-prev.png')
