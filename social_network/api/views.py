from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from django.db import models


from .permissions import IsOwnerOrReadOnly
from .services import get_client_ip
from ..models import Post
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCRUDlSerializer,
    CreateLikeSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().annotate(like=models.Count(models.F("post_like")))
    serializer_class = PostCRUDlSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.all().annotate(like=models.Count(models.F("post_like")))
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostDetailSerializer(instance)
        return Response(serializer.data)

    # def get_permissions(self):
    #     if self.action in ["create"]:
    #         self.permission_classes = [
    #             permissions.IsAuthenticated,
    #         ]
    #     elif self.action in [
    #         "update",
    #         "partial_update",
    #     ]:
    #         self.permission_classes = [
    #             IsOwnerOrReadOnly,
    #         ]
    #     elif self.action in ["destroy"]:
    #         self.permission_classes = [
    #             permissions.IsAdminUser,
    #         ]
    #     else:
    #         self.permission_classes = [
    #             permissions.AllowAny,
    #         ]
    #     return super(self.__class__, self).get_permissions()


class AddLike(generics.CreateAPIView):

    serializer_class = CreateLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))