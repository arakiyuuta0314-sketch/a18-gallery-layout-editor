from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops
ROOT=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
PAGE=ROOT/"architecture-review/entrance-gallery5-comparison"
source=Image.open(PAGE/"gallery5-v21.png").convert("RGB")
raw=np.array(source)
out=raw.copy()
# The only permitted edits are the two existing numerical markers.
# Preserve all foliage, architecture, gold frame carving, art openings, and right #3.
regions=[
    {"old":"1","new":"2","roi":(245,210,276,260),"size":28},
    {"old":"2","new":"1","roi":(445,203,489,253),"size":33},
]
for item in regions:
    x0,y0,x1,y1=item["roi"]
    crop=out[y0:y1,x0:x1].copy()
    # Real lettering is the only pale region within these restricted teal windows.
    pale=(crop[:,:,0]>155)&(crop[:,:,1]>150)&(crop[:,:,2]>135)
    yv,xv=np.where(pale)
    assert 20<len(xv)<600,(item,len(xv))
    minx,maxx=int(xv.min()),int(xv.max())
    miny,maxy=int(yv.min()),int(yv.max())
    mask=np.uint8(pale)*255
    mask=cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
    cleared=cv2.inpaint(crop,mask,4,cv2.INPAINT_TELEA)
    # Draw the replacement in the identical center of the source letter.
    c=(minx+maxx)/2,(miny+maxy)/2
    art=Image.fromarray(cleared)
    layer=Image.new("RGBA",art.size,(0,0,0,0))
    draw=ImageDraw.Draw(layer)
    font=ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf",item["size"])
    bbox=draw.textbbox((0,0),item["new"],font=font)
    cx,cy=c
    tx=cx-(bbox[0]+bbox[2])/2
    ty=cy-(bbox[1]+bbox[3])/2
    draw.text((tx,ty),item["new"],font=font,fill=(233,220,192,255),stroke_width=0)
    art=Image.alpha_composite(art.convert("RGBA"),layer).convert("RGB")
    out[y0:y1,x0:x1]=np.array(art)
    print(f"{item['old']}->{item['new']}: original glyph box {(x0+minx,y0+miny,x0+maxx,y0+maxy)}")
result=Image.fromarray(out,"RGB")
diff=np.any(np.asarray(source)!=out,axis=2)
allowed=np.zeros((582,930),dtype=bool)
for item in regions:
    x0,y0,x1,y1=item["roi"]
    allowed[y0:y1,x0:x1]=True
assert diff.any() and not (diff&~allowed).any()
assert (source.crop((625,180,730,298)).tobytes()==result.crop((625,180,730,298)).tobytes())
for p in (PAGE/"gallery5-v22.png",ROOT/"rooms/gallery5/gallery5_palace_E_material_v22_REVIEW.png"):
    result.save(p,optimize=True)
print("v22 numbers L2 C1 R3; changed pixels",diff.sum())
