import os
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from flask import Flask, request, jsonify, render_template
import chromadb
import json
import csv
import fitz  # PyMuPDF

# Initialize tokenizer and model
MODEL_NAME = "deepset/bert-base-cased-squad2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForQuestionAnswering.from_pretrained(MODEL_NAME)

# Set up ChromaDB for document retrieval
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="ai_literacy_docs")

# Flask app for chatbot
app = Flask(__name__)

# Helper function to extract text from PDFs
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    return " ".join(page.get_text() for page in doc)

# Load documents from various formats into ChromaDB
def load_documents_from_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".json"):
                with open(file_path, 'r') as f:
                    documents = json.load(f)
                    for doc in documents:
                        collection.add(documents=[doc["content"]], metadatas=[{"title": doc["title"]}])
            elif file.endswith(".txt"):
                with open(file_path, 'r') as f:
                    content = f.read()
                    collection.add(documents=[content], metadatas=[{"title": os.path.basename(file_path)}])
            elif file.endswith(".csv"):
                with open(file_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        collection.add(documents=[row["content"]], metadatas=[{"title": row.get("title", os.path.basename(file_path))}])
            elif file.endswith(".pdf"):
                content = extract_text_from_pdf(file_path)
                collection.add(documents=[content], metadatas=[{"title": os.path.basename(file_path)}])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get("question")

    # Retrieve relevant documents from ChromaDB with improved search
    results = collection.query(query_texts=[question], n_results=5)

    context = " ".join(results["documents"]) if results["documents"] else ""

    # Answer extraction using BERT
    qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)
    answer = qa_pipeline({"question": question, "context": context}) if context else {"answer": "No relevant information found.", "score": 0.0}

    return jsonify({"answer": answer["answer"], "score": answer["score"]})

if __name__ == '__main__':
    if not os.path.exists("./chroma_db"):
        load_documents_from_folder("./documents")
    app.run(host='0.0.0.0', port=5000)

# Dockerfile creation
with open("Dockerfile", "w") as f:
    f.write("""
    FROM python:3.10-slim

    WORKDIR /app

    COPY . /app

    RUN pip install torch transformers flask chromadb pymupdf

    EXPOSE 5000

    CMD ["python", "your_script.py"]
    """)

# HTML UI creation
os.makedirs("templates", exist_ok=True)
with open("templates/index.html", "w") as f:
    f.write("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>AI Literacy Chatbot</title>
    </head>
    <body>
        <h1>AI Literacy Chatbot</h1>
        <form id="chat-form">
            <label for="question">Ask a question:</label>
            <input type="text" id="question" name="question" required>
            <button type="submit">Submit</button>
        </form>
        <h2>Answer:</h2>
        <p id="answer"></p>

        <script>
            const form = document.getElementById('chat-form');
            form.addEventListener('submit', async (event) => {
                event.preventDefault();
                const question = document.getElementById('question').value;

                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question })
                });
                const data = await response.json();
                document.getElementById('answer').textContent = data.answer;
            });
        </script>
    </body>
    </html>
    """)
