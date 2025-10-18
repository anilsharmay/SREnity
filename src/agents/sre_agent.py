"""
SREnity Agent - LangGraph ReAct Implementation

This module contains the main SRE agent using LangGraph with a 2-node ReAct pattern.
"""

from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from src.utils.config import get_model_factory
from src.agents.tools import TOOLS


class GraphState(TypedDict):
    """State for the agent graph"""
    messages: Annotated[Sequence[BaseMessage], operator.add]


class SREAgent:
    """
    SRE Agent using LangGraph ReAct pattern with 2 tools:
    - search_runbooks: Search GitLab runbooks
    - search_web: Search web for latest updates
    """
    
    def __init__(self):
        """Initialize the SRE agent"""
        self.model_factory = get_model_factory()
        self.llm = self.model_factory.get_llm()
        self.llm_with_tools = self.llm.bind_tools(TOOLS)
        self.tool_node = ToolNode(TOOLS)
        self.graph = self._build_graph()
    
    def _assistant(self, state: GraphState):
        """
        Assistant node: Agent reasoning and tool selection
        """
        messages = state["messages"]
        
        # Add system message if this is the first message
        if len(messages) == 1 and isinstance(messages[0], HumanMessage):
            system_message = """
You are SREnity, an expert SRE (Site Reliability Engineer) assistant specialized in production incident response.

Your expertise includes:
- Infrastructure troubleshooting (Redis, PostgreSQL, Elastic, etc.)
- GitLab runbook procedures
- Production incident resolution
- DevOps best practices

TOOL USAGE RULES:
1. ALWAYS start with search_runbooks for SRE procedures and troubleshooting
2. Use search_web ONLY when:
   - Runbooks don't have the specific information needed
   - You need latest updates, CVEs, or version-specific issues
   - The query involves recent changes or breaking updates
3. REFUSE non-SRE queries politely but firmly

GUARDRAILS:
- If the query is clearly off-topic (weather, cooking, general knowledge, personal advice), respond:
  "I'm specialized in SRE incident response and can only help with infrastructure troubleshooting, runbook procedures, and production issues. Please ask about system operations or technical problems."
- Do NOT use tools for off-topic queries

Always provide clear, actionable guidance based on the information you find.
"""
            messages = [AIMessage(content=system_message)] + messages
        
        # Get response from LLM
        response = self.llm_with_tools.invoke(messages)
        
        return {"messages": [response]}
    
    def _should_continue(self, state: GraphState):
        """
        Conditional edge: Determine if tools need to be called
        """
        messages = state["messages"]
        last_message = messages[-1]
        
        # If the last message has tool calls, go to tools
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        
        # Otherwise, we're done
        return END
    
    def _build_graph(self):
        """Build and compile the LangGraph"""
        # Build the graph
        builder = StateGraph(GraphState)
        
        # Add nodes
        builder.add_node("assistant", self._assistant)
        builder.add_node("tools", self.tool_node)
        
        # Set entry point
        builder.add_edge(START, "assistant")
        
        # Add conditional edge
        builder.add_conditional_edges(
            "assistant",
            self._should_continue,
            {"tools": "tools", END: END}
        )
        
        # Add edge from tools back to assistant
        builder.add_edge("tools", "assistant")
        
        # Compile the graph
        return builder.compile()
    
    def invoke(self, query: str, verbose: bool = False):
        """
        Invoke the agent with a query
        
        Args:
            query: The user's question
            verbose: Whether to show reasoning steps
            
        Returns:
            The agent's response
        """
        # Create initial state
        initial_state = {"messages": [HumanMessage(content=query)]}
        
        # Run the graph
        result = self.graph.invoke(initial_state, config={"recursion_limit": 10})
        
        # Extract final response
        final_message = result["messages"][-1]
        
        if verbose:
            print(f"Agent reasoning steps: {len(result['messages'])} messages")
            for i, msg in enumerate(result["messages"]):
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    print(f"Step {i+1}: Called tools: {[tc['name'] for tc in msg.tool_calls]}")
                elif i == len(result["messages"]) - 1:
                    print(f"Step {i+1}: Final response")
        
        return final_message.content
    
    def get_graph_structure(self):
        """Get a string representation of the graph structure"""
        return """
Graph structure:
START → assistant → [tools or END]
              ↑          ↓
              └──────────┘

Tools available:
- search_runbooks: Search GitLab SRE runbooks
- search_web: Search web for latest updates
"""
