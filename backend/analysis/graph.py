"""
Multi-layer LangGraph with all tools as separate nodes.

Architecture:
- Layer 1: Router - Routes log files directly to their corresponding tools
  * web.log to web_tool
  * app.log to app_tool  
  * db.log to db_tool
  No keyword searching needed - direct file-to-tool routing

- Layer 2: Tool Nodes - web_tool, app_tool, db_tool (separate nodes)
  Each tool receives its log file directly without extraction

- Layer 3: Aggregator - Collects results from all tools
- Layer 4: Summarizer - Creates final summary
"""
from typing import Annotated, List
import operator
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, AIMessage
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class MultiLayerState(TypedDict):
    """State for multi-layer log analysis graph"""
    messages: Annotated[List[BaseMessage], operator.add]
    web_log: str  # Web tier logs directly from web.log
    app_log: str  # App tier logs directly from app.log
    db_log: str   # DB tier logs directly from db.log
    cache_log: str  # Cache tier (Redis) logs directly from cache.log
    web_result: str
    app_result: str
    db_result: str
    cache_result: str
    next: str  # Incident manager decision: "web_tool", "app_tool", "db_tool", "cache_tool", "aggregate"
    tool_results: dict  # Store all tool results


def create_incident_manager_node():
    """
    Layer 1: Incident manager node that decides which tools to use.
    Directly routes based on available log files - no keyword searching needed.
    No LLM needed - simple logic based on log file availability.
    """
    def incident_manager_node(state: MultiLayerState):
        """Route logs to the appropriate tool based on available log files"""
        # Get separate log files
        web_log = state.get("web_log", "").strip()
        app_log = state.get("app_log", "").strip()
        db_log = state.get("db_log", "").strip()
        
        cache_log = state.get("cache_log", "").strip()
        
        # Check what's already been done
        web_done = bool(state.get("web_result"))
        app_done = bool(state.get("app_result"))
        db_done = bool(state.get("db_result"))
        cache_done = bool(state.get("cache_result"))
        
        # Check which log files are available
        has_web_log = bool(web_log)
        has_app_log = bool(app_log)
        has_db_log = bool(db_log)
        has_cache_log = bool(cache_log)
        
        # If all available tools are done, go to aggregate
        if (
            (not has_web_log or web_done)
            and (not has_app_log or app_done)
            and (not has_db_log or db_done)
            and (not has_cache_log or cache_done)
        ):
            return {"next": "aggregate"}
        
        # Route to first available and undone tool
        # Priority: web -> app -> db -> cache
        if has_web_log and not web_done:
            return {"next": "web_tool"}
        elif has_app_log and not app_done:
            return {"next": "app_tool"}
        elif has_db_log and not db_done:
            return {"next": "db_tool"}
        elif has_cache_log and not cache_done:
            return {"next": "cache_tool"}
        else:
            # All available tools done, go to aggregate
            return {"next": "aggregate"}
    
    return incident_manager_node


def create_web_tool_node(web_rag_tool):
    """
    Layer 2: Web tool node - executes web RAG analysis.
    Directly uses web.log content - no extraction needed.
    """
    def web_tool_node(state: MultiLayerState):
        """Execute web tier analysis"""
        # Get web log directly from state
        web_logs = state.get("web_log", "")
        
        if not web_logs.strip():
            return {
                "web_result": "No web logs available",
                "messages": [AIMessage(content="Web Tier Analysis: No web logs available", name="web_tool")],
                "next": "incident_manager"
            }
        
        # Use web RAG tool directly with web.log content
        result = web_rag_tool.invoke(web_logs[:5000] if len(web_logs) > 5000 else web_logs)
        
        return {
            "web_result": result,
            "messages": [AIMessage(content=f"Web Tier Analysis:\n{result}", name="web_tool")],
            "next": "incident_manager"
        }
    
    return web_tool_node


def create_app_tool_node(app_rag_tool):
    """
    Layer 2: App tool node - executes app RAG analysis.
    Directly uses app.log content - no extraction needed.
    """
    def app_tool_node(state: MultiLayerState):
        """Execute app tier analysis"""
        # Get app log directly from state
        app_logs = state.get("app_log", "")
        
        if not app_logs.strip():
            return {
                "app_result": "No app logs available",
                "messages": [AIMessage(content="App Tier Analysis: No app logs available", name="app_tool")],
                "next": "incident_manager"
            }
        
        # Use app RAG tool directly with app.log content
        result = app_rag_tool.invoke(app_logs[:5000] if len(app_logs) > 5000 else app_logs)
        
        return {
            "app_result": result,
            "messages": [AIMessage(content=f"App Tier Analysis:\n{result}", name="app_tool")],
            "next": "incident_manager"
        }
    
    return app_tool_node


def create_db_tool_node(db_rag_tool):
    """
    Layer 2: DB tool node - executes db RAG analysis.
    Directly uses db.log content - no extraction needed.
    """
    def db_tool_node(state: MultiLayerState):
        """Execute db tier analysis"""
        # Get db log directly from state
        db_logs = state.get("db_log", "")
        
        if not db_logs.strip():
            return {
                "db_result": "No db logs available",
                "messages": [AIMessage(content="DB Tier Analysis: No db logs available", name="db_tool")],
                "next": "incident_manager"
            }
        
        # Use db RAG tool directly with db.log content
        result = db_rag_tool.invoke(db_logs[:5000] if len(db_logs) > 5000 else db_logs)
        
        return {
            "db_result": result,
            "messages": [AIMessage(content=f"DB Tier Analysis:\n{result}", name="db_tool")],
            "next": "incident_manager"
        }
    
    return db_tool_node


