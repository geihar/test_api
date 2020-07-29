from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from social_network.models import User, Like, Post


class UserViewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            "user",
            "user@test.com",
            "123"
        )
        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        self.user_1 = User.objects.create(
            username="test_user1", email="email@gmail.com",
        )
        self.user_2 = User.objects.create(
            username="test_user2", email="email@gmail.com",
        )
        self.user_3 = User.objects.create(
            username="test_user3", email="email@gmail.com",
        )
        self.user_4 = User.objects.create(
            username="test_user4", email="email@gmail.com",
        )
        self.post_1 = Post.objects.create(
            title="post title", content="post content", author=self.admin
        )
        self.like_1 = Like.objects.create(post=self.post_1, user=self.admin,)
        self.like_2 = Like.objects.create(post=self.post_1, user=self.user_1,)
        self.like_3 = Like.objects.create(post=self.post_1, user=self.user_2,)
        self.like_4 = Like.objects.create(post=self.post_1, user=self.user_3,)
        self.like_5 = Like.objects.create(post=self.post_1, user=self.user_4,)

    def test_valid_date_analytics(self):
        response = self.client.get(
            "/api/analytics/",
            {
                "date_from": {self.like_1.creation_date},
                "date_to": {self.like_5.creation_date},
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["total_likes"], 5)

    def test_invalid_date_analytics(self):
        response = self.client.get(
            "/api/analytics/",
            {"date_from": "2020-02-21", "date_to": "2020-07-21"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
