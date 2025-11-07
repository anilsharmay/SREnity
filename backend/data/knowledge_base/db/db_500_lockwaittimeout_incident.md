# Database 500 Internal Server Error — MySQL InnoDB Lock Wait Timeout

---

## 🧩 Overview

A lock wait timeout occurs when a MySQL InnoDB transaction waits too long to acquire a lock that is held by another transaction. This error indicates that a transaction cannot proceed because it is waiting for a lock that exceeds the configured timeout period.

### What is a Lock Wait Timeout?

A lock wait timeout occurs when:
- Transaction A holds a lock on a row
- Transaction B tries to acquire the same lock
- Transaction B waits for the lock to be released
- The wait exceeds the `innodb_lock_wait_timeout` setting (default 50 seconds)
- MySQL returns error 1205 (Lock wait timeout exceeded)

### MySQL InnoDB Behavior

When a lock wait timeout occurs in MySQL InnoDB:
- The waiting transaction times out
- Error 1205 is returned to the application
- The transaction is rolled back
- Application must handle the timeout error
- Lock-holding transaction continues

### Database Tier Symptoms

**MySQL/InnoDB Symptoms:**
- Lock wait timeout errors in database logs
- Transaction timeout errors
- Long-running transactions blocking others
- Application errors due to timeouts
- Performance degradation

---

## 📊 Log Samples

### Database Tier (MySQL/InnoDB) Logs

```
2024-01-15T10:00:01.585Z [ERROR] [trace_id:req-014-eigtrw] [request_id:req-014] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Lock Wait Timeout: Lock wait timeout exceeded - 19619ms
2024-01-15T10:00:02.278Z [ERROR] [trace_id:req-035-wn9gq8] [request_id:req-035] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Lock Wait Timeout: Lock wait timeout exceeded - 21624ms
2024-01-15T10:00:02.344Z [ERROR] [trace_id:req-037-r11was] [request_id:req-037] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Lock Wait Timeout: Lock wait timeout exceeded - 28378ms
2024-01-15T10:00:02.509Z [ERROR] [trace_id:req-045-z8svlw] [request_id:req-045] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Lock Wait Timeout: Lock wait timeout exceeded - 17213ms
2024-01-15T10:00:03.631Z [ERROR] [trace_id:req-057-ojcguk] [request_id:req-057] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Lock Wait Timeout: Lock wait timeout exceeded - 23144ms
2024-01-15T10:00:03.994Z [ERROR] [trace_id:req-087-79iv9x] [request_id:req-087] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Lock Wait Timeout: Lock wait timeout exceeded - 20858ms
```

### MySQL Error Format

```
2024-01-15T10:00:01.585Z [ERROR] [RDS:database-sg] [DB:whizlabs-db] 
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
```

### MySQL Process List

```
+----+------+-----------------+--------+---------+------+------------+------------------+
| Id | User | Host            | db     | Command | Time | State      | Info             |
+----+------+-----------------+--------+---------+------+------------+------------------+
| 100| app  | 192.168.1.100   | whizlabs-db | Query | 45  | updating   | UPDATE users SET status = 'active' WHERE id = 1 |
| 101| app  | 192.168.1.101   | whizlabs-db | Query | 30  | Waiting for table metadata lock | SELECT * FROM users WHERE id = 1 |
+----+------+-----------------+--------+---------+------+------------+------------------+
```

---

## 🔍 Root Cause Analysis

### Primary Causes

1. **Long-Running Transactions**
   - Transactions holding locks for extended periods
   - Transactions not committing or rolling back
   - Long-running queries within transactions
   - External operations within transactions

2. **Lock Contention**
   - High concurrency on same rows
   - Multiple transactions waiting for same locks
   - Missing indexes causing table locks
   - Large transactions locking many rows

3. **Transaction Design Issues**
   - Transactions too long
   - Holding locks during external calls
   - Not releasing locks promptly
   - Complex business logic in transactions

4. **Configuration Issues**
   - `innodb_lock_wait_timeout` too low
   - Transaction isolation level too high
   - Lock escalation issues
   - Inappropriate lock modes

### Common Scenarios

1. **Update Conflicts**
   - Multiple transactions updating same rows
   - Long-running updates
   - Updates blocking selects

2. **Select for Update**
   - SELECT ... FOR UPDATE holding locks
   - Long-running SELECT FOR UPDATE
   - Not releasing locks promptly

3. **Table Locks**
   - Missing indexes causing table locks
   - ALTER TABLE operations
   - Large DDL operations

---

## 🛠️ Troubleshooting Steps

### Immediate Actions

1. **Check MySQL Error Logs**
   ```bash
   # Check MySQL error log for lock wait timeouts
   tail -f /var/log/mysql/error.log | grep -i "lock wait timeout"
   
   # Check RDS logs
   aws rds describe-db-log-files --db-instance-identifier whizlabs-db
   ```

