from django.test import TestCase
from django.core.urlresolvers import reverse

from milkman.dairy import milkman

from .models import Page
from users.test_base import UserTest


class RenderingTest(TestCase):
    def test_basic_rendering(self):
        page = milkman.deliver(Page, content="hello world")
        self.assertEqual(page.get_rendered_content().strip(), """<div class="document">
<p>hello world</p>
</div>""")

    def test_h1_rendered(self):
        page = milkman.deliver(Page, content="foo\n===")
        self.assertIn('<h1>foo</h1>', page.get_rendered_content())

    def test_h2_rendered(self):
        page = milkman.deliver(Page, content="""
bar
===

foo 1
-----

foo 2
-----

""")

        self.assertIn('<h2>foo 1</h2>', page.get_rendered_content())
        self.assertIn('<h2>foo 2</h2>', page.get_rendered_content())


class PageDeletingTest(UserTest):
    def test_page_delete(self):
        page = milkman.deliver(Page)

        self.client.post(reverse('delete_page', args=[page.id]))
        self.assertFalse(Page.objects.filter(id=page.id).exists())
        

class PageVersioningTest(UserTest):
    def test_page_edit(self):
        page = milkman.deliver(Page)

        page.title = 'new title'
        page.save()

        self.assertEqual(page.version, 2)
