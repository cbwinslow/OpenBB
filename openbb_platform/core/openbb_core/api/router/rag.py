"""RAG knowledge base router."""

from __future__ import annotations

import glob
import os
from typing import List

from fastapi import APIRouter
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from pydantic import BaseModel

router = APIRouter(prefix="/rag", tags=["RAG"])

DB_DIR = os.getenv("RAG_DB", "rag_db")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
vector_db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)


def load_docs(directory: str) -> List[Document]:
    """
    Load all `.txt` files from the specified directory as Document objects.
    
    Parameters:
    	directory (str): Path to the directory containing text files.
    
    Returns:
    	List[Document]: A list of Document objects, each containing the content of a text file.
    """
    docs: List[Document] = []
    for path in glob.glob(os.path.join(directory, "*.txt")):
        with open(path, encoding="utf-8") as f:
            docs.append(Document(page_content=f.read()))
    return docs


@router.post("/ingest")
def ingest() -> dict:
    """
    Loads and ingests text documents from the knowledge base directory into the vector database.
    
    Returns:
        dict: A dictionary containing the number of ingested document chunks under the key "ingested".
    """
    docs = load_docs("knowledge_base/docs")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    if chunks:
        vector_db.add_documents(chunks)
        vector_db.persist()
    return {"ingested": len(chunks)}


class Query(BaseModel):
    question: str


@router.post("/query")
def query_rag(q: Query) -> dict:
    """
    Retrieve relevant information from the knowledge base in response to a user question.
    
    Parameters:
    	q (Query): The query object containing the user's question.
    
    Returns:
    	dict: A dictionary with the generated answer string and the number of source documents retrieved.
    """
    retriever = vector_db.as_retriever()
    results = retriever.get_relevant_documents(q.question)
    answer = " ".join(r.page_content for r in results[:3])
    return {"answer": answer, "sources": len(results)}
