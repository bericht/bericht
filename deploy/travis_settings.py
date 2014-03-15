# local settings.py for builds on travis-ci.org

import os

HOME = os.environ['HOME']
PROJECT_ROOT = HOME + '/bericht-data'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Europe/Vienna'
SECRET_KEY = 'testkey'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'test.sqlite')
    }
}

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FROM_ADDRESS = 'projekt.xyz@riseup.net'
