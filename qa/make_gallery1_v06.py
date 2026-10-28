from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
r=Path('C:/Users/User/source/repos/a18-gallery-layout-editor')
q=r/'qa/architecture-bases-20261029'
v5=Image.open(q/'gallery1_architecture_closed_door_sidewalls_v05_REVIEW.png').convert('RGB')
base=Image.open(q/'gallery1_architecture_no_frames_v04_REVIEW.png').convert('RGB')
out=v5.copy()
out.paste(base.crop((0,220,36,582)),(0,220))
# Use an adjacent strip of the *existing floor*, not generated architecture.
out.paste(base.crop((836,220,880,582)),(886,220))
d=ImageDraw.Draw(out)
d.rectangle((0,220,8,581),fill='#55321c')
d.line((8,220,8,581),fill='#c18b53',width=2)
d.rectangle((922,220,929,581),fill='#55321c')
d.line((921,220,921,581),fill='#c18b53',width=2)
out.save(q/'gallery1_architecture_v06_no_green_sidewalls_REVIEW.png')
dst=r/'gallery1-architecture-v05-review'
out.save(dst/'gallery1-v06.png')
comp=Image.new('RGB',(1860,620),'#f4f4f0')
comp.paste(v5,(0,38));comp.paste(out,(930,38))
dd=ImageDraw.Draw(comp)
dd.text((15,12),'v05 / GREEN SIDE SURFACES',fill='#222')
dd.text((945,12),'v06 / NO GREEN SIDE SURFACES',fill='#222')
comp.save(dst/'comparison-v05-v06.png')
a=np.asarray(v5);b=np.asarray(out)
allowed=np.zeros((582,930),bool)
allowed[220:,:36]=True;allowed[220:,886:]=True
assert np.array_equal(a[~allowed],b[~allowed])
print('PASS',np.count_nonzero(np.any(a!=b,axis=2)))
html=(dst/'index.html').read_text(encoding='utf-8')
html=html.replace('展示室1｜建築背景 v05','展示室1｜建築背景 v06').replace('修復後 v05','修復後 v06（左右の緑を除去）').replace('src="gallery1-v05.png"','src="gallery1-v06.png"').replace('v04との比較（左：変更前、右：v05）','v05との比較（左：v05、右：v06）').replace('src="comparison.png"','src="comparison-v05-v06.png"')
(dst/'index.html').write_text(html,encoding='utf-8')
