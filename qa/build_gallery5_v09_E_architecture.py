from PIL import Image,ImageDraw,ImageFilter
from pathlib import Path
import numpy as np
r=Path(r'C:\Users\User\source\repos\a18-gallery5-material-review')
original=Image.open(r/'rooms/gallery5/gallery5_palace_E.png').convert('RGB')
a=np.array(original).astype(np.float32);h,w=a.shape[:2]
y,x=np.mgrid[:h,:w]
# Keep all architecture, burgundy/gold/wood palette, E layout, and three slots.
# Gradual ambient light: lit rear wall, subtly shaded sidewalls, slightly brighter stone aisle.
rear=(y<225);side=((x<184)|(x>745))&(y>=225)
ambient=1+0.13*np.exp(-((x-465)/380)**2-((y-95)/170)**2)
a[rear]*=ambient[rear,None]
side_grad=(0.78+0.18*np.clip((y-220)/360,0,1))
a[side]*=side_grad[side,None]
# Marble's subdued warm neutral cast; do not borrow the entrance floor.
floor=(y>=230)&(~side)&(a[:,:,0]>60)&(np.max(a,axis=2)-np.min(a,axis=2)<20)
a[floor,0]*=1.075;a[floor,1]*=1.045;a[floor,2]*=1.005
# Very low-contrast large scale illumination, avoiding noisy marble speckling.
shine=5*np.exp(-((x-465)/260)**2-((y-365)/240)**2)
for c in range(3):a[:,:,c]+=shine*floor
im=Image.fromarray(np.uint8(np.clip(a,0,255)),'RGB')
# Physically consistent recessed portals. Retain E arches, add wall thickness / jamb shading.
d=ImageDraw.Draw(im,'RGBA')
for mirrored in (False,True):
 def p(x,y):return (929-x,y) if mirrored else (x,y)
 # Recessed inner opening darkens with depth, but original arch remains visible.
 d.polygon([p(68,334),p(133,334),p(132,467),p(68,467)],fill=(4,16,16,115))
 # Inner wood reveal gives depth without introducing a different architectural style.
 d.line([p(61,464),p(61,345),p(65,322),p(75,307),p(89,301)],fill=(40,23,15,155),width=8)
 d.line([p(139,468),p(139,344),p(134,323),p(123,308),p(109,303)],fill=(19,13,10,190),width=9)
 d.line([p(63,465),p(137,465)],fill=(160,119,77,95),width=4)
 # Side wall floor contact shadow strengthens the E perspective.
 d.polygon([p(1,535),p(184,535),p(184,547),p(0,575)],fill=(13,10,9,85))
# Gentle wall sconces, painted into the same E material.
glow=Image.new('RGBA',(w,h),(0,0,0,0));g=ImageDraw.Draw(glow,'RGBA')
for cx in (185,746):
 for rad,alpha in [(76,7),(54,10),(32,15)]:
  g.ellipse((cx-rad,106-rad,cx+rad,106+rad),fill=(244,180,98,alpha))
glow=glow.filter(ImageFilter.GaussianBlur(18));im=Image.alpha_composite(im.convert('RGBA'),glow).convert('RGB')
p=r/'architecture-review/gallery5/gallery5_v09_E_architecture_finish_REVIEW.png';im.save(p)
print('SAVED',p,'SIZE',im.size)
