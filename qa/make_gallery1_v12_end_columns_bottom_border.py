"""A18 gallery1 v12 QA: original end pillars, two lower-border variants.
Pixel-derived only from existing v04/v11 assets. No generative redraw.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

ROOT=Path("C:/Users/User/source/repos/a18-gallery-layout-editor")
QA=ROOT/"qa/architecture-bases-20261029"
original=Image.open(QA/"gallery1_architecture_no_frames_v04_REVIEW.png").convert("RGB")
prior=Image.open(QA/"gallery1_v11_rectangular_black_frame_upper_right_entrance_REVIEW.png").convert("RGB")
assert prior.size==original.size==(930,582)

# Original corner pillars were hidden by the black perimeter in v11:
# bring exactly those real, existing pillar pixels to the INNER ends of the back wall.
# Existing wall roof / wainscoting remain in place. The restored columns terminate
# at the same y=220 footing as all the other pillars on this wall.
restored=prior.copy()
LEFT_SRC=(0,39,31,220)
RIGHT_SRC=(899,39,930,220)
LEFT_DST=(44,39)
RIGHT_DST=(855,39)
restored.paste(original.crop(LEFT_SRC),LEFT_DST)
restored.paste(original.crop(RIGHT_SRC),RIGHT_DST)

# Two review alternatives keep the exact same upper-right open passage.
without=restored.copy()
with_bottom=restored.copy()
border_color=(5,6,7)
bottom_y=566
draw=ImageDraw.Draw(with_bottom)
draw.rectangle((0,bottom_y,929,581),fill=border_color)

before=np.asarray(prior)
afterA=np.asarray(without)
afterB=np.asarray(with_bottom)
allowed=np.zeros((582,930),dtype=bool)
allowed[39:220,44:75]=True
allowed[39:220,855:886]=True
assert np.array_equal(before[~allowed],afterA[~allowed]),"Unexpected modification beyond pillar restoration"
assert np.array_equal(afterA[:bottom_y],afterB[:bottom_y]),"Only bottom strip may differ"
assert np.all(afterB[bottom_y:]==np.asarray(border_color)),"Bottom edge must be rectangular/black"
assert np.array_equal(afterA[220:349,886:930],before[220:349,886:930]),"East entrance position/texture changed"
assert np.array_equal(afterA[250:540,100:830],before[250:540,100:830]),"Room floor changed"
assert np.array_equal(afterB[250:540,100:830],before[250:540,100:830]),"Room floor changed in bordered variant"
assert np.array_equal(afterA[39:220,44:75],np.asarray(original)[39:220,0:31]),"Left pillar differs from real original"
assert np.array_equal(afterA[39:220,855:886],np.asarray(original)[39:220,899:930]),"Right pillar differs from real original"
a_name="gallery1_v12_restored_corner_columns_NO_bottom_border_REVIEW.png"
b_name="gallery1_v12_restored_corner_columns_WITH_bottom_border_REVIEW.png"
without.save(QA/a_name)
with_bottom.save(QA/b_name)
# Also generate easy side-by-side comparison (not a substitute for individual PNGs).
canvas=Image.new("RGB",(1860,618),"#1c1e20")
canvas.paste(without,(0,36))
canvas.paste(with_bottom,(930,36))
draw=ImageDraw.Draw(canvas)
draw.rectangle((0,0,1859,35),fill="#27292d")
draw.text((16,12),"A: ORIGINAL CORNER PILLARS / NO BOTTOM BORDER",fill="white")
draw.text((946,12),"B: ORIGINAL CORNER PILLARS / BOTTOM BLACK BORDER",fill="white")
canvas.save(QA/"gallery1_v12_bottom_border_comparison_REVIEW.png")
print("PASS: pillars restored using existing source pixels")
print("PASS: bottom strip 16 px, east upper entrance unchanged")
print("PASS: original floor and rear wall unchanged beyond column footprints")
print(a_name,b_name)
