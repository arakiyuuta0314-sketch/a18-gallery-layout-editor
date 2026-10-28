"""A18 gallery 2: review-only architectural black surround matching gallery1 v13.
No new generated art. Use ONLY existing, approved gallery2 architecture and pixels.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
ROOT = Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
QA = ROOT / "qa/architecture-bases-20261029"
SRC = ROOT / "rooms/gallery2/architecture_only_v01.png"
original = Image.open(SRC).convert("RGB")
assert original.size == (930,582)
a = np.asarray(original)
result = a.copy()

# Remove the legacy diagonal left-side spur from the floor, which otherwise
# protrudes from the new straight edge. All repair pixels are taken from the
# SAME original tiled floor at mirrored local coordinates; do not redraw floor.
# Source area x=68..136 is open, uninterrupted original floor.
for y in range(268,490):
    af = min(1.0, (y-268)/9.0, (490-y)/10.0)
    for x in range(68):
        xf = min(1.0,(68-x)/7.0)
        alpha = max(0.0, min(1.0, af*xf))
        if alpha:
            c = a[y,136-x].astype(float)
            result[y,x] = np.rint(result[y,x].astype(float)*(1-alpha) + c*alpha).astype(np.uint8)
out = Image.fromarray(result,"RGB")
# Place original corner columns INWARD so exterior black side frame does not
# erase them. No column re-design or perspective edits.
out.paste(original.crop((11,39,39,220)),(44,39))
out.paste(original.crop((872,39,900,220)),(858,39))

# Same straight perimeter geometry as gallery1 v13, mirrored entrance:
# gallery2 left entrance from the main hall at x=0..43, y=244..348.
black=(5,6,7)
draw = ImageDraw.Draw(out)
draw.rectangle((0,0,929,15),fill=black)
draw.rectangle((0,0,43,243),fill=black)  # west above passage
draw.rectangle((0,349,43,581),fill=black) # west below passage
draw.rectangle((886,0,929,581),fill=black) # east is fully closed
draw.rectangle((0,566,929,581),fill=black) # south border from approved B
b=np.asarray(out)
assert out.size==(930,582)
allowed=np.zeros((582,930),dtype=bool)
allowed[0:16,:]=True
allowed[0:244,0:44]=True
allowed[349:,0:44]=True
allowed[:,886:]=True
allowed[566:,:]=True
allowed[268:490,0:68]=True
allowed[39:220,44:72]=True
allowed[39:220,858:886]=True
assert np.array_equal(a[~allowed],b[~allowed]),"Unexpected change outside perimeter/pillars/old floor spur"
assert np.all(b[:16,:,:] == black),"Top border"
assert np.all(b[566:,:,:]==black),"Bottom border"
assert np.all(b[200:244,8,:]==black),"Upper west wall"
assert np.all(b[349:565,8,:]==black),"Lower west wall"
assert np.all(b[15:566,920,:]==black),"East wall"
assert not np.any(np.all(b[244:349,8,:]==black,axis=1)),"West corridor unexpectedly closed"
assert np.array_equal(a[39:220,11:39],b[39:220,44:72]),"Left corner pillar must be existing art"
assert np.array_equal(a[39:220,872:900],b[39:220,858:886]),"Right corner pillar must be existing art"
# North arch and all approved-display-wall locations stay completely unchanged.
assert np.array_equal(a[39:220,665:805],b[39:220,665:805]),"North arch modified"
assert np.array_equal(a[310:560,100:850],b[310:560,100:850]),"Central floor changed"
f=QA/"gallery2_v02_black_frame_left_upper_entrance_REVIEW.png"
out.save(f)
comparison=Image.new("RGB",(1860,625),"#252525")
comparison.paste(original,(0,43));comparison.paste(out,(930,43))
d=ImageDraw.Draw(comparison)
d.rectangle((0,0,1859,42),fill="#282b2d")
d.text((12,14),"GALLERY 2 / APPROVED ARCHITECTURE - NO REAR FRAMES",fill="white")
d.text((942,14),"GALLERY 2 / BLACK FRAME + UPPER LEFT ENTRANCE - REVIEW",fill="white")
compare=QA/"gallery2_v01_vs_v02_black_frame_comparison_REVIEW.png"
comparison.save(compare)
print("PASS gallery2 black perimeter / existing pillars / north arch unchanged / west upper corridor open")
print("OUTPUT",f,"COMPARISON",compare)
