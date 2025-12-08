from dataclasses import dataclass
from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class RetrievedChunk:
    text: str
    score: float
    index: int


class TfidfRetriever:
    """Simple TF-IDF based retriever (no torch or HF models)."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.chunk_texts: List[str] = []
        self.chunk_matrix = None

    def index_chunks(self, chunks: List[str]) -> None:
        self.chunk_texts = chunks
        if not chunks:
            self.chunk_matrix = None
            return
        self.chunk_matrix = self.vectorizer.fit_transform(chunks)

    def retrieve(self, query: str, top_k: int = 5) -> List[RetrievedChunk]:
        if not self.chunk_texts or self.chunk_matrix is None:
            return []

        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.chunk_matrix)[0]

        top_k = min(top_k, len(self.chunk_texts))
        top_indices = np.argsort(sims)[::-1][:top_k]

        results: List[RetrievedChunk] = []
        for idx in top_indices:
            results.append(
                RetrievedChunk(
                    text=self.chunk_texts[idx],
                    score=float(sims[idx]),
                    index=int(idx),
                )
            )
        return results
