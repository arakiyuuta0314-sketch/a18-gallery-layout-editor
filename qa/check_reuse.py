"""Reusable-room QA: ephemeral synthetic fixture only, never deployed as gallery2."""
from pathlib import Path
from tempfile import TemporaryDirectory
from shutil import copy2
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import json
SOURCE=Path(__file__).resolve().parent.parent
with TemporaryDirectory(prefix='a18-layout-room-reuse-') as tmp:
    root=Path(tmp)
    (root/'rooms/gallery1').mkdir(parents=True)
    (root/'rooms/testroom').mkdir(parents=True)
    for name in ['index.html','editor.js']:
        copy2(SOURCE/name,root/name)
    for name in ['architecture.png','side-walls.png','counter135_staff.png']:
        copy2(SOURCE/'rooms/gallery1'/name,root/'rooms/testroom'/name)
    for p in (SOURCE/'rooms/gallery1').glob('*'):
        copy2(p,root/'rooms/gallery1'/p.name)
    config=json.loads((SOURCE/'rooms/gallery1/room.json').read_text('utf8'))
    config.update(id='testroom',name='仮テスト展示室',subtitle='実サイトには公開しないQA用')
    config['objects']=[{'id':'fixture-alpha','label':'仮配置設備','image':'rooms/testroom/counter135_staff.png',
                         'rect':{'x':200,'y':380,'w':135,'h':76}}]
    config['background']='rooms/testroom/architecture.png'
    config['foreground']='rooms/testroom/side-walls.png'
    (root/'rooms/testroom/room.json').write_text(json.dumps(config,ensure_ascii=False),encoding='utf8')
    catalog={'rooms':[{'id':'gallery1','name':'展示室1','config':'rooms/gallery1/room.json'},
                      {'id':'testroom','name':'仮テスト展示室','config':'rooms/testroom/room.json'}]}
    (root/'rooms/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False),encoding='utf8')
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self,*args): pass
    srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
    Thread(target=srv.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',args=['--no-sandbox'])
            page=browser.new_page(viewport={'width':390,'height':844})
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(f'http://127.0.0.1:{srv.server_port}/?room=testroom',wait_until='networkidle')
            page.wait_for_function('typeof window.__A18_LAYOUT_EDITOR__==="object"')
            get=lambda:page.evaluate('window.__A18_LAYOUT_EDITOR__.getState()')
            assert get()['roomId']=='testroom'
            assert list(get()['objects'])==['fixture-alpha']
            assert page.locator('[data-pick]').count()==1
            assert get()['objects']['fixture-alpha']['x']==200
            page.locator('[data-move="10,0"]').click()
            assert get()['objects']['fixture-alpha']['x']==210
            page.locator('#room-select').select_option('gallery1')
            page.wait_for_function('window.__A18_LAYOUT_EDITOR__.getState().roomId==="gallery1"')
            assert list(get()['objects'])==['wall4','wall5','counter']
            assert get()['objects']['counter']['w']==135 and get()['objects']['counter']['h']==76
            page.locator('#room-select').select_option('testroom')
            page.wait_for_function('window.__A18_LAYOUT_EDITOR__.getState().roomId==="testroom"')
            assert get()['objects']['fixture-alpha']['x']==210
            page.locator('summary').click()
            page.locator('#show-import').click()
            invalid={'roomId':'gallery1','objects':get()['objects']}
            page.locator('#json-text').fill(json.dumps(invalid))
            page.locator('#apply-import').click()
            assert '失敗' in page.locator('#status').inner_text()
            assert not errors,errors
            print('PASS reusable engine: second room with different ID/object count, switch, per-room persistence, wrong-room import rejected')
            browser.close()
    finally:
        srv.shutdown()
        srv.server_close()
