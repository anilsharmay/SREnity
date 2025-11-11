# Database 500 Internal Server Error — MySQL Slow Query

---

## 🧩 Overview

A slow query occurs when a MySQL query takes longer than the configured threshold to execute. Slow queries can cause database performance degradation, lock contention, and application timeouts. This is a critical performance issue in MySQL databases that requires optimization.

### What is a Slow Query?

A slow query is a MySQL query that:
- Takes longer than `long_query_time` to execute (default 10 seconds)
- Exceeds performance expectations
- Causes database performance degradation
- May hold locks for extended periods
- Can block other transactions

### MySQL Behavior

When a slow query occurs in MySQL:
- Query execution exceeds threshold
- Query is logged to slow query log
- Performance may degrade
- Locks may be held longer
- Other queries may be blocked

### Database Tier Symptoms

**MySQL Symptoms:**
- Slow query log entries
- High query execution times
- Database performance degradation
- Increased lock wait times
- Application timeouts

---

## 📊 Log Samples

### Database Tier (MySQL) Logs

```
2024-01-15T10:00:01.189Z [ERROR] [trace_id:req-002-ueyqkw] [request_id:req-002] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Slow Query: SELECT query taking too long - 6646ms
2024-01-15T10:00:02.806Z [ERROR] [trace_id:req-051-9v7kdi] [request_id:req-051] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Slow Query: SELECT query taking too long - 11085ms
2024-01-15T10:00:02.839Z [ERROR] [trace_id:req-052-wmwc31] [request_id:req-052] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Slow Query: SELECT query taking too long - 5379ms
2024-01-15T10:00:02.872Z [ERROR] [trace_id:req-053-6iefll] [request_id:req-053] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Slow Query: SELECT query taking too long - 13172ms
2024-01-15T10:00:03.763Z [ERROR] [trace_id:req-080-3uzs1x] [request_id:req-080] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Slow Query: SELECT query taking too long - 10597ms
2024-01-15T10:00:03.895Z [ERROR] [trace_id:req-064-4byxhi] [request_id:req-064] [RDS:database-sg] [AZ:us-east-1a] [DB:whizlabs-db] Slow Query: SELECT query taking too long - 13169ms
```

### MySQL Slow Query Log Format

```
# Time: 2024-01-15T10:00:01.189000Z
# User@Host: app[app] @ [192.168.1.100] Id: 100
# Query_time: 6.646000  Lock_time: 0.001000 Rows_sent: 0  Rows_examined: 1000000
SET timestamp=1705316401;
SELECT * FROM users u 
JOIN orders o ON u.id = o.user_id 
WHERE u.status = 'active' 
AND o.created_at > '2024-01-01' 
ORDER BY o.created_at DESC;
```

---

## 🔍 Root Cause Analysis

### Primary Causes

1. **Missing Indexes**
   - Queries scanning full tables
   - Missing indexes on WHERE clauses
   - Missing indexes on JOIN columns
   - Missing indexes on ORDER BY columns
   - Composite indexes not optimal

2. **Inefficient Query Design**
   - Cartesian products in JOINs
   - Suboptimal JOIN order
   - Using SELECT * unnecessarily
   - Not using LIMIT for large result sets
   - Complex subqueries

3. **Data Volume Issues**
   - Large tables without partitioning
   - Tables growing unbounded
   - Historical data not archived
   - Full table scans on large tables

4. **Resource Constraints**
   - Insufficient memory for sorting
   - Disk I/O bottlenecks
   - CPU saturation
   - Network latency for RDS

### Common Scenarios

1. **Full Table Scans**
   - Missing indexes on WHERE clauses
   - Queries not using indexes
   - Index not being chosen by optimizer
   - Statistics out of date

2. **Join Performance**
   - Missing indexes on JOIN columns
   - Large result sets from JOINs
   - Suboptimal JOIN order
   - Cartesian products

3. **Sorting Operations**
   - ORDER BY without indexes
   - Large result sets being sorted
   - Filesort operations
   - Insufficient sort buffer

---

## 🛠️ Troubleshooting Steps

### Immediate Actions

1. **Check Slow Query Log**
   ```bash
   # Check slow query log
   tail -f /var/log/mysql/slow-query.log
   
   # Check RDS slow query log
   aws rds describe-db-log-files --db-instance-identifier whizlabs-db | grep slow
   
   # Download slow query log
   aws rds download-db-log-file-portion \
     --db-instance-identifier whizlabs-db \
     --log-file-name slowquery/mysql-slowquery.log
   ```

2. **Analyze Slow Queries**
   ```sql
   -- Check slow query log table
   SELECT * FROM mysql.slow_log 
   WHERE start_time > DATE_SUB(NOW(), INTERVAL 1 HOUR)
   ORDER BY query_time DESC
   LIMIT 10;
   
   -- Use pt-query-digest if available
   pt-query-digest /var/log/mysql/slow-query.log
   ```

