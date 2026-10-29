# A18 gallery5 v13: material and side-passage reconstruction using existing approved entrance pixels.
# Original gallery5_palace_E.png is preserved; this script generates review material only.
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageFont
import numpy as np,cv2,math
ROOT=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
SRC=Image.open(r"C:\Users\User\source\repos\web-tools-preview-a18-entrance-2d-assets-20261028\a18\layout-test\assets\entrance\approved_initial_20261027\entrance_background_initial_approved.png").convert("RGB")
LV6=Image.open(ROOT/"architecture-review/entrance-comparison/entrance-lv6-approved.png").convert("RGB")
E=Image.open(ROOT/"rooms/gallery5/gallery5_palace_E.png")
W,H=930,582; S=2
def tint(im,color,strength=.65,brightness=1.0):
    a=np.asarray(im.convert("RGB")).astype(np.float32); c=np.array(color,dtype=np.float32)
    lum=a@np.array([.299,.587,.114],dtype=np.float32)
    # Reinterpret diffuse surface reflectance, retaining the texture's local contrast.
    ref=(lum-145)*.55
    out=(c[None,None,:]+ref[:,:,None])*brightness
    out=out*(strength)+(1-strength)*a
    return Image.fromarray(np.uint8(np.clip(out,0,255)))
def paste_mask(img,source,mask):
    img.paste(source,(0,0),mask)
def quad_mask(poly):
    m=Image.new("L",(W,H),0);ImageDraw.Draw(m).polygon(poly,fill=255);return m
def homography_tex(texture,quad,sw=None,sh=None):
    tex=np.asarray(texture.convert('RGB'));h,w=tex.shape[:2]
    p1=np.float32([[0,0],[w-1,0],[w-1,h-1],[0,h-1]])
    p2=np.float32(quad)
    M=cv2.getPerspectiveTransform(p1,p2)
    result=cv2.warpPerspective(tex,M,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT_101)
    mask=cv2.warpPerspective(np.full((h,w),255,dtype=np.uint8),M,(W,H),flags=cv2.INTER_LINEAR)
    return Image.fromarray(result),Image.fromarray(mask)
def line_multi(d,points,layers):
    for width,color in layers:d.line(points,fill=color,width=width,joint="curve")
def points_arc(cx,top_y,radx,rady,count=60):
    return [(cx+radx*math.cos(t),top_y+rady*(1-math.sin(t))) for t in np.linspace(math.pi,0,count)]
def inner_arch(cx,ytop,rx,ry,leftbot,rightbot):
    # top is semicircle flattening from center ytop to shoulder ytop+ry
    pts=points_arc(cx,ytop,rx,ry)
    return pts+[(cx+rx,rightbot),(cx-rx,leftbot)]
def woodstrip(w,h,crop,shade=(1,1,1)):
    raw=SRC.crop(crop).resize((w,h),Image.Resampling.LANCZOS)
    a=np.asarray(raw).astype(np.float32);a=a*np.array(shade)[None,None,:]
    return Image.fromarray(np.uint8(np.clip(a,0,255)))
# -------------------------------------------------------------------
# Gallery floor: actual approved entrance stone joints with deep taupe slate tone.
# Start with a single non-stretched stone surface, maintaining converging grout geometry.
out=Image.new("RGB",(W,H),(22,16,14))
floor=SRC.crop((100,518,1222,949)).resize((W,H-222),Image.Resampling.LANCZOS)
fa=np.asarray(floor).astype(np.float32)
gray=fa@np.array([.30,.59,.11],dtype=np.float32)
# Preserve source tile micro-contrast and mortar, recolor material (not blur/noise overlay).
base=np.stack((gray*.73-15,gray*.72-14,gray*.70-12),axis=2)
base=np.clip(base,36,214).astype('uint8')
floor=Image.fromarray(base)
out.paste(floor,(0,222))
# Ambient shade at foot of rear wall
ov=Image.new('RGBA',(W,H),(0,0,0,0));od=ImageDraw.Draw(ov)
for y in range(222,270):
    od.line((180,y,750,y),fill=(17,9,6,int(56*(1-(y-222)/48))),width=1)
