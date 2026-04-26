import ollama
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

print("Loading embedding model...")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://172.23.32.1:11434"
)

print("Opening database...")

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

query = input("Enter topic: ")

print("Searching chunks...")

docs = db.similarity_search(query, k=3)

print("Retrieved", len(docs), "chunks")

context = "\n".join([d.page_content for d in docs])

print("Connecting to Ollama...")

client = ollama.Client(host="http://172.23.32.1:11434")

prompt = f"""
You are an exam setter.

Using ONLY the context below, generate 10 MCQs.

Rules:
- 4 options
- no duplicates
- medium difficulty
- include correct answer

Context:
{context}
"""

print("Generating now...\n")

stream = client.chat(
    model="gemma4:e4b",
    messages=[{"role":"user","content":prompt}],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)