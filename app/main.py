from unittest import loader

from fastapi import FastAPI
from app.config import settings
from app.ingestion.pdf_loader import PDFLoader


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

            return {
                "number_of_documents": len(docs),
                "documents": docs[:1]  # show first doc only
            }
    


# Create application instance
application = Application()
app = application.app