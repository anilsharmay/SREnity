# SREnity Backend - Minimal Scaffolding

Simple FastAPI backend for invoking the LangGraph SREAgent.

## Setup

1. Install dependencies (if not already installed):
```bash
pip install fastapi uvicorn[standard] pydantic
```

2. Run the server:
```bash
cd backend
python main.py
# Or use uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API docs at `http://localhost:8000/docs`

## Integration TODO

The `analyze` endpoint in `main.py` needs to be connected to the SREAgent:

1. Import `analyze_incident` from `agent_service.py`
2. Call it with the request query
3. Return the agent response

See `backend/agent_service.py` for the service layer that handles SREAgent initialization and invocation.

