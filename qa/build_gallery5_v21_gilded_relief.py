"""A18 Gallery 5 v21 – gilded laurel/cartouche relief on two existing burgundy insets.

Real material editing: replace only the two unfinished gold marks in the upper
side panels. Preserve approved E, v16 frame geometry, v20 architecture/corridors,
wood panelling, carpet and floor pixel-for-pixel outside the panel motif masks.
Source gold textures are sampled from v20's authentic gilded central frame.
No standalone generated image or new furniture is inserted.
"""
from pathlib import Path
import math
import cv2
import numpy as np
from PIL import Image,ImageDraw,ImageChops,ImageFilter
ROOT=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
PAGE=ROOT/"architecture-review/entrance-gallery5-comparison"
PREV=Image.open(PAGE/"gallery5-v20.png").convert("RGB")
assert PREV.size==(930,582)
arr=np.asarray(PREV).copy()
H,W=arr.shape[:2]
S=5
px=86; py=105
# Two panels are mirror images across canvas center, no approximate re-placement.
# Left ornamental red field x=55..141, y=77..182; right mirrored x=789..875.
LEFT_X=55; TOP_Y=77

# Remove *only* the old four malformed golden squiggles with inpainting.
# The surrounding walnut frame and the wine-red architectural recess are retained.
remove=np.zeros((H,W),np.uint8)
for reflected in (False,True):
    transform=lambda x: W-1-x if reflected else x
    for xa,xb in ((65,78),(119,133)):
        x0,x1=sorted((transform(xa),transform(xb)))
        remove[84:120,x0:x1+1]=255
# This small-area restoration copies material from adjacent original wine-red pixels.
arr=cv2.inpaint(arr,remove,5,cv2.INPAINT_TELEA)
bg=Image.fromarray(arr,"RGB")

msize=(px*S,py*S)
goldmask=Image.new("L",msize,0)
highlightmask=Image.new("L",msize,0)
etchmask=Image.new("L",msize,0)
g=ImageDraw.Draw(goldmask)
hi=ImageDraw.Draw(highlightmask)
et=ImageDraw.Draw(etchmask)
def q(pt):
    return (int(round(pt[0]*S)),int(round(pt[1]*S)))
def bez(a,b,c,d,n=24):
    return [((1-t)**3*a[0]+3*(1-t)**2*t*b[0]+3*(1-t)*t*t*c[0]+t**3*d[0],
             (1-t)**3*a[1]+3*(1-t)**2*t*b[1]+3*(1-t)*t*t*c[1]+t**3*d[1])
            for t in np.linspace(0,1,n)]
def stroke(target,pts,width,fill=255):
    target.line([q(pt) for pt in pts],fill=fill,width=max(1,int(round(width*S))),joint="curve")
def diamond(cx,cy,rx,ry,target):
    target.polygon([q(p) for p in [(cx,cy-ry),(cx+rx,cy),(cx,cy+ry),(cx-rx,cy)]],fill=255)
def leaf(target,base,tip,width):
    bx,by=base;tx,ty=tip;dx,dy=tx-bx,ty-by
    l=max(.01,math.hypot(dx,dy));nx=-dy/l;ny=dx/l
    lcurve=bez((bx,by),(bx+dx*.10+nx*width,by+dy*.10+ny*width),
               (bx+dx*.75+nx*width*.56,by+dy*.75+ny*width*.56),(tx,ty),10)
    rcurve=bez((tx,ty),(bx+dx*.77-nx*width*.4,by+dy*.77-ny*width*.4),
               (bx+dx*.09-nx*width*.78,by+dy*.09-ny*width*.78),(bx,by),10)
    target.polygon([q(p) for p in (lcurve+rcurve)],fill=255)
    stroke(et,[(bx,by),((bx+tx)/2,(by+ty)/2),(tx,ty)],.46,175)
# An open pair of chased laurel sprays: gold foliage, bronze shadow and engraved veins.
for mirrored in (False,True):
    flip=lambda p: (px-p[0],p[1]) if mirrored else p
    stem=bez(*[flip(t) for t in [(43,95),(22,76),(11,43),(28,23)]],n=65)
    stroke(g,stem,1.35)
    stroke(hi,[(x-0.8 if not mirrored else x+0.8,y-0.8) for x,y in stem[1:-4]],.45)
    # One genuinely ornamental branch, no extra furniture or wall light.
    settings=[
      ((39,91),(30,83),3.0),
      ((31,80),(19,76),4.0),
      ((24,66),(12,61),4.3),
      ((20,53),(10,47),4.0),
      ((22,40),(11,35),3.4),
      ((28,27),(20,18),3.0),
      ((33,84),(39,75),2.7),
      ((26,70),(37,62),3.2),
      ((23,55),(34,48),3.4),
      ((25,41),(36,35),3.0)
    ]
    for b,t,w in settings:leaf(g,flip(b),flip(t),w)
    # Small scrolls at the upper terminus and at the joined stalk base.
    stroke(g,[flip(p) for p in bez((28,23),(27,14),(36,12),(40,17),24)],1.1)
    stroke(g,[flip(p) for p in bez((40,92),(38,99),(44,101),(45,97),22)],1.1)

# Cartouche sits BETWEEN the laurel branches: burgundy enamel center,
# double gilded ring and one inset jewel – not a letter/number/logo.
# Its symmetry is deliberately quieter than the wood and frame gold decoration.
cx=43
# upper palmette, 5 pointed petals on an oval pad
stroke(g,bez((cx,32),(cx-8,26),(cx-8,20),(cx,20),18),1.1)
stroke(g,bez((cx,32),(cx+8,26),(cx+8,20),(cx,20),18),1.1)
for sx in (-1,0,1):
    diamond(cx+sx*5,25+(3 if sx else 0),2.2 if sx else 3,5 if sx==0 else 3,g)
