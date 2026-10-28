from PIL import Image, ImageDraw
from pathlib import Path
r=Path('C:/Users/User/source/repos/a18-gallery-layout-editor')
p=r/'qa/architecture-bases-20261029'
im=Image.open(p/'gallery1_architecture_v06_no_green_sidewalls_REVIEW.png').convert('RGB')
d=ImageDraw.Draw(im)
d.rectangle((0,220,8,581),fill='black')
d.rectangle((921,220,929,581),fill='black')
im.save(p/'gallery1_architecture_v07_black_edges_REVIEW.png')
print(im.size)
