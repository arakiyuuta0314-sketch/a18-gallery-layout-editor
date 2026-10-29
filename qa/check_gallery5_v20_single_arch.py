"""v20 gallery5 skewed-portal source QA, geometry preservation and actual mobile page QA."""
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
v18=Image.open(D/"gallery5-v19.png").convert("RGB")
v20=Image.open(D/"gallery5-v20.png").convert("RGB")
assert v18.size==v20.size==(930,582)
assert (D/"gallery5-v20.png").read_bytes()==(ROOT/"architecture-review/gallery5/gallery5_v20_single_arched_portals_REVIEW.png").read_bytes()
assert (D/"gallery5-v20.png").read_bytes()==(ROOT/"rooms/gallery5/gallery5_palace_E_material_v20_REVIEW.png").read_bytes()
# Main room area must be pixel-perfect: frame geometry, runner, and stone floor.
assert ImageChops.difference(v18.crop((190,0,746,582)),v20.crop((190,0,746,582))).getbbox() is None
# Top wall, sidewall panel motif unchanged.
assert ImageChops.difference(v18.crop((0,0,930,270)),v20.crop((0,0,930,270))).getbbox() is None
# Double-line contour cleaned on BOTH passages; geometry remains left/right.
for box in ((0,278,160,572),(770,278,930,572)):
    assert ImageChops.difference(v18.crop(box),v20.crop(box)).getbbox() is not None
# Perspective is structural: left shoulder LOWER than far-right shoulder.
text=(ROOT/"qa/build_gallery5_v20_single_arch.py").read_text(encoding="utf-8")
assert "(20,348)" in text and "(156,315)" in text
assert "rear_arch=" not in text, "duplicate receding arch should be removed"
assert 'dr.line(X(rear_arch)' not in text, "second arch stroke must not return"
assert '"#ad8050",width=2,joint="curve"' not in text, "interior golden arc is forbidden"
print("PASS: E protected, central imagery unchanged, both portal interiors revised; secondary arch removed")
qa=ROOT/"qa/gallery5-v20-review";qa.mkdir(exist_ok=True)
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
        assert "v20" in page.title()
        imgs=page.locator("article img")
        assert imgs.count()==5
        assert imgs.evaluate_all("(els)=>els.every(img=>img.complete && img.naturalWidth>0 && img.naturalHeight>0)")
        assert page.locator('img[src^="gallery5-v20.png"]').evaluate("(img)=>img.naturalWidth===930 && img.naturalHeight===582")
        assert page.locator("body").evaluate("(el)=>el.scrollWidth<=innerWidth+2")
        assert not errors,errors
        page.screenshot(path=str(qa/f"v20_comparison_{width}.png"),full_page=True)
        print(f"PASS browser: {width}px; actual 5 images, no JS errors/overflow")
        page.close()
    browser.close()
finally:
 server.shutdown()
print("v20 QA PASS")