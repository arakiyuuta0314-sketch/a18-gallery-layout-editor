from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
r=Path('C:/Users/User/source/repos/a18-gallery-layout-editor')
g=Path('C:/Users/User/source/repos/web-tools-preview/a18/layout-test')
items=[
('ENTRANCE Lv.1 / QUALITY REFERENCE',g/'assets/entrance/approved_initial_20261027/entrance_background_initial_approved.png'),
('GALLERY 1 / CURRENT',r/'rooms/gallery1/architecture.png'),
('GALLERY 2 / LAYOUT DRAFT',r/'rooms/gallery2/architecture_only_v01.png'),
('GALLERY 3 / LAYOUT DRAFT',r/'rooms/gallery3/gallery3_architecture_only_E.png'),
('GALLERY 4 / LAYOUT DRAFT',r/'rooms/gallery4/architecture_only_A.png'),
('GALLERY 5 / LAYOUT DRAFT',r/'rooms/gallery5/gallery5_palace_architecture_fixed_E_v01.png')]
w,h=650,407
out=Image.new('RGB',(1340,1390),'#f4f2ee')
d=ImageDraw.Draw(out)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
for i,(label,p) in enumerate(items):
 x=10+(i%2)*670
 y=10+(i//2)*460
 d.text((x+5,y+4),label,font=font,fill='#26372e')
 im=Image.open(p).convert('RGB')
 im.thumbnail((w,h),Image.Resampling.LANCZOS)
 out.paste(im,(x+(w-im.width)//2,y+37+(h-im.height)//2))
dest=r/'qa/architecture-bases-20261029/entrance_lv1_all_six_areas.png'
out.save(dest,optimize=True)
print('PASS',dest,out.size)
