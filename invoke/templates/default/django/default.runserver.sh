#!/bin/sh

source {path_env}/bin/activate

python {path_app}/manage.py runserver {hostname}:{django_port}