out=Image.alpha_composite(out.convert('RGBA'),ov).convert('RGB')
# -------------------------------------------------------------------
# Continuous walnut wall: base field derived from entrance teal wall's real diffuse shading.
wall=SRC.crop((77,103,505,389)).resize((W,223),Image.Resampling.LANCZOS)
wall=tint(wall,(108,44,53),strength=.98)
out.paste(wall,(0,0))
# textured wainscoting cut from real antique wood panels, composed in long panels
panel_source=SRC.crop((67,398,505,512))
panel_scaled=panel_source.resize((444,73),Image.Resampling.LANCZOS)
for x in range(-7,W,444):out.paste(panel_scaled,(x,150))
# Warm dark wood crown, real source carving and grain rather than painted horizontal stripes.
crown=SRC.crop((71,0,506,93)).resize((W,55),Image.Resampling.LANCZOS)
crown=tint(crown,(116,67,35),.45)
out.paste(crown,(0,0))
d=ImageDraw.Draw(out)
d.line((0,53,930,53),fill="#3b2118",width=4)
d.line((0,57,930,57),fill="#9a6235",width=2)
d.line((0,148,930,148),fill="#351d16",width=6)
d.line((0,151,930,151),fill="#c2945d",width=2)
d.line((0,221,930,221),fill="#251711",width=5)
d.line((0,223,930,223),fill="#98714d",width=2)
# Extend the *rear exhibition wall* just below the approved three hanging frames.
# The original v12 floor began at y=222. Without moving this baseboard, enlarging
# frames would make them hang over the floor plane. Only the rear-wall bay is filled;
# side corridors, piers, and all opening geometry remain unchanged.
rear_dado=out.crop((184,171,746,218)).resize((562,27),Image.Resampling.LANCZOS)
out.paste(rear_dado,(184,222))
rd=ImageDraw.Draw(out)
rd.line((184,246,746,246),fill="#2c1c13",width=5)
rd.line((184,249,746,249),fill="#92643d",width=2)
# Real architectural pilasters, recolored to amber walnut/stone shades.
pil=SRC.crop((515,8,581,515)).resize((48,226),Image.Resampling.LANCZOS)
a=np.asarray(pil).astype(np.float32)
# Ivory shaft becomes warmer red-brown rather than a white marble column.
bright=np.maximum(0,((a.mean(2)-112)/120))[:,:,None]
col=np.array([116,70,42],dtype=np.float32); a=a*(1-.82*bright)+col*(.82*bright)
pil=Image.fromarray(np.uint8(np.clip(a,0,255)))
 # Sidewall forecourt pillars are constructed after occluding all rear-wall pixels.
# -------------------------------------------------------------------
# Side passage is cut into the NEAR wall, not laid across the visible rear wall.
# The full-height near wall occludes the rear molding and rear pillars behind it.
# Side-wall and arch share one coordinate system with the outer/inner vertical posts.
sidebase=Image.new("RGB",(183,582),(91,38,48))
side_top=SRC.crop((86,107,484,386)).resize((183,465),Image.Resampling.LANCZOS)
sidebase.paste(tint(side_top,(101,42,50),.98),(0,0))
side_wood=SRC.crop((72,402,508,512)).resize((183,117),Image.Resampling.LANCZOS)
sidebase.paste(tint(side_wood,(110,57,36),.45),(0,465))
# Source-authentic continuous timber cornice on this same near-wall surface.
side_crown=SRC.crop((73,0,259,93)).resize((183,57),Image.Resampling.LANCZOS)
sidebase.paste(tint(side_crown,(108,66,39),.45),(0,0))
sb=ImageDraw.Draw(sidebase)
sb.line((0,56,182,56),fill="#2e1b13",width=4)
sb.line((0,60,182,60),fill="#b2804e",width=2)
sb.rectangle((0,463,182,467),fill="#2c1c15")
sb.line((0,469,182,469),fill="#b08859",width=2)
sb.rectangle((0,574,182,581),fill="#2b1b15")
for mirrored in (False,True):
    q=[(0,0),(183,0),(183,545),(0,582)]
    if mirrored:
        q=[(W-x,y) for x,y in q]
        tex=Image.fromarray(np.asarray(sidebase)[:,::-1,:].copy())
    else:
        tex=sidebase
    wall,mask=homography_tex(tex,q)
    out.paste(wall,(0,0),mask)
