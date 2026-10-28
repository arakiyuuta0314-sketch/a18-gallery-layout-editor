"""Build faithful six-room visual overview from approved assets; no game changes."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json,hashlib,shutil
root=Path(__file__).resolve().parents[1]
output=root/"whole-museum-review"
output.mkdir(exist_ok=True)
entrance_root=root.parent/"a18-art-previews-publish"/"entrance-lv6-review-20261028"
entrance_source=entrance_root/"approved-entrance-lv6-20261028.png"
manifest=json.loads((entrance_root/"APPROVED_ENTRANCE_LV6_MANIFEST.json").read_text(encoding="utf-8"))
expected=manifest["sha256"]
assert hashlib.sha256(entrance_source.read_bytes()).hexdigest()==expected,"Entrance Lv6 approval source hash mismatch"
Image.open(entrance_source).verify()
if not (output/"entrance_approved_lv6.png").exists():
    shutil.copyfile(entrance_source,output/"entrance_approved_lv6.png")
assert hashlib.sha256((output/"entrance_approved_lv6.png").read_bytes()).hexdigest()==expected

rooms={}
for i in range(1,6):
    room=json.loads((root/f"rooms/gallery{i}/room.json").read_text(encoding="utf-8"))
    assert room["id"]==f"gallery{i}"
    sz=room["size"]; assert (sz["width"],sz["height"])==(930,582)
    base=Image.open(root/room["background"]).convert("RGBA")
    assert base.size==(930,582)
    for obj in room["objects"]:
        rc=obj["rect"]
        art=Image.open(root/obj["image"]).convert("RGBA").resize((rc["w"],rc["h"]),Image.Resampling.LANCZOS)
        base.alpha_composite(art,(rc["x"],rc["y"]))
    # The editor draws the separate foreground above movable gallery walls.
    fg=Image.open(root/room["foreground"]).convert("RGBA")
    assert fg.size==(930,582),f"unexpected foreground size gallery{i}: {fg.size}"
    base.alpha_composite(fg)
    base.convert("RGB").save(output/f"gallery{i}_approved_layout.png")
    rooms[f"gallery{i}"]=base.convert("RGB")
assert json.loads((root/"rooms/gallery5/room.json").read_text(encoding="utf-8"))["approvedTargetFrameCount"]==3

# Approved entrance image is 1200x880 screenshot; DO NOT crop away furniture/character/UI.
entrance=Image.open(output/"entrance_approved_lv6.png").convert("RGB")
canvas=Image.new("RGB",(930,582),"#203e34")
fits=ImageOps.contain(entrance,(930,582),Image.Resampling.LANCZOS)
canvas.paste(fits,((930-fits.width)//2,(582-fits.height)//2))
rooms["entrance"]=canvas
font_path="C:/Windows/Fonts/meiryo.ttc"
title=ImageFont.truetype(font_path,26)
sub=ImageFont.truetype(font_path,16)
labels={
    "gallery1":("展示室1","Lv.2｜配置承認・5枠"),
    "gallery2":("展示室2","Lv.3｜配置承認・5枠"),
    "gallery3":("展示室3","Lv.4｜G案・5枠"),
    "gallery4":("展示室4","Lv.5｜A案・5枠"),
    "gallery5":("展示室5","Lv.6｜E案・正式3枠（未実装）"),
    "entrance":("エントランス","Lv.1〜6｜画像はLv.6正式デザイン")
}
ordering=[["gallery3","gallery5","gallery4"],["gallery1","entrance","gallery2"]]
thumb=(590,370)
margin=20;gap=18;header=70;footer=57
sheet_w=margin*2+thumb[0]*3+gap*2
sheet_h=margin*2+(thumb[1]+header)*2+gap+footer
sheet=Image.new("RGB",(sheet_w,sheet_h),"#f4f0e9")
d=ImageDraw.Draw(sheet)
for r,row in enumerate(ordering):
 for col,k in enumerate(row):
    x=margin+col*(thumb[0]+gap);y=margin+r*(header+thumb[1]+gap)
    d.rounded_rectangle((x,y,x+thumb[0],y+header+thumb[1]),radius=9,fill="#ffffff",outline="#c0b6a6",width=2)
    t,st=labels[k]
    d.text((x+14,y+10),t,font=title,fill="#25483c")
    d.text((x+14,y+42),st,font=sub,fill="#615f56")
    img=ImageOps.fit(rooms[k],thumb,method=Image.Resampling.LANCZOS)
    sheet.paste(img,(x,y+header))
d.text((margin,sheet_h-footer+12),"※展示室は承認済み配置の合成プレビュー。入口は承認済みLv.6画像（試験UIが写り込む）。通行判定は未検証。",font=sub,fill="#5a5b52")
sheet.save(output/"whole_museum_map_3x2.png")
# Text metadata for UI and provenance.
meta={
 "schema":"a18-whole-museum-review/v1",
 "source":"approved layout configs and entrance approved Lv6 image",
 "reviewOnly":True,
 "order":[z for row in ordering for z in row],
 "approvedTargets":{"entrance":3,"gallery1":5,"gallery2":5,"gallery3":5,"gallery4":5,"gallery5":3,"total":26},
 "runtime": {"currentTotalFrames":28,"currentGallery5Frames":5,"status":"deferred implementation"},
 "entranceApprovedSha256":expected,
 "rooms":[{"id":k,"title":labels[k][0],"subtitle":labels[k][1],
           "preview":f"{k}_approved_layout.png" if k!="entrance" else "entrance_approved_lv6.png"} for row in ordering for k in row]
}
(output/"overview.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("PASS overview",sheet.size,"rooms",len(meta["rooms"]),"entrance_SHA",expected[:16])
