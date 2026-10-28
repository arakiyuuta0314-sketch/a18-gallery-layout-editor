"""A18 approved rooms 3-5: reuse clean architectural sources, reconstruct only E fixed details.
Never edit the original approved layouts, room.json or source PNGs.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json, hashlib

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'qa/architecture-bases-20261029'
QA.mkdir(exist_ok=True)

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_against_approved(room, approved, base, frame_bounds, description):
    src=Image.open(approved).convert('RGB')
    clean=Image.open(base).convert('RGB')
    assert src.size==clean.size==(930,582)
    # Pixel-by-pixel: architectural geometry must agree outside the rear art frame masks.
    a=src.load(); b=clean.load(); outside=0; inside=0; bad=[]
    for y in range(582):
        for x in range(930):
            if a[x,y]==b[x,y]: continue
            if any(x0<=x<=x1 and y0<=y<=y1 for x0,y0,x1,y1 in frame_bounds): inside+=1
            else: outside+=1; bad.append((x,y,a[x,y],b[x,y]))
    assert outside==0, (room, "unintended differences",outside,bad[:15])
    assert inside>0
    review=Image.new('RGB',(1860,616),'#e7e7e7')
    review.paste(src,(0,34))
    review.paste(clean,(930,34))
    d=ImageDraw.Draw(review)
    d.text((15,11),f'{room} / APPROVED WITH FRAMES',fill='#202020')
    d.text((945,11),f'{room} / ARCHITECTURAL BASE (same structure)',fill='#202020')
    sheet=QA/(room+'_before_after.png')
    review.save(sheet,optimize=True)
    return {'room':room,'approved_source':str(approved.relative_to(ROOT)).replace('\\','/'),
            'architecture_base':str(base.relative_to(ROOT)).replace('\\','/'),
            'approved_sha256':digest(approved),'architecture_sha256':digest(base),
            'rear_frames_removed':len(frame_bounds),'changed_pixels_within_frame_bounds':inside,
            'changed_pixels_outside_frame_bounds':outside,'removal_bounding_rectangles':frame_bounds,
            'method':description,'status':'candidate_for_user_review_not_game_integrated'}
rooms={
  'gallery3':(ROOT/'rooms/gallery3/gallery3_layout_G_rear_frames.png',
              ROOT/'rooms/gallery3/gallery3_architecture_only_E.png',
              [(69,73,241,169),(343,60,605,180),(714,73,877,169)],
              'Exact already-preserved E architecture, referenced by G renderer'),
  'gallery4':(ROOT/'rooms/gallery4/gallery4_A_rear.png',
              ROOT/'rooms/gallery4/architecture_only_A.png',
              [(125,39,223,182),(294,69,487,174),(541,39,641,182),(693,69,864,174)],
              'Exact already-preserved A architecture before four built-in frames')
}
results=[]
for room,(approved,base,rects,method) in rooms.items():
    assert approved.is_file() and base.is_file()
    results.append(verify_against_approved(room,approved,base,rects,method))

# Room 5: its existing E architectural source intentionally omits wall sconces and
# decorative curtain lines applied BEFORE frames in qa/gallery5_palace_EF.py.
# Retain those approved fixed details by replaying their original pixel geometry
# onto the original architectural E source; never retouch the palace architecture.
e=ROOT/'rooms/gallery5/gallery5_palace_architecture_E.png'
original=ROOT/'rooms/gallery5/gallery5_palace_E.png'
final=ROOT/'rooms/gallery5/gallery5_palace_architecture_fixed_E_v01.png'
im=Image.open(e).convert('RGBA')
d=ImageDraw.Draw(im)
for x in (185,746):
    d.ellipse((x-17,92,x+17,122),fill='#3b2c25',outline='#ae8b56',width=3)
    for dx in (-17,17):
        d.line((x,119,x+dx,128),fill='#a88455',width=4)
        d.line((x+dx,117,x+dx,102),fill='#dbc190',width=3)
        d.ellipse((x+dx-4,95,x+dx+4,105),fill='#f5dfac')
    d.line((x-18,118,x+18,118),fill='#edce9b',width=3)
    d.ellipse((x-4,118,x+4,131),fill='#ddba7d')
for x in (360,571):
    d.ellipse((x-5,54,x+5,65),fill='#e7cb93',outline='#886740',width=2)
for x0,x1 in ((57,162),(761,868)):
    for x in range(x0,x1,17):
        d.line((x,58,x+2,186),fill='#60323b',width=3)
im.convert('RGB').save(final,optimize=True)
results.append(verify_against_approved(
 'gallery5', original,final,
 [(202,45,328,212),(329,46,599,225),(609,45,735,212)],
 'Preserved palace E architecture + exact approved fixed sconces, vault lights and curtains from source generator, with 3 display frames excluded'))
# Rooms' coordinates remain authoritatively unchanged.
for n, expected in [('gallery3',2),('gallery4',1),('gallery5',0)]:
    p=ROOT/f'rooms/{n}/room.json'
    v=json.loads(p.read_text(encoding='utf-8'))
    assert len(v['objects'])==expected,(n,v['objects'])
    assert v['size']=={'width':930,'height':582}
(QA/'gallery345_qa.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
for item in results:
    print('PASS',item['room'],'frames',item['rear_frames_removed'],
          'outside_pixel_changes',item['changed_pixels_outside_frame_bounds'],
          'inside',item['changed_pixels_within_frame_bounds'],
          'base',item['architecture_base'])
