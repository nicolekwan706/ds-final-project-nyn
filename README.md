<h1>Movie RAG System</h1>

<p><strong>Group members:</strong> Nishita Koya (vfj8ba), Yuhan Liu (yl7gk), Nicole Kwan (ypt2vj)</p>

<hr>

<p>This project implements a Retrieval-Augmented Generation (RAG) system using:</p>
<ul>
  <li>A cleaned CSV dataset (<code>etl_cleaned_dataset.csv</code>)</li>
  <li>A film box-office PDF:
    <a href="https://www.researchgate.net/publication/281730174_The_determinants_of_box_office_performance_in_the_film_industry_revisited" target="_blank">
      The determinants of box office performance in the film industry revisited
    </a>
  </li>
</ul>

<p>The system performs:</p>
<ul>
  <li>Document ingestion and chunking</li>
  <li>Embedding with <code>bge-small-en-v1.5</code></li>
  <li>FAISS vector search</li>
  <li>Local LLM generation using <code>Phi-3-mini-4k-instruct</code></li>
  <li>A Flask API endpoint at <code>/api/ask</code></li>
  <li>A simple optional HTML user interface</li>
</ul>

<h2>Folder Structure</h2>

<pre>
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
├── outputs/                       #all generated files stored here
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
</pre>

<h2> Before Running: Move Required Output Files</h2>

<p>
Because the RAG pipeline was originally developed in Google Colab, it uses a flat directory structure.
To run the API successfully, please move all files inside <code>outputs/</code> into the project root, so the folder looks like:
</p>

<pre>
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
</pre>

<p>No path changes are required — the system expects these artifacts to be in the project root.</p>

<hr>

<h2>How to Run (Under 2 Minutes)</h2>

<h3>1. Navigate to the API folder</h3>
<pre><code>cd api
</code></pre>

<h3>2. Install dependencies</h3>

<p><strong>Python Version Warning</strong><br>
The serialized files (<code>texts.pkl</code>, <code>metadatas.pkl</code>, <code>faiss_index.bin</code>, etc.) were created using Python 3.12.
These files may not load correctly under other Python versions.</p>

<p>Install using Python 3.12:</p>
<pre><code>python3.12 -m pip install -r requirements.txt
</code></pre>

<h3>3. Start the server</h3>

<pre><code>python3.12 app.py
</code></pre>

<p>The API will be available at:</p>
<pre><code>http://127.0.0.1:8000
</code></pre>

<hr>

<h2>API Usage</h2>

<h3>POST /api/ask</h3>

<p>Example CURL request:</p>

<pre><code>curl -X POST http://127.0.0.1:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Which movie has the highest IMDb rating?"}'
</code></pre>

<p>Example JSON response:</p>

<pre><code>{
  "answer": "Based on the context ...",
  "sources": [
    { "id": "file.pdf", "page": 7, "snippet": "..." },
    { "id": "etl_cleaned_dataset.csv", "snippet": "..." }
  ]
}
</code></pre>

<hr>

<h2>Bonus UI</h2>

<p>
Open <code>ui/chat.html</code> in a browser to use a simple chat interface that sends queries to
<code>/api/ask</code> and displays the answer and cited sources.
</p>
