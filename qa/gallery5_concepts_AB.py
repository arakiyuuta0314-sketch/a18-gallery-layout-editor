from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import json
root=Path(__file__).resolve().parents[1]
out=root/'rooms/gallery5'
out.mkdir(exist_ok=True)
base=Image.open(root/'rooms/gallery4/architecture_only_A.png').convert('RGB')
assert base.size==(930,582)
fnum=ImageFont.truetype(r'C:\Windows\Fonts\meiryo.ttc',27)
fhead=ImageFont.truetype(r'C:\Windows\Fonts\meiryo.ttc',20)
def architecture():
 im=base.copy(); d=ImageDraw.Draw(im)
 d.rectangle((0,37,929,169),fill='#204a40')
 d.rectangle((0,170,929,217),fill='#72462d')
 d.rectangle((0,171,929,178),fill='#a1764a')
 for x in range(5,925,44):
  d.rectangle((x,183,min(x+36,928),209),fill='#7f4a2b',outline='#a9784b',width=2)
 d.line((0,215,929,215),fill='#d7b185',width=5)
 for left,right in [(40,172),(201,300),(326,608),(639,731),(760,891)]:
  d.rectangle((left,46,right,166),fill='#174338',outline='#537465',width=3)
  d.line((left+6,53,right-6,53),fill='#6d8b75',width=2)
 for x in (22,187,314,624,747,907):
  d.rectangle((x-11,34,x+11,218),fill='#6e482f',outline='#55321f',width=3)
  d.rectangle((x-7,39,x+7,211),fill='#d8c39f')
  d.line((x-5,44,x-5,208),fill='#f0e3c8',width=2)
  d.rectangle((x-15,207,x+15,220),fill='#aa7950',outline='#694127',width=2)
 left_portal=base.crop((0,221,184,538))
 im.paste(ImageOps.mirror(left_portal),(746,221))
 im.paste(base.crop((368,526,570,582)),(368,526))
 return im
def frame(d,n,rect,signature=False):
 x,y,w,h=rect
 d.rectangle((x+4,y+7,x+w+5,y+h+8),fill='#2a221b')
 d.rectangle((x-5,y-5,x+w+5,y+h+5),fill='#51321f',outline='#b78b53',width=3)
 d.rectangle((x,y,x+w,y+h),fill='#977044',outline='#f0d19b',width=4)
 d.rectangle((x+9,y+9,x+w-9,y+h-9),fill='#235045',outline='#c59d68',width=3)
 d.text((x+w/2,y+h/2),str(n),fill='#f6e5c4',font=fnum,anchor='mm')
 if signature:d.rectangle((x-9,y-9,x+w+9,y+h+9),outline='#927046',width=2)
A=[(1,(54,79,111,82)),(2,(216,56,71,116)),(3,(340,63,246,109)),
 (4,(658,56,71,116)),(5,(765,79,111,82))]
B=[(1,(53,49,107,49)),(2,(53,117,107,49)),(3,(340,61,246,114)),
 (4,(774,49,107,49)),(5,(774,117,107,49))]
arch=architecture()
arch.save(out/'gallery5_architecture_only.png')
for tag,items in [('A',A),('B',B)]:
 im=arch.copy(); d=ImageDraw.Draw(im)
 for n,rect in items:frame(d,n,rect,signature=(n==3))
 im.save(out/f'gallery5_concept_{tag}.png')
comparison=Image.new('RGB',(1904,643),'#efe9df')
dc=ImageDraw.Draw(comparison)
dc.text((12,14),'A案｜横一列に5枠・中央に大作',font=fhead,fill='#264137')
dc.text((962,14),'B案｜左右2段ずつ＋中央に大作',font=fhead,fill='#264137')
comparison.paste(Image.open(out/'gallery5_concept_A.png'),(12,49))
comparison.paste(Image.open(out/'gallery5_concept_B.png'),(962,49))
comparison.save(out/'gallery5_AB_comparison.png')
room={
 'schema':'a18-gallery-editor/room-v1','id':'gallery5','name':'展示室5',
 'subtitle':'A/B比較中｜3方向に開く広間（A：奥5枠、床の展示壁なし）',
 'previewFocusX':465,'mobileOverview':True,
 'size':{'width':930,'height':582},
 'entrance':'南：エントランス（下部中央）',
 'exit':'西：展示室3（左側面）、東：展示室4（右側面）',
 'background':'rooms/gallery5/gallery5_concept_A.png',
 'foreground':'rooms/gallery3/foreground.png','objects':[],
 'layoutRevision':'gallery5-AB-unapproved-20261029',
 'status':'unapproved architecture and five-frame visual concepts',
 'frameCount':5,
 'proposals':{'A':'five rear frames in one row, center 3 enlarged',
              'B':'two-tier side pairs around a large center frame 3'},
 'notes':'No north exit. All five placeholders are baked into preview backdrop, not game fixtures. Staff, collision, walkability, image orientation and gameplay are not validated.'
}
(out/'room.json').write_text(json.dumps(room,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert len(A)==len(B)==5 and arch.size==(930,582)
print('PASS gallery5 A/B images, 5 frames each and south-west-east portals')
