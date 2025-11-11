# Application 503 Service Unavailable — ServiceUnavailableException

---

## 🧩 Overview

A ServiceUnavailableException occurs when a Java/Spring Boot microservice is unable to process requests due to temporary unavailability of required resources, dependencies, or services. This exception indicates that the service is operational but cannot fulfill requests at the current time.

### What is a ServiceUnavailableException?

A ServiceUnavailableException is a Java exception that occurs when:
- External services or dependencies are unavailable
- Required resources are temporarily exhausted
- Service is in maintenance mode
- Circuit breakers are open
- Rate limiting is active
- Service is overloaded

### Java/Spring Boot Behavior

When a ServiceUnavailableException occurs in a Spring Boot microservice:
- The service throws ServiceUnavailableException
- Spring may return 503 Service Unavailable HTTP status
- Circuit breakers may open to protect downstream services
- Retry logic may be triggered
- Service degradation may occur

### Application Tier Symptoms

**Java/Spring Boot Symptoms:**
- ServiceUnavailableException in application logs
- 503 Service Unavailable HTTP responses
- Circuit breaker open states
- External service connection failures
- Resource exhaustion warnings
- Service degradation

---

## 📊 Log Samples

### Application Tier (Java/Spring Boot) Logs

```
2024-01-15T15:00:02.189Z [ERROR] [trace_id:req-202-a2b3c4] [request_id:req-202] [ELB:backend-sg] [AZ:us-east-1b] [EC2:i-0987654321fedcba1] [Service:order-service] ServiceUnavailableException: Order processing service unavailable - 3456ms
2024-01-15T15:00:07.354Z [ERROR] [trace_id:req-207-a7b8c9] [request_id:req-207] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:payment-service] ServiceUnavailableException: Payment gateway connection timeout - 6789ms
2024-01-15T15:00:12.387Z [ERROR] [trace_id:req-212-b1c2d3] [request_id:req-212] [ELB:backend-sg] [AZ:us-east-1b] [EC2:i-0987654321fedcba1] [Service:notification-service] ServiceUnavailableException: Email service unavailable - 2345ms
2024-01-15T15:00:17.420Z [ERROR] [trace_id:req-217-b2c3d4] [request_id:req-217] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:shipping-service] ServiceUnavailableException: Shipping API timeout - 5678ms
2024-01-15T15:00:22.453Z [ERROR] [trace_id:req-222-b3c4d5] [request_id:req-222] [ELB:backend-sg] [AZ:us-east-1b] [EC2:i-0987654321fedcba1] [Service:inventory-service] ServiceUnavailableException: Inventory service circuit breaker open - 1234ms
```

### Spring Boot Exception Format

```
org.springframework.web.server.ServiceUnavailableException: Service temporarily unavailable
    at com.example.orderservice.OrderService.processOrder(OrderService.java:67)
    at com.example.orderservice.OrderController.createOrder(OrderController.java:34)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.java:895)
```

---

## 🔍 Root Cause Analysis

### Primary Causes

1. **External Service Unavailability**
   - Downstream services not responding
   - External APIs unavailable
   - Third-party services down
   - Network connectivity issues
   - Service timeouts

2. **Resource Exhaustion**
   - Connection pool exhausted
   - Thread pool exhausted
   - Database connections unavailable
   - Memory pressure
   - CPU saturation

3. **Circuit Breaker States**
   - Circuit breaker open due to failures
   - Too many failures triggering circuit breaker
   - Circuit breaker not recovering
   - Fallback mechanisms not working

4. **Service Configuration Issues**
   - Incorrect service endpoints
   - Timeout configurations too low
   - Rate limiting too restrictive
   - Service discovery failures

### Common Scenarios

1. **Service Dependencies**
   - Payment gateway unavailable
   - Email service down
   - Database connection issues
   - Cache service unavailable

2. **Load and Capacity**
   - Service overloaded
   - Rate limiting active
   - Request queue full
   - Resource limits reached

3. **Network Issues**
   - Network timeouts
   - Connection failures
   - DNS resolution issues
   - Firewall blocking connections

---

## 🛠️ Troubleshooting Steps

### Immediate Actions