# Preserve the two original-E burgundy panels, now ON the forward wall,
# not on the distant wall that the new passage occludes.
# E original's left/right burgundy ornamental wall panels: built as recessed real walnut
# moulding, not new furniture or decorations.
d=ImageDraw.Draw(out)
for x in (42,772):
    d.rectangle((x,61,x+116,195),fill='#33201b',outline='#8d663d',width=3)
    d.rectangle((x+5,66,x+111,190),fill='#7f4a36',outline='#c39a65',width=2)
    d.rectangle((x+10,71,x+106,185),fill='#542530',outline='#2a1715',width=3)
    d.line((x+17,78,x+17,177),fill='#713746',width=2)
    d.line((x+98,78,x+98,177),fill='#713746',width=2)
    # Only original E's two small hanging motifs in each recessed panel.
    for q in (x+28,x+87):
        d.ellipse((q-2,88,q+2,94),fill='#c3a16a')
        d.line((q,95,q-2,107,q+3,113),fill='#b99660',width=2)

# Four structural corner posts. The two columns at the inner edges finish at
# the same x as the door arch (x=153 and its mirrored x=777).
# No detached post/column remains behind the corridor opening.
post=SRC.crop((515,8,581,515)).resize((33,546),Image.Resampling.LANCZOS)
post=tint(post,(103,62,37),.96)
for x in (0,153,744,897):
    out.paste(post,(x,0))
d=ImageDraw.Draw(out)
for m in (False,True):
    def edge(x,y):return (W-x,y) if m else (x,y)
    d.line([edge(184,0),edge(184,544)],fill="#261912",width=5)
    d.line([edge(181,0),edge(181,542)],fill="#b48b57",width=2)

# crisp architectural front wall boundary & floor corner occlusion (before door cavities)
d=ImageDraw.Draw(out)
for mirror in (False,True):
    def pt(x,y):return (W-x,y) if mirror else (x,y)
    d.line([pt(184,225),pt(184,544)],fill="#1d1713",width=5)
    d.line([pt(181,225),pt(181,541)],fill="#a47a50",width=2)
    d.line([pt(0,581),pt(183,544)],fill="#20160f",width=7)
    d.line([pt(0,574),pt(181,540)],fill="#8f6850",width=3)
