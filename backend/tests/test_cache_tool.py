"""
Utility script to exercise the cache (Redis) RAG tool in isolation.

Usage:
    python backend/tests/test_cache_tool.py --log-file path/to/cache.log

If --log-file is omitted, a built-in sample of connection pool exhaustion
events will be analysed.
"""
import argparse
import sys
from pathlib import Path
import getpass
import os

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.analysis.tools import create_cache_rag_tool

DEFAULT_SAMPLE = """2024-01-17T09:00:01.950Z [ERROR] [redis-node:cache-primary] ERR max number of clients reached
2024-01-17T09:00:02.012Z [WARN]  [redis-node:cache-primary] Connected clients: 998 / maxclients: 1000
2024-01-17T09:00:02.145Z [ERROR] [redis-node:cache-primary] ConnectionError: ERR max number of clients reached (service: order-service)
2024-01-17T09:00:02.214Z [WARN]  [redis-node:cache-primary] Slow command: HGETALL cart:session:88321 took 284ms (threshold 100ms)
2024-01-17T09:00:02.318Z [ERROR] [redis-node:cache-primary] BLPOP queue:notifications timeout - blocking clients: 12
2024-01-17T09:00:02.576Z [WARN]  [redis-node:cache-primary] INFO clients: connected_clients=1000, blocked_clients=15
"""


def load_logs(log_path: Path | None) -> str:
    if log_path is None:
        return DEFAULT_SAMPLE
    if not log_path.exists():
        raise FileNotFoundError(f"Log file not found: {log_path}")
    return log_path.read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Test the Redis cache analysis tool")
    parser.add_argument(
        "--log-file",
        type=Path,
        help="Path to a cache.log file to analyse (optional; uses built-in sample if omitted)",
    )
    args = parser.parse_args()

    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key: ")

    logs = load_logs(args.log_file)

    analyze_cache_logs = create_cache_rag_tool()
    print("\n=== Cache Tool Analysis ===\n")
    result = analyze_cache_logs.invoke({"query": logs})
    print(result)


if __name__ == "__main__":
    main()

