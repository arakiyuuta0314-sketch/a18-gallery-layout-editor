"""A18 v11 review-page QA. No gameplay, game source or merge."""
from pathlib import Path
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
import subprocess
ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/"architecture-review/entrance-gallery5-comparison"
ref=ROOT/"rooms/gallery5/gallery5_palace_E.png"
candidate=ROOT/"rooms/gallery5/gallery5_palace_E_material_v11_REVIEW.png"
page=folder/"index.html"
assert ref.is_file() and candidate.is_file() and page.is_file()
assert Image.open(ref).size==(930,582)
assert Image.open(candidate).size==(930,582)
assert Image.open(folder/"gallery5-v11.png").size==(930,582)
assert ImageChops.difference(Image.open(ref).convert("RGB"),Image.open(candidate).convert("RGB")).getbbox()
assert ImageChops.difference(Image.open(folder/"gallery5-v11.png").convert("RGB"),Image.open(candidate).convert("RGB")).getbbox() is None
# Exact canonical original hash must match HEAD, not just visual similarity
tracked=subprocess.check_output(["git","rev-parse","HEAD:rooms/gallery5/gallery5_palace_E.png"],cwd=ROOT,text=True).strip()
disk=subprocess.check_output(["git","hash-object",str(ref)],cwd=ROOT,text=True).strip()
assert tracked==disk,(tracked,disk)
print("E original protected, image dimensions and new asset copies: PASS")
OUT=ROOT/"qa/gallery5-v11-review"
OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(channel="chrome",headless=True)
    for width,height in ((1180,900),(390,844)):
        t=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1)
        errors=[]
        t.on("pageerror",lambda e:errors.append(str(e)))
        t.goto(page.as_uri(),wait_until="load")
        imgs=t.locator("article img")
        assert imgs.count()==5,imgs.count()
        assert imgs.evaluate_all("(els) => els.every(el => el.complete && el.naturalWidth > 0 && el.naturalHeight > 0)")
        assert t.locator("body").evaluate("(el) => el.scrollWidth <= innerWidth + 2")
        assert t.locator("article").first.bounding_box()["width"]<=width
        assert not errors,errors
        t.screenshot(path=str(OUT/f"v11_browser_{width}_QA.png"),full_page=True)
        print(f"review page {width}x{height}: PASS, 5 actual images, no horizontal overflow")
        t.close()
    browser.close()
print("V11 QA PASS")
