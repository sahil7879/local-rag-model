from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv 
load_dotenv()
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
    base_url=os.getenv("OLLAMA_HOST")
)

db = Chroma.from_texts(
    texts=chunks,
    embedding=embeddings,
    persist_directory=os.getenv("DB_PATH")
)

print("✅ Vector DB Ready")