from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
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


# @TODO: protected
# @TODO: extra app for administrative views?
# @TODO: pagination
@csrf_exempt
def article_list_json(request):
    if request.method == 'GET':
        articles = Item.objects.order_by('-updated_at')
        filter = ArticleFilter(request.GET, queryset=articles)
        serializer = ArticleSerializer(filter[:20], many=True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        return HttpResponseForbidden()

    # @TODO Articles, not Items
