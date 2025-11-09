# Database 500 Internal Server Error — MySQL InnoDB Deadlock

---

## 🧩 Overview

A deadlock occurs when two or more MySQL InnoDB transactions are waiting for each other to release locks, creating a circular dependency that prevents any of the transactions from proceeding. This is a critical error in MySQL/InnoDB databases that causes transaction rollbacks and application failures.

### What is a MySQL Deadlock?

A deadlock is a situation where:
- Two or more transactions are waiting for locks held by each other
- Neither transaction can proceed
- MySQL InnoDB automatically detects and resolves deadlocks
- One transaction is rolled back (chosen as the deadlock victim)
- The other transaction can proceed

### MySQL InnoDB Behavior

When a deadlock occurs in MySQL InnoDB:
- InnoDB deadlock detection mechanism identifies the deadlock
- One transaction is chosen as the victim and rolled back
- Error 1213 (Deadlock found when trying to get lock) is returned
- Application receives deadlock error
- Transaction must be retried

### Database Tier Symptoms

**MySQL/InnoDB Symptoms:**
- Deadlock errors in database logs
- Transaction rollback errors
- Application errors due to deadlocks
- Increased transaction retry rates
- Performance degradation

---

## 📊 Log Samples

### Database Tier (MySQL/InnoDB) Logs

```
2024-01-15T10:00:01.321Z [ERROR] [trace_id:req-006-fpy952] [request_id:req-006] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Deadlock: Deadlock detected in transaction - 4424ms
2024-01-15T10:00:01.420Z [ERROR] [trace_id:req-009-ak47c0] [request_id:req-009] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Deadlock: Deadlock detected in transaction - 1539ms
2024-01-15T10:00:01.519Z [ERROR] [trace_id:req-012-7fmeok] [request_id:req-012] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Deadlock: Deadlock detected in transaction - 3980ms
2024-01-15T10:00:02.542Z [ERROR] [trace_id:req-043-k49i3z] [request_id:req-043] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Deadlock: Deadlock detected in transaction - 1276ms
2024-01-15T10:00:03.169Z [ERROR] [trace_id:req-062-kdgnjq] [request_id:req-062] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Deadlock: Deadlock detected in transaction - 3820ms
2024-01-15T10:00:03.334Z [ERROR] [trace_id:req-067-4bkt42] [request_id:req-067] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Deadlock: Deadlock detected in transaction - 1224ms
```

### MySQL Error Format

```
2024-01-15T10:00:01.321Z [ERROR] [RDS:database-sg] [DB:whizlabs-db] 
ERROR 1213 (40001): Deadlock found when trying to get lock; try restarting transaction
```

### MySQL InnoDB Status

```
LATEST DETECTED DEADLOCK
------------------------
2024-01-15 10:00:01 0x7f8b8c00b700
*** (1) TRANSACTION:
TRANSACTION 12345, ACTIVE 4 sec starting index read
mysql tables in use 1, locked 1
LOCK WAIT 2 lock struct(s), heap size 1136, 1 row lock(s)
MySQL thread id 100, OS thread handle 140234567890176, query id 5000 updating
UPDATE users SET status = 'active' WHERE id = 1

*** (2) TRANSACTION:
TRANSACTION 12346, ACTIVE 3 sec starting index read
mysql tables in use 1, locked 1
2 lock struct(s), heap size 1136, 1 row lock(s)
MySQL thread id 101, OS thread handle 140234567890177, query id 5001 updating
UPDATE orders SET status = 'processed' WHERE user_id = 1

*** (2) HOLDS THE LOCK(S):
RECORD LOCKS space id 10 page no 5 n bits 72 index PRIMARY of table `whizlabs_db`.`users` trx id 12346 lock_mode X locks rec but not gap
*** (2) WAITING FOR THIS LOCK TO BE RELEASED:
RECORD LOCKS space id 10 page no 5 n bits 72 index PRIMARY of table `whizlabs_db`.`users` trx id 12346 lock_mode X locks rec but not gap
*** WE ROLL BACK TRANSACTION (2)
```

---

## 🔍 Root Cause Analysis

### Primary Causes

1. **Concurrent Transaction Conflicts**
   - Multiple transactions accessing same rows in different order
   - Transactions updating overlapping data sets
   - Concurrent inserts into same tables
   - Multiple transactions locking same resources

2. **Transaction Ordering Issues**
   - Transactions acquiring locks in different order
   - No consistent lock ordering strategy
   - Complex transaction logic
   - Nested transactions

3. **Lock Contention**
   - High concurrency on same tables
   - Long-running transactions holding locks
   - Missing indexes causing table locks
   - Large transactions locking many rows

4. **Application Logic Issues**
   - Transactions too long
   - Holding locks during external calls
   - Not releasing locks promptly
   - Complex business logic in transactions

### Common Scenarios

1. **Update Patterns**
   - Multiple transactions updating same rows
   - Updates in different order
   - Concurrent updates to related tables

2. **Insert Patterns**
   - Concurrent inserts with unique constraints
   - Gap locks on indexes
   - Auto-increment contention

