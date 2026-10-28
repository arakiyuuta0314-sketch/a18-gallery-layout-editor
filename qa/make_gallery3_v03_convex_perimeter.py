"""Gallery3 v03: rebuild a true 凸-shaped architectural footprint.
Existing real gallery1/2 wall and floor pixels only. No synthetic replacement
scene, no door, preserve gallery3 E-approved alcove and bottom-center entrance.
Review only: never updates room.json or production game.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import numpy as np
import cv2

ROOT=Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
QA=ROOT/"qa/architecture-bases-20261029"
G1=Image.open(QA/"gallery1_v13_B_right_passage_top_lowered_24px_REVIEW.png").convert("RGB")
G2=Image.open(QA/"gallery2_v04_architecture_matching_entrance_gallery1_REVIEW.png").convert("RGB")
old=Image.open(QA/"gallery3_v02_deep_recess_open_east_passage_REVIEW.png").convert("RGB")
assert G1.size==G2.size==old.size==(930,582)
BLACK=(5,6,7)
im=G1.copy()
# Clean baseline: entire floor comes from the accepted gallery1; not the
# old v02 that left a side pillar projecting into the right passage.
draw=ImageDraw.Draw(im)
draw.rectangle((0,16,929,79),fill=BLACK)

# Front transverse walls left and right are positioned 42px *closer* to
# the viewer than the recessed back wall. The raised middle section and
# lower side wings create an unmistakable 凸-shaped upper outer boundary.
# Source walls are existing gallery1 artwork with full real cornice/columns.
frontY=81
im.paste(G1.crop((44,39,270,220)),(44,frontY))   # west wing 44..269
im.paste(G1.crop((680,39,886,220)),(680,frontY)) # east wing 680..885
# Front black top line: upper left/right sections y0..80 are external space.
draw=ImageDraw.Draw(im)
draw.rectangle((0,0,269,80),fill=BLACK)
draw.rectangle((680,0,929,80),fill=BLACK)
# Rear wall within the central raised boundary, x295..654 at y39..180.
# Use seamless photo-source wallpaper/wood work from gallery2's clear bays.
a=G2.crop((95,39,275,220)).resize((180,142),Image.Resampling.LANCZOS)
b=G2.crop((348,39,528,220)).resize((180,142),Image.Resampling.LANCZOS)
back=Image.new("RGB",(360,142))
back.paste(a,(0,0));back.paste(b,(180,0))
# A darker light level inside the recess, so it reads behind the front wall.
back=ImageEnhance.Brightness(back).enhance(.83)
im.paste(back,(295,39))
# Central raised roof, matching real wood cornice cropped from gallery1.
beam=G1.crop((490,16,650,39))
for xx in range(270,680,beam.width):
    w=min(beam.width,680-xx)
    im.paste(beam.crop((0,0,w,23)),(xx,16))
# Back niche FLOOR (behind the front sidewall) must be visibly lower than
# the back wall but extend naturally into the existing central room floor.
floor=np.asarray(G1)
rear_floor=Image.fromarray(floor[220:261,295:655].copy())
rear_floor=ImageEnhance.Brightness(rear_floor).enhance(.84)
im.paste(rear_floor,(295,181))
# At the front, side wall floors start y262; center floor appears all the
# way to the rear wall at y181. This is the architectural depth.

def perspective_paste(tile, corners, brightness=.7):
    tile=ImageEnhance.Brightness(tile).enhance(brightness)
    pix=np.asarray(tile)
    h,w=pix.shape[:2]
    M=cv2.getPerspectiveTransform(
       np.float32([[0,0],[w-1,0],[w-1,h-1],[0,h-1]]),
       np.float32(corners))
    warped=cv2.warpPerspective(pix,M,(930,582),flags=cv2.INTER_LINEAR)
    mask=cv2.warpPerspective(np.full((h,w),255,np.uint8),M,(930,582),flags=cv2.INTER_NEAREST)
    im.paste(Image.fromarray(warped),(0,0),Image.fromarray(mask))

# Side returns: from lowered front-wall plane x270/680,y81..262 back
# to raised niche x295/655,y39..181. Textured, physically connected.
side=G1.crop((670,39,688,220))
perspective_paste(side,[(269,81),(295,39),(295,181),(269,262)],brightness=.54)
perspective_paste(side.transpose(Image.Transpose.FLIP_LEFT_RIGHT),
                  [(655,39),(680,81),(680,262),(655,181)],brightness=.50)
draw=ImageDraw.Draw(im)
# Dark triangular join beneath the two wood side returns, natural baseboard.
draw.polygon([(269,219),(295,181),(295,223),(269,263)],fill=(89,53,31))
draw.polygon([(655,181),(680,219),(680,263),(655,223)],fill=(82,48,28))
draw.line([(269,261),(295,221)],fill=(169,109,66),width=2)
draw.line([(655,221),(680,261)],fill=(161,102,63),width=2)
# Fine ceiling seam above the recessed rear wall.
draw.line((295,39,654,39),fill=(52,35,23),width=3)
draw.line((297,42,652,42),fill=(121,74,43),width=1)
# Real columns face the camera on the lowered front walls, never project
# a detached column onto the right EXIT.
pillar=G1.crop((452,39,484,220))
im.paste(pillar,(44,81))
im.paste(pillar,(238,81))
im.paste(pillar,(680,81))
im.paste(pillar,(854,81))

# EAST OPENING: straight, unobstructed floor in the right black wall.
# No freestanding side-wall block, floating jamb, door or green carpet.
# Use existing *same-row* floor pixels immediately to the left and place
# them in the 44-pixel outside perimeter for a floor continuation.
R_TOP,R_BOTTOM=264,397
smooth=np.asarray(im).copy()
g=np.asarray(G1)
# Sample x842..885 from the same y, preserving floor perspective and glow.
smooth[R_TOP:R_BOTTOM,886:930]=g[R_TOP:R_BOTTOM,842:886]
im=Image.fromarray(smooth)
draw=ImageDraw.Draw(im)
draw.rectangle((0,81,43,565),fill=BLACK)   # full west wall, no exit
draw.rectangle((886,81,929,R_TOP-1),fill=BLACK) # right wall above opening
draw.rectangle((886,R_BOTTOM,929,565),fill=BLACK) # below opening
# Preserve original perimeter on other levels, make right passage truly open.
# South connection to gallery1 is central bottom, side regions remain black.
draw.rectangle((0,566,400,581),fill=BLACK)
draw.rectangle((531,566,929,581),fill=BLACK)
im.paste(G2.crop((401,566,531,582)),(401,566))

after=np.asarray(im)
base=np.asarray(G1)
assert im.size==(930,582)
assert np.all(after[:16,:,:]==BLACK), "Top perimeter should be closed"
assert np.all(after[18:76,60:235]==BLACK), "Left wing black shoulder missing"
assert np.all(after[18:76,715:850]==BLACK), "Right wing black shoulder missing"
assert not np.array_equal(after[40:67,345:602],base[40:67,345:602]), "Raised central niche missing"
assert np.array_equal(after[300:550,80:800],base[300:550,80:800]),"Original floor changed"
assert np.array_equal(after[R_TOP:R_BOTTOM,886:930],g[R_TOP:R_BOTTOM,842:886]), "East opening not floor"
assert np.all(after[199:260,910]==BLACK) and np.all(after[415:565,910]==BLACK), "East wall is not a simple break"
assert np.array_equal(after[566:582,401:531],np.asarray(G2)[566:582,401:531]),"South entry lost"
assert np.all(after[566:582,:400]==BLACK)
# Art is unobstructed at the accepted central 252x110 wall-hanging placement.
assert np.max(after[65:130,356:601].mean(axis=2))<125,"Central display bay has bright pillar"
out=QA/"gallery3_v03_convex_black_outline_open_east_REVIEW.png"
im.save(out)
comparison=Image.new("RGB",(1860,624),"#191c1e")
comparison.paste(old,(0,42))
comparison.paste(im,(930,42))
dd=ImageDraw.Draw(comparison)
dd.rectangle((0,0,1859,41),fill="#2b2b2b")
dd.text((14,14),"V02: FLAT TOP FRAME / EXIT BLOCK",fill="white")
dd.text((946,14),"V03: CONVEX TOP PERIMETER / SIMPLE EAST EXIT",fill="white")
comparison.save(QA/"gallery3_v02_vs_v03_convex_black_outline_REVIEW.png")
print("PASS 凸-shaped upper border, central rear wall, clear right exit and south entrance")
print(out)
