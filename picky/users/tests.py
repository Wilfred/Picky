from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class LoginTest(TestCase):
    def test_login_on_404(self):
        """Test that we force the user to log in, even for non-existent URLs."""
        response = self.client.get('/i-dont-exist', follow=True)

        self.assertTemplateUsed(response, "users/login.html")

class SuperuserOnlyTest(TestCase):
    """Check that a normal user can't access views intended for superusers."""
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.client.login(username="testuser", password="testpassword")
    
    def test_create_user(self):
        response = self.client.get(reverse('create_user'))
        self.assertTemplateUsed(response, "users/permission_denied.html")

    def test_edit_user(self):
        response = self.client.get(reverse('edit_user', args=[self.test_user.id]))
        self.assertTemplateUsed(response, "users/permission_denied.html")

    def test_delete_user(self):
        response = self.client.get(reverse('delete_user', args=[self.test_user.id]))
        self.assertTemplateUsed(response, "users/permission_denied.html")

