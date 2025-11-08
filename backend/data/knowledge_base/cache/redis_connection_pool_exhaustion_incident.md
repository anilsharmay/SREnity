# Redis Connection Pool Exhaustion Incident

## Overview

- **Service:** Redis cache tier  
- **Severity:** High  
- **Primary Symptom:** Application errors indicating `ERR max number of clients reached` and elevated latency on cache commands.  
- **Root Cause:** Connection pool limit reached because idle connections were not released and traffic spikes were not accommodated by the current configuration.

## Sample Logs

```
2024-01-17T09:00:01.950Z [ERROR] [trace_id:req-401-a1b2c3] [redis-node:cache-primary] [Redis] ERR max number of clients reached - exception while processing GET user:profile:12345
2024-01-17T09:00:02.012Z [WARN]  [redis-node:cache-primary] [Redis] Connected clients: 998 / maxclients: 1000 - pool almost exhausted
2024-01-17T09:00:02.145Z [ERROR] [trace_id:req-402-a2b3c4] [redis-node:cache-primary] [Redis] ConnectionError: ERR max number of clients reached (service: order-service)
2024-01-17T09:00:02.214Z [WARN]  [redis-node:cache-primary] [Redis] Slow command: HGETALL cart:session:88321 took 284ms (threshold 100ms)
2024-01-17T09:00:02.318Z [ERROR] [trace_id:req-403-a3b4c5] [redis-node:cache-primary] [Redis] BLPOP queue:notifications timeout - blocking clients: 12
2024-01-17T09:00:02.576Z [WARN]  [redis-node:cache-primary] [Redis] INFO clients: connected_clients=1000, blocked_clients=15, tracking_clients=0
2024-01-17T09:00:02.712Z [ERROR] [trace_id:req-405-a5b6c7] [redis-node:cache-primary] [Redis] redis.exceptions.ConnectionError: Timeout connecting to Redis - connection pool exhausted
2024-01-17T09:00:02.895Z [ERROR] [trace_id:req-406-a6b7c8] [redis-node:cache-primary] [Redis] ERR max number of clients reached - failed command: SET session:token:99431
```

## Detection

- Application or API logs show `redis.exceptions.ConnectionError` or `ERR max number of clients reached`.
- Redis `INFO clients` command reveals `connected_clients` close to or equal to `maxclients`.
- Monitoring dashboards display elevated command latency, increased CPU usage, and an abnormal number of blocked clients.

## Immediate Actions

1. Validate the Redis instance health:
   - `redis-cli -h <host> -p <port> INFO clients`
   - `redis-cli CLIENT LIST | head` to spot long-lived or unresponsive clients.
2. Identify which upstream services are exhausting connections (check application pool settings, connection leaks).
3. Restart or recycle those application instances if necessary to free connections.

## Remediation Plan

1. **Increase Connection Limits Temporarily**
   - Adjust the `maxclients` value if the server resources allow it.
   - Ensure the operating system limit (`ulimit -n`) exceeds the new `maxclients` setting.
2. **Tune Application Connection Pools**
   - Review pool configurations in the calling services.
   - Set connection timeouts and maximum pool size to reasonable values.
3. **Enable Idle Connection Cleanup**
   - Configure the application or sidecar to close unused connections.
4. **Scale Redis Vertically or Horizontally**
   - Increase instance size or deploy read replicas/sentinels if sustained load requires it.

## Verification

- Confirm `connected_clients` is comfortably below `maxclients`.
- Monitor application error rates and response times for at least 30 minutes.
- Verify that Redis command latency returns to baseline thresholds.

## Prevention

- Implement proactive alerts for connection utilization >80%.
- Schedule regular reviews of application pool settings.
- Use connection pooling libraries that enforce idle timeouts and max usage limits.

