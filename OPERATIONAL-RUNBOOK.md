# Clinical BDD Creator - Operational Runbook

## Emergency Contacts

| Role | Contact | Availability |
|------|---------|--------------|
| Development Lead | [dev-lead@company.com](mailto:dev-lead@company.com) | 24/7 |
| DevOps Engineer | [devops@company.com](mailto:devops@company.com) | Business Hours |
| Security Team | [security@company.com](mailto:security@company.com) | 24/7 |
| On-call Engineer | [oncall@company.com](mailto:oncall@company.com) | 24/7 |

## Service Overview

- **Main Application**: Flask/Gunicorn on port 3000
- **Monitoring**: Prometheus (port 9090) + Grafana (port 3001)
- **Reverse Proxy**: Nginx with SSL/TLS termination
- **Metrics**: Application metrics exposed on port 8000

## Common Operational Procedures

### Starting Services

```bash
# Start all services
./deploy.sh deploy

# Start individual service
docker-compose up -d clinical-bdd-creator

# Start with specific configuration
ENVIRONMENT=production ./deploy.sh deploy
```

### Stopping Services

```bash
# Graceful shutdown
./deploy.sh stop

# Force stop
docker-compose down --timeout 10

# Emergency stop
docker-compose kill
```

### Service Health Checks

#### Application Health

```bash
# Quick health check
curl -k https://localhost/health

# Detailed health with SSL validation
curl -v https://localhost/health

# Check service logs
./deploy.sh logs clinical-bdd-creator | tail -50
```

#### Monitoring Stack Health

```bash
# Prometheus
curl http://localhost:9090/-/healthy

# Grafana
curl http://localhost:3001/api/health

# Check all container health
docker-compose ps
```

### Log Management

#### Viewing Logs

```bash
# Application logs
./deploy.sh logs clinical-bdd-creator

# All services
docker-compose logs

# Follow logs in real-time
./deploy.sh logs -f clinical-bdd-creator

# Last hour of logs
./deploy.sh logs --since "1h" clinical-bdd-creator
```

#### Log Rotation

- Automatic log rotation configured in `config/production.ini`
- Max file size: 100MB
- Retention: 5 backup files
- Location: `/app/logs/clinical_bdd.log`

### Backup Procedures

#### Configuration Backup

```bash
# Daily configuration backup
tar -czf config_backup_$(date +%Y%m%d).tar.gz config/ .env nginx/

# Upload to secure storage
aws s3 cp config_backup_$(date +%Y%m%d).tar.gz s3://backups/clinical-bdd/
```

#### Data Backup (Future)

```bash
# Database backup (when implemented)
pg_dump clinical_bdd > db_backup_$(date +%Y%m%d).sql

# Upload to secure storage
aws s3 cp db_backup_$(date +%Y%m%d).sql s3://backups/clinical-bdd/
```

### SSL Certificate Management

#### Certificate Renewal

```bash
# Stop services
./deploy.sh stop

# Generate new certificate
openssl req -x509 -newkey rsa:4096 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem \
  -days 365 -nodes \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=your-domain.com"

# Start services
./deploy.sh deploy

# Validate certificate
openssl s_client -connect localhost:443 -servername your-domain.com < /dev/null
```

#### Certificate Validation

```bash
# Check certificate expiry
openssl x509 -in nginx/ssl/cert.pem -text -noout | grep "Not After"

# Test SSL connection
curl -v https://localhost/health
```

## Troubleshooting Guide

### Application Issues

#### High Response Times

1. Check system resources: `docker stats`
2. Review application logs for bottlenecks
3. Check database connections (future)
4. Scale up resources if needed

#### Service Unavailable

1. Check container status: `docker-compose ps`
2. Review container logs: `./deploy.sh logs clinical-bdd-creator`
3. Test health endpoint: `curl -k https://localhost/health`
4. Restart service: `./deploy.sh restart`

#### Memory Issues

1. Monitor memory usage: `docker stats`
2. Check for memory leaks in application logs
3. Restart service: `./deploy.sh restart`
4. Scale up memory limits if persistent

### Infrastructure Issues

#### Docker Issues

```bash
# Check Docker daemon
docker system info

# Clean up unused resources
docker system prune -f

# Restart Docker daemon
sudo systemctl restart docker
```

#### Network Issues

```bash
# Check network connectivity
ping google.com

# Check container networking
docker-compose exec clinical-bdd-creator ping prometheus

# Restart networking
docker-compose restart
```

### Monitoring Issues

#### Prometheus Not Collecting Metrics

