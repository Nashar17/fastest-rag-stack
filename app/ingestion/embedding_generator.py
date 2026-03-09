import ollama


class EmbeddingGenerator:
    """
    Responsible for generating embeddings from text chunks
    using a local Ollama embedding model.
    """

    def __init__(self, model_name: str = "nomic-embed-text"):
        self.model_name = model_name

    def generate_embeddings(self, chunks):
        embedded_chunks = []

        for chunk in chunks:
            response = ollama.embeddings(
                model=self.model_name,
                prompt=chunk["content"]
            )

            embedding = response["embedding"]

            embedded_chunks.append({
                "file_name": chunk["file_name"],
                "content": chunk["content"],
                "embedding": embedding
            })

        return embedded_chunks