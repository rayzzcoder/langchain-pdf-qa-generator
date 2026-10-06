# LangChain PDF Q&A Generator

Generate question-answer pairs from any **social sciences PDF** using LangChain, Groq, Gemini embeddings, and FAISS, through a simple FastAPI web app.

Upload a PDF (a report, research paper, or lecture notes), and get study questions with answers grounded in the document's own content. Preview the results on the page and download them as a CSV.

## Demo

**[▶ Watch the demo on Loom](https://www.loom.com/share/b9bcd0da321c48e29e2e2acdcb120348)**

### App overview

![App overview](assets/1.png)

### Successful generation

![Generated questions and answers](assets/2.png)

### How it works

![How it works](assets/3.png)

## Features

- Web interface built with FastAPI: upload, progress steps, on-page results preview, and CSV download
- Validates uploads on the backend (valid PDF, page count, file size)
- Splits the PDF into chunks and generates questions with a first-pass and a refine chain
- Retrieves relevant context with FAISS so answers stay grounded in the document
- Built with the LangChain v1 LCEL pipeline (`retriever | prompt | llm | parser`)
- Cleans model output (markdown symbols, numbering, special characters) before saving

## Tech Stack

| Component | Tool |
|---|---|
| Framework | LangChain v1 (LCEL) |
| LLM | Groq |
| Embeddings | Google Gemini |
| Vector store | FAISS |
| Web app | FastAPI |
| Language | Python 3.10 |

## How It Works

```
PDF -> Text chunks -> Questions (first pass + refine) -> Gemini embeddings -> FAISS index
    -> Retrieved context -> Groq LLM -> Answers -> CSV
```

1. The PDF is loaded and split into chunks.
2. Questions are generated from the document text.
3. Chunks are embedded with Gemini and stored in FAISS.
4. For each question, relevant context is retrieved and passed to the LLM.
5. The answers are cleaned and written to a CSV file.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/rayzzcoder/langchain-pdf-qa-generator.git
cd langchain-pdf-qa-generator
```

### 2. Create an environment

Using Python's built-in virtual environment:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
```

Alternatively, using Conda:

```bash
conda create -n interview python=3.10 -y
conda activate interview
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

The repository does not require the generated `*.egg-info` directory to run. The command above installs the runtime dependencies needed by the application.

### 4. Add your API keys

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_gemini_api_key
```

Get keys from the [Groq Console](https://console.groq.com) and [Google AI Studio](https://aistudio.google.com).

### 5. Start the app

With the environment activated and inside the project folder, run:

```bash
python app.py
```

Then open the local address shown in the terminal (usually **http://127.0.0.1:8000**) in your browser.

## Using the App

1. Open the page and upload a text-based PDF.
2. Wait while the progress steps run (this can take a few minutes for longer documents).
3. Preview the generated questions and answers on the page.
4. Download the CSV, or remove the file and try another one.

The page shows the current limits for page count and file size.

## Sample Data

The `data/` folder contains a few publicly available social sciences reports used for testing. You can also use your own PDFs.

## Limitations and Future Work

- Only text-based PDFs are supported. Scanned or handwritten documents need OCR.
- The Groq free tier has a tokens-per-minute limit, so long documents run slowly.
- Planned: unique file names per upload, a background job queue for multiple users, and an OCR/ICR version for scanned documents.

## Author

**Raja Abdul Rafay**, BS IT, Quaid-i-Azam University
GitHub: [@rayzzcoder](https://github.com/rayzzcoder)
