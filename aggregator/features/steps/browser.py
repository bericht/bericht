from time import sleep
from urlparse import urljoin

from behave import given, when, then
from django.core.management import call_command


@given(u'we have some test data loaded from "{fixture}"')
def we_have_some_test_data(context, fixture):
    call_command('loaddata', fixture,
                 **{'verbosity': 0, 'skip_validation': True})


@when(u'the user accesses the url "{url}"')
def the_user_accesses_the_url(context, url):
    full_url = urljoin(context.config.server_url, url)
    context.browser.visit(full_url)


@when(u'the user clicks on the link "{label}"')
def the_user_clicks_on_the_link(context, label):
    context.browser.find_link_by_partial_text(label)[0].click()
    sleep(1)


@then(u'she should see {expected:d} articles in the sidebar')
def she_should_see_articles(context, expected):
    found = len(context.browser.find_by_css('#sidebar-list li'))
    assertEqual(found, int(expected), 'expected %r articles, found %r'
                % (int(expected), found))


@then(u'the {number:d}. article should have the title "{title}"')
def the_article_should_have_the_title(context, number, title):
    entry = context.browser.find_by_css('#sidebar-list li')[number-1]
    assertEqual(entry.text, title)


def assertEqual(first, second, msg=None):
    assert first == second, msg or "%r != %r" % (first, second)
