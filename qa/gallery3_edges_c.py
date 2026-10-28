from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]; f=root/'rooms/gallery3'
base=Image.open(root/'rooms/gallery1/architecture.png').convert('RGB')
im=base.copy(); d=ImageDraw.Draw(im)
# Rebuild rear wall rather than stacking frames over the gallery2 architecture.
d.rectangle((0,36,929,218),fill='#214e42')
d.rectangle((0,171,929,218),fill='#5c321d')
for x in range(0,930,45):
 d.rectangle((x+3,179,min(928,x+40),210),outline='#9b6539',width=2)
d.line((0,217,929,217),fill='#c69a66',width=4)
for x in (12,306,596,899):
 d.rectangle((x-10,37,x+10,216),fill='#d9c4a3',outline='#8a5a36',width=4)
 d.rectangle((x-7,42,x+6,211),fill='#f3e5c6')
font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',32)
for n,x in [(1,120),(2,475)]:
 w=180
 d.rectangle((x,78,x+w,164),fill='#4e2918',outline='#c69758',width=5)
 d.rectangle((x+9,87,x+w-9,155),fill='#204f42',outline='#e3ba79',width=2)
 d.text((x+w/2,120),str(n),font=font,anchor='mm',fill='#f4dfb4')
# Left edge: continuous solid architectural wall and trim, no false portal.
d.polygon([(0,218),(37,218),(37,475),(0,492)],fill='#d9c6a7')
d.polygon([(0,218),(13,218),(13,488),(0,492)],fill='#aa865c')
d.line([(37,218),(37,475),(0,492)],fill='#765039',width=5)
d.line([(15,218),(15,484)],fill='#f2e4c8',width=3)
# South entrance: open floor channel on the near-left, not an upright doorway.
d.polygon([(61,537),(205,537),(226,581),(39,581)],fill='#755036')
d.polygon([(74,544),(191,544),(204,581),(58,581)],fill='#25463d')
d.line([(61,537),(205,537)],fill='#d2a571',width=5)
d.line([(39,581),(61,537)],fill='#b58a59',width=5)
d.line([(226,581),(205,537)],fill='#b58a59',width=5)
# Right edge: distinct full-height wall with arched doorway and visible inner wall thickness.
d.polygon([(863,217),(929,217),(929,486),(863,456)],fill='#4e2d1b')
d.polygon([(876,248),(929,235),(929,466),(876,444)],fill='#a57b50')
d.polygon([(888,271),(929,260),(929,448),(888,430)],fill='#12392f')
d.polygon([(897,283),(929,275),(929,441),(897,425)],fill='#09271f')
d.line([(876,248),(886,239),(899,233),(915,232),(929,235)],fill='#d7a971',width=6)
d.line([(876,248),(876,444),(929,466)],fill='#d7a971',width=6)
d.line([(888,271),(888,430),(929,448)],fill='#72452b',width=5)
d.polygon([(888,430),(929,448),(929,480),(863,456)],fill='#8c684a')
d.line([(863,456),(929,480)],fill='#d4ac78',width=4)
im.save(f/'architecture.png')
room=json.loads((f/'room.json').read_text(encoding='utf-8'))
room['subtitle']='C concept - clear closed west wall and east arched exit'
room['layoutRevision']='gallery3-concept-C-20261028'
room['notes']='B display wall coordinates unchanged. West edge is solid; south entrance at lower left; east arched passage to gallery5 at right. No collision QA.'
(f/'room.json').write_text(json.dumps(room,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
out=im.convert('RGBA')
for o in room['objects']:
 r=o['rect'];a=Image.open(root/o['image']).convert('RGBA').resize((r['w'],r['h']))
 out.alpha_composite(a,(r['x'],r['y']))
out.save(f/'gallery3_concept_C.png')
print('Gallery3 C: rebuilt background, unchanged object coordinates',out.size)
