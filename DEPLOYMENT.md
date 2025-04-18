# Deployment Guide

## Prerequisites

- Ubuntu/Debian server
- Python 3.8+
- PostgreSQL
- Nginx
- Domain name (optional)

## 1. Environment Setup

```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

## 2. Database Setup

```bash
# Create PostgreSQL database and user
sudo -u postgres psql
CREATE DATABASE ecommerce;
CREATE USER ecommerce_user WITH PASSWORD 'your_secure_password';
ALTER ROLE ecommerce_user SET client_encoding TO 'utf8';
ALTER ROLE ecommerce_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ecommerce_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ecommerce TO ecommerce_user;
\q
```

## 3. Environment Variables

Create a `.env` file in your project directory:

```bash
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://ecommerce_user:your_secure_password@localhost:5432/ecommerce
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## 4. Gunicorn Setup

Create a Gunicorn service file at `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=your_user
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock ecommerce.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable the Gunicorn service:

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## 5. Nginx Configuration

Create an Nginx configuration file at `/etc/nginx/sites-available/ecommerce`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/your/project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Enable the site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 6. SSL Setup (Optional)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## 7. Security Best Practices

1. Keep all dependencies updated
2. Use strong passwords and secrets
3. Enable HTTPS
4. Set appropriate file permissions
5. Regularly backup your database
6. Monitor server logs
7. Use a firewall (e.g., UFW)
8. Implement rate limiting
9. Use secure headers
10. Regular security audits

## 8. Performance Optimization
1. Enable caching where appropriate
2. Use CDN for static files
3. Optimize database queries
4. Implement pagination
5. Use database indexing
6. Use async tasks for long-running operations
7. Monitor server resources
8. Implement proper error handling

## 9. Deployment Automation

For automated deployments, consider using:

1. GitHub Actions or GitLab CI/CD
2. Ansible for configuration management
Example GitHub Actions workflow:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.KEY }}
          script: |
            cd /path/to/project
            git pull
            source venv/bin/activate
            pip install -r requirements.txt
            python manage.py migrate
            python manage.py collectstatic --noinput
            sudo systemctl restart gunicorn
```

## 10. Monitoring and Maintenance

1. Set up monitoring (e.g., Prometheus + Grafana)
2. Configure logging
3. Set up alerts
4. Regular backups
5. Performance monitoring
6. Security scanning
7. Regular updates
8. Database maintenance
10. Regular security audits 