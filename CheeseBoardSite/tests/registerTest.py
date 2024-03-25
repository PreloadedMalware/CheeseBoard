from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from CheeseBoardSite.models import Account, Stats, Cheese
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import authenticate
from django.utils.dateparse import parse_date


class RegisterTest(TestCase):
    def setUp(self):
        # Prepare data for registration
        self.register_url = reverse('CheeseBoardSite:register')
        # Assuming there is at least one Cheese object in the database. If not, create one in the test setup.
        self.cheese = Cheese.objects.create(name="Test Cheese")
        self.registration_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Testpassword123',
            'passwordConfirm': 'Testpassword123',
            'first_name': 'New',
            'last_name': 'User',
            'dateOfBirth': '01/01/2000',  # Match the input format specified in AccountForm
            'faveCheese': self.cheese.id  # Use the ID of the cheese object
        }

    def test_user_registration(self):
        # Submit the registration form
        response = self.client.post(self.register_url, self.registration_data, follow=True)
        # Check for redirection (e.g., to the home page after successful registration)
        self.assertRedirects(response, '/')  # Assuming redirection to the home page '/'

        # Verify the user was created and can log in
        user = authenticate(username='newuser', password='Testpassword123')
        self.assertIsNotNone(user)
        self.assertTrue(user.is_authenticated)

        # Verify the Account object's creation and its details
        account = Account.objects.get(user=user)
        self.assertEqual(account.dateOfBirth, parse_date('2000-01-01'))  # Ensure date matches the expected format
        self.assertEqual(account.faveCheese, self.cheese)

    def testEmptyField(self):
        # recieve an empty username
        form_data =  form_data = {"username": "", "password": "testpassword", "email": "test@example.com", "first_name":"first", "last_name":"last" }
        request = self.client.post(reverse("CheeseBoardSite:register"), data = form_data)
        # decode it
        content = request.content.decode("utf-8")
        # confirm that response has an error
        self.assertTrue('<div class="error">' in content, "No error is being raised for fields left blank")

    def tearDown(self):
        # Cleanup any objects created
        User.objects.filter(username='newuser').delete()
        self.cheese.delete()  # Cleanup the test cheese object