# -------------------------------------------------------------------
# Side corridor openings: no tilted pasted doors; construct actual wall cut, returns,
# dark receding corridor surfaces, front stone threshold and timber jamb material.
# Use bezier-like arch polygons at 2x alpha quality.
def corridor(left=True):
    global out
    def X(x):return x if left else W-x
    def P(x,y):return (X(x),y)
    # Front opening at x=38..144; distant corridor visible toward actual screen edge x=0.
    # The dark reveal directly replaces wall pixels, hence it is a genuine cutout.
    front=inner_arch(91,293,53,32,512,512)
    front=[P(x,y) for x,y in front]
    dr=ImageDraw.Draw(out)
    dr.polygon(front,fill="#100f10")
    # Corrugated dark timber ceiling visible in perspective, deeper at left.
    far=inner_arch(45,319,43,28,478,483)
    far=[P(x,y) for x,y in far]
    dr.polygon(far,fill="#101514")
    # Recess: top of arch underside / ceiling return shaded visibly but not flat black
    farch=[P(x,y) for x,y in points_arc(91,293,53,32)]
    backarch=[P(x,y) for x,y in points_arc(45,319,43,28)]
    dr.polygon(farch+list(reversed(backarch)),fill="#17120e")
    dr.line(farch,fill="#140d0b",width=6,joint="curve")
    dr.line(backarch,fill="#2e221b",width=3,joint="curve")
    # Deep side jambs, trapezoids perspectively receding outward into corridor
    dr.polygon([P(37,329),P(10,343),P(8,480),P(38,513)],fill="#4d3324")
    dr.polygon([P(145,328),P(88,344),P(88,482),P(145,513)],fill="#2c1b17")
    dr.polygon([P(139,328),P(97,351),P(98,485),P(139,504)],fill="#422a1d")
    # Subtle natural sidewall wood texture over the receding right jamb.
    # Recessed wine-red wall. A door-panel sprite here would incorrectly look like a hinged door.
    jamb=sidebase.crop((34,26,103,196)).resize((50,172),Image.Resampling.LANCZOS)
    poly=[P(139,329),P(98,353),P(99,477),P(139,505)]
    jtex,jmask=homography_tex(tint(jamb,(100,47,52),.92),poly)
    out.paste(jtex,(0,0),jmask)
    dr=ImageDraw.Draw(out)
    # A thin line of the opposite inner wall reads as interior and keeps hall direction clear.
    dr.line([P(13,352),P(13,474)],fill="#39261d",width=4)
    dr.line([P(101,350),P(100,483)],fill="#100d0b",width=5)
    # Corridor receding stone-floor wedge and threshold, touching main room seamlessly.
    pathpoly=[P(11,479),P(90,485),P(144,514),P(40,539),P(0,521)]
    dr.polygon(pathpoly,fill="#665c51")
    # Use the same real stone floor, foreshortened into the side corridor.
    ft=floor.crop((160,150,350,225)).resize((110,80),Image.Resampling.LANCZOS)
    farr=np.asarray(ft).astype(np.float32)*.65
    ft=Image.fromarray(np.uint8(np.clip(farr,0,255)))
    depthquad=[P(8,484),P(86,484),P(142,518),P(0,531)]
    fwarp,fmask=homography_tex(ft,depthquad)
    fmask=Image.fromarray(np.minimum(np.asarray(fmask),np.asarray(quad_mask(pathpoly))))
    out.paste(fwarp,(0,0),fmask)
    dr=ImageDraw.Draw(out)
    dr.line([P(10,485),P(0,520)],fill="#7d7262",width=2)
    dr.line([P(92,483),P(41,539)],fill="#94826e",width=2)
    dr.line([P(43,539),P(143,516)],fill="#c29b69",width=3)
    dr.line([P(45,545),P(143,519)],fill="#36261d",width=5)
    # First doorway arch is a cutout ring in walnut. Build thick dark extrusion rim.
    # Wider outside arch is not a skewed upright door sprite.
    outerarch=[P(x,y) for x,y in points_arc(91,284,63,43)]
    rim_outer=outerarch+[P(154,520),P(28,520)]
    rim_inner=farch+[P(144,513),P(38,513)]
    # Use open outlines rather than fill polygons to preserve cutout/cavity.
    dr.line(outerarch+[P(154,519)],fill="#25170f",width=13,joint="curve")
    dr.line(outerarch+[P(154,519)],fill="#775033",width=9,joint="curve")
    dr.line(outerarch+[P(154,519)],fill="#ae8355",width=3,joint="curve")
    dr.line(list(reversed(outerarch))+[P(28,519)],fill="#25170f",width=12,joint="curve")
    dr.line(list(reversed(outerarch))+[P(28,519)],fill="#805534",width=7,joint="curve")
    dr.line([P(33,516),P(33,330)],fill="#302019",width=9)
    dr.line([P(35,513),P(35,328)],fill="#a27749",width=3)
    dr.line([P(149,517),P(149,330)],fill="#38241a",width=11)
    dr.line([P(151,512),P(151,329)],fill="#b58b5b",width=3)
    dr.line(farch,fill="#c39b68",width=3,joint="curve")
    # Physically grounded cavity shadow at the doorway foot, not an extended dark wedge.
    dr.line([P(45,515),P(139,515)],fill="#281a13",width=5)
    dr.line([P(46,517),P(136,517)],fill="#c5a879",width=2)
