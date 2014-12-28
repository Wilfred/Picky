**Table of Contents**  *generated with [DocToc](http://doctoc.herokuapp.com/)*

- [Introduction](#introduction)
- [Development](#development)
- [Deploying](#deploying)
- [Known bugs](#known-bugs)
- [Philosophy/Aims](#philosophyaims)
	- [Purpose](#purpose)
	- [Syntax](#syntax)
	- [External Links](#external-links)
	- [Internal Links](#internal-links)
	- [Changes](#changes)
	- [Error pages](#error-pages)
	- [Users](#users)
	- [Technology](#technology)
	- [Editing](#editing)
	- [Discussions](#discussions)
	- [Media](#media)
	- [User Interface](#user-interface)
	- [Longevity](#longevity)
	- [Hypertext](#hypertext)
	- [Scaling Content](#scaling-content)
	- [Maintenance](#maintenance)

### Introduction

Picky is a wiki implemented with Python and Django. It aims to explore
designing a site that encourages thorough, high quality,
community-developed content through careful feature choice and UI
design.

GPLv2 license.

[![Build Status](https://secure.travis-ci.org/Wilfred/Picky.png?branch=master)](http://travis-ci.org/Wilfred/Picky)
[![Requirements Status](https://requires.io/github/Wilfred/Picky/requirements.png?branch=master)](https://requires.io/github/Wilfred/Picky/requirements/?branch=master)

### Development

You will need to install the dependencies:

    $ virtualenv ~/.py_envs/picky -p python2.7
    $ . ~/.py_envs/picky/bin/activate
    $ pip install -r requirements.pip
    
Running the app is then simply:

    $ cd picky
    $ python manage.py syncdb
    $ python manage.py migrate
    $ python manage.py runserver_plus

You will need to remove the Twitter login on login_picker.html, as
your local settings won't have the necessary keys.

### Deploying

There's a Fabric file that deploys my personal instance. You'll need
to modify this for your own production instance.

    $ fab deploy

I run picky with gunicorn as the HTTP server and supervisord
monitoring the process. Here's my configuration:

    [program:picky]
    command=/home/picky/.envs/picky/bin/gunicorn_django -b 127.0.0.1:9000 --workers=3
    directory=/home/picky/src/Picky
    user=picky
    autostart=True
    autorestart=True
    redirect_stderr=True

### Known bugs

Live preview renders links `ftp://foo` as anchor tags but server-side
does not. Also, in the following table:

    |= Header title               |= Another header title     |
    | {{{ //not italic text// }}} | {{{ **not bold text** }}} |
    | //italic text//             | **  bold text **          |

the live preview does not wrap the escaped content in `<code>` tags.

Live preview currently does not label nonexistent pages.

### Philosophy/Aims

This sections sets out the design goals of Picky. Not all these
features have been implemented yet.

#### Purpose

A wiki should foster high quality content written by a community. It
should aid many users getting involved through effortless editing and
facilitating building consensus.

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

#### External Links

External links should be highlighted differently to internal links,
e.g. `http://www.example.com` vs `/page/foo`. Absolute paths to
internal links (e.g. `http://wiki.example.com/page/foo`) should be
canonicalised and highlighted as internal.

Links to external sites should be fetched and cached when they are
first added to the page. A popover should give the user the ability to
access the cached version, the link should otherwise still go to the
live site. Good wiki content has links to the canonical references;
this external information should be preserved.

#### Internal Links

A page title should be free text, there should be no issues with
characters like '#' (Wikipedia had this problem). Page URLs should
allow non-ASCII characters. Page titles are more likely to contain
hyphens than underscores, so spaces should be replaced by underscores
to maximise URL readability.

Links to nonexistent pages should be styled differently to legitimate
URLs.

#### Changes

Every edit should be associated with a user, a time, and an optional
summary. All old states of a page should be preserved. Deletes should
be reversible.

Basic summaries should be auto-generated ('edited section Foo',
'created page', etc).

The age of the page (creation and last edited timestamps) should be
prominent to help in the case of poorly maintained content.

When viewing all history, the user should be able to get an overview
(e.g. collapse changes by week/month).

It should be possible to see diffs between page revisions, with the
changed lines highlighted.

It should be possible to subscribe to page changes, page comments, or
changes by a certain user. This should support email
notifications. Each of these change categories should also be
available as an RSS feed. If a user subscribes to things, he/she
should be able to see only subscribed changes on the 'recent changes'
page if he/she chooses.

#### Error pages

The 500 error page should not be scary, nor should the user feel they
did something wrong. It should be clear, comprehensible and include a
link to the GitHub issue tracker.

The 404 error page should be maximally helpful. It should suggest
pages with similar spelling, pages which previously had that name, and
make it easy to create a page with that name.

The 403 page should be clear and explicit.

#### Users

Logging in should be with an email address and password; it's easier
to remember. Alternatively, users should be able to simply use a
pre-existing account (Twitter, Facebook) etc.

Anonymous editing should also be possible, but may require a CAPTCHA.

Wherever possible, all users should be given the power to change
things.

Users (both anonymous and signed-in) need to be able to be banned if
necessary.

Anything associated with a user (comments, changes) should prominently
display an avatar, to visually group actions by the same user.

Users should be able to have an editable page about themselves.

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

Edit conflicts should be detected and the site should try to help fix
the situation.

#### Discussions

All wikis have discussions, but not all wiki separate the discussion
from the content (cf. Ward's Wiki vs MediaWiki).

Users should be able to leave comments. Comments should be
threaded. Comment syntax should be the same as pages.

It should be possible to vote up comments, and comments should be
displayed ordered by votes. Deep trees should be collapsed according
to voting, but collapsing trees should be togglable by the user.

#### Media

It should be possible to upload files. It should be possible to
display uploaded images on articles.

#### User Interface

The interface should be as simple as possible. A wiki is fundamentally
about reading and editing text, so the design should reflect this.

This emphasis on text will require good typographic stylic, with
adequately sized fonts and line lengths kept comfortable (code
snippets, however should be free to have longer lines).

Editing should be effortless.

The interface should encourage users to make positive contributions,
but discourage flamewars and vandalism.

The design should clearly distinguish content (e.g. the text of a
page) from metadata (e.g. when a page was last edited) and from UI
components (e.g. buttons). There should be a consistent visual design
for each of these categories.

The colour scheme should be very simple, with a colour associated with
each of the major wiki actions (viewing, editing, history). This
colour language should be used consistently and pervasively to provide
visual cues (e.g. all edit buttons the same colour).

Whenever a username is shown, an avatar should be alongside to make it
easy to skim through to find things from the same user (even anonymous
editors).

When showing history, relevant metadata should be shown. Who made each
change, how much of the page changed.

It should be possible to see all changes, changes of a specific page
or changes by a specific user. It should also be possible to watch
users or pages and only see these changes. All this data should be
available as RSS feeds.

#### Longevity

The wiki should be able to run for ten years without problem. This
requires pure dependencies (e.g. pure Python dependencies rather than
Python C modules). External dependencies (e.g. database) should be
well-established, actively maintained tools. JavaScript should be
hosted on the site itself.

In addition to logging in with accounts from social networks, users
should be able to create 'native' accounts that don't depend on the
availability of other sites.

#### Hypertext

The wiki design should be based on the principles of traditional
hypertext. Early hypertext designs, such as Xanadu, included
transclusion (including parts of other pages), strove to avoid broken
links, version control, and rights management.

The wiki should therefore combat link rot, show reverse links ('what
links to this page?'), allow previewing of links without visiting the
page, have an explicit content license, and (of course!) store history
of pages. Ideally, it would be possible to link to an arbitrary place
in content, with the links surviving edits (cf Emacs markers).

Transclusion is another hypertext feature that hasn't gained much
traction in the web at large, although embedded tweets are a good
example.

Discovering existing content is very
important. [Everything2](http://en.wikipedia.org/wiki/Everything2#Soft_links)
detects where users go next to calculate related pages. Stack Overflow
displays similar question. The wiki should therefore show similar
pages to help users discover or merge related pages. For example, most
linked to, most edited, most wanted, longest, most viewed.

There are some git features that are desirable: a 'git blame'
equivalent would be useful, as would the ability to move content
between pages whilst still tracing the original author. GitHub style
permalinks would also help: allowing linking to the visible version, rather than just linking
to latest version.

#### Scaling Content

The larger the wiki is, the more tools are needed to help the user
find what they want.

The wiki must have a search feature that indexes the full text of
pages, preferably including historical versions.

The wiki must allow (automatically generated) tables of contents, to
give an overview of larger pages. Note that Wikipedia makes these
collapsible, since they can themselves become large. We may want to
allow the user to control the depth of the table of contents
(e.g. just H1 and H2s, or including H3s and H4s too).

The wiki must allow content to be tagged. These need editable names
and descriptions (naturally).

#### Maintenance

The wiki should be easy to set up, to make it easy for people to set
up the wiki for use within their organisation (even skunkworks
projects). Therefore the wiki code should be as self-contained as
possible, with minimal server dependencies.

Once set up, the wiki should require very little maintenance, so the
users are as self-sufficient as possible.

#### Similar projects

Diigo has been developed with some similar ideas in mind. There's also
comprehensive list of wiki features at
[WikiMatrix](http://www.wikimatrix.org/wiki/mediawiki:intro).
