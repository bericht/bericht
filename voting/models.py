from datetime import datetime
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now

from voting.managers import VoteManager


class Vote(models.Model):
    """
    A vote on an object by a User.
    """
    VOTES = [
        ('YES',  'yes'),
        ('NO',   'no'),
        ('VETO', 'veto')
    ]
    VOTE_IDS = map(lambda x: x[0], VOTES)

    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')
    vote = models.CharField(choices=VOTES, max_length=256)
    time_stamp = models.DateTimeField(editable=False, default=now)

    objects = VoteManager()

    class Meta:
        db_table = 'votes'
        # One vote per user per object
        unique_together = (('user', 'content_type', 'object_id'),)

    def __unicode__(self):
        return u'%s: %s on %s' % (self.user, self.vote, self.object)
