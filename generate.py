import ollama
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv 
load_dotenv()
print("Loading embedding model...")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url=os.getenv("OLLAMA_HOST")
)

print("Opening database...")

db = Chroma(
    persist_directory=os.getenv("DB_PATH"),
    embedding_function=embeddings
)

query = input("Enter topic: ")

print("Searching chunks...")

docs = db.similarity_search(query, k=3)

print("Retrieved", len(docs), "chunks")

context = "\n".join([d.page_content for d in docs])

print("Connecting to Ollama...")

client = ollama.Client(host=os.getenv("OLLAMA_HOST"))

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
    model=os.getenv("CHAT_MODEL"),
    messages=[{"role":"user","content":prompt}],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)