from rest_framework import serializers
from aggregator.models import Item


class ArticleSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(source='slug', read_only=True)
    content = serializers.CharField(source='get_content', read_only=True)

    class Meta:
        model = Item  # @TODO Article, not Item
        fields = ('id', 'slug', 'title', 'tags', 'content', 'updated_at')
