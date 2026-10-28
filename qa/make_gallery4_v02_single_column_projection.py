"""A18 gallery4 review v02: add ONLY one modest attached column/projection
to the west passage (from review v01), no arch/door or protruding full sidewall.
All source pixels from already accepted gallery1; game and A layout untouched.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance
import numpy as np, hashlib, json

ROOT=Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
QA=ROOT/"qa/architecture-bases-20261029"
ROOM=ROOT/"rooms/gallery4"
base=Image.open(QA/"gallery4_v01_plain_west_passage_architecture_REVIEW.png").convert("RGB")
g1=Image.open(QA/"gallery1_v13_B_right_passage_top_lowered_24px_REVIEW.png").convert("RGB")
assert base.size==g1.size==(930,582)
room_json=ROOM/"room.json"
a_original=ROOM/"architecture_only_A.png"
original_hashes={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in (room_json,a_original)}
out=base.copy()
# One post attached exactly to the inside edge of the upper west wall.
# Front surface uses a real cream stone/pillar with dark wooden footing.
# This is the same original gallery1 physical material, not a new drawn pillar.
front=g1.crop((452,39,484,220)).resize((32,188),Image.Resampling.LANCZOS)
front=ImageEnhance.Brightness(front).enhance(.90)
out.paste(front,(44,241))
# Existing source pillar's dark-wood flank, a narrow visible right-hand face.
flank=g1.crop((476,39,484,220)).resize((10,184),Image.Resampling.LANCZOS)
flank=ImageEnhance.Brightness(flank).enhance(.67)
out.paste(flank,(76,245))
dr=ImageDraw.Draw(out)
# Roof/cap, base trim and contact shadow remain inside one column assembly.
dr.polygon([(43,237),(74,237),(86,243),(76,248),(44,246)],fill=(102,65,38))
dr.line([(45,238),(74,238),(83,242)],fill=(191,137,79),width=2)
dr.line([(44,243),(75,243)],fill=(214,168,104),width=2)
# Floor/base: only right of the actual open passage and anchored to upper wall.
dr.polygon([(42,426),(76,426),(88,433),(86,438),(43,435)],fill=(89,51,27))
dr.line([(44,428),(75,428),(86,433)],fill=(185,130,72),width=2)
dr.line([(44,437),(82,440),(91,445)],fill=(59,40,27),width=2)
# No decorative doorway frame, no free-standing second post or arch.
old=np.asarray(base);new=np.asarray(out)
mask=np.zeros((582,930),dtype=bool)
mask[236:448,42:93]=True
assert np.array_equal(old[~mask],new[~mask]),"Unrelated area changed"
assert np.array_equal(old[39:220],new[39:220]),"Approved A four rear bay wall changed"
assert np.array_equal(old[294:427,0:42],new[294:427,0:42]),"West EXIT floor no longer clear"
assert np.array_equal(old[522:582,380:561],new[522:582,380:561]),"South entrance moved"
assert np.array_equal(old[:,886:930],new[:,886:930]),"East closed wall changed"
assert np.array_equal(old[449:565],new[449:565]),"Main floor changed"
assert np.any(old[245:426,44:86] != new[245:426,44:86]),"Column not added"
for p,h in original_hashes.items():
    assert hashlib.sha256(p.read_bytes()).hexdigest()==h,("Original overwritten",p)
column=QA/"gallery4_v02_west_attached_column_REVIEW.png"
out.save(column)
# Reuse exact original A rear frame pixels and standalone frame in same positions.
def frames_overlay(bg):
    image=bg.copy()
    rear=Image.open(ROOM/"gallery4_A_rear.png").convert("RGB")
    rects=[(125,39,224,182),(294,69,489,175),(541,39,641,182),(693,69,864,175)]
    for x1,y1,x2,y2 in rects:
        image.paste(rear.crop((x1,y1,x2,y2)),(x1,y1))
    layout=json.loads(room_json.read_text(encoding="utf-8"))
    assert layout["layoutRevision"]=="gallery4-A-visual-layout-approved-20261029"
    assert len(layout["objects"])==1
    wall=layout["objects"][0]
    assert wall["rect"]=={"x":614,"y":323,"w":210,"h":165}
    pane=Image.open(ROOT/wall["image"]).convert("RGBA")
    image.paste(pane,(614,323),pane)
    return image
full=frames_overlay(out)
withframes=QA/"gallery4_v02_attached_column_approved_A_five_frames_REVIEW.png"
full.save(withframes)
before=frames_overlay(base)
comparison=Image.new("RGB",(1860,624),"#242829")
comparison.paste(before,(0,42));comparison.paste(full,(930,42))
cd=ImageDraw.Draw(comparison)
cd.rectangle((0,0,1859,41),fill="#272b2c")
cd.text((12,13),"LEFT: PLAIN EXIT / NO PILLAR (V01)",fill="white")
cd.text((942,13),"RIGHT: ONLY ONE ATTACHED PILLAR (V02)",fill="white")
comp=QA/"gallery4_v01_plain_vs_v02_column_COMPARISON.png"
comparison.save(comp)
detail=Image.new("RGB",(1200,625),"#27292b")
for i,(label,img) in enumerate([("V01: plain opening",base),("V02: column edge",out)]):
    crop=img.crop((0,193,190,477)).resize((580,540),Image.Resampling.LANCZOS)
    detail.paste(crop,(i*600+10,55))
    ImageDraw.Draw(detail).text((i*600+14,17),label,fill="white")
close=QA/"gallery4_v01_v02_west_column_detail_COMPARISON.png"
detail.save(close)
print("PASS gallery4 v02: one column change, 4+1 layout stays, 2 entrances open")
print("CHANGED PIXELS",int(np.any(old!=new,axis=2).sum()))
for x in (column,withframes,comp,close):print("OUTPUT",x.name)
