from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from CheeseBoardSite.models import Account, Stats, Cheese
from django.core.files.uploadedfile import SimpleUploadedFile

class UserAuthenticationTest(TestCase):
    def setUp(self):
        # Create a user, stats, and cheese for testing.
        self.test_user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
        self.test_stats = Stats.objects.create()
        self.test_cheese = Cheese.objects.create(name="Cheddar")

        # Create an associated account for the test user.
        self.test_account = Account.objects.create(
            user=self.test_user,
            dateOfBirth="2000-01-01",
            stats=self.test_stats,
            faveCheese=self.test_cheese,
            profilePic=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
        )

        # Define the login URL.
        self.login_url = reverse('CheeseBoardSite:login')

    def test_successful_login(self):
        # Test logging in with correct credentials.
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword123'})
        self.assertRedirects(response, reverse('CheeseBoardSite:index'))
        self.assertTrue(authenticate(username='testuser', password='testpassword123').is_authenticated)

    def test_failed_login(self):
        # Test logging in with incorrect credentials.
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Incorrect Login details.", response.content.decode())

    def tearDown(self):
        # Delete the test user after tests run.
        self.test_user.delete()
