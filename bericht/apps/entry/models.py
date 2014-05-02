from django.db import models
from polymorphic import PolymorphicModel
from ..voting.models import Vote


class Entry(PolymorphicModel):
    # cache the result of is_public here to make it easier to query.
    public = models.BooleanField(default=False)

    def is_public(self):
        """
        Change this method here or in a child class to (selectivly) override
        the criteria for public Entries.
        """
        votes = Vote.objects.get_votes(self)
        if votes['NO'] < 10 and votes['VETO'] < 1 and votes['YES'] >= 10:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        self.public = self.is_public()
        super(Entry, self).save(*args, **kwargs)
