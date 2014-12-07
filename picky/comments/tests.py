from django.core.urlresolvers import reverse

from picky.pages.test_mixins import PageTest
from picky.users.test_base import UserTest
from .models import Comment


class CreateCommentTest(UserTest, PageTest):
    def test_create(self):
        page = self.create_page()
        
        self.client.post(
            reverse('new_comment', args=[page.name_slug]),
            {'text': 'hello world'})

        # we should now have a comment associated with this page
        self.assertTrue(Comment.objects.filter(page=page))
