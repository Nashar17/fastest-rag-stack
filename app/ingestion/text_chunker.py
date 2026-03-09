class TextChunker:
    """
    Responsible for splitting documents into smaller chunks.
    """

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_documents(self, documents):
        chunks = []

        for doc in documents:
            text = doc["content"]

            start = 0
            while start < len(text):
                end = start + self.chunk_size

                chunk_text = text[start:end]

                chunks.append({
                    "file_name": doc["file_name"],
                    "content": chunk_text
                })

                start += self.chunk_size - self.chunk_overlap

        return chunks