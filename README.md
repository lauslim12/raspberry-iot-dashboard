# Raspberry IoT Dashboard

Your very own IoT-powered website using Raspberry Pi computers with Flask, Redis, Nginx, S3, and many more. This is a 'dashboard' or a 'homepage' that will be run when you try to connect to your Raspberry Pi. The purpose of this website is to keep track of your IoT projects and/or favorite links. This application is similar to a bookmark application.

## Introduction

This is more like a repository / learning note to teach myself how to deploy Flask application with Nginx, Redis, Cerbot, and Minio manually in a Raspberry Pi instance with Raspbian OS (Debian-based). Actually, that is the secondary reason. The primary reason is because I want to create a simple website to keep track of IoT devices and services that I have available in my house, so I don't get lost.

## Features

- Powerful nginx configuration to serve the Gunicorn instance.
- Fast CRUD operations using Redis NoSQL database.
- Easy on the eyes design, custom-made, and responsive.
- Implements S3-compatible interface with Minio (separate from the application).
- Easy to read, implements application factories and blueprints for Flask.

## Requirements

- Raspberry Pi 4
- Raspbian OS
- Python 3.9 and up
- Poetry

After getting a Raspberry Pi 4, you also need the following, but we will install them together in this documentation.

- Certbot (optional)
- Minio
- Nginx
- Redis

## Installation

The installation is a bit long. We are going to split it to several parts. I am going to assume that you will setup the application in the `$HOME` directory.

### Preparations

- Raspberry Pi usually does not come with the latest Python version. But, we are going to need it in this project. Because of that, please install Python by building from the source code.
- You also need [Poetry](https://python-poetry.org/) for the package manager. You can install it the recommended way by copy-pasting this into your terminal.

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

- But I recommend you to simply use Python virtual environment and install Poetry there. Your choice. If you are going with this approach, then you're going to need these in order to compile because Raspbian cannot compile Poetry by itself, it will fail when building `cryptography`:

```bash
sudo apt install build-essential libssl-dev libffi-dev python3-dev cargo
```

- In the further steps (especially in the configurations), please don't forget to replace your application path, Linux username, virtual environment paths, etcetera to prevent bugs.

### Setup Application

- First off, we clone the repository.

```bash
git clone https://github.com/lauslim12/raspberry-iot-dashboard.git
```

- Then, we install the dependencies in a new virtual environment.

```bash
cd $HOME/raspberry-iot-dashboard

# if you are using venv
python3 -m venv .venv
source .venv/bin/activate
pip3 install poetry
poetry install

# if you are using poetry
poetry shell
poetry install
```

- Prepare your environment variables and fill it according to the example. If you're using defaults, I don't think you need to change the environment variable, but you have to include it (`.env` file) in the project.

```bash
mv .env.example .env
nano .env
```

- Take note of the path to your virtual environment, then exit the shell.

```bash
# take note of the output of 'pwd', if you are using python venv
cd .venv/bin
pwd
deactivate

# take note of the output of 'poetry env info --path', if you are using poetry
poetry env info --path
exit
```

### Setup Redis

- Installing Redis is pretty simple, even using `apt` is possible.

```bash
sudo apt update
sudo apt install redis-server
```

- Allow Redis to use `systemd`, so it can be run everytime the Raspberry starts.

```bash
sudo nano /etc/redis/redis.conf
```

- You have to change the default `supervised no` directive to `supervised systemd`. Then, restart and check the status of your Redis.

```bash
sudo systemctl restart redis
sudo systemctl status redis
```

- Enable automatic boot!

```bash
sudo systemctl enable redis
```

- Test your Redis!

```bash
ping
set hello world
get hello
del hello
keys *
```

### Setup Gunicorn

We are going to set up our Gunicorn instance to be used with nginx. You can (and should) replace the username (in this repo it is `miyuki`), the virtual environment directory (adjust it to your created virtual environment beforehand, remember the `poetry env info --path` or `pwd` result?), and optionally the `raspberry-iot-dashboard` name.

The idea behind these commands is that we are going to have nginx listen to the socket that is exposed by the Gunicorn instance.

- Edit or create the service with `sudo nano /etc/systemd/system/raspberry-iot-dashboard.service`.

```bash
[Unit]
Description=Gunicorn instance to serve Raspberry IoT Dashboard
After=network.target

[Service]
User=miyuki
Group=www-data
WorkingDirectory=/home/miyuki/raspberry-iot-dashboard
Environment="PATH=/home/miyuki/raspberry-iot-dashboard/.venv/bin"
ExecStart=/home/miyuki/raspberry-iot-dashboard/.venv/bin/gunicorn --workers 4 --bind unix:raspberry-iot-dashboard.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

- Start our service.

```bash
sudo systemctl start raspberry-iot-dashboard
sudo systemctl status raspberry-iot-dashboard
```

- We are going to ensure it starts on boot time.

```bash
sudo systemctl enable raspberry-iot-dashboard
```

Your Gunicorn has now started successfully!

### Setup Nginx

Then, we are going to reverse proxy to that socket with these nginx commands.

- First off, install nginx.

```bash
sudo apt update
sudo apt install nginx
```

- Check if nginx has been installed successfully.

```bash
hostname -I               # you will get an IP address
curl http://192.168.1.6   # test your connection according to the IP
```

- Even though nginx came with default settings, its always better for us to improve upon the given settings. Here is my nginx setting. You can change this by using `sudo nano /etc/nginx/nginx.conf`.

```bash
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
  worker_connections 768;
  multi_accept on; # accept multi_accept to accept all new connections at a time
}

