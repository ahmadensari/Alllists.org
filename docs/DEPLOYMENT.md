# Deployment guide (draft, untested)

Target: one Ubuntu server running Nginx, Gunicorn (as a systemd service) and PostgreSQL, with HTTPS.
Prerequisite: the backend must first be repaired so it starts (see "Current state" in README.md).
It must expose a WSGI entry point `wsgi:app` (an app factory is recommended).

None of these commands have been run against a real server. Test on a throwaway VM first.

## 1. System packages and firewall

```
sudo apt update && sudo apt install -y python3 python3-venv nginx postgresql
sudo ufw allow OpenSSH && sudo ufw allow 'Nginx Full' && sudo ufw enable
```

Only ports 22, 80 and 443 are open. The app port (5000) is never exposed.

## 2. Database

```
sudo -u postgres psql -c "CREATE USER alllists WITH PASSWORD '<generate-a-long-password>';"
sudo -u postgres psql -c "CREATE DATABASE alllists OWNER alllists;"
```

## 3. App code and virtual environment

```
sudo mkdir -p /srv/alllists && sudo chown $USER /srv/alllists
git clone <repo-url> /srv/alllists/app && cd /srv/alllists/app/backend
python3 -m venv /srv/alllists/venv
/srv/alllists/venv/bin/pip install -r requirements.txt gunicorn
```

## 4. Secrets (never committed)

Create `/etc/alllists.env`, readable only by the service user (`chmod 600`):

```
SECRET_KEY=<random 64+ chars>
DATABASE_URL=postgresql://alllists:<password>@localhost/alllists
```

## 5. Database migrations

Use Flask-Migrate, and make sure `Migrate(app, db)` is actually created in the app code:

```
export FLASK_APP=wsgi:app
/srv/alllists/venv/bin/flask db init      # first time only
/srv/alllists/venv/bin/flask db migrate -m "initial"
/srv/alllists/venv/bin/flask db upgrade
```

## 6. Gunicorn as a service

`/etc/systemd/system/alllists.service`:

```
[Unit]
Description=AllLists API
After=network.target postgresql.service

[Service]
User=www-data
WorkingDirectory=/srv/alllists/app/backend
EnvironmentFile=/etc/alllists.env
ExecStart=/srv/alllists/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload && sudo systemctl enable --now alllists
```

## 7. Nginx and HTTPS

`/etc/nginx/sites-available/alllists`:

```
server {
    listen 80;
    server_name alllists.org www.alllists.org;

    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        root /srv/alllists/app/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

```
sudo ln -s /etc/nginx/sites-available/alllists /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d alllists.org -d www.alllists.org
```

If the frontend becomes a server-rendered app (Next.js), Nginx proxies `/` to it instead of serving static files.

## 8. Check

```
curl -i https://alllists.org/api/
sudo journalctl -u alllists -n 50
```

## Updating

```
cd /srv/alllists/app && git pull
/srv/alllists/venv/bin/pip install -r backend/requirements.txt
FLASK_APP=wsgi:app /srv/alllists/venv/bin/flask db upgrade
sudo systemctl restart alllists
```
