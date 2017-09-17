#!/bin/sh

systemctl stop {app_name}
cp {path_app_setup}/{systemd_conf_filename} {path_systemd_conf}
systemctl enable {app_name}
systemctl daemon-reload
systemctl start {app_name}
systemctl status {app_name}
