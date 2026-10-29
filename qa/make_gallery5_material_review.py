"""Gallery 5 material studies. Review PNGs only; no game assets are edited.
Reuses the approved Gallery 4 perspective floor/cornice as material reference.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"qa"/"gallery5-material-20261029"
OUT.mkdir(parents=True,exist_ok=True)
SRC=ROOT/"qa"/"architecture-bases-20261029"/"gallery4_v01_plain_west_passage_architecture_REVIEW.png"
OLD=ROOT/"rooms"/"gallery5"/"gallery5_palace_E.png"
W,H=930,582
rng=np.random.default_rng(51029)

def carpet(draw,variant):
    # Visual runner only. No fixtures, collision, or north-facing opening.
    draw.polygon([(423,245),(508,245),(612,581),(319,581)], fill="#1d171b")
    draw.polygon([(429,251),(502,251),(598,581),(333,581)], fill="#927148")
    draw.polygon([(433,253),(499,253),(590,581),(341,581)], fill="#381e24")
    draw.polygon([(438,260),(495,260),(576,581),(355,581)], fill="#632b39" if variant==1 else "#702c39")
    draw.line([(430,254),(336,581)],fill="#c4a26e",width=2)
    draw.line([(502,254),(596,581)],fill="#c4a26e",width=2)

def inset_frame(draw,box,bright=False):
    x0,y0,x1,y1=box
    # Shadow, mitred walnut, one thin brass accent.
    draw.rectangle((x0-3,y0-2,x1+4,y1+5), fill="#17100f")
    draw.rectangle((x0,y0,x1,y1), fill="#43231d",outline="#b69058",width=2)
    draw.rectangle((x0+4,y0+4,x1-4,y1-4), fill="#6d3037" if bright else "#472026",outline="#7a5039",width=2)
    draw.line((x0+5,y0+5,x1-5,y0+5), fill="#b87e64",width=1)
    draw.line((x0+5,y0+6,x0+5,y1-5), fill="#a8745f",width=1)

def wall_and_wood(im,variant):
    a=np.array(im.convert("RGB")).astype(np.float32)
    yy,xx=np.mgrid[0:H,0:W]
    grain=rng.normal(0,2.0,size=(H,W))
    # Dark stone retains source tile seams and perspective: no artificial grid.
    floor=yy>=221
    lum=np.mean(a,axis=2)
    ambient=8*np.exp(-((xx-465)/295)**2)
    st=63 + (lum-155)*.40 + ambient + grain*.50
    for c,k in enumerate((1.07,1.01,.96)):
        a[:,:,c]=np.where(floor,np.clip(st*k,20,130),a[:,:,c])
    # Deep burgundy fabric wall, with a restrained central illumination and textile grain.
    upper=(xx>=44)&(xx<886)&(yy>=39)&(yy<169)
    lamps=np.exp(-((xx-171)/92)**2)*10 + np.exp(-((xx-759)/92)**2)*10
    red=np.array([64,26,35] if variant==1 else [75,30,39],dtype=float)
    texture=np.sin(xx*.23)*.7+np.cos(yy*.31)*.8+grain
    shade=1+(lamps+6*np.exp(-((xx-465)/285)**2))/95+(yy-90)*.0001
    for c in range(3):
        a[:,:,c]=np.where(upper,np.clip(red[c]*shade+texture,0,255),a[:,:,c])
    # Replace the ordinary lower rails with rich walnut panels while retaining the original
    # source's natural shading variation; this visually binds gallery 5 to rooms 1-4.
    lower=(xx>=44)&(xx<886)&(yy>=167)&(yy<=221)
    walnuts=np.array([60,35,28] if variant==1 else [72,39,31],dtype=float)
    for c in range(3):
        a[:,:,c]=np.where(lower,np.clip(walnuts[c]+(lum-90)*.27+grain*.55,0,255),a[:,:,c])
    im=Image.fromarray(np.uint8(np.clip(a,0,255)),"RGB").convert("RGBA")
    d=ImageDraw.Draw(im)
    # Cornice stays aligned with the approved gallery backgrounds (same y16-39).
    d.line((44,39,885,39),fill="#d3a56b",width=2)
    d.line((44,41,885,41),fill="#39251e",width=3)
    d.line((44,164,885,164),fill="#bd8a57",width=2)
    d.line((44,169,885,169),fill="#261b18",width=3)
    d.line((44,212,885,212),fill="#be8e5e",width=2)
    d.line((44,219,885,219),fill="#191415",width=4)
    # Actual photo-shaded wooden panelling from the approved Gallery 4 art.
    # Re-tint the real bevels and grain, not a newly improvised flat vector pattern.
    panel=np.array(Image.open(SRC).convert("RGB").crop((78,169,121,218)),dtype=np.float32)
    tint=np.array([.70,.75,.89] if variant==1 else [.90,.86,.94],dtype=np.float32)
    panel=np.clip(panel*tint,0,255).astype("uint8")
    tile=Image.fromarray(panel,"RGB").convert("RGBA")
    for x in range(44,886,43):
        tile_w=min(43,886-x)
        im.paste(tile.crop((0,0,tile_w,49)),(x,170))
    d=ImageDraw.Draw(im)
    d.line((44,166,885,166),fill="#a47b55",width=2)
    d.line((44,216,885,216),fill="#bd8f5f",width=2)
    d.line((44,221,885,221),fill="#1a1212",width=4)
    return im

def draw_pilaster(im,x,variant):
    d=ImageDraw.Draw(im)
    dark="#281914" if variant==1 else "#503727"
    core="#5e3c2a" if variant==1 else "#a77b54"
    d.rectangle((x-14,40,x+14,210),fill=dark)
    # Approved-room pilaster supplies real shading; recolor it like antique wood.
    sample=Image.open(SRC).convert("RGB").crop((252,40,275,205)).resize((21,163))
    s=np.array(sample,dtype=np.float32)
    lum=s[:,:,0]*.30+s[:,:,1]*.58+s[:,:,2]*.12
    base=np.array([65,42,30] if variant==1 else [110,78,53],dtype=np.float32)
    gains=np.array([.38,.29,.24],dtype=np.float32)
    ret=np.clip(base[None,None,:]+(lum[:,:,None]-175)*gains[None,None,:],0,255).astype("uint8")
    im.paste(Image.fromarray(ret,"RGB"),(x-10,45))
    d.line((x-9,51,x-9,205),fill="#b28654",width=2)
    d.line((x+8,51,x+8,205),fill="#2d1d19",width=3)
    for offs in (-5,0,5):
        d.line((x+offs,59,x+offs,202),fill="#886043" if offs<0 else "#40271e",width=1)
    d.rectangle((x-16,42,x+16,55),fill="#6f5038" if variant==1 else "#a98c65",outline="#d2a570",width=2)
    d.line((x-12,47,x+12,47),fill="#e0bb85",width=2)
    d.rectangle((x-18,205,x+18,225),fill="#63432d" if variant==1 else "#896441",outline="#c79961",width=2)
    d.line((x-16,209,x+16,209),fill="#dbad75",width=2)
    d.line((x-17,220,x+17,220),fill="#261716",width=3)

def draw_arch_and_sidewalls(im,variant):
    d=ImageDraw.Draw(im)
    # Side returns, visibly continuing the architecture toward west/east portals.
    # No doors, floors/holes remain open.
    side="#53372e" if variant==1 else "#644639"
    hi="#775443" if variant==1 else "#85604b"
    for flip in (False,True):
        def p(x,y):return ((W-1-x) if flip else x,y)
        poly=[p(0,222),p(182,222),p(182,527),p(0,576)]
        d.polygon(poly,fill=side)
        d.polygon([p(0,222),p(182,222),p(181,233),p(0,242)],fill=hi)
        d.line([p(183,223),p(183,524)],fill="#1b1413",width=5)
        d.line([p(8,240),p(8,561)],fill="#9e7654",width=2)
        for gx in (4,11,21,28,37,45,161,168,176):
            for k in (0,1):
                d.line([p(gx+k*2,245),p(gx+k*2,521)],
                       fill="#76503b" if k==0 else "#3e2b23",width=1)
        # Flat wall becomes wood with inset plank frames, never blocking the portal.
        d.line([p(14,253),p(45,253),p(45,493)],fill="#bd8f60",width=2)
        d.line([p(161,250),p(177,250),p(177,502)],fill="#a77f59",width=2)
        # Paneling establishes a fine material texture without adding new fixtures.
        for x in (16,):
            d.line([p(x,244),p(x,553)],fill="#3b2923",width=3)
        # Receding arched opening: dark void with subtle floor beyond, not a locked door.
        a=p(59,339);b=p(147,483)
        xlo,xhi=sorted((a[0],b[0]))
        d.rectangle((xlo,330,xhi,488),fill="#101c1c")
        d.pieslice((xlo,282,xhi,389),180,360,fill="#101c1c")
        # Nested stone/bronze intrados: subdued gilt only on bevel.
        if not flip:
            arc=(51,275,155,375); arc2=(57,285,149,374)
            lx,rx=52,154
        else:
            arc=(W-156,275,W-52,375);arc2=(W-150,285,W-58,374)
            lx,rx=W-155,W-53
        d.arc(arc,180,360,fill="#b18a61",width=9)
        d.arc(arc2,180,360,fill="#dfb884",width=3)
        d.line((lx,324,lx,488),fill="#bb9063",width=8)
        d.line((rx,324,rx,488),fill="#4a342b",width=8)
        d.line((lx+4,338,lx+4,479),fill="#e0ba86",width=1)
        d.line((min(lx,rx),489,max(lx,rx),489),fill="#9e7753",width=4)
        # Floor continuation in passage opening at bottom; no physical door.
        d.polygon([p(59,472),p(146,472),p(156,497),p(54,497)],fill="#403936")
        d.line([p(60,483),p(145,483)],fill="#62534a",width=1)
        d.polygon([p(0,560),p(178,521),p(183,534),p(0,577)],fill="#352820")
        d.line([p(4,565),p(177,526)],fill="#9b7653",width=3)
    # Strong baseboard with real separation between rear wall and floor.
    d.line((183,224,744,224),fill="#a48059",width=3)
    d.line((183,228,744,228),fill="#201714",width=3)
    # Subtle room light reflected by central focal wall, not floodlit gold.
    return im

def draw_central_arch(im,variant):
    d=ImageDraw.Draw(im)
    color="#ba9567" if variant==1 else "#d0ab79"
    # E's central vault stays architectural, behind the large artwork.
    d.arc((310,35,620,155),180,360,fill="#2b1c18",width=11)
    d.arc((315,36,615,151),180,360,fill=color,width=5)
    d.arc((320,42,610,151),180,360,fill="#74553a",width=3)
    d.ellipse((457,35,473,51),fill="#7e5836",outline=color,width=2)
    d.rectangle((313,94,321,213),fill="#302019")
    d.rectangle((609,94,617,213),fill="#302019")
    d.line((321,92,321,211),fill="#b18b5c",width=2)
    d.line((610,92,610,211),fill="#b18b5c",width=2)
    return im

def sconce(im,x):
    d=ImageDraw.Draw(im)
    d.ellipse((x-8,111,x+8,128),fill="#432d20",outline="#b7955c",width=2)
    d.line((x,118,x,137),fill="#bd9663",width=3)
    for s in (-1,1):
        d.line((x,126,x+14*s,120),fill="#c29a67",width=3)
        d.ellipse((x+14*s-4,113,x+14*s+4,121),fill="#d9b47a")
        d.ellipse((x+14*s-2,108,x+14*s+2,114),fill="#fff0be")
    # No extra lamps or chandeliers; 2 approved E wall lights only.

def velvet_texture(im,variant):
    # Fabric grain on the approved runner's trapezoid.
    a=np.asarray(im.convert("RGB")).copy()
    yy,xx=np.mgrid[0:H,0:W]
    t=np.clip((yy-258)/323,0,1)
    left=440-85*t
    right=493+83*t
    mask=(yy>=261)&(xx>left)&(xx<right)
    noise=np.random.default_rng(198).normal(0,3,(H,W))
    v=4*np.sin(xx*.22+yy*.045)+noise
    for c in range(3):
        a[:,:,c][mask]=np.clip(a[:,:,c][mask].astype(float)+v[mask]*(.7 if c==0 else .3),0,255)
    return Image.fromarray(a,"RGB").convert("RGBA")

def placeholders(im):
    d=ImageDraw.Draw(im)
    for i,(x0,y0,x1,y1) in enumerate(((225,84,296,197),(340,87,588,206),(635,84,706,197))):
        d.rectangle((x0-8,y0-7,x1+9,y1+10),fill="#211615",outline="#513626",width=3)
        d.rectangle((x0-5,y0-5,x1+5,y1+5),fill="#815b34",outline="#dfbb7d",width=3)
        d.rectangle((x0-1,y0-1,x1+1,y1+1),fill="#32261e",outline="#ad7c48",width=2)
        d.rectangle((x0+5,y0+5,x1-5,y1-5),fill="#253d35",outline="#765d43",width=2)
        # Placeholder blank: never suggest an actual photo or artwork exists.
        d.line((x0+9,y0+9,x1-9,y0+9),fill="#425c51",width=1)
    return im

def compose(v):
    im=Image.open(SRC).convert("RGBA")
    im=wall_and_wood(im,v)
    im=draw_arch_and_sidewalls(im,v)
    for x in (61,190,319,611,739,869):
        draw_pilaster(im,x,v)
    im=draw_central_arch(im,v)
    for x in (177,753):
        sconce(im,x)
    d=ImageDraw.Draw(im)
    # Southern passage: open over the last tiles, bounded by side thresholds.
    d.line((383,581,411,526),fill="#a57c50",width=5)
    d.line((518,526,548,581),fill="#a57c50",width=5)
    d.line((411,525,518,525),fill="#5d4837",width=5)
    carpet(d,v)
    im=velvet_texture(im,v)
    assert im.size==(930,582)
    p=OUT/f"gallery5_v0{v}_material_architecture_REVIEW.png"
    im.convert("RGB").save(p)
    q=OUT/f"gallery5_v0{v}_material_3frame_mock_REVIEW.png"
    placeholders(im.copy()).convert("RGB").save(q)
    return p,q

def compare():
    old=Image.open(OLD).convert("RGB")
    first=Image.open(OUT/"gallery5_v01_material_3frame_mock_REVIEW.png")
    second=Image.open(OUT/"gallery5_v02_material_3frame_mock_REVIEW.png")
    for a,b,fn in [(old,first,"gallery5_original_E_vs_v01_REVIEW.png"),(first,second,"gallery5_v01_vs_v02_REVIEW.png")]:
        out=Image.new("RGB",(1864,618),"#f0ede8")
        d=ImageDraw.Draw(out)
        out.paste(a,(0,36));out.paste(b,(934,36))
        d.text((12,10),"LEFT: previous visual E / version 01" if a is old else "LEFT: v01 walnut",fill="#171b1a")
        d.text((946,10),"RIGHT: proposed material v01" if a is old else "RIGHT: proposed material v02",fill="#171b1a")
        out.save(OUT/fn)
for v in (1,2):
    compose(v)
compare()
print("Generated",*[p.name for p in OUT.glob("*.png")],sep="\n - ")
