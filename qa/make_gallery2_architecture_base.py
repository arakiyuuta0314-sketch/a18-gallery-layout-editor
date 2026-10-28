"""A18 gallery2 architectural base from approved A: remove only baked-in rear frames.
Original room.json, approved composites and independently placed walls remain unchanged.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "rooms/gallery2/architecture.png"
dst = ROOT / "rooms/gallery2/architecture_only_v01.png"
qa_dir = ROOT / "qa/architecture-bases-20261029"
qa_dir.mkdir(parents=True, exist_ok=True)

img = Image.open(src).convert("RGBA")
assert img.size == (930, 582)
room = json.loads((ROOT / "rooms/gallery2/room.json").read_text(encoding="utf-8"))
assert room["layoutRevision"] == "A-approved-user-positions-20261028"
assert [(x["id"], x["rect"]) for x in room["objects"]] == [
    ("wall3", {"x": 105, "y": 308, "w": 212, "h": 181}),
    ("wall4", {"x": 380, "y": 251, "w": 212, "h": 181}),
    ("wall5", {"x": 664, "y": 310, "w": 212, "h": 181}),
]
# Source generator build_gallery2_editor.py: the wall was first painted flat #214e43,
# and the two rectangular rear display frames were drawn inside these exact bounds.
# No flood-fill, inpainting, geometry redraw or edits to surrounding pixels.
rects = [(80, 78, 259, 166), (349, 78, 509, 166)]
wall = (0x21, 0x4e, 0x43, 255)
for x1, y1, x2, y2 in rects:
    for y in (y1 - 1, y2 + 1):
        assert img.getpixel(((x1+x2)//2, y)) == wall, (x1, y, img.getpixel(((x1+x2)//2,y)))
base = img.copy()
draw = ImageDraw.Draw(base)
for xy in rects:
    draw.rectangle(xy, fill=wall)
base.save(dst, optimize=True)
reloaded = Image.open(dst).convert("RGBA")
assert reloaded.size == img.size
# Every original pixel outside the strictly defined removal rectangles must be identical.
diff = ImageChops.difference(img.convert("RGB"), reloaded.convert("RGB"))
bbox = diff.getbbox()
assert bbox is not None
for y in range(img.height):
    for x in range(img.width):
        if not any(x1 <= x <= x2 and y1 <= y <= y2 for x1,y1,x2,y2 in rects):
            assert img.getpixel((x,y)) == reloaded.getpixel((x,y)), (x,y)
        else:
            assert reloaded.getpixel((x,y)) == wall, (x,y)
preview = Image.new("RGB", (img.width * 2, img.height + 34), "#e5e5e5")
preview.paste(img.convert("RGB"), (0,34))
preview.paste(reloaded.convert("RGB"), (img.width,34))
dd = ImageDraw.Draw(preview)
dd.text((16,10), "BEFORE / approved architectural source", fill="#202020")
dd.text((img.width+16,10), "AFTER / structural base, rear frames removed", fill="#202020")
preview.save(qa_dir / "gallery2_before_after.png", optimize=True)
record = {
    "room": "gallery2", "source": str(src.relative_to(ROOT)).replace("\\","/"),
    "output": str(dst.relative_to(ROOT)).replace("\\","/"),
    "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
    "output_sha256": hashlib.sha256(dst.read_bytes()).hexdigest(),
    "removed_rear_frames_rects_inclusive": rects,
    "modified_pixels_outside_rects": 0,
    "original_room_json_modified": False,
    "display_walls_3_4_5_modified": False,
    "construction": "Exact erasure using recovered source wall fill; no generative reconstruction",
    "status": "review_candidate_not_game_integrated"
}
(qa_dir / "gallery2_qa.json").write_text(json.dumps(record, ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("PASS", dst, "diff_bbox", bbox, "preview", qa_dir/"gallery2_before_after.png")
