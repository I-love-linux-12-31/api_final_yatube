from rest_framework import permissions
import django.contrib.auth.models


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and obj.author == request.user

class IsAuthorOrReadOnlyForComments(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if isinstance(request.user, django.contrib.auth.models.AnonymousUser):
            # Not working ?!!
            return False
        return obj.author == request.user
