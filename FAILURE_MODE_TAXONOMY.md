# Failure Mode Taxonomy - SREnity

This document outlines the failure modes observed or anticipated for the SREnity AIOps system. Each failure mode includes a title, a concise definition, and illustrative examples.

## Failure Mode 1: Unsubstantiated Root Cause Claims

**Definition:** AI identifies a root cause without sufficient evidence or fails to indicate confidence level/uncertainty.

**Slug:** `unsubstantiated_root_cause_claims`

**Examples:**

**Trace Input (id: 3721):**
```
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-3721] Database connection timeout: Unable to acquire connection from pool after 30s
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-3722] Connection pool exhausted: 100/100 connections in use
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-3723] Database connection timeout: Unable to acquire connection from pool after 30s
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-3724] Connection pool exhausted: 100/100 connections in use
2024-01-15T14:30:07.891Z [ERROR] [trace_id:req-3725] Database connection timeout: Unable to acquire connection from pool after 30s
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-4721] Database connection timeout: Unable to acquire connection from pool after 30s
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-4722] Connection pool exhausted: 100/100 connections in use
```

**AI Response Issue:** AI states "Root cause: Database connection pool exhaustion" without showing evidence from logs or metrics. AI should indicate this is a hypothesis based on pattern matching and request additional metrics to confirm.

**Trace Input (id: 8392):**
```
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-8392] [service:payment] Redis connection failed: Connection refused
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-8393] [service:payment] POST /api/payments - 500 Internal Server Error - Redis connection timeout
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-8394] [service:payment] Redis connection failed: Connection refused
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-8395] [service:payment] POST /api/payments - 500 Internal Server Error - Redis connection timeout
2024-01-15T14:30:07.891Z [ERROR] [trace_id:req-8396] [service:payment] Redis connection failed: Connection refused
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-9392] [service:payment] Redis connection failed: Connection refused
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-9393] [service:payment] POST /api/payments - 500 Internal Server Error - Redis connection timeout
```

**AI Response Issue:** AI claims "Root cause: Redis cache connection failures" without analyzing app tier logs that might show different error patterns. AI should state this is a likely cause based on available evidence and note missing context.

**Trace Input (id: 2746):**
```
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-2746] [ELB:frontend-sg] [Apache] AH01084: GET /api/auth - 502 Bad Gateway - 5234ms
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-2747] [ELB:frontend-sg] [Apache] AH01085: POST /api/login - 502 Bad Gateway - 6123ms
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-2748] [ELB:frontend-sg] [Apache] AH01084: GET /api/auth - 502 Bad Gateway - 5234ms
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-2749] [ELB:frontend-sg] [Apache] AH01085: POST /api/login - 502 Bad Gateway - 6123ms
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-3746] [ELB:frontend-sg] [Apache] AH01084: GET /api/auth - 502 Bad Gateway - 5234ms
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-3747] [ELB:frontend-sg] [Apache] AH01085: POST /api/login - 502 Bad Gateway - 6123ms
```

**AI Response Issue:** AI identifies root cause as "Database deadlock" but only analyzed web tier logs. AI should indicate that app and db tier analysis is needed to confirm this hypothesis.

---

## Failure Mode 2: Missing Critical Tier Analysis

**Definition:** AI fails to analyze relevant system tiers (web, app, db, cache) or skips tiers that contain important evidence.

**Slug:** `missing_critical_tier_analysis`

**Examples:**

**Trace Input (id: 5913):**
```
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-5913] [ELB:frontend-sg] [Apache] AH01084: GET /api/users - 502 Bad Gateway - 5234ms - Timeout while reading response header
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-5914] [ELB:frontend-sg] [Apache] AH01085: POST /api/orders - 502 Bad Gateway - 6123ms - Upstream server timed out
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-5915] [ELB:frontend-sg] [Apache] AH01084: GET /api/products - 502 Bad Gateway - 5234ms - Timeout while reading response header
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-5916] [ELB:frontend-sg] [Apache] AH01085: POST /api/cart - 502 Bad Gateway - 6123ms - Upstream server timed out
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-6913] [ELB:frontend-sg] [Apache] AH01084: GET /api/users - 502 Bad Gateway - 5234ms - Timeout while reading response header
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-6914] [ELB:frontend-sg] [Apache] AH01085: POST /api/orders - 502 Bad Gateway - 6123ms - Upstream server timed out
```

**AI Response Issue:** AI only analyzes web tier logs and provides recommendations. AI should analyze app tier and db tier logs to identify where the latency is actually occurring.

