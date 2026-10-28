"""Gallery3 v02 preview: show actual depth at the previously approved E niche.
Right/east exit is a FLOOR corridor without a door. Same real gallery1/2 assets.
All changes remain strictly review-only. Neither game nor room JSON updated.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageEnhance,ImageFilter
import numpy as np
import cv2
ROOT=Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
QA=ROOT/"qa/architecture-bases-20261029"
g1=Image.open(QA/"gallery1_v13_B_right_passage_top_lowered_24px_REVIEW.png").convert("RGB")
g2=Image.open(QA/"gallery2_v04_architecture_matching_entrance_gallery1_REVIEW.png").convert("RGB")
v01=Image.open(QA/"gallery3_v01_matched_architecture_recess_side_door_REVIEW.png").convert("RGB")
E=Image.open(ROOT/"rooms/gallery3/gallery3_architecture_only_E.png").convert("RGB")
assert g1.size==v01.size==E.size==(930,582)
out=v01.copy()
black=(5,6,7)

# RECESSED WALL: make an actual deep floor alcove, rather than simply tinting
# the front wall. Back wall, ceiling, side returns, and floor have separated
# parallel planes. E's true front boundary x~270..682, and inner back-wall
# width x295..652 remain the authoritative shape.
# Floor inside the recess y178..222, sourced from already approved actual tiles.
inside_floor=g1.crop((295,220,655,264)).resize((360,44),Image.Resampling.BICUBIC)
out.paste(ImageEnhance.Brightness(inside_floor).enhance(.78),(295,178))
# Niche rear wallpaper + wood wainscot: two original wall panels compressed
# vertically (receding perspective) instead of a newly generated texture.
pieces=[]
for box in [(95,39,275,220),(348,39,528,220)]:
    # These two spans contain NO pillar: #2 rear exhibit stays unobstructed.
    pieces.append(g2.crop(box).resize((180,123),Image.Resampling.LANCZOS))
backwall=Image.new("RGB",(360,123))
backwall.paste(pieces[0],(0,0))
backwall.paste(pieces[1],(180,0))
# Feather the join so the two original light gradients don't make a seam.
raw=np.asarray(backwall).copy()
for ix in range(168,193):
    weight=(ix-168)/24
    a=raw[:,ix].astype(float)
    near=raw[:,ix-14].astype(float) if ix<180 else raw[:,ix+14].astype(float)
    raw[:,ix]=np.uint8(np.clip(np.rint(a*(.80+.20*weight)+near*(.20-.20*weight)),0,255))
backwall=ImageEnhance.Brightness(Image.fromarray(raw)).enhance(.76)
out.paste(backwall,(295,55))
dr=ImageDraw.Draw(out)
# Visible dark ceiling (front top edge x272-681 -> back x295-655);
# this is the depth plane approved in E, not a decorative frame.
dr.polygon([(275,39),(681,39),(654,55),(295,55)],fill=(28,22,17))
dr.line([(276,39),(678,39)],fill=(87,53,28),width=3)
dr.line([(294,55),(655,55)],fill=(122,78,41),width=2)
# Textured side returns, trapezoidal with deeper rear ends. Match wood
# material to approved columns; not closed wooden doors.
left_return=g1.crop((669,39,690,220)).resize((29,183),Image.Resampling.LANCZOS)
left_im=ImageEnhance.Brightness(left_return).enhance(.50)
mask=Image.new("L",(29,183),0)
ImageDraw.Draw(mask).polygon([(0,0),(28,16),(28,139),(0,182)],fill=255)
out.paste(left_im,(266,39),mask)
right_return=g1.crop((669,39,690,220)).resize((29,183),Image.Resampling.LANCZOS).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
right_im=ImageEnhance.Brightness(right_return).enhance(.46)
mask2=Image.new("L",(29,183),0)
ImageDraw.Draw(mask2).polygon([(28,0),(0,16),(0,139),(28,182)],fill=255)
out.paste(right_im,(654,39),mask2)
dr=ImageDraw.Draw(out)
# Side planes project forward across floor edges.
dr.polygon([(266,221),(295,178),(295,222),(280,243)],fill=(65,40,25))
dr.line([(266,221),(295,178)],fill=(177,122,74),width=3)
dr.line([(295,178),(295,220)],fill=(120,78,46),width=2)
dr.polygon([(654,178),(683,221),(677,243),(654,222)],fill=(60,36,24))
dr.line([(654,178),(683,221)],fill=(167,111,66),width=3)
dr.line([(654,178),(654,220)],fill=(119,77,45),width=2)
# A dark base shadow at the back-wall / niche-floor seam.
dr.line([(295,178),(654,178)],fill=(51,29,18),width=3)
dr.line([(296,181),(652,181)],fill=(145,91,52),width=1)
# Rear columns in front of side returns (the exact original approved art).
pillar=g1.crop((452,39,484,220))
for x in [248,681]:
    out.paste(pillar,(x,39))

# EAST EXIT: no door. Restore right-facing wall return from real approved
# wall pixels, cut a readable corridor through that wall toward screen-right.
# Build the sided wall first, so the carved closed door in v01 is fully removed.
def warp(tile,pts):
    arr=np.asarray(tile.convert("RGB"))
    h,w=arr.shape[:2]
    H=cv2.getPerspectiveTransform(np.float32([[0,0],[w-1,0],[w-1,h-1],[0,h-1]]),np.float32(pts))
    mapped=cv2.warpPerspective(arr,H,(930,582),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
    alpha=cv2.warpPerspective(np.full((h,w),255,np.uint8),H,(930,582),flags=cv2.INTER_NEAREST)
    return Image.fromarray(mapped),Image.fromarray(alpha)
# All of original right wall and door are cleared using actual floor pixels
# and backdrop from gallery1, not painted-over with a new synthetic artwork.
# Partial side wall retains shape x807->front and the cutout on its right.
out.paste(g1.crop((790,220,930,537)),(790,220))
# Floor corridor is direct, uninterrupted floor from established game artwork:
# x826-929, y290-500 uses same row of tiled floor shifted from x680..783.
reused_floor=g1.crop((681,286,785,508))
out.paste(reused_floor,(826,286))
dr=ImageDraw.Draw(out)
# Right wall's upper lintel, a wooden projection above the corridor.
sidewall=g1.crop((76,42,221,219))
wall_im,wall_mask=warp(sidewall,[(806,219),(929,219),(929,284),(806,281)])
out.paste(wall_im,(0,0),wall_mask)
# The left jamb extends to the bottom of the sidewall, leaving a clear
# rightward floor exit x834..929.
jamb=g1.crop((452,39,484,220)).resize((28,253),Image.Resampling.LANCZOS)
out.paste(jamb,(806,259))
dr=ImageDraw.Draw(out)
dr.line([(806,220),(806,508),(825,512)],fill=(67,38,21),width=5)
dr.line([(815,275),(815,496)],fill=(174,113,68),width=2)
dr.line([(834,282),(929,284)],fill=(153,99,55),width=5)
dr.line([(834,288),(929,290)],fill=(67,38,21),width=2)
# Right corridor occupies x834..929, y290..508 and reaches image right edge.
# Above it, black perimeter, below it full floor smoothly joins the gallery.
dr.rectangle((920,16,929,218),fill=black)
# Clear any residual dark-right edge from base v01 to leave actual open floor.
out.paste(g1.crop((826,508,930,566)),(826,508))
# A shadow cast by the wall across the threshold is small, never a carpet.
shadow=Image.new("RGBA",out.size,(0,0,0,0))
sd=ImageDraw.Draw(shadow)
for y in range(288,299):
    sd.line([(835,y),(929,y)],fill=(18,12,9,max(0,38-3*(y-288))),width=1)
out=Image.alpha_composite(out.convert("RGBA"),shadow).convert("RGB")

# South center remains the approved E entry to gallery1.
before=np.asarray(v01)
after=np.asarray(out)
assert out.size==(930,582)
assert np.array_equal(after[260:550,60:790],before[260:550,60:790]),"Center floor unexpectedly edited"
assert np.array_equal(after[566:582],before[566:582]),"South entrance/border unexpectedly altered"
assert np.array_equal(after[39:220,248:280],np.asarray(pillar)), "Left inner column altered"
assert np.array_equal(after[39:220,681:713],np.asarray(pillar)), "Right inner column altered"
assert np.linalg.norm(after[65,314].astype(float)-after[65,90].astype(float))>8, "Niche lacks light gradient"
print("RECESS BRIGHTNESS",float(np.mean(after[73:145,325:640])), "FRONT",float(np.mean(after[73:145,85:200])))
assert float(np.mean(after[73:145,325:640])) < float(np.mean(after[73:145,85:200]))+10, "Recess unexpectedly brighter"
assert not np.array_equal(after[190:220,326:630],before[190:220,326:630]), "Niche floor absent"
assert np.max(after[75:137,430:525].mean(axis=2))<115,"Rear center has light-colored pillar/artifact obstructing exhibit 2"
assert np.array_equal(after[330:455,850:930],np.asarray(g1)[330:455,705:785]), "East exit must be uncovered tiled floor"
assert np.count_nonzero(np.any(after[235:525,800:930] != before[235:525,800:930],axis=2))>5000, "Door was not removed"
name="gallery3_v02_deep_recess_open_east_passage_REVIEW.png"
out.save(QA/name)
comparison=Image.new("RGB",(1860,624),"#242729")
comparison.paste(v01,(0,42));comparison.paste(out,(930,42))
dr=ImageDraw.Draw(comparison);dr.rectangle((0,0,1859,41),fill="#242729")
dr.text((12,14),"v01 / flat alcove + wooden side door",fill="white")
dr.text((942,14),"v02 / deep alcove + OPEN east passage",fill="white")
comparison.save(QA/"gallery3_v01_vs_v02_recess_east_corridor_COMPARISON.png")
print("PASS gallery3 v02: deep recess and door-free east passage")
print(name)
