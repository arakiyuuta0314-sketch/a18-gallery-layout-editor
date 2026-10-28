from playwright.sync_api import sync_playwright
from pathlib import Path
p=Path('C:/Users/User/source/repos/a18-gallery-layout-editor/qa/architecture-bases-20261029')
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe')
 page=b.new_page(viewport={'width':1180,'height':860})
 page.goto('https://arakiyuuta0314-sketch.github.io/web-tools-preview/a18/layout-test/')
 page.wait_for_timeout(900)
 page.get_by_text('開始',exact=True).click()
 page.wait_for_timeout(350)
 page.locator('#a18OpeningSkip').click()
 page.locator('input').first.fill('QA')
 page.locator('#confirmName').click()
 page.wait_for_timeout(1300)
 print('visible',[(x.get_attribute('id'),x.inner_text()[:25].encode('unicode_escape').decode()) for x in page.locator('button:visible').all()][:25])
 page.screenshot(path=str(p/'entrance_lv1_live_game.png'),full_page=True)
 b.close()
