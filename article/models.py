import logging
import requests

from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

from mezzanine.generic.fields import CommentsField

from bericht.entry.models import Entry

logger = logging.getLogger(__name__)


class Article(Entry):
    """ This model holds content common to all types of Article. """
    #: Holds the datetime when this item was created.
    created_at = models.DateTimeField()
    #: Holds the datetime when this item was updated.
    updated_at = models.DateTimeField(auto_now=True)
    #: Holds the datetime when this item was first published.
    published_at = models.DateTimeField(null=True)
    #: The title of the article.
    title = models.CharField(max_length=512)
    #: The content, or body, of the article.
    content = models.TextField(blank=True)
    #: The description/teaser for this article.
    teaser = models.TextField()
    #: Tags assigned to this article.
    tags = TaggableManager()
    #: Comments of this article.
    comments = CommentsField()

    def slug(self):
        return "%d-%s" % (self.id, slugify(self.title))

    def get_absolute_url(self):
        return reverse('bericht.article.views.article_detail',
                       args=[str(self.id)])

class ImportedArticle(Article):
    """
    This model is created from an aggregator.FeedItem and contains
    additional data that is useful for this scenario.
    """
    #: The FeedItem this ImportedArticle was created from.
    feeditem = models.OneToOneField('aggregator.FeedItem')
    #: This holds the full HTML of the article linked to by the FeedItem.
    link_html = models.TextField(blank=True)

    def fetch_html_and_extract(self):
        """
        Fetches the full HTML from this article's link and extracts the full
        article content using article extraction (via artex).
        """
        # @TODO: Ask if the html was actually modified (ETag, 304).
        req = requests.get(self.feeditem.link,
                           headers={'user-agent': 'readability'},
                           verify=False)

        # requests.get handles redirection, so everything except 200 here
        # should be an actual error.
        if req.status_code != 200:
            logger.error("error while fetching HTML of '%s': %s" %
                         (self.feeditem.link, req.status_code))
            return

        self.link_html = req.content
        # @TODO add article extraction here
        self.save()

    @classmethod
    def from_feeditem(cls, feeditem):
        """ Creates an ImportedArticle from a FeedItem. """
        article, new = cls.objects.get_or_create(
            feeditem=feeditem,
            title=feeditem.title,
            created_at=feeditem.updated_at,
            teaser=feeditem.description)
        # @TODO Check if this works, looks like it does not.
        article.tags.add(*feeditem.tags.all())
        if new:
            article.save()

        status = "new" if new else "updated"
        logger.info("Created %s ImportedArticle: %s" % (status,
                                                        article.title))
