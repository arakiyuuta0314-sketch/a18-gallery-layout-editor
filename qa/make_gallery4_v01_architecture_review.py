"""A18 Gallery4 architecture v01 - plain western exit, NO arch/door/3D wall.
Reuses existing accepted gallery1 and gallery3 photography, exact A four rear
bays and one independent wall. Review only; originals and game unchanged.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
import hashlib,json
ROOT=Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
ROOM=ROOT/"rooms/gallery4"
QA=ROOT/"qa/architecture-bases-20261029"
g1=Image.open(QA/"gallery1_v13_B_right_passage_top_lowered_24px_REVIEW.png").convert("RGB")
g3=Image.open(QA/"gallery3_v09_architecture_south_passage_REVIEW.png").convert("RGB")
approved=Image.open(ROOM/"architecture_only_A.png").convert("RGB")
assert g1.size==g3.size==approved.size==(930,582)
rsha=hashlib.sha256((ROOM/"room.json").read_bytes()).hexdigest()
asha=hashlib.sha256((ROOM/"architecture_only_A.png").read_bytes()).hexdigest()
BLACK=(5,6,7)
im=g1.copy()
# Replace north arch and use real green wallpaper/wood panels from accepted
# gallery1. Four wall bays retain original gallery4 A slot clearances.
source=(485,39,655,220)
bays=[(76,254),(281,499),(527,655),(682,865)]
for l,r in bays:
    tile=g1.crop(source).resize((r-l,181),Image.Resampling.LANCZOS)
    im.paste(tile,(l,39))
# Preserve real carved wooden cornice, fill the old north door's top section.
beam=g1.crop((487,16,656,39))
for l in range(44,886,beam.width):
    w=min(beam.width,886-l)
    im.paste(beam.crop((0,0,w,23)),(l,16))
# Add real columns between all rear bays: no blank or merged panels.
pillar=g1.crop((452,39,484,220))
columns=[(44,76),(254,281),(499,527),(655,682),(865,886)]
for l,r in columns:
    im.paste(pillar.resize((r-l,181),Image.Resampling.LANCZOS),(l,39))
# Uninterrupted approved central room floor, except the previously accepted
# south entrance from gallery3; avoids gallery4's unapproved green carpet.
im.paste(g3.crop((381,521,560,582)),(381,521))
# Exterior contour; right wall CLOSED. Left only one simple floor opening.
dr=ImageDraw.Draw(im)
dr.rectangle((0,0,929,15),fill=BLACK)
dr.rectangle((0,16,43,293),fill=BLACK)
dr.rectangle((0,427,43,581),fill=BLACK)
dr.rectangle((886,16,929,581),fill=BLACK)
dr.rectangle((0,566,380,581),fill=BLACK)
dr.rectangle((560,566,929,581),fill=BLACK)
# West PASSAGE: simply extend the existing tiled floor 44px to the left.
# No arched molding, vertical wall panels, freestanding columns or closed door.
a=np.asarray(im).copy()
floor=np.asarray(g1)
a[294:427,0:44,:]=floor[294:427,44:88,:]
im=Image.fromarray(a,"RGB")
out=np.asarray(im)
assert np.all(out[0:16]==BLACK)
assert np.all(out[250:294,0:44]==BLACK)
assert np.all(out[427:566,0:44]==BLACK)
assert np.array_equal(out[294:427,0:44],floor[294:427,44:88])
assert np.all(out[220:565,886:930]==BLACK)
assert np.array_equal(out[266:520,76:885],np.asarray(g1)[266:520,76:885]),"Main floor modified"
assert np.array_equal(out[522:566,400:545],np.asarray(g3)[522:566,400:545]),"South entry not reused"
assert np.array_equal(out[566:582,400:545],np.asarray(g3)[566:582,400:545]),"South entry closed"
assert np.array_equal(out[39:220,44:76],np.asarray(g1)[39:220,452:484]),"Left pillar differs from original"
assert not np.any(np.all(out[294:427,0:44]==BLACK,axis=2)),"West passage has black blocking pixels"
assert len(bays)==4
# Four already approved rear-frame rectangles sit INSIDE the actual bays.
rear_rects=[(125,39,224,182),(294,69,489,175),(541,39,641,182),(693,69,864,175)]
for i,(x1,y1,x2,y2) in enumerate(rear_rects):
    l,r=bays[i]
    assert x1>=l and x2<r,(i,l,r,x1,x2)
    assert y1>=39 and y2<=220
assert hashlib.sha256((ROOM/"room.json").read_bytes()).hexdigest()==rsha
assert hashlib.sha256((ROOM/"architecture_only_A.png").read_bytes()).hexdigest()==asha
archpath=QA/"gallery4_v01_plain_west_passage_architecture_REVIEW.png"
im.save(archpath)
# Visual overlay keeps approved A rear frames and actual independent wall 5.
withframes=im.copy()
Aframes=Image.open(ROOM/"gallery4_A_rear.png").convert("RGB")
for rect in rear_rects:
    withframes.paste(Aframes.crop(rect),(rect[0],rect[1]))
r=json.loads((ROOM/"room.json").read_text(encoding="utf-8"))
assert r["layoutRevision"]=="gallery4-A-visual-layout-approved-20261029"
assert len(r["objects"])==1
for o in r["objects"]:
    box=o["rect"]
    item=Image.open(ROOT/o["image"]).convert("RGBA")
    assert item.size==(box["w"],box["h"])
    withframes.paste(item,(box["x"],box["y"]),item)
framespath=QA/"gallery4_v01_approved_A_five_frames_REVIEW.png"
withframes.save(framespath)
comparison=Image.new("RGB",(1860,624),"#1f2223")
comparison.paste(approved,(0,42))
comparison.paste(im,(930,42))
draw=ImageDraw.Draw(comparison)
draw.rectangle((0,0,1859,41),fill="#292b2d")
draw.text((14,14),"ORIGINAL A / ARCH & GREEN CARPET",fill="white")
draw.text((944,14),"V01 / PLAIN WEST OPENING + MATCHED MATERIALS",fill="white")
comparepath=QA/"gallery4_original_A_vs_v01_plain_corridor_COMPARISON.png"
comparison.save(comparepath)
print("PASS: west opening plain, south passage open, east closed, 4+1 approved positions untouched")
print(archpath.name,framespath.name,comparepath.name)
