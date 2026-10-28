"""A18 Gallery 5: E/F palace-grade concept previews, 3 and 5 works (NOT approved).
Build on preserved heavy-C architecture; never overwrite old concepts or game fixtures.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"rooms/gallery5"
SOURCE=OUT/"gallery5_heavy_architecture_C.png"
ORIG_HASH=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
W,H=930,582
NUM=ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc",30)
SMALL=ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc",16)
def radial(im, cx,cy,rx,ry,rgb,a):
 layer=Image.new("RGBA",im.size,(0,0,0,0)); pix=layer.load()
 for y in range(max(0,round(cy-ry)),min(H,round(cy+ry))):
  for x in range(max(0,round(cx-rx)),min(W,round(cx+rx))):
   t=((x-cx)/rx)**2+((y-cy)/ry)**2
   if t<1:pix[x,y]=(*rgb,int(a*(1-t)**2))
 return Image.alpha_composite(im,layer)
def filigree(d,x,y,scale=1,mirror=1):
 # Subtle classical relief: gold flowers + curled stems (wall corners only).
 s=scale; m=mirror
 pts=[(0,0),(6,4),(11,13),(8,23),(2,30)]
 path=[(round(x+m*px*s),round(y+py*s)) for px,py in pts]
 d.line(path,fill="#aa8555",width=2)
 d.arc((round(x+m*(2 if m>0 else 22)*s),round(y+9*s),round(x+m*(22 if m>0 else 2)*s),round(y+28*s)),0,185,fill="#c3a36b",width=2)
 for k in (0,1,2):
  xx=x+m*(7+k*4)*s; yy=y+(k*8+9)*s
  d.ellipse((xx-2*s,yy-2*s,xx+2*s,yy+2*s),fill="#d7b784")
def base_palace():
 im=Image.open(SOURCE).convert("RGBA")
 d=ImageDraw.Draw(im)
 # Coffered palace cornice and carved dentils remain at top, without replacing wall geometry.
 for x in range(30,920,62):
  d.rounded_rectangle((x,2,x+41,23),radius=3,fill="#392c25",outline="#9a7952",width=2)
  d.line((x+5,7,x+36,7),fill="#d4b384",width=2)
  d.line((x+5,18,x+36,18),fill="#6a4a36",width=2)
 for x in range(8,930,18):
  d.rectangle((x,25,x+8,32),fill="#b18a5e",outline="#2c241e",width=1)
 d.line((0,34,929,34),fill="#e2c58e",width=3)
 # Deep-burgundy velvet panel inserts and double raised brass inlay.
 for x0,x1 in ((38,161),(202,301),(631,724),(764,892)):
  d.rounded_rectangle((x0,53,x1,196),radius=5,fill="#42262b",outline="#98784d",width=3)
  d.rounded_rectangle((x0+8,60,x1-8,190),radius=3,fill="#4d2b30",outline="#a78857",width=1)
  d.line((x0+11,64,x1-11,64),fill="#65494a",width=1)
  if x1-x0>110:
   filigree(d,x0+16,72,0.8,1);filigree(d,x1-16,72,0.8,-1)
 # Carved fluted pilaster shafts. The old architecture shape remains underneath.
 for x in (21,184,319,611,747,912):
  d.rectangle((x-11,47,x+11,208),fill="#78644d",outline="#3a3129",width=2)
  for dx in (-7,-3,2,7): d.line((x+dx,56,x+dx,205),fill="#a98a63" if dx==-7 else "#534b40",width=1)
  d.rectangle((x-18,39,x+18,55),fill="#a58b65",outline="#e1c595",width=2)
  d.rectangle((x-22,210,x+22,229),fill="#94734f",outline="#d9b986",width=2)
  d.line((x-19,217,x+19,217),fill="#e3c891",width=2)
  # capitals curl away from artwork
  d.arc((x-20,47,x-4,63),180,355,fill="#e4c78d",width=2)
  d.arc((x+4,47,x+20,63),180,355,fill="#e4c78d",width=2)
 # Antique stone panels at side arch with gold outline, openings not occluded.
 for left,right in ((53,152),(778,877)):
  d.arc((left,282,right,377),180,360,fill="#d3b782",width=5)
  d.line((left,328,left,485),fill="#cba96c",width=4)
  d.line((right,328,right,485),fill="#cba96c",width=4)
  d.line((left+7,331,left+7,466),fill="#755839",width=2)
  d.line((right-7,331,right-7,466),fill="#755839",width=2)
 # Central arched vault above focal image, layered stone and discreet rococo scroll.
 d.arc((313,27,618,150),180,360,fill="#e2c58b",width=8)
 d.arc((325,38,606,155),180,360,fill="#947248",width=4)
 d.ellipse((453,25,478,50),fill="#be955c",outline="#f5dcac",width=3)
 d.arc((430,35,458,56),35,270,fill="#e7d0a0",width=2)
 d.arc((473,35,501,56),265,155,fill="#e7d0a0",width=2)
 # Massive dark stone base beneath artwork, without protruding into walk path.
 d.polygon([(310,223),(619,223),(628,233),(299,233)],fill="#a18b68")
 d.polygon([(303,233),(627,233),(638,243),(292,243)],fill="#3e352f")
 d.line((305,230,624,230),fill="#d9be8a",width=3)
 # Coherent palace carpet: red center runner from the south entrance toward the feature wall.
 # Its footprint remains visual only; never generates collision.
 d.polygon([(424,246),(507,246),(607,580),(322,580)],fill="#241b20")
 d.polygon([(429,251),(502,251),(592,581),(337,581)],fill="#b99a64")
 d.polygon([(435,257),(496,257),(584,581),(345,581)],fill="#471d2b")
 d.polygon([(440,261),(492,261),(570,581),(360,581)],fill="#6c2835")
 for t in (0.19,0.37,0.59,0.83):
  y=int(260+(580-260)*t);left=int(442-82*t);right=int(490+82*t)
  d.line((left+8,y,right-8,y),fill="#b18b58",width=2)
  d.line((left+14,y+5,right-14,y+5),fill="#7c4950",width=1)
  mx=(left+right)//2
  d.polygon([(mx,y+5),(mx+5+5*t,y+12+5*t),(mx,y+18+7*t),(mx-5-5*t,y+12+5*t)],outline="#c4a36e")
 # South side threshold remains centered. Burgundy carpet meets, not hides, the doorway.
 im=radial(im,467,84,325,260,(246,204,145),36)
 for x in (183,746):
  im=radial(im,x,133,70,118,(255,212,137),75)
 return im
def gallery_frame(im,num,x,y,w,h,signature=False):
 d=ImageDraw.Draw(im)
 # Bespoke thick gilt frame whose mount, shine and rosettes are separable in future.
 d.rounded_rectangle((x+5,y+8,x+w+9,y+h+10),radius=3,fill="#161715")
 for pad,stroke,border in ((11,"#1d1f1d","#6e4b2d"),(8,"#85552b","#f1cd85"),
                            (5,"#c29856","#f2dba2"),(1,"#4a3325","#c6a166")):
  d.rectangle((x-pad,y-pad,x+w+pad,y+h+pad),fill=stroke,outline=border,width=2)
 d.rectangle((x+7,y+7,x+w-7,y+h-7),fill="#23483f",outline="#d9b984",width=2)
 d.rectangle((x+14,y+14,x+w-14,y+h-14),fill="#173d34",outline="#8f7553",width=1)
 # Thin dimensional highlights convey gilding, not a plain yellow rectangle.
 d.line((x-6,y-7,x+w+7,y-7),fill="#f4dca7",width=2)
 d.line((x-6,y-7,x-6,y+h+7),fill="#d0a66d",width=2)
 d.line((x+w+7,y-7,x+w+7,y+h+7),fill="#6b4e31",width=3)
 d.line((x-6,y+h+7,x+w+7,y+h+7),fill="#77532f",width=3)
 for xx in (x-8,x+w+8):
  for yy in (y-8,y+h+8):
   d.ellipse((xx-5,yy-5,xx+5,yy+5),fill="#b99051",outline="#f7dea1",width=2)
   d.ellipse((xx-2,yy-2,xx+2,yy+2),fill="#fff0bc")
 # Sculpted crowns and small gold cartouche.
 if signature:
  d.line((x-17,y-20,x+w+17,y-20),fill="#c2a074",width=5)
  d.line((x+1,y-27,x+w-1,y-27),fill="#e0be84",width=2)
  d.arc((x+w/2-32,y-41,x+w/2+32,y+3),180,355,fill="#b99161",width=4)
  d.ellipse((x+w/2-11,y-43,x+w/2+11,y-27),fill="#a58152",outline="#f5dfb1",width=2)
  for cx in (x+20,x+w-20):
   d.ellipse((cx-5,y-25,cx+5,y-16),fill="#ceae77",outline="#f4dba9")
 d.text((x+w/2,y+h/2),str(num),font=NUM,fill="#f5e2bf",anchor="mm")
def candle_lights(im):
 # Wall chandeliers/sconces at both sides, kept away from artwork and doors.
 d=ImageDraw.Draw(im)
 for x in (185,746):
  d.ellipse((x-17,92,x+17,122),fill="#3b2c25",outline="#ae8b56",width=3)
  for dx in (-17,17):
   d.line((x,119,x+dx,128),fill="#a88455",width=4)
   d.line((x+dx,117,x+dx,102),fill="#dbc190",width=3)
   d.ellipse((x+dx-4,95,x+dx+4,105),fill="#f5dfac")
  d.line((x-18,118,x+18,118),fill="#edce9b",width=3)
  d.ellipse((x-4,118,x+4,131),fill="#ddba7d")
 # Tiny light sources along the upper feature vault, not a giant ceiling chandelier.
 for x in (360,571):
  d.ellipse((x-5,54,x+5,65),fill="#e7cb93",outline="#886740",width=2)
def make(name):
 im=base_palace()
 candle_lights(im)
 # Inner maroon vertical curtains add a historic palace look, but never conceal frames.
 d=ImageDraw.Draw(im)
 for x0,x1 in ((57,162),(761,868)):
  for x in range(x0,x1,17):
   d.line((x,58,x+2,186),fill="#60323b",width=3)
 if name=="E":
  fixtures=[(1,219,88,92,111),(2,346,89,236,123),(3,626,88,92,111)]
 else:
  fixtures=[(1,215,72,92,51),(2,215,153,92,51),
            (3,346,89,236,123),(4,625,72,92,51),(5,625,153,92,51)]
 for n,x,y,w,h in fixtures:
  gallery_frame(im,n,x,y,w,h,signature=(n==(2 if name=="E" else 3)))
 return im.convert("RGB")
original=Image.open(OUT/"gallery5_heavy_C.png").convert("RGB")
arch=base_palace().convert("RGB")
arch.save(OUT/"gallery5_palace_architecture_E.png")
for variant in ("E","F"):
 make(variant).save(OUT/f"gallery5_palace_{variant}.png")
compare=Image.new("RGB",(1904,640),"#ede8e0")
d=ImageDraw.Draw(compare)
title=ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc",20)
d.text((12,15),"C案：前回の重厚な展示室（3枠）",fill="#334036",font=title)
d.text((962,15),"E案：宮殿風・柱と金装飾・絨毯（3枠）",fill="#334036",font=title)
compare.paste(original,(12,48))
compare.paste(Image.open(OUT/"gallery5_palace_E.png"),(962,48))
compare.save(OUT/"gallery5_C_vs_E_palace.png")
compare2=Image.new("RGB",(1904,640),"#ede8e0")
d=ImageDraw.Draw(compare2)
d.text((12,15),"E案：宮殿の特別展示室（3枠）",fill="#334036",font=title)
d.text((962,15),"F案：同じ宮殿装飾で5枠を維持",fill="#334036",font=title)
compare2.paste(Image.open(OUT/"gallery5_palace_E.png"),(12,48))
compare2.paste(Image.open(OUT/"gallery5_palace_F.png"),(962,48))
compare2.save(OUT/"gallery5_palace_E_vs_F.png")
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==ORIG_HASH
assert Image.open(OUT/"gallery5_palace_E.png").size==(930,582)
print("PASS palace E=3 and F=5, original heavy-C architecture byte unchanged")
