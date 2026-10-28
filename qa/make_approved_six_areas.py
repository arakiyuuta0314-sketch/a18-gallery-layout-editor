from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
r=Path('C:/Users/User/source/repos/a18-gallery-layout-editor')
q=r/'qa/architecture-bases-20261029'
items=[('ENTRANCE Lv.1 / LIVE GAME',q/'entrance_lv1_live_game.png')]
items += [(f'GALLERY {i} / APPROVED LAYOUT',r/f'whole-museum-review/gallery{i}_approved_layout.png') for i in range(1,6)]
W,H=650,407
out=Image.new('RGB',(1340,1390),'#f4f2ee')
d=ImageDraw.Draw(out)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
for i,(label,p) in enumerate(items):
 x=10+(i%2)*670;y=10+(i//2)*460
 d.text((x+5,y+4),label,font=font,fill='#26372e')
 im=Image.open(p).convert('RGB')
 im.thumbnail((W,H),Image.Resampling.LANCZOS)
 out.paste(im,(x+(W-im.width)//2,y+37+(H-im.height)//2))
dest=q/'entrance_lv1_live_plus_approved_gallery1to5.png'
out.save(dest,optimize=True)
print('PASS',dest,out.size)
