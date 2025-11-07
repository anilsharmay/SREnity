# Apache 504 Gateway Timeout — Upstream Server Timeout

---

## 🧩 Overview

A 504 Gateway Timeout error occurs when Apache, acting as a reverse proxy, cannot receive a timely response from an upstream server within the configured timeout period. This error indicates Apache proxy timeout issues or upstream server unresponsiveness.

### What is a 504 Gateway Timeout?

A 504 Gateway Timeout is an HTTP status code that indicates Apache did not receive a response from an upstream server within the allotted time. This differs from a 502 Bad Gateway, which indicates the upstream server returned an invalid response, or a 503 Service Unavailable, which indicates Apache is temporarily overloaded.

### Apache mod_proxy Behavior

When Apache's mod_proxy forwards a request to an upstream server, it waits for a response based on several configuration parameters:
- **ProxyTimeout**: Maximum time to wait for a response from the backend
- **Timeout**: Maximum time to wait for any I/O operation
- **KeepAliveTimeout**: Time to keep connections alive to backends

### Symptoms Across Infrastructure

**ELB/ALB Symptoms:**
- Increased latency metrics
- 504 error rate spikes
- Backend health check failures
- Connection timeout alerts

**Web Tier Symptoms:**
- Apache error logs showing timeout messages
- Increased worker process utilization
- Connection pool exhaustion
- Memory pressure from pending requests

**Apache Proxy Symptoms:**
- Apache proxy timeout errors (AH01079, AH01084)
- Upstream server unresponsive
- Apache connection pool exhaustion
- Apache proxy configuration issues

---

## 📊 Log Samples

### Web Tier (Apache) Logs

```
2024-01-15T10:00:01.123Z [ERROR] [trace_id:req-001-abc123] [request_id:req-001] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] [Apache] AH01079: GET /api/orders - 504 Gateway Timeout - 30000ms - Timeout specified has expired
2024-01-15T10:00:01.456Z [ERROR] [trace_id:req-002-def456] [request_id:req-002] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] POST /api/checkout - 504 Gateway Timeout - 30000ms - Backend service timeout
2024-01-15T10:00:01.789Z [ERROR] [trace_id:req-003-ghi789] [request_id:req-003] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] GET /api/reports - 504 Gateway Timeout - 30000ms - Backend service unresponsive
2024-01-15T10:00:02.123Z [ERROR] [trace_id:req-004-jkl012] [request_id:req-004] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] GET /api/analytics - 504 Gateway Timeout - 30000ms - Backend service overloaded
2024-01-15T10:00:02.456Z [ERROR] [trace_id:req-005-mno345] [request_id:req-005] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] POST /api/upload - 504 Gateway Timeout - 30000ms - Backend processing timeout
2024-01-15T10:00:02.789Z [ERROR] [trace_id:req-006-pqr678] [request_id:req-006] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] GET /api/import - 504 Gateway Timeout - 30000ms - Backend processing timeout
2024-01-15T10:00:03.123Z [ERROR] [trace_id:req-007-stu901] [request_id:req-007] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] GET /api/backup - 504 Gateway Timeout - 30000ms - Backend service overloaded
2024-01-15T10:00:03.456Z [ERROR] [trace_id:req-008-vwx234] [request_id:req-008] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] GET /api/metrics - 504 Gateway Timeout - 30000ms - Backend timeout
2024-01-15T10:00:03.789Z [ERROR] [trace_id:req-009-yza567] [request_id:req-009] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] GET /api/stream - 504 Gateway Timeout - 30000ms - Backend stream timeout
2024-01-15T10:00:04.123Z [ERROR] [trace_id:req-010-bcd890] [request_id:req-010] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] POST /api/process - 504 Gateway Timeout - 30000ms - Backend service unavailable
2024-01-15T10:00:04.456Z [ERROR] [trace_id:req-011-efg123] [request_id:req-011] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] GET /api/export - 504 Gateway Timeout - 30000ms - Backend export timeout
2024-01-15T10:00:04.789Z [ERROR] [trace_id:req-012-hij456] [request_id:req-012] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] POST /api/sync - 504 Gateway Timeout - 30000ms - Backend sync timeout
2024-01-15T10:00:05.123Z [ERROR] [trace_id:req-013-klm789] [request_id:req-013] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] GET /api/validate - 504 Gateway Timeout - 30000ms - Backend validation timeout
2024-01-15T10:00:05.456Z [ERROR] [trace_id:req-014-nop012] [request_id:req-014] [ELB:frontend-sg] [AZ:us-east-1b] [EC2:i-0123456789abcdef1] PUT /api/update - 504 Gateway Timeout - 30000ms - Backend update timeout
2024-01-15T10:00:05.789Z [ERROR] [trace_id:req-015-qrs345] [request_id:req-015] [ELB:frontend-sg] [AZ:us-east-1a] [EC2:i-0123456789abcdef0] DELETE /api/cleanup - 504 Gateway Timeout - 30000ms - Backend cleanup timeout
```

