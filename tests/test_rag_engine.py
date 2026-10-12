from unittest.mock import patch
from langchain_core.documents import Document
from rag_engine import answer_question
class FakeDB:
 def similarity_search(self,q,k=5): return [Document(page_content='Visit the department office for details.',metadata={'title':'Test source','url':'https://example.gov.in/scheme','department':'Agriculture'})]
def test_answer_has_source():
 with patch('rag_engine.generate',return_value='Check with the department. [Source 1]'):
  result=answer_question(FakeDB(),'How do I apply?','en')
 assert 'Source 1' in result['answer']; assert result['sources'][0]['url']=='https://example.gov.in/scheme'
