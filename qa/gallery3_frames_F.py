"""Gallery3 F: 5-frame placement on approved E architecture, proposal only."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib

root=Path(__file__).resolve().parents[1]
f=root/"rooms/gallery3"
original=f/"gallery3_architecture_only_E.png"
approved_digest=hashlib.sha256(original.read_bytes()).hexdigest()
base=Image.open(original).convert("RGBA")
assert base.size==(930,582)
background=base.copy()
d=ImageDraw.Draw(background)
font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf",30)
# Three fixed rear frames, one inside the recessed bay.
# Door edges, cornice, alcove geometry and entrance remain E unchanged.
rear=[(1,74,78,162,86),(2,366,73,200,100),(3,719,78,153,86)]
for n,x,y,w,h in rear:
    d.rectangle((x-5,y-5,x+w+5,y+h+5),fill="#4c2b1a",outline="#9b673c",width=2)
    d.rectangle((x,y,x+w,y+h),fill="#714526",outline="#d5a26c",width=4)
    d.rectangle((x+9,y+9,x+w-9,y+h-9),fill="#234b40",outline="#d7bb83",width=2)
    d.line((x+11,y+h-13,x+w-11,y+h-13),fill="#15382f",width=2)
    d.text((x+w/2,y+h/2),str(n),fill="#f5deb0",font=font,anchor="mm")
background_path=f/"gallery3_layout_F_rear_frames.png"
background.save(background_path)
# Two existing movable partition materials only. No new fake photo slots.
objects=[
 ("wall4","独立展示壁④",125,334,215,176),
 ("wall5","独立展示壁⑤",579,301,204,176),
]
room_path=f/"room.json"
room=json.loads(room_path.read_text(encoding="utf-8"))
assert room["id"]=="gallery3"
assert room["layoutRevision"] in ("gallery3-architecture-only-E-20261028", "gallery3-E-architecture-approved-F-five-frames-unapproved-20261029")
assert room["objects"]==[] or [o["id"] for o in room["objects"]]==["wall4","wall5"]
assert all((0<=x<930 and 0<=y<582 and x+w<=930 and y+h<=582) for _,_,x,y,w,h in objects)
# Foreground overlaps are allowed for future character depth but no south door overlap.
assert all((x+w<395 or x>540 or y+h<525) for _,_,x,y,w,h in objects)
assert all((x+w<805 or y>500) for _,_,x,y,w,h in objects)
room.update({
 "background":"rooms/gallery3/gallery3_layout_F_rear_frames.png",
 "objects":[{"id":n,"label":label,"image":f"rooms/gallery3/{n}.png",
  "rect":{"x":x,"y":y,"w":w,"h":h}} for n,label,x,y,w,h in objects],
 "subtitle":"F配置案：奥の3枠＋独立展示壁2枠（建築E案は承認済み）",
 "entrance":"南：展示室1（画面下中央）",
 "exit":"東：展示室5（右側面アーチ、Lv.6開放）",
 "layoutRevision":"gallery3-E-architecture-approved-F-five-frames-unapproved-20261029",
 "status":"E architecture approved; F frame placement pending user review",
 "notes":"Exactly five exhibit slots: fixed rear 1-3 and movable wall4-5. Preserve original E image. Dedicated guide staff and interaction/collision/depth validation pending.",
 "previewFocusX":469
})
room_path.write_text(json.dumps(room,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
# Assemble a full concept image independent of browser.
view=background.copy()
for o in room["objects"]:
    r=o["rect"]
    a=Image.open(root/o["image"]).convert("RGBA").resize((r["w"],r["h"]),Image.Resampling.LANCZOS)
    view.alpha_composite(a,(r["x"],r["y"]))
view.save(f/"gallery3_layout_F_five_frames.png")
assert hashlib.sha256(original.read_bytes()).hexdigest()==approved_digest
assert len(rear)+len(objects)==5
print("PASS gallery3 F assets:",view.size,"fixed",len(rear),"movable",len(objects),
      "E-preserved-sha256",approved_digest[:12])
