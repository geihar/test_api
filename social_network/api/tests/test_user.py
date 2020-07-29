import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from social_network.models import User


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

    def test_add_user(self):
        self.valid_data = {
            "username": "test_user2",
            "email": "email@gmail.com",
            "password": "1234",
        }

        response = self.client.post(
            "/api/signup/",
            data=json.dumps(self.valid_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_invalid_user(self):
        self.valid_data = {
            "username": "test_user",
            "email": "email@gmail.com",
            "password": "1234",
        }

        response = self.client.post(
            "/api/signup/",
            data=json.dumps(self.valid_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_visit(self):
        response = self.client.get(f"/api/user/{self.user_1.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user_1.username)
        self.assertIsNotNone(response.data["last_visit"])
