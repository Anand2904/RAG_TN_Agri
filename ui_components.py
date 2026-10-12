import streamlit as st
from translations import T
def inject_css():
 st.markdown("""<style>:root{--green:#174A35;--leaf:#DDEFE2;--cream:#F7FAF6;--ink:#26352D}.stApp{background:var(--cream);color:var(--ink)}[data-testid="stSidebar"]{background:#EDF5EE;border-right:1px solid #D3E2D6}.hero{background:linear-gradient(110deg,#174A35,#286849);color:white;padding:1.4rem 1.5rem;border-radius:18px;margin-bottom:1rem;box-shadow:0 4px 18px #174a3518}.hero h1{font-size:clamp(1.35rem,3vw,2rem);margin:0 0 .4rem;color:white}.hero p{margin:.25rem 0;color:#F1FAF3}div.stButton>button{border-radius:10px;border:1px solid #C8DDCE;background:white;color:#174A35;min-height:2.6rem}div.stButton>button:hover{border-color:#2D8054;background:#E7F4EA;color:#123C2B}[data-testid="stChatMessage"]{border:1px solid #E1E9E2;border-radius:14px;padding:.5rem}a{color:#176B43!important}@media(max-width:700px){.hero{padding:1rem;border-radius:12px}}</style>""",unsafe_allow_html=True)
def render_header(lang):
 subtitle="Trusted information from locally indexed government sources" if lang=="en" else "உள்ளூரில் குறியிடப்பட்ட அரசு ஆதாரங்களிலிருந்து தகவல்கள்"
 st.markdown(f'<div class="hero"><h1>🌾 Tamil Nadu Agriculture Schemes Assistant</h1><p>தமிழ்நாடு வேளாண்மைத் திட்டங்கள் உதவியாளர்</p><p>{subtitle}</p></div>',unsafe_allow_html=True)
def render_sources(sources,lang="en"):
 tr=T.get(lang,T["en"])
 with st.expander(f"🔎 {tr['source']} ({len(sources)})"):
  for i,s in enumerate(sources,1):
   st.markdown(f"**{i}. {s.get('title') or 'Government document'}**")
   if s.get('department'): st.caption(s['department'])
   if s.get('url'): st.markdown(f"[{tr['open_source']}]({s['url']})")
   if s.get('updated'): st.caption("Document date: "+s['updated'])
   if s.get('excerpt'): st.write(s['excerpt'][:600])
   st.divider()
def render_scheme_explorer(documents,lang):
 tr=T.get(lang,T["en"])
 if not documents: st.info(tr['no_docs']); return
 levels=sorted({d.get('government_level','Unknown') for d in documents}); cats=sorted({d.get('category','Other') for d in documents}); depts=sorted({d.get('department','Unknown') for d in documents}); types=sorted({d.get('document_type','Web page') for d in documents})
 c1,c2=st.columns(2); level=c1.selectbox(tr['level'],[tr['all']]+levels); category=c2.selectbox(tr['category'],[tr['all']]+cats)
 c3,c4=st.columns(2); dept=c3.selectbox(tr['department'],[tr['all']]+depts); dtype=c4.selectbox(tr['doctype'],[tr['all']]+types); query=st.text_input("Search title or scheme")
 filtered=[]
 for d in documents:
  if level!=tr['all'] and d.get('government_level')!=level: continue
  if category!=tr['all'] and d.get('category')!=category: continue
  if dept!=tr['all'] and d.get('department')!=dept: continue
  if dtype!=tr['all'] and d.get('document_type')!=dtype: continue
  if query and query.lower() not in (d.get('title','')+' '+d.get('scheme_name','')).lower(): continue
  filtered.append(d)
 st.caption(f"{len(filtered)} documents")
 for d in filtered[:100]:
  with st.container(border=True):
   st.markdown('**'+(d.get('title') or d.get('scheme_name') or 'Untitled document')+'**')
   st.caption(' · '.join(x for x in [d.get('government_level'),d.get('category'),d.get('department')] if x))
   if d.get('url'): st.markdown(f"[Open source]({d['url']})")
   if d.get('summary'): st.write(d['summary'][:300])
