"""Gallery 5 balance A/B/C actual-artifact QA; not gameplay QA."""
from pathlib import Path
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import json, subprocess, threading
R=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
G=R/"architecture-review/entrance-gallery5-comparison/frame-balance"
BASE=R/"architecture-review/entrance-gallery5-comparison"
e=R/"rooms/gallery5/gallery5_palace_E.png"
head=subprocess.check_output(["git","rev-parse","HEAD:rooms/gallery5/gallery5_palace_E.png"],cwd=R,text=True).strip()
disk=subprocess.check_output(["git","hash-object",str(e)],cwd=R,text=True).strip()
assert head==disk,(head,disk)
data=json.loads((G/"variants.json").read_text(encoding="utf-8"))
assert len(data)==3
side_reference=Image.open(BASE/"frame-adjuster/gallery5_unframed.png").convert("RGB")
for rec in data:
    image=Image.open(G/rec["image"]).convert("RGB")
    assert image.size==(930,582)
    assert {r["bottom"] for r in rec["rects"].values()}=={338}
    assert all(rec["rects"][name]["x"]==x for name,x in (("left",190),("center",329),("right",605)))
    # Existing side corridors and architecture untouched outside the rear wall.
    for box in ((0,0,184,582),(746,0,930,582)):
        assert ImageChops.difference(image.crop(box),side_reference.crop(box)).getbbox() is None,(rec["id"],box)
assert [data[0]["rects"]["left"]["h"],data[1]["rects"]["left"]["h"],data[2]["rects"]["left"]["h"]]==[262,202,232]
print("ASSET geometry and preserved side architecture PASS")
out=R/"qa/gallery5-frame-balance-review";out.mkdir(exist_ok=True)
server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(R)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
    browser=pw.chromium.launch(channel="chrome",headless=True)
    for w,h in ((1180,900),(390,844)):
        page=browser.new_page(viewport={"width":w,"height":h})
        errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
        res=page.goto(f"http://127.0.0.1:{server.server_port}/architecture-review/entrance-gallery5-comparison/frame-balance/",wait_until="load")
        assert res.status==200
        imgs=page.locator(".card img")
        assert imgs.count()==4
        assert imgs.evaluate_all("(els)=>els.every(el=>el.complete && el.naturalWidth===930 && el.naturalHeight===582)")
        assert page.locator("body").evaluate("(e)=>e.scrollWidth<=innerWidth+2")
        assert not errors,errors
        page.screenshot(path=str(out/f"balance_{w}.png"),full_page=True)
        print("BROWSER",w,"PASS, four art assets loaded")
        page.close()
    browser.close()
finally:
 server.shutdown()
print("Gallery5 balance review QA PASS")
