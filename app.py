import os
import streamlit as st
from config import settings
from translations import T, detect_language
from vector_store import load_vector_store, get_index_metadata, list_processed_documents
from rag_engine import answer_question
from ui_components import inject_css, render_header, render_sources, render_scheme_explorer

st.set_page_config(page_title="Tamil Nadu Agriculture Schemes Assistant", page_icon="🌾", layout="wide")
inject_css()
if "ui_language" not in st.session_state: st.session_state.ui_language="en"
if "messages" not in st.session_state: st.session_state.messages=[]
if "selected_question" not in st.session_state: st.session_state.selected_question=""
def tr(key): return T.get(st.session_state.ui_language,T["en"]).get(key,T["en"].get(key,key))
meta=get_index_metadata(); docs=list_processed_documents()
with st.sidebar:
    st.markdown("## 🌱 TN Agri Assist")
    choice=st.selectbox("Interface language",["English","தமிழ்","Auto-detect"], index={"en":0,"ta":1}.get(st.session_state.ui_language,0))
    if choice=="English": st.session_state.ui_language="en"
    elif choice=="தமிழ்": st.session_state.ui_language="ta"
    else:
        last=next((m["content"] for m in reversed(st.session_state.messages) if m["role"]=="user"),"")
        st.session_state.ui_language=detect_language(last) if last else "en"
    st.divider(); st.markdown(f"**{tr('knowledge_base')}**")
    ready=os.path.exists(os.path.join(settings.FAISS_INDEX_DIR,"index.faiss"))
    st.write(("🟢 " if ready else "🟠 ")+tr("ready" if ready else "not_ready"))
    st.caption(f"{tr('documents')}: {meta.get('document_count',0)}")
    st.caption(f"{tr('chunks')}: {meta.get('chunk_count',0)}")
    st.caption(f"{tr('last_updated')}: {meta.get('last_successful_indexing','—')}")
    st.caption(f"Ollama model: `{settings.OLLAMA_MODEL}`")
    if st.button(tr("clear_chat"),use_container_width=True): st.session_state.messages=[]; st.rerun()
    with st.expander(tr("help")): st.write(tr("help_text"))
    with st.expander("Admin / maintenance"):
        st.warning("Run maintenance separately from normal chat.")
        st.code("python scraper.py\npython build_index.py",language="bash")
        st.caption("Protect maintenance operations with authentication before any shared deployment.")
render_header(st.session_state.ui_language)
tab_chat,tab_explorer=st.tabs([tr("ask_tab"),tr("explorer_tab")])
with tab_chat:
    st.subheader(tr("ask_heading")); st.write(tr("intro"))
    suggestions=[("machinery","What subsidies are available for agricultural machinery?"),("irrigation","What support is available for drip or micro irrigation?"),("insurance","Explain crop insurance schemes for farmers."),("eligibility","How can I check eligibility for an agriculture scheme?"),("documents_needed","What documents are commonly required to apply?"),("application","How do I apply for an agriculture scheme?")]
    cols=st.columns(3)
    for i,(key,q) in enumerate(suggestions):
        if cols[i%3].button(tr(key),key="suggest_"+key,use_container_width=True): st.session_state.selected_question=q; st.rerun()
    for m in st.session_state.messages:
        with st.chat_message(m["role"],avatar="🌾" if m["role"]=="assistant" else "👤"):
            st.markdown(m["content"])
            if m.get("sources"): render_sources(m["sources"],st.session_state.ui_language)
    question=st.chat_input(tr("question_placeholder"))
    if st.session_state.selected_question: question=st.session_state.selected_question; st.session_state.selected_question=""
    if question:
        question=question.strip()
        if not question: st.warning(tr("empty_question"))
        else:
            st.session_state.messages.append({"role":"user","content":question})
            with st.chat_message("user",avatar="👤"): st.markdown(question)
            with st.chat_message("assistant",avatar="🌾"):
                with st.spinner(tr("thinking")):
                    try:
                        db=load_vector_store()
                        if db is None: answer=tr("index_missing"); sources=[]
                        else:
                            result=answer_question(db,question,st.session_state.ui_language); answer=result["answer"]; sources=result["sources"]
                        st.markdown(answer)
                        if sources: render_sources(sources,st.session_state.ui_language)
                        st.session_state.messages.append({"role":"assistant","content":answer,"sources":sources})
                    except Exception as exc:
                        msg=tr("ollama_error") if "ollama" in str(exc).lower() or "connection" in str(exc).lower() else tr("general_error")
                        st.error(msg); st.caption("Check README.md → Troubleshooting. Detail: "+str(exc)[:200])
                        st.session_state.messages.append({"role":"assistant","content":msg,"sources":[]})
with tab_explorer:
    st.subheader(tr("explorer_heading")); render_scheme_explorer(docs,st.session_state.ui_language)
