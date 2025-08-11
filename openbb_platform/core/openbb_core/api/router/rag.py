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

    return docs


@router.post("/ingest")
def ingest() -> dict:

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
    	dict: A dictionary with the concatenated answer from the top three relevant documents and the total number of retrieved source documents.
    """
    retriever = vector_db.as_retriever()
    results = retriever.get_relevant_documents(q.question)
    answer = " ".join(r.page_content for r in results[:3])
    return {"answer": answer, "sources": len(results)}
