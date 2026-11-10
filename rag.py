
import chromadb
import numpy as np

from sentence_transformers import SentenceTransformer
from google import genai

from config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    GEMINI_API_KEY,
    LLM_MODEL,
    TOP_K
)

# Initialize embedding model
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

# Initialize Gemini
if GEMINI_API_KEY:
    gemini_client = genai.Client(
        api_key=GEMINI_API_KEY
    )
else:
    gemini_client = None


def get_collection():
    return collection


def get_embedding_model():
    return embedding_model


def retrieve_documents(question, top_k=TOP_K):

    if collection.count() == 0:
        return []

    question_embedding = embedding_model.encode(
        question,
        normalize_embeddings=True
    )

    results = collection.query(
        query_embeddings=[
            question_embedding.tolist()
        ],
        n_results=min(top_k, collection.count()),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    retrieved = []

    for i, document in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][i]

        retrieved.append({
            "content": document,
            "source": metadata.get("source", "Unknown"),
            "distance": results["distances"][0][i]
        })

    return retrieved


def generate_answer(question, context=""):

    if gemini_client is None:
        raise ValueError(
            "Gemini API key is missing. Configure your .env file."
        )

    if context:
        prompt = f"""
You are a helpful AI document assistant.

Answer the question using ONLY the information
provided in the document context.

If the answer is not available in the context,
clearly say that the information was not found
in the uploaded documents.

Do not invent information.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""
    else:
        prompt = f"""
You are a general AI assistant.

Answer the following question using your
general knowledge without accessing any
uploaded documents.

If you do not know the answer, say so.

QUESTION:
{question}

ANSWER:
"""

    response = gemini_client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt
    )

    return response.text


def answer_question(question, use_rag=True):

    if not use_rag:

        answer = generate_answer(question)

        return {
            "answer": answer,
            "sources": [],
            "retrieved_chunks": []
        }

    retrieved_docs = retrieve_documents(question)

    if not retrieved_docs:
        return {
            "answer": "No documents found. Please upload and ingest a PDF first.",
            "sources": [],
            "retrieved_chunks": []
        }

    context = "\n\n".join(
        [
            f"Source: {doc['source']}\n{doc['content']}"
            for doc in retrieved_docs
        ]
    )

    answer = generate_answer(
        question,
        context
    )

    sources = list(
        dict.fromkeys(
            doc["source"] for doc in retrieved_docs
        )
    )

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_docs
    }
