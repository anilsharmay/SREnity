"""
SREnity FastAPI Backend - Streaming Analysis API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
backend_dir = Path(__file__).parent
project_root = backend_dir.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Add project root and backend directory to path
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_dir))

from rca_service import rca_agent_analyze
from runbook_service import search_runbooks_with_metadata

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
    Legacy analyze endpoint (non-streaming)
    
    TODO: Consider deprecating in favor of /api/analyze/stream
    """
    return {
        "status": "pending",
        "message": "Use /api/analyze/stream for streaming analysis"
    }

@app.post("/api/analyze/stream")
async def analyze_stream(request: AnalyzeRequest):
    """
    Stream analysis updates via Server-Sent Events
    
    Orchestrates:
    1. RCA Agent analysis (collaborator's LangGraph agent)
    2. Runbook RAG search (using RCA recommendations)
    3. Structured results with action steps and source URLs
    """
    async def event_generator():
        try:
            rca_recommendations = None
            root_cause = None
            
            # Phase 1: RCA Analysis (stream from collaborator's agent)
            async for update in rca_agent_analyze(
                query=request.query,
                alert_id=request.alert_id,
                service_id=request.service_id
            ):
                # Yield status strings as-is
                if isinstance(update, str):
                    yield f"data: {json.dumps({'type': 'status', 'message': update})}\n\n"
                
                # Capture RCA results
                elif isinstance(update, dict) and update.get('type') == 'rca_complete':
                    yield f"data: {json.dumps(update)}\n\n"
                    rca_data = update.get('rca', {})
                    rca_recommendations = rca_data.get('recommendations', [])
                    root_cause = rca_data.get('root_cause', '')
            
            # Phase 2: Runbook RAG Search (only if RCA complete)
            if rca_recommendations and root_cause:
                yield f"data: {json.dumps({'type': 'status', 'message': 'Searching runbooks for resolution steps...'})}\n\n"
                
                try:
                    runbook_results = await search_runbooks_with_metadata(
                        rca_recommendations=rca_recommendations,
                        root_cause=root_cause,
                        max_results=3
                    )
                    
                    yield f"data: {json.dumps({
                        'type': 'runbook_complete',
                        'runbooks': runbook_results
                    })}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({
                        'type': 'error',
                        'message': f'Error searching runbooks: {str(e)}'
                    })}\n\n"
            
            # Signal completion
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable buffering for nginx
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

