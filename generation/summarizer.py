import os
import re
from collections import Counter
from typing import Dict

from huggingface_hub import InferenceClient

class Summarizer:
    """Generate summaries using a Hugging Face LLM via Inference API, with extractive fallback."""

    def __init__(self):
        self.client = None
        self._init_client()

    def _init_client(self):
        token = os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HF_TOKEN")
        if not token:
            print("WARNING: No Hugging Face token found. LLM summarization disabled.")
            self.client = None
            return

        # Hosted summarization model
        self.client = InferenceClient(
            model="facebook/bart-large-cnn",
            token=token,
        )

    def generate_summary(self, text: str, max_sentences: int = 3) -> str:
        if not text or not text.strip():
            return "No text provided for summarization."

        # Try LLM first
        if self.client is not None:
            try:
                return self._hf_summarize(text, max_sentences)
            except Exception as e:
                print(f"Hugging Face Inference summarization failed: {e}")

        # Fallback: extractive
        return self._extractive_summarize(text, max_sentences)

    def _hf_summarize(self, text: str, max_sentences: int = 3) -> str:
        """Call Hugging Face Inference API for abstractive summarization."""
        prompt = (
            "Summarize the following text in about "
            f"{max_sentences} concise, well-formed sentences without repetition:\n\n"
            f"{text}"
        )

        # Minimal, compatible call – no extra kwargs
        result = self.client.summarization(
            prompt,
            clean_up_tokenization_spaces=True,
        )

        return result.summary_text.strip()



    def _extractive_summarize(self, text: str, max_sentences: int = 3) -> str:
        """Simple word-frequency based extractive summarizer."""
        sentences = re.split(r"(?<=[.!?])\s+", text)
        if len(sentences) <= max_sentences:
            return text.strip()

        words = re.findall(r"\w+", text.lower())
        word_freq = Counter(words)

        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "is", "was", "are", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "must", "can", "this", "that", "these", "those",
            "i", "you", "he", "she", "it", "we", "they"
        }
        for w in stop_words:
            word_freq.pop(w, None)

        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words_in_sentence = re.findall(r"\w+", sentence.lower())
            score = sum(word_freq.get(w, 0) for w in words_in_sentence)
            sentence_scores[i] = score

        top_indices = sorted(
            sentence_scores.items(), key=lambda x: x[1], reverse=True
        )[:max_sentences]
        top_indices = sorted(idx for idx, _ in top_indices)

        summary_sentences = [sentences[i].strip() for i in top_indices]

        cleaned = []
        seen = set()
        for s in summary_sentences:
            if s and s not in seen:
                cleaned.append(s)
                seen.add(s)

        return " ".join(cleaned)

    def get_summary_stats(self, original_text: str, summary: str) -> Dict:
        orig_chars = len(original_text)
        summary_chars = len(summary)
        orig_words = len(original_text.split())
        summary_words = len(summary.split())
        compression = (1 - summary_chars / orig_chars) * 100 if orig_chars > 0 else 0
        word_reduction = (1 - summary_words / orig_words) * 100 if orig_words > 0 else 0
        return {
            "original_characters": orig_chars,
            "summary_characters": summary_chars,
            "compression_ratio": f"{compression:.1f}%",
            "original_words": orig_words,
            "summary_words": summary_words,
            "word_reduction": f"{word_reduction:.1f}%",
        }
