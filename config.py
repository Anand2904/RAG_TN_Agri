import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()
@dataclass(frozen=True)
class Settings:
    ROOT: str=os.path.dirname(os.path.abspath(__file__))
    OLLAMA_BASE_URL: str=os.getenv("OLLAMA_BASE_URL","http://localhost:11434")
    OLLAMA_MODEL: str=os.getenv("OLLAMA_MODEL","llama3.2:1b")
    EMBEDDING_MODEL: str=os.getenv("EMBEDDING_MODEL","sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    CHUNK_SIZE: int=int(os.getenv("CHUNK_SIZE","900"))
    CHUNK_OVERLAP: int=int(os.getenv("CHUNK_OVERLAP","150"))
    TOP_K: int=int(os.getenv("TOP_K","5"))
    REQUEST_TIMEOUT: int=int(os.getenv("REQUEST_TIMEOUT","120"))
    @property
    def DATA_DIR(self): return os.path.join(self.ROOT,"data")
    @property
    def RAW_DIR(self): return os.path.join(self.DATA_DIR,"raw")
    @property
    def PROCESSED_DIR(self): return os.path.join(self.DATA_DIR,"processed")
    @property
    def FAISS_INDEX_DIR(self): return os.path.join(self.ROOT,"faiss_index")
    @property
    def SOURCES_FILE(self): return os.path.join(self.ROOT,"sources.json")
    @property
    def METADATA_FILE(self): return os.path.join(self.DATA_DIR,"metadata.json")
settings=Settings()
for p in (settings.RAW_DIR,settings.PROCESSED_DIR): os.makedirs(p,exist_ok=True)
