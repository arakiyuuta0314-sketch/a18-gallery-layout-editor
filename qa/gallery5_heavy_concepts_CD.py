"""Gallery5 C/D: solemn old-master hall, design studies only, no saved fixture changes."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageEnhance,ImageFont
import math,hashlib
root=Path(__file__).resolve().parents[1]
out=root/'rooms/gallery5'
assert out.is_dir()
orig=out/'gallery5_architecture_only.png'
orig_hash=hashlib.sha256(orig.read_bytes()).hexdigest()
W,H=930,582
base=Image.open(orig).convert('RGB')
assert base.size==(W,H)
font=ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc',26)
subfont=ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc',17)
def rect(d,xy,fill,outline=None,width=1):
 d.rectangle(xy,fill=fill,outline=outline,width=width)
def lighten(a,b,p):
 return tuple(int(a[k]*(1-p)+b[k]*p) for k in range(3))
def structure():
 im=base.copy()
 # Brown-stone/charcoal darkening above, and preserved legible floor pattern.
 d=ImageDraw.Draw(im)
 for y in range(36,222):
  t=(y-36)/185
  dark=lighten((35,40,37),(50,42,34),t)
  d.line((0,y,929,y),fill=dark)
 # Wide wall panels of deep wine-brown walnut, a deliberately warmer contrast.
 for x0,x1 in [(21,174),(196,322),(339,597),(614,736),(758,910)]:
  d.rectangle((x0,44,x1,212),fill='#3c2b27',outline='#7e5b40',width=3)
  d.rectangle((x0+8,51,x1-8,209),fill='#48352d',outline='#1e2524',width=3)
  d.line((x0+12,57,x1-12,57),fill='#a07c52',width=2)
  d.line((x0+12,199,x1-12,199),fill='#a07c52',width=2)
  d.line((x0+16,62,x0+16,195),fill='#594536',width=2)
 # Raised deep center shrine: architectural alcove, not an extra frame.
 d.polygon([(325,35),(610,35),(624,222),(306,222)],fill='#191c1e')
 d.rounded_rectangle((330,49,608,221),radius=12,fill='#272b2a',outline='#9d7747',width=4)
 d.rounded_rectangle((340,56,597,216),radius=9,fill='#343530',outline='#4d4437',width=6)
 # Large arched canopy
 d.arc((313,34,625,170),180,360,fill='#c8a16c',width=8)
 d.arc((320,41,618,174),180,360,fill='#765634',width=5)
 # Layered roof cornice. Architectural not illumination.
 for y0,y1,col in [(0,6,'#1b1d1c'),(7,12,'#4c392d'),(13,16,'#bd9863'),(17,25,'#3c2e25'),(26,30,'#906c47'),(31,36,'#281f1d')]:
  rect(d,(0,y0,929,y1),col)
 # Pilasters support roof on each side of central recess.
 for x in (20,184,319,611,747,914):
  d.rectangle((x-12,36,x+12,221),fill='#1e211f',outline='#b28a56',width=2)
  d.rectangle((x-8,42,x+8,214),fill='#5f5142')
  d.rectangle((x-4,43,x+5,209),fill='#796750')
  d.line((x-4,45,x-4,207),fill='#c8a67b',width=1)
  d.rectangle((x-18,39,x+18,52),fill='#9b7e58',outline='#c5a373',width=2)
  d.rectangle((x-20,206,x+20,224),fill='#9b7d5b',outline='#3b291f',width=2)
 # Baseboard dark timber, stepped.
 rect(d,(0,223,929,228),'#241c1a')
 d.line((0,228,929,228),fill='#a58254',width=3)
 # Re-paste full passage arches from untouched three-door museum geometry.
 im.paste(ImageEnhance.Brightness(base.crop((0,220,184,538))).enhance(.76),(0,220))
 im.paste(ImageEnhance.Brightness(base.crop((746,220,930,538))).enhance(.76),(746,220))
 # Dark side stone buttresses on top, without blocking their openings.
 d=ImageDraw.Draw(im)
 for x in (0,179,745,926):
  d.line((x,229,x,502),fill='#69523d',width=4)
 # Preserve front south entrance and foreground tile work.
 im.paste(base.crop((367,525,572,582)),(367,525))
 # Polished dark-stone floor; keep every original perspective tile seam.
 pixels=im.load()
 for y in range(231,H):
  for x in range(W):
   if y<538 and (x<184 or x>=746):continue
   r,g,b=pixels[x,y]
   edge=(abs(x-465)/465)**1.5
   light=1.0-(0.22*edge)
   # Stone grayscale retains tile grid and restrained warm reflections.
   value=(.28*r+.57*g+.15*b)
   pixels[x,y]=(int((.48*value+28)*light),int((.47*value+23)*light),int((.43*value+23)*light))
 # Keep the threshold a readable, slightly lighter connection to the entrance.
 d=ImageDraw.Draw(im)
 d.line((373,578,429,530),fill='#8b7657',width=3)
 d.line((567,578,512,530),fill='#8b7657',width=3)
 return im
def gold_frame(im,n,box,major=False):
 x,y,w,h=box;d=ImageDraw.Draw(im)
 # Drop shadow and three timber/gilt molding bands.
 d.rounded_rectangle((x+4,y+7,x+w+7,y+h+9),radius=3,fill='#101615')
 rect(d,(x-9,y-9,x+w+9,y+h+9),'#201d1c','#6c4c30',2)
 rect(d,(x-6,y-6,x+w+6,y+h+6),'#86633c','#d8b37c',3)
 rect(d,(x-1,y-1,x+w+1,y+h+1),'#392b23','#c49b5a',2)
 rect(d,(x+7,y+7,x+w-7,y+h-7),'#183b33','#ad8451',2)
 # Decorative corner rosettes and a centered keystone
 for px in (x-6,x+w+6):
  for py in (y-6,y+h+6):
   d.ellipse((px-3,py-3,px+3,py+3),fill='#e2c391',outline='#654526',width=1)
 d.polygon([(x+w/2-7,y-9),(x+w/2+7,y-9),(x+w/2+4,y+1),(x+w/2-4,y+1)],fill='#ddc090')
 d.text((x+w/2,y+h/2),str(n),font=font,fill='#f2dbb5',anchor='mm')
 if major:
  # Gilded crown and small sculpted finial without adding another picture.
  d.line((x-12,y-14,x+w+12,y-14),fill='#b99a6b',width=4)
  d.line((x+6,y-19,x+w-6,y-19),fill='#d4b886',width=2)
  d.ellipse((x+w/2-6,y-28,x+w/2+6,y-17),fill='#b49a6d',outline='#efe1ba')
def lamps(im):
 d=ImageDraw.Draw(im)
 for x in (185,746):
  # Sconces are part of the wall, avoid covering exhibit artwork.
  d.line((x-4,95,x-4,147),fill='#c8a66b',width=3)
  d.line((x+4,95,x+4,147),fill='#c8a66b',width=3)
  d.ellipse((x-9,80,x+9,99),fill='#f0d7a5',outline='#9b7041',width=3)
  d.polygon([(x-11,121),(x+11,121),(x+6,149),(x-6,149)],fill='#a67844')
  d.line((x-13,152,x+13,152),fill='#dab88a',width=3)
def build(which):
 im=structure()
 lamps(im)
 if which=='C':
  frames=[(1,(215,82,91,121)),(2,(342,77,246,139)),(3,(628,82,91,121))]
 else:
  frames=[(1,(210,76,98,53)),(2,(210,150,98,53)),(3,(342,77,246,139)),
          (4,(627,76,98,53)),(5,(627,150,98,53))]
 for n,b in frames:gold_frame(im,n,b,major=n==(2 if which=='C' else 3))
 # Low geometric molding at center, leaves all pathways visually empty.
 d=ImageDraw.Draw(im)
 d.polygon([(309,229),(621,229),(637,239),(293,239)],fill='#4d4235')
 d.line((310,228,619,228),fill='#c3a276',width=3)
 return im
arch=structure()
arch.save(out/'gallery5_heavy_architecture_C.png')
for name in ('C','D'):
 build(name).save(out/f'gallery5_heavy_{name}.png')
comparison=Image.new('RGB',(1904,639),'#eeeae3')
d=ImageDraw.Draw(comparison)
head=ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc',20)
d.text((12,12),'C案｜3作品・中央を主役にした重厚な特別室',fill='#384638',font=head)
d.text((963,12),'D案｜5作品・中央主役＋左右2段',fill='#384638',font=head)
comparison.paste(Image.open(out/'gallery5_heavy_C.png'),(12,48))
comparison.paste(Image.open(out/'gallery5_heavy_D.png'),(962,48))
comparison.save(out/'gallery5_heavy_C_D_comparison.png')
assert hashlib.sha256(orig.read_bytes()).hexdigest()==orig_hash
print('PASS gallery5 heavy C(3),D(5), unapproved; architecture base unchanged')
