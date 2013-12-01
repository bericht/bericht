from mezzanine.conf import settings
from mezzanine.utils.views import render, paginate

from bericht.aggregator.models import Item


def frontpage(request):
    # @TODO: Use weight and featured fields, which need to be implemented.
    # @TODO: use_editable for mezzanines inline editing?
    # @TODO: probably we should support other conntent types here?
    articles = Item.objects.order_by('-updated_at')[:5]
    articles = paginate(articles, request.GET.get("page", 1),
                        settings.BLOG_POST_PER_PAGE,
                        settings.MAX_PAGING_LINKS)
    return render(request, ['frontpage.html'], {'articles': articles})
