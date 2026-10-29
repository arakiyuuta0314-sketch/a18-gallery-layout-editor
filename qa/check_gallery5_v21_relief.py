"""A18 v21 side inset relief: true PNG / layout / release-preview QA.

Checks strict containment of edits to two ornamental panels, real-material
source preservation, original E integrity, PNG copy identity, and mobile/PC
comparison display. This is art-preview QA, NOT gameplay collision testing.
"""
from pathlib import Path
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import numpy as np,subprocess,threading,tempfile
ROOT=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
F=ROOT/"architecture-review/entrance-gallery5-comparison"
E=ROOT/"rooms/gallery5/gallery5_palace_E.png"
head=subprocess.check_output(["git","rev-parse","HEAD:rooms/gallery5/gallery5_palace_E.png"],cwd=ROOT,text=True).strip()
disk=subprocess.check_output(["git","hash-object",str(E)],cwd=ROOT,text=True).strip()
assert head==disk,(head,disk)
v20=Image.open(F/"gallery5-v20.png").convert("RGB")
v21=Image.open(F/"gallery5-v21.png").convert("RGB")
assert v20.size==v21.size==(930,582)
assert (F/"gallery5-v21.png").read_bytes()==(ROOT/"rooms/gallery5/gallery5_palace_E_material_v21_REVIEW.png").read_bytes()
a=np.array(v20,dtype=np.int16)
b=np.array(v21,dtype=np.int16)
diff=np.any(a!=b,axis=2)
allowed=np.zeros((582,930),dtype=bool)
allowed[77:183,55:142]=True
allowed[77:183,788:875]=True
assert not np.any(diff&~allowed),("Unexpected outside edit",int(np.sum(diff&~allowed)))
left=int(diff[77:183,55:142].sum());right=int(diff[77:183,788:875].sum())
assert left>1000 and right>1000,(left,right)
# Explicit source preservation for key areas, besides the full-mask assertion.
for rect in ((187,0,745,582),(0,194,185,582),(745,194,930,582),(0,0,930,60)):
    assert ImageChops.difference(v20.crop(rect),v21.crop(rect)).getbbox() is None,rect
for prefix,src in (("before",v20),("after",v21)):
    preview=Image.open(F/f"gallery5_panel_{prefix}_detail.png")
    expect=src.crop((43,60,153,195)).resize((440,540),Image.Resampling.NEAREST)
    assert preview.size==(440,540) and ImageChops.difference(preview.convert("RGB"),expect).getbbox() is None
print("PASS original E preserved; all changes restricted to two inset panels; true preview image copies")

server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
folder=Path(tempfile.gettempdir())/"a18_gallery5_v21_qa"
folder.mkdir(parents=True,exist_ok=True)
try:
  with sync_playwright() as p:
    browser=p.chromium.launch(channel="chrome",headless=True)
    for width,height in ((1180,900),(390,844)):
        page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1)
        errors=[];page.on("pageerror",lambda err:errors.append(str(err)))
        response=page.goto(f"http://127.0.0.1:{server.server_port}/architecture-review/entrance-gallery5-comparison/",wait_until="load")
        assert response.status==200 and "v21" in page.title()
        imgs=page.locator("article img")
        assert imgs.count()==7,imgs.count()
        assert imgs.evaluate_all("(els)=>els.every(el=>el.complete && el.naturalWidth>0 && el.naturalHeight>0)")
        assert page.locator('img[src^="gallery5-v21.png"]').evaluate("(el)=>el.naturalWidth===930 && el.naturalHeight===582")
        assert page.locator('img[src^="gallery5_panel_after_detail.png"]').evaluate("(el)=>el.naturalWidth===440 && el.naturalHeight===540")
        assert page.locator("body").evaluate("(el)=>el.scrollWidth<=innerWidth+2")
        assert not errors,errors
        page.screenshot(path=str(folder/f"ornament_v21_{width}.png"),full_page=True)
        print(f"PASS responsive review width={width}; images=7; overflow=none; errors=none")
        page.close()
    browser.close()
finally:
  server.shutdown()
print("QA screenshots (not committed):",folder)
print("A18 v21 art review QA PASS")
