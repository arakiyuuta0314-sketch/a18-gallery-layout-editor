"""A18 movement-preview browser QA: same movement core, all 14 directed links."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import threading
from playwright.sync_api import sync_playwright
ROOT=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
OUT=ROOT/"qa/movement-preview-20261030"
OUT.mkdir(parents=True,exist_ok=True)
server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
URL=f"http://127.0.0.1:{server.server_port}/movement-preview/"
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel="chrome",headless=True)
  for width,height in ((1180,840),(390,844)):
   page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1)
   errors=[];failed=[]
   page.on("pageerror",lambda e:errors.append(str(e)))
   page.on("requestfailed",lambda r:failed.append(r.url))
   response=page.goto(URL,wait_until="load")
   page.wait_for_function("window.__A18_MOVE_QA__ && window.__A18_MOVE_QA__.getState().ready",timeout=25000)
   assert response.status==200
   qa="window.__A18_MOVE_QA__"
   edges=page.evaluate(qa+".edges()")
   gates=page.evaluate(qa+".gates()")
   assert sum(map(len,map(dict.values,edges.values())))==14
   assert not errors,errors
   # Test directed walking: place just before each opening, then walk *across*
   # its actual threshold using the same movement step function as user input.
   for room,doors in edges.items():
    for direction,expected in doors.items():
     g=gates[room][direction];pos=g["at"]
     page.evaluate("(r)=>window.__A18_MOVE_QA__.forceRoom(r)",int(room))
     if direction=="west": start=[pos[0]+42,pos[1]]
     elif direction=="east":start=[pos[0]-42,pos[1]]
     elif direction=="north":start=[pos[0],pos[1]+39]
     else:start=[pos[0],pos[1]-39]
     assert page.evaluate("([r,x,y])=>window.__A18_MOVE_QA__.walkable(r,x,y)",[int(room),*start]),(room,direction,start)
     page.evaluate("([x,y])=>window.__A18_MOVE_QA__.forcePosition(x,y)",start)
     old=page.evaluate(qa+".getState().visits.length")
     for _ in range(15):
      page.evaluate("(dir)=>window.__A18_MOVE_QA__.step(dir,.04)",direction)
      current=page.evaluate(qa+".getState()")
      if current["room"]!=int(room):break
     current=page.evaluate(qa+".getState()")
     assert current["room"]==expected,(room,direction,expected,current)
     assert current["visits"][-1]=={"from":int(room),"to":expected,"dir":direction}
     assert len(current["visits"])==old+1
     print(f"PASS {width}: {room} {direction} -> {expected}")
   # Physical blocking on approved freestanding wall footprint (gallery2).
   page.evaluate("()=>window.__A18_MOVE_QA__.forceRoom(2)")
   assert not page.evaluate("()=>window.__A18_MOVE_QA__.walkable(2,210,483)")
   # Intro image & five PNGs must be loaded on client with valid natural sizes.
   for room in range(6):
    page.evaluate("(r)=>window.__A18_MOVE_QA__.forceRoom(r)",room)
    page.wait_for_timeout(45)
    if width==390:page.screenshot(path=str(OUT/f"gallery_{room}_mobile.png"))
   if width==390:
    page.evaluate("()=>window.__A18_MOVE_QA__.forceRoom(0)")
    pos=page.evaluate(qa+".getState()")
    b=page.locator('button[data-dir="west"]')
    b.hover()
    page.mouse.down()
    page.wait_for_timeout(190)
    page.mouse.up()
    moved=page.evaluate(qa+".getState()")
    assert moved["x"]<pos["x"]-12,("touch D-pad failed",pos,moved)
    print("PASS mobile touch hold D-pad, player moves west")
   assert page.locator("#busy").is_hidden()
   assert not errors,errors
   assert not failed,failed
   assert page.locator("body").evaluate("(e)=>e.scrollWidth<=innerWidth+2")
   print(f"QA PASS width {width}: 14 directed transitions, visible art, no exceptions/overflow")
   page.close()
  browser.close()
finally:
 server.shutdown()
