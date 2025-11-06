"""
SREnity FastAPI Backend - Minimal Scaffolding
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="SREnity API", version="1.0.0")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    alert_id: Optional[str] = None
    service_id: Optional[str] = None
    query: str  # The incident description/query

@app.post("/api/analyze")
async def analyze(request: AnalyzeRequest):
    """
    Analyze an incident using the LangGraph SREAgent
    
    TODO: Integrate with SREAgent from src.agents.sre_agent
    """
    # TODO: Initialize SREAgent (singleton pattern recommended)
    # TODO: Invoke agent with the query
    # TODO: Return agent response
    
    return {
        "status": "pending",
        "message": "Analysis endpoint - implement agent integration here"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

