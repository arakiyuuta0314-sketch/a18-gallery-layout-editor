"""Exhibition room 3 G: larger central frame and symmetric Hachi-shaped angled partitions.

Architecture E remains byte-exact; preserves F as independent comparison.
Proposal only. No game implementation/collision claims.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json, hashlib, shutil

root=Path(__file__).resolve().parents[1]
f=root/"rooms/gallery3"
e_arch=f/"gallery3_architecture_only_E.png"
sha_e=hashlib.sha256(e_arch.read_bytes()).hexdigest()
config=f/"room.json"
room=json.loads(config.read_text(encoding="utf-8"))
assert room["id"]=="gallery3" and room["layoutRevision"] in ("gallery3-E-architecture-approved-F-five-frames-unapproved-20261029","gallery3-E-approved-G-hachi-proposal-20261029")
assert sorted(o["id"] for o in room["objects"])==["wall4","wall5"]
# Snapshot F's coordinates/layout in JSON before switching editor to the proposed G.
f_ref=f/"room_F_reference.json"
if room["layoutRevision"]=="gallery3-E-architecture-approved-F-five-frames-unapproved-20261029":
    assert not f_ref.exists(), "F snapshot already exists"
    f_ref.write_text(json.dumps(room,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
else:
    assert json.loads(f_ref.read_text(encoding="utf-8"))["layoutRevision"]=="gallery3-E-architecture-approved-F-five-frames-unapproved-20261029"

# E architecture, unmodified. Positions #1 and #3 from approved F initial proposal.
arch=Image.open(e_arch).convert("RGBA")
bg=arch.copy()
d=ImageDraw.Draw(bg)
font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf",30)
rear=[(1,74,78,162,86),(2,348,65,252,110),(3,719,78,153,86)]
for n,x,y,w,h in rear:
    d.rectangle((x-5,y-5,x+w+5,y+h+5),fill="#4c2b1a",outline="#9b673c",width=2)
    d.rectangle((x,y,x+w,y+h),fill="#714526",outline="#d5a26c",width=4)
    d.rectangle((x+9,y+9,x+w-9,y+h-9),fill="#234b40",outline="#d7bb83",width=2)
    d.line((x+11,y+h-13,x+w-11,y+h-13),fill="#15382f",width=2)
    d.text((x+w/2,y+h/2),str(n),fill="#f5deb0",font=font,anchor="mm")
bg.save(f/"gallery3_layout_G_rear_frames.png")

def perspective_wall(src_path, out_path, quad, size=(232,198)):
    """Map rectangular front face to a tilted-in-depth quadrilateral (NOT rotate pixels)."""
    src=Image.open(src_path).convert("RGBA")
    sw,sh=src.size
    # Solve 3x3 homography H: destination local coords -> source coords.
    pts=[(0,0),(sw,0),(sw,sh),(0,sh)]
    a=[]; b=[]
    for (xd,yd),(xs,ys) in zip(quad,pts):
        a.append([xd,yd,1,0,0,0,-xs*xd,-xs*yd]); b.append(xs)
        a.append([0,0,0,xd,yd,1,-ys*xd,-ys*yd]); b.append(ys)
    v=np.linalg.solve(np.array(a,dtype=float),np.array(b,dtype=float))
    warped=src.transform(size,Image.Transform.PERSPECTIVE,tuple(v),resample=Image.Resampling.BICUBIC,fillcolor=(0,0,0,0))
    warped.save(out_path)
    return warped

# Perspective: left slants / up to center, right slants back down \.
width,height=232,198
left=perspective_wall(f/"wall4.png",f/"wall4_angle_G.png",
                      [(2,20),(230,1),(230,155),(2,196)])
right=perspective_wall(f/"wall5.png",f/"wall5_angle_G.png",
                       [(2,1),(230,20),(230,196),(2,155)])
items=[
 ("wall4","独立展示壁④／ハの字左",119,314,width,height,"wall4_angle_G.png"),
 ("wall5","独立展示壁⑤／ハの字右",578,312,width,height,"wall5_angle_G.png")
]
for _,_,x,y,w,h,_ in items:assert x>=0 and y>=0 and x+w<930 and y+h<582
# South entrance ground threshold is centered x~470 near lower edge.
assert all((x+w<395 or x>540 or y+h<527) for _,_,x,y,w,h,_ in items)
# East exit begins near right wall x=808, leave extra margin.
assert items[1][2]+items[1][4]<=810

view=bg.copy()
for n,label,x,y,w,h,filename in items:
    view.alpha_composite(Image.open(f/filename).convert("RGBA"),(x,y))
view.save(f/"gallery3_layout_G_hachi.png")

# Honest side-by-side comparison with the exact F image.
f_img=Image.open(f/"gallery3_layout_F_five_frames.png").convert("RGB")
g_img=view.convert("RGB")
compare=Image.new("RGB",(930*2+48,582+64),"#f1eadf")
compare.paste(f_img,(12,54)); compare.paste(g_img,(942,54))
ad=ImageDraw.Draw(compare)
headfont=ImageFont.truetype(r"C:\Windows\Fonts\meiryo.ttc",19)
ad.text((12,18),"F案：従来の正面配置／中央作品200×100",fill="#263a33",font=headfont)
ad.text((942,18),"G案：中央作品252×110＋ハの字展示壁",fill="#263a33",font=headfont)
compare.save(f/"gallery3_F_vs_G_comparison.png")

room.update({
 "background":"rooms/gallery3/gallery3_layout_G_rear_frames.png",
 "objects":[{"id":n,"label":label,"image":f"rooms/gallery3/{filename}",
             "rect":{"x":x,"y":y,"w":w,"h":h}}
            for n,label,x,y,w,h,filename in items],
 "subtitle":"G比較案：奥の②を拡大＋展示壁④⑤をハの字（未承認）",
 "layoutRevision":"gallery3-E-approved-G-hachi-proposal-20261029",
 "status":"E architectural outline approved, G frame sizes/angles unapproved",
 "notes":"E architectural base remains preserved unchanged. Rear 1&3 unchanged. Rear 2 enlarged 200x100 =>252x110; movable 4&5 perspective-distorted as dedicated images, no geometric rotation applied to a flat rectangle. Walkability, wall footprints, layer sorting and staff placement pending QA.",
})
config.write_text(json.dumps(room,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
assert hashlib.sha256(e_arch.read_bytes()).hexdigest()==sha_e
print("PASS G",view.size,"rear",len(rear),"angled panels",len(items),"E sha",sha_e[:12])
print("INFO G objects",[(x[0],x[2:6]) for x in items])
