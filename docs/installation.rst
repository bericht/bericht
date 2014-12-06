Installation Instructions
=========================

Bericht is currently written in python 2, because mezzanine has not
been ported to python 3 so far. So you need at least python 2 (including
development headers) and pip, pythons package manager as well as two
libraries for xml-parsing, libxml and libxslt. On Debian(-based)
systems the following should  be sufficient:::

  apt-get install python python-dev python-pip libxml2-dev libxslt-dev

.. TIP::
   Usage of `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ is strongly
   recommended!


Install the requirements::

  pip install -r requirements.txt

Create a ``local_settings.py`` file::

  DEBUG = True
  DATABASES = {
      "default": {
          "ENGINE": "django.db.backends.sqlite3",
          "NAME": "dev.db",
      }
  }

Initialize the database::

  python manage.py createdb --nodata
  python manage.py migrate

Run the development server::

  python manage.py runserver

Have fun!


Ansible
-------

We deploy our systems using `ansible <http://ansible.com>`_, the scripts are
tested to run on debian stable and included in ``deploy/``. Change ``bericht.dev``
in ``deploy/hosts`` to the IP or hostname of your debian server and run::

  ansible-playbook -i deploy/hosts -K deploy/site.yml
