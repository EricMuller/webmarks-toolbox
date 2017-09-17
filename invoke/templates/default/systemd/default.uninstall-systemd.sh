#!/bin/sh
systemctl stop {app_name}
rm -rf {path_systemd_conf}/{systemd_conf_filename} 
systemctl daemon-reload

