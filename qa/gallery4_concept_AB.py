"""Gallery4 A/B architectural prototypes only; no game logic, no orientation restrictions yet."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math,json
root=Path(__file__).resolve().parents[1]
out=root/'rooms/gallery4'
out.mkdir(parents=True,exist_ok=True)
W,H=930,582
font=ImageFont.truetype(r'C:\Windows\Fonts\meiryo.ttc',24)
small=ImageFont.truetype(r'C:\Windows\Fonts\meiryo.ttc',15)
def frame(d,n,rect,shape):
 x,y,w,h=rect
 # clear physical portrait/landscape silhouette, never just an orientation label
 d.rectangle((x+3,y+6,x+w+5,y+h+8),fill='#3b291d')
 d.rectangle((x-5,y-5,x+w+5,y+h+5),fill='#54351f',outline='#9f693b',width=3)
 d.rectangle((x,y,x+w,y+h),fill='#ac7a45',outline='#ecc794',width=4)
 d.rectangle((x+10,y+10,x+w-10,y+h-10),fill='#20483d',outline='#d7ac75',width=3)
 d.text((x+w/2,y+h/2-5),str(n),font=font,anchor='mm',fill='#f7e2b9')
 d.text((x+w/2,y+h-24),'縦' if shape=='portrait' else '横',font=small,anchor='mm',fill='#dbb986')
def architecture():
 im=Image.new('RGB',(W,H),'#e1c5a2')
 base=Image.open(root/'rooms/gallery2/architecture.png').convert('RGB')
 # Reuse the original perspective floor exactly, including its tile grid.
 im.paste(base.crop((0,218,W,H)),(0,218))
 corn=Image.open(root/'rooms/gallery3/gallery3_architecture_only_E.png').convert('RGB')
 im.paste(corn.crop((0,0,W,36)),(0,0))
 d=ImageDraw.Draw(im)
 d.rectangle((0,36,929,169),fill='#235044')
 d.rectangle((0,169,929,214),fill='#714329')
 d.rectangle((0,169,929,178),fill='#9a6a3f')
 for x in range(6,930,45):
  d.rectangle((x,181,min(x+36,928),211),fill='#7d492b',outline='#aa7747',width=2)
 d.line((0,216,929,216),fill='#dec08d',width=5)
 # Four distinct wall bays, NOT the central alcove of Gallery3.
 for x1,x2 in [(36,252),(282,502),(526,662),(677,878)]:
  d.rectangle((x1,45,x2,164),fill='#1d473d',outline='#416558',width=3)
  d.line((x1+7,51,x2-7,51),fill='#567e6c',width=2)
 for x in (22,267,513,669,897):
  d.rectangle((x-13,34,x+13,217),fill='#805532',outline='#54351f',width=2)
  d.rectangle((x-8,40,x+8,211),fill='#e5d4b2')
  d.line((x-6,44,x-6,204),fill='#f9edd5',width=2)
  d.rectangle((x-16,205,x+16,221),fill='#a9784c',outline='#57351e',width=3)
 # Left-facing gallery5 door - FULL opening, not clipped at the image boundary.
 # The left side-wall is opaque, with both arch jambs visible.
 d.polygon([(0,224),(183,238),(180,482),(0,532)],fill='#b1906d')
 d.polygon([(4,227),(32,230),(32,515),(4,529)],fill='#856344')
 d.line([(183,238),(180,482),(0,532)],fill='#64432c',width=7)
 d.rectangle((61,332,149,475),fill='#0e302a')
 d.polygon([(68,469),(147,468),(169,487),(53,502)],fill='#a07954')
 d.arc((58,285,152,382),180,360,fill='#e0ba87',width=12)
 d.line((58,333,58,486),fill='#e0ba87',width=12)
 d.line((153,332,153,479),fill='#e0ba87',width=12)
 d.arc((66,296,145,373),180,360,fill='#6b4c32',width=5)
 d.line((68,333,68,471),fill='#745033',width=5)
 d.line((146,334,146,468),fill='#745033',width=5)
 d.line((52,485,173,489),fill='#67452c',width=7)
 # Right side: solid full-height side-wall, no false east portal.
 d.polygon([(875,222),(929,221),(929,519),(876,481)],fill='#c4a581')
 d.polygon([(896,222),(908,222),(908,499),(896,488)],fill='#e0c39e')
 d.line((876,223,876,482),fill='#8a603e',width=6)
 d.line((876,482,929,519),fill='#6b472d',width=6)
 # South entrance at front center, gallery2, preserving the approved hallway convention.
 d.polygon([(427,530),(513,530),(569,581),(371,581)],fill='#826141')
 d.polygon([(439,537),(501,537),(541,581),(397,581)],fill='#244a40')
 d.line((428,532,512,532),fill='#e4c492',width=7)
 d.line((429,533,377,581),fill='#d5a970',width=5)
 d.line((511,533,564,581),fill='#d5a970',width=5)
 return im
def panel(n,shape,w=210,h=165):
 im=Image.new('RGBA',(w,h),(0,0,0,0))
 d=ImageDraw.Draw(im)
 d.polygon([(4,13),(w-22,6),(w-5,14),(w-5,h-21),(8,h-7)],fill='#4b2d1b')
 d.polygon([(10,16),(w-27,10),(w-27,h-16),(10,h-9)],fill='#235044',outline='#ad7b49')
 d.line([(8,16),(w-25,10),(w-25,h-17),(8,h-10)],fill='#d5a36c',width=5)
 d.rectangle((18,h-44,w-33,h-16),fill='#784629',outline='#aa784a',width=2)
 if shape=='portrait':frame(d,n,(w//2-41,21,82,113),shape)
 else:frame(d,n,(30,39,w-66,79),shape)
 return im
base=architecture()
base.save(out/'architecture_only_A.png')
variants={
 'A':{'rear':[(1,(130,44,88,130),'portrait'),(2,(299,74,183,92),'landscape'),(3,(546,44,90,130),'portrait'),(4,(698,74,161,92),'landscape')],
      'foreground':[(5,'landscape',(614,323,210,165))]},
 'B':{'rear':[(1,(133,44,88,130),'portrait'),(2,(357,74,190,92),'landscape'),(3,(734,44,90,130),'portrait')],
      'foreground':[(4,'landscape',(284,328,210,165)),(5,'landscape',(606,313,210,165))]}
}
for v,dat in variants.items():
 scene=base.copy()
 if v=='B':
  bd=ImageDraw.Draw(scene)
  bd.rectangle((496,37,530,168),fill='#235044')
  bd.rectangle((496,169,530,214),fill='#714329')
  bd.rectangle((496,169,530,178),fill='#9a6a3f')
  bd.rectangle((497,181,528,211),fill='#7d492b',outline='#aa7747',width=2)
  bd.line((496,216,530,216),fill='#dec08d',width=5)
 d=ImageDraw.Draw(scene)
 for n,rect,shape in dat['rear']:frame(d,n,rect,shape)
 scene.save(out/f'gallery4_{v}_rear.png')
 rgba=scene.convert('RGBA')
 for n,shape,xywh in dat['foreground']:
  x,y,w,h=xywh
  obj=panel(n,shape,w,h)
  obj.save(out/f'gallery4_{v}_wall{n}.png')
  rgba.alpha_composite(obj,(x,y))
 rgba.convert('RGB').save(out/f'gallery4_concept_{v}.png')
compare=Image.new('RGB',(1904,638),'#ede8dd')
cd=ImageDraw.Draw(compare)
big=ImageFont.truetype(r'C:\Windows\Fonts\meiryo.ttc',19)
cd.text((12,15),'A｜奥4枠＋室内1枠（縦2・横3）',font=big,fill='#30453a')
cd.text((962,15),'B｜奥3枠＋室内2枠（縦2・横3）',font=big,fill='#30453a')
for j,v in enumerate(('A','B')):
 img=Image.open(out/f'gallery4_concept_{v}.png')
 compare.paste(img,(12+950*j,48))
compare.save(out/'gallery4_AB_comparison.png')
print('Gallery4 A/B drafts generated, 930x582, 5 frames each, south+west exits. Unapproved.')
