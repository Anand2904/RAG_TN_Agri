# Tamil Nadu Agriculture Schemes Assistant — Local RAG

Bilingual English/Tamil Streamlit chatbot using Playwright, LangChain text splitting, multilingual Sentence Transformers embeddings, local FAISS vector search, and Ollama local generation.

> This is a learning project, not an official government service. Scheme information changes; confirm eligibility, amounts, deadlines and application steps at the linked official department. The app does not verify live scheme status.

## Requirements
- macOS; Python 3.11 or 3.12 recommended (newest Python versions may have ML dependency compatibility issues).
- Ollama installed; 16 GB RAM recommended.
- Internet for initial model download and permitted public-site collection.
- Review each site's terms and robots.txt. The scraper skips URLs if robots rules cannot be checked or disallow access. Never bypass access controls or rate limits.

## Setup on Mac
Extract this ZIP, open the extracted `TN_Agriculture_RAG` folder in VS Code, then use its integrated terminal:

```bash
python3 --version
python3 -m venv Myvenv
source Myvenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
cp .env.example .env
```

If you already have a `Myvenv` in this folder, just activate it with `source Myvenv/bin/activate`.

## Ollama
Install from https://ollama.com/download/mac. Then run:

```bash
ollama pull qwen2.5:3b
ollama list
ollama run qwen2.5:3b
```
Type a test question and `/bye` to exit. If unavailable, use a tag shown by `ollama list` and update `OLLAMA_MODEL` in `.env`. The multilingual embedding model downloads separately on first indexing.

## Collect and index
Review `sources.json` and add verified official scheme URLs or direct public PDF URLs. The starter list contains seed pages only; it does not automatically crawl every linked scheme page.

```bash
python scraper.py
python build_index.py
```

Raw downloads are in `data/raw/`, scrape results in `data/scrape_manifest.json`, processed document metadata in `data/processed/documents.json`, and FAISS files in `faiss_index/`. Do not commit the raw data, index or `.env` to a public repository.

## Run Streamlit

```bash
python -m streamlit run app.py
```
Open the local URL Streamlit prints, usually http://localhost:8501.

## Refresh index
Run `python scraper.py` then `python build_index.py`. Scraping/indexing is deliberately separate from ordinary chat. Restart Streamlit after a refresh to reload the dashboard counts.

## Troubleshooting
- `streamlit: command not found`: activate the environment, run `pip install -r requirements.txt`, then `python -m streamlit run app.py`.
- Ollama connection error: start the Ollama app, run `ollama list`, check `.env` model tag.
- Missing index: run scraper then build_index and confirm `faiss_index/index.faiss` exists.
- No documents: inspect `data/scrape_manifest.json`; site terms/robots, network, dynamic pages, or low text may be responsible. Only add URLs you are permitted to access. OCR for scanned PDFs is not included.
- Tamil retrieval: the default embedding model is multilingual, but validate with real Tamil questions and Tamil-language source pages.

## Security and limits
Scraped text is untrusted context. Only load FAISS files you created or trust because LangChain local persistence uses pickle deserialization. This app has no login system; do not expose it publicly or add privileged maintenance buttons without real authentication. The explorer lists collected documents, not a verified live list of active schemes.

## Manual validation
- [ ] scraper creates `data/scrape_manifest.json`
- [ ] build_index reports document and chunk counts
- [ ] `faiss_index/index.faiss` and `index.pkl` exist
- [ ] Ollama model responds
- [ ] app starts and chat works in English and Tamil
- [ ] source links are valid and support answers
- [ ] missing-index and Ollama-offline errors are friendly
- [ ] out-of-scope questions receive uncertainty, not invented facts
- [ ] explorer filters use actual processed documents
- [ ] check layout at narrow width and Tamil Unicode rendering

## Project tree
`app.py`, `config.py`, `translations.py`, `ui_components.py`, `scraper.py`, `document_processor.py`, `vector_store.py`, `rag_engine.py`, `build_index.py`, `sources.json`, `requirements.txt`, `.env.example`, `data/`, `tests/`.