http {
  ##
  # Basic Settings
  ##
  sendfile on;
  tcp_nopush on;
  tcp_nodelay on;
  keepalive_timeout 65;
  types_hash_max_size 2048;
  server_tokens off; # remove nginx version number

  # server_names_hash_bucket_size 64;
  # server_name_in_redirect off;

  include /etc/nginx/mime.types;
  default_type application/octet-stream;

  ##
  # SSL Settings
  ##
  ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
  ssl_prefer_server_ciphers on;

  ##
  # Logging Settings
  ##
  access_log /var/log/nginx/access.log;
  error_log /var/log/nginx/error.log;

  ##
  # Gzip Settings
  ##
  gzip on;
  gzip_vary on; # cache both the gzipped and regular version of a resource
  gzip_proxied any; # ensures all proxied request responses are gzipped
  gzip_comp_level 5; # compress up to level 5 for performance

  # gzip_buffers 16 8k;

  gzip_http_version 1.1; # enable compression for both HTTP 1.0/1.1
  gzip_min_length 256; # files smaller than 256 bytes would not be gzipped to prevent overhead
  gzip_types
    application/atom+xml
    application/javascript
    application/json
    application/rss+xml
    application/vnd.ms-fontobject
    application/x-font-ttf
    application/x-web-app-manifest+json
    application/xhtml+xml
    application/xml
    font/opentype
    image/svg+xml
    image/x-icon
    text/css
    text/plain
    text/x-component
    text/javascript
    text/xml;

  ##
  # Virtual Host Configs
  ##
  include /etc/nginx/conf.d/*.conf;
  include /etc/nginx/sites-enabled/*;
}

# mail {
#       # See sample authentication script at:
#       # http://wiki.nginx.org/ImapAuthenticateWithApachePhpScript

#       # auth_http localhost/auth.php;
#       # pop3_capabilities "TOP" "USER";
#       # imap_capabilities "IMAP4rev1" "UIDPLUS";

#       server {
#               listen     localhost:110;
#               protocol   pop3;
#               proxy      on;
#       }

#       server {
#               listen     localhost:143;
#               protocol   imap;
#               proxy      on;
#       }
# }
```

- Then, we will create an nginx configuration by using `sudo nano /etc/nginx/sites-available/default`. You can replace the `default` or you can create a new configuration, let's say `/etc/nginx/sites-available/raspberry-iot-dashboard` and symlink it.

```bash
upstream miyuki_server {
  server unix:/home/miyuki/raspberry-iot-dashboard/raspberry-iot-dashboard.sock;
}

server {
  # Server metadata.
  listen 80 default_server;
  listen [::]:80;
  # server_name my-domain.com www.my-domain.com -- keep this commented

  # Add custom headers.
  add_header X-Raspberry-IoT-Dashboard 1.0.0;
  add_header X-Raspberry-IoT-Dashboard-Id Miyuki;

  # Main entrypoint.
  location / {
    # Include proxy parameters and passes.
    include proxy_params;
    proxy_pass http://miyuki_server;

    # Turn off proxy buffering for performance.
    proxy_redirect off;
    proxy_buffering off;

    # Do not change these.
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

- Symlink the nginx configuration. You don't need to do this if you are using the `default` configuration.

```bash
sudo ln -s /etc/nginx/sites-available/raspberry-iot-dashboard /etc/nginx/sites-enabled
```

- Test for syntax errors and restart the nginx instance!

```bash
sudo nginx -t
sudo systemctl restart nginx
```

- Don't forget to have it run on boot.

```bash
sudo systemctl enable nginx
```

You should now be able to connect to your Raspberry IoT Dashboard by opening your web browser and typing the local IP Address of your Pi. Ensure that both your Pi and your device are connected to the same network/Wi-Fi.

### Setup Cerbot and HTTPS

Please note that this will not work if you only deployed this in your local network. Certbot and Let's Encrypt will only work if you have a domain name and exposed your Raspberry Pi port to the worldwide internet. This is something that you should think about because this is a security risk. I recommend you to use Amazon EC2 if you want to try playing with these commands.

We will use Let's Encrypt for HTTPS.

- Add Certbot repository for Raspberry Pi, and install Certbot for Python.

```bash
sudo apt install certbot python-certbot-nginx
```

- Configure Certbot.

```bash
sudo certbot --nginx
```

The nginx SSL configuration (`default`) will be done automatically by Let's Encrypt, but if you want, you can use my settings below to achieve the same effect. Please consider the automatic renewals though.

### Alternative: Using `mkcert` for HTTPS

There is a package called `mkcert` from [FiloSottile](https://github.com/FiloSottile/mkcert) that allows you to use HTTPS even in local networks. **This will only work on that Raspberry Pi instance though. You will get invalid certification error if you try to access from other devices**.

- To install it is very simple.

```bash
# keep this updated!
cd $HOME
sudo apt install libnss3-tools
wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-arm
chmod +x mkcert-v1.4.3-linux-arm
./mkcert-v1.4.3-linux-arm -install
./mkcert-v1.4.3-linux-arm -key-file key.pem -cert-file cert.pem 192.168.1.6 localhost 127.0.0.1 ::1
```

- Then, we'll set up nginx with SSL with the certificate. Move the files first.

```bash
sudo mkdir /etc/mkcert
cd /etc/mkcert
sudo mv $HOME/key.pem /etc/mkcert
sudo mv $HOME/cert.pem /etc/mkcert
```

- And then, let's reconfigure our nginx settings. Perform `sudo nano /etc/nginx/sites-available/default` or any other file that you use to edit the configuration earlier.

```bash
upstream miyuki_server {
  server unix:/home/miyuki/raspberry-iot-dashboard/raspberry-iot-dashboard.sock;
}

server {
  # Server metadata.
  listen 80 default_server;
  listen [::]:80;
  # server_name my-domain.com www.my-domain.com -- keep this commented

  # Main entrypoint.
  location / {
    return 301 https://$host$request_uri;
  }
}

server {
  # Server metadata.
  listen 443 ssl;

  # SSL certificates.
  ssl on;
  ssl_certificate /etc/mkcert/cert.pem;
  ssl_certificate_key /etc/mkcert/key.pem;

  # Add custom headers.
  add_header X-Raspberry-IoT-Dashboard 1.0.0;
  add_header X-Raspberry-IoT-Dashboard-Id Miyuki-SSL;

  # Always route to HTTPS on subsequent requests.
  add_header Strict-Transport-Security "max-age=31536000";

  # Main entrypoint.
  location / {
    # Include proxy parameters and passes.
    include proxy_params;
    proxy_pass https://miyuki_server;

    # Turn off proxy buffering for performance.
    proxy_redirect off;
    proxy_buffering off;

    # Do not change these.
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

You can now access your server in HTTPS, but only in the Raspberry Pi.

### Setup Minio

You can setup your Minio server in order to make your Pi a walking Cloud Storage that is S3 compatible.

- Installation procedures (remember Raspberry Pi is `arm`, not `arm-64`):

```bash
cd $HOME/Minio
wget https://dl.minio.io/server/minio/release/linux-arm/minio
chmod +x minio
```

- Running Minio:

```bash
./minio server ./minio-data
```

- Of course we can let it run in the background. First, press `CTRL+Z` or `Command+Z`, and then:

```bash
bg                        # resume in background
jobs                      # find out your job number here
disown %<YOUR_JOB_NUMBER> # keep the '%' char, this is to disown the process so it doesn't exit when you logout
```

And it's done!

## Updates

Some notes to keep in mind:

- If you want to update dependencies, use `poetry update`.
- If you have just updated the website, restart service by using `sudo systemctl restart raspberry-iot-dashboard`.

## Cleaning Up

To clear up any build artifacts during development or deployment, use this command.

```bash
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
```

## License

This application is licensed under MIT License. Feel free to check `LICENSE` file for more information.

## Credits

- [Iconixar](https://www.flaticon.com/authors/iconixar) for providing the favicon.

## References

Here are the references that I use to make this project.

- [Installing Redis on Raspberry Pi](https://lindevs.com/install-redis-from-source-code-on-raspberry-pi/)
- [Configurations for Nginx](https://www.e-tinkers.com/2018/08/how-to-properly-host-flask-application-with-nginx-and-guincorn/)
- [Gunicorn Recommended Deploying Guidelines](https://docs.gunicorn.org/en/stable/deploy.html)
- [Build Private Cloud on Raspberry Pi with Minio](https://www.linkedin.com/pulse/build-your-own-private-cloud-home-raspberry-pi-minio-huerta-arias/)
- [DigitalOcean - Deploy Flask with Gunicorn and Nginx](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04)
- [DigitalOcean - How to Setup Nginx](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04)
- [DigitalOcean - How to Setup Redis](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04)
- [DigitalOcean - How to Setup Minio](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-object-storage-server-using-minio-on-ubuntu-18-04)
