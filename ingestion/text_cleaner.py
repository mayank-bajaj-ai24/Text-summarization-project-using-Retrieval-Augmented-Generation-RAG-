import re
from bs4 import BeautifulSoup

class TextCleaner:
    """Clean and preprocess text"""

    def __init__(self):
        self.html_parser = "html.parser"

    def clean(self, text: str) -> str:
        text = self._remove_html_tags(text)
        text = self._normalize_whitespace(text)
        text = self._remove_special_chars(text)
        text = self._normalize_punctuation(text)
        return text.strip()

    def _remove_html_tags(self, text: str) -> str:
        soup = BeautifulSoup(text, self.html_parser)
        return soup.get_text()

    def _normalize_whitespace(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\n+", "\n", text)
        return text

    def _remove_special_chars(self, text: str) -> str:
        text = re.sub(r"[\x00-\x1F\x7F-\x9F]", "", text)
        return text

    def _normalize_punctuation(self, text: str) -> str:
        text = re.sub(r'["“”]', '"', text)
        text = re.sub(r"[‘’`]", "'", text)
        text = re.sub(r"[–—−]", "-", text)
        return text

    def extract_sentences(self, text: str) -> list:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]

    def get_text_stats(self, text: str) -> dict:
        sentences = self.extract_sentences(text)
        words = text.split()
        return {
            "character_count": len(text),
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_words_per_sentence": len(words) / len(sentences) if sentences else 0,
        }
