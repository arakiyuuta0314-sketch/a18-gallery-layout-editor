"""Gallery 4 optional decor visual comparison; never changes approved A architecture/frames."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib
root=Path(__file__).resolve().parents[1]
room=root/"rooms/gallery4"
base=room/"gallery4_concept_A.png"
original=base.read_bytes()
h=hashlib.sha256(original).hexdigest()
scene=Image.open(base).convert("RGBA")
assert scene.size==(930,582)
# Optional asset is preserved locally so a clean checkout can regenerate the comparison.
# It was cropped from existing A18 QA statue art; never treated as final-quality art.
sculpture=Image.open(room/"gallery4_optional_sculpture.png").convert("RGBA")
assert sculpture.size==(100,153)
bbox=sculpture.getchannel("A").getbbox()
assert bbox and bbox[2]-bbox[0]>30
scene.alpha_composite(sculpture,(350,323))
scene.convert("RGB").save(room/"gallery4_A_optional_sculpture_preview.png")
compare=Image.new("RGB",(1904,648),"#f3efe6")
for i,im in enumerate([Image.open(base).convert("RGB"),scene.convert("RGB")]):compare.paste(im,(12+i*950,50))
d=ImageDraw.Draw(compare)
font=ImageFont.truetype(r"C:\Windows\Fonts\meiryo.ttc",21)
d.text((12,12),"A案：確定した建築と展示枠のみ",font=font,fill="#294c3d")
d.text((962,12),"装飾候補：小さな彫像を追加（未承認）",font=font,fill="#294c3d")
compare.save(room/"gallery4_A_decoration_comparison.png")
assert hashlib.sha256(base.read_bytes()).hexdigest()==h
print("PASS decoration comparison; approved A unchanged; optional sculpture crop",bbox)
