from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, permissions, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated

from posts.models import Post, Comment, Follow, Group
from .serializers import (
    PostSerializer,
    CommentSerializer,
    FollowSerializer,
    GroupSerializer
)
from .permissions import IsAuthorOrReadOnly, IsAuthorOrReadOnlyForComments


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        if isinstance(
                self.request.user,
                AnonymousUser
        ) or not self.request.user.is_authenticated:
            raise NotAuthenticated("Not authenticated")
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnlyForComments]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        if isinstance(
                self.request.user, AnonymousUser
        ) or not self.request.user.is_authenticated:
            # print("DEBUG: Create comment: not authenticated!")
            raise NotAuthenticated("Not authenticated")

        post_id = self.kwargs.get('post_id')

        if serializer.is_valid():
            post = Post.objects.get(id=post_id)
            serializer.save(author=self.request.user, post=post)
            # print("DEBUG: created comment", obj)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    # def post(self, request): # , post_id
    #     post_id = self.kwargs.get('post_id')
    #     if not request.user.is_authenticated:
    #         return Response(
    #         "Not authenticated", status=status.HTTP_401_UNAUTHORIZED
    #         )
    #     return super().post(request, post_id)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'following__username']

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # def get(self, request, *args, **kwargs):
    #     user = self.request.user
    #     if not user.is_authenticated:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)
    #     return super().get(request, *args, **kwargs)
