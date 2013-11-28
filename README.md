Bericht
=======

Is the codename for a custom django project, aiming to provide the
following to small or medium-sized communities:

* an RSS-aggregator with full-content archiving features.
* cms features to mix aggregated content with custom articles.
* a open calendar system with ical import and export.
* a forum in the style of popular question and answer sites.

Installation
============

Usage of [virtalenv](https://pypi.python.org/pypi/virtualenv) is strongly
recommended! Currently, Bericht needs python 2 because mezzanine has not
been ported to python 3 so far.

1. Install the requirements:

    pip install -r requirements/project.txt

2. Create a local_settings.py file:

    DEBUG = True
    TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "dev.db",
        }
    }

3. Initialize the database:

    python manage.py createdb --nodata

4. Run the development server:

    python manage.py runserver

5. Have fun!
