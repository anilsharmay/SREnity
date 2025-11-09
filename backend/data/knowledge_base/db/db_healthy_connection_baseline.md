# MySQL Healthy Connection — Connection Baseline

---

## 🧩 Overview

This document provides baseline examples of healthy MySQL database connections. These examples represent normal connection patterns and should be used as a reference point for Root Cause Analysis (RCA) when investigating connection-related incidents.

### Purpose

- **Baseline Comparison**: Compare error logs against healthy connection patterns
- **RCA Support**: Identify what changed between healthy and failed connections
- **Performance Baseline**: Understand normal connection behavior
- **Health Monitoring**: Recognize normal connection patterns

---

## 📊 Healthy Connection Log Samples

### Database Tier (MySQL) - Healthy Connection Logs

```
2024-01-15T14:30:01.156Z [INFO] [trace_id:req-101-w1x2y3] [request_id:req-101] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Connection established - total connections: 45/100
2024-01-15T14:30:02.189Z [INFO] [trace_id:req-102-w2x3y4] [request_id:req-102] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Connection established - total connections: 46/100
2024-01-15T14:30:03.222Z [INFO] [trace_id:req-103-w3x4y5] [request_id:req-103] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Connection established - total connections: 47/100
2024-01-15T14:30:04.255Z [INFO] [trace_id:req-104-w4x5y6] [request_id:req-104] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Connection closed - total connections: 46/100
2024-01-15T14:30:05.288Z [INFO] [trace_id:req-105-w5x6y7] [request_id:req-105] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Connection established - total connections: 47/100
```

### MySQL Connection Status (Healthy)

```
Threads_connected: 45
Threads_running: 5
Max_used_connections: 50
max_connections: 100
Connection utilization: 45%
```

### MySQL Process List (Healthy)

```
+----+------+-----------------+--------+---------+------+------------+------------------+
| Id | User | Host            | db     | Command | Time | State      | Info             |
+----+------+-----------------+--------+---------+------+------------+------------------+
| 100| app  | 192.168.1.100   | whizlabs-db | Query | 0  | executing  | SELECT * FROM users WHERE id = 12345 |
| 101| app  | 192.168.1.101   | whizlabs-db | Sleep | 5  |            | NULL |
| 102| app  | 192.168.1.102   | whizlabs-db | Query | 0  | executing  | INSERT INTO orders ... |
+----+------+-----------------+--------+---------+------+------------+------------------+
```

---

## 📈 Normal Performance Characteristics

### Connection Metrics Baseline

| Metric | Normal Value | Status |
|--------|--------------|--------|
| Total Connections | < 80% of max_connections | ✅ Healthy |
| Active Connections | < 20% of total connections | ✅ Healthy |
| Idle Connections | < 60% of total connections | ✅ Healthy |
| Connection Pool Utilization | < 80% | ✅ Healthy |
| Connection Wait Time | 0ms | ✅ Healthy |

### Typical Connection Patterns
- **Normal**: 40-60% of max_connections
- **Acceptable**: Up to 80% of max_connections
- **Warning**: 80-90% of max_connections
- **Critical**: > 90% or at limit

---

## 🔍 Healthy State Indicators

**Normal Connection Operation:**
- Connections established successfully
- No "Too many connections" errors
- Connection pool not exhausted
- Connections released properly
- No connection leaks
- Connection wait time: 0ms

**Key Metrics:**
- Connection success rate: 100%
- Connection pool utilization: < 80%
- Active connections: < 20% of total
- Idle connections: < 60% of total
- Connection errors: 0%

---

## 🔄 Comparison: Healthy vs Error States

### Example: Connection States

**Healthy State (Normal Connection):**
```
2024-01-15T14:30:01.156Z [INFO] [RDS:database-sg] [DB:whizlabs-db] Connection established - total connections: 45/100
Threads_connected: 45
Connection utilization: 45%
```

**Error State (Too Many Connections):**
```
2024-01-15T16:00:03.222Z [ERROR] [RDS:database-sg] [DB:whizlabs-db] Connection Error: Too many connections (max_connections = 100) - 0ms
Threads_connected: 100
Connection utilization: 100%
```

**Error State (Connection Pool Exhausted):**
```
2024-01-15T16:00:07.354Z [ERROR] [RDS:database-sg] [DB:whizlabs-db] Connection Error: Database connection pool exhausted - 2345ms
```

**Key Differences:**
- Connection count: 45/100 (healthy) vs 100/100 (error)
- Status: Established vs Error
- Log level: INFO vs ERROR
- Wait time: 0ms vs timeout

---

## 📋 RCA Usage Guidelines

### When Investigating Connection Incidents

1. **Compare Connection Patterns**
   - Same time period (before/after)
   - Same application/service
   - Same connection pool

2. **Analyze Connection Usage**
   - Normal: < 80% of max_connections
   - Warning: 80-90%
   - Critical: > 90% or at limit

3. **Check Connection Lifecycle**
   - Connections established properly?
   - Connections released properly?
   - Connection leaks?
   - Idle connections accumulating?

4. **Identify Changes**
   - What changed between healthy and error states?
   - Application scaling?
   - Connection pool configuration?
   - Traffic patterns?
   - Connection leaks?

---

## 🎯 Monitoring Recommendations

### Metrics to Track

1. **Connection Usage**
   - Current connections: < 80% of max
   - Peak connections: < 90% of max
   - Connection pool utilization: < 80%

2. **Connection Success Rate**
   - Target: 100%
   - Monitor: Successful vs failed connections

3. **Connection Wait Time**
   - Target: 0ms average
   - Alert: Wait time > 100ms

4. **Connection Errors**
   - Target: 0%
   - Alert: Any connection errors

---

This baseline document should be used as a reference point when performing Root Cause Analysis on MySQL connection incidents.

