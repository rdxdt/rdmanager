<div align="center">

# 🖥️ RDManager

**A self-hosted RustDesk "address book" for Free and Self-Hosted users**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![RustDesk](https://img.shields.io/badge/for-RustDesk-024EFF?logo=rustdesk&logoColor=white)](https://rustdesk.com/)

</div>

## 📖 About

RDManager is a simple ID/password database for RustDesk terminals, letting you organize them by customer organization.

- Customers and their terminals (CRUD)
- Multi-user access with login history
- Password recovery by e-mail
- hCaptcha on the login and recovery pages, plus IP banning after repeated failed attempts
- SQLite or MySQL/MariaDB backend

## 📂 Directory structure

```
rdmanager/
├── app.py                  # Entrypoint, exposes the Flask `app` to gunicorn
├── .env                    # Configuration (not versioned, see below)
├── requirements.txt        # Python dependencies
└── rdmanager/
    ├── __init__.py         # Creates the app, its extensions and registers the blueprints
    ├── config.py           # Reads the settings from .env
    ├── models.py           # SQLAlchemy models
    ├── main/               # Install, login/logout, password recovery and home page
    ├── user/               # User management
    ├── customer/           # Customers and their terminals
    ├── errors/             # Error handlers
    ├── static/             # css/, js/ and img/ files
    └── templates/          # Jinja templates, one subdirectory per module
        └── base.html       # Outer shell (navbar and footer) extended by every page
```

Each module (`main`, `user`, `customer`, `errors`) is a Flask blueprint with its routes in `routes.py` and its forms in `forms.py`.

## 🚀 Installation

### 1. Get the code and dependencies

```bash
git clone https://github.com/rdxdt/rdmanager.git
cd rdmanager
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 2. Configure the `.env` file

All settings are read from a `.env` file in the project root. Create it with the example below and adjust it to your environment:

```ini
# App mode: true = development (debug on, hCaptcha off), false = production
FLASK_DEBUG=false

SECRET_KEY=3f9c1e7a5b2d48c6a0e4f7b19d2c8e6a4b7f0d3c9e1a5b8f2d6c4e0a7b3f9d1c
DATABASE_URI=sqlite:////opt/rdmanager/db.sqlite3

# SMTP (used to send the password recovery codes)
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=rdmanager@example.com
MAIL_PASSWORD=SuperSecretMailPassword
MAIL_DEFAULT_SENDER=RDManager <rdmanager@example.com>

# hCaptcha
HCAPTCHA_SITE_KEY=10000000-ffff-ffff-ffff-000000000001
HCAPTCHA_SECRET_KEY=0x0000000000000000000000000000000000000000
```

> ⚠️ All values above are fictitious. Never commit your real `.env`; it is already listed in `.gitignore`.

| Variable | Description |
| --- | --- |
| `FLASK_DEBUG` | `true` for development, `false` (default) for production. hCaptcha is only enabled when debug is off. |
| `SECRET_KEY` | Signs the session cookies and CSRF tokens. Must be long, random and kept secret. |
| `DATABASE_URI` | SQLAlchemy connection string, see [Database](#database) below. |
| `MAIL_SERVER` / `MAIL_PORT` | SMTP server address and port (usually `587` for STARTTLS or `465` for SSL). |
| `MAIL_USE_TLS` / `MAIL_USE_SSL` | Enable STARTTLS or implicit SSL. Use only one of them. |
| `MAIL_USERNAME` / `MAIL_PASSWORD` | SMTP credentials. |
| `MAIL_DEFAULT_SENDER` | The `From` address of the recovery e-mails. |
| `HCAPTCHA_SITE_KEY` / `HCAPTCHA_SECRET_KEY` | Keys from your [hCaptcha dashboard](https://dashboard.hcaptcha.com/). |

#### Generating a secure `SECRET_KEY`

Generate a random value with Python's `secrets` module and paste it into `.env`:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Changing the key later logs out every user.

<a id="database"></a>
#### Database

**SQLite** – simplest option, no server required. Use four slashes followed by an absolute path:

```ini
DATABASE_URI=sqlite:////opt/rdmanager/db.sqlite3
```

The user running gunicorn must have write permission on the file **and** its directory. A relative path (`sqlite:///db.sqlite3`) is placed inside the Flask `instance/` folder.

**MySQL / MariaDB** – the `PyMySQL` driver is already in `requirements.txt`. Create the database and a dedicated user:

```sql
CREATE DATABASE rdmanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'rdmanager'@'localhost' IDENTIFIED BY 'ChangeMe!2024';
GRANT ALL PRIVILEGES ON rdmanager.* TO 'rdmanager'@'localhost';
FLUSH PRIVILEGES;
```

Then point `DATABASE_URI` to it:

```ini
DATABASE_URI=mysql+pymysql://rdmanager:ChangeMe%212024@localhost:3306/rdmanager?charset=utf8mb4
```

> Special characters in the password must be URL-encoded (e.g. `!` → `%21`, `@` → `%40`).

### 3. Create the service with systemd

Create a service unit to automatically start the gunicorn server that will serve the application.
For systemd distros, create the file `/etc/systemd/system/rdmanager.service`:

```ini
[Unit]
Description=RDManager Application
After=network.target

[Service]
WorkingDirectory=/path/to/rdmanager
User=REPLACE_WITH_YOUR_USER
ExecStart=/path/to/rdmanager/.venv/bin/gunicorn --bind=127.0.0.1:8000 -w 3 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Gunicorn listens only on `127.0.0.1` because nginx will be the one facing the internet. Now execute:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now rdmanager
sudo systemctl status rdmanager
```

### 4. Configure nginx as a reverse proxy

Install nginx and create `/etc/nginx/sites-available/rdmanager`:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name rdmanager.example.com;

    location /static/ {
        alias /path/to/rdmanager/rdmanager/static/;
        expires 7d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
    }
}
```

The `X-Forwarded-*` headers are required: the app reads the client IP from them to record logins and ban brute force attempts.

Enable the site and reload nginx:

```bash
sudo ln -s /etc/nginx/sites-available/rdmanager /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

HTTPS is intentionally left out of this file, certbot will add it in the next step.

### 5. Enable HTTPS with certbot

Make sure your domain's DNS points to the server and that ports `80` and `443` are open, then:

```bash
# Debian/Ubuntu
sudo apt install certbot python3-certbot-nginx

# Request the certificate and let certbot edit the nginx site
sudo certbot --nginx -d rdmanager.example.com
```

Certbot adds the `listen 443 ssl` block and the certificate paths to the server block, and can also set up the HTTP → HTTPS redirect. Certificates are renewed automatically by a systemd timer; you can check it with:

```bash
sudo systemctl list-timers | grep certbot
sudo certbot renew --dry-run
```

### 6. Run the installer

Open `https://rdmanager.example.com/install` in your browser and fill in the form with the first user's name, e-mail and password, then click **Install**.

The installer creates the database tables and the first user, then redirects you to the login page. Once the database exists the `/install` route is disabled and simply redirects to the home page, so it can't be used to take over an existing installation.

> To reinstall from scratch, delete the SQLite file (or drop the MySQL tables) and open `/install` again.

## 📝 Todo

- Test the application
- API for possible integration

## 📄 License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
