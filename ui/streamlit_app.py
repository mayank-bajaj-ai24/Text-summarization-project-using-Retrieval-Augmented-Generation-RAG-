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

with st.sidebar:
    st.header("⚙️ Settings")
    chunk_size = st.slider("Chunk size (chars)", 500, 2000, settings.CHUNK_SIZE, step=100)
    overlap = st.slider("Chunk overlap (chars)", 0, 500, settings.CHUNK_OVERLAP, step=50)
    top_k = st.slider("Top-k retrieved chunks", 1, 10, settings.TOP_K_RETRIEVAL, step=1)
    summary_len = st.slider("Summary length (sentences)", 1, 10, settings.SUMMARY_LENGTH, step=1)

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

        stats = summarizer.get_summary_stats(context_text, summary)

        summary_placeholder.text_area(
            "Generated Summary:", value=summary, height=250, disabled=True
        )

        st.markdown("### 📊 Summary Statistics")
        c1, c2, c3 = st.columns(3)
        c1.metric("Compression", stats["compression_ratio"])
        c2.metric("Word Reduction", stats["word_reduction"])
        c3.metric("Summary Words", stats["summary_words"])

        st.markdown("### 🔍 Retrieved Chunks (R in RAG)")
        for rc in retrieved:
            with st.expander(f"Chunk {rc.index} (score={rc.score:.3f})"):
                st.write(rc.text)
