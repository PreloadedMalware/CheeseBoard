from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from CheeseBoardSite.models import Account, Stats, Cheese, Post
from datetime import datetime

class CreatePostTest(TestCase):
    def setUp(self):
        # Create a user and their account for authentication
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
        self.stats = Stats.objects.create()
        self.account = Account.objects.create(user=self.user, stats=self.stats)
        self.client.login(username='testuser', password='testpassword123')
        
        # Create a Cheese instance for the cheese selection in the post
        self.cheese = Cheese.objects.create(name="Test Cheese")
        
        # URL for creating a post
        self.create_post_url = reverse('CheeseBoardSite:create_post')

        # Initial cheese points
        self.initial_cheese_points = self.account.cheese_points

        # Prepare post data
        self.post_data = {
            'title': 'Test Post',
            'image': SimpleUploadedFile(name='test_image.jpg', content=b'test image content', content_type='image/jpeg'),
            'caption': 'A test caption.',
            'body': 'This is the body of the test post.',
            'cheeses': [self.cheese.id],  
        }

    def test_create_post(self):
        # Submit a POST request to create a new post
        response = self.client.post(self.create_post_url, self.post_data, follow=True)
    
        
        # Success
        self.assertEqual(response.status_code, 200)
        
        
        # Verify the post was created
        self.assertTrue(Post.objects.filter(title='Test Post').exists())

        # Verify the user's cheese points were updated
        self.account.refresh_from_db()
        self.assertEqual(self.account.cheese_points, self.initial_cheese_points + 10)

    def tearDown(self):
        # Cleanup any objects created
        self.user.delete()
        self.cheese.delete()
        Post.objects.all().delete()
