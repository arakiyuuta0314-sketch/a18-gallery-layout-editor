"""A18 gallery3 v05 review: replace unnatural niche side returns with real
green wallpaper and proportionate wooden wainscoting from gallery2's
existing approved-quality image. All geometry stays exactly v04.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageEnhance
import numpy as np
import cv2

ROOT=Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
QA=ROOT/"qa/architecture-bases-20261029"
v04=Image.open(QA/"gallery3_v04_completed_side_cornices_lowered_east_passage_REVIEW.png").convert("RGB")
gallery2=Image.open(QA/"gallery2_v04_architecture_matching_entrance_gallery1_REVIEW.png").convert("RGB")
assert v04.size==gallery2.size==(930,582)
out=v04.copy()
# Replace the old oversized solid-brown triangles beneath the side walls
# using tiles from the adjoining *same approved v04 floor*.
# These regions were brown wedges that extended BELOW the side wall geometry.
old_wedges=[
    ([(269,219),(295,181),(295,223),(269,263)],305),
    ([(655,181),(680,219),(680,263),(655,223)],645),
]
pixels=np.asarray(out).copy()
baseline=np.asarray(v04)
for corners,floor_x in old_wedges:
    mask=np.zeros((582,930),dtype=np.uint8)
    cv2.fillPoly(mask,[np.asarray(corners,np.int32)],255)
    ys,xs=np.where(mask>0)
    pixels[ys,xs]=baseline[ys,floor_x]
out=Image.fromarray(pixels,"RGB")

# Side walls should contain the SAME green wallpaper and wooden lower
# panel as the front/rear walls, perspective compressed, not blank concrete.
# The wall panel x105-161 in gallery2 has no pillar.
source=gallery2.crop((106,39,161,220))
src=np.asarray(source)
h,w=src.shape[:2]
source_quad=np.float32([[0,0],[w-1,0],[w-1,h-1],[0,h-1]])
returns=[
    ([(269,81),(295,39),(295,181),(269,263)],0.78),
    ([(655,39),(680,81),(680,263),(655,181)],0.72),
]
for quad,level in returns:
    wall=ImageEnhance.Brightness(source).enhance(level)
    m=cv2.getPerspectiveTransform(source_quad,np.float32(quad))
    rgb=cv2.warpPerspective(np.asarray(wall),m,(930,582),flags=cv2.INTER_LINEAR)
    alpha=cv2.warpPerspective(np.full((h,w),255,np.uint8),m,(930,582),flags=cv2.INTER_NEAREST)
    out.paste(Image.fromarray(rgb),(0,0),Image.fromarray(alpha))
# Defined edges and very thin dark base seams: correct perspective, but
# do NOT cover the wainscot with large solid-brown triangles again.
draw=ImageDraw.Draw(out)
draw.line([(269,81),(295,39)],fill=(57,37,23),width=2)
draw.line([(655,39),(680,81)],fill=(57,37,23),width=2)
draw.line([(269,263),(295,181)],fill=(111,68,39),width=2)
draw.line([(655,181),(680,263)],fill=(111,68,39),width=2)
# Lower side edges have natural thin baseboard; preserved wall geometry.
before=np.asarray(v04)
after=np.asarray(out)
allowed=np.zeros((582,930),dtype=bool)
allowed[38:265,267:298]=True
allowed[38:265,653:683]=True
assert np.array_equal(before[~allowed],after[~allowed]),"Unexpected changes outside exact left/right niche side returns"
assert np.array_equal(before[0:38],after[0:38]),"Convex black top/cornice modified"
assert np.array_equal(before[39:181,298:653],after[39:181,298:653]),"Recessed BACK WALL changed"
assert np.array_equal(before[300:566],after[300:566]),"Main room floor changed"
assert np.array_equal(before[566:582],after[566:582]),"South entry changed"
assert np.array_equal(before[294:427,886:930],after[294:427,886:930]),"East passage changed"
# Color check: both sides should actually have green in the wall-paper zone
for x,y in [(279,105),(672,105)]:
    r,g,b=after[y,x]
    assert g>r and g>b,"Sidewall has no green wallpaper"
# Within lower sides: significant wooden-brown pixels
for x,y in [(278,203),(672,203)]:
    r,g,b=after[y,x]
    assert r>g and g>b,"Sidewall has no wood wainscot"
name="gallery3_v05_green_sidewalls_no_brown_wedges_REVIEW.png"
out.save(QA/name)
cmp=Image.new("RGB",(1860,624),"#24272a")
cmp.paste(v04,(0,42));cmp.paste(out,(930,42))
d=ImageDraw.Draw(cmp)
d.rectangle((0,0,1859,41),fill="#292b2d")
d.text((10,13),"v04 / Unnatural flat returns + giant brown wedges",fill="white")
d.text((940,13),"v05 / Actual green wall + wood wainscot on niche sides",fill="white")
cmp.save(QA/"gallery3_v04_v05_niche_sidewalls_COMPARISON.png")
# Detail crop as separate QA review asset.
detail=Image.new("RGB",(1400,560),"#25272a")
for i,(label,img) in enumerate((("v04 previous",v04),("v05 revised",out))):
    cropped=img.crop((202,30,749,275))
    cropped=cropped.resize((700,314),Image.Resampling.LANCZOS)
    detail.paste(cropped,(700*i,86))
    ImageDraw.Draw(detail).text((700*i+15,42),label,fill="white")
detail.save(QA/"gallery3_v05_niche_side_detail_COMPARISON.png")
print("PASS v05",name)
print("Diff pixels",int(np.any(before!=after,axis=2).sum()))