3. **Delete Patterns**
   - Concurrent deletes on same rows
   - Cascading deletes
   - Foreign key constraint checks

---

## 🛠️ Troubleshooting Steps

### Immediate Actions

1. **Check MySQL Error Logs**
   ```bash
   # Check MySQL error log for deadlocks
   tail -f /var/log/mysql/error.log | grep -i "deadlock"
   
   # Check RDS logs
   aws rds describe-db-log-files --db-instance-identifier whizlabs-db
   
   # Download and check RDS log file
   aws rds download-db-log-file-portion --db-instance-identifier whizlabs-db --log-file-name error/mysql-error.log
   ```

2. **Check InnoDB Status**
   ```sql
   -- Check latest deadlock information
   SHOW ENGINE INNODB STATUS\G
   
   -- Look for "LATEST DETECTED DEADLOCK" section
   ```

3. **Check Active Transactions**
   ```sql
   -- Check active transactions
   SELECT * FROM information_schema.INNODB_TRX;
   
   -- Check lock waits
   SELECT * FROM performance_schema.data_lock_waits;
   
   -- Check locks
   SELECT * FROM performance_schema.data_locks;
   ```

### Deadlock Analysis

1. **Analyze Deadlock Information**
   ```sql
   -- Get detailed deadlock information
   SHOW ENGINE INNODB STATUS\G
   
   -- Review deadlock graph
   -- Identify which transactions are involved
   -- Determine lock order
   ```

2. **Identify Problematic Queries**
   ```sql
   -- Check slow query log
   SELECT * FROM mysql.slow_log WHERE sql_text LIKE '%UPDATE%' OR sql_text LIKE '%DELETE%';
   
   -- Check process list for long-running transactions
   SHOW PROCESSLIST;
   ```

---

## 🔧 Resolution Actions

### Short-term Fixes

1. **Retry Transactions**
   ```java
   // Implement deadlock retry logic
   int maxRetries = 3;
   for (int i = 0; i < maxRetries; i++) {
       try {
           // Execute transaction
           return executeTransaction();
       } catch (DeadlockLoserDataAccessException e) {
           if (i == maxRetries - 1) throw e;
           Thread.sleep(100 * (i + 1)); // Exponential backoff
       }
   }
   ```

2. **Kill Blocking Transactions**
   ```sql
   -- Find blocking transactions
   SELECT * FROM information_schema.INNODB_TRX 
   WHERE trx_state = 'LOCK WAIT';
   
   -- Kill specific transaction if needed
   KILL <thread_id>;
   ```

3. **Reduce Transaction Scope**
   - Break large transactions into smaller ones
   - Release locks as soon as possible
   - Avoid long-running operations in transactions

### Long-term Solutions

1. **Fix Lock Ordering**
   - Always acquire locks in same order
   - Use consistent transaction patterns
   - Implement lock ordering strategy
   - Document lock acquisition order

2. **Optimize Queries**
   - Add missing indexes
   - Optimize query execution plans
   - Reduce lock contention
   - Use appropriate isolation levels

3. **Transaction Design**
   - Keep transactions short
   - Avoid external calls in transactions
   - Use optimistic locking where possible
   - Implement proper retry logic

---

## 📈 Prevention Strategies

### Best Practices

1. **Transaction Design**
   - Keep transactions short
   - Acquire locks in consistent order
   - Release locks promptly
   - Avoid long-running operations

2. **Query Optimization**
   - Add appropriate indexes
   - Optimize query execution
   - Use covering indexes
   - Reduce lock scope

3. **Application Logic**
   - Implement deadlock retry logic
   - Use appropriate isolation levels
   - Monitor deadlock rates
   - Alert on deadlock spikes

---

## 📋 Incident Response Checklist

### Immediate Response (0-15 minutes)
- [ ] Acknowledge the incident
- [ ] Check MySQL error logs for deadlocks
- [ ] Review InnoDB status
- [ ] Identify affected transactions
- [ ] Check active transactions
- [ ] Begin troubleshooting

### Short-term Response (15-60 minutes)
- [ ] Implement transaction retries if possible
- [ ] Kill blocking transactions if needed
- [ ] Review deadlock patterns
- [ ] Update monitoring alerts
- [ ] Document findings
- [ ] Communicate status updates

### Long-term Response (1-24 hours)
- [ ] Root cause analysis from InnoDB status
- [ ] Fix lock ordering issues
- [ ] Optimize problematic queries
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

-- Check deadlock history
SELECT * FROM performance_schema.events_statements_history_long 
WHERE sql_text LIKE '%deadlock%';
```

### RDS-Specific Diagnostics
```bash
# Check RDS instance status
aws rds describe-db-instances --db-instance-identifier whizlabs-db

# Download error logs
aws rds download-db-log-file-portion \
  --db-instance-identifier whizlabs-db \
  --log-file-name error/mysql-error.log \
  --output text > mysql-error.log
```

This comprehensive incident documentation provides detailed guidance for understanding, troubleshooting, and preventing MySQL InnoDB deadlock incidents in database tier.

