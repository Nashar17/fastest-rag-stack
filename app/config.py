import os
from dotenv import load_dotenv


class Settings:
    """
    Application configuration class.
    Loads environment variables and provides centralized access.
    """

    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY", None)



# Singleton instance
settings = Settings()