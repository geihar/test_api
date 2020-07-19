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
        fields = ("__all__",)
        read_only_fields = ("slug",)


class CreateLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            "post",
            "creation_date",
        )
        read_only_fields = ("user",)

    def create(self, validated_data):

        like = Like.objects.filter(
            user=validated_data.get("user"), post=validated_data.get("post")
        )
        if like:
            post = Like.objects.get(
                post=self.data["post"], user=validated_data.get("user")
            ).delete()
            return post
        else:
            like = Like.objects.create(
                user=validated_data.get("user"), post=validated_data.get("post")
            )
            return like


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        write_only_fields = ("password",)
