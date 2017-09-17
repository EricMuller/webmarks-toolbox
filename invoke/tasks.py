import logging
import os
import sys
from invoke.exceptions import UnexpectedExit
from invoke import task
from os.path import dirname, join


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

base_dir = dirname(os.path.abspath(__file__))
# print os.environ['HOME']
DEFAULT_PYTHON_ENV_DIRNAME = 'env'


def run(ctx):
    ctx.run("python setup.py sdist register upload")


def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


# default_git_repo = 'https://github.com/EricMuller/django-oauth2-server-sample.git'
default_git_repo = 'https://github.com/EricMuller/mywebmarks-backend.git'


class AppRunner():

    def __init__(self, runner):
        self.runner = runner

    def rmdir(self, path):
        self.runner.run('rm -rf {0}'.format(path))

    def mkdir(self, path, raise_error=True):
        try:
            self.runner.run('mkdir {0}'.format(
                path))
        except UnexpectedExit:
            # print("Unexpected error:", sys.exc_info())
            if raise_error:
                raise

    def mk_app_dir(self, path_dir, name):

        path = join(path_dir, name)
        try:
            self.runner.run(' mkdir {0} '.format(path))
        except UnexpectedExit:
            print("Unexpected error:", sys.exc_info())

        return path

    def git_clone(self, path_app, git_repo, branch):

        cmd = ''
        if branch is not None:
            cmd = 'git clone -b {0} {1} {2} '.format(
                branch, git_repo, path_app)
        else:
            logger.warn('Cloning HEAD !!')
            cmd = 'git clone {0} {1} '.format(
                git_repo, path_app)

        return self.runner.run(cmd)

    def create_env(self, path_env, path_app):
        self.runner.run('python3 -m venv {0} '.format(path_env))
        self.runner.run('source {0}/bin/activate'.format(path_env))

    def pip(self, path_env, cmd):
        self.runner.run(
            '{0}/bin/pip  {1}'.format(path_env, cmd))

    def install_app_requirement(self, path_env, path_app, filename):

        path_requirements = join(path_app, filename)
        cmd = '{0}/bin/pip  install -r {1}'.format(path_env,
                                                   path_requirements)
        self.runner.run(cmd)

    def python(self, path_env, cmd):

        self.runner.run(
            '{0}/bin/python {1} '.format(path_env, cmd))

    def django_manage(self, path_env, path_app, cmd):
        path_manage = join(path_app, 'manage.py')
        self.runner.run(
            '{0}/bin/python {1}  {2} '.format(path_env, path_manage, cmd))

    def django_make_migrations(self, path_env, path_app, file_name):
        file_name = join(path_app, file_name)
        with open(file_name) as f:
            for appli in f:
                self.django_manage(path_env, path_app,
                                   'makemigrations {0} '.format(appli))

    def template_copy(self, src_file_name, dest_file_name, **kwargs):
        try:
            buffer = open(src_file_name, 'rU').read()
            f = open(dest_file_name, 'w')
            f.write(buffer.format(**kwargs))
            f.close()

        except:
            print("Unexpected error:", sys.exc_info())
            pass

    def copy_template_django(self, app_name, template, env,
                             path_app, path_app_var, path_app_logs,
                             path_static, path_env, path_app_bin,
                             hostname, django_port,
                             owner):

        django_dir = os.path.join(os.path.join(base_dir, 'templates', template,
                                               'django'))

        var = {'hostname': hostname, 'path_app_var': path_app_var,
               'path_app_logs': path_app_logs, 'path_static': path_static,
               'path_env': path_env, 'path_app': path_app,
               'django_port': django_port,
               'app_name': app_name, 'owner': owner}

        src_file_name = join(django_dir, env + '.local.env')
        dest_dir = join(path_app, 'config/settings/')
        dest_file_name = join(dest_dir, 'local.env')

        self.template_copy(src_file_name, dest_file_name, **var)

        src_file_name = join(django_dir, env + '.runserver.sh')
        dest_file_name = join(path_app_bin, 'runserver.sh')

        self.template_copy(src_file_name, dest_file_name, **var)

        src_file_name = join(django_dir, env + '.run-gunicorn.sh')
        dest_file_name = join(path_app_bin, 'run-gunicorn.sh')

        self.template_copy(src_file_name, dest_file_name, **var)

    def copy_template_module(self, app_name, template, env,
                             path_app, path_app_var, path_app_logs,
                             path_static, path_env, path_app_bin,
                             path_app_setup, path_os_conf,
                             hostname, django_port, http_port,
                             owner, module, extension):

        src_file_name = join(
            base_dir, 'templates',
            template, module, env + '.' + module + extension)

        conf_filename = app_name + extension
        path_setup_conf = join(path_app_setup, conf_filename)

        var = {'hostname': hostname, 'path_app_var': path_app_var,
               'path_app_logs': path_app_logs, 'path_static': path_static,
               'path_env': path_env, 'path_app': path_app,
               'django_port': django_port, 'http_port': http_port,
               'app_name': app_name, 'owner': owner,
               'path_app_setup': path_app_setup,
               module + '_conf_filename': conf_filename,
               'path_' + module + '_conf': path_os_conf}

        self.template_copy(src_file_name, path_setup_conf, **var)

        src_file_name = join(
            base_dir, 'templates', template,
            module, env + '.install-' + module + '.sh')
        dest_file_name = join(path_app_setup, module + '-install.sh')

        self.template_copy(src_file_name, dest_file_name, **var)

        src_file_name = join(
            base_dir, 'templates', template,
            module, env + '.uninstall-' + module + '.sh')
        dest_file_name = join(path_app_setup, module + '-uninstall.sh')

        self.template_copy(src_file_name, dest_file_name, **var)

    def chown(self, path, user):
        self.runner.run('chown {0} -R {1}'.format(user, path))

    def run(self, cmd):
        self.runner.run(cmd)

    def install_app_os_dependencies(self, path_app, file_name):
        file_name = join(path_app, file_name)
        with open(file_name) as f:
            for line in f:
                self.runner.run('yum install -y {0}'.format(line.strip()))


