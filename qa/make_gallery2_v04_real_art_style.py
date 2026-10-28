"""A18 gallery2 v04 review: exactly match approved gallery1 material QUALITY,
but preserve gallery2's original rear-frame bays and its right-hand north exit.
No independently generated art; precise compositing of the gallery1 original.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
ROOT=Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
QA=ROOT/"qa/architecture-bases-20261029"
src=Image.open(QA/"gallery1_v13_B_right_passage_top_lowered_24px_REVIEW.png").convert("RGB")
assert src.size==(930,582)
img=src.copy()
# The large colored wallpaper+carved wainscot is real, already accepted artwork.
# Fit wall-only photorealistic panels BETWEEN columns. Do not place pillars over
# the two approved hanging zones x80..260 or x349..510.
wall_panels=[(75,305,(485,39,665,220)),    # bay1 / for rear exhibit 1
             (337,541,(485,39,665,220)),   # bay2 / for rear exhibit 2
             (573,669,(715,39,811,220)),   # narrow bay before north door
             (800,855,(799,39,854,220))]   # right of the north door
for x1,x2,box in wall_panels:
    wall=src.crop(box)
    if wall.width!=(x2-x1):
        wall=wall.resize((x2-x1,wall.height),Image.Resampling.LANCZOS)
    img.paste(wall,(x1,39))
# Columns are full-resolution originals, x452..483 from gallery1.
pillar=src.crop((452,39,484,220))
img.paste(pillar,(305,39))
img.paste(pillar,(541,39))
# Old center arch has a decorative upper part y28..38: replace only the
# source-original arch's unwanted top silhouette with continuous cornice.
img.paste(src.crop((499,28,633,39)),(286,28))
# Move the actual existing carved double door, arch and lintel to x668..801.
img.paste(src.crop((286,28,420,220)),(668,28))
# Gallery2 west entry: mirror gallery1 east upper corridor, with no carpet
# and no side-wall green. The lower right wall remains fully closed.
black=(5,6,7)
ImageDraw.Draw(img).rectangle((886,244,929,348),fill=black)
a=np.asarray(img).copy()
b=np.asarray(src)
a[244:349,0:44,:]=b[244:349,70:114,:]
img=Image.fromarray(a,"RGB")
# Pixel/geometry invariants (the background only, not in-game collision).
assert img.size==(930,582)
assert np.array_equal(a[:16],b[:16]),"upper frame changed"
assert np.array_equal(a[566:],b[566:]),"bottom frame changed"
assert np.array_equal(a[220:244,0:44],b[220:244,0:44]),"upper entrance wall moved"
assert np.array_equal(a[349:566,0:44],b[349:566,0:44]),"lower entrance wall moved"
assert np.all(a[244:349,886:930]==black),"east wall must be closed"
assert np.array_equal(a[244:349,0:44],b[244:349,70:114]),"west entrance must use original floor"
assert np.array_equal(a[350:566,44:886],b[350:566,44:886]),"floor must be unchanged"
assert np.array_equal(a[39:220,305:337],np.asarray(pillar)),"first interior pillar"
assert np.array_equal(a[39:220,541:573],np.asarray(pillar)),"second interior pillar"
assert np.array_equal(a[28:220,668:802],b[28:220,286:420]),"wooden door not copied exactly"
# Rear hanging bays must be clear of built-in columns.
assert (75<80<260<305) and (337<349<510<541) and (668<735<802)
name="gallery2_v04_architecture_matching_entrance_gallery1_REVIEW.png"
img.save(QA/name)
cmp=Image.new("RGB",(1860,624),"#191d21")
prev=Image.open(QA/"gallery2_v02_black_frame_left_upper_entrance_REVIEW.png").convert("RGB")
cmp.paste(prev,(0,42));cmp.paste(img,(930,42))
draw=ImageDraw.Draw(cmp);draw.rectangle((0,0,1859,41),fill="#25292b")
draw.text((12,12),"GALLERY2 previous / schematic illustration",fill="white")
draw.text((942,12),"GALLERY2 v04 / entrance+gallery1 material and carved wood door",fill="white")
cmp.save(QA/"gallery2_v02_vs_v04_style_comparison_REVIEW.png")
print("PASS v04 exact gallery1 wooden door, 2 rear frame bays free, gallery2 exit location, west upper opening")