**Trace Input (id: 4827):**
```
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-4827] [app-tier] Redis cache error: Connection timeout after 5s
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-4828] [app-tier] Cache operation failed: Unable to connect to Redis cluster
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-4829] [app-tier] Redis cache error: Connection timeout after 5s
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-4830] [app-tier] Cache operation failed: Unable to connect to Redis cluster
2024-01-15T14:30:07.891Z [ERROR] [trace_id:req-4831] [app-tier] Redis cache error: Connection timeout after 5s
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-5827] [app-tier] Redis cache error: Connection timeout after 5s
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-5828] [app-tier] Cache operation failed: Unable to connect to Redis cluster
```

**AI Response Issue:** AI analyzes app tier but doesn't analyze cache tier logs to understand the full picture. AI should indicate that cache tier analysis is needed and either request those logs or note their absence.

**Trace Input (id: 7351):**
```
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-7351] [db-tier] Query timeout: SELECT * FROM orders WHERE user_id=? exceeded 30s limit
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-7352] [db-tier] Query timeout: SELECT * FROM products WHERE category=? exceeded 30s limit
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-7353] [db-tier] Query timeout: SELECT * FROM cart WHERE user_id=? exceeded 30s limit
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-7354] [db-tier] Query timeout: SELECT * FROM orders WHERE user_id=? exceeded 30s limit
2024-01-15T14:30:07.891Z [ERROR] [trace_id:req-7355] [db-tier] Query timeout: SELECT * FROM products WHERE category=? exceeded 30s limit
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-8351] [db-tier] Query timeout: SELECT * FROM orders WHERE user_id=? exceeded 30s limit
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-8352] [db-tier] Query timeout: SELECT * FROM cart WHERE user_id=? exceeded 30s limit
```

**AI Response Issue:** AI analyzes db tier but doesn't check app tier logs to see if connection pooling issues or application-level problems are contributing. AI should cross-reference findings across tiers.

---

## Failure Mode 3: Overconfident Severity Assessment

**Definition:** AI assigns severity levels (P0, P1, P2) or impact assessments without sufficient evidence or fails to disclaim uncertainty.

**Slug:** `overconfident_severity_assessment`

**Examples:**

**Trace Input (id: 6284):**
```
2024-01-15T14:30:01.123Z [WARN] [trace_id:req-6284] [service:logging] Failed to write log entry: Buffer full
2024-01-15T14:30:15.456Z [WARN] [trace_id:req-6285] [service:logging] Failed to write log entry: Buffer full
2024-01-15T14:30:30.789Z [WARN] [trace_id:req-6286] [service:logging] Failed to write log entry: Buffer full
2024-01-15T14:30:45.234Z [WARN] [trace_id:req-6287] [service:logging] Failed to write log entry: Buffer full
2024-01-15T14:31:00.891Z [WARN] [trace_id:req-6288] [service:logging] Failed to write log entry: Buffer full
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:45.123Z [WARN] [trace_id:req-7284] [service:logging] Failed to write log entry: Buffer full
2024-01-15T14:45:00.456Z [WARN] [trace_id:req-7285] [service:logging] Failed to write log entry: Buffer full
```

**AI Response Issue:** AI classifies this as "P1 - High Severity" without analyzing error frequency, user impact, or business metrics. AI should state that severity assessment requires additional context about error rate and user impact.

**Trace Input (id: 3719):**
```
2024-01-15T14:30:01.123Z [WARN] [trace_id:req-3719] [app-tier] Memory usage: 85% (8.5GB/10GB) - Threshold: 80%
2024-01-15T14:30:02.456Z [WARN] [trace_id:req-3720] [app-tier] Memory usage: 87% (8.7GB/10GB) - Threshold: 80%
2024-01-15T14:30:03.789Z [WARN] [trace_id:req-3721] [app-tier] Memory usage: 89% (8.9GB/10GB) - Threshold: 80%
2024-01-15T14:30:05.234Z [WARN] [trace_id:req-3722] [app-tier] Memory usage: 91% (9.1GB/10GB) - Threshold: 80%
2024-01-15T14:30:07.891Z [WARN] [trace_id:req-3723] [app-tier] Memory usage: 93% (9.3GB/10GB) - Threshold: 80%
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [WARN] [trace_id:req-4719] [app-tier] Memory usage: 94% (9.4GB/10GB) - Threshold: 80%
2024-01-15T14:44:59.456Z [WARN] [trace_id:req-4720] [app-tier] Memory usage: 95% (9.5GB/10GB) - Threshold: 80%
```

