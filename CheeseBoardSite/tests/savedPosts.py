from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from CheeseBoardSite.models import Post, Account, Stats, Saved
from django.test.client import Client

class PostSaveTest(TestCase):
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
            timeDate=timezone.now()
        )

    def test_save_post(self):
        # Saving the post
        response = self.client.post(reverse('CheeseBoardSite:save_post', kwargs={'slug': self.post.slug}))

        # Checking if the post is added to saved posts
        saved_posts = Saved.objects.filter(account=self.account, posts__in=[self.post])
        self.assertTrue(saved_posts.exists())

        # check redirect happens
        self.assertEqual(response.status_code, 302)
