# Database 503 Service Unavailable — MySQL Too Many Connections

---

## 🧩 Overview

A "Too Many Connections" error occurs when the number of concurrent connections to MySQL exceeds the `max_connections` setting. This error prevents new connections from being established and can cause application failures.

### What is Too Many Connections?

A "Too Many Connections" error occurs when:
- Number of active connections reaches `max_connections` limit
- New connection attempts are rejected
- Error 1040 (Too many connections) is returned
- Applications cannot connect to database
- Service becomes unavailable

### MySQL Behavior

When the connection limit is reached in MySQL:
- New connection attempts are rejected
- Error 1040 is returned
- Existing connections continue to work
- Applications receive connection errors
- Service availability is impacted

### Database Tier Symptoms

**MySQL Symptoms:**
- "Too many connections" errors in logs
- Connection refused errors
- Application connection failures
- High connection count
- Service unavailability

---

## 📊 Log Samples

### Database Tier (MySQL) Logs

```
2024-01-15T10:00:05.288Z [ERROR] [trace_id:req-205-a5b6c7] [request_id:req-205] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Connection Error: Too many connections (max_connections = 100) - 0ms
2024-01-15T10:00:10.321Z [ERROR] [trace_id:req-210-b1c2d3] [request_id:req-210] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Connection Error: Too many connections (max_connections = 100) - 0ms
2024-01-15T10:00:15.354Z [ERROR] [trace_id:req-215-b2c3d4] [request_id:req-215] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Connection Error: Too many connections (max_connections = 100) - 0ms
2024-01-15T10:00:20.387Z [ERROR] [trace_id:req-220-b3c4d5] [request_id:req-220] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Connection Error: Too many connections (max_connections = 100) - 0ms
```

### MySQL Error Format

```
2024-01-15T10:00:05.288Z [ERROR] [RDS:database-sg] [DB:whizlabs-db] 
ERROR 1040 (08004): Too many connections
```

### MySQL Connection Status

```
mysql> SHOW STATUS LIKE 'Threads_connected';
+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| Threads_connected | 100   |
+-------------------+-------+

mysql> SHOW VARIABLES LIKE 'max_connections';
+-----------------+-------+
| Variable_name   | Value |
+-----------------+-------+
| max_connections | 100   |
+-----------------+-------+
```

---

## 🔍 Root Cause Analysis

### Primary Causes

1. **Connection Pool Exhaustion**
   - Application connection pools too large
   - Connections not being released
   - Connection leaks in application code
   - Too many application instances
   - Connection pool misconfiguration

2. **Insufficient max_connections**
   - `max_connections` setting too low
   - Not accounting for all applications
   - Not accounting for admin connections
   - RDS instance size limitations

3. **Connection Leaks**
   - Connections not closed properly
   - Exception handling not closing connections
   - Long-running transactions holding connections
   - Idle connections not timing out

4. **High Concurrency**
   - Traffic spikes
   - Too many concurrent requests
   - Application scaling issues
   - Load balancer distributing to many instances

### Common Scenarios

1. **Application Scaling**
   - Multiple application instances
   - Each instance creating connections
   - Total connections exceeding limit
   - Auto-scaling increasing instances

2. **Connection Pool Issues**
   - Connection pool size too large
   - Connections not being reused
   - Pool exhaustion
   - Connection timeout issues

3. **Long-Running Connections**
   - Idle connections not closing
   - Long-running queries
   - Transactions not committing
   - Sleep connections accumulating

---

## 🛠️ Troubleshooting Steps

### Immediate Actions

1. **Check Connection Count**
   ```sql
   -- Check current connections
   SHOW STATUS LIKE 'Threads_connected';
   
   -- Check max connections
   SHOW VARIABLES LIKE 'max_connections';
   
   -- Check connection details
   SHOW PROCESSLIST;
   
   -- Count connections by user
   SELECT user, COUNT(*) as connections
   FROM information_schema.PROCESSLIST
   GROUP BY user;
   ```

2. **Check MySQL Error Logs**
   ```bash
   # Check for connection errors
   tail -f /var/log/mysql/error.log | grep -i "too many connections"
   
   # Check RDS logs
   aws rds describe-db-log-files --db-instance-identifier whizlabs-db
   ```

3. **Identify Connection Sources**
   ```sql
   -- Check connections by host
   SELECT host, user, COUNT(*) as connections
   FROM information_schema.PROCESSLIST
   GROUP BY host, user
   ORDER BY connections DESC;
   ```

