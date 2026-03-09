from unittest import loader

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config import settings
from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.text_chunker import TextChunker
from app.ingestion.embedding_generator import EmbeddingGenerator


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
        def test_pdf_loader():
            loader = PDFLoader("data/pdfs")
            docs = loader.extract_text()

            chunker = TextChunker()
            chunks = chunker.chunk_documents(docs)

            embedder = EmbeddingGenerator()
            embedded_chunks = embedder.generate_embeddings(chunks[:3])

            return {
                "number_of_documents": len(docs),
                "chunks_created": len(chunks),
                "documents": docs[:2],
                "chunks": chunks[:2],
                "embeddings_generated": len(embedded_chunks),
                "sample_embedding_dimension": len(embedded_chunks[0]["embedding"])
            }

# Create application instance
application = Application()
app = application.app