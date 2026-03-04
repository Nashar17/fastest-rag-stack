from fastapi import FastAPI
from app.config import settings


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


# Create application instance
application = Application()
app = application.app