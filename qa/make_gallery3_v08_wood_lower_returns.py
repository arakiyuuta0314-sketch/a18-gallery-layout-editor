"""A18 Gallery3 v08. User requested real wood wainscot on the LOWER
part of both recessed sidewalls, while keeping the 3-D pillar/return.
Base v07; only the two return polygons may change.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance
import numpy as np
import cv2

ROOT=Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
QA=ROOT/"qa/architecture-bases-20261029"
v07=Image.open(QA/"gallery3_v07_existing_nonblack_wall_material_REVIEW.png").convert("RGB")
G2=Image.open(QA/"gallery2_v04_architecture_matching_entrance_gallery1_REVIEW.png").convert("RGB")
G1=Image.open(QA/"gallery1_v13_B_right_passage_top_lowered_24px_REVIEW.png").convert("RGB")
assert v07.size==G2.size==G1.size==(930,582)
out=v07.copy()

# Real, already accepted decorative wainscot from a clean central bay.
# Its last 53 source rows are used as the lower portion of the returns.
# This maps to the front-side wainscot start y~210 and rear start y~140,
# matching the near and far wall's actual panels in this perspective.
wood=G2.crop((116,166,215,219)).resize((100,53),Image.Resampling.LANCZOS)
src=np.asarray(wood)
print("wood RGB median",np.median(src.reshape(-1,3),axis=0).round(1).tolist())
# Crop is strictly inside existing framed wall, not a synthesized texture.
assert wood.size==(100,53)
srect=np.float32([[0,0],[99,0],[99,52],[0,52]])
# Quadrilateral order maps near/front to x269 and far/back to x295
# without reversing the known visible wood trim perspective.
sides=[
 {"quad":[(269,211),(295,140),(295,181),(269,263)],"dim":.91,
  "top":[(269,211),(295,140)],"foot":[(269,263),(295,181)]},
 {"quad":[(655,140),(680,211),(680,263),(655,181)],"dim":.81,
  "top":[(655,140),(680,211)],"foot":[(655,181),(680,263)]},
]
for side in sides:
    data=np.uint8(np.clip(src.astype(float)*side["dim"],0,255))
    H=cv2.getPerspectiveTransform(srect,np.float32(side["quad"]))
    rgb=cv2.warpPerspective(data,H,(930,582),flags=cv2.INTER_LINEAR)
    mask=cv2.warpPerspective(np.full((53,100),255,np.uint8),H,(930,582),
                              flags=cv2.INTER_NEAREST)
    out.paste(Image.fromarray(rgb),(0,0),Image.fromarray(mask))

# Narrow volume faces on the pillars where front wall turns into recess.
# Original column's dark wood side face is sampled, not bright cream face.
# These chamfers make the existing front column edges read as 3-D.
def warp_pillar_edge(crop,points,exposure):
    ar=np.asarray(crop.convert("RGB"))
    h,w=ar.shape[:2]
    base=np.float32([[0,0],[w-1,0],[w-1,h-1],[0,h-1]])
    H=cv2.getPerspectiveTransform(base,np.float32(points))
    mapped=cv2.warpPerspective(np.uint8(np.clip(ar.astype(float)*exposure,0,255)),
                                  H,(930,582),flags=cv2.INTER_LINEAR)
    mask=cv2.warpPerspective(np.full((h,w),255,np.uint8),H,(930,582),
                            flags=cv2.INTER_NEAREST)
    out.paste(Image.fromarray(mapped),(0,0),Image.fromarray(mask))
# Use carved brown side-molding from the actual column asset.
edge=G1.crop((478,39,483,220))
warp_pillar_edge(edge,[(269,81),(274,78),(274,258),(269,263)],.89)
warp_pillar_edge(edge.transpose(Image.Transpose.FLIP_LEFT_RIGHT),
                 [(675,78),(680,81),(680,263),(675,258)],.81)
draw=ImageDraw.Draw(out)
# The wood top rail and baseboard follow the actual depth lines.
draw.line([(270,210),(295,139)],fill=(137,90,51),width=2)
draw.line([(655,139),(680,210)],fill=(125,82,48),width=2)
draw.line([(270,261),(295,181)],fill=(87,52,29),width=2)
draw.line([(655,181),(680,261)],fill=(81,48,27),width=2)
# Keep a narrow pillar edge highlight, not an independent floating pillar.
draw.line([(274,79),(274,258)],fill=(116,72,38),width=1)
draw.line([(675,79),(675,258)],fill=(99,62,37),width=1)

orig=np.asarray(v07)
new=np.asarray(out)
allowed=np.zeros((582,930),dtype=bool)
allowed[38:265,267:298]=True
allowed[38:265,653:683]=True
assert np.array_equal(orig[~allowed],new[~allowed]),"Change outside left/right side returns"
assert np.array_equal(orig[:38],new[:38]),"Convex roof changed"
assert np.array_equal(orig[39:139,278:289],new[39:139,278:289]),"Left upper wall unexpectedly changed"
assert np.array_equal(orig[39:139,660:672],new[39:139,660:672]),"Right upper wall unexpectedly changed"
assert np.array_equal(orig[39:181,298:653],new[39:181,298:653]),"Rear wall changed"
assert np.array_equal(orig[265:],new[265:]),"Floor/south passage changed"
assert np.array_equal(orig[294:427,886:930],new[294:427,886:930]),"East passage changed"
assert np.array_equal(orig[81:210,60:235],new[81:210,60:235]),"Left front wall changed"
assert np.array_equal(orig[81:210,713:855],new[81:210,713:855]),"Right front wall changed"
# Upper beige material stays muted. Lower is now genuine wood with panels.
for x,y in [(289,105),(661,105)]:
    assert int(new[y,x,0])<170 and int(new[y,x,0])>int(new[y,x,1])>int(new[y,x,2])
for x,y in [(281,237),(669,237)]:
    pix=new[y,x]
    assert 38 < int(pix[0]) < 220 and int(pix[0])>=int(pix[1]),(x,y,pix)
changed=int(np.any(orig!=new,axis=2).sum())
assert changed>2500
f=QA/"gallery3_v08_wood_lower_returns_3d_columns_REVIEW.png"
out.save(f)
compare=Image.new("RGB",(1860,624),"#1d2325")
compare.paste(v07,(0,42));compare.paste(out,(930,42))
cd=ImageDraw.Draw(compare);cd.rectangle((0,0,1859,41),fill="#26292a")
cd.text((12,13),"v07 / NON-BLACK WALL MATERIAL, LOWER SIDE IS FLAT",fill="white")
cd.text((942,13),"v08 / MATCHING WOOD WAINSCOT + 3-D COLUMN EDGE",fill="white")
compare.save(QA/"gallery3_v07_v08_wood_lower_returns_COMPARISON.png")
detail=Image.new("RGB",(1400,435),"#272a2b")
for i,(label,img) in enumerate([("v07: flat side",v07),("v08: wood and 3D column",out)]):
    patch=img.crop((218,29,736,255)).resize((690,302),Image.Resampling.LANCZOS)
    detail.paste(patch,(i*700+5,65))
    ImageDraw.Draw(detail).text((i*700+12,25),label,fill="white")
detail.save(QA/"gallery3_v08_wood_sidewalls_detail_COMPARISON.png")
print("PASS: only two sidewall return areas changed, pixels=",changed)
