# Problem Statement: Mutual Fund FAQ Assistant (Facts-Only Q&A)

## Overview
The objective of this project is to build a facts-only FAQ assistant for mutual fund schemes, using Groww as the reference product context. The assistant will answer objective, verifiable queries related to mutual funds by retrieving information exclusively from official public sources, such as AMC (Asset Management Company) websites, AMFI, and SEBI.

The system must strictly avoid providing investment advice, opinions, or recommendations. Every response must include a single, clear source link and adhere to defined constraints around clarity, accuracy, and compliance.

## Objective
Design and implement a lightweight Retrieval-Augmented Generation (RAG)-based assistant that:
- Answers factual queries about mutual fund schemes
- Uses a curated corpus of official documents
- Provides concise, source-backed responses

## Target Users
- Retail investors comparing mutual fund schemes
- Customer support and content teams handling repetitive mutual fund queries

## Scope of Work

### 1. Corpus Definition
The corpus is strictly limited to the following Groww scheme URLs (no PDFs, AMC, AMFI, or SEBI websites):
1. [Nippon India Small Cap Fund Direct Growth](https://groww.in/mutual-funds/nippon-india-small-cap-fund-direct-growth)
2. [Nippon India Large Cap Fund Direct Growth](https://groww.in/mutual-funds/nippon-india-large-cap-fund-direct-growth)
3. [Nippon India Multi Cap Fund Direct Growth](https://groww.in/mutual-funds/nippon-india-multi-cap-fund-direct-growth)
4. [Nippon India Growth Mid Cap Fund Direct Growth](https://groww.in/mutual-funds/nippon-india-growth-mid-cap-fund-direct-growth)
5. [Nippon India Silver ETF FOF Direct Growth](https://groww.in/mutual-funds/nippon-india-silver-etf-fof-direct-growth)

### 2. FAQ Assistant Requirements
The assistant must:
- Answer facts-only queries, such as:
  - Expense ratio of a scheme
  - Exit load details
  - Minimum SIP amount
  - ELSS lock-in period
  - Riskometer classification
  - Benchmark index
  - Process to download statements or capital gains reports
- Ensure:
  - Each response is limited to a maximum of 3 sentences
  - Each response includes exactly one citation link
  - Each response includes a footer:
    > "Last updated from sources: <date>"

### 3. Refusal Handling
The assistant must refuse non-factual or advisory queries, such as:
- “Should I invest in this fund?”
- “Which fund is better?”

Refusal responses should:
- Be polite and clearly worded
- Reinforce the facts-only limitation
- Provide a relevant educational link (e.g., AMFI or SEBI resource)

### 4. User Interface (Minimal)
The solution should include a simple interface with:
- A welcome message
- Three example questions
- A visible disclaimer:
  > **"Facts-only. No investment advice."**

## Constraints

### Data and Sources
- Use only the explicitly provided Groww scheme URLs.
- Do not use any external sources (e.g., AMC, AMFI, SEBI websites, factsheets, KIM, SID) or third-party blogs.

### Privacy and Security
Do not collect, store, or process:
- PAN or Aadhaar numbers
- Account numbers
- OTPs
- Email addresses or phone numbers

### Content Restrictions
- No investment advice or recommendations
- No performance comparisons or return calculations
- For performance-related queries, provide a link to the official factsheet only

### Transparency
- Responses must be short, factual, and verifiable
- Every answer must include a source link and last updated date
