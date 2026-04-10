---
title: Codebase Explainer
emoji: 🚀
colorFrom: indigo
colorTo: purple
sdk: docker
app_file: app.py
pinned: false
---

# Codebase Explainer

An advanced AI-powered tool to explore and understand GitHub repositories using Agentic RAG (Retrieval-Augmented Generation).

## Features

- **Automated Ingestion**: Clone any public GitHub repository and index its code.
- **Intelligent Parsing**: Uses Tree-sitter for AST-based symbol extraction (functions, classes, methods).
- **Agentic Workflow**: Orchestrated by LangGraph with specialized agents:
  - **Planner**: Classifies user intent.
  - **Retrieval**: Fetches relevant code chunks from ChromaDB.
  - **Summarizer**: Fuses context into a coherent explanation using Llama 3.3.
- **Premium UI**: Modern dark-mode interface with glassmorphism and real-time feedback.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key
   HF_API_KEY=your_huggingface_api_key
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000`.

## Tech Stack

- **Backend**: Flask, LangChain, LangGraph
- **LLM**: Groq (Llama-3.3-70b-versatile)
- **Embeddings**: Local (BAAI/bge-small-en-v1.5)
- **Vector DB**: ChromaDB
- **Parsing**: Tree-sitter
- **UI**: Vanilla HTML/JS, Premium CSS
