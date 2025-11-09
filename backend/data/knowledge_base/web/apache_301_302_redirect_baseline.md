# Apache 301/302 Redirect — Redirection Baseline

---

## 🧩 Overview

This document provides baseline examples of Apache HTTP Server requests returning 301 (Permanent Redirect) and 302 (Temporary Redirect) status codes. These examples represent normal redirection operations and should be used as a reference point for Root Cause Analysis (RCA).

### Purpose

- **Baseline Comparison**: Compare error logs against successful redirection patterns
- **RCA Support**: Identify what changed between successful and failed redirects
- **Performance Baseline**: Understand normal redirection response times
- **Health Monitoring**: Recognize normal redirection patterns

---

## 📊 Successful Redirect Request Log Samples

### Web Tier (Apache) - 301 Permanent Redirect Logs

```
2024-01-15T15:00:01.123Z [INFO] [trace_id:req-201-a1b2c3] [request_id:req-201] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] GET /api - 301 Moved Permanently - 12ms - Redirected to /api/v1
2024-01-15T15:00:02.456Z [INFO] [trace_id:req-202-a2b3c4] [request_id:req-202] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] [Apache] GET /old-path - 301 Moved Permanently - 15ms - Redirected to /new-path
```

### Web Tier (Apache) - 302 Temporary Redirect Logs

```
2024-01-15T15:00:03.789Z [INFO] [trace_id:req-203-a3b4c5] [request_id:req-203] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] GET /api/login - 302 Found - 18ms - Redirected to /dashboard
2024-01-15T15:00:04.012Z [INFO] [trace_id:req-204-a4b5c6] [request_id:req-204] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] [Apache] POST /api/auth - 302 Found - 22ms - Redirected to /api/profile
```

### Apache Access Log Format (301/302 Redirect)

```
192.168.1.100 - - [15/Jan/2024:15:00:01 +0000] "GET /api HTTP/1.1" 301 0 "https://example.com" "Mozilla/5.0" 12
192.168.1.101 - - [15/Jan/2024:15:00:02 +0000] "GET /old-path HTTP/1.1" 301 0 "https://example.com" "Mozilla/5.0" 15
192.168.1.102 - - [15/Jan/2024:15:00:03 +0000] "GET /api/login HTTP/1.1" 302 0 "https://example.com" "Mozilla/5.0" 18
```

---

## 📈 Normal Performance Characteristics

### Response Time Baseline

| Redirect Type | Status Code | Normal Response Time | Status |
|---------------|-------------|----------------------|--------|
| Permanent Redirect | 301 | 12-15ms | ✅ Healthy |
| Temporary Redirect | 302 | 18-22ms | ✅ Healthy |

### Typical Response Time Range
- **Fast**: 10-15ms
- **Normal**: 15-25ms
- **Acceptable**: Up to 50ms
- **Warning**: 50-200ms
- **Critical**: > 200ms

---

## 🔍 Healthy State Indicators

**Normal Operation:**
- Status code: 301 or 302
- Location header present with redirect URL
- Response time within normal range (12-25ms)
- No Apache error codes
- Redirect target is accessible

---

This baseline document should be used as a reference point when performing Root Cause Analysis on redirection operations.

