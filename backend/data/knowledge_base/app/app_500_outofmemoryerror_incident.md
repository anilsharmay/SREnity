# Application 500 Internal Server Error — OutOfMemoryError

---

## 🧩 Overview

An OutOfMemoryError occurs when the Java Virtual Machine (JVM) cannot allocate an object because it is out of memory, and no more memory could be made available by the garbage collector. This is a critical error in Java/Spring Boot applications that can cause service crashes and unavailability.

### What is an OutOfMemoryError?

An OutOfMemoryError is a Java runtime error that occurs when:
- The JVM heap space is exhausted
- The JVM cannot allocate memory for new objects
- Garbage collection cannot free enough memory
- Memory leaks prevent proper garbage collection
- Application memory requirements exceed available heap

### Java/Spring Boot Behavior

When an OutOfMemoryError occurs in a Spring Boot microservice:
- The JVM throws OutOfMemoryError when heap is exhausted
- The application may crash or become unresponsive
- Garbage collection may run continuously (GC thrashing)
- Service becomes unavailable
- May require JVM restart to recover

### Application Tier Symptoms

**Java/Spring Boot Symptoms:**
- OutOfMemoryError in application logs
- JVM heap space exhaustion
- Service crashes or becomes unresponsive
- High garbage collection activity
- Slow application performance before crash
- 500 Internal Server Error responses

---

## 📊 Log Samples

### Application Tier (Java/Spring Boot) Logs

```
2024-01-15T15:00:03.222Z [ERROR] [trace_id:req-203-a3b4c5] [request_id:req-203] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:product-service] OutOfMemoryError: Java heap space exhausted - 1234ms
2024-01-15T15:00:10.453Z [ERROR] [trace_id:req-210-a0b1c2] [request_id:req-210] [ELB:backend-sg] [AZ:us-east-1b] [EC2:i-0987654321fedcba1] [Service:dashboard-service] OutOfMemoryError: Unable to allocate memory for dashboard data - 5678ms
2024-01-15T15:00:15.486Z [ERROR] [trace_id:req-215-b4c5d6] [request_id:req-215] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:analytics-service] OutOfMemoryError: Java heap space - 3456ms
2024-01-15T15:00:20.519Z [ERROR] [trace_id:req-220-b5c6d7] [request_id:req-220] [ELB:backend-sg] [AZ:us-east-1b] [EC2:i-0987654321fedcba1] [Service:report-service] OutOfMemoryError: GC overhead limit exceeded - 7890ms
2024-01-15T15:00:25.552Z [ERROR] [trace_id:req-225-b6c7d8] [request_id:req-225] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:cache-service] OutOfMemoryError: Metaspace exhausted - 2345ms
```

### JVM Error Format

```
Exception in thread "main" java.lang.OutOfMemoryError: Java heap space
    at java.util.Arrays.copyOf(Arrays.java:3210)
    at java.util.ArrayList.grow(ArrayList.java:267)
    at java.util.ArrayList.ensureExplicitCapacity(ArrayList.java:241)
    at java.util.ArrayList.ensureCapacityInternal(ArrayList.java:233)
    at java.util.ArrayList.add(ArrayList.java:464)
    at com.example.service.DataProcessor.process(DataProcessor.java:45)
```

---

## 🔍 Root Cause Analysis

### Primary Causes

1. **Memory Leaks**
   - Objects not being garbage collected
   - Static collections growing unbounded
   - Event listeners not removed
   - Caches without size limits
   - Thread-local variables not cleared

2. **Insufficient Heap Size**
   - JVM heap size too small for workload
   - Max heap (-Xmx) not configured properly
   - Initial heap (-Xms) too small
   - Heap size not matching application needs

3. **Large Object Allocations**
   - Processing large datasets in memory
   - Loading entire files into memory
   - Large collections without pagination
   - In-memory caching of large objects

4. **Garbage Collection Issues**
   - GC not running frequently enough
   - GC unable to free memory
   - GC overhead limit exceeded
   - Inefficient GC configuration

### Common Scenarios

1. **Data Processing Issues**
   - Processing large datasets without streaming
   - Loading entire database result sets
   - In-memory sorting of large collections
   - Batch processing without memory limits

2. **Caching Problems**
   - Unbounded cache growth
   - Cache eviction not working
   - Memory-intensive cache implementations
   - Cache size not configured

3. **Concurrency Issues**
   - Too many concurrent requests
   - Thread pool exhaustion
   - Memory per request too high
   - Request queue growing unbounded

---

## 🛠️ Troubleshooting Steps

### Immediate Actions

1. **Check JVM Memory Usage**
   ```bash
   # Check JVM process memory
   jps -l
   jmap -heap <pid>
   
   # Check memory statistics
   jstat -gc <pid> 1000
   
   # Check heap dump
   jmap -dump:format=b,file=heap.hprof <pid>
   ```

