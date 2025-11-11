# Application 500 Internal Server Error — SQLException

---

## 🧩 Overview

An SQLException occurs when a Java application encounters problems accessing a database. This exception indicates database connectivity issues, query execution problems, or database constraint violations in Java/Spring Boot applications using JDBC or JPA.

### What is an SQLException?

An SQLException is a Java database exception that occurs when:
- Database connection failures
- SQL query execution errors
- Database constraint violations
- Transaction failures
- Connection pool exhaustion
- Database timeout errors

### Java/Spring Boot Behavior

When an SQLException occurs in a Spring Boot microservice:
- JDBC or JPA throws SQLException
- Spring's exception handling may catch it
- Transaction may be rolled back
- Service may return 500 Internal Server Error
- Database connection may be closed

### Application Tier Symptoms

**Java/Spring Boot Symptoms:**
- SQLException in application logs
- Database connection errors
- Query execution failures
- Transaction rollback errors
- Connection pool exhaustion
- 500 Internal Server Error responses

---

## 📊 Log Samples

### Application Tier (Java/Spring Boot) Logs

```
2024-01-15T15:00:05.288Z [ERROR] [trace_id:req-205-a5b6c7] [request_id:req-205] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:user-service] SQLException: Database connection pool exhausted - 8901ms
2024-01-15T15:00:10.321Z [ERROR] [trace_id:req-210-b1c2d3] [request_id:req-210] [ELB:backend-sg] [AZ:us-east-1b] [EC2:i-0987654321fedcba1] [Service:order-service] SQLException: Connection timeout - 15000ms
2024-01-15T15:00:15.354Z [ERROR] [trace_id:req-215-b2c3d4] [request_id:req-215] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:product-service] SQLException: Query execution failed - 2345ms
2024-01-15T15:00:20.387Z [ERROR] [trace_id:req-220-b3c4d5] [request_id:req-220] [ELB:backend-sg] [AZ:us-east-1b] [EC2:i-0987654321fedcba1] [Service:cart-service] SQLException: Transaction rollback - 5678ms
2024-01-15T15:00:25.420Z [ERROR] [trace_id:req-225-b4c5d6] [request_id:req-225] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:user-service] SQLException: Constraint violation - 1234ms
```

### Java SQLException Format

```
java.sql.SQLException: Connection pool exhausted
    at com.zaxxer.hikari.pool.HikariPool.getConnection(HikariPool.java:195)
    at com.zaxxer.hikari.pool.HikariPool.getConnection(HikariPool.java:147)
    at com.zaxxer.hikari.HikariDataSource.getConnection(HikariDataSource.java:112)
    at org.springframework.jdbc.datasource.DataSourceUtils.fetchConnection(DataSourceUtils.java:158)
    at org.springframework.jdbc.datasource.DataSourceUtils.doGetConnection(DataSourceUtils.java:116)
    at org.springframework.jdbc.datasource.DataSourceUtils.getConnection(DataSourceUtils.java:79)
```

---

## 🔍 Root Cause Analysis

### Primary Causes

1. **Connection Pool Exhaustion**
   - All database connections in use
   - Connections not being released
   - Connection pool size too small
   - Connection leaks
   - Long-running transactions

2. **Database Connectivity Issues**
   - Database server unavailable
   - Network connectivity problems
   - Firewall blocking connections
   - Database connection timeout
   - DNS resolution failures

3. **Query Execution Problems**
   - SQL syntax errors
   - Invalid table or column names
   - Query timeout
   - Database locks
   - Constraint violations

4. **Transaction Issues**
   - Transaction timeout
   - Deadlock detection
   - Transaction rollback
   - Isolation level conflicts
   - Long-running transactions

### Common Scenarios

1. **Connection Management**
   - Connections not closed properly
   - Connection pool misconfiguration
   - Too many concurrent requests
   - Connection leaks in code

2. **Database Performance**
   - Slow queries blocking connections
   - Database locks
   - High database load
   - Missing indexes

3. **Configuration Issues**
   - Incorrect database URL
   - Wrong credentials
   - Connection pool size too small
   - Timeout values too low

---

## 🛠️ Troubleshooting Steps

### Immediate Actions

