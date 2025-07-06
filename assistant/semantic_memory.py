import chromadb
from sentence_transformers import SentenceTransformer

class SemanticMemory:
    def __init__(self, collection_name="karo_memory", model_name="all-MiniLM-L6-v2"):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.model = SentenceTransformer(model_name)

    def add_to_memory(self, text: str, metadata: dict = None):
        embedding = self.model.encode(text).tolist()
        doc_id = str(len(self.collection.get(include=["documents"])["documents"]) + 1)

        # Ensure metadata is never empty (Chroma requires at least one attribute)
        if not metadata:
            metadata = {"source": "karo"}  # or "task": text[:30] as fallback

        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[doc_id]
        )
        print(f"✅ Added to semantic memory: {text[:50]}...")

    def search_memory(self, query: str, n_results: int = 5) -> list[str]:
        query_embedding = self.model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents"]
        )
        return results["documents"][0] if results["documents"] else []