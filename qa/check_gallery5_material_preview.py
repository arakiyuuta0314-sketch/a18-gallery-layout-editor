"""QA for Gallery 5 web-only material review. Does not touch game or fixture schemas."""
from pathlib import Path
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
import re
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"qa/gallery5-material-20261029"
page_file=ROOT/"architecture-review/gallery5/index.html"
assert page_file.is_file()
pngs=sorted(OUT.glob("gallery5_*.png"))
assert len(pngs)>=6,pngs
for p in pngs:
    sz=Image.open(p).size
    assert sz==((1864,618) if "vs_" in p.name else (930,582)),(p,sz)
old=Image.open(ROOT/"rooms/gallery5/gallery5_palace_E.png").convert("RGB")
for f in ("gallery5_v01_material_3frame_mock_REVIEW.png","gallery5_v02_material_3frame_mock_REVIEW.png"):
    new=Image.open(OUT/f).convert("RGB")
    assert ImageChops.difference(old,new).getbbox() is not None
print("PNG size and material differences: PASS")
with sync_playwright() as p:
    browser=p.chromium.launch(channel="chrome",headless=True)
    for width,height in ((1180,880),(390,844)):
        page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1)
        err=[]
        page.on("pageerror",lambda e:err.append(str(e)))
        page.goto(page_file.as_uri(),wait_until="load")
        images=page.locator("#view img")
        assert images.count()==2
        print('Image states',images.evaluate_all("(els)=>els.map(el=>({src:el.src,complete:el.complete,w:el.naturalWidth,h:el.naturalHeight}))"))
        assert images.evaluate_all("(els)=>els.every(el=>el.complete && el.naturalWidth===930 && el.naturalHeight===582)")
        page.locator('[data-layer="frames"]').click()
        page.wait_for_function("() => [...document.querySelectorAll('#view img')].every(el => el.complete && el.naturalWidth === 930)")
        assert images.evaluate_all("(els)=>els.every(el=>el.complete && el.naturalWidth===930)")
        page.locator('[data-pair="new12"]').click()
        page.wait_for_function("() => [...document.querySelectorAll('#view img')].every(el => el.complete && el.naturalWidth === 930)")
        assert images.evaluate_all("(els)=>els.every(el=>el.complete && el.naturalWidth===930)")
        page.locator("#position").fill("70")
        assert page.locator("#view").evaluate("(el)=>el.style.getPropertyValue('--pos')")=="70%"
        # Restore the intentionally unapproved architecture-only comparison for screenshots.
        page.locator('[data-layer="bare"]').click()
        page.locator('[data-pair="old1"]').click()
        page.locator("#position").fill("50")
        assert not err,err
        assert page.locator("body").evaluate("(el)=>el.scrollWidth <= innerWidth + 2")
        page.screenshot(path=str(OUT/f"browser_{width}_comparison_QA.png"),full_page=True)
        print(f"Browser {width}px: PASS")
        page.close()
    browser.close()
print("QA PASS")
