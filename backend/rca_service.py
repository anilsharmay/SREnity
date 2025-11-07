"""
RCA Agent Service - Interface for collaborator's LangGraph RCA agent

This module provides the interface for the Root Cause Analysis agent.
The collaborator should implement the rca_agent_analyze() function using their LangGraph agent.
"""
from typing import AsyncIterator, Optional, Dict
from langchain_core.messages import HumanMessage


async def rca_agent_analyze(
    query: str,
    alert_id: Optional[str] = None,
    service_id: Optional[str] = None
) -> AsyncIterator[str | dict]:
    """
    RCA Agent streaming interface - Compatible with LangGraph
    
    This function should be implemented by the collaborator using their LangGraph RCA agent.
    
    Requirements:
    1. Must be an async generator (yield, not return)
    2. Can yield string status updates at any time during processing
    3. Must yield a dict with type="rca_complete" when RCA is done
    4. Can use LangGraph's astream() or astream_events() internally
    
    Yields:
    - String messages: Status updates like "Retrieving logs...", "Analyzing patterns..."
    - Dict: When RCA complete:
        {
            "type": "rca_complete",
            "rca": {
                "root_cause": "Description of root cause",
                "evidence": ["Evidence 1", "Evidence 2"],
                "recommendations": ["Recommendation 1", "Recommendation 2"]
            }
        }
    
    Example using LangGraph astream():
        initial_state = {"messages": [HumanMessage(content=query)]}
        
        async for state in rca_agent.graph.astream(initial_state):
            # Process state, yield status strings
            messages = state.get("messages", [])
            if messages:
                last_msg = messages[-1]
                if hasattr(last_msg, 'tool_calls'):
                    yield f"Calling {last_msg.tool_calls[0]['name']}..."
        
        # Extract RCA from final state
        final_state = state
        rca_data = extract_rca_result(final_state)
        yield {"type": "rca_complete", "rca": rca_data}
    
    Example using LangGraph astream_events():
        initial_state = {"messages": [HumanMessage(content=query)]}
        
        async for event in rca_agent.graph.astream_events(
            initial_state,
            version="v2",
            config={"recursion_limit": 10}
        ):
            event_type = event.get("event")
            name = event.get("name")
            
            # Stream status based on events
            if event_type == "on_chain_start":
                if name == "retrieve_logs":
                    yield "Retrieving logs from monitoring system..."
                elif name == "analyze_patterns":
                    yield "Analyzing log patterns and metrics..."
            
            elif event_type == "on_chain_end":
                if name == "rca_summary":
                    # Extract RCA from event data
                    rca_data = event.get("data", {}).get("output", {})
                    yield {"type": "rca_complete", "rca": rca_data}
    """
    # TODO: Collaborator implements this using their LangGraph RCA agent
    
    # Mock implementation for testing/demo
    yield "Retrieving logs from monitoring system..."
    yield "Analyzing log patterns and metrics..."
    yield "Identifying root cause..."
    
    # Mock RCA result
    yield {
        "type": "rca_complete",
        "rca": {
            "root_cause": "Database connection pool exhaustion due to unclosed connections in application code",
            "evidence": [
                "234 timeout errors in last 15 minutes",
                "Connection pool at 100% capacity",
                "Pattern: Connections not released after queries"
            ],
            "recommendations": [
                "Restart connection pool",
                "Review application connection handling",
                "Monitor connection pool metrics"
            ]
        }
    }

