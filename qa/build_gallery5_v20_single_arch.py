"""A18 gallery5 v20 – remove competing depth arch; single forward oblique portal.
Only the left/right front-wall architecture changes. The v16-approved three-frame
geometry, the v18 stone floor and runner, and the E original are kept untouched.
No AI imagery, no flat door-sprite rotation, no gameplay integration.
"""
from pathlib import Path
import math, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
R=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
D=R/"architecture-review/entrance-gallery5-comparison"
SOURCE=Path(r"C:\Users\User\source\repos\web-tools-preview-a18-entrance-2d-assets-20261028\a18\layout-test\assets\entrance\approved_initial_20261027\entrance_background_initial_approved.png")
src=Image.open(SOURCE).convert("RGB")
prior=Image.open(D/"gallery5-v18.png").convert("RGB")
W,H=prior.size; SCALE=3
assert (W,H)==(930,582)
# Source authentic near-wall surface BEFORE side passages are drawn in v14.
source=(R/"qa/build_gallery5_v14_entrance_view_frames.py").read_text(encoding="utf-8-sig")
key="# Side corridor openings:"
assert key in source
scope={"__name__":"a18_gallery5_sidewall_restore"}
exec(compile(source.split(key)[0],"a18 source wall before portal","exec"),scope)
blank=scope["out"].convert("RGB")
out=prior.copy()
def poly_mask(points):
    mask=Image.new("L",(W*SCALE,H*SCALE),0)
    ImageDraw.Draw(mask).polygon([(int(x*SCALE),int(y*SCALE)) for x,y in points],fill=255)
    return mask.resize((W,H),Image.Resampling.LANCZOS)
def fill_tex(target,polygon,rgb):
    target.paste(rgb,(0,0),poly_mask(polygon))
def bezier(a,b,c,d,n=36):
    return [((1-t)**3*a[0]+3*(1-t)**2*t*b[0]+3*(1-t)*t*t*c[0]+t**3*d[0],
             (1-t)**3*a[1]+3*(1-t)**2*t*b[1]+3*(1-t)*t*t*c[1]+t**3*d[1])
            for t in np.linspace(0,1,n)]
def arch(outer=False):
    # Shoulder line has a 30px oblique incline; near-left stands lower.
    if outer:
      return bezier((20,348),(25,309),(69,277),(99,282))+bezier((99,282),(133,283),(154,296),(156,315))
    return bezier((37,357),(45,320),(76,295),(100,300))+bezier((100,300),(123,302),(140,310),(143,328))
def mirror_points(poly):return [(W-x,y) for x,y in poly]
# Rebuild BOTH mouths from the actual wall; old front-facing arch is completely removed.
remove=[(0,268),(160,268),(160,553),(0,582)]
for poly in (remove,mirror_points(remove)):
    out.paste(blank,(0,0),poly_mask(poly))
