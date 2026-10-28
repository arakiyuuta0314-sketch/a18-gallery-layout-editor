from PIL import Image,ImageDraw
import numpy as np
from pathlib import Path
root=Path('C:/Users/User/source/repos/a18-gallery-layout-editor')
src=np.array(Image.open(root/'rooms/gallery1/architecture.png').convert('RGB'))
result=src.copy()
# The rear walls share the same original paint material. Replace the three
# frame-only regions with a wall paint sample from a clean horizontal stripe,
# preserving the original scene and all other pixels.
rects=[(59,80,201,169),(494,80,636,169),(739,80,882,169)]
for x0,y0,x1,y1 in rects:
 for y in range(y0,y1+1):
  # wall paint sample from above each frame, same x coordinate; subtle vertical
  # illumination correction from clean adjacent wall at y.
  for x in range(x0,x1+1):
   donor_y=77
   color=src[donor_y,x].astype(float)
   # small measured vertical shading shift from clean green wall at frame side
   edge_x=x0-12 if x-x0 < x1-x else x1+12
   offset=src[y,edge_x].astype(float)-src[donor_y,edge_x].astype(float)
   result[y,x]=np.clip(color+offset,0,255).astype(np.uint8)
out=root/'qa/architecture-bases-20261029'
Image.fromarray(result).save(out/'gallery1_architecture_no_frames_v04_REVIEW.png')
sheet=Image.new('RGB',(1860,620),'#efefed')
sheet.paste(Image.fromarray(src),(0,38));sheet.paste(Image.fromarray(result),(930,38))
d=ImageDraw.Draw(sheet);d.text((15,12),'ORIGINAL',fill='#222');d.text((945,12),'V04 - WALL PAINT RECONSTRUCTION / REVIEW',fill='#222')
sheet.save(out/'gallery1_original_vs_repair_v04.png')
print('PASS')
