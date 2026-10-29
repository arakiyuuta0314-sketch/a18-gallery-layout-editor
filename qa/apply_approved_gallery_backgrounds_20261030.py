"""Populate the independent A18 layout preview with *confirmed* backgrounds for gallery 1..5.

- read approved source PNGs, never rewrite them
- preserve 930x582 pixels and room IDs / objects / foreground
- gallery 5 latest design is v21 with only numeric marker 1<->2 swapped (v22)
- this is not the game's 589x482 rendering pipeline
"""
from pathlib import Path
from PIL import Image
import hashlib, json
ROOT=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
OTHER=Path(r"C:\Users\User\source\repos\a18-gallery-layout-editor")
BASE={
 "gallery1":(OTHER/"qa/architecture-bases-20261029/gallery1_v13_B_right_passage_top_lowered_24px_REVIEW.png","v13 B; right passage top -24px; approved"),
 "gallery2":(OTHER/"rooms/gallery2/architecture_only_v01.png","A arrangement; architecture-only background, no baked rear frame numbers"),
 "gallery3":(OTHER/"qa/architecture-bases-20261029/gallery3_v09_architecture_south_passage_REVIEW.png","v09 approved architecture structure; frame geometry not final"),
 "gallery4":(OTHER/"qa/architecture-bases-20261029/gallery4_v01_plain_west_passage_architecture_REVIEW.png","v01 plain west passage, no pillar; approved"),
 "gallery5":(ROOT/"architecture-review/entrance-gallery5-comparison/gallery5-v22.png","v21 adopted aesthetics; markers left 2 center 1 right 3; 3 frames"),
}
PREVIOUS={"gallery1":"rooms/gallery1/architecture.png",
          "gallery2":"rooms/gallery2/architecture.png",
          "gallery3":"rooms/gallery3/gallery3_layout_G_rear_frames.png",
          "gallery4":"rooms/gallery4/gallery4_A_rear.png",
          "gallery5":"rooms/gallery5/gallery5_palace_E.png"}
records={}
for room,(source,decision) in BASE.items():
    if not source.is_file():raise FileNotFoundError(str(source))
    with Image.open(source) as im:
        if im.size!=(930,582) or im.mode not in ("RGB","RGBA"):
            raise AssertionError((room,im.size,im.mode))
        im.verify()
    actual=ROOT/f"rooms/{room}/background_approved.png"
    actual.write_bytes(source.read_bytes())
    data=json.loads((ROOT/f"rooms/{room}/room.json").read_text(encoding="utf-8"))
    assert data["id"]==room
    if data["size"]!={"width":930,"height":582}:raise AssertionError(room)
    prior=PREVIOUS[room]
    assert data["background"] in (prior,f"rooms/{room}/background_approved.png"),room
    data["background"]=f"rooms/{room}/background_approved.png"
    (ROOT/f"rooms/{room}/room.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    assert hashlib.sha256(actual.read_bytes()).hexdigest()==sha
    records[room]={"decision":decision,"asset":data["background"],"sourceFile":str(source),"sha256":sha,"previousBackground":prior}
manifest={"schema":"a18-layout-editor/approved-backgrounds-v1","size":[930,582],
          "purpose":"layout preview background integration; gameplay rendering and collisions remain separate",
          "galleryCount":5,"gallery5VisualBase":"v21; left2/center1/right3 only => v22",
          "rooms":records}
(ROOT/"rooms/approved_backgrounds_20261030.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("APPROVED BACKGROUND PACK:")
for k,v in records.items():print(k,v["sha256"],v["decision"])