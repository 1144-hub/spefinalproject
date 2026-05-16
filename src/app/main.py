import streamlit as st
import os
import sys
import logging
import time
import json

# Ensure the src module is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.retrieval.vector_store import TelecomVectorStore
from src.retrieval.hybrid_search import TelecomHybridRetriever
from src.llm.qa_engine import ProceduralQAEngine
from llama_index.core.memory import ChatMemoryBuffer

# ---------------------------------------------------------------------------
# Structured JSON Logging (for ELK Stack ingestion via Filebeat/Logstash)
# ---------------------------------------------------------------------------
logger = logging.getLogger("netrestore")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '{"timestamp":"%(asctime)s","level":"%(levelname)s","module":"%(name)s","message":%(message)s}'
    ))
    logger.addHandler(handler)

# Configure the Streamlit page
st.set_page_config(
    page_title="NetRestore",
    page_icon="📡",
    layout="wide",
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 3rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        text-align: center;
        margin-top: 1rem;
        line-height: 1.6;
    }
    
    .header-icon {
        font-size: 4rem;
        text-align: center;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #ffffff;
    }
    
    .sidebar-title {
        color: #667eea;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Chat Message Styling */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        outline: none;
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #f1f5f9;
        border-radius: 8px;
        padding: 0.75rem;
        font-weight: 600;
        color: #475569;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background-color: #dcfce7;
        border-left: 4px solid #22c55e;
        padding: 1rem;
        border-radius: 8px;
    }
    
    .stError {
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
    }
    
    .stWarning {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
    }
    
    /* Info Messages */
    .stInfo {
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
    }
    
    /* Footer Styling */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 3rem;
        border-top: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize the QA Engine once and store it in session state
@st.cache_resource
def load_qa_engine(api_key: str = None):
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "chroma_db"))
    if not os.path.exists(db_path):
        return None
    
    # We must set the Env variable here immediately so LlamaIndex picks it up during initialization
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
        
    vs_manager = TelecomVectorStore(db_path=db_path)
    retriever = TelecomHybridRetriever(vector_store_manager=vs_manager, similarity_top_k=10)
    return ProceduralQAEngine(retriever_pipeline=retriever)

