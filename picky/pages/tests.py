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
        
