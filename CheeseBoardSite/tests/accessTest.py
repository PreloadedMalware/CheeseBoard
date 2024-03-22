from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from CheeseBoardSite.models import Account, Stats
from datetime import datetime
from django.utils import timezone

class UserLoginLogoutTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.mock_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.test_user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.test_stats = Stats.objects.create()

        self.test_account = Account.objects.create(
            user=self.test_user,
            dateOfBirth=datetime.now(),
            profilePic=self.mock_image,
            stats=self.test_stats
        )
    def test_account_creation(self):
        self.assertEqual(self.test_account.user.username, 'testuser')
        self.assertTrue(self.test_account.profilePic, 'Profile picture is set')

        
    def test_user_login_valid_credentials(self):
        # Test logging in with valid credentials
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'password123'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, '/')

    def test_user_login_invalid_credentials(self):
        # Test login with invalid credentials
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertIn("Incorrect Login details.", response.content.decode())

    def test_inactive_user_login(self):
        # Deactivate the test user
        self.test_user.is_active = False
        self.test_user.save()

        # Attempt to log in with the inactive user
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'password123'})
        self.assertIn("Account is disabled.", response.content.decode())

    def test_user_logout(self):
        # Log the user in
        self.client.login(username='testuser', password='password123')

        # Test logging out
        response = self.client.get('/logout/', follow=True)
        self.assertRedirects(response, '/')
        # After logout, the user should be anonymous and not authenticated
        self.assertFalse(response.context['user'].is_authenticated)

    def tearDown(self):
        # Clean up the test user
        self.test_user.delete()
