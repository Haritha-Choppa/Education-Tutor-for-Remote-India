# Production Deployment Guide

## Overview

This guide covers deploying the Education Tutor Platform to production for remote area deployment.

## Pre-Deployment Checklist

- [ ] Environment variables configured
- [ ] Database backup strategy implemented
- [ ] Error logging enabled
- [ ] Performance optimized
- [ ] Security hardened
- [ ] Tested on target hardware
- [ ] Backup plan in place

## Environment Configuration

### Backend (.env)

```env
# Server Configuration
FLASK_ENV=production
FLASK_DEBUG=false
API_HOST=0.0.0.0
API_PORT=5000

# Database
DATABASE_URL=sqlite:///instance/tutoring.db
DATABASE_BACKUP=/backups/tutoring.db

# Security
SECRET_KEY=your-very-secure-random-key-here

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://192.168.1.100:3000

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/tutoring-api.log
```

### Frontend (.env)

```env
# API Configuration
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_API_TIMEOUT=5000

# Feature Flags
REACT_APP_OFFLINE_MODE=true
REACT_APP_DEBUG_MODE=false

# Storage
REACT_APP_CACHE_DURATION=86400
```

## Installation Steps

### 1. Prepare System

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip nodejs npm postgresql
```

### 2. Install Backend

```bash
# Clone/copy project
cp -r /source/backend /opt/tutoring-app/backend
cd /opt/tutoring-app/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Initialize database
python init_db.py

# Create systemd service
sudo nano /etc/systemd/system/tutoring-api.service
```

Systemd service file:
```ini
[Unit]
Description=Education Tutor API
After=network.target

[Service]
Type=simple
User=tutoring
WorkingDirectory=/opt/tutoring-app/backend
Environment="PATH=/opt/tutoring-app/backend/venv/bin"
ExecStart=/opt/tutoring-app/backend/venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl start tutoring-api
sudo systemctl enable tutoring-api
```

### 3. Install Frontend

```bash
# Install and build
cp -r /source/frontend /opt/tutoring-app/frontend
cd /opt/tutoring-app/frontend
npm install
npm run build

# Setup nginx
sudo apt install -y nginx
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    root /opt/tutoring-app/frontend/build;
    index index.html;
    
    # API proxy
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # React routing
    location / {
        try_files $uri, $uri/, /index.html;
    }
    
    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable nginx:
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

## Database Backup

### Automated Backup Script

Create `/opt/tutoring-app/backup.sh`:
```bash
#!/bin/bash
DB_FILE="/opt/tutoring-app/backend/instance/tutoring.db"
BACKUP_DIR="/opt/tutoring-app/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp $DB_FILE $BACKUP_DIR/tutoring_$DATE.db

# Keep only last 30 days
find $BACKUP_DIR -name "tutoring_*.db" -mtime +30 -delete

echo "Backup completed: $BACKUP_DIR/tutoring_$DATE.db"
```

Cron job:
```bash
# Backup daily at 2 AM
0 2 * * * /opt/tutoring-app/backup.sh
```

## Security Hardening

### 1. Firewall Setup

```bash
sudo ufw enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS (future)
sudo ufw allow 5000/tcp  # API (local only)
```

### 2. SSL/HTTPS Setup

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

### 3. Application Security

Update Flask settings:
```python
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=3600
)
```

## Monitoring

### System Monitoring

```bash
# Install monitoring tools
sudo apt install -y htop iotop nethogs

# Check status
systemctl status tutoring-api
```

### Log Rotation

Create `/etc/logrotate.d/tutoring`:
```
/var/log/tutoring-*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 tutoring tutoring
}
```

### Application Monitoring

```python
# Add to backend/run.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    app.logger.addHandler(file_handler)
```

## Performance Optimization

### Backend

```python
# Add caching
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/lessons')
@cache.cached(timeout=3600)
def get_lessons():
    return ...
```

### Frontend

```javascript
// Code splitting
const Dashboard = lazy(() => import('./components/Dashboard'));
const Lessons = lazy(() => import('./components/LessonsList'));

// Lazy load routes
<Suspense fallback={<Loading />}>
  <Routes>
    <Route path="/dashboard" element={<Dashboard />} />
  </Routes>
</Suspense>
```

## Rollback Procedure

```bash
# View recent backups
ls -la /opt/tutoring-app/backups/

# Restore from backup
cp /opt/tutoring-app/backups/tutoring_20240115_020000.db \
   /opt/tutoring-app/backend/instance/tutoring.db

# Restart service
sudo systemctl restart tutoring-api
```

## Remote Deployment

### For Areas with Internet

1. Set up server in nearest connected location
2. Use Wi-Fi hotspot for initial sync
3. Operate fully offline once data is cached

### For Areas with Limited/No Internet

1. Pre-load all content on USB drives
2. Use local network (LAN) for connectivity
3. Manual sync via USB when going to connected areas

## Health Check

```bash
#!/bin/bash

# Check API
curl -s http://localhost:5000/api/lessons | jq . > /dev/null
if [ $? -eq 0 ]; then
  echo "API: OK"
else
  echo "API: FAILED"
  systemctl restart tutoring-api
fi

# Check Frontend
curl -s http://localhost/ | grep "root" > /dev/null
if [ $? -eq 0 ]; then
  echo "Frontend: OK"
else
  echo "Frontend: FAILED"
  systemctl restart nginx
fi

# Check Database
ls -l /opt/tutoring-app/backend/instance/tutoring.db > /dev/null
if [ $? -eq 0 ]; then
  echo "Database: OK"
else
  echo "Database: FAILED"
fi
```

## Troubleshooting Production Issues

### API Not Responding

```bash
# Check service status
sudo systemctl status tutoring-api

# View logs
sudo journalctl -u tutoring-api -f

# Restart service
sudo systemctl restart tutoring-api
```

### Database Corruption

```bash
# Backup corrupted database
cp instance/tutoring.db instance/tutoring.db.corrupted

# Restore from backup
cp backups/tutoring_YYYYMMDD_HHMMSS.db instance/tutoring.db

# Restart
sudo systemctl restart tutoring-api
```

### High Memory Usage

```bash
# Check process memory
ps aux | grep python

# Check database size
du -sh backend/instance/tutoring.db

# Consider archiving old data or implementing pagination
```

## Upgrade Procedure

### 1. Backup Everything
```bash
cp -r /opt/tutoring-app /opt/tutoring-app.backup
```

### 2. Stop Services
```bash
sudo systemctl stop tutoring-api
sudo systemctl stop nginx
```

### 3. Deploy New Version
```bash
cp -r /source/backend /opt/tutoring-app/backend
cp -r /source/frontend /opt/tutoring-app/frontend
cd /opt/tutoring-app/backend
source venv/bin/activate
pip install -r requirements.txt
cd /opt/tutoring-app/frontend
npm install
npm run build
```

### 4. Start Services
```bash
sudo systemctl start tutoring-api
sudo systemctl start nginx
```

### 5. Verify
```bash
curl http://localhost/api/lessons
```

## Documentation

Create a runbook for operators:
- How to backup data
- How to restore from backup
- How to handle common issues
- Emergency contact numbers

## Maintenance Schedule

| Task | Frequency | Owner |
|------|-----------|-------|
| Backups | Daily | Automated |
| Updates | Monthly | Admin |
| Security patches | ASAP | Admin |
| Performance review | Weekly | Tech |
| User reports | As-needed | Support |

---

**Version**: 1.0
**Last Updated**: 2024
**Maintained By**: Your Organization
