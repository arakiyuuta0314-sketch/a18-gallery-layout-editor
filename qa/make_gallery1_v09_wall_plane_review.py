"""Gallery 1 v09: original v04 image, wall planes and a real east passage.
A visual review only. No approved game asset overwritten."""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

ROOT = Path(r"C:/Users/User/source/repos/a18-gallery-layout-editor")
OUT = ROOT / "qa/architecture-bases-20261029"
base = Image.open(OUT / "gallery1_architecture_no_frames_v04_REVIEW.png").convert("RGB")
closed = Image.open(OUT / "gallery1_architecture_closed_door_sidewalls_v05_REVIEW.png").convert("RGB")
assert base.size == closed.size == (930, 582)
im = base.copy()
# Reuse only the existing north-facing closed door. Do not redraw rear architecture.
im.paste(closed.crop((318,85,390,208)), (318,85))
draw = ImageDraw.Draw(im)
# West: a continuous black wall plane, not a strip painted on the floor.
# The wooden inner rim tracks the wall depth toward the viewer.
draw.polygon([(0,218),(56,218),(69,581),(0,581)], fill="#08090a")
draw.polygon([(46,218),(56,218),(69,581),(59,581)], fill="#51351f")
draw.line([(49,218),(62,581)], fill="#9d7043", width=2)
draw.line([(56,219),(69,581)], fill="#26190f", width=3)
draw.polygon([(0,217),(56,217),(56,224),(0,224)], fill="#6e4528")
draw.line([(0,217),(56,217)], fill="#b18a5a", width=2)
# Cast a narrow shadow onto existing tiles at the base of the wall.
shadow = Image.new("RGBA",(930,582),(0,0,0,0))
sd = ImageDraw.Draw(shadow)
for k in range(10):
    opacity = round(34*(1-k/10)**2)
    sd.line([(56+k,224),(69+k,581)], fill=(15,10,8,opacity),width=1)
im = Image.alpha_composite(im.convert("RGBA"),shadow).convert("RGB")
draw = ImageDraw.Draw(im)
# East: upper wall meets the rear wall; no free-floating rectangle.
draw.polygon([(885,218),(929,218),(929,335),(875,335)],fill="#07090a")
draw.polygon([(883,219),(890,219),(880,335),(873,335)],fill="#57361f")
draw.line([(884,220),(876,335)],fill="#aa7945",width=2)
draw.rectangle((875,330,929,335),fill="#53351d")
draw.line((875,331,929,331),fill="#ae8655",width=2)
# East: the lower wall joins the lower edge of the screen.
# Between y336 and y473 there is an open corridor, using the ORIGINAL floor.
draw.polygon([(885,474),(929,474),(929,581),(865,581)],fill="#08090a")
draw.polygon([(878,474),(888,474),(873,581),(863,581)],fill="#50321e")
draw.line([(881,475),(867,581)],fill="#a47747",width=2)
draw.rectangle((885,474,929,482),fill="#55351f")
draw.line((885,474,929,474),fill="#ac8353",width=2)

original = np.asarray(base)
result = np.asarray(im)
allowed = np.zeros((582,930),dtype=bool)
allowed[85:208,318:390] = True
allowed[217:,:80] = True
allowed[217:,860:] = True
assert np.array_equal(original[~allowed],result[~allowed]), "Modification outside planned wall and door polygons"
# The exit corridor is completely untouched: no carpet, overlay or black band.
assert np.array_equal(original[336:474,900:930],result[336:474,900:930])
# Top- and bottom-right wall portions exist, and west is closed.
assert all(im.getpixel((925,y)) == (7,9,10) for y in [275,315])
assert im.getpixel((925,525)) == (8,9,10)
assert im.getpixel((10,450)) == (8,9,10)
assert np.asarray(im).shape == (582,930,3)

png = OUT / "gallery1_v09_structural_walls_REVIEW_NOT_APPROVED.png"
im.save(png)
comparison = Image.new("RGB",(1860,624),"#f4f1eb")
comparison.paste(base,(0,42))
comparison.paste(im,(930,42))
header=ImageDraw.Draw(comparison)
header.rectangle((0,0,1859,41), fill="#25282b")
header.text((15,14),"v04 / ORIGINAL FRAME-FREE BASE",fill="white")
header.text((945,14),"v09 / WEST WALL + EAST OPEN CORRIDOR (REVIEW)",fill="white")
cmp = OUT / "gallery1_v04_vs_v09_structural_walls_REVIEW.png"
comparison.save(cmp)
count = int(np.any(original != result,axis=2).sum())
print("PASS",png,cmp,"changed_pixels",count)
