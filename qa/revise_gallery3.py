from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil
root=Path(__file__).resolve().parents[1]; f=root/'rooms/gallery3'; src=root/'rooms/gallery2'
im=Image.open(src/'architecture.png').convert('RGBA');d=ImageDraw.Draw(im)
# Seal gallery2 west entrance, restore plain west-side wall.
d.polygon([(0,277),(59,297),(59,466),(0,482)],fill='#d9c8ad')
d.line([(0,277),(59,297),(59,466),(0,482)],fill='#835c39',width=4)
# Remove north doorway; gallery3 has no north link.
d.rectangle((650,36,816,220),fill='#284e42')
d.rectangle((650,176,816,215),fill='#60331e')
for x in range(654,814,44):d.rectangle((x,181,x+38,207),outline='#92572f',width=2)
d.line((650,215,816,215),fill='#c18b53',width=5)
# Two permanent rear exhibits, not three.
font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',33)
for n,x,w in [(1,160,180),(2,450,180)]:
 d.rectangle((x,79,x+w,164),fill='#4d2c1c',outline='#ba8550',width=5)
 d.rectangle((x+9,88,x+w-9,155),fill='#235548',outline='#d5ad71',width=2)
 d.text((x+w/2,121),str(n),font=font,anchor='mm',fill='#eed8aa')
# South passage, deliberately lower LEFT (screen-local); entrance from gallery1 north.
d.polygon([(50,536),(202,536),(220,581),(32,581)],fill='#64432d')
d.polygon([(66,544),(185,544),(198,581),(49,581)],fill='#29473e')
d.line((50,536,202,536),fill='#c49963',width=5)
d.line((32,581,50,536),fill='#ad7a4c',width=4)
d.line((220,581,202,536),fill='#ad7a4c',width=4)
# East connection to gallery5 at upper right of floor.
d.polygon([(870,268),(929,256),(929,453),(870,435)],fill='#4e2d1b')
d.polygon([(890,287),(929,278),(929,431),(890,419)],fill='#0c2e29')
d.line([(870,268),(890,287),(890,419),(870,435)],fill='#ba8755',width=5)
im.save(f/'architecture.png')
# 3 independent panels: near-left, mid-right, near-centre; strong zig-zag rhythm.
for n in (3,4,5):
 source=root/'rooms/gallery2'/f'wall{n}.png'
 shutil.copy2(source,f/f'wall{n}.png')
objects=[('wall3',86,302,196,171),('wall4',567,271,211,178),('wall5',351,371,219,178)]
room=json.loads((f/'room.json').read_text(encoding='utf-8'))
room['subtitle']='B concept - offset exhibition promenade (unapproved)'
room['entrance']='South, lower-left in screen: connects to gallery1 north'
room['exit']='East, upper-right in screen: connects to gallery5 (Lv6)'
room['objects']=[{'id':n,'label':'Display '+n[-1]+' (draft)','image':f'rooms/gallery3/{n}.png','rect':{'x':x,'y':y,'w':w,'h':h}} for n,x,y,w,h in objects]
room['layoutRevision']='gallery3-concept-B-20261028'
room['notes']='2 fixed rear displays + 3 independent display walls. Screen-local lower-left south entry, upper-right east exit. Room adjacency verified against ROOM_LINKS. Collision/depth not tested.'
(f/'room.json').write_text(json.dumps(room,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
for n,x,y,w,h in objects:
 a=Image.open(f'{f}/{n}.png').convert('RGBA').resize((w,h));im.alpha_composite(a,(x,y))
im.save(f/'gallery3_concept_B.png')
print('gallery3 B created',im.size)
