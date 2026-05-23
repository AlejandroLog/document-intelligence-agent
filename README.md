# Agentic RAG Platform & Data Lake 🤖📊

An enterprise-grade, containerized Retrieval-Augmented Generation (RAG) system powered by Agentic AI. This platform automates the ingestion, processing, and semantic indexing of unstructured documents (PDF/DOCX) using a robust 3-layer Data Lake architecture.

Unlike standard LLM wrappers, this system relies on a cognitive agent that autonomously decides which tools to use (Semantic Search, Summarization, Entity Extraction) while strictly grounding its answers in the provided private context to eliminate hallucinations.

## 🌟 Key Features

* **3-Layer Data Lake Architecture:**
  * **RAW (MinIO):** Immutable storage for original binary files.
  * **STAGING (MinIO):** Normalized plain-text extraction using automated pipelines.
  * **CURATED (ChromaDB):** Advanced text chunking and semantic vector indexing.
* **Agentic AI Core:** Powered by LangChain and OpenAI, featuring conversational memory and multi-step reasoning.
* **Smart Data Pipelines:** Intelligent document chunking with semantic overlap preservation.
* **Interactive UI:** Built with Streamlit for drag-and-drop document uploads, visual pipeline monitoring, and real-time chat.
* **Containerized Infrastructure:** Isolated and reproducible environments deployed via Docker Compose.

## 🛠️ Tech Stack

* **AI & NLP:** LangChain, OpenAI API, ChromaDB Vector Store
* **Data Engineering:** MinIO (S3 Object Storage), PyPDF, Python-Docx
* **Backend & Infra:** Python, Docker, PostgreSQL
* **Frontend:** Streamlit

## 🚀 Getting Started

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Python 3.10+
* An active OpenAI API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/agentic-rag-datalake.git](https://github.com/your-username/agentic-rag-datalake.git)
   cd agentic-rag-datalake
