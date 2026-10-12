from vector_store import get_index_metadata,list_processed_documents
def test_metadata_defaults():
 m=get_index_metadata(); assert 'document_count' in m and 'chunk_count' in m
def test_documents_is_list(): assert isinstance(list_processed_documents(),list)
