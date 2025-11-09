"""
Multi-Layer LangGraph Log Analysis

Run this script to analyze logs using the multi-layer LangGraph system.
Usage: python run.py [scenario_name]

Example: python run.py scenario1_web_issue
"""
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root .env if available
_SCRIPT_PATH = Path(__file__).resolve()
_NOTEBOOKS_DIR = _SCRIPT_PATH.parent
_BACKEND_DIR = _NOTEBOOKS_DIR.parent
_PROJECT_ROOT = _BACKEND_DIR.parent
load_dotenv(_PROJECT_ROOT / ".env")

# Set OpenAI API key if not already set (fallback to interactive prompt)
if "OPENAI_API_KEY" not in os.environ:
    import getpass
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key: ")

# Read path from config
from config import BACKEND_DIR, LOGS_DIR

# Add backend parent to Python path
backend_parent = BACKEND_DIR.parent
if str(backend_parent) not in sys.path:
    sys.path.insert(0, str(backend_parent))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from backend.analysis.tools import (
    create_web_rag_tool,
    create_app_rag_tool,
    create_db_rag_tool,
    create_cache_rag_tool,
)
from backend.analysis.graph import (
    create_incident_manager_node,
    create_web_tool_node,
    create_app_tool_node,
    create_db_tool_node,
    create_cache_tool_node,
    create_aggregator_node,
    create_summarizer_node,
    build_multi_layer_graph,
    MultiLayerState
)


def load_logs(scenario="scenario1_web_issue"):
    """
    Load log files separately from logs directory.
    Returns a dictionary with separate log contents - NOT joined/combined.
    Each log file stays separate: web.log, app.log, db.log
    
    Args:
        scenario: Scenario directory name (default: "scenario1_web_issue")
    
    Returns:
        dict: Dictionary with keys 'web', 'app', 'db' containing log file contents
    """
    # Logs are in backend/data/logs/scenario/
    logs_dir = LOGS_DIR / scenario
    
    if not logs_dir.exists():
        raise FileNotFoundError(
            f"Logs directory not found: {logs_dir}\n"
            f"Available scenarios: {list(LOGS_DIR.iterdir()) if LOGS_DIR.exists() else 'No logs directory found'}"
        )
    
    # Load each log file separately - keep them separate, don't combine
    logs = {}
    for tier in ["web", "app", "db", "cache"]:
        path = logs_dir / f"{tier}.log"
        if tier == "cache" and not path.exists():
            print("Cache log missing, inserting default Redis error sample.")
            logs[tier] = """2024-01-17T09:00:01.950Z [ERROR] [trace_id:req-401-a1b2c3] [redis-node:cache-primary] [Redis] ERR max number of clients reached - exception while processing GET user:profile:12345
2024-01-17T09:00:02.012Z [WARN]  [redis-node:cache-primary] [Redis] Connected clients: 998 / maxclients: 1000 - pool almost exhausted
2024-01-17T09:00:02.145Z [ERROR] [trace_id:req-402-a2b3c4] [redis-node:cache-primary] [Redis] ConnectionError: ERR max number of clients reached (service: order-service)
2024-01-17T09:00:02.214Z [WARN]  [redis-node:cache-primary] [Redis] Slow command: HGETALL cart:session:88321 took 284ms (threshold 100ms)
2024-01-17T09:00:02.318Z [ERROR] [trace_id:req-403-a3b4c5] [redis-node:cache-primary] [Redis] BLPOP queue:notifications timeout - blocking clients: 12
2024-01-17T09:00:02.443Z [ERROR] [trace_id:req-404-a4b5c6] [redis-node:cache-primary] [Redis] Connection reset by peer - unable to allocate new client connection
2024-01-17T09:00:02.576Z [WARN]  [redis-node:cache-primary] [Redis] INFO clients: connected_clients=1000, blocked_clients=15, tracking_clients=0
2024-01-17T09:00:02.712Z [ERROR] [trace_id:req-405-a5b6c7] [redis-node:cache-primary] [Redis] redis.exceptions.ConnectionError: Timeout connecting to Redis - connection pool exhausted
2024-01-17T09:00:02.895Z [ERROR] [trace_id:req-406-a6b7c8] [redis-node:cache-primary] [Redis] ERR max number of clients reached - failed command: SET session:token:99431
2024-01-17T09:00:03.015Z [WARN]  [redis-node:cache-primary] [Redis] Recommendation: review connection pooling configuration and consider increasing maxclients or scaling cache tier"""
        elif path.exists():
            with open(path, encoding="utf-8") as f:
                logs[tier] = f.read()
        else:
            logs[tier] = ""
            print(f"Warning: {path} not found")
    
    return logs