2. **Check Application Logs**
   ```bash
   # Check for OutOfMemoryError
   tail -f /var/log/application/application.log | grep -i "OutOfMemoryError"
   
   # Check GC logs
   tail -f /var/log/application/gc.log
   
   # Check service logs
   journalctl -u product-service -f | grep -i "OutOfMemoryError"
   ```

3. **Check System Resources**
   ```bash
   # Check system memory
   free -h
   
   # Check process memory
   ps aux | grep java
   
   # Check memory limits
   cat /proc/<pid>/limits
   ```

### Memory Analysis

1. **Analyze Heap Dump**
   ```bash
   # Use jhat to analyze heap dump
   jhat heap.hprof
   
   # Use Eclipse MAT (Memory Analyzer Tool)
   # Import heap.hprof into Eclipse MAT
   # Analyze memory leaks
   # Identify largest objects
   ```

2. **Review GC Logs**
   ```bash
   # Check GC frequency and duration
   grep "GC" /var/log/application/gc.log
   
   # Check GC overhead
   grep "GC overhead" /var/log/application/gc.log
   
   # Analyze GC patterns
   # Use GCViewer or similar tools
   ```

---

## 🔧 Resolution Actions

### Short-term Fixes

1. **Increase Heap Size**
   ```bash
   # Increase JVM heap size
   export JAVA_OPTS="-Xms2g -Xmx4g -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m"
   
   # Restart service
   systemctl restart product-service
   ```

2. **Restart Service**
   ```bash
   # Restart service to clear memory
   systemctl restart product-service
   
   # Verify service is running
   systemctl status product-service
   ```

3. **Clear Caches**
   ```bash
   # Clear application caches if possible
   curl -X POST http://localhost:8080/actuator/caches/clear
   
   # Or restart service
   systemctl restart product-service
   ```

### Long-term Solutions

1. **Fix Memory Leaks**
   - Identify and fix memory leaks from heap dump analysis
   - Remove unbounded collections
   - Implement proper cache eviction
   - Clear thread-local variables

2. **Optimize Memory Usage**
   - Implement streaming for large datasets
   - Use pagination for database queries
   - Optimize object creation
   - Reduce object retention

3. **JVM Tuning**
   ```bash
   # Optimize GC settings
   export JAVA_OPTS="-Xms4g -Xmx8g \
     -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=200 \
     -XX:+HeapDumpOnOutOfMemoryError \
     -XX:HeapDumpPath=/var/log/application/heap-dumps"
   ```

---

## 📈 Prevention Strategies

### Best Practices

1. **Memory Management**
   - Set appropriate heap sizes
   - Monitor memory usage
   - Implement memory limits
   - Use memory-efficient data structures

2. **Code Quality**
   - Avoid memory leaks
   - Use streaming for large data
   - Implement proper caching
   - Clear resources properly

3. **Monitoring**
   - Monitor heap usage
   - Alert on high memory usage
   - Track GC performance
   - Monitor OutOfMemoryError rates

---

## 📋 Incident Response Checklist

### Immediate Response (0-15 minutes)
- [ ] Acknowledge the incident
- [ ] Check application logs for OutOfMemoryError
- [ ] Check JVM memory usage
- [ ] Identify affected service
- [ ] Restart service if needed
- [ ] Begin troubleshooting

### Short-term Response (15-60 minutes)
- [ ] Increase heap size if needed
- [ ] Generate heap dump for analysis
- [ ] Check GC logs
- [ ] Update monitoring alerts
- [ ] Document findings
- [ ] Communicate status updates

### Long-term Response (1-24 hours)
- [ ] Root cause analysis from heap dump
- [ ] Fix memory leaks
- [ ] Optimize memory usage
- [ ] Tune JVM settings
- [ ] Update monitoring
- [ ] Implement preventive measures

---

## 🔍 Advanced Troubleshooting

### JVM Memory Diagnostics
```bash
# Generate heap dump
jmap -dump:live,format=b,file=heap.hprof <pid>

# Analyze heap dump with jhat
jhat -J-Xmx4g heap.hprof

# Check memory statistics
jstat -gc <pid> 1000 10

# Check memory pools
jmap -heap <pid>
```

### GC Analysis
```bash
# Enable GC logging
export JAVA_OPTS="-Xlog:gc*:file=/var/log/application/gc.log:time,level,tags"

# Analyze GC logs
# Use GCViewer, GCPlot, or similar tools
```

This comprehensive incident documentation provides detailed guidance for understanding, troubleshooting, and preventing OutOfMemoryError incidents in Java/Spring Boot microservices.

