from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .test_base import UserTest, SuperuserTest


class LoginTest(TestCase):
    def test_login_on_404(self):
        """Test that we force the user to log in, even for non-existent URLs."""
        response = self.client.get('/i-dont-exist', follow=True)

        self.assertTemplateUsed(response, "users/login_picker.html")


class SuperuserOnlyTest(UserTest):
    """Check that a normal user can't access views intended for superusers."""
    def test_create_user(self):
        response = self.client.get(reverse('create_user'))
        self.assertTemplateUsed(response, "users/permission_denied.html")

    def test_edit_user(self):
        response = self.client.get(reverse('edit_user', args=[self.test_user.id]))
        self.assertTemplateUsed(response, "users/permission_denied.html")

    def test_delete_user(self):
        response = self.client.get(reverse('delete_user', args=[self.test_user.id]))
        self.assertTemplateUsed(response, "users/permission_denied.html")


class UserDeleteTest(SuperuserTest):
    def test_delete_user(self):
        user_to_delete = User.objects.create_user('delete_me', 'test@example.com', 'testpassword')
        
        self.client.post(reverse('delete_user', args=[user_to_delete.id]))
        
        self.assertFalse(User.objects.filter(id=user_to_delete.id).exists())

    def test_delete_nonexistent_user(self):
        nonexistent_user_id = 12345
        response = self.client.get(reverse('delete_user', args=[nonexistent_user_id]))
        
        self.assertTemplateUsed(response, "site_config/404.html")

class AllUsersTest(UserTest):
    def test_view_all_users(self):
        response = self.client.post(reverse('all_users'))
        self.assertEqual(response.status_code, 200)

