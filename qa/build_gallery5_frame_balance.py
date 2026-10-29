"""A18 Gallery 5: actual-material proportion comparison for a +60px lower edge.
Options are UNAPPROVED review candidates. Uses original 3 frame sprites;
approved E and gameplay remain untouched.
"""
from PIL import Image
from pathlib import Path
import json
R=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
AS=R/"architecture-review/entrance-gallery5-comparison/frame-adjuster"
OUT=R/"architecture-review/entrance-gallery5-comparison/frame-balance"
OUT.mkdir(exist_ok=True)
W,H=930,582
base=Image.open(AS/"gallery5_unframed.png").convert("RGB")
sources={n:Image.open(AS/f"frame_{n}.png").convert("RGBA") for n in ("left","center","right")}
original={
 "left":{"x":190,"y":76,"w":133,"h":202,"padX":6,"padY":5},
 "center":{"x":329,"y":68,"w":270,"h":210,"padX":6,"padY":5},
 "right":{"x":605,"y":76,"w":133,"h":202,"padX":6,"padY":5},
}
options=[
 ("a_full_extension","A｜上端を固定して60px延長",{"left":(76,262),"center":(68,270),"right":(76,262)}),
 ("b_original_ratio","B｜元の縦横比を維持し、下へ60px移動",{"left":(136,202),"center":(128,210),"right":(136,202)}),
 ("c_compromise","C｜30px下へ移動＋30px延長（折衷）",{"left":(106,232),"center":(98,240),"right":(106,232)})
]
def make_wall(extra=60):
    out=base.copy()
    # Shift only the back wall/floor seam, leaving side corridors (x outside 184..746) intact.
    l,r=184,746;ww=r-l
    walnut=base.crop((l,224,r,286)).resize((ww,extra+6),Image.Resampling.BICUBIC)
    out.paste(walnut,(l,280))
    floor=base.crop((l,292,r,582)).resize((ww,290-extra),Image.Resampling.BICUBIC)
    out.paste(floor,(l,292+extra))
    trim=base.crop((l,286,r,292))
    out.paste(trim,(l,286+extra))
    return out
def material_frame(sprite,extra):
    if extra==0:return sprite
    if extra<0:raise ValueError(extra)
    w,h=sprite.size
    top,bottom=43,39
    middle=sprite.crop((0,top,w,h-bottom)).resize((w,h-top-bottom+extra),Image.Resampling.BICUBIC)
    result=Image.new("RGBA",(w,h+extra),(0,0,0,0))
    result.alpha_composite(sprite.crop((0,0,w,top)),(0,0))
    result.alpha_composite(middle,(0,top))
    result.alpha_composite(sprite.crop((0,h-bottom,w,h)),(0,h-bottom+extra))
    return result
records=[]
for slug,title,specs in options:
    canvas=make_wall()
    rects={}
    for n in ("left","center","right"):
        o=original[n];y,h=specs[n];extra=h-o["h"]
        # x and width are unchanged. Only top or height change.
        frame=material_frame(sources[n],extra)
        canvas.paste(frame,(o["x"]-o["padX"],y-o["padY"]),frame)
        rects[n]={"x":o["x"],"y":y,"w":o["w"],"h":h,"bottom":y+h,"aspect":round(o["w"]/h,3)}
    assert {r["bottom"] for r in rects.values()}=={338}
    assert canvas.size==(930,582)
    path=OUT/f"{slug}.png";canvas.save(path,optimize=True)
    print(slug,title,"image",path.stat().st_size,"rects",rects)
    records.append({"id":slug,"title":title,"image":path.name,"rects":rects})
(OUT/"variants.json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
