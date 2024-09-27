# Deploy to EC2

### make EC2 instance create key pair(login).


### Add security group rules

| Type  | Port range   |
|------------|------------|
| SSH | 22 |
| HTTP | 80 |
| Custom TCP | 5000 |
          


### Give permission to the downloaded key file
`chmod 400 <KEY_NAME>.pem`

## log into the EC2 instance
`ssh -i "<KEY_NAME>.pem" <USERNAME>@<INSTANCE_PUBLIC_DNS>`


### update ubuntu and install pip
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip -y
```

### create a new user
`sudo adduser subadmin`

### give them admin privileges
`sudo usermod -aG sudo subadmin`

### log into the newly created account
`su — subadmin`

### Create a .ssh directory in the subadmin home directory
`mkdir .ssh`

### Change its permissions (only the owner can read, write, or open the directory) 
`chmod 700 .ssh`

### Create a file named authorized_keys in the .ssh directory
`touch .ssh/authorized_keys`

### change its permissions to 600 (only the owner can read or write to the file)
`chmod 600 .ssh/authorized_keys`

### Open the authorized_keys file
`sudo nano .ssh/authorized_keys`

### open another terminal and generate a public key for the newly created account
`ssh-keygen -y -f <KEY_NAME>.pem`

### copy the value into the authorized_keys file

### Now the new account can log into EC2 directly
`ssh -i “ec2.pem” lyle@<your-instance-hostname>`

## Setup the Server

### install poetry
`curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"`

### clone the repo there

### install dependencies
`poetry install`

### install gunicorn
poetry add gunicorn

### run server 
`poetry run gunicorn app:app --bind 0.0.0.0:5000`

### Get env path
`poetry env info --path`

### Create a Systemd Service
`sudo nano /etc/systemd/system/sse_flask.service`

```ini
[Unit]
Description=Gunicorn instance to serve SSE_flask
After=network.target

[Service]
User=subadmin
Group=www-data
WorkingDirectory=/home/subadmin/SSE_flask
Environment=PATH=/home/subadmin/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=/home/subadmin/.local/bin/poetry run gunicorn --access-logfile - --workers 3 --bind 0.0.0.0:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

```

### Start and Enable the Service
```bash
sudo systemctl daemon-reload
sudo systemctl start sse_flask
sudo systemctl enable sse_flask
```

## Configure NGINX
### create config
`sudo nano /etc/nginx/sites-available/sse_flask`

```nginx
server {
    listen 80;
    server_name <SERVER_IP>;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    error_log /var/log/nginx/sse_flask_error.log;
    access_log /var/log/nginx/sse_flask_access.log;
}
```

### enable config
`sudo ln -s /etc/nginx/sites-available/sse_flask /etc/nginx/sites-enabled/`

### test
`sudo nginx -t`

### restart or reload
```bash
sudo systemctl restart nginx
sudo systemctl reload nginx
```

## check logs
### Nginx logs
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### service logs
```bash
sudo journalctl -u sse_flask.service
sudo journalctl -f -u sse_flask.service
```

# Set Up GitHub Actions (CI/CD pipeline)
