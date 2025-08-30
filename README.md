# arrow-rsc

Django project (Django 4.2) with DRF, TinyMCE, modeltranslation, gsheets, imagekit.

Technologies:
- Python 3.10+
- Django 4.2
- Django REST framework
- TinyMCE, modeltranslation, imagekit, gsheets

Requirements:
- Python 3.10+ and pip
- virtualenv (python3 -m venv .venv)
- Optional for local dev: PostgreSQL (otherwise SQLite is used by default)

Quick start (local):
1) Clone the repository and install dependencies
   - python -m venv .venv
   - source .venv/bin/activate  (Windows: .venv\Scripts\activate)
   - pip install -r requirements.txt
2) Create your environment file from the template
   - cp .env_template .env
   - edit .env and set your values (SECRET_KEY, DEBUG, email, etc.)
3) Initialize the DB and run the server
   - python manage.py migrate
   - python manage.py collectstatic --noinput  (if needed)
   - python manage.py runserver

Notes about .env:
- SECRET_KEY=change-me (generate a strong key for production)
- DEBUG=True for local; set to False in production
- For PostgreSQL in production (or local if you prefer):
  # DB_ENGINE=django.db.backends.postgresql
  # DB_NAME=arrow_rsc
  # DB_USER=arrow
  # DB_PASSWORD=strong-password
  # DB_HOST=127.0.0.1
  # DB_PORT=5432
- Email:
  SMTP_LOGIN=example@gmail.com
  SMTP_PASSWORD=app-password
- Telegram:
  TELEGRAM_TOKEN=...
  TELEGRAM_CHAT_ID=...
  PARTNER_CHATID_TG=...
- Forms:
  FORM_SEND_TYPE=mail
  FORM_SEND_MAIL=admin@example.com

Useful commands:
- Create superuser: python manage.py createsuperuser
- Migrations: python manage.py makemigrations && python manage.py migrate
- Collect static: python manage.py collectstatic --noinput
- Compile messages: python manage.py compilemessages

Deployment:
- See the deployment guide: [DEPLOYMENT.md](./DEPLOYMENT.md) (Ubuntu, systemd, Nginx, PostgreSQL, Gunicorn, Certbot).

