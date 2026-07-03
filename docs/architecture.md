# Architecture Design: Mutual Fund FAQ Assistant (RAG)

## 1. High-Level System Architecture

The Mutual Fund FAQ Assistant follows a Retrieval-Augmented Generation (RAG) pattern, fortified with strict input and output guardrails to ensure compliance with the "facts-only" and "no-advice" constraints.

```mermaid
graph TD
    User([User]) --> UI[Minimal UI]
    UI --> InputGuardrail{Input Guardrails & Intent Classifier}
    
    %% Input Guardrails
    InputGuardrail -- "Advisory / Subjective / PII" --> Refusal[Refusal Handler]
    Refusal --> UI
    InputGuardrail -- "Factual / Objective" --> QueryEmbed[Query Embedding]
    
    %% Retrieval
    QueryEmbed --> VectorDB[(Vector Database)]
    VectorDB --> Retriever[Semantic Retriever]
    
    %% Generation
    Retriever --> PromptBuilder[Prompt Builder]
    PromptBuilder --> LLM[Large Language Model (Groq Free API)]
    
    %% Formatting
    LLM --> Formatter[Response Formatter]
    Formatter -. "Enforces 3-sentence limit\nAdds Citation & Footer" .-> UI
    
    %% Data Ingestion
    subgraph Data Ingestion Pipeline
        Scheduler([Daily Scheduler]) -. "Triggers Daily" .-> Extractor
        Docs[Groww Scheme URLs] --> Extractor[Data Extractor]
        Extractor --> Chunker[Text Chunker]
        Chunker --> DocEmbed[Document Embedding]
        DocEmbed --> VectorDB
    end
```

## 2. Core Components

### 2.1. Minimal User Interface
A lightweight frontend designed to set user expectations immediately:
- Includes a welcome message.
- Prominently displays a static disclaimer: **"Facts-only. No investment advice."**
- Provides three clickable example queries to guide user behavior.

### 2.2. Input Guardrails & Intent Classifier
Before any retrieval occurs, the query passes through a strict evaluation layer:
- **PII Filter**: Rejects queries containing PAN, Aadhaar, account numbers, OTPs, or contact info.
- **Intent Classifier**: Detects subjective or comparative queries (e.g., "Which fund is better?", "Should I invest?").
- **Refusal Handler**: If a query is rejected, it returns a polite refusal reinforcing the facts-only policy and provides a link to AMFI/SEBI educational resources.

### 2.3. Data Ingestion Pipeline (Offline)
Responsible for building the factual knowledge base:
- **Sources**: Strictly limited to the following Groww scheme URLs (no PDFs or other external sources):
  1. [Nippon India Small Cap Fund Direct Growth](https://groww.in/mutual-funds/nippon-india-small-cap-fund-direct-growth)
  2. [Nippon India Large Cap Fund Direct Growth](https://groww.in/mutual-funds/nippon-india-large-cap-fund-direct-growth)
  3. [Nippon India Multi Cap Fund Direct Growth](https://groww.in/mutual-funds/nippon-india-multi-cap-fund-direct-growth)
  4. [Nippon India Growth Mid Cap Fund Direct Growth](https://groww.in/mutual-funds/nippon-india-growth-mid-cap-fund-direct-growth)
  5. [Nippon India Silver ETF FOF Direct Growth](https://groww.in/mutual-funds/nippon-india-silver-etf-fof-direct-growth)
- **Extraction**: Text extraction exclusively from the provided Groww HTML pages.
- **Chunking**: Splitting documents into manageable segments. Each chunk tightly couples the text with its source URL metadata.
- **Vector Storage**: Chunks are embedded and stored in a vector database for rapid semantic search.

### 2.4. Retrieval System
- Converts the approved, factual user query into a vector embedding.
- Retrieves the top highly relevant chunks from the Vector Database to serve as context for the LLM.

### 2.5. Generation & Formatting Module (LLM - Groq Free API)
The LLM (using the Free Groq API) is prompted with a strict system instruction containing the retrieved context. The application should gracefully handle any rate limits associated with the free tier.
- **System Prompt Instructions**:
  - Answer using *only* the provided context.
  - Remain 100% objective.
- **Output Formatter**:
  - Enforces the strict maximum length of **3 sentences**.
  - Extracts the source URL from the metadata of the retrieved chunk and inserts **exactly one citation link**.
  - Appends the mandatory footer: `Last updated from sources: <date>`.

### 2.6. Automated Scheduler Component
- A cron-based or application-level scheduler (e.g., APScheduler) that triggers the Data Ingestion Pipeline once a day.
- Ensures the Vector Database is populated with the most up-to-date NAVs, expense ratios, and fund details from the Groww URLs.
- Designed to run independently of the core retrieval API to prevent blocking user requests.
