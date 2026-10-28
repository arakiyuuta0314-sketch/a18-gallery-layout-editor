from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

ROOT = Path(r'C:/Users/User/source/repos/a18-gallery-layout-editor')
QA = ROOT / 'qa/architecture-bases-20261029'
BASE = Image.open(QA / 'gallery1_architecture_no_frames_v04_REVIEW.png').convert('RGB')
V05 = Image.open(QA / 'gallery1_architecture_closed_door_sidewalls_v05_REVIEW.png').convert('RGB')
SIDES = Image.open(ROOT / 'rooms/gallery1/side-walls.png').convert('RGBA')
assert BASE.size == V05.size == SIDES.size == (930, 582)
out = BASE.copy()
# Keep north arch and wall; copy only the EXISTING v05 closed-door pixels.
out.paste(V05.crop((318, 85, 390, 208)), (318, 85))
# Original v04 includes a dark-green top-right sidewall inset that is part
# of the BASE (not of the separate side-wall layer). Darken ONLY that inset.
base_pixels = np.asarray(out).copy()
base_rgb = base_pixels.astype(np.int16)
by, bx = np.indices((582,930))
right_top = (bx >= 885) & (by >= 220) & (by <= 310)
base_green = (base_rgb[:,:,1] > base_rgb[:,:,0] + 7) & (base_rgb[:,:,1] > base_rgb[:,:,2] + 1) & (base_rgb[:,:,0] < 65)
base_pixels[right_top & base_green] = (6, 7, 8)
out = Image.fromarray(base_pixels, 'RGB')
s = np.asarray(SIDES).copy()
rgb = s[:, :, :3].astype(np.int16)
alpha = s[:, :, 3]
# Existing side-wall dark-green inset panels only; timber and edge highlights untouched.
green = (alpha > 0) & (rgb[:,:,1] > rgb[:,:,0] + 7) & (rgb[:,:,1] > rgb[:,:,2] + 1) & (rgb[:,:,0] < 65)
s[green, :3] = (6, 7, 8)
# Existing sidewall asset used only where wall STRUCTURALLY exists.
# West is closed along its full height. East retains its EXISTING
# upper wall (already in BASE), but the floor below it is an open corridor.
ys, xs = np.indices((582,930))
keep = (xs <= 45) & (ys >= 217)
s[~keep,3] = 0
out = Image.alpha_composite(out.convert('RGBA'), Image.fromarray(s, 'RGBA')).convert('RGB')
# Preserve original pixels everywhere except the arch door and actual side edges.
a = np.asarray(BASE); b = np.asarray(out)
allowed = np.zeros((582,930), dtype=bool)
allowed[85:208,318:390]=True
allowed[217:, :46]=True
allowed[217:311, 885:]=True
assert np.array_equal(a[~allowed],b[~allowed])
assert all(out.getpixel((929,y)) == BASE.getpixel((929,y)) for y in range(311,582))
changed=int(np.any(a!=b,axis=2).sum())
dst = QA / 'gallery1_architecture_v08_wall_structure_REVIEW.png'
out.save(dst)
sheet=Image.new('RGB',(1860,624),'#f5f2ec')
sheet.paste(BASE,(0,42));sheet.paste(out,(930,42))
dr=ImageDraw.Draw(sheet)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',21)
dr.rectangle((0,0,1860,41),fill='#292b2c')
dr.text((14,10),'BASE v04 / 3 REAR FRAMES REMOVED',font=font,fill='white')
dr.text((944,10),'v08 REVIEW / CLOSED DOOR + BLACK SIDE WALLS + EAST CORRIDOR',font=font,fill='white')
comp=QA/'gallery1_v04_vs_v08_wall_structure_COMPARISON.png'
sheet.save(comp)
print('PASS:',dst.name,changed, 'pixels changed, preview',comp.name)
