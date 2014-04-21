from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import generics
from mezzanine.utils.views import render
from django_filters import FilterSet

from .models import Article
from .serializers import ArticleSerializer


class ArticleFilter(FilterSet):
    class Meta:
        model = Article
        fields = ['title']


# @TODO: authentification/permissions
class ArticlesView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    filter_class = ArticleFilter
    paginate_by = 10

    def get_queryset(self):
        queryset = Article.objects.order_by('-updated_at')

        public = self.request.QUERY_PARAMS.get('public', None)
        if public == 't':
            return queryset.filter(public=True)
        elif public == 'f':
            return queryset.filter(public=False)
        return queryset


def article_list(request, public=None):
    api_endpoint = '/api/articles/?'
    if public:
        api_endpoint += "public=%s&" % public

    return render(request, ['article_list.html'],
                  {'api_endpoint': api_endpoint})


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if not article.public:
        return Http404()

    return render(request, ['article_detail.html'], {'article': article})
