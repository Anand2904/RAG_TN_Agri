import json,os,re,hashlib
from bs4 import BeautifulSoup
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import settings
def process_documents():
 manifest=os.path.join(settings.DATA_DIR,'scrape_manifest.json')
 if not os.path.exists(manifest): raise FileNotFoundError('Run python scraper.py first.')
 with open(manifest,encoding='utf-8') as f: data=json.load(f)
 docs=[]
 for item in data.get('saved',[]):
  path=item.get('raw_path','')
  if not os.path.exists(path): continue
  try:
   if path.lower().endswith('.pdf'):
    title=item.get('name',os.path.basename(path)); text='\n'.join(p.extract_text() or '' for p in PdfReader(path).pages); dtype='PDF'
   else:
    with open(path,encoding='utf-8',errors='ignore') as f: soup=BeautifulSoup(f.read(),'html.parser')
    for tag in soup(['script','style','nav','footer','header','noscript','svg']): tag.decompose()
    title=soup.title.get_text(' ',strip=True) if soup.title else item.get('name','Government page'); text=re.sub(r'\s+',' ',soup.get_text(' ',strip=True)); dtype='Web page'
   if len(text)<80: continue
   md={k:item.get(k,'') for k in ['url','department','government_level','category','scheme_name','fetched_at','updated']}; md.update({'title':title,'document_type':dtype,'content_hash':hashlib.sha256(text.encode()).hexdigest()})
   docs.append(Document(page_content=text,metadata=md))
  except Exception as e: print(f"Skipping {path}: {e}")
 chunks=RecursiveCharacterTextSplitter(chunk_size=settings.CHUNK_SIZE,chunk_overlap=settings.CHUNK_OVERLAP).split_documents(docs)
 records=[{**d.metadata,'summary':d.page_content[:500]} for d in docs]
 with open(os.path.join(settings.PROCESSED_DIR,'documents.json'),'w',encoding='utf-8') as f: json.dump(records,f,ensure_ascii=False,indent=2)
 return chunks,len(docs)