**AI Response Issue:** AI claims "Critical impact - service degradation imminent" without checking if actual user-facing errors are occurring. AI should indicate this is a warning that requires monitoring actual service health metrics.

**Trace Input (id: 5826):**
```
2024-01-15T14:30:01.123Z [INFO] [trace_id:req-5826] [db-tier] Connection pool status: 80/100 connections in use (80%)
2024-01-15T14:30:02.456Z [INFO] [trace_id:req-5827] [db-tier] Connection pool status: 81/100 connections in use (81%)
2024-01-15T14:30:03.789Z [INFO] [trace_id:req-5828] [db-tier] Connection pool status: 82/100 connections in use (82%)
2024-01-15T14:30:05.234Z [INFO] [trace_id:req-5829] [db-tier] Connection pool status: 83/100 connections in use (83%)
2024-01-15T14:30:07.891Z [INFO] [trace_id:req-5830] [db-tier] Connection pool status: 84/100 connections in use (84%)
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [INFO] [trace_id:req-6826] [db-tier] Connection pool status: 85/100 connections in use (85%)
2024-01-15T14:44:59.456Z [INFO] [trace_id:req-6827] [db-tier] Connection pool status: 86/100 connections in use (86%)
```

**AI Response Issue:** AI states "P0 - Critical" without considering if this is normal peak usage or an actual incident. AI should ask about baseline metrics and recent changes before assigning severity.

---

## Failure Mode 4: Missing Context Questions

**Definition:** AI fails to ask for critical missing information needed for accurate analysis, such as time ranges, affected services, or baseline metrics.

**Slug:** `missing_context_questions`

**Examples:**

**Trace Input (id: 1947):**
```
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-1947] [service:api] 500 Internal Server Error
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-1948] [service:api] 500 Internal Server Error
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-1949] [service:api] 500 Internal Server Error
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-1950] [service:api] 500 Internal Server Error
2024-01-15T14:30:07.891Z [ERROR] [trace_id:req-1951] [service:api] 500 Internal Server Error
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-2947] [service:api] 500 Internal Server Error
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-2948] [service:api] 500 Internal Server Error
```

**AI Response Issue:** AI provides analysis without asking what time range the errors occurred in, which services are affected, or what the baseline error rate is. AI should ask for these details before providing recommendations.

**Trace Input (id: 8362):**
```
2024-01-15T14:30:01.123Z [WARN] [trace_id:req-8362] [service:checkout] POST /api/checkout - Response time: 3456ms (p95: 500ms)
2024-01-15T14:30:02.456Z [WARN] [trace_id:req-8363] [service:checkout] POST /api/checkout - Response time: 4123ms (p95: 500ms)
2024-01-15T14:30:03.789Z [WARN] [trace_id:req-8364] [service:checkout] POST /api/checkout - Response time: 3890ms (p95: 500ms)
2024-01-15T14:30:05.234Z [WARN] [trace_id:req-8365] [service:checkout] POST /api/checkout - Response time: 4234ms (p95: 500ms)
2024-01-15T14:30:07.891Z [WARN] [trace_id:req-8366] [service:checkout] POST /api/checkout - Response time: 4012ms (p95: 500ms)
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [WARN] [trace_id:req-9362] [service:checkout] POST /api/checkout - Response time: 4567ms (p95: 500ms)
2024-01-15T14:44:59.456Z [WARN] [trace_id:req-9363] [service:checkout] POST /api/checkout - Response time: 4345ms (p95: 500ms)
```

**AI Response Issue:** AI analyzes logs but doesn't ask when the degradation started, what the normal response time is, or if there were recent deployments. AI should request this context to provide accurate root cause analysis.

**Trace Input (id: 4719):**
```
2024-01-15T14:30:01.123Z [INFO] [trace_id:req-4719] [cache-tier] Cache miss rate: 15% (normal: 5%)
2024-01-15T14:30:02.456Z [INFO] [trace_id:req-4720] [cache-tier] Cache miss rate: 18% (normal: 5%)
2024-01-15T14:30:03.789Z [INFO] [trace_id:req-4721] [cache-tier] Cache miss rate: 22% (normal: 5%)
2024-01-15T14:30:05.234Z [INFO] [trace_id:req-4722] [cache-tier] Cache miss rate: 25% (normal: 5%)
2024-01-15T14:30:07.891Z [INFO] [trace_id:req-4723] [cache-tier] Cache miss rate: 28% (normal: 5%)
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [INFO] [trace_id:req-5719] [cache-tier] Cache miss rate: 32% (normal: 5%)
2024-01-15T14:44:59.456Z [INFO] [trace_id:req-5720] [cache-tier] Cache miss rate: 35% (normal: 5%)
```

