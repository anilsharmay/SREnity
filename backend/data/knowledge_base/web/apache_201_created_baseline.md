# Apache 201 Created — Resource Creation Baseline

---

## 🧩 Overview

This document provides baseline examples of successful Apache HTTP Server requests returning 201 Created status codes. These examples represent successful resource creation operations and should be used as a reference point for Root Cause Analysis (RCA).

### Purpose

- **Baseline Comparison**: Compare error logs against successful resource creation patterns
- **RCA Support**: Identify what changed between successful and failed creation requests
- **Performance Baseline**: Understand normal creation response times
- **Health Monitoring**: Recognize normal resource creation patterns

---

## 📊 Successful Creation Request Log Samples

### Web Tier (Apache) - 201 Created Logs

```
2024-01-15T15:00:01.123Z [INFO] [trace_id:req-201-a1b2c3] [request_id:req-201] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] POST /api/users - 201 Created - 52ms - User created successfully
2024-01-15T15:00:02.456Z [INFO] [trace_id:req-202-a2b3c4] [request_id:req-202] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] [Apache] POST /api/orders - 201 Created - 58ms - Order created successfully
2024-01-15T15:00:03.789Z [INFO] [trace_id:req-203-a3b4c5] [request_id:req-203] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] POST /api/products - 201 Created - 61ms - Product created successfully
2024-01-15T15:00:04.012Z [INFO] [trace_id:req-204-a4b5c6] [request_id:req-204] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] [Apache] POST /api/cart/items - 201 Created - 55ms - Cart item created successfully
2024-01-15T15:00:05.345Z [INFO] [trace_id:req-205-a5b6c7] [request_id:req-205] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] POST /api/sessions - 201 Created - 48ms - Session created successfully
```

### Apache Access Log Format (201 Created)

```
192.168.1.100 - - [15/Jan/2024:15:00:01 +0000] "POST /api/users HTTP/1.1" 201 1234 "-" "Mozilla/5.0" 52
192.168.1.101 - - [15/Jan/2024:15:00:02 +0000] "POST /api/orders HTTP/1.1" 201 2345 "-" "Mozilla/5.0" 58
192.168.1.102 - - [15/Jan/2024:15:00:03 +0000] "POST /api/products HTTP/1.1" 201 3456 "-" "Mozilla/5.0" 61
```

---

## 📈 Normal Performance Characteristics

### Response Time Baseline

| Endpoint | Method | Normal Response Time | Status |
|----------|--------|----------------------|--------|
| `/api/users` | POST | 48-52ms | ✅ Healthy |
| `/api/orders` | POST | 55-58ms | ✅ Healthy |
| `/api/products` | POST | 58-61ms | ✅ Healthy |
| `/api/cart/items` | POST | 52-55ms | ✅ Healthy |
| `/api/sessions` | POST | 45-48ms | ✅ Healthy |

### Typical Response Time Range
- **Fast**: 45-55ms
- **Normal**: 50-60ms
- **Acceptable**: Up to 100ms
- **Warning**: 100-500ms
- **Critical**: > 500ms

---

## 🔍 Healthy State Indicators

**Normal Operation:**
- Status code: 201 Created
- Response includes Location header with new resource URI
- Response time within normal range (50-60ms)
- No Apache error codes
- Resource successfully created in database

---

This baseline document should be used as a reference point when performing Root Cause Analysis on resource creation operations.

