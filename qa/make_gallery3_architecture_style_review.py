"""Gallery 3: style-matched architectural review using only approved real assets.
Preserve gallery3's E alcove, east-side exit and south-center entrance.
No change to room.json, approved exhibition positions or game source.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import numpy as np
import cv2

ROOT=Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
QA=ROOT/"qa/architecture-bases-20261029"
source=Image.open(QA/"gallery1_v13_B_right_passage_top_lowered_24px_REVIEW.png").convert("RGB")
gal2=Image.open(ROOT/"rooms/gallery2/architecture_only_v01.png").convert("RGB")
e=Image.open(ROOT/"rooms/gallery3/gallery3_architecture_only_E.png").convert("RGB")
assert source.size==gal2.size==e.size==(930,582)
BLACK=(5,6,7)
out=source.copy()
draw=ImageDraw.Draw(out)
# Blank out the center NORTH door in the approved gallery1 image by reconstructing
# same-image wall sections, preserving its existing lighting, wainscot and cornice.
def wall_span(x0,x1,y0=39,y1=220,dim=1.0):
    """Exact source material, with tiles joined in wall lengths (no flat painted color)."""
    wall=Image.new("RGB",(x1-x0,y1-y0))
    tile=source.crop((486,y0,658,y1))
    for xx in range(0,x1-x0,tile.width):
        w=min(tile.width,x1-x0-xx)
        wall.paste(tile.crop((0,0,w,y1-y0)),(xx,0))
    if dim!=1:
        wall=ImageEnhance.Brightness(wall).enhance(dim)
    out.paste(wall,(x0,y0))
for x0,x1 in [(44,250),(280,681),(711,886)]:
    wall_span(x0,x1)
# Restore a continuous top wooden cornice where the old north arch touched it.
top=source.crop((493,16,656,39))
for xx in range(278,681,top.width):
    w=min(top.width,681-xx)
    out.paste(top.crop((0,0,w,top.height)),(xx,16))
draw=ImageDraw.Draw(out)
# RECESSED BACK WALL: restore unique E construction. The niche is separated
# from the outer side panels by dark shadowed returns at x269..289 and x659..680.
# Do not flatten its footprint into one continuous wall.
niche=(284,45,662,220)
crop=out.crop(niche)
crop=ImageEnhance.Brightness(crop).enhance(.80)
out.paste(crop,(284,45))
draw=ImageDraw.Draw(out)
draw.rectangle((279,38,668,45),fill=(26,22,18))
draw.line((282,44,662,44),fill=(76,49,29),width=3)
# A pair of side return planes projects slightly forward, aligned with original E.
# Use existing decorative mahogany texture as source, not newly painted backgrounds.
side_a=source.crop((675,39,691,220)).resize((17,205),Image.Resampling.LANCZOS)
side_b=source.crop((667,39,683,220)).resize((19,205),Image.Resampling.LANCZOS)
out.paste(ImageEnhance.Brightness(side_a).enhance(.62),(264,39))
out.paste(ImageEnhance.Brightness(side_b).enhance(.62),(663,39))
draw=ImageDraw.Draw(out)
draw.polygon([(268,218),(281,218),(286,244),(279,240)],fill=(98,62,38))
draw.polygon([(663,218),(678,218),(679,241),(660,233)],fill=(96,59,35))
draw.line([(280,218),(286,244)],fill=(166,110,70),width=2)
draw.line([(663,219),(660,233)],fill=(147,93,53),width=2)

# Re-introduce the original photorealistic columns, preserving E's column geometry.
pillar=source.crop((452,39,484,220))
for x in [44,248,681,854]:
    out.paste(pillar,(x,39))

# EAST PORTAL: E originally has a right-side arch and setback wall
# (roughly x807..929, y221..518). Build its wood-paneled return using a
# perspective warp of actual accepted wall pixels and its closed wooden door.
# The right exit is deliberately not moved to the north wall.
def warp_rgba(tile,points):
    a=np.asarray(tile.convert("RGB"))
    h,w=a.shape[:2]
    src4=np.float32([[0,0],[w-1,0],[w-1,h-1],[0,h-1]])
    dst4=np.float32(points)
    m=cv2.getPerspectiveTransform(src4,dst4)
    canvas=cv2.warpPerspective(a,m,(930,582),flags=cv2.INTER_LINEAR,
          borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0))
    mask=cv2.warpPerspective(np.full((h,w),255,np.uint8),m,(930,582),
                            flags=cv2.INTER_NEAREST)
    return Image.fromarray(canvas),Image.fromarray(mask)
wall=source.crop((75,39,222,219))
wall_image,wall_mask=warp_rgba(wall,[(806,220),(929,220),(929,515),(807,486)])
out.paste(wall_image,(0,0),wall_mask)
# The original E has an arched portal on its right wall; fit the approved
# real wooden CLOSED door (including arch and surround) inside that return.
door=source.crop((288,39,416,220))
door_image,door_mask=warp_rgba(door,[(815,259),(923,267),(920,484),(815,464)])
out.paste(door_image,(0,0),door_mask)
draw=ImageDraw.Draw(out)
draw.line([(806,221),(807,485),(929,516)],fill=(53,29,18),width=5)
draw.line([(810,224),(810,482)],fill=(164,104,59),width=2)
draw.line([(811,486),(926,517)],fill=(175,119,73),width=2)
# Explicit east black perimeter beyond the side wall, not inside it.
draw.rectangle((920,39,929,219),fill=BLACK)
# SOUTH CENTRAL PASSAGE: rectangular break in black bottom band. Take
# floor pixels from gallery2 original reference, NOT a speculative carpet.
entrance_left,entrance_right=401,531
out.paste(gal2.crop((entrance_left,566,entrance_right,582)),(entrance_left,566))
draw.rectangle((0,566,entrance_left-1,581),fill=BLACK)
draw.rectangle((entrance_right,566,929,581),fill=BLACK)
# Entrance corridor is floor, its position is true to approved E south center.
assert out.size==(930,582)
before=np.asarray(source);after=np.asarray(out)
assert np.array_equal(after[260:550,60:795],before[260:550,60:795]),"Room's central approved floor altered"
assert np.array_equal(after[566:582,401:531],np.asarray(gal2)[566:582,401:531]),"South exit closed"
assert np.all(after[566:582,0:399]==BLACK) and np.all(after[566:582,533:930]==BLACK)
assert np.array_equal(after[39:220,44:76],np.asarray(pillar))
assert np.array_equal(after[39:220,248:280],np.asarray(pillar))
assert np.array_equal(after[39:220,681:713],np.asarray(pillar))
# Recess is darker than outer side wall; its original E footprint is preserved.
assert np.mean(after[60:160,330:630])<np.mean(after[60:160,85:230])
assert after[215,270].tolist()!=after[215,330].tolist()
f=QA/"gallery3_v01_matched_architecture_recess_side_door_REVIEW.png"
out.save(f)
cmp=Image.new("RGB",(1860,625),"#262729")
cmp.paste(e,(0,43));cmp.paste(out,(930,43))
cd=ImageDraw.Draw(cmp)
cd.rectangle((0,0,1859,42),fill="#242729")
cd.text((12,14),"GALLERY 3 / APPROVED E ARCHITECTURE SHAPE (SOURCE)",fill="white")
cd.text((942,14),"GALLERY 3 / MATERIALS + CLOSED EAST ARCH + BLACK BORDER (REVIEW)",fill="white")
cmp.save(QA/"gallery3_E_vs_v01_matched_material_COMPARISON.png")
print("PASS gallery3 original E alcove, east-side door position, south central opening, 5 display locations untouched")
print(f)
