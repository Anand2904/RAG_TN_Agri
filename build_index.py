from document_processor import process_documents
from vector_store import build_vector_store
def main():
 print('Processing scraped documents…'); chunks,count=process_documents(); print(f'Found {count} documents and {len(chunks)} chunks.'); meta=build_vector_store(chunks,count); print('Index built:'); [print(f'  {k}: {v}') for k,v in meta.items()]
if __name__=='__main__': main()
