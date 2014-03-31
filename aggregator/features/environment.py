import os
from logging import WARNING
from splinter.browser import Browser
from selenium.webdriver.remote.remote_connection import LOGGER


LOGGER.setLevel(WARNING)


def before_all(context):
    browser = context.config.browser or os.environ.get('browser') or 'firefox'
    context.browser = Browser(browser)


def after_all(context):
    context.browser.quit()
    context.browser = None
