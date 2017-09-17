#/bin/sh
# sudo setenforce 0
cp {path_app_setup}/{httpd_conf_filename}  {path_httpd_conf}

service httpd reload