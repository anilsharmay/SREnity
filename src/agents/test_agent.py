"""
Test script for the SRE Agent

This script tests the agent with various scenarios to ensure it works correctly.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from src.agents.sre_agent import SREAgent


def test_agent():
    """Test the SRE agent with various scenarios"""
    
    print("🤖 Initializing SRE Agent...")
    agent = SREAgent()
    print("✅ Agent initialized successfully!")
    
    print("\n" + "="*60)
    print("AGENT GRAPH STRUCTURE")
    print("="*60)
    print(agent.get_graph_structure())
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Standard SRE Query (Redis)",
            "query": "How to monitor Redis memory usage?",
            "expected": "Should use runbooks tool"
        },
        {
            "name": "Version-specific Query",
            "query": "Redis 7.2 memory leak issues and fixes",
            "expected": "Should use both tools"
        },
        {
            "name": "Off-topic Query",
            "query": "What's the weather like today?",
            "expected": "Should refuse politely"
        },
        {
            "name": "Complex SRE Query",
            "query": "PostgreSQL connection pool exhaustion in production - how to diagnose and fix?",
            "expected": "Should use both tools"
        },
        {
            "name": "Command-specific Query",
            "query": "Show me the exact syntax for Redis MEMORY STATS command",
            "expected": "Should use runbooks tool"
        }
    ]
    
    print("\n" + "="*60)
    print("RUNNING TEST SCENARIOS")
    print("="*60)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🧪 Test {i}: {scenario['name']}")
        print(f"Query: {scenario['query']}")
        print(f"Expected: {scenario['expected']}")
        print("-" * 40)
        
        try:
            response = agent.invoke(scenario['query'], verbose=True)
            print(f"Response: {response[:200]}...")
            print("✅ Test completed successfully")
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
        
        print("-" * 40)
    
    print("\n🎉 All tests completed!")


if __name__ == "__main__":
    test_agent()
