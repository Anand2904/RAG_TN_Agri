"""Fetch explicitly listed public URLs. Respect site terms and robots.txt; no crawling beyond sources.json."""
import asyncio,json,os,time,hashlib,logging
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from playwright.async_api import async_playwright
from config import settings
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s")
AGENT="TNAgricultureSchemesResearchBot/1.0 (polite public information indexing)"
def robots_allowed(url):
 p=urlparse(url); rp=RobotFileParser(); rp.set_url(f"{p.scheme}://{p.netloc}/robots.txt")
 try: rp.read(); return rp.can_fetch(AGENT,url)
 except Exception: return False
async def main():
 with open(settings.SOURCES_FILE,encoding='utf-8') as f: sources=json.load(f)
 saved=[]; failed=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True); context=await browser.new_context(user_agent=AGENT); page=await context.new_page()
  for src in sources:
   url=src.get('url','')
   if not url.startswith('https://') or not robots_allowed(url):
    failed.append({'url':url,'error':'Non-HTTPS, robots disallowed, or robots.txt unavailable'}); logging.warning('Skipping %s',url); continue
   try:
    resp=await page.goto(url,wait_until='domcontentloaded',timeout=45000); await page.wait_for_timeout(800)
    if not resp or resp.status>=400: raise RuntimeError(f"HTTP {resp.status if resp else 'no response'}")
    ctype=(resp.headers.get('content-type') or '').lower(); ext='.pdf' if 'pdf' in ctype or url.lower().endswith('.pdf') else '.html'
    body=await resp.body() if ext=='.pdf' else (await page.content()).encode('utf-8')
    name=''.join(c if c.isalnum() or c in '-_' else '_' for c in src.get('name','source'))[:60]
    path=os.path.join(settings.RAW_DIR,f"{name}_{hashlib.sha256(url.encode()).hexdigest()[:10]}{ext}")
    with open(path,'wb') as f: f.write(body)
    saved.append({**src,'raw_path':path,'content_type':ctype,'fetched_at':time.strftime('%Y-%m-%d %H:%M:%S'),'sha256':hashlib.sha256(body).hexdigest()})
    await asyncio.sleep(max(2,float(src.get('delay_seconds',2))))
   except Exception as e: failed.append({'url':url,'error':str(e)[:250]}); logging.exception('Failed %s',url)
  await browser.close()
 with open(os.path.join(settings.DATA_DIR,'scrape_manifest.json'),'w',encoding='utf-8') as f: json.dump({'saved':saved,'failed':failed},f,ensure_ascii=False,indent=2)
 print(f"Saved {len(saved)} source(s); failed/skipped {len(failed)}. See data/scrape_manifest.json")
if __name__=='__main__': asyncio.run(main())
