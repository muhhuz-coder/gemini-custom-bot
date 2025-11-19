import streamlit as st
import os
import json
import uuid
import google.generativeai as genai
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Gemini Research Papers Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'store_id' not in st.session_state:
    st.session_state.store_id = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'files_loaded' not in st.session_state:
    st.session_state.files_loaded = False

def create_document_store(api_key, uploaded_files):
    """Create a document store from uploaded files"""
    try:
        genai.configure(api_key=api_key)

        # Create papers directory if it doesn't exist
        papers_dir = Path("papers")
        papers_dir.mkdir(exist_ok=True)

        # Save uploaded files
        file_paths = []
        for uploaded_file in uploaded_files:
            file_path = papers_dir / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_paths.append(str(file_path))

        # Upload files to Gemini
        uploaded_files_gemini = []
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, file_path in enumerate(file_paths):
            status_text.text(f"Uploading {Path(file_path).name}...")
            file_obj = genai.upload_file(file_path)
            uploaded_files_gemini.append(file_obj)
            progress_bar.progress((i + 1) / len(file_paths))

        progress_bar.empty()
        status_text.empty()

        # Create store data
        store_id = str(uuid.uuid4())
        store_data = {
            "id": store_id,
            "name": "Research Papers Collection",
            "files": [f.name for f in uploaded_files_gemini]
        }

        # Save to JSON file
        store_file = f"{store_id}.json"
        with open(store_file, "w") as f:
            json.dump(store_data, f)

        return store_id, len(uploaded_files_gemini)

    except Exception as e:
        st.error(f"Error creating document store: {str(e)}")
        return None, 0

def load_document_store(store_id):
    """Load files from an existing store"""
    try:
        store_file = f"{store_id}.json"
        with open(store_file, "r") as f:
            store_data = json.load(f)

        genai.configure(api_key=st.session_state.api_key)
        files = []
        for file_name in store_data["files"]:
            try:
                file_obj = genai.get_file(file_name)
                files.append(file_obj)
            except Exception as e:
                st.warning(f"Could not load file {file_name}: {str(e)}")

        return files
    except Exception as e:
        st.error(f"Error loading document store: {str(e)}")
        return []

def chat_with_documents(question, files, history):
    """Chat with documents using Gemini"""
    try:
        model = genai.GenerativeModel("gemini-pro")

        # Build context from history
        system_prompt = "You are a helpful Q&A assistant for research papers. Answer questions based on the provided documents. Include citations to specific sources when possible."

        if history:
            context = "\n".join([f"User: {h['question']}\nAssistant: {h['answer']}" for h in history[-3:]])
            full_prompt = f"{system_prompt}\n\nPrevious conversation:\n{context}\n\nCurrent question: {question}"
        else:
            full_prompt = f"{system_prompt}\n\nQuestion: {question}"

        # Generate response
        response = model.generate_content([full_prompt] + files)

        # Extract citations
        citations = []
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'grounding_attributions'):
                for attr in candidate.grounding_attributions:
                    if hasattr(attr, 'title') and attr.title:
                        citations.append(attr.title)
                    elif hasattr(attr, 'uri') and attr.uri:
                        source = attr.uri.split('/')[-1]
                        citations.append(source)

        citation_text = f"\n\n📚 **Sources:** {', '.join(set(citations))}" if citations else ""

        return response.text + citation_text

    except Exception as e:
        return f"Error: {str(e)}"

# Main UI
st.title("🤖 Gemini Research Papers Chatbot")
st.markdown("Upload your research papers and ask questions about them!")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # API Key input
    api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        help="Get your API key from https://aistudio.google.com/"
    )

    if api_key:
        st.session_state.api_key = api_key
        st.success("✅ API Key configured")
    else:
        st.warning("⚠️ Please enter your API key")

    st.divider()

    # Document upload section
    st.header("📄 Document Management")

    # Option to upload new documents or load existing store
    upload_option = st.radio(
        "Choose option:",
        ["Upload New Documents", "Load Existing Store"],
        help="Upload new PDFs or load a previously created document store"
    )

    if upload_option == "Upload New Documents":
        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True,
            help="Select one or more PDF research papers"
        )

        if uploaded_files and api_key:
            if st.button("🚀 Create Document Store", type="primary"):
                with st.spinner("Creating document store..."):
                    store_id, num_files = create_document_store(api_key, uploaded_files)

                if store_id:
                    st.session_state.store_id = store_id
                    st.session_state.files_loaded = True
                    st.success(f"✅ Document store created with {num_files} files!")
                    st.info(f"Store ID: `{store_id}`")
                    st.rerun()

    else:  # Load Existing Store
        store_id_input = st.text_input(
            "Store ID",
            help="Enter the Store ID from a previously created document store"
        )

        if store_id_input and api_key:
            if st.button("📂 Load Document Store"):
                with st.spinner("Loading document store..."):
                    files = load_document_store(store_id_input)

                if files:
                    st.session_state.store_id = store_id_input
                    st.session_state.files_loaded = True
                    st.success(f"✅ Loaded document store with {len(files)} files!")
                    st.rerun()
                else:
                    st.error("❌ Could not load the document store")

    # Clear data button
    if st.button("🗑️ Clear All Data"):
        st.session_state.store_id = None
        st.session_state.chat_history = []
        st.session_state.files_loaded = False
        st.success("✅ All data cleared!")
        st.rerun()

# Main chat interface
if st.session_state.files_loaded and st.session_state.api_key:
    st.header("💬 Chat with Your Documents")

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(message["question"])
            with st.chat_message("assistant"):
                st.write(message["answer"])

    # Chat input
    if question := st.chat_input("Ask a question about your research papers..."):
        # Load files for chat
        files = load_document_store(st.session_state.store_id)

        if files:
            # Add user question to history
            st.session_state.chat_history.append({"question": question, "answer": ""})

            # Display user question
            with chat_container:
                with st.chat_message("user"):
                    st.write(question)

            # Generate and display response
            with chat_container:
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        answer = chat_with_documents(question, files, st.session_state.chat_history[:-1])
                    st.write(answer)

            # Update history with answer
            st.session_state.chat_history[-1]["answer"] = answer
        else:
            st.error("❌ Could not load documents for chat")

else:
    if not st.session_state.api_key:
        st.info("👆 Please enter your API key in the sidebar to get started.")
    elif not st.session_state.files_loaded:
        st.info("📄 Upload documents or load an existing store from the sidebar to start chatting.")

# Footer
st.divider()
st.markdown("""
**Gemini Research Papers Chatbot** - Powered by Google Gemini AI

*Upload your research papers, create a searchable knowledge base, and get AI-powered answers with automatic citations.*
""")

# Hide Streamlit branding
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)