2. **Check Blocking Transactions**
   ```sql
   -- Check for blocking transactions
   SELECT * FROM information_schema.INNODB_TRX 
   WHERE trx_state = 'LOCK WAIT';
   
   -- Check process list for long-running queries
   SHOW PROCESSLIST;
   
   -- Check lock waits
   SELECT * FROM performance_schema.data_lock_waits;
   ```

3. **Check Lock Information**
   ```sql
   -- Check current locks
   SELECT * FROM performance_schema.data_locks;
   
   -- Check lock waits
   SELECT * FROM performance_schema.data_lock_waits;
   
   -- Check InnoDB status
   SHOW ENGINE INNODB STATUS\G
   ```

### Lock Analysis

1. **Identify Blocking Transactions**
   ```sql
   -- Find transactions holding locks
   SELECT * FROM information_schema.INNODB_TRX 
   WHERE trx_state = 'RUNNING' 
   ORDER BY trx_started;
   
   -- Find waiting transactions
   SELECT * FROM information_schema.INNODB_TRX 
   WHERE trx_state = 'LOCK WAIT';
   ```

2. **Review Query Execution**
   ```sql
   -- Check slow query log
   SELECT * FROM mysql.slow_log 
   WHERE start_time > DATE_SUB(NOW(), INTERVAL 1 HOUR)
   ORDER BY query_time DESC;
   ```

---

## 🔧 Resolution Actions

### Short-term Fixes

1. **Kill Blocking Transactions**
   ```sql
   -- Find blocking transaction
   SELECT trx_mysql_thread_id, trx_query 
   FROM information_schema.INNODB_TRX 
   WHERE trx_state = 'RUNNING' 
   AND trx_started < DATE_SUB(NOW(), INTERVAL 1 MINUTE);
   
   -- Kill blocking transaction
   KILL <thread_id>;
   ```

2. **Increase Lock Wait Timeout**
   ```sql
   -- Temporarily increase timeout
   SET GLOBAL innodb_lock_wait_timeout = 120;
   
   -- Or set per session
   SET SESSION innodb_lock_wait_timeout = 120;
   ```

3. **Retry Transactions**
   ```java
   // Implement retry logic for lock wait timeouts
   int maxRetries = 3;
   for (int i = 0; i < maxRetries; i++) {
       try {
           return executeTransaction();
       } catch (QueryTimeoutException e) {
           if (i == maxRetries - 1) throw e;
           Thread.sleep(1000 * (i + 1));
       }
   }
   ```

### Long-term Solutions

1. **Optimize Transactions**
   - Keep transactions short
   - Release locks promptly
   - Avoid long-running operations
   - Use appropriate isolation levels

2. **Fix Query Performance**
   - Add missing indexes
   - Optimize query execution plans
   - Reduce lock contention
   - Use covering indexes

3. **Transaction Design**
   - Break large transactions into smaller ones
   - Avoid external calls in transactions
   - Use optimistic locking where possible
   - Implement proper retry logic

---

## 📈 Prevention Strategies

### Best Practices

1. **Transaction Design**
   - Keep transactions short
   - Release locks promptly
   - Avoid external operations in transactions
   - Use appropriate isolation levels

2. **Query Optimization**
   - Add appropriate indexes
   - Optimize query execution
   - Use covering indexes
   - Reduce lock scope

3. **Monitoring**
   - Monitor lock wait times
   - Track long-running transactions
   - Alert on lock wait timeouts
   - Monitor lock contention

---

## 📋 Incident Response Checklist

### Immediate Response (0-15 minutes)
- [ ] Acknowledge the incident
- [ ] Check MySQL error logs for lock wait timeouts
- [ ] Identify blocking transactions
- [ ] Check active transactions
- [ ] Review lock information
- [ ] Begin troubleshooting

### Short-term Response (15-60 minutes)
- [ ] Kill blocking transactions if needed
- [ ] Increase lock wait timeout if appropriate
- [ ] Implement transaction retries
- [ ] Review transaction patterns
- [ ] Update monitoring alerts
- [ ] Document findings

### Long-term Response (1-24 hours)
- [ ] Root cause analysis
- [ ] Optimize problematic transactions
- [ ] Fix query performance
- [ ] Improve transaction design
- [ ] Implement preventive measures

---

## 🔍 Advanced Troubleshooting

### MySQL InnoDB Diagnostics
```sql
-- Check InnoDB status
SHOW ENGINE INNODB STATUS\G

-- Check transaction information
SELECT * FROM information_schema.INNODB_TRX;

-- Check lock information
SELECT * FROM performance_schema.data_locks;
SELECT * FROM performance_schema.data_lock_waits;

-- Check lock wait timeout setting
SHOW VARIABLES LIKE 'innodb_lock_wait_timeout';
```

### RDS-Specific Diagnostics
```bash
# Check RDS instance status
aws rds describe-db-instances --db-instance-identifier whizlabs-db

# Check RDS performance insights
aws rds describe-db-instances --db-instance-identifier whizlabs-db --query 'DBInstances[0].PerformanceInsightsEnabled'
```

This comprehensive incident documentation provides detailed guidance for understanding, troubleshooting, and preventing MySQL InnoDB lock wait timeout incidents in database tier.

