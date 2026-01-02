# Deployment Guide: Django (DRF) + React to Contabo VPS

This guide outlines the steps to deploy your application to a Contabo VPS, transitioning from PythonAnywhere and Netlify.

## 1. Server Preparation

Connect to your VPS:
```bash
ssh root@YOUR_VPS_IP
```

Update system packages:
```bash
sudo apt update && sudo apt upgrade -y
```

Install dependencies:
```bash
sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib curl git
```

## 2. Database Setup (PostgreSQL)

Login to Postgres:
```bash
sudo -u postgres psql
```

Create database and user:
```sql
CREATE DATABASE cysm_db;
CREATE USER cysm_user WITH PASSWORD 'your_secure_password';
ALTER ROLE cysm_user SET client_encoding TO 'utf8';
ALTER ROLE cysm_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE cysm_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE cysm_db TO cysm_user;
\q
```

## 3. Backend Deployment (Django)

1. **Clone the backend repository**:
   ```bash
   mkdir -p ~/apps
   cd ~/apps
   git clone <your-backend-repo-url> cysm-backend
   cd cysm-backend
   ```

2. **Setup Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in `~/apps/cysm-backend/`:
   ```bash
   DJANGO_SECRET_KEY=your_secret_key
   DJANGO_DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,YOUR_VPS_IP
   DATABASE_URL=postgres://cysm_user:your_secure_password@localhost:5432/cysm_db
   CORS_ALLOWED_ORIGINS=https://yourdomain.com,http://yourdomain.com
   CSRF_TRUSTED_ORIGINS=https://yourdomain.com,http://yourdomain.com
   ```

4. **Prepare Django**:
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

5. **Test Gunicorn**:
   ```bash
   gunicorn --bind 0.0.0.0:8000 cysm.wsgi:application
   ```

## 4. Frontend Deployment (React)

1. **Build Locally**:
   On your local machine (where you are now):
   ```bash
   # In New-project-101 directory
   VITE_API_BASE_URL=https://api.yourdomain.com npm run build
   ```
   This creates a `dist` folder.

2. **Upload to VPS**:
   ```bash
   scp -r dist root@YOUR_VPS_IP:~/apps/cysm-frontend
   ```

## 5. Nginx Configuration

Create a new Nginx site configuration:
```bash
sudo nano /etc/nginx/sites-available/cysm
```

Paste the following (adjust paths and domains):
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /root/apps/cysm-frontend;
        try_files $uri /index.html;
    }

    # Backend API & Admin
    location /api/ {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }

    location /admin/ {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }

    # Static files for Django (Admin, etc)
    location /static/ {
        alias /root/apps/cysm-backend/staticfiles/;
    }

    location /media/ {
        alias /root/apps/cysm-backend/media/;
    }
}
```

## 6. Gunicorn Systemd Setup

Create a systemd socket unit: `sudo nano /etc/systemd/system/gunicorn.socket`
```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Create a systemd service unit: `sudo nano /etc/systemd/system/gunicorn.service`
```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/apps/cysm-backend
ExecStart=/root/apps/cysm-backend/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          cysm.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable Gunicorn:
```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

## 7. SSL (HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```
