from pathlib import Path
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
import subprocess
root=Path(__file__).resolve().parents[1]
a=root/'rooms/gallery5/gallery5_palace_E.png'
b=root/'rooms/gallery5/gallery5_palace_E_material_v13_REVIEW.png'
c=root/'architecture-review/entrance-gallery5-comparison/gallery5-v13.png'
assert all(Image.open(p).size == (930,582) for p in (a,b,c))
assert b.read_bytes() == c.read_bytes()
assert 'v13' in (root/'architecture-review/entrance-gallery5-comparison/index.html').read_text(encoding='utf-8')
assert ImageChops.difference(Image.open(a).convert('RGB'),Image.open(b).convert('RGB')).getbbox()
head=subprocess.check_output(['git','rev-parse','HEAD:rooms/gallery5/gallery5_palace_E.png'],cwd=root,text=True).strip()
actual=subprocess.check_output(['git','hash-object',str(a)],cwd=root,text=True).strip()
assert head==actual,(head,actual)
pix=Image.open(b).convert('RGB')
for x in (100,830):
    r,g,blue=pix.getpixel((x,253))
    assert r > g*1.2 and r > blue*0.78,(x,r,g,blue)
# Verify that left and right corridors retain *exactly* their v12 pixels.
prev=Image.open(root/'rooms/gallery5/gallery5_palace_E_material_v12_REVIEW.png').convert('RGB')
now=Image.open(b).convert('RGB')
assert ImageChops.difference(prev.crop((0,0,180,582)),now.crop((0,0,180,582))).getbbox() is None
assert ImageChops.difference(prev.crop((750,0,930,582)),now.crop((750,0,930,582))).getbbox() is None
# Verify the new frames have actually extended down without shifting their top edges.
for x,y in ((265,231),(465,233),(660,231)):
    assert prev.getpixel((x,y)) != now.getpixel((x,y)),(x,y)
for x,y in ((268,77),(465,88),(665,77)):
    assert prev.getpixel((x,y)) == now.getpixel((x,y)),(x,y)
print('v13 image copies, preserved E, unchanged corridors, lower-only frame extension PASS')
out=root/'qa/gallery5-v13-review'
out.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    for width,height in ((1180,900),(390,844)):
        page=browser.new_page(viewport={'width':width,'height':height})
        errors=[]
        page.on('pageerror',lambda e: errors.append(str(e)))
        page.goto((root/'architecture-review/entrance-gallery5-comparison/index.html').as_uri(),wait_until='load')
        images=page.locator('article img')
        assert 'v13' in page.title() and images.count()==5
        assert images.evaluate_all('(els)=>els.every(el=>el.complete && el.naturalWidth>0)')
        assert page.locator('body').evaluate('(el)=>el.scrollWidth <= innerWidth + 2')
        assert not errors,errors
        page.screenshot(path=str(out/f'v13_browser_{width}_QA.png'),full_page=True)
        print('browser',width,'PASS')
        page.close()
    browser.close()