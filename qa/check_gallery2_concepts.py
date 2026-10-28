"""Static reachability checks for gallery2 concepts; NOT gameplay collision QA."""
import ast
from collections import deque
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SRC=(ROOT/'qa'/'make_gallery2_concepts.py').read_text(encoding='utf-8')
start=SRC.index('layouts={')
end=SRC.index('\nfor key,spec in layouts.items():')
layouts=ast.literal_eval(SRC[start+len('layouts='):end])
P=ROOT/'rooms'/'gallery2'/'concepts'
assert set(layouts)=={'A','B','C'}
assert Image.open(P/'architecture_draft.png').size==(930,582)
for label,body in layouts.items():
    pic=Image.open(P/f'gallery2_concept_{label}.png')
    assert pic.size==(930,582)
    rects=[(x,y,x+w,y+h) for n,x,y,w,h,kind in body['obj']]
    nums=[n for n,x,y,w,h,kind in body['obj']]
    assert sorted(nums)==([3,5] if label=='B' else [3,4,5]),(label,nums)
    if label=='B':
        assert body['obj'][0][-1]=='double'
    assert all(x>=100 and xx<=878 and y>=250 and yy<=548 for x,y,xx,yy in rects),(label,'bounds',rects)
    # No frame, entry, or north corridor intersects a movable screen.
    anchors=[(65,390),(710,246),(183,246),(440,246),(621,275)]
    anchors += [((x+xx)//2,yy+18) for x,y,xx,yy in rects]
    if label=='B':anchors += [(350,540),(515,540)]
    margin=12
    def free(x,y):
        if not (24<=x<=894 and 230<=y<=565):return False
        if any(x>=a-margin and x<=c+margin and y>=b-margin and y<=d+margin for a,b,c,d in rects):return False
        if x>876 and y>=259:return False
        return True
    step=4
    s=(64//step*step,392//step*step)
    assert free(*s)
    visited={s};q=deque([s])
    while q:
        x,y=q.popleft()
        for nx,ny in ((x+step,y),(x-step,y),(x,y+step),(x,y-step)):
            p=(nx,ny)
            if p not in visited and free(*p):
                visited.add(p);q.append(p)
    def reach(x,y):
        return any((nx,ny) in visited for nx in range((x-28)//step*step,(x+28)//step*step+1,step) for ny in range((y-28)//step*step,(y+28)//step*step+1,step) if (nx-x)**2+(ny-y)**2<=28**2)
    misses=[a for a in anchors if not reach(*a)]
    assert not misses,(label,'unreachable',misses)
    print(label,'PASS',len(visited),'cells,',len(anchors),'anchors, 5 artwork positions')
print('Three distinct concepts: STATIC PASS; original game collision/depth/camera still NOT tested.')
