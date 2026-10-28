"""Gallery3 E: architecture-only draft for review (not approved/game-ready)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json, math, random

root = Path(__file__).resolve().parents[1]
outdir = root / "rooms" / "gallery3"
w, h = 930, 582
src = Image.open(root / "rooms" / "gallery1" / "architecture.png").convert("RGB")
im = Image.new("RGB", (w, h), "#dbc8ac")
im.paste(src.crop((0, 218, w, h)), (0, 218))
d = ImageDraw.Draw(im)

# The existing cornice is reused exactly; the wall below is redrawn WITHOUT art.
im.paste(src.crop((0, 0, w, 36)), (0, 0))
d = ImageDraw.Draw(im)
for y in range(36, 171):
    t = (y - 36) / 135
    d.line((0, y, 929, y), fill=(int(24+9*t), int(68+10*t), int(57+7*t)))
# Distinctive deep-set center bay, with solid north wall (NO north door).
d.rectangle((288, 43, 658, 173), fill="#1b4239")
d.line((288, 40, 658, 40), fill="#a0784d", width=5)
d.line((290, 45, 290, 173), fill="#11382f", width=7)
d.line((658, 45, 658, 173), fill="#a77e51", width=7)
# Side bay molding and north-wall pilasters remain structural (not decoration).
for x1, x2 in [(43, 250), (702, 872)]:
    d.rectangle((x1, 52, x2, 163), outline="#3c6253", width=3)
    d.line((x1+7, 59, x2-7, 59), fill="#6b8468", width=1)
# Low wood paneling with individual visible recessed panels.
d.rectangle((0, 169, 929, 218), fill="#5e3824")
d.rectangle((0, 171, 929, 178), fill="#8c5831")
for x in range(5, 930, 46):
    d.rectangle((x, 182, min(x+38, 928), 210), fill="#744429", outline="#a47349", width=2)
    d.line((x+4, 207, min(x+34,928), 207), fill="#4a2b20", width=2)
d.line((0, 214, 929, 214), fill="#c49660", width=4)
d.line((0, 219, 929, 219), fill="#755036", width=3)
# Deep-set center has two architecturally angled returns to emphasize the U-shape.
d.polygon([(267,171),(289,177),(289,235),(269,244)], fill="#af855d")
d.polygon([(659,177),(683,170),(681,244),(659,235)], fill="#80593b")
d.line([(267,171),(267,242),(281,251)], fill="#dfbe8f", width=4)
d.line([(683,170),(683,242),(671,251)], fill="#d7b183", width=4)
# Four load-bearing pilasters, arranged to frame this bay.
for x in [21, 259, 692, 913]:
    d.rectangle((x-12, 35, x+12, 217), fill="#805231", outline="#4a2a19", width=2)
    d.rectangle((x-7, 39, x+7, 210), fill="#e6d4b0")
    d.line((x-6, 44, x-6, 207), fill="#fff1d7", width=2)
    d.rectangle((x-15, 206, x+15, 218), fill="#9f774d", outline="#59351e", width=2)
# Left edge is sealed: wall with visible near and far edges, no false door.
d.polygon([(0,219),(47,233),(47,468),(0,491)],fill="#d0bda2")
d.polygon([(0,219),(12,223),(12,484),(0,491)],fill="#916c4b")
d.line([(47,233),(47,468),(0,491)],fill="#6d4c37",width=5)
d.line((16,227,16,481),fill="#f1dcc0",width=4)
# South gallery1 entrance: centered on the ACTUAL south portal (~469/930).
# A threshold OPEN to the camera edge; neither side gets clipped.
d.polygon([(427,530),(513,530),(565,581),(374,581)],fill="#866345")
d.polygon([(439,537),(501,537),(540,581),(400,581)],fill="#2b473e")
for x in [432, 507]:
    d.line((x,534, int(470+(x-470)*1.54),581),fill="#d4a66c",width=5)
d.line((429,531,511,531),fill="#e2c394",width=7)
d.line((437,539,503,539),fill="#5e3e2d",width=2)
# East gallery5 exit: complete arch VISIBLE within canvas, centered at x~875.
# The side wall reaches the right edge; the doorway is cut THROUGH it.
d.polygon([(808,222),(929,220),(929,513),(808,477)],fill="#795339")
d.polygon([(815,232),(929,223),(929,498),(815,470)],fill="#b99673")
d.polygon([(832,293),(919,293),(919,474),(832,457)],fill="#2b5348")
d.rectangle((840,336,911,465),fill="#102f29")
# the interior floor recedes toward right, making clear this is passable space
d.polygon([(838,444),(912,453),(927,477),(813,471)],fill="#a77f56")
d.line([(839,444),(910,453),(924,471)], fill="#d6ad78",width=3)
# full arch and both jambs, unlike the clipped D concept
d.arc((817,267,931,361), 180, 360, fill="#d2ac7a", width=10)
d.arc((827,276,921,355), 180, 360, fill="#66422d", width=6)
d.line((818,314,818,473),fill="#dbb588",width=10)
d.line((924,314,924,492),fill="#dbb588",width=9)
d.line((825,318,825,469),fill="#69472f",width=5)
d.line((917,318,917,477),fill="#69472f",width=5)
d.line((808,477,929,513),fill="#654127",width=6)
# A subtle shadow on east portal floor shows crossing direction.
d.polygon([(838,473),(919,483),(929,507),(816,480)],fill="#816246")
# Save the *clean architecture* alone.
dest = outdir / "gallery3_architecture_only_E.png"
im.save(dest)

# Separate human-readable guide image: annotation NOT used in app/art.
guide = im.convert("RGBA")
layer = Image.new("RGBA", (w,h), (0,0,0,0))
a = ImageDraw.Draw(layer)
font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
small = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 17)
a.rounded_rectangle((333,465,603,506),10,fill=(22,45,38,205),outline=(232,205,145,245),width=2)
a.text((467,484),"南入口 → 展示室1",font=small,anchor="mm",fill="white")
a.line([(469,507),(469,546)],fill="#f3d290",width=5)
a.polygon([(469,552),(459,538),(479,538)],fill="#f3d290")
a.rounded_rectangle((646,243,900,280),10,fill=(22,45,38,210),outline=(232,205,145,245),width=2)
a.text((774,261),"東出口 → 展示室5",font=small,anchor="mm",fill="white")
a.line([(862,283),(862,310)],fill="#f3d290",width=4)
a.rounded_rectangle((66,335,314,376),10,fill=(25,50,42,190))
a.text((190,354),"西・北は通路なし",font=small,anchor="mm",fill="white")
guide = Image.alpha_composite(guide,layer)
guide.save(outdir/"gallery3_architecture_E_guide.png")

# Draft-only editor config. Keep D & older concepts untouched.
config = outdir/"room.json"
room = json.loads(config.read_text(encoding="utf-8"))
assert room["id"] == "gallery3" and room["layoutRevision"] in ("gallery3-architecture-only-D-20261028", "gallery3-architecture-only-E-20261028")
room["background"] = "rooms/gallery3/gallery3_architecture_only_E.png"
room["objects"] = []
room["entrance"] = "South: gallery1; x≈469/930, front center (visual draft)"
room["exit"] = "East: gallery5; x≈875/930, right side (visual draft)"
room["subtitle"] = "E案：中央手前に南入口／右側に東出口（建築のみ・額縁0）"
room["previewFocusX"] = 469
room["layoutRevision"] = "gallery3-architecture-only-E-20261028"
room["status"] = "unapproved architecture-only proposal; gameplay not implemented"
room["notes"] = "Visually aligned to museum-navigation.js south/east portal directions. No frames placed by design. Five fixtures remain required and unpositioned. No walk/collision/depth QA."
config.write_text(json.dumps(room,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("OK E architecture and annotated guide:",dest,im.size)
