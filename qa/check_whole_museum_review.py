"""Ensure full-museum review matches approved sources and is phone/desktop readable."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright
from PIL import Image
import hashlib,json
repo=Path(__file__).resolve().parents[1]
out=repo/"whole-museum-review"
metadata=json.loads((out/"overview.json").read_text(encoding="utf-8"))
assert metadata["reviewOnly"] is True
assert metadata["approvedTargets"]=={"entrance":3,"gallery1":5,"gallery2":5,"gallery3":5,"gallery4":5,"gallery5":3,"total":26}
assert metadata["runtime"]=={"currentTotalFrames":28,"currentGallery5Frames":5,"status":"deferred implementation"}
assert metadata["order"]==["gallery3","gallery5","gallery4","gallery1","entrance","gallery2"]
assert len(metadata["rooms"])==6
assert hashlib.sha256((out/"entrance_approved_lv6.png").read_bytes()).hexdigest()==metadata["entranceApprovedSha256"]
assert Image.open(out/"whole_museum_map_3x2.png").size==(1846,995)
for i in range(1,6):
 assert Image.open(out/f"gallery{i}_approved_layout.png").size==(930,582)
source=json.loads((repo/"rooms/gallery5/room.json").read_text(encoding="utf-8"))
assert (source["frameCount"],source["approvedTargetFrameCount"],source["previewArtworkCount"])==(5,3,3)
assert "DECIDED_NOT_IMPLEMENTED"==source["frameCountChangeStatus"]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
srv=ThreadingHTTPServer(("127.0.0.1",0),partial(Quiet,directory=str(repo)))
Thread(target=srv.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",args=["--no-sandbox"])
  for width in (390,1180):
   ctx=browser.new_context(viewport={"width":width,"height":800})
   page=ctx.new_page();errors=[]
   page.on("pageerror",lambda e:errors.append(str(e)))
   r=page.goto(f"http://127.0.0.1:{srv.server_port}/whole-museum-review/",wait_until="networkidle",timeout=18000)
   assert r.status==200
   assert page.locator(".card").count()==6
   assert page.locator("img").count()==6
   assert all(page.locator("img").evaluate_all("(els)=>els.map(e=>e.complete && e.naturalWidth>0)"))
   cols=page.evaluate("getComputedStyle(document.querySelector('.museum')).gridTemplateColumns.split(' ').length")
   assert cols==(1 if width==390 else 3),(width,cols)
   assert not errors,errors
   page.screenshot(path=str(out/f"whole_museum_browser_{width}.png"),full_page=True)
   print("PASS six-room review",width,"cols",cols,"images",6,"runtime untouched")
   ctx.close()
  browser.close()
finally:
 srv.shutdown();srv.server_close()
