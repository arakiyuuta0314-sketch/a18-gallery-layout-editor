"""Gallery5 v16: original E visual hierarchy; center hangs above AND below the side frames.
Based on the v15 central-emphasis preview. Center stays 270x240 (y=98..338),
side frames keep the same top y=133 but finish at 324 so the center extends
14px below both. No approved E, side corridors, room ids, or gameplay changes.
Uses extracted real v14 frame sprites; E and gameplay remain untouched.
"""
from pathlib import Path
from PIL import Image,ImageChops
import json
R=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
AS=R/"architecture-review/entrance-gallery5-comparison/frame-adjuster"
BAL=R/"architecture-review/entrance-gallery5-comparison/frame-balance"
R15=R/"rooms/gallery5"
ARCH=R/"architecture-review/gallery5"
src={n:Image.open(AS/f"frame_{n}.png").convert("RGBA") for n in ("left","center","right")}
base=Image.open(AS/"gallery5_unframed.png").convert("RGB")
C=Image.open(BAL/"c_compromise.png").convert("RGB")
W,H=base.size
assert (W,H)==(930,582)
def backwall(extra=60):
    output=base.copy()
    l,r=184,746;ww=r-l
    output.paste(base.crop((l,224,r,286)).resize((ww,extra+6),Image.Resampling.BICUBIC),(l,280))
    output.paste(base.crop((l,292,r,582)).resize((ww,290-extra),Image.Resampling.BICUBIC),(l,292+extra))
    output.paste(base.crop((l,286,r,292)),(l,286+extra))
    return output
def resize_real_frame(sprite,targetW,extraH):
    w,h=sprite.size
    cap_top,cap_bot=43,39
    mid=sprite.crop((0,cap_top,w,h-cap_bot)).resize((w,h-cap_top-cap_bot+extraH),Image.Resampling.BICUBIC)
    result=Image.new("RGBA",(w,h+extraH))
    result.alpha_composite(sprite.crop((0,0,w,cap_top)),(0,0))
    result.alpha_composite(mid,(0,cap_top))
    result.alpha_composite(sprite.crop((0,h-cap_bot,w,h)),(0,h-cap_bot+extraH))
    # Horizontal change is modest (~6%) and applies to each real frame sprite.
    actualW=targetW+14
    return result.resize((actualW,h+extraH),Image.Resampling.LANCZOS)
# The large central frame is 35 px ABOVE and 14 px BELOW the side pair.
# Keep the center image proportions and its established bottom at 338.
# Lower side ends are raised, not the central frame stretched into a square.
specs={
 "left":{"x":197,"y":133,"w":125,"h":191},
 "center":{"x":329,"y":98,"w":270,"h":240},
 "right":{"x":608,"y":133,"w":125,"h":191}
}
original={"left":(133,202),"center":(270,210),"right":(133,202)}
out=backwall()
for name in ("left","center","right"):
    rect=specs[name];oldW,oldH=original[name]
    frame=resize_real_frame(src[name],rect["w"],rect["h"]-oldH)
    out.paste(frame,(rect["x"]-6,rect["y"]-5),frame)
assert specs["left"]["y"]==specs["right"]["y"]==133
assert specs["left"]["y"]+specs["left"]["h"]==324
assert specs["right"]["y"]+specs["right"]["h"]==324
assert specs["center"]["y"]==98 and specs["center"]["y"]+specs["center"]["h"]==338
assert specs["center"]["y"]<specs["left"]["y"] and specs["center"]["y"]+specs["center"]["h"]>specs["left"]["y"]+specs["left"]["h"]
assert specs["left"]["x"]+specs["left"]["w"]<specs["center"]["x"]
assert specs["center"]["x"]+specs["center"]["w"]<specs["right"]["x"]
assert specs["right"]["x"]+specs["right"]["w"]<746
# Pixel-identical at the architectural side planes.
for box in [(0,0,184,H),(746,0,W,H)]:
    assert ImageChops.difference(C.crop(box),out.crop(box)).getbbox() is None
p=BAL/"e_central_projection_v16.png"
out.save(p,optimize=True)
( R/"architecture-review/entrance-gallery5-comparison/gallery5-v16.png" ).write_bytes(p.read_bytes())
q=ARCH/"gallery5_v16_central_projection_REVIEW.png";out.save(q,optimize=True)
r=R15/"gallery5_palace_E_material_v16_REVIEW.png";out.save(r,optimize=True)
metadata={
 "schema":"a18-gallery5-frame-balance/v16",
 "base":"v15 (center 270x240 unchanged); side bottom raised by 14 px",
 "status":"UNAPPROVED",
 "canvas":{"width":930,"height":582},
 "rects":{n:{**v,"bottom":v["y"]+v["h"]} for n,v in specs.items()},
 "sideCorridorsChanged":False,
 "approvedEChanged":False}
(BAL/"v16_layout.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding="utf-8")
print("saved",p,p.stat().st_size,"C diff",ImageChops.difference(out,Image.open(BAL/"d_central_emphasis_v15.png").convert("RGB")).getbbox())
print(json.dumps(specs,ensure_ascii=False))