from fabric.api import env, cd, run


env.hosts = ['wilfred.webfactional.com']
env.directory = "~/webapps/django/picky" # FIXME: this is a lousy folder name
env.activate   = "source ~/.virtualenvs/picky/bin/activate"


def virtualenv(command):
    run(env.activate + ' && ' + command)
    

def deploy():
    with cd(env.directory):
        run('git pull origin master')
        virtualenv('pip install -r requirements.pip')

        with cd("picky"):
            virtualenv('python manage.py migrate')
            virtualenv('python manage.py collectstatic --noinput')

    restart()


def restart():
    run("~/webapps/django/apache2/bin/restart")

