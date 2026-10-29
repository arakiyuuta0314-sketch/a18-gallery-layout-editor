"""Gallery5 v18 material detailing review: true wood trim and burgundy wall inset.
Built over the stone/wool v17; no changes to 3 approved-size frame images,
side corridor geometry, carpet silhouette, or movement data.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFilter
import numpy as np,math
R=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
src=Image.open(r"C:\Users\User\source\repos\web-tools-preview-a18-entrance-2d-assets-20261028\a18\layout-test\assets\entrance\approved_initial_20261027\entrance_background_initial_approved.png").convert("RGB")
prior=Image.open(R/"architecture-review/entrance-gallery5-comparison/gallery5-v17.png").convert("RGB")
out=prior.copy(); W,H=out.size
def shade(im,col,alpha=.75):
  arr=np.asarray(im.convert("RGB")).astype(np.float32)
  intensity=(arr @ np.array([.30,.59,.11])).astype(np.float32)
  light=(intensity-115)*.48
  made=np.clip(np.array(col)[None,None,:]+light[:,:,None],0,255)
  arr=arr*(1-alpha)+made*alpha
  return Image.fromarray(np.uint8(np.clip(arr,0,255)))
# 1. Genuine matte wall surface, using the approved entrance's natural lighting gradation.
# Restrict to the inner burgundy recess; original gold motif stays on top.
texture=src.crop((70,110,310,365)).resize((92,109),Image.Resampling.LANCZOS)
texture=shade(texture,(94,40,54),.99)
for x in (53,785):
    out.paste(texture,(x,73))
    # No inventing decorative motif; retain the two already present gilded figures from v16.
    for mx in (x+15,x+74):
        # Preserve only original gold strokes, not the rectangular maroon patches.
        patch=prior.crop((mx-5,82,mx+7,116))
        pa=np.asarray(patch).astype(np.int16)
        gold=(pa[:,:,0]>110)&(pa[:,:,1]>70)&(pa[:,:,2]<130)&(pa[:,:,0]>pa[:,:,1]*1.1)
        mask=Image.fromarray(np.uint8(gold)*255,"L")
        out.paste(patch,(mx-5,82),mask)
    dr=ImageDraw.Draw(out)
    # Existing carved upper and lower wood stops have a metallic lighting edge.
    dr.line((x,73,x+91,73),fill="#b38755",width=2)
    dr.line((x+1,181,x+91,181),fill="#42241a",width=3)
    dr.line((x+91,75,x+91,178),fill="#3e221c",width=3)
    dr.line((x+2,75,x+2,178),fill="#b0804e",width=2)
# 2. Trace existing wooden portal moulding using authentic carved wood grain.
# Arc and jamb positions stay identical, so this is NOT a front-facing door pasted on its side.
wood=src.crop((72,414,310,505)).resize((184,260),Image.Resampling.LANCZOS)
wood=shade(wood,(112,67,35),.52)
for right in (False,True):
    def P(x,y):return (W-x,y) if right else (x,y)
    mask=Image.new("L",(W,H),0);md=ImageDraw.Draw(mask)
    tt=np.linspace(math.pi,0,85) if False else [math.pi*i/84 for i in range(84,-1,-1)]
    arc=[P(91+63*math.cos(t),284+43*(1-math.sin(t))) for t in tt]
    md.line(arc,fill=108,width=9,joint="curve")
    md.line([P(30,327),P(30,512)],fill=110,width=7)
    md.line([P(151,328),P(151,512)],fill=100,width=7)
    layer=Image.new("RGB",(W,H))
    section=wood.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if right else wood
    layer.paste(section,(746 if right else 0,278))
    out.paste(layer,(0,0),mask)
# On the real wood edge, reproduce restrained highlights already present in v16.
for right in (False,True):
    def P(x,y):return (W-x,y) if right else (x,y)
    d=ImageDraw.Draw(out)
    # lines follow the current portal opening, without adding a new arch or floor structure
    d.line([P(36,329),P(36,512)],fill="#b08352",width=2)
    d.line([P(149,333),P(149,511)],fill="#b78e5c",width=2)
# keep the actual frame imagery exactly: never repaint pixels inside the frames.
v16=Image.open(R/"architecture-review/entrance-gallery5-comparison/gallery5-v16.png").convert("RGB")
for b in [(190,130,329,330),(325,95,603,345),(602,130,741,330)]:
    assert ImageChops.difference(out.crop(b),prior.crop(b)).getbbox() is None,b
# No pixel may change in the main central gallery floor or runner.
assert ImageChops.difference(out.crop((185,350,745,582)),prior.crop((185,350,745,582))).getbbox() is None
for p in (R/"architecture-review/entrance-gallery5-comparison/gallery5-v18.png",
          R/"architecture-review/gallery5/gallery5_v18_wall_portal_material_REVIEW.png",
          R/"rooms/gallery5/gallery5_palace_E_material_v18_REVIEW.png"):
    out.save(p,optimize=True)
print("v18 saved",ImageChops.difference(out,prior).getbbox())
