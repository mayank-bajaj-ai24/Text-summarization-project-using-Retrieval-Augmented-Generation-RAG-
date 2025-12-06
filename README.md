**Text Summarization with RAG**
**Overview**
This project is a simple text summarization app built with Python and Streamlit.
It cleans raw text, chunks it, and generates summaries using:

Extractive summarization (word frequency) - works without any API

Hugging Face LLM (optional) - for better summaries when token is provided

**Features**
✨ Text cleaning (HTML removal, punctuation normalization)
✨ Intelligent chunking at sentence boundaries
✨ Extractive summarization (no API needed)
✨ Optional Hugging Face LLM summarization
✨ Minimal, clean Streamlit web UI
✨ Download summaries as text files

**Project Structure**
text
config/          → Settings & environment variables
ingestion/       → Text cleaning and chunking
generation/      → Summarization logic
retrieval/       → RAGFlow integration (stub for future)
ui/              → Streamlit web interface
utils/           → Utilities package
data/            → Raw and processed text directories

#Installation
1. Clone the Repository
bash
git clone https://github.com/<your-username>/text-summarization-rag.git
cd text-summarization-rag
2. Create Virtual Environment
bash
python -m venv venv
venv\Scripts\activate   # Windows
3. Install Dependencies
bash
pip install -r requirements.txt
4. Setup Environment Variables
bash
cp env.example .env

# Edit .env and add your Hugging Face token
# HUGGINGFACEHUB_API_TOKEN=hf_your_token_here
Get Your Hugging Face Token
Go to https://huggingface.co/

Sign up or log in (free)

Visit https://huggingface.co/settings/tokens

Click "New token"

Name: rag-summarizer

Select: Read permission

Copy the token

Paste into .env file:

text
HUGGINGFACEHUB_API_TOKEN=hf_xxxxxxxxxxxxx
Run the App
bash
python main.py
Open your browser at http://localhost:8501

**Methodology**
1. Ingestion Phase
TextCleaner removes HTML tags and normalizes whitespace/punctuation

TextChunker splits large text into overlapping chunks at sentence boundaries

2. Summarization Phase
If Hugging Face token is set → tries to use facebook/bart-large-cnn model

If token is missing or fails → falls back to word-frequency extractive summarization

Both methods produce good summaries; HF model is higher quality

3. UI Phase
Simple Streamlit interface for text input
Adjustable chunk size and summary length
Shows summary output
Displays chunked text for reference

Security Notes
⚠️ Important:
.env is in .gitignore - never commit it
API keys stay private and local
Share only env.example as a template
If you accidentally commit .env:
bash
git rm --cached .env
git commit -m "Remove .env from tracking"

**File	Purpose**
main.py	Entry point - runs Streamlit app
config/settings.py	Loads environment variables
ingestion/text_cleaner.py	Cleans text (BeautifulSoup)
ingestion/chunker.py	Splits text into chunks
generation/summarizer.py	Generates summaries (with HF fallback)
ui/streamlit_app.py	Web interface
retrieval/retriever.py	RAGFlow integration (for future use)

**Testing**
Test 1: Simple Text
text
Artificial Intelligence is changing the world. Machine learning is a subset of AI. 
Deep learning uses neural networks. AI is used in many industries today.
✅ Should produce a 3-sentence summary

Test 2: Long Text
Copy a long article from Wikipedia
Paste into app
Should handle up to 50K characters

Test 3: Settings
Try different chunk sizes (500-2000)
Try different summary lengths (1-10 sentences)
See how results change

**License**
MIT License - feel free to use for learning and projects

**Questions?**
If you have questions about the code or setup, open an issue on GitHub.