1. Check Prometheus configuration
2. Verify target endpoints are accessible
3. Check Prometheus logs: `docker-compose logs prometheus`
4. Restart Prometheus: `docker-compose restart prometheus`

#### Grafana Not Loading

1. Check Grafana logs: `docker-compose logs grafana`
2. Verify database connectivity
3. Check configuration files
4. Restart Grafana: `docker-compose restart grafana`

## Performance Tuning

### Application Tuning

#### Gunicorn Configuration

```yaml
# In docker-compose.yml
command: ["gunicorn",
  "--bind", "0.0.0.0:3000",
  "--workers", "4",           # CPU cores * 2 + 1
  "--worker-class", "sync",   # Or "gevent" for async
  "--max-requests", "1000",   # Restart worker after N requests
  "--max-requests-jitter", "50"]
```

#### Resource Limits

```yaml
# In docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 2G
    reservations:
      cpus: '0.5'
      memory: 512M
```

### Monitoring Tuning

#### Prometheus Scrape Intervals

```yaml
# In monitoring/prometheus.yml
global:
  scrape_interval: 15s        # How often to scrape
  evaluation_interval: 15s    # How often to evaluate rules

scrape_configs:
  - job_name: 'clinical-bdd-creator'
    scrape_interval: 5s       # Override for this job
```

## Security Procedures

### Access Control

#### SSH Access

- Use key-based authentication only
- Disable password authentication
- Use fail2ban for brute force protection
- Regular key rotation

#### Application Security

- Regular dependency updates
- Security scanning with tools like `safety`
- Log monitoring for suspicious activity
- Regular security audits

### Incident Response

#### Security Incident

1. **Isolate**: Disconnect affected systems
2. **Assess**: Determine scope and impact
3. **Contain**: Stop the attack vector
4. **Eradicate**: Remove malicious components
5. **Recover**: Restore from clean backups
6. **Learn**: Document and improve procedures

#### Data Breach

1. **Notify**: Legal and affected parties
2. **Contain**: Stop data exfiltration
3. **Forensic**: Preserve evidence
4. **Remediate**: Fix vulnerabilities
5. **Report**: Comply with regulations

## Maintenance Windows

### Scheduled Maintenance

- **Weekly**: Log rotation and cleanup
- **Monthly**: Security updates and patches
- **Quarterly**: Major version updates
- **Annually**: Infrastructure review

### Maintenance Checklist

- [ ] Notify stakeholders of maintenance window
- [ ] Create system backup
- [ ] Test rollback procedures
- [ ] Perform maintenance tasks
- [ ] Validate system functionality
- [ ] Notify stakeholders of completion

## Escalation Procedures

### Alert Levels

#### Level 1 (Low)

- Service degradation < 10%
- Automatic resolution attempted
- Email notification to team

#### Level 2 (Medium)

- Service degradation 10-50%
- Manual intervention required
- SMS notification to on-call engineer

#### Level 3 (High)

- Service down or critical degradation
- Immediate response required
- Phone call to on-call engineer
- Escalation to management

### Escalation Timeline

- **T+0**: Alert triggered
- **T+5min**: Email notification
- **T+10min**: SMS notification
- **T+15min**: Phone call
- **T+30min**: Management notification
- **T+1hr**: Executive notification

## Recovery Procedures

### Service Recovery

1. **Assess**: Determine root cause
2. **Choose**: Select recovery strategy
3. **Execute**: Perform recovery steps
4. **Validate**: Test system functionality
5. **Monitor**: Observe for recurrence

### Data Recovery

1. **Identify**: Determine data loss scope
2. **Locate**: Find appropriate backup
3. **Restore**: Recover data from backup
4. **Validate**: Verify data integrity
5. **Resume**: Return to normal operations

## Communication Templates

### Maintenance Notification Template

```text
Subject: Scheduled Maintenance: Clinical BDD Creator - [Date/Time]

Dear Stakeholders,

We will be performing scheduled maintenance on the Clinical BDD Creator system.

Maintenance Window: [Start Time] - [End Time]
Expected Downtime: [Duration]
Services Affected: [List services]

During this maintenance, the following activities will be performed:
- [List maintenance activities]

Please plan accordingly. We apologize for any inconvenience.

Best regards,
DevOps Team
```

### Incident Notification Template

```text
Subject: INCIDENT: Clinical BDD Creator - [Severity] - [Brief Description]

Dear Stakeholders,

We have detected an incident affecting the Clinical BDD Creator system.

Status: Investigating
Impact: [Describe impact]
Start Time: [Time incident began]

We are working to resolve this issue and will provide updates.

Best regards,
Incident Response Team
```

---

*This runbook should be reviewed and updated quarterly or after significant incidents.*
