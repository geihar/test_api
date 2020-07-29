import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from social_network.models import User, Post, Like


class LikeViewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            "user",
            "user@test.com",
            "123"
        )
        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        self.user_1 = User.objects.create(
            username="test_user", email="email@gmail.com",
        )
        self.post_1 = Post.objects.create(
            title="post title", content="post content", author=self.admin
        )
        self.post_2 = Post.objects.create(
            title="post title", content="post content", author=self.admin
        )
        self.like_1 = Like.objects.create(
            post=self.post_1,
            user=self.admin,
            creation_date="2020-07-21 14:58:30.849005Z",
        )

    def test_add_like(self):
        self.valid_data = {"post": self.post_2.id}

        response = self.client.post(
            "/api/like/",
            data=json.dumps(self.valid_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_like(self):
        self.valid_data = {"post": self.post_1.id}

        response = self.client.post(
            "/api/like/",
            data=json.dumps(self.valid_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        with self.assertRaises(Like.DoesNotExist):
            Like.objects.get(id=self.like_1.id)