class InvokeRunner(object):

    def __init__(self, ctx):
        self.ctx = ctx

    def run(self, cmd, warn=True):

        logger.info(cmd)
        result = self.ctx.run(cmd, hide=False)

        lines = result.stdout.splitlines()
        if len(lines) > 1:
            logger.info('  ' + lines[-1])

        return result


def default_path(path_apps, path_apps_var, path_static, app_name):

    if path_apps is None:
        path_apps = join(base_dir, 'opt')

    if path_apps_var is None:
        path_apps_var = join(base_dir, 'var')

    if path_static is None:
        path_static = join(path_apps_var, app_name, 'static')

    path_app = join(base_dir, path_apps, app_name)
    path_app_var = join(path_apps_var, app_name)
    path_app_bin = join(path_app, 'bin')
    return path_apps, path_apps_var, path_static, path_app, path_app_var,\
        path_app_bin


@task
def install_setup(ctx, app_name, template,
                  hostname, http_port, django_port, module,
                  env='default',
                  path_apps=None, path_apps_var=None, path_static=None,
                  show=False, branch=None,
                  owner=None):

    path_apps, path_apps_var, path_static, path_app, path_app_var,\
        path_app_bin \
        = default_path(path_apps, path_apps_var, path_static, app_name)

    path_app_logs = join(path_app_var, 'logs')

    path_env = join(path_app, DEFAULT_PYTHON_ENV_DIRNAME)

    invoke = InvokeRunner(ctx)
    invoke.hide = not show
    invoke.warn = True
    runner = AppRunner(invoke)

    path_app_setup = runner.mk_app_dir(path_app, 'setup')

    if module == 'httpd':

        runner.copy_template_module(app_name, template, env,
                                    path_app, path_app_var,
                                    path_app_logs, path_static,
                                    path_env, path_app_bin, path_app_setup,
                                    '/etc/httpd/conf.d/',
                                    hostname, django_port, http_port,
                                    owner, 'httpd', '.conf')

        logger.info(
            " httpd conf proxy {0}:{1} --> {0}:{2} {3}  ok!"
            .format(hostname, http_port, django_port, path_static))

        runner.chown(path_static, owner)

    if module == 'systemd':
        # django conf / run.sh
        runner.copy_template_module(app_name, template, env,
                                    path_app, path_app_var,
                                    path_app_logs, path_static,
                                    path_env, path_app_bin, path_app_setup,
                                    '/etc/systemd/system',
                                    hostname, django_port, http_port,
                                    owner, 'systemd', '.service')

        logger.info(" systemd conf ok!")

    runner.chown(path_app_setup, owner)
    runner.run('chmod +x {0} '.format(os.path.join(
        path_app_setup, '*.sh')))


