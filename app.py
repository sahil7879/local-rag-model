import streamlit as st
import ollama
import fitz
import io
import os
import pytesseract

from PIL import Image
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Local RAG Assistant", layout="wide")

OLLAMA_HOST = "http://172.23.32.1:11434"
DB_PATH = "chroma_db"
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# --------------------------------------------------
# SIDEBAR SETTINGS
# --------------------------------------------------
st.sidebar.title("⚙️ Controls")

model = st.sidebar.selectbox(
    "Choose Model",
    ["gemma4:e4b", "qwen3.5:9b"]
)

k_value = st.sidebar.slider(
    "Retrieved Chunks",
    1, 5, 2
)

mode = st.sidebar.selectbox(
    "Mode",
    [
        "General",
        "MCQ Generator",
        "Summarizer",
        "Interview Prep"
    ]
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("🧠 Local RAG Assistant")
st.caption("Upload PDFs/PPTs • Ask Questions • Generate MCQs")

# --------------------------------------------------
# EMBEDDINGS + DB
# --------------------------------------------------
@st.cache_resource
def get_embeddings():
    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=OLLAMA_HOST
    )

@st.cache_resource
def load_db():
    embeddings = get_embeddings()

    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

db = load_db()

# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def save_uploaded_file(uploaded_file):
    filepath = os.path.join(
        UPLOAD_DIR,
        uploaded_file.name
    )

    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return filepath


def extract_pdf(filepath):
    text = ""

    doc = fitz.open(filepath)

    for page in doc:
        # page text
        text += page.get_text()

        # OCR images inside page
        for img in page.get_images(full=True):
            xref = img[0]
            base = doc.extract_image(xref)
            image_bytes = base["image"]

            image = Image.open(
                io.BytesIO(image_bytes)
            )

            ocr_text = pytesseract.image_to_string(
                image
            )

            text += "\n" + ocr_text + "\n"

    return text


def add_to_vector_db(raw_text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_text(raw_text)

    chunks = [
        c.strip()
        for c in chunks
        if c.strip()
    ]

    if chunks:
        db.add_texts(chunks)


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------
st.sidebar.header("📄 Upload Files")

uploaded = st.sidebar.file_uploader(
    "Upload PDF / PPTX",
    type=["pdf", "pptx"]
)

if uploaded:
    filepath = save_uploaded_file(uploaded)

    st.sidebar.info(
        f"Saved: {uploaded.name}"
    )

    # PDF handling
    if uploaded.name.lower().endswith(".pdf"):
        with st.spinner("Processing PDF..."):
            text = extract_pdf(filepath)
            add_to_vector_db(text)

        st.sidebar.success(
            "PDF Added to Knowledge Base!"
        )

    # PPTX placeholder
    elif uploaded.name.lower().endswith(".pptx"):
        st.sidebar.warning(
            "PPTX support coming next."
        )

# --------------------------------------------------
# SHOW SAVED FILES
# --------------------------------------------------
st.sidebar.header("📚 Uploaded Files")

files = os.listdir(UPLOAD_DIR)

if files:
    for f in files:
        st.sidebar.write("• " + f)
else:
    st.sidebar.caption("No files uploaded yet.")

# --------------------------------------------------
# CHAT MEMORY
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input(
    "Ask anything from your uploaded files..."
)

# --------------------------------------------------
# CHAT FLOW
# --------------------------------------------------
if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Retrieve docs
    docs = db.similarity_search(
        prompt,
        k=k_value
    )

    context = "\n\n".join(
        [d.page_content for d in docs]
    )

    # Modes
    if mode == "MCQ Generator":
        instruction = """
Generate MCQs using the context.
Include answers.
"""
    elif mode == "Summarizer":
        instruction = """
Summarize clearly and simply.
"""
    elif mode == "Interview Prep":
        instruction = """
Create interview questions with answers.
"""
    else:
        instruction = """
Answer accurately using context.
"""

    final_prompt = f"""
{instruction}

User Question:
{prompt}

Relevant Context:
{context}
"""

    client = ollama.Client(
        host=OLLAMA_HOST
    )

    with st.chat_message("assistant"):
        response_box = st.empty()
        full_response = ""

        stream = client.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],
            stream=True
        )

        for chunk in stream:
            token = chunk["message"]["content"]
            full_response += token
            response_box.markdown(
                full_response
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )