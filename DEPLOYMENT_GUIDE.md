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
   mkdir -p /home/cysm/backend
   cd /home/cysm/backend
   git clone <your-backend-repo-url> cysm2024
   cd cysm2024
   ```

2. **Setup Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in `/home/cysm/backend/cysm2024/`:
   ```bash
   DJANGO_SECRET_KEY=your_secret_key
   DJANGO_DEBUG=False
   ALLOWED_HOSTS=cysmkd.org,api.cysmkd.org,YOUR_VPS_IP
   DATABASE_URL=postgres://cysm_user:your_secure_password@localhost:5432/cysm_db
   CORS_ALLOWED_ORIGINS=https://cysmkd.org,http://cysmkd.org
   CSRF_TRUSTED_ORIGINS=https://cysmkd.org,http://cysmkd.org
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
   VITE_API_BASE_URL=https://cysmkd.org npm run build
   ```

2. **Upload to VPS**:
   ```bash
   # From your local machine
   # Note: Uploading to /home/cysm/frontend directly
   scp -r dist root@YOUR_VPS_IP:/home/cysm/frontend
   ```

## 5. Nginx Configuration

Create a new Nginx site configuration:
```bash
sudo nano /etc/nginx/sites-available/cysm
```

Paste the following:
```nginx
server {
    listen 80;
    server_name cysmkd.org;

    # Frontend
    location / {
        root /home/cysm/frontend/dist;
        try_files $uri /index.html;
    }

    # Backend API & Admin
    location /api/ {
        include proxy_params;
        proxy_pass http://unix:/run/cysm.sock;
    }

    location /admin/ {
        include proxy_params;
        proxy_pass http://unix:/run/cysm.sock;
    }

    # Static files for Django (Admin, etc)
    location /static/ {
        alias /home/cysm/backend/cysm2024/staticfiles/;
    }

    location /media/ {
        alias /home/cysm/backend/cysm2024/media/;
    }
}
```

Link the config and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/cysm /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 6. Gunicorn Systemd Setup

Create a systemd service unit:
`sudo nano /etc/systemd/system/cysm.service`

```ini
[Unit]
Description=cysm gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/cysm/backend/cysm2024
ExecStart=/home/cysm/backend/cysm2024/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/cysm.sock \
          cysm.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start cysm
sudo systemctl enable cysm
```

## 7. SSL (HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d cysmkd.org
```
