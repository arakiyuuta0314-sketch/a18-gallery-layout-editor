"""Create review-only visual montage of approved architectural-only rooms 2-5."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa/architecture-bases-20261029/gallery2to5_architecture_overview.png'
files=[
 ("展示室2｜A・奥2枠除去",ROOT/'rooms/gallery2/architecture_only_v01.png'),
 ("展示室3｜G・奥3枠除去",ROOT/'rooms/gallery3/gallery3_architecture_only_E.png'),
 ("展示室4｜A・奥4枠除去",ROOT/'rooms/gallery4/architecture_only_A.png'),
 ("展示室5｜E・奥3枠除去",ROOT/'rooms/gallery5/gallery5_palace_architecture_fixed_E_v01.png'),
]
w,h=650,407
margin,gutter,head=18,24,37
image=Image.new("RGB",(2*w+2*margin+gutter,2*(h+head)+2*margin+gutter),"#f7f6f2")
d=ImageDraw.Draw(image)
font=ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc",19)
for k,(label,path) in enumerate(files):
    x=margin+(k%2)*(w+gutter)
    y=margin+(k//2)*(h+head+gutter)
    src=Image.open(path).convert("RGB")
    assert src.size==(930,582),path
    thumb=src.resize((w,h),Image.Resampling.LANCZOS)
    d.text((x+5,y+4),label,font=font,fill="#26392e")
    image.paste(thumb,(x,y+head))
image.save(OUT,optimize=True)
print("PASS",OUT,image.size)
