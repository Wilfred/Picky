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
        self.assertEqual(page.get_rendered_content().strip(), "<p>hello world</p>")
