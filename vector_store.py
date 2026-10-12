import os,json,shutil,time
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import settings
_embeddings=None
def embeddings():
 global _embeddings
 if _embeddings is None: _embeddings=HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL,model_kwargs={'device':'cpu'},encode_kwargs={'normalize_embeddings':True})
 return _embeddings
def build_vector_store(chunks,doc_count):
 if not chunks: raise ValueError('No text chunks created. Check source URLs and extracted content.')
 temp=settings.FAISS_INDEX_DIR+'.building'; backup=settings.FAISS_INDEX_DIR+'.backup'
 for p in (temp,backup):
  if os.path.exists(p): shutil.rmtree(p)
 FAISS.from_documents(chunks,embeddings()).save_local(temp)
 FAISS.load_local(temp,embeddings(),allow_dangerous_deserialization=True)
 if os.path.exists(settings.FAISS_INDEX_DIR): os.replace(settings.FAISS_INDEX_DIR,backup)
 os.replace(temp,settings.FAISS_INDEX_DIR)
 if os.path.exists(backup): shutil.rmtree(backup)
 meta={'document_count':doc_count,'chunk_count':len(chunks),'last_successful_indexing':time.strftime('%Y-%m-%d %H:%M:%S'),'embedding_model':settings.EMBEDDING_MODEL}
 with open(settings.METADATA_FILE,'w',encoding='utf-8') as f: json.dump(meta,f,indent=2)
 return meta
def load_vector_store():
 if not os.path.exists(os.path.join(settings.FAISS_INDEX_DIR,'index.faiss')): return None
 return FAISS.load_local(settings.FAISS_INDEX_DIR,embeddings(),allow_dangerous_deserialization=True)
def get_index_metadata():
 try:
  with open(settings.METADATA_FILE,encoding='utf-8') as f: return json.load(f)
 except Exception: return {'document_count':0,'chunk_count':0,'last_successful_indexing':'—'}
def list_processed_documents():
 try:
  with open(os.path.join(settings.PROCESSED_DIR,'documents.json'),encoding='utf-8') as f: return json.load(f)
 except Exception: return []
