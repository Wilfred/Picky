from datetime import datetime

from fabric.api import env, cd, run, get, sudo


env.hosts = ['picky@wiki.wilfred.me.uk']
env.directory = "/home/picky/src/Picky"
env.activate   = "source /home/picky/.envs/picky/bin/activate"


def virtualenv(command):
    run(env.activate + ' && ' + command)


def backup():
    """Backup the production database to our current system."""
    with cd(env.directory):
        now = datetime.now()
        backup_name = "%s-backup.db" % (now.strftime("%Y-%m-%d--%H-%M-%S"))
        get('picky/picky.db', backup_name)


def deploy():
    backup()
    
    with cd(env.directory):
        run('git checkout master')        
        run('git fetch')
        run('git reset --hard origin/master')

        run("find . -name '*.pyc' -delete")

        virtualenv('pip install -r requirements.pip')

        with cd("picky"):
            virtualenv('python manage.py collectstatic --noinput')
            virtualenv('python manage.py syncdb')
            virtualenv('python manage.py migrate')
            virtualenv('python manage.py rebuild_index --noinput')

    restart()

    with cd(env.directory):
        run('cp configuration/wiki.wilfred.me.uk /etc/nginx/sites-enabled/')

    sudo("service nginx reload", shell=False)

    with cd(env.directory):
        run('cp configuration/picky.conf /etc/supervisor/conf.d/')


def restart():
    sudo("supervisorctl restart picky", shell=False)


def update_settings():
    url = raw_input("URL for live settings: ").strip()

    with cd(env.directory):
        with cd('picky'):
            run("wget -N '%s'" % url)

    restart()
