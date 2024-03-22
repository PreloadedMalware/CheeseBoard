from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from CheeseBoardSite.models import Post, Account, Stats
from django.test.client import Client


class PostLikeTest(TestCase):
    def setUp(self):
        # Creating user and account
        self.user = User.objects.create_user('testuser', 'user@example.com', 'testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Creating a Stats instance
        self.stats = Stats.objects.create()

        # Creating an Account and linking it with the User
        self.account = Account.objects.create(user=self.user, stats=self.stats, dateOfBirth=timezone.now())

        # Creating a Post
        self.post = Post.objects.create(
            title="Test Post",
            body="Test Body",
            account=self.account,
            likes=0,
            timeDate=timezone.now()
        )

    def test_like_post(self):
        # Initial likes count
        initial_likes_count = self.post.likes

        # Liking the post
        response = self.client.get(reverse('CheeseBoardSite:like_post', kwargs={'slug': self.post.slug}))

        # Fetching the updated post from the database
        self.post.refresh_from_db()

        # Check if the likes count has increased by 1
        self.assertEqual(self.post.likes, initial_likes_count + 1)

