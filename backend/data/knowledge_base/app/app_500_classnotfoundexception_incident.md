# Application 500 Internal Server Error — ClassNotFoundException

---

## 🧩 Overview

A ClassNotFoundException occurs when the Java Virtual Machine (JVM) cannot find a required class at runtime. This exception indicates classpath issues, missing dependencies, or class loading failures in Java/Spring Boot applications.

### What is a ClassNotFoundException?

A ClassNotFoundException is a Java exception that occurs when:
- Required class is not found in classpath
- JAR file is missing from classpath
- Class file is not in expected location
- Dependency is not included in deployment
- Class loader cannot locate the class

### Java/Spring Boot Behavior

When a ClassNotFoundException occurs in a Spring Boot microservice:
- JVM throws ClassNotFoundException during class loading
- Application may fail to start
- Service initialization may fail
- Spring context may fail to load
- Service becomes unavailable

### Application Tier Symptoms

**Java/Spring Boot Symptoms:**
- ClassNotFoundException in application logs
- Application startup failures
- Spring context initialization failures
- Service not starting
- Missing dependency errors

---

## 📊 Log Samples

### Application Tier (Java/Spring Boot) Logs

```
2024-01-15T15:00:09.420Z [ERROR] [trace_id:req-209-a9b0c1] [request_id:req-209] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:settings-service] ClassNotFoundException: Settings configuration class not found - 3456ms
2024-01-15T15:00:14.453Z [ERROR] [trace_id:req-214-b1c2d3] [request_id:req-214] [ELB:backend-sg] [AZ:us-east-1b] [EC2:i-0987654321fedcba1] [Service:config-service] ClassNotFoundException: Configuration manager class not found - 4567ms
2024-01-15T15:00:19.486Z [ERROR] [trace_id:req-219-b2c3d4] [request_id:req-219] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:auth-service] ClassNotFoundException: Security provider class not found - 5678ms
2024-01-15T15:00:24.519Z [ERROR] [trace_id:req-224-b3c4d5] [request_id:req-224] [ELB:backend-sg] [AZ:us-east-1b] [EC2:i-0987654321fedcba1] [Service:integration-service] ClassNotFoundException: Integration adapter class not found - 6789ms
2024-01-15T15:00:29.552Z [ERROR] [trace_id:req-229-b4c5d6] [request_id:req-229] [ELB:backend-sg] [AZ:us-east-1a] [EC2:i-0987654321fedcba0] [Service:report-service] ClassNotFoundException: Report generator class not found - 7890ms
```

### Java Exception Format

```
java.lang.ClassNotFoundException: com.example.settings.SettingsConfiguration
    at java.net.URLClassLoader.findClass(URLClassLoader.java:382)
    at java.lang.ClassLoader.loadClass(ClassLoader.java:418)
    at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:352)
    at java.lang.ClassLoader.loadClass(ClassLoader.java:351)
    at org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider.findCandidateComponents(ClassPathScanningCandidateComponentProvider.java:280)
```

---

## 🔍 Root Cause Analysis

### Primary Causes

1. **Missing Dependencies**
   - Required JAR file not in classpath
   - Maven/Gradle dependency not included
   - Dependency version mismatch
   - Missing transitive dependencies
   - Dependency not packaged in deployment

2. **Classpath Issues**
   - Incorrect classpath configuration
   - Class not in expected package
   - Class file not compiled
   - Class removed from codebase
   - Package structure changed

3. **Deployment Issues**
   - Missing files in deployment package
   - Incorrect deployment structure
   - Files not copied to deployment
   - Build artifacts incomplete
   - Deployment process errors

4. **Class Loading Problems**
   - Class loader configuration issues
   - Multiple class loaders conflict
   - Class visibility problems
   - Module system issues

### Common Scenarios

1. **Build and Deployment**
   - Missing dependencies in build
   - Incomplete deployment package
   - Build configuration errors
   - Deployment script issues

2. **Dependency Management**
   - Dependency not declared
   - Version conflicts
   - Scope issues (provided vs compile)
   - Transitive dependency problems

3. **Code Changes**
   - Class renamed or moved
   - Package structure changed
   - Class removed from codebase
   - Refactoring issues

---

## 🛠️ Troubleshooting Steps

### Immediate Actions