### ELB/ALB Logs

```
2024-01-15T10:00:01.123Z [INFO] [ELB:frontend-sg] [AZ:us-east-1a] Backend health check failed for target i-0987654321fedcba0
2024-01-15T10:00:01.456Z [WARN] [ELB:frontend-sg] [AZ:us-east-1b] Connection timeout to backend i-0987654321fedcba1
2024-01-15T10:00:01.789Z [ERROR] [ELB:frontend-sg] [AZ:us-east-1a] Target group health check failure - all targets unhealthy
2024-01-15T10:00:02.123Z [INFO] [ELB:frontend-sg] [AZ:us-east-1b] Auto scaling triggered due to unhealthy targets
2024-01-15T10:00:02.456Z [WARN] [ELB:frontend-sg] [AZ:us-east-1a] High latency detected - 95th percentile > 5000ms
2024-01-15T10:00:02.789Z [ERROR] [ELB:frontend-sg] [AZ:us-east-1b] Target group deregistering unhealthy instances
2024-01-15T10:00:03.123Z [INFO] [ELB:frontend-sg] [AZ:us-east-1a] New instances being registered to target group
2024-01-15T10:00:03.456Z [WARN] [ELB:frontend-sg] [AZ:us-east-1b] Health check grace period expired for new instances
```

### Apache Error Log Format

```
[Wed Oct 15 10:00:01.123456 2024] [error] [pid 12345:tid 140234567890176] [client 192.168.1.100:54321] AH01079: Timeout specified has expired
[Wed Oct 15 10:00:01.456789 2024] [error] [pid 12345:tid 140234567890177] [client 192.168.1.101:54322] AH01084: Timeout while reading response header from upstream server
[Wed Oct 15 10:00:01.789012 2024] [error] [pid 12345:tid 140234567890178] [client 192.168.1.102:54323] AH01079: Proxy timeout expired
[Wed Oct 15 10:00:02.123456 2024] [error] [pid 12345:tid 140234567890179] [client 192.168.1.103:54324] AH01084: Upstream server timeout
[Wed Oct 15 10:00:02.456789 2024] [error] [pid 12345:tid 140234567890180] [client 192.168.1.104:54325] AH01079: Timeout waiting for upstream response
```

---

## 🔍 Root Cause Analysis

### Primary Causes

1. **Upstream Server Unresponsive**
   - Upstream server not responding within timeout period
   - Upstream server overloaded
   - Network latency between Apache and upstream
   - Upstream server processing delays

2. **Apache Proxy Configuration Issues**
   - Inadequate ProxyTimeout settings
   - Insufficient Apache worker process limits
   - Improper Apache KeepAlive configuration
   - Missing Apache proxy error handling

3. **Network Connectivity Problems**
   - High latency between Apache and upstream servers
   - Network packet loss or congestion
   - DNS resolution delays
   - Firewall or security group misconfigurations

4. **Apache Resource Contention**
   - Apache connection pool exhaustion
   - Network bandwidth limitations
   - Apache worker process saturation
   - System resource constraints affecting Apache

### Configuration Issues

1. **Apache Proxy Configuration Problems**
   - Inadequate ProxyTimeout settings
   - Insufficient Apache worker process limits
   - Improper Apache KeepAlive configuration
   - Missing Apache proxy error handling

