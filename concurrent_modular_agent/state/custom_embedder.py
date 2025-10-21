from sentence_transformers import SentenceTransformer
from chromadb import Documents, EmbeddingFunction, Embeddings

class CustomEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model_id: str, device: str = "cpu", truncate_dim: int = 128):
        self.model_id = model_id
        self._model = SentenceTransformer(model_id, device=device)
        self.truncate_dim = truncate_dim

    def name(self) -> str:
        return self.model_id
    
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = self._model.encode(
            input,
            truncate_dim=self.truncate_dim,
            normalize_embeddings=True
        ).tolist()
        return embeddings



"""
# embedder == "embeddinggemma-300M"
self._embedding_function = CustomEmbeddingFunction(
    model_id="google/embeddinggemma-300M",
    device="cpu",
    truncate_dim=128
)
"""