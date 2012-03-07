"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from milkman.dairy import milkman

from .models import Page


class RenderingTest(TestCase):
    def test_basic_rendering(self):
        page = milkman.deliver(Page, content="hello world")
        self.assertEqual(page.get_rendered_content().strip(), """<div class="document">
<p>hello world</p>
</div>""")

    def test_h1_rendered(self):
        page = milkman.deliver(Page, content="foo\n===")
        self.assertIn('<h1 class="title">foo</h1>', page.get_rendered_content())

    def test_h2_rendered(self):
        page = milkman.deliver(Page, content="bar\n===\n\nfoo\n---")
        self.assertIn('<h2 class="subtitle" id="foo">foo</h2>', page.get_rendered_content())
        
