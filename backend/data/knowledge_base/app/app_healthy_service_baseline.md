# Java/Spring Boot Healthy Service — Service Health Baseline

---

## 🧩 Overview

This document provides baseline examples of healthy Java/Spring Boot microservice states. These examples represent normal service health and should be used as a reference point for Root Cause Analysis (RCA) when investigating service health incidents.

### Purpose

- **Baseline Comparison**: Compare error logs against healthy service patterns
- **RCA Support**: Identify what changed between healthy and unhealthy services
- **Health Monitoring**: Recognize normal service health patterns
- **Service Status**: Understand normal service availability

---

## 📊 Healthy Service Log Samples

### Application Tier (Java/Spring Boot) - Healthy Service Logs

```
2024-01-15T14:30:01.156Z [INFO] [trace_id:startup-001] [request_id:startup-001] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:user-service] Service started successfully - Spring Boot 2.7.0
2024-01-15T14:30:01.234Z [INFO] [trace_id:startup-001] [request_id:startup-001] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:user-service] Tomcat started on port(s): 8080 (http)
2024-01-15T14:30:01.256Z [INFO] [trace_id:startup-001] [request_id:startup-001] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:user-service] Started UserServiceApplication in 2.345 seconds
2024-01-15T14:30:01.278Z [INFO] [trace_id:health-001] [request_id:health-001] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:user-service] Health check: UP
2024-01-15T14:30:01.300Z [INFO] [trace_id:health-001] [request_id:health-001] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:user-service] Database connection: Connected
2024-01-15T14:30:01.322Z [INFO] [trace_id:health-001] [request_id:health-001] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:user-service] Connection pool: 5/10 active connections
```

### Spring Boot Actuator Health (All Services Healthy)

```
GET /actuator/health
{
  "status": "UP",
  "components": {
    "db": {
      "status": "UP",
      "details": {
        "database": "MySQL",
        "validationQuery": "isValid()"
      }
    },
    "diskSpace": {
      "status": "UP",
      "details": {
        "total": 500000000000,
        "free": 250000000000,
        "threshold": 10485760
      }
    },
    "ping": {
      "status": "UP"
    }
  }
}
```

### Service Discovery (Healthy)

```
GET /actuator/info
{
  "app": {
    "name": "user-service",
    "version": "1.0.0",
    "status": "UP"
  },
  "build": {
    "version": "1.0.0",
    "time": "2024-01-15T10:00:00Z"
  }
}
```

---

## 📈 Normal Service Health Characteristics

### Service Status Baseline

| Service | Status | Health Check | Status |
|---------|--------|--------------|--------|
| user-service | UP | /actuator/health | ✅ Healthy |
| order-service | UP | /actuator/health | ✅ Healthy |
| product-service | UP | /actuator/health | ✅ Healthy |
| cart-service | UP | /actuator/health | ✅ Healthy |
| session-service | UP | /actuator/health | ✅ Healthy |
| payment-service | UP | /actuator/health | ✅ Healthy |
| notification-service | UP | /actuator/health | ✅ Healthy |
| settings-service | UP | /actuator/health | ✅ Healthy |
| dashboard-service | UP | /actuator/health | ✅ Healthy |

### Service Startup Time Baseline
- **Normal**: 2-5 seconds
- **Acceptable**: Up to 10 seconds
- **Warning**: 10-30 seconds
- **Critical**: > 30 seconds or startup failure

---

## 🔍 Healthy State Indicators

**Normal Service Operation:**
- Service status: UP
- Health check: Passing
- Database connection: Connected
- Connection pool: < 80% utilization
- Memory usage: < 80% of heap
- No exceptions during startup
- All dependencies available

**Key Metrics:**
- Service availability: 100%
- Health check success rate: 100%
- Startup success rate: 100%
- Dependency availability: 100%
- Resource utilization: < 80%

---

## 🔄 Comparison: Healthy vs Error States

### Example: Service Health States

**Healthy State (Service UP):**
```
2024-01-15T14:30:01.278Z [INFO] [trace_id:health-001] [request_id:health-001] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:user-service] Health check: UP
GET /actuator/health
{
  "status": "UP",
  "components": {
    "db": { "status": "UP" }
  }
}
```

**Error State (ServiceUnavailableException):**
```
2024-01-15T15:00:02.189Z [ERROR] [trace_id:req-202-a2b3c4] [request_id:req-202] [ELB:backend-sg] [AZ:us-east-1b] [EC2:i-0987654321fedcba1] [Service:order-service] ServiceUnavailableException: Order processing service unavailable - 3456ms
GET /actuator/health
{
  "status": "DOWN",
  "components": {
    "db": { "status": "DOWN" }
  }
}
```

**Error State (ClassNotFoundException):**
```
2024-01-15T15:00:09.420Z [ERROR] [trace_id:req-209-a9b0c1] [request_id:req-209] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:settings-service] ClassNotFoundException: Settings configuration class not found - 3456ms
Service failed to start
```

**Key Differences:**
- Status: UP vs DOWN/Exception
- Health check: Passing vs Failing
- Service availability: Available vs Unavailable
- Dependencies: Available vs Missing

---

## 📋 RCA Usage Guidelines

### When Investigating Service Health Incidents

1. **Compare Service States**
   - Same service, different time periods
   - Same service, before/after changes
   - Multiple services for patterns

2. **Check Health Endpoints**
   - Normal: All endpoints UP
   - Warning: Some endpoints degraded
   - Critical: Service DOWN

3. **Analyze Dependencies**
   - Normal: All dependencies available
   - Warning: Some dependencies unavailable
   - Critical: Critical dependencies unavailable

4. **Identify Changes**
   - What changed between healthy and error states?
   - Configuration changes?
   - Dependency updates?
   - Resource constraints?

---

## 🎯 Monitoring Recommendations

### Metrics to Track

1. **Service Availability**
   - Target: 99.9%+
   - Monitor: Service UP time vs DOWN time

2. **Health Check Success Rate**
   - Target: 100%
   - Alert: Any health check failures

3. **Startup Success Rate**
   - Target: 100%
   - Alert: Any startup failures

4. **Dependency Availability**
   - Target: 100%
   - Alert: Any dependency failures

---

This baseline document should be used as a reference point when performing Root Cause Analysis on Java/Spring Boot service health incidents.

