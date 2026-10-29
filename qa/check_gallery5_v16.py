"""A18 gallery 5 v16: center protrudes on BOTH edges.
Verify canonical E protection, identical center and corridors, real PNG copies,
and 390px/1180px comparison preview. Does not test gameplay.
"""
from pathlib import Path
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import json,subprocess,threading
R=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
C=R/"architecture-review/entrance-gallery5-comparison"
B=C/"frame-balance"
E=R/"rooms/gallery5/gallery5_palace_E.png"
assert E.is_file()
head=subprocess.check_output(["git","rev-parse","HEAD:rooms/gallery5/gallery5_palace_E.png"],cwd=R,text=True).strip()
disk=subprocess.check_output(["git","hash-object",str(E)],cwd=R,text=True).strip()
assert head==disk
metadata=json.loads((B/"v16_layout.json").read_text(encoding="utf-8"))
rects=metadata["rects"]
assert [(rects[n]["w"],rects[n]["h"],rects[n]["y"],rects[n]["bottom"]) for n in ("left","center","right")]==[(125,191,133,324),(270,240,98,338),(125,191,133,324)]
assert rects["center"]["y"]<rects["left"]["y"] and rects["center"]["bottom"]>rects["right"]["bottom"]
v15=Image.open(C/"gallery5-v15.png").convert("RGB")
v16=Image.open(C/"gallery5-v16.png").convert("RGB")
assert v15.size==v16.size==(930,582)
for key in ("rooms/gallery5/gallery5_palace_E_material_v16_REVIEW.png","architecture-review/gallery5/gallery5_v16_central_projection_REVIEW.png","architecture-review/entrance-gallery5-comparison/frame-balance/e_central_projection_v16.png"):
    assert (R/key).read_bytes()==(C/"gallery5-v16.png").read_bytes(),key
# Changes are local to the side frames; central exhibit and all architecture untouched.
for box in ((0,0,190,582),(344,95,583,341),(747,0,930,582)):
    assert ImageChops.difference(v15.crop(box),v16.crop(box)).getbbox() is None,box
for box in ((197,325,323,340),(608,325,734,340)):
    assert ImageChops.difference(v15.crop(box),v16.crop(box)).getbbox() is not None,box
print("PASS geometry: middle above+below, source E unchanged, same center/corridors")
out=R/"qa/gallery5-v16-review"
out.mkdir(exist_ok=True)
server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(R)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
    browser=pw.chromium.launch(channel="chrome",headless=True)
    for width,height in ((1180,900),(390,844)):
        page=browser.new_page(viewport={"width":width,"height":height})
        errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
        res=page.goto(f"http://127.0.0.1:{server.server_port}/architecture-review/entrance-gallery5-comparison/frame-balance/",wait_until="load")
        assert res.status==200
        imgs=page.locator(".card img")
        assert imgs.count()==6,imgs.count()
        assert imgs.evaluate_all("(items)=>items.every(i=>i.complete&&i.naturalWidth===930&&i.naturalHeight===582)")
        assert page.locator("body").evaluate("(el)=>el.scrollWidth<=innerWidth+2")
        page.screenshot(path=str(out/f"balance_v16_{width}.png"),full_page=True)
        res2=page.goto(f"http://127.0.0.1:{server.server_port}/architecture-review/entrance-gallery5-comparison/",wait_until="load")
        assert res2.status==200 and "v16" in page.title()
        assert page.locator('img[src^="gallery5-v16.png"]').evaluate("(img)=>img.complete&&img.naturalWidth===930")
        assert page.locator("body").evaluate("(el)=>el.scrollWidth<=innerWidth+2")
        page.screenshot(path=str(out/f"main_v16_{width}.png"),full_page=True)
        assert not errors,errors
        print("PASS browser",width,"six comparison PNGs / v16 front / no horizontal overflow / no errors")
        page.close()
    browser.close()
finally:
 server.shutdown()
print("Gallery5 v16 QA PASS")
