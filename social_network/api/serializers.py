from rest_framework import serializers

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
    likes = serializers.IntegerField()

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
    likes = serializers.IntegerField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "slug",
            "author",
            "comment",
            "likes",
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
        fields = ("post",)

    def create(self, validated_data):
        like, _ = Like.objects.update_or_create(
            author=validated_data.get("user", None),
            post=validated_data.get("post", None),
        )
        return like
