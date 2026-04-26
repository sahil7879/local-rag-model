# 🧠 Local RAG Assistant

A fully local **Retrieval-Augmented Generation (RAG)** chatbot that allows you to upload PDFs, store them as searchable embeddings, and chat with your own documents using local LLMs powered by Ollama.

This project is designed to run **completely offline / locally** using your own hardware.

---

# 🚀 What This Project Does

This application combines:

* **Streamlit** → ChatGPT-style web interface
* **Ollama** → Runs local AI models
* **ChromaDB** → Stores embeddings (vector database)
* **LangChain** → Retrieval pipeline integrations
* **PyMuPDF + OCR** → Reads text + images inside PDFs

You can:

✅ Upload PDFs
✅ Store uploaded files permanently
✅ Ask questions from uploaded notes
✅ Generate MCQs
✅ Summarize chapters
✅ Create interview questions
✅ Run everything locally

---

# 🏗 How It Works

```text
Upload PDF
   ↓
Extract Text + OCR Images
   ↓
Split into Chunks
   ↓
Create Embeddings
   ↓
Store in ChromaDB
   ↓
Ask Question
   ↓
Retrieve Relevant Chunks
   ↓
Send Prompt + Context to Ollama
   ↓
Get AI Response
```

---

# 📁 Project Structure

```text
mcq-rag/
│── app.py
│── uploads/
│── chroma_db/
│── requirements.txt
│── README.md
```

### Folder Explanation

## `app.py`

Main Streamlit application.

## `uploads/`

Stores all uploaded PDFs permanently.

## `chroma_db/`

Stores vector embeddings and searchable chunks.

---

# 🧰 Tech Stack

| Component   | Tool             |
| ----------- | ---------------- |
| UI          | Streamlit        |
| LLM Runtime | Ollama           |
| Models      | Gemma / Qwen     |
| Embeddings  | nomic-embed-text |
| Vector DB   | ChromaDB         |
| OCR         | Tesseract        |
| PDF Parsing | PyMuPDF          |

---

# 💻 System Requirements

## Minimum

* Windows 10/11
* WSL Ubuntu
* Python 3.10+
* 8 GB RAM

## Recommended

* RTX GPU (4050 or better)
* 16 GB RAM

---

# 🤖 Ollama Models Used

## Fast Generation

```text
gemma4:e4b
```

## Better Quality

```text
qwen3.5:9b
```

## Embedding Model

```text
nomic-embed-text
```

---

# 🛠 Full Setup Guide

# Step 1 — Clone Repository

```bash
git clone https://github.com/yourusername/mcq-rag.git
cd mcq-rag
```

---

# Step 2 — Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Step 3 — Install Python Packages

```bash
pip install -r requirements.txt
```

If no requirements file exists:

```bash
pip install streamlit ollama langchain langchain-chroma langchain-ollama langchain-text-splitters chromadb pymupdf pillow pytesseract
```

---

# Step 4 — Install OCR Engine

Inside Ubuntu WSL:

```bash
sudo apt update
sudo apt install tesseract-ocr -y
```

---

# Step 5 — Install Ollama (Windows)

Download:

[https://ollama.com](https://ollama.com)

Install normally.

---

# Step 6 — Pull Models

Open Windows PowerShell:

```powershell
ollama pull gemma4:e4b
ollama pull qwen3.5:9b
ollama pull nomic-embed-text
```

---

# Step 7 — Start Ollama Server

```powershell
ollama serve
```

Keep it running.

---

# Step 8 — Find Windows Host IP for WSL

In Windows:

```powershell
ipconfig
```

Look for:

```text
vEthernet (WSL)
```

Example:

```text
172.23.32.1
```

Use that IP inside `app.py`

```python
OLLAMA_HOST = "http://172.23.32.1:11434"
```

---

# ▶️ Run Project

Inside WSL:

```bash
source venv/bin/activate
streamlit run app.py
```

---

# 🌐 Open in Browser

```text
http://localhost:8501
```

---

# 📄 Using the App

# Upload Documents

Use sidebar uploader.

Supported:

* PDF

(You can add PPTX later)

---

# Ask Questions

Examples:

```text
Explain Jenkins pipeline
Generate 20 MCQs from uploaded notes
Summarize chapter 4
Create DevOps interview questions
```

---

# 🎯 Available Modes

* General Assistant
* MCQ Generator
* Summarizer
* Interview Prep

---

# 🔒 Privacy

Everything runs locally.

No OpenAI API.
No cloud uploads.
No paid usage.

Your files stay on your machine.

---

# ⚡ Performance Tips

## Faster Responses

Use:

```text
gemma4:e4b
```

## Better Quality

Use:

```text
qwen3.5:9b
```

## If GPU Has 6GB VRAM

Prefer Gemma.

---

# 🧠 Why This Project Is Valuable

This project demonstrates:

* AI Engineering
* RAG Pipelines
* Vector Search
* Local LLM Deployment
* UI Development
* OCR Processing

Useful for:

* Resume projects
* Capstone projects
* Freelance work
* Internal company tools

---

# 🐛 Troubleshooting

# Streamlit Auto Browser Error

If WSL shows:

```text
gio: Operation not supported
```

Ignore it.

Open browser manually:

```text
http://localhost:8501
```

---

# Ollama Connection Failed

Ensure Windows PowerShell has:

```powershell
ollama serve
```

running.

---

# Slow Model Output

Use:

```text
gemma4:e4b
```

instead of heavier models.

---

# Uploaded Files Not Showing

Check:

```bash
ls uploads
```

---

# Future Improvements

* PPTX support
* DOCX export
* Source citations
* Multiple document folders
* Authentication
* Better UI theme
* Deploy on LAN

---

# 👨‍💻 Author

Built as a local open-source AI project using Ollama + Streamlit + ChromaDB.

---

# ⭐ If You Like This Project

Star the repository and keep building.
