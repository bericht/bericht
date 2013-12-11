Installation Instructions
=========================

Bericht is currently written in python 2, because mezzanine has not
been ported to python 3 so far. So you need at least python 2 (including
development headers) and pip, pythons package manager. On Debian(-based)
systems the following should  be sufficient:::

  apt-get install python python-dev python-pip

.. TIP::
   Usage of `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ is strongly
   recommended!


Install the requirements::

  pip install -r requirements/project.txt

Create a ``local_settings.py`` file::

  DEBUG = True
  TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'
  DATABASES = {
      "default": {
          "ENGINE": "django.db.backends.sqlite3",
          "NAME": "dev.db",
      }
  }

Initialize the database::

  python manage.py createdb --nodata

Run the development server::

  python manage.py runserver

Have fun!
