# Usage: python3 make-pdf.py <dir with sNN.png> <out.pdf>
import sys,glob
from PIL import Image
d,out=sys.argv[1:3]
ims=[Image.open(f).convert('RGB') for f in sorted(glob.glob(d+'/s*.png'))]
# 3200x1800 px at 200 dpi = 16x9 inch page
ims[0].save(out,save_all=True,append_images=ims[1:],resolution=200,quality=86,optimize=True)
print(len(ims),'pages')
