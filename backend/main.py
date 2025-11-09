"""
SREnity FastAPI Backend - Streaming Analysis API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json
import re
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

# Add notebooks directory to path to import run.py
notebooks_dir = backend_dir / "notebooks"
sys.path.insert(0, str(notebooks_dir))

from run import analyze_scenario_stream
from runbook_service import search_runbooks_with_metadata


TARGET_SECTION_TITLES = {
    "root cause analysis": "Root Cause Analysis",
    "impact assessment": "Impact Assessment",
    "remediation plan": "Remediation Plan",
}


def _extract_summary_sections(summary: str):
    """
    Extract only the sections whose headings match the target titles.
    Returns both the filtered markdown and structured section content.
    """
    if not summary:
        return summary, []

    lines = summary.splitlines()
    heading_pattern = re.compile(r"^#{1,6}\s*(.+)$")

    sections = []
    current_section = None

    def _normalize_title(title_text: str) -> str:
        # Remove numeric prefixes like "4." or "##"
        normalized = re.sub(r"^\d+\.\s*", "", title_text).strip()
        return normalized

    def _match_target(title_text: str):
        normalized = _normalize_title(title_text).lower()
        for key, display in TARGET_SECTION_TITLES.items():
            if key in normalized:
                return display
        return None

    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped:
            if current_section is not None:
                current_section["content_lines"].append("")
            continue

        heading_match = heading_pattern.match(stripped)
        if heading_match:
            matched_title = _match_target(heading_match.group(1))
            if matched_title:
                current_section = {
                    "title": matched_title,
                    "content_lines": []
                }
                sections.append(current_section)
            else:
                current_section = None
            continue

        if current_section is not None:
            current_section["content_lines"].append(stripped)

    if not sections:
        return summary, []

    filtered_output_lines = []
    structured_sections = []

    for section in sections:
        filtered_output_lines.append(f"### {section['title']}")
        filtered_output_lines.extend(section["content_lines"])

        structured_sections.append({
            "title": section["title"],
            "content": "\n".join(section["content_lines"]).strip()
        })

    filtered_summary = "\n".join(filtered_output_lines).strip()
    return filtered_summary, structured_sections

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
    
    Directly calls run.py analyze_scenario_stream function and passes through output
    """
    async def event_generator():
        try:
            # Use default scenario (cache incident)
            scenario = "scenario4_cache_issue"
            
            # Stream from run.py and pass through output directly
            rca_data = None
            async for update in analyze_scenario_stream(scenario=scenario, query=request.query):
                # Yield status strings as-is
                if isinstance(update, str):
                    yield f"data: {json.dumps({'type': 'status', 'message': update})}\n\n"
                
                # Pass through RCA results directly from run.py with complete output
                elif isinstance(update, dict) and update.get('type') == 'rca_complete':
                    rca_data = update.get('rca')
                    if rca_data:
                        summary_text = rca_data.get('summary', '') or rca_data.get('root_cause', '')
                        filtered_summary, structured_sections = _extract_summary_sections(summary_text)
                        if filtered_summary:
                            rca_data['summary'] = filtered_summary
                            rca_data['root_cause'] = filtered_summary
                            rca_data['summary_sections'] = structured_sections
                            update['rca']['summary'] = filtered_summary
                            update['rca']['root_cause'] = filtered_summary
                            update['rca']['summary_sections'] = structured_sections
                    # Pass through complete output from run.py (includes full summary and all results)
                    yield f"data: {json.dumps(update)}\n\n"
                    
                    # Phase 2: Runbook RAG Search
                    if rca_data:
                        yield f"data: {json.dumps({'type': 'status', 'message': 'Searching runbooks for resolution steps...'})}\n\n"
                        
                        try:
                            # Use full summary for runbook search (not truncated root_cause)
                            search_query = rca_data.get('summary', '') or rca_data.get('root_cause', '')
                            runbook_results = await search_runbooks_with_metadata(
                                rca_recommendations=rca_data.get('recommendations', []),
                                root_cause=search_query[:1000] if search_query else '',  # Use first 1000 chars for search
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
            "X-Accel-Buffering": "no",
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

