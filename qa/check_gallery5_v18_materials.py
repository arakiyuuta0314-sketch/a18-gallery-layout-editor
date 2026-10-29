"""A18 gallery5 v18 review QA: source-protection, material changes, browser and responsive layout."""
from pathlib import Path
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import subprocess,threading
R=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
D=R/"architecture-review/entrance-gallery5-comparison"
E=R/"rooms/gallery5/gallery5_palace_E.png"
assert E.is_file()
ref=subprocess.check_output(["git","rev-parse","HEAD:rooms/gallery5/gallery5_palace_E.png"],cwd=R,text=True).strip()
disk=subprocess.check_output(["git","hash-object",str(E)],cwd=R,text=True).strip()
assert ref==disk,(ref,disk)
v16=Image.open(D/"gallery5-v16.png").convert("RGB")
v17=Image.open(D/"gallery5-v17.png").convert("RGB")
v18=Image.open(D/"gallery5-v18.png").convert("RGB")
assert v16.size==v17.size==v18.size==(930,582)
for path in (R/"rooms/gallery5/gallery5_palace_E_material_v18_REVIEW.png",R/"architecture-review/gallery5/gallery5_v18_wall_portal_material_REVIEW.png"):
    assert path.read_bytes()==(D/"gallery5-v18.png").read_bytes(),path
for box in ((190,130,329,330),(325,95,603,345),(602,130,741,330),(317,23,616,94)):
    assert ImageChops.difference(v16.crop(box),v18.crop(box)).getbbox() is None,box
# Stone and carpet must actually have changed, instead of an unmodified relabeled PNG.
assert ImageChops.difference(v16.crop((190,370,300,575)),v18.crop((190,370,300,575))).getbbox()
assert ImageChops.difference(v16.crop((385,412,550,570)),v18.crop((385,412,550,570))).getbbox()
# Passage material changed but geometry remains: the mouth darkness is still the same.
for x,y in ((90,372),(840,372)):
    assert v16.getpixel((x,y))==v18.getpixel((x,y)),(x,y)
assert ImageChops.difference(v17.crop((185,355,745,582)),v18.crop((185,355,745,582))).getbbox() is None
print("PASS source E protected, v16 three frames unchanged, stone+rug edited, door opening geometry preserved")
OUT=R/"qa/gallery5-v18-review";OUT.mkdir(exist_ok=True)
server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(R)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
    browser=pw.chromium.launch(channel="chrome",headless=True)
    for width,height in ((1180,900),(390,844)):
        page=browser.new_page(viewport={"width":width,"height":height})
        errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
        res=page.goto(f"http://127.0.0.1:{server.server_port}/architecture-review/entrance-gallery5-comparison/",wait_until="load")
        assert res.status==200
        assert "v18" in page.title()
        imgs=page.locator("article img")
        assert imgs.count()==5,imgs.count()
        assert imgs.evaluate_all("(els)=>els.every(e=>e.complete && e.naturalWidth>0)")
        assert page.locator('img[src^="gallery5-v18.png"]').evaluate("(el)=>el.naturalWidth==930 && el.naturalHeight==582")
        assert page.locator("body").evaluate("(el)=>el.scrollWidth<=innerWidth+2")
        assert not errors,errors
        page.screenshot(path=str(OUT/f"v18_browser_{width}.png"),full_page=True)
        print("PASS comparison browser",width,"images 5 and no overflow")
        page.close()
    browser.close()
finally:
 server.shutdown()
print("PASS v18 material review")
