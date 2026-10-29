from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from pathlib import Path
import numpy as np
R=Path(r'C:\Users\User\source\repos\a18-gallery5-material-review')
SRC=Image.open(r'C:\Users\User\source\repos\web-tools-preview-a18-entrance-2d-assets-20261028\a18\layout-test\assets\entrance\approved_initial_20261027\entrance_background_initial_approved.png').convert('RGB')
LV6=Image.open(R/'architecture-review/entrance-comparison/entrance-lv6-approved.png').convert('RGB')
W,H=930,582
# Source-authentic wall and floor; avoid drawn-on vector-style textures.
out=Image.new('RGB',(W,H),'#211710')
floor=SRC.crop((0,518,SRC.width,SRC.height)).resize((W,H-224),Image.Resampling.LANCZOS)
out.paste(floor,(0,224))
wall=SRC.crop((62,22,505,518)).resize((930,224),Image.Resampling.LANCZOS)
out.paste(wall,(0,0))
# Replace source stretched panel rails with repeated authentic wooden panel texture.
wood=SRC.crop((72,398,515,511)).resize((W,60),Image.Resampling.LANCZOS)
out.paste(wood,(0,164))
# Actual source pilasters and crown molding.
crown=SRC.crop((70,20,512,105)).resize((W,40),Image.Resampling.LANCZOS)
out.paste(crown,(0,0))
pil=SRC.crop((512,20,580,520)).resize((40,225),Image.Resampling.LANCZOS)
for x in (15,185,745,875):out.paste(pil,(x,0))
# Actual dark doorway recesses on left and right side walls, with subtly angled jambs.
d=ImageDraw.Draw(out)
for mirror in (False,True):
 def xy(x,y):return (W-1-x,y) if mirror else (x,y)
 # Sidewall perspective and warm walnut wood material sampled from the approved entrance.
 p=[xy(0,225),xy(175,225),xy(175,548),xy(0,582)]
 d.polygon(p,fill='#442a1d')
 # Map actual wall and wood texture onto sidewall, clipped to polygon.
 mask=Image.new('L',(W,H));md=ImageDraw.Draw(mask);md.polygon(p,fill=255)
 side=SRC.crop((65,105,506,510)).resize((175,357),Image.Resampling.LANCZOS)
 layer=Image.new('RGB',(W,H));layer.paste(side,(0 if not mirror else W-175,225))
 out.paste(layer,(0,0),mask)
 d=ImageDraw.Draw(out)
 # Portal is a rectangular, walkable-looking dark opening (no arches), with slanted jambs.
 q=[xy(43,301),xy(126,301),xy(137,515),xy(40,534)]
 d.polygon(q,fill='#0e1e1b')
 d.line([xy(40,534),xy(43,301),xy(126,301),xy(137,515)],fill='#bd8e54',width=7,joint='curve')
 d.line([xy(46,529),xy(49,307),xy(121,307),xy(130,512)],fill='#634025',width=4)
 d.line([xy(40,534),xy(137,515)],fill='#c09a68',width=5)
 # Architectural return/shadow and floor perspective.
 d.line([xy(175,225),xy(175,548)],fill='#2b1a13',width=8)
 d.line([xy(0,582),xy(175,548)],fill='#775338',width=5)
# Keep the original E arrangement: exactly three picture spaces, central larger.
def nine(src,w,h,e=16):
 sw,sh=src.size
 result=Image.new('RGB',(w,h))
 for j,(sy0,sy1,dy0,dy1) in enumerate([(0,e,0,e),(e,sh-e,e,h-e),(sh-e,sh,h-e,h)]):
  for i,(sx0,sx1,dx0,dx1) in enumerate([(0,e,0,e),(e,sw-e,e,w-e),(sw-e,sw,w-e,w)]):
   if dx1>dx0 and dy1>dy0:result.paste(src.crop((sx0,sy0,sx1,sy1)).resize((dx1-dx0,dy1-dy0),Image.Resampling.LANCZOS),(dx0,dy0))
 return result
frame=LV6.crop((195,148,465,315))
for x,y,w,h in [(216,67,114,149),(339,58,252,165),(600,67,114,149)]:
 d=ImageDraw.Draw(out);d.rectangle((x-4,y-3,x+w+4,y+h+5),fill='#29190f')
 out.paste(nine(frame,w,h),(x,y))
 d=ImageDraw.Draw(out);d.rectangle((x+17,y+17,x+w-18,y+h-18),fill='#13534c');d.rectangle((x+18,y+18,x+w-19,y+h-19),outline='#8d6a43',width=2)
# E's burgundy runner; render restrained fabric shading rather than vector outlines.
d=ImageDraw.Draw(out)
runner=[(423,229),(507,229),(605,581),(325,581)]
d.polygon(runner,fill='#8e6939')
d.polygon([(429,233),(501,233),(592,581),(338,581)],fill='#4b1828')
d.polygon([(434,239),(496,239),(577,581),(353,581)],fill='#8c293e')
# A very soft fabric luminance gradient inside carpet, no added fixtures.
a=np.array(out,dtype=np.float32)
for y in range(242,582):
 t=(y-229)/353
 left=434-81*t;right=496+81*t
 for x in range(max(0,int(left)),min(W,int(right))):
  light=1+0.055*(1-abs((x-(left+right)/2)/max(1,(right-left)/2)))
  a[y,x,:]=np.clip(a[y,x,:]*light,0,255)
out=Image.fromarray(a.astype('uint8'),'RGB')
p=R/'architecture-review/gallery5/gallery5_v04_authentic_entrance_material_REVIEW.png';out.save(p)
print('SAVED',p,out.size)
