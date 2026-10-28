"""Resize the approved preview's wooden gallery guide counter for staff behind it.

User-approved positions are authoritative. Horizontal edges move inward 20px each.
Only counter height is estimated for review (96->76 px), with exact top Y preserved.
No staff artwork is invented or placed.
"""
from pathlib import Path
from PIL import Image, ImageChops
import json
ROOT=Path(__file__).resolve().parents[1]
ROOM=ROOT/'rooms/gallery1'
old=ROOM/'counter175.png'
assert old.is_file(),'Expected known previous asset is absent'
im=Image.open(old).convert('RGBA')
assert im.size==(175,96),im.size
# Result: x 405+20=425, 175-40=135, y339 retained.
new=im.resize((135,76), Image.Resampling.LANCZOS)
new_path=ROOM/'counter135_staff.png'
new.save(new_path,optimize=True)
assert Image.open(new_path).size==(135,76)
p=ROOM/'room.json'
data=json.loads(p.read_text(encoding='utf-8'))
assert data['id']=='gallery1' and data['size']=={'width':930,'height':582}
found={o['id']:o for o in data['objects']}
assert set(found)=={'wall4','wall5','counter'}
assert found['counter']['rect']=={'x':425,'y':396,'w':175,'h':96}
assert found['wall4']['rect']=={'x':132,'y':328,'w':240,'h':182}
assert found['wall5']['rect']=={'x':628,'y':286,'w':240,'h':182}
found['wall4']['rect']={'x':102,'y':275,'w':240,'h':182}
found['wall5']['rect']={'x':636,'y':326,'w':240,'h':182}
found['counter']['rect']={'x':425,'y':339,'w':135,'h':76}
found['counter']['image']='rooms/gallery1/counter135_staff.png'
data['subtitle']='採用配置・案内台135px×76px／北側出口は展示室3'
data['layoutRevision']='v07-user-positions-counter135-staff-space'
data['staffPlacement']={
 'status':'not placed',
 'intent':'place staff behind the guide desk later',
 'counterResize':'height 96px -> 76px provisional to reveal staff; top y=339 preserved',
 'staffArt':'not chosen',
}
data['origin']='User layout JSON 2026-10-28; preserved coordinates except centered counter width and provisional height'
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS gallery1 v07 JSON; resized preview counter',new.size,'centerX',425+135/2)
print('STAFF: not rendered; 76px counter height is a review candidate')