async def analyze_scenario_stream(scenario="scenario1_web_issue", query=None):
    """
    Stream multi-layer analysis with status updates.
    Yields status messages and final results.
    """
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    yield "Initializing multi-layer analysis..."
    
    # Create RAG tools
    yield "Creating RAG tools..."
    web_rag_tool = create_web_rag_tool()
    app_rag_tool = create_app_rag_tool()
    db_rag_tool = create_db_rag_tool()
    cache_rag_tool = create_cache_rag_tool()
    
    # Create nodes for each layer
    yield "Creating graph nodes..."
    incident_manager_node = create_incident_manager_node()
    web_tool_node = create_web_tool_node(web_rag_tool)
    app_tool_node = create_app_tool_node(app_rag_tool)
    db_tool_node = create_db_tool_node(db_rag_tool)
    cache_tool_node = create_cache_tool_node(cache_rag_tool)
    aggregator_node = create_aggregator_node()
    summarizer_node = create_summarizer_node(llm)
    
    # Build graph
    yield "Building multi-layer graph..."
    compiled_graph = build_multi_layer_graph(
        incident_manager_node,
        web_tool_node,
        app_tool_node,
        db_tool_node,
        cache_tool_node,
        aggregator_node,
        summarizer_node
    )
    
    # Load logs
    yield f"Loading logs for scenario: {scenario}..."
    logs = load_logs(scenario)
    
    # Keep logs separate - web.log to web_tool, app.log to app_tool, db.log to db_tool
    web_log = logs.get("web", "")
    app_log = logs.get("app", "")
    db_log = logs.get("db", "")
    
    if not any([web_log, app_log, db_log]):
        yield "Warning: No log files found, proceeding with query-based analysis..."
    else:
        yield f"Loaded logs: Web={len(web_log)} chars, App={len(app_log)} chars, DB={len(db_log)} chars"
    
    # Create initial state
    analysis_query = query if query else "Analyzing system logs from web, app, db, and cache tiers"
    initial_state: MultiLayerState = {
        "messages": [HumanMessage(content=analysis_query)],
        "web_log": web_log,
        "app_log": app_log,
        "db_log": db_log,
        "cache_log": logs.get("cache", ""),
        "web_result": "",
        "app_result": "",
        "db_result": "",
        "cache_result": "",
        "next": "",
        "tool_results": {}
    }
    
    yield "Running multi-layer analysis..."
    
    # Stream graph execution
    final_result = None
    async for step in compiled_graph.astream(initial_state, {"recursion_limit": 20}):
        for node_name, node_output in step.items():
            if node_name != "__end__":
                # Yield status updates based on node
                if node_name == "incident_manager":
                    next_node = node_output.get("next", "")
                    if next_node:
                        yield f"Routing to {next_node} analysis..."
                elif node_name == "web_tool":
                    yield "Analyzing web tier logs..."
                elif node_name == "app_tool":
                    yield "Analyzing application tier logs..."
                elif node_name == "db_tool":
                    yield "Analyzing database tier logs..."
                elif node_name == "aggregate":
                    yield "Aggregating analysis results..."
                elif node_name == "summarizer":
                    yield "Generating root cause analysis summary..."
                    final_result = node_output
    
    # If we didn't get final result from stream, invoke once more
    if final_result is None:
        yield "Finalizing analysis..."
        final_result = await compiled_graph.ainvoke(initial_state, {"recursion_limit": 20})
    
    # Extract summary
    summary = ""
    if "messages" in final_result:
        for msg in final_result["messages"]:
            if hasattr(msg, "name") and msg.name == "summarizer":
                if hasattr(msg, "content"):
                    summary = str(msg.content)
                    break
            elif hasattr(msg, "content") and "FINAL INCIDENT SUMMARY" in str(msg.content):
                summary = str(msg.content)
                break
    
    # Extract RCA data in format expected by frontend
    web_result = final_result.get("web_result", "")
    app_result = final_result.get("app_result", "")
    db_result = final_result.get("db_result", "")
    cache_result = final_result.get("cache_result", "")
    
    # Build RCA structure with complete data
    rca_summary_markdown = final_result.get("rca_summary_markdown", summary)
    rca_root_cause = final_result.get("rca_root_cause", summary or "Analysis completed")
    rca_recommendations = final_result.get("rca_recommendations", [])
    rca_evidence = final_result.get("rca_evidence", [])

    rca_data = {
        "root_cause": rca_root_cause,
        "summary": rca_summary_markdown,
        "evidence": rca_evidence,
        "recommendations": rca_recommendations,
        "web_result": web_result,
        "app_result": app_result,
        "db_result": db_result,
        "cache_result": cache_result,
    }
    
    # Add tool results as evidence (full results, not truncated)
    if web_result:
        rca_data["evidence"].append(f"Web tier: {web_result}")
    if app_result:
        rca_data["evidence"].append(f"App tier: {app_result}")
    if db_result:
        rca_data["evidence"].append(f"DB tier: {db_result}")
    if cache_result:
        rca_data["evidence"].append(f"Cache tier: {cache_result}")
    
    # Yield final result with complete output
    yield {
        "type": "rca_complete",
        "rca": rca_data
    }