def create_cache_tool_node(cache_rag_tool):
    """
    Layer 2: Cache tool node - executes Redis cache RAG analysis.
    """
    def cache_tool_node(state: MultiLayerState):
        """Execute cache tier analysis"""
        cache_logs = state.get("cache_log", "")
        
        if not cache_logs.strip():
            return {
                "cache_result": "No cache logs available",
                "messages": [AIMessage(content="Cache Tier Analysis: No cache logs available", name="cache_tool")],
                "next": "incident_manager"
            }
        
        query_text = cache_logs[:5000] if len(cache_logs) > 5000 else cache_logs
        result = cache_rag_tool.invoke({"query": query_text})
        
        return {
            "cache_result": result,
            "messages": [AIMessage(content=f"Cache Tier Analysis:\n{result}", name="cache_tool")],
            "next": "incident_manager"
        }
    
    return cache_tool_node


def create_aggregator_node():
    """
    Layer 3: Aggregator node - collects all tool results.
    """
    def aggregator_node(state: MultiLayerState):
        """Aggregate all tool results"""
        results = {}
        if state.get("web_result"):
            results["web"] = state["web_result"]
        if state.get("app_result"):
            results["app"] = state["app_result"]
        if state.get("db_result"):
            results["db"] = state["db_result"]
        if state.get("cache_result"):
            results["cache"] = state["cache_result"]
        
        # Combine results
        combined = "\n\n".join([
            f"=== {tier.upper()} TIER ===\n{result}"
            for tier, result in results.items()
        ])
        
        return {
            "tool_results": results,
            "messages": [AIMessage(content=f"Aggregated Results:\n{combined}", name="aggregator")],
            "next": "summarizer"  # Go to summarizer
        }
    
    return aggregator_node


def create_summarizer_node(llm: ChatOpenAI):
    """
    Layer 4: Summarizer node - creates final comprehensive summary.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a senior observability engineer creating comprehensive incident summaries.
        
Create a final summary that includes:
1. Executive Summary: High-level overview
2. Tier Analysis: Key findings from each tier (web, app, db, cache)
3. Cross-Tier Correlations: How issues relate across tiers
4. Root Cause Analysis: Unified root cause
5. Impact Assessment: Overall system impact
6. Remediation Plan: Prioritized action items
7. Prevention Recommendations: How to prevent similar incidents

Be concise but comprehensive. Focus on actionable insights."""),
        ("human", "Below are the aggregated analysis results:\n\n{aggregated_results}\n\nCreate a comprehensive final summary.")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    def summarizer_node(state: MultiLayerState):
        """Create final summary"""
        aggregated = state.get("tool_results", {})
        
        if not aggregated:
            return {
                "messages": [AIMessage(content="No results to summarize.", name="summarizer")],
                "next": "FINISH"
            }
        
        # Format aggregated results
        formatted = "\n\n".join([
            f"=== {tier.upper()} TIER ===\n{result}"
            for tier, result in aggregated.items()
        ])
        
        # Generate summary
        summary = chain.invoke({"aggregated_results": formatted})
        
        return {
            "messages": [AIMessage(content=f"# FINAL INCIDENT SUMMARY\n\n{summary}", name="summarizer")],
            "next": "FINISH"
        }
    
    return summarizer_node


def build_multi_layer_graph(
    incident_manager_node,
    web_tool_node,
    app_tool_node,
    db_tool_node,
    cache_tool_node,
    aggregator_node,
    summarizer_node
):
    """
    Build multi-layer LangGraph with all tools as separate nodes.
    
    Architecture:
    Layer 1: Router - decides which tool to use
    Layer 2: Tool Nodes - web_tool, app_tool, db_tool (separate nodes)
    Layer 3: Aggregator - collects all results
    Layer 4: Summarizer - creates final summary
    
    Args:
        router_node: Router node function
        web_tool_node: Web tool node function
        app_tool_node: App tool node function
        db_tool_node: DB tool node function
        aggregator_node: Aggregator node function
        summarizer_node: Summarizer node function
    
    Returns:
        Compiled LangGraph
    """
    graph = StateGraph(MultiLayerState)
    
    # Add all nodes
    graph.add_node("incident_manager", incident_manager_node)
    graph.add_node("web_tool", web_tool_node)
    graph.add_node("app_tool", app_tool_node)
    graph.add_node("db_tool", db_tool_node)
    graph.add_node("cache_tool", cache_tool_node)
    graph.add_node("aggregate", aggregator_node)
    graph.add_node("summarizer", summarizer_node)
    
    # Set entry point
    graph.set_entry_point("incident_manager")
    
    # Router can route to tools or aggregate
    graph.add_conditional_edges(
        "incident_manager",
        lambda x: x.get("next", "aggregate"),
        {
            "web_tool": "web_tool",
            "app_tool": "app_tool",
            "db_tool": "db_tool",
            "cache_tool": "cache_tool",
            "aggregate": "aggregate",
        },
    )
    
    # Tools go back to router
    graph.add_edge("web_tool", "incident_manager")
    graph.add_edge("app_tool", "incident_manager")
    graph.add_edge("db_tool", "incident_manager")
    graph.add_edge("cache_tool", "incident_manager")
    
    # Aggregator goes to summarizer
    graph.add_edge("aggregate", "summarizer")
    
    # Summarizer goes to END
    graph.add_edge("summarizer", END)
    
    return graph.compile()

