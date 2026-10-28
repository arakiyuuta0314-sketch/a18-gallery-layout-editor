"""A18 gallery 3 v04 review. ONLY two requested changes from approved-shape v03.
1. Complete the cropped top of each lower front wing with *actual* wood cornice
   pixels from the accepted gallery1 image, aligned to the front columns.
2. Lower the east floor passage from y264..396 to y294..426 (+30 px),
   avoiding level alignment with the side-wing bottom y262.
Does not alter the room shape, niche, staff, frame positions or game.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np

ROOT=Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
QA=ROOT/"qa/architecture-bases-20261029"
v03=Image.open(QA/"gallery3_v03_convex_black_outline_open_east_REVIEW.png").convert("RGB")
source=Image.open(QA/"gallery1_v13_B_right_passage_top_lowered_24px_REVIEW.png").convert("RGB")
assert v03.size==source.size==(930,582)
im=v03.copy()
BLACK=(5,6,7)
# The front wings' picture starts at y=81 with columns and wood wainscot.
# In gallery1 original, the *existing* top cornice runs y=16..38,
# and its columns start y=39. Therefore y=58..80 on the front
# wings is exactly where its cornice belongs, immediately above columns y=81.
for left,right in [(44,270),(680,886)]:
    cornice=source.crop((left,16,right,39))
    assert cornice.size==(right-left,23)
    im.paste(cornice,(left,58))

# The old east opening started immediately after the front wing's base
# at y=262 (opening y264). Move the entire opening 30 pixels down:
# 30 pixels of upper wall fill; same floor tile at its new lower end.
old_top,old_bottom=264,397
new_top,new_bottom=294,427
assert new_top-old_top==new_bottom-old_bottom==30
assert new_top-262==32
draw=ImageDraw.Draw(im)
draw.rectangle((886,old_top,929,new_top-1),fill=BLACK)
# Use the exact same-row real tile floor that existing v03 uses.
for yy in range(old_bottom,new_bottom):
    im.paste(source.crop((842,yy,886,yy+1)),(886,yy))

a=np.asarray(v03)
b=np.asarray(im)
s=np.asarray(source)
allowed=np.zeros((582,930),dtype=bool)
for l,r in [(44,270),(680,886)]:
    allowed[58:81,l:r]=True
allowed[old_top:new_top,886:930]=True
allowed[old_bottom:new_bottom,886:930]=True
assert np.array_equal(a[~allowed],b[~allowed]), "Changes leaked outside two cornices and east passage"
for l,r in [(44,270),(680,886)]:
    assert np.array_equal(b[58:81,l:r],s[16:39,l:r]),"Original cornice is not an exact pixel copy"
    assert np.array_equal(b[81:220,l:r],a[81:220,l:r]),"Wall body unexpectedly modified"
assert np.all(b[old_top:new_top,886:930]==BLACK),"Upper wall above the moved opening is missing"
assert np.array_equal(b[new_top:new_bottom,886:930],s[new_top:new_bottom,842:886]), "Open east corridor floor changed"
assert np.all(b[new_bottom:565,886:930]==BLACK),"Wall below opening missing"
assert np.array_equal(b[0:58,:,:],a[0:58,:,:]),"Convex upper roof changed"
assert np.array_equal(b[220:566,55:850,:],a[220:566,55:850,:]),"Interior floor/alcove footprint changed"
assert np.array_equal(b[566:582],a[566:582]),"South central entrance changed"
assert np.array_equal(b[39:181,295:655],a[39:181,295:655]),"Recessed back wall changed"
assert np.array_equal(b[39:181,270:295],a[39:181,270:295]),"Left recess side changed"
assert np.array_equal(b[39:181,655:680],a[39:181,655:680]),"Right recess side changed"
f=QA/"gallery3_v04_completed_side_cornices_lowered_east_passage_REVIEW.png"
im.save(f)
cmp=Image.new("RGB",(1860,624),"#212325")
cmp.paste(v03,(0,42));cmp.paste(im,(930,42))
cd=ImageDraw.Draw(cmp)
cd.rectangle((0,0,1859,41),fill="#272a2b")
cd.text((12,14),"v03 / CROPPED WALL TOP, EQUAL-HEIGHT EXIT",fill="white")
cd.text((942,14),"v04 / WOOD CORNICES RESTORED, EXIT LOWERED 30px",fill="white")
comparison=QA/"gallery3_v03_vs_v04_cornice_east_passage_COMPARISON.png"
cmp.save(comparison)
print("PASS v04",f.name,comparison.name)
print("PASS changed pixel regions:",int(np.any(a!=b,axis=2).sum()))
print("Cornices x44-269 and x680-885 at y58-80; right opening now y294..426")