**AI Response Issue:** AI provides recommendations without asking about the time period, whether this is a gradual increase or sudden spike, or if there were configuration changes. AI should gather this context first.

---

## Failure Mode 5: Inappropriate Remediation Steps

**Definition:** AI suggests remediation actions that are incorrect, dangerous, or not appropriate for the identified issue.

**Slug:** `inappropriate_remediation_steps`

**Examples:**

**Trace Input (id: 7258):**
```
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-7258] [db-tier] Connection pool exhausted: 100/100 connections in use
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-7259] [db-tier] Unable to acquire connection: Pool exhausted
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-7260] [db-tier] Connection pool exhausted: 100/100 connections in use
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-7261] [db-tier] Unable to acquire connection: Pool exhausted
2024-01-15T14:30:07.891Z [ERROR] [trace_id:req-7262] [db-tier] Connection pool exhausted: 100/100 connections in use
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-8258] [db-tier] Connection pool exhausted: 100/100 connections in use
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-8259] [db-tier] Unable to acquire connection: Pool exhausted
```

**AI Response Issue:** AI recommends "Restart the database cluster" without first suggesting to check for connection leaks or scaling the pool. AI should provide less disruptive options first and escalate only if needed.

**Trace Input (id: 3916):**
```
2024-01-15T14:30:01.123Z [WARN] [trace_id:req-3916] [cache-tier] Redis memory usage: 8.5GB/10GB (85%)
2024-01-15T14:30:02.456Z [WARN] [trace_id:req-3917] [cache-tier] Redis memory usage: 8.7GB/10GB (87%)
2024-01-15T14:30:03.789Z [WARN] [trace_id:req-3918] [cache-tier] Redis memory usage: 8.9GB/10GB (89%)
2024-01-15T14:30:05.234Z [WARN] [trace_id:req-3919] [cache-tier] Redis memory usage: 9.1GB/10GB (91%)
2024-01-15T14:30:07.891Z [WARN] [trace_id:req-3920] [cache-tier] Redis memory usage: 9.3GB/10GB (93%)
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [WARN] [trace_id:req-4916] [cache-tier] Redis memory usage: 9.5GB/10GB (95%)
2024-01-15T14:44:59.456Z [WARN] [trace_id:req-4917] [cache-tier] Redis memory usage: 9.7GB/10GB (97%)
```

**AI Response Issue:** AI suggests "Clear all cache entries" without considering impact on application performance or suggesting to check for memory leaks first. AI should recommend investigating root cause before destructive actions.

**Trace Input (id: 2648):**
```
2024-01-15T14:30:01.123Z [WARN] [trace_id:req-2648] [db-tier] Slow query detected: SELECT * FROM orders WHERE user_id=? took 4523ms
2024-01-15T14:30:02.456Z [WARN] [trace_id:req-2649] [db-tier] Slow query detected: SELECT * FROM products WHERE category=? took 5234ms
2024-01-15T14:30:03.789Z [WARN] [trace_id:req-2650] [db-tier] Slow query detected: SELECT * FROM cart WHERE user_id=? took 4891ms
2024-01-15T14:30:05.234Z [WARN] [trace_id:req-2651] [db-tier] Slow query detected: SELECT * FROM orders WHERE user_id=? took 5123ms
2024-01-15T14:30:07.891Z [WARN] [trace_id:req-2652] [db-tier] Slow query detected: SELECT * FROM products WHERE category=? took 5456ms
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [WARN] [trace_id:req-3648] [db-tier] Slow query detected: SELECT * FROM orders WHERE user_id=? took 4789ms
2024-01-15T14:44:59.456Z [WARN] [trace_id:req-3649] [db-tier] Slow query detected: SELECT * FROM cart WHERE user_id=? took 5012ms
```

**AI Response Issue:** AI recommends "Kill long-running queries" without first suggesting to check query plans, indexes, or if queries are legitimate business operations. AI should provide safer diagnostic steps first.

---

## Failure Mode 6: False Correlation Between Events

**Definition:** AI incorrectly correlates unrelated events or assumes causation when only correlation exists.

**Slug:** `false_correlation_events`

**Examples:**