1. **Check Service Health**
   ```bash
   # Check service health endpoint
   curl http://localhost:8080/actuator/health
   
   # Check service status
   systemctl status order-service
   
   # Check service logs
   tail -f /var/log/application/application.log | grep -i "ServiceUnavailableException"
   ```

2. **Check External Dependencies**
   ```bash
   # Test external service connectivity
   curl -v http://payment-gateway:8080/health
   
   # Check network connectivity
   ping payment-gateway-host
   telnet payment-gateway-host 8080
   
   # Check DNS resolution
   nslookup payment-gateway-host
   ```

3. **Check Circuit Breaker Status**
   ```bash
   # Check circuit breaker metrics
   curl http://localhost:8080/actuator/metrics/circuit.breaker.state
   
   # Check Hystrix dashboard if using
   # Access Hystrix dashboard at /hystrix
   ```

### Service Analysis

1. **Review Service Configuration**
   ```yaml
   # Check application.yml or application.properties
   spring:
     cloud:
       circuitbreaker:
         hystrix:
           enabled: true
       loadbalancer:
         enabled: true
   ```

2. **Check Connection Pools**
   ```bash
   # Check database connection pool
   curl http://localhost:8080/actuator/metrics/hikari.connections.active
   
   # Check HTTP client connection pool
   # Review connection pool configuration
   ```

---

## 🔧 Resolution Actions

### Short-term Fixes

1. **Restart Service**
   ```bash
   # Restart service
   systemctl restart order-service
   
   # Verify service is running
   systemctl status order-service
   ```

2. **Reset Circuit Breaker**
   ```java
   // Programmatically reset circuit breaker
   circuitBreaker.reset();
   
   // Or wait for circuit breaker to close automatically
   ```

3. **Increase Timeouts**
   ```yaml
   # Temporarily increase timeouts
   spring:
     cloud:
       loadbalancer:
         timeout: 10000
   ```

### Long-term Solutions

1. **Improve Resilience**
   - Implement proper circuit breakers
   - Add retry logic with exponential backoff
   - Implement fallback mechanisms
   - Add timeout configurations

2. **Service Dependencies**
   - Monitor external service health
   - Implement service discovery
   - Add health checks
   - Implement graceful degradation

3. **Resource Management**
   - Optimize connection pools
   - Implement proper thread pool management
   - Add resource monitoring
   - Scale services as needed

---

## 📈 Prevention Strategies

### Best Practices

1. **Resilience Patterns**
   - Implement circuit breakers
   - Add retry logic
   - Implement fallbacks
   - Use bulkhead pattern

2. **Monitoring**
   - Monitor service health
   - Track circuit breaker states
   - Monitor external dependencies
   - Alert on service unavailability

3. **Configuration**
   - Set appropriate timeouts
   - Configure connection pools
   - Set rate limits
   - Configure circuit breakers

---

## 📋 Incident Response Checklist

### Immediate Response (0-15 minutes)
- [ ] Acknowledge the incident
- [ ] Check application logs for ServiceUnavailableException
- [ ] Check service health endpoints
- [ ] Verify external service availability
- [ ] Check circuit breaker states
- [ ] Begin troubleshooting

### Short-term Response (15-60 minutes)
- [ ] Restart service if needed
- [ ] Check external dependencies
- [ ] Review service configuration
- [ ] Update monitoring alerts
- [ ] Document findings
- [ ] Communicate status updates

### Long-term Response (1-24 hours)
- [ ] Root cause analysis
- [ ] Improve resilience patterns
- [ ] Optimize service dependencies
- [ ] Update configuration
- [ ] Implement preventive measures

---

## 🔍 Advanced Troubleshooting

### Spring Boot Diagnostics
```bash
# Check all actuator endpoints
curl http://localhost:8080/actuator

# Check health details
curl http://localhost:8080/actuator/health

# Check metrics
curl http://localhost:8080/actuator/metrics

# Check environment
curl http://localhost:8080/actuator/env
```

### Circuit Breaker Analysis
```bash
# Check circuit breaker metrics
curl http://localhost:8080/actuator/metrics/circuit.breaker.calls

# Check Hystrix stream
curl http://localhost:8080/actuator/hystrix.stream
```

This comprehensive incident documentation provides detailed guidance for understanding, troubleshooting, and preventing ServiceUnavailableException incidents in Java/Spring Boot microservices.

