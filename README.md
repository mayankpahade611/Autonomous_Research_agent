# 🔬 Autonomous Research Agent

An AI-powered research agent that autonomously plans, searches, retrieves, and synthesizes structured investment-grade research reports on any topic.

Built with **LangGraph**, **Groq (Llama 3.1)**, **Tavily**, and **Qdrant** — deployed on **Hugging Face Spaces** with a **Streamlit** frontend.

---

## 🚀 Live Demo

| Service | URL |
|---------|-----|
| 🖥️ Frontend (Streamlit) | [your-streamlit-url.streamlit.app](https://autonomousresearchagent-py2jjwjaznw4aoz2cpdqhv.streamlit.app) |
| ⚙️ Backend API (Hugging Face) | [Phantom611-autonoumous-research-agent.hf.space](https://Phantom611-autonoumous-research-agent.hf.space) |
| 📖 API Docs | [/docs](https://Phantom611-autonoumous-research-agent.hf.space/docs) |

---

## 🧠 How It Works

The agent runs a multi-step pipeline powered by **LangGraph**:

```
Query
  │
  ▼
🗂️ Planner        → Breaks query into 3–5 research subtopics
  │
  ▼
🔍 Search         → Parallel Tavily search for each subtopic
  │
  ▼
🌐 Scraper        → Fetches and extracts content from web pages
  │
  ▼
💾 Store          → Chunks and stores documents in Qdrant vector DB
  │
  ▼
📚 Retrieve       → Hybrid search (Dense + BM25 + RRF scoring)
  │
  ▼
✍️ Summarizer     → Grounded summary from retrieved context
  │
  ▼
🧐 Critic         → Evaluates quality → loops back if needed (max 1x)
  │
  ▼
📄 Reporter       → Structured investment-style memo
```

---

## ✨ Features

- **Autonomous multi-agent pipeline** — no human-in-the-loop required
- **Parallel search** — searches all subtopics simultaneously
- **Hybrid retrieval** — combines dense vector search + BM25 with Reciprocal Rank Fusion
- **Self-critique loop** — critic agent evaluates and triggers re-research if needed
- **Grounding evaluation** — checks if the summary is supported by retrieved context
- **Structured report** — investment-style memo with sections for market, risks, outlook
- **Fast inference** — Groq's Llama 3.1 8B Instant for low-latency LLM calls

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Orchestration | LangGraph |
| LLM | Groq — Llama 3.1 8B Instant |
| Web Search | Tavily API |
| Vector Store | Qdrant Cloud |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Backend | FastAPI |
| Frontend | Streamlit |
| Backend Hosting | Hugging Face Spaces (Docker) |
| Frontend Hosting | Streamlit Cloud |

---

## 📁 Project Structure

```
autonomous-research-agent/
│
├── app/
│   ├── agents/
│   │   ├── planner.py        # Breaks query into subtopics
│   │   ├── search.py         # Parallel Tavily search
│   │   ├── scraper.py        # Async web scraping
│   │   ├── store.py          # Document ingestion
│   │   ├── retrieve.py       # Hybrid retrieval
│   │   ├── summarizer.py     # Grounded summarization
│   │   ├── critic.py         # Quality evaluation
│   │   └── reporter.py       # Final report generation
│   │
│   ├── retrieval/
│   │   ├── vector_store.py   # Qdrant vector store
│   │   ├── hybrid_retriever.py # Dense + BM25 + RRF
│   │   ├── ingest.py         # Document chunking & storage
│   │   └── embeddings.py     # Sentence transformer embeddings
│   │
│   ├── evaluation/
│   │   └── grounding.py      # Grounding check
│   │
│   ├── utils/
│   │   ├── llm.py            # Groq LLM client (cached)
│   │   └── logger.py         # Event logging
│   │
│   ├── graph.py              # LangGraph pipeline definition
│   └── config.py             # Settings & env vars
│
├── main.py                   # FastAPI app
├── streamlit_app.py          # Streamlit frontend
├── Dockerfile                # Hugging Face deployment
├── requirements.txt
└── README.md
```

---

## 🔧 Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/mayankpahade611/autonomous-research-agent.git
cd autonomous-research-agent
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
```

### 5. Run the backend
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Run the frontend (in a new terminal)
```bash
streamlit run streamlit_app.py
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Service status |
| POST | `/research-plan` | Generate research report |
| POST | `/ingest` | Ingest a document |
| POST | `/query` | RAG query |

### Example Request

```bash
curl -X POST "https://Phantom611-autonoumous-research-agent.hf.space/research-plan" \
  -H "Content-Type: application/json" \
  -d '{"query": "latest trends in AI agents 2026"}'
```

### Example Response

```json
{
  "final_report": "## Executive Summary\n...",
  "iterations": 2,
  "retrieved_chunks": 5,
  "execution_time_seconds": 36.8,
  "grounding_check": "PARTIALLY_GROUNDED"
}
```

---

## 🚢 Deployment

### Backend — Hugging Face Spaces (Docker)

1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select **Docker** as the SDK
3. Add secrets in Space Settings:
   ```
   GROQ_API_KEY
   TAVILY_API_KEY
   QDRANT_URL
   QDRANT_API_KEY
   ```
4. Push your code:
   ```bash
   git remote add space https://huggingface.co/spaces/YOUR_USERNAME/your-space-name
   git push space main --force
   ```

### Frontend — Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repo
3. Set main file as `streamlit_app.py`
4. Deploy

---

## ⚡ Performance

| Metric | Value |
|--------|-------|
| Average response time | ~35-40s |
| Max iterations | 2 |
| Search results per subtopic | 2 |
| Retrieved chunks | 5 |
| Embedding model | all-MiniLM-L6-v2 (384 dims) |

---

## 🔑 Getting API Keys

| Service | Link | Free Tier |
|---------|------|-----------|
| Groq | [console.groq.com](https://console.groq.com) | ✅ Free |
| Tavily | [tavily.com](https://tavily.com) | ✅ 1000 searches/month |
| Qdrant | [cloud.qdrant.io](https://cloud.qdrant.io) | ✅ 1GB free cluster |

---

