"""A18 Gallery 5 down-only, independent-material adjustable-frame QA.
Uses Chromium on localhost (not file://), tests real canvas pixels and mobile export.
"""
from pathlib import Path
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
import json,subprocess,threading
R=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
S=R/"architecture-review/entrance-gallery5-comparison/frame-adjuster"
E=R/"rooms/gallery5/gallery5_palace_E.png"
assert subprocess.check_output(["git","hash-object",str(E)],cwd=R,text=True).strip()==subprocess.check_output(["git","rev-parse","HEAD:rooms/gallery5/gallery5_palace_E.png"],cwd=R,text=True).strip()
for name in ("gallery5_unframed.png","frame_left.png","frame_center.png","frame_right.png"):
    p=S/name;assert p.is_file() and Image.open(p).width>0,p
assert Image.open(S/"gallery5_unframed.png").size==(930,582)
O=R/"qa/gallery5-frame-adjuster-review";O.mkdir(exist_ok=True)
server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(R)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
    browser=pw.chromium.launch(channel="chrome",headless=True)
    for width,height in ((1180,900),(390,844)):
        page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1,accept_downloads=True)
        errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
        response=page.goto(f"http://127.0.0.1:{server.server_port}/architecture-review/entrance-gallery5-comparison/frame-adjuster/",wait_until="load")
        page.get_by_text("実素材読込完了").wait_for()
        assert response.status==200
        assert not errors,errors
        assert page.locator("body").evaluate("(e)=>e.scrollWidth<=innerWidth+2"),width
        aspect=page.locator(".comparison img").evaluate("(e)=>e.getBoundingClientRect().width/e.getBoundingClientRect().height")
        assert abs(aspect-930/582)<0.02,aspect
        first=json.loads(page.locator("#json").input_value())
        assert first["valid"] and first["extendDownPx"]==0 and first["direction"]=="down-only"
        assert [(z["x"],z["y"],z["w"],z["h"]) for z in first["rects"]]==[(190,76,133,202),(329,68,270,210),(605,76,133,202)]
        assert all(z["bottom"]==278 for z in first["rects"])
        page.screenshot(path=str(O/f"initial_{width}.png"),full_page=True)
        original=page.locator("#stage").evaluate("(e)=>{const c=e.getContext('2d');return [[50,300],[875,300],[465,97],[265,100],[650,102]].map(([x,y])=>Array.from(c.getImageData(x,y,1,1).data))}")
        page.locator("#extend").fill("100")
        large=json.loads(page.locator("#json").input_value())
        assert large["valid"] and large["extendDownPx"]==100 and large["wallEnd"]==392,large
        assert all(z["bottom"]==378 for z in large["rects"])
        assert [(z["x"],z["y"],z["w"]) for z in large["rects"]]==[(z["x"],z["y"],z["w"]) for z in first["rects"]]
        assert [z["h"] for z in large["rects"]]==[302,310,302]
        assert page.locator("body").evaluate("(e)=>e.scrollWidth<=innerWidth+2")
        updated=page.locator("#stage").evaluate("(e)=>{const c=e.getContext('2d');return [[50,300],[875,300],[465,97],[265,100],[650,102]].map(([x,y])=>Array.from(c.getImageData(x,y,1,1).data))}")
        assert original==updated,("top and side must not move",original,updated)
        # Bottom interior clearly changes when extended, not just the label/JSON.
        before=page.locator("#stage").screenshot()
        page.locator("#extend").fill("0")
        zero=page.locator("#stage").screenshot()
        assert before!=zero
        page.locator("#extend").fill("100")
        page.screenshot(path=str(O/f"enlarged_{width}.png"),full_page=True)
        with page.expect_download() as download:page.locator("#save").click()
        assert download.value.suggested_filename=="gallery5_frames_extended_down.png"
        page.locator("#medium").click()
        assert json.loads(page.locator("#json").input_value())["extendDownPx"]==60
        page.locator("#large").click()
        assert json.loads(page.locator("#json").input_value())["extendDownPx"]==100
        page.locator("#reset").click()
        assert json.loads(page.locator("#json").input_value())["extendDownPx"]==0
        assert not errors,errors
        print(f"PASS viewport={width}: fixed tops and widths / 3 equal extensions / unchanged upper detail and corridors / exported / presets")
        page.close()
    browser.close()
finally:
 server.shutdown()
print("Down-only frame adjuster QA PASS")
