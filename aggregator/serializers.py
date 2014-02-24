from rest_framework import serializers
from aggregator.models import FeedItem


class ArticleSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(source='slug', read_only=True)
    content = serializers.CharField(source='get_content', read_only=True)
    source = serializers.CharField(source='feed.title', read_only=True)
    tags = serializers.CharField(source='tags.names', read_only=True)

    class Meta:
        model = FeedItem  # @TODO Article, not FeedItem
        fields = ('id', 'slug', 'title', 'tags', 'content', 'updated_at',
                  'source')
