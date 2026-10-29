"""Gallery5 v17 actual-material architecture refinement.
Based on v16; frame masks, passage wall geometry and approved E are immutable.
Replace synthetic grey floor with genuine entrance stone, rework runner with
real woven rug pixels, match side threshold to stone, add physical contact shadows.
Only gallery material PNGs and QA are emitted; no gameplay changes.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import numpy as np, cv2
R=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
V=Image.open(R/"architecture-review/entrance-gallery5-comparison/gallery5-v16.png").convert("RGB")
SRC=Image.open(r"C:\Users\User\source\repos\web-tools-preview-a18-entrance-2d-assets-20261028\a18\layout-test\assets\entrance\approved_initial_20261027\entrance_background_initial_approved.png").convert("RGB")
LV6=Image.open(R/"architecture-review/entrance-comparison/entrance-lv6-approved.png").convert("RGB")
E=Image.open(R/"rooms/gallery5/gallery5_palace_E.png").convert("RGB")
W,H=V.size
assert (W,H)==(930,582)
def mask_poly(points):
    m=Image.new("L",(W,H),0)
    ImageDraw.Draw(m).polygon(points,fill=255)
    return m
def warped(src,quad):
    ar=np.array(src.convert("RGB"));h,w=ar.shape[:2]
    m=cv2.getPerspectiveTransform(np.float32([[0,0],[w-1,0],[w-1,h-1],[0,h-1]]),np.float32(quad))
    im=cv2.warpPerspective(ar,m,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT_101)
    ma=cv2.warpPerspective(np.ones((h,w),np.uint8)*255,m,(W,H))
    return Image.fromarray(im),Image.fromarray(ma)
def recolour(im,scale,bias):
    arr=np.asarray(im.convert("RGB")).astype(np.float32)
    arr=arr*np.array(scale)[None,None,:]+np.array(bias)[None,None,:]
    return Image.fromarray(np.uint8(np.clip(arr,0,255)))
out=V.copy()
# -------------------------------------------------------------------
# 1. Entrance's actual tile & highlights, not a flat gradient or generated noise.
# The chosen raw-source range starts at the rear floor and keeps perspective grout joints.
stone=SRC.crop((0,516,1322,892)).resize((W,H-350),Image.Resampling.LANCZOS)
stone=recolour(stone,(.84,.83,.82),(-6,-5,-2))
tile=Image.new("RGB",(W,H));tile.paste(stone,(0,350))
ground=[(184,350),(746,350),(746,545),(930,582),(0,582),(184,545)]
out.paste(tile,(0,0),mask_poly(ground))
# Rear skirting cast shadow, realistic anchored base.
over=Image.new("RGBA",(W,H),(0,0,0,0));dr=ImageDraw.Draw(over)
for yy in range(350,372):
    t=(yy-350)/22
    dr.line((185,yy,745,yy),fill=(24,12,7,int(85*(1-t)**2)),width=1)
out=Image.alpha_composite(out.convert("RGBA"),over).convert("RGB")
# Walnut base moulding from actual approved entrance (dark bevel + metallic thread).
wood=SRC.crop((68,494,507,515)).resize((562,14),Image.Resampling.LANCZOS)
wood=recolour(wood,(.88,.78,.65),(-8,-5,1))
out.paste(wood,(184,341))
p=ImageDraw.Draw(out)
p.line((184,352,746,352),fill="#291913",width=3)
p.line((184,354,746,354),fill="#b88e5c",width=1)
# -------------------------------------------------------------------
# 2. Original geometry and edge ornament; replace the flat dark carpet interior
# with real Lv6 red wool texture. Preserve its 4-sided perspective and gilded edges.
# A cast shadow under the runner creates material contact with the stone.
shadow=Image.new("RGBA",(W,H),(0,0,0,0))
ImageDraw.Draw(shadow).polygon([(420,350),(510,350),(617,582),(311,582)],fill=(24,7,6,90))
shadow=shadow.filter(ImageFilter.GaussianBlur(8))
out=Image.alpha_composite(out.convert("RGBA"),shadow).convert("RGB")
# Preserve all previously approved carpet border pixels in their exact positions.
carpet_outer=[(422,354),(509,354),(611,582),(319,582)]
out.paste(V,(0,0),mask_poly(carpet_outer))
# Copy genuine wool from the Lv6 runner, not UI or character pixels.
wool=LV6.crop((607,495,652,696)).convert("RGB")
wa=np.asarray(wool)
weave=np.concatenate([wa,wa[:,::-1,:],wa],axis=1)
wool=Image.fromarray(weave).resize((136,234),Image.Resampling.BICUBIC)
# Muted garnet tone distinguishes the last room while retaining real fabric streaks.
wool=recolour(wool,(.79,.66,.83),(3,1,18))
topL,topR=(438,361),(492,361)
bottomR,bottomL=(572,582),(359,582)
warp,alpha=warped(wool,[topL,topR,bottomR,bottomL])
inside=mask_poly([topL,topR,bottomR,bottomL])
al=np.minimum(np.array(alpha),np.array(inside)).astype("uint8")
out.paste(warp,(0,0),Image.fromarray(al))
p=ImageDraw.Draw(out)
# Linen-gold side binding and inset stitch, both on the existing runner outline.
p.line([(436,360),(351,582)],fill="#b89869",width=2)
p.line([(494,360),(581,582)],fill="#b89869",width=2)
p.line([(442,367),(366,582)],fill="#60313c",width=2)
p.line([(488,367),(566,582)],fill="#60313c",width=2)
# retain the 4 quiet rosettes / stitch marks from the E design.
for yy in (394,432,482,542):
    t=(yy-354)/(582-354)
    lx=438+(359-438)*t;rx=492+(572-492)*t
    p.line((lx+8,yy,rx-8,yy),fill="#b18b57",width=1)
    mid=(lx+rx)/2
    p.polygon([(mid,yy-4),(mid+3,yy),(mid,yy+4),(mid-3,yy)],outline="#d1a66c")
# -------------------------------------------------------------------
# 3. Side thresholds: warm stone only at the LIP of the existing passage.
# Never cover the dark inner corridor or the red wall returns with a bright slab.
for mirror in (False,True):
    def P(x,y):return (W-x,y) if mirror else (x,y)
    # Narrow threshold, where the passage floor meets the public gallery floor.
    threshold=[P(0,520),P(42,539),P(143,515),P(143,528),P(43,550),P(0,536)]
    tex=SRC.crop((97,577,392,698)).resize((123,46),Image.Resampling.LANCZOS)
    tex=recolour(tex,(.66,.65,.63),(-6,-6,-3))
    img,m=warped(tex,[P(0,520),P(42,539),P(143,528),P(0,536)])
    m=Image.fromarray(np.minimum(np.array(m),np.array(mask_poly(threshold))))
    out.paste(img,(0,0),m)
    dr=ImageDraw.Draw(out)
    dr.line([P(42,539),P(143,515)],fill="#322116",width=6)
    dr.line([P(42,536),P(143,513)],fill="#aa8456",width=2)
    dr.line([P(0,531),P(40,548)],fill="#594334",width=2)
# -------------------------------------------------------------------
# v16 frames (including their real gilded shadows) must be pixel-identical.
frame_rois=[(190,130,329,330),(325,95,603,345),(602,130,741,330)]
for b in frame_rois:out.paste(V.crop(b),b[:2])
# No edits permitted to title/arched crown region or central frame.
assert ImageChops.difference(out.crop((325,95,603,345)),V.crop((325,95,603,345))).getbbox() is None
assert ImageChops.difference(out.crop((190,130,329,330)),V.crop((190,130,329,330))).getbbox() is None
assert ImageChops.difference(out.crop((602,130,741,330)),V.crop((602,130,741,330))).getbbox() is None
# Comparison only: no change to E, v16, room.json or game files.
for dest in [
 R/"architecture-review/entrance-gallery5-comparison/gallery5-v17.png",
 R/"architecture-review/gallery5/gallery5_v17_stone_wool_material_REVIEW.png",
 R/"rooms/gallery5/gallery5_palace_E_material_v17_REVIEW.png"
]:
    out.save(dest,optimize=True)
print("v17 saved; changed bounding box",ImageChops.difference(out,V).getbbox(), "E",E.size)