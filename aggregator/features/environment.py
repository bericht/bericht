from splinter.browser import Browser
from selenium.webdriver.remote.remote_connection import LOGGER
from logging import WARNING


LOGGER.setLevel(WARNING)


def before_all(context):
    print(context.config.browser)
    context.browser = Browser()


def after_all(context):
    context.browser.quit()
    context.browser = None
