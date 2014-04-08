from django.db import models
from ..voting.models import Vote


# TODO: Abstract?
class Entry(models.Model):
    def is_public(self):
        votes = Vote.objects.get_votes(self)
        if votes['NO'] < 10 and votes['VETO'] < 1 and votes['YES'] >= 10:
            return True
        else:
            return False

    class Meta:
        abstract = True