def analyze_scenario(scenario="scenario1_web_issue", query=None):
    """
    Run multi-layer analysis and return results.
    Returns dict with summary, web_result, app_result, db_result
    """
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    # Create RAG tools
    web_rag_tool = create_web_rag_tool()
    app_rag_tool = create_app_rag_tool()
    db_rag_tool = create_db_rag_tool()
    cache_rag_tool = create_cache_rag_tool()
    
    # Create nodes for each layer
    incident_manager_node = create_incident_manager_node()
    web_tool_node = create_web_tool_node(web_rag_tool)
    app_tool_node = create_app_tool_node(app_rag_tool)
    db_tool_node = create_db_tool_node(db_rag_tool)
    cache_tool_node = create_cache_tool_node(cache_rag_tool)
    aggregator_node = create_aggregator_node()
    summarizer_node = create_summarizer_node(llm)
    
    # Build graph
    compiled_graph = build_multi_layer_graph(
        incident_manager_node,
        web_tool_node,
        app_tool_node,
        db_tool_node,
        cache_tool_node,
        aggregator_node,
        summarizer_node
    )
    
    # Load logs
    logs = load_logs(scenario)
    
    # Keep logs separate - web.log to web_tool, app.log to app_tool, db.log to db_tool
    web_log = logs.get("web", "")
    app_log = logs.get("app", "")
    db_log = logs.get("db", "")
    cache_log = logs.get("cache", "")
    
    # Create initial state
    analysis_query = query if query else "Analyzing system logs from web, app, db, and cache tiers"
    initial_state: MultiLayerState = {
        "messages": [HumanMessage(content=analysis_query)],
        "web_log": web_log,
        "app_log": app_log,
        "db_log": db_log,
        "cache_log": cache_log,
        "web_result": "",
        "app_result": "",
        "db_result": "",
        "cache_result": "",
        "next": "",
        "tool_results": {}
    }
    
    # Run the graph
    final_result = compiled_graph.invoke(initial_state, {"recursion_limit": 20})
    
    # Extract summary
    summary = ""
    if "messages" in final_result:
        for msg in final_result["messages"]:
            if hasattr(msg, "name") and msg.name == "summarizer":
                if hasattr(msg, "content"):
                    summary = str(msg.content)
                    break
            elif hasattr(msg, "content") and "FINAL INCIDENT SUMMARY" in str(msg.content):
                summary = str(msg.content)
                break
    
    return {
        "summary": summary,
        "web_result": final_result.get("web_result", ""),
        "app_result": final_result.get("app_result", ""),
        "db_result": final_result.get("db_result", ""),
        "cache_result": final_result.get("cache_result", ""),
        "final_result": final_result
    }


