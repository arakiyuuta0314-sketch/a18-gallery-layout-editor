"""A18 Gallery 5 adjustable frame preview QA. Local static page and smartphone behavior only."""
from pathlib import Path
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
import subprocess,json
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
import threading
R=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
S=R/"architecture-review/entrance-gallery5-comparison/frame-adjuster"
E=R/"rooms/gallery5/gallery5_palace_E.png"
assert E.is_file()
assert subprocess.check_output(["git","hash-object",str(E)],cwd=R,text=True).strip()==subprocess.check_output(["git","rev-parse","HEAD:rooms/gallery5/gallery5_palace_E.png"],cwd=R,text=True).strip()
for name in ("gallery5_unframed.png","frame_left.png","frame_center.png","frame_right.png"):
    p=S/name;assert p.is_file() and Image.open(p).width>0,(p,Image.open(p).size)
assert Image.open(S/"gallery5_unframed.png").size==(930,582)
O=R/"qa/gallery5-frame-adjuster-review";O.mkdir(exist_ok=True)
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(R)))
threading.Thread(target=server.serve_forever,daemon=True).start()
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
        # The fixed v14 image must retain its 930:582 aspect ratio on a phone.
        aspect=page.locator(".comparison img").evaluate("(e)=>e.getBoundingClientRect().width/e.getBoundingClientRect().height")
        assert abs(aspect-930/582)<0.02,aspect
        first=json.loads(page.locator("#json").input_value())
        assert first["valid"] and first["widthPercent"]==100 and first["heightPercent"]==100
        assert [z["h"] for z in first["rects"]]==[202]*3
        assert first["rects"][1]["w"]>first["rects"][0]["w"]
        page.screenshot(path=str(O/f"initial_{width}.png"),full_page=True)
        page.locator("#height").fill("130")
        page.locator("#bottom").fill("347")
        large=json.loads(page.locator("#json").input_value())
        assert large["valid"] and large["heightPercent"]==130 and large["bottom"]==347,large
        assert all(z["y"]+z["h"]==347 for z in large["rects"])
        assert all(z["h"]==263 for z in large["rects"])
        assert large["wallEnd"]==360
        assert page.locator("body").evaluate("(e)=>e.scrollWidth<=innerWidth+2")
        # Sidewall pixels must remain identical even while rear wall & carpet shift.
        # Compare screenshots of the canvas' side bands while render is changed.
        page.locator("#reset").click()
        original=page.locator("#stage").evaluate("(e)=>{const c=e.getContext('2d');return [Array.from(c.getImageData(50,300,1,1).data),Array.from(c.getImageData(875,300,1,1).data)]}")
        page.locator("#height").fill("130");page.locator("#bottom").fill("347")
        updated=page.locator("#stage").evaluate("(e)=>{const c=e.getContext('2d');return [Array.from(c.getImageData(50,300,1,1).data),Array.from(c.getImageData(875,300,1,1).data)]}")
        assert original==updated,(original,updated)
        page.screenshot(path=str(O/f"enlarged_{width}.png"),full_page=True)
        with page.expect_download() as got:page.locator("#save").click()
        assert got.value.suggested_filename=="gallery5_frame_adjust_preview.png"
        page.locator("#width").fill("110")
        invalid=json.loads(page.locator("#json").input_value())
        assert not invalid["valid"]
        assert page.locator("#copy").is_disabled() and page.locator("#save").is_disabled()
        page.locator("#large").click()
        preset=json.loads(page.locator("#json").input_value())
        assert preset["valid"] and preset["heightPercent"]==125 and preset["bottom"]==334
        page.locator("#reset").click()
        assert json.loads(page.locator("#json").input_value())["heightPercent"]==100
        assert not errors,errors
        print(f"PASS viewport={width} initial / enlarged / sidewall protected / invalid width / export / presets / scroll")
        page.close()
    browser.close()
server.shutdown()
print("Frame adjuster QA PASS")
