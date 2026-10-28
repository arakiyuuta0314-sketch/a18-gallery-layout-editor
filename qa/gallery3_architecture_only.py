from pathlib import Path
from PIL import Image, ImageDraw
import json
root=Path(__file__).resolve().parents[1]
f=root/'rooms/gallery3'
# Structural-only study. New paint from scratch: no prior gallery frames or furniture.
im=Image.new('RGB',(930,582),'#e7d5bb')
d=ImageDraw.Draw(im)
# Floor and rear wall: existing gallery palette, but no exhibition frames.
d.rectangle((0,0,929,218),fill='#224b40')
d.rectangle((0,0,929,35),fill='#56341f')
for y in (7,16,27):d.line((0,y,929,y),fill='#ae8050',width=2)
d.rectangle((0,174,929,218),fill='#633b23')
for x in range(0,930,46):d.rectangle((x+3,181,min(x+42,928),210),outline='#aa7646',width=2)
d.line((0,216,929,216),fill='#c39a66',width=5)
for x in (18,303,602,895):
 d.rectangle((x-11,35,x+11,216),fill='#9c7653')
 d.rectangle((x-7,39,x+7,211),fill='#e8d9bb')
 d.line((x-7,42,x-7,209),fill='#fff2d5',width=2)
d.polygon([(0,220),(929,220),(929,581),(0,581)],fill='#e6d3b9')
for y in range(221,582,48):
 d.line((0,y,929,y),fill='#d1b99c',width=2)
for x in range(-200,1150,56):
 d.line((x,221,x+90,581),fill='#d2b99c',width=1)
# Left side is a full solid side wall with perspective depth.
d.polygon([(0,218),(56,231),(56,476),(0,497)],fill='#d9c4a7')
d.polygon([(0,218),(14,221),(14,492),(0,497)],fill='#a88058')
d.line([(56,231),(56,476),(0,497)],fill='#795438',width=5)
d.line([(16,226),(16,487)],fill='#f3e4c9',width=4)
# Southern threshold at front-left: entrance from gallery1.
d.polygon([(65,537),(209,537),(232,581),(42,581)],fill='#755137')
d.polygon([(79,545),(195,545),(210,581),(60,581)],fill='#27473e')
d.line((65,537,209,537),fill='#d4ae7b',width=6)
d.line([(42,581),(65,537)],fill='#c49b68',width=5)
d.line([(232,581),(209,537)],fill='#c49b68',width=5)
# East passage: side-wall recess, opening and visible inner thickness.
d.polygon([(845,219),(929,219),(929,492),(845,456)],fill='#6c4229')
d.polygon([(862,242),(929,225),(929,475),(862,445)],fill='#c0986c')
d.polygon([(879,273),(929,261),(929,454),(879,431)],fill='#173b32')
d.polygon([(891,282),(929,274),(929,444),(891,425)],fill='#0c2923')
d.line([(862,242),(875,230),(894,225),(916,226),(929,235)],fill='#e1b887',width=7)
d.line([(862,242),(862,445),(929,475)],fill='#e1b887',width=7)
d.line([(879,273),(879,431),(929,454)],fill='#805337',width=5)
d.polygon([(879,431),(929,454),(929,492),(845,456)],fill='#8c6646')
d.line([(845,456),(929,492)],fill='#d5ae7d',width=5)
im.save(f/'gallery3_architecture_only_D.png')
# A separate editor draft with no furniture, preserving the previous C file as a named image.
room=json.loads((f/'room.json').read_text(encoding='utf-8'))
room['background']='rooms/gallery3/gallery3_architecture_only_D.png'
room['objects']=[]
room['subtitle']='D architecture-only study - no exhibition frames'
room['layoutRevision']='gallery3-architecture-only-D-20261028'
room['status']='unapproved architecture-only concept'
room['notes']='Only architecture: 0 frames displayed; planned 5 fixtures remain a specification, to be positioned after architectural approval. C preserved in gallery3_concept_C.png.'
(f/'room.json').write_text(json.dumps(room,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
print('PASS architecture-only',im.size,'objects',len(room['objects']))
