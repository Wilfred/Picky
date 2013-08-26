from django.core.urlresolvers import reverse

from milkman.dairy import milkman

from pages.models import Page
from users.test_base import UserTest
from .models import Comment


class CreateCommentTest(UserTest):
    def test_create(self):
        page = milkman.deliver(Page)
        
        self.client.post(
            reverse('new_comment', args=[page.name_slug]),
            {'text': 'hello world'})

        # we should now have a comment associated with this page
        self.assertTrue(Comment.objects.filter(page=page))
