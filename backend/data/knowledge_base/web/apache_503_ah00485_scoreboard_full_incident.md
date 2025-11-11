# Apache AH00485 - Scoreboard is Full (503 Service Unavailable)

---

## 🧩 Overview

This incident involves Apache HTTP Server error code **AH00485**, which occurs when Apache's internal scoreboard (used to track worker processes) becomes full. This typically happens when `MaxRequestWorkers` is reached or when the scoreboard size is insufficient for the number of configured workers. This results in 503 Service Unavailable errors.

### Incident Summary

**Apache Error Code**: AH00485  
**HTTP Status**: 503 Service Unavailable  
**Technology**: Apache HTTP Server  
**Module**: Apache MPM (Multi-Processing Module)  
**Impact**: New requests rejected, scoreboard capacity exhausted

---

## 📊 Log Samples

### Web Tier (Apache) Logs

```
2024-01-15T14:30:06.678Z [ERROR] [trace_id:req-106-w6x7y8] [request_id:req-106] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] [Apache] AH00485: DELETE /api/sessions - 503 Service Unavailable - 9123ms - Scoreboard is full, MaxRequestWorkers reached
```

### Apache Error Log Format

```
[Wed Oct 15 14:30:06.678901 2024] [error] [pid 12345:tid 140234567890176] [client 192.168.1.100:54321] AH00485: scoreboard is full, not at MaxRequestWorkers
```

---

## 🔍 Root Cause Analysis

### Primary Causes

1. **Scoreboard Size Mismatch**
   - Scoreboard size smaller than MaxRequestWorkers
   - `ServerLimit` exceeds scoreboard capacity
   - Scoreboard not properly sized for worker configuration

2. **MaxRequestWorkers Reached**
   - All workers are busy processing requests
   - Traffic spike exceeding capacity
   - Slow backend responses holding workers

3. **Configuration Mismatch**
   - `ServerLimit` set higher than scoreboard allows
   - MPM configuration inconsistent
   - Scoreboard size hardcoded at compile time

4. **Resource Constraints**
   - Shared memory limits preventing scoreboard expansion
   - System memory constraints
   - File descriptor limits

### Apache Scoreboard Behavior

The Apache scoreboard:
- Tracks status of all worker processes/threads
- Uses shared memory (SHM) for communication
- Has a fixed size determined at compile time or configuration
- When full, Apache cannot track additional workers
- Results in AH00485 error and 503 responses

---

## 🛠️ Troubleshooting Steps

### Immediate Actions

1. **Check Apache Error Logs**
   ```bash
   # View AH00485 errors
   tail -f /var/log/apache2/error.log | grep AH00485
   
   # Check for scoreboard-related errors
   tail -f /var/log/apache2/error.log | grep -i scoreboard
   ```

2. **Verify Current Configuration**
   ```bash
   # Check MaxRequestWorkers and ServerLimit
   grep -r "MaxRequestWorkers\|ServerLimit" /etc/apache2/
   
   # Check Apache version and build info
   apache2ctl -V
   
   # Check MPM in use
   apache2ctl -V | grep "Server MPM"
   ```

3. **Check System Resources**
   ```bash
   # Check shared memory
   ipcs -m
   
   # Check memory usage
   free -h
   
   # Check file descriptors
   ulimit -n
   lsof -p $(pgrep apache2 | head -1) | wc -l
   ```

### Configuration Validation

1. **Check MPM Configuration**
   ```apache
   # /etc/apache2/mods-available/mpm_event.conf
   <IfModule mpm_event_module>
       ServerLimit 16
       MaxRequestWorkers 400
       ThreadsPerChild 25
   </IfModule>
   ```

2. **Verify Scoreboard Size**
   ```bash
   # Apache scoreboard size is typically:
   # - Determined at compile time for some MPMs
   # - Based on ServerLimit for others
   # Check Apache documentation for your MPM
   
   # For event/worker MPM:
   # Scoreboard size should be >= ServerLimit
   ```

---

## 🔧 Resolution Actions

### Short-term Fixes

1. **Reduce MaxRequestWorkers**
   ```apache
   # Temporarily reduce to fit scoreboard
   <IfModule mpm_event_module>
       ServerLimit 16
       MaxRequestWorkers 384  # Reduce if scoreboard is smaller
       ThreadsPerChild 24
   </IfModule>
   
   # Reload Apache
   systemctl reload apache2
   ```

