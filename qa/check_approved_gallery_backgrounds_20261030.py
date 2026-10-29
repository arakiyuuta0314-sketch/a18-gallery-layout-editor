"""A18 all five approved backgrounds – editor integration QA, no gameplay claim."""
from pathlib import Path
from PIL import Image
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from playwright.sync_api import sync_playwright
import threading,hashlib,json,subprocess,tempfile
ROOT=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
records=json.loads((ROOT/"rooms/approved_backgrounds_20261030.json").read_text(encoding="utf-8"))["rooms"]
assert len(records)==5 and set(records)=={f"gallery{i}" for i in range(1,6)}
for k,v in records.items():
    p=ROOT/v["asset"]
    assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==v["sha256"]
    assert Image.open(p).size==(930,582)
    current=json.loads((ROOT/f"rooms/{k}/room.json").read_text(encoding="utf-8"))
    baseline=subprocess.check_output(["git","show",f"HEAD:rooms/{k}/room.json"],cwd=ROOT)
    old=json.loads(baseline.decode("utf-8-sig"))
    assert current.pop("background")==v["asset"]
    assert old.pop("background") in (v["previousBackground"],v["asset"])
    assert current==old, f"Not allowed to modify frame/object/layout data for {k}"
head=subprocess.check_output(["git","rev-parse","HEAD:rooms/gallery5/gallery5_palace_E.png"],cwd=ROOT,text=True).strip()
disk=subprocess.check_output(["git","hash-object","rooms/gallery5/gallery5_palace_E.png"],cwd=ROOT,text=True).strip()
assert head==disk
out=Path(tempfile.gettempdir())/"a18_approved_5_rooms_qa"
out.mkdir(exist_ok=True)
server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel="chrome",headless=True)
  for width,height in ((1180,900),(390,844)):
   page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1)
   errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
   for room in records:
    url=f"http://127.0.0.1:{server.server_port}/?room={room}&rev=20261030-backgrounds"
    response=page.goto(url,wait_until="load")
    page.wait_for_function("window.__A18_LAYOUT_EDITOR__ && document.querySelector('#scene-layers img.art').complete")
    assert response.status==200
    assert page.locator("#room-title").inner_text()=="展示室"+room[-1]
    img=page.locator("#scene-layers img.art").first
    assert img.evaluate("(el)=>el.complete&&el.naturalWidth===930&&el.naturalHeight===582")
    assert img.get_attribute("src").split("?")[0]==records[room]["asset"]
    assert page.locator("#warning").inner_text().find("読み込みに失敗")<0
    page.evaluate("() => { document.querySelector(\'#stage\').style.transform=\'scale(.35)\';document.querySelector(\'#outer\').style.width=\'325.5px\';document.querySelector(\'#outer\').style.height=\'203.7px\'; }")
    page.screenshot(path=str(out/f"{room}_{width}.png"),full_page=True)
    print(f"PASS {room} {width}: actual approved image loaded; no source layout changes")
   response=page.goto(f"http://127.0.0.1:{server.server_port}/whole-museum-review/approved-backgrounds/",wait_until="load")
   assert response.status==200
   cards=page.locator(".card img")
   assert cards.count()==6,cards.count()
   assert cards.evaluate_all("(els)=>els.every(i=>i.complete&&i.naturalWidth>0)")
   assert page.locator("body").evaluate("(e)=>e.scrollWidth<=innerWidth+2")
   page.screenshot(path=str(out/f"all_rooms_{width}.png"),full_page=True)
   print(f"PASS whole-museum approved backgrounds overview {width}: 6 cards (entrance+five galleries)")
   assert not errors,errors
   page.close()
  browser.close()
finally:
 server.shutdown()
print("ALL 5 EDITOR BACKGROUNDS PASS; report screenshots:",out)