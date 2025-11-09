# Database 503 Service Unavailable — MySQL Connection Pool Exhausted

---

## 🧩 Overview

A connection pool exhaustion occurs when all available connections in a database connection pool are in use and no connections are available for new requests. This error indicates that the application's connection pool has reached its maximum capacity.

### What is Connection Pool Exhaustion?

Connection pool exhaustion occurs when:
- All connections in pool are in use
- No connections available for new requests
- Application cannot acquire database connection
- Requests queue waiting for connections
- Service becomes unavailable

### MySQL/Application Behavior

When connection pool is exhausted:
- Application cannot get connection from pool
- Requests wait for available connections
- Timeout errors occur
- Application errors propagate
- Service degradation occurs

### Database Tier Symptoms

**MySQL/Application Symptoms:**
- Connection pool exhaustion errors
- Connection timeout errors
- Application request failures
- High connection pool usage
- Service unavailability

---

## 📊 Log Samples

### Application Tier Logs

```
2024-01-15T15:00:05.288Z [ERROR] [trace_id:req-205-a5b6c7] [request_id:req-205] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:user-service] SQLException: Database connection pool exhausted - 8901ms
2024-01-15T15:00:10.321Z [ERROR] [trace_id:req-210-b1c2d3] [request_id:req-210] [ELB:backend-sg] [AZ:us-east-1b] [EC2:i-0987654321fedcba1] [Service:order-service] SQLException: Connection pool exhausted - 12000ms
2024-01-15T15:00:15.354Z [ERROR] [trace_id:req-215-b2c3d4] [request_id:req-215] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:product-service] SQLException: Unable to acquire connection from pool - 15000ms
```

### Database Tier (MySQL) Logs

```
2024-01-15T15:00:05.288Z [INFO] [RDS:database-sg] [DB:whizlabs-db] Connection established - total connections: 95/100
2024-01-15T15:00:10.321Z [INFO] [RDS:database-sg] [DB:whizlabs-db] Connection established - total connections: 98/100
2024-01-15T15:00:15.354Z [WARN] [RDS:database-sg] [DB:whizlabs-db] High connection count: 99/100
```

### Java Exception Format

```
java.sql.SQLException: Connection pool exhausted
    at com.zaxxer.hikari.pool.HikariPool.getConnection(HikariPool.java:195)
    at com.zaxxer.hikari.pool.HikariPool.getConnection(HikariPool.java:147)
    at com.zaxxer.hikari.HikariDataSource.getConnection(HikariDataSource.java:112)
```

---

## 🔍 Root Cause Analysis

### Primary Causes

1. **Connection Pool Too Small**
   - Maximum pool size insufficient for load
   - Not accounting for concurrent requests
   - Pool size not matching application needs
   - Traffic spikes exceeding pool capacity

2. **Connection Leaks**
   - Connections not returned to pool
   - Exception handling not closing connections
   - Long-running transactions
   - Connection not released properly

3. **Long-Running Operations**
   - Queries taking too long
   - Transactions not committing
   - Database operations blocking
   - Slow queries holding connections

4. **High Concurrency**
   - Too many concurrent requests
   - Application scaling issues
   - Traffic spikes
   - Load balancer distributing widely

### Common Scenarios

1. **Application Scaling**
   - Multiple application instances
   - Each instance with connection pool
   - Total connections exceeding database limit
   - Auto-scaling increasing instances

2. **Connection Management**
   - Connections not being reused
   - Pool not configured properly
   - Connection timeout too high
   - Idle connections not closing

3. **Database Performance**
   - Slow queries holding connections
   - Long-running transactions
   - Database locks
   - Resource contention

---

## 🛠️ Troubleshooting Steps

### Immediate Actions

1. **Check Connection Pool Status**
   ```bash
   # Check application connection pool metrics
   curl http://localhost:8080/actuator/metrics/hikari.connections.active
   curl http://localhost:8080/actuator/metrics/hikari.connections.idle
   curl http://localhost:8080/actuator/metrics/hikari.connections.pending
   
   # Check HikariCP pool status
   curl http://localhost:8080/actuator/metrics/hikari.connections
   ```

