from app.ingestion.embedding_generator import EmbeddingGenerator
from app.retrieval.vector_store import VectorStore


class Retriever:
    """
    Responsible for retrieving the most relevant chunks
    from the vector database given a user query.
    """

    def __init__(self):
        self.embedder = EmbeddingGenerator()
        self.vector_store = VectorStore()

    def retrieve(self, query: str, k: int = 3):
        """
        Retrieve the top k relevant chunks for a query.
        """

        # Generate embedding for the query
        query_embedding = self.embedder.generate_embeddings([
            {
                "file_name": "query",
                "content": query
            }
        ])[0]["embedding"]

        # Search the vector database
        results = self.vector_store.similarity_search(
            query_embedding=query_embedding,
            k=k
        )

        return results