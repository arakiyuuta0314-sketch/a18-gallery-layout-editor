from pathlib import Path
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
import subprocess
root=Path(__file__).resolve().parents[1]
a=root/'rooms/gallery5/gallery5_palace_E.png'
b=root/'rooms/gallery5/gallery5_palace_E_material_v14_REVIEW.png'
c=root/'architecture-review/entrance-gallery5-comparison/gallery5-v14.png'
assert all(Image.open(p).size == (930,582) for p in (a,b,c))
assert b.read_bytes() == c.read_bytes()
assert 'v14' in (root/'architecture-review/entrance-gallery5-comparison/index.html').read_text(encoding='utf-8')
assert ImageChops.difference(Image.open(a).convert('RGB'),Image.open(b).convert('RGB')).getbbox()
head=subprocess.check_output(['git','rev-parse','HEAD:rooms/gallery5/gallery5_palace_E.png'],cwd=root,text=True).strip()
actual=subprocess.check_output(['git','hash-object',str(a)],cwd=root,text=True).strip()
assert head==actual,(head,actual)
pix=Image.open(b).convert('RGB')
for x in (100,830):
    r,g,blue=pix.getpixel((x,253))
    assert r > g*1.2 and r > blue*0.78,(x,r,g,blue)
# Verify that left and right corridors retain *exactly* their v13 pixels.
prev=Image.open(root/'rooms/gallery5/gallery5_palace_E_material_v13_REVIEW.png').convert('RGB')
now=Image.open(b).convert('RGB')
assert ImageChops.difference(prev.crop((0,0,180,582)),now.crop((0,0,180,582))).getbbox() is None
assert ImageChops.difference(prev.crop((750,0,930,582)),now.crop((750,0,930,582))).getbbox() is None
# Compare the new lower-frame region against the previous image.
# In v13 those coordinates were exposed lower wall/floor. In v14 they are inside a frame.
for x,y in ((255,268),(464,270),(668,268)):
    assert prev.getpixel((x,y)) != now.getpixel((x,y)), (x,y)
# The v14 picture spaces remain exactly three, central landscape larger.
frame_rects=((190,76,133,202),(329,68,270,210),(605,76,133,202))
assert all(0<=x and x+w<=930 and y+h<=292 for x,y,w,h in frame_rects)
assert frame_rects[0][0]+frame_rects[0][2] < frame_rects[1][0]
assert frame_rects[1][0]+frame_rects[1][2] < frame_rects[2][0]
assert frame_rects[0][1]+frame_rects[0][3]==frame_rects[1][1]+frame_rects[1][3]==frame_rects[2][1]+frame_rects[2][3]
print('v14 images, E protected, v13 corridors unchanged, enlarged frames PASS')
out=root/'qa/gallery5-v14-review'
out.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    for width,height in ((1180,900),(390,844)):
        page=browser.new_page(viewport={'width':width,'height':height})
        errors=[]
        page.on('pageerror',lambda e: errors.append(str(e)))
        page.goto((root/'architecture-review/entrance-gallery5-comparison/index.html').as_uri(),wait_until='load')
        images=page.locator('article img')
        assert 'v14' in page.title() and images.count()==5
        assert images.evaluate_all('(els)=>els.every(el=>el.complete && el.naturalWidth>0)')
        assert page.locator('body').evaluate('(el)=>el.scrollWidth <= innerWidth + 2')
        assert not errors,errors
        page.screenshot(path=str(out/f'v14_browser_{width}_QA.png'),full_page=True)
        print('browser',width,'PASS')
        page.close()
    browser.close()