Picky: An opinonated wiki

GPLv2 license. Django. Python. Meeting real needs.

[![Build Status](https://secure.travis-ci.org/Wilfred/Picky.png?branch=master)](http://travis-ci.org/Wilfred/Picky)

### Philosophy/Aims

A wiki should be:

1. Effortless to write. The syntax should be simple and
[without gotchas](http://www.wilfred.me.uk/blog/2012/07/30/why-markdown-is-not-my-favourite-language/).

2. Effortless to interlink. Link syntax should be very lightweight,
or even use WikiWords as automatic links.

3. Safe to edit. The entire history of a page should be kept.

4. Available to anyone who wants to contribute. A permissions model is
a necessary evil, but should be as simple as possible.

5. Reliable. Thorough unit tests of all major functionality.

6. Simple accounts. Use emails as usernames (less to forget), and
allow anonymous editing.

7. Extremely editable. The home page should be editable too.

8. About the content. The wiki should support (ideally threaded) discussion,
but discourage comments being written inline.

### Development

Picky uses Postgresql. Create an account called 'postgres' with no
password, and a table called 'picky':

    $ psql -U postgres
    psql> CREATE DATABASE picky;
    psql> \q

You also need to install the dependencies:

    $ virtualenv ~/.py_envs/picky -p python2.7
    $ . ~/.py_envs/picky/bin/activate
    $ pip install -r requirements.pip
    
Running the app is then simply:

    $ cd picky
    $ python manage.py syncdb
    $ python manage.py runserver

### Deploying

There's a Fabric file that deploys my personal instance. You'll need
to modify this for your own production instance.

   $ fab deploy
