 

 # webmarks-backend

 #  installation

 sudo pip install -e git+https://github.com/pyinvoke/invoke#egg=invoke


 # requirement

 create hostname bookmarks-dev in /etc/hosts

 # deploy


1. django application

sudo invoke install-django --app-name=bookmarks-dev --template=default --path-apps=/opt --path-apps-var=/var/opt --owner=webdev --git-repo=https://github.com/EricMuller/mywebmarks-backend.git --branch=refactor --hostname=bookmarks-dev --django-port=8002

2. apache httpd

sudo invoke install-setup --module=httpd --app-name=bookmarks-dev --template=default --path-apps=/opt --path-apps-var=/var/opt  --owner=webdev --hostname=bookmarks-dev --django-port=8002 --http-port=80

3. apache systemd

sudo invoke install-setup --module=systemd --app-name=bookmarks-dev --template=default --path-apps=/opt --path-apps-var=/var/opt  --owner=webdev --hostname=bookmarks-dev --django-port=8002 --http-port=80