**Trace Input (id: 6428):**
```
2024-01-15T14:25:00.000Z [INFO] [trace_id:req-6428] [cache-tier] Redis cluster restart initiated
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-6429] [app-tier] Application error: NullPointerException in OrderService
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-6430] [app-tier] Application error: NullPointerException in PaymentService
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-6431] [app-tier] Application error: NullPointerException in OrderService
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-6432] [app-tier] Application error: NullPointerException in PaymentService
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-7429] [app-tier] Application error: NullPointerException in OrderService
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-7430] [app-tier] Application error: NullPointerException in PaymentService
```

**AI Response Issue:** AI assumes the cache restart caused the errors without checking if errors started before the restart or if there's a different root cause. AI should analyze timing and correlation more carefully.

**Trace Input (id: 5827):**
```
2024-01-15T14:30:01.123Z [WARN] [trace_id:req-5827] [db-tier] Slow query: SELECT * FROM orders took 4523ms
2024-01-15T14:30:01.234Z [ERROR] [trace_id:req-5828] [ELB:frontend-sg] [Apache] AH01084: GET /api/orders - 504 Gateway Timeout - 30123ms
2024-01-15T14:30:02.456Z [WARN] [trace_id:req-5829] [db-tier] Slow query: SELECT * FROM products took 5234ms
2024-01-15T14:30:02.567Z [ERROR] [trace_id:req-5830] [ELB:frontend-sg] [Apache] AH01084: GET /api/products - 504 Gateway Timeout - 30123ms
2024-01-15T14:30:03.789Z [WARN] [trace_id:req-5831] [db-tier] Slow query: SELECT * FROM cart took 4891ms
2024-01-15T14:30:03.890Z [ERROR] [trace_id:req-5832] [ELB:frontend-sg] [Apache] AH01084: GET /api/cart - 504 Gateway Timeout - 30123ms
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [WARN] [trace_id:req-6827] [db-tier] Slow query: SELECT * FROM orders took 5123ms
2024-01-15T14:44:58.234Z [ERROR] [trace_id:req-6828] [ELB:frontend-sg] [Apache] AH01084: GET /api/orders - 504 Gateway Timeout - 30123ms
```

**AI Response Issue:** AI claims database issues are causing web timeouts without checking if web tier has its own issues or if they're independent problems. AI should analyze each tier separately before correlating.

**Trace Input (id: 4916):**
```
2024-01-15T14:29:00.000Z [INFO] [trace_id:req-4916] [deployment] Service v2.3.1 deployed to production
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-4917] [service:api] 500 Internal Server Error - Database connection failed
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-4918] [service:api] 500 Internal Server Error - Database connection failed
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-4919] [service:api] 500 Internal Server Error - Database connection failed
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-4920] [service:api] 500 Internal Server Error - Database connection failed
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-5917] [service:api] 500 Internal Server Error - Database connection failed
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-5918] [service:api] 500 Internal Server Error - Database connection failed
```

**AI Response Issue:** AI immediately blames the deployment without checking if errors started before deployment or if there are other contributing factors. AI should analyze timing and other potential causes.

---

## Failure Mode 7: Unsubstantiated Impact Claims

**Definition:** AI makes claims about business impact, user experience, or cost without evidence or disclaimers.

**Slug:** `unsubstantiated_impact_claims`

**Examples:**

**Trace Input (id: 3729):**
```
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-3729] [db-tier] Connection error: Connection refused
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-3730] [db-tier] Connection error: Connection refused
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-3731] [db-tier] Connection error: Connection refused
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-3732] [db-tier] Connection error: Connection refused
2024-01-15T14:30:07.891Z [ERROR] [trace_id:req-3733] [db-tier] Connection error: Connection refused
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-4729] [db-tier] Connection error: Connection refused
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-4730] [db-tier] Connection error: Connection refused
```

**AI Response Issue:** AI states "This is affecting 10,000+ users" without having access to user metrics or traffic data. AI should disclaim that impact assessment requires user-facing metrics that aren't available in logs.

**Trace Input (id: 8417):**
```
2024-01-15T14:30:01.123Z [INFO] [trace_id:req-8417] [service:api] GET /api/users - Response time: 700ms (baseline: 500ms)
2024-01-15T14:30:02.456Z [INFO] [trace_id:req-8418] [service:api] GET /api/products - Response time: 720ms (baseline: 500ms)
2024-01-15T14:30:03.789Z [INFO] [trace_id:req-8419] [service:api] GET /api/orders - Response time: 710ms (baseline: 500ms)
2024-01-15T14:30:05.234Z [INFO] [trace_id:req-8420] [service:api] GET /api/users - Response time: 730ms (baseline: 500ms)
2024-01-15T14:30:07.891Z [INFO] [trace_id:req-8421] [service:api] GET /api/products - Response time: 740ms (baseline: 500ms)
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [INFO] [trace_id:req-9417] [service:api] GET /api/users - Response time: 750ms (baseline: 500ms)
2024-01-15T14:44:59.456Z [INFO] [trace_id:req-9418] [service:api] GET /api/orders - Response time: 760ms (baseline: 500ms)
```

