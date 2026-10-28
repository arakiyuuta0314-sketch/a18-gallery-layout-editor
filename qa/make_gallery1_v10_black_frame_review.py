from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

root = Path(r"C:/Users/User/source/repos/a18-gallery-layout-editor")
qa = root / "qa/architecture-bases-20261029"
base = Image.open(qa / "gallery1_architecture_no_frames_v04_REVIEW.png").convert("RGB")
v05 = Image.open(qa / "gallery1_architecture_closed_door_sidewalls_v05_REVIEW.png").convert("RGB")
assert base.size == v05.size == (930,582)
canvas = base.copy()
# Keep original back wall and arch; closed door is copied from previous existing asset.
canvas.paste(v05.crop((318,85,390,208)),(318,85))
draw = ImageDraw.Draw(canvas)
BLACK = "#070809"
WOOD_DARK = "#49301e"
WOOD_MID = "#7a502c"
WOOD_EDGE = "#a87a49"
# A continuous black frame around top and west. Top starts at the true canvas edge.
draw.rectangle((0,0,929,17), fill=BLACK)
draw.line([(0,17),(929,17)],fill=WOOD_DARK,width=3)
draw.line([(0,19),(929,19)],fill=WOOD_EDGE,width=1)
# West is fully enclosed: no leftover green/white wall on upper-left.
draw.polygon([(0,18),(46,18),(46,219),(54,219),(70,581),(0,581)],fill=BLACK)
draw.line([(45,20),(45,219),(53,219),(69,581)], fill=WOOD_DARK,width=7)
draw.line([(44,21),(44,217),(50,217),(65,581)], fill=WOOD_MID,width=3)
draw.line([(43,22),(43,216),(48,216),(63,581)], fill=WOOD_EDGE,width=1)
# East frame is continuous over the rear wall and down to the upper passage.
# The passage must align with the actual gameplay gallery east portal:
# 345..417 in a 482px game room, projected to 930x582 -> y417..503.
passage_top, passage_bottom = 395, 526
assert passage_top <= round(345*582/482) and passage_bottom >= round(417*582/482)
draw.rectangle((888,18,929,passage_top-1),fill=BLACK)
draw.line([(887,21),(887,passage_top-1)],fill=WOOD_DARK,width=6)
draw.line([(885,22),(885,passage_top-2)],fill=WOOD_MID,width=3)
draw.line([(884,22),(884,passage_top-3)],fill=WOOD_EDGE,width=1)
# Top of right passage is underside of the side wall, not a floating block.
draw.rectangle((884,passage_top-8,929,passage_top-1),fill=WOOD_DARK)
draw.line([(884,passage_top-7),(929,passage_top-7)],fill=WOOD_EDGE,width=2)
# Bottom front wall resumes below the passage; corridor floor y395..525 is untouched.
draw.polygon([(884,passage_bottom),(929,passage_bottom),(929,581),(873,581)],fill=BLACK)
draw.line([(884,passage_bottom),(874,581)],fill=WOOD_DARK,width=7)
draw.line([(882,passage_bottom),(872,581)],fill=WOOD_MID,width=3)
draw.line([(880,passage_bottom),(870,581)],fill=WOOD_EDGE,width=1)
draw.rectangle((880,passage_bottom,929,passage_bottom+7),fill=WOOD_DARK)
draw.line([(880,passage_bottom),(929,passage_bottom)],fill=WOOD_EDGE,width=2)

before = np.asarray(base)
after = np.asarray(canvas)
allowed = np.zeros((582,930),dtype=bool)
allowed[:21,:] = True
allowed[18:,:75] = True
allowed[18:,869:] = True
allowed[85:208,318:390] = True
assert np.array_equal(before[~allowed], after[~allowed]), "Outside planned geometry changed"
assert np.all(after[21:215, 3:35]==(7,8,9)), "west upper corner not continuously black"
assert np.all(after[22:370, 901:928]==(7,8,9)), "east upper corner not continuously black"
assert np.array_equal(before[passage_top:passage_bottom, 897:930],after[passage_top:passage_bottom, 897:930]), "east opening must use original floor"
assert after[0,450].tolist()==[7,8,9], "top border absent"
# Unchanged full rear exhibition wall, except for the approved existing closed door.
assert np.array_equal(before[48:205,410:840],after[48:205,410:840])
image_file = qa / "gallery1_v10_black_outer_frame_entrance_aligned_REVIEW.png"
canvas.save(image_file)
cmp=Image.new("RGB",(1860,614),"#ebe9e4")
cmp.paste(Image.open(qa / "gallery1_v09_structural_walls_REVIEW_NOT_APPROVED.png").convert("RGB"),(0,32))
cmp.paste(canvas,(930,32))
cd=ImageDraw.Draw(cmp)
cd.rectangle((0,0,1859,31), fill="#25282b")
cd.text((12,10),"v09 / off-position passage and unframed upper wall",fill="white")
cd.text((942,10),"v10 / continuous outer black frame + aligned east passage",fill="white")
comparison=qa / "gallery1_v09_v10_comparison_REVIEW.png"
cmp.save(comparison)
print("PASS",image_file.name,comparison.name, "changed", np.count_nonzero(np.any(before!=after,axis=2)))
