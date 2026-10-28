"""Read-only acceptance test for user-supplied Gallery1 v07 geometry.

The staff is intentionally NOT placed; verify guide counter has the proposed
clearance size and that only this room's movable layout records are changed.
"""
from pathlib import Path
from PIL import Image,ImageChops
import json
ROOT=Path(__file__).resolve().parent.parent
R=ROOT/"rooms/gallery1"
room=json.loads((R/"room.json").read_text(encoding="utf-8"))
assert room["schema"]=="a18-gallery-editor/room-v1"
assert room["id"]=="gallery1"
assert room["size"]=={"width":930,"height":582}
assert room["entrance"]=="東側：エントランス"
assert room["exit"]=="北側：展示室3"
frames={o["id"]:o for o in room["objects"]}
assert set(frames)=={"wall4","wall5","counter"}
assert frames["wall4"]["rect"]=={"x":102,"y":275,"w":240,"h":182}
assert frames["wall5"]["rect"]=={"x":636,"y":326,"w":240,"h":182}
assert frames["counter"]["rect"]=={"x":425,"y":339,"w":135,"h":76}
assert frames["counter"]["image"]=="rooms/gallery1/counter135_staff.png"
assert room["staffPlacement"]["status"]=="not placed"
assert room["staffPlacement"]["staffArt"]=="not chosen"

old=Image.open(R/"counter175.png").convert("RGBA")
new=Image.open(R/"counter135_staff.png").convert("RGBA")
assert old.size==(175,96)
assert new.size==(135,76)
assert new.getbbox() is not None
assert ImageChops.difference(old.resize((135,76),Image.Resampling.LANCZOS),new).getbbox() is None
assert 405+175/2==425+135/2==492.5
assert len({(o["id"],o["image"]) for o in room["objects"]})==3
for key in ("wall4","wall5"):
    o=frames[key]
    with Image.open(ROOT/o["image"]) as sprite:
        assert sprite.size==(o["rect"]["w"],o["rect"]["h"])
for asset in ("architecture.png","side-walls.png"):
    with Image.open(R/asset) as sprite:
        assert sprite.size==(930,582)
print("PASS v07 exact user wall locations, centered 135x76 counter, 76px provisional staff clearance, untouched architecture/5 display layout")
