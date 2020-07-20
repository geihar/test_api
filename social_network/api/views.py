from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from django.db import models
from django.contrib.auth.hashers import make_password

from .permissions import IsOwnerOrReadOnly
from ..models import Post, User, Like
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCRUDlSerializer,
    CreateLikeSerializer,
    UserCreateSerializer,
    UserActivitySerializer,
    AnalyticSerializer,
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

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [
                permissions.IsAuthenticated,
            ]
        elif self.action in [
            "update",
            "partial_update",
        ]:
            self.permission_classes = [
                IsOwnerOrReadOnly,
            ]
        elif self.action in ["destroy"]:
            self.permission_classes = [
                permissions.IsAdminUser,
            ]
        else:
            self.permission_classes = [
                permissions.AllowAny,
            ]
        return super(self.__class__, self).get_permissions()


class AddLike(generics.CreateAPIView):

    serializer_class = CreateLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserCreate(generics.CreateAPIView):

    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        serializer.validated_data["password"] = make_password(
            serializer.validated_data["password"]
        )
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


class UserLastActivity(generics.RetrieveAPIView):

    serializer_class = UserActivitySerializer
    queryset = User.objects.all()

    class Meta:
        models = User


class AnalyticView(generics.ListAPIView):

    serializer_class = AnalyticSerializer

    def get_queryset(self):
        queryset = (
            Like.objects.filter(
                creation_date__gte=self.request.GET.getlist("date_from")[0],
                creation_date__lte=self.request.GET.getlist("date_to")[0],
            )
            .values("creation_date")
            .annotate(total_likes=models.Count("id"))
        )
        return queryset
