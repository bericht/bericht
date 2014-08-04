from time import sleep
from urlparse import urljoin

from behave import given, when, then
from django.core.management import call_command
from django.contrib.auth.models import User


@given(u'we have some test data loaded from "{fixture}"')
def we_have_some_test_data(context, fixture):
    call_command('loaddata', fixture,
                 **{'verbosity': 0, 'skip_validation': True})


@when(u'the user logs in as "{username}"')
def the_user_logs_in(context, username):
    user, created = User.objects.get_or_create(
        username=username, defaults={'password': username, 'is_staff': True})
    if created:
        user.set_password(username)
        user.save()
        #context.browser.reload()
    context.browser.visit(urljoin(context.config.server_url, '/admin/'))
    context.browser.fill('username', username)
    context.browser.fill('password', username)
    context.browser.find_by_value('Log in').first.click()


@when(u'the user accesses the url "{url}"')
def the_user_accesses_the_url(context, url):
    full_url = urljoin(context.config.server_url, url)
    context.browser.visit(full_url)


@when(u'the user clicks on the link "{label}"')
def the_user_clicks_on_the_link(context, label):
    context.browser.find_link_by_partial_text(label)[0].click()
    sleep(1)


@when(u'the user votes "{vote}"')
def the_user_votes(context, vote):
    for button in context.browser.find_by_css('article .vote'):
        if button.find_by_css('.name').first.text.lower() == vote.lower():
            button.click()
            break


@then(u'they should see {expected:d} articles in the sidebar')
@then(u'they should see {expected:d} articles in the sidebar, for example')
def they_should_see_articles(context, expected):
    found = len(context.browser.find_by_css('#sidebar-list li'))
    assertEqual(found, int(expected), 'expected %r articles, found %r'
                % (int(expected), found))
    if context.table:
        for row in context.table:
            position = int(row['position']) - 1
            entry = context.browser.find_by_css('#sidebar-list li')[position]
            assertEqual(entry.text, row['title'])


@then(u'they should see an article with the following attributes')
def they_should_see_an_article(context):
    attributes = {
        'title':    'article h2',
        'source':   'article .meta .source',
        'updated':  'article .meta .updated',
        'public':   'article .meta .public',
        'tags':     'article .meta .tags',
    }
    for row in context.table:
        for key, value in zip(row.headings, row.cells):
            if key in attributes:
                el = context.browser.find_by_css(attributes[key])[0]

                if key == 'updated':
                    assertEqual(el['title'], value)
                else:
                    assertEqual(el.text, value)


def assertEqual(first, second, msg=None):
    assert first == second, msg or "%r != %r" % (first, second)
