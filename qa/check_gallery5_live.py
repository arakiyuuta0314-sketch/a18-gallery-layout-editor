from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
from PIL import Image
import json
root=Path(__file__).resolve().parents[1]
room=json.loads((root/'rooms/gallery5/room.json').read_text(encoding='utf-8'))
assert room['id']=='gallery5'
assert room['frameCount']==5
assert room['previewArtworkCount']==3 and room['background'].endswith('gallery5_palace_E.png')
assert room['entrance'].startswith('南') and room['exit'].startswith('西')
assert '東' in room['exit'] and len(room['objects'])==0
assert room['layoutRevision']=='gallery5-palace-E-visual-approved-20261029'
assert room['status'].startswith('E palace visual design approved')
for name in ('gallery5_concept_A.png','gallery5_concept_B.png','gallery5_architecture_only.png',
             'gallery5_heavy_C.png','gallery5_heavy_D.png','gallery5_heavy_architecture_C.png',
             'gallery5_palace_E.png','gallery5_palace_F.png','gallery5_palace_architecture_E.png'):
 assert Image.open(root/'rooms/gallery5'/name).size==(930,582)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',args=['--no-sandbox'])
  for width in (1180,390):
   ctx=browser.new_context(viewport={'width':width,'height':850})
   page=ctx.new_page();errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   r=page.goto(f'http://127.0.0.1:{server.server_port}/?room=gallery5&rev=palace-EF-qa',wait_until='networkidle')
   assert r.status==200
   page.wait_for_function('window.__A18_LAYOUT_EDITOR__ && window.__A18_LAYOUT_EDITOR__.getState().roomId==="gallery5"')
   st=page.evaluate('window.__A18_LAYOUT_EDITOR__.getState()')
   assert st['objects']=={},st
   assert page.locator('#zoom').input_value()==('.35' if width==390 else '.8')
   assert all(page.locator('#stage img').evaluate_all('(es)=>es.map(e=>e.complete && e.naturalWidth>0)'))
   assert any('gallery5_palace_E.png' in s for s in page.locator('#stage img').evaluate_all('(es)=>es.map(e=>e.src)'))
   assert not errors,errors
   page.screenshot(path=str(root/'rooms/gallery5'/f'editor_gallery5_{width}.png'),full_page=True)
   print('PASS gallery5 palace E visually approved',width,'3 art visuals; original game 5 fixtures unchanged')
   ctx.close()
  browser.close()
finally:
 server.shutdown();server.server_close()