for isleft in (True,False):corridor(isleft)
# -------------------------------------------------------------------
# Three actual approved game-style gold frames, with realistic carved bevel + wood backboard.
# Source is the approved Lv6 frame, not an invented vector approximation.
frame=LV6.crop((195,148,466,314))
def subdued_gold(img):
    ar=np.asarray(img.convert("RGB")).astype(np.float32)
    lum=ar.mean(2); hi=np.maximum(0,(lum-135)/110)[:,:,None]
    ar=ar*(1-hi*.30)+np.array([147,107,57],dtype=np.float32)*hi*.30
    return Image.fromarray(np.uint8(np.clip(ar,0,255)))
frame=subdued_gold(frame)
def nine_slice(src,w,h,edge=29):
    sw,sh=src.size; e=min(edge,sw//3,sh//3,w//3,h//3)
    dst=Image.new('RGB',(w,h))
    xsrc=[0,e,sw-e,sw]; ysrc=[0,e,sh-e,sh]
    xdst=[0,e,w-e,w];ydst=[0,e,h-e,h]
    for iy in range(3):
        for ix in range(3):
            crop=src.crop((xsrc[ix],ysrc[iy],xsrc[ix+1],ysrc[iy+1]))
            dst.paste(crop.resize((xdst[ix+1]-xdst[ix],ydst[iy+1]-ydst[iy]),Image.Resampling.LANCZOS),(xdst[ix],ydst[iy]))
    return dst
def frame_at(x,y,w,h,label):
    global out
    dr=ImageDraw.Draw(out)
    dr.rounded_rectangle((x-5,y-4,x+w+6,y+h+7),radius=3,fill="#23160f")
    dr.rectangle((x-2,y-2,x+w+2,y+h+2),fill="#7c4d2a")
    out.paste(nine_slice(frame,w,h), (x,y))
    # Cut out artwork window to a deep teal as in the entrance, without harsh synthetic border.
    dr=ImageDraw.Draw(out)
    bx=19 if w<160 else 21
    ix0,iy0=x+bx,y+bx;ix1,iy1=x+w-bx,y+h-bx
    # Intrinsic velvet surface rather than flat fill
    ww=max(2,ix1-ix0);hh=max(2,iy1-iy0)
    aa=np.zeros((hh,ww,3),np.uint8)
    for j in range(hh):
        for i in range(ww):
            rr=((i-ww*.48)/ww)**2+((j-hh*.43)/hh)**2
            v=max(0,1-rr*1.5)
            aa[j,i,:]=[13+int(13*v),45+int(21*v),42+int(16*v)]
    out.paste(Image.fromarray(aa),(ix0,iy0))
    dr=ImageDraw.Draw(out)
    dr.rectangle((ix0,iy0,ix1-1,iy1-1),outline="#ad8751",width=2)
    dr.line((ix0+2,iy0+3,ix1-4,iy0+3),fill="#25493f",width=2)
    # Keep the official E 1/2/3 preview markers (not actual uploaded photos).
    try:font=ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf",33 if label==2 else 28)
    except:font=ImageFont.load_default()
    bbox=dr.textbbox((0,0),str(label),font=font)
    dr.text((x+w/2-(bbox[2]-bbox[0])/2,y+h/2-(bbox[3]-bbox[1])/2-5),str(label),fill="#e9dcc0",font=font)
# Bookend pilasters are not clipped by frames.
# Keep all three *top edges and widths* fixed; grow only toward the floor.
frame_at(209,76,118,162,1)    # y=76..238; +18 px
frame_at(333,68,262,172,2)    # y=68..240; +19 px
frame_at(602,76,118,162,3)    # y=76..238; +18 px
# Central carved arch heading, E geometry retained but restrained.
d=ImageDraw.Draw(out)
arc=[(465+145*math.cos(t),82-40*math.sin(t)) for t in np.linspace(math.pi,0,100)]
for width,color in [(16,"#2b1c12"),(12,"#81502b"),(8,"#bb8a52"),(3,"#d0ad78")]:d.line(arc,fill=color,width=width,joint="curve")
# Small existing E crown medallion, no additional room decoration
d.ellipse((448,23,482,48),fill="#59331d",outline="#ab7c45",width=4)
d.ellipse((455,29,475,42),fill="#9b7044",outline="#d3ad73",width=2)
# restrained two wall-sconce motifs at original positions, from original E only
for x in (185,745):
    d.ellipse((x-13,95,x+13,116),fill="#372118")
    d.rectangle((x-4,111,x+4,136),fill="#a27642")
    d.ellipse((x-9,88,x+9,99),fill="#b49662")
# -------------------------------------------------------------------
# E runner footprint and perspective. Use textured red textile from actual approved Lv6.
runner_border=[(423,253),(507,253),(610,582),(320,582)]
d=ImageDraw.Draw(out)
d.polygon(runner_border,fill="#241813")
d.polygon([(426,256),(504,256),(601,582),(330,582)],fill="#be9562")
d.polygon([(431,261),(499,261),(593,582),(339,582)],fill="#491c28")
d.polygon([(435,266),(495,266),(582,582),(348,582)],fill="#792b3f")
# actual Lv6 red rug weave sample; perspective mapped to E opening, transparent mask
tex=LV6.crop((608,520,648,700)).resize((96,340),Image.Resampling.LANCZOS)
arr=np.asarray(tex).astype(np.float32)
arr=.48*arr+.52*np.array([104,31,52],dtype=np.float32)
arr[:,:,0]=np.clip(arr[:,:,0],52,119)
arr[:,:,1]*=.54;arr[:,:,2]=np.clip(arr[:,:,2]*.84+12,18,75)
woven=Image.fromarray(np.uint8(np.clip(arr,0,255)))
quad=[(437,268),(493,268),(579,582),(352,582)]
warp,mask=homography_tex(woven,quad)
out.paste(warp,(0,0),mask)
d=ImageDraw.Draw(out)
d.line([(431,261),(338,582)],fill="#c7a06b",width=3)
d.line([(499,261),(593,582)],fill="#c7a06b",width=3)
d.line([(442,273),(362,582)],fill="#6a2636",width=2)
d.line([(488,273),(569,582)],fill="#6a2636",width=2)
# Preserve quiet repeating gold stitching from E (not lavish additional ornament).
for y in (320,382,452,532):
    t=(y-253)/(582-253)
    x1=(437+(352-437)*t);x2=(493+(579-493)*t)
    d.line((x1+10,y,x2-10,y),fill="#b59667",width=1)
    cx=(x1+x2)/2
    d.polygon([(cx,y-6),(cx+4,y),(cx,y+6),(cx-4,y)],outline="#b59667")
# save review output, never mutate E source or room.json
target=ROOT/"architecture-review/entrance-gallery5-comparison/gallery5-v13.png"
out.save(target,optimize=True)
target2=ROOT/"architecture-review/gallery5/gallery5_v13_extended_frames_REVIEW.png"
out.save(target2,optimize=True)
candidate=ROOT/'rooms/gallery5/gallery5_palace_E_material_v13_REVIEW.png'
out.save(candidate,optimize=True)
print('saved',target,target2,candidate,out.size,'E unchanged',E.size)