1. **Check Application Logs**
   ```bash
   # Check for ClassNotFoundException
   tail -f /var/log/application/application.log | grep -i "ClassNotFoundException"
   
   # Check startup logs
   journalctl -u settings-service -f | grep -i "ClassNotFoundException"
   
   # Check Spring Boot logs
   tail -f /var/log/spring-boot/spring.log | grep -i "ClassNotFoundException"
   ```

2. **Check Service Status**
   ```bash
   # Check if service started
   systemctl status settings-service
   
   # Check service startup logs
   journalctl -u settings-service --since "10 minutes ago" | grep -i "Error\|Exception\|Failed"
   ```

3. **Verify Classpath**
   ```bash
   # Check JAR files in deployment
   ls -la /opt/settings-service/lib/
   
   # Check classpath in service configuration
   cat /etc/systemd/system/settings-service.service | grep -i "classpath\|cp"
   ```

### Dependency Analysis

1. **Check Maven/Gradle Dependencies**
   ```xml
   <!-- Check pom.xml for missing dependencies -->
   <dependency>
       <groupId>com.example</groupId>
       <artifactId>settings-config</artifactId>
       <version>1.0.0</version>
   </dependency>
   ```

2. **Verify Deployment Package**
   ```bash
   # Check JAR contents
   jar -tf settings-service.jar | grep "SettingsConfiguration"
   
   # Check if dependency JARs are present
   ls -la /opt/settings-service/lib/ | grep "settings-config"
   ```

---

## 🔧 Resolution Actions

### Short-term Fixes

1. **Add Missing Dependency**
   ```xml
   <!-- Add to pom.xml -->
   <dependency>
       <groupId>com.example</groupId>
       <artifactId>settings-config</artifactId>
       <version>1.0.0</version>
   </dependency>
   ```

2. **Rebuild and Redeploy**
   ```bash
   # Rebuild application
   mvn clean package
   
   # Or with Gradle
   ./gradlew clean build
   
   # Redeploy service
   systemctl restart settings-service
   ```

3. **Manual Dependency Addition**
   ```bash
   # Copy missing JAR to classpath
   cp settings-config-1.0.0.jar /opt/settings-service/lib/
   
   # Restart service
   systemctl restart settings-service
   ```

### Long-term Solutions

1. **Fix Build Configuration**
   - Ensure all dependencies are declared
   - Fix dependency versions
   - Resolve version conflicts
   - Update build scripts

2. **Improve Deployment Process**
   - Verify deployment package completeness
   - Add dependency validation
   - Implement deployment checks
   - Add automated testing

3. **Dependency Management**
   - Use dependency management tools
   - Implement dependency versioning
   - Add dependency scanning
   - Monitor dependency updates

---

## 📈 Prevention Strategies

### Best Practices

1. **Dependency Management**
   - Declare all dependencies explicitly
   - Use dependency management tools
   - Keep dependencies up to date
   - Resolve version conflicts

2. **Build Process**
   - Validate build artifacts
   - Test deployment packages
   - Verify classpath configuration
   - Add build validation

3. **Deployment**
   - Verify deployment packages
   - Test deployments in staging
   - Validate classpath at startup
   - Monitor deployment process

---

## 📋 Incident Response Checklist

### Immediate Response (0-15 minutes)
- [ ] Acknowledge the incident
- [ ] Check application logs for ClassNotFoundException
- [ ] Identify missing class
- [ ] Check service startup status
- [ ] Verify classpath configuration
- [ ] Begin troubleshooting

### Short-term Response (15-60 minutes)
- [ ] Add missing dependency
- [ ] Rebuild and redeploy if needed
- [ ] Verify classpath
- [ ] Check deployment package
- [ ] Update monitoring alerts
- [ ] Document findings

### Long-term Response (1-24 hours)
- [ ] Root cause analysis
- [ ] Fix build configuration
- [ ] Improve deployment process
- [ ] Update dependency management
- [ ] Add validation checks
- [ ] Implement preventive measures

---

## 🔍 Advanced Troubleshooting

### Classpath Analysis
```bash
# Check classpath
echo $CLASSPATH

# Check JVM classpath
jps -l
jinfo <pid> | grep "java.class.path"

# List classes in JAR
jar -tf application.jar | grep "ClassName"
```

### Dependency Analysis
```bash
# Check Maven dependencies
mvn dependency:tree

# Check Gradle dependencies
./gradlew dependencies

# Check for missing dependencies
mvn dependency:analyze
```

This comprehensive incident documentation provides detailed guidance for understanding, troubleshooting, and preventing ClassNotFoundException incidents in Java/Spring Boot microservices.

