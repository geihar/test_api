from rest_framework import serializers, status
from rest_framework.response import Response

from ..models import User, Post, Like


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )


class PostListSerializer(serializers.ModelSerializer):

    author = AuthorSerializer(read_only=True)
    like = serializers.IntegerField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "slug",
            "author",
            "like",
        )


class PostDetailSerializer(serializers.ModelSerializer):

    author = AuthorSerializer(read_only=True)
    like = serializers.IntegerField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "slug",
            "author",
            "like",
        )


class PostCRUDlSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("__all__")
        read_only_fields = ("slug",)


class CreateLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("__all__")
        read_only_fields = ("ip",)

    def create(self, validated_data):

        like = Like.objects.filter(
            ip=validated_data.get("ip"), post=validated_data.get("post")
        )
        if like:
            post = Like.objects.get(post=self.data["post"], ip=validated_data.get("ip")).delete()
            return post
        else:
            like = Like.objects.create(
                ip=validated_data.get("ip"), post=validated_data.get("post")
            )
            return like

