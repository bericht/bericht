import os
from logging import WARNING
from splinter.browser import Browser
from selenium.webdriver.remote.remote_connection import LOGGER


LOGGER.setLevel(WARNING)


def before_all(context):
    browser = context.config.browser or os.environ.get('browser') or 'firefox'

    username = os.environ.get('SAUCE_USERNAME')
    access_key = os.environ.get('SAUCE_ACCESS_KEY')

    if username and access_key:
        server_url = 'http://%s:%s@ondemand.saucelabs.com/wd/hub' % (
            username, access_key)
        capabilities = {
            'tunnel_identifier': os.environ['TRAVIS_JOB_NUMBER'],
            'platform': 'Linux',
        }
        context.browser = Browser('remote', server_url, **capabilities)
    else:
        context.browser = Browser(browser)


def after_all(context):
    context.browser.quit()
    context.browser = None