### Connection Analysis

1. **Find Idle Connections**
   ```sql
   -- Find idle connections
   SELECT id, user, host, db, command, time, state, info
   FROM information_schema.PROCESSLIST
   WHERE command = 'Sleep' AND time > 60
   ORDER BY time DESC;
   ```

2. **Find Long-Running Queries**
   ```sql
   -- Find long-running queries
   SELECT id, user, host, db, command, time, state, info
   FROM information_schema.PROCESSLIST
   WHERE command != 'Sleep' AND time > 30
   ORDER BY time DESC;
   ```

---

## 🔧 Resolution Actions

### Short-term Fixes

1. **Kill Idle Connections**
   ```sql
   -- Kill idle connections
   SELECT CONCAT('KILL ', id, ';') as kill_command
   FROM information_schema.PROCESSLIST
   WHERE command = 'Sleep' AND time > 300
   AND user != 'system user';
   
   -- Execute kill commands
   -- KILL <connection_id>;
   ```

2. **Increase max_connections**
   ```sql
   -- Temporarily increase (requires restart for permanent)
   SET GLOBAL max_connections = 200;
   
   -- For RDS, modify parameter group
   -- aws rds modify-db-parameter-group ...
   ```

3. **Kill Long-Running Queries**
   ```sql
   -- Kill long-running queries
   SELECT id, time, info
   FROM information_schema.PROCESSLIST
   WHERE command != 'Sleep' AND time > 300;
   
   -- Kill specific connection
   KILL <connection_id>;
   ```

### Long-term Solutions

1. **Fix Connection Leaks**
   - Ensure connections are closed
   - Use connection pooling properly
   - Implement connection timeout
   - Monitor connection usage

2. **Optimize Connection Pools**
   - Reduce connection pool sizes
   - Implement connection reuse
   - Configure appropriate timeouts
   - Monitor pool usage

3. **Database Configuration**
   - Set appropriate max_connections
   - Configure connection timeouts
   - Implement connection limits per user
   - Monitor connection usage

---

## 📈 Prevention Strategies

### Best Practices

1. **Connection Management**
   - Use connection pooling
   - Close connections properly
   - Implement connection timeouts
   - Monitor connection usage

2. **Application Design**
   - Optimize connection pool sizes
   - Reuse connections
   - Implement connection limits
   - Monitor connection leaks

3. **Database Configuration**
   - Set appropriate max_connections
   - Configure wait_timeout
   - Set interactive_timeout
   - Implement connection limits

---

## 📋 Incident Response Checklist

### Immediate Response (0-15 minutes)
- [ ] Acknowledge the incident
- [ ] Check connection count
- [ ] Identify connection sources
- [ ] Check for idle connections
- [ ] Review connection patterns
- [ ] Begin troubleshooting

### Short-term Response (15-60 minutes)
- [ ] Kill idle connections if needed
- [ ] Increase max_connections if appropriate
- [ ] Review connection pool configurations
- [ ] Check for connection leaks
- [ ] Update monitoring alerts
- [ ] Document findings

### Long-term Response (1-24 hours)
- [ ] Root cause analysis
- [ ] Fix connection leaks
- [ ] Optimize connection pools
- [ ] Update database configuration
- [ ] Implement monitoring
- [ ] Implement preventive measures

---

## 🔍 Advanced Troubleshooting

### MySQL Connection Diagnostics
```sql
-- Check connection statistics
SHOW STATUS LIKE 'Connections';
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';
SHOW STATUS LIKE 'Threads_running';

-- Check connection variables
SHOW VARIABLES LIKE 'max_connections';
SHOW VARIABLES LIKE 'wait_timeout';
SHOW VARIABLES LIKE 'interactive_timeout';

-- Check process list
SHOW FULL PROCESSLIST;
```

### RDS-Specific Diagnostics
```bash
# Check RDS instance connections
aws rds describe-db-instances --db-instance-identifier whizlabs-db \
  --query 'DBInstances[0].DBInstanceStatus'

# Check RDS parameter group
aws rds describe-db-parameters \
  --db-parameter-group-name <parameter-group-name> \
  --query 'Parameters[?ParameterName==`max_connections`]'
```

This comprehensive incident documentation provides detailed guidance for understanding, troubleshooting, and preventing MySQL "Too Many Connections" incidents in database tier.

