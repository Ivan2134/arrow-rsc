# Deploy to a VPS (Ubuntu, systemd, Nginx, PostgreSQL, Gunicorn, Certbot)

Target environment:
- Ubuntu 22.04 LTS (or newer)
- Python 3.10+
- PostgreSQL, Nginx, Certbot, systemd
- Gunicorn as the WSGI server

1) Prepare the server
- sudo apt update && sudo apt upgrade -y
- sudo apt install -y python3-pip python3-venv git nginx postgresql postgresql-contrib certbot python3-certbot-nginx

(Optional) UFW:
- sudo ufw allow OpenSSH
- sudo ufw allow 'Nginx Full'
- sudo ufw enable

1.1) User/group and permissions (recommended)
Create a system user for the app, a shared group with Nginx, and set permissions on /srv/arrow-rsc:
- sudo addgroup --system webdev
- sudo adduser --system --group --home /srv/arrow-rsc --no-create-home arrow
- sudo usermod -aG webdev arrow
- sudo usermod -aG webdev www-data
- sudo mkdir -p /srv/arrow-rsc
- sudo chown -R arrow:webdev /srv/arrow-rsc
- sudo find /srv/arrow-rsc -type d -exec chmod 2775 {} +
- sudo find /srv/arrow-rsc -type f -exec chmod 664 {} +

Notes:
- The setgid bit (2 in 2775) ensures new files/dirs inherit the webdev group.
- Deploy as user arrow or any user in the webdev group.

2) Create the PostgreSQL DB and user
- sudo -u postgres psql
  CREATE USER arrow WITH PASSWORD 'strong-password';
  CREATE DATABASE arrow_rsc OWNER arrow;
  ALTER ROLE arrow SET client_encoding TO 'utf8';
  ALTER ROLE arrow SET default_transaction_isolation TO 'read committed';
  ALTER ROLE arrow SET timezone TO 'UTC';
  \q

3) Fetch and deploy the code
- sudo mkdir -p /srv/arrow-rsc
- git clone <YOUR_REPO_URL> /srv/arrow-rsc
- cd /srv/arrow-rsc
- python3 -m venv .venv
- source .venv/bin/activate
- pip install --upgrade pip
- pip install -r requirements.txt

4) Environment configuration (.env)
- Copy from the provided template and fill values:
  cp /srv/arrow-rsc/.env_template /srv/arrow-rsc/.env
- Example variables:
SECRET_KEY=change-me
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=arrow_rsc
DB_USER=arrow
DB_PASSWORD=strong-password
DB_HOST=127.0.0.1
DB_PORT=5432
SMTP_LOGIN=example@gmail.com
SMTP_PASSWORD=app-password
FORM_SEND_TYPE=mail
FORM_SEND_MAIL=admin@example.com
# TELEGRAM_TOKEN=...
# TELEGRAM_CHAT_ID=...
# PARTNER_CHATID_TG=...
# Optionally:
# ALLOWED_HOSTS=example.com,www.example.com
# CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com

5) Prepare the application
- source /srv/arrow-rsc/.venv/bin/activate
- cd /srv/arrow-rsc
- python manage.py migrate
- python manage.py collectstatic --noinput
- (optional) python manage.py createsuperuser

6) Create a systemd service for Gunicorn
Create /etc/systemd/system/arrow-rsc.service:
[Unit]
Description=Gunicorn service for arrow-rsc
After=network.target

[Service]
User=arrow
Group=webdev
WorkingDirectory=/srv/arrow-rsc
Environment="PYTHONUNBUFFERED=1"
ExecStart=/srv/arrow-rsc/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8001 arrow_rsc.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target

Notes:
- Adjust User/Group if needed; the service user must own /srv/arrow-rsc and www-data should be in the webdev group.
- .env is auto-loaded because settings.py uses load_dotenv() and WorkingDirectory points to the project root.

Enable the service:
- sudo systemctl daemon-reload
- sudo systemctl enable --now arrow-rsc
- sudo systemctl status arrow-rsc

7) Configure Nginx
Create /etc/nginx/sites-available/arrow-rsc:
server {
    listen 80;
    server_name example.com www.example.com;

    client_max_body_size 20m;

    location /static/ {
        alias /srv/arrow-rsc/staticfiles/;
        expires 30d;
        add_header Cache-Control "public";
    }

    location /media/ {
        alias /srv/arrow-rsc/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

Enable the site and reload Nginx:
- sudo ln -s /etc/nginx/sites-available/arrow-rsc /etc/nginx/sites-enabled/arrow-rsc
- sudo nginx -t
- sudo systemctl reload nginx

8) SSL certificates (Let’s Encrypt)
- sudo certbot --nginx -d example.com -d www.example.com --redirect
- Check auto-renewal: sudo systemctl status certbot.timer

9) Updates (step-by-step, zero-downtime)
- cd /srv/arrow-rsc
- git pull
- source .venv/bin/activate
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py collectstatic --noinput
- sudo systemctl reload arrow-rsc   # graceful; fallback: sudo systemctl restart arrow-rsc

Done. The site is served at https://example.com via Nginx -> Gunicorn -> Django -> PostgreSQL.
