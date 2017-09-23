#!/bin/sh

export APPS_DIR=/opt
export APPS_VAR_DIR=/var/opt

export  APP_NAME=bookmarks-dev
export  DJANGO_PORT=8002

export  APP_HOSTNAME=bookmarks-dev
export  HTTPD_PORT=80

export  USER=webdev

sudo ln -s  /usr/local/bin/python3 /usr/bin

sudo /opt/$APP_NAME/setup/httpd-uninstall.sh

sudo /opt/$APP_NAME/setup/systemd-uninstall.sh

sudo invoke install-django --app-name=$APP_NAME --template=default --path-apps=$APPS_DIR --path-apps-var=$APPS_VAR_DIR --owner=$USER --git-repo=https://github.com/EricMuller/mywebmarks-backend.git --branch=refactor --hostname=$APP_HOSTNAME --django-port=$DJANGO_PORT


sudo invoke install-setup --module=httpd --app-name=$APP_NAME --template=default --path-apps=$APPS_DIR --path-apps-var=$APPS_VAR_DIR  --owner=$USER --hostname=$APP_HOSTNAME --django-port=$DJANGO_PORT --http-port=$HTTPD_PORT


sudo invoke install-setup --module=systemd --app-name=$APP_NAME --template=default --path-apps=$APPS_DIR --path-apps-var=$APPS_VAR_DIR  --owner=$USER --hostname=$APP_HOSTNAME --django-port=$DJANGO_PORT --http-port=$HTTPD_PORT


sudo /opt/$APP_NAME/setup/httpd-install.sh

sudo /opt/$APP_NAME/setup/systemd-install.sh
