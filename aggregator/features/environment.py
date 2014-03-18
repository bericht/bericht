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
        print("Launching sauce_connect...")
        hub_url = '%s:%s@ondemand.saucelabs.com:80' % (username, access_key)
        capabilities = {
            'tunnel-identifier': os.environ['TRAVIS_JOB_NUMBER'],
            'build': os.environ['TRAVIS_BUILD_NUMBER'],
            'tags': [os.environ['TRAVIS_PYTHON_VERSION'], 'CI'],
            'platform': 'Linux',
        }
        context.browser = Browser(
            'remote',
            desired_capabilities=capabilities,
            command_executor="http://%s/wd/hub" % hub_url)
        print("Sauce Labs job: https://saucelabs.com/jobs/%s" %
              context.browser.session_id)
        context.browser.implicitly_wait(30)
    else:
        context.browser = Browser(browser)


def after_all(context):
    context.browser.quit()
    context.browser = None
