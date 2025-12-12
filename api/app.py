from flask import Flask, request, jsonify, render_template_string
from rag import RAGPipeline

#initialize Flask + RAG
app = Flask(__name__)
rag = RAGPipeline()

#format sources for API responses
def format_sources(sources):
    formatted = []
    for src in sources:
        meta = src["metadata"]

        entry = {
            "id": meta.get("file_name", meta.get("title", "unknown")),
            "page": meta.get("page", None),
            "snippet": src["text"][:200].replace("\n", " ") + "..."
        }
        formatted.append(entry)
    return formatted


#api
@app.post("/api/ask")
def ask():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Request must include 'question'."}), 400

    question = data["question"]
    result = rag.answer(question, k=5)

    response = {
        "answer": result["answer"],
        "sources": format_sources(result["sources"])
    }
    return jsonify(response)



#web chat
CHAT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>RAG Chat Interface</title>
    <style>
        body { font-family: Arial; max-width: 700px; margin: 40px auto; }
        #chat { border: 1px solid #ccc; padding: 15px; height: 400px; overflow-y: auto; }
        .msg-user { margin: 10px 0; color: blue; }
        .msg-bot { margin: 10px 0; color: green; }
        .src { font-size: 12px; color: #555; }
    </style>
</head>
<body>

<h2>RAG Movie Chatbot</h2>

<div id="chat"></div>

<input id="question" type="text" placeholder="Type a question..." style="width:80%;">
<button onclick="sendQuestion()">Send</button>

<script>
async function sendQuestion() {
    const q = document.getElementById("question").value;
    if (!q) return;

    const chat = document.getElementById("chat");
    chat.innerHTML += `<div class='msg-user'><b>You:</b> ${q}</div>`;
    document.getElementById("question").value = "";

    // Call backend API
    const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q })
    });

    const data = await res.json();

    chat.innerHTML += `<div class='msg-bot'><b>Bot:</b> ${data.answer}</div>`;

    if (data.sources) {
        data.sources.forEach((s, idx) => {
            chat.innerHTML += `<div class='src'>[Source ${idx+1}] ${s.id}, page=${s.page}, snippet=${s.snippet}</div>`;
        });
    }

    chat.scrollTop = chat.scrollHeight;
}
</script>

</body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(CHAT_HTML)


#run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