1. **Check Database Connectivity**
   ```bash
   # Test database connection
   mysql -h database-host -u username -p -e "SELECT 1"
   
   # Check network connectivity
   ping database-host
   telnet database-host 3306
   
   # Check DNS resolution
   nslookup database-host
   ```

2. **Check Application Logs**
   ```bash
   # Check for SQLException
   tail -f /var/log/application/application.log | grep -i "SQLException"
   
   # Check connection pool metrics
   curl http://localhost:8080/actuator/metrics/hikari.connections.active
   
   # Check service logs
   journalctl -u user-service -f | grep -i "SQLException"
   ```

3. **Check Connection Pool Status**
   ```bash
   # Check HikariCP connection pool
   curl http://localhost:8080/actuator/metrics/hikari.connections
   
   # Check connection pool configuration
   # Review application.properties or application.yml
   ```

### Database Analysis

1. **Check Database Status**
   ```sql
   -- Check database connections
   SHOW PROCESSLIST;
   
   -- Check connection count
   SHOW STATUS LIKE 'Threads_connected';
   
   -- Check max connections
   SHOW VARIABLES LIKE 'max_connections';
   ```

2. **Review Connection Pool Configuration**
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

---

## 🔧 Resolution Actions

### Short-term Fixes

1. **Restart Service**
   ```bash
   # Restart service to clear connection pool
   systemctl restart user-service
   
   # Verify service is running
   systemctl status user-service
   ```

2. **Increase Connection Pool Size**
   ```yaml
   # Temporarily increase pool size
   spring:
     datasource:
       hikari:
         maximum-pool-size: 20
   ```

3. **Kill Long-Running Queries**
   ```sql
   -- Find long-running queries
   SHOW PROCESSLIST;
   
   -- Kill specific query
   KILL <process_id>;
   ```

### Long-term Solutions

1. **Fix Connection Leaks**
   - Ensure connections are properly closed
   - Use try-with-resources
   - Implement connection monitoring
   - Add connection leak detection

2. **Optimize Database Queries**
   - Add missing indexes
   - Optimize slow queries
   - Implement query timeouts
   - Use connection pooling best practices

3. **Database Configuration**
   - Increase database max_connections if needed
   - Optimize connection pool settings
   - Configure appropriate timeouts
   - Monitor database performance

---

## 📈 Prevention Strategies

### Best Practices

1. **Connection Management**
   - Use connection pooling
   - Close connections properly
   - Monitor connection usage
   - Implement connection leak detection

2. **Query Optimization**
   - Optimize SQL queries
   - Add appropriate indexes
   - Use pagination for large results
   - Implement query timeouts

3. **Monitoring**
   - Monitor connection pool usage
   - Track SQLException rates
   - Monitor database performance
   - Alert on connection pool exhaustion

---

## 📋 Incident Response Checklist

### Immediate Response (0-15 minutes)
- [ ] Acknowledge the incident
- [ ] Check application logs for SQLException
- [ ] Verify database connectivity
- [ ] Check connection pool status
- [ ] Identify affected service
- [ ] Begin troubleshooting

### Short-term Response (15-60 minutes)
- [ ] Restart service if needed
- [ ] Check database status
- [ ] Review connection pool configuration
- [ ] Kill long-running queries if needed
- [ ] Update monitoring alerts
- [ ] Document findings

### Long-term Response (1-24 hours)
- [ ] Root cause analysis
- [ ] Fix connection leaks
- [ ] Optimize database queries
- [ ] Update connection pool configuration
- [ ] Implement preventive measures

---

## 🔍 Advanced Troubleshooting

### Spring Boot Database Diagnostics
```bash
# Check datasource health
curl http://localhost:8080/actuator/health/db

# Check HikariCP metrics
curl http://localhost:8080/actuator/metrics/hikari.connections.active
curl http://localhost:8080/actuator/metrics/hikari.connections.idle
curl http://localhost:8080/actuator/metrics/hikari.connections.pending

# Check database connection pool
# Review HikariCP JMX metrics if enabled
```

### Database Diagnostics
```sql
-- Check active connections
SHOW PROCESSLIST;

-- Check connection statistics
SHOW STATUS LIKE 'Connections';
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';

-- Check for locks
SHOW ENGINE INNODB STATUS;
```

This comprehensive incident documentation provides detailed guidance for understanding, troubleshooting, and preventing SQLException incidents in Java/Spring Boot microservices.

