from pathlib import Path
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
import subprocess
root=Path(__file__).resolve().parents[1]
a=root/'rooms/gallery5/gallery5_palace_E.png'
b=root/'rooms/gallery5/gallery5_palace_E_material_v12_REVIEW.png'
c=root/'architecture-review/entrance-gallery5-comparison/gallery5-v12.png'
assert all(Image.open(p).size == (930,582) for p in (a,b,c))
assert b.read_bytes() == c.read_bytes()
assert 'v12' in (root/'architecture-review/entrance-gallery5-comparison/index.html').read_text(encoding='utf-8')
assert ImageChops.difference(Image.open(a).convert('RGB'),Image.open(b).convert('RGB')).getbbox()
head=subprocess.check_output(['git','rev-parse','HEAD:rooms/gallery5/gallery5_palace_E.png'],cwd=root,text=True).strip()
actual=subprocess.check_output(['git','hash-object',str(a)],cwd=root,text=True).strip()
assert head==actual,(head,actual)
pix=Image.open(b).convert('RGB')
for x in (100,830):
    r,g,blue=pix.getpixel((x,253))
    assert r > g*1.2 and r > blue*0.78,(x,r,g,blue)
print('v12 images, original E protected, near-wall occlusion PASS')
out=root/'qa/gallery5-v12-review'
out.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    for width,height in ((1180,900),(390,844)):
        page=browser.new_page(viewport={'width':width,'height':height})
        errors=[]
        page.on('pageerror',lambda e: errors.append(str(e)))
        page.goto((root/'architecture-review/entrance-gallery5-comparison/index.html').as_uri(),wait_until='load')
        images=page.locator('article img')
        assert 'v12' in page.title() and images.count()==5
        assert images.evaluate_all('(els)=>els.every(el=>el.complete && el.naturalWidth>0)')
        assert page.locator('body').evaluate('(el)=>el.scrollWidth <= innerWidth + 2')
        assert not errors,errors
        page.screenshot(path=str(out/f'v12_browser_{width}_QA.png'),full_page=True)
        print('browser',width,'PASS')
        page.close()
    browser.close()
