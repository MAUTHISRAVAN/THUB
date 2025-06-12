import openai
import chromadb
from sentence_transformers import SentenceTransformer

openai.api_key = os.getenv("OPENAI_API_KEY")

def search_relevant_chunks(query, k=3):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_vector = model.encode([query])[0].tolist()

    chroma_client = chromadb.PersistentClient(path="rag_db")
    collection = chroma_client.get_collection("rag_docs")

    results = collection.query(query_embeddings=[query_vector], n_results=k)

    return results['documents'][0], results['ids'][0], results['distances'][0]

def generate_rag_response(query):
    chunks, ids, scores = search_relevant_chunks(query)

    context = "\n".join(chunks)
    prompt = f"""
You are a helpful assistant. Based on the following context, answer the user's question. Be concise and provide references.

Context:
{context}

Question: {query}
Answer:
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message["content"],
        "sources": ids,
        "similarity_scores": scores
    }
