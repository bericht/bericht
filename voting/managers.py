from django.db import models
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType


class VoteManager(models.Manager):
    def get_votes(self, obj):
        """
        Returns true if the given object should be published.
        """
        ctype = ContentType.objects.get_for_model(obj)
        result = self.filter(
            object_id=obj._get_pk_val(),
            content_type=ctype
        ).values('vote').annotate(number=Count('vote'))
        return {i['vote']: i['number'] for i in result}

    def record_vote(self, obj, user, vote):
        """
        Record a user's vote on a given object. Only allows a given user
        to vote once, though that vote may be changed.
        """
        ctype = ContentType.objects.get_for_model(obj)

        if vote not in self.model.VOTE_IDS:
            raise ValueError('Invalid vote (must be one of %s).' %
                             ', '.join(self.model.VOTE_IDS))
        try:
            v = self.get(user=user, content_type=ctype,
                         object_id=obj._get_pk_val())
            if vote == 'ABSTAIN':
                v.delete()
            else:
                v.vote = vote
                v.save()
        except models.ObjectDoesNotExist:
            if vote == 'ABSTAIN':
                return
            self.create(user=user, content_type=ctype,
                        object_id=obj._get_pk_val(), vote=vote)

    def get_for_user(self, obj, user):
        """
        Get the vote made on the given object by the given user, or
        ``None`` if no matching vote exists.
        """
        if not user.is_authenticated():
            return None
        ctype = ContentType.objects.get_for_model(obj)
        try:
            vote = self.get(content_type=ctype, object_id=obj._get_pk_val(),
                            user=user)
        except models.ObjectDoesNotExist:
            vote = None
        return vote

    def get_for_user_in_bulk(self, objects, user):
        """
        Get a dictionary mapping object ids to votes made by the given
        user on the corresponding objects.
        """
        vote_dict = {}
        if len(objects) > 0:
            ctype = ContentType.objects.get_for_model(objects[0])
            votes = list(self.filter(content_type__pk=ctype.id,
                                     object_id__in=[obj._get_pk_val()
                                                    for obj in objects],
                                     user__pk=user.id))
            vote_dict = dict([(vote.object_id, vote) for vote in votes])
        return vote_dict
