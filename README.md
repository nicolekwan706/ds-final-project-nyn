# Movie RAG System

**Group members:** Nishita Koya (vfj8ba), Yuhan Liu (yl7gk), Nicole Kwan (ypt2vj)

---
## 1. Overview
This project implements a Retrieval-Augmented Generation (RAG) system using:
* A cleaned CSV dataset (`etl_cleaned_dataset.csv`)
* A film box-office PDF:
[The determinants of box office performance in the film industry revisited](https://www.researchgate.net/publication/281730174_The_determinants_of_box_office_performance_in_the_film_industry_revisited")

The system performs:
* Document ingestion and chunking
* Embedding with `bge-small-en-v1.5`
* FAISS vector search
* Local LLM generation using `Phi-3-mini-4k-instruct`
  * A Flask API endpoint at `/api/ask`
  * A simple optional HTML user interface

---
## 2. Folder Structure

```bash
ds-final-project-nyn/
│
├── api/
│   ├── app.py
│   └── requirements.txt
│
├── rag_pipeline/
│   ├── ingest.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── rag.py
│
├── data/
│   ├── etl_cleaned_dataset.csv
│   └── additional_documents/
│
├── outputs/                       
│   ├── ingested_documents.jsonl
│   ├── embeddings.npy
│   ├── faiss_index.bin
│   ├── texts.pkl
│   ├── metadatas.pkl
│
├── ui/
│   └── chat.html
│
├── notebooks/
│   └── exploration.ipynb
│
├── README.md
└── reflection.pdf
```

---
## 3. Before Running: Move Required Output Files

Because the RAG pipeline was originally developed in Google Colab, it uses a flat directory structure.
To run the API successfully, please move all files inside `outputs` into the project root, so the folder looks like:

```bash
ds-final-project-nyn/
│
├── app.py
├── ingested_documents.jsonl
├── embeddings.npy
├── faiss_index.bin
├── texts.pkl
├── metadatas.pkl
│
├── rag_pipeline/
├── data/
├── ui/
├── api/
└── ...
```

No path changes are required. The system expects these artifacts to be in the project root.

---
## 4. How to Run

**Step 1** - Navigate to the API folder
```bash
cd api
```

**Step 2** - Install dependencies

*Note: The serialized files (`texts.pkl`, `metadatas.pkl`, `faiss_index.bin`, etc.) were created using Python 3.12. These files may not load correctly under other Python versions.*

Install using Python 3.12:
```bash
python3.12 -m pip install -r requirements.txt
```

**Step 3** - Start the server

```bash
python3.12 app.py
```

**Step 4** - The API will be available at:
```bash
http://127.0.0.1:8000
```

---
## 5. API Usage

### POST /api/ask

Example CURL request:
```bash
curl -X POST http://127.0.0.1:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Which movie has the highest IMDb rating?"}'
```

Example JSON response:
```bash
  "answer": "Based on the context ...",
  "sources": [
    { "id": "file.pdf", "page": 7, "snippet": "..." },
    { "id": "etl_cleaned_dataset.csv", "snippet": "..." }
  ]
}
```

---
## 6. Bonus UI
Open `ui/chat.html` in a browser to use a simple chat interface that sends queries to
`/api/ask` and displays the answer and cited sources.
