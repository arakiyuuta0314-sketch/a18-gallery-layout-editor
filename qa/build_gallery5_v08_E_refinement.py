from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,cv2
r=Path(r'C:\Users\User\source\repos\a18-gallery5-material-review')
base=np.asarray(Image.open(r/'rooms/gallery5/gallery5_palace_E.png').convert('RGB')).copy()
h,w=base.shape[:2];yy,xx=np.mgrid[0:h,0:w];rng=np.random.default_rng(18)
a=base.astype(np.float32)
# All operations are tonal/material refinements to the approved E pixels, not transplanted architecture.
# Rich walnut and burgundy micrograin: use original palette as the material mask.
wood=(a[:,:,0]>65)&(a[:,:,0]<155)&(a[:,:,1]>43)&(a[:,:,1]<117)&(a[:,:,2]<94)&(yy<242)
red=(a[:,:,0]>52)&(a[:,:,0]<140)&(a[:,:,1]<83)&(a[:,:,2]<90)&(yy<228)
floor=(yy>238)&(a[:,:,0]>60)&(a[:,:,0]<112)&(abs(a[:,:,0]-a[:,:,1])<15)&(abs(a[:,:,1]-a[:,:,2])<15)
noise=rng.normal(0,1,(h,w)).astype(np.float32)
woodgrain=np.sin(xx*0.42+np.sin(yy*0.10)*2.0)*1.1+np.sin(xx*.13+yy*.08)*1.0
for c in range(3):
 a[:,:,c]+=wood*(woodgrain*1.5+noise*1.3)
 a[:,:,c]+=red*(np.sin(xx*.09+yy*.27)*1.2+noise*.8)
 a[:,:,c]+=floor*(noise*1.2+np.sin(xx*.028+yy*.041)*1.0)
# Wall sconces: soft, localized amber light, preserving original drawing.
for cx,cy in [(186,111),(748,111)]:
 light=np.exp(-(((xx-cx)/62)**2+((yy-cy)/75)**2)*1.6)
 for c,k in enumerate([21,12,4]):a[:,:,c]+=light*k*(yy<226)
# Subtle architectural overhead light on burgundy rear wall, leaving frames untouched.
for cx in [96,826]:
 light=np.exp(-(((xx-cx)/120)**2+((yy-80)/100)**2)*1.5)*red
 for c,k in enumerate([11,6,4]):a[:,:,c]+=light*k
# Center aisle is deliberately deep, but floor gains believable soft warm illumination.
illum=np.exp(-(((xx-465)/390)**2+((yy-285)/290)**2)*1.4)*floor
for c,k in enumerate([13,11,9]):a[:,:,c]+=illum*k
# A small amount of shadow at floor/wall junction, original E geometry intact.
shadow=np.exp(-((yy-241)/16)**2)*((yy>228)&(yy<273))
for c in range(3):a[:,:,c]-=shadow*9
out=Image.fromarray(np.clip(a,0,255).astype('uint8'),'RGB')
# Gold details are already in E. Preserve them rather than pasting mismatched gilding.
p=r/'architecture-review/gallery5/gallery5_v08_E_material_refinement_REVIEW.png';out.save(p)
print('SAVED',p,out.size,'unchanged pixels',np.mean(np.all(base==np.array(out),axis=2)))

