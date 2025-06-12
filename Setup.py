import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions

def initialize_chroma_db(path="rag_db"):
    chroma_client = chromadb.PersistentClient(path=path)
    return chroma_client

def load_documents(folder_path):
    documents = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        with open(file_path, "r", encoding="utf-8") as f:
            documents.append((file, f.read()))
    return documents

def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def embed_and_store_documents(chroma_client, documents):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    collection = chroma_client.get_or_create_collection("rag_docs")

    for doc_id, (filename, content) in enumerate(documents):
        chunks = chunk_text(content)
        embeddings = model.encode(chunks).tolist()
        ids = [f"{filename}_{i}" for i in range(len(chunks))]
        collection.add(documents=chunks, embeddings=embeddings, ids=ids)

    return "Documents embedded and stored successfully."
