Bericht
=======

[![Build Status](https://travis-ci.org/bericht/bericht.png?branch=master)](https://travis-ci.org/bericht/bericht)

Is the codename for a custom django project, aiming to provide the
following to small or medium-sized communities:

* an RSS-aggregator with full-content archiving features.
* cms features to mix aggregated content with custom articles.
* a open calendar system with ical import and export.
* a forum in the style of popular question and answer sites.

Documentation is available in the docs/ directory and on [readthedocs.org](http://bericht.readthedocs.org/en/latest/).

We are currently using a fork of django_behave which has not been merged into
the mainline and due to [a bug in pip](https://github.com/pypa/pip/issues/713)
it does not write the right version to requirements.txt. Please install it
manually for the time being:

    pip install git+git://github.com/dgreisen-cfpb/django-behave.git@my_fixes#django-behave 
