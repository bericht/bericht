from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from mezzanine.utils.views import render
from django_filters import FilterSet

from aggregator.models import Item
from aggregator.serializers import ArticleSerializer


class ArticleFilter(FilterSet):
    class Meta:
        model = Item  # @TODO Article, not Item
        fields = ['title']


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def article_list(request):
    return render(request, ['article_list.html'])


# @TODO: authentification/permissions
# @TODO: extra app for administrative views?
# @TODO: pagination
# @TODO: Articles, not Items
class ArticlesView(generics.ListCreateAPIView):
    queryset = Item.objects.order_by('-updated_at')
    serializer_class = ArticleSerializer
    filter_class = ArticleFilter
    paginate_by = 10
