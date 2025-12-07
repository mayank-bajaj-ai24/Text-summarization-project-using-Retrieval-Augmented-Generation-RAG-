# 🧠 Text Summarization with RAG  

A practical **Retrieval-Augmented Generation (RAG)** app for long-text summarization, built with **Python** and **Streamlit**. The system ingests large text, builds an embedding-based index, retrieves the most relevant chunks, and generates concise summaries using a modular **ingestion → retrieval → generation** pipeline.  

***

## 🌟 Features  

- 🧹 **Robust Ingestion:** Cleans raw text (HTML, control chars, noisy punctuation) and splits it into coherent chunks.  
- 🧮 **Embedding-Based Index:** Uses a sentence-transformer model to embed chunks and store them in a vector index for fast similarity search.  
- 🔍 **True RAG Retrieval:** For each query/summary request, retrieves the most relevant chunks via vector similarity before summarization.  
- 🧩 **Hybrid Summarization:**  
  - **Extractive:** Word-frequency-based summarizer (offline, no API).  
  - **Abstractive (Optional):** Hugging Face LLM (e.g., `facebook/bart-large-cnn`) via HuggingFaceHub.  
- 🖥️ **Streamlit Dashboard:** Clean UI to paste text, configure chunking, retrieval, and summary length.  
- 💾 **Exportable Output:** Download generated summaries as plain `.txt` files.  

***

## 🗂️ Project Structure  

```bash
text-summarization-rag/
├── config/               # Settings & environment variables
├── ingestion/            # Text cleaning, chunking, embedding & indexing
├── retrieval/            # Vector similarity search over embedded chunks
├── generation/           # Extractive + optional HF-based summarization
├── ui/                   # Streamlit web UI
├── utils/                # Helper utilities (placeholders/extensions)
├── data/                 # Local storage for raw text / indices
├── requirements.txt      # Python dependencies
└── main.py               # Application entry point
```

***

## ⚙️ Installation  

### 1️⃣ Clone the Repository  

```bash
git clone https://github.com/mayank-bajaj-ai24/text-summarization-rag.git
cd text-summarization-rag
```

### 2️⃣ Create & Activate a Virtual Environment  

```bash
python -m venv venv          #Advised to use python 3.11 for downloading all libraries.
venv\Scripts\activate        # Windows
# OR
source venv/bin/activate     # macOS / Linux
```

### 3️⃣ Install Dependencies  

```bash
pip install -r requirements.txt
```

### 4️⃣ Environment Configuration  

Create your `.env` from the template:

```bash
cp env.example .env          # or create .env manually on Windows
```

Edit `.env` and set:

```env
HUGGINGFACEHUB_API_TOKEN=hf_your_token_here   # for optional LLM summarization
# other settings: CHUNK_SIZE, SUMMARY_LENGTH, etc.
```

#### 🔑 Getting a Hugging Face Token  

1. Go to [https://huggingface.co](https://huggingface.co) and log in / sign up.  
2. Open [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).  
3. Click **“New token”**, name it `rag-summarizer`, grant **Read** permission.  
4. Copy the token and paste it into `.env` as `HUGGINGFACEHUB_API_TOKEN`.  

***

## 🚀 Running the App  

```bash
python main.py
```

Then open the app in your browser:  
👉 [http://localhost:8501](http://localhost:8501)

***

## 🧩 RAG Methodology  

### 1. Ingestion & Indexing  

- `TextCleaner` strips HTML with **BeautifulSoup**, removes control characters, and normalizes whitespace and punctuation to create a clean document.  
- `TextChunker` splits the cleaned document into overlapping chunks (configurable size and overlap) at sentence/whitespace boundaries.  
- An embedding model from **sentence-transformers** converts each chunk into a vector; these vectors and their metadata are stored in an in-memory or lightweight vector index, preparing the data for retrieval.  

### 2. Retrieval (R in RAG)  

- When the user requests a summary, the app embeds the input (or a query derived from it) using the same sentence-transformer model.  
- It performs **vector similarity search** over the indexed chunk embeddings to select the top‑k most relevant chunks as context.  
- These retrieved chunks form the “knowledge base” that conditions the summarization step, following the standard retriever → generator RAG pattern.  

### 3. Generation (G in RAG)  

- **Primary path:** The retrieved chunks are concatenated into a context window and passed to the summarization module.  
- **If Hugging Face is enabled:** a model like `facebook/bart-large-cnn` (via HuggingFaceHub) produces an abstractive summary over the retrieved context.  
- **Fallback path:** A word-frequency-based extractive summarizer scores sentences and selects the most informative ones from the retrieved context, working fully offline.  

### 4. UI & Output  

- A **Streamlit** interface exposes controls for: chunk size, number of retrieved chunks, and target summary length.  
- The UI displays: original text, retrieved context (optional), final summary, and basic statistics (compression ratio, word reduction, etc.).  
- Users can download the summary as a text file for reuse.  

***

## 🔒 Security & Best Practices  

- `.env` is **git-ignored** – API keys and secrets are never committed.  
- Use `env.example` as a safe template when sharing or for collaborators.  
- If a secret is accidentally committed, remove it from history and rotate the key.  

***

## 🧪 How to Try It  

- Start with a **short paragraph** to verify basic summarization.  
- Then test with a **long article or report** (up to ~50,000 characters) to see ingestion, retrieval, and summarization in action.  
- Experiment with:  
  - Different **chunk sizes** (e.g., 500–2000 characters).  
  - Different **top‑k retrieved chunks**.  
  - Different **summary lengths** (1–10 sentences).  

***

## 📁 Key Modules  

| Module / File                 | Role                                                                 |
|------------------------------|----------------------------------------------------------------------|
| `main.py`                    | Launches the Streamlit application                                  |
| `config/settings.py`         | Loads environment variables and global configuration                 |
| `ingestion/text_cleaner.py`  | Cleans and normalizes raw text                                      |
| `ingestion/chunker.py`       | Splits documents into overlapping chunks                            |
| `retrieval/retriever.py`     | Embeds chunks, builds index, and performs vector similarity search  |
| `generation/summarizer.py`   | Extractive + optional Hugging Face LLM summarization                |
| `ui/streamlit_app.py`        | Streamlit UI for interaction, settings, and visualization           |

***

## 📜 License  

Released under the **MIT License** – use, modify, and extend for learning, research, and personal projects.

***

## 💬 Feedback & Contributions  

Have suggestions, feature ideas, or found a bug?  
Open an issue or pull request here:  

👉 [https://github.com/mayank-bajaj-ai24/text-summarization-rag](https://github.com/mayank-bajaj-ai24/text-summarization-rag)
