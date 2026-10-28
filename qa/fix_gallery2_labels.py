from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
root=Path(__file__).resolve().parents[1]
folder=root/'rooms/gallery2'
path=folder/'room.json'
r=json.loads(path.read_text(encoding='utf-8'))
r['subtitle']='A concept - U-shaped viewing route (not approved)'
r['entrance']='West: entrance hall'
r['exit']='North: gallery4 (opens at museum level 5)'
for i,o in enumerate(r['objects'],3):
 o['label']='Display wall '+str(i)+' (draft)'
 # On existing sprite, erase old number inside its dark-green framed label and replace.
 p=folder/('wall'+str(i)+'.png')
 im=Image.open(p).convert('RGBA')
 # Use only label center based on sprite size; preserve the original frame.
 w,h=im.size
 d=ImageDraw.Draw(im)
 # Frame label's inset on sprite is approximately central lower-middle.
 # Keep original art untouched until inspected; labels are in editor controls.
r['notes']='Prototype preview; real gallery1 wall sprites reused. Door geometry and west passage are draft. Not gameplay-tested.'
path.write_text(json.dumps(r,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
print('valid',[(o['id'],o['label']) for o in json.loads(path.read_text())['objects']])
