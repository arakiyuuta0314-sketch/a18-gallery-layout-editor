"""Gallery1 v11 / straight black bounding walls + upper east entrance.
Only a QA preview; original v04, existing door and floor material reused.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

ROOT=Path(r"C:/Users/User/source/repos/a18-gallery-layout-editor")
QA=ROOT/"qa/architecture-bases-20261029"
v04=Image.open(QA/"gallery1_architecture_no_frames_v04_REVIEW.png").convert("RGB")
closed=Image.open(QA/"gallery1_architecture_closed_door_sidewalls_v05_REVIEW.png").convert("RGB")
floor_reference=Image.open(QA/"gallery1_architecture_v06_no_green_sidewalls_REVIEW.png").convert("RGB")
assert v04.size==closed.size==floor_reference.size==(930,582)
image=v04.copy()
# Copy the existing wooden north door; do not regenerate other architecture.
image.paste(closed.crop((318,85,390,208)),(318,85))

# East, upper opening is the FLOOR, not green side-wall texture.
# Inpaint the old v04 green region from existing floor-only v06 (x<=916).
# A 14-pixel rightmost section is extended from verified floor pixels.
for y in range(220,315):
    for x in range(875,930):
        # Use the clean floor band at x891..912, avoiding both v06
        # rightmost wood and the obsolete inset seam near x884.
        floor_x=891+round(max(0,x-885)*21/44)
        target=floor_reference.getpixel((floor_x,y))
        original=image.getpixel((x,y))
        blend=min(1.0,max(0.0,(x-875)/10))
        color=tuple(round(original[k]*(1-blend)+target[k]*blend) for k in range(3))
        image.putpixel((x,y),color)

d=ImageDraw.Draw(image)
BLACK=(5,6,7)
# Outer boundary uses only true horizontal/vertical rectangles.
# West: fully closed. North: straight frame. East: wall above/below upper passage.
d.rectangle((0,0,929,15),fill=BLACK)
d.rectangle((0,0,43,581),fill=BLACK)
d.rectangle((886,0,929,219),fill=BLACK)
d.rectangle((886,349,929,581),fill=BLACK)
# Nothing else: no slanted planes, no little black detached blocks, no carpet.

before=np.asarray(v04)
after=np.asarray(image)
allowed=np.zeros((582,930),dtype=bool)
allowed[:16,:]=True
allowed[:,:44]=True
allowed[:220,886:]=True
allowed[349:,886:]=True
allowed[220:315,875:]=True
allowed[315:349,886:]=True
allowed[85:208,318:390]=True
assert np.array_equal(before[~allowed],after[~allowed]),"unexpected modification outside frame, door and corridor"
assert np.all(after[:,20,:]==np.array(BLACK)),"left border is not rectangular"
assert np.all(after[2,100:880,:]==np.array(BLACK)),"top border is not rectangular"
assert np.all(after[300,900,:]!=np.array(BLACK)),"upper east corridor blocked"
assert np.all(after[450,900,:]==np.array(BLACK)),"lower east wall absent"
assert np.all(after[180,900,:]==np.array(BLACK)),"upper east wall absent"
assert np.array_equal(before[350:,44:884],after[350:,44:884]),"floor outside outer walls changed"

output=QA/"gallery1_v11_rectangular_black_frame_upper_right_entrance_REVIEW.png"
image.save(output)
v10=Image.open(QA/"gallery1_v10_black_outer_frame_entrance_aligned_REVIEW.png").convert("RGB")
comparison=Image.new("RGB",(1860,622),color="#eeeae3")
comparison.paste(v10,(0,40))
comparison.paste(image,(930,40))
dd=ImageDraw.Draw(comparison)
dd.rectangle((0,0,1859,39),fill="#282828")
dd.text((18,13),"v10 / IRREGULAR BLACK EDGE, ENTRANCE TOO LOW",fill="white")
dd.text((948,13),"v11 / RECTANGULAR BLACK FRAME, ENTRANCE UPPER RIGHT",fill="white")
comparison_output=QA/"gallery1_v10_vs_v11_rectangular_comparison_REVIEW.png"
comparison.save(comparison_output)
print("PASS",output.name,comparison_output.name,"modified pixels:",int(np.any(before!=after,axis=2).sum()))
