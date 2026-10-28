from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
from PIL import Image
import json
root=Path(__file__).resolve().parents[1]
room=json.loads((root/'rooms/gallery4/room.json').read_text(encoding='utf-8'))
assert room['id']=='gallery4'
assert room['entrance'].startswith('南') and room['exit'].startswith('西')
assert len(room['objects'])==1 and room['objects'][0]['id']=='wall5'
shapes=room['proposedFixtureShapes']
assert list(shapes.values()).count('portrait')==2
assert list(shapes.values()).count('landscape')==3
assert set(shapes)=={f'frame-4-{i}' for i in range(5)}
for f in ('gallery4_concept_A.png','gallery4_concept_B.png','gallery4_AB_comparison.png'):
 assert Image.open(root/'rooms/gallery4'/f).width>=930
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
   res=page.goto(f'http://127.0.0.1:{server.server_port}/?room=gallery4&rev=A-qa',wait_until='networkidle')
   assert res.status==200
   page.wait_for_function('window.__A18_LAYOUT_EDITOR__ && window.__A18_LAYOUT_EDITOR__.getState().roomId==="gallery4"')
   state=page.evaluate('window.__A18_LAYOUT_EDITOR__.getState()')
   assert state['objects']=={'wall5':{'x':614,'y':323,'w':210,'h':165}},state
   assert page.locator('#zoom').input_value()==('.35' if width==390 else '.8')
   assert all(page.locator('#stage img').evaluate_all('(es)=>es.map(e=>e.complete&&e.naturalWidth>0)'))
   assert not errors,errors
   page.screenshot(path=str(root/'rooms/gallery4'/f'editor_gallery4_{width}.png'),full_page=True)
   print('PASS gallery4 A draft',width,state['objects'])
   ctx.close()
  browser.close()
finally:
 server.shutdown();server.server_close()
