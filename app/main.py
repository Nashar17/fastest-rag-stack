import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config import settings
from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.text_chunker import TextChunker
from app.ingestion.embedding_generator import EmbeddingGenerator
from app.retrieval.vector_store import VectorStore
from app.retrieval.retriever import Retriever
from app.generation.llm_generator import LLMGenerator


class Application:
    """
    Main Application class responsible for initializing FastAPI
    and configuring routes.
    """

    def __init__(self):
        self.app = FastAPI(title="Fastest RAG Stack API")
        self._register_routes()

    def _register_routes(self):

        # ── Health ────────────────────────────────────────────────
        @self.app.get("/", tags=["Health"])
        def health_check():
            return {
                "status": "OK",
                "message": "Fastest RAG Stack is running!",
            }

        # ── Ingestion ─────────────────────────────────────────────
        @self.app.post("/ingest", tags=["Ingestion"])
        async def ingest():
            """
            Load PDFs → chunk → embed → store in vector DB.
            Call this once before querying.
            """
            try:
                loader = PDFLoader("data/pdfs")
                docs = loader.extract_text()

                chunker = TextChunker()
                chunks = chunker.chunk_documents(docs)

                embedder = EmbeddingGenerator()
                embedded_chunks = embedder.generate_embeddings(chunks)

                vector_store = VectorStore()
                vector_store.add_embeddings(embedded_chunks)

                return {
                    "status": "Ingestion complete",
                    "documents_loaded": len(docs),
                    "chunks_created": len(chunks),
                    "embeddings_stored": len(embedded_chunks),
                    "sample_embedding_dimension": len(embedded_chunks[0]["embedding"]),
                }

            except Exception as e:
                traceback.print_exc()
                return JSONResponse(status_code=500, content={"error": str(e)})

        # ── Retrieval ─────────────────────────────────────────────
        @self.app.get("/retrieve", tags=["Retrieval"])
        async def retrieve(query: str, k: int = 3):
            """
            Retrieve the top k relevant chunks for a query.
            """
            try:
                retriever = Retriever()
                retrieved_chunks = retriever.retrieve(query=query, k=k)

                return {
                    "query": query,
                    "retrieved_chunks": retrieved_chunks,
                }

            except Exception as e:
                traceback.print_exc()
                return JSONResponse(status_code=500, content={"error": str(e)})

        # ── Generation ────────────────────────────────────────────
        @self.app.get("/ask", tags=["Generation"])
        async def ask(query: str, k: int = 3):
            """
            Full RAG pipeline: retrieve relevant chunks + generate answer.
            """
            try:
                retriever = Retriever()
                retrieved_chunks = retriever.retrieve(query=query, k=k)

                generator = LLMGenerator()
                answer = generator.generate_answer(
                    query=query,
                    retrieved_chunks=retrieved_chunks
                )

                return {
                    "query": query,
                    "answer": answer,
                    "retrieved_chunks": retrieved_chunks,
                }

            except Exception as e:
                traceback.print_exc()
                return JSONResponse(status_code=500, content={"error": str(e)})


# Create application instance
application = Application()
app = application.app