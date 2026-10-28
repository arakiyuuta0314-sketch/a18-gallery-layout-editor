from pathlib import Path
from PIL import Image
import json
root=Path(__file__).resolve().parents[1]
folder=root/'rooms/gallery2'
p=folder/'room.json'
r=json.loads(p.read_text(encoding='utf-8'))
assert r['id']=='gallery2' and r['size']=={'width':930,'height':582}
expected={'wall3':(105,308,212,181),'wall4':(380,251,212,181),'wall5':(664,310,212,181)}
assert {o['id'] for o in r['objects']}==set(expected)
for o in r['objects']:
 x,y,w,h=expected[o['id']]
 o['rect']={'x':x,'y':y,'w':w,'h':h}
r['subtitle']='A layout approved 2026-10-28'
r['layoutRevision']='A-approved-user-positions-20261028'
r['status']='layout approved; game implementation pending'
r['notes']='User approved exact JSON positions. Keep architecture and entrance/exit draft status separate. Gameplay collision, character depth, camera, door transitions and decorations not yet validated.'
p.write_text(json.dumps(r,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
im=Image.open(folder/'architecture.png').convert('RGBA')
for o in r['objects']:
 b=o['rect']; a=Image.open(root/o['image']).convert('RGBA').resize((b['w'],b['h']))
 im.alpha_composite(a,(b['x'],b['y']))
im.save(folder/'gallery2_A_actual_assets_preview.png')
print('APPROVED POSITIONS',expected)
