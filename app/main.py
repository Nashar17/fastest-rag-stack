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
        @self.app.get("/")
        def health_check():
            return {
                "status": "OK",
                "message": "Fastest RAG Stack is running!",
            }

        @self.app.get("/check-openai")
        def check_openai_key():
            return {
                "openai_key_loaded": bool(settings.openai_api_key)
            }
        
        @self.app.get("/test-pdf-loader")
        async def test_pdf_loader(query: str):
            try:
                loader = PDFLoader("data/pdfs")
                docs = loader.extract_text()

                chunker = TextChunker()
                chunks = chunker.chunk_documents(docs)

                embedder = EmbeddingGenerator()
                embedded_chunks = embedder.generate_embeddings(chunks[:10])  # Only embed the first 10 chunks for testing

                vector_store = VectorStore()
                vector_store.add_embeddings(embedded_chunks)

                retriever = Retriever()

                retrieved_chunks = retriever.retrieve(query=query, k=3)

                generator = LLMGenerator()

                answer = generator.generate_answer(
                    query = query,
                    retrieved_chunks = retrieved_chunks
                )

            except Exception as e:
                traceback.print_exc()
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)}
                )

            return {
                "number_of_documents": len(docs),
                "chunks_created": len(chunks),
                "embeddings_generated": len(embedded_chunks),
                "sample_embedding_dimension": len(embedded_chunks[0]["embedding"]),
                "stored_in_vector_db": len(embedded_chunks),
                "documents": docs[:2],
                "chunks": chunks[:2],
                "query": query,
                "answer": answer

            }

# Create application instance
application = Application()
app = application.app