Picky: An opinonated wiki

GPLv2 license. Django. Python. Meeting real needs.

[![Build Status](https://secure.travis-ci.org/Wilfred/Picky.png?branch=master)](http://travis-ci.org/Wilfred/Picky)

### Philosophy/Aims

This sections sets out the design goals of Picky. Not all these
features have been implemented yet.

#### Purpose

A wiki is a collection of documents, edited by a community. It
encourages everyone to contribute. Adding or modifying content should
be effortless, to encourage users to keep the content thorough and
up-to-date.

#### Syntax

The syntax should be lightweight and
[without gotchas](http://www.wilfred.me.uk/blog/2012/07/30/why-markdown-is-not-my-favourite-language/).

A live preview when editing removes the fear of 'messing up'.

Internal links should be particularly easy, as a well interlinked wiki
is more valuable.

WikiWords syntax, whilst very easy to write, forces unnatural page
names.

Wiki links should have a unintrusive GUI to aid linking to existing pages.

Code snippets should have automatic highlighting, with the option of
specifying the language if needs be.

#### History

Every edit should be associated with a user, a time, and an optional
summary. All old states of a page should be preserved.

Basic summaries should be auto-generated ('edited section Foo').

The age of the page (creation and last edited timestamps) should be
prominent to help in the case of poorly maintained content.

#### Accounts

Logging in should be with an email address and password; it's easier
to remember.

Editing without logging in should be possible.

Wherever possible, all users should be given the power to change
things.

#### Technology

Clean code and thorough unit tests.

HTML 5, but should work without JS enabled.

JS should be used when beginning / finishing editing a page, to speed
up the UI.

#### Editing

The site should be maximally editable: page content, page titles and
the site name.

Users should be able to upload attachments (images for pages, and
other useful files). These should have the same history model as pages
-- undoable, with edit summaries.

#### Discussions

All wikis have discussions, but not all wiki separate the discussion
from the content (cf. Ward's Wiki vs MediaWiki).

Users should be able to leave comments. Comments should be
threaded. Comments should be shown on the article itself, rather than
on a separate page. Comment syntax should be the same as pages.

#### User Interface

The interface should be as simple as possible. Editing should be
effortless.

The interface should encourage users to make positive contributions,
but discourage flamewars and vandalism.

Internal and external links should be styled differently. Internal
links to nonexistent pages should be styled differently, and load up
the page editor if clicked.

Whenever a username is shown, an avatar should be alongside to make it
easy to skim through to find things from the same user (even anonymous
editors).

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
