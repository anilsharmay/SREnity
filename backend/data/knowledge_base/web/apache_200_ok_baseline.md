# Apache 200 OK — Healthy State Baseline

---

## 🧩 Overview

This document provides baseline examples of successful Apache HTTP Server requests returning 200 OK status codes. These examples represent healthy, normal operation and should be used as a reference point for Root Cause Analysis (RCA) when investigating incidents.

### Purpose

- **Baseline Comparison**: Compare error logs against successful request patterns
- **RCA Support**: Identify what changed between successful and failed requests
- **Performance Baseline**: Understand normal response times and patterns
- **Health Monitoring**: Recognize normal operational patterns

### When to Use This Baseline

- During incident investigation to compare failed vs successful requests
- When analyzing performance degradation
- To understand normal request/response patterns
- For establishing monitoring thresholds

---

## 📊 Successful Request Log Samples

### Web Tier (Apache) - 200 OK Logs

```
2024-01-15T15:00:01.123Z [INFO] [trace_id:req-201-a1b2c3] [request_id:req-201] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] GET /api/users - 200 OK - 45ms - Request successful
2024-01-15T15:00:02.456Z [INFO] [trace_id:req-202-a2b3c4] [request_id:req-202] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] [Apache] POST /api/orders - 200 OK - 52ms - Request successful
2024-01-15T15:00:03.789Z [INFO] [trace_id:req-203-a3b4c5] [request_id:req-203] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] GET /api/products - 200 OK - 38ms - Request successful
2024-01-15T15:00:04.012Z [INFO] [trace_id:req-204-a4b5c6] [request_id:req-204] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] [Apache] PUT /api/cart - 200 OK - 41ms - Request successful
2024-01-15T15:00:05.345Z [INFO] [trace_id:req-205-a5b6c7] [request_id:req-205] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] GET /api/profile - 200 OK - 47ms - Request successful
2024-01-15T15:00:06.678Z [INFO] [trace_id:req-206-a6b7c8] [request_id:req-206] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] [Apache] DELETE /api/sessions - 200 OK - 43ms - Request successful
2024-01-15T15:00:07.901Z [INFO] [trace_id:req-207-a7b8c9] [request_id:req-207] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] POST /api/payments - 200 OK - 39ms - Request successful
2024-01-15T15:00:08.234Z [INFO] [trace_id:req-208-a8b9c0] [request_id:req-208] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] [Apache] GET /api/notifications - 200 OK - 44ms - Request successful
2024-01-15T15:00:09.567Z [INFO] [trace_id:req-209-a9b0c1] [request_id:req-209] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] PUT /api/settings - 200 OK - 46ms - Request successful
2024-01-15T15:00:10.890Z [INFO] [trace_id:req-210-a0b1c2] [request_id:req-210] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] [Apache] GET /api/dashboard - 200 OK - 42ms - Request successful
```

### Apache Access Log Format (200 OK)

```
192.168.1.100 - - [15/Jan/2024:15:00:01 +0000] "GET /api/users HTTP/1.1" 200 1234 "-" "Mozilla/5.0" 45
192.168.1.101 - - [15/Jan/2024:15:00:02 +0000] "POST /api/orders HTTP/1.1" 200 2345 "-" "Mozilla/5.0" 52
192.168.1.102 - - [15/Jan/2024:15:00:03 +0000] "GET /api/products HTTP/1.1" 200 3456 "-" "Mozilla/5.0" 38
192.168.1.103 - - [15/Jan/2024:15:00:04 +0000] "PUT /api/cart HTTP/1.1" 200 4567 "-" "Mozilla/5.0" 41
192.168.1.104 - - [15/Jan/2024:15:00:05 +0000] "GET /api/profile HTTP/1.1" 200 5678 "-" "Mozilla/5.0" 47
```

### Apache Error Log Format (No Errors - Normal Operation)

```
[Wed Jan 15 15:00:01.123456 2024] [info] [pid 12345:tid 140234567890176] [client 192.168.1.100:54321] Connection to child 0 established (server localhost:80, client 192.168.1.100)
[Wed Jan 15 15:00:01.123789 2024] [info] [pid 12345:tid 140234567890176] [client 192.168.1.100:54321] Request received from client: GET /api/users HTTP/1.1
[Wed Jan 15 15:00:01.168456 2024] [info] [pid 12345:tid 140234567890176] [client 192.168.1.100:54321] Response sent to client: 200 OK (45ms)
```

---

## 📈 Normal Performance Characteristics

### Response Time Baseline