def main(scenario="scenario1_web_issue", stream=False, show_graph=False):
    """Main function to run the multi-layer analysis"""
    
    print("\n" + "=" * 80)
    print("Initializing Multi-Layer LangGraph System...")
    print("=" * 80)
    print("Layer 1: Incident Manager - Decides which tools to use")
    print("Layer 2: Tool Nodes - web_tool, app_tool, db_tool, cache_tool (separate nodes)")
    print("Layer 3: Aggregator - Collects all tool results")
    print("Layer 4: Summarizer - Creates final summary")
    print("=" * 80)
    
    # Initialize LLM
    print("\nInitializing LLM...")
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    # Create RAG tools
    print("\nCreating RAG tools...")
    web_rag_tool = create_web_rag_tool()
    app_rag_tool = create_app_rag_tool()
    db_rag_tool = create_db_rag_tool()
    cache_rag_tool = create_cache_rag_tool()
    print("All RAG tools created")
    
    # Create nodes for each layer
    print("\nCreating graph nodes...")
    
    # Layer 1: Incident manager (no LLM needed - simple routing logic)
    incident_manager_node = create_incident_manager_node()
    print("  Incident manager node created")
    
    # Layer 2: Tool nodes
    web_tool_node = create_web_tool_node(web_rag_tool)
    app_tool_node = create_app_tool_node(app_rag_tool)
    db_tool_node = create_db_tool_node(db_rag_tool)
    cache_tool_node = create_cache_tool_node(cache_rag_tool)
    print("  Tool nodes created (web, app, db, cache)")
    
    # Layer 3: Aggregator
    aggregator_node = create_aggregator_node()
    print("  Aggregator node created")
    
    # Layer 4: Summarizer
    summarizer_node = create_summarizer_node(llm)
    print("  Summarizer node created")
    
    # Build graph
    print("\nBuilding multi-layer graph...")
    compiled_graph = build_multi_layer_graph(
        incident_manager_node,
        web_tool_node,
        app_tool_node,
        db_tool_node,
        cache_tool_node,
        aggregator_node,
        summarizer_node
    )
    print("Graph built successfully")
    
    # Load logs
    print(f"\nLoading logs for scenario: {scenario}...")
    logs = load_logs(scenario)
    
    # Keep logs separate - web.log to web_tool, app.log to app_tool, db.log to db_tool
    web_log = logs.get("web", "")
    app_log = logs.get("app", "")
    db_log = logs.get("db", "")
    
    total_chars = len(web_log) + len(app_log) + len(db_log)
    if total_chars == 0:
        print("Warning: No logs found.")
        return
    else:
        cache_log = logs.get("cache", "")
        print(f"Loaded logs: Web={len(web_log)} chars, App={len(app_log)} chars, DB={len(db_log)} chars, Cache={len(cache_log)} chars")
    
    # Create initial state with separate log files
    initial_state: MultiLayerState = {
        "messages": [HumanMessage(content="Analyzing system logs from web, app, db, and cache tiers")],
        "web_log": web_log,
        "app_log": app_log,
        "db_log": db_log,
        "cache_log": logs.get("cache", ""),
        "web_result": "",
        "app_result": "",
        "db_result": "",
        "cache_result": "",
        "next": "",
        "tool_results": {}
    }
    
    print("Initial state created with separate log files")
    
    # Run the graph
    print("\nRunning multi-layer analysis...")
    print("=" * 80)
    
    if stream:
        # Stream results to see each layer
        try:
            for step in compiled_graph.stream(initial_state, {"recursion_limit": 20}):
                for node_name, node_output in step.items():
                    if node_name != "__end__":
                        print(f"\n[Layer: {node_name}]")
                        if "messages" in node_output and node_output["messages"]:
                            last_msg = node_output["messages"][-1]
                            if hasattr(last_msg, "content"):
                                content = str(last_msg.content)
                                # Show first 300 chars
                                preview = content[:300] + "..." if len(content) > 300 else content
                                print(preview)
                        if "next" in node_output:
                            print(f"  Next: {node_output['next']}")
                        print("-" * 80)
        except Exception as e:
            print(f"Error during streaming: {e}")
            import traceback
            traceback.print_exc()
            return
    
    # Get final result
    try:
        final_result = compiled_graph.invoke(initial_state, {"recursion_limit": 20})
        
        print("\nAnalysis Complete!")
        print("=" * 80)
        
        # Print final summary
        if "messages" in final_result:
            print("\nFINAL SUMMARY")
            print("=" * 80)
            for msg in final_result["messages"]:
                if hasattr(msg, "name") and msg.name == "summarizer":
                    if hasattr(msg, "content"):
                        print(msg.content)
                    break
        
        # Optionally show individual results
        print("\n" + "=" * 80)
        print("Individual Tool Results")
        print("=" * 80)
        print("\nWeb Tier Results:")
        print(final_result.get("web_result", "No results"))
        print("\nApp Tier Results:")
        print(final_result.get("app_result", "No results"))
        print("\nDB Tier Results:")
        print(final_result.get("db_result", "No results"))
        print("\nCache Tier Results:")
        print(final_result.get("cache_result", "No results"))
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
    
    # Optionally save graph structure
    if show_graph:
        print("\n" + "=" * 80)
        print("Graph Structure (Mermaid Diagram)")
        print("=" * 80)
        mermaid_diagram = compiled_graph.get_graph().draw_mermaid()
        print(mermaid_diagram)
        
        graph_file = Path(__file__).parent / "graph_structure.mmd"
        with open(graph_file, "w", encoding="utf-8") as f:
            f.write(mermaid_diagram)
        print(f"\nGraph saved to {graph_file}")
        print("You can view it at: https://mermaid.live/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Layer LangGraph Log Analysis")
    parser.add_argument(
        "--scenario",
        type=str,
        default="scenario1_web_issue",
        help="Scenario directory name (default: scenario1_web_issue)"
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream results to see each layer execution"
    )
    parser.add_argument(
        "--show-graph",
        action="store_true",
        help="Show and save graph structure as Mermaid diagram"
    )
    
    args = parser.parse_args()
    
    main(scenario=args.scenario, stream=args.stream, show_graph=args.show_graph)


