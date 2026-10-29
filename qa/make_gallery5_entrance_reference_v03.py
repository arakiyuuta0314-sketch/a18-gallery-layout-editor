from PIL import Image,ImageDraw,ImageEnhance
from pathlib import Path
r=Path(r'C:\Users\User\source\repos\a18-gallery5-material-review')
base=Image.open(r/'qa/gallery5-material-20261029/gallery5_v02_material_architecture_REVIEW.png').convert('RGB')
ref=Image.open(r/'architecture-review/entrance-comparison/entrance-lv6-approved.png').convert('RGB')
# Reuse the actual approved entrance's gold frame as a nine-slice material, preserving the E geometry.
frame=ref.crop((193,145,466,315))
canvas=base.copy(); d=ImageDraw.Draw(canvas)
def nineslice(src,box,edge=19):
 x0,y0,x1,y1=box;w=x1-x0;h=y1-y0;sw,sh=src.size;e=edge
 out=Image.new('RGB',(w,h));regions=[((0,0,e,e),(0,0,e,e)),((sw-e,0,sw,e),(w-e,0,w,e)),((0,sh-e,e,sh),(0,h-e,e,h)),((sw-e,sh-e,sw,sh),(w-e,h-e,w,h)),((e,0,sw-e,e),(e,0,w-e,e)),((e,sh-e,sw-e,sh),(e,h-e,w-e,h)),((0,e,e,sh-e),(0,e,e,h-e)),((sw-e,e,sw,sh-e),(w-e,e,w,h-e))]
 for a,b in regions:out.paste(src.crop(a).resize((b[2]-b[0],b[3]-b[1])),(b[0],b[1]))
 return out
# Keep the E-plan's three frames, larger central piece and two narrower side pieces.
for i,(x0,y0,x1,y1) in enumerate([(201,77,321,215),(330,71,599,222),(610,77,730,215)]):
 d.rectangle((x0-5,y0-4,x1+5,y1+5),fill='#251711')
 canvas.paste(nineslice(frame,(x0,y0,x1,y1)),(x0,y0))
 d=ImageDraw.Draw(canvas)
 d.rectangle((x0+20,y0+20,x1-20,y1-20),fill='#163e34')
 d.rectangle((x0+21,y0+21,x1-21,y1-21),outline='#8c6845',width=2)
# No invented furnishings or artwork; retain approved E side portals and runner.
out=r/'architecture-review/gallery5/gallery5_entrance_material_reference_v03.png';canvas.save(out)
print(out,canvas.size)
