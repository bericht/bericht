from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(source='slug', read_only=True)
    source = serializers.CharField(source='feeditem.feed.title',
                                   read_only=True)
    tags = serializers.CharField(source='tags.names', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'slug', 'title', 'tags', 'content', 'updated_at',
                  )  # 'source')
