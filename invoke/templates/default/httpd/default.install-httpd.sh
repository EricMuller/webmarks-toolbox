#/bin/sh
# sudo setenforce 0
chcon -R -t httpd_sys_content_t {path_static}
semanage port -m -t http_port_t -p tcp {http_port}
semanage port -m -t http_port_t -p tcp {django_port}

cp {path_app_setup}/{httpd_conf_filename}  {path_httpd_conf}

service httpd reload