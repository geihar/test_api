import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from social_network.models import User, Post


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
            username="test_user", email="email@gmail.com",
        )
        self.post_1 = Post.objects.create(
            title="post title", content="post content", author=self.admin
        )

    def test_get_list(self):
        post_2 = Post.objects.create(
            title="post title", content="post content", author=self.user_1
        )

        response = self.client.get("/api/posts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], self.post_1.id)
        self.assertEqual(response.data[0]["title"], self.post_1.title)
        self.assertEqual(response.data[0]["content"], self.post_1.content)
        self.assertEqual(
            response.data[0]["author"]["username"], self.post_1.author.username
        )
        self.assertEqual(response.data[1]["id"], post_2.id)
        self.assertEqual(response.data[1]["title"], post_2.title)
        self.assertEqual(response.data[1]["content"], post_2.content)
        self.assertEqual(
            response.data[1]["author"]["username"], post_2.author.username
        )

    def test_get_one_post(self):
        response = self.client.get(f"/api/posts/{self.post_1.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.post_1.id)
        self.assertEqual(response.data["title"], self.post_1.title)
        self.assertEqual(response.data["content"], self.post_1.content)
        self.assertEqual(
            response.data["author"]["username"], self.post_1.author.username
        )

    def test_create_valid_post(self):
        self.valid_data = {
            "title": "My post",
            "content": "content",
            "author": self.admin.id,
        }

        response = self.client.post(
            "/api/posts/",
            data=json.dumps(self.valid_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_post(self):
        self.invalid_data = {"title": "My post", "author": self.admin.id}

        response = self.client.post(
            "/api/posts/",
            data=json.dumps(self.invalid_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_post_put(self):
        self.valid_data = {
            "title": "New post",
            "content": " new content",
            "slug": "new-post",
            "creation_date": "2020-07-21 14:58:30.849005Z",
            "author": self.admin.id,
        }

        response = self.client.put(
            f"/api/posts/{self.post_1.id}/",
            data=json.dumps(self.valid_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post_1.refresh_from_db()
        self.assertEqual(response.data["id"], self.post_1.id)
        self.assertEqual(response.data["title"], "New post")
        self.assertEqual(response.data["content"], "new content")
        self.assertEqual(
            response.data["author"]["username"], self.post_1.author.username
        )
        self.assertIsNotNone(response.data["creation_date"])

    def test_update_post_patch(self):
        self.valid_data = {
            "title": "New post2",
        }

        response = self.client.patch(
            f"/api/posts/{self.post_1.id}/",
            data=json.dumps(self.valid_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post_1.refresh_from_db()
        self.assertEqual(response.data["id"], self.post_1.id)
        self.assertEqual(response.data["title"], "New post2")
        self.assertEqual(response.data["content"], self.post_1.content)
        self.assertEqual(
            response.data["author"]["username"], self.post_1.author.username
        )
        self.assertIsNotNone(response.data["creation_date"])

    def test_delete_post(self):
        response = self.client.delete(f"/api/posts/{self.post_1.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=self.post_1.id)
