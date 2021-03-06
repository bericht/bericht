from rest_framework import serializers
from .models import Article, ImportedArticle
from ..voting.models import Vote


class ArticleSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    source = serializers.SerializerMethodField('get_source_info')
    tags = serializers.CharField(source='tags.names', read_only=True)
    is_public = serializers.CharField(read_only=True)
    votes = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'slug', 'title', 'tags', 'content', 'updated_at',
                  'source', 'votes', 'user_vote', 'is_public')

    def get_source_info(self, obj):
        if isinstance(obj, ImportedArticle):
            return {'title': obj.feeditem.feed.title,
                    'url': obj.feeditem.link}
        else:
            return None

    def get_votes(self, obj):
        return Vote.objects.get_votes(obj)

    def get_user_vote(self, obj):
        user = self.context['request'].user
        if user.is_authenticated():
            return Vote.objects.get_for_user(obj, user)
