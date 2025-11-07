# Apache 400 Bad Request — Client Error Baseline

---

## 🧩 Overview

This document provides baseline examples of Apache HTTP Server requests returning 400 Bad Request status codes. These examples represent client-side errors (invalid requests) and should be used as a reference point for Root Cause Analysis (RCA) to distinguish between client errors and server errors.

### Purpose

- **Baseline Comparison**: Compare error logs against expected client error patterns
- **RCA Support**: Identify if errors are client-side (400) vs server-side (500)
- **Error Classification**: Understand when 400 is expected vs unexpected
- **Health Monitoring**: Recognize normal client error patterns

---

## 📊 Client Error Request Log Samples

### Web Tier (Apache) - 400 Bad Request Logs

```
2024-01-15T15:00:01.123Z [WARN] [trace_id:req-201-a1b2c3] [request_id:req-201] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] POST /api/users - 400 Bad Request - 25ms - Invalid request body format
2024-01-15T15:00:02.456Z [WARN] [trace_id:req-202-a2b3c4] [request_id:req-202] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] [Apache] GET /api/users?id= - 400 Bad Request - 18ms - Missing required parameter
2024-01-15T15:00:03.789Z [WARN] [trace_id:req-203-a3b4c5] [request_id:req-203] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] POST /api/orders - 400 Bad Request - 22ms - Validation failed: invalid email format
2024-01-15T15:00:04.012Z [WARN] [trace_id:req-204-a4b5c6] [request_id:req-204] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] [Apache] PUT /api/products/abc - 400 Bad Request - 20ms - Invalid product ID format
```

### Apache Access Log Format (400 Bad Request)

```
192.168.1.100 - - [15/Jan/2024:15:00:01 +0000] "POST /api/users HTTP/1.1" 400 234 "-" "Mozilla/5.0" 25
192.168.1.101 - - [15/Jan/2024:15:00:02 +0000] "GET /api/users?id= HTTP/1.1" 400 189 "-" "Mozilla/5.0" 18
```

---

## 📈 Normal Performance Characteristics

### Response Time Baseline

| Error Type | Status Code | Normal Response Time | Status |
|------------|-------------|----------------------|--------|
| Invalid Request Body | 400 | 20-25ms | ⚠️ Client Error |
| Missing Parameters | 400 | 15-20ms | ⚠️ Client Error |
| Validation Failed | 400 | 20-25ms | ⚠️ Client Error |
| Invalid Format | 400 | 18-22ms | ⚠️ Client Error |

### Typical Response Time Range
- **Fast**: 15-20ms
- **Normal**: 18-25ms
- **Acceptable**: Up to 50ms
- **Warning**: > 50ms (may indicate server-side processing issues)

---

## 🔍 Error State Indicators

**Expected Client Errors (400):**
- Status code: 400 Bad Request
- Error message indicates client-side issue
- Response time typically fast (15-25ms)
- No Apache error codes (AH0xxxx)
- Error is due to invalid request format/parameters

**When 400 is Unexpected:**
- High volume of 400 errors (may indicate client application bug)
- 400 errors on previously working endpoints
- 400 errors with slow response times (> 50ms)

---

## 🔄 Comparison: 400 vs 500 Errors

### 400 Bad Request (Client Error)
```
2024-01-15T15:00:01.123Z [WARN] [trace_id:req-201-a1b2c3] [request_id:req-201] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] POST /api/users - 400 Bad Request - 25ms - Invalid request body format
```
- **Cause**: Client-side (invalid request)
- **Response Time**: Fast (15-25ms)
- **Log Level**: WARN
- **Apache Error Code**: None

### 500 Internal Server Error (Server Error)
```
2024-01-15T15:00:01.123Z [ERROR] [trace_id:req-201-a1b2c3] [request_id:req-201] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] POST /api/users - 500 Internal Server Error - 5234ms - Application error
```
- **Cause**: Server-side (application/database error)
- **Response Time**: Slow (may timeout)
- **Log Level**: ERROR
- **Apache Error Code**: May include AH0xxxx codes

---

## 📋 RCA Usage Guidelines

### When Investigating 400 Errors

1. **Check if Expected**
   - Is this a known client validation error?
   - Is the client sending invalid data?
   - Is this a new client application bug?

2. **Compare with 200 OK Baseline**
   - What's different about the request?
   - Missing required fields?
   - Invalid format?

3. **Check Volume**
   - Is this a single client error?
   - Or widespread client errors (may indicate server-side issue)?

---

This baseline document should be used as a reference point when performing Root Cause Analysis on client error patterns.

