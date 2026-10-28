from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',args=['--no-sandbox'])
  for width in (1180,390):
   ctx=browser.new_context(viewport={'width':width,'height':850})
   page=ctx.new_page();errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   res=page.goto(f'http://127.0.0.1:{server.server_port}/?room=gallery3',wait_until='networkidle')
   assert res.status==200
   page.wait_for_function('window.__A18_LAYOUT_EDITOR__ && window.__A18_LAYOUT_EDITOR__.getState().roomId === "gallery3"')
   state=page.evaluate('window.__A18_LAYOUT_EDITOR__.getState()')
   assert len(state['objects'])==3,state
   assert all(e.evaluate('e=>e.complete && e.naturalWidth>0') for e in page.locator('#stage img').all())
   assert not errors,errors
   page.screenshot(path=str(root/'rooms/gallery3'/f'editor_gallery3_{width}.png'),full_page=True)
   print('PASS gallery3',width,state['objects'])
   ctx.close()
  browser.close()
finally:
 server.shutdown();server.server_close()
