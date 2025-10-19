"""
SREnity Agent - LangGraph ReAct Implementation

This module contains the main SRE agent using LangGraph with a 2-node ReAct pattern.
"""

from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
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
        
        # Initialize database components
        from src.utils.database_utils import create_database_components
        from src.agents.tools import initialize_tools_with_database
        
        print("🔄 Initializing SRE agent database components...")
        self.vector_store, self.chunked_docs = create_database_components()
        initialize_tools_with_database(self.vector_store, self.chunked_docs)
        print("✅ Database components initialized")
        
        # Now create tools and LLM
        from src.agents.tools import TOOLS
        self.llm = self.model_factory.get_llm()
        self.llm_with_tools = self.llm.bind_tools(TOOLS)
        self.tool_node = ToolNode(TOOLS)
        self.graph = self._build_graph()
        print("✅ SRE agent ready!")
    
    def _assistant(self, state: GraphState):
        """
        Assistant node: Agent reasoning and tool selection
        """
        messages = state["messages"]
        
        # Check if we're processing a tool result (after tool execution)
        if len(messages) >= 2:
            last_message = messages[-1]
            prev_message = messages[-2]
            
            # If previous message was a tool call and current is a tool result
            if (hasattr(prev_message, 'tool_calls') and 
                hasattr(last_message, 'type') and 
                last_message.type == 'tool'):
                
                # Extract tool name and result
                tool_name = prev_message.tool_calls[0]['name']
                tool_result = last_message.content
                
                # For search_runbooks, return raw output without LLM processing
                if tool_name == 'search_runbooks':
                    return {"messages": [AIMessage(content=tool_result)]}
        
        # Add system message if this is the first message
        if len(messages) == 1 and isinstance(messages[0], HumanMessage):
            system_message = """
You are SREnity, an expert SRE (Site Reliability Engineer) assistant specialized in production incident response.

CRITICAL: FIRST check if the query is related to technology, infrastructure, or software engineering. If NOT, refuse immediately without using any tools.

BEFORE doing anything else, ask yourself: "Is this question about technology, infrastructure, software engineering, SRE, DevOps, or technical concepts?" If NO, respond with: "I'm specialized in SRE incident response and can only help with infrastructure troubleshooting, runbook procedures, and production issues. Please ask about system operations or technical problems."

REFUSE these types of queries immediately:
- Food, restaurants, cooking (e.g., "what is chipotle", "how to cook pasta")
- Weather, travel, entertainment
- Personal advice, relationships, health
- General knowledge unrelated to technology (e.g., "who is ceo of google", "what is the capital of france")
- Business information, company details, stock prices
- Non-technical topics

ONLY answer questions about:
- Technology concepts and definitions (e.g., "what is elasticsearch", "what is kubernetes")
- SRE concepts, DevOps, infrastructure, troubleshooting
- System operations, technical methodologies
- Production incident response, runbook procedures
- Technology stack questions (Redis, PostgreSQL, Elastic, etc.)

TOOL USAGE RULES:
1. Start with search_runbooks for SRE procedures and troubleshooting
2. Use search_web for latest updates, CVEs, or version-specific issues that runbooks don't cover
3. Do NOT use tools for off-topic queries - refuse them first

Always provide clear, actionable guidance for technical questions only.
"""
            messages = [SystemMessage(content=system_message)] + messages
        
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