3. **Check Query Execution Plans**
   ```sql
   -- Explain slow query
   EXPLAIN SELECT * FROM users u 
   JOIN orders o ON u.id = o.user_id 
   WHERE u.status = 'active';
   
   -- Check for full table scans
   EXPLAIN FORMAT=JSON SELECT * FROM users WHERE status = 'active';
   ```

### Query Analysis

1. **Identify Problematic Queries**
   ```sql
   -- Find slow queries
   SELECT sql_text, query_time, lock_time, rows_examined, rows_sent
   FROM mysql.slow_log
   WHERE start_time > DATE_SUB(NOW(), INTERVAL 1 HOUR)
   ORDER BY query_time DESC
   LIMIT 10;
   ```

2. **Check Index Usage**
   ```sql
   -- Check indexes on table
   SHOW INDEXES FROM users;
   
   -- Check index usage statistics
   SELECT * FROM sys.schema_unused_indexes;
   
   -- Check missing indexes
   SELECT * FROM sys.schema_redundant_indexes;
   ```

---

## 🔧 Resolution Actions

### Short-term Fixes

1. **Kill Long-Running Queries**
   ```sql
   -- Find long-running queries
   SELECT id, user, host, db, command, time, state, info
   FROM information_schema.PROCESSLIST
   WHERE command != 'Sleep' AND time > 30
   ORDER BY time DESC;
   
   -- Kill specific query
   KILL <query_id>;
   ```

2. **Add Missing Indexes**
   ```sql
   -- Add index on WHERE clause column
   CREATE INDEX idx_users_status ON users(status);
   
   -- Add composite index
   CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);
   ```

3. **Optimize Query**
   ```sql
   -- Use EXPLAIN to optimize
   EXPLAIN SELECT * FROM users WHERE status = 'active';
   
   -- Add LIMIT if appropriate
   SELECT * FROM users WHERE status = 'active' LIMIT 100;
   ```

### Long-term Solutions

1. **Query Optimization**
   - Add missing indexes
   - Optimize JOIN order
   - Use appropriate indexes
   - Optimize subqueries

2. **Database Design**
   - Implement table partitioning
   - Archive historical data
   - Normalize/denormalize as needed
   - Optimize data types

3. **Monitoring and Alerting**
   - Monitor slow query rates
   - Alert on query performance
   - Track query execution times
   - Implement query performance testing

---

## 📈 Prevention Strategies

### Best Practices

1. **Index Management**
   - Add indexes on frequently queried columns
   - Monitor index usage
   - Remove unused indexes
   - Maintain index statistics

2. **Query Design**
   - Use EXPLAIN to analyze queries
   - Optimize JOIN operations
   - Use appropriate WHERE clauses
   - Limit result sets

3. **Monitoring**
   - Monitor slow query log
   - Track query performance
   - Alert on slow queries
   - Regular query review

---

## 📋 Incident Response Checklist

### Immediate Response (0-15 minutes)
- [ ] Acknowledge the incident
- [ ] Check slow query log
- [ ] Identify slow queries
- [ ] Check query execution plans
- [ ] Review index usage
- [ ] Begin troubleshooting

### Short-term Response (15-60 minutes)
- [ ] Kill long-running queries if needed
- [ ] Add missing indexes
- [ ] Optimize problematic queries
- [ ] Review query patterns
- [ ] Update monitoring alerts
- [ ] Document findings

### Long-term Response (1-24 hours)
- [ ] Root cause analysis
- [ ] Comprehensive query optimization
- [ ] Database design improvements
- [ ] Implement monitoring
- [ ] Update best practices
- [ ] Implement preventive measures

---

## 🔍 Advanced Troubleshooting

### MySQL Query Analysis
```sql
-- Enable query profiling
SET profiling = 1;

-- Execute query
SELECT * FROM users WHERE status = 'active';

-- Check profile
SHOW PROFILES;
SHOW PROFILE FOR QUERY 1;

-- Check optimizer trace
SET optimizer_trace = 'enabled=on';
SELECT * FROM users WHERE status = 'active';
SELECT * FROM information_schema.OPTIMIZER_TRACE;
```

### Performance Schema
```sql
-- Check statement statistics
SELECT * FROM performance_schema.events_statements_summary_by_digest
ORDER BY avg_timer_wait DESC
LIMIT 10;

-- Check table I/O
SELECT * FROM performance_schema.table_io_waits_summary_by_table
ORDER BY sum_timer_wait DESC
LIMIT 10;
```

This comprehensive incident documentation provides detailed guidance for understanding, troubleshooting, and preventing MySQL slow query incidents in database tier.

