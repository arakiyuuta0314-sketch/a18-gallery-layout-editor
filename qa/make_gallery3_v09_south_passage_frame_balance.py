"""A18 Gallery3 v09: visually readable southern passage + frame aspect balance.
Preview-only; v08 art and approved E/G sources are NEVER overwritten.
Five-frame composition uses original G art for side frames and angled walls.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np, json, hashlib

ROOT=Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
QA=ROOT/"qa/architecture-bases-20261029"
ROOM=ROOT/"rooms/gallery3"
base=Image.open(QA/"gallery3_v08_wood_lower_returns_3d_columns_REVIEW.png").convert("RGB")
gallery1=Image.open(QA/"gallery1_v13_B_right_passage_top_lowered_24px_REVIEW.png").convert("RGB")
approved_E=Image.open(ROOM/"gallery3_architecture_only_E.png").convert("RGB")
assert base.size==gallery1.size==approved_E.size==(930,582)
assert json.loads((ROOM/"room.json").read_text(encoding="utf-8"))["layoutRevision"]=="gallery3-G-approved-user-positions-20261029"
roomsha=hashlib.sha256((ROOM/"room.json").read_bytes()).hexdigest()
esha=hashlib.sha256((ROOM/"gallery3_architecture_only_E.png").read_bytes()).hexdigest()
arch=base.copy()
a=np.asarray(base)
# SOUTH: reveal open path to gallery1. Original E design has the entrance
# at x427..513 y530 with a trapezoid widening to the bottom. Use precisely
# its geometry but render original tile floor instead of green carpet.
# The scene's preexisting bottom black contour was just a 16px tiny gap.
floorref=np.asarray(gallery1)
out=np.asarray(arch).copy()
# Under the threshold the passage remains a continuous ordinary tiled floor.
# A subtle darkening in y530..581 gives visual depth, not a green runner.
for y in range(530,582):
    t=(y-530)/51.
    xleft=int(round(428-34*t))
    xright=int(round(511+35*t))
    for x in range(max(0,xleft),min(930,xright+1)):
        if a[y,x].max()<15:  # replace previously black 16px base with tiled floor
            out[y,x]=a[min(565,y-16),x]  # continue actual visible room tiles through bottom
        # Gently shade the floor inside the path near the front.
        out[y,x]=np.uint8(np.clip(out[y,x].astype(float)*(0.96-0.025*t),0,255))
arch=Image.fromarray(out,"RGB")
dr=ImageDraw.Draw(arch)
# Existing architecture palette, dark oak and gilded lip like the original E.
dr.line([(427,528),(514,528)],fill=(55,33,20),width=7)
dr.line([(429,526),(512,526)],fill=(186,141,91),width=3)
dr.line([(430,532),(511,532)],fill=(226,186,129),width=2)
# Wood side jambs open outward toward camera, perspective continues off-screen.
dr.line([(425,531),(393,581)],fill=(74,46,28),width=10)
dr.line([(426,532),(399,581)],fill=(176,119,72),width=3)
dr.line([(516,531),(550,581)],fill=(74,46,28),width=10)
dr.line([(514,532),(544,581)],fill=(176,119,72),width=3)
# Only the right/left sides are black at the bottom; center is a visible opening.
dr.line([(0,581),(390,581)],fill=(5,6,7),width=1)
dr.line([(551,581),(929,581)],fill=(5,6,7),width=1)
im=np.asarray(arch)
allowed=np.zeros((582,930),dtype=bool)
allowed[522:582,381:561]=True
assert np.array_equal(a[~allowed],im[~allowed]),"Changed outside south passage"
assert np.array_equal(a[:522],im[:522]),"Wall/alcove/corridor modified"
assert np.array_equal(a[294:427,886:930],im[294:427,886:930]),"East passage changed"
assert np.array_equal(a[39:263,268:682],im[39:263,268:682]),"Niche changed"
assert any(im[575,x].max()>20 for x in range(406,535)),"South entrance still sealed"
arch_path=QA/"gallery3_v09_architecture_south_passage_REVIEW.png"
arch.save(arch_path)

# Fixed frame positions are review only: sides keep approved G dimensions;
# center is +20-21% vs frame1 in BOTH axes, aspect ratio 1.885.
previous=[(1,74,78,162,86),(2,348,65,252,110),(3,719,78,153,86)]
proposal=[(1,74,78,162,86),(2,376,68,196,104),(3,719,78,153,86)]
assert abs(196/104-162/86)<.002
assert 1.15<196/162<1.25 and 1.15<104/86<1.25
assert all(x>0 and y>0 and x+w<930 and y+h<582 for _,x,y,w,h in proposal)
# Keep content aspect-fit when the actual photo is inserted. These are ONLY
# the visual gold/wood frames with green placeholder and numeric slot index.
frame_style=dict(fill="#714526", outline="#d5a26c", width=4)
font=ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf",30)

def framed_scene(architecture, layout, include_objects):
    image=architecture.convert("RGBA")
    d=ImageDraw.Draw(image)
    for n,x,y,w,h in layout:
        d.rectangle((x-5,y-5,x+w+5,y+h+5),fill="#4c2b1a",outline="#9b673c",width=2)
        d.rectangle((x,y,x+w,y+h),**frame_style)
        d.rectangle((x+9,y+9,x+w-9,y+h-9),fill="#234b40",outline="#d7bb83",width=2)
        d.line((x+11,y+h-13,x+w-11,y+h-13),fill="#15382f",width=2)
        d.text((x+w/2,y+h/2),str(n),fill="#f5deb0",font=font,anchor="mm")
    if include_objects:
        room=json.loads((ROOM/"room.json").read_text(encoding="utf-8"))
        for o in room["objects"]:
            rect=o["rect"]
            panel=Image.open(ROOT/o["image"]).convert("RGBA")
            assert panel.size==(rect["w"],rect["h"]),("Unexpected asset size",o["id"],panel.size,rect)
            image.alpha_composite(panel,(rect["x"],rect["y"]))
    return image.convert("RGB")

frames=framed_scene(arch,proposal,False)
full=framed_scene(arch,proposal,True)
frame_path=QA/"gallery3_v09_rear_frames_balanced_REVIEW.png"
full_path=QA/"gallery3_v09_five_frames_full_layout_REVIEW.png"
frames.save(frame_path);full.save(full_path)
# Original accepted G 252x110 shown against new 196x104 on same v09 architecture.
before=framed_scene(arch,previous,False)
old_full=framed_scene(arch,previous,True)
old_full_path=QA/"gallery3_v09_before_old_center_full_layout_REVIEW.png"
old_full.save(old_full_path)
south=Image.new("RGB",(1200,245),"#252a2a")
for i,(label,picture) in enumerate([("v08 / south exit only a black-edge gap",base),("v09 / gallery1 passage visible",arch)]):
    crop=picture.crop((318,480,618,582)).resize((600,204),Image.Resampling.LANCZOS)
    south.paste(crop,(600*i,41))
    ImageDraw.Draw(south).text((i*600+12,13),label,fill="white")
south_path=QA/"gallery3_v08_v09_south_entrance_detail_REVIEW.png"
south.save(south_path)
compare=Image.new("RGB",(1860,624),"#272b2c")
compare.paste(before,(0,42));compare.paste(frames,(930,42))
cd=ImageDraw.Draw(compare)
cd.rectangle((0,0,1859,41),fill="#292b2c")
cd.text((12,14),"G approved / center 252x110 (ratio 2.29)",fill="white")
cd.text((942,14),"v09 proposal / center 196x104 (ratio 1.885)",fill="white")
compare_path=QA/"gallery3_v09_rear_frame_size_comparison_REVIEW.png"
compare.save(compare_path)

review={
 "schema":"a18-gallery3-architecture-frame-review/v1",
 "roomId":"gallery3","canvas":{"width":930,"height":582},
 "architectureReference":arch_path.as_posix().split("qa/")[-1],
 "rearFrameSource": "rooms/gallery3/gallery3_layout_G_rear_frames.png",
 "approvedFrames": [dict(id=n,x=x,y=y,w=w,h=h) for n,x,y,w,h in previous],
 "proposedFrames":[dict(id=n,x=x,y=y,w=w,h=h) for n,x,y,w,h in proposal],
 "imageInsertionRule":"Preserve artwork aspect ratio; scale to fit inside frame, never stretch",
 "independentWallPositions": [{"id":o["id"],**o["rect"]} for o in json.loads((ROOM/"room.json").read_text(encoding="utf-8"))["objects"]],
 "approval":"PENDING - no room.json or game asset changed"
}
jsonpath=QA/"gallery3_v09_south_passage_rear_frame_PROPOSAL.json"
jsonpath.write_text(json.dumps(review,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
assert hashlib.sha256((ROOM/"room.json").read_bytes()).hexdigest()==roomsha
assert hashlib.sha256((ROOM/"gallery3_architecture_only_E.png").read_bytes()).hexdigest()==esha
print("PASS Gallery3 v09 architecture south exit, center ratio, two independent panels")
for f in [arch_path,frame_path,full_path,old_full_path,south_path,compare_path,jsonpath]:print("OUTPUT",f)
