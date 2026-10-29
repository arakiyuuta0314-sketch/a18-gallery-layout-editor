from PIL import Image,ImageDraw,ImageFilter
from pathlib import Path
import numpy as np
r=Path(r'C:\Users\User\source\repos\a18-gallery5-material-review')
im=Image.open(r/'rooms/gallery5/gallery5_palace_E.png').convert('RGB')
d=ImageDraw.Draw(im)
# Correct 2D side-door construction: perspective inset inside angled side wall.
# Never paste an upright door. Preserve E burgundy wall, ceiling, center frames, carpet and marble.
for mirror in (False,True):
 def p(x,y):return (929-x,y) if mirror else (x,y)
 # Cover only old frontal arch; use E's own original ochre-brown wall palette.
 d.polygon([p(28,268),p(162,268),p(162,508),p(28,508)],fill='#78634c')
 # Draw a wall receding obliquely to the left/right: far jamb narrower and shifted.
 # Outer reveal as trapezoid, with floor threshold connecting to room floor.
 d.polygon([p(38,318),p(126,290),p(151,483),p(49,516)],fill='#2b1b18')
 d.polygon([p(44,321),p(122,300),p(140,474),p(55,501)],fill='#4b382e')
 # Corridor wall on the deep side, with darkening toward interior.
 d.polygon([p(55,335),p(101,324),p(109,468),p(61,485)],fill='#392c28')
 # Passage continues into deep shadow, distinct from a closed black door.
 d.polygon([p(101,324),p(128,307),p(138,472),p(109,468)],fill='#122722')
 d.polygon([p(108,342),p(127,329),p(135,459),p(115,463)],fill='#09211e')
 # Door jamb: top lintel and edges follow same oblique plane.
 d.line([p(39,317),p(126,291),p(150,484)],fill='#c5a272',width=9,joint='curve')
 d.line([p(45,325),p(123,303),p(141,474)],fill='#8e704d',width=4)
 d.line([p(38,318),p(49,516)],fill='#c6a578',width=9)
 d.line([p(49,516),p(151,483)],fill='#b49268',width=7)
 d.line([p(58,505),p(142,478)],fill='#3a2920',width=3)
 # Floor leads through opening with converging joints, not a black hole.
 d.polygon([p(56,507),p(142,479),p(115,506),p(13,541)],fill='#706357')
 d.line([p(18,537),p(116,505)],fill='#9b8060',width=2)
 d.line([p(57,505),p(109,489)],fill='#c1a17b',width=2)
 # Add cast shadow on floor from thick front-facing wall.
 d.polygon([p(0,540),p(182,540),p(181,551),p(0,574)],fill='#594a3d')
# Keep all 3 slots unaltered. No extraneous decorative objects.
p=r/'architecture-review/gallery5/gallery5_v10_E_diagonal_side_passages_REVIEW.png';im.save(p)
print('SAVED',p,im.size)
