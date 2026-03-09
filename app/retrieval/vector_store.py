import chromadb


class VectorStore:
    """
    Responsible for storing and retrieving embeddings using Chroma.
    """

    def __init__(self):
        self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(
            name="rag_documents"
        )

    def add_embeddings(self, embedded_chunks):
        """
        Store embeddings in the vector database.
        """

        for idx, chunk in enumerate(embedded_chunks):
            self.collection.add(
                ids=[str(idx)],
                embeddings=[chunk["embedding"]],
                documents=[chunk["content"]],
                metadatas=[{
                    "file_name": chunk["file_name"]
                }]
            )

    def similarity_search(self, query_embedding, k=3):
        """
        Search for the most similar chunks.
        """

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        return results