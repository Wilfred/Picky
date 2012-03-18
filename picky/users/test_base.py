from django.test import TestCase
from django.contrib.auth.models import User


class UserTest(TestCase):
    """Stub for testing views that require a normal user to be logged in."""
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.client.login(username="testuser", password="testpassword")

        
class SuperuserTest(TestCase):
    """Stub for testing views that require a superuser to be logged in."""
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.save()
        
        self.client.login(username="testuser", password="testpassword")
        