**AI Response Issue:** AI claims "Significant revenue impact expected" without knowing business metrics or if this affects critical user flows. AI should state that business impact requires additional metrics analysis.

**Trace Input (id: 5294):**
```
2024-01-15T14:30:01.123Z [INFO] [trace_id:req-5294] [cache-tier] Cache hit rate: 85% (baseline: 95%)
2024-01-15T14:30:02.456Z [INFO] [trace_id:req-5295] [cache-tier] Cache hit rate: 84% (baseline: 95%)
2024-01-15T14:30:03.789Z [INFO] [trace_id:req-5296] [cache-tier] Cache hit rate: 83% (baseline: 95%)
2024-01-15T14:30:05.234Z [INFO] [trace_id:req-5297] [cache-tier] Cache hit rate: 82% (baseline: 95%)
2024-01-15T14:30:07.891Z [INFO] [trace_id:req-5298] [cache-tier] Cache hit rate: 81% (baseline: 95%)
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [INFO] [trace_id:req-6294] [cache-tier] Cache hit rate: 80% (baseline: 95%)
2024-01-15T14:44:59.456Z [INFO] [trace_id:req-6295] [cache-tier] Cache hit rate: 79% (baseline: 95%)
```

**AI Response Issue:** AI states "This will increase database load by 50%" without calculating actual impact or considering other factors. AI should indicate this is an estimate and requires monitoring to confirm.

---

## Failure Mode 8: Missing Evidence in Recommendations

**Definition:** AI provides recommendations without linking them to specific evidence from logs, metrics, or analysis.

**Slug:** `missing_evidence_recommendations`

**Examples:**

**Trace Input (id: 1593):**
```
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-1593] [service:auth] POST /api/login - 500 Internal Server Error
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-1594] [service:auth] POST /api/login - 500 Internal Server Error
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-1595] [service:auth] POST /api/login - 500 Internal Server Error
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-1596] [service:auth] POST /api/login - 500 Internal Server Error
2024-01-15T14:30:07.891Z [ERROR] [trace_id:req-1597] [service:auth] POST /api/login - 500 Internal Server Error
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-2593] [service:auth] POST /api/login - 500 Internal Server Error
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-2594] [service:auth] POST /api/login - 500 Internal Server Error
```

**AI Response Issue:** AI recommends "Scale up database connections" without showing evidence from logs that database connections are the issue. AI should cite specific log entries or metrics that support each recommendation.

**Trace Input (id: 8264):**
```
2024-01-15T14:30:01.123Z [WARN] [trace_id:req-8264] [app-tier] Memory usage: 7.2GB/8GB (90%)
2024-01-15T14:30:15.456Z [WARN] [trace_id:req-8265] [app-tier] Memory usage: 7.4GB/8GB (92.5%)
2024-01-15T14:30:30.789Z [WARN] [trace_id:req-8266] [app-tier] Memory usage: 7.6GB/8GB (95%)
2024-01-15T14:30:45.234Z [WARN] [trace_id:req-8267] [app-tier] Memory usage: 7.7GB/8GB (96.25%)
2024-01-15T14:31:00.891Z [WARN] [trace_id:req-8268] [app-tier] Memory usage: 7.8GB/8GB (97.5%)
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:45.123Z [WARN] [trace_id:req-9264] [app-tier] Memory usage: 7.9GB/8GB (98.75%)
2024-01-15T14:45:00.456Z [WARN] [trace_id:req-9265] [app-tier] Memory usage: 7.95GB/8GB (99.4%)
```

**AI Response Issue:** AI suggests "Restart application servers" without showing evidence of actual memory leaks from metrics or logs. AI should provide evidence from memory usage patterns before recommending actions.

