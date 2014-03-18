
def get_model():
    from mezzanine.generic.models import ThreadedComment
    return ThreadedComment


def get_form():
    from .forms import ModeratedCommentForm
    return ModeratedCommentForm
