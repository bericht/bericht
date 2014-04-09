from mezzanine.conf import settings
from mezzanine.utils.views import render, paginate

from bericht.article.models import Article


def frontpage(request):
    # @TODO: Use weight and featured fields, which need to be implemented.
    articles = Article.objects.order_by('-updated_at')[:5]
    articles = paginate(articles, request.GET.get("page", 1),
                        settings.BLOG_POST_PER_PAGE,
                        settings.MAX_PAGING_LINKS)
    return render(request, ['frontpage.html'], {'articles': articles})
