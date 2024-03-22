from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from CheeseBoardSite.models import Account, Stats, Cheese, Post
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
class IndexPageTest(TestCase):
    def setUp(self):
        # Create a Stats instance
        self.stats1 = Stats.objects.create()

        # Create a User instance
        self.user1 = User.objects.create_user(username='user1', password='testpassword123')
        mock_image = SimpleUploadedFile('test_image.jpg', b'test_image_content', content_type='image/jpeg')
        # Create an Account instance
        self.account1 = Account.objects.create(user=self.user1, stats=self.stats1, dateOfBirth=timezone.now())

        # Create Cheeses for testing
        self.cheese1 = Cheese.objects.create(name="Cheddar")
        self.cheese2 = Cheese.objects.create(name="Gouda")

        # Create sample posts with Cheeses for testing
        for i in range(5):
            post = Post.objects.create(
                title=f"Test Post {i}",
                body="Test Body",
                account=self.account1,
                image = mock_image,
                timeDate=timezone.now() - timedelta(days=i),
                likes=i,
            )
            post.cheeses.add(self.cheese1 if i % 2 == 0 else self.cheese2)

    def test_index_page_unauthenticated(self):
        response = self.client.get(reverse('CheeseBoardSite:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CheeseBoardSite/index.html')
        # Check tags and posts in context
        tags = response.context['tags']
        self.assertIn(self.cheese1.name, tags)
        self.assertIn(self.cheese2.name, tags)
        posts = response.context['posts']
        self.assertTrue(any(post['title'] == 'Test Post 0' for post in posts))
        self.assertTrue(any(post['content'] == 'Test Body' for post in posts))

    def test_index_page_authenticated(self):
        self.client.login(username='user1', password='testpassword123')
        response = self.client.get(reverse('CheeseBoardSite:index'))
        self.assertEqual(response.status_code, 200)
        # Check tags, posts, followingPosts, and mostLiked in context
        self.assertTrue('tags' in response.context)
        self.assertTrue('posts' in response.context)
        self.assertTrue('followingPosts' in response.context)
        self.assertTrue('mostLiked' in response.context)
        # Ensure mostLiked posts are correctly ordered by likes
        mostLiked = response.context['mostLiked']
        self.assertTrue(all(mostLiked[i]['likes'] >= mostLiked[i + 1]['likes'] for i in range(len(mostLiked) - 1)))

