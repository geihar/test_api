from django.test import TestCase

from social_network.models import User, Like, Post


class PostTest(TestCase):
    """ Tests for Post model. """

    def setUp(self):
        self.user_1 = User.objects.create(
            username="Casper",
            first_name="Tom",
            last_name="Adams",
            email="email@mail.com",
            password="password",
            last_visit="2020-07-21 14:58:30.849005Z",
        )
        self.post_1 = Post.objects.create(
            title="Тема поста",
            content="Тело поста",
            slug="",
            creation_date="2020-07-21 14:58:30.849005Z",
            author=self.user_1,
        )

    def test_str(self):
        post = Post.objects.get(title="Тема поста")

        self.assertEqual(str(post), "Тема поста")


class LikeTest(TestCase):
    """ Test module for Like model """

    def setUp(self):
        self.user_1 = User.objects.create(
            username="Casper",
            first_name="Tom",
            last_name="Adams",
            email="email@mail.com",
            password="password",
            last_visit="2020-07-21 14:58:30.849005Z",
        )
        self.post_1 = Post.objects.create(
            title="Тема поста",
            content="Тело поста",
            slug="",
            creation_date="2020-07-21 14:58:30.849005Z",
            author=self.user_1,
        )
        self.like = Like.objects.create(
            post=self.post_1,
            creation_date="2020-07-21 14:58:30.849005Z",
            user=self.user_1,
        )

    def test_str(self):
        like = Like.objects.filter(post=self.post_1.id, user=self.user_1.id)

        self.assertRegex(str(like), self.post_1.title)
