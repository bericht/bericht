from rest_framework import generics
from mezzanine.utils.views import render
from django_filters import FilterSet
from django.shortcuts import get_object_or_404

from aggregator.models import FeedItem
from aggregator.serializers import ArticleSerializer


class ArticleFilter(FilterSet):
    class Meta:
        model = FeedItem  # @TODO Article, not FeedItem
        fields = ['title']


# @TODO: authentification/permissions
# @TODO: extra app for administrative views?
# @TODO: Articles, not FeedItems
class ArticlesView(generics.ListCreateAPIView):
    queryset = FeedItem.objects.order_by('-updated_at')
    serializer_class = ArticleSerializer
    filter_class = ArticleFilter
    paginate_by = 10


def article_list(request):
    return render(request, ['article_list.html'])


# @TODO: Articles, not items
def article_detail(request, article_id):
    article = get_object_or_404(FeedItem, pk=article_id)
    return render(request, ['article_detail.html'], {'article': article})
