"""Gallery1 v13 review: lower ONLY the upper edge of the right-side passage by 24 px.
Base is the user-selected v12 B, no other change.
"""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont

ROOT=Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
QA=ROOT/"qa/architecture-bases-20261029"
src=QA/"gallery1_v12_restored_corner_columns_WITH_bottom_border_REVIEW.png"
base=Image.open(src).convert("RGB")
assert base.size==(930,582)
# The passage currently begins at y=220; the top black wall ends at y=219.
# Extend only that black wall to y=243; keep the passage's lower end at y=348.
old_top=220
new_top=244
x1,x2=886,930
bottom=349
out=base.copy()
drawer=ImageDraw.Draw(out)
black=(5,6,7)
drawer.rectangle((x1,old_top,x2-1,new_top-1),fill=black)
a=np.asarray(base)
b=np.asarray(out)
allowed=np.zeros((582,930),bool)
allowed[old_top:new_top,x1:x2]=True
assert np.array_equal(a[~allowed],b[~allowed]),"Unexpected pixels changed outside right passage top"
assert np.all(b[0:244,900:929,:]==black),"Upper right wall not continuous"
assert np.array_equal(a[new_top:bottom,x1:x2],b[new_top:bottom,x1:x2]),"Passage floor not preserved"
assert np.array_equal(a[566:582],b[566:582]),"Approved bottom border modified"
assert np.array_equal(a[35:220,44:75],b[35:220,44:75]),"West column modified"
assert np.array_equal(a[35:220,855:886],b[35:220,855:886]),"East column modified"
name="gallery1_v13_B_right_passage_top_lowered_24px_REVIEW.png"
out.save(QA/name)
# Compare full frames without overlay or arrows that might obscure the detail.
side=Image.new("RGB",(1860,624),"#1b1c1e")
side.paste(base,(0,42))
side.paste(out,(930,42))
dr=ImageDraw.Draw(side)
dr.rectangle((0,0,1859,41),fill="#292b2d")
dr.text((16,14),"v12 B / opening starts at y220",fill="white")
dr.text((946,14),"v13 B / opening starts at y244 (+24px)",fill="white")
side.save(QA/"gallery1_v12B_vs_v13_opening_comparison_REVIEW.png")
# Enlarged right-side detail image for mobile review; original region only.
details=Image.new("RGB",(640,600),"#1b1c1e")
for i,(label,img) in enumerate([("v12 B",base),("v13",out)]):
    pane=img.crop((780,168,930,428)).resize((300,520),Image.Resampling.NEAREST)
    details.paste(pane,(i*320+10,56))
    ImageDraw.Draw(details).text((i*320+15,23),label,fill="white")
details.save(QA/"gallery1_v13_right_entrance_detail_REVIEW.png")
print("PASS v13:",name)
print("Changed only the opening top: (886..929,220..243), old floor unchanged below y244")
print("Changed pixels:",int(np.any(a!=b,axis=2).sum()),"expected:",(x2-x1)*(new_top-old_top))
