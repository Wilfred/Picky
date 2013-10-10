from datetime import datetime

from fabric.api import env, cd, run, get


env.hosts = ['picky@wiki.wilfred.me.uk']
env.directory = "/home/picky/src/Picky"
env.activate   = "source /home/picky/.envs/picky/bin/activate"


def virtualenv(command):
    run(env.activate + ' && ' + command)
    

def deploy():
    with cd(env.directory):
        # backup the production database to our current system
        now = datetime.now()
        backup_name = "%s-backup.db" % (now.strftime("%Y-%m-%d--%H-%M-%S"))
        get('picky/picky.db', backup_name)

        run('git pull origin master')
        virtualenv('pip install -r requirements.pip')

        with cd("picky"):
            virtualenv('python manage.py collectstatic --noinput')
            virtualenv('python manage.py syncdb')
            virtualenv('python manage.py migrate')

    restart()


def restart():
    run("sudo supervisorctl restart picky")