# Main diamond medallion – no opaque gold block in the middle
med=[(43,49),(52,59),(43,69),(34,59)]
stroke(g,med+[med[0]],2.1)
stroke(hi,[(43,49),(52,59),(43,69)],.65)
diamond(cx,59,3.2,5.4,g)
# small gold beads/dots crossing the middle
for x,y,r in [(43,43,1.7),(43,75,1.7),(31,59,1.05),(55,59,1.05)]:
    g.ellipse([q((x-r,y-r)),q((x+r,y+r))],fill=255)
# Thin subdued flourishes beneath pendant, taper naturally into vine tails.
stroke(g,bez((41,78),(34,82),(35,88),(43,95),25),.8)
stroke(g,bez((45,78),(52,82),(51,88),(43,95),25),.8)
# The wood panel itself already has a visible gilded border. Do not add a second border.

# Actual gilded-frame grain drives relief modulation; avoids flat vector gold.
src=np.asarray(PREV.crop((342,100,580,115)).convert("RGB"),np.float32)
strip=(src @ np.array([.30,.59,.11],np.float32))
rep=np.tile(strip,(math.ceil(py/15)+1,1))[:py,:]
rep_img=Image.fromarray(np.uint8(np.clip(rep,0,255))).resize(msize,Image.Resampling.BICUBIC)
metal_luma=np.asarray(rep_img,np.float32)
# Gold texture deliberately darker than the gilded picture frames.
metal=np.zeros((msize[1],msize[0],3),dtype=np.uint8)
v=np.clip((metal_luma-125)*.42,-32,35)
for ch,(base,strength) in enumerate(((173,1.0),(126,.86),(64,.71))):
    metal[:,:,ch]=np.uint8(np.clip(base+v*strength,0,255))
metal=Image.fromarray(metal,"RGB")
# Engraved contact shadow offset downward-right by <1px; highlight upper-left.
gold=goldmask.filter(ImageFilter.GaussianBlur(.24*S))
drop=Image.new("L",msize,0);drop.paste(gold,(int(.75*S),int(1*S)))
shade=Image.new("RGB",msize,(28,13,14))
relief=Image.new("RGB",msize)
relief.paste(shade,(0,0),drop.point(lambda i:int(i*.88)))
relief.paste(metal,(0,0),gold)
# A hint of directional shimmer follows upper strokes, not every leaf.
hcol=Image.new("RGB",msize,(224,178,98))
relief.paste(hcol,(0,0),highlightmask.point(lambda i:int(i*.55)))
# etched leaf midribs are only barely warmer/darker than gold.
ecol=Image.new("RGB",msize,(111,72,34))
relief.paste(ecol,(0,0),etchmask.point(lambda i:int(i*.42)))
# compose tightly within 86×105 content; do not resample the whole room.
alpha=ImageChops.lighter(gold,drop).resize((px,py),Image.Resampling.LANCZOS)
relief=relief.resize((px,py),Image.Resampling.LANCZOS)
base=np.array(bg)
result=np.asarray(relief,dtype=np.float32)
m=np.asarray(alpha,np.float32)/255.
for mirror in (False,True):
    x=LEFT_X if not mirror else W-LEFT_X-px
    patch=result[:,::-1,:] if mirror else result
    mask=m[:,::-1] if mirror else m
    # Inlaid gilding: color only where our relief marks exist.
    original=base[TOP_Y:TOP_Y+py,x:x+px,:].astype(np.float32)
    base[TOP_Y:TOP_Y+py,x:x+px,:]=np.uint8(np.clip(original*(1-mask[...,None])+patch*mask[...,None],0,255))
out=Image.fromarray(base)
# Original v20 image must be completely unchanged outside the two inset ornaments,
# including both arches, both corridors, all three picture frames and the runner.
diff=ImageChops.difference(PREV,out)
assert diff.getbbox() is not None
allowed=Image.new("L",(W,H),0)
a=ImageDraw.Draw(allowed)
for xx in (LEFT_X,W-LEFT_X-px):
    a.rectangle((xx,TOP_Y,xx+px,TOP_Y+py),fill=255)
change=np.max(np.asarray(diff),axis=2)>0
outside=(np.asarray(allowed)==0)
assert not (change & outside).any(), "unexpected pixel changes outside ornamental panels"
# Require meaningful changes in both actual panels.
for xx in (LEFT_X,W-LEFT_X-px):
    changed=int(change[TOP_Y:TOP_Y+py,xx:xx+px].sum())
    assert changed>120, ("motif not rendered",xx,changed)
targets=[
    PAGE/"gallery5-v21.png",
    ROOT/"rooms/gallery5/gallery5_palace_E_material_v21_REVIEW.png",
]
for target in targets:
    out.save(target,optimize=True)
# Cropped previews from the two actual game PNGs: no separately imagined artwork.
for label,original in (("before",PREV),("after",out)):
    detail=original.crop((43,60,153,195))
    detail.resize((440,540),Image.Resampling.NEAREST).save(PAGE/f"gallery5_panel_{label}_detail.png",optimize=True)
print("v21 authentic-gold carved laurel/cartouche motif saved",[(p.name,p.stat().st_size) for p in targets])
print("changed panel pixels",(change[TOP_Y:TOP_Y+py,LEFT_X:LEFT_X+px].sum(),change[TOP_Y:TOP_Y+py,W-LEFT_X-px:W-LEFT_X].sum()))
