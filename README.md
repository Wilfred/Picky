Picky: An opinonated wiki

GPLv2 license. Django. Python. Meeting real needs.

[![Build Status](https://secure.travis-ci.org/Wilfred/Picky.png?branch=master)](http://travis-ci.org/Wilfred/Picky)

### Development

Picky uses Postgresql. Create an account called 'postgresql' with no
password, and a table called 'picky'.

    $ virtualenv ~/.py_envs/picky -p python2
    $ . ~/.py_envs/picky/bin/activate
    $ pip install -r requirements.txt
    $ cd picky
    $ python manage.py runserver
