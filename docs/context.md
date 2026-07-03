# Project Context: Mutual Fund FAQ Assistant

## 1. Domain & Purpose
This project is a Retrieval-Augmented Generation (RAG) assistant designed to answer factual, objective questions about mutual fund schemes. The primary context is modeled around Groww's product environment, aimed at retail investors and customer support teams.

## 2. Core Operational Rules
The assistant must adhere strictly to the following rules when generating responses:
- **Facts-Only**: Responses must be 100% objective and verifiable.
- **No Advice**: Absolutely no investment advice, opinions, performance comparisons, or return calculations.
- **Length Constraint**: Responses must be concise, limited to a maximum of **3 sentences**.
- **Citation**: Every response must include **exactly one** valid source link.
- **Footer**: Every response must end with the exact text: `Last updated from sources: <date>`.

## 3. Handling Out-of-Scope Queries (Refusal Policy)
If a user asks for investment advice, opinions, or subjective comparisons (e.g., "Which fund is better?" or "Should I invest?"):
- The system must trigger a **Refusal Response**.
- The refusal must be polite, clearly state the facts-only limitation, and provide an official educational link (e.g., AMFI or SEBI).

## 4. Data Corpus & Sources
The RAG retrieval system must exclusively use the provided Groww scheme URLs. No PDFs or other external websites (such as AMC, AMFI, or SEBI) are permitted.

The corpus focuses strictly on the following 5 Groww URLs:
1. [Nippon India Small Cap Fund Direct Growth](https://groww.in/mutual-funds/nippon-india-small-cap-fund-direct-growth)
2. [Nippon India Large Cap Fund Direct Growth](https://groww.in/mutual-funds/nippon-india-large-cap-fund-direct-growth)
3. [Nippon India Multi Cap Fund Direct Growth](https://groww.in/mutual-funds/nippon-india-multi-cap-fund-direct-growth)
4. [Nippon India Growth Mid Cap Fund Direct Growth](https://groww.in/mutual-funds/nippon-india-growth-mid-cap-fund-direct-growth)
5. [Nippon India Silver ETF FOF Direct Growth](https://groww.in/mutual-funds/nippon-india-silver-etf-fof-direct-growth)

## 5. Security & Privacy
The system operates under strict data privacy constraints. It must not collect, process, or store:
- PAN or Aadhaar numbers
- Account numbers
- OTPs
- Email addresses or phone numbers
