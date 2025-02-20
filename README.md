# AI Literacy Chatbot with BERT and ChromaDB

## 📌 Project Overview

This project implements an **AI Literacy Chatbot** using:

- **BERT Model**: For accurate question-answering.
- **ChromaDB**: For efficient document storage and semantic search.
- **Flask**: Web interface for user interaction.
- **Docker**: For containerized deployment.

The chatbot can process and index documents from **PDF**, **JSON**, **CSV**, and **TXT** formats, retrieve relevant content, and answer questions in real-time.

---

## 📊 Project Structure

```
.
├── Dockerfile                      # Docker configuration
├── app.py                          # Main Flask application
├── documents/                      # Folder for source documents
├── templates/                      # HTML UI
│    └── index.html                 # User interface for chatbot
└── chroma_db/                      # Persistent storage for ChromaDB
```

---

## 📚 Data Requirements

The chatbot supports multiple file formats for document ingestion:

1. **PDF**: Extracts text from each page.
2. **JSON**: Parses and indexes structured content.
3. **CSV**: Processes rows with `content` and optional `title` columns.
4. **TXT**: Loads plain-text files.

Ensure all documents are stored in the `documents/` directory.

Example CSV format:

| content                   | title            |
|---------------------------|------------------|
| AI improves data handling | AI Advances 2024 |

---

## 🧠 Model Architecture

1. **Document Retrieval**: ChromaDB is used for indexing and retrieving relevant documents.
2. **QA Pipeline**: BERT ("deepset/bert-base-cased-squad2") is used for extracting answers from retrieved content.

---

## 🚀 Setup & Installation

1. **Clone the Repository:**
```bash
$ git clone https://github.com/your-repo/ai-literacy-chatbot.git
$ cd ai-literacy-chatbot
```

2. **Create a Virtual Environment (Optional):**
```bash
$ python -m venv venv
$ source venv/bin/activate
```

3. **Install Dependencies:**
```bash
$ pip install torch transformers flask chromadb pymupdf
```

4. **Ensure GPU is Available (Optional for CUDA users):**
```bash
$ python -c "import torch; print(torch.cuda.is_available())"
```

---

## 🔨 Usage

1. **Prepare Data**: Place your documents in the `documents/` folder.

2. **Run the Flask Application:**
```bash
$ python app.py
```

3. **Access the Chatbot:**
Navigate to:
```
http://localhost:5000
```

4. **Ask Questions:**
Type your question and receive AI-generated answers.

---

## 📊 API Endpoints

1. **Home Page (UI):**
```
GET /
```

2. **Ask a Question:**
```
POST /ask

Request:
{
  "question": "What is artificial intelligence?"
}

Response:
{
  "answer": "Artificial Intelligence refers to...",
  "score": 0.98
}
```

---

## 🐳 Docker Deployment

1. **Build the Docker Image:**
```bash
$ docker build -t ai-literacy-chatbot .
```

2. **Run the Docker Container:**
```bash
$ docker run -p 5000:5000 ai-literacy-chatbot
```

3. **Access the UI:**
```
http://localhost:5000
```

---

## 📊 Performance Optimization

1. Use GPU acceleration with **CUDA** for faster model inference.
2. Optimize document search using ChromaDB's vector search capabilities.

---

## 📈 Future Improvements

1. **Enhanced Document Search**: Implement fuzzy search for partial queries.
2. **Scalability**: Integrate with larger models for more accurate answers.
3. **Fine-Tuning**: Fine-tune BERT on domain-specific datasets.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License**.

