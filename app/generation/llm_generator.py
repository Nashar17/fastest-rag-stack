import ollama


class LLMGenerator:
    """
    Responsible for generating answers using retrieved chunks
    and a local LLM via Ollama.
    """

    def __init__(self, model_name: str = "llama2"):
        self.model_name = model_name

    def generate_answer(self, query: str, retrieved_chunks):
        """
        Generate an answer using the retrieved context.
        """

        # Combine retrieved documents into context
        documents = retrieved_chunks["documents"][0]

        context = "\n\n".join(documents)

        prompt = f"""
You are an AI assistant that answers questions using the provided context.

Context:
{context}

Question:
{query}

Answer the question using ONLY the context above.
If the answer is not contained in the context, say you don't know.
"""

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]