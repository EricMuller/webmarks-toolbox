 #!/bin/sh

export APPS_DIR=/opt
export APPS_VAR_DIR=/var/opt

export  APP_NAME=oauth2-dev
export  DJANGO_PORT=8003

export  APP_HOSTNAME=oauth2-dev
export  HTTPD_PORT=80

export  USER=webdev

export  REPO=https://github.com/EricMuller/django-oauth2-server-sample.git
export  BRANCH=master

sudo ln -s  /usr/local/bin/python3 /usr/bin

sudo /opt/$APP_NAME/setup/httpd-uninstall.sh

sudo /opt/$APP_NAME/setup/systemd-uninstall.sh

sudo invoke install-django --app-name=$APP_NAME --template=default --path-apps=$APPS_DIR --path-apps-var=$APPS_VAR_DIR --owner=$USER --git-repo=$REPO --branch=$BRANCH --hostname=$APP_HOSTNAME --django-port=$DJANGO_PORT


sudo invoke install-setup --module=httpd --app-name=$APP_NAME --template=default --path-apps=$APPS_DIR --path-apps-var=$APPS_VAR_DIR  --owner=$USER --hostname=$APP_HOSTNAME --django-port=$DJANGO_PORT --http-port=$HTTPD_PORT


sudo invoke install-setup --module=systemd --app-name=$APP_NAME --template=default --path-apps=$APPS_DIR --path-apps-var=$APPS_VAR_DIR  --owner=$USER --hostname=$APP_HOSTNAME --django-port=$DJANGO_PORT --http-port=$HTTPD_PORT


sudo /opt/$APP_NAME/setup/httpd-install.sh

sudo /opt/$APP_NAME/setup/systemd-install.sh