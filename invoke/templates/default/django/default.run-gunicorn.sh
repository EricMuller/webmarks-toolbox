#!/bin/sh

NAME="{app_name}-server"                         	 # Name of the application
# DJANGODIR=`pwd`
DJANGODIR={path_app}

USER={owner}                                      	 # the user to run as
GROUP={owner}                                     	 # the group to run as
NUM_WORKERS=4                                        # how many worker processes should Gunicorn spawn
NUM_THREAD=4                                         # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=config.settings.development   # which settings file should Django use
DJANGO_WSGI_MODULE=config.wsgi                       # WSGI module name

echo "Starting $NAME as `whoami` "

# Activate the virtual environment
cd $DJANGODIR
source {path_env}/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export DJANGO_DEBUG=False
export DJANGO_LOG_LEVEL=WARN
export BIND={hostname}:{django_port}

echo $PYTHONPATH

# python /app/manage.py collectstatic --noinput
# gunicorn config.wsgi -w $NUM_WORKERS -b 0.0.0.0:5000 --chdir=/app
gunicorn -w $NUM_WORKERS --threads $NUM_THREAD -b $BIND --env DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE $DJANGO_WSGI_MODULE
