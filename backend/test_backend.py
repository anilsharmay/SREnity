"""
Simple test script for the backend API
"""
import requests
import json
import sys

def test_stream_endpoint():
    """Test the streaming analysis endpoint"""
    url = "http://localhost:8000/api/analyze/stream"
    
    # Test request
    payload = {
        "query": "Database Cluster Connection Issues. Connection pool exhausted across database cluster. Affects: Multiple services",
        "alert_id": "alert-001",
        "service_id": None
    }
    
    print("=" * 60)
    print("Testing Backend API")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("=" * 60)
    print("\nStreaming response:\n")
    
    try:
        response = requests.post(url, json=payload, stream=True, timeout=120)
        response.raise_for_status()
        
        # Read streaming response
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]  # Remove 'data: ' prefix
                    if data_str.strip() == '[DONE]':
                        print("\n[DONE] - Stream completed")
                        break
                    try:
                        data = json.loads(data_str)
                        update_type = data.get('type', 'unknown')
                        
                        if update_type == 'status':
                            print(f"[STATUS] {data.get('message', '')}")
                        elif update_type == 'rca_complete':
                            rca = data.get('rca', {})
                            print(f"\n[RCA COMPLETE]")
                            print(f"  Root Cause: {rca.get('root_cause', 'N/A')[:200]}...")
                            print(f"  Evidence: {len(rca.get('evidence', []))} items")
                            print(f"  Recommendations: {len(rca.get('recommendations', []))} items")
                        elif update_type == 'runbook_complete':
                            runbooks = data.get('runbooks', [])
                            print(f"\n[RUNBOOKS COMPLETE] {len(runbooks)} runbooks found")
                        elif update_type == 'error':
                            print(f"\n[ERROR] {data.get('message', 'Unknown error')}")
                    except json.JSONDecodeError:
                        print(f"[RAW] {data_str[:100]}")
        
        print("\n" + "=" * 60)
        print("Test completed successfully!")
        print("=" * 60)
        return True
        
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to backend.")
        print("Make sure the backend is running: python backend/main.py")
        return False
    except requests.exceptions.Timeout:
        print("\n[ERROR] Request timed out")
        return False
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_stream_endpoint()
    sys.exit(0 if success else 1)

