from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil
root=Path(__file__).resolve().parents[1]; src=root/'rooms/gallery2'; out=root/'rooms/gallery3';out.mkdir(exist_ok=True)
bg=Image.open(src/'architecture.png').convert('RGBA')
d=ImageDraw.Draw(bg)
# Restore rear wall where gallery2 had north doorway: gallery3 has south/east exits.
d.rectangle((653,36,816,222),fill='#285144')
d.rectangle((653,177,816,216),fill='#60331e')
for x in range(657,816,45):d.rectangle((x,181,x+38,208),outline='#92572f',width=2)
d.line((653,216,816,216),fill='#c18b53',width=5)
# West entrance of gallery2 is sealed in gallery3.
d.polygon([(0,280),(52,299),(52,462),(0,479)],fill='#d5c5a7')
d.line([(0,280),(52,299),(52,462),(0,479)],fill='#7d4927',width=5)
# Gallery3 east portal -> Gallery5, keep passage at right foreground.
d.polygon([(872,282),(929,270),(929,488),(872,463)],fill='#4e2d1b')
d.polygon([(890,300),(929,291),(929,466),(890,449)],fill='#0c2e29')
d.line([(872,282),(890,301),(890,448),(872,463)],fill='#ba8755',width=5)
# Gallery3 south portal -> Gallery1: floor-edge passage. Deliberately leave a clear strip.
d.polygon([(394,535),(544,535),(562,581),(375,581)],fill='#6d4a32')
d.polygon([(408,542),(530,542),(541,581),(395,581)],fill='#2a4038')
d.line([(394,535),(544,535)],fill='#c49963',width=5)
d.line([(375,581),(394,535)],fill='#ad7a4c',width=4)
d.line([(562,581),(544,535)],fill='#ad7a4c',width=4)
# Gallery3: three back-wall art frames. Independent art walls two, placed asymmetrically.
for i,x,w in [(1,69,178),(2,336,175),(3,601,175)]:
 d.rectangle((x,78,x+w,164),fill='#4d2c1c',outline='#ba8550',width=5)
 d.rectangle((x+9,87,x+w-9,155),fill='#235548',outline='#d5ad71',width=2)
 font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',33)
 d.text((x+w/2,120),str(i),font=font,anchor='mm',fill='#eed8aa')
bg.save(out/'architecture.png')
Image.new('RGBA',(930,582),(0,0,0,0)).save(out/'foreground.png')
for n in (4,5):
 shutil.copy2(root/'rooms/gallery1'/f'wall{n}.png',out/f'wall{n}.png')
objects=[('wall4',105,301,240,182),('wall5',598,354,240,182)]
room={'schema':'a18-gallery-editor/room-v1','id':'gallery3','name':'展示室3','subtitle':'Gallery3 draft - asymmetric viewing route','size':{'width':930,'height':582},'entrance':'South: gallery1','exit':'East: gallery5 (opens at museum level 6)','background':'rooms/gallery3/architecture.png','foreground':'rooms/gallery3/foreground.png','objects':[{'id':n,'label':n+' (draft)','image':f'rooms/gallery3/{n}.png','rect':{'x':x,'y':y,'w':w,'h':h}} for n,x,y,w,h in objects],'limits':{'left':40,'right':40,'top':270,'bottom':18},'layoutRevision':'gallery3-concept-A-20261028','status':'unapproved visual layout proposal','notes':'Same art direction and floor as gallery1/gallery2. 3 rear frames + 2 independent walls. South and east passages draft; collision and character layering not implemented.'}
(out/'room.json').write_text(json.dumps(room,ensure_ascii=True,indent=2)+'\n')
catalog=root/'rooms/catalog.json';data=json.loads(catalog.read_text(encoding='utf-8'))
assert [x['id'] for x in data['rooms']]==['gallery1','gallery2']
data['rooms'].append({'id':'gallery3','name':'Gallery 3 (draft)','config':'rooms/gallery3/room.json'})
catalog.write_text(json.dumps(data,ensure_ascii=True,indent=2)+'\n')
for n,x,y,w,h in objects:
 a=Image.open(out/f'{n}.png').convert('RGBA').resize((w,h));bg.alpha_composite(a,(x,y))
bg.save(out/'gallery3_concept_A.png')
print('Gallery3 draft built, 930x582, 5 frames, south+east passages')
