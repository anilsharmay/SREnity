"""
Service layer for SREAgent integration
"""
from src.agents.sre_agent import SREAgent
from langchain_core.messages import HumanMessage

# Singleton instance
_agent_instance = None

def get_agent() -> SREAgent:
    """Get or create SREAgent instance (singleton)"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = SREAgent()
    return _agent_instance

def analyze_incident(query: str) -> str:
    """
    Analyze an incident using the SREAgent
    
    Args:
        query: Incident description or question
        
    Returns:
        Agent response as string
    """
    agent = get_agent()
    
    # Invoke the agent graph with the query
    messages = [HumanMessage(content=query)]
    result = agent.graph.invoke({"messages": messages})
    
    # Extract final response from messages
    # TODO: Handle the response format appropriately
    if result["messages"]:
        last_message = result["messages"][-1]
        return last_message.content if hasattr(last_message, 'content') else str(last_message)
    
    return "No response generated"

