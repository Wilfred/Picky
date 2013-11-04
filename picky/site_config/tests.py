from django.core.urlresolvers import reverse

from users.test_base import UserTest


class SiteSettingsTest(UserTest):
    def test_settings(self):
        response = self.client.get(reverse('configure_site'))
        self.assertEqual(response.status_code, 200)