**Trace Input (id: 4738):**
```
2024-01-15T14:30:01.123Z [WARN] [trace_id:req-4738] [db-tier] Slow query: SELECT * FROM orders WHERE user_id=? AND status=? took 4523ms
2024-01-15T14:30:02.456Z [WARN] [trace_id:req-4739] [db-tier] Slow query: SELECT * FROM products WHERE category=? AND price>? took 5234ms
2024-01-15T14:30:03.789Z [WARN] [trace_id:req-4740] [db-tier] Slow query: SELECT * FROM cart WHERE user_id=? took 4891ms
2024-01-15T14:30:05.234Z [WARN] [trace_id:req-4741] [db-tier] Slow query: SELECT * FROM orders WHERE user_id=? AND status=? took 5123ms
2024-01-15T14:30:07.891Z [WARN] [trace_id:req-4742] [db-tier] Slow query: SELECT * FROM products WHERE category=? AND price>? took 5456ms
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [WARN] [trace_id:req-5738] [db-tier] Slow query: SELECT * FROM orders WHERE user_id=? AND status=? took 4789ms
2024-01-15T14:44:59.456Z [WARN] [trace_id:req-5739] [db-tier] Slow query: SELECT * FROM cart WHERE user_id=? took 5012ms
```

**AI Response Issue:** AI recommends "Add database indexes" without showing which queries are slow or if indexes would help. AI should provide specific slow query examples and explain why indexes would help.

---

## Failure Mode 9: Incomplete Runbook Retrieval

**Definition:** AI fails to retrieve relevant runbooks or retrieves runbooks that don't match the identified issue.

**Slug:** `incomplete_runbook_retrieval`

**Examples:**

**Trace Input (id: 901):**
```
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-901] [cache-tier] Redis connection pool exhausted: 50/50 connections in use
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-902] [cache-tier] Unable to acquire Redis connection: Pool exhausted
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-903] [cache-tier] Redis connection pool exhausted: 50/50 connections in use
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-904] [cache-tier] Unable to acquire Redis connection: Pool exhausted
2024-01-15T14:30:07.891Z [ERROR] [trace_id:req-905] [cache-tier] Redis connection pool exhausted: 50/50 connections in use
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-1901] [cache-tier] Redis connection pool exhausted: 50/50 connections in use
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-1902] [cache-tier] Unable to acquire Redis connection: Pool exhausted
```

**AI Response Issue:** AI retrieves runbooks about Redis configuration but not about connection pool troubleshooting. AI should retrieve runbooks that specifically address the root cause identified.

**Trace Input (id: 902):**
```
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-902] [db-tier] Deadlock detected: Transaction 12345 waiting for lock held by transaction 67890
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-903] [db-tier] Deadlock detected: Transaction 67890 waiting for lock held by transaction 12345
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-904] [db-tier] Deadlock resolved: Transaction 12345 rolled back
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-905] [db-tier] Deadlock detected: Transaction 23456 waiting for lock held by transaction 78901
2024-01-15T14:30:07.891Z [ERROR] [trace_id:req-906] [db-tier] Deadlock detected: Transaction 78901 waiting for lock held by transaction 23456
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-1902] [db-tier] Deadlock detected: Transaction 34567 waiting for lock held by transaction 89012
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-1903] [db-tier] Deadlock resolved: Transaction 34567 rolled back
```

**AI Response Issue:** AI doesn't retrieve any runbooks or retrieves generic database runbooks instead of deadlock-specific procedures. AI should search for runbooks matching the specific issue type.

**Trace Input (id: 903):**
```
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-903] [app-tier] NullPointerException: at com.example.OrderService.processOrder(OrderService.java:45)
  at com.example.OrderController.createOrder(OrderController.java:23)
  at java.base/java.lang.Thread.run(Thread.java:833)
2024-01-15T14:30:02.456Z [ERROR] [trace_id:req-904] [app-tier] NullPointerException: at com.example.PaymentService.processPayment(PaymentService.java:67)
2024-01-15T14:30:03.789Z [ERROR] [trace_id:req-905] [app-tier] NullPointerException: at com.example.OrderService.processOrder(OrderService.java:45)
  at com.example.OrderController.createOrder(OrderController.java:23)
2024-01-15T14:30:05.234Z [ERROR] [trace_id:req-906] [app-tier] NullPointerException: at com.example.PaymentService.processPayment(PaymentService.java:67)
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [ERROR] [trace_id:req-1903] [app-tier] NullPointerException: at com.example.OrderService.processOrder(OrderService.java:45)
  at com.example.OrderController.createOrder(OrderController.java:23)
2024-01-15T14:44:59.456Z [ERROR] [trace_id:req-1904] [app-tier] NullPointerException: at com.example.PaymentService.processPayment(PaymentService.java:67)
```