2. **Check Database Connections**
   ```sql
   -- Check current connections
   SHOW STATUS LIKE 'Threads_connected';
   
   -- Check connections by application
   SELECT host, user, COUNT(*) as connections
   FROM information_schema.PROCESSLIST
   GROUP BY host, user
   ORDER BY connections DESC;
   ```

3. **Check Application Logs**
   ```bash
   # Check for connection pool errors
   tail -f /var/log/application/application.log | grep -i "connection pool"
   
   # Check HikariCP logs
   tail -f /var/log/application/application.log | grep -i "hikari"
   ```

### Pool Analysis

1. **Review Connection Pool Configuration**
   ```yaml
   # Check Spring Boot datasource configuration
   spring:
     datasource:
       hikari:
         maximum-pool-size: 10
         minimum-idle: 5
         connection-timeout: 30000
         idle-timeout: 600000
         max-lifetime: 1800000
   ```

2. **Check Connection Usage**
   ```sql
   -- Find long-running connections
   SELECT id, user, host, db, command, time, state, info
   FROM information_schema.PROCESSLIST
   WHERE command != 'Sleep' AND time > 30
   ORDER BY time DESC;
   ```

---

## 🔧 Resolution Actions

### Short-term Fixes

1. **Increase Connection Pool Size**
   ```yaml
   # Temporarily increase pool size
   spring:
     datasource:
       hikari:
         maximum-pool-size: 20
         minimum-idle: 10
   ```

2. **Kill Long-Running Queries**
   ```sql
   -- Find and kill long-running queries
   SELECT id, time, info
   FROM information_schema.PROCESSLIST
   WHERE command != 'Sleep' AND time > 300;
   
   KILL <connection_id>;
   ```

3. **Restart Application**
   ```bash
   # Restart to clear connection pool
   systemctl restart user-service
   ```

### Long-term Solutions

1. **Fix Connection Leaks**
   - Ensure connections are closed
   - Use try-with-resources
   - Implement connection monitoring
   - Add connection leak detection

2. **Optimize Connection Pool**
   - Set appropriate pool sizes
   - Configure connection timeouts
   - Implement connection reuse
   - Monitor pool usage

3. **Optimize Database Queries**
   - Fix slow queries
   - Optimize transaction scope
   - Reduce lock contention
   - Improve query performance

---

## 📈 Prevention Strategies

### Best Practices

1. **Connection Pool Configuration**
   - Set appropriate pool sizes
   - Configure timeouts properly
   - Monitor pool usage
   - Implement pool monitoring

2. **Connection Management**
   - Close connections properly
   - Use connection pooling
   - Implement connection reuse
   - Monitor connection leaks

3. **Monitoring**
   - Monitor connection pool usage
   - Alert on pool exhaustion
   - Track connection metrics
   - Monitor database connections

---

## 📋 Incident Response Checklist

### Immediate Response (0-15 minutes)
- [ ] Acknowledge the incident
- [ ] Check connection pool status
- [ ] Check database connections
- [ ] Identify connection leaks
- [ ] Review pool configuration
- [ ] Begin troubleshooting

### Short-term Response (15-60 minutes)
- [ ] Increase pool size if needed
- [ ] Kill long-running queries
- [ ] Fix connection leaks
- [ ] Restart application if needed
- [ ] Update monitoring alerts
- [ ] Document findings

### Long-term Response (1-24 hours)
- [ ] Root cause analysis
- [ ] Optimize connection pool
- [ ] Fix connection leaks
- [ ] Optimize database queries
- [ ] Implement monitoring
- [ ] Implement preventive measures

---

## 🔍 Advanced Troubleshooting

### Spring Boot Connection Pool Diagnostics
```bash
# Check HikariCP metrics
curl http://localhost:8080/actuator/metrics/hikari.connections.active
curl http://localhost:8080/actuator/metrics/hikari.connections.idle
curl http://localhost:8080/actuator/metrics/hikari.connections.pending
curl http://localhost:8080/actuator/metrics/hikari.connections.timeout

# Check datasource health
curl http://localhost:8080/actuator/health/db
```

### MySQL Connection Diagnostics
```sql
-- Check connection statistics
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';

-- Check process list
SHOW FULL PROCESSLIST;
```

This comprehensive incident documentation provides detailed guidance for understanding, troubleshooting, and preventing MySQL connection pool exhaustion incidents in database tier.

