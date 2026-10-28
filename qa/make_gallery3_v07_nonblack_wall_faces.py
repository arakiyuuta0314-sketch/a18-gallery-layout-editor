"""A18 Gallery3 v07: correct mistaken "white" sidewalls using the actual
NON-BLACK wall-facing material in v04. No white pillar, no wood, no green
wallpaper. Fix only the two 3D side returns; preserve all other pixels.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
import cv2

ROOT=Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
QA=ROOT/"qa/architecture-bases-20261029"
v06=Image.open(QA/"gallery3_v06_plain_white_niche_sidewalls_REVIEW.png").convert("RGB")
# v04 has BOTH nearly black shadow and original non-black warm-gray/brown
# wall-facing pixels. Use ONLY the non-black face, not the black side.
v04=Image.open(QA/"gallery3_v04_completed_side_cornices_lowered_east_passage_REVIEW.png").convert("RGB")
assert v06.size==v04.size==(930,582)
out=v06.copy()
base=np.asarray(v04,dtype=np.uint8)
# Non-black material locations checked pixel-by-pixel:
# LEFT x290..293 y57..145 RGB ~123,103,79
# RIGHT x657..660 y57..145 RGB ~114,95,73
# The dark shadow is x279..285 and x665..671: explicitly EXCLUDED.
panels=[
  {"quad":[(269,81),(295,39),(295,181),(269,263)],
   "src":(290,57,294,145),"boost":1.10},
  {"quad":[(655,39),(680,81),(680,263),(655,181)],
   "src":(657,57,661,145),"boost":1.11},
]
for side in panels:
    x1,y1,x2,y2=side["src"]
    patch=np.array(v04.crop((x1,y1,x2,y2)).convert("RGB"),dtype=np.uint8)
    # Sample luminance/texture solely from the existing beige wall. A tiny
    # exposure adjustment keeps it legible while never turning it white.
    material=np.clip(np.round(patch.astype(float)*side["boost"]),0,255).astype(np.uint8)
    material=np.asarray(Image.fromarray(material,"RGB").resize((52,190),Image.Resampling.BICUBIC))
    h,w=material.shape[:2]
    source4=np.float32([[0,0],[w-1,0],[w-1,h-1],[0,h-1]])
    H=cv2.getPerspectiveTransform(source4,np.float32(side["quad"]))
    expanded=cv2.warpPerspective(material,H,(930,582),flags=cv2.INTER_LINEAR)
    mask=cv2.warpPerspective(np.full((h,w),255,np.uint8),H,(930,582),flags=cv2.INTER_NEAREST)
    out.paste(Image.fromarray(expanded),(0,0),Image.fromarray(mask))
# Dark outlines are already present in v06; use subdued matching edge
# colors rather than white seams or a conspicuous black beam.
draw=ImageDraw.Draw(out)
draw.line([(269,81),(295,39)],fill=(75,58,43),width=2)
draw.line([(655,39),(680,81)],fill=(68,53,41),width=2)
draw.line([(269,263),(295,181)],fill=(104,79,56),width=2)
draw.line([(655,181),(680,263)],fill=(92,73,53),width=2)

a=np.asarray(v06);b=np.asarray(out)
allowed=np.zeros((582,930),dtype=bool)
allowed[38:265,267:298]=True
allowed[38:265,653:683]=True
outside=np.where(np.any(a!=b,axis=2)&~allowed)
print("outside count",len(outside[0]),"positions",list(zip(outside[1][:14],outside[0][:14])))
assert np.array_equal(a[~allowed],b[~allowed]),"Modified outside return walls"
assert np.array_equal(a[:38],b[:38]),"Convex upper contour changed"
assert np.array_equal(a[39:181,298:653],b[39:181,298:653]),"Back wall changed"
assert np.array_equal(a[265:582],b[265:582]),"Original floor/south passage changed"
assert np.array_equal(a[294:427,886:930],b[294:427,886:930]),"East corridor changed"
# The original material hue must remain taupe, NOT black, NOT pure-white.
for x,y in [(290,105),(659,105),(290,125),(658,125)]:
    r,g,bl=(int(i) for i in b[y,x])
    assert 95 <=r<=165 and 75<=g<=145 and 45<=bl<=120,(x,y,r,g,bl)
    assert r>g>bl,(x,y,r,g,bl)
    assert max(r,g,bl)<180,(x,y,r,g,bl)
name="gallery3_v07_existing_nonblack_wall_material_REVIEW.png"
out.save(QA/name)
cmp=Image.new("RGB",(1860,624),"#202326")
cmp.paste(v06,(0,42));cmp.paste(out,(930,42))
dd=ImageDraw.Draw(cmp);dd.rectangle((0,0,1859,41),fill="#292b2c")
dd.text((12,14),"v06 | TOO WHITE (PILLAR COLOR)",fill="white")
dd.text((942,14),"v07 | ORIGINAL NON-BLACK WALL MATERIAL",fill="white")
cmp.save(QA/"gallery3_v06_v07_actual_wall_material_COMPARISON.png")
detail=Image.new("RGB",(1400,435),"#23272b")
for i,(label,img) in enumerate([("v06: white mistake",v06),("v07: actual wall",out)]):
    fragment=img.crop((218,29,736,255)).resize((690,302),Image.Resampling.LANCZOS)
    detail.paste(fragment,(i*700+5,65))
    ImageDraw.Draw(detail).text((i*700+12,25),label,fill="white")
detail.save(QA/"gallery3_v07_niche_material_closeup_COMPARISON.png")
print("PASS: used ONLY beige face of v04, not black side or white pillar")
print("Changed pixels",int(np.any(a!=b,axis=2).sum()),"output",name)
