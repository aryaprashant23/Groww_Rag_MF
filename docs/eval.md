# Evaluation Strategy (Eval): Mutual Fund FAQ Assistant

This document defines the evaluation criteria and testing methodologies for each phase of the `implementationplan.md`. It ensures that the system strictly adheres to the architectural constraints, specifically regarding the Groq LLM, BGE embeddings, and the 5 Groww URLs.

---

## Phase 1: Environment Setup & Data Ingestion
**Objective:** Ensure complete, clean, and accurate data extraction exclusively from the 5 approved sources.

### Evaluation Criteria:
- [ ] **Extraction Completeness:** The scraper successfully retrieves HTML from all 5 Groww URLs (no 403 Forbidden or CAPTCHA blocks).
- [ ] **Data Cleanliness:** Manual review of a random sample of chunks confirms that navigation bars, footers, ads, and irrelevant HTML tags are completely removed.
- [ ] **Metadata Accuracy:** 100% of chunks in the Vector DB have the correct Groww source URL attached to their metadata.
- [ ] **Vector DB Integrity:** The BGE embedding model successfully processes all chunks without token limit errors, and the Vector DB (ChromaDB/FAISS) can be queried programmatically.

---

## Phase 2: Input Guardrails & Intent Classification
**Objective:** Validate that the system successfully blocks restricted inputs (PII and subjective queries) with minimal false positives.

### Evaluation Criteria:
- [ ] **PII Filter Accuracy (True Positives):** A test suite of 20 queries containing dummy PANs, Aadhaar numbers, and emails must be blocked 100% of the time.
- [ ] **Intent Classifier Accuracy:** A test suite of 30 queries (15 factual, 15 advisory/subjective) is run. The classifier must achieve >95% accuracy in blocking advisory queries ("Which is better?") while allowing factual queries ("What is the exit load?").
- [ ] **Refusal Formatting:** All blocked queries must return a polite refusal response that explicitly includes an educational link to AMFI or SEBI.

---

## Phase 3: Core RAG Retrieval & Generation (Backend)
**Objective:** Validate the accuracy of BGE retrieval and the strict output constraints of the Groq LLM.

### Evaluation Criteria:
- [ ] **Retrieval Precision:** For 20 ground-truth factual questions, the BGE Semantic Retriever must return the chunk containing the correct answer within the top-3 results at least 90% of the time.
- [ ] **Hallucination Rate:** For the 20 factual questions, the Groq LLM must generate answers that are 100% supported by the retrieved context (0% hallucination).
- [ ] **Sentence Constraint:** 100% of the generated responses must be exactly 3 sentences or fewer.
- [ ] **Citation & Footer Constraint:** 100% of the generated responses must contain exactly one Groww citation link (extracted from the chunk metadata) and the exact footer string: `Last updated from sources: <date>`.
- [ ] **Out-of-Corpus Handling:** When asked about a fund outside the 5 selected schemes (e.g., "HDFC Flexi Cap"), the LLM must explicitly state it cannot answer, rather than hallucinating.

---

## Phase 4: Minimal User Interface (Frontend)
**Objective:** Ensure the UI meets the minimalistic and compliance requirements.

### Evaluation Criteria:
- [ ] **Disclaimer Visibility:** The disclaimer **"Facts-only. No investment advice."** is prominently displayed and cannot be hidden.
- [ ] **Example Queries Functionality:** Clicking the 3 example queries correctly populates the input field and triggers an end-to-end response.
- [ ] **End-to-End Latency:** The time from user submission to the final UI render (including BGE retrieval and Groq generation) averages less than 3 seconds.
- [ ] **Error Handling:** The UI gracefully handles API timeouts (e.g., Groq rate limits) by displaying a user-friendly error message.

---

## Phase 5: Testing & Validation (User Acceptance Testing)
**Objective:** Final sign-off before deployment.

### Evaluation Criteria:
- [ ] **Golden Dataset Pass Rate:** Run an automated evaluation script against a "Golden Dataset" of 50 varied queries. The pass rate (measured by correct facts, sentence limits, and citations) must be >95%.
- [ ] **Red-Teaming Sign-Off:** A human tester attempts to jailbreak the system or bypass the PII filter for 30 minutes. The system must successfully defend against all attacks without leaking PII or giving financial advice.
