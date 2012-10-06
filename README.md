Picky: An opinonated wiki

GPLv2 license. Django. Python. Meeting real needs.

[![Build Status](https://secure.travis-ci.org/Wilfred/Picky.png?branch=master)](http://travis-ci.org/Wilfred/Picky)

### Philosophy/Aims

A wiki should be:

1. Effortless to write. That requires a simple syntax. [No gotchas](http://www.wilfred.me.uk/blog/2012/07/30/why-markdown-is-not-my-favourite-language/).
2. Effortless to interlink. That requires WikiWords becoming links automatically.
3. Safe to edit. That requires history of all edits.
4. Available to anyone who wants to contribute. That requires a simple permissions model.
5. Reliable. That requires thorough unit tests.

### Development

Picky uses Postgresql. Create an account called 'postgres' with no
password, and a table called 'picky':

    $ psql -U postgres
    psql> CREATE DATABASE picky;
    psql> \q

You also need to install the dependencies:

    $ virtualenv ~/.py_envs/picky -p python2
    $ . ~/.py_envs/picky/bin/activate
    $ pip install -r requirements.txt
    
Running the app is then simply:

    $ cd picky
    $ python manage.py runserver
