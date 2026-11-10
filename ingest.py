
import hashlib
from pathlib import Path

from pypdf import PdfReader

from config import (
    DOCUMENTS_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

from rag import get_collection, get_embedding_model


def extract_text(pdf_path):

    reader = PdfReader(str(pdf_path))

    all_text = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        if text.strip():
            all_text.append(
                f"[Page {page_number}]\n{text}"
            )

    return "\n".join(all_text), len(reader.pages)


def split_into_chunks(text):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + CHUNK_SIZE

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def ingest_pdf(pdf_path):

    pdf_path = Path(pdf_path)

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    text, page_count = extract_text(pdf_path)

    if not text.strip():
        raise ValueError(
            "No readable text found in this PDF. "
            "Scanned PDFs may require OCR."
        )

    chunks = split_into_chunks(text)

    if not chunks:
        raise ValueError("No document chunks were created.")

    collection = get_collection()
    model = get_embedding_model()

    # Generate embeddings
    embeddings = model.encode(
        chunks,
        normalize_embeddings=True
    )

    # Create unique document IDs
    file_hash = hashlib.sha256(
        pdf_path.read_bytes()
    ).hexdigest()[:16]

    ids = [
        f"{file_hash}_{i}"
        for i in range(len(chunks))
    ]

    metadata = [
        {
            "source": pdf_path.name,
            "chunk_index": i,
            "page_count": page_count
        }
        for i in range(len(chunks))
    ]

    # Remove previous version of the same filename
    collection.delete(
        where={"source": pdf_path.name}
    )

    # Store chunks and embeddings
    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadata
    )

    return {
        "filename": pdf_path.name,
        "pages": page_count,
        "chunks": len(chunks),
        "message": "Document successfully indexed!"
    }


def ingest_all_pdfs():

    for pdf_path in DOCUMENTS_DIR.glob("*.pdf"):

        try:
            result = ingest_pdf(pdf_path)
            print(result)

        except Exception as error:
            print(f"Error processing {pdf_path.name}: {error}")


if __name__ == "__main__":

    print("Starting document ingestion...")

    ingest_all_pdfs()

    print("Document ingestion completed!")
