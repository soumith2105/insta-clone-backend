from django.contrib import admin
from .models import PostLike, CommentLike, ReplyCommentLike

# Register your models here.

admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(ReplyCommentLike)