# Header Information
st.markdown("""
<div class="header-container">
    <div class="header-icon">📡</div>
    <h1 class="header-title">NetRestore: Procedural QA RAG for Network Fault Restoration</h1>
    <p class="header-subtitle">
        A RAG-based system designed for network fault restoration operations by retrieving precise restoration SOPs for outages, faults, and incidents using hybrid search and LLM reasoning, enabling faster and more reliable service recovery.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# API Key Configuration: Prioritize Environment Variables for Automation
# ---------------------------------------------------------------------------
if "GROQ_API_KEY" in os.environ:
    st.session_state.api_key = os.environ["GROQ_API_KEY"]
elif "api_key" not in st.session_state:
    # Sidebar input for API Key if not found in env
    api_key = st.sidebar.text_input("Groq API Key (Free)", type="password")
    if not api_key:
        st.warning("Please enter your Groq API Key (from console.groq.com) in the sidebar to use the free LLM.")
        st.stop()
    else:
        st.session_state.api_key = api_key
        os.environ["GROQ_API_KEY"] = api_key

# Load Engine dynamically AFTER key is set
qa_engine = load_qa_engine(st.session_state.get("api_key", os.environ.get("GROQ_API_KEY")))

if not qa_engine:
    st.error("Vector Database not found! Please run the Phase 2/3 test scripts first to index the documents.")
    st.stop()

# ---------------------------------------------------------------------------
# Initialize Chat Memory (persists across Streamlit re-runs within a session)
# ---------------------------------------------------------------------------
if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = ChatMemoryBuffer.from_defaults(token_limit=3072)

# Inject session-specific memory into the engine for conversational continuity
qa_engine.set_memory(st.session_state.chat_memory)

st.divider()

# Sidebar for explicit Metadata Filtering (Mimicking Hybrid Keyword Search)
st.sidebar.markdown('<h2 class="sidebar-title">⚙️ Configuration</h2>', unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown('<h3 class="sidebar-title">🔍 Pre-Filtering</h3>', unsafe_allow_html=True)
st.sidebar.markdown("Use these filters to ensure exact error codes are retrieved via Metadata Filtering, solving the issue of pure vector search missing specific model numbers.")
vendor_filter = st.sidebar.selectbox(
    "Equipment Vendor", 
    ["Any", "Nokia", "Cisco", "Juniper", "Ericsson", "Huawei"],
    label_visibility="visible"
)
VENDOR_ALARM_HINTS = {
    "Cisco":    "Cisco codes: 301–302, 1000–1099",
    "Nokia":    "Nokia codes: 404, 501, 1100–1199",
    "Ericsson": "Ericsson codes: 701–702, 1300–1399",
    "Juniper":  "Juniper codes: 601–602, 1200–1299",
    "Huawei":   "Huawei codes: 801–802, 1400–1499",
    "Any":      "e.g. 301, 404, 601, 701, 801, 1000",
}
alarm_hint = VENDOR_ALARM_HINTS.get(vendor_filter, "e.g. 1000, 1101, 1201")
alarm_filter = st.sidebar.text_input(f"Exact Alarm Code ({alarm_hint})", value="", help="Enter the exact alarm code for precise filtering")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add a clear chat button to the sidebar
st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
    st.session_state.messages = []
    st.session_state.chat_memory = ChatMemoryBuffer.from_defaults(token_limit=3072)
    qa_engine.set_memory(st.session_state.chat_memory)
    logger.info(json.dumps({"event": "chat_cleared"}))
    st.rerun()

# Display chat history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📄 Show Retrieved Context (For Academic Evaluation)", expanded=False):
                for idx, source in enumerate(message["sources"], 1):
                    st.markdown(f"### Source {idx}")
                    st.markdown(f"**Document:** `{source['file_name']}`  \n**Section Header:** `{source['header']}`  \n**Confidence Score:** `{source['score']:.2f}`")
                    st.text(source['text'])
                    if idx < len(message["sources"]):
                        st.markdown("---")

# React to user input
if prompt := st.chat_input("Ask a procedural question (e.g., 'How to clear ALARM_CODE_404 on router XYZ?'): "):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare filters
    filters = {}
    if vendor_filter != "Any":
        filters["equipment_vendor"] = vendor_filter
    if alarm_filter.strip():
        filters["alarm_code"] = alarm_filter.strip()
        
    # Query Engine with timing for structured logging
    with st.chat_message("assistant"):
        with st.spinner("Retrieving SOPs and Synthesizing Answer (with Chain-of-Thought)..."):
            try:
                start_time = time.time()
                response = qa_engine.query(prompt, filters=filters if filters else None)
                latency = time.time() - start_time
                
                # Get response text (ContextChatEngine returns AgentChatResponse)
                response_text = str(response)
                
                # --- Zero-results guard ---
                # For the first question, we REQUIRE retrieved sources.
                # For follow-ups, we allow the LLM to answer from existing chat memory.
                is_follow_up = len(st.session_state.messages) > 1
                num_sources = len(response.source_nodes) if hasattr(response, 'source_nodes') and response.source_nodes else 0
                
                if (num_sources == 0 and not is_follow_up) or not response_text.strip():
                    parts = []
                    if alarm_filter.strip():
                        parts.append(f"alarm code **{alarm_filter.strip()}**")
                    if vendor_filter != "Any":
                        parts.append(f"vendor **{vendor_filter}**")
                    detail = " for " + " and ".join(parts) if parts else ""
                    response_text = (
                        f"⚠️ No matching SOP documents found{detail}.\n\n"
                        f"**Possible reasons:**\n"
                        f"- The alarm code may not exist in the {vendor_filter} dataset\n"
                        f"- Try a 4-digit code (e.g. `1101`, `1201`, `1301`) instead\n"
                        f"- Clear the alarm code filter and search by description only"
                    )
                
                st.markdown(response_text)
                
                # Structured logging for ELK ingestion
                logger.info(json.dumps({
                    "event": "query_executed",
                    "query": prompt,
                    "vendor_filter": vendor_filter,
                    "alarm_filter": alarm_filter,
                    "latency_seconds": round(latency, 3),
                    "num_sources": len(response.source_nodes) if hasattr(response, 'source_nodes') and response.source_nodes else 0,
                    "status": "success"
                }))
                
                # Extract Sources explicitly for grading
                source_data = []
                if hasattr(response, 'source_nodes') and response.source_nodes:
                    with st.expander("📄 Show Retrieved Context (For Academic Evaluation)", expanded=False):
                        for idx, node in enumerate(response.source_nodes, 1):
                            file_name = node.node.metadata.get('file_name', 'Unknown')
                            header = node.node.metadata.get('header_path', 'No Header')
                            source_text = node.node.get_content()
                            score = node.score if node.score is not None else 0.0
                            
                            st.markdown(f"### Source {idx}")
                            st.markdown(f"**Document:** `{file_name}`  \n**Section Header:** `{header}`  \n**Confidence Score:** `{score:.2f}`")
                            st.text(source_text[:500] + "...\n[TRUNCATED]")
                            if idx < len(response.source_nodes):
                                st.markdown("---")
                            
                            source_data.append({
                                "file_name": file_name,
                                "header": header,
                                "score": score,
                                "text": source_text[:500] + "...\n[TRUNCATED]"
                            })
                            
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response_text, "sources": source_data})
                
            except Exception as e:
                latency = time.time() - start_time
                error_msg = f"**Error:** Failed to generate response. Please check your Groq API Key.\n\n`{str(e)}`"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
                # Log the error for ELK
                logger.error(json.dumps({
                    "event": "query_failed",
                    "query": prompt,
                    "vendor_filter": vendor_filter,
                    "alarm_filter": alarm_filter,
                    "latency_seconds": round(latency, 3),
                    "error": str(e),
                    "status": "error"
                }))

