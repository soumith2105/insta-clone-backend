from rest_framework import permissions


class IsOwnerOfCommentOrOwnerOfPostOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.sender == request.user or obj.comment_on.user == request.user


class IsOwnerOfCommentOrOwnerOfReplyOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.reply_sender == request.user or obj.reply_on.sender == request.user
