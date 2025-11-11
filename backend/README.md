# SREnity Backend

FastAPI backend service for SREnity's multi-tier incident analysis pipeline.

## Overview

The backend provides a streaming API endpoint that orchestrates LangGraph-based analysis of production incidents across web, application, database, and cache tiers.

## Architecture

- **FastAPI**: RESTful API with Server-Sent Events (SSE) for real-time streaming
- **LangGraph**: Multi-step agent orchestration for incident analysis
- **RAG Pipeline**: Knowledge-based retrieval using Qdrant vector database
- **Analysis Flow**: Incident Manager → Tier Analysis → Aggregation → RCA → Runbook Retrieval

## Setup

1. **Install dependencies** (if not already installed):
```bash
pip install -e ..
```

2. **Configure environment variables**:
```bash
# Ensure .env file exists in project root with OPENAI_API_KEY
cp ../env.example ../.env
# Edit ../.env with your API keys
```

3. **Run the server**:
```bash
python main.py
# Or use uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API docs at `http://localhost:8000/docs`

## API Endpoints

### POST `/api/analyze/stream`
Streaming analysis endpoint that processes incident queries and returns real-time updates via Server-Sent Events (SSE).

**Request Body:**
```json
{
  "alert_id": "optional-alert-id",
  "service_id": "optional-service-id",
  "query": "Incident description or query"
}
```

**Response:** Server-Sent Events stream with the following event types:
- `status`: Progress updates
- `rca_complete`: Root cause analysis results
- `runbook_complete`: Runbook recommendations
- `error`: Error messages

## Key Components

### `main.py`
FastAPI application with streaming endpoint that orchestrates the analysis pipeline.

### `analysis/graph.py`
LangGraph definition for multi-tier analysis:
- Incident Manager node (routing)
- Tier-specific RAG tools (web, app, db, cache)
- Aggregator node
- Summarizer node (RCA generation)
- Runbook node (remediation guidance)

### `analysis/tools/`
RAG tools for each tier that retrieve relevant incident patterns from the knowledge base.

### `runbook_service.py`
Service for retrieving relevant runbook procedures based on RCA recommendations.

### `data/`
- `logs/`: Log scenarios for testing different incident types
- `knowledge_base/`: Incident patterns and runbook documentation

## Development

The backend uses LangGraph to orchestrate a multi-step analysis pipeline:

1. **Incident Manager**: Routes analysis to appropriate tier tools based on query
2. **Tier Analysis**: Parallel analysis of logs using RAG tools with knowledge base
3. **Aggregation**: Combines findings from all analyzed tiers
4. **RCA Generation**: Creates structured root cause analysis
5. **Runbook Retrieval**: Finds relevant remediation procedures

## Testing

Test scenarios are available in `backend/data/logs/`:
- `scenario1_web_issue/`: Web tier incidents
- `scenario2_app_issue/`: Application tier incidents
- `scenario3_db_issue/`: Database tier incidents
- `scenario4_cache_issue/`: Cache tier incidents

Run analysis:
```bash
cd notebooks
python run.py scenario1_web_issue
```
