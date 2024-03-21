import os
import re
import inspect
import tempfile
from CheeseBoardSite import models, forms
from populate_cheese import populate
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields

# Create your tests here.

class RegisterTests(TestCase):
    def testEmptyField(self):
        # recieve an empty username
        form_data =  form_data = {"username": "", "password": "testpassword", "email": "test@example.com", "first_name":"first", "last_name":"last" }
        request = self.client.post(reverse("CheeseBoardSite:register"), data = form_data)
        # decode it
        content = request.content.decode("utf-8")
        # confirm that response has an error
        self.assertTrue('<div class="error">' in content, "No error is being raised for fields left blank")

class ProfileTest(TestCase):
    def randomTest():
        return

class LoginTest(TestCase):
    def randomTest():
        return

# etc, change the classes to more specific tests e.g. class TestRegisterForm(TestCase)
