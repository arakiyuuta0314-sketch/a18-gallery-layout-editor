from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'qa'
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',args=['--no-sandbox'])
  for w,h in [(1180,920),(390,844)]:
   ctx=browser.new_context(viewport={'width':w,'height':h},permissions=['clipboard-read','clipboard-write'])
   page=ctx.new_page()
   errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   result=page.goto(f'http://127.0.0.1:{server.server_port}/?room=gallery1',wait_until='networkidle')
   assert result.status==200,result.status
   page.wait_for_function('typeof window.__A18_LAYOUT_EDITOR__ === "object"',timeout=10000)
   state=lambda:page.evaluate('window.__A18_LAYOUT_EDITOR__.getState()')
   s=state()
   assert s['roomId']=='gallery1'
   assert s['objects']['counter']==dict(x=425,y=396,w=175,h=96)
   assert page.locator('[data-object]').count()==3
   assert page.locator('#warning').inner_text()==''
   assert page.locator('#stage img').count()==5
   assert all(n.evaluate('e=>e.complete && e.naturalWidth>0') for n in page.locator('#stage img').all())
   page.locator('[data-pick=counter]').click()
   page.locator('[data-move="10,0"]').click()
   assert state()['objects']['counter']['x']==435
   page.locator('#undo').click()
   assert state()['objects']['counter']['x']==425
   page.locator('#redo').click()
   assert state()['objects']['counter']['x']==435
   page.locator('#coord-x').fill('425')
   page.locator('#coord-x').press('Tab')
   assert state()['objects']['counter']['x']==425
   page.locator('#center-view').click()
   rect=page.locator('[data-object="wall5"]').bounding_box()
   assert rect and rect['width']>100,(w,rect)
   x=rect['x']+rect['width']*.5;y=rect['y']+rect['height']*.65
   page.mouse.move(x,y);page.mouse.down();page.mouse.move(x-24,y+8,steps=5);page.mouse.up()
   assert state()['objects']['wall5']['x']==598,state()['objects']['wall5']
   page.reload(wait_until='networkidle')
   page.wait_for_function('typeof window.__A18_LAYOUT_EDITOR__ === "object"',timeout=10000)
   assert state()['objects']['wall5']['x']==598
   page.locator('summary').click();page.locator('#show-import').click()
   bad=state();bad['objects']['counter']['w']=205
   page.locator('#json-text').fill(json.dumps(bad))
   page.locator('#apply-import').click()
   assert '失敗' in page.locator('#status').inner_text()
   page.once('dialog',lambda diag:diag.accept())
   page.locator('#reset').click()
   assert state()['objects']['wall5']['x']==628
   page.locator('#pan-mode').click()
   assert page.locator('[data-object=wall4]').evaluate('e=>getComputedStyle(e).pointerEvents')=='none'
   page.locator('#zoom').select_option('.5')
   assert page.locator('#outer').evaluate('e=>Math.round(e.getBoundingClientRect().width)')==465
   page.locator('#edit-mode').click()
   page.screenshot(path=str(OUT/f'editor_{w}.png'),full_page=True)
   assert not errors,errors
   print('PASS',w,'catalog+gallery1+drag+coordinates+history+persistence+JSON+zoom+images')
   ctx.close()
  browser.close()
finally:
 server.shutdown();server.server_close()
