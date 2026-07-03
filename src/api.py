from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Ensure we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from guardrails import GuardrailManager
from rag_pipeline import RAGPipeline

app = FastAPI(
    title="Mutual Fund FAQ API",
    description="Backend API for the RAG-powered Mutual Fund Assistant",
    version="1.0.0"
)

# Configure CORS to allow the React frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact origin of the Vite frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize backend models
print("Initializing Guardrails and RAG Pipeline...")
guardrails = GuardrailManager()
pipeline = RAGPipeline()
print("Backend fully initialized!")

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    raw_answer: str

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Receives a user query, processes it through the Guardrails, and if valid,
    passes it to the RAG Pipeline for a factual response.
    """
    query = request.query.strip()
    if not query:
        return ChatResponse(
            answer="Please provide a valid query.",
            sources=[],
            raw_answer=""
        )

    # Step 1: Guardrails Verification (PII & Intent)
    is_valid, refusal_msg = guardrails.validate_query(query)
    
    if not is_valid:
        return ChatResponse(
            answer=refusal_msg,
            sources=[],
            raw_answer=""
        )
        
    # Step 2: RAG Pipeline Generation
    result = pipeline.get_answer(query)
    
    return ChatResponse(
        answer=result.get("answer", ""),
        sources=result.get("sources", []),
        raw_answer=result.get("raw_answer", "")
    )

if __name__ == "__main__":
    import uvicorn
    # Allow running directly via `python src/api.py`
    uvicorn.run(app, host="0.0.0.0", port=8001)
