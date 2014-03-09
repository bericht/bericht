from urlparse import urljoin

from behave import given, when, then


@given(u'the user accesses the url "{url}"')
def the_user_accesses_the_url(context, url):
    full_url = urljoin(context.config.server_url, url)
    context.browser.visit(full_url)


@then(u'she should see {expected:d} articles in the sidebar')
def she_should_see_articles(context, expected):
    #context.browser.is_element_present_by_css('#sidebar li', wait_time=3)
    found = len(context.browser.find_by_css('#sidebar li'))
    assert found == int(expected), 'expected %r articles, found %r' \
        % (int(expected), found)


@when('we implement a test')
def implement_a_test(context):
    assert True is not False


@then('behave will test it for us')
def behave_will_test(context):
    assert context.failed is False
