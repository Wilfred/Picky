from fabric.api import env, cd, run


env.hosts = ['picky@wiki.wilfred.me.uk']
env.directory = "/home/picky/src/Picky"
env.activate   = "source /home/picky/.envs/picky/bin/activate"


def virtualenv(command):
    run(env.activate + ' && ' + command)
    

def deploy():
    with cd(env.directory):
        run('git pull origin master')
        virtualenv('pip install -r requirements.pip')

        with cd("picky"):
            virtualenv('python manage.py collectstatic --noinput')
            virtualenv('python manage.py syncdb')
            virtualenv('python manage.py migrate')

    restart()


def restart():
    run("sudo supervisorctl restart picky")

