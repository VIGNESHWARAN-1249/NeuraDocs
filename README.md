
# DocuMind - AI Document Assistant

## About the Project

DocuMind is a Retrieval-Augmented Generation (RAG)
based document question-answering system.

It allows users to upload PDF documents and ask
questions about their content.

Instead of depending only on the general knowledge
of an AI model, the system retrieves relevant
information from uploaded documents and uses it
to generate context-based answers.

## Features

- PDF document upload
- Text extraction using PyPDF
- Text chunking with overlap
- Semantic embeddings using Sentence Transformers
- Vector storage using ChromaDB
- Similarity-based document retrieval
- AI-generated answers using Gemini
- RAG vs. non-RAG comparison
- Simple web-based chatbot interface

## Technology Stack

Frontend:
- HTML
- CSS
- JavaScript

Backend:
- Python
- Flask

AI and Vector Database:
- Google Gemini API
- Sentence Transformers
- ChromaDB

## Project Architecture

1. User uploads a PDF.
2. Text is extracted from the PDF.
3. Extracted text is divided into chunks.
4. Each chunk is converted into an embedding.
5. Embeddings are stored in ChromaDB.
6. User enters a question.
7. The question is converted into an embedding.
8. ChromaDB retrieves the most relevant chunks.
9. Retrieved chunks are added to the Gemini prompt.
10. Gemini generates an answer based on the context.

## Installation

Clone the repository:

git clone YOUR_GITHUB_REPOSITORY_URL

Navigate to the project:

cd DocuMind

Create a virtual environment:

python -m venv venv

Activate the environment on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

## API Configuration

Create a .env file in the root directory.

Add your Gemini API key:

GEMINI_API_KEY=your_api_key_here

## Run the Application

Start the application:

python app.py

Open the browser:

http://127.0.0.1:5000

Upload a PDF and start asking questions.

## Document Requirements

Use real PDF documents containing at least
10-20 pages of meaningful content.

The system uses approximately 500 words per chunk
with an overlap of 80 words.

## RAG vs Without RAG Comparison

Question:
[Insert a question that can only be answered
using your uploaded document.]

### Without RAG

[Insert the actual response without retrieval.]

### With RAG

[Insert the actual response using retrieved
document chunks.]

### Observation

The normal LLM response does not have access to
the uploaded document.

The RAG system retrieves relevant information
from ChromaDB and uses that information to
generate a grounded answer.

## Future Improvements

- Support multiple document formats.
- Add conversation history.
- Display page-level citations.
- Improve document retrieval.
- Support multiple users.

## Author

VIGNESHWARAN V.
Computer Science and Engineering
