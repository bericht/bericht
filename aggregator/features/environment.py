from splinter.browser import Browser
from selenium.webdriver.remote.remote_connection import LOGGER
from logging import WARNING


LOGGER.setLevel(WARNING)


def before_all(context):
    context.browser = Browser(context.config.browser or 'firefox')


def after_all(context):
    context.browser.quit()
    context.browser = None