@task
def install_django(ctx, template, env='default', hostname=None,
                   git_repo=default_git_repo,
                   show=False, branch=None,
                   path_apps=None, path_apps_var=None,
                   app_name=None, owner=None, path_static=None,
                   django_port=None):

    if app_name is None:
        app_name = os.path.basename(git_repo).split('.')[0]

    path_apps, path_apps_var, path_static, path_app, path_app_var,\
        path_app_bin \
        = default_path(path_apps, path_apps_var, path_static, app_name)

    if owner is None:
        owner = 'webdev'

    if hostname is None:
        hostname = os.getenv('HOSTNAME')

    if django_port is None:
        django_port = '8000'

    path_env = join(path_app, DEFAULT_PYTHON_ENV_DIRNAME)

    install_django_src(ctx, template, env, git_repo,
                       path_apps, path_apps_var, path_static, path_app,
                       path_app_var, path_app_bin, path_env,
                       app_name, owner, hostname, django_port,
                       show, branch)


def install_django_src(ctx, template, env, git_repo,
                       path_apps, path_apps_var, path_static, path_app,
                       path_app_var, path_app_bin, path_env,
                       app_name, owner, hostname, django_port,
                       show=False, branch=None):

    invoke = InvokeRunner(ctx)
    invoke.hide = not show
    invoke.warn = True

    runner = AppRunner(invoke)

    runner.rmdir(path_app)
    runner.rmdir(path_app_var)
    runner.rmdir(path_static)
    runner.mkdir(path_apps, False)
    runner.git_clone(path_app, git_repo, branch)

    runner.mkdir(path_app_var, False)
    runner.mkdir(path_static, False)
    runner.mkdir(path_app_bin, False)

    path_app_logs = runner.mk_app_dir(path_app_var, 'logs')

    runner.mk_app_dir(path_app_var, 'filestore')

    # django conf / run.sh
    runner.copy_template_django(app_name, template, env,
                                path_app, path_app_var,
                                path_app_logs, path_static,
                                path_env, path_app_bin,
                                hostname, django_port,
                                owner)

    # yum centos
    runner.install_app_os_dependencies(path_app, 'requirement-centos7.apt')

    # python
    runner.create_env(path_env, path_app)
    runner.pip(path_env, ' install --upgrade pip')
    runner.install_app_requirement(path_env, path_app, 'requirements.txt')

    # django
    runner.django_make_migrations(path_env, path_app, 'applications.txt')
    path_manage = join(path_app, 'manage.py')
    runner.python(path_env, path_manage + ' migrate')
    runner.python(path_env, path_manage + ' loaddata initial_data')
    runner.python(path_env, path_manage + ' collectstatic --noinput')

    runner.chown(path_app, owner)
    runner.chown(path_app_var, owner)
    runner.chown(path_static, owner)
    runner.run('chmod +x {0} '.format(os.path.join(
        path_app_bin, '*.sh')))

    logger.info("  Installation {} ok!".format(path_app))
