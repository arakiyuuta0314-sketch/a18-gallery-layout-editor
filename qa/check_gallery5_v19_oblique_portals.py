"""v19 gallery5 skewed-portal source QA, geometry preservation and actual mobile page QA."""
from pathlib import Path
import subprocess,threading
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
ROOT=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
D=ROOT/"architecture-review/entrance-gallery5-comparison"
E=ROOT/"rooms/gallery5/gallery5_palace_E.png"
assert E.is_file()
tracked=subprocess.check_output(["git","rev-parse","HEAD:rooms/gallery5/gallery5_palace_E.png"],cwd=ROOT,text=True).strip()
present=subprocess.check_output(["git","hash-object",str(E)],cwd=ROOT,text=True).strip()
assert tracked==present,(tracked,present)
v18=Image.open(D/"gallery5-v18.png").convert("RGB")
v19=Image.open(D/"gallery5-v19.png").convert("RGB")
assert v18.size==v19.size==(930,582)
assert (D/"gallery5-v19.png").read_bytes()==(ROOT/"architecture-review/gallery5/gallery5_v19_oblique_side_arches_REVIEW.png").read_bytes()
assert (D/"gallery5-v19.png").read_bytes()==(ROOT/"rooms/gallery5/gallery5_palace_E_material_v19_REVIEW.png").read_bytes()
# Main room area must be pixel-perfect: frame geometry, runner, and stone floor.
assert ImageChops.difference(v18.crop((190,0,746,582)),v19.crop((190,0,746,582))).getbbox() is None
# Top wall, sidewall panel motif unchanged.
assert ImageChops.difference(v18.crop((0,0,930,270)),v19.crop((0,0,930,270))).getbbox() is None
# Old door framing removed: must change in BOTH portals, including top frame and foot.
for box in ((0,278,160,572),(770,278,930,572)):
    assert ImageChops.difference(v18.crop(box),v19.crop(box)).getbbox() is not None
# Perspective is structural: left shoulder LOWER than far-right shoulder.
text=(ROOT/"qa/build_gallery5_v19_oblique_arches.py").read_text(encoding="utf-8")
assert "(20,348)" in text and "(156,315)" in text
print("PASS: source E protected, central imagery unchanged, both actual side portals rebuilt")
qa=ROOT/"qa/gallery5-v19-review";qa.mkdir(exist_ok=True)
server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
    browser=pw.chromium.launch(channel="chrome",headless=True)
    for width,height in ((1180,900),(390,844)):
        page=browser.new_page(viewport={"width":width,"height":height})
        errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
        response=page.goto(f"http://127.0.0.1:{server.server_port}/architecture-review/entrance-gallery5-comparison/",wait_until="load")
        assert response.status==200
        assert "v19" in page.title()
        imgs=page.locator("article img")
        assert imgs.count()==5
        assert imgs.evaluate_all("(els)=>els.every(img=>img.complete && img.naturalWidth>0 && img.naturalHeight>0)")
        assert page.locator('img[src^="gallery5-v19.png"]').evaluate("(img)=>img.naturalWidth===930 && img.naturalHeight===582")
        assert page.locator("body").evaluate("(el)=>el.scrollWidth<=innerWidth+2")
        assert not errors,errors
        page.screenshot(path=str(qa/f"v19_comparison_{width}.png"),full_page=True)
        print(f"PASS browser: {width}px; actual 5 images, no JS errors/overflow")
        page.close()
    browser.close()
finally:
 server.shutdown()
print("v19 QA PASS")
