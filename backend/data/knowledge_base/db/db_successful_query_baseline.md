# MySQL Successful Query — Healthy State Baseline

---

## 🧩 Overview

This document provides baseline examples of successful MySQL/InnoDB database queries. These examples represent healthy, normal database operation and should be used as a reference point for Root Cause Analysis (RCA) when investigating database incidents.

### Purpose

- **Baseline Comparison**: Compare error logs against successful query patterns
- **RCA Support**: Identify what changed between successful and failed queries
- **Performance Baseline**: Understand normal query execution times
- **Health Monitoring**: Recognize normal database operational patterns

### When to Use This Baseline

- During incident investigation to compare failed vs successful queries
- When analyzing query performance degradation
- To understand normal query execution patterns
- For establishing monitoring thresholds

---

## 📊 Successful Query Log Samples

### Database Tier (MySQL/InnoDB) - Successful Query Logs

```
2024-01-15T14:30:01.156Z [INFO] [trace_id:req-101-w1x2y3] [request_id:req-101] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Query executed successfully - 18ms
2024-01-15T14:30:02.189Z [INFO] [trace_id:req-102-w2x3y4] [request_id:req-102] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Query executed successfully - 22ms
2024-01-15T14:30:03.222Z [INFO] [trace_id:req-103-w3x4y5] [request_id:req-103] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Query executed successfully - 19ms
2024-01-15T14:30:04.255Z [INFO] [trace_id:req-104-w4x5y6] [request_id:req-104] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Query executed successfully - 21ms
2024-01-15T14:30:05.288Z [INFO] [trace_id:req-105-w5x6y7] [request_id:req-105] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Query executed successfully - 17ms
2024-01-15T14:30:06.321Z [INFO] [trace_id:req-106-w6x7y8] [request_id:req-106] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Query executed successfully - 20ms
2024-01-15T14:30:07.354Z [INFO] [trace_id:req-107-w7x8y9] [request_id:req-107] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Query executed successfully - 18ms
2024-01-15T14:30:08.387Z [INFO] [trace_id:req-108-w8x9y0] [request_id:req-108] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Query executed successfully - 23ms
2024-01-15T14:30:09.420Z [INFO] [trace_id:req-109-w9x0y1] [request_id:req-109] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Query executed successfully - 19ms
2024-01-15T14:30:10.453Z [INFO] [trace_id:req-110-w0x1y2] [request_id:req-110] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Query executed successfully - 21ms
```

### MySQL Slow Query Log Format (Successful - Not Slow)

```
# Time: 2024-01-15T14:30:01.156000Z
# User@Host: app[app] @ [192.168.1.100] Id: 100
# Query_time: 0.018000  Lock_time: 0.001000 Rows_sent: 10  Rows_examined: 10
SET timestamp=1705316401;
SELECT * FROM users WHERE id = 12345;
```

### MySQL General Query Log Format (Successful)

```
2024-01-15T14:30:01.156000Z      100 Query     SELECT * FROM users WHERE id = 12345
2024-01-15T14:30:01.174000Z      100 Query     COMMIT
2024-01-15T14:30:02.189000Z      101 Query     INSERT INTO orders (user_id, total) VALUES (12345, 99.99)
2024-01-15T14:30:02.211000Z      101 Query     COMMIT
```

---

## 📈 Normal Performance Characteristics

### Query Execution Time Baseline

| Query Type | Normal Execution Time | Status |
|------------|----------------------|--------|
| Simple SELECT (indexed) | 15-25ms | ✅ Healthy |
| Simple INSERT | 18-25ms | ✅ Healthy |
| Simple UPDATE (indexed) | 20-30ms | ✅ Healthy |
| Simple DELETE (indexed) | 18-25ms | ✅ Healthy |
| JOIN queries (small) | 25-50ms | ✅ Healthy |
| Aggregate queries | 30-60ms | ✅ Healthy |

### Typical Query Execution Time Range
- **Fast**: 15-25ms
- **Normal**: 18-30ms
- **Acceptable**: Up to 100ms
- **Warning**: 100-1000ms (approaching slow query threshold)
- **Critical**: > 1000ms (slow query)

---

## 🔍 Healthy State Indicators

### MySQL Database Health

**Normal Operation:**
- Query execution time: 15-30ms
- No deadlock errors
- No lock wait timeout errors
- No connection errors
- Transactions commit successfully
- No slow query warnings

**Key Metrics:**
- Query success rate: 100%
- Average query time: 18-25ms
- Error rate: 0%
- Connection pool utilization: < 80%
- Active connections: < max_connections limit

### Database Connection Health

**Normal Connection State:**
```
Threads_connected: 45
Threads_running: 5
Max_used_connections: 50
max_connections: 100
Connection utilization: 45%
```

---

## 🔄 Comparison: Healthy vs Error States

### Example: Same Query, Different States

**Healthy State (Successful Query):**
```
2024-01-15T14:30:01.156Z [INFO] [trace_id:req-101-w1x2y3] [request_id:req-101] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Query executed successfully - 18ms
```

**Error State (Deadlock):**
```
2024-01-15T16:00:01.156Z [ERROR] [trace_id:req-301-d1e2f3] [request_id:req-301] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Deadlock: Deadlock detected in transaction - 15234ms
```

**Key Differences:**
- Execution time: 18ms (healthy) vs 15234ms (error)
- Status: Success vs Deadlock error
- Log level: INFO vs ERROR
- Transaction: Committed vs Rolled back

### Example: Connection States

**Healthy State (Normal Connection):**
```
2024-01-15T14:30:01.156Z [INFO] [RDS:database-sg] [DB:whizlabs-db] Connection established - total connections: 45/100
```

**Error State (Too Many Connections):**
```
2024-01-15T16:00:03.222Z [ERROR] [RDS:database-sg] [DB:whizlabs-db] Connection Error: Too many connections (max_connections = 100) - 0ms
```

---

## 📋 RCA Usage Guidelines

### When Investigating Database Incidents

1. **Compare Query Patterns**
   - Same query, same table
   - Same time period (before/after)
   - Same connection/user if applicable

2. **Analyze Execution Times**
   - Normal: 15-30ms
   - Degraded: 100-1000ms
   - Failed: Timeout or error

3. **Check Connection State**
   - Normal: < 80% of max_connections
   - Warning: 80-90%
   - Critical: > 90% or at limit

4. **Identify Changes**
   - What changed between healthy and error states?
   - Configuration changes?
   - Query patterns?
   - Load patterns?
   - Resource constraints?

### Common RCA Questions

- Was this query working before? (Check baseline)
- What was the normal execution time? (Compare with baseline)
- Are other queries affected? (Check baseline patterns)
- When did it start failing? (Compare timestamps)
- What's different about failing queries? (Compare patterns)

---

## 🎯 Monitoring Recommendations

### Metrics to Track

1. **Query Performance**
   - P50 (median): ~20ms
   - P95: ~50ms
   - P99: ~100ms

2. **Success Rate**
   - Target: 99.9%+
   - Monitor: Successful queries vs error queries

3. **Connection Usage**
   - Normal: < 80% of max_connections
   - Alert: > 80% utilization

4. **Error Rate**
   - Target: < 0.1%
   - Alert: Any increase from baseline

---

## 📚 Related Documents

- **Error Incidents**: See other db_incidents files for error state examples
- **Technology Stack**: See TECHNOLOGY_IDENTIFICATION.md for infrastructure details
- **Scenarios**: See logs/scenario1_web_issue and scenario2_app_issue for healthy database tier examples

---

This baseline document should be used as a reference point when performing Root Cause Analysis on MySQL/InnoDB database incidents.