2. **Apache Timeout Configuration**
   - ProxyTimeout too low for upstream processing
   - Timeout directive misconfiguration
   - KeepAliveTimeout conflicts
   - ProxyReceiveTimeout settings

3. **Apache Module Configuration**
   - mod_proxy module issues
   - mod_proxy_http configuration errors
   - SSL proxy timeout settings
   - Proxy connection pool configuration

---

## 🛠️ Troubleshooting Steps

### Immediate Actions

1. **Check Apache Error Logs**
   ```bash
   # Check Apache error logs for timeout errors
   tail -f /var/log/apache2/error.log | grep -E "AH01079|AH01084|504"
   
   # Check Apache access logs
   tail -f /var/log/apache2/access.log | grep "504"
   
   # Check Apache status
   systemctl status apache2
   ```

2. **Verify Upstream Server Connectivity**
   ```bash
   # Test upstream server connectivity
   curl -v --max-time 5 http://upstream-server:8080/health
   
   # Check network connectivity
   ping upstream-server-ip
   telnet upstream-server-ip 8080
   
   # Check DNS resolution
   nslookup upstream-server-hostname
   ```

3. **Review Apache Configuration**
   ```bash
   # Check Apache configuration
   apache2ctl configtest
   
   # Check Apache proxy settings
   apache2ctl -S | grep ProxyPass
   
   # Check loaded modules
   apache2ctl -M | grep proxy
   ```

### Configuration Validation

1. **Apache Proxy Settings**
   ```apache
   # Verify ProxyTimeout configuration
   ProxyTimeout 300
   Timeout 300
   KeepAliveTimeout 15
   ProxyReceiveTimeout 300
   
   # Check proxy configuration
   ProxyPass /api/ http://upstream-server:8080/
   ProxyPassReverse /api/ http://upstream-server:8080/
   
   # Add error handling
   ProxyErrorOverride On
   ProxyPreserveHost On
   ```

2. **Apache mod_proxy Module**
   ```apache
   # Verify mod_proxy is loaded
   LoadModule proxy_module modules/mod_proxy.so
   LoadModule proxy_http_module modules/mod_proxy_http.so
   
   # Check proxy settings
   ProxyRequests Off
   ProxyPreserveHost On
   ```

---

## 🔧 Resolution Actions

### Short-term Fixes

1. **Increase Apache Timeout Values**
   - Temporarily increase ProxyTimeout to 300 seconds
   - Adjust ProxyReceiveTimeout settings
   - Increase Timeout directive value
   - Configure appropriate KeepAliveTimeout

2. **Fix Apache Proxy Configuration**
   - Update upstream server addresses
   - Verify mod_proxy module is loaded
   - Check Apache proxy connection pools
   - Review Apache worker process limits

3. **Implement Apache Error Handling**
   - Configure ProxyErrorOverride
   - Add custom error pages for 504 errors
   - Implement Apache proxy retry logic
   - Monitor Apache proxy connection status

### Long-term Solutions

1. **Apache Performance Optimization**
   - Optimize Apache proxy configuration
   - Implement Apache connection pooling
   - Tune Apache worker process settings
   - Optimize Apache KeepAlive settings

2. **Apache Architecture Improvements**
   - Configure multiple upstream servers for redundancy
   - Implement Apache load balancing
   - Add Apache health check monitoring
   - Configure Apache proxy failover

3. **Apache Monitoring and Alerting**
   - Set up proactive monitoring for Apache timeout conditions
   - Monitor Apache error logs (AH01079, AH01084)
   - Add Apache performance dashboards
   - Implement Apache proxy metrics collection

---

## 📈 Prevention Strategies

### Monitoring and Alerting

1. **Key Apache Metrics to Monitor**
   - Apache response time percentiles (P95, P99)
   - Apache 504 error rates by endpoint
   - Apache proxy connection pool utilization
   - Apache worker process utilization
   - Apache system resource utilization (CPU, memory, disk, network)

2. **Apache Alert Thresholds**
   - Apache response time > 5 seconds
   - Apache 504 error rate > 5%
   - Apache proxy connection pool > 80% utilization
   - Apache worker process exhaustion
   - Apache CPU utilization > 80%

