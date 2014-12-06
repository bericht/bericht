from django.conf.urls import patterns, include, url
from django.contrib import admin

from .apps.article.views import ArticlesView
from .apps.entry.views import VotesView

admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = patterns(
    "",
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    ("^admin/", include(admin.site.urls)),

    url("^$", "bericht.apps.entry.views.frontpage", name='home'),

    url("^api/articles/$", ArticlesView.as_view(), name='articles-view'),

    url("^backend/articles/$", "bericht.apps.article.views.article_list",
        name='backend-articles'),
    url("^backend/articles/hidden/$",
        "bericht.apps.article.views.article_list",
        {'public': 'f'}, name='backend-articles-hidden'),
    url("^backend/articles/public/$",
        "bericht.apps.article.views.article_list",
        {'public': 't'}, name='backend-articles-public'),

    url("^api/votes/(?P<entry_id>\d+)(?:/(?P<vote>yes|no|veto|abstain))?/$",
        VotesView.as_view(), name='votes-view'),

    url(r'(?P<article_id>\d+)/$', "bericht.apps.article.views.article_detail",
        name='article-detail'),

    # MEZZANINE'S URLS
    # ----------------
    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!

    # If you'd like more granular control over the patterns in
    # ``mezzanine.urls``, go right ahead and take the parts you want
    # from it, and use them directly below instead of using
    # ``mezzanine.urls``.
    ("^", include("mezzanine.urls")),

    # MOUNTING MEZZANINE UNDER A PREFIX
    # ---------------------------------
    # You can also mount all of Mezzanine's urlpatterns under a
    # URL prefix if desired. When doing this, you need to define the
    # ``SITE_PREFIX`` setting, which will contain the prefix. Eg:
    # SITE_PREFIX = "my/site/prefix"
    # For convenience, and to avoid repeating the prefix, use the
    # commented out pattern below (commenting out the one above of course)
    # which will make use of the ``SITE_PREFIX`` setting. Make sure to
    # add the import ``from django.conf import settings`` to the top
    # of this file as well.
    # Note that for any of the various homepage patterns above, you'll
    # need to use the ``SITE_PREFIX`` setting as well.

    # ("^%s/" % settings.SITE_PREFIX, include("mezzanine.urls"))

)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
