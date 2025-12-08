import sys
from pathlib import Path
import subprocess

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_streamlit():
    app_path = project_root / "ui" / "streamlit_app.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])

if __name__ == "__main__":
    print("Starting RAG Text Summarization App at http://localhost:8501")
    run_streamlit()
