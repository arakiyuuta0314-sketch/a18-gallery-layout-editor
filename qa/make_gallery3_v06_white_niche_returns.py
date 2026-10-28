"""A18 gallery3 v06 review: replace ONLY niche's green/wood returns
with plain warm-white wall surfaces matching the light pillar material.
Base: v05. Preserve accepted convex footprint and every room/portal pixel.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np
import cv2

ROOT=Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
QA=ROOT/"qa/architecture-bases-20261029"
v05=Image.open(QA/"gallery3_v05_green_sidewalls_no_brown_wedges_REVIEW.png").convert("RGB")
g1=Image.open(QA/"gallery1_v13_B_right_passage_top_lowered_24px_REVIEW.png").convert("RGB")
assert v05.size==g1.size==(930,582)
out=v05.copy()
# White/cream from the *real white pillar face*, avoiding its dark wood
# moldings. Normalize its warm tint toward a lighter, neutral ivory plaster;
# keep source's subtle luminance variation, unlike a solid color polygon.
face=np.asarray(g1.crop((457,62,471,155)).resize((52,190),Image.Resampling.BICUBIC),dtype=np.float32)
brightness=face.mean(axis=2)
median=float(np.median(brightness))
# Neutral ivory plaster reference. Slightly different illumination per side:
# left catches more light; right reads shaded. No decorative green/wainscot.
walls=[
    ([(269,81),(295,39),(295,181),(269,263)],(232,227,217),0.96),
    ([(655,39),(680,81),(680,263),(655,181)],(217,213,205),0.93),
]
for quad,target,atten in walls:
    h,w=face.shape[:2]
    tex=np.empty((h,w,3),dtype=np.uint8)
    # Restore original pillar's microtone without preserving its strong
    # yellow coloration or wooden surrounds.
    variation=np.clip((brightness-median)*0.16,-7,7)
    for k in range(3):
        tex[:,:,k]=np.clip(np.round(target[k]*atten + variation),0,255).astype(np.uint8)
    source4=np.float32([[0,0],[w-1,0],[w-1,h-1],[0,h-1]])
    hom=cv2.getPerspectiveTransform(source4,np.float32(quad))
    mapped=cv2.warpPerspective(tex,hom,(930,582),flags=cv2.INTER_LINEAR)
    mask=cv2.warpPerspective(np.full((h,w),255,np.uint8),hom,(930,582),flags=cv2.INTER_NEAREST)
    out.paste(Image.fromarray(mapped),(0,0),Image.fromarray(mask))
# Keep only restrained architectural seams, not dark wood trim.
draw=ImageDraw.Draw(out)
draw.line([(269,81),(295,39)],fill=(89,77,66),width=2)
draw.line([(655,39),(680,81)],fill=(81,72,63),width=2)
draw.line([(269,263),(295,181)],fill=(138,125,111),width=2)
draw.line([(655,181),(680,263)],fill=(127,117,104),width=2)

original=np.asarray(v05)
revised=np.asarray(out)
changed=np.any(original!=revised,axis=2)
allowed=np.zeros((582,930),dtype=bool)
allowed[38:265,267:298]=True
allowed[38:265,653:683]=True
assert np.array_equal(original[~allowed],revised[~allowed]),"Unexpected change outside niche sidewall returns"
assert np.array_equal(original[:38],revised[:38]),"Convex upper edge changed"
assert np.array_equal(original[39:181,298:653],revised[39:181,298:653]),"Rear niche wall changed"
assert np.array_equal(original[265:],revised[265:]),"Main floor/entrance changed"
assert np.array_equal(original[294:427,886:930],revised[294:427,886:930]),"East passage changed"
for x,y in [(289,116),(661,116),(287,150),(662,150)]:
    pix=revised[y,x]
    assert min(map(int,pix))>=165, ("White plaster became too dark",x,y,pix)
    assert max(map(int,pix))-min(map(int,pix))<=45, ("Side too saturated",x,y,pix)
assert changed.sum()>1000
name="gallery3_v06_plain_white_niche_sidewalls_REVIEW.png"
out.save(QA/name)
compare=Image.new("RGB",(1860,624),"#222629")
compare.paste(v05,(0,42));compare.paste(out,(930,42))
c=ImageDraw.Draw(compare)
c.rectangle((0,0,1859,41),fill="#2a2c2f")
c.text((16,14),"v05 | GREEN WALLPAPER + WOOD SIDE WALLS",fill="white")
c.text((946,14),"v06 | PLAIN WARM-WHITE SIDE WALLS",fill="white")
compare.save(QA/"gallery3_v05_v06_white_sidewalls_COMPARISON.png")
detail=Image.new("RGB",(1400,435),"#25282a")
for i,(label,img) in enumerate([("v05: patterned",v05),("v06: white plaster",out)]):
    crop=img.crop((218,29,736,255)).resize((690,302),Image.Resampling.LANCZOS)
    detail.paste(crop,(i*700+5,65))
    ImageDraw.Draw(detail).text((i*700+12,25),label,fill="white")
detail.save(QA/"gallery3_v06_sidewalls_closeup_COMPARISON.png")
print("PASS v06 WHITE SIDES",name,"changed pixels",int(changed.sum()))
