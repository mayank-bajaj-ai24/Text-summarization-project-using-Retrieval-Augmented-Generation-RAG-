***

# 🧠 Text Summarization with RAG  

A simple yet powerful text summarization app built with **Python** and **Streamlit**, combining both **extractive** and **abstractive (LLM-based)** summarization. Clean your raw text, chunk it intelligently, and generate concise summaries — all with a minimal and elegant interface.  

***

## 🌟 Features  

- 🧹 **Text Cleaning:** Removes HTML tags, punctuation, and normalizes whitespace.  
- ✂️ **Smart Chunking:** Splits text at sentence boundaries for better coherence.  
- 🧩 **Extractive Summarization:** Uses word frequency (no API required).  
- 🤖 **Optional LLM Summarization:** Integrates Hugging Face models like `facebook/bart-large-cnn`.  
- 🖥️ **Streamlit UI:** Clean and interactive web interface.  
- 💾 **Download Summaries:** Export generated summaries as text files.  

***

## 🗂️ Project Structure  

```
text-summarization-rag/
├── config/          # Settings & environment variables
├── ingestion/       # Text cleaning and chunking
├── generation/      # Summarization logic
├── retrieval/       # RAGFlow integration (stub for future)
├── ui/              # Streamlit web interface
├── utils/           # Utility scripts
├── data/            # Raw and processed text storage
└── main.py          # Entry point
```

***

## ⚙️ Installation  

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<mayank-bajaj-ai24>/text-summarization-rag.git
cd text-summarization-rag
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # macOS/Linux
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variables
```bash
cp env.example .env
```

Then open `.env` and add your Hugging Face token:  
```
HUGGINGFACEHUB_API_TOKEN=hf_your_token_here
```

#### 🔑 Get Your Hugging Face Token
1. Go to [huggingface.co](https://huggingface.co/) and log in or sign up (free).  
2. Visit [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).  
3. Click **“New token”**, name it `rag-summarizer`, and grant **Read** permission.  
4. Copy your token and paste it into `.env`.  

***

## 🚀 Run the App
```bash
python main.py
```

Then open your browser at [http://localhost:8501](http://localhost:8501)

***

## 🧩 Methodology  

### **1. Ingestion Phase**
- `TextCleaner` removes HTML and normalizes text.  
- `TextChunker` splits large text into overlapping chunks at sentence boundaries.  

### **2. Summarization Phase**
- If a Hugging Face token is set → uses `facebook/bart-large-cnn` for high-quality abstractive summaries.  
- If not → falls back to **extractive summarization** (word frequency-based).  

### **3. UI Phase**
- Streamlit interface for text input.  
- Adjustable chunk size and summary length.  
- Displays both output summary and chunked text.  

***

## 🔒 Security Notes  

- `.env` is **already in `.gitignore`** – never commit it!  
- Keep API keys private and local.  
- If you accidentally committed your `.env`:  
  ```bash
  git rm --cached .env
  git commit -m "Remove .env from tracking"
  ```

***

## 🧪 Testing  

### ✅ Test 1: Simple Text
**Input:**
```
Artificial Intelligence is changing the world. Machine learning is a subset of AI. 
Deep learning uses neural networks. AI is used in many industries today.
```
**Expected:** ~3-sentence summary.

### ✅ Test 2: Long Text
- Paste a long Wikipedia article (up to **50K characters**).  
- Should still summarize effectively.

### ✅ Test 3: Settings Variations
- Try different **chunk sizes (500–2000)**.  
- Adjust **summary lengths (1–10 sentences)**.  
- Observe summary quality and coherence changes.  

***

## 📁 Key Files  

| File | Purpose |
|------|----------|
| `main.py` | Streamlit app entry point |
| `config/settings.py` | Loads environment variables |
| `ingestion/text_cleaner.py` | Cleans text using BeautifulSoup |
| `ingestion/chunker.py` | Splits text into chunks |
| `generation/summarizer.py` | Summarizes text (with Hugging Face fallback) |
| `ui/streamlit_app.py` | Web UI interface |
| `retrieval/retriever.py` | Stub for future RAGFlow integration |

***

## 📜 License  

This project is licensed under the **MIT License** — free to use, modify, and share for learning and projects.  

***

## 💬 Questions or Feedback?  

Open an issue on [GitHub](https://github.com/<your-username>/text-summarization-rag/issues) — contributions and suggestions are welcome!  
