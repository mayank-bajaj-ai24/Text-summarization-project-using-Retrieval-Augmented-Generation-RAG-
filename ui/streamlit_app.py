import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings
from ingestion.text_cleaner import TextCleaner
from ingestion.chunker import TextChunker
from retrieval.retriever import TfidfRetriever
from generation.summarizer import Summarizer

st.set_page_config(page_title="RAG Text Summarizer", page_icon="🧠", layout="wide")

st.title("🧠 RAG-based Text Summarization")
st.markdown("Paste long text, retrieve the most relevant chunks, and generate a concise summary.")

if "retriever" not in st.session_state:
    st.session_state.retriever = TfidfRetriever()

chunk_size = 1000
overlap = 150
top_k = 5
summary_len = 3

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Input Text")
    input_text = st.text_area(
        "Enter or paste text here:",
        height=300,
        placeholder="Paste long article, report, or document...",
        max_chars=settings.MAX_TEXT_LENGTH,
    )
    run_button = st.button("🚀 Run RAG Summarization")

with col2:
    st.subheader("📤 Summary")
    summary_placeholder = st.empty()

if run_button:
    if not input_text or len(input_text.strip()) < 10:
        st.error("Please provide at least a few sentences of text.")
    else:
        cleaner = TextCleaner()
        cleaned = cleaner.clean(input_text)

        chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=overlap)
        chunks = chunker.chunk(cleaned)

        st.session_state.retriever.index_chunks(chunks)
        retrieved = st.session_state.retriever.retrieve(cleaned, top_k=top_k)

        # Concatenate retrieved chunks as RAG context
        context_text = "\n\n".join([c.text for c in retrieved])

        summarizer = Summarizer()
        prompt = (
               "Summarize the following healthcare AI description in "
                f"{summary_len} concise sentences, avoiding repetition:\n\n{context_text}"
                 )
        summary = summarizer.generate_summary(prompt, max_sentences=summary_len)
        summary_placeholder.write(summary)
        
