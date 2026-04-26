from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

text = open("content.txt", encoding="utf-8").read()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

chunks = splitter.split_text(text)
chunks = [c for c in chunks if c.strip()]

print("Chunks:", len(chunks))

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://172.23.32.1:11434"
)

db = Chroma.from_texts(
    texts=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

print("✅ Vector DB Ready")