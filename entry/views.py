from mezzanine.conf import settings
from mezzanine.utils.views import render, paginate
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, HttpResponseForbidden, Http404
from voting.models import Vote

from bericht.article.models import Article
from bericht.entry.models import Entry


class VotesView(APIView):

    def get_entry(self, pk):
        try:
            return Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            raise Http404

    def get(self, request, entry_id, vote=None, format=None):
        entry = self.get_entry(entry_id)
        votes = Vote.objects.get_votes(entry)
        return HttpResponse(JSONRenderer().render(votes),
                            {'content_type': 'application/json'})

    def post(self, request, entry_id, vote=None, format=None):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        entry = self.get_entry(entry_id)
        if vote == 'veto':
            pass  # @TODO: Implement Veto in our django-voting fork.
        elif vote:
            Vote.objects.record_vote(entry, request.user, vote)

        return self.get(request, entry_id, format=format)


def frontpage(request):
    # @TODO: Use weight and featured fields, which need to be implemented.
    articles = Article.objects.order_by('-updated_at')[:5]
    articles = paginate(articles, request.GET.get("page", 1),
                        settings.BLOG_POST_PER_PAGE,
                        settings.MAX_PAGING_LINKS)
    return render(request, ['frontpage.html'], {'articles': articles})
