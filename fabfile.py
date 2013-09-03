from fabric.api import env, cd, sudo


env.hosts = ['wilfred@wiki.wilfred.me.uk']
env.directory = "/home/picky/src/Picky"
env.activate   = "source /home/picky/.envs/picky/bin/activate"


def virtualenv(command, user="picky"):
    sudo(env.activate + ' && ' + command, user=user)
    

def deploy():
    with cd(env.directory):
        sudo('git pull origin master', user="picky")
        virtualenv('pip install -r requirements.pip')

        with cd("picky"):
            virtualenv('python manage.py collectstatic')
            virtualenv('python manage.py syncdb')
            virtualenv('python manage.py migrate')

    restart()


def restart():
    sudo("supervisorctl restart picky")

