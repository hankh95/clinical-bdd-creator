# Clinical BDD Creator - Production Operations Guide

## Overview

This guide provides operational procedures for running the Clinical BDD Creator in production environments.

## Documentation Structure

This production deployment includes comprehensive operational documentation:

- **[OPERATIONAL-RUNBOOK.md](OPERATIONAL-RUNBOOK.md)** - Complete operational procedures, troubleshooting guides, escalation procedures, and emergency contacts
- **[UAT-CHECKLIST.md](UAT-CHECKLIST.md)** - User acceptance testing validation checklist for production readiness
- **[PRODUCTION-README.md](PRODUCTION-README.md)** - This quick-reference operations guide

**Start with the Operational Runbook for comprehensive procedures, then use this guide for daily operations.**

## Quick Start

### Initial Deployment

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd clinical-bdd-creator
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your production values
   ```

3. **Deploy the application:**
   ```bash
   ./deploy.sh deploy
   ```

4. **Verify deployment:**
   ```bash
   ./deploy.sh status
   ```

## Service Architecture

```
Internet → Nginx (SSL/TLS) → Clinical BDD Creator (Flask)
                           → Grafana (Monitoring UI)
                           → Prometheus (Metrics Collection)
```

### Service Ports

- **Main Application:** https://your-domain:443
- **Health Check:** https://your-domain/health
- **Grafana:** http://your-domain:3001 (admin/admin)
- **Prometheus:** http://your-domain:9090

## Daily Operations

### Health Monitoring

**Check service health:**
```bash
# Quick health check
curl -k https://localhost/health

# Detailed status
./deploy.sh status

# View logs
./deploy.sh logs clinical-bdd-creator
```

**Monitor key metrics:**
- Access Grafana at http://localhost:3001
- Check Prometheus at http://localhost:9090
- Review application logs in `/app/logs/`

### Backup Procedures

**Automated backups (configure cron):**
```bash
# Database backup (when implemented)
# pg_dump clinical_bdd > backup_$(date +%Y%m%d_%H%M%S).sql

# Configuration backup
tar -czf config_backup_$(date +%Y%m%d).tar.gz config/ .env

# Log rotation (handled by logrotate)
```

### Log Management

**View application logs:**
```bash
# Real-time logs
./deploy.sh logs clinical-bdd-creator

# Specific time range
docker-compose logs --since "2024-01-01T00:00:00" clinical-bdd-creator

# Error logs only
docker-compose logs clinical-bdd-creator 2>&1 | grep ERROR
```

**Log rotation:**
- Configured in `config/production.ini`
- Max size: 100MB per file
- Backup count: 5 files
- Automatic rotation handled by Python logging

## Troubleshooting

### Common Issues

#### Service Unhealthy

**Symptoms:** Health check fails
**Solution:**
```bash
# Restart the service
./deploy.sh restart

# Check logs for errors
./deploy.sh logs clinical-bdd-creator

# If persistent, rebuild and redeploy
./deploy.sh stop
docker-compose build --no-cache clinical-bdd-creator
./deploy.sh deploy
```

#### High Memory Usage

**Symptoms:** Container memory > 80%
**Solution:**
```bash
# Check memory usage
docker stats

# Restart service
./deploy.sh restart

# If persistent, investigate with profiling
# Add memory profiling to application
```

#### Slow Response Times

**Symptoms:** P95 latency > 5 seconds
**Solution:**
- Check system resources: `docker stats`
- Review application logs for bottlenecks
- Scale up resources if needed
- Check database connections (future)

### Performance Tuning

**Current limits:**
- Max concurrent requests: 10
- Request timeout: 300 seconds
- Memory limit: 2GB
- CPU limit: 2.0 cores

**Scaling:**
```bash
# Increase resources
docker-compose up -d --scale clinical-bdd-creator=2

# Update limits in docker-compose.yml
# Restart services
./deploy.sh restart
```

## Security Operations

### SSL/TLS Management

**Certificate renewal:**
```bash
# Generate new certificates
./deploy.sh stop
rm -f nginx/ssl/*
openssl req -x509 -newkey rsa:4096 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=your-domain.com"

# Restart services
./deploy.sh deploy
```

### Access Control

**Update admin credentials:**
```bash
# Grafana admin password
docker-compose exec grafana grafana-cli admin password admin newpassword

# Update .env file
echo "GRAFANA_ADMIN_PASSWORD=newpassword" >> .env
```

### Security Monitoring

**Monitor for security events:**
- Review application logs for authentication failures
- Check Prometheus metrics for unusual patterns
- Monitor SSL/TLS handshake failures

## Maintenance Procedures

### Weekly Tasks

1. **Review logs:** Check for errors and warnings
2. **Update dependencies:** `docker-compose pull && ./deploy.sh deploy`
3. **Backup configurations:** See backup procedures
4. **Monitor disk usage:** `df -h`

### Monthly Tasks

1. **Security updates:** Update base images
2. **Performance review:** Analyze metrics trends
3. **Log archive:** Archive old logs
4. **Certificate check:** Verify SSL certificates

### Emergency Procedures

#### Service Outage

1. **Assess impact:** Check service status and user impact
2. **Check logs:** Identify root cause
3. **Implement fix:** Restart, rollback, or emergency patch
4. **Communicate:** Notify stakeholders
5. **Post-mortem:** Document incident and prevention measures

#### Data Loss

1. **Stop services:** Prevent further data corruption
2. **Assess damage:** Determine scope of data loss
3. **Restore from backup:** Use latest backup
4. **Verify integrity:** Run integration tests
5. **Resume operations:** Bring services back online

## Monitoring & Alerting

### Key Metrics to Monitor

- **Application Health:** Service availability and response times
- **Resource Usage:** CPU, memory, disk usage
- **Error Rates:** Application and infrastructure errors
- **Performance:** Request latency and throughput
- **Security:** Failed authentication attempts

### Alert Configuration

**Recommended alerts:**
- Service down for > 5 minutes
- Memory usage > 90%
- Error rate > 5%
- Response time > 10 seconds
- Disk usage > 85%

## Scaling & Performance

### Horizontal Scaling

```bash
# Scale application instances
docker-compose up -d --scale clinical-bdd-creator=3

# Add load balancer (nginx already configured)
# Update nginx.conf upstream block
```

### Vertical Scaling

```bash
# Increase resource limits
# Edit docker-compose.yml
# Restart services
./deploy.sh restart
```

## Backup & Recovery

### Automated Backups

**Configure cron jobs:**
```bash
# Daily configuration backup
0 2 * * * /path/to/clinical-bdd-creator/backup-config.sh

# Weekly full backup
0 3 * * 0 /path/to/clinical-bdd-creator/backup-full.sh
```

### Disaster Recovery

**Recovery time objective (RTO):** 4 hours
**Recovery point objective (RPO):** 1 hour

**Recovery steps:**
1. Provision new infrastructure
2. Restore from latest backup
3. Update DNS/configuration
4. Test and validate
5. Resume operations

## Support & Contact

### Internal Support

- **Development Team:** For application issues
- **DevOps Team:** For infrastructure issues
- **Security Team:** For security incidents

### External Resources

- **Documentation:** https://clinical-bdd-creator.readthedocs.io/
- **GitHub Issues:** For bug reports and feature requests
- **Community Forum:** For general questions

---

*This operations guide should be updated as the system evolves and new operational procedures are established.*