| Endpoint | Method | Normal Response Time | Status |
|----------|--------|----------------------|--------|
| `/api/users` | GET | 38-48ms | ✅ Healthy |
| `/api/orders` | POST | 39-52ms | ✅ Healthy |
| `/api/products` | GET | 38-39ms | ✅ Healthy |
| `/api/cart` | PUT | 41-44ms | ✅ Healthy |
| `/api/profile` | GET | 42-47ms | ✅ Healthy |
| `/api/sessions` | DELETE | 42-43ms | ✅ Healthy |
| `/api/payments` | POST | 39-41ms | ✅ Healthy |
| `/api/notifications` | GET | 43-44ms | ✅ Healthy |
| `/api/settings` | PUT | 45-46ms | ✅ Healthy |
| `/api/dashboard` | GET | 40-42ms | ✅ Healthy |

### Typical Response Time Range
- **Fast**: 35-45ms
- **Normal**: 40-50ms
- **Acceptable**: Up to 100ms
- **Warning**: 100-500ms
- **Critical**: > 500ms

---

## 🔍 Healthy State Indicators

### Apache Server Health

**Normal Operation:**
- No Apache error codes (AH0xxxx) in logs
- Response times within normal range (35-50ms)
- All requests returning 200 OK
- No timeout errors
- No connection errors
- No upstream server errors

**Key Metrics:**
- Request success rate: 100%
- Average response time: 40-50ms
- Error rate: 0%
- Connection pool utilization: < 80%
- Active workers: < MaxRequestWorkers

### Request Flow (Healthy)

```
Client Request
    ↓
Apache HTTP Server (Frontend)
    ↓ (Proxies to)
Application Server (Backend)
    ↓ (Queries)
Database (RDS)
    ↓ (Returns)
Application Server
    ↓ (Returns)
Apache HTTP Server
    ↓ (Returns)
Client (200 OK)
```

---

## 🔄 Comparison: Healthy vs Error States

### Example: Same Endpoint, Different States

**Healthy State (200 OK):**
```
2024-01-15T15:00:01.123Z [INFO] [trace_id:req-201-a1b2c3] [request_id:req-201] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] GET /api/users - 200 OK - 45ms - Request successful
```

**Error State (502 Bad Gateway):**
```
2024-01-15T14:30:01.123Z [ERROR] [trace_id:req-101-w1x2y3] [request_id:req-101] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] AH01084: GET /api/users - 502 Bad Gateway - 5234ms - Timeout while reading response header from upstream server
```

**Key Differences:**
- Response time: 45ms (healthy) vs 5234ms (error)
- Status code: 200 OK vs 502 Bad Gateway
- Log level: INFO vs ERROR
- Apache error code: None vs AH01084
- Message: "Request successful" vs "Timeout while reading response header"

---

## 📋 RCA Usage Guidelines

### When Investigating Incidents

1. **Compare Request Patterns**
   - Same endpoint, same method
   - Same time period (before/after)
   - Same client/user if applicable

2. **Analyze Response Times**
   - Normal: 40-50ms
   - Degraded: 100-500ms
   - Failed: Timeout or error

3. **Check Request Flow**
   - Verify all tiers are healthy
   - Check upstream server availability
   - Verify database connectivity

4. **Identify Changes**
   - What changed between healthy and error states?
   - Configuration changes?
   - Traffic patterns?
   - Resource constraints?

### Common RCA Questions

- Was this endpoint working before? (Check baseline)
- What was the normal response time? (Compare with baseline)
- Are other endpoints affected? (Check baseline patterns)
- When did it start failing? (Compare timestamps)
- What's different about failing requests? (Compare patterns)

---

## 🎯 Monitoring Recommendations

### Metrics to Track

1. **Response Time**
   - P50 (median): ~45ms
   - P95: ~50ms
   - P99: ~60ms

2. **Success Rate**
   - Target: 99.9%+
   - Monitor: 200 OK vs error status codes

3. **Request Volume**
   - Normal: Baseline volume
   - Alert: Significant increase/decrease

4. **Error Rate**
   - Target: < 0.1%
   - Alert: Any increase from baseline

---

## 📚 Related Documents

- **Error Incidents**: See other web_incidents files for error state examples
- **Technology Stack**: See TECHNOLOGY_IDENTIFICATION.md for infrastructure details
- **Scenarios**: See logs/scenario2_app_issue and scenario3_db_issue for healthy web tier examples

---

This baseline document should be used as a reference point when performing Root Cause Analysis on Apache HTTP Server incidents.

