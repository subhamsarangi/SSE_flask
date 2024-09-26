# Deploy to EC2
[LINK](https://medium.com/@lyle-okoth/how-to-deploy-a-production-grade-flask-application-to-an-aws-ec2-instance-using-github-actions-fabc8c16f8db)1

### make EC2 instance create key pair(login). Add security group rule with port 5000.

### Give permission to the downloaded key file
`chmod 400 ec2-key.pem`

## log into the ec2 instance
`ssh -i "ec2-key.pem" ubuntu@<your-instance-hostname>`


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
`ssh-keygen -y -f ec2-key.pem`

### copy the value into the authorized_keys file

### Now the new account can log into EC2 directly
`ssh -i “ec2.pem” lyle@<your-instance-hostname>`


# Set Up CICD pipeline


### install poetry

`curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"`

### clone the repo there

### install dependencies
`poetry install`

## Setup Gunicorn

### install gunicorn
poetry add gunicorn

### run server 
`poetry run gunicorn app:app --bind 0.0.0.0:8000`

### create server
`sudo nano /etc/systemd/system/SSE_flask.service`

### Create a Systemd Service
```bash
[Unit]
Description=Gunicorn instance to serve SSE_flask
After=network.target

[Service]
User=subadmin
Group=www-data
WorkingDirectory=/home/subadmin/SSE_flask
ExecStart=/home/subadmin/.local/bin/poetry run gunicorn --workers 3 --bind unix:/home/subadmin/SSE_flask/SSE_flask.sock app:app --log-file /home/subadmin/SSE_flask/gunicorn.log --access-logfile /home/subadmin/SSE_flask/gunicorn-access.log
Restart=always
RestartSec=10
Environment=PATH=/home/subadmin/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

[Install]
WantedBy=multi-user.target

```

### enable permission (if necessary)
`sudo chown subadmin:www-data /home/subadmin/SSE_flask/SSE_flask.sock`

### Start and Enable the Service

`sudo systemctl start SSE_flask`
`sudo systemctl enable SSE_flask`


## Configure Nginx


### create config
`sudo nano /etc/nginx/sites-available/SSE_flask`

```bash
server {
    listen 80;
    server_name 13.201.28.120;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/subadmin/SSE_flask/SSE_flask.sock;
    }

    error_log /var/log/nginx/SSE_flask_error.log;
    access_log /var/log/nginx/SSE_flask_access.log;
}

```
## enable permissions (if necessary)
`sudo chmod 660 /home/subadmin/SSE_flask/SSE_flask.sock`

### enable config
```bash
sudo ln -s /etc/nginx/sites-available/SSE_flask /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl reload nginx
```

### Nginx logs

`sudo tail -f /var/log/nginx/error.log`
`sudo tail -f /var/log/nginx/access.log`

### service logs
sudo journalctl -u SSE_flask.service
sudo journalctl -f -u SSE_flask.service

### gunicorn logs

tail -f /home/subadmin/SSE_flask/gunicorn.log
tail -f /home/subadmin/SSE_flask/gunicorn-access.log

## Set Up GitHub Actions