2. **Restart Apache**
   ```bash
   # Restart to clear scoreboard
   systemctl restart apache2
   
   # Verify workers are tracking correctly
   apache2ctl status
   ```

3. **Scale Horizontally**
   ```bash
   # Add more Apache instances
   # Distribute load across multiple servers
   aws autoscaling set-desired-capacity \
       --auto-scaling-group-name apache-asg \
       --desired-capacity 4
   ```

### Long-term Solutions

1. **Rebuild Apache with Larger Scoreboard**
   ```bash
   # If using custom Apache build:
   # Recompile with larger scoreboard size
   # Or use pre-built packages with appropriate limits
   
   # For Ubuntu/Debian:
   apt-get install --reinstall apache2
   ```

2. **Optimize Configuration**
   ```apache
   # Ensure ServerLimit matches scoreboard capacity
   <IfModule mpm_event_module>
       # Set ServerLimit to match scoreboard size
       ServerLimit 16
       MaxRequestWorkers 400
       ThreadsPerChild 25
       # Ensure: MaxRequestWorkers <= ServerLimit × ThreadsPerChild
   </IfModule>
   ```

3. **Infrastructure Improvements**
   - Use multiple Apache instances
   - Implement load balancing
   - Scale horizontally
   - Use Application Load Balancer (ALB)
   - Optimize backend response times

---

## 📈 Prevention Strategies

### Best Practices

1. **Configuration Alignment**
   - Ensure ServerLimit matches scoreboard capacity
   - Verify MaxRequestWorkers calculation
   - Test configuration under load
   - Document scoreboard limits

2. **Monitoring and Alerting**
   - Monitor AH00485 error rates
   - Alert when worker usage approaches limits
   - Track scoreboard utilization
   - Monitor system resources

3. **Capacity Planning**
   - Plan for traffic spikes
   - Size scoreboard appropriately
   - Regular capacity reviews
   - Load testing before production

---

## 📋 Incident Response Checklist

### Immediate Response (0-15 minutes)
- [ ] Acknowledge the incident
- [ ] Check Apache error logs for AH00485
- [ ] Verify MaxRequestWorkers and ServerLimit settings
- [ ] Check scoreboard status
- [ ] Review system resources
- [ ] Begin troubleshooting

### Short-term Response (15-60 minutes)
- [ ] Adjust MaxRequestWorkers if needed
- [ ] Restart Apache if safe
- [ ] Scale horizontally (add instances)
- [ ] Check for traffic spikes
- [ ] Update monitoring alerts
- [ ] Document findings

### Long-term Response (1-24 hours)
- [ ] Root cause analysis
- [ ] Review and optimize configuration
- [ ] Consider rebuilding Apache if needed
- [ ] Implement auto-scaling
- [ ] Conduct capacity planning review
- [ ] Implement preventive measures

---

## 🔗 Related Apache Error Codes

- **AH01078**: Server reached MaxRequestWorkers (often occurs with AH00485)
- **AH01084**: Timeout while reading response header (may cause workers to be held)
- **AH00485**: Scoreboard is full (this error)

---

## 📚 Apache Documentation References

- Apache Scoreboard: https://httpd.apache.org/docs/2.4/misc/scoreboard.html
- ServerLimit: https://httpd.apache.org/docs/2.4/mod/event.html#serverlimit
- MaxRequestWorkers: https://httpd.apache.org/docs/2.4/mod/event.html#maxrequestworkers

---

## 💡 Technical Notes

### Scoreboard Size

- Scoreboard size is typically determined by `ServerLimit`
- Some MPMs have compile-time limits
- Scoreboard uses shared memory (SHM)
- Size depends on MPM type (event, worker, prefork)

### Relationship to MaxRequestWorkers

```
AH00485 occurs when:
- Scoreboard is full AND
- MaxRequestWorkers may or may not be reached
- Workers cannot be tracked due to scoreboard limit
```

### Common Causes

1. **ServerLimit too high** for scoreboard size
2. **Traffic spike** causing all workers to be busy
3. **Slow backend** responses holding workers
4. **Configuration mismatch** between ServerLimit and scoreboard

---

This incident documentation provides guidance for troubleshooting Apache AH00485 errors when the scoreboard is full in a 3-tier architecture with Apache HTTP Server.

