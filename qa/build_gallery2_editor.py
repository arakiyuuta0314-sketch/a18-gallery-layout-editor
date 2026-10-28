from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil
root=Path(__file__).resolve().parents[1]
src=root/'rooms/gallery1'
dst=root/'rooms/gallery2'
dst.mkdir(exist_ok=True)
base=Image.open(src/'architecture.png').convert('RGBA')
d=ImageDraw.Draw(base)
# Keep the actual 930x582 stone floor and art direction. Replace gallery1's 3-frame rear wall with 2 frames + north exit.
d.rectangle((0,0,929,219),fill='#214e43')
d.rectangle((0,0,929,38),fill='#5c301c')
d.rectangle((0,0,929,11),fill='#925b32')
d.rectangle((0,27,929,35),fill='#a76d3d')
d.rectangle((0,176,929,216),fill='#60331e')
for x in range(0,930,45):
 d.rectangle((x+3,181,x+42,209),outline='#92572f',width=2)
d.line((0,216,929,216),fill='#c18b53',width=5)
for x in [10,304,536,870]:
 d.rectangle((x,36,x+27,217),fill='#e8d7b8',outline='#7d4927',width=3)
 d.line((x+7,42,x+7,167),fill='#f7e9d0',width=5)
for i,(x,w) in enumerate([(80,179),(349,160)],1):
 d.rectangle((x,78,x+w,166),fill='#4d2c1c',outline='#ba8550',width=5)
 d.rectangle((x+9,87,x+w-9,157),fill='#235548',outline='#d5ad71',width=2)
 f=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',33)
 d.text((x+w/2,121),str(i),font=f,anchor='mm',fill='#eed8aa')
# North door opens toward gallery4 after level 5, kept free of display walls.
d.rounded_rectangle((671,37,798,223),radius=55,fill='#4b2c1a',outline='#bd8853',width=6)
d.rounded_rectangle((684,47,785,219),radius=45,fill='#0b2924',outline='#91663c',width=3)
d.rectangle((688,116,781,220),fill='#0b2924')
# West passage, leading from the entrance's upper-right passage (screen coordinates are room-local).
d.polygon([(0,284),(47,300),(47,459),(0,476)],fill='#4e2d1b')
d.polygon([(0,301),(33,314),(33,444),(0,456)],fill='#0c2e29')
d.line([(0,283),(49,300),(49,458),(0,476)],fill='#ba8755',width=5)
base.save(dst/'architecture.png')
# Existing display-wall images are real preview sprites, not regenerated illustration.
for name,out in [('wall4.png','wall3.png'),('wall5.png','wall4.png'),('wall4.png','wall5.png')]:
 shutil.copy2(src/name,dst/out)
# Foreground is intentionally transparent for this room: gallery1 side walls block west access.
Image.new('RGBA',(930,582),(0,0,0,0)).save(dst/'foreground.png')
room={'schema':'a18-gallery-editor/room-v1','id':'gallery2','name':'展示室2','subtitle':'A案・コの字回遊／未採用の配置監修用','size':{'width':930,'height':582},'entrance':'西側：エントランス右上の通路に接続','exit':'北側：展示室4（館Lv5で開放）','background':'rooms/gallery2/architecture.png','foreground':'rooms/gallery2/foreground.png','objects':[{'id':f'wall{i}','label':f'展示壁{i}（仮）','image':f'rooms/gallery2/wall{i}.png','rect':{'x':x,'y':y,'w':w,'h':h}} for i,x,y,w,h in [(3,105,308,212,181),(4,370,369,212,181),(5,664,310,212,181)]],'limits':{'left':54,'right':34,'top':275,'bottom':14,'clearRearCorridorY':275},'layoutRevision':'A-provisional-20261028','status':'not approved; layout preview only','notes':'Gallery1 background art direction and real preview wall sprites reused. Gallery2 back wall and passages are provisional image composition, not final game assets. No new staff, no decorations. Game collisions, depth, transitions not verified.'}
(dst/'room.json').write_text(json.dumps(room,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
catalog=root/'rooms/catalog.json'
data=json.loads(catalog.read_text(encoding='utf-8'))
assert [r['id'] for r in data['rooms']]==['gallery1']
data['rooms'].append({'id':'gallery2','name':'展示室2（A案・仮）','config':'rooms/gallery2/room.json'})
catalog.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Composite visual evidence with actual assets, at native canvas dimensions.
preview=base.copy()
for o in room['objects']:
 a=Image.open(root/o['image']).convert('RGBA').resize((o['rect']['w'],o['rect']['h']))
 preview.alpha_composite(a,(o['rect']['x'],o['rect']['y']))
preview.save(dst/'gallery2_A_actual_assets_preview.png')
print('Built gallery2 room, preview',preview.size)
