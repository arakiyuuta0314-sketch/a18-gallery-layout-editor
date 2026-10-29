"""Build true adjustable Gallery5 assets from the existing v14 construction.
No AI-rendered substitutes; E and v14 canonical files are never modified.
"""
from pathlib import Path
from PIL import Image, ImageChops, ImageFilter
import numpy as np
ROOT=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
OUT=ROOT/"architecture-review/entrance-gallery5-comparison/frame-adjuster"
OUT.mkdir(parents=True,exist_ok=True)
source=(ROOT/"qa/build_gallery5_v14_entrance_view_frames.py").read_text(encoding="utf-8-sig")
targets=[
    "frame_at(190,76,133,202,1)",
    "frame_at(329,68,270,210,2)",
    "frame_at(605,76,133,202,3)",
]
for t in targets:
    assert source.count(t)==1,(t,source.count(t))
    source=source.replace(t,"# bare backdrop: "+t)
marker="# save review output, never mutate E source or room.json"
assert source.count(marker)==1
source=source.split(marker)[0]+"""
out.save(r'C:\\Users\\User\\source\\repos\\a18-gallery5-material-review\\architecture-review\\entrance-gallery5-comparison\\frame-adjuster\\gallery5_unframed.png',optimize=True)
"""
# Execute the actual same v14 materials pipeline without the three frame draws.
namespace={"__name__":"gallery5_unframed"}
exec(compile(source,"gallery5 v14 materials without frames","exec"),namespace)
bare=Image.open(OUT/"gallery5_unframed.png").convert("RGB")
v14=Image.open(ROOT/"architecture-review/entrance-gallery5-comparison/gallery5-v14.png").convert("RGB")
specs=[
    ("left",(190,76,133,202)),
    ("center",(329,68,270,210)),
    ("right",(605,76,133,202)),
]
for name,(x,y,w,h) in specs:
    # 7 px padding captures the authentic dark shadow below the gold border.
    box=(x-6,y-5,x+w+8,y+h+9)
    crop=v14.crop(box)
    under=bare.crop(box)
    delta=np.asarray(ImageChops.difference(crop,under).convert("RGB")).max(axis=2)
    # Hard mask in the real gilded/artwork region, softened only on natural shadow edges.
    alpha=np.where(delta>=14,255,np.where(delta>=4,np.clip((delta-4)/10*255,0,255),0)).astype(np.uint8)
    alpha=Image.fromarray(alpha,"L").filter(ImageFilter.GaussianBlur(.45))
    rgba=crop.convert("RGBA")
    rgba.putalpha(alpha)
    rgba.save(OUT/f"frame_{name}.png",optimize=True)
print("ASSETS:",OUT)
for p in sorted(OUT.glob("*.png")):
    print(p.name,Image.open(p).size,p.stat().st_size)
