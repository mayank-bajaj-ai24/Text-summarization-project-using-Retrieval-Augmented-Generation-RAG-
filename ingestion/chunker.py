from typing import List, Dict
import re

class TextChunker:
    """Split text into chunks"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str) -> List[str]:
        if not text:
            return []

        if len(text) <= self.chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            if end < len(text):
                last_period = text.rfind(".", start, end)
                last_newline = text.rfind("\n", start, end)
                last_space = text.rfind(" ", start, end)
                boundary = max(last_period, last_newline, last_space)
                if boundary > start:
                    end = boundary + 1

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            start = end - self.chunk_overlap

        return chunks

    def get_chunk_metadata(self, chunks: List[str]) -> List[Dict]:
        metadata = []
        for i, chunk in enumerate(chunks):
            words = chunk.split()
            sentences = re.split(r"(?<=[.!?])\s+", chunk)
            metadata.append(
                {
                    "chunk_id": i,
                    "character_count": len(chunk),
                    "word_count": len(words),
                    "sentence_count": len([s for s in sentences if s.strip()]),
                    "preview": chunk[:100] + "..." if len(chunk) > 100 else chunk,
                }
            )
        return metadata