**AI Response Issue:** AI retrieves runbooks about infrastructure but not about application error troubleshooting. AI should match runbook retrieval to the tier and issue type being analyzed.

---

## Failure Mode 10: Missing Follow-up Analysis

**Definition:** AI completes initial analysis but doesn't suggest follow-up steps, monitoring, or validation actions.

**Slug:** `missing_followup_analysis`

**Examples:**

**Trace Input (id: 1001):**
```
2024-01-15T14:30:01.123Z [INFO] [trace_id:req-1001] [db-tier] Database cluster restart completed successfully
2024-01-15T14:30:02.456Z [INFO] [trace_id:req-1002] [db-tier] Connection pool restored: 0/100 connections in use
2024-01-15T14:30:03.789Z [INFO] [trace_id:req-1003] [db-tier] All database connections healthy
2024-01-15T14:30:05.234Z [INFO] [trace_id:req-1004] [db-tier] Connection pool status: 5/100 connections in use (5%)
2024-01-15T14:30:07.891Z [INFO] [trace_id:req-1005] [db-tier] Connection pool status: 10/100 connections in use (10%)
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [INFO] [trace_id:req-2001] [db-tier] Connection pool status: 15/100 connections in use (15%)
2024-01-15T14:44:59.456Z [INFO] [trace_id:req-2002] [db-tier] All database connections healthy
```

**AI Response Issue:** AI confirms resolution but doesn't suggest monitoring connection pool metrics or investigating root cause to prevent recurrence. AI should recommend follow-up actions.

**Trace Input (id: 1002):**
```
2024-01-15T14:30:01.123Z [WARN] [trace_id:req-1002] [cache-tier] Cache hit rate: 75% (baseline: 95%)
2024-01-15T14:30:02.456Z [WARN] [trace_id:req-1003] [cache-tier] Cache response time: 45ms (baseline: 5ms)
2024-01-15T14:30:03.789Z [WARN] [trace_id:req-1004] [cache-tier] Cache memory usage: 9.2GB/10GB (92%)
2024-01-15T14:30:05.234Z [WARN] [trace_id:req-1005] [cache-tier] Cache hit rate: 73% (baseline: 95%)
2024-01-15T14:30:07.891Z [WARN] [trace_id:req-1006] [cache-tier] Cache response time: 48ms (baseline: 5ms)
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [WARN] [trace_id:req-2002] [cache-tier] Cache hit rate: 70% (baseline: 95%)
2024-01-15T14:44:59.456Z [WARN] [trace_id:req-2003] [cache-tier] Cache memory usage: 9.5GB/10GB (95%)
```

**AI Response Issue:** AI provides remediation steps but doesn't suggest how to validate the fix worked or what metrics to monitor. AI should include validation and monitoring steps.

**Trace Input (id: 1003):**
```
2024-01-15T14:30:01.123Z [INFO] [trace_id:req-1003] [app-tier] Application error fix deployed: Fixed NullPointerException in OrderService
2024-01-15T14:30:02.456Z [INFO] [trace_id:req-1004] [app-tier] Application restart completed
2024-01-15T14:30:03.789Z [INFO] [trace_id:req-1005] [app-tier] Application health check: OK
2024-01-15T14:30:05.234Z [INFO] [trace_id:req-1006] [app-tier] Application metrics: Error rate 0%, Response time 200ms
2024-01-15T14:30:07.891Z [INFO] [trace_id:req-1007] [app-tier] Application health check: OK
... [truncated: ~1000+ more log lines over 15-minute window] ...
2024-01-15T14:44:58.123Z [INFO] [trace_id:req-2003] [app-tier] Application health check: OK
2024-01-15T14:44:59.456Z [INFO] [trace_id:req-2004] [app-tier] Application metrics: Error rate 0%, Response time 210ms
```

**AI Response Issue:** AI doesn't suggest checking if errors are actually resolved, monitoring error rates, or investigating if the fix addressed the root cause. AI should provide post-remediation validation steps.

---

## Summary

These failure modes represent critical areas where SREnity could provide inaccurate, incomplete, or potentially harmful guidance during incident response. Addressing these failure modes will improve the system's reliability, trustworthiness, and effectiveness in production incident scenarios.

**Key Themes:**
- **Evidence-based analysis**: Always link findings to specific evidence
- **Uncertainty acknowledgment**: Disclaim when confidence is low or information is missing
- **Context gathering**: Ask for missing critical information before making claims
- **Appropriate escalation**: Suggest less disruptive options before destructive actions
- **Validation and follow-up**: Include steps to verify fixes and monitor outcomes