# Coloured real wood grain from approved entrance carpentry.
wood=src.crop((80,402,495,506)).resize((W,H),Image.Resampling.BICUBIC)
arr=np.asarray(wood).astype(np.float32)
gray=arr@np.array([.30,.59,.11],np.float32)
tone=np.stack((84+(gray-115)*.37,53+(gray-115)*.31,32+(gray-115)*.24),axis=2)
wood=Image.fromarray(np.uint8(np.clip(tone,0,255)))
for flipped in (False,True):
    X=(lambda points:mirror_points(points)) if flipped else (lambda points:points)
    def P(x,y):return (W-x,y) if flipped else (x,y)
    outer=arch(True); inner=arch(False)
    shell=outer+[(156,537),(22,572)]
    # Wood opening is one genuine side-wall hole, not a pasted doorway.
    fill_tex(out,X(shell),wood)
    interior=inner+[(143,531),(39,557)]
    dark=Image.new("RGB",(W,H),(8,17,18))
    fill_tex(out,X(interior),dark)
    dr=ImageDraw.Draw(out)
    # Corridor disappears westwards; floor, wall return and curved ceiling share
    # one perspective. The underside of the arch is a CURVED OFFSET SURFACE,
    # not a filled flat triangular cap.
    dr.polygon(X([(40,378),(82,359),(99,372),(100,509),(39,552)]),fill="#111c1c")
    dr.polygon(X([(44,376),(63,377),(71,506),(42,540)]),fill="#15221f")
    # One continuous undersurface, not a second receding arch line:
    # the inner opening is progressively darkened only immediately behind
    # its front fascia. The "rear arch" outlines from v19 are gone.
    # Keep this narrow shaded soffit subdued and completely unoutlined.
    soffit_near=inner[7:-7]
    soffit_far=[(x-8,y+8) for x,y in soffit_near]
    dr.polygon(X(soffit_near+list(reversed(soffit_far))),fill="#22201b")
    # The distant ceiling is black/dark teal without any bright rim competing
    # with the front architectural arch.
    # Wall return is separate from the front frame; its base meets the sill.
    # Deep wine-red return at the RIGHT jamb is a single flat wall plane:
    # its top is hidden behind the arch and its leading edge stays behind
    # the inner opening. No duplicate arch-shaped line is painted here.
    dr.polygon(X([(140,343),(113,366),(111,515),(141,530)]),fill="#462529")
    dr.line([P(114,368),P(112,512)],fill="#26191b",width=3)
    dr.line([P(139,347),P(137,526)],fill="#794033",width=2)
    # Opposite return: narrow oak-shadow wedge, no overlay across the arch.
    dr.polygon(X([(38,364),(29,378),(26,540),(39,554)]),fill="#38291f")
    dr.line([P(34,381),P(32,543)],fill="#715035",width=2)
    # Real entrance stone foreshortened in four-point perspective, with joints.
    floor_poly=[(39,539),(101,511),(142,531),(22,566)]
    stone=src.crop((110,540,410,698)).resize((135,90),Image.Resampling.LANCZOS)
    stonearr=np.asarray(stone,dtype=np.float32)
    stonearr=np.uint8(np.clip(stonearr*np.array([.47,.46,.45])[None,None,:]-5,12,180))
    hh,ww=stonearr.shape[:2]
    source_quad=np.float32([[0,0],[ww-1,0],[ww-1,hh-1],[0,hh-1]])
    target_quad=np.float32(X([(39,539),(101,511),(142,531),(22,566)]))
    matr=cv2.getPerspectiveTransform(source_quad,target_quad)
    dst=cv2.warpPerspective(stonearr,matr,(W,H),flags=cv2.INTER_CUBIC)
    stain=Image.fromarray(dst)
    out.paste(stain,(0,0),poly_mask(X(floor_poly)))
    dr=ImageDraw.Draw(out)
    dr.line([P(44,535),P(102,517)],fill="#756554",width=1)
    dr.line([P(39,555),P(141,531)],fill="#ae926b",width=2)
    dr.line([P(24,570),P(155,538)],fill="#332116",width=5)
    # Side wall FRONT surface: wood has actual grain and physically thick jambs.
    # Inclined jamb bases follow the same oblique floor/foot line as near wall.
    dr.line([P(22,356),P(22,567)],fill="#2f1d14",width=11)
    dr.line([P(25,356),P(24,562)],fill="#997047",width=4)
    dr.line([P(151,329),P(152,538)],fill="#251812",width=6)
    dr.line([P(150,332),P(150,534)],fill="#986c40",width=2)
    # Oblique arch carved as a SINGLE curved band of the same walnut facade:
    # near-left arch shoulder descends 30px relative to far-right shoulder.
    # No horizontal/symmetric/front-facing semicircular border survives.
    o=X(outer); i=X(inner)
    dr.line(o,fill="#291c15",width=15,joint="curve")
    dr.line(o,fill="#936842",width=11,joint="curve")
    dr.line(o,fill="#c19a67",width=3,joint="curve")
    # Inner edge is a single subdued contact shadow, not another bright
    # outline that could be misread as an additional arch behind the first.
    dr.line(i,fill="#241b15",width=3,joint="curve")
    # Very fine light from the room side belongs to the FRONT frame only.
    highlight=[(x+1,y+2) for x,y in outer]
    dr.line(X(highlight),fill="#87603c",width=1,joint="curve")
    # Cast shadow anchored to stone sill and the near wall foot.
    dr.line([P(18,568),P(155,534)],fill="#1f1712",width=3)
# Reapply the real v18 front-wall edge where an opening touches the inner pier:
# the center frames and stone main-floor must stay pixel-identical.
for box in ((190,0,746,582),):
    assert ImageChops.difference(prior.crop(box),out.crop(box)).getbbox() is None
# E original never touched. Save only new, separate, unapproved review assets.
for p in (D/"gallery5-v20.png",
          R/"architecture-review/gallery5/gallery5_v20_single_arched_portals_REVIEW.png",
          R/"rooms/gallery5/gallery5_palace_E_material_v20_REVIEW.png"):
    out.save(p,optimize=True)
print("SAVED v20; changed bbox:",ImageChops.difference(prior,out).getbbox())