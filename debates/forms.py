from django.contrib.comments.forms import CommentForm
from bericht.bericht_comments.models import ModeratedComment


class ModeratedCommentForm(CommentForm):
    def get_comment_model(self):
        return ModeratedComment

    def get_comment_create_data(self):
        data = super(ModeratedCommentForm, self).get_comment_create_data()
        data['is_public'] = False
        return data
