from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
r=Path('C:/Users/User/source/repos/a18-gallery-layout-editor')
q=r/'qa/architecture-bases-20261029'
src=Image.open(q/'gallery1_architecture_no_frames_v04_REVIEW.png').convert('RGB')
side=Image.open(r/'rooms/gallery1/side-walls.png').convert('RGBA')
a=np.array(src)
# Only replace the deep green opening within existing wood arch with closed doors.
# The arch's structural pixels are preserved exactly.
out=src.copy(); d=ImageDraw.Draw(out)
# closed double door recessed inside the arch; original arch frame remains untouched
d.rectangle((318,85,389,207),fill='#75411f')
for x0,x1 in [(320,352),(356,387)]:
 d.rectangle((x0,91,x1,198),fill='#875029',outline='#452512',width=2)
 d.rectangle((x0+4,96,x1-4,139),outline='#b77d47',width=2)
 d.rectangle((x0+4,145,x1-4,192),outline='#b77d47',width=2)
d.line((354,86,354,207),fill='#352014',width=3)
d.ellipse((347,149,351,158),fill='#d9b16c')
d.ellipse((358,149,362,158),fill='#d9b16c')
# Existing left/right walls are layered from the approved transparent asset.
out=Image.alpha_composite(out.convert('RGBA'),side).convert('RGB')
dst=q/'gallery1_architecture_closed_door_sidewalls_v05_REVIEW.png'
out.save(dst)
before=Image.alpha_composite(src.convert('RGBA'),side).convert('RGB')
compare=Image.new('RGB',(1860,620),'#efefec')
compare.paste(before,(0,38));compare.paste(out,(930,38))
dd=ImageDraw.Draw(compare)
dd.text((15,12),'V04 + APPROVED SIDE WALLS / OPEN DOOR',fill='#222')
dd.text((945,12),'V05 / CLOSED DOOR + SAME SIDE WALLS',fill='#222')
compare.save(q/'gallery1_v04_vs_v05_closed_door_sidewalls.png')
# All pixels outside the arch opening are identical to the prior v04 + side walls.
aa=np.asarray(before);bb=np.asarray(out)
mask=np.zeros((582,930),bool);mask[85:208,318:390]=True
assert np.array_equal(aa[~mask],bb[~mask])
print('PASS',dst, 'modified',np.count_nonzero(np.any(aa!=bb,axis=2)))
