from rest_framework import serializers
from .models import Article, ImportedArticle


class ArticleSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(source='slug', read_only=True)
    source = serializers.SerializerMethodField('get_source_info')
    tags = serializers.CharField(source='tags.names', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'slug', 'title', 'tags', 'content', 'updated_at',
                  'source')

    def get_source_info(self, obj):
        if isinstance(obj, ImportedArticle):
            return {'title': obj.feeditem.feed.title,
                    'url': obj.feeditem.link}
        else:
            return None
