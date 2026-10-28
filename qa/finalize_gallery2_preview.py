from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
root=Path(__file__).resolve().parents[1]
folder=root/'rooms/gallery2'
for i in (3,4,5):
 p=folder/f'wall{i}.png'
 im=Image.open(p).convert('RGBA')
 d=ImageDraw.Draw(im)
 color=im.getpixel((90,93))
 d.rectangle((107,81,135,110),fill=color)
 font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',19)
 d.text((120,96),str(i),font=font,fill='#f5dfb5',anchor='mm')
 im.save(p)
cat=root/'rooms/catalog.json'
c=json.loads(cat.read_text(encoding='utf-8'))
for room in c['rooms']:
 if room['id']=='gallery2':
  room['name']='Gallery 2 (A draft)'
cat.write_text(json.dumps(c,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
r=json.loads((folder/'room.json').read_text(encoding='utf-8'))
im=Image.open(folder/'architecture.png').convert('RGBA')
for o in r['objects']:
 box=o['rect']
 sprite=Image.open(root/o['image']).convert('RGBA').resize((box['w'],box['h']))
 im.alpha_composite(sprite,(box['x'],box['y']))
im.save(folder/'gallery2_A_actual_assets_preview.png')
print('corrected sprite numbers and composite')
