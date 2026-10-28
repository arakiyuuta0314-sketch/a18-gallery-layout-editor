"""Gallery2 layout concepts. Preview only; no game/export changes."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from pathlib import Path
from random import Random

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'rooms'/'gallery2'/'concepts'
OUT.mkdir(parents=True,exist_ok=True)
SRC=Image.open(ROOT/'rooms'/'gallery1'/'architecture.png').convert('RGBA')
W,H=930,582
font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',36)
tiny=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
rng=Random(20028)

def woodfill(d, box):
    x1,y1,x2,y2=box
    d.rectangle(box,fill='#5c3420')
    for y in range(y1+3,y2-1,5):
        d.line((x1,y,x2,y),fill='#764729' if (y//5)%2 else '#422519',width=1)

def frame(d,x,y,w,h,n):
    d.rectangle((x+4,y+5,x+w+5,y+h+6),fill='#1d211a')
    d.rectangle((x-5,y-5,x+w+5,y+h+5),fill='#4a2a18')
    d.rectangle((x-2,y-3,x+w+2,y+h+2),outline='#bf8050',width=3)
    d.rectangle((x+4,y+3,x+w-4,y+h-3),fill='#775031')
    d.rectangle((x+10,y+9,x+w-10,y+h-9),fill='#284d41')
    d.rectangle((x+14,y+13,x+w-14,y+h-13),fill='#31594c')
    d.line((x+6,y+4,x+w-6,y+4),fill='#e0ac67',width=2)
    d.text((x+w/2,y+h/2),str(n),font=font,fill='#f1d6a3',anchor='mm')

def architecture():
    im=Image.new('RGBA',(W,H),'#d1c0ab')
    im.alpha_composite(SRC.crop((0,220,W,H)),(0,220))
    d=ImageDraw.Draw(im)
    # Upper architectural structure with sage wall, warm carved wood and cream pillars.
    d.rectangle((0,0,W,219),fill='#26463d')
    for x in range(0,W,4):
        c='#29473e' if x%12<5 else '#2d4b42'
        d.line((x,35,x,166),fill=c,width=2)
    woodfill(d,(0,0,W,35))
    d.rectangle((0,8,W,14),fill='#9e6b3c')
    d.line((0,31,W,31),fill='#d0a070',width=2)
    woodfill(d,(0,171,W,218))
    d.line((0,170,W,170),fill='#c59a67',width=4)
    d.line((0,214,W,214),fill='#bc8754',width=3)
    for x in range(8,W,44):
        d.rectangle((x,181,x+36,209),fill='#482a1c',outline='#97633e',width=2)
        d.rectangle((x+4,185,x+32,205),outline='#603922',width=2)
    for x in (24,323,551,870):
        d.rectangle((x-17,35,x+18,218),fill='#d4c4a4',outline='#4b2c1c',width=4)
        d.rectangle((x-10,37,x+11,159),fill='#eee0c6')
        d.line((x-12,157,x+15,157),fill='#bc9666',width=4)
        d.rectangle((x-22,24,x+23,39),fill='#70462a',outline='#cc9558',width=2)
    # Two architectural frames: third frame deliberately goes to the floor.
    frame(d,99,77,165,83,1)
    frame(d,368,77,153,83,2)
    # Offset NORTH door: Gallery4, still locked on museum Lv3
    dx1,dx2=656,764
    d.rounded_rectangle((dx1-11,35,dx2+11,219),radius=37,fill='#4b2b1a',outline='#a97440',width=5)
    d.rounded_rectangle((dx1+2,45,dx2-2,219),radius=31,fill='#102b29')
    d.ellipse((dx1+11,47,dx2-11,124),fill='#14312d')
    d.rectangle((dx1+11,86,dx2-11,212),fill='#14312d')
    for x in (dx1+20,dx2-20):
        d.line((x,96,x,205),fill='#294a42',width=5)
    d.rectangle((dx1+7,209,dx2-7,221),fill='#6e4325',outline='#bc8856',width=3)
    # Small lock cartouche is a provisional door-state cue.
    d.rounded_rectangle((696,127,724,154),radius=5,fill='#a77e4c',outline='#f3d39b',width=2)
    d.arc((702,116,718,137),180,360,fill='#dfc392',width=3)
    # West entrance in left foreground, no east connection.
    d.polygon([(0,267),(33,273),(62,292),(64,462),(34,478),(0,480)],fill='#4b2c20')
    d.polygon([(0,284),(17,288),(40,309),(40,444),(18,456),(0,456)],fill='#102f2a')
    d.line([(0,271),(35,276),(60,300),(60,463)],fill='#c38b57',width=5)
    d.rectangle((40,315,46,453),fill='#a46a3d')
    d.polygon([(880,257),(930,245),(930,581),(909,581),(896,465)],fill='#402e25')
    d.line([(880,257),(901,254),(901,465)],fill='#b17c4f',width=5)
    for y in (313,399,484):
        d.line((901,y,930,y-8),fill='#855737',width=3)
    return im

def screen(num,w,h,kind='flat'):
    im=Image.new('RGBA',(w,h))
    d=ImageDraw.Draw(im)
    # Pixel-art independent screen with side depth, not a background-level photo.
    d.polygon(((5,11),(w-14,11),(w-1,22),(w-1,h-2),(15,h-2),(4,h-14)),fill='#422516')
    d.rectangle((0,0,w-16,h-13),fill='#62351f',outline='#bd8751',width=3)
    d.rectangle((10,9,w-26,h-34),fill='#234c40',outline='#b17c4d',width=2)
    d.line((0,4,w-14,4),fill='#dda66b',width=3)
    d.line((4,h-18,w-17,h-18),fill='#d09a5d',width=4)
    d.line((w-16,5,w-16,h-15),fill='#2f1d14',width=5)
    for xx in range(18,w-34,37):
        d.rectangle((xx,h-31,xx+30,h-19),outline='#946039',width=2)
    if kind=='double':
        # Connected two-face island for candidate B.
        for i,x in enumerate((42,w-140)):
            frame(d,x,34,102,79,num+i)
    else:
        fw=min(142,w-62);fh=min(83,h-69)
        frame(d,(w-16-fw)//2,33,fw,fh,num)
    return im

BG=architecture()
BG.save(OUT/'architecture_draft.png')
layouts={
  'A':{'title':'Staggered passage / 段違い回遊','obj':[(3,132,306,218,178,'flat'),(4,388,343,206,174,'flat'),(5,681,351,179,175,'flat')]},
  'B':{'title':'Central island / 中央の展示島','obj':[(3,248,337,350,185,'double'),(5,693,322,179,176,'flat')]},
  'C':{'title':'Open salon / ひらけた小広場','obj':[(3,128,287,221,177,'flat'),(4,375,339,220,171,'flat'),(5,684,331,178,180,'flat')]},
}
for key,spec in layouts.items():
    out=BG.copy()
    # Add soft contact shadow, independent-wall sprites front/back simulated.
    dr=ImageDraw.Draw(out,'RGBA')
    for n,x,y,w,h,kind in spec['obj']:
        dr.ellipse((x+12,y+h-23,x+w-3,y+h-3),fill=(18,24,16,58))
    for n,x,y,w,h,kind in spec['obj']:
        out.alpha_composite(screen(n,w,h,kind),(x,y))
    out.save(OUT/f'gallery2_concept_{key}.png')
# One stitched sheet with original 930x582 pixels per concept.
sheet=Image.new('RGBA',(W*3,H),'#faf8f3')
for i,k in enumerate('ABC'):
    sheet.alpha_composite(Image.open(OUT/f'gallery2_concept_{k}.png'),(i*W,0))
sheet.save(OUT/'gallery2_comparison_ABC.png')
print('Created',str(OUT),[(p.name,p.stat().st_size) for p in sorted(OUT.glob('*.png'))])
