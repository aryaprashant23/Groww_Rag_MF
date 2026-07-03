# Implementation Plan: Mutual Fund FAQ Assistant

This document outlines the step-by-step implementation strategy for the Mutual Fund RAG Assistant, based on the strict data boundaries defined in the architecture and the chosen technology stack.

## Technology Stack Specifications
- **LLM Provider**: Groq (Free API Tier)
- **Embedding Model**: BGE Small model (`BAAI/bge-small-en-v1.5`) via HuggingFace (Optimized for smaller chunks and faster local execution)
- **Vector Database**: ChromaDB (or FAISS)
- **Frontend Framework**: Streamlit (or Gradio)
- **Environment Management**: `python-dotenv` (for managing Free Groq API Key)

---

## Phase 1: Environment Setup & Data Ingestion (Offline Pipeline)
**Goal:** Extract data strictly from the 5 approved Groww URLs and build the vector database.

1. **Project Setup**
   - Initialize Python environment (`venv`).
   - Install core dependencies: `langchain`, `langchain-groq`, `langchain-community`, `sentence-transformers` (for BGE model), `chromadb`, `beautifulsoup4`, and `python-dotenv`.
   - Setup `.env` file to securely store the `GROQ_API_KEY`.
2. **Web Scraping**
   - Write a script to fetch the HTML content exclusively from the 5 selected Nippon India Groww scheme URLs.
   - Clean the HTML (removing navbars, footers, and ads) to extract pure factual text.
3. **Chunking & Metadata Tagging**
   - Split the extracted text into manageable chunks (using `RecursiveCharacterTextSplitter` with `chunk_size=500` and `chunk_overlap=50` to better isolate dense financial facts).
   - Inject the source Groww URL directly into each chunk's metadata.
4. **Vector Storage Setup**
   - Initialize the **BGE Small embedding model** (`BAAI/bge-small-en-v1.5`).
   - Generate embeddings for each chunk and persist them in a local Vector DB.

## Phase 2: Input Guardrails & Intent Classification
**Goal:** Secure the system against PII leaks and subjective queries before retrieval happens.

1. **PII Filter**
   - Implement Regex patterns to detect and block queries containing: PAN, Aadhaar, account numbers, emails, and phone numbers.
2. **Intent Classifier**
   - Implement a lightweight zero-shot classifier or heuristics-based check to detect advisory/subjective queries (e.g., "Should I invest?", "Which fund is better?").
3. **Refusal Handler**
   - Create a standard, polite refusal response for queries blocked by the guardrails.
   - Ensure the refusal includes a link to AMFI or SEBI educational resources.

## Phase 3: Core RAG Retrieval & Generation (Backend)
**Goal:** Retrieve factual context and generate constrained answers using Groq.

1. **Semantic Retriever**
   - Build a retriever function that embeds the user query using the **BGE model** and flexibly fetches the top-10 relevant chunks from the Vector DB. Given the removal of strict API constraints, retrieving 10 chunks provides ~5000 characters of context, maximizing the LLM's chance of finding the correct factual answer without hitting context window issues.
   - Implement similarity score thresholding to ensure only highly relevant chunks are retrieved.
2. **Prompt Engineering for Groq**
   - Design a strict system prompt instructing the Groq LLM to:
     - Answer *only* using the provided context chunks.
     - Keep the answer to a strict maximum of **3 sentences**.
     - Extract the exact URL from the chunk metadata.
3. **Output Formatter**
   - Validate the LLM output to ensure it includes **exactly one citation link**.
   - Dynamically append the exact footer: `Last updated from sources: <date>`.
4. **Rate Limiting & Error Handling (Groq Constraints)**
   - **Model Configuration**: Use `llama-3.3-70b-versatile`.
   - **API Limits Management**: Manage the free-tier limits (30 Req/min, 1K Req/day, 12K Tokens/min, 100K Tokens/day).
   - **Implementation Strategies**:
     - Implement retry logic with exponential backoff (e.g., using `tenacity` or LangChain built-in retries) to gracefully handle `429 Too Many Requests` errors.
     - Enable LLM caching (e.g., `langchain.globals.set_llm_cache`) to avoid redundant API calls for repeated identical queries, saving token usage and request counts.
     - Surface rate limit errors politely in the UI instead of crashing.

## Phase 4: Backend API (FastAPI)
**Goal:** Expose the RAG pipeline as a robust REST API for frontend consumption.

1. **API Initialization**
   - Setup a FastAPI application in `src/api.py`.
   - Configure CORS middleware to accept requests from the frontend.
2. **Endpoint Development**
   - Create a POST `/chat` endpoint.
   - Accept JSON payloads with a `query` string.
3. **Pipeline Integration**
   - The endpoint sequentially processes the query: Guardrails -> RAG Pipeline.
   - Returns a structured JSON response containing the answer and source links.

## Phase 5: Premium Web Frontend (React + Vite)
**Goal:** Provide a highly aesthetic, visually stunning interface.

1. **UI Framework & Architecture**
   - Scaffold a rapid single-page app using Vite + React.
2. **Premium Aesthetics (Vanilla CSS)**
   - Implement a dark mode design system with glassmorphism and modern typography (e.g., 'Inter').
   - Add micro-animations for interactivity (hover states, loading spinners, message bubbles).
3. **Components**
   - **Chat UI:** Render markdown responses and clickable source links.
   - **Interactive Examples:** Animated pill buttons for testing edge cases (NAV, Exit Load, Subjective).
   - **Disclaimer:** Prominent "Facts-only. No investment advice." banner.

## Phase 6: Testing & Validation
**Goal:** Ensure all constraints and requirements are met across the stack.

1. **Backend API Testing:** Verify the `/chat` endpoint returns the correct JSON payload.
2. **Frontend UI Testing:** Ensure the UI correctly displays the stream and handles edge cases gracefully.

## Phase 7: Automated Scheduler Component
**Goal:** Ensure the vector database remains up-to-date by triggering the data ingestion pipeline daily.

1. **Scheduler Implementation**
   - Create a GitHub Actions workflow (e.g., `.github/workflows/daily-ingestion.yml`) with a `schedule` trigger (using cron syntax) to execute the offline ingestion pipeline script (`ingest.py`) once a day.
2. **Database Overwrite/Update Logic**
   - Ensure the ingestion pipeline can seamlessly clear the existing ChromaDB collection and recreate it with freshly fetched data (or perform an upsert) without causing downtime for the backend API.
3. **Logging & Alerts**
   - Add logging to track the success or failure of the daily ingestion run, and monitor for scraping failures due to potential UI changes on the source websites.
