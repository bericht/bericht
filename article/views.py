from rest_framework import generics
from mezzanine.utils.views import render
from django_filters import FilterSet
from django.shortcuts import get_object_or_404

from .models import Article
from .serializers import ArticleSerializer


class ArticleFilter(FilterSet):
    class Meta:
        model = Article
        fields = ['title']


# @TODO: authentification/permissions
class ArticlesView(generics.ListCreateAPIView):
    queryset = Article.objects.order_by('-updated_at')
    serializer_class = ArticleSerializer
    filter_class = ArticleFilter
    paginate_by = 10


def article_list(request):
    return render(request, ['article_list.html'],
                  {'api_endpoint': '/api/articles'})


# @TODO: Articles, not items
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, ['article_detail.html'], {'article': article})
