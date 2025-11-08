# Redis Cache Healthy Baseline

## Overview

- **Service:** Redis cache tier  
- **Status:** Healthy  
- **Usage Pattern:** Connection count and memory usage within expected thresholds. Command latency low and stable.

## Sample Logs

```
2024-01-17T08:45:01.002Z [INFO] [redis-node:cache-primary] [Redis] INFO stats: instantaneous_ops_per_sec=143, rejected_connections=0, total_commands_processed=381245
2024-01-17T08:45:01.015Z [INFO] [redis-node:cache-primary] [Redis] INFO clients: connected_clients=124, blocked_clients=0, tracking_clients=0, clients_in_timeout_table=0
2024-01-17T08:45:01.029Z [INFO] [redis-node:cache-primary] [Redis] LATENCY LATEST: command=GET latency_ms=0.35, command=SET latency_ms=0.42
2024-01-17T08:45:01.044Z [INFO] [redis-node:cache-primary] [Redis] INFO memory: used_memory=154321232 (147.2M), maxmemory=536870912 (512M), maxmemory_policy=allkeys-lru
2024-01-17T08:45:01.058Z [INFO] [redis-node:cache-primary] [Redis] INFO replication: role=master, connected_slaves=2, master_repl_offset=351925189
```

## Expected Metrics

- `connected_clients` well below the configured `maxclients` limit.
- CPU utilization under 40% during peak traffic.
- No blocked clients (`blocked_clients = 0`).
- Command latency < 1 ms for simple GET/SET operations.

## Operational Checklist

1. Periodically run `redis-cli INFO` and record key client/memory statistics.
2. Ensure `maxmemory-policy` matches business expectations (e.g. `allkeys-lru` if eviction is acceptable).
3. Validate that monitoring alerts exist for:
   - Connection utilization
   - Memory pressure
   - Replication lag (if applicable)

## Runbook Notes

- This baseline is used by the cache analysis tool to determine whether logs indicate abnormal behaviour.