### Apache Capacity Planning

1. **Apache Load Testing**
   - Regular Apache performance testing
   - Stress testing Apache with realistic loads
   - Apache capacity planning based on growth projections
   - Apache proxy timeout testing

2. **Apache Configuration**
   - Proper ProxyTimeout settings
   - Apache worker process limits
   - Apache connection pool sizing
   - Apache proxy timeout configuration

### Apache Best Practices

1. **Apache Configuration Management**
   - Use infrastructure as code for Apache
   - Implement Apache configuration validation
   - Regular Apache configuration audits
   - Environment-specific Apache configurations

2. **Apache Deployment Practices**
   - Apache configuration testing before deployment
   - Apache graceful reload procedures
   - Apache configuration backup and rollback
   - Apache health check validation

---

## 🔄 Recovery Procedures

### Automated Recovery

1. **Apache Health Check Recovery**
   ```bash
   #!/bin/bash
   ERROR_COUNT=$(grep -c "AH01079\|AH01084" /var/log/apache2/error.log | tail -100)
   if [ $ERROR_COUNT -gt 10 ]; then
       # Restart Apache
       systemctl restart apache2
       sleep 10
       # Verify Apache is running
       if ! systemctl is-active --quiet apache2; then
           # Alert operations team
           echo "Apache recovery failed" | mail -s "Alert" ops@company.com
       fi
   fi
   ```

2. **Apache Configuration Recovery**
   ```bash
   # Backup Apache configuration
   cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/000-default.conf.backup
   
   # Restore from backup if needed
   # cp /etc/apache2/sites-available/000-default.conf.backup /etc/apache2/sites-available/000-default.conf
   
   # Reload Apache
   apache2ctl graceful
   ```

### Manual Recovery Steps

1. **Apache Restart**
   ```bash
   # Restart Apache
   systemctl restart apache2
   
   # Or graceful reload
   apache2ctl graceful
   
   # Verify Apache is running
   systemctl status apache2
   
   # Check Apache error logs
   tail -f /var/log/apache2/error.log | grep -E "AH01079|AH01084"
   ```

2. **Apache Configuration Fix**
   ```bash
   # Backup current Apache configuration
   cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/000-default.conf.backup
   
   # Update Apache configuration
   vi /etc/apache2/sites-available/000-default.conf
   
   # Test Apache configuration
   apache2ctl configtest
   
   # Reload Apache with new configuration
   apache2ctl graceful
   ```

---

## 📋 Incident Response Checklist

### Immediate Response (0-15 minutes)
- [ ] Acknowledge the incident
- [ ] Check Apache error logs for AH01079/AH01084
- [ ] Review Apache proxy configuration
- [ ] Test upstream server connectivity
- [ ] Begin troubleshooting

### Short-term Response (15-60 minutes)
- [ ] Implement temporary Apache fixes
- [ ] Adjust Apache ProxyTimeout if needed
- [ ] Update Apache monitoring alerts
- [ ] Document findings
- [ ] Communicate status updates

### Long-term Response (1-24 hours)
- [ ] Root cause analysis
- [ ] Implement permanent fixes
- [ ] Update runbooks
- [ ] Conduct post-incident review
- [ ] Implement preventive measures

---

## 🎯 Key Performance Indicators (KPIs)

### Response Time Metrics
- **Target P95 Response Time**: < 2 seconds
- **Target P99 Response Time**: < 5 seconds
- **Maximum Acceptable Timeout**: 30 seconds

### Error Rate Metrics
- **Target Error Rate**: < 0.1%
- **Maximum Acceptable Error Rate**: < 1%
- **Timeout Rate Threshold**: < 0.5%

### Availability Metrics
- **Target Uptime**: 99.9%
- **Maximum Acceptable Downtime**: 8.76 hours/year
- **Recovery Time Objective (RTO)**: < 15 minutes
- **Recovery Point Objective (RPO)**: < 5 minutes

This comprehensive incident documentation provides detailed guidance for understanding, troubleshooting, and preventing Apache 504 Gateway Timeout errors (AH01079, AH01084) related to Apache HTTP Server proxy timeout configuration and upstream server connectivity issues.



